# Round 29 liveness wording audit

- Behavior: drafted an append-only SCORECARD correction and case-insensitive five-surface grep inventory; no frozen or production file was changed.
- Evidence: `landed-fixture.network.json` contains 8 allowed `GET` request events and 8 responses with status 200; `differential-receipt.json` binds `landed-fixture`, production bytes unchanged, 40/40 observed, and recorded exit 1. The embedded command and summary are in `drafts.md`; not rerun here.
- Search findings: lesson lines 1, 6, 78, 96, 98; knowledge lines 1, 107, 112; SCORECARD lines 1617, 1619, 1635; README line 932; no `live` in LOG's round 29 lines 1186–1201. Per-line receipt limits are in the draft.
- Scope note: frozen `corpus/evidence/round29/claims.md:41-42` also says “live source”; opened, not modified, and outside the requested five-surface grep.
- Gates: read/grep calls succeeded; this seat ran no candidate, counter, tests, or network command and installed no tools.
- Limit: the network receipt proves only 8 GETs and 8 HTTP 200 responses in one guarded fixture run; it does not make the counter a live-network measurement or prove all URLs reachable.
- Artifacts: `.ufo/waves/round-30/build/ScribeD1Liveness/drafts.md`; `.ufo/waves/round-30/build/ScribeD1Liveness.md`.
