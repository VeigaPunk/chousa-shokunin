# CritC1Detached — round 61 w1 — counter process handling (claims A1(2))

Scope: `corpus/evidence/round61/c1-count.py` `run()` and its leg verdicts. The frozen file was read only; its sha256 prefix `f1d8b6fde8dedd88` matched the claims' `f1d8b6fd…` when I copied it. I changed nothing under `corpus/`, `tools/` or `SKILL.md`. Adversarial builders, helpers and a prototype counter lived in scratch `/fast/scratch/hyaku/chousa-r61/CritC1Detached` (deleted before yield). No installs. No git mutation (read-only `merge-base`, `cat-file`, `status`).

## Verdict on A1(2)

A1(2) is a demonstrated forge, not hardening. Three routes flip a fail to a pass against the frozen counter:

1. **Post-exit mutation through a setsid grandchild (detached).** The builder forks a helper that calls `os.setsid()`, arms `PR_SET_PDEATHSIG`, and waits for the builder's death. The helper then acts before the counter snapshots. `run()` kills only the child's process group (`os.killpg(p.pid)`), so a new session escapes it.
   - P03 (`tools/__pycache__` removal) flips fail→pass in 3/3 seeds.
   - H10, H11, H12 (symlink-victim restore) flip fail→pass with a forced exit 2 plus a restore: H10 3/3, H11 3/3, H12 2/3.
2. **Survival into later legs (detached).** One run spawns a setsid poller that is still alive when later legs run. P03 passes 3/3 with the spawner in an earlier group.
3. **Not a survival route, but in the same wait4 design: unwaited RSS.** A child that is never waited for holds the 192 MiB read; `wait4` only sees the direct child. H14 and H15 flip fail→pass in 3/3 seeds each, with the child's memory unmeasured. This needs no helper to survive; it is a measurement hole, and the claim's "peak RSS" wording does not disclose it.

Routes 1–2 are the detached class the item asked about. Route 3 is a separate hole that A1(2) does not address.

## Findings and receipts

All runs: frozen counter, seeds 61001–61003, absolute `--work`/`--builder` paths. Each counter run takes about 3 s. Base reproduction on this host matches `controls/c1-before.txt`: seed 61001 gives `LEGS=7/20 C1=FAIL`, failing P03, H07–H17, H20.

| variant (scratch) | mechanism | result (seeds) | control |
|---|---|---|---|
| `f1_pyc_setsid` | builder spawns setsid helper; PDEATHSIG; `rmtree(tools/__pycache__)` | P03 pass 3/3 (LEGS 8/20) | `f1c_pyc_group` (same helper, same group): P03 fail 3/3 |
| `f2_rc2_restore_setsid` | forced rc 2 + setsid helper restores symlink victims (pre-state bytes and mtime) | H10 pass 3/3, H11 pass 3/3, H12 pass 2/3 | `f2c_rc2_only` (no restore): H10–H12 fail 3/3; `f2c_rc2_restore_group`: H10 1/3, H11 0/3, H12 0/3 |
| `f4s_daemon_once` | one run spawns a setsid poller (deletes `leg-*/tools/__pycache__`); flag file limits spawns to one | P03 pass 3/3, spawner in an earlier group | `f4c_daemon_group` (same poller, same group): P03 pass 3/3 (deleted during the run; the poller is dead before the check) |
| `f3_rss_unwaited` | fork child reads whole cache; parent sleeps 1 s and exits 1 without waiting | H14 pass 3/3 (rss 18.2–18.6 MB); H15 pass 3/3 (rss 18.5–18.7 MB) | `f3c_rss_waited`: H14 fail 3/3 (rss ~207.8 MB), H15 fail 3/3 |
| `f5_self_clean` | builder removes its own `__pycache__` via `atexit`; no child | P03 pass 3/3 | — |

Probe receipts for route 3: the unwaited child wrote `bytes=201326592 VmHWM_kB≈206000–207000` (its own `/proc/self/status`) before the parent exited. The counter reported `rss_kib≈18000` for the same leg.

Details that matter for the verdict:
- The H14/H15 pass in route 3 comes from the RSS threshold alone: the builder exits 1, the tree is clean, and no process was waited for.
- The P03 window is wide: `tools_unchanged()` runs after the snapshot and the golden build, so the helper has milliseconds (INFERENCE from the leg order; not timed). The H10–H12 window is narrow (snapshot immediately after `run()` returns), and the restore still won 8 of 9 setsid trials.
- The group-restore control (`f2c_rc2_restore_group`, 1/9) shows the in-group race is real but mostly lost. The setsid route is the reliable one.
- Route 2 is verified by spawn order, computed with the counter's own seeded shuffle (`random.Random(seed*7919+1).shuffle`). Seed 61003: first group is H10 (plan index 7), P03 group at position 3. Seed 61002: first group is H11 (index 8), P03 at position 15. Seed 61001: first group is H14 (index 11), P03 at position 13. The poller spawns once (`once.flag`; `daemons_spawned_in_run=1`).
- The counter docstring says "its own process group (killed when the run ends, so no detached helper outlives its leg)". Under setsid that sentence is false, and the tested results show it.
- The admission sweep regex (`getppid|/proc/|c1-count|round61|leg-|argv\[0\]`) does not match `fork`, `setsid`, `prctl`, `unshare` or `wait4`. The sweep therefore does not catch any of these routes (read from claims.md; not run).
- P03 is satisfiable by the builder alone (`f5_self_clean`, 3/3). That leg measures a side effect the builder can undo in-process; it is not evidence of process isolation. Only a tree or RSS check isolated from the builder's descendants can be trusted to measure builder behaviour.

## Proposal (smallest change; NOT applied)

I prototyped three variants on a scratch copy of the counter, in a scratch tree laid out so the copy's `LANE` resolves to scratch. Lane files are untouched. The honest control was `controls/ref-build-spans.py` (sha `86d64c31…`, copied to scratch).

- **(a) Subreaper:** `prctl(PR_SET_CHILD_SUBREAPER)` in the counter; after `wait4`, SIGKILL and reap every orphan; take the max `ru_maxrss` across all reaped processes (about 35 lines).
  - Reference 20/20 (`prop-ref-61001`).
  - Closes route 3: H14 and H15 fail (rss 207.9 MB, 208.1 MB).
  - Closes route 2: `f4s_daemon_once` seed 61002 gives P03 fail.
  - Does **not** close route 1: `f1_pyc_setsid` seed 61001 P03 pass; `f2_rc2_restore_setsid` seeds 61001/61002 H10–H12 pass.
- **(b) PID namespace:** run the builder as PID 1 of a fresh namespace: `argv = ["unshare","-Ufp","--fork","--kill-child", sys.executable, builder, ...]`. One argv line changed in `run()`.
  - Reference 20/20, including H17 (`ns-ref-61001`).
  - Closes route 1: `f1_pyc_setsid` seeds 61001 and 61002 give P03 fail; `f2_rc2_restore_setsid` seed 61001 gives H10, H11, H12 fail.
  - Closes route 2: `f4s_daemon_once` seed 61002 gives P03 fail.
  - Does **not** close route 3: H14 and H15 pass (rss 16.9 MB and 18.7 MB) because the unwaited child is torn down without being reaped by the counter.
- **(c) Shim as namespace init:** the builder runs under a small reaper shim that kills and reaps all namespace processes after the builder exits.
  - Reference 20/20 (`shim-ref-61001`).
  - Closes routes 2 and 3.
  - Does **not** close route 1: P03 pass 2/2, H11 pass once. The shim acts only after the builder's death is observed, so a PDEATHSIG helper wins that race.
  - Conclusion: closing route 1 needs the kernel to tear the namespace down at the moment its init exits, which (b) does and (c) cannot. (INFERENCE from these results; kernel source not checked.)

**Recommended minimal change:** (b), the one-line `unshare -Ufp --fork --kill-child` prefix. It needs unprivileged user namespaces, which this host has (`unprivileged_userns_clone=1`, `max_user_namespaces=122865`); the counter should fail closed if `unshare` is absent. (b) does not fix route 3. Options for route 3: measure the namespace's memory with a cgroup v2 `memory.peak` (UNTESTED here), or narrow H14/H15's claim to "the direct child's peak RSS" and say so in the frozen text. Either is a claim or freeze change, which is the L1's call; I did not apply or propose a predicate change.

## Limits

- Three seeds per variant; the (b) and (c) follow-ups ran on the seeds listed above only. Route 1 under (b) is 2 seeds; H10–H12 under (b) is 1 seed.
- Route 2's "later-leg" evidence depends on spawn order, computed with the counter's seeded shuffle formula.
- I did not test the 60 s timeout path under (b). A helper that arms PDEATHSIG after its parent has already exited would wait forever and do nothing; that is a race in my helper, not a flip, and I did not measure it.
- The H10–H12 flip uses a forced exit 2. Without the restore it fails (control), so both ingredients are needed; a builder can supply both.
- I did not test a builder whose post-exit helper writes the golden tree. That would probably flip more legs, but I have not verified it.

## Other observations (not verdict-affecting)

- My first counter run used a relative `--work`. Builder calls then failed with ENOENT (rc 2; `counter exception` on P04), and the counter printed `C1=FAIL` without naming the cause. The counter resolves `--builder` but not `--work`. Operability note only.
- Lane `git rev-parse HEAD` is `9f32ac05…`, not `2b0e17b2…`. `2b0e17b2` is an ancestor of HEAD (`merge-base --is-ancestor`, exit 0), so the freeze is intact.
- `git status` shows untracked files beside the frozen directory: `corpus/evidence/round61/controls/run-sniff-controls.py`, `corpus/evidence/round61/extras.py`, `corpus/evidence/round61/sniff-sweep.py`. They are not frozen; I did not read them.

## Commands run (abbreviated)

- `python3 -B …/c1-count.py --builder $S/b/base.py --work $S/runs/base-61001 --seed 61001` → `LEGS=7/20 C1=FAIL`, same failing legs as `c1-before.txt`.
- `python3 -B …/c1-count.py --builder $S/v/<variant>.py --work $S/runs/<variant>-<seed> --seed <seed>` for the variants above, seeds 61001–61003 (`f2_rc2_restore_setsid` and `f4s_daemon_once` also at 61002; `f2c_*` at 61001–61003).
- Proposal: scratch copy of the counter with `subreaper()`, `reap_descendants()` and the `unshare` prefix (`proposal/shim.py` for (c)); seeds 61001/61002 as listed.
- `unshare -Ufp --fork true` → exit 0.
- `sha256sum …/c1-count.py` → `f1d8b6fde8dedd8894dfbb31…` (matches claims).
- `git merge-base --is-ancestor 2b0e17b2… HEAD` → exit 0.

Scratch removed: `rm -rf /fast/scratch/hyaku/chousa-r61/CritC1Detached` (other seats' directories left untouched). A `/proc` scan after the runs found no stragglers (0 killed).

VERDICT: DETACHED_FLIP_POSSIBLE=yes legs=P03,H10,H11,H12
