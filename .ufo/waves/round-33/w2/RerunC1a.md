# RerunC1a — C1 re-run on the landed gate (round 33, wave 2 = FALSIFY)

Seat: `ChousaR33.RerunC1a`. Lane `chousa-shokunin` (tip `0fb300b5c27900ab8bb3abeb5f54776d71e04beb`), no lane
file edited. Evidence-only seat: all code experiments in `/fast/scratch/hyaku/chousa-r33/w2/RerunC1a/`,
artifacts under `.ufo/waves/round-33/w2/RerunC1a/`.

## 0. Objects measured (hashes read before the runs)

| object | sha256 |
|---|---|
| landed gate `tools/research-gate.sh` | `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e` |
| counter `corpus/evidence/round33/c1-count-v2.py` | `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514` |
| base gate (`git show 2b9cc73a:tools/research-gate.sh` → scratch copy) | `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` |

Command (cwd = lane root, `C1_TMP`/`TMPDIR` in scratch, kill rule honoured — receipt on every run, stdout
redirected to a file, never piped):

```
timeout 900 prlimit --nproc=2000 --as=4000000000 python3 corpus/evidence/round33/c1-count-v2.py \
  --gate tools/research-gate.sh --seed <N> --receipt .ufo/waves/round-33/w2/RerunC1a/landed-seed<N>.json \
  > .ufo/waves/round-33/w2/RerunC1a/landed-seed<N>.out 2> .../landed-seed<N>.err
```

## 1. Three fresh-seed runs on the landed gate (all reported, whatever they printed)

Seeds 7701, 7702, 7703 (none in 3301–3373). Each run: **exit 0**, stderr empty, ~3.1 s.

```
TOPLEVEL_FIELD_MATCH=156/156
  N1_nested_line_decoy 12/12
  N2_nested_line_only 12/12
  N3_top_line_wrong_nested_right 12/12
  N4_nested_sha_decoy 12/12
  N5_nested_sha_only 12/12
  N6_top_sha_stale_nested_right 12/12
  N7_nested_source_decoy_sup 6/6
  N8_nested_source_decoy_uns 6/6
  N9_nested_id_decoy 6/6
  N10_nested_span_decoy 6/6
  N11_nested_marker_expect_decoy 6/6
  D1_duplicate_top_level 24/24
  S1_flat_confusers 12/12
  S2_nested_confusers 6/6
  F1_flat_plain 12/12
```

Identical on all three seeds (`landed-seed770{1,2,3}.out`, all sha256
`1eeb8be8062e53154648a1561adc741386d679d7a21ab05ae895e9a4936c31ab`). Receipt fields (all three):

| seed | receipt | gate_sha256 | counter_sha256 | gate_rc | matched/total | `predicate_holds` |
|---|---|---|---|---|---|---|
| 7701 | `.../RerunC1a/landed-seed7701.json` (sha256 `6c92c0ba…4e28`) | `94a7be5a…506e` | `cb354dd1…a514` | 1 (expected: fixture always drifts) | 156/156 | **true** |
| 7702 | `.../RerunC1a/landed-seed7702.json` (sha256 `065996ca…0c5c`) | `94a7be5a…506e` | `cb354dd1…a514` | 1 | 156/156 | **true** |
| 7703 | `.../RerunC1a/landed-seed7703.json` (sha256 `ec2057d8…ec987`) | `94a7be5a…506e` | `cb354dd1…a514` | 1 | 156/156 | **true** |

`misses: []`, `gate_timed_out: false`, per_class all full in each receipt.

**P1 v2 on each run: HOLDS** (156/156, `predicate_holds=true`, receipt carries the landed gate hash and the
v2 counter hash; two-fresh-seed requirement met by three).

## 2. "No lower run" clause — wave-wide receipt scan

Parsed every `*.json` under `.ufo/waves/round-33/` (read-only) whose `gate_sha256` is the landed hash **and**
`counter_sha256` is the v2 counter hash: **29 receipts, every one 156/156** (seeds 3371, 3372, 3401, 3404,
3411, 3412, 3471, 3472, 4101–4105, 4207, 4209, 4401, 6181, 6182, 7701–7703, 884231, 3383101–3383104,
3388101, 3388102, 93330101, 93330102). Minimum = 156. **No lower run** is visible in this round's lane
evidence.

## 3. Attack: C1 contract on inputs the counter does not generate

The counter asserts `json.loads(row)` is a dict for every row and never top-level `marker_default`, never
non-string duplicate values, never a duplicate read key *inside* a nested container, never malformed tokens.
I built those by hand: `probe_build.py` → `claims.jsonl` (27 lines, sha256 `14204fb1…f909`) over a fixture
root with the gate's own `lib/span.md` (4 lines, span `alpha beta gamma delta` on line 1). Landed gate:
`bash tools/research-gate.sh verify-claims claims.jsonl --root root` → **exit 1**, `claims=23 supported=15
invalid=7 mismatched=1` (`landed.out`, sha256 `02e116ae…2c6b`). Base gate on the same file → **exit 1**,
`claims=23 supported=16 invalid=2 mismatched=5` (`base.out`, sha256 `69fa856e…7881`).

Counted items, landed gate:

| contract item | probe (base → landed) | landed output | holds? |
|---|---|---|---|
| 1 — nested member changes nothing | `B1` `{"...","meta":{"line":"9","line":"8"},"line":"1"}`, `B2` array of two nested `line`, `B3` two-level, `B4` nested-only dup `sha256` | all `observed=supported … at=line:1` (base: B1–B3 `mislocated` via nested decoy, B4 `invalid` sha malformed) | **yes** |
| 2 — repeated top-level read field invalid | `A1` `line` twice (`"1"`,`4`), `A2` `span` twice (2nd `null`), `A3` `expect` twice (2nd `["x"]`), `A4` `source` twice (2nd `{}`), `A5` `sha256` twice (2nd `7`) | all `observed=invalid`, ids carried; findings `duplicate top-level key line/span/expect/source/sha256` at lines 5–9 | **yes** |
| 3 — string content never structure | `C1` value `"\"line\": \"9\", \"sha256\": \"00\""`, `C2` value ending `\\`, `C3` `"\u007b\u0022line\u0022:\u00229\u0022\u007d"`, `C4` array holding `"}\"line\": \"9\""` + `{"line":"8"}` before the top-level `line` | all `observed=supported … at=line:1` | **yes** |
| 2 (uncounted keys the contract lists) | `M1` duplicate `marker` (`expect=contradicted`), `M2` duplicate `id` differing | `invalid` / `duplicate top-level key marker`; `invalid` with `CLAIM id=line15` / `duplicate top-level key id` | **yes** |

Independent valid-JSON fuzz (never touching non-JSON): `fuzz.landed.out` — 60 records whose nested values
are random strings over `\ " } ] { [ : ,` (plus `\\`, `\"`, `\\\"`) with nested `line` decoys: **60/60
supported**; 20 records with the same nesting plus a duplicated top-level `line`: **20/20 invalid**, exit 1.
`fuzz2.landed.out` — 350 records (300 shuffled-order nested confusers incl. nested duplicate keys, 50
nested duplicates of `line`/`sha256`/`id`): **350/350 supported**, `RESEARCH_GATE: CLEAN`, exit 0 (the
follow-up `grep -vc` printed 0 and exited 1 only because it selected no lines). No counted-item break found
in 449 valid-JSON records.

## 4. Findings outside the counted predicate (P1 unaffected; reported for the L1)

### F1 — a duplicated top-level read field is silently swallowed on a `marker_default` row

Minimal input line (one JSON object, valid JSON):

```
{"marker_default":"md","line":"1","line":"2"}
```

* landed: **no CLAIM line, no finding**, `RESEARCH_GATE: CLEAN (claims=0 … invalid=0 findings=0)`, **exit 0**
  (`probe3.jsonl` sha256 `a7a33ab6…b4dd`).
* base: byte-identical output, exit 0 (same swallow; inherited, not introduced by C1).

What the gate says vs does: the C1 comment at `tools/research-gate.sh:1608-1609` states *"a marker-default
row has a top-level 'marker_default' string and no top-level 'id' string; a duplicated read field is never
such a row"*, but the guard at `:1610-1611` tests only `json_dup id` and `json_dup marker_default`; the
duplicate loop at `:1622-1624` is therefore unreachable for a row with a top-level `marker_default` string and
no top-level id **string**. Confirmed for duplicated `line`, `span` (probe line 18) and, with a present
non-string id, `{"id":7,"marker_default":"md","line":"1","line":"2"}` (probe line 17) — all swallowed, while
`{"id":"MD1","marker_default":"md","line":"1","line":"2"}` is correctly `invalid` (`probe2.jsonl`).
Contract scope: `claims.md:80` ("Not claimed: `marker_default` rows") excludes these rows, so this is **not** a
P1 break and the counter cannot see it (it never emits top-level `marker_default`). It is a false C1 comment
and a real zero-signal path for a duplicated read field; the `id`-non-string variant is inconsistent with the
normal path, which calls the same record `missing id`/invalid.

### F2 — malformed scalar tokens are accepted; one case also mangles the field read (base → landed verdict change)

Minimal inputs (all rejected by `json.loads` except `NaN`, a Python extension not in RFC 8259):

| id | suffix after the valid fields | landed | base |
|---|---|---|---|
| E1 | `"x":01` | `supported`, `at=line:1` | `supported` |
| E2 | `"x":tru` | `supported` | `supported` |
| E3 | `"x":xyz` | `supported` | `supported` |
| E4 | `"x":+1` | `supported` | `supported` |
| E5 | `"x":.5` | `supported` | `supported` |
| E6 | `"x":1.` | `supported` | `supported` |
| E7 | `"x":NaN` | `supported` | `supported` |
| **E8** | `"x":1"line":"1","line":"9"` | **`mislocated` `line=9-9` + `FINDING CLAIM_LINE_MISMATCH`** | `supported`, `at=line:1` |

Cause: the scalar branch `tools/research-gate.sh:1218-1230` consumes any run up to space/`,`/`}`/`]` without
validating it. On E8 it swallows `1"line":"1"` as the value of `x`, so `json_dup` sees only one top-level
`line` (`"9"`) and the gate **issues a verdict instead of failing closed**. Contract: `claims.md:136-140`
says such lines are *"not claimed … (the candidate is asked to fail closed on them; no fixture class counts
it)"*; the seat's own C1 summary lists "a line that is not one well-formed object is invalid". So E1–E8 meet
neither reading. P1 v2 is unaffected (the counter asserts every row is `json.loads`-valid). E8 is the only
input I found where landed differs from base on a C1 surface and the difference is *not* a contract-fixing
one: base read the first `line`, landed turns a repeated top-level `line` into scalar content and reports a
wrong verdict instead of `invalid`.

### F3 — measured boundary (documented, not a break)

`{"id":"K1",…,"line":"1","l\u0069ne":"9"}` → `supported`, no duplicate (`probe2.jsonl`): escape-spelled keys
are raw-compared, which `claims.md:80-81` excludes ("keys spelled with JSON escapes").

## 5. Verdict

* **P1 v2: HOLDS** on three fresh seeds (7701/7702/7703, all 156/156, `predicate_holds=true`, landed gate
  `94a7be5a…`, counter `cb354dd1…`), and every one of the 29 wave receipts on that gate/counter is 156/156
  — no lower run.
* **C1 counted contract: HOLDS** on every input I generated, including the classes the counter never
  generates in valid JSON: nested duplicates (item 1), non-string repeated read fields (item 2), escaped
  quote/backslash/`\u` string content (item 3), duplicate `marker` and differing `id`.
* **Two uncounted defects** documented (F1 false C1 comment + silent duplicate swallow on marker_default
  rows, inherited from base; F2 malformed-token fail-open, with E8 a base→landed verdict change on an
  invalid line). Neither touches the 156-record predicate; F2 means the "asked to fail closed" sentence in
  `claims.md:139-140` is not met by the landed reader.

## 6. Limits

* Only `verify-claims` was exercised; `verify`, `verify-all`, the selftest and mutants are other seats'.
* The "no lower run" scan covers `.ufo/waves/round-33/` receipts only; a receipt kept solely in scratch
  (outside the lane) would not be seen.
* Probes ran with the default locale and the counter's `CHOUSA_*`-stripped env; gate run cwd inside the
  fixture root, `--root` explicit. No network, no installs this seat.
* F1/F2 line references are the landed gate at `94a7be5a…`; base comparisons are the base-revision file
  `f4731885…` extracted read-only (`git show`), both hashes re-verified before use.

## 7. Artifacts (all under `.ufo/waves/round-33/w2/RerunC1a/`, each < 100 KiB)

`landed-seed770{1,2,3}.json` / `.out` / `.err` (receipts and stdio of the three runs);
`claims.jsonl` `14204fb1…f909`, `landed.out` `02e116ae…2c6b`, `base.out` `69fa856e…7881`,
`probe2.jsonl`, `probe3.jsonl` `a7a33ab6…b4dd`, `probe_build.py`;
`fuzz.landed.out`, `fuzz2.jsonl` `48b6aaeb…6949`, `fuzz2.landed.out` `77a35dc3…7936`, `fuzz_build.py`.
Scratch (not an artifact): `/fast/scratch/hyaku/chousa-r33/w2/RerunC1a/{root,base-gate.sh,probe_key_lines.txt}`.
