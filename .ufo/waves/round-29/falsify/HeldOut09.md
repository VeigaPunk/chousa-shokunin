# HeldOut09 — wave-2 falsify, held-out generalization attack on C1

**Verdict: HOLDS** (3/3 held-out items AGREE: blind contract reading == tool verdict)

## What I attacked

C1 (`tools/quote-reopen.py verify`) on 3 items never in the fixture:
`.ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv` rows h25 (S026),
h26 (S027), h27 (S028), cited in lessons/round-25.md:75-77.

## STEP 1 — blind verdicts (before running the tool)

Method: opened each registry URL in `corpus/SOURCES.md` with the `read` tool
(GET, 2xx, text/html for all three), then fetched the same three URLs once each
with curl into scratch and simulated the frozen contract (html.parser, drop
script/style/noscript/template/head/comments, exact v2 block list emits space,
NFKC + quote/dash/space normalization, case-sensitive, non-alnum boundary).

| item | source | words | blind verdict | basis |
|---|---|---|---|---|
| h25 | S026 https://www.gofair.foundation/r1-2 | 20 | VERBATIM | Page DOM text (outside script JSON — checked): "Detailed provenance includes facets such as how the resource was generated, why it was generated, by whom, under what conditions, using what starting-data or source-resource, …". Simulated match at offset 470, before=' ' after=',' |
| h26 | S027 https://en.wikipedia.org/wiki/Wikipedia:As_of | 12 | VERBATIM | Raw-HTML DOM text contains "use the {{Update after}} template to indicate when it should be updated." (API markdown also shows it). Simulated match, before=' ' after=' ' |
| h27 | S028 https://www.crossref.org/services/crossmark/ | 8 | VERBATIM | Intro paragraph: "…has been updated, corrected, or retracted. Crossmark makes this information more visible to readers. With one click,…". Simulated match at offset 4225, before=' ' after=' ' |

None TOO_LONG (≤20 words), none UNREACHABLE, all ids registered with http(s) URLs.

## STEP 2 — tool run

`cd /home/vgpnk/Projects/shokunin/chousa-shokunin && timeout 300 python3 tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/HeldOut09/items.tsv`

```
QUOTE_REOPEN	h25	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h26	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h27	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=3 absent=0 too_long=0 no_source=0 unreachable=0
```

exit 0. Per item: h25 AGREE, h26 AGREE, h27 AGREE. No DISAGREE to adjudicate.

## Freshness check on the lane's own citations

- No held-out item is ABSENT → no inexact-citation finding that flips a verdict.
- Observation only: h25's lane quote (lessons/round-25.md:75) is a mid-sentence
  truncation — the page sentence continues ", using what starting-data or
  source-resource, using what funding/resources, …". Under the contract it is
  still VERBATIM (`,` is a non-alnum boundary), so this is a fidelity nuance in
  the lane's prose (sentence clipped without ellipsis), not a contract defect.

## Notes / limits

- h26 exercises `{{`/`}}` braces through normalization: matched, no defect.
- h26 also shows the tool handles Wikipedia raw HTML (not the API markdown my
  `read` used): `{{Update after}}` sits in inline DOM text and survives.
- Coverage exercised: VERBATIM path only; no PDF/non-2xx/UNREACHABLE/NO_SOURCE/
  TOO_LONG case in this slice.
- No installs needed (python3, curl present). No lane files mutated; items.tsv +
  this report only. Fetches were GET-only to registry URLs (read tool + 3 curls
  in scratch, plus the tool's own run).
