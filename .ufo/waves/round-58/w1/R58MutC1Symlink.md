# R58MutC1Symlink — C1 symlink mutation probe

## Scope and bytes
- Read frozen `claims.md` and C1 counter at freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634`; counter SHA-256 (freeze `git show` and lane file): `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`.
- Scratch: `/fast/scratch/hyaku/chousa-r58/R58MutC1Symlink/`. Copied counter and `tools/build-spans.py`; copied counter bytes match freeze. Builder SHA-256: `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` (round-55 pin).
- Builder guard inspection: `Forms.get` checks `raw.is_file()`/`txt.is_file()` then reads through `Path.read_bytes()`; no symlink rejection. `main` constructs `cache`/`out` and writes without an output symlink lstat guard.

## Detector and results
Command for pristine:
```sh
cd /fast/scratch/hyaku/chousa-r58/R58MutC1Symlink
env TMPDIR=/fast/scratch/hyaku/chousa-r58/R58MutC1Symlink python3 -B c1-count.py --builder /fast/scratch/hyaku/chousa-r58/R58MutC1Symlink/build-spans.py --work /fast/scratch/hyaku/chousa-r58/R58MutC1Symlink/pristine
```
Observed output (exit 1):
```text
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'Traceback (most recent call last):\n  File "/fast/scratch/hyaku/chousa-r58/R58MutC1Symlink/build-spans.py", line 217, in <module>\n    sys.exit(main())\n          ')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=fail(rc=1 )
BEFORE_FOREIGN=absent
DENIED=0/0
SUMMARY OK=3/4 REFUSE=0/7 BEFORE_FOREIGN=absent DENIED=0/0
C1=FAIL
```

| Proposed mutation | Frozen detector leg / expected signal | Result |
|---|---|---|
| Remove `--out` lstat guard | `SYMLINK_OUT` must refuse with `SYMLINK` and leave linked target untouched | Baseline already writes into linked target; `SYMLINK_OUT=fail(...target-dir-written!)`. Mutation probe inconclusive: baseline failed. |
| Follow cache symlink | `SYMLINK_CACHE` must refuse with symlink/regular-file reason | Baseline accepts cache symlink: `SYMLINK_CACHE=fail(rc=0, expected refusal)`. Mutation probe inconclusive: baseline failed. |
| Permit symlinked capture | C1 has no separate symlinked-capture leg; cache-input symlink is represented by `SYMLINK_CACHE` | No distinct frozen detector. Existing cache read follows symlinks (`is_file()` then `read_bytes()`); separate mutation/score not performed. |

No mutant was applied: the corresponding output/cache guards are already absent in the round-55 pinned builder, and the pristine counter fails. Per rule, these failures cannot be credited as killed mutants. No post-mutation/restored run was possible or appropriate without an intact baseline detector. Scratch was removed; no lane source bytes were changed. Before/after source builder SHA-256: `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` (unchanged).

VERDICT: INCONCLUSIVE — pristine pinned builder fails frozen C1, including both symlink refusal legs; individual symlink mutants were not scored.