# R58MutC1Fifo — C1 regular-file/FIFO probe

## Scope and setup
- Read frozen `claims.md` and `c1-count.py`; C1 requires FIFO/device refusal without blocking. The counter's FIFO leg has a 20-second builder timeout.
- Freeze commit `9e73a031ab1ac3bac343de008850d7d87f9e5634` is an ancestor of observed HEAD `5da0a6375a554e1229492a8cb0b9695bd8e85456`. Post-freeze commits added receipts; the counter and builder were unchanged. Worktree showed untracked `.ufo/waves/round-58/`.
- Lane builder SHA-256 before and after: `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` (the pinned r55 builder). Counter SHA-256: `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`.
- Scratch: `/fast/scratch/hyaku/chousa-r58/R58MutC1Fifo/`, removed before completion. Scratch builder's adjacent `capture-text.py` copy matched pin `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`.
- Detector command for each run: `( ulimit -v 2097152; TMPDIR="$S" timeout 900 python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py --builder "$BUILDER" --work "$WORK" )`. The address-space cap constrained mutant `/dev/zero` reads. No live fetch.

## Baseline / mutant / restored
**Pristine baseline** — builder bytes SHA-256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`; command exit `1`; final `C1=FAIL`. Observed FIFO: `FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form ...')`. Device leg likewise failed for absent reason; baseline was already failing, not a passing detector.

**One mutant (M1)** — copied pristine builder and changed only `elif txt.is_file():` to `elif txt.exists():` in `Forms.get`. Mutant SHA-256 `f07c36eaf097e8cef09fb29250f222b97a47ebb093e85dd0c35ca94907cb903a`. Same frozen counter command, separate fresh work dir; exit `1`, final `C1=FAIL`. Exact affected output:
```
FIFO_TXT=fail(hung reading the FIFO)
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'Traceback (most recent call last):\n  File "/fast/scratch/hyaku/chousa-r58/R58MutC1Fifo/build-spans.m1-txtgate.py", line 217, in <module>\n    sys.exit(main())\n  ')
```
The FIFO read was killed by the counter's 20s timeout (no completion/read result); `/dev/zero` produced a bounded-memory traceback, not a hang. Other leg results matched the baseline.

**Restored/pristine repeat** — used the untouched pristine copy; command exit `1`, output matched baseline byte-for-byte, final `C1=FAIL`. Builder SHA-256 remained `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` before and after. Lane builder/counter hashes unchanged; scratch removed (`SCRATCH_REMOVED`).

## Verdict
The mutation changes the FIFO observation from an unnamed refusal to a timed-out blocking read, so the frozen leg reports the hang. However, the pristine detector already returns `C1=FAIL`; per mutation protocol this is **inconclusive, not a killed mutant**. No passing baseline exists in the frozen lane for a strict kill verdict.

VERDICT: INCONCLUSIVE — `txt.is_file()` → `txt.exists()` FIFO-gate mutant; frozen counter detects a hung FIFO read, but baseline C1 fails.
