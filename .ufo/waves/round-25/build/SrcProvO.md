# Round 25 source scout — W3C PROV-O

- **Opened / access:** Requested `https://www.w3.org/TR/prov-o/`; HTTP 200. The reader identified the canonical versioned Recommendation, which was also opened directly: **https://www.w3.org/TR/2013/REC-prov-o-20130430/** (HTTP 200; 464,179 bytes; reader content type `text/markdown`, fetched via W3C API). Access date: **2026-10-21**. The document identifies itself as status REC (Recommendation).
- HTTP evidence: `curl -sSL -o /dev/null -w 'HTTP:%{http_code} FINAL:%{url_effective} BYTES:%{size_download}\n' --max-time 60 https://www.w3.org/TR/2013/REC-prov-o-20130430/` → `HTTP:200 FINAL:https://www.w3.org/TR/2013/REC-prov-o-20130430/ BYTES:464179`.
- **Verbatim quote (19 words):** “The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence.”
- **Exact location:** §3.2, “Expanded Terms,” fourth category (entity lifetime), paragraph describing entity lifetime.

## Proposed SOURCES.md row (S019; recommendation only, not added to registry)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S019 | PROV-O: The PROV Ontology — https://www.w3.org/TR/2013/REC-prov-o-20130430/ | spec | A | PROV provenance terms for derivation/source lineage and entity generation/invalidation times; not scheduled rechecks or verification policy | §3.1 “Starting Point Terms” (`prov:wasDerivedFrom`); §3.2 “Expanded Terms,” fourth category; `prov:generatedAtTime` and `prov:invalidatedAtTime` property entries; W3C Recommendation 2013-04-30 | Use PROV-O's derivation and entity-lifetime terms to express provenance and temporal boundaries; do not treat them as a recheck schedule. | queued | 2026-10-21 | on-release | — |

## Claim and recommendation

**Assessment: partial.** `prov:wasDerivedFrom` supplies a derivation relation, while `prov:generatedAtTime` and `prov:invalidatedAtTime` express generation and invalidation times. These terms can support provenance-aware freshness records. The quoted generation time is production time, not inherently `verified-at`; PROV-O does not define a scheduled recheck date/cadence or require source/verified-at metadata as a precondition for re-verification. The scheduling and verification rule therefore need a separate operational policy.

**Recommend admit as `queued`** for the scoped provenance/time vocabulary: it is a W3C Recommendation and relevant to traceable metadata, but only partially supports the operational claim. Keep `used-by` as `—` until a knowledge entry or lesson cites the row; then it may become `mined` under the contract.

VERDICT: Admit S019 as queued, scoped to provenance lineage and entity-time terms; partial support only, not authority for recheck scheduling or verification prerequisites. No tools installed or updated.
