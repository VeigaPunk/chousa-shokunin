# Round 100 — external-target approval table (chousa)

SKILL.md `## Boundaries`: a window without an approval table is loopback-only; the approval table is itself a
chousa deliverable. This table follows the round-99 table's shape (`corpus/evidence/round99/egress-approval.md`),
narrowed to this round's three documents. It does not answer L0 `8d77e6c1` (fetch scope in general). Every row was
written before the round's first GET. No web search runs this round: every URL below was named by a committed
round-99 artifact (`SCORECARD.md` `## Planned — round 100` item 2; `.ufo/waves/round-99/w1/R99ScoutSources.md`).

Context: the lane holds Jergas & Baethge 2015's pooled quotation-error rates only through the authors' abstract
(S236, tier B) and Mogull 2017's re-derivation (S233). Round 99 routed two reads it could not make: the review's own
body (S235's route answered 500 to the lane's GET and 200 to a seat's re-open) and the 2025 update's Europe PMC record
(pmid 40696441, PMC12285159), whose publisher page served the lane a challenge page (S234).

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| Jergas & Baethge 2015 full text through Europe PMC's REST service (S235's route; a 200 is recorded as a new row that supersedes S235) | yes, at most 3 attempts | one `curl` GET per attempt through `tools/capture-fetch.py`, by the L1 only: `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML` | POST, cookies, credentials, crawling links, anything behind a login or captcha (a challenge page is a failed attempt, never a capture) | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/<key>.raw/.txt`; the lesson `## Gate` line (URL, access date, located quote) |
| Baethge & Jergas 2025 update ("Systematic review and meta-analysis of quotation inaccuracy in medicine", Research Integrity and Peer Review 2025) as indexed by Europe PMC's public REST API (core record, JSON) | yes, at most 3 attempts | as the first row: `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json` | as the first row | as the first row |
| the same 2025 update's Europe PMC full text | yes, at most 3 attempts | as the first row: `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12285159/fullTextXML` | as the first row | as the first row |
| seats of this round's wave | read-only re-open of the same URLs into the seat's own scratch, only when its item names it | as the first row | writing `corpus/captures/` or `refetch.tsv` | the seat's report |

Every other external target stays loopback-only. `tools/gate-records.py` (including the round-100 change) reads only
committed lane files, never fetches and never opens a socket.
