# Round 87 — external-target approval table (chousa)

Written and committed **before the first fetch of round 87** (round-81 routed defect 3 discipline, kept in 82–86).
The commit carrying this file precedes every `corpus/evidence/round57/refetch.tsv` row whose `fetched` is
`2026-11-08T1` or later; the closure can compare the commit time with the refetch rows.

SKILL.md `## Boundaries`: "A window without an approval table is loopback-only. The approval table is itself a
chousa deliverable." This table does not answer the open general fetch-scope L0 question; it records the narrower
direction under which this round fetches, on the round-57/81/82/83/84/85/86 tables' terms.

Authority: the round-87 dispatch prompt §2b — rows are "written only after its source is opened this round" with "the
URL, access date, and a ≤25-word located quote" — and the run-15 addendum line "each round must leave the lane
measurably more capable … a curated `corpus/SOURCES.md` delta". The lane's province refuses *live-target* research
(bounty or system targets); a GET of a public standards document is source research.

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| re-open of a registered documentation URL, committed as intended below | yes | one `curl -fsSL --compressed --max-time 15 -A <campaign UA>` GET per attempt, by the L1 only, through `tools/capture-fetch.py` | POST, cookies, credentials, anything behind a login, paywall or captcha, crawling links, more than 3 attempts per URL | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/` |
| web search to locate such a document | yes | the session's search tool | — | query and chosen URL in the lesson `## Gate` |
| a seat of this round's wave | never performs a network GET this round | — | any fetch, capture write or `refetch.tsv` write | seats read only committed bytes |

Intended targets (each gets at most 3 attempts):

| intended id | URL | purpose |
|---|---|---|
| S216 (re-open) | https://www.rfc-editor.org/rfc/rfc9110.html | re-open the registered 203 row for this round's access date and its located §15.3.4 quote. The same clause grounds both 203 classes C1 closes: "the request was successful but the enclosed content has been modified from that of the origin server's 200 (OK) response" — the body is not the origin's (D1: an admit over it must be refused) and the response is not a failed transfer (D2: the `url/unreach` form must refuse it) |

Note: the intended-targets list is the machine-checkable scope. A fetch of any URL absent from this table is out of
scope, even if this prose would have allowed it (QUALITY 168). No other URL is fetched this round. The one new registry
row this round (`S218`) is `own-work`: its source is the lane's own `corpus/QUALITY.md` criterion 178 read from the
committed tree, which is opened by reading a file, not by a GET.
