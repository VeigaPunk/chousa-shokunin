# R53ExecSeedRuns — flake & independence check of the frozen C1 counter

Seat: `R53ExecSeedRuns` (leaf). Lane repo `$L=/home/vgpnk/Projects/shokunin/chousa-shokunin`; scratch
`$S=/fast/scratch/hyaku/chousa-r53/R53ExecSeedRuns` (exported as `TMPDIR`, cwd for every run, removed at
finish; every receipt cited below is pasted into this report before that removal). No production file,
counter, index or jj state touched; this report is my only write. **No install
performed** — `python3` 3.14.8, `/usr/bin/strace`, `git` were already present; no package manager, `uv`,
`npx` or binary was invoked.

## 0. Subject identity and frozen inputs

```
$ cd $L && git log --oneline -6
6365f15 round-53: wave-1 spec and dispatch (49 seats)
32aab5e round-53: C1 candidate — adopter v4 twin label, recheck pre-pass, registry-first refusal; self-test cases
a6ff732 round-53: freeze claims C1 (adopter twin/order) and C2 (search-record instruments) with counters, controls …
$ git show 32aab5e:tools/assimilate-rows.py | sha256sum ; sha256sum tools/assimilate-rows.py
32628bbc33d1d293e789b7d8f44cd769996e56678c40fd5f3943b50b8d8ed636  -      # candidate blob
32628bbc33d1d293e789b7d8f44cd769996e56678c40fd5f3943b50b8d8ed636  tools/assimilate-rows.py
$ git diff 32aab5e -- tools/assimilate-rows.py   # empty -> measured the candidate exactly
$ git diff --stat -- corpus/evidence/round53/    # empty -> counter at commit, unmodified
```

`claims.md` (frozen at `a6ff732`) was read first; no predicate, target, counter or control was questioned,
and nothing was patched. Driver script (the ≤60-line script asked for; ran with `TMPDIR=$S`, cwd `$S`):

```python
# $S/drive.py — 20 unseeded + 20 seeded + 5 per-leg-10, tabulating LEGS/C1 per run
import subprocess, os, pathlib, time
S = pathlib.Path("/fast/scratch/hyaku/chousa-r53/R53ExecSeedRuns"); RUNS = S/"runs"; RUNS.mkdir(exist_ok=True)
CTR = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round53/c1-count.py"
env = dict(os.environ); env["TMPDIR"] = str(S)
def go(tag, extra=()):
    before = len(list(S.iterdir())); t0 = time.time()
    r = subprocess.run(["python3", CTR, *extra], capture_output=True, text=True, env=env, cwd=str(S))
    dt = time.time() - t0; after = len(list(S.iterdir()))
    (RUNS/f"{tag}.log").write_text(f"RC={r.returncode}\n"+r.stdout+r.stderr, encoding="utf-8")
    g = lambda p: ([l for l in r.stdout.splitlines() if l.startswith(p)] or ["MISSING"])[-1]
    return dict(tag=tag, rc=r.returncode, legs=g("LEGS="), c1=g("C1="), seed=g("SEED="), dt=round(dt,2),
                before=before, after=after, fails=[l for l in r.stdout.splitlines() if "FAIL" in l])
rows = [go(f"un.{i:02d}") for i in range(1, 21)]
rows += [go(f"seed{n:02d}", ("--seed", str(n))) for n in range(1, 21)]
rows += [go(f"pl10.{i}", ("--per-leg", "10")) for i in range(1, 6)]
for r in rows:
    print(f"{r['tag']:<9} {r['legs']:<8} {r['c1']:<8} rc={r['rc']} {r['seed']:<12} tmp:{r['before']}->{r['after']} {r['dt']}s {r['fails'] or ''}")
print("NOT-8/8:", [r["tag"] for r in rows if r["legs"] != "LEGS=8/8" or r["c1"] != "C1=PASS" or r["rc"] != 0])
```

## 1. Required matrix — 45/45 runs `LEGS=8/8 C1=PASS` rc=0 (per-run table, 5 per line)

```
un.01 8/8 PASS | un.02 8/8 PASS | un.03 8/8 PASS | un.04 8/8 PASS | un.05 8/8 PASS
un.06 8/8 PASS | un.07 8/8 PASS | un.08 8/8 PASS | un.09 8/8 PASS | un.10 8/8 PASS
un.11 8/8 PASS | un.12 8/8 PASS | un.13 8/8 PASS | un.14 8/8 PASS | un.15 8/8 PASS
un.16 8/8 PASS | un.17 8/8 PASS | un.18 8/8 PASS | un.19 8/8 PASS | un.20 8/8 PASS
seed01..seed05 8/8 PASS | seed06..seed10 8/8 PASS | seed11..seed15 8/8 PASS | seed16..seed20 8/8 PASS
  (seeded block verbose form: "seed01 LEGS=8/8 C1=PASS rc=0 SEED=1 tmp:1->1 1.31s" .. "seed20 … SEED=20 … 1.28s")
pl10.1 8/8 PASS 3.09s | pl10.2 8/8 PASS 3.18s | pl10.3 8/8 PASS 3.06s | pl10.4 8/8 PASS 2.98s | pl10.5 8/8 PASS 3.00s
NOT-8/8: []          # raw per-run stdout: $S/runs/*.log ; table: $S/table.json
```

Every run's own leg lines were `TWIN=HELD=MIX=RECHECK=ORDER=NOENTRY=REAL=REGRESS=PASS`, e.g. from
`$S/runs/un.01.log`: `REAL PASS rc=0 map=ok rows=5 count-line=['CITED=6 APPEND=5 HELD=0 TWIN=1']` /
`REGRESS PASS r50-pin=ok r51-counter=LEGS=5/5` / `LEGS=8/8` / `C1=PASS`. Unseeded timing 1.26–1.54 s,
`--per-leg 10` 2.98–3.18 s, and `TMPDIR` entry count was 1→1 in every run (the 1 is my `runs/` dir).
**No run in the required matrix deviated, so there is no required-run defect output to paste.**
Generated packages exercised: 40 default runs × 6 legs × 3 + 5 × 6 × 10 = 1,020, plus the extras below.

## 2. Wider seed sweep (extra falsifier, same counter, no edit) — 140/140

```
seeds 21..160 run: 140 failures: 0
sweep-tmp leftovers: 0
```

Seeded coverage 1..160 plus 20 independent unseeded runs: no seed produced ≠8/8.

## 3. Independence and determinism

```
$ python3 $CTR --seed 7 --work $S/w7a ; --seed 7 --work $S/w7b ; --seed 8 --work $S/w8
w7a rc=0  w7b rc=0  w8 rc=0
seeded text determinism (7 vs 7): IDENTICAL_TEXT       package trees 7 vs 7: IDENTICAL_TREES (189 files each)
package trees 7 vs 8: DIFFERENT_TREES (w8 193 files)   unseeded --work trees u1 vs u2: UNSEEDED_DIFFERENT
cwd independence (run from /): LEGS=8/8 C1=PASS        per-leg 1 x2: 8/8, 8/8 ; --seed 7 --per-leg 10: 8/8
PYTHONHASHSEED=random and =0: 8/8, 8/8                 discrimination sanity --tool /bin/true: LEGS=0/8 C1=FAIL
```

Same seed ⇒ byte-identical package trees and identical stdout; unseeded ⇒ different packages; the pass is
not vacuous (`/bin/true` scores 0/8). The counter never reads the lane worktree registry
(`grep -c 'chousa-shokunin/corpus/SOURCES.md"' $S/strace2.log` → `0`), so lane edits cannot move it.

## 4. Scratch hygiene (counter deletes its own scratch)

```
$ ls -A $S/tmpcheck | wc -l          # 0 before
$ TMPDIR=$S/tmpcheck python3 $CTR    # rc=0, LEGS=8/8 C1=PASS ; ls -A $S/tmpcheck | wc -l -> 0 after
isolated TMPDIR t2, 3 further runs: run1 rc=0 entries=0 | run2 rc=0 entries=0 | run3 rc=0 entries=0
3 concurrent runs sharing one TMPDIR: run1/2/3 rc=0, each LEGS=8/8 C1=PASS, leftovers in conc: 0
$ ls -A $S   # after everything (all mine, no counter residue): cites-env.txt conc conc.1.txt conc.2.txt
#  conc.3.txt git-after.txt git-before.txt gitdir.txt r51t repro-cites-seed7.txt runs strace-net.log
#  strace.log strace.out strace2.log strace2.out sweep sweep-tmp t2 t2.out table.json tmpcheck
#  tmpcheck.out u1 u1.txt u2 u2.txt w7a w7a.txt w7b w7b.txt w8 w8.txt
```

`--work DIR` leaves the generated packages by design (`own = a.work is None`); with no `--work` the
`tempfile.mkdtemp` tree is removed in `finally` — confirmed above, including under concurrency.

## 5. Write confinement — `strace -f -y` over a full run

```
$ TMPDIR=$S strace -f -y -e trace=openat,creat,mkdir,mkdirat,rename,renameat,renameat2,unlink,unlinkat \
      -o $S/strace2.log python3 $CTR        # rc=0, LEGS=8/8 C1=PASS
strace2.log: 8337 lines; write-mode path ops: 1221; read opens: 7043
=== writes outside scratch: 1
  openat    /dev/null   :: AT_FDCWD<$S>, "/dev/null",
=== write ops touching lane: 0        === write-mode opens under lane/.git: 0
=== lane write-mode opens total: 0    === campaign write-mode (/home/vgpnk/Projects/shokuknow): 0
```

Only `/dev/null` (a child's redirect sink). No write in `$L`, its `.git`, the read-only campaign package,
the fleet repo or `/tmp`. Network: `strace -f -e trace=connect,socket` over a full run printed
`LEGS=8/8 C1=PASS` with `inet sockets: 0`.

## 6. `git show` in leg REAL is read-only

```
$ sha256sum $L/.git/index $L/.git/HEAD > git-before.txt ; ls $L/.git | grep -E 'lock|MERGE|CHERRY' -> no lock files before
$ python3 $CTR | tail -2  ->  LEGS=8/8 / C1=PASS
$ sha256sum ... > git-after.txt ; diff git-before.txt git-after.txt -> INDEX_HEAD_UNCHANGED ; no lock files after
.git reads by the counter's git child: .git/HEAD, .git/config x3, .git/shallow, .git/packed-refs, .git/refs/,
  .git/objects/a4/534a841b6c924089e629391b7def37ee5f6a53 x2        (read opens only; 0 write-mode ops)
```

REAL's four on-disk inputs open `O_RDONLY|O_CLOEXEC`: `merge/chousa/SOURCES.append.md` and the three campaign
entries (`search-tracking-record-r40.md`, `western-instrument-alignment-r50.md`,
`quality-control-guideline-issued-text-r48.md`); the registry it continues from is the `git show
BASE_REV:corpus/SOURCES.md` blob, reproducing the frozen `HELD=0 TWIN=1` line on every one of 185+ runs.

## 7. Findings (reported, not patched)

**F1 — ambient `ASSIMILATE_CITES` is not inherited-hermetic: REGRESS fails, 7/8.** The generated legs strip
it (`run()` does `e.pop("ASSIMILATE_CITES", None)`, c1-count.py:77), but `leg_regress` hands the round-51
counter the raw `os.environ`, and `tools/assimilate-rows.py:390,395` reads that variable as the default for
`--cites`. Reproduced with a seed as asked (output below elides only the 18 generated-leg case lines, all
`PASS` notes; full text in `$S/repro-cites-seed7.txt`):

```
$ ASSIMILATE_CITES=all python3 $CTR --seed 7      # rc=1 ; case lines 1-18 all PASS
SEED=7
REAL PASS rc=0 map=ok rows=5 count-line=['CITED=6 APPEND=5 HELD=0 TWIN=1']
REGRESS FAIL r50-pin=ok r51-counter=FAIL rc=1
TWIN=PASS HELD=PASS MIX=PASS RECHECK=PASS ORDER=PASS NOENTRY=PASS REAL=PASS REGRESS=FAIL
LEGS=7/8
C1=FAIL
$ ASSIMILATE_CITES=all python3 $L/corpus/evidence/round51/c1-count.py --tool $L/tools/assimilate-rows.py --seed 53
SOURCE_ONLY=FAIL default_rc=0 map=['S610','S733','S757'] appended=2 bodyonly=[] all_rc=0 all_map=['S610','S733','S757']
LEGS=4/5
$ (same command, variable unset)  LEGS=5/5
```

Scope: **not** a failure of the frozen C1 target — the frozen runs are three unseeded runs and `--seed 7` in
an ordinary environment, and all 160 seeded + 20 unseeded ordinary runs are 8/8. It is a
measurement-hygiene hazard: a shell exporting `ASSIMILATE_CITES=all` would report `C1=FAIL`. Routed to the
L1: measure with that variable unset (popping it in `leg_regress` as well is the L1's call, not mine).

**F2 — ambient `GIT_DIR` makes REAL unreportable (exit 2, by design).** `leg_real` shells `git -C $L show`,
and a stray `GIT_DIR` overrides `-C`:

```
$ GIT_DIR=/nonexistent python3 $CTR ; echo rc=$?
ENV git show failed
rc=2
```

The counter degrades into its documented `ENV` path instead of a false PASS/FAIL — correct, but since
`ENV_CHANGED` exit 2 means C1 fails, the measuring shell must export no `GIT_DIR` / `GIT_WORK_TREE` /
`GIT_OBJECT_DIRECTORY`. Recorded as an operator precondition. No other flake source was found: locale/hash
seed, cwd, concurrency, TMPDIR reuse and per-leg size are all clean.

## 8. Risks / blockers

- No blocker. Nothing needs to change in the lane for C1 to hold on the candidate.
- Residual risk: a pass over 1,020+ generated packages is not a proof; only the representations the
  generator emits (0–3 leading spaces, space/tab heading, http|https, trailing `/`, upper-case host) are
  exercised. Untouched branches: `ENV_CHANGED` on a drifted campaign pin (needs mutating the read-only
  package — not done), and `--work` reuse of a non-empty directory.
- F1 and F2 are the only sensitivity findings and both sit outside the frozen predicate.

VERDICT: attacked the candidate `tools/assimilate-rows.py` (`32628bbc…d636`) through the frozen C1 counter —
45/45 required runs (20 unseeded, 20 seeded 1–20, 5 × `--per-leg 10`) and 140 extra seeds all `LEGS=8/8
C1=PASS` rc=0, seeded runs byte-reproducible, scratch self-cleaning, zero writes outside `$TMPDIR`/`--work`
except `/dev/null`, no inet sockets, `git show` index/HEAD unchanged — surviving; the only defects found are
ambient-env sensitivities (F1 `ASSIMILATE_CITES` ⇒ 7/8; F2 `GIT_DIR` ⇒ ENV exit 2), reported for the L1, not
patched.
