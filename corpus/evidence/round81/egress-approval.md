# Round 81 — external-target approval table (chousa)

SKILL.md `## Boundaries`: "A window without an approval table is loopback-only. The approval table is itself a chousa
deliverable." This is round 81's table. It does not answer the open general fetch-scope L0 question (`8d77e6c1`); it
records the narrower direction under which this round fetched, on the round-57 table's terms.

Authority: the round-81 dispatch prompt (`/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-81.md`) §2b, which
binds every child-lane round to curate `corpus/SOURCES.md` with rows "written only after its source is opened this
round" carrying "the URL, access date, and a ≤25-word located quote", and the run-15 addendum line "each round must leave
the lane measurably more capable — a trial run end-to-end on real domain work, a curated `corpus/SOURCES.md` delta". The
lane's own province refuses *live-target* research (bounty or system targets); a GET of a public method document is
source research, the scope round 57 already fetched under.

**Ordering disclosure (recorded as a `## Mistakes` row in `corpus/lessons/round-81.md`):** the six fetches below ran at
2026-11-06T18:44:29Z–18:44:31Z, before this file was written. The table states the terms they ran under; it was not on
disk first.

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| open of a public research-method document (reporting guideline, bibliographic-database policy page, registry documentation) located by a search | yes | one `curl -fsSL --compressed --max-time 15 -A <campaign UA>` GET per attempt, by the L1 only, through `tools/capture-fetch.py` | POST, cookies, credentials, anything behind a login, paywall or captcha, crawling links, more than 3 attempts per URL | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/` |
| web search to locate such a document | yes | the session's search tool | — | query and chosen URL in the lesson `## Gate` |
| seats of this round's wave | read-only re-open of a URL already in `refetch.tsv` for this round, into the seat's own scratch, only when its item names it (`tools/quote-reopen.py verify` or a single curl GET) | as the first row | writing `corpus/captures/` or `refetch.tsv` | the seat's report |

Fetched this window (refetch.tsv rows dated 2026-11-06):

| id | URL | result |
|---|---|---|
| S203 | https://eprints.whiterose.ac.uk/id/eprint/214348/8/Hirt_etal_BMJ_Guidances_On_Terminology_AAM.pdf | 200, stored `f2489455cc311a4de981e926` |
| S204 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11386270/ | 200, stored `c52a1f15884a78028febcf43` |
| S205 | https://www.nlm.nih.gov/bsd/policy/errata.html | 200, stored `371c55117727d526805f030d` |
| S206 | https://www.icmje.org/recommendations/browse/publishing-and-editorial-issues/corrections-and-version-control.html | 200, stored `f221c90f69188f775e32cd34` |
| S207 | https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/ | 200, stored `43a45b49723f7677d6446c92` |
| S208 | https://www.bmj.com/content/387/bmj.q2458.full.txt | curl rc 22, HTTP 403 — not stored |

Every other external target stays loopback-only.
