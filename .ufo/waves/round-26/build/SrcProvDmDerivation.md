# W3C PROV-DM derivation — source opening

- **Open / outcome:** Requested `https://www.w3.org/TR/prov-dm/`; `read` returned the canonical `https://www.w3.org/TR/2013/REC-prov-dm-20130430/` via W3C API, and its raw HTML was opened. `curl -sSL ... -w '%{http_code} %{url_effective}'` returned `200 https://www.w3.org/TR/2013/REC-prov-dm-20130430/`.
- **Located quote (23 words):** “To provide a completely accurate description of the derivation, the generation and usage of the generated and used entities, respectively, can be provided” — PROV-DM §5.2.1, “Derivation,” paragraph after the definition; anchor [`#term-Derivation`](https://www.w3.org/TR/2013/REC-prov-dm-20130430/#term-Derivation). Section §5.2 is “Component 2: Derivations” (`#component2`).
- **Observed:** The same subsection names the `generatedEntity` and `usedEntity` identifiers and describes generation/usage detail as optional. The quote says this detail *can* be provided, not that it is required (W3C PROV-DM §5.2.1, same anchor).
- **Proposed registry row (contract-v1 order; id intentionally TBD):**

  | TBD | PROV-DM: The PROV Data Model — https://www.w3.org/TR/2013/REC-prov-dm-20130430/ | spec | A | PROV-DM's own model of derivation between entities and optional generation/usage detail; not a registry or verification requirement | §5.2.1 “Derivation,” #term-Derivation; W3C Recommendation, 2013-04-30 | PROV-DM permits explicit generation and usage details for entities in a derivation | queued | 2026-10-21 | 365d | — |

- **Tier reason:** A only for PROV-DM's own model: this is the W3C Recommendation defining that model. The `SOURCES.md` tier field stays the contract enum `A`; see `/home/vgpnk/Projects/shokunin/CORPUS.md:86-108,112-115`.
- **Duplicate check:** No existing PROV-DM row observed. Related but distinct PROV-O rows S020 and S033 already exist (`corpus/SOURCES.md:30,43`). Proposed status is `queued` because no knowledge entry yet cites this row; flip to `mined` only when an entry cites it and is listed in `used-by` (`CORPUS.md:103-108`).
- **Limits / calibration:** `[INFERENCE]` Using the source/used-by pairing as an analogy for a two-sided derivation record is a lane design choice, not a PROV-DM requirement. PROV-DM does not prescribe this registry, a checker, metadata fields, citation-support verification, source truth, freshness, or recheck cadence. A derivation link alone does not establish that a cited source supports an entry or that the entry is true. Keep the row's scope to the model statement: `QUALITY.md:24-31` requires scoped authority and distinguishes source opening, topic, stated claim, and truth.

VERDICT: Opened the W3C primary source successfully; it supports the narrow derivation-model claim, not the C3 registry policy or truth of linked claims.
Installs: none.
