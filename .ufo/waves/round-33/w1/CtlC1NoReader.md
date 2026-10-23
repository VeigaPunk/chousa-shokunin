# Round 33 W1 — CtlC1NoReader

## Scope and axes

Scored axis: **operability**. Probe axes: detector discrimination, source-I/O bypass, reproducibility and isolation. This is a pre-data control probe, not a C1 candidate implementation or a round-admission judgment.

Read `corpus/evidence/round33/claims.md` first, then the frozen counter docstring. Constructed three controls from the base gate, changed only a record-only helper and an early `verify_claims` loop bypass, and ran the unchanged counter on pristine, mutated and exactly restored bytes. No production file, counter, Git index or jj state was changed. No source-network access, installations or agent runtime invocations were performed.

Paths below use:
- `L=/home/vgpnk/Projects/shokunin/chousa-shokunin`
- `S=/fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader`
- `A=.ufo/waves/round-33/w1/CtlC1NoReader` (relative to L).

`timeout 10s df -h /fast` exited 0: 804G size, 606G used, 198G available, 76% used. All artifacts in A are below 1 MiB; control sizes from `timeout 10s wc -c ...` were 338357, 338661 and 338391 bytes for a/b/c respectively (exit 0).

## Mutants and expected detector

Expected detector: frozen `python3 corpus/evidence/round33/c1-count.py --gate ... --seed ... --receipt ...`. P1 requires 144/144; its per-record rule compares the observed verdict and the iff-presence of line/revision mismatch findings (`c1-count.py:34-41,369-379`). A no-reader shortcut should miss P1.

- **(a), `A/control-a.sh`:** correct top-level, duplicate-preserving JSON pair reader; `supported` unless any of id/source/span/expect/marker/line/sha256 is duplicated at top level, in which case `invalid`. The helper is at `:1109-1133`; the loop bypass is at `:1474-1494`.
- **(b), `A/control-b.sh`:** the same reader and duplicate rule, otherwise `stale` if top-level sha256 is present, `mislocated` if top-level line is present, otherwise `supported`. Corresponding mismatch findings are emitted. Sha256 has precedence if both keys exist. Helper `:1109-1133`; bypass `:1474-1500`.
- **(c), `A/control-c.sh`:** (b) with the unchanged base flat `json_str`/`json_has_key` reader for id/source/expect and line/sha256 presence. Only duplicate detection retains the correct top-level pair parser, holding duplicate policy constant. Duplicate helper `:1109-1128`; bypass `:1469-1493`.

Each control unconditionally continues to the next record before the original source-resolution, hashing and content-read path. The original base operations are `tools/research-gate.sh:1527-1552`. The control helper consumes only the record argument; it never opens or hashes the cited source. This source-I/O bypass is established by control flow, not a syscall trace. The base pre-loop scan still reads the claims file itself, not cited sources.

## Input and control hashes

`timeout 10s sha256sum tools/research-gate.sh corpus/evidence/round33/c1-count.py` exited 0 and matched the frozen design:

| Bytes | SHA-256 |
|---|---|
| Base/pristine/restored gate | `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` |
| Frozen counter | `ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229` |
| Control (a) | `f6c94eda52b0b654bf23b0730cd5fd3aac0e0a76b23c9d94c1a1fc475590a51d` |
| Control (b) | `11f91f5be528cbbbcb19358b5b7e6260b2fae2f5e0011b2c6656d36c5c2668c3` |
| Control (c) | `c0f935cdd97f39d06271429743409bb3228aac555a782bb86c51c22f7de7d776` |

The mutated gates were copied into A before scoring; `timeout 10s sha256sum` on those copies exited 0 with the three control hashes above. The counter receipts independently pin these same hashes (`A/mutated-a-71816041.json:3-14`, `A/mutated-b-71816047.json:3-14`, `A/mutated-c-71816059.json:3-14`).

**Receipt path caveat:** receipt `gate` paths name working files in S, which have now been restored to base. The retained mutated bytes are the `A/control-{a,b,c}.sh` copies, identified by their receipt hashes. Use those retained copies to reproduce the mutant scores.

## Commands and actual output

Each command ran from L. `C1_TMP`, `C2_TMP` and `TMPDIR` were all set to `S/tmp`. The preserved runner `A/run-probe.py` invokes this bounded command for each seed and records its command, exit, stdout, stderr, and before/after gate hashes in the corresponding `.out` file:

```text
timeout 850s prlimit --as=1073741824 --nproc=2000 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py --gate /fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader/control-<a|b|c>.sh --seed <seed> --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/CtlC1NoReader/<phase>-<control>-<seed>.json
```

This is a command template; all 18 fully expanded commands are preserved at `A/{pristine,mutated,restored}-{a,b,c}-<seed>.out:1`. Exact outer invocations were:

```text
timeout 890s python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader/run-probe.py pristine a 71816041 71816043
timeout 890s python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader/run-probe.py pristine b 71816047 71816051
timeout 890s python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader/run-probe.py pristine c 71816059 71816061
timeout 890s python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader/run-probe.py mutated a 71816041 71816043
timeout 890s python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader/run-probe.py mutated b 71816047 71816051
timeout 890s python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader/run-probe.py mutated c 71816059 71816061
timeout 890s python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader/run-probe.py restored a 71816041 71816043
timeout 890s python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader/run-probe.py restored b 71816047 71816051
timeout 890s python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1NoReader/run-probe.py restored c 71816059 71816061
```

All outer invocations completed successfully; the runner intentionally accepts detector exits 0/1. Every individual detector run exited **1**, with gate exit **1**, no timeout and empty detector stderr. The six seeds were fresh choices for this paired probe, never 3301–3303; the same seed was deliberately reused across its pristine/mutated/restored comparison.

| Control | Seeds | Pristine | Mutated | Restored | Target verdict |
|---|---|---|---|---|---|
| (a) | 71816041, 71816043 | 60/144 each | **99/144 each** | 60/144 each | **MISSES** |
| (b) | 71816047, 71816051 | 60/144 each | **96/144 each** | 60/144 each | **MISSES** |
| (c) | 71816059, 71816061 | 60/144 each | **69/144 each** | 60/144 each | **MISSES** |

Actual per-class stdout lines were identical across the two seeds in each column. Pristine and restored were identical across all six seeds:

| Class | Pristine/restored | (a) | (b) | (c) |
|---|---:|---:|---:|---:|
| N1_nested_line_decoy | 6/12 | 12/12 | 0/12 | 0/12 |
| N2_nested_line_only | 0/12 | 12/12 | 12/12 | 0/12 |
| N3_top_line_wrong_nested_right | 6/12 | 0/12 | 12/12 | 12/12 |
| N4_nested_sha_decoy | 6/12 | 12/12 | 0/12 | 0/12 |
| N5_nested_sha_only | 0/12 | 12/12 | 12/12 | 0/12 |
| N6_top_sha_stale_nested_right | 6/12 | 0/12 | 12/12 | 12/12 |
| N7_nested_source_decoy_sup | 3/6 | 6/6 | 6/6 | 6/6 |
| N8_nested_source_decoy_uns | 3/6 | 0/6 | 0/6 | 0/6 |
| N9_nested_id_decoy | 3/6 | 6/6 | 6/6 | 3/6 |
| N10_nested_span_decoy | 3/6 | 6/6 | 6/6 | 6/6 |
| N11_nested_marker_expect_decoy | 0/6 | 6/6 | 6/6 | 6/6 |
| D1_duplicate_top_level | 0/12 | 12/12 | 12/12 | 12/12 |
| S1_flat_confusers | 12/12 | 6/12 | 6/12 | 6/12 |
| S2_nested_confusers | 0/6 | 6/6 | 0/6 | 0/6 |
| F1_flat_plain | 12/12 | 3/12 | 6/12 | 6/12 |

Evidence: each `.out:8-23` contains its exact count and all 15 class lines; each `.json` includes `predicate_holds=false`, per-class results and individual misses. The six mutated receipt paths are:

- `A/mutated-a-71816041.json`, `A/mutated-a-71816043.json`
- `A/mutated-b-71816047.json`, `A/mutated-b-71816051.json`
- `A/mutated-c-71816059.json`, `A/mutated-c-71816061.json`

For every listed receipt, both matching `pristine-...` and `restored-...` receipts and `.out` files are retained in A.

## Verdict and limits

**No no-reader control MEETS-TARGET.** (a) misses genuine mislocated/stale/unsupported cases despite correctly ignoring nesting and rejecting duplicates. (b) catches wrong bindings but cannot distinguish a correct pin/line from an incorrect one merely by presence. (c) additionally reads nested-only line/sha keys and nested-first ids through the base flat reader. These explanations align with the observed class table and the fixture branches at `c1-count.py:190-225,254-284`.

Strict mutation-test verdict: **INCONCLUSIVE for killed/survived attribution**, not “killed”: pristine itself exits 1 at 60/144. The separate requested control-target verdict is **MISSES for all three**. None is a surviving 144/144 counterexample, and these runs do not establish that every possible no-reader shortcut would fail.

Only the assigned detector was run. No candidate implementation was scored, no counter was edited, and no no-harm battery or production verification is claimed.

## Exact restoration and process closure

After the mutant scores, each `S/control-{a,b,c}.sh` was overwritten with `S/base.pristine.sh` using individual `timeout 10s cp` commands. `timeout 10s sha256sum` on the pristine copy and all three restored working files exited 0; all four hashes were exactly `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`.

The same detector then reproduced 60/144 on both seeds per restored control. `A/restored-a-71816041.out:4-8` and every other restored `.out:4-8` record exit 1, unchanged base hashes before/after, and the 60/144 label. Mutated `.out:5-6` record their unchanged mutant hashes; pristine `.out:5-6` record the base hash. Thus the paired evidence is base → named control → exact base for every seed.

No background job was intentionally started. The tool temporarily managed pristine commands as jobs `bg_2838`, `bg_2839`, `bg_2840`; all three completion notices were received before mutation. All later commands also completed. No process was signalled and no work remains running. Unused scratch fragments were removed; the retained gates, receipts, bounded logs and runner are the probe evidence.
