# `quote-reopen.py verify` — live quote location check (round 29)

source: S046 https://www.w3.org/TR/annotation-model/#text-quote-selector §4.2.4 “Text Quote Selector”; S047 https://wicg.github.io/scroll-to-text-fragment/#context-terms §3.2.1 “Context Terms”; S048 https://unicode.org/reports/tr15/#Compatibility_Equivalence and https://unicode.org/reports/tr15/#Norm_Forms §§1.1–1.2 “Canonical and Compatibility Equivalence” and “Normalization Forms”; S049 https://docs.python.org/3/library/html.parser.html#html.parser.HTMLParser constructor `convert_charrefs`
verified-at: 2026-10-22 (read the frozen C1 v2 contract and opened the four cited source passages; the command implementation was not run)
recheck: 180d (re-open S046–S049 and compare with `corpus/evidence/round29/claims.md`)

## Behavior

The frozen C1 v2 contract defines `python3 tools/quote-reopen.py verify` as a live locator: it reads UTF-8, tab-separated item rows whose first row has the three cells `id`, `source_id`, and `quote`; resolves each source ID against the lane registry; fetches the registered source page; extracts page text; and reports whether the normalized quote occurs there. The default registry is `corpus/SOURCES.md` under the lane root, the parent of `tools/`. An explicit `--registry` path can override it. The tool checks location only; it does not judge why the quote matters.

Fetching is limited to registry URLs: use the first `http://` or `https://` URL in a source cell, remove its URL fragment, follow redirects only to HTTP(S) URLs, and send GET requests only. The contract sets a 30-second timeout, one retry, no cookies or credentials, and at most one fetch per URL per run; the User-Agent contains `chousa-quote-reopen`. A final non-2xx response, a failed fetch, an unsupported content type, or a body over 8 MiB is `UNREACHABLE`. Supported types are `text/html`, `application/xhtml+xml`, and `text/plain`.

Each item produces one tab-separated `QUOTE_REOPEN` record in input order, followed by a `QUOTE_REOPEN_SUMMARY` record with counts for `verbatim`, `absent`, `too_long`, `no_source`, and `unreachable`.

## Verdict order

1. `NO_SOURCE`: the ID is absent from the registry, or its `source` cell has no HTTP(S) URL. The first URL is used; trailing `.,;)` characters are stripped. This first gate ties retrieval to a declared source rather than to an arbitrary item URL.
2. `TOO_LONG`: the normalized quote has more than 25 whitespace-separated words. The length gate is checked before fetching, so rejected long quotes do not require page retrieval.
3. `UNREACHABLE`: fetching fails, the final status is not 2xx, the content type is not one of the three supported types, or the body exceeds 8 MiB.
4. `VERBATIM` or `ABSENT`: the quote either satisfies the normalized, boundary-limited match rule below or does not.

## Extraction, normalization, and match boundaries

For HTML and XHTML, the contract uses Python `html.parser` semantics and decodes character references. It drops comments and content inside `script`, `style`, `noscript`, `template`, and `head`; these are excluded by the contract's selected text-extraction boundary. Exactly these elements emit one space at both start and end: `p div li ul ol table tr td th h1 h2 h3 h4 h5 h6 br section article header footer nav pre blockquote dt dd dl figure figcaption hr main aside`. Those separators keep text in distinct blocks from being accidentally glued together. Every other element emits nothing, so inline markup does not itself interrupt a quote.

The same normalization is applied to page text and quote, in this order:

- Unicode NFKC: it makes compatibility-equivalent forms compare alike. This is a deliberate matching choice, not a universal rule for quotations; UAX #15 warns that compatibility normalization can erase meaningful distinctions.
- U+2018, U+2019, U+201A, and U+201B become ASCII apostrophe; U+201C, U+201D, U+201E, and U+201F become ASCII quotation mark. This treats typographic punctuation variants as the same punctuation for this locator.
- U+00AD, U+200B, U+200C, U+200D, and U+FEFF are deleted. These soft-hyphen, zero-width, joiner, and byte-order-mark characters otherwise can interrupt a visible-text match.
- Python `str.split()` whitespace runs become one ASCII space, then leading and trailing whitespace is removed. This makes layout whitespace, including line breaks, immaterial to the comparison.

A quote is `VERBATIM` only if it occurs in the normalized page text with a non-alphanumeric character on each side when that side exists; matching is case-sensitive. The outside-edge rule prevents a quote from matching as only part of a larger token, while still allowing a match at the page-text start or end. This is a simple `str.isalnum` boundary, not a full linguistic word-boundary algorithm. It rejects a word matched only as the start of a token whose next character is a digit, because digits are alphanumeric.

## How to run

CWD: the lane root, `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

```sh
python3 tools/quote-reopen.py verify --items corpus/fixtures/quote-reopen-r29/items.tsv
```

Exit code 0 means every item received `VERBATIM`; exit code 1 means at least one item received another verdict; exit code 2 means a usage or I/O error. The default registry is used unless an explicit registry file is supplied with `--registry corpus/SOURCES.md` or another path.

## Source excerpts

These excerpts were opened directly from the cited sources. They motivate scoped design choices; they do not make those sources requirements for this command.

- S046, §4.2.4: “including some of the text immediately before (a prefix) and after (a suffix) it to distinguish between multiple copies of the same sequence of characters.” https://www.w3.org/TR/annotation-model/#text-quote-selector (accessed 2026-10-22).
- S047, §3.2.1: “Context terms are used to disambiguate the target text fragment.” https://wicg.github.io/scroll-to-text-fragment/#context-terms (accessed 2026-10-22).
- S048, §1.2: “Normalization Forms KC and KD must not be blindly applied to arbitrary text.” https://unicode.org/reports/tr15/#Norm_Forms (accessed 2026-10-22).
- S049, `HTMLParser` constructor: “all character references (except the ones in elements like `script` and `style`) are automatically converted to the corresponding Unicode characters.” https://docs.python.org/3/library/html.parser.html#html.parser.HTMLParser (accessed 2026-10-22).

## Limits

- No prefix or suffix disambiguation: if the same boundary-valid quote appears more than once, the command does not select among those locations.
- No PDF parsing or JavaScript page rendering; content outside the supported types or over the body limit is unreachable.
- NFKC can merge distinct strings, including distinctions that matter in some contexts.
- A quote crossing block elements is not reliably reconstructed as a reader would see it; this extractor follows the fixed separator list above.
- The live page can drift after its access date, and the command does not preserve a historical page snapshot.
- `VERBATIM` means only that text was located under these rules; it is not claim support, source quality, or truth. Case-folded and paraphrased matches are not attempted.

Measured result: see SCORECARD.md Round 29.
