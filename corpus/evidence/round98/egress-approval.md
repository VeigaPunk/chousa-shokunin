# Round 98 — external-target approval table (chousa)

SKILL.md `## Boundaries`: a window without an approval table is loopback-only; the approval table is itself a
chousa deliverable. This table is the round-97 table (`corpus/evidence/round97/egress-approval.md`) narrowed to
this round's documents. It does not answer L0 `8d77e6c1` (fetch scope in general). Its first four rows (CADTH
appendices, CADTH main PDF, web search, and the seats row, now last) were written before any round-98 GET; the
PubMed, NCBI Bookshelf and Europe PMC rows were appended after the GETs their own text names, each before its own
GET (corrected at F2 after `R98ScribeLesson`'s note: this sentence first said the whole table preceded every GET).

Context: SCORECARD `## Planned — round 98` item 2 — the PRESS 2015 checklist is held only through two third-party
reprints (S225 tier B, S226 tier C); the primary routes answered 403 in round 97; `R97ScoutSources` §4 names one
untried CADTH route, the appendices PDF of CADTH report 477 (search snippet "APPENDIX G: PRESS CHECKLIST").

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| CADTH report 477 appendices (the PRESS 2015 guideline's own CADTH publication) | yes, at most 3 attempts | one `curl` GET per attempt through `tools/capture-fetch.py`, by the L1 only: `https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Report%20477_PRESS_Peer%20Review%20of%20Electronic%20Search%20Strategies_Appendices.pdf` | POST, cookies, credentials, crawling links, anything behind a login or captcha (a challenge page is a failed attempt, never a capture) | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/<key>.raw/.txt`; the lesson `## Gate` line (URL, access date, located quote) |
| the CADTH report 477 main PDF, only if the appendices PDF names it as the location of the checklist text | yes, at most 3 attempts | as the first row, URL taken from the appendices PDF or the CADTH resource page as found by web search | as the first row | as the first row |
| web search to locate the documents above | yes | the session's search tool | — | queries in the lesson `## Gate` |
| the PRESS 2015 guideline statement's PubMed record (its own published abstract; the full text stayed 403 in round 97) — added after the CADTH appendices GET answered 403 (attempt 1, `refetch.tsv`), before any GET below | yes, at most 3 attempts | as the first row: `https://pubmed.ncbi.nlm.nih.gov/27005575/` | as the first row | as the first row |
| the AHRQ methods research report "Peer Review of Search Strategies" on NCBI Bookshelf (an agency report on search peer review practice, the round-96/97 entries' topic) — added at the same time | yes, at most 3 attempts | as the first row: `https://www.ncbi.nlm.nih.gov/books/NBK98350/` and, if that page is a chapter only, the report's other Bookshelf chapter pages it links (each counted as its own URL) | as the first row | as the first row |
| the PRESS 2015 guideline statement's abstract as indexed by Europe PMC's public REST API (core record, JSON) — added after both NCBI GETs returned challenge pages (`refetch.tsv` S229 http 203 "Cookies must be enabled", S230 http 200 reCAPTCHA "Checking your browser"; both bytes are challenge pages, failed attempts, never cited) | yes, at most 3 attempts | as the first row: `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json` | as the first row | as the first row |
| seats of this round's wave | read-only re-open of the same URLs into the seat's own scratch, only when its item names it | as the first row | writing `corpus/captures/` or `refetch.tsv` | the seat's report |

Every other external target stays loopback-only. `tools/search-rerun.py` (including its `--selftest` mode)
reads only committed lane files, runs `git` only against `/dev/null` in its self-test (cases r29, r34: a process
that cannot open any repository), and never opens a socket.
