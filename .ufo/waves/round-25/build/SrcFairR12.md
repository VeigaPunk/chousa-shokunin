# GO FAIR R1.2 source check

- **Opened:** 2026-10-21. Requested URL: `https://www.go-fair.org/fair-principles/r1-2-metadata-associated-detailed-provenance/`. Final URL actually opened: `https://www.gofair.foundation/r1-2` (canonical URL shown by reader and curl). **HTTP:** GET returned `http_code=200`, `url_effective=https://www.gofair.foundation/r1-2` (`curl -L -sS -o /dev/null -w ...`; successful page retrieval, not blocked/paywalled).
- **Verbatim quote (20 words):** “Detailed provenance includes facets such as how the resource was generated, why it was generated, by whom, under what conditions” — GO FAIR Foundation, **“Interpretation of R1.2,”** first paragraph: https://www.gofair.foundation/r1-2.

## Proposed SOURCES.md fields

Per contract columns and scoped tiers (`CORPUS.md:86-108`):

- **source:** GO FAIR Foundation, R1.2 — https://www.gofair.foundation/r1-2
- **kind / tier:** docs / A, narrowly for the Foundation's own interpretation of FAIR sub-principle R1.2.
- **scope:** What this interpretation says detailed provenance includes and how provenance informs assessment of intended reuse.
- **anchor:** “Interpretation of R1.2,” first paragraph; page as served 2026-10-21.
- **teaches:** Detailed provenance can include how/why/by whom/under what conditions a resource was generated, its source resources, ownership/credit and post-generation processing; provenance helps assess reuse suitability.
- **status / opened / recheck / used-by:** queued / 2026-10-21 / 365d / —.

## Claim assessment

- **Partial support** for claim 1's proposition that source provenance matters (`round25-claims.md:10-15`; required metadata keys are specified at `:26-28`). The page explicitly includes starting-data/source-resource among provenance facets and says provenance helps assess reuse criteria. It does **not** say that a scheduled recheck date or cadence makes staleness computable, that `verified-at` is required, or that either is a precondition of re-verification. It cannot support the full compound claim.
- **Recommend admit as queued**, scoped only to R1.2's detailed-provenance interpretation; do not cite it as evidence for scheduled rechecks or the `verified-at` gate rule. It is opened and worth mining for the provenance portion, but not mined because no knowledge entry uses it.

No tools installed or updated.

VERDICT: Admit queued for the scoped provenance interpretation; partial support only for the compound metadata claim.
