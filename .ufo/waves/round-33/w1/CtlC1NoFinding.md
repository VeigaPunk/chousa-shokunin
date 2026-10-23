# Round 33 W1 — CtlC1NoFinding

## Scope and result

Axis: **operability**. This probe challenges the frozen C1 detector's finding-set requirements and duplicate-CLAIM rejection, not a candidate implementation. All four defective controls **MISSES / KILLED** on both assigned fresh seeds. No tested defective control reached 144/144; no counter gap was found in these four probes. This is not a verdict on a landed C1 implementation.

Read `corpus/evidence/round33/claims.md` first, then `c1-count.py`'s docstring. The expected detector is the unchanged counter's rule: exactly one correctly observed CLAIM per top-level id, line-mismatch finding iff mislocated, revision-mismatch finding iff stale (`c1-count.py:34-41,353-378`).

All paths below are relative to the lane unless explicitly absolute. Artifact directory **A** = `.ufo/waves/round-33/w1/CtlC1NoFinding/`. Scratch **S** = `/fast/scratch/hyaku/chousa-r33/w1/CtlC1NoFinding/`.

## Provenance and construction

Observed SHA-256 values, command `timeout 20s sha256sum <base> <oracle> <counter>`, exit 0:

- BASE `tools/research-gate.sh`: `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`.
- Frozen L1 feasibility oracle `.ufo/waves/round-33/controls/L1-design/oracle-gate.sh`: **O** = `930a20755418eed3277a893c5b8a96bffd93f2ea90a79fd79bc122426e5677a9`.
- Frozen counter `corpus/evidence/round33/c1-count.py`: `ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229`.

Copied the oracle into `S/oracle-pristine.sh` first, and BASE into `S/base-pristine.sh` and all four control paths. Applied the exact existing oracle bytes to those BASE copies before introducing each single finding/output defect. `timeout 20s diff -u S/base-pristine.sh S/oracle-pristine.sh` exited 1 (differences expected): only the `json_str`/`json_has_key` reader block, oracle duplicate-read-key helper, and duplicate-key invalidation branch differed. No new candidate reader was built or scored.

Before mutation, each control path had hash O and scored 144/144 on its two seeds. Mutated gates were copied to A before scoring; scratch paths were subsequently restored, while the archived A copies deliberately retain the mutant bytes. All six archived shell files are 336,677–337,134 bytes. `timeout 20s stat -c '%n %s bytes' A/*.sh` and `timeout 20s sha256sum A/*.sh` exited 0.

## Mutants and expected detector

| Control | Small behavior-bearing mutation, archived location | Expected failure |
|---|---|---|
| a `a-no-line.sh` | Suppress only the line-mismatch `emit_finding` at `A/a-no-line.sh:1607`; leave `observed=mislocated` intact. | Mislocated records fail finding-set equality. |
| b `b-no-revision.sh` | Suppress only the revision-mismatch `emit_finding` at `A/b-no-revision.sh:1553`; leave `observed=stale` intact. | Stale records fail finding-set equality. |
| c `c-both-everywhere.sh` | At CLAIM output, emit both mismatch findings for every id, including invalid records (`A/c-both-everywhere.sh:1649-1654`). | Every record has at least one forbidden finding. |
| d `d-duplicate-claim.sh` | Print every CLAIM output record twice (`A/d-duplicate-claim.sh:1649`); retain original observations and findings. | Repeated ids become `observed=none`, per `c1-count.py:363-368`. |

Control d exercises duplicated output records, not duplicate-key parsing: each id gets two CLAIM lines.

## Commands and actual outputs

Every detector command used lane cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin` and this exact parameterized form:

```sh
timeout --kill-after=10s 850s prlimit --nproc=2000 --as=2147483648 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r33/w1/CtlC1NoFinding C2_TMP=/fast/scratch/hyaku/chousa-r33/w1/CtlC1NoFinding TMPDIR=/fast/scratch/hyaku/chousa-r33/w1/CtlC1NoFinding python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py --gate /fast/scratch/hyaku/chousa-r33/w1/CtlC1NoFinding/CONTROL.sh --seed SEED --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/CtlC1NoFinding/PHASE-CONTROL-SEED.json
```

`PHASE` was `pristine`, `mutated`, then `restored`. `A/probe-evidence.json` records all **24 expanded commands**, cwd, actual stdout/stderr, exit codes, elapsed times, receipt paths, before/after hashes, and restoration commands. Its SHA-256 is `accf8bc60f3aba8dc673c6d180b64cddf5c60ac42de5ddb7d9e63b60c0ddb361` (41,061 bytes). Detectors ran in joined foreground batches with at most four concurrent calls; each subprocess also had an 875-second parent deadline.

Counts below occurred on **each** seed listed. All detector stderr was empty. Detector exit status was 0 for pristine/restored and 1 for mutated. The underlying gate exit status was 1; no reported gate timeout occurred.

| Control | Fresh seeds | Pristine | Mutated key output | Restored | Verdict |
|---|---|---|---|---|---|
| a | 3374101, 3374102 | 144/144 | `TOPLEVEL_FIELD_MATCH=123/144` | 144/144 | MISSES / KILLED |
| b | 3374201, 3374202 | 144/144 | `TOPLEVEL_FIELD_MATCH=129/144` | 144/144 | MISSES / KILLED |
| c | 3374301, 3374302 | 144/144 | `TOPLEVEL_FIELD_MATCH=0/144` | 144/144 | MISSES / KILLED |
| d | 3374401, 3374402 | 144/144 | `TOPLEVEL_FIELD_MATCH=0/144` | 144/144 | MISSES / KILLED |

### Per-class output

These ratios are identical across each control's two seeds. Pristine/restored columns describe all sixteen passing runs. The original per-class stdout lines for every run are retained in `A/probe-evidence.json`; each receipt also records `per_class`.

| Counter class | Pristine / restored | a | b | c | d |
|---|---:|---:|---:|---:|---:|
| N1_nested_line_decoy | 12/12 | 12/12 | 12/12 | 0/12 | 0/12 |
| N2_nested_line_only | 12/12 | 12/12 | 12/12 | 0/12 | 0/12 |
| N3_top_line_wrong_nested_right | 12/12 | 0/12 | 12/12 | 0/12 | 0/12 |
| N4_nested_sha_decoy | 12/12 | 12/12 | 12/12 | 0/12 | 0/12 |
| N5_nested_sha_only | 12/12 | 12/12 | 12/12 | 0/12 | 0/12 |
| N6_top_sha_stale_nested_right | 12/12 | 12/12 | 0/12 | 0/12 | 0/12 |
| N7_nested_source_decoy_sup | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| N8_nested_source_decoy_uns | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| N9_nested_id_decoy | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| N10_nested_span_decoy | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| N11_nested_marker_expect_decoy | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| D1_duplicate_top_level | 12/12 | 12/12 | 12/12 | 0/12 | 0/12 |
| S1_flat_confusers | 12/12 | 6/12 | 12/12 | 0/12 | 0/12 |
| S2_nested_confusers | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| F1_flat_plain | 12/12 | 9/12 | 9/12 | 0/12 | 0/12 |

### Receipt paths

All of these are under A. Each exact filename listed has three versions, prefixed `pristine-`, `mutated-`, and `restored-` (24 receipts total); the full expanded paths are in `probe-evidence.json`:

- `a-no-line-3374101.json`, `a-no-line-3374102.json`.
- `b-no-revision-3374201.json`, `b-no-revision-3374202.json`.
- `c-both-everywhere-3374301.json`, `c-both-everywhere-3374302.json`.
- `d-duplicate-claim-3374401.json`, `d-duplicate-claim-3374402.json`.

Opened mutated seed-one receipts with JSON selectors. Actual miss classifications:

- `A/mutated-a-no-line-3374101.json`: 21 `mislocated+finding-set` misses (12 N3, six S1, three F1).
- `A/mutated-b-no-revision-3374201.json`: 15 `stale+finding-set` misses (12 N6, three F1).
- `A/mutated-c-both-everywhere-3374301.json`: all 144 retain the correct observation but fail finding-set equality: invalid 12, mislocated 21, stale 15, supported 87, unsupported 9.
- `A/mutated-d-duplicate-claim-3374401.json`: 144 `none` misses.

Those four opened receipts carry the frozen counter hash above, `gate_rc=1`, `gate_timed_out=false`, and `predicate_holds=false`. `A/restored-d-duplicate-claim-3374402.json:3-14` records the frozen counter hash, restored gate hash O, 144/144 and `predicate_holds=true`.

The counter therefore distinguishes correct observed verdicts from missing or extraneous findings; c cannot pass merely by printing both finding names. It also rejects repeated CLAIM lines rather than accepting either occurrence. No defective control met the target, so there is no surviving-control explanation to report.

## Hashes and exact restoration

| Control | Pristine SHA-256 | Mutated SHA-256 (archived A copy) | Restored SHA-256 |
|---|---|---|---|
| a | O | `50dbce6f73ccf1fa4995fea713566b25ba495bd4fc5c53e1d3d910850850c5f5` | O |
| b | O | `af07412f4b1d033cf90a6478ab377eaf972b356dae38400474e75ecbca221605` | O |
| c | O | `d996e6be14d1a9783c59ce9cf871fbac063ec45c3eeeb7b6e55daf247f70c52f` | O |
| d | O | `4071b038f6932968edf617fef55dfd86dbc8b2e9e1c0ef0538554e5e87f08f4c` | O |

Restoration ran in a `finally` block after all mutated detector calls joined. For each control, actual command `timeout 15s cp S/oracle-pristine.sh S/CONTROL.sh` exited 0, stdout/stderr empty, and comparison of the full restored bytes to the pristine oracle returned `exact_bytes_equal=true`. `probe-evidence.json` records each expanded command and before/after digest. The same frozen counter, same control path and same two seeds then returned 144/144 on every restored gate. The preserved source oracle and BASE were never mutated.

## Bounds and limits

`timeout 10s df -h /fast` exited 0 before fixture work: 198G available. Counter runs were bounded by timeout, a 2 GiB address-space limit, process limit 2000 and 1 MiB file-size limit. No network requests, installs, subagents, background jobs, process-name signals, Git/JJ writes or lane production-file writes were performed. No builds, selftests or broader battery ran. Only the four assigned finding/output controls were scored; all were feasibility-oracle controls, not an ExecC1Build-style candidate. Other possible defects remain outside this probe.
