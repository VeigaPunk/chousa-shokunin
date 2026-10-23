# CtlC1PartialFields — round 33, wave 1

## Axes and scope

Axes: **operability** (the scored axis), isolated mutation/exact restoration, and reproducible evidence. These are two deliberately incomplete CONTROL gates, not candidate implementations. No production source, counter, Git index, or jj state was edited. No candidate was scored.

Read first: `corpus/evidence/round33/claims.md:1-91`, then the counter docstring at `corpus/evidence/round33/c1-count.py:1-43`. Frozen target is `TOPLEVEL_FIELD_MATCH=144/144` on both fresh seeds (`claims.md:51-58`).

Paths below use:

- `A = /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/CtlC1PartialFields`
- `S = /fast/scratch/hyaku/chousa-r33/w1/CtlC1PartialFields`
- All commands ran with cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

## Mutants and expected detector

1. **Partial fields (`partial-fields.sh`)**: only `line` and `sha256` use a string-aware top-level reader, with repeated top-level occurrences rejected. `id/source/span/expect/marker` retain the exact base flat regex. The helper uses Python's `JSONDecoder.raw_decode` to skip each complete value and returns the original string body, preserving escapes. Presence remains true for duplicate/non-string values; the string read fails for duplicated `line`/`sha256`, so existing gate validation produces `invalid`. The control routes only these two keys through the helper (`A/partial-fields.sh:1159-1162,1174-1177`). Expected frozen detector failure: nested fields outside those two keys and duplicated `source`.
2. **Partial duplicate policy (`partial-duplicates.sh`)**: every key uses that top-level reader, but only duplicated `line`/`sha256` are rejected. Other duplicate keys take their first top-level value. Helper delegation is at `A/partial-duplicates.sh:1157-1165`. Expected frozen detector failure: duplicated `source`. The counter's D1 class deliberately includes `source` as well as `line` and `sha256` (`c1-count.py:85,233-253`).

Both start from the supplied BASE gate; only the JSON helper area was changed. The archived gate copies retain the control bytes; the experimental gate paths in scratch were restored after scoring.

## Command and output evidence

Initial commands (all exit 0):

```sh
timeout 20s df -h /fast
timeout 20s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py
```

`/fast` had 198G available. Observed hashes:

```text
BASE    f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0
COUNTER ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229
```

Each detector invocation used environment `C1_TMP=S`, `C2_TMP=S`, `TMPDIR=S`, and this argv, with the placeholders expanded according to the run table:

```sh
timeout 660s prlimit --as=1073741824 --nproc=2000 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py --gate S/CONTROL.sh --seed SEED --receipt A/STAGE-CONTROL-SEED.json
```

The process was awaited synchronously with a 680-second outer subprocess deadline; there were no background jobs. The detector itself bounds the gate to 600 seconds (`c1-count.py:57,348-349`). `A/runs.json` contains every fully expanded command argv, cwd, environment overrides, actual exit code, stdout, stderr, elapsed time, receipt path, and before/after gate hashes. Every run's stderr was empty. All 12 counter exits were **1**; all 12 receipt `gate_rc` values were **1**, without gate timeout.

| Control | Seed | Pristine | Mutated | Restored | Control verdict |
|---|---:|---:|---:|---:|---|
| partial-fields | 633207 | 60/144 | 122/144 | 60/144 | **MISSES** |
| partial-fields | 633241 | 60/144 | 122/144 | 60/144 | **MISSES** |
| partial-duplicates | 633269 | 60/144 | 140/144 | 60/144 | **MISSES** |
| partial-duplicates | 633283 | 60/144 | 140/144 | 60/144 | **MISSES** |

These are four fresh seeds, none of 3301–3303. For each control, the identical counter, seed, gate path, limits, and temporary-directory environment were used on pristine, mutated, and restored bytes. Only the receipt/output filename's stage changed.

### Partial-fields: actual per-class stdout (identical on both seeds)

```text
TOPLEVEL_FIELD_MATCH=122/144
  N1_nested_line_decoy 12/12
  N2_nested_line_only 12/12
  N3_top_line_wrong_nested_right 12/12
  N4_nested_sha_decoy 12/12
  N5_nested_sha_only 12/12
  N6_top_sha_stale_nested_right 12/12
  N7_nested_source_decoy_sup 3/6
  N8_nested_source_decoy_uns 3/6
  N9_nested_id_decoy 3/6
  N10_nested_span_decoy 3/6
  N11_nested_marker_expect_decoy 0/6
  D1_duplicate_top_level 8/12
  S1_flat_confusers 12/12
  S2_nested_confusers 6/6
  F1_flat_plain 12/12
```

Receipts:

- `A/mutated-partial-fields-633207.json`
- `A/mutated-partial-fields-633241.json`

Both label `predicate_holds=false`. The first receipt's fields and class counts are at `:3-30`; its 22 misses are at `:32-165`. Examples: nested id is observed `none` (`:46-49`), nested source produces `unsupported` instead of `supported` (`:76-79`), and a duplicated source is observed `supported` rather than `invalid` (`:34-37`). Nested marker/expect failures are also retained (`:64-67,94-97`).

### Partial-duplicates: actual per-class stdout (identical on both seeds)

```text
TOPLEVEL_FIELD_MATCH=140/144
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
  D1_duplicate_top_level 8/12
  S1_flat_confusers 12/12
  S2_nested_confusers 6/6
  F1_flat_plain 12/12
```

Receipts:

- `A/mutated-partial-duplicates-633269.json`
- `A/mutated-partial-duplicates-633283.json`

Both label `predicate_holds=false`. The first receipt records all four misses, exclusively D1 (`:32-57`): truth `invalid`, observed `supported` or `unsupported`. D1's four source-duplicate records are generated by `c1-count.py:85,243-253`; the control checks duplicates only for the other two D1 keys. Thus fixing top-level selection for every field but restricting duplicate rejection to `line`/`sha256` is insufficient. **Neither control reaches 144/144; there is no partial-fix false pass in these probes.**

### Pristine and restored: actual per-class stdout (all eight runs)

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

These receipts are `A/{pristine,restored}-partial-fields-{633207,633241}.json` and `A/{pristine,restored}-partial-duplicates-{633269,633283}.json` (eight concrete files). Each run also has matching `.stdout.txt` and `.stderr.txt` artifacts.

## Hashes and exact restoration

Before mutation, both experimental gates had BASE SHA-256. Archived mutant copies:

| Artifact | SHA-256 | Bytes |
|---|---|---:|
| `A/partial-fields.sh` | `97343280fb9f46cc183e6ee8cb69fb4ff8e22ffac225a1a6a998f2688ab9cc54` | 338126 |
| `A/partial-duplicates.sh` | `9330f2b50fc39fe94f475db1648ac342843023ad99f08ddb81eb2af52b02acfd` | 337466 |

The scratch and archived mutant hashes were measured before scoring; every mutated receipt independently records its control hash. Restoration ran in a Python `finally` block after the mutated runs, using these argv (exit **0** each):

```sh
timeout 20s cp /fast/scratch/hyaku/chousa-r33/w1/CtlC1PartialFields/pristine.sh /fast/scratch/hyaku/chousa-r33/w1/CtlC1PartialFields/partial-fields.sh
timeout 20s cp /fast/scratch/hyaku/chousa-r33/w1/CtlC1PartialFields/pristine.sh /fast/scratch/hyaku/chousa-r33/w1/CtlC1PartialFields/partial-duplicates.sh
```

`A/restorations.json` records each mutant's before hash, restored BASE hash, archive hash, and `exact_pristine_match=true` from byte-for-byte comparison with the untouched pristine copy. Restored scores are shown above, not inferred from hashing.

Final command (exit **0**):

```sh
timeout 20s sha256sum /fast/scratch/hyaku/chousa-r33/w1/CtlC1PartialFields/pristine.sh /fast/scratch/hyaku/chousa-r33/w1/CtlC1PartialFields/partial-fields.sh /fast/scratch/hyaku/chousa-r33/w1/CtlC1PartialFields/partial-duplicates.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py
```

Observed: pristine, both restored experimental gates, and lane production gate all equal BASE; frozen counter still equals COUNTER. Archived gates retain their mutant hashes.

Evidence manifest hashes (measured by `timeout 20s sha256sum`):

- `A/runs.json`: `657e6d26147ab9ee4977793b4d48e7b8c91538963d058b8527a3af2a54139606`
- `A/restorations.json`: `bd4b1b800dc0309ed0845ba1d2197b6e1c1cb52c9501b4004d6dc2e0df119b8c`

`timeout 20s wc -c A/*` (with A expanded; exit **0**) measured 805407 total bytes before this report, maximum individual artifact 338126 bytes. Receipts are at most 11330 bytes; `runs.json` is 21535 bytes. Every artifact is under 1 MiB. `A/probe-errors.json` is `[]`.

## Verdict and limits

- **Partial-fields control: MISSES**, 122/144 on both fresh seeds.
- **Partial-duplicates control: MISSES**, 140/144 on both fresh seeds.
- Formal mutation-test classification: **INCONCLUSIVE**, not killed, because the pristine implementation also fails the frozen detector (60/144). The control results establish the requested predicate misses, not a passing-baseline mutant kill.
- No counter changes, candidate scores, integration, source/network opens, tool installs/updates, background jobs, process signals, production changes, or additional tests. No claim beyond these two controls and these four seeds. General duplicate coverage is limited to the counter's three D1 keys (`c1-count.py:85`); this probe does not establish coverage for duplicate id/span/expect/marker.
