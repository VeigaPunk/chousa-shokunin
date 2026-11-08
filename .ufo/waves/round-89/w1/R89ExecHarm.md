# R89ExecHarm — harm sweep

Godspeed axes: harm over the round. Keep any move that improves a claim and harms none; the pack is one pass across both C1/C2 with shared trees.

Tooling: `python3` (stdlib only, already installed); no install/upgrade this round. Scratch `/fast/scratch/hyaku/chousa-r89/R89ExecHarm` removed after run.

Trees: `git archive` of `ac0a0892c15de11fb28d3208f2b287687c00477e` (freeze) and `f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8` (base) under scratch. Subject tool byte-identical: blob `dc7a4176…` both revisions, sha256 `905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60` (`receipts/tool-sha.out`).

## (a) harm-recheck → moved=0
`python3 -B $S/freeze/corpus/evidence/round89/harm-recheck.py --root $S/freeze --repo <lane> --base-tool <base blob>` → `HARM_RECHECK files=13 records=29 moved=0 base_rc=0 r88_rc=0` (exit 0). `receipts/a-harm-recheck.out`.

## (b) wider sweep — EVERY GATE-RECORD line
`git grep '^GATE-RECORD'` at freeze: whole tree 688 lines; `.ufo/waves/**` 660; `plans/` 0; `corpus/evidence/**` 0 (`receipts/b-grep-counts.out`).
Ran the single tool blob (identical at both revisions) over all 989 files containing `GATE-RECORD` → 733 verified records, per-file `OK/FAIL + codes` in `receipts/b-verdicts.tsv`; freeze and base verdict maps are byte-identical (moved=0). Totals: OK=195 FAIL=538 SETUP=0; `corpus/lessons` subset 29/29 OK; `c1-positives.tsv` 15/15 expected OK (`receipts/b-summary.txt`).
Finding on composition: all 538 FAILs are deliberate forged/mutant/fixture records (past-wave experiment fixtures, `R83ExecForge/*` forge corpora, detached-ok attack artifacts, docstring example lines — e.g. `R80CriticA.md:336` nonexistent-file attack, `gate-grounding-check.py:13` docstring). No genuine committed lesson record fails; no verdict differs from the `c1-positives.tsv` expectation. The sweep is non-vacuous: it distinguishes the 195 genuine OKs from the 538 deliberate FAILs.

## (c) curated entries identical
`git diff f8fa55ec..ac0a0892 -- corpus/knowledge/` is EMPTY (1-line receipt, `receipts/c-knowledge-diff.out`). The two curated files (`search-transparency-reporting-r84.md`, `provenance-recording-r85.md`) are byte-identical across revisions. `curation-r89.py --root` on freeze and base trees prints byte-identical output including `CURATION_R89=PASS`, `QUOTES_LOCATED=20/20`, `WARRANT_OK=17/17`, `TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0` (`receipts/c-curation-freeze.out`, `receipts/c-curation-base.out`) — the two entries' leg verdicts do not move.

## (d) registry: exactly two used-by cells
`git diff f8fa55ec..ac0a0892 -- corpus/SOURCES.md`: only S216 and S218 rows change, each by appending `corpus/evidence/round89/claims.md` to the `used-by` cell (cell 10). Cell-by-cell comparison over all 220 `|` rows: changed_rows=2, both single-cell `used-by` appends, no other cell moved (`receipts/d-sources-diff.out`, `receipts/d-cells.out`).

## (e) positive control — the sweep can fail
Isolated fixture root (minimal `corpus/` + same tool): forged S209 record with zeroed `capture_sha256` → `FAIL CAPTURE_KEY,CAPTURE_SHA,REFETCH`, `ok=0 fail=1`, exit 1 (`receipts/e-iso-broken.out`). In the freeze root, a file pairing the genuine S199 rev record (OK) with a broken S209 record (FAIL `CAPTURE_KEY,REFETCH`) → `ok=1 fail=1`, exit 1 (`receipts/e-positive-control.out`). Refusal is live, not blanket: genuine positives in the same lanes still OK.

## Counter predicates (as claimed)
C1: `GATE_RECORDS_R89=PASS` exit 0, `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16`, round-88 fields intact (`POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=EXPECTED_CODE=362/362`, `D1_REFUSED=3/3`, `D2_REFUSED=3/3`, `MUT_ADMIT_KILLED=1`, `MUT_UNREACH_KILLED=1`, `DERIVE_NEG=1`) — `receipts/c1-battery.out`. `mutate-r89.py` → `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2` with E7c/E7b dying as `UNRECONCILED` and E7d/E7f as `UNCROSSCHECKED` — `receipts/c1-mutants.out`.
C2: `CURATION_R89=PASS` with the printed fields (nine legs, `VERDICT fields_hold=1`) — `receipts/c-curation-freeze.out`. `curation-r89-controls.py` → `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7` — `receipts/c2-controls.out`. `curation-r89-mutants.py` → `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1` — `receipts/c2-mutants.out`.

No other files written; no sibling/lane mutation; no network. Factors moved: none.

VERDICT: R89ExecHarm C1 held — harm-recheck moved=0 and the identical tool blob's wider sweep moved no genuine record.
VERDICT: R89ExecHarm C2 held — both curated entries produce identical pass verdicts across revisions and only the two claimed used-by cells moved.
