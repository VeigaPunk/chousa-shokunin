# Round 33 W1 — CtlC1AllJunk

## Scope and axes

Scored axis: **operability**, frozen C1 only. Probe safeguards: reproducibility and exact scratch restoration. This is a pre-data control report, not a candidate or round-admission judgment.

Read `corpus/evidence/round33/claims.md` first, then the counter docstring. Observed with `timeout 30s sha256sum tools/research-gate.sh corpus/evidence/round33/c1-count.py` (exit 0):

- BASE gate: `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`.
- Frozen counter: `ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229`.

All artifact names below are relative to `.ufo/waves/round-33/w1/CtlC1AllJunk/`. Scratch: `/fast/scratch/hyaku/chousa-r33/w1/CtlC1AllJunk`.

## Mutants and expected detector

Four independent BASE copies received only an early-return insertion immediately after `verify_claims`' `local claims=$1`. The first three decode JSON solely to obtain the top-level id for output association; they bypass all actual source verification. The existing field readers remain untouched.

| Control | Insertion in archived gate | Behavior | Expected detector |
|---|---|---|---|
| all-invalid | `all-invalid.sh:1418-1426` | Emit `observed=invalid` for every record; return 1 | MISSES; only duplicate-invalid truth can match |
| all-supported | `all-supported.sh:1418-1426` | Emit `observed=supported` for every record, no findings; return 0 | MISSES; non-supported truths cannot match |
| random-labels | `random-labels.sh:1418-1429` | Draw from supported/mislocated/stale/unsupported/invalid; no findings; return 1 | MISSES; random correctness is partial, and required mismatch findings are absent |
| no-claims | `no-claims.sh:1418-1419` | Return 1 without reading records or emitting CLAIM lines | MISSES, 0/144 |

The label RNG is independent of the counter seed: Python `random.Random(81332047)`. Its fixed seed makes the junk stream reproducible, while fixture order differs across counter seeds. Matching and missing/duplicate-id rules are frozen at `c1-count.py:34-41,353-379`; the threshold is `:390-412`.

## Commands and receipts

Cwd for every counter invocation: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. The following is the exact parameterized command; full expanded commands, exit codes, stdout and stderr are recorded in `pristine-runs.json`, `mutated-runs.json`, and `restored-runs.json`.

```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin
S=/fast/scratch/hyaku/chousa-r33/w1/CtlC1AllJunk
A="$L/.ufo/waves/round-33/w1/CtlC1AllJunk"
C1_TMP="$S" C2_TMP="$S" TMPDIR="$S" \
  timeout 650s prlimit --as=2147483648 --nproc=2000 \
  python3 "$L/corpus/evidence/round33/c1-count.py" \
  --gate "$S/$control.sh" --seed "$seed" \
  --receipt "$A/$control-$phase-$seed.json"
```

`control` = each of the four names above; `phase` = pristine, mutated, restored; `seed` = **331041 and 331042**. Both seeds were selected for this probe, never 3301–3303, and reused across phases for paired comparisons. Every run generated a new temporary fixture root. Mutated seed-331041 commands additionally used `--keep "$S/$control-fixture-331041"` for the bounded output audit. There were four concurrent foreground subprocesses at most, with all calls awaited.

Receipts: `<control>-<phase>-331041.json` and `<control>-<phase>-331042.json`. All eight mutated receipts were opened and have the frozen counter hash above, the matching mutant hash below, `gate_timed_out=false`, and `predicate_holds=false`. Every counter invocation exited **1**, with empty stderr; this includes all-supported, whose gate itself exited 0.

## Counts and verdicts

Each cell is the actual `TOPLEVEL_FIELD_MATCH` numerator/denominator.

| Control | Pristine seeds 331041 / 331042 | Mutated seeds 331041 / 331042 | Restored seeds 331041 / 331042 | Mutated gate rc | Control verdict |
|---|---|---|---|---|---|
| all-invalid | 60/144 / 60/144 | **12/144 / 12/144** | 60/144 / 60/144 | 1 / 1 | **MISSES** |
| all-supported | 60/144 / 60/144 | **87/144 / 87/144** | 60/144 / 60/144 | 0 / 0 | **MISSES** |
| random-labels | 60/144 / 60/144 | **19/144 / 14/144** | 60/144 / 60/144 | 1 / 1 | **MISSES** |
| no-claims | 60/144 / 60/144 | **0/144 / 0/144** | 60/144 / 60/144 | 1 / 1 | **MISSES** |

No control MEETS-TARGET. No 144/144 bypass was observed. Mutation-kill classification is **INCONCLUSIVE for all four**, not killed: pristine BASE already fails P1 at 60/144. The narrower, directly observed result is that the frozen counter does not accept these four controls.

### Per-class output

Exact stdout lines are retained in `mutated-runs.json`; each mutated receipt also contains `per_class`. “Both” means the lines were identical on both seeds, not averaged.

| Counter class | all-invalid both | all-supported both | random 331041 | random 331042 | no-claims both |
|---|---|---|---|---|---|
| N1_nested_line_decoy | 0/12 | 12/12 | 3/12 | 1/12 | 0/12 |
| N2_nested_line_only | 0/12 | 12/12 | 4/12 | 0/12 | 0/12 |
| N3_top_line_wrong_nested_right | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 |
| N4_nested_sha_decoy | 0/12 | 12/12 | 2/12 | 2/12 | 0/12 |
| N5_nested_sha_only | 0/12 | 12/12 | 1/12 | 1/12 | 0/12 |
| N6_top_sha_stale_nested_right | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 |
| N7_nested_source_decoy_sup | 0/6 | 6/6 | 0/6 | 2/6 | 0/6 |
| N8_nested_source_decoy_uns | 0/6 | 0/6 | 0/6 | 1/6 | 0/6 |
| N9_nested_id_decoy | 0/6 | 6/6 | 1/6 | 1/6 | 0/6 |
| N10_nested_span_decoy | 0/6 | 6/6 | 1/6 | 2/6 | 0/6 |
| N11_nested_marker_expect_decoy | 0/6 | 6/6 | 1/6 | 0/6 | 0/6 |
| D1_duplicate_top_level | 12/12 | 0/12 | 5/12 | 2/12 | 0/12 |
| S1_flat_confusers | 0/12 | 6/12 | 0/12 | 1/12 | 0/12 |
| S2_nested_confusers | 0/6 | 6/6 | 1/6 | 0/6 | 0/6 |
| F1_flat_plain | 0/12 | 3/12 | 0/12 | 1/12 | 0/12 |

### Actual output-shape audit

`raw-gate-runs.json` preserves full stdout, stderr, expanded commands and exit codes for each archived mutant on its kept seed-331041 fixture. Command:

```sh
timeout 60s prlimit --as=2147483648 --nproc=2000 \
  bash "$A/$control.sh" verify-claims \
  "$S/$control-fixture-331041/claims.jsonl" \
  --root "$S/$control-fixture-331041"
```

These foreground commands used the same scratch temp variables and removed CHOUSA_* variables, matching the counter environment. The audit counted output lines by `CLAIM ` / `FINDING ` prefixes and `observed=` tokens:

- all-invalid: exit 1; 144 CLAIM lines, all invalid; 0 FINDING lines.
- all-supported: exit 0; 144 CLAIM lines, all supported; 0 FINDING lines.
- random-labels: exit 1; 144 CLAIM lines: supported 21, mislocated 27, stale 29, unsupported 31, invalid 36; 0 FINDING lines.
- no-claims: exit 1; empty stdout; 0 CLAIM and 0 FINDING lines.

## Hashes and restoration evidence

Before mutation, `timeout 30s sha256sum` reported the BASE hash for `base-gate.sh` and all four scratch controls. Archived mutated gate hashes (also independently carried by both score receipts):

| Archived control | SHA-256 | Bytes |
|---|---|---|
| all-invalid.sh | `29300e9621461c6a6afa0d18ec24ae7b431bafd608bf72d3cdd64508dfd852fb` | 337050 |
| all-supported.sh | `b6a9ec386de3dd900bf32f5a1973088c0a7812e7293eff41662e106a33a83d73` | 337063 |
| random-labels.sh | `f008744810a58813c39543108e69cad9afd22279eb8a3d990237bc573e5af1ba` | 337200 |
| no-claims.sh | `f8215684150b1bb8f585d27312a9f7fe1223b773e0da173918c239f947445a91` | 336765 |

Archive copy/hash/size commands (exit 0) were `timeout 30s cp -t "$A"` with the four explicit scratch control paths, `timeout 30s sha256sum "$A"/*.sh`, and `timeout 30s wc -c "$A"/*.sh`.

Restoration ran in a `finally` block immediately after mutant scoring, including on detector failure. For each control:

```sh
timeout 30s cp "$S/base-gate.sh" "$S/$control.sh"
```

All four copies exited 0. The following `timeout 30s sha256sum` over `base-gate.sh` and the four scratch controls exited 0 and reported **`f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` for every file**. Full commands/output: `restoration.json`. All eight subsequent restored runs again printed 60/144 (`restored-runs.json` and corresponding receipts). Mutated bytes remain only in the archived control artifacts; the four experiment paths are restored exactly.

## Bounds and limits

`timeout 30s df -h /fast` exited 0: 198G available before fixture creation. Final `timeout 30s wc -c "$A"/*` exited 0: every individual artifact was below 1 MiB; the largest was 337200 bytes. Logs and receipts were finite; fixtures contain the counter's fixed 144 records. No tool installs, network, background jobs, process signals, subagents, production-file edits, counter edits, git writes or jj writes were performed. No C1 candidate implementation was scored, and no selftest/no-harm battery was run by this seat. The claims/counter contract was not changed. Results cover these four controls and two seeds only.
