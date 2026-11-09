# Round 97 — external-target approval table (chousa)

SKILL.md `## Boundaries`: a window without an approval table is loopback-only; the approval table is itself a
chousa deliverable. This table is the round-96 table (`corpus/evidence/round96/egress-approval.md`) narrowed to
this round's documents. It does not answer L0 `8d77e6c1` (fetch scope in general).

Context: the round-96 named limit — the PRESS 2015 checklist's own element wording is not held — names three
primary routes, and all three answered http 403 to a browser-UA GET from this host on 2026-11-09 before this
table was written (CADTH E&E PDF, CADTH Table 9 PDF, J Clin Epidemiol PDF; the core.ac.uk copy also 403), and
`web.archive.org` timed out (TCP connect to 207.241.237.3, 25 s and 120 s). The routes below are reproductions
of the checklist by third parties, opened as such and tiered as such.

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| the PRESS 2015 Evidence-Based Checklist as reproduced by Cochrane's editorial methods material (a two-page PDF that reprints the PRISMA-S checklist and the PRESS 2015 checklist for editors) | yes | one `curl` GET per attempt through `tools/capture-fetch.py`, by the L1 only: `https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf` | POST, cookies, credentials, crawling links, more than 3 attempts per URL, anything behind a login or captcha | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/<key>.raw/.txt`; the lesson `## Gate` line (URL, access date, located quote) |
| the same checklist as reproduced by Karolinska Institutet University Library's public guide page | yes | as the first row: `https://kib.ki.se/en/search-evaluate/systematic-reviews/press-2015-checklist-search-strategies` | as the first row | as the first row |
| one more attempt at the primary checklist (CADTH Table 9 PDF) so the route refusal is recorded by the tool, not only by the pre-table probe | yes, one attempt | as the first row: `https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Table_9-PRESS.pdf` | as the first row; a challenge page is a failed attempt, never a capture | as the first row |
| web search to locate the documents above | yes | the session's search tool | — | queries `PRESS Peer Review of Electronic Search Strategies 2015 Guideline Explanation and Elaboration CADTH PDF` and `"orphan lines" "PRESS 2015" checklist "Are there any spelling errors" "Translation of the research question"` in the lesson `## Gate` |
| seats of this round's wave | read-only re-open of the same URLs into the seat's own scratch, only when its item names it | as the first row | writing `corpus/captures/` or `refetch.tsv` | the seat's report |

Every other external target stays loopback-only. `tools/search-rerun.py` (including its `--selftest` mode)
reads only committed lane files and never opens a socket.
