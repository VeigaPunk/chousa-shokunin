# SrcRetractionWatchCrossref — round 26 source opening (C2 event triggers)

Axes: quote fidelity · registry-fit (contract v1) · scope-narrowness (QUALITY 7) · support-state honesty (QUALITY 8) · recheck freshness.

## 1. What answered (observed, 2026-10-21)

- `https://www.crossref.org/blog/retraction-watch-database-now-open/` → HTTP 404 (guessed; not opened).
- `https://www.crossref.org/documentation/retraction-watch/` → HTTP 404 (guessed; not opened).
- **`https://www.crossref.org/blog/news-crossref-and-retraction-watch/` → successful native fetch, `text/html`; numeric HTTP status not exposed by reader** (canonical confirms same URL; DOI 10.13003/c23rw1d9; published 12 September 2023; page carries a 2024-10-10 edit locating the dataset in a GitLab repo). Primary target answered — no mirror tried.
- **`https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/` → successful native fetch, `text/html`; numeric HTTP status not exposed by reader** (canonical confirms; page last updated 2025-January-19). Opened because it states where the machine-checkable fields live.

## 2. Quotes (verbatim, located)

Primary (announcement): "An agreement between the two organisations will allow Retraction Watch to keep the data populated on an ongoing basis and always open" — opening paragraph under "Crossref acquires Retraction Watch data and opens it for the scientific community", 12 September 2023 (22 words).
Supporting (docs): "Retractions are included in the `update-to` field of json files in the REST API" — section "Accessing the Retraction Watch Database", subsection "REST API" (14 words). Same page documents `?filter=update-type:retraction` and a CSV "updated once per working day".

## 3. Proposed SOURCES.md rows (contract v1 column order; ids TBD — table ends at S033, SOURCES.md:43, but sibling seats also propose rows; L1 assigns)

Row A:
`| TBD | Crossref news release: Crossref and Retraction Watch — https://www.crossref.org/blog/news-crossref-and-retraction-watch/ (DOI 10.13003/c23rw1d9) | docs | A | that Crossref acquired the Retraction Watch database and made it a public resource, kept populated on an ongoing basis; not data completeness or accuracy, and not a lane recheck policy | opening paragraph under "Crossref acquires Retraction Watch data and opens it for the scientific community", dated 12 September 2023; page with 2024-10-10 dataset-location edit | Retraction records are open, continuously maintained infrastructure metadata — the real-world precedent for an event-triggered recheck | queued | 2026-10-21 | 365d | — |`

Row B:
`| TBD | Crossref documentation: Retraction Watch — https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/ | docs | A | how retraction data is retrieved — REST API update-to/update-type fields and a daily CSV; not that coverage is complete (docs say corrections/EoC are "not as comprehensive as retractions") | section "Accessing the Retraction Watch Database", subsections "REST API" and "CSV dataset"; page last updated 2025-January-19 | Retraction data is exposed in queryable update metadata (update-to field and update-type:retraction filter) — an event a checker can see | queued | 2026-10-21 | 180d | — |`

Tier A reason (both): maintainer statement / official docs of the service's own behavior (SOURCES tier definition). Status `queued`: no knowledge entry cites them yet; C2's Cited entry may cite Row A/B per the sourced-claim rule.

## 4. What these sources do NOT support (QUALITY 7/8)

- Not completeness: docs page itself says other update types are "not as comprehensive as retractions"; no claim that every retraction is recorded.
- Not accuracy of any record: neither page evaluates record correctness; "the claim is true about a specific paper" is never supportable from these rows.
- Not lane policy: no cadence, classification, or C2 spec rule derives from them; `freshness=event` remains the lane's own invention (Row B grounds only that real update events arrive as dated machine-checkable metadata).
- QUALITY 8: these sources establish "source exists/opens" and state where retraction metadata lives; an entry citing them may claim only the quoted availability/retrieval facts.
- QUALITY 7: tier A is scoped to the stated `scope` cells; use beyond them (e.g. "all cited literature is retraction-screened") would be an unlabelled inference.

## 5. Duplication check

No duplicate. S028 is the Crossmark service page (`/services/crossmark/`) — publisher-registered update status, different URL and scope; no existing row covers the Retraction Watch acquisition announcement or the retrieve-metadata/retraction-watch docs page. Related, not overlapping; S028 and Row B could cross-support a future entry but stay separate rows.

## 6. Search-log note (SOURCES rule 5, for the round lesson)

Query: "Crossref blog Retraction Watch database open announcement"; where: web search then crossref.org direct reads; 2026-10-21. Identified 2 candidate URLs after 2 guessed 404s; screened 2; included 2 proposed rows; excluded 0. Stop: pre-assigned single target; both announcement and its retrieval doc opened and quoted.

## 7. Bounds

No installs. No clone needed (read-only seat; no tools/patches produced). Only file written: this report; no checks or probes were run.

VERDICT: Both Crossref pages opened successfully (numeric status unavailable); two tier-A rows proposed with verbatim ≤25-word quotes grounding C2's "event triggers are machine-checkable metadata"; no existing row duplicated.
