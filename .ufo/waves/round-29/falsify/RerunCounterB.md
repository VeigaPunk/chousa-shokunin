# RerunCounterB — independent second re-derivation of C1

**Verdict: HOLDS**

## What I attacked
Independent re-run of the frozen predicate at the claimed lane revision
`30c9d24da1815e01e161ed2f52d5f951005cc2b8`, plus provenance checks on the wave-1
receipts in `.ufo/waves/round-29/measure/`.

## Revision verification
- `git rev-parse HEAD` = `b18b3ec9d8a01f966dd81991615bac27df6d66a1` (lane worktree
  is at the receipt-landing commit, not at `30c9d24d`).
- `git merge-base --is-ancestor 30c9d24d HEAD` → exit 0 (`ANCESTOR_OK`).
- `git diff --name-only 30c9d24d..HEAD -- corpus tools` → **0 files**. Counter,
  tool, fixture and `SOURCES.md` are byte-identical at HEAD vs the claimed
  revision; `git status --porcelain` on those paths is clean. Running from the
  lane worktree is therefore equivalent to running at `30c9d24d` for this claim.

## Predicate runs (both from lane root, `timeout 900`)
```
timeout 900 python3 corpus/evidence/round29/c1-count.py \
  --receipt .ufo/waves/round-29/falsify/RerunCounterB/receipt-N.json \
  -- python3 tools/quote-reopen.py verify
```
- Run 1: `QUOTE_REOPEN_MATCH=130/130`, seed=5392061795029416258, wall_s=2.34, `EXIT=0`.
- Run 2: `QUOTE_REOPEN_MATCH=130/130`, seed=1932010155184684229, wall_s=2.25, `EXIT=0`.
- Every class bucket 100% in both runs (verbatim-plain 3/3, verbatim-inline-markup
  9/9, runtime-page-window 24/24, runtime-page-transpose 24/24, all absent-*
  classes, etc. — 16 classes, all full marks).
- Receipts: `counter_sha256=cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`,
  `cmd=['python3','tools/quote-reopen.py','verify']`, `predicate_holds=true`.

## Provenance checks on wave-1 receipts
- Frozen counter sha: `git show 30c9d24d:corpus/evidence/round29/c1-count.py | sha256sum`
  = `cd509650…175d`; worktree file hashes identically.
- `measure/after-run1.json` and `after-run2.json`: `counter_sha256=cd509650…175d` ✓,
  `cmd=['python3','tools/quote-reopen.py','verify']` (the predicate CMD) ✓,
  `match=130/130`, `predicate_holds=true`, distinct fresh seeds
  (1858171162794361068, 11266274748383853032).

## Observations / limits
- `tool_exit=1` on all runs including mine: `quote-reopen.py verify` exits 1 even
  when every emitted verdict matches the label. The frozen counter scores stdout
  verdict lines only (does not check the exit code), so this is consistent
  observed behaviour in all 4 runs — flagged as data, not scored.
- Runs hit live source URLs (counter + tool fetch per SOURCES.md); 2.2–2.3 s walls.
- Scope was re-derivation + provenance only; no mutant or held-out attack.
- No installs performed; no lane/git mutations. Artifacts:
  `.ufo/waves/round-29/falsify/RerunCounterB/receipt-{1,2}.json`.
