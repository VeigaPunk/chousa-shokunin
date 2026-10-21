# CiTO source opening — SrcCito-3

Axes: calibration; freshness. This source bears on citation-relation calibration only.

## Opened source and findings

- Opened the exact official current page: https://sparontologies.github.io/cito/current/cito.html — HTTP 200, final URL unchanged (`curl -L -sS -o /dev/null -w 'http_code=%{http_code} final_url=%{url_effective}\n' ...` → `http_code=200 final_url=https://sparontologies.github.io/cito/current/cito.html`). Page title: “The Citation Typing Ontology (CiTO)”.
- Verbatim located quote (21 words): “A relation according to which the citing entity cites the cited entity as source of factual evidence for statements it contains.” Section “cites as evidence op”, anchor `#id_010554247447337669685a3ec311d6ea_Relation`, RDF provenance `rdfs:comment` (page lines 3084–3092, quote at 3090): https://sparontologies.github.io/cito/current/cito.html#id_010554247447337669685a3ec311d6ea_Relation.
- CiTO declares `cito:citesAsEvidence` an OWL object property and a subproperty of `cito:cites` (same page, lines 3084–3092). It distinguishes this from `cito:citesAsDataSource` (“source of data”, lines 2913–2921); `cito:supports` describes the citing entity providing support for statements in the cited entity (lines 17090–17093). These are different relation meanings, not interchangeable labels.
- C3 calibration boundary: round-26 Claim 3 checks that an S-id has a registry row, that its status is `mined`, that `used-by` names the entry, and that `verified-at` says what was checked (`corpus/evidence/round26-claims.md:84–93`). CiTO grounds the narrower proposition that a citation can be represented by a typed relation; it does not specify those registry checks.
- No duplicate CiTO row found: case-insensitive search of `corpus/SOURCES.md` for “CiTO”, “cito”, and “Citation Typing Ontology” returned “No matches found”; latest existing ID is S033 (`corpus/SOURCES.md:43`).
- Contract v1 column order and tier/status rules: `CORPUS.md:86–108`; QUALITY 7–8 require scope-specific tier and distinguish source existence/topic/statement from truth (`corpus/QUALITY.md:24–31`).

## Proposed `corpus/SOURCES.md` row (not written to registry)

| TBD | Citation Typing Ontology (CiTO), SPAR Ontologies — https://sparontologies.github.io/cito/current/cito.html | spec | A | CiTO's own semantics for `cito:citesAsEvidence` and neighboring citation predicates; tier A only for its primary ontology definitions | “cites as evidence op” (anchor above), RDF provenance lines 3084–3092; compare “cites as data source” lines 2913–2921 and `supports` lines 17090–17093 | Distinguishes citing an entity as factual evidence for the citing entity's statements from citing it as a data source or expressing support in the reverse direction | queued | 2026-10-21 | 365d | — |

Queued rationale / flip: opened and relevant, but no admitted knowledge path currently cites this row; change to mined only when a scoped knowledge entry cites it and is added to `used-by`.

## Limits

- Does not establish that a source actually is evidence, that the cited statements are supported or true, or that a declared CiTO relation is accurate; QUALITY 8 keeps these states distinct (`corpus/QUALITY.md:28–31`).
- Does not prescribe an entry registry schema, metadata verification algorithm, required citation relation, or C3 acceptance rule (`round26-claims.md:84–93`).
- Does not support a recheck interval or research-record freshness policy; its page date is not evidence that a research claim remains current.

VERDICT: Tier A for CiTO's own typed citation-relation definitions; queued pending a knowledge entry. No mirror needed; primary page answered. Installs: none.
