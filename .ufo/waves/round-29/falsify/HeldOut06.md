# HeldOut06 — held-out generalization attack on C1 (h16/h17/h18)

Seat: ChousaR29.HeldOut06. Lane: chousa-shokunin. Date: 2026-10-22.
Attacked: claim C1 (`tools/quote-reopen.py verify` re-opens located quotes against
the live registry URL under the frozen normalization/match contract), on three
held-out items the lane cited in earlier Gate sections but never put in the
fixture: h16 (S017), h17 (S018), h18 (S019). No tool installs (stdlib only).

## Method

STEP 1 blind: opened each registry URL once via the `read` tool, applied the
frozen contract by reading, and recorded verdicts with quoted page text in
`falsify/HeldOut06/blind.md` BEFORE ever running the tool.

STEP 2: wrote `falsify/HeldOut06/items.tsv` (header `id<TAB>source_id<TAB>quote`)
and ran from the lane root:

    timeout 300 python3 tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/HeldOut06/items.tsv

## Results — all 3 AGREE

| id | source_id | quote | blind | tool | cmp |
|---|---|---|---|---|---|
| h16 | S017 | an expanded checklist that details reporting recommendations for each item/sub-item | VERBATIM | VERBATIM | AGREE |
| h17 | S018 | we systematically analyze 134 papers, introduce a unified taxonomy | VERBATIM | VERBATIM | AGREE |
| h18 | S019 | All Cochrane reviews should be assessed periodically to determine whether an update is needed. | VERBATIM | VERBATIM | AGREE |

Tool output: `QUOTE_REOPEN_SUMMARY verbatim=3 absent=0 too_long=0 no_source=0 unreachable=0`, exit 0, 1.86 s.

Evidence seen blind (full text in blind.md):
- h16: the phrase sits verbatim in the PRISMA 2020 first paragraph, inside the
  "expanded checklist" link text; comma follows "item/sub-item" — boundary ok.
- h17: verbatim sub-span of the ACL Anthology abstract sentence "To bridge this
  gap, we systematically analyze 134 papers, introduce a unified taxonomy of
  evidence-based text generation ..."; space boundaries both sides.
- h18: verbatim first sentence of Cochrane Handbook IV.1 paragraph 2 ("All
  Cochrane reviews should be assessed periodically ... is needed. Some areas
  ..."), preceded by paragraph break, followed by space — boundary ok. The
  Key Points bullet reads without "All" and does not match; IV.1 does.

Differential negative control (same hosts, `falsify/HeldOut06/differential.tsv`,
run immediately after): d1 one-digit edit on S018 → ABSENT; d2 h17 quote
cross-attributed to S017 → ABSENT; d3 "All"→"Some" on S019 → ABSENT. Summary
`absent=3`, exit 1. The tool discriminates; it is not an always-VERBATIM stub.

## Freshness finding (lane's own citation, not a tool defect)

lessons/round-25.md:68 records h18's located quote as `Key Points: "All Cochrane
reviews should be assessed periodically ..."`. On the live page the "All"-led
sentence is the opening of IV.1 Introduction; the Key Points bullet reads
"Cochrane reviews should be assessed ..." with no "All". The quote text still
locates (VERBATIM), but the recorded location label is inexact — the lane
attributed IV.1's wording to Key Points. (S029, the superseding row, anchors
IV.1 correctly.)

## Verdict

**HOLDS** for this slice: 3/3 held-out items AGREE blind-vs-tool, and the
negative-control differential shows real discrimination. No DISAGREE, so no
tool-defect/contract-limit attribution needed.

## Limits

Three items, all happened to be VERBATIM labels — held-out coverage of
ABSENT/TOO_LONG/UNREACHABLE paths on these specific sources was only exercised
via my differential, not assigned items. Blind reading used the `read` tool's
extraction; the tool's own HTMLParser semantics could differ on markup inside
the span (checked: none found — all three spans are contiguous text in the
served HTML). Verdicts are as-served 2026-10-22; live pages can drift.
