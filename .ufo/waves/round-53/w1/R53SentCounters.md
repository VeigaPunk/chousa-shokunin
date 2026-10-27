# R53SentCounters — hazard review: round-53 counters and adopter v4

Seat R53SentCounters (godspeed), 2026-10-26. Scope: write paths, scratch/TMPDIR lifecycle,
resource behaviour and the git path of `corpus/evidence/round53/{c1-count,c2-count,build-spans}.py`,
`controls/build-c{1,2}-controls.py`, candidate `tools/assimilate-rows.py` v4 (`32aab5e`, base
`5b550133`); claims read at `a6ff732c`, nothing frozen changed, no production file written.
No install/upgrade (pacman untouched, no uv/npx, no network). Runs with
`TMPDIR=/fast/scratch/hyaku/chousa-r53/R53SentCounters/tmp*`; scratch removed. Baseline:
`c1-count.py --per-leg 1 --seed 7` -> `LEGS=8/8 C1=PASS` exit 0; `c2-count.py --lane-only`
-> `C2=FAIL` (`ENTRIES=0/3`, expected pre-integration).

| id | surface | severity | one line |
|---|---|---|---|
| H1 | c1-count | high (integrity) | `--per-leg 0` prints `LEGS=8/8 C1=PASS` exit 0 with zero generated cases |
| H2 | c1-count / adopter | medium-high | cadence-only recheck accepted though the frozen sentence requires refusal; no leg generates it |
| H3 | c1-count `--work` | medium | used verbatim, uncanonicalised, unguarded; created-and-left; file -> traceback |
| H4 | c1-count lifecycle | low | SIGINT cleans; SIGTERM leaks the whole scratch tree |
| H5 | adopter `--out` | medium | a symlink under `--out` redirects entry writes outside `--out` |
| H6 | adopter | medium (data loss) | `--out` == `--knowledge` unlinks every `--entry` input before reading it |
| H7 | adopter | low | `--entry` naming a directory under `--out` -> `IsADirectoryError`, exit 1, claims already deleted |
| H8 | adopter recheck | medium (validity) | cadence arm unbounded: 200 000-char recheck lands verbatim in `append.md`, unrecorded |
| H9 | adopter perf | low | 10 000 staged rows = 5.13 s / 49 MB; O(n^2) `twins` scan per appended row |
| H10 | c2-count / build-spans | low | `safe_span` blocks `..`/absolute but follows symlinks |
| H11 | c2-count `--root` | low (design) | `--root` executes `root/tools/inference-ground.py`, not only reads |
| H12 | adopter | low | `--entry` a symlink under `--knowledge` reads outside `--knowledge` |

Clean items (checks in the last section): no hardcoded `/tmp`; no write into the lane; no
mutating git command; 200 KB / 10 k inputs are not a DoS.

## H1 — `--per-leg 0` passes the frozen counter with no generated evidence
`type=int`, no lower bound (`c1-count.py:325`); the loop is `range(a.per_leg)` and each leg is
`all(res)`, so empty is True and only REAL/REGRESS run.
```
$ TMPDIR=<scratch>/tmp python3 corpus/evidence/round53/c1-count.py --per-leg 0 --seed 5
SEED=5
REAL PASS rc=0 map=ok rows=5 count-line=['CITED=6 APPEND=5 HELD=0 TWIN=1']
REGRESS PASS r50-pin=ok r51-counter=LEGS=5/5
TWIN=PASS HELD=PASS MIX=PASS RECHECK=PASS ORDER=PASS NOENTRY=PASS REAL=PASS REGRESS=PASS
LEGS=8/8
C1=PASS
rc=0 case_lines=0
```
`--per-leg -3` gives the same. A mistyped or "quick" run gets the target verdict for the six
predicate legs with no package; default/target runs are unaffected. Fix: `if a.per_leg < 1:
ap.error(...)` and print the count in the summary.

## H2 — cadence-only recheck: frozen sentence vs tool, invisible to the counter
Frozen text (`claims.md:44-45`, copied in `c1-count.py:12-13`): refuses "when one has no
leading calendar-valid date or `NNd`". `RECHECK_RE` (`assimilate-rows.py:128`) has a third arm
`[A-Za-z][A-Za-z0-9 _-]*` accepting a bare cadence; the tool docstring says so (`:63-64`,
"or cadence").
```
$ sed -i 's/| 90d |/| quarterly |/' <pkg>/staged.md
$ python3 tools/assimilate-rows.py ... --out <scratch>/cad-out --entry corpus/knowledge/a.md
COLLISIONS=0
CITED=1 APPEND=1 HELD=0 TWIN=0
rc=0
```
`renumber.tsv` is written, so by the frozen sentence this input had to exit 1 with
`REFUSED <id>: recheck`; `stripped.tsv` does not record it (cell unchanged). The counter
cannot catch it: `Gen.recheck_ok`/`recheck_bad` (`c1-count.py:120-133`) emit only ISO/NNd and
invalid dates, never cadence-only. Reported, not patched: align the tool to "or `NNd`" or
refreeze with "or cadence"; if the sentence stands, the RECHECK leg needs a cadence-only case.

## H3 — `--work` is trusted verbatim
`work = ...mkdtemp(...) if own else pathlib.Path(a.work)` (`:335-336`), then
`mkdir(parents=True, exist_ok=True)`: no canonicalisation, no lane/cwd guard, no emptying.
```
$ touch <scratch>/wB/sentinel; ... --work <scratch>/wB        -> sentinel=kept (right)
$ ... --work <scratch>/wC    # absent before -> rc=0 exists=yes entries=117
$ cd <scratch>; ... --work relw                              -> relw_created=yes
$ : > <scratch>/wfile; ... --work <scratch>/wfile
FileExistsError: [Errno 17] File exists: '.../wfile'          rc=1 (traceback)
```
Impact: `--work .` from the fleet root writes package trees there; `--work <lane>` writes in
the lane, contradicting "Writes nothing in the lane". Fix: require an absent/empty directory,
refuse when `LANE` is a prefix of `work.resolve()`, refuse `.` and `/`.

## H4 — SIGINT clean, SIGTERM not
`finally: if own: shutil.rmtree(work, ignore_errors=True)` (`:373-375`) covers exceptions and
KeyboardInterrupt, not SIGTERM/SIGKILL (no `signal` import).
```
$ TMPDIR=<scratch>/tmp2 ... --per-leg 40 --seed 11 & sleep 1; kill -INT $!
INT rc=130 ; count=0                    # scratch empty
$ TMPDIR=<scratch>/tmp3 ... --per-leg 40 --seed 12 & sleep 1; kill -TERM $!
TERM rc=143 ; count=585                 # r53c1-<hex>-*/ left whole, no orphans
```
Fix: install a SIGTERM/SIGHUP handler raising `SystemExit` before creating the work dir.

## H5 — a symlink under `--out` writes outside `--out`
`dst = out / e; dst.parent.mkdir(...); dst.write_text(...)` (`:547-549`); the pre-clean unlink
(`:435`) removes a leaf symlink but not a parent one.
```
$ mkdir -p <scratch>/o2 <scratch>/target2; ln -s <scratch>/target2 <scratch>/o2/corpus
$ python3 tools/assimilate-rows.py ... --out <scratch>/o2 --entry corpus/knowledge/a.md
CITED=1 APPEND=1 HELD=0 TWIN=0 ; rc=0
$ find <scratch>/target2 -type f
<scratch>/target2/knowledge/a.md        # written outside --out
```
Not reachable in default counter runs (fresh `mkdtemp` outs; REAL uses `work/real-out`), but
reachable whenever `--out`/`--work` is a prepared or shared directory. Fix: require
`dst.resolve()` under `out.resolve()`, else refuse.

## H6 — `--out` == `--knowledge` destroys the inputs
The pre-clean loop (`:433-435`) unlinks `out/<entry>` before any entry is read.
```
$ cp -a <pkg> <pkg3>
$ python3 tools/assimilate-rows.py ... --knowledge <pkg3>/knowledge \
    --out <pkg3>/knowledge --entry corpus/knowledge/a.md
COLLISIONS=0
REFUSED entry missing: corpus/knowledge/a.md
rc=1
$ ls <pkg3>/knowledge/corpus/knowledge/       # empty
```
The knowledge tree also gains `reg-ids`/`staged-ids`/`collisions`. The docstring promises
"Read-only on its inputs". Fix: refuse (exit 2) when `out.resolve()` equals or is inside
`knowledge.resolve()` before the unlink loop, or read all entries first.

## H7 — `--entry` naming a directory: traceback after the claim files were deleted
```
$ ... --out <scratch>/o4 --entry corpus/knowledge/a.md     # rc=0
$ ... --out <scratch>/o4 --entry corpus
  File ".../assimilate-rows.py", line 435, in main
    (out / e).unlink(missing_ok=True)
IsADirectoryError: [Errno 21] Is a directory: '<scratch>/o4/corpus'
rc=1
```
Exit 1 looks like a refusal, but `append.md`/`renumber.tsv` were already unlinked: the old
claim is gone and no new one exists. Fix: unlink only `(out/e).is_file() or
(out/e).is_symlink()`.

## H8 — unbounded cadence arm: a 200 000-char recheck accepted verbatim
```
$ # cell 10 = "a"*200000 (letter-initial, no pipe)
CITED=1 APPEND=1 HELD=0 TWIN=0 ; wall=0.06s maxrss_kb=23612 rc=0
append.md bytes: 200121 ; recheck field length: 200118 / 200000
stripped.tsv rows: S002 used-by 1        # the recheck change is NOT recorded
$ # cell 10 = "90d " + "x"*200000 (prose after a leading NNd)
wall=0.04s maxrss_kb=23408 ; stripped.tsv=200076 bytes ; row S006 recheck 200004
```
Not a DoS (0.04-0.06 s, 23 MB), but a row can carry 200 KB of arbitrary text as a "recheck"
the census never blessed, and the Gate record omits it. Fix: bound the arm (`{0,31}`) and
record the clipped cell in `stripped.tsv`.

## H9 — 10 000 staged rows: acceptable, quadratic
Generated packages (10 000 unique staged rows, 10 000 header `source:` lines, registry 5):
`2 000 rows: CITED=2000 APPEND=2000 wall=0.27s maxrss_kb=28064`;
`10 000 rows: CITED=10000 APPEND=10000 wall=5.13s maxrss_kb=49364`. 19x for 5x rows: the
append loop recomputes `twins = {t for t in cited if mapping[t][0] == lid}` (`:533`) per
appended row, O(n^2). Fine at this round's scale; ~minutes at 100 k. Fix: precompute
`twins_by_lane` once.

## H10 — c2-count span containment: `..` blocked, symlinks followed
`safe_span` (`c2-count.py:144-148`) rejects `""`, absolute parts and `..` (unit check:
`'../a' -> None`, `'/etc/passwd' -> None`, `'spans/../../etc/passwd' -> None`), but returns
`ev / raw` unresolved and `:214` reads it.
```
$ ln -s <scratch>/outside <root>/corpus/evidence/round53/spans   # span file outside ev
$ python3 corpus/evidence/round53/c2-count.py --root <root> --lane-only
QUOTE_ROWS=1 ON_BOUND=0/1
QUOTES_IN_SPAN=1/1
QUOTES_IN_ENTRY=1/1
QUOTES_IN_LESSON=1/1
```
`CAPTURE_BOUND` still ties content to the capture, so only `--lane-only` (and the span-file
identity part) can be satisfied this way. Fix: resolve `p` and require `ev.resolve()` as
prefix. `build-spans.py` has the same shape on the write side (`sd.mkdir`,
`(ev/name).write_text`, orphan unlink).
## H11 — `--root` is an execution pointer
`tool = root/"tools"/"inference-ground.py"` runs under `sys.executable`
(`c2-count.py:255-261`); `root` also supplies the registry, entries and lesson. Operator-only
(the TOOLED control does this deliberately with a lane copy). Optional fix: refuse a `root`
outside the lane, or keep executing the lane's tool.
## H12 — `--entry` a symlink under `--knowledge` (informational)
```
$ ln -s <scratch>/secret.txt <pkg5>/knowledge/corpus/knowledge/link.md
$ ... --entry corpus/knowledge/link.md            # rc=0
out read-back: SECRET-OUTSIDE-KNOWLEDGE
```
Read-only escape; same fix as H5 on the knowledge side.

## Clean items — checks behind them
**(1) Write paths.** `grep -n 'write\|mkdtemp\|open(\|rmtree\|tempfile\|/tmp'` over the three
counters and both control builders: no `/tmp` literal; `tempfile.mkdtemp` in all five;
`rmtree` only on the process's own `mkdtemp` (H3 shows `--work` kept). A Python audit hook
(`sys.addaudithook`: `open` with `w/a/x/+` or `O_WRONLY|O_RDWR|O_CREAT|O_APPEND`,
`os.mkdir/remove/rename/rmdir/unlink`, `shutil.rmtree`) over a full `--per-leg 1` run:
`ABS_WRITES=72 OUTSIDE_SCRATCH=0`, `writes touching the lane repo: []`. `c2-count.py
--lane-only` under the same hook: `AUDIT_WRITES=0`. `build-spans.py` is a lane writer by
design (spans.tsv, spans/*.txt, orphan unlink); `inference-ground.py` writes only its `--json`
file, never passed; `--counts /dev/null`.
**(2) TMPDIR.** All `mkdtemp` calls inherit `TMPDIR`; c1 exports `TMPDIR=<work>` to the
round-51 child (`:315`) and strips `ASSIMILATE_CITES` from every tool child (`:78-80`);
verified by the scratch inventories in H3/H4.
**(5) git path.** c1 REAL runs exactly
`["git","-C",LANE,"show","5b5501…c3e:corpus/SOURCES.md"]`; c2 runs the same plus
`git grep -l -e … 5b5501…c3e -- corpus/knowledge`. List argv, no shell, rev constant. In a
scratch fixture repo (`rev-parse --show-toplevel` == fixture): a ref literally named the
40-hex rev is ignored ("Git normally never creates a ref that ends with 40 hex characters …
will be ignored when you just specify 40-hex"), so `GIT_DIR` at an unrelated repo gives
`fatal: path … not in '5b5501…'`; with `GIT_ALTERNATE_OBJECT_DIRECTORIES` the same lane blob is
read (content-addressed); `core.fsmonitor` does not fire on `show`/`grep` (`hook_ran=no`).
The counter under that `GIT_DIR` prints `ENV git show failed` and exits 2 — no false PASS.
Residual: `pin()` covers the campaign package, not the registry bytes REAL derives from `git
show`; a re-verifier should digest those too.
**(4) `..`/content.** `--entry ../a.md` and `--entry /etc/passwd` -> "must be relative",
exit 2. Content never becomes a write path: write names are constants, validated `--entry`s,
or `S###` ids; the escape is the symlink (H5), not content.

## VERDICT
Attacked the round-53 counters and adopter v4 end to end: found `--per-leg 0/-n` printing
`LEGS=8/8 C1=PASS` with zero generated cases (high, cheap fix), a frozen-sentence/tool
divergence the counter cannot see (cadence-only recheck, exit 0), a symlink write escape and
an input-destroying `--out`==`--knowledge` path (medium), an unbounded 200 000-char symbolic
recheck, unguarded `--work`, SIGTERM scratch leakage and a symlink-following span read —
while confirming no hardcoded `/tmp`, no lane write by any counter (72/72 absolute writes in
scratch, c2 zero), TMPDIR honoured, 10 000 rows in 5.1 s / 49 MB, and no mutating or
spoofable git path (env only forces exit 2).

Report: .ufo/waves/round-53/w1/R53SentCounters.md
