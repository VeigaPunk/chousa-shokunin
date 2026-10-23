# CtlC1DupPolicy — round 33 wave 1 duplicate-policy controls

Date: 2026-10-23. Axis under challenge: **operability** (C1 duplicate invalidation). Probe safeguards: frozen-detector integrity, isolation, and exact-byte restoration. This is a control experiment, not a candidate score or a lane admission judgment.

## Result

All four assigned controls **MISSES** on both fresh seeds and are **killed** by the frozen detector. None meets 144/144. Pristine and restored feasibility-oracle bytes score 144/144 on the same seed pairs for every control, so none of these mutation verdicts rests on a failing baseline.

Paths below use:
- `L=/home/vgpnk/Projects/shokunin/chousa-shokunin`
- `S=/fast/scratch/hyaku/chousa-r33/w1/CtlC1DupPolicy`
- `A=$L/.ufo/waves/round-33/w1/CtlC1DupPolicy`

## Construction and expected detector

Read `corpus/evidence/round33/claims.md` first, then the counter contract. C1 rejects duplicated top-level read fields even when their values agree (`claims.md:29-40`). The detector requires the correct per-id observation and exact line/revision finding membership (`c1-count.py:34-41,369-379`), not merely a nonzero gate exit.

The production base gate and scratch `base-gate.sh` have SHA-256 `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`. The frozen counter has SHA-256 `ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229`.

Created the strict feasibility reference using the supplied L1 builder, not a candidate implementation:

```sh
timeout 30 cp "$L/tools/research-gate.sh" "$S/base-gate.sh"
timeout 30 python3 "$L/.ufo/waves/round-33/controls/L1-design/mk-oracle.py" "$S/base-gate.sh" "$S/strict-oracle.sh"
```

Both commands exited 0. The supplied builder SHA-256 is `3731596f4cc9a053f7bc8274494b81d00eceaad8a8889de92621eb8acd130264`. Its top-level readers and duplicate check are at `.ufo/waves/round-33/controls/L1-design/mk-oracle.py:7-40`.

Four scratch copies began as exact `strict-oracle.sh` bytes. After pristine scoring, only the duplicate-policy points were changed:

- **A — last-wins:** retain default `json.loads` string/presence readers; make `json_dup_read_key` return 1 (`A/a-last-wins.sh:1113,1119-1121`).
- **B — first-wins:** use `object_pairs_hook=lambda p: dict(reversed(p))` in both readers and make duplicate rejection return 1 (`A/b-first-wins.sh:1113,1119-1121,1128`).
- **C — differing-values only:** retain the top-level pairs and reject a duplicated read key only if two values differ (`A/c-differ-only.sh:1119-1126`). Other reads remain default last-wins.
- **D — line only:** narrow the duplicate-check set to `R={"line"}` (`A/d-line-only.sh:1119-1126`). Other reads remain default last-wins.

The `A/...` references above denote retained control artifacts under the artifact directory, not lane production paths. Their hashes match the scratch bytes scored below. The expected detector is `TOPLEVEL_FIELD_MATCH<144/144`, exit 1, with losses confined to `D1_duplicate_top_level`; the other 132 records exercise the unchanged, correct top-level reading.

## Commands and receipts

All detector subprocesses ran with cwd `L` and `C1_TMP=C2_TMP=TMPDIR=S`. A foreground bounded batch awaited at most four subprocesses at once; no background jobs or subagents were dispatched. Every detector command used this exact bound/resource prefix:

```sh
timeout --kill-after=5s 660s prlimit --nproc=2000 --as=2147483648 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count.py --gate /fast/scratch/hyaku/chousa-r33/w1/CtlC1DupPolicy/a-last-wins.sh --seed 72487941887875 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/CtlC1DupPolicy/a-last-wins-mutated-72487941887875.json
```

That command exited 1 and printed `TOPLEVEL_FIELD_MATCH=132/144`. The exact commands, environment, exit codes, elapsed times, stdout and stderr for all runs are retained in:
- `A/pristine-command-output.json`
- `A/mutated-command-output.json`
- `A/restored-command-output.json`

For each row and each seed below there are three frozen receipts: `A/<control>-pristine-<seed>.json`, `A/<control>-mutated-<seed>.json`, and `A/<control>-restored-<seed>.json`. Thus the experiment contains 24 receipts (4 controls × 2 seeds × 3 phases), enumerated by the command-output files and `A/seed-plan.json`.

| Control | Fresh seeds | Pristine counts / exits | Mutated counts / exits | Restored counts / exits | Verdict |
|---|---|---|---|---|---|
| `a-last-wins` | 72487941887875; 275687207013566 | 144/144; 144/144 — 0; 0 | 132/144; 132/144 — 1; 1 | 144/144; 144/144 — 0; 0 | **MISSES; killed** |
| `b-first-wins` | 237399751422001; 134800489541589 | 144/144; 144/144 — 0; 0 | 132/144; 132/144 — 1; 1 | 144/144; 144/144 — 0; 0 | **MISSES; killed** |
| `c-differ-only` | 123586801970670; 90427433215607 | 144/144; 144/144 — 0; 0 | 138/144; 138/144 — 1; 1 | 144/144; 144/144 — 0; 0 | **MISSES; killed** |
| `d-line-only` | 159720566953931; 174250632886859 | 144/144; 144/144 — 0; 0 | 136/144; 136/144 — 1; 1 | 144/144; 144/144 — 0; 0 | **MISSES; killed** |

All eight mutated receipts record the frozen counter hash above, `gate_rc=1`, `gate_timed_out=false`, and `predicate_holds=false`. The `misses` arrays contain only `D1_duplicate_top_level` entries. Standard error was empty in the saved detector command outputs.

## Per-class output

These are the actual per-class counts; both seeds give the same vector for each control. Complete verbatim lines for every invocation are in the three command-output artifacts. Every pristine/restored invocation matches the class denominator in every row.

| Counter class | A last-wins | B first-wins | C differing only | D line only |
|---|---:|---:|---:|---:|
| `N1_nested_line_decoy` | 12/12 | 12/12 | 12/12 | 12/12 |
| `N2_nested_line_only` | 12/12 | 12/12 | 12/12 | 12/12 |
| `N3_top_line_wrong_nested_right` | 12/12 | 12/12 | 12/12 | 12/12 |
| `N4_nested_sha_decoy` | 12/12 | 12/12 | 12/12 | 12/12 |
| `N5_nested_sha_only` | 12/12 | 12/12 | 12/12 | 12/12 |
| `N6_top_sha_stale_nested_right` | 12/12 | 12/12 | 12/12 | 12/12 |
| `N7_nested_source_decoy_sup` | 6/6 | 6/6 | 6/6 | 6/6 |
| `N8_nested_source_decoy_uns` | 6/6 | 6/6 | 6/6 | 6/6 |
| `N9_nested_id_decoy` | 6/6 | 6/6 | 6/6 | 6/6 |
| `N10_nested_span_decoy` | 6/6 | 6/6 | 6/6 | 6/6 |
| `N11_nested_marker_expect_decoy` | 6/6 | 6/6 | 6/6 | 6/6 |
| `D1_duplicate_top_level` | **0/12** | **0/12** | **6/12** | **4/12** |
| `S1_flat_confusers` | 12/12 | 12/12 | 12/12 | 12/12 |
| `S2_nested_confusers` | 6/6 | 6/6 | 6/6 | 6/6 |
| `F1_flat_plain` | 12/12 | 12/12 | 12/12 | 12/12 |
| **TOPLEVEL_FIELD_MATCH** | **132/144** | **132/144** | **138/144** | **136/144** |

D1 explicitly constructs `(line, sha256, source) × (same, diff) × 2` (`c1-count.py:85,233-253`). A and B miss all twelve duplicates. C fails to reject the six equal-value duplicates; its six missed observations are all `supported`, not `invalid`. D rejects the four line duplicates but misses the eight source/sha256 duplicates. These losses follow the retained control predicates and the fixed D1 construction; the receipt miss arrays supply the concrete ids and observations.

No assigned control escaped the counter. In particular, agreement of duplicate values is not an escape hatch for C: D1 contains equal-value duplicates whose hidden truth remains `invalid`.

## Hashes and restoration evidence

Every initialized/pristine scratch control, the retained strict oracle, and every restored scratch control has SHA-256:

`930a20755418eed3277a893c5b8a96bffd93f2ea90a79fd79bc122426e5677a9`

This is the exact before/after-restoration reference, distinct from the untouched base gate. The mutated artifacts are intentionally retained as requested:

| Retained artifact | Mutated SHA-256 | Bytes |
|---|---|---:|
| `A/a-last-wins.sh` | `51f9d0d2d8546ad21e9e2fdb8c9ee3478b7dfc2f2efbbb69dae620eda085731b` | 336671 |
| `A/b-first-wins.sh` | `06ad8ac4b8d61022d0ae30c13791d184dd9a5e39e4bf43e65cc4d7bc9c91a4c4` | 336747 |
| `A/c-differ-only.sh` | `a221832295678646d50604b8e1961f40eb20b7ef9d070ebd26932ba68e25117a` | 336968 |
| `A/d-line-only.sh` | `9531d520269770e3110a1bc1b1a0806b48c89739a7db5870c91d0b1da92bf7a0` | 336867 |

`A/mutant-hashes.txt` records the `timeout 30 sha256sum ...` command, exit 0, and matching scratch/artifact digests. The mutated phase was enclosed in a `finally` restoration: four `timeout 30 cp "$S/strict-oracle.sh" "$S/<control>.sh"` commands all exited 0 (`A/restoration-commands.json`). The subsequent same-seed detector reruns all returned 144/144. `A/restored-hashes.txt` records the final `timeout 30 sha256sum ...`, exit 0: all four scratch controls exactly match the pristine hash, scratch `base-gate.sh` and production gate still match the base hash, and the production counter still matches its frozen hash. Scratch gate paths in old mutated receipts now contain restored bytes; the correspondingly named retained artifacts contain the scored mutant bytes.

`timeout 30 df -h /fast` exited 0 before copying (198G available). `timeout 30 stat --printf='%s %n\n' "$A"/*` exited 0; the largest retained artifact was 336968 bytes, below 1 MiB. No unbounded fixture/log writes were used.

## Limits and scope

Only these four duplicate-policy controls were scored; no candidate C1 implementation, no lane no-harm battery, no other runtime, and no network were invoked. The production gate, corpus, index and jj state were not edited. No tools were installed or updated, and no processes were signalled by name or pattern.

D1 exercises duplicated `line`, `sha256`, and `source`, not duplicated `id`, `span`, `expect`, or `marker` (`c1-count.py:85`). These kills therefore demonstrate detection of the assigned policies, not exhaustive coverage of every contract member. The frozen counter was never edited. No surviving-control finding arose from this assignment.
