# ExecRegressRows — differential run, base builder vs reference (round 61 w1)

## Findings
- 66 quotes tables built, each with the base builder and the reference builder into separate empty scratch outputs: 0 differ.
  Compared per table: exit code, stdout, stderr, and the full output tree (file list plus sha256 of every file; success trees are `spans.tsv` + `spans/` + n span files).
- Primary run (the item's spec): 40 distinct rows drawn at random (seed 61555) from the committed `quotes.tsv` of round55, round56 and round57/c3,
  split into 6 tables of 5,6,7,8,9,5 rows. All 6: exit 0 on both builders, byte-identical stdout (210..357 bytes) and trees.
- Supplementary run (depth, same seed stream): 60 more tables of 5-10 rows drawn with replacement.
  - 50 success tables, the first 40 of them forced to hold at least one OLE-`.raw` row and one `.txt` row: all exit 0, outputs identical.
  - 10 refusal tables, one quote tampered (`...ZZ-not-there`) so the quote is not found: both builders exit 1, write nothing (tree empty), stderr byte-identical.
    This shows the output-safety additions do not change refusal behaviour.
- Row pool: 52 data rows over the three sets (all 52 have a capture in `corpus/captures`): 41 `.txt`-form rows, 11 OLE-`.raw`-form rows
  (3 distinct OLE captures; `capture-text` path exercised). **No zip `.raw` row exists in these three quote tables** (the store holds 1 zip `.raw`,
  not quoted in rounds 55-57), so the zip branch is not exercised by this run — INFERENCE: it is the same `_read`/`_ct_form` path as OLE, but not run here.
- Not covered by this run, by design: the hazard legs (links, FIFO, oversize, non-empty `--out`) — those belong to c1-count.py. `--check` and `--replace` were not exercised.

## Evidence (commands run)
- Builders: base `tools/build-spans.py` (git blob 072415ad…, sha256 1ed2650a…c80bf6) and `controls/ref-build-spans.py` (sha256 86d64c31…eccfd, matches the claims file),
  each copied beside `tools/capture-text.py` in its own scratch dir; run as `python3 -B <copy> --quotes <table> --cache <lane>/corpus/captures --out <empty dir>`.
- Driver `/fast/scratch/hyaku/chousa-r61/ExecRegressRows/drv.py 61555` (scratch, deleted). Last line observed: `TABLES 66 DIFFERENT 0`.
  Header observed: `rows 52 eligible 52 Counter({'txt': 41, 'ole': 11})`, `primary sizes [5, 6, 7, 8, 9, 5]`.
- Spot check: `diff -r o/P4/base o/P4/ref` printed nothing (IDENT).
- No install, no lane or fleet write other than this report; no git mutation.

## Risks / limits
- Random sample of 52 rows: the same rows recur across supplementary tables, so row diversity is bounded at 52 rows / 3 OLE captures / 1 zip not used.
- The refusal tables only cover "quote not found", not the other refusal reasons.

VERDICT: TABLES=66 DIFFERENT=0
