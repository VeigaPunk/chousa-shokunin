# AttackRowS047 — round 29, wave 2

## Scope, axes, verdict

Attacked registry row `corpus/SOURCES.md:57`, its use in `corpus/knowledge/quote-reopen-r29.md`, and the landed command on that entry's S047 quotation. Axes: **operability** (primary), quotation fidelity, scoped authority, provenance, and no-harm.

**FALSIFIED, narrowly:** the entry's literal quotation changes the source's final period to a comma; its visible-page quotation also exposes the already-disclosed omitted-head extraction limit. The registry's recorded opening date conflicts with its source author's recorded opening. The substantive kind/tier/scope/teaching claims hold. This is **not a measured failure of the frozen C1 predicate**: I did not run or modify the counter; S047 is outside its 8 fixture source ids (`claims.md:73–76`). No canonical admission judgment is made.

## Every S047 cell

| Cell | Verdict | Evidence / qualification |
|---|---|---|
| id | OK | `S047` identifies the reviewed registry row and the entry cites that id. |
| source | OK | Opened https://wicg.github.io/scroll-to-text-fragment/ myself with both reader and raw HTML, then captured a bounded GET. Title and canonical URL match. The page identifies itself as a Draft Community Group Report dated 13 December 2023. |
| kind: `spec` | OK | It is an authored specification draft. Its status explicitly says it is not a W3C Standard or on the W3C Standards Track; the row correctly says WICG draft rather than Recommendation. |
| tier: `A` | OK | Primary authority for what this specification itself says, which is the row's restricted scope. This does not establish browser conformance, universal matching policy, or truth outside that scope. |
| scope | OK | Restricted to its own search, word-boundary and context-term behavior; explicitly excludes lane normalization policy. |
| anchor | OK | `#find-a-string-in-range`, `#word-boundaries` and `#context-terms` exist. Locator precision note: §3.6.1 is actually titled “Finding Ranges in a Document”; “find a string in range” is an algorithm within it, not that section's heading. The supplied locator nevertheless resolves unambiguously. |
| teaches | OK | The page describes base-character/UTS 10 primary-level comparison, explicitly glossed as case-insensitive and ignoring accents, umlauts and other marks; §3.6.2 makes boundaries locale-sensitive; §3.2.1 explains disambiguation with prefix/suffix context. |
| status: `mined` | OK | Structural use exists: the knowledge entry cites and discusses S047 at lines 3 and 71–75. This is not a statement that all of the entry is correct. |
| opened: `2026-10-23` | WRONG | As-of the supplied review date, this is future-dated. More importantly, `.ufo/waves/round-29/build/ScribeSrcTextFragments.md:3,7` explicitly records the author's actual opening as `2026-10-22` and warns against replacing it with the requested future date. A distinct later opening is not established by the evidence I opened. The source's 2023 publication date is a separate fact. |
| recheck: `365d` | OK | A valid lane-selected cadence, not a promise made by the page or proof that the draft cannot change. |
| used-by | OK | Names the existing `corpus/knowledge/quote-reopen-r29.md`, which actually uses the row. |

No out-of-scope use of S047 was found in the whole knowledge entry I read. Lines 71–75 explicitly contrast the specification with this tool's deliberately different case/accent/boundary choices. Lines 85–92 use the fetched page as an observed HTML example, not as authority for lane normalization. Tier A is therefore not inflated into W3C-standard status or a lane-policy mandate.

## Exact quotation: WRONG punctuation, correct proposition

Page text I see at [Context Terms](https://wicg.github.io/scroll-to-text-fragment/#context-terms), also captured in `falsify/AttackRowS047/page.html:1031`:

> Context terms are used to disambiguate the target text fragment.

The knowledge entry at lines 71–72 instead places `Context terms are used to disambiguate the target text fragment,` inside quotation marks. Its words agree, but the comma is not the page's period. The exact comma-ended string is absent even from body-only extraction. This is a quotation-fidelity defect, not a false claim about the purpose of context terms.

The `verified-at:` header at line 4 should not be read as demonstrating that every literal quotation below passed full-page reference extraction: the S047 limit at lines 85–92 expressly says otherwise. The source author's opening-date warning above also limits the header's `2026-10-23` provenance; the knowledge author's own handoff (`build/ScribeKnowledge.md:6`) records the same actual `2026-10-22` date.

## Landed-tool runs and correctness

Both commands ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Each TSV has the prescribed header and exactly 1 data row. The first preserves the entry's literal comma; the second independently uses the actual page's period to avoid mistaking a punctuation mismatch for the extractor defect.

```sh
timeout 120 python3 tools/quote-reopen.py verify --items /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/AttackRowS047/items.tsv
```

Observed exit **1**:

```text
QUOTE_REOPEN	s047-entry-literal	ABSENT	no match in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=0 absent=1 too_long=0 no_source=0 unreachable=0
```

For that literal comma-ended quote, **ABSENT is right**. However, the full-page parser cannot establish why it is absent: it extracts no text.

```sh
timeout 120 python3 tools/quote-reopen.py verify --items /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/AttackRowS047/items-source.tsv
```

Observed exit **1**:

```text
QUOTE_REOPEN	s047-page-literal	ABSENT	no match in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=0 absent=1 too_long=0 no_source=0 unreachable=0
```

For the period-ended page quotation, **ABSENT is wrong as a visible-source-location answer**, but consistent with the frozen extraction semantics. The existing Limits section correctly discloses this distinction; I found no concealment of that miss.

## Isolating the cause without changing production

Captured only the authorized URL, without following redirects:

```sh
timeout 120 curl --request GET --max-time 90 --fail --silent --show-error --output /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/AttackRowS047/page.html --write-out 'HTTP=%{http_code} URL=%{url_effective} SIZE=%{size_download}\n' https://wicg.github.io/scroll-to-text-fragment/
```

Output: `HTTP=200 URL=https://wicg.github.io/scroll-to-text-fragment/ SIZE=368361`. Successful completion; the tool did not display a numeric exit status.

An isolated scratch probe loaded the landed functions using `runpy.run_path`, without executing the CLI or writing bytecode, and compared the complete saved response with the substring beginning at its existing `<body>` start tag:

```sh
timeout 30 python3 -B /fast/scratch/hyaku/chousa-r29/w2/AttackRowS047/probe.py
```

Successful completion; the tool did not display a numeric exit status. Key output:

```text
head_start_tags=1
head_end_tags=0
body_start_tags=1
full_normalized_characters=0
body_normalized_characters=98413
page_quote_in_full=False
page_quote_in_body=True
entry_quote_in_full=False
entry_quote_in_body=False
```

This directly confirms the entry's omitted-`</head>` explanation. `_Text` increments its skip counter on `<head>` and never resets it on `<body>` (`tools/quote-reopen.py:75–101`). The reference extractor also has this skip-counter structure (`corpus/evidence/round29/c1-count.py:63–95`, inspected only). The exact visible quote cannot rescue a parser that discards every body text node.

## Smallest safe correction and limits

1. Correct the knowledge quotation to the page's period-ended sentence, or put editorial punctuation outside a truly verbatim substring. Keep both actual `ABSENT` observations and the extraction limitation.
2. Preserve the documented `2026-10-22` opening provenance; use `2026-10-23` only for a separately evidenced event. Make the header distinguish full-page tool results from body-only human confirmation.
3. Optionally sharpen the anchor wording to “§3.6.1, algorithm `#find-a-string-in-range`.” No tier downgrade or scope expansion is warranted by this review.
4. Do **not** silently repair the frozen extractor, change the claim/counter/fixture, or rescale C1. The omitted-head behavior is an explicit contract/coverage limitation, not demonstrated divergence from that frozen contract. An HTML-implied-head repair would require its own separately authorized specification and evidence.

Limits: one live S047 response was saved, in addition to reader/raw openings and the CLI's own GETs; no browser-runtime conformance was tested. The body-only probe is diagnostic, not a replacement oracle or claimed C1 run. No production edits, Git/jj commands, installs, subagents, servers, or background jobs were started; all shell commands were timeout-bounded. Only the required report and evidence in my allocated falsify directory were written in the lane; probe code is in my permitted scratch directory.
