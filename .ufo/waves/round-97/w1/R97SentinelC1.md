# R97SentinelC1 — side-effect audit (round 97, C1 and C2 instruments)

Attacked tree: F `9a0ce2015fa0254848f2f32f612b20caf7dc5478`, cloned with `git clone -q --shared` into scratch and checked
out at F (`git -C "$R" rev-parse HEAD` = F; `git -C "$R" status --porcelain` empty). The lane itself was never run
against: every command ran on my clone, and every git call named `-C` my clone or a fixture whose toplevel I asserted.

Tools: `strace` 7.2 at `/usr/bin/strace` (pre-installed; **nothing installed, upgraded or removed by this seat**),
git 2.56.0, Python 3.14.8. No pacman, sudo, network, sysctl or service change. Scratch
`/fast/scratch/hyaku/chousa-r97/R97SentinelC1`, removed before yield; no `/tmp` use (`tmp_paths=0` in every trace).

## Method

- Every run under `strace -f -qq -e trace=file,network,process`.
- `R97SentinelC1-attrib.py` resolves every write-mode `open`/`openat` (successful only) and every mutating syscall
  (unlink, rename, mkdir, rmdir, symlink, link, chmod, utimensat, …) to an absolute path, tracking per-pid cwd (from
  `chdir`, inherited on `clone`/`vfork`) and per-pid dirfd tables. Relative writes such as git's `.git/logs/HEAD` are
  therefore attributed to where they landed. Categories: `LANE`, `REPO(my clone)`, `WORK(scratch)`, `DEV`, `OTHER`,
  `UNRESOLVED`. `LANE` and `OTHER` must be zero.
- Four traces: selftest (st), C1 battery `--no-regression` (c1), entry-controls (entry), C1 battery with the r95
  regression legs (full, 28,627,970 lines).

## (1) `python3 -B tools/search-rerun.py --selftest` under strace

- Exit 0; last stdout line `SEARCH_RERUN_SELFTEST: PASS cases=47/47` (`R97SentinelC1-selftest-stdout.txt`); stderr 0 bytes.
- Trace 534 lines: write-mode opens 0; mutating syscalls 0; socket/connect/sendto/getaddrinfo 0; `/tmp` 0;
  successful execs: `/usr/bin/python3` ×1 and nothing else; no git. Attribution: all categories 0, `UNRESOLVED {}`.
  Receipts: `R97SentinelC1-selftest-strace-summary.txt`, `R97SentinelC1-st-strace-write-attribution.txt`.
- This closes named limit (e) of C1 for the self-test: it makes no system-call writes at all, not only none into the
  empty directory.

## (2) Does the r13 `os.environ` mutation leak?

Harness `R97SentinelC1-harness-r13.py` imports the tool in-process, plants caller `GIT_*` values (dirty mode:
`GIT_DIR=/caller/own/gitdir`, `GIT_NO_REPLACE_OBJECTS=7`, `GIT_TERMINAL_PROMPT=1`, `GIT_CONFIG_PARAMETERS`), runs
`selftest()`, and compares the Python `os.environ` and the C-level environment (`/usr/bin/env -0`) before and after.

- `MODE=dirty rc=0 last='SEARCH_RERUN_SELFTEST: PASS cases=47/47'`, `PY_ENV_DIFF {}`, `C_ENV_SAME True vars_before 277 vars_after 277`, harness exit 0.
- `MODE=clean rc=0 …`, `PY_ENV_DIFF {}`, `C_ENV_SAME True vars_before 270 vars_after 270`, harness exit 0.
- Receipts: `R97SentinelC1-r13-harness-output.txt`. **Held**: the `finally` restore works in both states.

## (3) C1 battery, `--no-regression`, under strace

Command `python3 -B corpus/evidence/round97/selftest-controls-r97.py --root . --work $S/work-c1 --no-regression` (cwd = clone), exit 0.
stdout last line `SELFTEST_CONTROLS_R97=PASS`, tally line `POSITIVE=1/1 EXTERNAL_KILLED=30/30 DO_NOTHING_REFUSED=1/1 R96_MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1 BASE_KILLED=10/30 CASES=47`; stderr 0 bytes.
Receipts: `R97SentinelC1-c1-battery-stdout.txt`, `-stderr.txt`, `-strace-summary.txt`, `-write-attribution.txt`.

- Trace 1,072,243 lines. Attribution: `DEV write-open=28` (`/dev/null`), `WORK(scratch)` 282 write-opens + 289 `unlinkat` + 11 `mkdir` + 4 `rmdir`,
  `REPO(my clone)` 8 write-opens + 8 unlinks (the `index.lock` pairs, below), **`LANE` 0, `OTHER` 0, `UNRESOLVED` 0**.
- Execs: `/usr/bin/python3` 291, `/usr/bin/git` 28. Git subcommands on the execs: `show` 12, `status` 8, `diff` 8.
  **Mutating git subcommands 0.** Sockets 0.
- Clone `.git/index` before and after: mtime `2026-11-08 23:15:39.268063721 -0300` and size `3390247` both times;
  sha256 `a5a9a737…0dd0a5832` both times (`R97SentinelC1-clone-index-before-after.txt`). `git status --porcelain`
  before and after: identical, empty (`…-c1-clone-status-before.txt`, `…-after.txt`).
- **Finding F1 (below):** `lane_state()` → `git status --porcelain` creates and removes `.git/index.lock` on each call
  (`O_RDWR|O_CREAT|O_EXCL` then `unlink`): 8 pairs in this run (`R97SentinelC1-c1-index-lock-lines.txt`, 16 lines).
  No rename onto `.git/index` occurred, so the index content and mtime are unchanged.
- **Full run with the r95 legs:** `python3 -B … selftest-controls-r97.py --root . --work $S/work-full` (no `--no-regression`), exit 0
  (`R97SentinelC1-full-battery-exit.txt` = `full_battery_exit=0`), `SELFTEST_CONTROLS_R97=PASS`, `REGRESSION_R95=2/2`,
  `regression-rerun-controls-r95 rc=0 ok`, `regression-mutants-r95 rc=0 ok`, stderr 0 bytes. Trace 28,627,970 lines.
  Attribution (`R97SentinelC1-full-write-attribution.txt`): `LANE 0`, `OTHER 0`, `UNRESOLVED 0`, `chdir` into the lane 0,
  lane-path write-opens 0, lane-path mutating syscalls 0, lane index mentions 0, sockets 0, `/tmp` 0.
  The 275 mutating git execs (`init` 55, `add` 55, `commit` 55, `clone` 55, `checkout` 55) all resolve under
  `work-full` (fixtures and `--shared` clones created by the r95 legs); the `WORK(scratch)` category carries them.
  Receipts: `R97SentinelC1-full-battery-strace-summary.txt`, `-stdout.txt`, `-stderr.txt`, `-clone-status-before/after.txt`.

## (4) `entry-controls-r97.py` under strace

Command `python3 -B corpus/evidence/round97/entry-controls-r97.py --root . --work $S/work-entry` (cwd = clone), exit 0;
last line `ENTRY_CONTROLS=PASS`; tally `… GATE_RECORDS=30/30 LQ_BOUND=29/29 … VERBATIM=10/26 LETTERS=14/26 METADATA=clean`.
Receipts: `R97SentinelC1-entry-controls-stdout.txt`, `-stderr.txt` (0 bytes), `-entry-strace-summary.txt`, `-entry-strace-write-attribution.txt`.

- Trace 110,907 lines. Attribution: `WORK(scratch)` 21 write-opens, 22 `unlinkat`, 3 `mkdir`, 2 `rmdir`, all inside `work-entry`;
  `DEV` 662 (`/dev/null` subprocess stdio); **`LANE` 0, `OTHER` 0, `UNRESOLVED` 0**.
- Four `openat("/dev/tty", O_RDWR|O_NONBLOCK) = -1 ENXIO` attempts: each follows a `libncursesw.so.6` load in a child process (the child was not identified); they fail, so they are not file writes and the attribution excludes them.
- Git subcommands: `cat-file` 542, `rev-parse` 6, `ls-tree` 6; **mutating 0**. Sockets 0. `/tmp` 0.
- `mktemp --version` ×2 is research-gate's pin probe; no directory was created by it.
- `gate-records.py` and `research-gate.sh verify-metadata` wrote nothing outside `work-entry`, touched no network.

## Lane state

- My four traces contain zero references to the lane `.git/index` (`R97SentinelC1-lane-index-mentions-per-trace.txt`).
- The lane `.git/index` mtime read `23:19:51` and later `23:36:43` (`R97SentinelC1-lane-index-stat.txt` at seat end, read-only
  `stat`; `index.lock` absent). I did not record a stat before my first run, so I cannot state the pre-run value. The
  change is not from my processes, which never opened that path; it is most likely sibling git activity in the lane
  [INFERENCE].

## Findings

**F1 — C1 battery docstring "Read-only on the lane" is literally false (low).** `corpus/evidence/round97/selftest-controls-r97.py:39`:
"Writes only under --work (removed at exit). Read-only on the lane (`git show`, `git status`, `git diff`)."
`git status --porcelain` takes and releases `.git/index.lock` on every call: 8 `O_CREAT|O_EXCL` opens and 8 `unlink`s in the
no-regression trace (`R97SentinelC1-c1-index-lock-lines.txt`). Functional harm was not observed:
`R97SentinelC1-index-lock-probe.txt` (fixture repo, asserted toplevel) shows `git status --porcelain` returns `rc=0` with
correct output while a foreign `.git/index.lock` is held, and `git --no-optional-locks status --porcelain` also returns `rc=0`
without creating a lock. A held lock could still make a sibling's concurrent `git add`/`commit` fail [INFERENCE — not run
against the lane]. Smallest fix: `git --no-optional-locks -C <root> status --porcelain` in `lane_state()`, and correct the docstring.

**F2 — mutant and oracle runs inherit the working directory of the battery, which is the lane root (low–moderate, latent).**
`selftest(tool)` (battery lines 66–67) calls `run([...])` with `cwd=None`, and `killed()` → `selftest(tool_path)` also passes no
cwd. Only the `NO_WRITE` run sets `cwd=empty`. Demonstrated with the battery's own `killed()` loaded by `importlib` and run from the
clone: `killed('leakmut.py')` → `(True, 1, '-')` — counted KILLED — while the fixture (a self-test that writes `leak-r97.txt`
relative to cwd and fails) left `?? leak-r97.txt` in the tree (`R97SentinelC1-leaking-mutant-killed.txt`; `git -C "$R" status --porcelain`
rc 0). The fixture file was removed afterwards (`clean_rc=0`). Consequences: a mutant that writes relative to cwd is scored as killed
and litters the lane root; the docstring's "Writes only under --work" is false for mutant runs. No real mutant leaked in these traces
(attribution `REPO(my clone)` shows only the index.lock pairs). Smallest fix: pass `cwd=<empty scratch dir>` (and HOME/TMPDIR) to every
`selftest()` call, and assert `lane_state` unchanged after each scored run.

**F3 — the `NO_WRITE` digest is blind to git-ignored paths (low, latent).** `NO_WRITE` compares `git status --porcelain` and `git diff`.
In a fixture with `.gitignore` = `__pycache__/` and `*.pyc` (the clone's `.gitignore` also lists `tools/__pycache__/`,
`R97SentinelC1-ignore-blind-probe.txt`), an ignored write `tools/__pycache__/w.cpython-314.pyc` does not appear in
`git status --porcelain` (rc 0); only `?? new-untracked.txt` does. It appears only under `--ignored` (`!! tools/`, rc 0). The
claim's named limit (e) names "system calls" and "the status and diff digest", not ignored paths. Latent: the self-test writes
nothing today (trace above) and the battery runs it with `-B`. Smallest fix: `git status --porcelain --ignored` in `lane_state()`.

## Held (no fire)

- Self-test: zero writes, zero exec beyond python, zero sockets, zero `/tmp` (1).
- r13 `os.environ` / C `environ` restore: no leak in either mode (2).
- C1 battery: writes only under `--work`, plus the transient `index.lock` of F1; no network; no `/tmp`; no mutating git in the
  `--no-regression` run; in the full run the only mutating git ran in fixtures under `--work` (3).
- Entry controls: writes only under `--work`; no network; read-only git only (4).
- Mutating git in the full run is a pre-existing r95 leg, not part of the r97 instruments, and is confined to `--work`.

## Receipts (all in this directory, prefix `R97SentinelC1-`)

selftest-stdout.txt, selftest-strace-summary.txt, st-strace-write-attribution.txt; c1-battery-stdout.txt, c1-battery-stderr.txt,
c1-battery-strace-summary.txt, c1-battery-write-attribution.txt, c1-index-lock-lines.txt, clone-index-before-after.txt,
c1-clone-status-before.txt, c1-clone-status-after.txt; full-battery-stdout.txt, full-battery-stderr.txt, full-battery-exit.txt,
full-battery-strace-summary.txt, full-write-attribution.txt, full-clone-status-before.txt, full-clone-status-after.txt;
entry-controls-stdout.txt, entry-controls-stderr.txt, entry-strace-summary.txt, entry-strace-write-attribution.txt;
r13-harness-r13.py (script), r13-harness-output.txt; index-lock-probe.sh, index-lock-probe.txt; ignore-blind-probe.sh,
ignore-blind-probe.txt; leakmut-fixture.py, leaking-mutant-killed.txt; lane-index-stat.txt, lane-index-mentions-per-trace.txt;
attrib.py (attribution script), receipts.sh, full-run.sh (drivers).

Raw strace traces (115 MB c1, 173 MB+ full) are not copied; their derived summaries and attribution outputs are. Raw traces were
deleted with the scratch tree before yield.

## Reproduce

```
R=<clone at F>; cd "$R"
strace -f -qq -e trace=file,network,process -o T python3 -B tools/search-rerun.py --selftest
strace -f -qq -e trace=file,network,process -o T python3 -B corpus/evidence/round97/selftest-controls-r97.py --root . --work W --no-regression
python3 -B R97SentinelC1-attrib.py T    # LANE 0, OTHER 0, UNRESOLVED 0 is the pass condition
```

VERDICT: R97SentinelC1 C1 held — the frozen sentence holds at F: the self-test makes no write, exec, socket or environment leak, and the no-regression battery leaves the clone's status and diff unchanged; but the battery's own wording fired (F1 "Read-only on the lane" with per-call index.lock; F2 mutant runs inherit the lane as cwd and a leaking mutant is counted killed; F3 NO_WRITE blind to ignored paths).
VERDICT: R97SentinelC1 C2 held — entry-controls-r97.py reaches ENTRY_CONTROLS=PASS with zero writes outside --work, no network, and read-only git only (cat-file, rev-parse, ls-tree); this seat audited side effects, not the entry's content.
