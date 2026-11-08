# Round 86 — external-target approval table (chousa)

Written and committed **before the first fetch of round 86** (round-81 routed defect 3 discipline, kept in 82–85).
The commit carrying this file precedes every `corpus/evidence/round57/refetch.tsv` row whose `fetched_utc` is
`2026-11-08T06` or later; the closure compares the commit time with the refetch rows.

SKILL.md `## Boundaries`: "A window without an approval table is loopback-only. The approval table is itself a
chousa deliverable." This table does not answer the open general fetch-scope L0 question (`8d77e6c1`); it records the
narrower direction under which this round fetches, on the round-57/81/82/83/84/85 tables' terms.

Authority: the round-86 dispatch prompt §2b — rows are "written only after its source is opened this round" with "the
URL, access date, and a ≤25-word located quote" — and the run-15 addendum line "each round must leave the lane
measurably more capable … a curated `corpus/SOURCES.md` delta". The lane's province refuses *live-target* research
(bounty or system targets); a GET of a public research-method document is source research.

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| open of a public standards document (RFC 9110, DCMI namespace policy) or re-open of a registered documentation URL, committed as intended below | yes | one `curl -fsSL --compressed --max-time 15 -A <campaign UA>` GET per attempt, by the L1 only, through `tools/capture-fetch.py` | POST, cookies, credentials, anything behind a login, paywall or captcha, crawling links, more than 3 attempts per URL | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/` |
| web search to locate such a document | yes | the session's search tool | — | query and chosen URL in the lesson `## Gate` |
| a seat of this round's wave | never performs a network GET this round | — | any fetch, capture write or `refetch.tsv` write | seats read only committed bytes |

Intended targets (each gets at most 3 attempts):

| intended id | URL | purpose |
|---|---|---|
| S216 | https://www.rfc-editor.org/rfc/rfc9110.html | RFC 9110 §15.3.4 `203 Non-Authoritative Information`: the status means a transforming intermediary changed the representation, so a 203 body is not the origin's own representation — the ground for the round-86 C1 200-only forgery class |
| S217 | https://www.dublincore.org/documents/dcmi-namespace/ | DCMI Namespace Policy: how a term registry maintains and supersedes its terms without deleting them — the ground for the round-86C2 supersession invariant |
| S031 (re-open) | https://schema.org/lastReviewed | re-open the registered `lastReviewed` row for this round's access date and located quote (round-85 routed defect 1) |
| S023 (re-open) | https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ | DCMI Terms — re-open to locate the `modified` Definition ("Date on which the resource was changed.") that the round-84 row-9 warrant needs and does not cite |

Note: the intended-targets list is the machine-checkable scope. A fetch of any URL absent from this table is out of
scope, even if this prose would have allowed it (QUALITY 168). No other URL is fetched this round.
