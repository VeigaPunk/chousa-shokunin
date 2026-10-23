# ReviewCounterV3 — round-31 counters v3 vs v2, run on landed round-32 gate

Scope: diff `corpus/evidence/round31/{c1,c2}-count-v3.py` vs the frozen v2
(`{c1,c2}-count.py`), check the new non-string class truth against the
round-31 contract, run each once on landed gate 10f2fe12 (rev 5d8a1707).

## Diff v3 vs v2 (both counters, only deltas)

- `TOTAL` 120 → 132; new class `I2_nonstring_*` (12 claims: number, null,
  true, false, array, object ×2) with truth `invalid`
  (c1-count-v3.py:77,220-224; c2-count-v3.py:71,204-208).
- `None` sentinel → `ABSENT = object()` so a present JSON `null` is emitted,
  not treated as absent (c1:144,254-255; c2:90,180,209-215). In v2 `sha=None`
  skipped the key entirely; v3's `null` sub-variant is the only value this
  change affects — confirmed by reading generate().
- Receipt schema label v2 → v3; all other scoring logic byte-identical.

## Truth vs round-31 contract — MATCHES

- C1 contract item 1 (claims.md:74-76): "Any other value of a present 'line'
  makes the record invalid". Gate enforces via `json_has_key` (gate:1464) +
  `json_str` failure → `bad="line not a JSON string"` → `observed=invalid`
  (gate:1500-1524). All six non-string kinds (incl. `"line":["5"]`,
  `"line":{"n":5}` — `json_str` requires a `"` right after `:`) take this arm.
- C2 contract item 1 (claims.md:141-143): same for `"sha256"`; gate sets
  `sha_present=1`, leaves `sha_pin='-'` for non-strings, regex
  `^[0-9a-f]{64}$` fails → invalid (gate:1471-1495). I2 spans are present
  (c2-count-v3.py:168 excludes only absent classes), so a gate treating a
  non-string pin as absent reports `supported` and misses — correct trap.
- Finding rule unchanged: only mislocated (C1) / stale (C2) need FINDING
  lines; invalid requires none — gate emits no per-claim FINDING for
  CLAIM_RECORD_INVALID's own line, matching counter's flagged check.
- No masking defect found: values carry no inner `"line":`/`"sha256":` string
  (docstring c2:205-206 verified in code), `null`/`true`/`false`/numbers/
  arrays/objects all fail `json_str` on the landed gate.

## Runs on landed gate (SHA-256 10f2fe12…4098, verified vs rev 5d8a1707)

- `C1_TMP=<scratch>/tmp python3 corpus/evidence/round31/c1-count-v3.py
  --seed 882013 --receipt …/c1-v3-s882013.json` → exit 0,
  `LINE_BINDING_MATCH=132/132`, every class full incl. I2 12/12;
  receipt gate_rc=1, predicate_holds=true, misses=[].
- `C2_TMP=<scratch>/tmp python3 corpus/evidence/round31/c2-count-v3.py
  --seed 779014 --receipt …/c2-v3-s779014.json` → exit 0,
  `REVISION_BINDING_MATCH=132/132`, I2 12/12; same receipt verdict.
- Receipts: `.ufo/waves/round-32/w2/ReviewCounterV3/c{1,2}-v3-*.json`.
- Both counter runs on this lane revision in this wave: 2, neither below
  132/132.

## verify-claims unchanged by the round-32 landing

- `git show 7a7259f0:tools/research-gate.sh` = base gate 0bc318b3…1258.
- Diff vs landed: 28 hunks; all in doc comments, verify_chain (base
  1785-1906 → landed 1813+), verify_all manifest append (3192-3202 →
  3273+), selftest fixtures (6802,6871 → 6910,6980+).
- Claims region base:1080-1625 == landed:1107-1652 byte-identical
  (`diff -q` → identical). Helpers `json_str`/`json_has_key`/`tok_span_*`
  and `verify_claims` untouched. Empirical: both v3 counters score identical
  132/132 — consistent with unchanged verify-claims.

## Verdict

HOLDS. The v3 counters faithfully encode the round-31 contract for
non-string "line"/"sha256" values (truth=invalid), the landed round-32 gate
scores 132/132 on both, and verify-claims behaviour is unchanged by the
round-32 landing. No run below target, no contract violation observed.

## Limits / residual

- One run each (per task), seeds fixed for reproducibility; v3 is a
  round-31 instrument on round-32's gate — it measures verify-claims only,
  not the round-32 surfaces (manifest append, exempt arm).
- The nested-key carrier (`{"meta":{"line":"9"}}` read as the record's own
  field via flat regex, gate:1121-1128) is a disclosed gate defect
  (v3 docstring; "Not claimed"/carried), deliberately not in the fixture.
- Docstring claims about MutC1Grammar (85d85a7b) / MutC2Parse (f9da8257)
  mutants not re-verified — mutants are never candidates.
