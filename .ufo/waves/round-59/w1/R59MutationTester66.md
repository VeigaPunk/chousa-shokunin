# R59MutationTester66 — counter mutation probe

- **Claim/counter:** Round-58 C1, `corpus/evidence/round58/claims.md` and frozen `c1-count.py` (the round-59 claims path named in tasking was absent; round58 claims were read before probing).
- **Mutant:** In an isolated scratch copy of `tools/build-spans.py`, removed orphan-span deletion in `main()` (lines 203–205): stale `S###-N.txt` files would persist on rebuild. This specifically targets C1's `FOREIGN` preservation/refusal behavior.
- **Detector/command:** `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py --builder <scratch-builder> --work <fresh-scratch-work>`.
- **Pristine observation:** Exit 1, `C1=FAIL`. `EMPTY_OK`/`REBUILD_OK` passed, but `FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)` and multiple other hazard legs failed. `HELDOUT_OK=fail(rc=1)`; `FAT_RAW` emitted traceback. This is consistent with the pinned round-55 builder, not a usable passing baseline.
- **Mutated observation:** Exit 1, `C1=FAIL`. `FOREIGN=fail(rc=0, orphans deleted: foreign gone=False)` establishes the mutation changed precisely the observed behavior, but detector already failed pristine; cannot credit this as a killed mutant under the prescribed baseline rule. Other baseline failures remained.
- **Verdict:** **INCONCLUSIVE** (baseline failure; mutant not classifiable as killed/survived). Counter is sensitive in its FOREIGN output, but no positive verdict-path calibration was demonstrated.
- **Restoration evidence:** pristine and restored scratch builder SHA-256 both `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`. Removed all scratch files and directory before report. No source/counter/claims bytes modified.
