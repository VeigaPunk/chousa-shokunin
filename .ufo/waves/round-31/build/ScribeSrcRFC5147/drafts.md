# S057 draft — RFC 5147

**Disposition:** rejected as evidence from this opening, not a substantive finding that RFC 5147 lacks the requested rule. The one GET to the requested URL returned HTTP 301 with a zero-byte body; no redirect or second request was made. Therefore no quote, two-sentence source context, or RFC fragment interpretation is available. In particular, I cannot verify from opened bytes the RFC's 0-based positions-between-lines convention or advise how it maps to the gate's 1-based `at=` line numbers.

## Draft SOURCES row

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S057 | RFC 5147 endpoint — https://www.rfc-editor.org/rfc/rfc5147 | spec | C | This failed fetch establishes only that the requested endpoint redirected; it does not establish RFC text-fragment line/position syntax or a mapping to the gate's 1-based `at=` lines. Tier C because the RFC body was unavailable; lead only. | requested URL response: HTTP 301, 0 body bytes, 2026-10-23; no RFC section reached | REJECTED: no RFC text was returned from which to substantiate line-position numbering; flip: on a separately authorized opening, retrieve a body from an allowed URL on www.rfc-editor.org and locate a passage explicitly defining line/range positioning | rejected | 2026-10-23 | 90d | corpus/knowledge/line-binding-r31.md |

## Gate-table line

| URL / response | Quote (≤25 words) | Verdict |
|---|---|---|
| https://www.rfc-editor.org/rfc/rfc5147 — HTTP 301, 0 body bytes | — (empty response body; no source quote available) | reject this opening as evidence; no line-position claim verified |

## Raw quote context

Unavailable: the response body was 0 bytes, so there were no two surrounding source sentences to quote. Response-body SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
