# ScoutRegistryFetch — freshness reconnaissance of `corpus/SOURCES.md` (round 29, wave 1)

Question: for every registry row whose `source` cell holds an http(s) URL, what
does one bounded GET return, and would the frozen C1 contract mark the row
`UNREACHABLE`? Full evidence is `.ufo/waves/round-29/build/ScoutRegistryFetch/report.md`;
the machine-readable table is `registry-fetch.tsv` and the two scripts sit beside
it in the same directory.

What I ran: `timeout 590 python3 registry_fetch.py <tsv>` → EXIT=0, 18.56 s shell
wall, 45 registry rows over 31 URLs; then, after the registry grew mid-run,
`timeout 200 python3 registry_fetch_more.py <tsv>` → EXIT=0, `new_rows=4 drift=0`.
One GET per unique URL throughout: 40 URL-bearing rows over 35 URLs (5 duplicate
pairs inherit one record and were not re-fetched). Fetch semantics copied from
`c1-count.py` `fetch_text` and checked behaviorally equal to it (`SKIP`, `BLOCK`
31 elements, `QMAP`, `norm`, HTML extraction). Registry revisions: 45 rows,
sha256 `8bc103823c…`, then 49 rows, sha256 `d8aa0454b5…`; final TSV sha256
`ba73e4ce50…`; access date 2026-10-23 (UTC clock 2026-10-23T01:26:00Z); no proxy;
no installs.

Observed: 32 × 200, 2 × 203, 1 × 403; 33 × `text/html`, 2 × `application/pdf`; no
body over 8 MiB (largest 3,652,650 B); one same-host redirect (S025
`/rfc/rfc9111` → `/info/rfc9111/`, final 200 `text/html`).

Rows the contract marks UNREACHABLE — named limits, not failures:

| id | status | content type | bytes | gate |
|---|---:|---|---:|---|
| S011 | 200 | `application/pdf` | 3,652,650 | content type |
| S037 | 200 | `application/pdf` | 1,457,761 | content type |
| S014 | 403 | `text/html` | 919 | status not 2xx |

Reachable by the letter, degraded in substance: S021 and S022 return `203` (2xx,
so the contract calls them reachable) with a 2,207/2,206 B body yielding 17 words
— [INFERENCE] a bot interstitial, not the abstract; I retained no body, so I quote
nothing from it. A `status != 200` gate would wrongly emit UNREACHABLE there.
S047 returns 200 `text/html`, 68,837 B and **1 word** of extracted text: any quote
citing it comes back ABSENT. Cause is not separable here (no retained bytes):
either client-side rendering or a skip element left open — Python `html.parser`
implies no end tags, so a document that opens `<head>` and never writes `</head>`
has its whole body text dropped, which I reproduced on synthetic input with the
counter's own extractor (3 words → 0 words). Both causes fall inside the claim's
"Not claimed" boundary. Thin-text rows otherwise: S017 197 words, S026 283, S024/S031 94.
S046's URL carries a fragment, which the contract strips: the tool reads the whole
Recommendation (49,021 B, 17,538 words), not the fragment's section.

Bearing on C1's 130/130 target (feasibility, not a measurement): the frozen
fixture's 40 items reference only S002, S003, S008, S013, S019, S020, S038, S044
(all 200 `text/html`, 393 to 25,125 words) plus S001, S045, S999 as `NO_SOURCE`,
and the counter's runtime subspan/transpose/cross-attribution items stay inside
those same 8 ids. No item touches S011, S037, S014 or S046–S049. All 8 page-sampled
sources yield text, so none is hit by the extractor gap above. No registry-side
reachability blocker for C1 was found on 2026-10-23.

Unresolved: two-fetch page stability is untested under my one-GET-per-URL bound
(`page_cases()` raises `ValueError`, counter exit 2, if a source cannot yield 3
windows present in both fetches; S013 at 393 words is the tightest margin); no
bodies retained, so no quotes appear here; a row added after this revision needs
its own check; live pages can change after 2026-10-23.
