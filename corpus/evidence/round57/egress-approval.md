# Round 57 — external-target approval table (chousa)

SKILL.md `## Boundaries`: "A window without an approval table is loopback-only. The approval table is itself a chousa
deliverable." This is the table for round 57's window. It does not answer L0 `8d77e6c1` (fetch scope in general);
it records the narrower direction under which this round fetched.

Authority: the orchestrator's note in the round-57 dispatch to `ChousaR57` (2026-10-27), verbatim: "Any claim needing
captures must re-fetch into lane-owned evidence (committed bytes + sha256) and say so. Counters pinned to .qcache
will exit ENV_CHANGED and must not be presented as measurements." It also forbids recreating the cache inside
`/home/vgpnk/Projects/shokuknow` ("shokuknow is read-only to you: do NOT recreate it there").

| scope | allowed | method | not allowed | record |
|---|---|---|---|---|
| re-open of a URL already registered in `corpus/SOURCES.md` and pinned by a committed spans manifest | yes | one `curl -fsSL --compressed --max-time 15 -A <campaign UA>` GET per attempt (the campaign recipe), by the L1 only, through `tools/capture-fetch.py` | POST, cookies, credentials, query rewriting, crawling links, more than 3 attempts per URL | `corpus/evidence/round57/refetch.tsv` row per attempt; bytes in `corpus/captures/<key>.raw/.txt` |
| open of a public document a registered source cites by name (R57-C3's lead: the documents S127's `2 规范性引用文件` names) | yes | as above, after the document's URL is located by a search | anything behind a login, paywall or captcha | the same record; the new row's lesson `## Gate` line |
| web search to locate such a document | yes | the session's search tool | — | the query and the chosen URL in the lesson `## Gate` |
| seats of this round's wave | read-only re-open of a URL already in `refetch.tsv`, into the seat's own scratch, only when its item names it | as the first row | writing `corpus/captures/` or `refetch.tsv` | the seat's report |

Every other external target stays loopback-only.
