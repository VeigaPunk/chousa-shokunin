# HeldOut02 — held-out generalization attack on C1

**Attacked:** claim C1 (`tools/quote-reopen.py verify`, frozen contract in
`corpus/evidence/round29/claims.md` design v3) on held-out items h04 (S005),
h05 (S006), h06 (S007) from `.ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv`
— located quotes the lane cited in round-24 Gate sections, never in the fixture.

## Step 1 — blind verdicts (before running the tool)

I opened each registry URL (GET + `read` tool; raw HTML saved to my scratch dir)
and judged under the frozen contract (NFKC, curly→straight quotes, whitespace
collapse, case-sensitive, non-alphanumeric boundary).

- **h04 / S005** (https://aclanthology.org/2025.acl-long.1534/, HTTP 200 text/html,
  43931 B): page text has "…the “telephone effect” - when citing papers have low
  fidelity to the original claim, future papers that cite the citing paper and
  the original have lower fidelity to the original." The normalized quote is a
  substring bounded by space (before "when") and space (before "to"), both
  non-alphanumeric. 23 words ≤ 25. **Verdict: VERBATIM.**
- **h05 / S006** (https://arxiv.org/html/2605.06635v1, HTTP 200 text/html,
  140546 B): the quote drops the enumeration markers. Page text reads "(1)
  Link Works verifies URL accessibility, (2) Relevant Content measures topical
  alignment, and (3) Fact Check validates factual accuracy against source
  content." — the "(2)"/"(3)" insertions break the claimed string in both the
  abstract and §1 ("via LLM-as-a-judge" variants there differ further). No
  other occurrence. **Verdict: ABSENT.** This is a lane freshness finding:
  the held-out TSV itself flags `lessons/round-24.md:53` as
  `[summary-not-verbatim]` — the lane paraphrased rather than quoted.
- **h06 / S007** (https://arxiv.org/html/2601.08536v3, HTTP 200 text/html,
  1324418 B): §2.1 text reads "…but this only measures the accuracy of the
  citations and does not necessarily confirm that the information is correct
  (e.g., false information…". Quote is a substring bounded by space (before
  "this") and space (before "(e.g."), non-alphanumeric. 17 words ≤ 25.
  **Verdict: VERBATIM.**

## Step 2 — tool run

`timeout 300 python3 tools/quote-reopen.py verify --items
.ufo/waves/round-29/falsify/HeldOut02/items.tsv` from the lane root
(items file: `.ufo/waves/round-29/falsify/HeldOut02/items.tsv`):

```
QUOTE_REOPEN	h04	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h05	ABSENT	no match in normalized page text
QUOTE_REOPEN	h06	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=2 absent=1 too_long=0 no_source=0 unreachable=0
```

Exit code 1 (correct: not all VERBATIM; contract says 0 only if all VERBATIM).

## Comparison

| item | blind | tool | result |
|---|---|---|---|
| h04 | VERBATIM | VERBATIM | AGREE |
| h05 | ABSENT | ABSENT | AGREE |
| h06 | VERBATIM | VERBATIM | AGREE |

3/3 AGREE, no DISAGREE to adjudicate.

## Verdict

**HOLDS.** On held-out generalization the tool produced the contract-correct
verdict on 3 of 3 items it had never seen, including the one (h05) whose label
requires noticing dropped "(2)"/"(3)" enumeration tokens — an item a
lookup-table or fuzzy-matcher would likely misjudge.

## Findings

- Freshness finding about the lane's own citations: h05's round-24 quote is a
  summary, not verbatim (flagged `[summary-not-verbatim]` in the TSV); the tool
  correctly reports ABSENT. The h28 row in the same TSV shows the lane later
  corrected round-24's claim about Link Works ("verifies URL accessibility" →
  "assesses URL accessibility without LLM inference").
- No tool defect found in this slice. Contract limits (spans-two-blocks,
  ellipsis, paraphrase, PDF, case-folding) are explicitly not claimed and were
  not triggered here.

## Limits

3 items only, all reachable English HTML; no UNREACHABLE/NO_SOURCE/TOO_LONG
path exercised; network availability at run time affects reproducibility of
the exact numbers but not the blind-vs-tool comparison.

## Tooling installs

None. Used system `curl` (GET, allowed hosts only) and `python3`.
