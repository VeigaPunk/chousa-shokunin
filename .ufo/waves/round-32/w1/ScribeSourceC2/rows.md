# C2 source row draft

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S060 | RFC 9110, HTTP Semantics — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | HTTP 404/410 response semantics at the origin server; not local-copy availability or a policy requiring local inspection | §§15.5.5 “404 Not Found” and 15.5.11 “410 Gone”; RFC 9110 (June 2022), body opened 2026-10-23, HTTP 200, SHA-256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | A 410 reports origin-server access as unavailable and likely permanent, while 404 does not specify whether missing representation is temporary or permanent; neither establishes local-copy availability, so C2’s separate local-evidence audit is a lane application | queued | 2026-10-23 | 365d | — |

Quote (9 words, §15.5.11, body line 7670): “resource is no longer available at the origin server”

Exact-literal locator command (from lane root; one result, line 7670): `grep -nF 'resource is no longer available at the origin server' .ufo/waves/round-32/w1/ScribeSourceC2/rfc9110.txt`

The literal was checked with the specialized grep search against the saved body; its sole match is line 7670. Fetch record: `rfc9110.headers`; saved source body: `rfc9110.txt`.
