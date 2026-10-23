VERDICT: pass — S051 Gate quote verbatim (16 words) at the named branch; tier/scope/teaches match the page; landed tool verify returns VERBATIM, exit 0.

## (1) Source check — row S051 (SOURCES.md:61)
- URL: https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html#the-in-head-insertion-mode
- Fetched once: `timeout 120 curl -sS -o s051-syntax.html -w "HTTP %{http_code} bytes %{size_download}\n" "…"` → HTTP 200, 4415303 bytes; SHA-256 prefix `1db65aef…` matches the Gate receipt (4415303 bytes, `1db65aef…e141`).
- Section found: `<h6 … data-level="8.2.5.4.4" id="the-in-head-insertion-mode">` — "The 'in head' insertion mode" (8.2.5.4.4).
- Branch "Anything else" (dt data-md "Anything else") contains exactly: `Pop the current node (which will be the head element) off the stack of open elements.` Tag-stripped text is character-identical to the Gate quote; 16 words (<=25). Verbatim confirmed.
- Cell truth vs page:
  - tier A spec: dated W3C Recommendation snapshot, normative spec — yes.
  - scope "tree-construction rules of the in head insertion mode; the head boundary only, not fetch behavior or quote verification": the section defines only in-head tree-construction; nothing about fetch/verification — not more.
  - teaches: whitespace branch → "Insert the character" (stays in head); the listed head start tags (base, basefont, bgsound, link, meta, title, noscript, noframes, style, script, template) are the handled start-tag branches; "Anything else" pops head ("Switch the insertion mode to 'after head'. Reprocess the token.") — matches.

## (2) Landed tool run
- Tool at tip a9d3a05 (`git log --oneline -1`); sha256sum tools/quote-reopen.py = 47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201 (matches the frozen hash).
- One-item TSV written to scratch `/fast/scratch/hyaku/chousa-r30/w2/AttackRowS051/s051-items.tsv`: header `id<TAB>source_id<TAB>quote`, row `s051-q1<TAB>S051<TAB>Pop the current node (which will be the head element) off the stack of open elements.`
- Ran from lane root: `timeout 120 python3 tools/quote-reopen.py verify --items /fast/scratch/hyaku/chousa-r30/w2/AttackRowS051/s051-items.tsv`
  Output:
  `QUOTE_REOPEN	s051-q1	VERBATIM	matched in normalized page text`
  `QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0`
  Exit 0 (all-verbatim).

## Notes
- No installs performed (curl/python3 present). GET only to the registered URL, one fetch. No other lane files touched; report is the only lane write. Predictable attacker: none (page unchanged, same bytes/hash as Gate).
