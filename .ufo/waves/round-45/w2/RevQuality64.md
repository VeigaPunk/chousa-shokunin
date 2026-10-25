# RevQuality64 — attack QUALITY 64 (round tag) / `tag-count.py` @ 5e8c7ad

Scope: `corpus/QUALITY.md` entry 64, `corpus/evidence/round45/tag-count.py`, control
`corpus/evidence/round45/controls/tag-control-r35-r44.txt`, SCORECARD.md rounds 35-44.
Measured over committed bytes extracted at 5e8c7ad (tree at `/tmp/chousa-r45-RevQuality64/tree`);
working-tree checksums equal committed (tag-count.py 587007fa…, control a0dce153…, QUALITY.md
550dc70f…, SCORECARD.md 7ae474af…).

## 1. Control reproduction (operability)
Command: `python3 corpus/evidence/round45/tag-count.py --from 35 --to 44` (inside tree).
Output byte-identical to the committed control through `TAG=FAIL`; exit 1. Only difference:
the control file has a trailing `exit=1` line the counter never prints (documentation
artifact, not a defect).
- `TAGGED=0/22`, `TAG=FAIL`, exit 1 — reproduced exactly.
- Exit contract holds: 0 = all rows tagged (nonempty), 1 = otherwise, 2 = usage/env
  (`--scorecard /nonexistent.md` → `TAG=FAIL scorecard-missing`, exit 2).
- Empty range `--from 99 --to 100` → `TAGGED=0/0` + `TAG=FAIL`, exit 1 — fail-closed on
  zero rows.

## 2. Independent count (depth)
Method: independent awk census (different implementation, same config): segment by `^## `
headings, match `^## Round ([0-9]+)`, count `^\| C[0-9]` lines in rounds 35-44.
Result: **22 rows** — identical to the counter's census. Section attribution verified:
three merged `## Round 40` headings (closure-corrections / measured-claims / routed-wave-findings)
all feed round 40; `###` subsections do not reset; `## Round-25 …`/`## Round 34 attempt 2`
non-matches behave as documented. No indented `| C<digit>` rows and no `| C<non-digit>`
rows in the file (the `| Capability | …` header rows are correctly excluded by `C\d`).
Also verified `TAGGED=0/22` is a true negative: a cell-exact scan of the 22 rows (strip,
`*`-strip) finds zero `ground`/`plumbing` cells, and neither word appears anywhere in the
22 rows.

## 3. Forges (scratch, committed counter, `--scorecard <forge>`)
- **Forge A — `ground` word inside a longer cell** (round-35 C1 cell „lowest scored axis"
  → „lowest **ground** scored axis"): counter still prints `UNTAGGED round=35`, `TAGGED=0/22`,
  exit 1. **Not fooled.**
- **Forge A2 — escaped-pipe variant** (cell `ground \| …`): `TAGGED=0/22`, exit 1.
  **Not fooled.** (Fragment `ground \` never strips to exact `ground`.)
- **Forge B — tag on a non-claim row** (inserted `| total rows | 2 | ground | done |` in
  round 35): `TAGGED=0/22`, exit 1. **Not fooled.**
- **True-positive sanity**: tagging exactly one real claim row → `TAGGED=1/22`, still exit 1;
  the detector does recognize real tags.

## 4. Defect found (calibration — check can be fooled)
**Leading-whitespace row evasion → false PASS.** The census regex `^\| C\d` is anchored at
column 0. Indenting a claim row by a single leading space removes it from the census while the
row remains a valid (CommonMark/GitHub-accepted, ≤3 spaces) table row. Constructed forge: all
22 rows tagged with an exact `ground` cell except the round-35 C2 row, which is indented one
space. Result: `TAGGED=21/21`, `TAG=PASS`, **exit 0** — a passing verdict on a scorecard that
still contains an untagged claim row in range. So a writer can hide any non-conforming row from
the check by indentation and pass.
Also documented (not a pass-fool alone): any line beginning `| C<digit>` counts as a claim row;
a masquerade header `| C1 | axis | before | after | ground |` inflates the denominator
(23/23 pass when all real rows are tagged). The "claim row" definition is shape-only, with no
protection against table-header or arbitrary rows that happen to start `| C<digit>`.

## 5. Verdict
Holds-narrowed: the control, exit contract and independent census (22 rows, true 0/22) all
hold, and neither mandated forge fools the check; but the check is fooled into PASS by indenting
an untagged claim row (leading-space evasion), and its row definition is shape-only
(`| C<digit>` prefix) with no header/claim disambiguation. Residual risk: row census robustness
(whitespace, header masquerade); no other findings in scope.
