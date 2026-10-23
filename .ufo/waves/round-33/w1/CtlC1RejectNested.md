# Round 33 W1 — CtlC1RejectNested

## Result and axes

Scored axis: **operability** (`TOPLEVEL_FIELD_MATCH`, frozen target 144/144). Evidence safeguards: unchanged counter/base, isolated controls, repeatability, byte-exact restoration. This was a controls-only mutation probe; no candidate implementation was scored.

| Control | Seeds | Actual counts | Task verdict |
|---|---|---|---|
| (a) Reject any raw `{` or `[` after the opening character | 33173341, 33173342 | 20/144, 20/144 | **MISSES** |
| (b) Reject a read key repeated anywhere, including nested members | 33173343, 33173344 | 36/144, 36/144 | **MISSES** |
| (c) Cut the record off before its first subsequent raw container opener; retain first-match/ignore-duplicate reads | 33173345, 33173346 | 35/144, 35/144 | **MISSES** |

No control met 144/144. These controls were not let through. **Mutation-kill verdict: INCONCLUSIVE for all three**, not killed: each pristine baseline already failed the frozen detector (60/144, exit 1), and each exact restoration returned the same 60/144. The control-specific MISSES results remain observed counter results, not claims of a passing-baseline mutation kill.

## Frozen inputs and isolation

Read first: `corpus/evidence/round33/claims.md:1-91`; then `corpus/evidence/round33/c1-count.py:1-43`. The expected detector is the committed counter, unchanged: exactly one top-level-id CLAIM with the true observed disposition, with line/revision finding membership iff mislocated/stale (`c1-count.py:34-41,369-379`). Frozen success is 144/144 (`claims.md:51-59`).

Paths used throughout:

- `L = /home/vgpnk/Projects/shokunin/chousa-shokunin`
- `S = /fast/scratch/hyaku/chousa-r33/w1/CtlC1RejectNested`
- `A = /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/CtlC1RejectNested`

`timeout 20s df -h /fast` exited 0 before copies: `/dev/nvme1n1p2`, 804G total, 606G used, 198G available, 76% used. `timeout 20s mkdir -p S A` created only the assigned directories. `timeout 20s cp --no-clobber L/tools/research-gate.sh S/base-gate.sh`, then three corresponding copies from `S/base-gate.sh`, each exited 0. These abbreviations denote the literal paths above; no production file was edited. No Git/jj commands, network requests, installations, background jobs, subagents, or process signals were used.

Initial and final `timeout 20s sha256sum L/tools/research-gate.sh L/corpus/evidence/round33/c1-count.py` both exited 0 and printed:

```text
f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0  tools/research-gate.sh
ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229  corpus/evidence/round33/c1-count.py
```

## Mutants and preserved artifacts

All controls started as exact copies of the base gate. Only the indicated insertion changed. Helpers otherwise remain the base's unanchored regex readers (`tools/research-gate.sh:1109-1128`). Preserved mutant gate copies are in `A`; scratch control filenames now contain restored base bytes, so use the archived copies to reproduce mutants.

### (a) Raw nested-opener refusal

Artifact `A/a-reject-nested.sh:1519-1521` adds, immediately before the existing invalid-record branch:

```bash
    if [[ ${line:1} == *'{'* || ${line:1} == *'['* ]]; then
      bad="control: nested container refused"
    fi
```

This deliberately refuses nested records instead of ignoring their unknown nested members. It is string-unaware: raw openers inside strings also trigger refusal. It does not add duplicate detection.

### (b) Anywhere-duplicate refusal

Artifact `A/b-reject-repeated-key.sh:1519-1530` adds, at the same site:

```bash
    local control_key control_re control_tail
    for control_key in id source span expect marker line sha256; do
      control_re="\"${control_key}\"[[:space:]]*:"
      control_tail=$line
      if [[ $control_tail =~ $control_re ]]; then
        control_tail=${control_tail#*"${BASH_REMATCH[0]}"}
        if [[ $control_tail =~ $control_re ]]; then
          bad="control: read key repeated anywhere"
          break
        fi
      fi
    done
```

The duplicate check has no depth boundary. Top-level plus nested occurrences are refused, not treated as a single top-level member. The base readers remain unchanged for records the extra check does not reject.

### (c) Prefix-only verification, duplicates ignored

Artifact `A/c-truncate-nested.sh:1448-1451` adds, after the base outer-object check and before field reads:

```bash
    local control_tail=${line:1}
    control_tail=${control_tail%%\{*}
    control_tail=${control_tail%%\[*}
    line="{${control_tail}"
```

“Cut off” here is literal prefix truncation at the first subsequent raw `{` or `[`, not balanced removal of a nested value. Later top-level text is discarded too; raw openers in strings are also cut points. The base regex helpers then verify whatever fields remain in the prefix, without enforcing JSON closure or duplicate invalidation. Flat duplicate records retain base first-match behavior. No shape-, filename-, id-, or truth-specific shortcut was added.

### Hashes and sizes

`timeout 20s cp S/a-reject-nested.sh S/b-reject-repeated-key.sh S/c-truncate-nested.sh A/` exited 0 before mutant scoring. `timeout 20s sha256sum` over scratch and archive files printed identical hashes for each pair:

| Artifact in A | Mutant SHA-256 | Size from `timeout 20s stat --printf='%n %s bytes\n' ...` (exit 0) |
|---|---|---:|
| `a-reject-nested.sh` | `4d3d1cdc8dcbb70cefe36812e186caff83f5a7b3a50513fa7e6d17e128022eb0` | 336790 bytes |
| `b-reject-repeated-key.sh` | `c422dee0dfc767bdbc1422d7c7ee9028a5fbbff9cfdd0bea597c9fc2dd8a059d` | 337125 bytes |
| `c-truncate-nested.sh` | `f2ac600bce5555522a4547bd1a98a128465d9c0bdd318e9f005634d595eb1fdf` | 336814 bytes |

Each artifact is below 1 MiB. Directory listing showed receipts of approximately 11.1–15.7 KiB each.

## Actual detector commands and receipts

All twelve invocations used cwd `L`, the same external bound and resource caps, and all three temp variables set to `S`. With the path abbreviations expanded, each command was:

```text
timeout 55s prlimit --nproc=2000 --as=1073741824 env C1_TMP=S C2_TMP=S TMPDIR=S python3 L/corpus/evidence/round33/c1-count.py --gate S/GATE --seed SEED --receipt A/RECEIPT
```

Exact substitutions and observed outputs:

| GATE | SEED | RECEIPT | Counter stdout headline | Counter exit |
|---|---:|---|---|---:|
| `a-reject-nested.sh` | 33173341 | `a-pristine-33173341.json` | `TOPLEVEL_FIELD_MATCH=60/144` | 1 |
| `b-reject-repeated-key.sh` | 33173343 | `b-pristine-33173343.json` | `TOPLEVEL_FIELD_MATCH=60/144` | 1 |
| `c-truncate-nested.sh` | 33173345 | `c-pristine-33173345.json` | `TOPLEVEL_FIELD_MATCH=60/144` | 1 |
| `a-reject-nested.sh` | 33173341 | `a-mutated-33173341.json` | `TOPLEVEL_FIELD_MATCH=20/144` | 1 |
| `a-reject-nested.sh` | 33173342 | `a-mutated-33173342.json` | `TOPLEVEL_FIELD_MATCH=20/144` | 1 |
| `b-reject-repeated-key.sh` | 33173343 | `b-mutated-33173343.json` | `TOPLEVEL_FIELD_MATCH=36/144` | 1 |
| `b-reject-repeated-key.sh` | 33173344 | `b-mutated-33173344.json` | `TOPLEVEL_FIELD_MATCH=36/144` | 1 |
| `c-truncate-nested.sh` | 33173345 | `c-mutated-33173345.json` | `TOPLEVEL_FIELD_MATCH=35/144` | 1 |
| `c-truncate-nested.sh` | 33173346 | `c-mutated-33173346.json` | `TOPLEVEL_FIELD_MATCH=35/144` | 1 |
| `a-reject-nested.sh` | 33173341 | `a-restored-33173341.json` | `TOPLEVEL_FIELD_MATCH=60/144` | 1 |
| `b-reject-repeated-key.sh` | 33173343 | `b-restored-33173343.json` | `TOPLEVEL_FIELD_MATCH=60/144` | 1 |
| `c-truncate-nested.sh` | 33173345 | `c-restored-33173345.json` | `TOPLEVEL_FIELD_MATCH=60/144` | 1 |

All twelve receipts were opened for metadata. Each has `counter_sha256=ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229`, `gate_rc=1`, `gate_timed_out=false`, and `predicate_holds=false`. Mutant receipt gate hashes match the artifact hashes above; pristine/restored receipt gate hashes equal `f4731885…`. All runs completed within the 55-second outer bound; mutant receipt elapsed times were 21.385, 22.081, 22.712, 23.173, 25.918, and 23.108 seconds respectively. Restored tool wall times were 41.48–41.61 seconds. There was no timeout or harness-error result.

### Per-class stdout: pristine and restored (all six runs identical)

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

### Per-class stdout: (a), seeds 33173341 and 33173342 (identical)

```text
TOPLEVEL_FIELD_MATCH=20/144
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
  S1_flat_confusers 8/12
  S2_nested_confusers 0/6
  F1_flat_plain 12/12
```

### Per-class stdout: (b), seeds 33173343 and 33173344 (identical)

```text
TOPLEVEL_FIELD_MATCH=36/144
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
  D1_duplicate_top_level 12/12
  S1_flat_confusers 12/12
  S2_nested_confusers 0/6
  F1_flat_plain 12/12
```

### Per-class stdout: (c), seed 33173345

```text
TOPLEVEL_FIELD_MATCH=35/144
  N1_nested_line_decoy 2/12
  N2_nested_line_only 0/12
  N3_top_line_wrong_nested_right 1/12
  N4_nested_sha_decoy 2/12
  N5_nested_sha_only 0/12
  N6_top_sha_stale_nested_right 1/12
  N7_nested_source_decoy_sup 1/6
  N8_nested_source_decoy_uns 2/6
  N9_nested_id_decoy 3/6
  N10_nested_span_decoy 0/6
  N11_nested_marker_expect_decoy 1/6
  D1_duplicate_top_level 0/12
  S1_flat_confusers 9/12
  S2_nested_confusers 1/6
  F1_flat_plain 12/12
```

### Per-class stdout: (c), seed 33173346

```text
TOPLEVEL_FIELD_MATCH=35/144
  N1_nested_line_decoy 2/12
  N2_nested_line_only 3/12
  N3_top_line_wrong_nested_right 0/12
  N4_nested_sha_decoy 1/12
  N5_nested_sha_only 3/12
  N6_top_sha_stale_nested_right 1/12
  N7_nested_source_decoy_sup 1/6
  N8_nested_source_decoy_uns 1/6
  N9_nested_id_decoy 0/6
  N10_nested_span_decoy 0/6
  N11_nested_marker_expect_decoy 0/6
  D1_duplicate_top_level 0/12
  S1_flat_confusers 10/12
  S2_nested_confusers 1/6
  F1_flat_plain 12/12
```

## Restoration evidence and limits

After mutant scoring, these three commands each exited 0:

```text
timeout 20s cp S/base-gate.sh S/a-reject-nested.sh
timeout 20s cp S/base-gate.sh S/b-reject-repeated-key.sh
timeout 20s cp S/base-gate.sh S/c-truncate-nested.sh
```

`timeout 20s sha256sum S/base-gate.sh S/a-reject-nested.sh S/b-reject-repeated-key.sh S/c-truncate-nested.sh` exited 0: all four hashes were exactly `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`. Then the same bounded detector was run on each restored control path, producing the three restored receipts listed above.

Each `timeout 20s cmp -s S/base-gate.sh S/<control-gate>` exited 0. The conjunction printed `RESTORATION_CMP=a:0,b:0,c:0; scratch gates equal pristine bytes`. The subsequent lane gate/counter hashes remained the frozen hashes quoted above. Required archived mutant copies in `A` were intentionally preserved, not restored.

Limits: only the three specified control shortcuts and six specified mutation seeds were scored. Results do not establish general adequacy of the frozen counter, or any candidate's correctness. Baseline failure prevents a clean killed-mutant inference. No candidate scoring, integration, shipping, counter edit, or out-of-scope battery was performed.
