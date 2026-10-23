# ProbeMalformed33 — fail-closed claim-record parsing (round 33, wave 2)

Seat: `ChousaR33.ProbeMalformed33`. Attacked surface: `claim_scan` and the
`verify_claims` fail-closed arm of `tools/research-gate.sh`.

Pins opened/verified this run:

| object | path | sha256 |
|---|---|---|
| landed gate | `tools/research-gate.sh` | `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e` |
| base gate | `git show 2b9cc73…:tools/research-gate.sh` → scratch `base-gate.sh` | `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` |
| counter v2 | `corpus/evidence/round33/c1-count-v2.py` | `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514` |
| feasibility oracle (L1) | `.ufo/waves/round-33/controls/L1-design/oracle-gate.sh` | `930a20755418eed3277a893c5b8a96bffd93f2ea90a79fd79bc122426e5677a9` |

Reference semantics for "is this line one well-formed JSON object": `python3
json.loads` (strict, the default). Contract text attacked: `corpus/evidence/round33/claims.md`
(design v2, contract items 1–4 + the "Not claimed" paragraph) and
`corpus/knowledge/claim-record-fields-r33.md:28-31,66-67`.

## What I ran

All fixture roots, fixtures and outputs are in
`.ufo/waves/round-33/w2/ProbeMalformed33/`; drivers were run from
`/fast/scratch/hyaku/chousa-r33/w2/ProbeMalformed33/` with `TMPDIR`/`C1_TMP` set there.
Every gate invocation was `bash <gate> verify-claims <root>/claims.jsonl --root <root>`
with `CHOUSA_STRICT=0` and `CHOUSA_CLAIMS/RECORD/ROOT` unset.

| # | command (cwd = scratch dir unless noted) | exit | artifact |
|---|---|---|---|
| 1 | `timeout 900 python3 probe.py` (34 lines, the eight named families) | 0 (driver); landed gate rc=1, base rc=1 | `landed.out`, `base.out`, `oracle-fx.out`, `fixtures/fx-claims.jsonl` |
| 2 | `timeout 900 python3 nested.py` (20 lines, malformed inside nested values / scalars) | 0; landed rc=1, oracle rc=1 | `nested-landed.out`, `nested-oracle.out`, `nested-matrix.txt`, `fixtures/fn-claims.jsonl` |
| 3 | `timeout 900 python3 escape.py` (12 valid-JSON lines, `\u` decoding) | 0; landed rc=1, base rc=1 | `escape-landed.out`, `escape-base.out`, `fixtures/fe-claims.jsonl` |
| 4 | `timeout 900 python3 keychar.py` (24 valid-JSON lines, exotic member names) | 0; landed rc=1, base rc=0 | `keychar-landed.out`, `keychar-base.out`, `fixtures/fk-claims.jsonl` |
| 5 | `timeout 900 python3 corpus/evidence/round33/c1-count-v2.py --seed 3471 --receipt …/c1-3471.json > c1-3471.log 2>&1` (cwd = lane root) | 0 | `c1-3471.json` (`aea57443…`), `TOPLEVEL_FIELD_MATCH=156/156`, `predicate_holds=true` |
| 6 | same, `--seed 3472` → `c1-3472.json` | 0 | `54f84880…`, `156/156`, `predicate_holds=true` |
| 7 | same, `--seed 3473 --gate <scratch>/base-gate.sh` → `c1-base-3473.json` | 1 | `9ca73b9a…`, `TOPLEVEL_FIELD_MATCH=60/156` |

Seeds 3471–3473 are outside 3301–3373 and outside the L1's 3351/3352/3371/3372. Both landed-gate
counter runs carried `--receipt` and redirected stdout to a file (kill rule). No lane file was
written; no jj/git write command was issued.

## Matrix 1 — the eight named families (34 lines, `fixtures/fx-claims.jsonl`, sha `2b48dc62…`)

`py` = `json.loads` accepts the line. `land`/`base` = `observed=` on the landed/base gate.

| case | minimal line (P = `"source":"src.txt","span":"alpha","expect":"supported"`) | py | base | landed |
|---|---|---|---|---|
| valid baseline | `{"id":"m01",P}` | ok | supported | **supported** ✓ |
| unterminated string, tail | `{"id":"m02",P,"note":"oops}` | no | supported | **invalid** ✓ |
| escaped quote ends id early | `{"id":"m03\",P}x}` | no | supported | **invalid** ✓ |
| unterminated, escaped `}` | `{"id":"m04",P,"n":"tail\}` | no | supported | **invalid** ✓ |
| unterminated in nested value | `{"id":"m05",P,"meta":{"a":"b}}` | no | supported | **invalid** ✓ |
| mismatched brackets nested | `{"id":"m06",P,"meta":{"a":[1}],"b":2}` | no | supported | **invalid** ✓ |
| extra close | `{"id":"m07",P,"meta":{"a":1}}}` | no | supported | **invalid** ✓ |
| missing close | `{"id":"m08",P,"meta":{"a":1}` | no | supported | **invalid** ✓ |
| missing array close | `{"id":"m09",P,"meta":[1,2}` | no | supported | **invalid** ✓ |
| bytes after `}` (brace tail) | `{"id":"m10",P}x}` | no | supported | **invalid** ✓ |
| bytes after `}` (word tail) | `{"id":"m11",P}junk` | no | supported | **invalid** ✓ (`not a JSON object`) |
| two objects, tight | `{"id":"m12",P}{"id":"other"}` | no | supported | **invalid** ✓ |
| two objects, spaced | `{"id":"m13",P} {"id":"other",P}` | no | supported | **invalid** ✓ |
| bare word as read field | `{"id":m15,P}` | no | invalid | **invalid** ✓ (`missing id`) |
| trailing comma, top level | `{"id":"m19",P,}` | no | supported | **invalid** ✓ |
| empty member name | `{"":"x","id":"m23",P}` | ok | supported | **supported** ✓ |
| NUL byte in unread string | `{"id":"m24",P,"note":"a\0b"}` | no | supported | supported ✗ |
| NUL byte in span | `{"id":"m25",…,"span":"al\0pha",…}` | no | supported | supported ✗ |
| NUL byte in id | `{"id":"m2\06",P}` | no | supported | supported ✗ |
| raw TAB in unread string | `{"id":"m27",P,"note":"a<TAB>b"}` | no | supported | supported ✗ |
| raw 0x01 in id | `{"id":"m2\x018",P}` | no | supported | supported ✗ |
| raw 0x01 as member name | `{"id":"m29",P,"\x01":1}` | no | supported | supported ✗ |
| bare word, unread member | `{"id":"m16",P,"note":foo}` | no | supported | supported ✗ |
| lone `-` value | `{"id":"m17",P,"n":-}` | no | supported | supported ✗ |
| `01` value | `{"id":"m18",P,"n":01}` | no | supported | supported ✗ |
| nested `[1,2,]` | `{"id":"m20",P,"meta":[1,2,]}` | no | supported | supported ✗ |
| nested bare key | `{"id":"m21",P,"meta":{a:1}}` | no | supported | supported ✗ |
| nested empty value | `{"id":"m22",P,"meta":{"a":}}` | no | supported | supported ✗ |
| nested `"line":"9"` decoy (control) | `{"id":"m31","meta":{"line":"9","sha256":"x"},P}` | ok | **invalid** | **supported** ✓ (base still had D4) |
| brackets inside a string (control) | `{"id":"m32",P,"meta":{"a":"}]"},"b":2}` | ok | supported | supported ✓ |
| trailing escaped backslash (control) | `{"id":"m33",P,"n":"a\\"}` | ok | supported | supported ✓ |
| escaped quote then `}` (control) | `{"id":"m34",P,"n":"a\"b"}` | ok | supported | supported ✓ |
| `:`/`,`/`}` inside a string (control) | `{"id":"m35",P,"n":"a:b,c}"}` | ok | supported | supported ✓ |
| raw DEL 0x7f in a string | `{"id":"m30",P,"note":"a\x7fb"}` | ok | supported | supported ✓ |

Landed summary line: `RESEARCH_GATE: DRIFT (claims=34 supported=20 … invalid=14 findings=14 drift=14)`.

## Matrix 2 — malformed syntax inside nested values and scalars (20 lines, `fixtures/fn-claims.jsonl`)

Every line is `{"id":"nNN",P,<extra>}` (`py=inv` means `json.loads` raises):

| extra member | py | base | landed | oracle |
|---|---|---|---|---|
| `"meta":[1,,2]` | inv | supported | supported ✗ | invalid |
| `"meta":{,}` | inv | supported | supported ✗ | invalid |
| `"meta":{"a"}` | inv | supported | supported ✗ | invalid |
| `"meta":"\z"` | inv | supported | supported ✗ | invalid |
| `"meta":"\u12"` | inv | supported | supported ✗ | invalid |
| `"meta":True` | inv | supported | supported ✗ | invalid |
| `"meta":+1` | inv | supported | supported ✗ | invalid |
| `"meta":.5` | inv | supported | supported ✗ | invalid |
| `"meta":1e` | inv | supported | supported ✗ | invalid |
| `"meta":0x10` | inv | supported | supported ✗ | invalid |
| `"meta":{"a":1,}` | inv | supported | supported ✗ | invalid |
| `"x"::"y"` | inv | supported | supported ✗ | invalid |
| `"meta":'a'` | inv | supported | supported ✗ | invalid |
| `"meta":{"a":1,,"b":2}` | inv | supported | supported ✗ | invalid |
| `"meta":[{"a":1},]` | inv | supported | supported ✗ | invalid |
| `"meta":1.` | inv | supported | supported ✗ | invalid |
| `"meta":tru` | inv | supported | supported ✗ | invalid |
| `"meta":NaN` | ok (Python extension) | supported | supported | supported |
| `"meta":-}` | inv | supported | **invalid** ✓ | invalid |
| `"meta":{"a":1}}` | inv | supported | **invalid** ✓ | invalid |

`nested-landed.out`: 18 `observed=supported`, 2 `observed=invalid`.

## Matrix 3 — escape decoding on fully valid JSON (12 lines, `fixtures/fe-claims.jsonl`)

| line | true decoded span | landed | base | oracle |
|---|---|---|---|---|
| `"span":"al\u0000pha"` | `'al\x00pha'` | **observed=supported at=line:1 verdict=match** | same | same |
| `"span":"al\u0000pha"`, `expect=unsupported` | `'al\x00pha'` | observed=supported (mismatch) | same | same |
| `"span":"alpha\u0000"` | `'alpha\x00'` | **observed=supported verdict=match** | same | same |
| `"span":"alpha\u0000 beta"` | `'alpha\x00 beta'` | **observed=supported verdict=match** | same | same |
| `"expect":"supp\u0000orted"` | — | observed=supported | same | same |
| `"line":"\u00002"` | — | observed=mislocated | same | same |
| `"source":"src\u0000.txt"` | — | observed=supported (file resolved) | same | same |
| `"id":"u\u00008"` | — | prints `CLAIM id=u8` | same | same |
| `"sha256":"00…00\u0000"` | — | **observed=invalid** (r31 guard) | invalid | invalid |
| `"span":"\u00e9"` | `'é'` | unsupported | unsupported | unsupported |
| `"span":"\ud800"` | lone surrogate | unsupported | unsupported | **invalid** |
| `"span":"\u0061lpha"` | `'alpha'` | supported | supported | supported |

## Findings

**F1 — the counted predicate holds.** `156/156` on two fresh seeds (3471, 3472) against the landed
gate, `predicate_holds=true` in both receipts; base is `60/156` (seed 3473). Every malformed class
in the ticket that is *structural at the top level* fails closed: unterminated strings (3 variants) and an escaped quote that ends the id string early,
mismatched/extra/missing brackets (4), bytes after the closing brace (2), two objects on one line
(2), trailing comma at top level, bare word as a read field, and a member name that is not a string
(`{"id":m15,…}`). The base gate reported `observed=supported` for 13 of those; the landed gate does
not. No regression in any of the 90 fixture lines I ran (34+20+12+24).

**F2 — the "asked to fail closed" property does not hold for anything below the top level.**
29 distinct minimal inputs — 12 from Matrix 1 (6 generic-validity and 6 NUL/control-byte lines) plus
17 from Matrix 2 — are `observed=supported` on the landed gate while `json.loads` rejects the line.
Root causes are visible
in the code: the nested skipper (`tools/research-gate.sh:1191-1216`) validates only bracket type and
string state — never commas, member syntax or escapes — and the scalar arm (`:1217-1226`) accepts any
nonempty run of bytes up to a delimiter (`tru`, `True`, `+1`, `.5`, `1e`, `0x10`, `01`, `-`).
The lane's own feasibility oracle — the same gate with `json_str`/`json_has_key` answered by
`python3 json.loads` — rejects 26 of these 29 (the 3 NUL lines are invisible to it too, see F3), so
the landed reader is strictly weaker than the reference the design used to claim feasibility.
`corpus/evidence/round33/claims.md` (v2, "Not claimed") does concede that no fixture class counts
these lines — so they do not falsify P1 — but the same sentence says "the candidate is asked to fail
closed on them", and it does not. `corpus/knowledge/claim-record-fields-r33.md:66-67` is therefore
overbroad: "malformed lines (the reader refuses them…)" is true only for the classes enumerated at
`:28-31`, not for nested values, scalars, control bytes or NUL.

**F3 — a NUL byte cannot be refused at all in the current architecture.** `verify_claims` reads
records with `while IFS= read -r line` (`tools/research-gate.sh:1587`); bash cannot hold NUL, so the
byte is deleted before `claim_scan` runs. Measured: `printf 'A\0B\n' | read` yields the 2-byte
string `AB`. Consequence: `{"id":"m25","source":"src.txt","span":"al\0pha","expect":"supported"}`
(one raw 0x00 inside the span) is verified as span `alpha` → `observed=supported at=line:1
verdict=match`, and the python oracle says the same, because it never sees the byte either. Fail-closed
on NUL is unreachable without a pre-read byte check (e.g. `grep -c $'\0'` or a byte-count comparison
per line). Raw control characters (TAB, 0x01) *are* reachable — `read` keeps them — and are also
accepted; `json.loads` rejects them, the oracle rejects them.

**F4 — on a fully valid JSON line, `\u0000` in a read value is decoded away and fabricates
`supported` (pre-existing, unchanged by C1).**
`{"id":"u1","source":"src.txt","span":"al\u0000pha","expect":"supported"}` is valid JSON whose span
value is `al\x00pha`; that byte string does not occur in `src.txt`. Landed output:
`CLAIM id=u1 expected=supported observed=supported source=src.txt at=line:1 verdict=match`.
`json_unescape` (`:1280-1328`) maps `\u0000` through `printf -v c '%b' '\000'`, and bash drops the
NUL, so the searched span is `alpha`. Same for `alpha\u0000`, `alpha\u0000 beta`, `source`, `expect`
and `id` (`CLAIM id=u\u00008` prints `id=u8`). The lane already treats exactly this hazard as
malformed for `sha256` (`:1666-1672`, "treat an escaped NUL (bash drops NULs) as malformed"), but
for no other read field. This is the one finding that sits inside C1's stated surface rather than
the "Not claimed" carve-out: the line *is* valid JSON, the `span` is a plain top-level string, and
C1 contract item 3 says characters inside JSON string values are content. Base and the oracle behave
identically, so it is not a regression introduced by round 33 — it is a hole the v2 fixture matrix
never generates (it has `string confusers` for `{ } [ ] : ,`, not for `\u` escapes) and that would
inflate the after-state if a future class used it.

**F5 — exotic member names are safe (contract item 1 holds).** 24 valid-JSON lines with member names
containing `] [ * ? $ \` ! @ # ( ) | & ; < > space = -n -e %s%d { }` all stayed
`observed=supported` on the landed gate; the two deliberately malformed ones (`"x""`, `"\` as a
name) were `invalid`. No associative-subscript or glob breakage at bash 5.3.20.

## Verdict

- **P1 v2 / the counted C1 predicate: HOLDS.** 156/156 on seeds 3471 and 3472, receipts
  `c1-3471.json` / `c1-3472.json`, no lower run.
- **The eight named families, structurally: HOLDS** — every top-level structural malformation I
  built is `CLAIM id=line<N> observed=invalid`, and the landed gate is strictly stronger than base
  (13 base fail-opens closed; 0 regressions in 90 lines).
- **The design's own fail-closed sentence and the knowledge row: BROKEN** on 23 observed=supported
  malformed inputs (F2) plus an architectural NUL blind spot (F3). Not falsifying for P1 because
  v2 explicitly counts none of them; falsifying for any claim that "the reader refuses lines that
  are not one well-formed JSON object".
- **New, contract-adjacent, uncounted: F4** — `\u0000` in a read value deletes characters and can
  turn an absent span into `observed=supported … verdict=match`, on valid JSON. Minimal input
  above; base and oracle identical; `sha256` already guarded.

If the L1 wants a single-line C1 amendment it would be: "a decoded NUL (`\u0000`) in any read field
makes the record invalid, exactly as for `sha256`" — extending `:1666-1672` to `span`, `id`,
`source`, `expect`, `line`. That is a repair, not a claim, and needs no counter change.

## Limits

- Python `json.loads` (strict) is my reference for well-formedness; the contract does not name a
  parser. `NaN`/`Infinity` are therefore scored "python-valid" though they are not RFC 8259 JSON.
- One environment: bash 5.3.20, LC_ALL=C inside `claim_scan`. Multi-byte UTF-8 inside strings was
  exercised only incidentally (`\u00e9`); invalid UTF-8 bytes were not tested.
- Not measured here (other seats): long lines / quadratic cost, duplicate-read-key variants,
  `marker_default` rows, source refusal paths, `verify-all`/`gate_drift_scan`.
- The oracle is an L1-built artifact, not independently audited; I only ran it.
- No network. No source row was opened; the RFC/Python rows were not re-read.
- No lane file, jj state or Git index was touched; artifacts are bounded (108 KiB total).
