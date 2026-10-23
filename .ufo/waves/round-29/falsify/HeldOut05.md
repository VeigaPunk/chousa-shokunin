# HeldOut05 — held-out generalization attack on C1 (h13/S014, h14/S015, h15/S016)

Verdict: **C1 HOLDS** within this scope. The tool generalized to 3 never-fixtured
items: 2 VERBATIM agreed with blind reading; the 1 disagreeing item is a
contract-correct UNREACHABLE caused by an upstream WAF, not a tool defect.

## Method (blind first, then tool)

STEP 1 — blind: opened each registry URL with the `read` tool (remote render for
S014/S015, Wikipedia API for S016), judged the quoted text under the frozen
contract (NFKC, curly→straight quotes, whitespace collapse, case-sensitive,
non-alnum boundary) and wrote verdicts before running anything.

STEP 2 — wrote `.ufo/waves/round-29/falsify/HeldOut05/items.tsv` (header
`id\tsource_id\tquote`, 3 rows) and ran, from the lane root:

```
timeout 300 python3 tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/HeldOut05/items.tsv
```

Observed output (exit 1, contract-correct since not all VERBATIM):

```
QUOTE_REOPEN	h13	UNREACHABLE	HTTP 403
QUOTE_REOPEN	h14	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h15	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=2 absent=0 too_long=0 no_source=0 unreachable=1
```

Output grammar matches the contract (one `QUOTE_REOPEN` line per item in input
order, then the five-field summary line).

## Per-item comparison

### h13 / S014 — DISAGREE: blind VERBATIM, tool UNREACHABLE. Tool is right; environment changed.

- Blind page text (read tool, jina path): "This must be read before using the
  Levels: **no evidence ranking system or decision tool can be used without a
  healthy dose of judgement and thought**." — exact, 18 words, boundaries `:` /
  `.`. Blind verdict VERBATIM.
- Tool verdict `UNREACHABLE  HTTP 403`. Independent probe:
  `curl -s -o /dev/null -w '%{http_code}'` returns **403** with both default and
  the tool's `chousa-quote-reopen/1.0` User-Agent; response headers show
  `server: CloudFront`, `x-cache: Error from cloudfront`, an AWS WAF captcha CSP,
  919-byte challenge body. www.cebm.ox.ac.uk now refuses direct programmatic GET.
- Adjudication: contract rule 3 makes a non-2xx final status `UNREACHABLE`. The
  tool did exactly that; my blind fetch succeeded only through a remote
  rendering proxy the GET-only contract cannot use. **Not a defect — a contract
  limit plus an environment change.**
- Freshness finding about the lane's own citation: S014 was opened 2026-10-19;
  by 2026-10-23 its registry URL is WAF-blocked to direct GET, so the lane's own
  tool can no longer re-open this cited source even though the quoted text is
  still served on the live page. The quote itself is not inexact — the text is
  verbatim on the page.

### h14 / S015 — AGREE: VERBATIM.

- Page text (Limitations): "It can sometimes hallucinate facts in responses or
  make incorrect inferences, though at a notably lower rate than existing
  ChatGPT models, according to internal evaluations." The held-out quote is the
  verbatim prefix ending at "rate"; the next char is a space → boundary holds.
- Contract observation (not a defect): the non-alnum boundary rule accepts a
  quote that is a mid-sentence prefix of the page text, so a sentence truncated
  without ellipsis is indistinguishable from a complete verbatim quote. The
  lane's round-24 Gate row quotes exactly this truncated span.

### h15 / S016 — AGREE: VERBATIM.

- Page text (Criticism): 'Blunt further concludes that "hierarchies are a poor
  basis for the application of evidence in clinical practice", since…' — exact
  quote inside the page's own double quotation marks; boundaries `"` / `"`.
  Matching is case-sensitive and the fixture's lowercase start matches.

## Findings by severity

1. **No tool defect found.** All 3 verdicts follow the frozen contract; the lone
   DISAGREE is decided in the tool's favor (403 → UNREACHABLE is mandated).
2. **Environment/freshness finding (lane citation, not the tool):** S014's URL is
   now behind a CloudFront/AWS WAF challenge; direct GET yields 403. The lane
   opened it 2026-10-19; its own re-open tool can no longer reach it. Quotes
   remain verbatim on the rendered page.
3. **Contract property noted:** verbatim-prefix acceptance (h14) — a quote cut
   mid-sentence without an ellipsis passes VERBATIM. Documented boundary of the
   contract; the fixture already covers truncation only via mid-word cuts
   (`absent-truncated-token`), not word-boundary truncation.

## Residual risk and verification gaps

- Only 3 held-out items exercised; VERBATIM and UNREACHABLE paths covered on
  live pages, TOO_LONG / ABSENT / NO_SOURCE paths not exercised here (the 130-item
  predicate covers them).
- For h13, blind VERBATIM rests on the rendered page text; the raw HTML body
  could not be fetched because the WAF blocks direct GET — presence in raw HTML
  is [INFERENCE] (high confidence: the challenge page proves reachability of the
  host, and the content page renders the sentence).
- h14/h15 blind verdicts are confirmed by the tool's own successful extraction,
  so blind-vs-tool agreement there is direct.

## Tooling record

No installs or updates performed. Used: python3 stdlib (tool itself), curl
(pre-installed, GET-only probes to the registry URL).

Report: .ufo/waves/round-29/falsify/HeldOut05.md
