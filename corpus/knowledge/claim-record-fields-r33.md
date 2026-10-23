# Claim-record fields are read from the top-level object only — round 33

source: S062 (RFC 8259 §4 Objects), S063 (Python `json` documentation, repeated names); lane contract `corpus/evidence/round33/claims.md` C1 (design v2)
verified-at: 2026-10-23 (both sources opened by ScribeSourceRFC8259 / ScribeSourcePyJson and re-opened by the L1: `.ufo/waves/round-33/measure/reopen-L1.txt`; gate behaviour measured on gate SHA-256 `52f07c74…1b2a`)
recheck: on-release (lane root: `python3 corpus/evidence/round33/c1-count-v2.py` → `TOPLEVEL_FIELD_MATCH=156/156`)

## The defect

Up to round 32, `verify-claims` read a claim record's fields with two unanchored regexes over the
raw line: `json_str` (a quoted key, a colon, a string value) and `json_has_key` (a quoted key and a
colon). Neither knew where a member sat. A member named `line`, `sha256`, `id`, `source`, `span`,
`expect` or `marker` inside a nested object or array was read as the record's own field when it
came first on the line, and a duplicated top-level field silently took its first value. Round 31
measured the nested case (`{"meta":{"line":"9"}}` read `mislocated`,
`corpus/evidence/round31/c1-count-v3.py:16-22`); the round-32 outside check routed it as D4.

## The rule now

- A claim record is one JSON object per line. The gate reads `id`, `source`, `span`, `expect`,
  `marker`, `line`, `sha256` (and `marker_default` on default rows) from the members of that
  top-level object only. A member of the same name inside a nested object or array is part of a
  skipped value and changes nothing.
- A read field that appears more than once among the top-level members makes the record
  `invalid` (`CLAIM_RECORD_INVALID … duplicate top-level key <k>`), even when the values agree. The
  CLAIM line keeps the record's id; a duplicated `id` prints that id only when both values are
  identical, otherwise `id=line<N>`.
- Braces, brackets, colons, commas, escaped quotes and a trailing escaped backslash inside a JSON
  string are string content. A line that is not one well-formed object (unbalanced or mismatched
  brackets, an unterminated string, bytes after the closing brace, a member name that is not a
  string) reads `CLAIM id=line<N> … observed=invalid`.

Implementation: `claim_scan` in `tools/research-gate.sh` (one pass per record in the C locale,
string- and escape-aware, bracket stack over `{}` and `[]`), with `json_str`, `json_has_key` and
`json_dup` answering from its depth-1 table.

## Why duplicates fail closed

RFC 8259 §4 recommends unique names — "The names within an object SHOULD be unique." (line 322)
— and says that when they are not, receiver behaviour is unpredictable: "Many implementations
report the last name/value pair" (line 333; the sentence ends "only." on line 334, and the next
sentence says other implementations "report an error or fail to parse") (S062). Python's decoder
keeps the last: "it ignores all but the last name-value pair for a given name" (S063). A
first-wins regex and a last-wins parser therefore read the same record differently. Refusing such
a record, as the RFC's error-reporting implementations do, rather than picking one value is this
lane's design choice; neither source says a verifier must.

## What a researcher writing claims JSONL should know

- Nested metadata is allowed: `{"id":"c1", …, "meta":{"line":"9","note":"…"}}` is verified on its
  top-level fields only.
- Never repeat a read key at the top level; the record is refused, not resolved.
- A key spelled with a JSON escape (`"l\u0069ne"`) is not the plain key: the reader compares member
  names as written (not claimed either way).

## Measured (round 33)

`python3 corpus/evidence/round33/c1-count-v2.py` (156 records, 15 classes): base gate
`f4731885…` 60/156; landed gate `52f07c74…` 156/156 on seeds 3351 and 3352
(`.ufo/waves/round-33/measure/candidate/`). No pre-data control reached 156; the best non-oracle
control (duplicates invalid only when values differ) scored 142/156
(`.ufo/waves/round-33/controls/L1-v2-rescore/summary.txt`).

## Limits

- Not counted: `marker_default` rows, a duplicated `marker`, an `id` duplicated with differing
  values, keys spelled with escapes, duplicated unread keys, malformed lines (the reader refuses
  them; no counter class measures it).
- Cost: the bash walk reads one character per `${s:i:1}`, which costs time proportional to the line
  length, so one record costs roughly quadratic time in its length (ExecParserCost33: about 1.7 ms
  for 500 bytes, about 3.5 s for 64 KiB). `json_unescape` already walked field values the same way
  before round 33.
- Other modes read JSON by other means (`gate_drift_scan` and selftest greps); they are outside
  this rule (ScoutJsonReaders33).
