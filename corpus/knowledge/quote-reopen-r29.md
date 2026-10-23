# `quote-reopen.py verify` — re-open located quotes against their live source (round 29)

source: S046 https://www.w3.org/TR/annotation-model/#text-quote-selector §4.2.4 "Text Quote Selector"; S047 https://wicg.github.io/scroll-to-text-fragment/#context-terms §3.2.1 "Context Terms" and §3.6.1 "Finding Ranges in a Document" (algorithm `#find-a-string-in-range`); S048 https://unicode.org/reports/tr15/#Norm_Forms §1.2 "Normalization Forms"; S049 https://docs.python.org/3/library/html.parser.html#html.parser.HTMLParser constructor `convert_charrefs`; frozen contract `corpus/evidence/round29/claims.md` (design v3)
verified-at: 2026-10-23 UTC (round 29; local clock 2026-10-22, UTC-3; the four source passages were opened. The S046, S048 and S049 quotes below were re-located by the reference extractor of `corpus/evidence/round29/c1-count.py` and by the landed tool (`VERBATIM`). The S047 quote was located only by running the same extractor on the page body, because the full page extracts to empty text (the `</head>` limit below), and the tool returns `ABSENT` for it. The command's measured result is in SCORECARD.md, section "Round 29")
recheck: 180d (`python3 corpus/evidence/round29/c1-count.py -- python3 tools/quote-reopen.py verify` from the lane root; re-open S046 to S049 on a new release)

## What it does

`tools/quote-reopen.py verify --items ITEMS.tsv [--registry SOURCES.md]` reads
tab-separated items (`id`, `source_id`, `quote`). For each item it finds the
row of the lane registry `corpus/SOURCES.md`, fetches the first http(s) URL of
that row's `source` cell and reports whether the quote is located on the page.
It checks location only. It does not judge whether the quote supports a claim
or whether the source is true (QUALITY criterion 8 keeps those states apart).
It is the executable form of the frontier rule that a located quote is
re-opened against its source (CORPUS.md SOURCES rule 1; QUALITY criterion 25).

Run from the lane root:

```sh
python3 tools/quote-reopen.py verify --items <items.tsv>
```

Exit 0 means every item is `VERBATIM`; 1 means at least one item got another
verdict; 2 means a usage or I/O error. Output is one
`QUOTE_REOPEN<TAB>id<TAB>VERDICT<TAB>detail` line per item in input order,
then `QUOTE_REOPEN_SUMMARY`.

## Verdict order and why

1. `NO_SOURCE`: the id has no registry row, or the row has no http(s) URL.
   This ties every fetch to a source the lane already registered. The tool
   never fetches a URL taken from the item itself.
2. `TOO_LONG`: the quote has more than 25 words after normalization. This is
   the CORPUS.md limit for a located quote, and it is checked before any fetch.
3. `UNREACHABLE`: the fetch failed, the final status is not 2xx, the content
   type is not HTML, XHTML or plain text, or the body is over 8 MiB. PDF
   sources (S011, S037) and challenge pages (S014 answered 403) land here.
4. `VERBATIM` or `ABSENT`: the result of the match rule below.

## Extraction, normalization, match

- Text comes from Python `html.parser` with character references decoded.
  S049 states it: "all character references (except the ones in elements like
  `script` and `style`) are automatically converted to the corresponding
  Unicode characters." The tool drops `script`, `style`, `noscript`,
  `template` and `head` content and comments. A fixed list of block elements
  emits a space, so text from two blocks is not glued together. Inline markup
  emits nothing, so `<em>`, `<a>` or `<code>` inside a sentence does not
  break a quote. In the round-29 fixture, 9 of 14 true quotes cross inline
  markup. A raw-HTML substring search fails them; the control `CtlRawGrep`
  scored 93 to 100 of 130.
- NFKC, then typographic quotes are mapped to ASCII, soft hyphen and
  zero-width characters are deleted, and whitespace runs collapse to one space.
  This lets a quote typed with `'` match a page that has U+2019. S048 warns that
  "Normalization Forms KC and KD must not be blindly applied to arbitrary
  text." NFKC can make visibly different strings equal (for example a circled
  digit and a plain digit). So `VERBATIM` means "equal after these folds", not
  "byte-identical".
- Match: the normalized quote must occur with a non-alphanumeric character
  (or the page edge) on each side, case-sensitive. The boundary rule is what
  rejects a quote cut inside a word: the control `CtlCasefoldNoBoundary`, which
  drops it, lost exactly the 4 truncated-token items (126 of 130).

## Design choices measured against the sources

- S046 locates a quote by its exact text plus, optionally, "some of the text
  immediately before (a prefix) and after (a suffix) it to distinguish between
  multiple copies of the same sequence of characters." This tool has no prefix
  or suffix. It answers "is this text on the page", not "which copy".
- S047 says: "Context terms are used to disambiguate the target text
  fragment." Its search is case- and accent-insensitive with locale-aware
  word boundaries. This tool is deliberately stricter: it is case-sensitive,
  does not fold accents and uses a `str.isalnum` boundary. A quote that
  differs from the page only in case or accents is `ABSENT` here.
- The lane gate `tools/research-gate.sh` (claims mode, round 4 boundaries)
  matches local Markdown byte-exactly and has a hyphen and apostrophe joiner
  rule that this tool lacks. A quote cut right after `cross-` is `ABSENT` under
  the gate but `VERBATIM` here. The other differences (whitespace, NFKC,
  markup) follow from the different input. Reverse-engineered by seat
  `RevengerGateSpan` (`.ufo/waves/round-29/build/RevengerGateSpan.md`).

## Limits

- **Pages that omit `</head>`.** HTML lets a page leave out the `</head>` end
  tag. Python `html.parser` does not infer it, so the frozen "drop head
  content" rule drops the whole page. The S047 page
  (https://wicg.github.io/scroll-to-text-fragment/) has `<head>` and `<body>`
  but no `</head>`, so its extracted text is empty and every quote is `ABSENT`.
  That `ABSENT` comes from the tool, not from the source. It was found while
  verifying this entry's own S047 quote. The quote was then confirmed on the
  body text only, and the gap is a candidate for a later contract version.
- **Challenge pages read as `ABSENT`.** A bot or cookie gate that answers
  2xx with HTML (PubMed S021 and S022 answered 203) passes the reachability
  check. The quote is then `ABSENT` from the gate page, and that `ABSENT`
  cannot be told apart from true absence. A gate that answers 403 (S014) is
  `UNREACHABLE`. Read an `ABSENT` on such a source as "not re-opened".
- No prefix or suffix disambiguation, and no PDF or JavaScript-rendered pages.
- A true quote cut mid-sentence at a word boundary is still `VERBATIM`. The
  tool checks location, not that the quote is a complete sentence.
- Mutation testing in round 29 found three code paths the frozen fixture does
  not exercise. Each mutant scored 130 of 130: checking `TOO_LONG` after the
  fetch, keeping `script`/`style`/`head` text, and case-insensitive matching.
  The fixture has no unreachable over-long item, no hidden-text-only item and
  no case-only edit (`.ufo/waves/round-29/falsify/MutOrder.md`,
  `MutSkipScript.md`, `MutCasefold.md`).
- **The round-29 counter does not prove a live fetch.** It checks the tool's
  verdicts against the pages as they are at count time. A wave-2 critic built
  a cache-only verifier from page snapshots taken 27 minutes earlier. It made
  no network call and still scored 130 of 130 twice
  (`.ufo/waves/round-29/falsify/CriticClaimDesign.md`). The evidence that this
  tool re-opens pages live comes from elsewhere. The loopback conformance
  harness counts server hits per URL; with only the address guard disabled,
  the tool passed 65 of 65 checks (`falsify/OfflineConformance.md`). The rest
  is code review (`falsify/SentinelTool.md`, `falsify/SimplifierTool.md`, no
  cache file).
- A quote that crosses two block elements matches with one space between the
  blocks. That may not be how a reader sees it.
- The page can change after the access date. The tool keeps no snapshot.
- Fetch scope: GET only, registry URLs only, http and https only, with bounded
  time and size. Whether re-opening registered public documentation needs a
  per-window approval row under the lane's "loopback-only without approval
  table" boundary (SKILL.md, Boundaries) is filed as an L0 question in round 29.
  The tool fetches exactly what the frontier step already requires a round to
  open.

Measured result: see SCORECARD.md Round 29.
