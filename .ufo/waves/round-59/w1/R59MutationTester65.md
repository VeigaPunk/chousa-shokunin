# R59MutationTester65 — mutation probe

## Scope and setup
The requested `corpus/evidence/round59/claims.md` was absent. I read the latest extant frozen claims at `corpus/evidence/round58/claims.md`; this probe tested its C1 claim using the frozen `corpus/evidence/round58/c1-count.py` counter and isolated scratch copies of the builder and counter. No source or frozen evidence was edited.

## Mutant
One-line plausible defect in `Forms.get`: change `if raw.is_file():` to `if raw.exists():` so a symlinked raw cache input is treated as a candidate raw file. This removes the regular-file check at that behavior-bearing point.

## Command and observed output
Detector (pristine, mutant, then restored) was the same bounded command apart from distinct fresh `--work` directories:

```sh
python3 /fast/scratch/hyaku/chousa-r59/R59MutationTester65/c1-count.py --builder /fast/scratch/hyaku/chousa-r59/R59MutationTester65/build-spans.py --work /fast/scratch/hyaku/chousa-r59/R59MutationTester65/work-{baseline,mutated,restored}
```

Pristine and restored outputs were identical; mutated output was also identical:

```text
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'Traceback (most recent call last):\n  File "/fast/scratch/hyaku/chousa-r59/R59MutationTester65/build-spans.py", line 217, in <module>\n    sys.exit(main())\n      ')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=fail(rc=1 )
BEFORE_FOREIGN=absent
DENIED=0/0
SUMMARY OK=3/4 REFUSE=0/7 BEFORE_FOREIGN=absent DENIED=0/0
C1=FAIL
```

## Verdict and restoration
**Inconclusive, not killed.** The pristine detector already exits 1 with `C1=FAIL`, and therefore cannot establish a mutant-caused failure. The frozen round59 receipt `controls/c1-before.txt` also records C1 failing all seven refusal legs, so the local run's baseline failure is consistent with that receipt. Mutant's detector output was unchanged. Builder pristine/restored SHA-256: `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`; mutation script change was discarded by copying pristine bytes back, and matching restored hash was observed. Scratch directory was removed after the restored detector run.
