# CtlC1BraceDepth — round 33, wave 1 pre-data controls

## Scope and verdict

Axes tracked: **operability** (the sole scored C1 axis), detector coverage, and isolation/restoration integrity. The latter two are probe constraints, not additional round claims.

Built only the three assigned naive-reader controls from the frozen BASE gate; changed only the `json_str` / `json_has_key` reader region (`tools/research-gate.sh:1109-1128`), adding a shared scanner there. All three select the first matching depth-1 field and do not reject duplicate top-level fields. No candidate implementation was scored, and neither the counter nor production files were edited.

| Control / mutant | Fresh seeds | Pristine count | Mutated count | Restored count | Requested control verdict |
|---|---|---|---|---|---|
| A: counts `{ [ } ]` without tracking string state | 33881 / 33882 | 60/144 / 60/144 | **121/144 / 122/144** | 60/144 / 60/144 | **MISSES** |
| B: tracks strings correctly, counts braces only, ignores arrays | 33883 / 33884 | 60/144 / 60/144 | **132/144 / 132/144** | 60/144 / 60/144 | **MISSES** |
| C: tracks strings and both container kinds, but a quote after any backslash is treated as escaped | 33885 / 33886 | 60/144 / 60/144 | **129/144 / 130/144** | 60/144 / 60/144 | **MISSES** |

All 18 frozen-detector invocations exited **1**, with the counts above. No control reached 144/144. Formal killed/survived mutation classification: **INCONCLUSIVE for each**, because its pristine BASE already fails the detector. These are measured negative-control rejections, not passing-baseline mutant kills.

## Provenance and retained gates

Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

In the rest of this report, `A` means `.ufo/waves/round-33/w1/CtlC1BraceDepth/` relative to the lane; `S` means `/fast/scratch/hyaku/chousa-r33/w1/CtlC1BraceDepth/`.

Read `corpus/evidence/round33/claims.md` first, then the frozen counter docstring. `timeout 15s sha256sum tools/research-gate.sh corpus/evidence/round33/c1-count.py` exited 0 and matched both frozen hashes:

- BASE gate: `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`.
- Frozen counter: `ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229`.

| Retained artifact | SHA-256 of scored bytes |
|---|---|
| `A/pristine-gate.sh` | `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` |
| `A/a-ignore-strings.sh` | `7cf0ae0dc0b1ce60ed15f6dcfb4a8f6b6f26e67e13619a6aebaee6e8ed857059` |
| `A/b-braces-only.sh` | `8c6a18472f34e79f94b0d4b682f731673f9af86d108eb8fa8ac147da33541ef5` |
| `A/c-bad-escape.sh` | `e53575b1c68d32459dfb8be560739a0a964f1ebb5e6e903051a64d581daf09f5` |

The archived mutant copies retain their scored bytes. The same-named scratch working files named in receipts have subsequently been restored; use the archived gates, not those restored working paths, to recover the mutants.

## Commands, bounds, and receipts

`S/run-control.py`, retained as `A/run-control.py`, invokes only the committed counter. Every invocation sets `C1_TMP`, `C2_TMP`, and `TMPDIR` to `S`; uses lane-root cwd; passes `--gate S/<control>.sh --seed <seed> --receipt A/<control>-<phase>-<seed>.json`; and captures the exact command, exit code, stdout, stderr, and gate hashes before/after in the corresponding `.run.json`. Mutated invocations also pass `--keep S/<control>-mutated-<seed>-fixture` for audit. The counter source was hash-checked before every two-seed batch. No counter was copied or edited.

These were the nine scoring batches, each with outer exit 0; detector exit 1 is recorded separately for each seed:

```sh
timeout 850s prlimit --as=1073741824 --nproc=2000 -- python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1BraceDepth/run-control.py a-ignore-strings pristine 33881 33882
timeout 850s prlimit --as=1073741824 --nproc=2000 -- python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1BraceDepth/run-control.py b-braces-only pristine 33883 33884
timeout 850s prlimit --as=1073741824 --nproc=2000 -- python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1BraceDepth/run-control.py c-bad-escape pristine 33885 33886
timeout 850s prlimit --as=1073741824 --nproc=2000 -- python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1BraceDepth/run-control.py a-ignore-strings mutated 33881 33882
timeout 850s prlimit --as=1073741824 --nproc=2000 -- python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1BraceDepth/run-control.py b-braces-only mutated 33883 33884
timeout 850s prlimit --as=1073741824 --nproc=2000 -- python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1BraceDepth/run-control.py c-bad-escape mutated 33885 33886
timeout 850s prlimit --as=1073741824 --nproc=2000 -- python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1BraceDepth/run-control.py a-ignore-strings restored 33881 33882
timeout 850s prlimit --as=1073741824 --nproc=2000 -- python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1BraceDepth/run-control.py b-braces-only restored 33883 33884
timeout 850s prlimit --as=1073741824 --nproc=2000 -- python3 /fast/scratch/hyaku/chousa-r33/w1/CtlC1BraceDepth/run-control.py c-bad-escape restored 33885 33886
```

The recorder bounds each counter subprocess to 400 s; the counter itself bounds the gate to 600 s (`c1-count.py:57,348-351`). All completed without reaching either bound. Memory/address space was capped at 1 GiB and process count at 2000. The same bounds and seed pair were used on pristine, mutated, and restored bytes.

Mutant receipts and exact per-class stdout:

- A: `A/a-ignore-strings-mutated-33881.json`, `A/a-ignore-strings-mutated-33882.json`; corresponding `.out` and `.run.json` files.
- B: `A/b-braces-only-mutated-33883.json`, `A/b-braces-only-mutated-33884.json`; corresponding `.out` and `.run.json` files.
- C: `A/c-bad-escape-mutated-33885.json`, `A/c-bad-escape-mutated-33886.json`; corresponding `.out` and `.run.json` files.
- Each also has `pristine` and `restored` receipts, `.out`, and `.run.json` under the same naming convention. Thus the before/mutated/restored sequence is independently recorded for every seed.

## Per-class output

The columns reproduce the stdout class counts. `BASE/restored` is identical on all twelve pristine/restored runs. Each mutant `.out` contains the literal `TOPLEVEL_FIELD_MATCH=...` line followed by these 15 class lines.

| Class | BASE/restored | A 33881 | A 33882 | B 33883 | B 33884 | C 33885 | C 33886 |
|---|---|---|---|---|---|---|---|
| N1_nested_line_decoy | 6/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| N2_nested_line_only | 0/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| N3_top_line_wrong_nested_right | 6/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| N4_nested_sha_decoy | 6/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| N5_nested_sha_only | 0/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| N6_top_sha_stale_nested_right | 6/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| N7_nested_source_decoy_sup | 3/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| N8_nested_source_decoy_uns | 3/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| N9_nested_id_decoy | 3/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| N10_nested_span_decoy | 3/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| N11_nested_marker_expect_decoy | 0/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| D1_duplicate_top_level | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 |
| S1_flat_confusers | 12/12 | 4/12 | 4/12 | 12/12 | 12/12 | 10/12 | 10/12 |
| S2_nested_confusers | 0/6 | 3/6 | 4/6 | 6/6 | 6/6 | 5/6 | 6/6 |
| F1_flat_plain | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| **TOPLEVEL_FIELD_MATCH** | **60/144** | **121/144** | **122/144** | **132/144** | **132/144** | **129/144** | **130/144** |

## Expected detector and observed failure mechanisms

### A — structure counted inside strings

Expected rejection: string confusers must expose delimiter counting inside JSON string values; duplicate first-wins must also fail D1.

Observed: S1 is 4/12 on both seeds; S2 is 3/6 then 4/6; D1 is 0/12. For example `A/a-ignore-strings-33881-claims.jsonl:7` contains `close } brace ] bracket` before the real top-level `line`. Receipt `A/a-ignore-strings-mutated-33881.json:51-55` records id `c4e4aa0f052`, truth `mislocated`, observed `supported`. The nested escaped-quote/brace confuser at `A/a-ignore-strings-33881-claims.jsonl:50` produces `invalid` instead of `supported` (`...33881.json:87-91`). Verdict: **MISSES**.

### B — object depth only, strings handled correctly

Expected rejection: all duplicate-read-field fixtures must be invalid, not first-wins. The deliberately omitted array-depth accounting is assessed separately from that duplicate policy.

Observed: every class except D1 is perfect on both seeds; D1 is 0/12. `A/b-braces-only-33883-claims.jsonl:6` duplicates `source` with the same value; receipt `A/b-braces-only-mutated-33883.json:33-38` records `cb3df6b0d76` as `supported`, truth `invalid`. Verdict: **MISSES**, entirely because of duplicate handling.

[INFERENCE] Ignoring array depth is not, by itself, shown to violate this valid-JSON-object member-reader contract: an object nested through an array still contributes an extra `{`, so its members are deeper in object depth. The counter's array fixtures use nested objects (`c1-count.py:129-138`). These results must not be described as killing an array-depth bug; only first-wins duplicates are rejected in this control.

### C — backslash parity ignored before a quote

Expected rejection: a JSON string ending in an escaped backslash must close normally; treating its closing quote as escaped loses subsequent field boundaries. The trailing-backslash confuser is explicitly fixture variant 3 (`c1-count.py:64-71`).

Observed: S1 is 10/12 on both seeds; S2 is 5/6 then 6/6; D1 is 0/12. `A/c-bad-escape-33885-claims.jsonl:7,8,60` contain the trailing-backslash confuser. Receipt `A/c-bad-escape-mutated-33885.json:39-49,69-74` records the two flat rows and one nested row as `none`, rather than their hidden truths. Verdict: **MISSES**.

### Coverage / repeatability limit, without changing the contract

Fixed fixture sub-variant counts do **not** produce fixed detected-miss counts for these controls: A's S2 changes 3/6 to 4/6; C's S2 changes 5/6 to 6/6. This limits the counter docstring's statement that mishandling a sub-variant misses it on every seed (`c1-count.py:24-26`). The receipts above record the actual variation; no counter repair was attempted.

[INFERENCE] Random member order can mask a field-reader defect when losing an optional correct `line` still yields the same `supported` verdict. S2 truth is always `supported` (`c1-count.py:87,263-268`), while BASE only enforces line binding when `line_present=1` (`A/pristine-gate.sh:1553-1578`). This explains why a passing S2 row does not certify correct parsing. The full controls still fail P1; there was no 144/144 survivor and no evidence here requiring the target to be weakened.

## Restoration and operational limits

For each control, before the restored scoring batch, ran the following with its control filename substituted:

```sh
timeout 15s cp "$S/pristine-gate.sh" "$S/<control>.sh" && timeout 15s cmp -s "$S/pristine-gate.sh" "$S/<control>.sh" && <restored scoring batch above>
```

The three `cp` and `cmp -s` operations exited 0 (the `&&`-guarded restored batches ran). All restored `.run.json` records contain both `gate_sha256_before` and `gate_sha256_after` equal to the original full BASE hash. Every restored detector output is 60/144, matching its corresponding pristine output and class counts. No exact-byte restoration was left pending.

Only the three helpers' scratch copies were mutated; retained control artifacts were copied before restoration. No git/jj write commands, lane production edits, network requests, installs, subagents, or unrelated verification were performed. Initial `timeout 15s df -h /fast` exited 0 (198 GiB available). Three long foreground tool calls were automatically represented by harness jobs `bg_2874`, `bg_2875`, `bg_2876`; all completion outputs were received before restoration, with outer exit 0. No detached processes were intentionally launched and no process signals were sent.

Artifact-size command (exit 0): `timeout 15s wc -c a-ignore-strings.sh b-braces-only.sh c-bad-escape.sh pristine-gate.sh a-ignore-strings-33881-claims.jsonl b-braces-only-33883-claims.jsonl c-bad-escape-33885-claims.jsonl c-bad-escape-33886-claims.jsonl run-control.py`, cwd `A`. Largest retained artifact is 337121 bytes; retained claim files are 39677–40091 bytes. Recorder-owned logs are explicitly bounded below 1 MiB. Complete generated fixtures remain only under the six named `S/*-mutated-*-fixture/` directories.

Tool limitation: the pristine batches requested a PTY but the tool reported it unavailable and ran without one; this was reported via `xd://report_issue`. The detector commands and recorded outputs above completed regardless. No build, gate selftest, candidate test, battery, integration, or admission judgment was part of this scoped probe.
