# Round 84 — external-target approval table (chousa)

Written and committed **before the first fetch of round 84** (round-81 routed defect 3 discipline, kept in rounds 82–83).
The commit that carries this file precedes every `corpus/evidence/round57/refetch.tsv` row dated 2026-11-08 with a time
after it; the closure compares the commit time with the refetch rows' `fetched_utc`.

SKILL.md `## Boundaries`: "A window without an approval table is loopback-only. The approval table is itself a chousa
deliverable." This table does not answer the open general fetch-scope L0 question (`8d77e6c1`); it records the narrower
direction under which this round fetches, on the round-57/81/82/83 tables' terms.

Authority: the round-84 dispatch prompt (`/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-84.md`) §2b — rows are
"written only after its source is opened this round" with "the URL, access date, and a ≤25-word located quote" — and the
run-15 addendum line "each round must leave the lane measurably more capable … a curated `corpus/SOURCES.md` delta". The
lane's province refuses *live-target* research (bounty or system targets); a GET of a public research-method document is
source research.

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| open of a public research-method document (PRISMA 2020 statement page) located by search | yes | one `curl -fsSL --compressed --max-time 15 -A <campaign UA>` GET per attempt, by the L1 only, through `tools/capture-fetch.py` | POST, cookies, credentials, anything behind a login, paywall or captcha, crawling links, more than 3 attempts per URL | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/` |
| web search to locate such a document | yes | the session's search tool | — | query and chosen URL in the lesson `## Gate` |
| a seat of this round's wave | a read-only re-open (one curl GET) of a URL that already has a round-84 row in `refetch.tsv`, into the seat's own scratch, only when its wave item names that URL | one GET per URL per seat, same UA | writing `corpus/captures/` or `refetch.tsv`; any URL without a round-84 refetch row | the seat's report names each GET and its HTTP status |

Intended targets (located by search before this file was written; each gets at most 3 attempts):

| intended id | URL | purpose |
|---|---|---|
| S017 (re-open) | https://www.prisma-statement.org/prisma-2020 | PRISMA 2020 reporting standard — search transparency checklist (queued since round 1; SCORECARD r84 plan item 2) |
