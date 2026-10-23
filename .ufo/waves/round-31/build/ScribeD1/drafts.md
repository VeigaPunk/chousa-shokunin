# D1 append-only correction drafts — 2026-10-23

## `corpus/README.md`

**Insertion point:** after line 952, at the end of `## Round30 frontier disposition (2026-10-23)`. Append; do not alter the preceding disposition.

**Paste-ready block:**

```markdown
### 2026-10-23 correction — Round30 frontier disposition (routed defect D1)

The Round30 held-ground change is limited to pages that omit `</head>` (C1). C2 fetch bounds did not meet their frozen kill rule and are not held ground: `QUOTE_REOPEN_FETCH_BOUND_MATCH` was 26/27 on 3 of 44 fresh-seed runs. The round-30 spot-check's consolidated tally is `corpus/lessons/round-30-verifier-spotcheck.md:109` (this correction was routed at `:165-168`). The three miss receipts record `n=26`, `t=27`, and `predicate_holds=false`: `.ufo/waves/round-30/falsify/RerunC2B/run2.json:478-480`, `.ufo/waves/round-30/falsify/RerunC2B/run4.json:478-480`, and `.ufo/waves/round-30/falsify/RerunC2B/extra16.json:478-480`. The earlier disposition is retained as history.
```

**Evidence:** `corpus/lessons/round-30-verifier-spotcheck.md:109,165-168`; receipts at the three paths and fields above; `RerunC2B.md:19-27,49-56` records the executed counter command and scores.

## `SCORECARD.md`

**Insertion point:** after line 1707, at the end of `## Capabilities (round-30 change)`, before `## Planned — round 31 (not started)`. Append; leave the row and its original pointer unchanged.

**Paste-ready block:**

```markdown
### 2026-10-23 correction — capabilities evidence pointer (routed defect D1)

The `27/27` C2 pointer above is not the round's frozen-predicate verdict. Although the two measurement runs scored 27/27, C2 missed its kill rule: 3 of 44 fresh-seed runs printed 26/27 (`corpus/lessons/round-30-verifier-spotcheck.md:109`; this correction was routed at `:165-168`). The three miss receipts record `n=26`, `t=27`, and `predicate_holds=false`: `.ufo/waves/round-30/falsify/RerunC2B/run2.json:478-480`, `.ufo/waves/round-30/falsify/RerunC2B/run4.json:478-480`, and `.ufo/waves/round-30/falsify/RerunC2B/extra16.json:478-480`. Keep the earlier row as history; its C2 evidence must be read as a miss, not as held ground.
```

**Evidence:** `SCORECARD.md:1687` records the two 27/27 measurement runs and the 26/27 misses; `corpus/lessons/round-30-verifier-spotcheck.md:109,165-168` gives the 3-of-44 tally and routes D1; each of the three receipts above has `predicate_holds=false`. No counter was rerun for this draft.
