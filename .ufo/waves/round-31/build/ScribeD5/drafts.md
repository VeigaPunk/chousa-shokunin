# D5 append-only correction drafts — 2026-10-23

Drafts only; do not rewrite or replace earlier wording. The proposed target insertions are limited to the two files below.

## Target 1 — control report

**File:** `.ufo/waves/round-30/controls/CtlNoReader.md`  
**Insertion point:** after line 44, at end of file (after the v4 section's existing final paragraph).

### 2026-10-23 correction to the v4 C1 control maximum (routed defect D5)

The 84/106 figure in this no-reader control report is the best no-reader result, not the maximum among all v4 C1 controls. The committed all-control tally lists 61 receipts carrying the v4 counter hashes and records the overall C1 maximum as 86/106: `.ufo/waves/round-30/controls/CtlParseShortcuts/receipt-skip-nothing-v4.json` (`n=86`, `t=106`, `predicate_holds=false`, `tool_rc=1`). The best no-reader result remains 84/106: `.ufo/waves/round-30/controls/CtlNoReader/receipt-relational-v4-c1-v4-run2.json` (`n=84`, `net_connect_events=0`, `predicate_holds=false`). See `.ufo/waves/round-31/build/ExecD5Controls/tally_v4_receipts.out:1-4,64-77`; routed by `corpus/lessons/round-30-verifier-spotcheck.md:182-183`. This addition clarifies scope only; earlier text is retained.

## Target 2 — round-30 lesson

**File:** `corpus/lessons/round-30.md`  
**Insertion point:** after line 165, at end of the `## Seats and holds` section / end of file.

### 2026-10-23 correction to the v4 C1 control result (routed defect D5)

The 79/106 and 84/106 figures above are the strengthened no-reader control's two C1 scores, not the maximum across all v4 C1 controls. The committed all-control tally lists 61 receipts carrying the v4 counter hashes: the overall maximum is 86/106 in `.ufo/waves/round-30/controls/CtlParseShortcuts/receipt-skip-nothing-v4.json` (`n=86`, `t=106`, `predicate_holds=false`, `tool_rc=1`), while the best no-reader result is 84/106 in `.ufo/waves/round-30/controls/CtlNoReader/receipt-relational-v4-c1-v4-run2.json` (`n=84`, `net_connect_events=0`, `predicate_holds=false`). Evidence: `.ufo/waves/round-31/build/ExecD5Controls/tally_v4_receipts.out:1-4,64-77`; routed by `corpus/lessons/round-30-verifier-spotcheck.md:182-183`. This clarification adds the all-control comparison without changing the earlier lesson row.

## Scorecard check

`SCORECARD.md:1692-1694` already says “best C1 no-reader 84/106,” which is accurate: the all-control tally gives the best no-reader result as 84/106 and separately gives the overall C1 maximum as 86/106. No scorecard correction or insertion is proposed.

## Evidence opened

- `.ufo/waves/round-31/build/ExecD5Controls/tally_v4_receipts.out:1-4,64-77` — 61 v4-hash receipts, overall C1 maximum 86/106, no-reader maximum 84/106.
- `.ufo/waves/round-30/controls/CtlParseShortcuts/receipt-skip-nothing-v4.json:202-211` — `n=86`, `t=106`, `predicate_holds=false`, exit 1.
- `.ufo/waves/round-30/controls/CtlNoReader/receipt-relational-v4-c1-v4-run2.json:212-221` — `n=84`, `net_connect_events=0`, `predicate_holds=false`, exit 1.
- `corpus/lessons/round-30-verifier-spotcheck.md:182-183` — routed D5 statement.