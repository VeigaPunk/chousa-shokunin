# Pin a claim to the source bytes read (round 31)

source: S058 https://www.w3.org/TR/2016/REC-SRI-20160623/ §3.3.1 "Apply algorithm to response", §3.3.5 "Does response match metadataList"; S059 https://docs.python.org/3/library/hashlib.html "Hash algorithms", "Hash Objects"; frozen contract `corpus/evidence/round31/claims.md` §C2 (design v2); `SKILL.md` "Checklist (executable)" item 1
verified-at: 2026-10-23 UTC (round 31; S058 and S059 opened once each on 2026-10-23 by scribe seats; located quotes in `corpus/lessons/round-31.md` `## Gate`. The counter's measured result is in SCORECARD.md, section "Round 31")
recheck: 365d (from the lane root: `python3 corpus/evidence/round31/c2-count.py`)

## The rule

The lane's C2 contract adds an optional JSON string field, `"sha256"`, to a claim record. If present, it must be exactly 64 lowercase hexadecimal characters. A malformed value makes the record `observed=invalid` with `CLAIM_RECORD_INVALID`.

For a valid pin, compare it with the SHA-256 digest of the exact bytes of the claim's source file. A mismatch is `observed=stale` with `FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims obs=id=<claim id> pin=<12 hex> actual=<12 hex>`, before and regardless of the span check. A source whose digest cannot be measured reads `stale` (`actual=unreadable`), never a match. A present non-string `"sha256"` is malformed. Unknown JSON keys are ignored, as before this round. A match proceeds to the existing span verdict (`supported` when the span is present; `unsupported` when absent). If `"sha256"` is absent, behavior is unchanged. Existing source-boundary refusals retain precedence: a refused source is never opened or hashed.

This is the lane's contract for `verify-claims`, not a schema or verdict requirement imposed by the cited sources. [S058] is the same move for a browser: hash the response, compare it with the expected metadata, fail when nothing matches. [S059] is what a SHA-256 hex digest is in Python; it does not say the hex is lowercase, so the lowercase rule is the lane's own.

## Why pin the revision

SKILL.md's executable checklist says that every claim carries a resolvable pointer to the artifact **and revision read**. A path alone identifies where to look, not which contents were read. Recording a digest with the claim makes that revision clause runnable: the gate can compare the recorded content identity with the source bytes now presented before it reuses the span check. This is a content pin, not a source-truth judgment.

## Why hash exact bytes

The pin covers the whole source file as bytes, not a decoded or normalized representation and not just the quoted span. Thus a CRLF-to-LF change, or adding/removing a final newline, changes the digest even when the displayed text looks the same. Normalizing such differences before hashing would stop the pin from distinguishing those exact source revisions.

## Precedence and outcome

1. A malformed present `"sha256"` is `invalid` (`CLAIM_RECORD_INVALID`).
2. A source refused by existing boundary checks remains `refused`; it is not read or hashed.
3. Otherwise, a valid pin that differs from the exact source bytes is `stale` (`CLAIM_SOURCE_REVISION_MISMATCH`), even if the span is absent.
4. Only after the pin matches (or when the field is absent) does the existing span check determine `supported` or `unsupported`.

The result is measured by `python3 corpus/evidence/round31/c2-count.py`; see SCORECARD.md, section "Round 31". A claim without a pin is not checked for revision; that is a named limit, not drift.

## Limits

- The digest pins content, not a Git commit or repository revision. Different commits with identical source bytes have the same content pin.
- Hashing and reading are not an atomic snapshot: if the file changes between those operations, this check does not eliminate that time-of-check/time-of-use race.
- A matching digest establishes byte identity for the checked content only. It does not prove that the claim is true, that the span is meaningful in context, or that the source itself is correct.
