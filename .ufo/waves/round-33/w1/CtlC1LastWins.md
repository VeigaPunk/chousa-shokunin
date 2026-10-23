# Round 33 W1 — CtlC1LastWins occurrence-order controls

## Scope, axes, and detector

- Axes: **operability** (the frozen 144-record / 15-class predicate), plus control isolation and byte-exact reproducibility. These are deliberately defective controls, not candidate C1 implementations.
- Read the frozen claim first (`corpus/evidence/round33/claims.md:16-83`), then the counter docstring (`corpus/evidence/round33/c1-count.py:1-42`). Expected detector: `TOPLEVEL_FIELD_MATCH=144/144` on both seeds; counter exit 0 only at 144 (`:390-412`). A lower count is **MISSES**.
- Base acquired with `timeout 20 git show 3b528b9a926dd53001a1f1da5df6be1c63fca3ca:tools/research-gate.sh` (exit 0), with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed from the subprocess environment. Its SHA-256 matched the assigned base. No candidate implementation was scored.
- Scratch: `/fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins/`. Artifact references below are relative to the lane; the common artifact directory is `.ufo/waves/round-33/w1/CtlC1LastWins`.

## Mutations and immutable gate copies

All edits are confined to the two field-reader helpers; callers and the counter are untouched. The archived copies below retain mutated bytes; the scratch working copies have been restored.

| Control | Exact behavior-bearing change | Archived gate | Bytes | SHA-256 |
|---|---|---|---:|---|
| last-occurrence | Prefix both regexes with greedy `.*`; the string reader selects the last matching occurrence. Presence remains existential (`last-occurrence.sh:1111,1126`). | `.ufo/waves/round-33/w1/CtlC1LastWins/last-occurrence.sh` | 336681 | `ff163945f7fadd2f69031089f13d7b3d87fdadcbf3a8baa5dc02f64f8b7975be` |
| comma-brace-anchored | Prefix both regexes with `[,{][[:space:]]*`; select the earliest occurrence whose preceding non-space character is comma or opening brace (`comma-brace-anchored.sh:1111,1126`). | `.ufo/waves/round-33/w1/CtlC1LastWins/comma-brace-anchored.sh` | 336709 | `6ecacaec31b124e6d8cfd8d3c5a0da654378eee6e3a4f629b5693570be9a2ae4` |
| after-last-close | Remove everything through the last `}`, then through the last remaining `]`, before both searches (`after-last-close.sh:1111-1112,1128-1132`). This literally includes the outer closing brace. | `.ufo/waves/round-33/w1/CtlC1LastWins/after-last-close.sh` | 336776 | `904fa1cf82925d5064c149e549c69b70332d0c363a55d743957eeefc60b75c60` |

Minimal diffs are the corresponding `.ufo/waves/round-33/w1/CtlC1LastWins/<control>.patch` files. `manifest.json:1-47` records the hashes, sizes, seeds and exact restoration.

## Results: same detector on pristine, mutated, and restored bytes

| Control | Seed | Pristine | Mutated | Restored | Control verdict |
|---|---:|---:|---:|---:|---|
| last-occurrence | 1631988779328 | 60/144 | 69/144 | 60/144 | **MISSES** |
| last-occurrence | 1490306144461 | 60/144 | 69/144 | 60/144 | **MISSES** |
| comma-brace-anchored | 2039944288127 | 60/144 | 60/144 | 60/144 | **MISSES** |
| comma-brace-anchored | 1328209670331 | 60/144 | 60/144 | 60/144 | **MISSES** |
| after-last-close | 1928707554551 | 60/144 | 0/144 | 60/144 | **MISSES** |
| after-last-close | 1283760385239 | 60/144 | 0/144 | 60/144 | **MISSES** |

**Mutation-test verdict: INCONCLUSIVE for every probe, not killed.** Every pristine baseline already failed the frozen predicate (60/144), so a mutant failure cannot be called a killed mutant. The separate control verdict is unambiguously MISSES on both fresh seeds for each control. No control met 144/144.

All 18 detector commands exited **1**; every recorded gate subprocess exited **1**, with `gate_timed_out=false`. There were no harness errors or timeouts. All receipts carry frozen counter SHA-256 `ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229` and the appropriate gate hash.

### Actual per-class stdout

For each control the following complete stdout was identical on its two seeds. Each individual output and exit code is also preserved in its `.log` file.

#### last-occurrence

```text
TOPLEVEL_FIELD_MATCH=69/144
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
  N11_nested_marker_expect_decoy 3/6
  D1_duplicate_top_level 0/12
  S1_flat_confusers 12/12
  S2_nested_confusers 6/6
  F1_flat_plain 12/12
```

#### comma-brace-anchored

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

#### after-last-close

```text
TOPLEVEL_FIELD_MATCH=0/144
  N1_nested_line_decoy 0/12
  N2_nested_line_only 0/12
  N3_top_line_wrong_nested_right 0/12
  N4_nested_sha_decoy 0/12
  N5_nested_sha_only 0/12
  N6_top_sha_stale_nested_right 0/12
  N7_nested_source_decoy_sup 0/6
  N8_nested_source_decoy_uns 0/6
  N9_nested_id_decoy 0/6
  N10_nested_span_decoy 0/6
  N11_nested_marker_expect_decoy 0/6
  D1_duplicate_top_level 0/12
  S1_flat_confusers 0/12
  S2_nested_confusers 0/6
  F1_flat_plain 0/12
```

### Receipt and command/output index

Every JSON below has an adjacent `.log` with the same stem, containing the exact command, PID, exit code, stdout, stderr, elapsed time, and gate hash. `.ufo/waves/round-33/w1/CtlC1LastWins/run-records.json` also contains all 18 exact commands and outputs.

| Control | Seed | Phase | Receipt (relative to the common artifact directory) |
|---|---:|---|---|
| last-occurrence | 1631988779328 | pristine | `last-occurrence-pristine-1631988779328.json` |
| last-occurrence | 1631988779328 | mutated | `last-occurrence-mutated-1631988779328.json` |
| last-occurrence | 1631988779328 | restored | `last-occurrence-restored-1631988779328.json` |
| last-occurrence | 1490306144461 | pristine | `last-occurrence-pristine-1490306144461.json` |
| last-occurrence | 1490306144461 | mutated | `last-occurrence-mutated-1490306144461.json` |
| last-occurrence | 1490306144461 | restored | `last-occurrence-restored-1490306144461.json` |
| comma-brace-anchored | 2039944288127 | pristine | `comma-brace-anchored-pristine-2039944288127.json` |
| comma-brace-anchored | 2039944288127 | mutated | `comma-brace-anchored-mutated-2039944288127.json` |
| comma-brace-anchored | 2039944288127 | restored | `comma-brace-anchored-restored-2039944288127.json` |
| comma-brace-anchored | 1328209670331 | pristine | `comma-brace-anchored-pristine-1328209670331.json` |
| comma-brace-anchored | 1328209670331 | mutated | `comma-brace-anchored-mutated-1328209670331.json` |
| comma-brace-anchored | 1328209670331 | restored | `comma-brace-anchored-restored-1328209670331.json` |
| after-last-close | 1928707554551 | pristine | `after-last-close-pristine-1928707554551.json` |
| after-last-close | 1928707554551 | mutated | `after-last-close-mutated-1928707554551.json` |
| after-last-close | 1928707554551 | restored | `after-last-close-restored-1928707554551.json` |
| after-last-close | 1283760385239 | pristine | `after-last-close-pristine-1283760385239.json` |
| after-last-close | 1283760385239 | mutated | `after-last-close-mutated-1283760385239.json` |
| after-last-close | 1283760385239 | restored | `after-last-close-restored-1283760385239.json` |

### Commands actually run

All counter commands ran with cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Parallel batches were bounded to three simultaneous foreground detector processes; all were awaited. The first mutated command for each control was:

```sh
timeout --kill-after=5 180 prlimit --as=1073741824 --nproc=2000 -- env C1_TMP=/fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins C2_TMP=/fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins TMPDIR=/fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py --gate /fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins/last-occurrence.sh --seed 1631988779328 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/CtlC1LastWins/last-occurrence-mutated-1631988779328.json --keep /fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins/last-occurrence-mutated-1631988779328-fixture
# exit 1
timeout --kill-after=5 180 prlimit --as=1073741824 --nproc=2000 -- env C1_TMP=/fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins C2_TMP=/fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins TMPDIR=/fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py --gate /fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins/comma-brace-anchored.sh --seed 2039944288127 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/CtlC1LastWins/comma-brace-anchored-mutated-2039944288127.json --keep /fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins/comma-brace-anchored-mutated-2039944288127-fixture
# exit 1
timeout --kill-after=5 180 prlimit --as=1073741824 --nproc=2000 -- env C1_TMP=/fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins C2_TMP=/fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins TMPDIR=/fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py --gate /fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins/after-last-close.sh --seed 1928707554551 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/CtlC1LastWins/after-last-close-mutated-1928707554551.json --keep /fast/scratch/hyaku/chousa-r33/w1/CtlC1LastWins/after-last-close-mutated-1928707554551-fixture
# exit 1
```

The other commands have the same `timeout --kill-after=5 180 prlimit --as=1073741824 --nproc=2000 -- env C1_TMP=... C2_TMP=... TMPDIR=... python3 ...` bounds and are recorded verbatim in the indexed logs. The three `--keep` fixtures remain only under the scratch directory. Historical command paths refer to scratch gates that are now restored; use the archived, hash-identical gate copies above to reproduce the mutant runs.

## Interpretation and limits

- **Last occurrence:** 69/144 does not repair top-level semantics. Nested-only fields still affect records, later nested decoys are still selected, and all 12 duplicated-top-level rows fail. The 9-point aggregate increase comes from N11 (+3) and S2 (+6), whose generated relevant top-level fields follow the decoys (`c1-count.py:226-232,262-268`). It is not a no-harm improvement: comparing receipt miss-id sets shows **45 gains and 36 losses** on each seed (`detector-deltas.json`).
- **Comma/brace anchored:** 60/144, with **0 gains and 0 losses** versus baseline on both fixtures. Nested object keys also have comma/brace predecessors; the prefix does not enforce top-level membership. Examples include supported records read as mislocated and duplicate records read as supported (`comma-brace-anchored-mutated-2039944288127.json:33-55`).
- **After last close:** this is the literal requested rule. A claim line ends with the outer `}` (`research-gate.sh:1442` at base), so removing through that delimiter leaves no suffix to search. [INFERENCE] This rule is therefore degenerate for these valid object records, not a meaningful test of “after the last nested container, excluding the outer close.” Observed evidence is **0/144** and all 144 receipt misses have `observed=none` on both seeds (`after-last-close-mutated-1928707554551.json:11-43`; full misses in that receipt). I did not silently implement the different nested-container heuristic.
- No 144/144 control was found, hence there is no passing-control loophole to explain for these three controls. This result says nothing about other heuristics, arbitrary JSON, or candidate correctness. No counter edits, candidate runs, builds, linters, selftests, network access, or production changes were performed.

## Before/after hashes and restoration

- Before every probe, scratch gate SHA-256 was `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` (all six pristine receipts). Counter SHA-256 was `ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229`.
- The mutated hashes are in the gate-copy table, all six mutated receipts, and `manifest.json:6-33`.
- A `finally` block restored each of the three scratch working gates from the exact saved base bytes; direct byte comparisons were true for all three, and every restored SHA-256 was `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` (`manifest.json:35-47`).
- All six restored detector runs returned 60/144. Per-class maps and the complete miss lists exactly equal their same-seed pristine receipts (`detector-deltas.json`); no restoration-only behavioral difference was observed.
- All started detector PIDs and completion codes are retained in `run-records.json` / `manifest.json`. Every process was awaited; no background job was left running and no process was signalled by name or pattern.
- Initial disk check: `timeout 20 df -h /fast` exited 0, showing 198G available (76% used). Each archived gate is under 337 KB; every artifact is under 1 MiB. All extra artifacts are in the assigned directory; scratch fixtures remain under the assigned scratch directory.
- Tools installed or updated: **none**.
