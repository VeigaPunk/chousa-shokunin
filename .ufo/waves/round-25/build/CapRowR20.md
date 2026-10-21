# Capability row backfill — round 20

Axes: freshness, calibration. Read-only review; no SCORECARD edit.

## Recorded claim and named behavior

- `LOG.md:764`: “**Verdicts** (SCORECARD §Round 20): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1.”
- `SCORECARD.md:1027-1031` names the implemented behavior: “`load_sections` now tracks `in_comment` alongside `fence_char` — comment state checked after fence state, before heading; a `## ` inside `<!-- -->` is literal. Case 124 pins the HTML-comment arm.” Its verdict table at `SCORECARD.md:1048-1050` records coverage improved because the HTML-comment shadow class is closed, operability improved with case 124, and depth improved with `corpus/knowledge/html-comment-r20.md`.
- `SCORECARD.md:1278-1280` explicitly says the capability acquisitions claimed for rounds 15 and 17–23 remain without rows. A direct search found no capabilities-table row ending in first-working round 20.

## Demonstration rerun

Created the assigned private clone and observed base `b820e4e40ce52deedf53b191140cd7b08ddda929`.

Command in `/tmp/chousa-r25-CapRowR20`: `bash tools/research-gate.sh --selftest`

Observed output: `RESEARCH_GATE_SELFTEST: PASS (136 cases, 0 skipped)` and the round-20 case:

```text
ok-case 124 scope-comment-shadow exit=1
```

At this base, later rounds have appended cases, so the rerun is the 136-case suite, not the historical 124-case-only suite. The r20 case is still case 124. Its fixture puts a fake `## Meta` inside an HTML comment after a bounty-scope row; the assertion expects `SCOPE_BOUNTY_ABSORBED` and drift (`tools/research-gate.sh:4992-5003` in the clone). The round-20 knowledge note records the same parser rule and the case-124 recheck (`corpus/knowledge/html-comment-r20.md:3-5,15-22`). The evidence index independently records the historical r20 selftest and before/after demo (`corpus/evidence/README.md:656-659`).

## Proposed SCORECARD row

| HTML-comment heading-shadow detection | Treats headings inside HTML comments as literal text, preventing a fake `## Meta` from shadowing the real scope metadata and letting out-of-scope bounty material pass clean | selftest case 124 (`scope-comment-shadow`); `corpus/knowledge/html-comment-r20.md` | 20 |

The capability is identifiable and its demonstration passes; this row is supported for integration. No SCORECARD change made by this seat.

Installs: none.

VERDICT: Recommend backfilling the round-20 capability row above; the assigned-base selftest passes and case 124 demonstrates the HTML-comment shadow fix.
