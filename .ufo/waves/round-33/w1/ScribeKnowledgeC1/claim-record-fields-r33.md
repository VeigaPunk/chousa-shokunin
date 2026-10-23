# Read claim-record fields only at the top level — round 33 (draft)

source: Pending source-row completion: `S062` (RFC 8259 §4, Objects; RFC source scribe reports this row is being drafted) and `S0XX-pyjson` (Python `json` documentation, repeated names; L1 ID pending); frozen lane contract `corpus/evidence/round33/claims.md` §C1. The source pages and final SOURCES.md row metadata were not inspected in this pass; do not admit this draft until both source rows have the required mined status, exact anchors, and this entry in `used-by`.
verified-at: 2026-10-23 UTC (read `corpus/QUALITY.md` entry criteria, the frozen round-33 C1 contract, its source-registry context, the round-31 counter note, and the cited gate code; external source pages were not opened in this pass)
recheck: on-release (from the lane root: `python3 corpus/evidence/round33/c1-count.py`)

## The defect

Before C1, `json_str` searched a raw claim-record line for a quoted key followed by a string value, and `json_has_key` searched the raw line for a quoted key followed by a colon (`tools/research-gate.sh:1109-1128`). Neither regex parsed JSON nesting or counted top-level occurrences. `verify_claims` used these helpers for the record fields (`tools/research-gate.sh:1448-1483`): for example, it reads `id`, `source`, `span`, `expect`, `marker`, optional `line`, and optional `sha256` from that raw line. As a result, a matching member inside a nested value could be mistaken for a record field, and a duplicate top-level field could be silently resolved by whichever match the regex finds first. The frozen contract records this defect and its surface (`corpus/evidence/round33/claims.md:18-27`).

This is the carried round-31 finding, not a new measurement in this draft: the round-31 counter note says a nested `"line"` under unknown key `meta` was read as the record's own field and produced `mislocated` on that then-landed gate (`corpus/evidence/round31/c1-count-v3.py:16-22`).

## Contract

For `verify-claims`, a claim record is one JSON object per line. The seven read keys—`id`, `source`, `span`, `expect`, `marker`, `line`, and `sha256`—are read from that top-level object only. A same-named member in a nested object or array is not the record field and changes nothing. A top-level read key occurring more than once makes the record `invalid` with `CLAIM_RECORD_INVALID`, even when the duplicate values agree. JSON punctuation, escaped quotes, trailing escaped backslashes, and field-like text inside a JSON string are string content, not structure. All other round-31/32 behavior is unchanged by this contract (`corpus/evidence/round33/claims.md:29-40`).

## What a researcher writing claims JSONL should know

Nested metadata is allowed as a JSON value and is ignored when choosing the claim's read fields. For example, a top-level `line` value is the claim's location; a `line` member under `meta` is not. Do not repeat any of the seven read keys among the top-level members: the record is invalid rather than first-value-wins or last-value-wins. Repeating a key that is not one of the fields this gate reads is outside this duplicate-key rule (`corpus/evidence/round33/claims.md:30-40,80-83`).

The citation rationale has two parts. RFC 8259 §4 says object names SHOULD be unique and duplicate names make receiver behavior unpredictable (`S062`; RFC source scribe reports this assigned ID, but its row was not inspected in this pass; frozen contract `claims.md:34-36,87-90`). The planned Python `json` documentation citation concerns repeated names and a common reader retaining the last value (`S0XX-pyjson`, pending L1 ID; frozen contract `claims.md:90-91`). That parser behavior is not the lane's policy: C1 rejects duplicate *read* keys instead of choosing either occurrence. The Python source ID remains pending, and neither source page was independently reopened for this draft.

## Evidence boundary

This entry explains the frozen contract; it is not evidence that a candidate implementation meets it. The frozen counter and its acceptance predicate are specified in `corpus/evidence/round33/claims.md:42-59`; no candidate or counter was run for this draft.

## Limits — “Not claimed” in `claims.md`

C1 does not claim behavior for `marker_default` rows (read by the same helpers, not counted); keys spelled with JSON escapes (for example, `"l\\u0069ne"`); duplicated unread keys; records that are not valid JSON; JSON reading in other modes (including `verify-all` manifest parsing); or the semantics or truth of a span (`corpus/evidence/round33/claims.md:80-83).
