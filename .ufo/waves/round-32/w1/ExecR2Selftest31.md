# Round 32 W1 — ExecR2Selftest31 (R2, selftest half)

Base: lane `master` @ `4111607c857bc29ff31883bc095ae00afb527e50`, gate `tools/research-gate.sh`
SHA-256 `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` (unchanged since base).
Sandbox clone (jj/git untouched): `/fast/scratch/hyaku/chousa-r32/w1/ExecR2Selftest31/gate-clone`.

## Deliverable

`.ufo/waves/round-32/w1/ExecR2Selftest31/r2.patch` — `git diff` vs `4111607c…`, one hunk
`@@ -6869,6 +6869,143 @@`, **137 insertions, 0 deletions**, all inside `run_selftest()`:
the block starts at patched-gate line 6872 (`# ---- round-32 R2: verify-claims grammar/binding
detectors ----`) immediately after the last existing case (`tclaims claims-sha-crlf`) and ends
before the `if [[ $failures -eq 0 ]]` summary at line 7009. No production mode, no existing case
line changed.

- patch sha256 `792cc1b812492dfc6ba31325bfa8951c61a4e17c5022790a13190a3dd8f32579`
- patched gate sha256 `82470e572345721da36c39f90776893e1f9d735d8172f19f19df276dbf66a8aa`
- `git apply --check` then `git apply` on a fresh clone checked out at `4111607c…` → applied, and
  the result is byte-identical to the working clone (`cmp` + equal sha256).

## Selftest runs (full, bounded)

| run | command | rc | result |
|---|---|---|---|
| base (unmodified 0bc318b3) | `TMPDIR=$PWD/tmp timeout 1800 bash gate-clone/tools/research-gate.sh --selftest` | 0 | `RESEARCH_GATE_SELFTEST: PASS (228 cases, 0 skipped)` 35.4 s |
| patched (82470e57) | same | 0 | `RESEARCH_GATE_SELFTEST: PASS (235 cases, 0 skipped)` 40.9 s |

Base-case invariance: `diff <(grep '^ok-case' base) <(grep '^ok-case' patched | head -228)` is
empty → the 228 base case lines are byte-identical (numbering, names and exit codes unchanged).
Logs: `base-selftest.log` (sha256 `00d3042d…`), `r2-selftest.log` (sha256 `cd5325a7…`) in this
directory.

## Case list — expected outcome (= contract, measured on the landed gate before being asserted)

| # | case | records / fixture | expected and observed |
|---|---|---|---|
| 229 | `claims-r2-sha-nonstring` | `claimsrc/sha-src.txt`; `"sha256"` present as number `5`, `null`, `["<valid hash>"]`, `{"v":"<valid hash>"}` | present non-string is malformed, never absent: 4× `observed=invalid`, `FINDING CLAIM_RECORD_INVALID … sha256 malformed (not 64 lowercase hex characters)`, `VERDICT_BEARING_CLAIMS=0/4`, `invalid=4 … drift=4`, exit 1 |
| 230 | `claims-r2-line-nonstring` | `lib/span.md`; `"line"` as `null`, `["1"]`, JSON float `1.5` | `line not a JSON string`, 3× `observed=invalid`, `0/3`, `invalid=3 … drift=3`, exit 1 |
| 231 | `claims-r2-endline` | `lib/span.md`; EL1 = span lines 2–3 pinned only `"line":"3"`; EX1 = span wholly on line 3 pinned `"3"` | end-line-only binding is not supported: EL1 `observed=mislocated at=lines:2-3`, finding `obs=id=EL1 line=3-3 first_delimited_occurrence=lines:2-3`; EX1 `observed=supported at=line:3`; `1/2`, `mismatched=1 … drift=1`, exit 1 |
| 232 | `claims-r2-span-stale` | `claimsrc/sha-src-tampered.txt` pinned with the *other* file's hash; SB1 span present + line 1, SB2 span present + wrong line 9, SB3 span absent | stale is decided before span and `line`: 3× `observed=stale at=-`, only `CLAIM_SOURCE_REVISION_MISMATCH`, `pin=ed82fd71c85e actual=a1b069a5106d`, `0/3`, `mismatched=3`, exit 1 |
| 233 | `claims-r2-ws-pin` | `claimsrc/sha-src.txt`; 64-hex pin with trailing, leading and both-side spaces | whitespace is not trimmed into a match: 3× `observed=invalid`, `sha256 malformed …`, `invalid=3`, `0/3`, exit 1 |
| 234 | `r2-hash-fault-shim` | `claimsrc/sha-src.txt` + valid pin; `$WORK/r2faultbin/sha256sum` = `#!/bin/sh; exit 127` placed first on PATH | control on the normal PATH reads `observed=supported`, `1/1`, exit 0; under the shim the claim never reads supported: `observed=stale`, `actual=unreadable`, `CLAIM_SOURCE_REVISION_MISMATCH`, `0/1`, exit 1, and no `observed=supported` in the output |
| 235 | `claims-r2-nested-string` | `lib/span.md`; `"note":"{\"line\":\"9\"}"` (key spelling inside a *string value*) | not read as the record's own key: `observed=supported at=line:1`, `VERDICT_BEARING_CLAIMS=1/1`, `CLEAN`, exit 0 |

Case 234 is a custom inline runner (not `tclaims`) because `tclaims` only forwards `CHOUSA_*`
environment overrides and the injection needs `PATH`. It still uses the same fresh-process
discipline (`env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0
CHOUSA_ROOT=$WORK CHOUSA_NOW_EPOCH=$NOW_EPOCH`) and the same `ok-case`/`FAIL-case` accounting.

The "source unreadable at hash time" arm cannot be produced deterministically in-process:
`claim_source_path` refuses anything failing `[[ ! -f $canon || ! -r $canon ]]`
(`tools/research-gate.sh:1218`), so readability would have to be dropped inside the TOCTOU window
before the hash read. Both arms converge on `[[ $sha_actual =~ ^[0-9a-f]{64}$ ]] ||
sha_actual=unreadable` (`tools/research-gate.sh:1512-1516`); the shim exercises that exact branch.
[INFERENCE: the convergence for the chmod arm is read from the code, not run.]

## Finding — nested-key contract violation (measured, not fixed)

The target's item 7 (`{"meta":{"line":"9"}}` is not read as the record's own key) is **violated by
the landed gate**. `json_str`/`json_has_key` are unanchored regexes scanned over the whole line
(`tools/research-gate.sh:1082-1101`), so a nested object's `"line"` is picked up as the record's
field. Probe (artifact `nested-key-probe.txt`, sha256 `6668be38…`), run on the patched gate whose
`verify-claims` is byte-identical:

```
$ CHOUSA_ROOT=probe2 bash gate-clone/tools/research-gate.sh verify-claims nested.jsonl
CLAIM id=NK1 … observed=mislocated source=lib/span.md at=line:1 verdict=mismatch
CLAIM id=NS1 … observed=supported  source=lib/span.md at=line:1 verdict=match
FINDING CLAIM_LINE_MISMATCH … obs=id=NK1 line=9-9 first_delimited_occurrence=line:1
VERDICT_BEARING_CLAIMS=1/2
rc=1
```

`NK1` is `{"meta":{"line":"9"}}` with its span on line 1; the gate names line 9 (from the nested
key) and calls the claim mislocated — exactly the "nested keys read as the record's own" residual
carried in `corpus/lessons/round-31.md:99` and
`corpus/lessons/round-31-verifier-spotcheck.md:233-234`.

Per the assignment I did **not** fix `verify_claims`. I also did **not** add a green case that
would codify the defective behaviour: a case asserting the contract fails today, and a case
asserting `mislocated` would pin a bug as expected output. Item 7 is therefore covered only by its
honoured half (case 235 — a key inside a string value *is* correctly not a field, the promise
stated at `tools/research-gate.sh:1094-1100`), with the violated half left as this finding. When
top-level key parsing lands, add:

```
  cat >"$WORK/claims-r2-nested-object.jsonl" <<'EOF'
{"id":"NK1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","meta":{"line":"9"}}
EOF
  tclaims claims-r2-nested-object 0 'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=NK1 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match'
```

## Limits and risks

- Delivered PASS count is from one full run of the patched gate; two earlier runs failed on my own
  fixture mistakes (case-name vs fixture-name mismatch; the first end-line span was drafted
  against a hand-made copy of `lib/span.md`, not the selftest's real 11-line fixture) and are not
  evidence. Scratch logs: `out/base-selftest.log`, `out/r2-selftest.log`,
  `out/r2-selftest2.log`.
- The block is appended last; if another wave lands cases before it at integration, its case
  numbers shift (names are stable).
- The gate comment at `tools/research-gate.sh:6802` ("cases 216-224") is still wrong (R4, not this
  item) and was left alone.
- No `c1-count.py`/`c2-count.py` run (control rule respected). No lane production file, index, jj
  or git state touched; no commit/push. Artifacts only in this directory and the scratch clone.
- No tool installs or updates were made.
