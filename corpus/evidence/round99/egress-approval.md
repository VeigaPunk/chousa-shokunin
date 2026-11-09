# Round 99 — external-target approval table (chousa)

SKILL.md `## Boundaries`: a window without an approval table is loopback-only; the approval table is itself a
chousa deliverable. This table follows the round-98 table's shape (`corpus/evidence/round98/egress-approval.md`),
narrowed to this round's documents. It does not answer L0 `8d77e6c1` (fetch scope in general). Every row below except
the Europe PMC core-record row (second) was written before the round's first GET; that row was appended after the
GETs its own text names and before its own GET. The session's one web search (the search row) ran before this table
was written, to learn the documents' identifiers.

Context: no knowledge entry holds the measured rate of quotation errors (a cited source that does not support the
citing sentence) — the empirical side of the province's claim-vs-source verification (`PROVINCE.md` **Owns**). C2
of round 99 opens the two meta-analyses of that literature and the one study that re-derived their rate.

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| Jergas H, Baethge C, "Quotation accuracy in medical journal articles — a systematic review and meta-analysis", PeerJ 2015;3:e1364 (publisher page) | yes, at most 3 attempts | one `curl` GET per attempt through `tools/capture-fetch.py`, by the L1 only: `https://peerj.com/articles/1364/` | POST, cookies, credentials, crawling links, anything behind a login or captcha (a challenge page is a failed attempt, never a capture) | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/<key>.raw/.txt`; the lesson `## Gate` line (URL, access date, located quote) |
| Jergas & Baethge 2015's own abstract as indexed by Europe PMC's public REST API (core record, JSON) — appended after the PeerJ GET answered 403 (S232) and the Europe PMC full-text GET answered 500 (S235), before its own GET; the round-98 S231 route | yes, at most 3 attempts | as the first row: `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json` | as the first row | as the first row |
| Mogull SA, "Accuracy of cited 'facts' in medical research articles: a review of study methodology and recalculation of quotation error rate", PLoS One 2017;12(9):e0184727 (publisher page) | yes, at most 3 attempts | as the first row: `https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727` | as the first row | as the first row |
| Baethge C, Jergas H, "Systematic review and meta-analysis of quotation inaccuracy in medicine", Research Integrity and Peer Review 2025 (publisher page) | yes, at most 3 attempts | as the first row: `https://researchintegrityjournal.biomedcentral.com/articles/10.1186/s41073-025-00173-z` | as the first row | as the first row |
| web search to identify the documents above | yes (one query, already run) | the session's search tool | — | the query in the lesson `## Gate` |
| any of the three documents' Europe PMC full-text record, only if its publisher row ends in a non-200 status or a challenge page | yes, at most 3 attempts per document | as the first row: `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML` with the PMCID the publisher page or the search names | as the first row | as the first row |
| seats of this round's wave | read-only re-open of the same URLs into the seat's own scratch, only when its item names it | as the first row | writing `corpus/captures/` or `refetch.tsv` | the seat's report |

Every other external target stays loopback-only. `tools/gate-records.py` (including the round-99 change) reads only
committed lane files, never fetches and never opens a socket.
