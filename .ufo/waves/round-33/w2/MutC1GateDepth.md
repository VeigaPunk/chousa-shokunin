# MutC1GateDepth — five isolated claim_scan mutation probes

## Scope and verdict

Axes: **operability** (C1 top-level reader), detector sensitivity, exact-byte restoration. These are probe criteria, not new round claims.

**HOLDS on the exercised inputs for the assigned landed bytes; no landed P1 miss found.** Counter + selftest killed **a/c/d** together; **b/e survived both** while violating the documented malformed-record fail-closed behavior. **c also survived selftest alone**, despite violating counted nesting behavior. These are coverage findings, not grounds to change the frozen contract or admit a lane revision.

All results below pin gate SHA-256 `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`, copied before experiments. The live lane changed during the probe; its later hash `165acd5f6cebfb1d0a179f75572315ae6458ae330fdfc1f1ac412c36478a3563` was **not tested** here (restoration note below).

Path abbreviations:
- `A` = `.ufo/waves/round-33/w2/MutC1GateDepth/` relative to the lane root.
- `S` = `/fast/scratch/hyaku/chousa-r33/w2/MutC1GateDepth`.
- `G` = `S/repo/tools/research-gate.sh`.
- `C` = `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count-v2.py`.

Contract: `corpus/evidence/round33/claims.md:29-38,93-140`; v2 governs. Malformed lines are explicitly **outside counted P1**, but the candidate is asked to fail closed (`:136-140`), and the assigned gate promises invalid for anything other than one well-formed object (`A/pristine-gate.sh:47-53,1115-1130`). Counter hash: `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514`.

## Mutants and observed detector outputs

Each mutation was applied alone to `G`, archived as `A/<letter>-mutant-gate.sh`, then reverted before the next mutation. Exact definitions and expected detectors: `A/mutations.json`. Line numbers in this section refer to `A/pristine-gate.sh`.

| Mutant | Smallest behavior change | Expected detector | Counter stdout / exit | Selftest stdout / exit | Verdict |
|---|---|---|---|---|---|
| a | At line 1190, only `{` enters nested-value tracking; array-valued members fall through to the scalar reader | Array variants N1–N11; array-valued line/sha selftests | `TOPLEVEL_FIELD_MATCH=119/156` / 1 | `FAIL (2/248 cases)` / 1 | KILLED by both |
| b | Lines 1208–1212 become unconditional `stk=${stk%?}`; mismatched closer types are accepted | Malformed-bracket rejection; counter generates only valid JSON | `TOPLEVEL_FIELD_MATCH=156/156` / 0 | `PASS (248 cases, 0 skipped)` / 0 | SURVIVED both; fail-closed violation |
| c | At line 1205, nested openers do not push: `'{'|'[') : ;;` | Deep-container variants | `TOPLEVEL_FIELD_MATCH=85/156` / 1 | `PASS (248 cases, 0 skipped)` / 0 | KILLED by counter; SURVIVED selftest |
| d | At line 1138, any nonempty `JSON_SCAN_LINE` hits cache, instead of comparing current line; later records reuse the first tables | Multi-record counter and selftests | `TOPLEVEL_FIELD_MATCH=0/156` / 1 | `FAIL (16/248 cases)` / 1 | KILLED by both |
| e | Both consumed-to-end checks (1156, 1250) replaced by `:` | Trailing-garbage rejection; counter generates only valid JSON | `TOPLEVEL_FIELD_MATCH=156/156` / 0 | `PASS (248 cases, 0 skipped)` / 0 | SURVIVED both; fail-closed violation |

Evidence: each `A/<letter>-mutated.counter.stdout:1-16`, corresponding `.counter.json:5-14`, and `.run.json` records actual argv, exit codes, elapsed times, before/after gate hashes, stdout/stderr paths and hashes. Selftest final lines: `A/a-mutated.selftest.stdout:270`, `A/b-mutated.selftest.stdout:250`, `A/c-mutated.selftest.stdout:250`, `A/d-mutated.selftest.stdout:399`, `A/e-mutated.selftest.stdout:250`. All stderr files are empty; no captured output was truncated.

For a, the existing selftest caught changed diagnostics/record identity in `claims-r2-sha-nonstring` and `claims-r2-line-nonstring` (`A/a-mutated.selftest.stdout:236-260`); the r33 object-only nested cases themselves passed. For d, the gate exited 0, so v2's mandatory gate-exit-1/DRIFT check scored every record none (`A/d-mutated.counter.json:9-14`; counter `:369-394`). The separate two-record witness also demonstrates stale identities: `A/d-mutated.probe-d.stdout` prints `id=D1` twice, where `A/pristine.probe-d.stdout` prints `D1` then `D2`.

### Mutated byte hashes

| Artifact | SHA-256 |
|---|---|
| `A/a-mutant-gate.sh` | `3f8f145f27bc3faac1b33ee82251dc99e17527856d504fcd52b5fb007e7af3c2` |
| `A/b-mutant-gate.sh` | `a29589dcc08800e37aa3a6de926c82d04390e957b77b2a23afaa6e8f41d94c22` |
| `A/c-mutant-gate.sh` | `10ff501b0ba5f193565048f667b73107d26a605dc5b810654a1a3f3452bfed79` |
| `A/d-mutant-gate.sh` | `15dec2302243767913d41a411315af9286ba942c629dce5a149c4d05be05604b` |
| `A/e-mutant-gate.sh` | `409c6f9591d2a0407781707daae49b585856f47cfc99bccbf78db70719cf4cda` |

## Minimal survivor witnesses and base comparison

Source `s` is exactly `alpha beta\n` (`A/source-s`). Inputs are preserved in `A/b.input.jsonl` and `A/e.input.jsonl`.

b — mismatched array/object closer:
```json
{"id":"B","source":"s","span":"alpha beta","expect":"supported","x":[}}
```

e — complete claim object followed by an extra closing brace:
```json
{"id":"E","source":"s","span":"alpha beta","expect":"supported"}}
```

Python JSON validation rejects both; exact errors and all executed commands are in `A/pristine.probes.json`. The gate's outer `{*}` shape guard still admits these shapes, so the removed scanner checks are behavior-bearing, not dead checks.

| Witness | Base `f4731885…` | Assigned landed `94a7be5a…` | Matching mutant | Restored |
|---|---|---|---|---|
| b | supported / CLEAN / exit 0 | invalid / DRIFT / exit 1 | supported / CLEAN / exit 0 | invalid / DRIFT / exit 1 |
| e | supported / CLEAN / exit 0 | invalid / DRIFT / exit 1 | supported / CLEAN / exit 0 | invalid / DRIFT / exit 1 |

Actual key output for b mutant: `CLAIM id=B expected=supported observed=supported source=s at=line:1 verdict=match` (`A/b-mutated.probe-b.stdout:2-4`). For e mutant: `CLAIM id=E expected=supported observed=supported source=s at=line:1 verdict=match` (`A/e-mutated.probe-e.stdout:2-4`). Landed/restored instead print `CLAIM id=line1 expected=- observed=invalid source=- at=- verdict=invalid` plus `CLAIM_RECORD_INVALID` (`A/pristine.probe-b.stdout:2-5`, `A/e-restored.probe-e.stdout:2-5`).

Complete comparison evidence: `A/base.probes.json`, `A/pristine.probes.json`, `A/b-mutated.probes.json`, `A/b-restored.probes.json`, `A/e-mutated.probes.json`, `A/e-restored.probes.json`, and their per-input stdout files. Base gate was extracted read-only with `timeout 30 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 2b9cc73aed30c2e2c95699db6617d9531ef49fb2:tools/research-gate.sh` (exit 0), SHA-256 `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`; archived as `A/base-gate.sh`.

c's selftest-only survival is a counted-contract coverage gap, not merely malformed handling: valid `A/c.input.jsonl` adds `"x":{"y":{}}` to an otherwise supported claim. Landed and restored support it, but c declares it invalid (`A/pristine.probe-c.stdout`, `A/c-mutated.probe-c.stdout`, `A/c-restored.probe-c.stdout`; argv/exits in corresponding `.probes.json`). Counter catches this class; selftest does not. Both b/e violate the broader fail-closed promise but are **not** counterexamples to the deliberately narrower P1 fixture domain (`claims.md:139-140`; counter validates all generated rows at `c1-count-v2.py:331-332`).

## Every counter run, including the setup failure

For every row below, receipt is `A/<phase>.counter.json:5-14`, stdout is `A/<phase>.counter.stdout:1`, and command/exit evidence is `A/<phase>.run.json`. All seven runs on exact landed bytes passed `--receipt`, redirected stdout to an opened regular file before launch, and used unique fresh seeds outside 3301–3373. There was no lower count on the assigned landed hash.

| Phase | Seed | Gate | Count | Counter exit | Selftest exit / final result |
|---|---:|---|---:|---:|---|
| a-before | 3388101 | pristine | 156/156 | 0 | 1 / FAIL 9/248 — initial layout, inconclusive baseline |
| pristine-a-before | 3388102 | pristine | 156/156 | 0 | 0 / PASS 248, 0 skipped |
| a-mutated | 3388103 | a | 119/156 | 1 | 1 / FAIL 2/248 |
| a-restored-b-before | 3388104 | pristine | 156/156 | 0 | 0 / PASS 248, 0 skipped |
| b-mutated | 3388105 | b | 156/156 | 0 | 0 / PASS 248, 0 skipped |
| b-restored-c-before | 3388106 | pristine | 156/156 | 0 | 0 / PASS 248, 0 skipped |
| c-mutated | 3388107 | c | 85/156 | 1 | 0 / PASS 248, 0 skipped |
| c-restored-d-before | 3388108 | pristine | 156/156 | 0 | 0 / PASS 248, 0 skipped |
| d-mutated | 3388109 | d | 0/156 | 1 | 1 / FAIL 16/248 |
| d-restored-e-before | 3388110 | pristine | 156/156 | 0 | 0 / PASS 248, 0 skipped |
| e-mutated | 3388111 | e | 156/156 | 0 | 0 / PASS 248, 0 skipped |
| e-restored | 3388112 | pristine | 156/156 | 0 | 0 / PASS 248, 0 skipped |

Restoration runs also serve as the next mutant's pristine baseline, with unchanged bytes and detector scripts. Fresh seeds change names/order, not enumerated sub-variant counts (`c1-count-v2.py:31-33,82-101`). The first setup had `G=S/tools/research-gate.sh`, putting `TMPDIR=S/tmp` inside the inferred lane root. It produced nine baseline selftest failures (`A/a-before.selftest.stdout:23-61,133-174,279-311`), so **no kill is attributed to that failed baseline**. [INFERENCE] The temporary outside fixtures fell inside lane fallback boundaries. After separating the copied repo into `S/repo/` while retaining `S/tmp` outside it, the measured pristine selftest passed all 248 cases; that corrected layout governed all five mutation comparisons.

## Commands, bounds and restoration

The recorded detector harness is `A/detect.py`; invocations were:
```text
timeout --kill-after=5 895 prlimit --nproc=2000 --as=4000000000 -- python3 S/detect.py <phase> <seed>
```
Actual inner argv (expanded paths are recorded in every `.run.json`):
```text
timeout --kill-after=5 650 prlimit --nproc=2000 --as=4000000000 -- python3 C --gate G --seed <seed> --receipt <absolute A>/<phase>.counter.json
timeout --kill-after=5 240 prlimit --nproc=2000 --as=4000000000 -- bash G --selftest
```
Environment: `C1_TMP=C2_TMP=TMPDIR=S/tmp`; inherited `CHOUSA_*`, `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` removed. Counter stdout was redirected directly to its `.counter.stdout` file; `.run.json` preserves output sizes and digests. Witness runner `A/contract-probe.py` uses `timeout --kill-after=2 15 prlimit --nproc=2000 --as=4000000000 -- bash G verify-claims S/cases/<letter>.jsonl --root S/cases`; outer runner limit 120 seconds. No recursive battery was run.

Each restoration `.run.json` records before/after SHA-256 equal to pristine, counter 156/156 and selftest PASS. Final `timeout 10 cmp -- S/research-gate.sh G` exited **0**, proving exact restoration against the original backup. Both separately hashed to `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`.

A subsequent comparison against the **live lane** exited 1, differing at byte 54728 / line 1120. Its observed hash was `165acd5f6cebfb1d0a179f75572315ae6458ae330fdfc1f1ac412c36478a3563`, with changed scanner tables and validation visible at live `tools/research-gate.sh:1120-1147`. This seat did not overwrite that intervening work or score the new revision. All probe conclusions remain pinned to the assigned original bytes; see `A/restoration.json` for commands, exits and hashes.

`timeout 10 df -h /fast` showed 179G available before fixtures. `timeout 10 wc -c <absolute A>/*` showed the largest then-existing artifact was 350085 bytes; `timeout 10 stat -c '%s %n' <absolute A>/pristine-gate.sh <absolute A>/base-gate.sh` measured the added snapshots as 350090/336677 bytes, respectively. Logs are at most 36236 bytes. No installs/updates, network requests, subagent dispatch, Git/jj writes, production edits or intentional background jobs. Three tool-auto-backgrounded finite invocations (`bg_4229`, `bg_4321`, `bg_4356`) completed before restoration/progression; no job remains outstanding from this probe.

Limits: five specified defects only, one seed per mutant, fresh seeds for every pristine/restored counter run; no independent source, D1–D5 repair, or newer-revision verdict. No production changes, integration, admission decision, or contract amendment was made.
