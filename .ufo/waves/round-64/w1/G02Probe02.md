# G02Probe02 — missing/non-directory knowledge-root fixture probe

## Result

Compared the read-only candidate `corpus/evidence/round64/controls/ref-preflight-v3.py` against frozen C1 `claims.md` §C1, lines 47–52. Both missing and non-directory `corpus/knowledge` fixtures are required to fail G02 rather than pass vacuously. Candidate matches both cases.

## Exact retained evidence

- `missing.out`: command used fixture with `corpus/README.md` and absent `corpus/knowledge`; exit 1. Output includes `GATE G02 knowledge-index FAIL corpus/knowledge is not a directory` and `PREFLIGHT=0/1 FAILED=G02 ENV=none SKIPPED=G01,G03,G04,G05,G06,G07,G08`.
- `nondir.out`: same fixture shape except `corpus/knowledge` is a regular file; exit 1 with the same G02 failure and summary.
- `G02Probe02/recipe.md`: reproducible fixture setup and commands. Captured stdout/stderr is preserved in the two `.out` files.

No candidate changes, installs, git/jj mutations, or external actions. Python runtime observed: 3.14.8; no tool installation. No blockers.