# CtlC1DoNothing — round 33, wave 1

## Verdict and axes

**MISSES.** The unchanged frozen base scored `TOPLEVEL_FIELD_MATCH=60/144` on three fresh seeds. Each run missed 84 records, returned counter exit 1 and recorded `predicate_holds=false`. The counter did not let this control through.

Axes: **operability** (the scored axis), with evidence integrity and scratch isolation as non-regression constraints. This is the requested identity/do-nothing control, not a C1 candidate. The defect retained is the base reader's first matching occurrence at any nesting depth, with no duplicate-read-key rejection. Mutation-kill verdict: **INCONCLUSIVE**, not killed or survived: the pristine baseline already fails and this control changes no bytes.

Read first: `corpus/evidence/round33/claims.md:1-91`, then the frozen counter docstring `corpus/evidence/round33/c1-count.py:1-43`. P1 requires 144/144; matching includes the top-level id, observed truth and both finding-set conditions (`c1-count.py:34-41,369-379,390-412`).

## Isolation and frozen bytes

Paths below are relative to the lane unless absolute:

- Lane/cwd: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
- Scratch (`S`): `/fast/scratch/hyaku/chousa-r33/w1/CtlC1DoNothing`.
- Artifact directory (`A`): `.ufo/waves/round-33/w1/CtlC1DoNothing`.
- Pristine backup: `S/base-pristine.sh`.
- Scored control: `S/research-gate-do-nothing.sh`.
- Archived control: `A/research-gate-do-nothing.sh` (336677 bytes).

Preparation copied the production gate to the pristine backup, then to the scored control, then to the archived control. Every copy was unchanged. The initial `timeout 30s sha256sum` of the production gate and frozen counter returned, respectively:

```text
f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0
ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229
```

All three initial copy hashes were the first value. Every receipt records these frozen gate/counter hashes at lines 3-5. No production source, counter, Git index or jj state was written.

Before copying, `timeout 30s df -h /fast` exited 0 and reported 198G available (76% used). Final `timeout 30s /usr/bin/du -b -s A` exited 0 and reported **672662 bytes for the entire artifact directory**, so every contained artifact is below 1 MiB. Fixtures are fixed at 144 records; there were no unbounded log/fixture writes.

## Commands, actual output and receipts

Exact expanded command lines, stdout, stderr and counter exit codes for all five invocations are preserved in `A/commands-and-output.json` (7555 bytes). The three fresh-seed invocations ran concurrently and were awaited; no background jobs or subagents were started.

Each actual invocation used this form (the journal contains absolute paths, not these abbreviations):

```sh
env C1_TMP="$S" C2_TMP="$S" TMPDIR="$S" \
  timeout 840s prlimit --as=1073741824 --nproc=2000 \
  python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py \
  --gate "$S/research-gate-do-nothing.sh" --seed SEED --receipt "$A/RECEIPT"
```

`A` in the commands is absolute. The first run additionally used `--keep "$A/fixture-seed-3108314469197929859"`; this retains the source fixtures, `claims.jsonl` and `truth.json` for audit. The Python command runner also had an 850-second bound; the frozen counter bounds the gate itself to 600 seconds (`c1-count.py:57,348-352`). Memory was capped at 1 GiB and processes at 2000 per invocation.

| Run | Seed | Counter exit | Output | Receipt under A |
| --- | --- | --- | --- | --- |
| Fresh control 1 | 3108314469197929859 | 1 | `TOPLEVEL_FIELD_MATCH=60/144` | `do-nothing-seed-3108314469197929859.json` |
| Fresh control 2 | 6584202093639497286 | 1 | `TOPLEVEL_FIELD_MATCH=60/144` | `do-nothing-seed-6584202093639497286.json` |
| Fresh control 3 | 8479468690444388855 | 1 | `TOPLEVEL_FIELD_MATCH=60/144` | `do-nothing-seed-8479468690444388855.json` |
| Pristine lifecycle audit | 3108314469197929859 | 1 | `TOPLEVEL_FIELD_MATCH=60/144` | `pristine-seed-3108314469197929859.json` |
| Restored lifecycle audit | 3108314469197929859 | 1 | `TOPLEVEL_FIELD_MATCH=60/144` | `restored-seed-3108314469197929859.json` |

All captured stderr strings were empty. The three fresh receipts record `gate_rc=1`, `gate_timed_out=false`, `matched=60`, `total=144`, `predicate_holds=false` at lines 9-14. The lifecycle audits use the same bounded detector and first seed; the pristine invocation changes only `--gate` to `S/base-pristine.sh`. They are repeats, not additional fresh seeds.

The following **actual per-class stdout was identical on all five invocations**; full unabridged copies are in the command journal and each receipt has its own `per_class` map:

```text
TOPLEVEL_FIELD_MATCH=60/144
  N1_nested_line_decoy 6/12
  N2_nested_line_only 0/12
  N3_top_line_wrong_nested_right 6/12
  N4_nested_sha_decoy 6/12
  N5_nested_sha_only 0/12
  N6_top_sha_stale_nested_right 6/12
  N7_nested_source_decoy_sup 3/6
  N8_nested_source_decoy_uns 3/6
  N9_nested_id_decoy 3/6
  N10_nested_span_decoy 3/6
  N11_nested_marker_expect_decoy 0/6
  D1_duplicate_top_level 0/12
  S1_flat_confusers 12/12
  S2_nested_confusers 0/6
  F1_flat_plain 12/12
```

## Every missing class: which occurrence wins

The base `json_str` is an unanchored Bash regex over the complete raw record; it returns the **leftmost matching key with a string value**, regardless of depth (`tools/research-gate.sh:1109-1117`). `json_has_key` similarly sees a matching key at any depth, including non-string values (`:1121-1128`). The read callers are `:1455-1483`. The archived gate has exactly these bytes and line numbers.

For nested before/after classes, the before variants miss because the nested field wins; the after variants pass because the top-level field is encountered first. Object, array and deeper-container variants share that behavior. The following observed counts refer to the first fresh receipt's `misses` array; the class scores above hold on every seed.

| Missing class | Misses | Base behavior and observed result | Fixture construction |
| --- | --- | --- | --- |
| `N1_nested_line_decoy` | 6/12 | First nested wrong string `line` wins over the later correct top-level line: six `mislocated` instead of `supported`. | `c1-count.py:190-192` |
| `N2_nested_line_only` | 12/12 | The only occurrence is nested. Six string lines are read and produce `mislocated`; six numeric lines make `json_has_key` true but have no `json_str` match, producing `invalid`. Top-level absence should leave all twelve `supported`. | `:193-196`; gate `:1463-1469,1500-1502` |
| `N3_top_line_wrong_nested_right` | 6/12 | First nested correct line wins over the later wrong top-level line: six `supported` instead of `mislocated`, with the required line-mismatch finding absent. | `:197-199` |
| `N4_nested_sha_decoy` | 6/12 | First nested hash wins over the later correct top-level hash. Three valid-but-wrong hashes produce `stale`; three malformed strings produce `invalid`; all should be `supported`. | `:200-203`; gate `:1493-1494,1536-1546` |
| `N5_nested_sha_only` | 12/12 | The only hash occurrence is nested. Six wrong hex pins produce `stale`, six malformed pins produce `invalid`; absent top-level sha256 should leave all twelve `supported`. | `:204-207` |
| `N6_top_sha_stale_nested_right` | 6/12 | First nested actual hash masks the later stale top-level pin: six `supported` instead of `stale`, with the required revision-mismatch finding absent. | `:208-210` |
| `N7_nested_source_decoy_sup` | 3/6 | First nested source names a file without the span, overriding the later top-level source that contains it: three `unsupported` instead of `supported`. | `:211-214` |
| `N8_nested_source_decoy_uns` | 3/6 | First nested source contains the span, overriding the later top-level source that lacks it: three `supported` instead of `unsupported`. | `:215-218` |
| `N9_nested_id_decoy` | 3/6 | First nested fake id replaces the later top-level id. The gate prints the fake id, so the counter observes `none` for each of the three real ids. | `:219-222`; counter `:363-371`; gate `:1637` |
| `N10_nested_span_decoy` | 3/6 | First nested nonexistent span overrides the later genuine top-level span: three `unsupported` instead of `supported`. | `:223-225` |
| `N11_nested_marker_expect_decoy` | 6/6 | For marker variants, the only nested marker is read as present with top-level `expect=supported`, giving three `invalid`. For expect variants, first nested `expect=contradicted` overrides later `supported`, giving three `unproven` because no marker is defined. | `:226-232`; gate `:1496-1497,1583-1593` |
| `D1_duplicate_top_level` | 12/12 | The first of two top-level string occurrences wins, including when values agree; no duplicate rejection occurs. In seed 3108314469197929859 the twelve required `invalid` results instead are ten `supported`, one `stale`, one `unsupported`. The generator may reverse the pair before placement, but the reader always takes the first textual occurrence. | `:233-253`; gate `:1109-1128` |
| `S2_nested_confusers` | 6/6 | After the confuser string, the first matching `line` is the wrong nested member, before the correct top-level member: six `mislocated` instead of `supported`. String confusers do not make this regex depth-aware. | `:262-268` |

`S1_flat_confusers` and `F1_flat_plain` have no misses (12/12 each). This is evidence for those frozen cases only, not a claim that every possible JSON string is parsed correctly. Their construction is `c1-count.py:254-261,269-284`. Verdict branches for the table are gate `:1519-1524,1536-1546,1576-1619`; all per-record mismatches remain in each receipt.

## Restoration evidence and limits

The control is an identity copy; no behavior-bearing byte was edited. Nevertheless, before the lifecycle audits I explicitly restored it with:

```sh
timeout 30s cp /fast/scratch/hyaku/chousa-r33/w1/CtlC1DoNothing/base-pristine.sh /fast/scratch/hyaku/chousa-r33/w1/CtlC1DoNothing/research-gate-do-nothing.sh
```

That command exited 0. Both immediately after restoration and after the restored detector run, `timeout 30s sha256sum` returned the same hash for pristine backup, scratch control and archived control:

```text
f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0
```

Thus before = scored identity = restored = archived bytes. The final counter hash also remained `ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229`. The same-seed pristine/control/restored outputs all equal 60/144; baseline failure is not counted as a killed mutant.

No candidate implementation was scored. No counter was edited, no network was used, no tools were installed or updated, and no process was signalled. All started detector subprocesses were awaited. No build, selftest or broader battery was run; this report is limited to the assigned do-nothing pre-data control.
