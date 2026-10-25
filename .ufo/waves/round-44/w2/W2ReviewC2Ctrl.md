# W2ReviewC2Ctrl

Seat: leaf reviewer. No subagent. No production edit. No network. No fetch. No commit.
Axes: operability (the named counter runs and returns a count-fail, not a usage error), calibration (the all-left table is the frozen do-nothing gate and must fail; `LEFT_NAMED=3/3` is not partial credit), depth (the fail is class, not missing files or a hash miss).
Milestone: Round 44 wave 2: genuine seats after the usage-error wave.
Verdict: the control holds. Expected `C2=FAIL`, exit 1, `REVERIFIED=0/36`. Not a miss of R44-C2. Not an admission of the scored table. Recommendation only.

## Graded command

Command:

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/c2-count.py --table /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/controls/all-left.tsv
```

Stdout, verbatim (second run; the first run printed the same four lines):

```
CONSISTENT=3/39
REVERIFIED=0/36
LEFT_NAMED=3/3
C2=FAIL
```

Exit code: 1.

Interpreter: `Python 3.14.8` at `/usr/bin/python3`. The script's missing-table branch was not taken (`C2=FAIL table-missing` was not printed). Exit 1 is the count-fail code in the script docstring, not exit 2 (usage/env).

## Frozen expectation

`corpus/evidence/round44/claims.md` lines 62–64: `controls/all-left.tsv` marks all 39 `left-named` and must print `REVERIFIED=0/36` and exit 1. Lines 69–70 name that table as the cheapest full-marks gate: copy the 39 names into 39 `left-named` rows.

Both required prints held. `C2=FAIL` follows the conjunction at `c2-count.py` lines 117–119 (`consistent == 39 and rev == 36 and left == 3`, else FAIL and return 1). The claims sentence does not require `CONSISTENT=0/39` or `LEFT_NAMED=0/3` for this control.

Construction receipt `corpus/evidence/round44/receipts/c2-all-left.txt` is the same four lines plus `exit=1`. This run matches that receipt. The receipt is a construction check, not a seat score, and it was not retuned.

Worktree of the graded inputs was clean. `git status --porcelain -- corpus/evidence/round44/c2-count.py corpus/evidence/round44/controls/all-left.tsv corpus/evidence/round44/claims.md corpus/evidence/round44/disposition.tsv` printed no lines. `HEAD` is `043f19a1db91288947493d9f879e61e7a9f07241` (`043f19a round-44: freeze parent-lifetime, disposition, and RFC quote claims before scoring`). `git merge-base --is-ancestor e6983f6e242c7b82bd9a9c5ee170257624e8f109 HEAD` exited 0. That base is the claims.md base; round-44 evidence is in the descendant, not in the base tree (`git ls-tree` of the base for `corpus/evidence/round44/` printed no paths).

`sha256sum` of the files that were run:

```
343ba2366e8b448062dfd262d23d8f3d4801bbea5936dbc7f4d8d7e19b8b26ad  corpus/evidence/round44/c2-count.py
d82f92c31316a3ed485aa643210a770d4ce23f69555bec1b6ada0d3755acc612  corpus/evidence/round44/controls/all-left.tsv
```

`wc -l` of the table printed `39`.

## Why the numerators are 0, 3, and 3

Independent recount against `UNTRACKED` (36) and `MODIFIED` (3) in `c2-count.py`, not a second print of the counter:

```
TABLE_DATA_ROWS 39
UNIQUE_PATHS 39
FROZEN 39 UNTRACKED 36 MODIFIED 3
MISSING_FROM_TABLE 0
EXTRA_IN_TABLE 0
SHORT 0
ALL_CLASS_LEFT True
ALL_DIGEST_DASH True
ALL_REASON_HAS_PHRASE True
UNTRACKED_CLASS_REVERIFIED 0
MODIFIED_LEFT_AND_PHRASE 3
LANE_PARENTS3 /home/vgpnk/Projects/shokunin/chousa-shokunin
UNTRACKED_PRESENT 36
MODIFIED_PRESENT 3
DISTINCT_REASONS 1
REASON not hunk-verified boilerplate copy of the spot-check list
```

The table is the 39 frozen paths, no extras, no short rows. Every class is `left-named`, every digest is `-`, and every reason is that one phrase.

Untracked example, table line 1:

```
.ufo/waves/round-40/w1/ConnectorSiblingScan.md	left-named	-	not hunk-verified boilerplate copy of the spot-check list
```

Modified example, table line 37:

```
.ufo/waves/round-40/w1/swarm-registry.json	left-named	-	not hunk-verified boilerplate copy of the spot-check list
```

The untracked loop (`c2-count.py` lines 101–107) sets `ok` only when `cls == 'reverified-commit'` and the file then passes stem, round token, length > 80, and sha256. All 36 classes are `left-named`, so that branch is not entered. `REVERIFIED` stays 0. The 36 files are present (`UNTRACKED_PRESENT 36`); the fail is not a missing path.

The modified loop (lines 108–113) sets `ok` when `cls == 'left-named'` and `not hunk-verified` is in a non-empty reason. It does not read the file or the digest. All 3 modified rows meet that clause, so `LEFT_NAMED=3/3` and those 3 increment `CONSISTENT`. `CONSISTENT=3/39` is 0 reverified plus 3 left-named. It is not a partial pass. The pass line requires all three equalities at once.

## Findings

No defect in this control.

- Operability: the named command completed on `/usr/bin/python3`. Exit 1, not 2, and not `table-missing`.
- Calibration: stdout and exit match claims.md lines 62–64 and `receipts/c2-all-left.txt`. `LEFT_NAMED=3/3` is the modified-path clause still holding under a naming-only table. Treating it as credit toward `36/36` would misread the conjunction.
- Depth: the kill is the class gate. Digests are `-` and were not compared. File presence was counted here and is not what the counter used for the 36.

## Not the graded command

The default counting command in claims.md line 57 was also run, so it is not left as an unrun check. It is not the seat command.

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/c2-count.py
```

Stdout:

```
CONSISTENT=0/39
REVERIFIED=0/36
LEFT_NAMED=0/3
C2=FAIL table-missing
```

Exit code: 1.

That matches `corpus/evidence/round44/receipts/c2-before.txt`. `ls` of `corpus/evidence/round44/disposition.tsv` printed `No such file or directory`. `git ls-files` of the round-44 evidence tree does not list `disposition.tsv`. `git check-ignore -v` on that path exited 1 (not ignored). `git show --name-status -1 HEAD` adds `c2-count.py`, `claims.md`, and `controls/all-left.tsv`; it does not add `disposition.tsv`. The commit subject says "disposition"; the tree does not contain the table. The before-receipt already records `table-missing`. This report does not retune claims.md and does not score the target `C2=PASS`.

## Residual

- The sha256, stem, and round-token checks were not exercised. All-left never enters that branch. A forged `reverified-commit` row with digest `-` was not run.
- The modified-path clause does not open the three JSON files. Their presence was counted outside the counter.
- The default table absence is the frozen before-state in `c2-before.txt`, not a new deletion by this seat.
- Each cited command was run once in the clean capture above. The graded command had already printed the same four lines and exit 1 in the first run.
