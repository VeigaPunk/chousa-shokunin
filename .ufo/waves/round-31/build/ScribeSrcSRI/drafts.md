# S058 candidate — Subresource Integrity

## Opening evidence

- Requested URL (one direct GET; redirects not followed): `https://www.w3.org/TR/2016/REC-SRI-20160623/`
- Command: `timeout 60 sh -c 'mkdir -p /fast/scratch/hyaku/chousa-r31/w1/ScribeSrcSRI && curl --silent --show-error --max-redirs 0 --output /fast/scratch/hyaku/chousa-r31/w1/ScribeSrcSRI/sri.html --write-out "HTTP_STATUS=%{http_code}\nDOWNLOADED_BYTES=%{size_download}\n" https://www.w3.org/TR/2016/REC-SRI-20160623/'`
- Outcome: HTTP 200; downloaded response body 89,641 bytes. The shell tool completed normally (exit 0 inferred; no explicit process status was emitted).
- Command: `timeout 10 sha256sum /fast/scratch/hyaku/chousa-r31/w1/ScribeSrcSRI/sri.html`
- Outcome: `947d942a2db9192d4936c9d1fc2f7cad919a107aed126ef5cd2302ec058d2c75`; tool completed normally (exit 0 inferred; no explicit process status was emitted). Opened 2026-10-23.

## Proposed SOURCES.md registry row

| S058 | W3C, Subresource Integrity — https://www.w3.org/TR/2016/REC-SRI-20160623/ (Recommendation, 2016-06-23) | spec | A | Browser Subresource Integrity response-digest validation (tier A: the primary W3C Recommendation for this mechanism); does not establish this lane gate's exact local-file byte contract, claim-schema validation, or read/hash race behavior | sections 3.3.1 “Apply algorithm to response” and 3.3.5 “Does response match metadataList”, dated Recommendation 2016-06-23 | Hash the response representation, compare the resulting digest with expected metadata, and return false when no expected value matches | mined | 2026-10-23 | 365d | corpus/knowledge/revision-binding-r31.md |

## Gate-table line

| URL | Quote | Verdict |
|---|---|---|
| https://www.w3.org/TR/2016/REC-SRI-20160623/#does-response-match-metadatalist | “If actualValue is a case-sensitive match for expectedValue, return true.” | SUPPORTS, scoped: §3.3.5 calculates the response value, accepts an expected-value match, then returns false when no value matches; §3.3.1 defines the response representation hashed. This establishes the browser SRI pattern, not the lane gate's filesystem-byte semantics. |

Quote length: 10 words (≤25). The algorithm's previous and next sentences provide the requested raw context, from section 3.3.5:

> Let actualValue be the result of applying algorithm to response.
>
> If actualValue is a case-sensitive match for expectedValue, return true.
>
> Return false.

## Verdict and limit

Accept as a scoped S058 candidate for C2's digest-comparison-and-failure principle. The Recommendation hashes response representation data (section 3.3.1; with its stated content-coding condition), so it is not evidence for every interpretation of “exact file bytes” or for this lane gate's implementation. No lane source row or product file was changed; no gate/counter was run.
