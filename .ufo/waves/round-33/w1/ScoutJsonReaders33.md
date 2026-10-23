# ScoutJsonReaders33 — regex / flat JSON field readers

Read-only. No lsp device in this seat's tool inventory; inventory is Read/Grep of `tools/research-gate.sh`, `tools/quote-reopen.py`, and `corpus/evidence/**/*count*.py`, plus one bash probe of copied patterns (not a gate run, not `c1-count.py`). Probe: `bash /fast/scratch/hyaku/chousa-r33/w1/ScoutJsonReaders33/probe.sh` exit 0. Functions copied from `tools/research-gate.sh:1109-1128`; sed copied from `:3386-3389` and `:3506`.

C1 surface, per `corpus/evidence/round33/claims.md:18-19`: `json_str` / `json_has_key` (`tools/research-gate.sh:1109-1128`) and their `verify_claims` callers (`:1448-1483`). Grep of `\b(json_str|json_has_key|jfield)\b` shows no other call site.

## In C1's surface

| path:line | reads | nested / duplicate |
|---|---|---|
| `tools/research-gate.sh:1109-1117` `json_str` | first `"KEY"\s*:\s*"…"` string body; key bytes literal | Nested same name **before** the top-level member wins. Probe `{"meta":{"line":"9"},"id":"A","line":"1"}` → `has=1 str=9`. Nested **after** does not: `{"id":"A","line":"1","meta":{"line":"9"}}` → `str=1`. Duplicate: first wins (`{"line":"1","line":"9"}` → `str=1`); a later copy does not change the value. |
| `:1119` `jfield` | `json_str` or empty | same |
| `:1121-1128` `json_has_key` | any `"KEY"\s*:` | Nested-only flips absent→present: `{"id":"A","meta":{"line":"9"}}` → `has=1 str=9`. A second copy does not change the boolean. Non-string value is present but not a string: `{"sha256":{"v":"abc"}}` → `has=1 str=<absent>`; `{"line":5}` → `has=1 str=<absent>`. |
| `:1448-1459` | `id`, `marker_default`, `source`, `span`, `expect`, `marker` via `json_str`/`jfield` | same first-match rule |
| `:1464-1482` | `line`, `sha256` via `json_has_key` then `json_str` | same |

`marker_default` (`:1448-1449`) is inside that caller range and uses the same helpers. `claims.md:80` excludes it from the counted predicate ("not counted"). It is on the helper surface, off the 144-record predicate.

Not matched, same helpers (the Not-claimed exclusions):

- Escaped key spelling. Probe `{"l\u0069ne":"9","id":"A"}` key `line` → `has=0 str=<absent>`. `json_unescape` (`:1130-1168`) runs only on an already matched value body, never on the key.
- Key text inside a string. Probe `{"id":"A","note":"{\"line\":\"9\"}"}` → `has=0 str=<absent>`. The selftest fixture at `:7365-7369` asserts only this half. The comment at `:7358-7364` says the object form `{"meta":{"line":"9"}}` is not asserted (observed there as `line=9-9`).
- Duplicated unread keys. Callers name only `id`, `marker_default`, `source`, `span`, `expect`, `marker`, `line`, `sha256`. Probe `{"id":"A","note":"x","note":"y"}` key `id` → `str=A`. No code path inspects `note`.
- Not-valid JSON. `:1442` only requires the trimmed line to start with `{` and end with `}`. There is no parser on the claim line. That is a property of this reader, not a second site.

## Out of C1 — other regex / flat readers

Production `verify-all` does **not** parse manifest fields. It writes the line (`:3263-3265`, `json_escape` `:3057`, `json_counts` `:3077`) and reads only the last byte for the delimiter (`:3266-3273`). `claims.md:82` ("verify-all manifest parsing uses python3 where present") is true only of the selftest validity checks below, which discard the object. The field checks beside them are grep.

| path:line | reads | nested / duplicate | C1 |
|---|---|---|---|
| `:3383-3391` `gate_drift_normalize` | global sed `"ts":"[^"]*"` and `"gate_sha256":"[^"]*"` → `<V>` | Nested and duplicate **values** of those two keys are masked (`nested-ts` and `dup-ts` both became `"ts":"<V>"`). A different value does not survive. The extra key text remains, so a second `"ts"` still differs from one key as bytes. String-escaped `"ts"` is not masked (`str-ts` left `\"ts\":\"1999…\"`). | out (drift/pin) |
| `:3464` `gate_canonical_capture` | line count of `^{"schema":"chousa-verify-all/v1"` | Anchored. Probe line with schema only inside `meta` → MISS. A later duplicate on the same line does not add a count. | out |
| `:3496-3514` `gate_drift_scan` | sed `"key":` → `key=`, commas → spaces, then `key=value` tokens; duplicate values concatenated (`:3513`, comment `:3499`) | Duplicate changes the stored value (tokens `line="1"` and `line="9"`). A nested key **after a comma** becomes its own field: `{"meta":{"x":1,"line":"9"},"id":"A"}` → tokens `meta={x=1`, `line="9"}`, `id="A"}`. A nested key with no comma before it stays inside the parent token (`{"meta":{"line":"9"},…}` → `meta={line="9"}` only). String-escaped `"line"` stayed inside `note=`. `sections[0].verdict` was extracted as its own `verdict` token. | out (drift) |
| `:4860-4863` `tall` | unanchored `"schema":"chousa-verify-all/v1"`, `"record_sha256":"[0-9a-f]{64}"`, `"gate_sha256":"[0-9a-f]{64}"`, `"verdict":"CLEAN"` | Nested spelling hits. Probe object whose only schema/sha/verdict were under `meta` → HIT, HIT, HIT. `grep -q` presence: a second copy does not change the result once one match exists. | out (selftest) |
| `:4855-4858` `tall` | `python3 json.loads`, object discarded | validity only, and only `if command -v python3`. Not a field read. | out |
| `:5991` `r24_case` | `^{"schema":"chousa-verify-all/v1"` on line 2 | anchored; same as `:3464` | out |
| `:5994` `r24_case` | whole line 1 `== '{"prior":true}'` | not a field read; any nested or extra key fails equality | out |
| `:5996-5999` | `json.loads`, discarded | validity only | out |
| `:7184` c1lk | whole line `== '{"frag":229}'` | not a field read | out |
| `:7185`, `:7215` | `^{"schema":"chousa-verify-all/v1"` (line 2; line count) | anchored; nested schema does not match; a second schema on the same line does not raise `grep -c` | out |
| `:7190-7193`, `:7221-7224` | `json.loads`, discarded | validity only | out |
| `:3163` | `grep -c '^[[:space:]]*{'` to decide the file is claims JSONL | shape, not a field. A `{` line that is not an object still counts. | out |

`:7358-7369` is a fixture and a comment, not a reader. It feeds the C1 helpers the string-escape case only.

## Not regex readers (checked, excluded)

- `tools/quote-reopen.py`: no `json` import. `re.search` at `:119` is a URL in a markdown cell.
- `corpus/evidence` counters: regexes are gate stdout or prose (`^CLAIM id=`, `^FINDING`, `^CHAIN hop=`, `MATCH=n/n`, `https?://`), not JSON keys. `round33/c1-count.py:318` `json.loads` only asserts each generated row is an object. `round32/c1-count.py:178-194` and `c1-count-v2.py` (same shape) parse manifest lines with `json.loads` and `o.get("schema")` — a parser, top-level key, not a regex. Duplicate-key policy of that parser was not measured here.

## Not-claimed list vs this inventory

`claims.md:80-83` holds for the counted predicate: `marker_default`, `\u` key spellings, duplicated unread keys, non-JSON records, and span truth are not separate counted surfaces. The parenthetical "any other mode's JSON reading (verify-all manifest parsing uses python3 where present)" is too narrow. Production verify-all does not parse manifest fields. Where fields are read outside `verify_claims`, it is sed/grep (`:3388-3389`, `:3464`, `:3506-3513`, `:4860-4863`, `:5991`, `:7185`, `:7215`). Python is only a discard-on-parse validity check, and only when `python3` is on `PATH`. Those grep sites are outside C1. Unanchored ones (`tall`) and `gate_drift_scan` (after a comma) do change result on a nested key; anchored `^{"schema"` checks do not.

No installs. Probe script left at `/fast/scratch/hyaku/chousa-r33/w1/ScoutJsonReaders33/probe.sh`.
