# R74Mutation — bounded frozen-matrix mutation probe

Author-lane evidence only; no promotion/admission judgment. Axes: detector sensitivity, exact restoration, bounded execution. Read godspeed and round74 claims. All three input scripts matched frozen revision `1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb`.

## Detector and actual outcomes

Same frozen matrix executed on pristine, each mutant, and restored bytes:
`python3 -B /fast/scratch/hyaku/chousa-r74/R74Mutation/matrix.py --counter /fast/scratch/hyaku/chousa-r74/R74Mutation/counter.py --work /fast/scratch/hyaku/chousa-r74/R74Mutation`

Expected: pristine/restored exit 0 with `LOADER_MATRIX=9/9 C1=PASS`; mutants below 9 with exit 1. Fixtures use real Git repositories beneath the seat scratch; frozen driver uses explicit `git -C` and asserts fixture toplevel before its first commit.

| Probe | Actual summary | Exit | Verdict |
|---|---|---:|---|
| Pristine successor | `LOADER_MATRIX=9/9 C1=PASS` | 0 | Valid baseline |
| M1: load line 131 reverted to original `int(parts[0]) if parts[0].isdigit() else 0` | `LOADER_MATRIX=3/9 C1=FAIL` | 1 | KILLED |
| Restored after M1 | `LOADER_MATRIX=9/9 C1=PASS` | 0 | Exact-byte restoration passes |
| M2: load line 131 becomes `deleted[parts[2]] = 0` | `LOADER_MATRIX=5/9 C1=FAIL` | 1 | KILLED |
| Restored after M2 | `LOADER_MATRIX=9/9 C1=PASS` | 0 | Exact-byte restoration passes |

M1 falsely rejects all three appends (actual exit 1, C2-6 failure) and accepts all three deletions (actual exit 0, no failed check). Equal replacement still rejects accidentally. M2 accepts all three deletions and equal replacement (actual exit 0, no failed check). Neither assigned mutant survives.

## Evidence and restoration

Absolute receipt directory: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Mutation/`.

- `pristine-matrix.txt`, `m1-additions-column-matrix.txt`, `m2-zero-deletions-matrix.txt`: complete actual stdout/stderr, exit, fixture commit IDs and selected-counter digest.
- `restored-after-m1-matrix.txt`, `restored-after-m2-matrix.txt`: identical detector on restored bytes.
- `m1-additions-column.diff`, `m2-zero-deletions.diff`: exact single-line patches; corresponding `.py` files retain mutant bytes.
- `evidence.json`: full results and source before/after/frozen SHA-256 values.
- `cleanup.txt`: scratch absent after finally cleanup; scratch counter restored exactly before removal.

Counter pristine/restored SHA-256: `9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41`.
M1 SHA-256: `f189723728230385c7b23b38b89aec162c9d7e1436dd62e65b5bd21d4708d65a`.
M2 SHA-256: `5799108333bff7c67bf57cdce2e568c3fd13c66f5b7da3a90b67e7b4a64e958c`.
Frozen matrix SHA-256: `979638251845071cfb2c5e130cd81800251c5a6cb041438deb258d8877e2ff8d`.
All shared source before/after hashes equal; no shared mutation, clone, network, installation, or lane index mutation. Runtime: existing Python 3.14.8.

## Frozen limitations

Only the nine frozen cases were exercised. They contain numeric numstat cells: neither probe isolates the successor's nonnumeric-deletion fallback, so rejecting nonnumeric cells is not independently certified by these results. Equal replacement covers LOG only; no additional path/rename/binary cases were added. Historical-landing second conjunct was not run by this seat. Existing substring-semantic weaknesses remain outside this claim, as the frozen claims specify. No inference of general expertise, historical admission, or broader coverage follows from two killed mutants.
