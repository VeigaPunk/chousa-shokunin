# Claim-record fields are read from the top-level object only — round 33

source: S062 (RFC 8259 §4 Objects), S063 (Python `json` documentation, repeated names); lane contract `corpus/evidence/round33/claims.md` C1 (design v2)
verified-at: 2026-10-23 (both sources opened by ScribeSourceRFC8259 / ScribeSourcePyJson and re-opened by the L1: `.ufo/waves/round-33/measure/reopen-L1.txt`; gate behaviour measured on the final round-33 gate SHA-256 `43a1af35…4346`)
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
  CLAIM line keeps the record's id; a duplicated `id` prints that id only when every repeat is a
  string with the same raw body as the first, otherwise `id=line<N>`. A marker_default row with a
  repeated read field is refused the same way.
- Braces, brackets, colons, commas, escaped quotes and a trailing escaped backslash inside a JSON
  string are string content. A line that is not one well-formed object (unbalanced or mismatched
  brackets, an unterminated string, bytes after the closing brace, a member name that is not a
  string, whitespace other than space/tab/CR/LF, a bare token that is not a JSON literal or
  number, an escape outside RFC 8259 §7) reads `CLAIM id=line<N> … observed=invalid`. An escaped
  NUL in a read string field is refused (bash would drop it).

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
`f4731885…` 60/156; candidate `52f07c74…` 156/156 on seeds 3351 and 3352
(`.ufo/waves/round-33/measure/candidate/`); final gate `43a1af35…` 156/156 on seeds 3701 and 3702
(`measure/final/`). **The counter does not verify clause 3 (string content):** a gate that masks
its six fixed confuser strings also scores 156/156 (`.ufo/waves/round-33/w2/L1ShortcutMask/`).
The reader's string handling rests instead on a differential fuzz against an independent python
reference: 1950/1950 records agree on the final gate (`measure/final/fz-9021{2,3,4}.json`). No pre-data control reached 156; the best non-oracle
control (duplicates invalid only when values differ) scored 142/156
(`.ufo/waves/round-33/controls/L1-v2-rescore/summary.txt`).

## Limits

- Not counted: `marker_default` rows, a duplicated `marker`, an `id` duplicated with differing
  values, keys spelled with escapes, duplicated unread keys, malformed lines. Not checked at all:
  raw control bytes inside strings, and member grammar inside nested values beyond bracket
  balance and bare tokens (as at base).
- Cost: the reader consumes string bodies and tokens with one regex match per run, not one
  `${s:i:1}` per byte (a substring costs time in the line length): a 64 KiB unread member takes
  0.11 s (base 0.07 s; the byte-walk candidate took 4.7–6.1 s, ProbeLongLines33). `json_unescape`
  still walks read field values byte by byte, as before round 33; spans of 32 KiB or more cannot be
  located at all (`tok_span_at` argv limit, base too).
- Other modes read JSON by other means (`gate_drift_scan` and selftest greps); they are outside
  this rule (ScoutJsonReaders33).
