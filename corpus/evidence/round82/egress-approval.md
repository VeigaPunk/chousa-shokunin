# Round 82 — external-target approval table (chousa)

Written and committed **before the first fetch of round 82** (round-81 routed defect 3: the round-81 table was written
after its fetches). The commit that carries this file precedes every `corpus/evidence/round57/refetch.tsv` row dated
2026-11-06 with a time after it; the closure can compare the commit time with the refetch rows' `fetched_utc`.

SKILL.md `## Boundaries`: "A window without an approval table is loopback-only. The approval table is itself a chousa
deliverable." This table does not answer the open general fetch-scope L0 question (`8d77e6c1`); it records the narrower
direction under which this round fetches, on the round-57/round-81 tables' terms.

Authority: the round-82 dispatch prompt (`/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-82.md`) §2b — rows are
"written only after its source is opened this round" with "the URL, access date, and a ≤25-word located quote" — and the
run-15 addendum line "each round must leave the lane measurably more capable … a curated `corpus/SOURCES.md` delta". The
lane's province refuses *live-target* research (bounty or system targets); a GET of a public research-method document is
source research.

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| open of a public research-method document (review-methods handbook chapter, evidence-synthesis manual page, registry/metadata-service documentation) located by a search | yes | one `curl -fsSL --compressed --max-time 15 -A <campaign UA>` GET per attempt, by the L1 only, through `tools/capture-fetch.py` | POST, cookies, credentials, anything behind a login, paywall or captcha, crawling links, more than 3 attempts per URL | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/` |
| web search to locate such a document | yes | the session's search tool | — | query and chosen URL in the lesson `## Gate` |
| a seat of this round's wave | a read-only re-open (one curl GET, or `tools/quote-reopen.py verify`) of a URL that already has a round-82 row in `refetch.tsv`, into the seat's own scratch, only when its wave item names that URL | one GET per URL per seat, same UA | writing `corpus/captures/` or `refetch.tsv`; any URL without a round-82 refetch row | the seat's report names each GET and its HTTP status |

Intended targets (located by search before this file was written; each gets at most 3 attempts):

| intended id | URL | purpose |
|---|---|---|
| S008 (re-open) | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-02 | question framing: review/synthesis/included-study PICO (queued since round 1) |
| new | https://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862667/10.2.2+Developing+the+title+and+question | question framing for scoping reviews (PCC) |
| new | https://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862687 | aligning objectives and questions |
| new | https://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862707 | aligning eligibility criteria with the question |
| S028 (re-open) | https://www.crossref.org/services/crossmark/ | disposition of the queued Crossmark row (round-81 routed defect 6) |

A URL not listed here is fetched only after a row is appended to this table in a later commit, before the fetch.
Every other external target stays loopback-only.
