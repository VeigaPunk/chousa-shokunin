# HeldOut04 — held-out generalization attack on C1 (items h10, h11, h12)

**Verdict: HOLDS.** On three held-out located quotes (never in the fixture), the tool's
verdicts agree with independent blind readings under the frozen contract for all 3 items.
No DISAGREE; no tool defect; no lane misquotation found.

## Items (from .ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv)

| id | source_id | registry URL | quote (normalized words) |
|---|---|---|---|
| h10 | S011 | https://trec.nist.gov/pubs/trec34/papers/Overview_rag.pdf | Each sentence in a generated answer is checked against its cited document to verify factual grounding (16) |
| h11 | S012 | https://aclanthology.org/2026.acl-long.1586/ | labels and rationales remain revisable: when a verifier disagrees with the current benchmark, it submits evidence (17) |
| h12 | S013 | https://jsonlines.org/ | If a line terminator follows the last JSON value in a file, it must be the last byte in the file (18) |

## STEP 1 — blind verdicts (recorded BEFORE running the tool)

Blind method: one bounded GET per registry URL (`curl -sIL` for status/type, `curl -s`
for body, `chousa-quote-reopen` User-Agent, timeout <= 90 s), then an independently
written extractor (`/fast/scratch/hyaku/chousa-r29/w2/HeldOut04/blind.py`) that follows
claims.md verbatim: html.parser with convert_charrefs, SKIP = script/style/noscript/
template/head, the v2 fixed BLOCK list emitting one space, NFKC + QMAP + whitespace
collapse, case-sensitive find with non-alphanumeric boundaries.

Status headers (all 200): `S011 ... HTTP 200 content_type application/pdf`,
`S012 ... HTTP 200 content_type text/html; charset=utf-8`,
`S013 ... HTTP 200 content_type text/html`.

- **h10 → UNREACHABLE** (blind). Final Content-Type `application/pdf` is not in the
  contract's allowed set {text/html, application/xhtml+xml, text/plain}; verdict order
  makes it UNREACHABLE before matching. Out-of-contract freshness check: `pdftotext`
  on the downloaded PDF (21 pages) shows lines 97–98:
  `3. Support Evaluation: Each sentence in a generated answer is checked against its cited document` / `to verify factual grounding.` — the lane's quote is verbatim
  in the real document (across one line break). UNREACHABLE here is the declared "not
  claimed: PDF sources" limit, not a tool defect and not a lane misquotation.
- **h11 → VERBATIM** (blind). Page text contains:
  `... in which labels and rationales remain revisable: when a verifier disagrees with the current benchmark, it submits evidence; an auditor adjudicates the dispute; ...`
  Boundaries: `'h '` before (space, non-alnum) and `';'` after (non-alnum).
- **h12 → VERBATIM** (blind). Page text contains:
  `... easier. If a line terminator follows the last JSON value in a file, it must be the last byte in the file. Conventions ...`
  Boundaries: space before, `'.'` after.

## STEP 2 — tool run

items.tsv written to `.ufo/waves/round-29/falsify/HeldOut04/items.tsv` (header
`id\tsource_id\tquote`, 3 rows). Command from lane root:

    timeout 300 python3 tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/HeldOut04/items.tsv

Output (exit 1, correct since not all items VERBATIM):

    QUOTE_REOPEN	h10	UNREACHABLE	content type application/pdf
    QUOTE_REOPEN	h11	VERBATIM	matched in normalized page text
    QUOTE_REOPEN	h12	VERBATIM	matched in normalized page text
    QUOTE_REOPEN_SUMMARY verbatim=2 absent=0 too_long=0 no_source=0 unreachable=1

## Comparison

| id | blind | tool | result |
|---|---|---|---|
| h10 | UNREACHABLE | UNREACHABLE | AGREE |
| h11 | VERBATIM | VERBATIM | AGREE |
| h12 | VERBATIM | VERBATIM | AGREE |

## Freshness / citation-quality finding

None of the 3 held-out quotes is absent because of inexact lane quoting. h11 and h12
are verbatim in the live pages; h10 is verbatim in the live PDF's text (normalized
across a line break). The lane's round-24 Gate quotations for S011/S012/S013 are exact
under the frozen normalization.

## Limits

- Blind extraction was checked against claims.md, not against the counter's own
  reference functions byte-for-byte; both use html.parser semantics and the frozen
  BLOCK list, so divergence risk is low [INFERENCE].
- One fetch per page; pages could change between my read and later runs. Both HTML
  pages are static (ACL Anthology bib page, jsonlines.org).
- Only the 3 assigned held-out items were tested; no claim about the other 30 rows.
- No tools were installed; nothing in the lane outside
  `.ufo/waves/round-29/falsify/HeldOut04/` was written.
