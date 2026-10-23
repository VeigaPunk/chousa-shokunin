# ExecD4Rerun — D4 audit: round-30 C1/C2 re-run counts (round 31 W1 BUILD)

Verdict: D4 audit complete. Exact distinct counts computed and confirmed; corrected sentences supplied below for L1 integration (append-only, dated).

## Method

- Local reads only; no network; no tools installed (nothing needed under the tooling directive).
- Extended `corpus/evidence/round30/rerun-check.py` into my dir
  `.ufo/waves/round-31/build/ExecD4Rerun/rerun-after-enum.py` (same receipt-loading
  logic, plus the after-receipt filter and the `(seed, content-sha256)` dedupe).
- Command that prints the counts (exit 0):
  ```
  cd /home/vgpnk/Projects/shokunin/chousa-shokunin && \
  timeout 600 python3 .ufo/waves/round-31/build/ExecD4Rerun/rerun-after-enum.py \
      .ufo/waves/round-30 > .ufo/waves/round-31/build/ExecD4Rerun/enum-output.txt 2>&1
  echo exit=$?   # 0
  ```
- Output saved at `.ufo/waves/round-31/build/ExecD4Rerun/enum-output.txt`.
- All enumerated files are committed: `git status --porcelain -- .ufo/waves/round-30`
  is empty; `git ls-files` tracks 589 files under the wave (RerunC2B: 23).

## C1 — every committed after-receipt (tool `47a657e7…` AND frozen counter `5b312d84…`)

- Distinct (seed, file-content-hash) count: **35** (raw 35; no duplicates).
- Per-directory breakdown (distinct):
  - falsify/ConnectorKagiPin 2
  - falsify/CriticClaimsAfter 3
  - falsify/MutHeadBodyOnly 2
  - falsify/MutHeadNoText 2
  - falsify/MutR29Casefold 2
  - falsify/MutR29Order 3
  - falsify/MutR29SkipScript 3
  - falsify/MutTitleKept 2
  - falsify/RerunC1A 3
  - falsify/RerunC1B 3
  - falsify/RerunC1C 3
  - falsify/ReviewKnowledge30 1
  - falsify/ReviewQuality30 1
  - falsify/SeparabilityRevs 2
  - falsify/SimplifierTool30 1
  - measure 2
  - total 35
- Match distribution: **32 at 106/106**, 3 at 0/106:
  - `falsify/ConnectorKagiPin/c1-run2.json` — low-cap run, disclosed (ConnectorKagiPin.md:3 "Low-cap observations: c1-run2.json scored 0/106 (exit 1)");
  - `falsify/MutR29Order/baseline.json` — initial 1 GiB baseline, disclosed inconclusive (MutR29Order.md:7);
  - `falsify/MutR29SkipScript/baseline.json` — initial low-profile baseline, disclosed inconclusive (MutR29SkipScript.md:6).

## C2 — every committed after-receipt (tool `47a657e7…` AND frozen counter `0a59e373…`)

- Distinct count: **64** (raw 64; no duplicates): 58 at 27/27; 3 at 26/27
  (`RerunC2B/run2`, `run4`, `extra16` — slow-ok UNREACHABLE misses);
  24/27 (`ConnectorKagiPin/c2-run1`, low-cap, disclosed); 20/27
  (`MutNoWatchdog/pristine-limit.json`, 2 GiB baseline, inconclusive); 18/27
  (`MutIgnoreDeadlineConst/baseline.json`, 2 GiB baseline, inconclusive).
- **RerunC2B subset: 23 raw = 23 distinct; 20 at 27/27, 3 at 26/27** — the
  expected 20/23 at 27/27 is confirmed verbatim.

## Corrected sentences (for L1; append-only, dated — earlier text never rewritten)

1. **SCORECARD.md Round 30 C1 row (line 1686) verdict cell** — replace
   "measured: met; re-derived 106/106 in every falsify-wave run (RerunC1A/B/C 9 runs,
   SeparabilityRevs, CriticClaimsAfter)" with:
   "measured: met; re-derived 106/106 on 32 of 35 distinct committed after-receipts
   (landed tool 47a657e7…, frozen counter 5b312d84…: measure 2, RerunC1A/B/C 9,
   CriticClaimsAfter 3, SeparabilityRevs 2, plus 16 more landed receipts); the other 3
   (ConnectorKagiPin/c1-run2, MutR29Order/baseline, MutR29SkipScript/baseline) scored
   0/106 under resource caps and are disclosed as inconclusive."
2. **Lesson `corpus/lessons/round-30.md:95-96`** — replace "CriticClaimsAfter 14 runs"
   (which was a 14-run total including the 9 and the 2 measure runs) with:
   "C1 holds: 106/106 on 32 of 35 distinct committed after-receipts (measure 2,
   RerunC1A/B/C 9, CriticClaimsAfter 3, SeparabilityRevs 2, plus 16 more landed
   receipts); the remaining 3 low-cap runs (ConnectorKagiPin/c1-run2,
   MutR29Order/baseline, MutR29SkipScript/baseline) scored 0/106 and are disclosed as
   inconclusive."
3. **CriticClaimsAfter.md:31** — "RerunC2B 17/20" → "RerunC2B 20/23"
   (committed: 23 receipts, 20 at 27/27, 3 at 26/27); the snapshot then tallies
   41/44 correctly (5+5+2+9+20).

## Limits

- Scope: only the committed round-30 wave tree `.ufo/waves/round-30/` was enumerated
  (task bounds); receipts elsewhere in the lane not examined.
- "After-receipt" defined strictly: both the landed tool SHA-256 and the frozen counter
  SHA-256 present; receipts with a mutant tool hash are correctly excluded.
- The 3 low-cap C1 receipts (0/106) are retained as committed receipts and reported
  separately; they are not counted as support for the 106/106 re-derivation.
- No git/jj writes, no network, no installs; nothing outside `.ufo/waves/round-31/build/ExecD4Rerun/`
  was written.
