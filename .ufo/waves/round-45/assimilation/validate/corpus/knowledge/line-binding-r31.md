# Binding a claim to its named line range — round 31

source: S057 https://www.rfc-editor.org/rfc/rfc5147.txt §2.2.3 "Line Position", §2.2.4 "Line Range"; frozen contract `corpus/evidence/round31/claims.md` §C1 (design v2); `corpus/knowledge/claim-verification-r2.md`; `corpus/knowledge/anchor-boundaries-r4.md`; `corpus/knowledge/claim-support-states-r24.md`
verified-at: 2026-10-23 UTC (round 31; S057 opened once by the L1 on 2026-10-23, HTTP 200, 37422 bytes; its located quote is in `corpus/lessons/round-31.md` `## Gate`. The counter's measured result is in SCORECARD.md, section "Round 31")
recheck: 365d (from the lane root: `python3 corpus/evidence/round31/c1-count.py`; re-read C1 if the gate's `at=` numbering changes)

## The move

Round 2 established that `verify-claims` locates a boundary-delimited span somewhere in its cited source; round 4 made the span's token boundaries explicit. Neither binds that occurrence to a line range named by the claim. Round 31 C1 adds an optional JSON string field, `"line"`, so a present span must also occur at the named line or range. The line reference is a separate location assertion, not a change to what the quoted span means.

## Contract

A claims JSONL record may carry `"line"` as a JSON string in either form:

- `"N"` names one line.
- `"N-M"` names a range, with the span starting on line N and ending on line M.

N and M are decimal, N is at least 1, neither has a leading zero, there are no spaces, and for a range M is greater than N. Any other value of a present `"line"` is invalid: `observed=invalid`, finding `CLAIM_RECORD_INVALID`.

Line numbers are 1-based and counted by newlines, as in the gate's `at=`; the bound occurrence need not be the first one, which is the only one `at=` reports when no line is named. The mismatch finding reads `FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=<claim id> …`. If no boundary-delimited occurrence of the span exists, the outcome remains `observed=unsupported`. If the span exists and `"line"` is present, it is bound only when some boundary-delimited occurrence starts on N and ends on N for `"N"`, or starts on N and ends on M for `"N-M"`. A bound claim retains its existing verdict (for example, `supported` when `expect=supported`). If the span occurs but none of its boundary-delimited occurrences spans the named line or range, the outcome is `observed=mislocated` with finding `CLAIM_LINE_MISMATCH`. When `"line"` is absent, behavior is unchanged.

RFC 5147 [S057] names parts of a text/plain entity by line position or line range, and it counts differently: "Line position counting starts with zero, so the line position before the first line of a text/plain MIME entity has the line position zero" (§2.2.3). A position sits *between* lines; a range runs from one position to another (§2.2.4). The gate's `at=` and the C1 `"line"` field number the lines themselves from 1. So RFC `line=3,5` (positions 3 to 5) covers the gate's lines 4 and 5, which is `"line":"4-5"`. Never copy an RFC fragment index into `"line"` without converting it.

## Worked examples

These are contract illustrations, not executions.

- **A later occurrence binds.** The source has a delimited occurrence of `quoted words` on line 3 and another on line 9 (`quoted words.`). A claim with span `quoted words` and `"line":"9"` binds to the later occurrence: the named line contains a boundary-delimited occurrence even though an earlier occurrence exists elsewhere.
- **A glued copy does not bind.** The source has `prefixquoted words` on line 4 and a delimited `quoted words.` on line 8. With span `quoted words` and `"line":"4"`, the bytes on line 4 are glued to the preceding word and are not a boundary-delimited occurrence. Since the span is found delimited on line 8 but not on the named line 4, the line-4 claim is mislocated; the glued substring cannot satisfy the location assertion.
- **A multi-line span needs a range.** If the span is `alpha\nbeta`, with `alpha` on line 20 and `beta` on line 21, its coordinates are 20 through 21. `"line":"20"` does not describe that span's end line; `"line":"20-21"` does. The range must name both the actual start and actual end.

## Why the named line is a separate observation

`claim-support-states-r24.md` defines state 3 as the source stating the claim **at a named anchor**. Finding the span somewhere establishes only an occurrence at the location the matcher found; it does not establish that the record's named location is where that occurrence sits. C1 makes that location assertion checkable by pairing the span occurrence with the line or range in the claim. This is a structural location check, not semantic entailment: it does not determine whether the span supports the proposition or whether the named line is the right place for its meaning.

## Result

Measured by `python3 corpus/evidence/round31/c1-count.py`; see SCORECARD.md, section "Round 31". Unknown JSON keys in a claim record are ignored, as before this round.

## Limits — “Not claimed” in `claims.md`

C1 does not claim the semantics or truth of a span; that a named line is the right line for the claim's meaning; git-revision binding (the C2 pin is a content hash of bytes, not a commit); verification of `## Claims` table pointers (`path:N`) in `verify` mode; verification of `verify-chain` hops; or protection from races if a source changes during reading or hashing.
