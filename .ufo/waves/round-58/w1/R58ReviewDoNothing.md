# R58ReviewDoNothing — cheapest do-nothing controls vs frozen targets (round 58)

Seat: run REFUSEALL and the pinned r55 builder against the frozen C1 counter, and base /
missing-entry roots against the frozen C2 counter; report exact target tokens and exit codes.
Lane: /home/vgpnk/Projects/shokunin/chousa-shokunin — read-only; only this report written.
Scratch: /fast/scratch/hyaku/chousa-r58/R58ReviewDoNothing (TMPDIR set on every run; removed
after runs, before this yield). No live fetch, no pacman, no installs. System python3 (3.14).

## Integrity of what I ran
- Freeze commit `9e73a031ab1a…` = 9e73a031ab1ac3bac343de008850d7d87f9e5634,
  2026-10-27 14:07:54 -0300, "round-58: freeze claims and before controls".
- `git diff --stat 9e73a031 -- corpus/evidence/round58/claims.md corpus/evidence/round58/c1-count.py corpus/evidence/round58/c2-count.py corpus/evidence/round58/c2/quotes.tsv` → empty.
  `git status --porcelain -- corpus/evidence/round58/` → empty. Worktree frozen artifacts are
  byte-identical to the freeze commit; runs below used the frozen bytes.
- REFUSEALL.py and build-spans-r55.py are NOT in the 9e73a031 tree; they are tracked and were
  added at `718e8d2` "round-58: record frozen control results" (ancestor of HEAD `5da0a63`
  "round-58: pin S101 opening and frozen C2 baseline").
- `sha256sum controls/build-spans-r55.py` = `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`
  — equals the claims.md pin (also pinned as constants inside both counters). REFUSEALL.py
  (5 lines, unconditional `sys.exit(1)`) has no hash pin in claims.md.
- Base commit `b13ca7b5c8bb…` reachable. Roots built with `git archive <commit> | tar -x -C <root>`
  (read-only export; no clone, no worktree, zero lane writes): base-root=b13ca7b5, missing-root=HEAD.
- `corpus/knowledge/` holds 82 files in both roots; `corpus/knowledge/carrier-alphabet-china-r58.md`
  absent in both (`ls` exit 2). The entry has not landed at HEAD, so missing-root needed no
  mutation — both roots are missing-entry by construction.

## Frozen target tokens (read from the unmodified counters)
- C1: final line `C1=PASS|C1=FAIL` (c1-count.py:401); exit 0 iff PASS (:402). DENIED channel
  denies a control iff the recursive run's stdout has no `C1=` line (:376-386).
- C2: final line `C2=PASS|C2=FAIL` (c2-count.py:162); exit 0 iff PASS (:163). ENTRY_REL
  `corpus/knowledge/carrier-alphabet-china-r58.md` (:17). Counter constants carry the same
  BUILDER_SHA/CT_SHA/RAW_SHA/URL as claims.md.

## A. REFUSEALL → C1
Command:
```
TMPDIR=/fast/scratch/hyaku/chousa-r58/R58ReviewDoNothing HYAKU_SCRATCH=/fast/scratch/hyaku \
python3 <lane>/corpus/evidence/round58/c1-count.py \
  --builder <lane>/corpus/evidence/round58/controls/REFUSEALL.py \
  --work /fast/scratch/hyaku/chousa-r58/R58ReviewDoNothing/w-refuseall
```
Observed output — complete: a Python traceback, no LEG lines:
```
Traceback (most recent call last):
  File ".../corpus/evidence/round58/c1-count.py", line 406, in <module>
    sys.exit(main())
  File ".../corpus/evidence/round58/c1-count.py", line 212, in main
    foreign.write_bytes(b"foreign evidence bytes\n")
FileNotFoundError: [Errno 2] No such file or directory:
  '/fast/scratch/hyaku/chousa-r58/R58ReviewDoNothing/w-refuseall/out-empty/spans/S777-1.txt'
```
Exit code: **1**. Token `C1=PASS` never printed → frozen target not reached. Mechanism (counter
source, unmodified): EMPTY_OK runs first, REFUSEALL refuses it, so `out/spans/` never exists;
line 212 then writes the FOREIGN fixture into that missing dir and the harness dies before any
leg prints. The do-nothing property holds only via harness crash here, not via a leg verdict.

## B. Pinned r55 builder → C1
Same command with `--builder <lane>/corpus/evidence/round58/controls/build-spans-r55.py --work …/w-r55`.
Observed (full leg table):
```
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'Traceback (most recent call last):\n  File ".../build-spans-r55.py", line 217, in <mod')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=fail(rc=1 )
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=3/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```
Exit code: **1**. `FOREIGN=fail(… foreign gone=True)` shows the pinned builder deletes the
foreign `S777-1.txt` — the destructive leg can fail, exactly as claims.md requires.

## C. Supported DENIED channel (r55 primary + --controls)
Same as B plus `--controls <lane>/corpus/evidence/round58/controls --work …/w-r55-denied`.
Additional lines: `CONTROL_REFUSEALL=denied`, `CONTROL_build-spans-r55=denied`, `DENIED=2/2`,
`SUMMARY OK=3/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2`, `C1=FAIL`. Exit code: **1**.
Matches the pre-wave receipt `controls/c1-controls.txt` (DENIED=2/2, C1=FAIL).

## D. Base root → C2
```
python3 <lane>/corpus/evidence/round58/c2-count.py \
  --root <scratch>/base-root --work <scratch>/w-c2-base
```
Observed:
```
ENTRIES=0/1 BOUND=0/1 REF_ID_UNBOUND=1
QUOTE_ROWS=0/12 CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12
SUBSTANCE=FAIL ANCHOR_BOUND=0/3 INFERENCE_GROUNDED=no STRAY_IDS=- NEW_GROUND=no REBUILD=FAIL
ERROR ENTRY_MISSING
ERROR PROVENANCE_TRIO
ERROR S101_NOT_IN_SOURCE
ERROR REF_ID_UNBOUND
ERROR QUOTES_MISSING
ERROR MANIFEST_MISSING
ERROR CAPTURE_BOUND=0/12
ERROR ANCHOR_BOUND=0/3
ERROR ENTRY_QUOTES=0/12
ERROR NEW_GROUND_FAIL
C2=FAIL
```
Exit code: **1**. Token `C2=PASS` never printed.

## E. Missing-entry root (HEAD) → C2
Same command with `--root <scratch>/missing-root --work <scratch>/w-c2-missing`. Same shape as D
except `ERROR QUOTES_MISSING` is replaced by `ERROR BUILDER_REBUILD_MISMATCH`; ends `C2=FAIL`.
Exit code: **1**. Structural fact only: base-root has no `corpus/evidence/round58` at all while
missing-root (HEAD) has `corpus/evidence/round58/c2/` — that is the observable root difference;
no interpretation beyond the counter's own ERROR tokens.

## Findings (frozen predicates untouched; findings, not fixes)
1. [medium — robustness of the frozen C1 counter] With a never-succeeding primary `--builder`,
   c1-count.py crashes (FileNotFoundError at :212, FOREIGN fixture into never-created
   `out-empty/spans/`) instead of printing legs and `C1=FAIL`. The do-nothing property still
   holds (exit 1, no `C1=PASS`), and the supported `--controls` DENIED channel is unaffected —
   but denial is defined as absence of a `C1=PASS` line, so DENIED conflates clean refusal with
   harness crash; `DENIED=2/2` is a weaker signal than it reads.
2. [low — provenance] Milestone says "frozen claims and controls at lane commit 9e73a031", but
   the control builders REFUSEALL.py / build-spans-r55.py and the receipts c1-controls.txt /
   c2-controls.txt are absent from that tree; they landed at 718e8d2 "record frozen control
   results". Identity is anchored by the claims.md sha256 pin (verified for build-spans-r55.py)
   and a clean worktree; REFUSEALL.py carries no hash pin anywhere in claims.md.
3. [informational] The pinned r55 builder also fails safe leg HELDOUT_OK (rc=1) and its FAT_RAW
   refusal surfaces a traceback rather than a named reason — consistent with it being the "before"
   builder; no bearing on the do-nothing property.
4. [informational] D vs E asymmetry (QUOTES_MISSING vs BUILDER_REBUILD_MISMATCH) shows the
   counter's rebuild path behaves differently on roots that predate the round-58 evidence dir;
   both roots fail the pass/fail boundary identically.

## Unrun checks (marked unrun)
- tools/build-spans.py (current target) not run — other seats own the C1 target measurement.
- build-c1-controls.py / build-c2-controls.py not run — generation receipts already preserved;
  this seat runs the controls, not the generator.
- c2 quote offsets/digests not re-verified — C2 substance seats own that surface.
- No NAIVE.py exists in controls/ despite the counter's help text; nothing to run.

## Residual risk
REFUSEALL.py's identity rests on git history alone (finding 2); a byte-swap could not strengthen
it (it can only refuse/crash), so the predicate is not exposed. Finding 1 is the only place a
do-nothing control could mask a counter defect rather than reveal one; this run recorded the
crash explicitly, so nothing is masked today.

Net result: all four do-nothing surfaces refused the frozen targets — C1: `C1=PASS` never
printed, exit 1 in all three runs; C2: `C2=PASS` never printed, exit 1 in both runs.

VERDICT: do-nothing controls (REFUSEALL, pinned r55 builder, base root, missing-entry root) all
fail their frozen targets with exit 1 and no PASS token — survives; falsified nothing, but
REFUSEALL-as-primary-builder crashes the C1 harness at c1-count.py:212 instead of producing a
leg verdict, and DENIED conflates crash with refusal (finding 1).
