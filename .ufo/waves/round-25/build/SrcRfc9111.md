# RFC 9111 source finding — 2026-10-21

## Open and evidence
- Requested source: https://www.rfc-editor.org/rfc/rfc9111. The reader opened it and returned RFC markdown (`Content-Type: text/markdown`, `Method: rfc`; metadata from the RFC Editor JSON API). The document identifies itself as RFC 9111, Standards Track, published June 2022 (RFC 9111, front matter).
- Final HTTP URL observed: `https://www.rfc-editor.org/info/rfc9111/`. A GET following redirects returned `http_code=200` and `url_effective=https://www.rfc-editor.org/info/rfc9111/` (`curl -sS -L -o /dev/null -w 'http_code=%{http_code}\nurl_effective=%{url_effective}\n' https://www.rfc-editor.org/rfc/rfc9111`). The RFC reader supplied the RFC text for the requested RFC URL.
- Access date: 2026-10-21.
- Quote: “response_is_fresh = (freshness_lifetime > current_age)” — RFC 9111 §4.2, “Freshness.”
- The specification derives `freshness_lifetime` from `s-maxage`, `max-age`, or `Expires`, or may use a heuristic (§4.2.1–4.2.2); it calculates `current_age` from corrected age plus resident time (§4.2.3), and defines stale in relation to the §4.2 freshness calculation (§4.2.4).

## Proposed SOURCES.md row fields
- kind: `spec`
- tier: `A` — authoritative standard for the narrowly stated HTTP-cache scope.
- scope: RFC 9111's freshness calculation and stale-response semantics for cached HTTP responses; not general research-record freshness.
- anchor: RFC 9111 §§4.2–4.2.4 (“Freshness,” “Calculating Freshness Lifetime,” “Calculating Heuristic Freshness,” “Calculating Age,” “Serving Stale Responses”), June 2022.
- teaches: HTTP-cache freshness is computed by comparing freshness lifetime with current age; lifetime can be explicit or heuristic, and a response is stale when it is not fresh under that calculation.
- status recommendation: `queued` (proposed next id S019; the registry currently ends at S018: `corpus/SOURCES.md:9-10,28-29`). It is opened and potentially useful as a carefully scoped analogy; it is not yet mined or used by a knowledge entry. Contract columns, scope-bound tiers, anchors, and status meanings: `/home/vgpnk/Projects/shokunin/CORPUS.md:86-108`.

## Claim relation and judgment
- Supports the composite claim **partially, as an analogy only**. It demonstrates computable freshness/staleness for HTTP cache responses from a lifetime and age. It does not establish that a scheduled recheck makes any research record stale, nor that `source` and `verified-at` are preconditions for re-verification; those are outside this HTTP-cache spec. Do not present this RFC as direct support for those record-metadata requirements. The lane's separate metadata criterion specifies `source`, `verified-at`, and `recheck`: `corpus/QUALITY.md:17-23`.
- Recommendation: admit as `queued`, tightly scoped to HTTP caches; if later mined to explain record freshness, label the transfer as an analogy/inference and cite direct lane-specific authority for provenance and re-verification requirements.

Installs: none.
VERDICT: Opened; HTTP freshness is computable in-scope, but RFC 9111 only partially supports the lane's broader record-metadata claim; queue only under the narrow HTTP-cache scope.