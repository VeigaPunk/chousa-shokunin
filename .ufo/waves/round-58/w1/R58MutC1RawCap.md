# R58MutC1RawCap — FAT_RAW size-guard mutation

## Frozen inputs and scope
- Read `corpus/evidence/round58/claims.md`: C1 requires refusal of an 80 MiB OLE-headed `.raw` fixture with named `SIZE` reason; FAT_RAW is among the refusal legs. Counter predicate is `C1=PASS`.
- Counter bytes SHA-256: `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`, matching `git show 9e73a031ab1ac3bac343de008850d7d87f9e5634:corpus/evidence/round58/c1-count.py` hash.
- Lane `tools/build-spans.py` SHA-256 was `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`, identical to pinned R55 before-builder. It had no 64 MiB guard. Thus this probe used a scratch-only *synthetic vehicle*: R55 bytes plus a minimal raw `stat().st_size > 64 MiB` refusal returning `SIZE`; this is not evidence about a landed C1 candidate.
- Counter `SIZE_CAP` is not used in behavior; FAT_RAW's outcome depends on builder refusal text containing `SIZE` and nonzero exit.

## Mutation and detector
- Pristine vehicle guard: `raw.stat().st_size > 64 * 1024 * 1024`; mutant changed only that threshold to `128 * 1024 * 1024`. FAT_RAW fixture is 80 MiB, so the mutant proceeds into the R55 OLE parsing/read path.
- Command template (ran with `ulimit -v 4194304` as an execution memory bound):
  `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py --builder <scratch-candidate> --work <fresh-scratch-work> --seed 7`
- Pristine output (exit 1): `FAT_RAW=pass(refused)`; `C1=FAIL`.
- Mutant output (exit 1): `FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'Traceback (most recent call last):\n  File "/fast/scratch/hyaku/chousa-r58/R58MutC1RawCap/cand-mutant.py", line 221, in <module>\n    sys.exit(main())\n           ')`; `C1=FAIL`.
- Restored pristine copy output (exit 1): `FAT_RAW=pass(refused)`; `C1=FAIL`.
- Other leg outputs were identical for pristine, mutant, restored: `EMPTY_OK=pass`, `REBUILD_OK=pass`, `FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)`, `SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)`, `SYMLINK_CACHE=fail(rc=0, expected refusal)`, `FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')`, `DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')`, `MANY_QUOTES=fail(rc=0, expected refusal)`, `ESCAPE_ENTRY=pass(refused)`, `HELDOUT_OK=fail(rc=1 )`, `BEFORE_FOREIGN=deleted`, `DENIED=0/0`.

## Evidence and verdict
- Scratch candidate hashes: pristine/restored `003f60000f91493339e49df1b95255003bfd946308d4f3051c4944c10c5b5bcc`; mutant `71d7c8b0b505fbab4196128cdca6758746abedddda80ab97e4cc568b32c110cb`. Restored bytes exactly match pristine hash; fresh work dirs used for all three detector runs. Removed `/fast/scratch/hyaku/chousa-r58/R58MutC1RawCap` before reporting (`scratch_removed=YES`).
- Lane counter and builder hashes after probe equal their pre-probe hashes above; no tracked lane edits were made. Current counter baseline is globally FAIL, so this does not establish C1 PASS or other leg coverage. Within the isolated SIZE leg, baseline refusal passed and raised-threshold mutant failed; every other leg's output was unchanged. The mutant's FAT_RAW output is a traceback whose excerpt is truncated by the frozen counter, but the predicate observed absence of `SIZE`.

VERDICT: FALSIFIED (the 64 MiB guard mutant was killed only by FAT_RAW's named SIZE class in this isolated synthetic vehicle; broader C1 baseline remains inconclusive/FAIL).