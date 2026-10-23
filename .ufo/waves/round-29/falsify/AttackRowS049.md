# AttackRowS049 — scoped source-row falsification

**Verdict: HOLDS for the S049 content, quotation, scope and requested live-tool check.** No counterexample to C1 was established by this seat; the frozen 130-item predicate was not run.

Axes: operability (requested quote re-opening), factual/source fidelity, scope discipline, provenance honesty and no-harm. No production files, frozen artifacts, Git index or jj state were changed.

## Independent source opening and cell verdicts

I opened only the permitted source URL, https://docs.python.org/3/library/html.parser.html, with `read`, including raw HTML ranges 100–175 and 176–275. It identifies itself as Python 3.15.1 documentation. The raw HTML contains `<dt class="sig sig-object py" id="html.parser.HTMLParser">`, followed by the `convert_charrefs=True` constructor and the quoted paragraph.

| S049 cell | Verdict | Evidence / qualification |
|---|---|---|
| id | OK | S049 is the registry identifier used by the entry and held-out input. |
| source | OK | The named Python documentation opens at exactly the registry URL. |
| kind | OK | `docs` accurately describes the official library documentation. |
| tier | OK | A is justified for Python's own documented API semantics, not for general HTML conformance. The lane's tier definition is primary/authoritative for the stated scope (`contextual-source-admission-r24.md:56–60`). |
| scope | OK | Narrowly character-reference conversion in HTMLParser, with an explicit general-conformance exclusion. |
| anchor | OK | Constructor and `convert_charrefs` exist; the knowledge entry's `#html.parser.HTMLParser` fragment has an actual HTML id. |
| teaches | OK | The page says conversion happens when `convert_charrefs` is true, except in elements like script and style. |
| status | OK | `mined` matches the actual quotation and use in the named knowledge entry. |
| opened | OK | Declared 2026-10-23 matches `.ufo/waves/round-29/build/ScribeSrcHtmlParser.md:4`; historical timing is not independently authenticated by the page. See date limit below. |
| recheck | OK | `on-release` is a declared lane cadence for versioned API documentation, not a purported statement by the page. |
| used-by | OK | `corpus/knowledge/quote-reopen-r29.md` cites S049 in its header and lines 43–46. |

Page text copied from the independent opening (display line wrapping retained):

> If convert_charrefs is true (the default), all character
> references (except the ones in elements like script and style) are
> automatically converted to the corresponding Unicode characters.

The knowledge entry's 20-word quote is the contiguous substring beginning “all character references” and ending “Unicode characters.” Its backticks around script/style represent inline code, not literal quote characters. Words, case, punctuation and parentheses match the page. Raw HTML places code tags inside the quotation, so this also exercises the claimed extraction rather than a raw-HTML substring match.

## Landed-tool execution

Created `.ufo/waves/round-29/falsify/AttackRowS049/items.tsv`, with a header and one S049 item containing the entry's rendered quotation. From `/home/vgpnk/Projects/shokunin/chousa-shokunin`, ran:

```sh
timeout 120 python3 tools/quote-reopen.py verify --items /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/AttackRowS049/items.tsv
```

Both executions returned the same successful output; the second appended `&& timeout 5 printf 'COMMAND_EXIT=0\n'` to expose the successful exit code explicitly:

```text
QUOTE_REOPEN	s049-entry-quote	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0
COMMAND_EXIT=0
```

Exit 0 / VERBATIM is right: I independently located the quotation in the source body and confirmed its anchor. This is not the S047 missing-head-end-tag failure; that page was not fetched or tested by this seat.

## Scope, strongest attempted counterexample and correction

The strongest checked counterexample was the entry's own quotation crossing inline code tags and line breaks. It survives extraction correctly. No S049 over-scope use was found: the entry attributes only character-reference conversion to S049. The following skip-element/block-element behavior is local tool behavior, corroborated by `tools/quote-reopen.py:58–109`, not a claim that S049 prescribes a general extraction policy. The omitted-head discussion is a separately labelled tool limitation, not a claim of HTML conformance derived from S049.

Smallest safe correction: none established for S049. Preserve the narrow API scope and do not treat this single passing case as proof of the frozen full predicate or universal HTML correctness.

Limits: the historical access-date assertion cannot be independently proven from a live page. The embedded date reminder says 2026-10-22, whereas `timeout 5 date -u +%FT%TZ` returned `2026-10-23T01:50:12Z` and the S049 source-opening report says 2026-10-23. `ScribeKnowledge.md:6` separately records its own opening on 2026-10-22; that does not rule out a later reopening. I therefore do not infer fabricated provenance or change dates from these conflicting clocks. The public documentation is mutable. No full-counter run, mutants, other source-row checks, or original-opening timestamp reconstruction was performed. No tools were installed or updated; no servers or background jobs were started.
