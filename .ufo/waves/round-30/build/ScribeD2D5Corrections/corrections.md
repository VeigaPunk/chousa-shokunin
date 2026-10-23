# Draft append-only correction blocks — 2026-10-23

Drafts only; do not overwrite the historical wording. No product, frozen claim, scorecard, log, or lesson file is changed by this artifact.

## D2 — append to the SCORECARD.md Round 29 section

### 2026-10-23 correction to the Round 29 re-derivation count (routed defect D2)

The Round 29 table says wave 2 re-derived C1 in 6 further runs. The committed outputs support 5 further runs, each scoring 130/130:

- `.ufo/waves/round-29/falsify/RerunCounterA/receipt.json` — seed `16442982337510174646`.
- `.ufo/waves/round-29/falsify/RerunCounterB/receipt-1.json` — seed `5392061795029416258`.
- `.ufo/waves/round-29/falsify/RerunCounterB/receipt-2.json` — seed `1932010155184684229`.
- `.ufo/waves/round-29/falsify/ScoutFreshnessH/rederive-receipt.json` and `rederive.out` — run 1, seed `13173258806708832500`.
- `.ufo/waves/round-29/falsify/ScoutFreshnessH/rederive3.out` — run 3, seed `3497534629407128034`.

`ScoutFreshnessH.md` labels run 2 with seed `12970099299958901445` but cites `rederive3.out`; that file records seed `3497534629407128034` (run 3). No separate committed output or receipt for the run 2 seed is in the falsify artifacts, so it is not included in the count of 5. This corrects the count and its evidence trail only; the earlier text is retained. Routed by `corpus/lessons/round-29-verifier-spotcheck.md:148-150`.

## D2 — append to the LOG.md Round 29 entry

### 2026-10-23 correction to the Round 29 run count (routed defect D2)

The Round 29 entry says there were 6 more wave-2 runs. Committed evidence supports 5 further runs at 130/130: `.ufo/waves/round-29/falsify/RerunCounterA/receipt.json` (seed `16442982337510174646`); `.ufo/waves/round-29/falsify/RerunCounterB/receipt-1.json` (seed `5392061795029416258`) and `receipt-2.json` (seed `1932010155184684229`); `.ufo/waves/round-29/falsify/ScoutFreshnessH/rederive-receipt.json` with `rederive.out` (run 1, seed `13173258806708832500`); and `ScoutFreshnessH/rederive3.out` (run 3, seed `3497534629407128034`). The ScoutFreshnessH report's run 2 row gives seed `12970099299958901445` but points to `rederive3.out`, whose output records run 3's seed; no separate committed output or receipt for the run 2 seed was located. The count is corrected without changing the underlying scores or historical text. Routed by `corpus/lessons/round-29-verifier-spotcheck.md:148-150`.

## D5 — append to corpus/lessons/round-29.md

### 2026-10-23 correction to the chronology wording (routed defect D5)

The frozen `corpus/evidence/round29/claims.md:13-14` says “Before any data seat had run the counter”. The supported wording is “before either primary executor scored its candidate”; it does not mean no wave-1 seat had executed counter machinery. Before the v3 freeze, the CtlCasefoldNoBoundary control produced a contract-following scratch reference baseline of 82/82 under v1 (`.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/report.md`, pristine output at lines 123-145). The adjacent `receipt.json` is the mutant result of 78/82, not the reference baseline. MutateCounter also replayed scratch `counter.main()` with recorded page cases and fixed entropy: receipts span 01:25:59 to 01:27:45 UTC, before the v3 freeze at 01:28:23 (`.ufo/waves/round-29/build/MutateCounter.md:11,43-45`; chronology corroboration: `.ufo/waves/round-29/falsify/CriticClaimDesign.md:13-28`). These were a reference baseline and counter-mutation replays, not measurements of either primary executor's candidate. The frozen claims file remains unchanged. Routed by `corpus/lessons/round-29-verifier-spotcheck.md:156-159`.

## D5 — carry-forward block for the round-30 lesson

### 2026-10-23 — Round 29 chronology correction

Read the frozen Round 29 chronology as “before either primary executor scored its candidate,” not as a claim that no wave-1 seat ran counter machinery. The v1 CtlCasefoldNoBoundary contract-following scratch reference scored 82/82; MutateCounter ran scratch counter replays from 01:25:59 to 01:27:45 UTC, before the v3 freeze at 01:28:23. Neither activity measured either primary executor's candidate. See `.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/report.md:123-145`, `.ufo/waves/round-29/build/MutateCounter.md:11,43-45`, and `.ufo/waves/round-29/falsify/CriticClaimDesign.md:13-28`; `claims.md` is frozen.
