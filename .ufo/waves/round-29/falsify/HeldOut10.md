# HeldOut10 — held-out generalization attack on C1

**Verdict: HOLDS.** 3/3 items agree between blind reading and tool output. No
tool defect found; no freshness defect found (the lane's earlier inexact S006
citation was already self-corrected in lessons/round-25.md).

## Method

STEP 1 (blind, before running the tool): fetched each registry URL once each
with `curl -sSL` (GET only, UA `chousa-quote-reopen-heldout10-blind`) into my
scratch dir, extracted text with a contract-faithful scratch parser
(`/fast/scratch/hyaku/chousa-r29/w2/HeldOut10/blind_extract.py`: html.parser,
drop script/style/noscript/template/head + comments, v2 block-element list
emits one space, NFKC + curly-to-straight + zero-width delete + whitespace
collapse, case-sensitive, non-alnum boundary), and judged by reading.

STEP 2: wrote the 3 rows to `.ufo/waves/round-29/falsify/HeldOut10/items.tsv`
and ran `timeout 300 python3 tools/quote-reopen.py verify --items ...` from the
lane root.

## Per-item evidence

### h28 — S006 (`https://arxiv.org/html/2605.06635v1`), HTTP 200 text/html, 140546 bytes
- Quote: `Link Works assesses URL accessibility without LLM inference` (8 words)
- Blind: VERBATIM — one boundary-clean hit at normalized-text offset 17399,
  inside §3.3.1: `...3.3.1 Link Works |Link Works assesses URL accessibility
  without LLM inference|. For each cited URL...`
- Tool: `QUOTE_REOPEN h28 VERBATIM matched in normalized page text` → **AGREE**
- Freshness note: the older quote at lessons/round-24.md:53 (`Link Works
  verifies URL accessibility...`, also present on the page at offsets 1993 and
  5806) was flagged by the lane itself as summary-not-verbatim and corrected in
  lessons/round-25.md lines 94–99 to exactly this h28 string. h28 is the
  corrected verbatim quote; it re-opens cleanly.

### h29 — S037 (Cochrane LSR guidance PDF), HTTP 200 `application/pdf`, 1457761 bytes
- Quote: `updated on a fixed-interval schedule approved by the editorial team
  (e.g. every four months).` (14 words)
- Blind: UNREACHABLE under the contract (content type `application/pdf` is not
  `text/html`/`application/xhtml+xml`/`text/plain`). Reading check via
  `pdftotext -f 18 -l 20`: the true text is present verbatim on p. 19 —
  `...the LSR results will be updated on a fixed-interval schedule approved by
  the editorial team (e.g. every four months).` — so the lane's round-26
  citation is exact, not inexact.
- Tool: `QUOTE_REOPEN h29 UNREACHABLE content type application/pdf` → **AGREE**
- Attribution: contract limit, not a defect — claims.md "Not claimed"
  explicitly excludes PDF sources.

### h30 — S038 (`https://docs.python.org/3/library/datetime.html`), HTTP 200 text/html, 430114 bytes
- Quote: `Return the proleptic Gregorian ordinal of the date, where January 1
  of year 1 has ordinal 1.` (17 words)
- Blind: VERBATIM — one hit at normalized-text offset 19417 under
  `date.toordinal()`: `...date.toordinal()¶ |Return the proleptic Gregorian
  ordinal of the date, where January 1 of year 1 has ordinal 1.| For any date
  object d...`
- Tool: `QUOTE_REOPEN h30 VERBATIM matched in normalized page text` → **AGREE**

## Result

Tool output (exit 1, correct since not all items are VERBATIM):

```
QUOTE_REOPEN	h28	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h29	UNREACHABLE	content type application/pdf
QUOTE_REOPEN	h30	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=2 absent=0 too_long=0 no_source=0 unreachable=1
```

3/3 AGREE. The tool generalizes to items never in the 130-item fixture:
verbatim location works on a live arXiv HTML page and a live docs.python.org
page, and a PDF registry row is correctly refused per contract.

## Limits

- 3 items only; all are VERBATIM-or-UNREACHABLE — no held-out item exercised
  the ABSENT, TOO_LONG, or NO_SOURCE branches against a fresh page.
- Blind extraction was my own scratch re-implementation of the contract; a
  shared bug in my reading and the tool cannot be excluded for h28/h30, but
  the located page text shown above is quoted verbatim from the fetched bytes.
- Fetches were one GET each; no retry behavior exercised.

## Tools installed

None. Used host-provided `curl`, `python3` (stdlib html.parser/unicodedata),
and `pdftotext` (`/usr/bin/pdftotext`). No pacman transactions.
