# Round 33 — frozen claim (design v1)

Base `2b9cc73aed30c2e2c95699db6617d9531ef49fb2` (lane `master`). Gate at base:
`tools/research-gate.sh` SHA-256 `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`
(the landed round-32 gate). Counter (this commit): `corpus/evidence/round33/c1-count.py`, SHA-256
`ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229`. Every receipt records the
counter that produced it (`counter_sha256`); only receipts carrying that hash count for design v1.

One claim this round. The round-32 routed defects D1–D5
(`corpus/lessons/round-32-verifier-spotcheck.md:152-169`) are repairs, not claims: D4 is the
defect C1 removes; D1 (the exempt-hop counter whose fixture order encodes the truth), D2 (receipt
tally), D3 (battery revision header) and D5 (signals by name) are repaired outside the counter and
never enter it. The repair of D1 is quality work on a rule the lane already holds; it is not a
coverage claim (round prompt §6.9).

## C1 — operability (lowest scored axis: the only scored axis, `SCORECARD.md:7`)

**Surface.** `verify-claims`' claim-record field reader: `json_str` and `json_has_key`
(`tools/research-gate.sh:1109-1128`) and their callers in `verify_claims`
(`:1448-1483`). Both are unanchored regexes over the raw line, so a member named `"line"`,
`"sha256"`, `"id"`, `"source"`, `"span"`, `"expect"` or `"marker"` inside a nested object or array
is read as the record's own field when it comes first, and a duplicated top-level field silently
takes its first value. The round-31 contract says unknown keys are ignored
(`corpus/evidence/round31/c1-count-v3.py:43`); a nested member under an unknown key is not ignored
(measured on the round-31 gate: `{"meta":{"line":"9"}}` reads `mislocated`,
`c1-count-v3.py:16-22`). Carried as round-31 D-C and round-32 D4. Operability (AXES.md): the
checklist command `verify-claims` does not produce its stated outcome on such records.

**Contract.**
1. A claim record is one JSON object per line. The fields the gate reads — `"id"`, `"source"`,
   `"span"`, `"expect"`, `"marker"`, `"line"`, `"sha256"` — are members of that top-level object
   only. A member of the same name inside a nested object or array value is not the record's
   field and changes nothing.
2. A read field that occurs more than once among the top-level members makes the record
   `invalid` (`CLAIM_RECORD_INVALID`), whether or not the values agree (RFC 8259 §4: duplicate
   names make receiver behaviour unpredictable; the gate fails closed).
3. Characters inside JSON string values (`{ } [ ] : ,`, escaped quotes, a trailing escaped
   backslash, text that looks like a member) are string content, never structure.
4. Everything else is the landed round-31/32 `verify-claims` behaviour: line and sha256 binding,
   verdicts, findings, exit codes. Records without nesting or duplicates verify exactly as at base.

**Counter.** `python3 corpus/evidence/round33/c1-count.py [--gate PATH] [--seed N] [--receipt F]
[--keep DIR]` (lane root). 144 records in 15 classes with fixed sub-variant counts (nested decoys
of each read field before and after the top-level member, in an object, an array and a two-level
container; nested-only fields; top-level wrong with nested right; duplicated top-level fields;
string confusers flat and nested; flat plain records). Every record carries `expect=supported`;
truth is hidden. Matching rule: the counter's docstring (same text): one `CLAIM id=<top-level id>`
line with `observed=` equal to the truth, `CLAIM_LINE_MISMATCH` naming the id iff the truth is
`mislocated`, `CLAIM_SOURCE_REVISION_MISMATCH` naming the id iff the truth is `stale`.

**P1 (frozen predicate).** C1 is met iff, on the landed lane revision, this counter prints
`TOPLEVEL_FIELD_MATCH=144/144` (receipt label `predicate_holds=true`) on each of two fresh-seed
runs, and no run of this counter on that revision in round 33 prints a lower count.

Code condition: `holds = matched == TOTAL` with `TOTAL = 144`. Receipt label: `predicate_holds`.

**Kill rule.** Any committed run of this counter on the landed revision below 144 is a miss. A
miss is reported as an honest stop; the counter, TOTAL and P1 are never amended after a candidate
is scored.

**Before (do-nothing control, L1).** Base gate (`f4731885…`), seed 3301:
`TOPLEVEL_FIELD_MATCH=60/144` (every nested-before decoy, nested-only, duplicate and
nested-confuser record misses; flat records 24/24). Feasibility oracle (L1, never a candidate): the
base gate with `json_str`/`json_has_key` replaced by a python3 `json.loads` top-level reader plus a
duplicate-read-key check, 144/144 on seeds 3302 and 3303 — receipts and the oracle builder under
`.ufo/waves/round-33/controls/L1-design/`.

**Pre-data controls (required before any candidate is scored).** Mutation-tester and executor
seats build and score, with this counter as committed: do-nothing (base gate) on fresh seeds;
all-invalid / junk / no-reader (never opens a source); last-occurrence-wins; brace-depth tracking
that ignores strings; string-aware depth tracking that mishandles `\\"`; strip nested `{…}` by
regex then read flat; drop records holding any nested container (invalid); ignore duplicates
(first or last wins); shortcuts keyed on the counter's ids, file names, class shapes or container
names. Their receipts are committed before the first candidate receipt. A control that meets
144/144 sends the design back to v2 before data.

**The command that would show C1 unmoved:** this counter on the landed gate printing a count below
144, as the base does (60/144).

**Not claimed.** `marker_default` rows (read by the same helpers, not counted); keys spelled with
JSON escapes (`"l\u0069ne"`); duplicated unread keys; records that are not valid JSON; any other
mode's JSON reading (`verify-all` manifest parsing uses python3 where present); semantics or truth
of a span.

## Sources (frontier step)

C1 rests on a `SOURCES.md` row opened this round: RFC 8259 (The JavaScript Object Notation (JSON)
Data Interchange Format), §4 Objects — names SHOULD be unique; duplicate names make receiver
behaviour unpredictable; object members are name/value pairs and values may themselves be objects
or arrays. A second row (Python `json` documentation, repeated names) may record that a common
reader keeps the last value, which is why the gate fails closed instead of picking one.
