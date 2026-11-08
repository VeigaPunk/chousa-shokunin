# Round 85 — external-target approval table (chousa)

Written and committed **before the first fetch of round 85** (round-81 routed defect 3 discipline, kept in rounds 82–84).
The commit that carries this file precedes every `corpus/evidence/round57/refetch.tsv` row dated 2026-11-08 with a time
after it; the closure compares the commit time with the refetch rows' `fetched_utc`.

SKILL.md `## Boundaries`: "A window without an approval table is loopback-only. The approval table is itself a chousa
deliverable." This table does not answer the open general fetch-scope L0 question (`8d77e6c1`); it records the narrower
direction under which this round fetches, on the round-57/81/82/83/84 tables' terms.

Authority: the round-85 dispatch prompt (`/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-85.md`) §2b — rows are
"written only after its source is opened this round" with "the URL, access date, and a ≤25-word located quote" — and the
run-15 addendum line "each round must leave the lane measurably more capable … a curated `corpus/SOURCES.md` delta". The
lane's province refuses *live-target* research (bounty or system targets); a GET of a public research-method document is
source research.

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| open of a public research-method document (PROV-O recommendation, DCMI Terms) committed as intended below | yes | one `curl -fsSL --compressed --max-time 15 -A <campaign UA>` GET per attempt, by the L1 only, through `tools/capture-fetch.py` | POST, cookies, credentials, anything behind a login, paywall or captcha, crawling links, more than 3 attempts per URL | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/` |
| web search to locate such a document | yes | the session's search tool | — | query and chosen URL in the lesson `## Gate` |
| a seat of this round's wave | a read-only re-open (one curl GET) of a URL that already has a round-85 row in `refetch.tsv`, into the seat's own scratch, only when its wave item names that URL | one GET per URL per seat, same UA | writing `corpus/captures/` or `refetch.tsv`; any URL without a round-85 refetch row | the seat's report names each GET and its HTTP status |

Intended targets (each gets at most 3 attempts):

| intended id | URL | purpose |
|---|---|---|
| S023 (re-open) | https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ | DCMI Terms — the `modified` Definition ("Date on which the resource was changed.") that uniquely locates the round-84 row-9 warrant; already `mined` (recheck anchor), re-opened for the locatable quote |
| S020 (alternate URL) | https://www.w3.org/TR/prov-o/ | PROV-O recommendation via the W3C's alternate URL (the `REC-prov-o-20130430` URL was HTTP 403 in round 84); registers the previously unopenable `prov:wasDerivedFrom` dimension under its own row |

Note: the intended-targets list is the machine-checkable scope. A fetch of any URL absent from this table is out of
scope, even if this prose would have allowed it (QUALITY 168).
