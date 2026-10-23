# Scribe D2/D5 corrections — 2026-10-23
**Axes / behavior:** coverage and operability are in task context; drafted append-only D2 run-count and D5 chronology corrections only; no claim verdict or C1/C2 score.
**Evidence:** read round-30 `claims.md` first, then D2 routing, Scorecard/Log round 29 entries, frozen round-29 claims, lesson, falsify reports/receipts, and baseline/replay evidence.
**Recorded command/outcome:** `RerunCounterA.md` records `timeout 900 python3 corpus/evidence/round29/c1-count.py --receipt .ufo/waves/round-29/falsify/RerunCounterA/receipt.json -- python3 tools/quote-reopen.py verify` → `QUOTE_REOPEN_MATCH=130/130`, counter exit 0 (candidate exit 1).
**D2 finding:** five committed outputs support 130/130; FreshnessH's run 2 seed `12970099299958901445` cites `rederive3.out`, which records run 3 seed `3497534629407128034`; full dated blocks and all paths/seeds are in `ScribeD2D5Corrections/corrections.md`.
**D5 finding:** frozen claims wording is narrowed to “before either primary executor scored its candidate”; draft discloses CtlCasefoldNoBoundary's v1 contract-following reference baseline 82/82 and MutateCounter's 01:25:59–01:27:45 UTC replays before the 01:28:23 freeze.
**Touched surfaces:** report and draft artifact only; no lane production/frozen files, VCS state, tests, counters, source fetches, judge, or installs. `round-30.md` was absent when read; carry-forward block is drafted for the lesson author.
Report: .ufo/waves/round-30/build/ScribeD2D5Corrections.md
