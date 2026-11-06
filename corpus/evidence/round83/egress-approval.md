# Round 83 — external-target approval table (chousa)

Written and committed **before the first fetch of round 83** (round-81 routed defect 3 discipline, kept in round 82).
The commit that carries this file precedes every `corpus/evidence/round57/refetch.tsv` row dated 2026-11-06 with a time
after it; the closure compares the commit time with the refetch rows' `fetched_utc`.

SKILL.md `## Boundaries`: "A window without an approval table is loopback-only. The approval table is itself a chousa
deliverable." This table does not answer the open general fetch-scope L0 question (`8d77e6c1`); it records the narrower
direction under which this round fetches, on the round-57/81/82 tables' terms.

Authority: the round-83 dispatch prompt (`/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-83.md`) §2b — rows are
"written only after its source is opened this round" with "the URL, access date, and a ≤25-word located quote" — and the
run-15 addendum line "each round must leave the lane measurably more capable … a curated `corpus/SOURCES.md` delta". The
lane's province refuses *live-target* research (bounty or system targets); a GET of a public research-method document is
source research.

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| open of a public research-method document (review-methods handbook chapter, conduct-standard page) located by a search | yes | one `curl -fsSL --compressed --max-time 15 -A <campaign UA>` GET per attempt, by the L1 only, through `tools/capture-fetch.py` | POST, cookies, credentials, anything behind a login, paywall or captcha, crawling links, more than 3 attempts per URL | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/` |
| web search to locate such a document | yes | the session's search tool | — | query and chosen URL in the lesson `## Gate` |
| a seat of this round's wave | a read-only re-open (one curl GET) of a URL that already has a round-83 row in `refetch.tsv`, into the seat's own scratch, only when its wave item names that URL | one GET per URL per seat, same UA | writing `corpus/captures/` or `refetch.tsv`; any URL without a round-83 refetch row | the seat's report names each GET and its HTTP status |

Intended targets (located by search before this file was written — query "Cochrane Handbook chapter 7 considering bias
and conflicts of interest among included studies two review authors independently"; each gets at most 3 attempts):

| intended id | URL | purpose |
|---|---|---|
| S009 (re-open) | https://www.cochrane.org/authors/handbooks-and-manuals/mecir-manual/standards-conduct-new-cochrane-intervention-reviews-c1-c75/performing-review-c24-c75/assessing-risk-bias-included-studies-c52-c60 | conduct standards for recording appraisal judgments (queued since round 1; SCORECARD r83 plan item 2) |
| new | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-07 | duplicate independent assessment, disagreement process, conflicts of interest of included studies |
| new | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08 | supporting each risk-of-bias judgement with recorded justification |

A URL not listed here is fetched only after a row is appended to this table in a later commit, before the fetch.
Every other external target stays loopback-only.
