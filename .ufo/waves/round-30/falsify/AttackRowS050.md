VERDICT: pass — S050 quote verbatim at §8.1.2.4 (23 words); landed tool VERBATIM 1/1; row cells match the page except the "superseded" teaches premise is not on the page.

## (1) Page open + quote check
- Row read: `corpus/SOURCES.md:60` — source `https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html#optional-tags`, kind spec, tier A, scope "what the HTML 5.2 Recommendation text states about omitting the head end tag".
- Gate table `corpus/lessons/round-30.md:45` claims the quote; §8.1.2.4.
- Fetch (once, registered row URL): `timeout 120 curl -sS -L --max-redirs 0 -o s050.html -w 'HTTP %{http_code} %{size_download} bytes\n' 'https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html'` → `HTTP 200 4415303 bytes`, exit 0, `sha256sum` = `1db65aefdde4f6a728aefde0069110eac400814be988ad4259a38800fb25e141` (matches Gate table SHA prefix `1db65aef…e141`; 4415303 bytes matches).
- `<h5 data-level="8.1.2.4" id="optional-tags">` at line 775 of the page; the quote `"A head element’s end tag may be omitted if the head element is not immediately followed by a space character or a comment."` appears verbatim (curly apostrophe, `&`-free) in that section: `VERBATIM IN SECTION: True`, 23 words (≤25). Page `<title>` = "HTML 5.2: 8. The HTML syntax"; status line `HTML 5.2 W3C Recommendation, 14 December 2017` confirms the dated snapshot.
- Row cells vs page: tier A spec and the dated-W3C-snapshot scope match the page's own self-signature. The teaches cell's "superseded by the WHATWG HTML Standard, so not current HTML" is NOT on the page: page body has 0 occurrences of "superseded"/"supersede"/"is not current" (the 3 "WHATWG" hits are normative spec references). That premise is the miner's inference, not a page statement — flagging as a nit, not a verdict change (teaches = lesson derived from quote; quote itself is verbatim).

## (2) Landed tool run
- TSV `/fast/scratch/hyaku/chousa-r30/w2/AttackRowS050/s050-item.tsv`, header `id\tsource_id\tquote`, one row `S050-quote<TAB>S050<TAB>A head element’s end tag may be omitted if the head element is not immediately followed by a space character or a comment.`
- From `/home/vgpnk/Projects/shokunin/chousa-shokunin`: `timeout 120 python3 tools/quote-reopen.py verify --items /fast/scratch/hyaku/chousa-r30/w2/AttackRowS050/s050-item.tsv` → exit 0:
  - `QUOTE_REOPEN	S050-quote	VERBATIM	matched in normalized page text`
  - `QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0`

Result: VERDICT pass. Unknowns: none for the quote or tool; the only gap is the teaches-cell "superseded" premise, which the opened page does not state (page states it is a W3C Recommendation dated 2017-12-14; the redirect evidence for the undated URL lives in the Gate "Rejected source" block, not on this page).
