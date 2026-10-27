# R58MutC1Foreign — C1 FOREIGN-guard mutation probe

## Scope and input
- Read frozen `corpus/evidence/round58/claims.md` and `c1-count.py`. The C1 FOREIGN predicate requires refusal, preservation of `spans/S777-1.txt`, and a reason containing `777` or `foreign`; overall acceptance is `C1=PASS` (exit 0).
- The designated candidate was unavailable: current lane `tools/build-spans.py` has the pinned R55 SHA `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`. L1 confirmed no committed candidate is available before integration. Per instruction, I did not mutate this base as a substitute.
- Frozen counter SHA: lane and scratch copies both `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`.

## Detector and observed negative-control run
Exact command (counter and builder were copied into my scratch; `--work` and `TMPDIR` were explicit):
```sh
cd /fast/scratch/hyaku/chousa-r58/R58MutC1Foreign && TMPDIR=/fast/scratch/hyaku/chousa-r58/R58MutC1Foreign HYAKU_SCRATCH=/fast/scratch/hyaku/chousa-r58/R58MutC1Foreign python3 -B ./c1-count.py --builder /fast/scratch/hyaku/chousa-r58/R58MutC1Foreign/build-spans-pristine.py --work /fast/scratch/hyaku/chousa-r58/R58MutC1Foreign/work-pinned
```
Observed output:
```text
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'Traceback (most recent call last):\n  File "/fast/scratch/hyaku/chousa-r58/R58MutC1Foreign/build-spans-pristine.py", line 217, in <module>\n    sys.exit(main())\n ')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=fail(rc=1 )
BEFORE_FOREIGN=absent
DENIED=0/0
SUMMARY OK=3/4 REFUSE=0/7 BEFORE_FOREIGN=absent DENIED=0/0
C1=FAIL
```
This is the expected failing R55 negative control, not a candidate baseline; it is inconclusive for mutation detection.

## Requested mutants
| Mutant | Intended leg | Reason / result |
|---|---|---|
| Delete foreign before refusal | FOREIGN | Not run: candidate absent; no survivor verdict. |
| Allow orphan deletion | FOREIGN | Not run: candidate absent; no survivor verdict. |
| Skip foreign-name check | FOREIGN | Not run: candidate absent; no survivor verdict. |

Expected detector for each is the frozen C1 counter's FOREIGN check above; mutation verdicts are **inconclusive**, not killed or survived. Candidate pristine/mutated/restored runs were unrun.

## Hash and cleanup evidence
- Lane builder before/after: `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` (unchanged; equals pinned R55 hash).
- Scratch pristine builder copy: same SHA `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`; no mutation was made, so no restore operation was needed.
- Lane and scratch counter copy hashes matched as recorded above. Scratch removed; command confirmed `scratch_removed=yes`.

VERDICT: INCONCLUSIVE — the C1 candidate is not available; only the pinned R55 negative control was run, and the three FOREIGN-guard mutations were not performed.