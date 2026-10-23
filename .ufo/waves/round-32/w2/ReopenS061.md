# Reopen S061 — RFC 9110

Attacked: S061 (`corpus/SOURCES.md:71`) and its use in `corpus/knowledge/exempt-hop-audit-r32.md:16-19`. Not a counter run.

## Reopen (identity HOLDS)

Command: `timeout 180s curl --silent --show-error --max-time 150 --max-filesize 900000 --max-redirs 0 --dump-header …/ReopenS061/rfc9110.headers --output …/ReopenS061/rfc9110.txt --write-out 'HTTP_STATUS=%{http_code} BYTES=%{size_download} URL=%{url_effective} REDIRECT=%{num_redirects}' https://www.rfc-editor.org/rfc/rfc9110.txt`

- Exit 0. `HTTP_STATUS=200`, `BYTES=502941`, URL unchanged, `REDIRECT=0`. Header `date: Fri, 23 Oct 2026 07:26:22 GMT` (`rfc9110.headers:1-2`). Access date 2026-10-23.
- `sha256sum` → `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`. Row anchor `21c1cdce…47232a` matches prefix and suffix. `cmp` exit 0 against `.ufo/waves/round-32/w1/ScribeSourceC2/rfc9110.txt` (same digest).
- Body line 11: `June 2022`. Headings `15.5.5.  404 Not Found` at line 7587 and `15.5.11.  410 Gone` at line 7667.
- Exact phrase `resource is no longer available at the origin server`: Python `str.count` = 1 (casefold 1), only at line 7670 inside §15.5.11. Quote is 9 words. URL https://www.rfc-editor.org/rfc/rfc9110.txt, accessed 2026-10-23.

## Scope / teaches (BROKEN)

Scope (`SOURCES.md:71`) correctly bounds the row: origin-server 404/410 semantics; "not local-copy availability and not a rule that a researcher must check a local copy."

§15.5.5 (lines 7589-7595) says the origin server did not find a current representation or will not disclose that one exists, and does not say whether that is permanent. §15.5.11 (lines 7669-7674) says access is no longer available at the origin server and likely permanent. Those two sentences are what the row may teach.

The teaches cell then says neither code "says anything about a local copy, so \"could not be followed\" is a claim about one access path — the gap the round-32 exempt-hop audit checks locally." Grep of the fetched body: zero hits for `could not be followed`, `local copy`, or `one access path`. The "so" clause is not in RFC 9110. It contradicts this row's own scope and `corpus/lessons/round-32.md:64` ("the local-audit rule is lane design"). `corpus/QUALITY.md` criterion 7: a source used outside its scope is an inference and must be labelled. The teaches cell is unlabelled.

Precision, not a second break: both sections also say the response "is heuristically cacheable" (lines 7597-7599 and 7686-7688), and §15.5.11 lines 7676-7679 say owners desire that remote links be removed. The absolute "says anything" ignores those sentences. They are not a researcher's local copy. [INFERENCE] they do not by themselves falsify a narrow "local text" reading.

## Knowledge use (BROKEN)

`exempt-hop-audit-r32.md:16-19` opens "S061 shows why the label alone says little" and then states, unmarked, that "Could not be followed" is one access path and that a local copy is a separate question the gate answers. The only `[INFERENCE]` in that file is line 37, which does not cover 16-19. Same out-of-scope use as the teaches cell (`QUALITY.md` criteria 3 and 7). The audit procedure in lines 21-30 is lane design and is not charged to the RFC except through that paragraph.

## Verdict

BROKEN. Body, status, hash, date, section numbers, and the §15.5.11 quote once all hold. The teaches cell and `exempt-hop-audit-r32.md:16-19` attribute the exempt-hop audit to S061. That attribution is outside the row's scope, absent from the RFC, and unlabelled. Counters do not check it.

## Limits

No counter run. No install. Did not open other hosts. Did not edit lane production files. Artifacts: `.ufo/waves/round-32/w2/ReopenS061/rfc9110.txt` (502941 bytes) and `rfc9110.headers`.
