# D3 append-only correction drafts

Axes: C1 coverage and C2 operability. Both original passages remain intact; append the specified block only.

## Target 1 — Round 30 report

**File:** `/home/vgpnk/Projects/shokunin/.ufo/reports/round-30/chousa.md`  
**Insertion point:** After current line 82, at the end of `## Trend verdicts`, before `## SHONEN`.

```markdown
### 2026-10-23 correction (D3)

The count above was wrong: the record shows three distinct control findings and two control-forced redesign versions, not four control-forced redesigns. CtlShapeKeyed's C2-v2 shortcut reached 20/20 and forced C2 v3; CtlNoReader's no-reader C1 control reached 104/106; and CtlTrivialC2 together with CriticClaimDesign30 identified the C2 slow-ok chunk-terminator timing defect. The latter two findings led to the C1 and C2 changes in v4, respectively. The earlier v2 redesign came from the L1's own read of exposed URL/host/order features before any control or data seat, not from a control. This is a count/attribution correction; the wording change altered no counter or harness bytes.

Evidence: routed D3, `corpus/lessons/round-30-verifier-spotcheck.md:175-177`; v2/v3/v4 history and L1-read account, `corpus/evidence/round30/claims.md:3-22,32-69`; C2-v2 20/20, `.ufo/waves/round-30/controls/CtlShapeKeyed/receipt-dns-header-c2-run1.json:336-343`; C1 104/106 with zero connections, `.ufo/waves/round-30/controls/CtlNoReader/receipt-relational-c1-h3.json:112-120`; slow-ok mismatch, `.ufo/waves/round-30/controls/CtlTrivialC2/receipt-do-nothing-c2-run1-v3.json:390-404`; timing finding, `.ufo/waves/round-30/controls/CtlTrivialC2.md:15` and `.ufo/waves/round-30/controls/CriticClaimDesign30.md:41`.
```

## Target 2 — Round 30 lesson

**File:** `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-30.md`  
**Insertion point:** After current line 137, at the end of `## Learning`, before `## Seats and holds`.

```markdown
### 2026-10-23 correction (D3)

The count in the paragraph above was wrong: the record shows three distinct control findings and two control-forced redesign versions, not four control-forced redesigns. CtlShapeKeyed's C2-v2 shortcut reached 20/20 and forced C2 v3; CtlNoReader's no-reader C1 control reached 104/106; and CtlTrivialC2 together with CriticClaimDesign30 identified the C2 slow-ok chunk-terminator timing defect. The latter two findings led to the C1 and C2 changes in v4, respectively. The earlier v2 redesign came from the L1's own read of exposed URL/host/order features before any control or data seat, not from a control. This is a count/attribution correction; the wording change altered no counter or harness bytes.

Evidence: routed D3, `corpus/lessons/round-30-verifier-spotcheck.md:175-177`; v2/v3/v4 history and L1-read account, `corpus/evidence/round30/claims.md:3-22,32-69`; C2-v2 20/20, `.ufo/waves/round-30/controls/CtlShapeKeyed/receipt-dns-header-c2-run1.json:336-343`; C1 104/106 with zero connections, `.ufo/waves/round-30/controls/CtlNoReader/receipt-relational-c1-h3.json:112-120`; slow-ok mismatch, `.ufo/waves/round-30/controls/CtlTrivialC2/receipt-do-nothing-c2-run1-v3.json:390-404`; timing finding, `.ufo/waves/round-30/controls/CtlTrivialC2.md:15` and `.ufo/waves/round-30/controls/CriticClaimDesign30.md:41`.
```

## Evidence interpretation

- The C2 v2 receipt records `QUOTE_REOPEN_FETCH_BOUND_MATCH`, `n=20`, `t=20`, and `predicate_holds=true`; the frozen history links it to the v3 redesign.
- The C1 receipt records `n=104`, `t=106`, `net_connect_events=0`, and `predicate_holds=false`; the frozen history links the finding to the C1 v4 redesign.
- The C2 slow-ok receipt records `DEADLINE=5.65`, label `VERBATIM`, and result `UNREACHABLE`. The control reports and timing critique explain the terminator-gap finding and its v4 C2 fix; the receipt alone does not record framing.
- The v2 L1-read fact is sourced from the frozen history text; it is not a control receipt or execution result.
- No target report or lesson file was edited. No gate, counter, build, or test was run; no tools were installed.