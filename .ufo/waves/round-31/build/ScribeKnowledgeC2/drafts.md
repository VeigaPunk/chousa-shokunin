source: S058; S059.
verified-at: 2026-10-23 — draft based on the frozen C2 contract and SKILL.md Checklist item 1; source rows cited by ID only and not re-opened here.
recheck: Results measured by c2-count.py; see SCORECARD Round 31.

# Pin a claim to the source bytes read

## The rule

The lane's C2 contract adds an optional JSON string field, `"sha256"`, to a claim record. If present, it must be exactly 64 lowercase hexadecimal characters. A malformed value makes the record `observed=invalid` with `CLAIM_RECORD_INVALID`.

For a valid pin, compare it with the SHA-256 digest of the exact bytes of the claim's source file. A mismatch is `observed=stale` with `CLAIM_SOURCE_REVISION_MISMATCH`, before and regardless of the span check. A match proceeds to the existing span verdict (`supported` when the span is present; `unsupported` when absent). If `"sha256"` is absent, behavior is unchanged. Existing source-boundary refusals retain precedence: a refused source is never opened or hashed.

This is the lane's contract for `verify-claims`, not a schema or verdict requirement imposed by the cited sources. Integrity mechanisms are the scoped context for [S058] and [S059].

## Why pin the revision

SKILL.md's executable checklist says that every claim carries a resolvable pointer to the artifact **and revision read**. A path alone identifies where to look, not which contents were read. Recording a digest with the claim makes that revision clause runnable: the gate can compare the recorded content identity with the source bytes now presented before it reuses the span check. This is a content pin, not a source-truth judgment.

## Why hash exact bytes

The pin covers the whole source file as bytes, not a decoded or normalized representation and not just the quoted span. Thus a CRLF-to-LF change, or adding/removing a final newline, changes the digest even when the displayed text looks the same. Normalizing such differences before hashing would stop the pin from distinguishing those exact source revisions. [S058] [S059]

## Precedence and outcome

1. A malformed present `"sha256"` is `invalid` (`CLAIM_RECORD_INVALID`).
2. A source refused by existing boundary checks remains `refused`; it is not read or hashed.
3. Otherwise, a valid pin that differs from the exact source bytes is `stale` (`CLAIM_SOURCE_REVISION_MISMATCH`), even if the span is absent.
4. Only after the pin matches (or when the field is absent) does the existing span check determine `supported` or `unsupported`.

The C2 counter result is measured by c2-count.py; see SCORECARD Round 31.

## Limits

- The digest pins content, not a Git commit or repository revision. Different commits with identical source bytes have the same content pin.
- Hashing and reading are not an atomic snapshot: if the file changes between those operations, this check does not eliminate that time-of-check/time-of-use race.
- A matching digest establishes byte identity for the checked content only. It does not prove that the claim is true, that the span is meaningful in context, or that the source itself is correct.
