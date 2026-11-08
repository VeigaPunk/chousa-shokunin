# Round 95 — external-target approval table (chousa)

SKILL.md `## Boundaries`: a window without an approval table is loopback-only; the approval table is itself a
chousa deliverable. This table is the round-57 table (`corpus/evidence/round57/egress-approval.md`) narrowed to
this round's one document. It does not answer L0 `8d77e6c1` (fetch scope in general).

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| fallback route for the same document after the Europe PMC GET answered http 500 (attempt 1, 2026-11-08T22:51:19Z) | yes | the publisher's own PDF of the JMLA co-publication, `https://jmla.pitt.edu/ojs/jmla/article/download/962/1274` (DOI 10.5195/jmla.2021.962; the same journal host whose download route S117 already captured), same tool and limits | as the first row | as the first row; the lesson `## Gate` names which route's bytes the quotes are located in |
| open of the public document two registered sources cite by name: PRISMA-S (Rethlefsen et al., Systematic Reviews 2021;10:39), named by S117's title and by S120's §4 statement that Cochrane search reporting aligns with PRISMA-S | yes | Europe PMC REST full-text XML for PMCID PMC7839230 (the route S078 used for another open-access paper), one `curl` GET per attempt through `tools/capture-fetch.py`, by the L1 only | POST, cookies, credentials, crawling links, more than 3 attempts per URL, anything behind a login or captcha | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/<key>.raw/.txt`; the new row's lesson `## Gate` line (URL, access date, located quote) |
| web search to locate that document | yes | the session's search tool | — | query `PRISMA-S extension for reporting literature searches Rethlefsen 2021 Systematic Reviews PMC` and the chosen URL in the lesson `## Gate` |
| seats of this round's wave | read-only re-open of the same URL into the seat's own scratch, only when its item names it | as the first row | writing `corpus/captures/` or `refetch.tsv` | the seat's report |

Every other external target stays loopback-only. The search-rerun tool this round builds (`tools/search-rerun.py`)
reads only committed lane files and never opens a socket.
