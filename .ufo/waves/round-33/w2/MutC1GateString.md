# Round 33 W2 — MutC1GateString

## Scope and verdict

Axis: **operability**. Probe axes: detector sensitivity, correct scratch layout, exact-byte restoration. This seat mutation-tested only `claim_scan` string handling; it makes no round-admission decision.

**BROKEN: the pinned gate's advertised fail-closed JSON-validity guarantee.** The invalid JSON escape `\q` is accepted as a supported claim (minimal reproducer below). This is **outside P1 v2's counted input domain**, not a counter kill on the landed revision. **P1 v2 was not falsified:** all 16 counter runs on the exact landed bytes printed `TOPLEVEL_FIELD_MATCH=156/156`, with receipts.

With calibrated pristine/restored controls, mutants **(a) and (c) were KILLED by both the counter and selftest; (b) and (d) SURVIVED both**. Escaped member names are expressly unclaimed, so these survivors establish a detector boundary, not permission to change the contract.

All paths below are relative to `/home/vgpnk/Projects/shokunin/chousa-shokunin` unless absolute. Abbreviations:

- `L=/home/vgpnk/Projects/shokunin/chousa-shokunin`
- `S=/fast/scratch/hyaku/chousa-r33/w2/MutC1GateString`
- `A=.ufo/waves/round-33/w2/MutC1GateString` (absolute `$L/$A` in commands)

## Pins and mutations

The governing design was opened at `corpus/evidence/round33/claims.md:1-140`, including Design v2. Read-only target inspection, exit 0:

```sh
timeout 15 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff 2b9cc73aed30c2e2c95699db6617d9531ef49fb2 0fb300b5c27900ab8bb3abeb5f54776d71e04beb -- tools/research-gate.sh
```

Saved output: `A/target.diff`. The gate was obtained with bounded `git show 0fb300b5c27900ab8bb3abeb5f54776d71e04beb:tools/research-gate.sh`, exit 0, and its SHA-256 checked before copying. Experiments used four isolated `$S/{a,b,c,d}/tools/research-gate.sh` files, never production gate files.

| Label | SHA-256 |
|---|---|
| H0: pristine and every restored gate | `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e` |
| Ha: mutant (a) | `4695fb4c95da880e9cba24576d787a4195d0ab3419033470c1b84d75585dee2d` |
| Hb: mutant (b) | `ef1ae5c82ad133736cc9f6fd978e2c1dcfbbc3f23ef1a46bea16d6868fccd774` |
| Hc: mutant (c) | `49804df0c9f5269ecfbb4727a889d33613483897a3ecc05da3e900b418020321` |
| Hd: mutant (d) | `74d53495ff0f6647b1397bad5918176b8c6ba3fc931f00f8b01ea6f7fce26683` |
| Base gate | `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` |
| Frozen counter v2, every receipt | `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514` |

Mutation definitions, relative to H0 line numbers:

| Mutant | Small behavior-bearing change | Expected detector | Calibrated output and verdict |
|---|---|---|---|
| (a) Escapes ignored in strings | Remove escape consumption at 1167–1168 and 1185–1186; replace nested escape/quote branch at 1197–1200 with quote-only termination. | Counter flat/nested escaped-quote confusers; selftest `claims-r2-nested-string`. | `148/156`, counter exit 1; selftest exit 1, `FAIL (1/248 cases)`: **KILLED**. |
| (b) Values honor escapes, member names do not | Remove only the two member-name escape statements at 1167–1168. | A member name containing an escaped quote would distinguish it; neither frozen detector requires such a case. | `156/156`, counter exit 0; selftest exit 0, `PASS (248 cases, 0 skipped)`: **SURVIVED**. |
| (c) Nested string state ignored | At 1204 change the quote arm from `in_str=1` to `:`; bracket counting consequently includes nested string content. | Counter nested confusers; selftest `r33-top-confuser-nested`. | `152/156`, counter exit 1; selftest exit 1, `FAIL (1/248 cases)`: **KILLED**. |
| (d) Compare keys after unescaping | Insert `key=$(json_unescape "$key")` immediately before the depth-1 table write at 1230. | Escaped read-key spellings would distinguish it; these are expressly outside the frozen claim. | `156/156`, counter exit 0; selftest exit 0, `PASS (248 cases, 0 skipped)`: **SURVIVED**. |

Exact changed bytes and readable diffs: `A/{a,b,c,d}-mutant-gate.sh`, `A/{a,b,c,d}-mutation.diff`; hashes also in `A/mutation-hashes.json`. Mutation (d) is not demonstrated to be a defect within P1; its semantic change is intentionally uncounted.

Counter loss details: (a) `S1_flat_confusers=6/12`, `S2_nested_confusers=4/6`; (c) `S2_nested_confusers=2/6`, with the other classes complete. Evidence: `A/a-cal-mutated-counter.json:15-30`, `A/c-cal-mutated-counter.json:15-30`. Selftest discriminators and actual invalid CLAIM lines: `A/a-cal-mutated-selftest.stdout:242-255`, `A/c-cal-mutated-selftest.stdout:248-255`. Surviving selftests: `A/b-cal-mutated-selftest.stdout:250`, `A/d-cal-mutated-selftest.stdout:250`.

## Bounded detector commands and layout controls

Actual argv, environment, stdout/stderr destinations, recorded child PIDs, exit codes, elapsed times and gate hashes before/after each detector are in `A/<phase>-runs.json`. Harnesses: `A/probe.py` (initial layout) and `A/calibrated-probe.py` (corrected layout). Each invocation ran under:

```sh
timeout 890 prlimit --nproc=2000 --as=4000000000 -- python3 <harness> <phase>
```

Every counter invocation used the following rendered argv and file-descriptor redirection, without a pipe or early stdout consumer:

```sh
timeout --signal=TERM --kill-after=5 750 prlimit --nproc=2000 --as=4000000000 --fsize=1000000 -- python3 "$L/corpus/evidence/round33/c1-count-v2.py" --gate "$S/$m/tools/research-gate.sh" --seed "$seed" --receipt "$L/$A/$run-counter.json" >"$L/$A/$run-counter.stdout" 2>"$L/$A/$run-counter.stderr"
```

Selftest argv:

```sh
timeout --signal=TERM --kill-after=5 600 prlimit --nproc=2000 --as=4000000000 --fsize=20000000 -- bash "$S/$m/tools/research-gate.sh" --selftest >"$S/$run-selftest.stdout" 2>"$S/$run-selftest.stderr"
```

Selftest logs were subsequently copied, without truncation, to `A/$run-selftest.{stdout,stderr}`. `C1_TMP`, `C2_TMP` and `TMPDIR` were set to the experiment's scratch directory; `CHOUSA_*` and Git index/worktree override variables were removed. Counter stdout was written directly to its artifact file, and every run supplied `--receipt`.

**Initial selftests are INCONCLUSIVE, not kills.** Their temp fixtures were inside the copied gate's lane root, and the gate copies initially lacked `PROVINCE.md`. Each pristine selftest failed 10/248 cases before mutation; examples appear at `A/a-pristine-selftest.stdout:23-28,130-134,316`. The initial restored runs reproduced that same 10/248 result. These results are retained, not discarded.

The calibrated triplet moved all temp fixtures to `$S/tmp/$m/<phase>-<detector>`, outside `$S/$m`, and supplied the exact pinned `PROVINCE.md` (`A/fixture-PROVINCE.md`) required by the gate's lane-fallback selftest. This follows the layout constraint in `corpus/QUALITY.md:265-270`. Four fresh pristine selftests then passed all 248 cases; after the identical mutations, only (a)/(c) failed; all four exact-byte restorations again passed all 248. Each calibrated triplet held that layout fixed. Initial and calibrated detector invocations are all disclosed below.

## Complete run ledger — no landed counter run omitted

For each **run** below, the receipt is `A/<run>-counter.json`, stdout is `A/<run>-counter.stdout`, and selftest stdout is `A/<run>-selftest.stdout`; corresponding stderr files are retained. Full combined ledger: `A/all-detector-results.json`, produced by reading the six phase manifests and their receipts. Its SHA-256 is `bfd59187096859a633b7b99a9d9ad430ede9d2f85410b79e86af4377c7b46025`.

Counter column abbreviates the printed `TOPLEVEL_FIELD_MATCH=` prefix. Selftest abbreviations reproduce these terminal lines: P248 = `RESEARCH_GATE_SELFTEST: PASS (248 cases, 0 skipped)`; F10/F11/F1 = `RESEARCH_GATE_SELFTEST: FAIL (10/248 cases)` / `(11/248 cases)` / `(1/248 cases)`.

| Run | Seed | Gate | Counter exit / output | Selftest exit / output |
|---|---:|---|---|---|
| a-pristine | 3383101 | H0 | 0 / 156/156 | 1 / F10 |
| b-pristine | 3383102 | H0 | 0 / 156/156 | 1 / F10 |
| c-pristine | 3383103 | H0 | 0 / 156/156 | 1 / F10 |
| d-pristine | 3383104 | H0 | 0 / 156/156 | 1 / F10 |
| a-mutated | 3383201 | Ha | 1 / 148/156 | 1 / F11 |
| b-mutated | 3383202 | Hb | 0 / 156/156 | 1 / F10 |
| c-mutated | 3383203 | Hc | 1 / 152/156 | 1 / F11 |
| d-mutated | 3383204 | Hd | 0 / 156/156 | 1 / F10 |
| a-restored | 3383301 | H0 | 0 / 156/156 | 1 / F10 |
| b-restored | 3383302 | H0 | 0 / 156/156 | 1 / F10 |
| c-restored | 3383303 | H0 | 0 / 156/156 | 1 / F10 |
| d-restored | 3383304 | H0 | 0 / 156/156 | 1 / F10 |
| a-cal-pristine | 3383401 | H0 | 0 / 156/156 | 0 / P248 |
| b-cal-pristine | 3383402 | H0 | 0 / 156/156 | 0 / P248 |
| c-cal-pristine | 3383403 | H0 | 0 / 156/156 | 0 / P248 |
| d-cal-pristine | 3383404 | H0 | 0 / 156/156 | 0 / P248 |
| a-cal-mutated | 3383501 | Ha | 1 / 148/156 | 1 / F1 |
| b-cal-mutated | 3383502 | Hb | 0 / 156/156 | 0 / P248 |
| c-cal-mutated | 3383503 | Hc | 1 / 152/156 | 1 / F1 |
| d-cal-mutated | 3383504 | Hd | 0 / 156/156 | 0 / P248 |
| a-cal-restored | 3383601 | H0 | 0 / 156/156 | 0 / P248 |
| b-cal-restored | 3383602 | H0 | 0 / 156/156 | 0 / P248 |
| c-cal-restored | 3383603 | H0 | 0 / 156/156 | 0 / P248 |
| d-cal-restored | 3383604 | H0 | 0 / 156/156 | 0 / P248 |

All 24 counter receipts report gate exit 1, no timeout; counter exit is separately shown above. All seeds are outside 3301–3373. All 16 runs carrying H0 matched 156/156; mutant misses are not landed-revision kill-rule misses.

## Uncounted fail-closed defect: minimal string escape

Input `A/minimal-invalid.jsonl:1`, with local source `s` containing `a\n` (`A/s`):

```json
{"id":"C","source":"s","span":"a","expect":"supported","x":"\q"}
```

Python's JSON decoder rejects this exact line: `Invalid \escape: line 1 column 61 (char 60)` (`A/minimal-input-validity.json`). The valid control is the same four required members with `x` omitted (`A/minimal-valid.jsonl`). Both the invalid record and the valid control were run against the base and pristine landed gates.

Rendered command for each gate/input pair, all exit **0**:

```sh
timeout 30 prlimit --nproc=2000 --as=4000000000 --fsize=1000000 -- bash <base-or-pristine-gate> verify-claims "$S/edge/minimal-<invalid-or-valid>.jsonl" --root "$S/edge" >"$L/$A/minimal-<base-or-landed>-<invalid-or-valid>.stdout" 2>"$L/$A/minimal-<base-or-landed>-<invalid-or-valid>.stderr"
```

Exact commands, gate hashes and exits: `A/minimal-runs.json`. Both base and landed print:

```text
CLAIM id=C expected=supported observed=supported source=s at=line:1 verdict=match
VERDICT_BEARING_CLAIMS=1/1
RESEARCH_GATE: CLEAN (claims=1 supported=1 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
```

Evidence: `A/minimal-base-invalid.stdout:2-4` and `A/minimal-landed-invalid.stdout:2-4`. This is pre-existing acceptance, not a newly introduced regression.

The advertised contract says a line that is not one well-formed JSON object is invalid (`tools/research-gate.sh` at pinned tip, lines 50–53 and 365–367). Design v2 explicitly asks malformed lines to fail closed while excluding them from P1 (`corpus/evidence/round33/claims.md:139-140`). The knowledge entry likewise says malformed lines are refused (`corpus/knowledge/claim-record-fields-r33.md:27-30,65-67`). This reproducer contradicts those broader assertions, without falsifying the counted predicate. The frozen counter only generates valid JSON (`c1-count-v2.py:331-332`).

The scanner consumes the character after a backslash without validating the escape alphabet (`A/pristine-gate.sh:1183-1188`). A second uncounted example, an unknown nested value `"meta":{"k":}`, is also accepted as supported by both base and landed (`A/edge-claims.jsonl:6`, `A/base-edge.stdout:7`, `A/pristine-edge.stdout:7`); JSON rejection evidence is in `A/edge-runs.json`.

## Survivor behavior was real, not equivalent bytes

Supplemental six-record fixture: `A/edge-claims.jsonl`, source `A/edge-source.md`. Actual bounded commands and exits are in `A/edge-runs.json`; the command shape was `timeout 30 prlimit --nproc=2000 --as=4000000000 --fsize=1000000 -- bash <gate> verify-claims "$S/edge/claims.jsonl" --root "$S/edge"`, with stdout/stderr redirected to `A/<gate-label>-edge.*`.

- **(b):** line 1 uses an unknown member name containing an escaped quote, `"n\"o":0`. Pristine prints `CLAIM id=KEY ... observed=supported`; (b) instead prints `CLAIM id=line1 ... observed=invalid` (`A/b-edge.stdout:2`). The values' escaped quote still works (`A/b-edge.stdout:4`).
- **(d):** line 4 has `"l\u0069ne":"9"`, no literal `line` member, and the actual span on source line 1. Pristine prints supported; (d) prints `observed=mislocated` plus `CLAIM_LINE_MISMATCH` (`A/d-edge.stdout:5,8`).
- Pristine/base supplemental runs exit 0; all four mutant supplemental runs exit 1, for the differing records recorded in `A/edge-runs.json`. After exact restoration all four supplemental runs exit 0 with the original six supported CLAIM lines (`A/restored-edge-runs.json`; e.g. `A/restored-b-edge.stdout:2-9`).

These supplemental differences do **not** turn (b)/(d) into kills by the frozen counter or selftest. Escaped keys are excluded at `claims.md:80-82` and `claim-record-fields-r33.md:52-53,65-67`.

## Restoration, limits and handoff

Both mutation cycles restored each scratch gate with the saved exact pristine bytes, even though detectors failed. `A/initial-restoration.json` and `A/final-restoration.json` record mutant-before SHA-256, restored-after H0 and `exact_bytes_equal=true` for every copy. Final restoration evidence SHA-256: `fdca075b6391c3d12f3f06402e250e918acf322a8a6705fc41cfaf7aff7d4325`. The calibrated restored counter receipts independently record H0; restored selftests all pass 248/248.

Artifact-integrity evidence: `A/artifact-integrity.json` records sizes and SHA-256 for the 189 preceding artifacts; largest file 350122 bytes, all below 1 MiB. Gate fixture/log writes were file-size bounded; all detector children were waited to recorded exits, with no detached jobs or process-name signaling. Initial disk check `timeout 10 df -h /fast`, exit 0, showed 179G available.

No tools were installed, no network was accessed, no subagents or other agent runtimes were invoked, and no production source, lane Git index or jj state was edited. S062/S063 registry rows and the local knowledge/QUALITY text were read; their external pages were not opened. D1/D2/D3/D5 repair behavior was not independently scored by this string-handling seat. No counter, contract or production repair was changed. The actionable handoff is the uncounted invalid-escape acceptance and the two explicitly scoped survivors, not a proposal to silently expand P1.
