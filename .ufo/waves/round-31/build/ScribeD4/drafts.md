# D4 append-only correction drafts — 2026-10-23

Each block is additive; it leaves the cited earlier wording untouched. The routed defect is `corpus/lessons/round-30-verifier-spotcheck.md:178-181`.

## 1. `SCORECARD.md`

**Insertion point:** after line 1701, at the end of the Round 30 section and before `## Capabilities`.

```markdown
### 2026-10-23 correction — routed D4

The Round 30 C1 re-derivation is corrected: 32 of 35 distinct committed after-receipts carrying the landed tool SHA `47a657e7…` and frozen C1 counter SHA `5b312d84…` scored 106/106. The other three (`falsify/ConnectorKagiPin/c1-run2.json`, `falsify/MutR29Order/baseline.json`, and `falsify/MutR29SkipScript/baseline.json`) scored 0/106 under resource caps and are inconclusive, not support for 106/106. `CriticClaimsAfter`'s 14/14 is a combined count of its 3 C1 receipts, the 9 `RerunC1A/B/C` receipts, and the 2 measurement receipts; it is not a separate 14-run bucket. `SeparabilityRevs` contributes 2 distinct C1 receipts. This corrects the duplicate count routed by `corpus/lessons/round-30-verifier-spotcheck.md:178-181`.

Evidence: `.ufo/waves/round-31/build/ExecD4Rerun/enum-output.txt:1-57` and `.ufo/waves/round-31/build/ExecD4Rerun.md:11-18,22-46` (recorded command exit 0).
```

## 2. `corpus/lessons/round-30.md`

**Insertion point:** after line 128, at the end of `## Falsify wave findings`, before `## Learning`.

```markdown
### 2026-10-23 correction — routed D4

The C1 re-derivation above is corrected: 32 of 35 distinct committed after-receipts carrying landed tool SHA `47a657e7…` and frozen C1 counter SHA `5b312d84…` scored 106/106. The other three (`falsify/ConnectorKagiPin/c1-run2.json`, `falsify/MutR29Order/baseline.json`, and `falsify/MutR29SkipScript/baseline.json`) scored 0/106 under resource caps and are inconclusive. The stated 14/14 for `CriticClaimsAfter` is the combined count of 3 `CriticClaimsAfter` C1 receipts, 9 `RerunC1A/B/C` receipts, and 2 measurement receipts—not an additional 14 runs. `SeparabilityRevs` contributes 2 distinct receipts. This repairs the count routed by `corpus/lessons/round-30-verifier-spotcheck.md:178-181` without rewriting the earlier finding.

Evidence: `.ufo/waves/round-31/build/ExecD4Rerun/enum-output.txt:1-57` and `.ufo/waves/round-31/build/ExecD4Rerun.md:11-18,22-46` (recorded command exit 0).
```

## 3. `.ufo/waves/round-30/falsify/CriticClaimsAfter.md`

**Insertion point:** append after line 58 (`CLAIMS: C1 holds, C2 falsified`), at end of file.

```markdown

## 2026-10-23 correction — routed D4

The RerunC2B portion of the 03:43:52Z snapshot above is corrected: it was 20/23 at 27/27, not 17/20. The committed RerunC2B set has 23 distinct receipts: 20 printed 27/27 and 3 printed 26/27. With RerunC2A 5, RerunC2C 5, `measure/after-c2` 2, and this report's 9 C2 runs, the snapshot total remains 41/44. This corrects the defect routed by `corpus/lessons/round-30-verifier-spotcheck.md:178-181`.

Evidence: `.ufo/waves/round-31/build/ExecD4Rerun/enum-output.txt:167-192` and `.ufo/waves/round-30/falsify/RerunC2B.md:21-27,49-52`. The receipt-enumerator command and recorded exit code 0 are at `.ufo/waves/round-31/build/ExecD4Rerun.md:11-18`.
```