# COPE Retraction Guidelines — source opening

Opened 2026-10-21 for C2 (event-triggered rechecks).

## Access and located text

- Exact page: https://publicationethics.org/guidance/guideline/retraction-guidelines. The native page reader returned the page text (status not exposed); a separate `curl -L` GET returned `HTTP 403`, final URL unchanged. Thus the readable-page result and raw HTTP outcome differ; do not record this as HTTP 200.
- Official full-text link on that page: https://publicationethics.org/media/848/download?attachment. Both native reader and `curl -L` reported HTTP 403. The DOI reader returned Crossref metadata, not the guideline full text; it is not used as a mirror or for the quote.
- Page identifies the current guideline as version 3; it says “Last reviewed: 29 August 2025” and its change history says version 3 was published 4 September 2025.
- Quote (18 words), section “Importance of timely handling of retractions”: “retraction notices should be published as soon as the editor is confident that the publication is seriously flawed”. Exact section heading and wording are from the page text returned by the native reader. The underlying page/PDF's direct HTTP availability remains blocked as above.

## Registry check and proposed v1 row

- `corpus/SOURCES.md:43` is S033, the last current ID; the full registry read contains no COPE Retraction Guidelines row. Targeted search `S033|COPE.*Retraction|Retraction guidelines` returned the S033 line only. If assigned now, the next ID is S034.
- SOURCES contract v1 requires opened-source evidence, scoped tier and exact anchor; see `/home/vgpnk/Projects/shokunin/CORPUS.md:64-122`. Proposal only; no registry file changed. ID is left TBD as requested.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| TBD (next unused S034) | COPE Council, COPE Guidelines: Retraction Guidelines — https://publicationethics.org/guidance/guideline/retraction-guidelines | docs | A — authoritative for COPE's own editorial guidance | COPE's recommendation on how promptly journal editors should publish retraction notices after confidence in serious flaws; not general record-freshness policy | “Importance of timely handling of retractions”; version 3, published 2025-09-04; page last reviewed 2025-08-29 | COPE recommends prompt publication once the editor is confident the publication is seriously flawed; using this as a downstream metadata recheck trigger is a lane inference | queued | 2026-10-21 | on-release | — |

## What this source does not support

- QUALITY 7 requires a tiered source's scope to cover the admitted claim; use beyond this editorial scope must be labelled inference (`corpus/QUALITY.md:24-27`). This source does not prescribe polling, automatic rechecks, notification feeds, calendar due dates, or a metadata freshness algorithm. It only makes an editorial recommendation about retraction-notice timing; translating an observed correction/retraction release into a C2 recheck is a lane inference, not COPE's stated rule.
- QUALITY 8 keeps existence/opening, topicality, statement, and truth distinct (`corpus/QUALITY.md:28-31`). The returned page text establishes what this guideline says, not that any particular cited work has been corrected/retracted, that a notice is complete/available in a given system, or that an underlying research claim is true. Raw page and linked PDF GETs both returned 403, so public direct-fetch availability is unresolved despite the native reader returning text.

VERDICT: Useful tier-A evidence for COPE's editorial advice on timely retraction notices; only indirect, explicitly labelled support for event-triggered metadata rechecks. No duplicate registry row found; direct HTTP access returned 403 and the official PDF mirror also returned 403.
