# Round 96 — external-target approval table (chousa)

SKILL.md `## Boundaries`: a window without an approval table is loopback-only; the approval table is itself a
chousa deliverable. This table is the round-95 table (`corpus/evidence/round95/egress-approval.md`) narrowed to
this round's documents. It does not answer L0 `8d77e6c1` (fetch scope in general).

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| open of the PRESS 2015 guideline that the registered source S222 (PRISMA-S item 14 and its glossary) names as the instrument for search peer review: the CADTH PRESS 2015 Explanation and Elaboration report (public PDF on the agency's own host) | yes | one `curl` GET per attempt through `tools/capture-fetch.py`, by the L1 only: `https://www.cda-amc.ca/sites/default/files/pdf/CP0015_PRESS_Update_Report_2016.pdf` | POST, cookies, credentials, crawling links, more than 3 attempts per URL, anything behind a login or captcha | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/<key>.raw/.txt`; the lesson `## Gate` line (URL, access date, located quote) |
| fallback route for the same guideline if the CADTH GET fails: the PRESS 2015 updated guideline statement in the open-access Journal of the Canadian Health Libraries Association, `https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210` | yes, only after a failed first row | as the first row | as the first row | as the first row |
| the guideline statement itself (McGowan J, Sampson M, Salzwedel DM, Cogo E, Foerster V, Lefebvre C, J Clin Epidemiol 2016;75:40-46, doi 10.1016/j.jclinepi.2016.01.021), the primary document the JCHLA abstract points at | yes, one attempt | as the first row: `https://www.jclinepi.com/article/S0895-4356(16)00058-5/pdf` | as the first row; a captcha or login page is a failed attempt, never a capture | as the first row |
| re-open of S222's Systematic Reviews co-publication front matter (round-95 spot-check D4: the row's "10:39" locator is true but unsupported by the lane's capture) via Europe PMC REST full-text XML for PMC7839230 | yes | as the first row (the round-95 route; it answered http 500 then and http 200 to the round-95 closure) | as the first row | as the first row; the round-96 lesson `## Gate` records the volume/elocation elements found |
| re-open of the PRISMA-S publisher PDF (S222's capture route) for a second, separately scoped registry row on its items 14 (search peer review) and 16 (deduplication): S222's scope cell excludes search quality and its anchor names items 8, 9, 12, 13 and 15 only, and its cells are append-only (CORPUS rule 2) | yes | as the first row: `https://jmla.pitt.edu/ojs/jmla/article/download/962/1274` (content-addressed: an unchanged PDF rewrites identical bytes under key `1a8c36c4c24444967bd9c3ce`) | as the first row | as the first row; the lesson `## Gate` records whether the raw and text digests equal S222's |
| web search to locate the documents above | yes | the session's search tool | — | query `PRESS Peer Review of Electronic Search Strategies 2015 Guideline Statement McGowan full text PDF` and the chosen URLs in the lesson `## Gate` |
| seats of this round's wave | read-only re-open of the same URLs into the seat's own scratch, only when its item names it | as the first row | writing `corpus/captures/` or `refetch.tsv` | the seat's report |

Every other external target stays loopback-only. `tools/search-rerun.py` (including the `--selftest` mode this
round adds) reads only committed lane files and never opens a socket.
