# C1 boundary-blind negative controls — round 34, wave 1

Access date: 2026-10-23. Seat: ChousaR34.CtlC1BoundaryBlind.

## Scope and axes

Axis challenged: **operability**. Token boundaries, adjacency and line binding are held contract requirements, not new coverage claims (`corpus/evidence/round34/claims.md:34-43`). This seat scored only three deliberately defective CONTROL copies of the base gate; no ExecC1Build candidate, production file, counter, Git index or jj state was modified. No network, installs, subagents or unrelated checks were used.

Read frozen `claims.md` first, then the counter docstring. The counter remained SHA-256 `5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565`. The pristine gate snapshot was SHA-256 `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`, matching `claims.md:3-7`. Both hashes were obtained with `timeout 30 sha256sum <scratch>/base.sh corpus/evidence/round34/c1-count.py` (exit 0).

Paths below use these exact prefixes:

- `A` = `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-34/w1/CtlC1BoundaryBlind`
- `S` = `/fast/scratch/hyaku/chousa-r34/w1/CtlC1BoundaryBlind`
- `L` = `/home/vgpnk/Projects/shokunin/chousa-shokunin`

`timeout 15 df -h /fast` exited 0 before fixtures were created: 88G available, 90% used. All commands ran from `L`. Each archived gate is below 1 MiB: `timeout 15 wc -c A/ignore-both.sh A/left-only.sh A/right-only.sh` reported 358684, 358746 and 358782 bytes (exit 0).

## Mutants and expected detector

All three controls add an exact byte-substring search for spans of at least 32768 bytes: haystack and span travel over stdin, separated by NUL; Python `bytes.find` enumerates adjacent occurrences, including overlaps. Short-span code remains on the unchanged base path. Only a raw-offset helper and long branches in `tok_span_at` / `tok_span_all` were added. Each control deliberately enumerates **all raw occurrences** for line binding.

| Control | Defect in long `tok_span_at` | Expected detector | Mutant SHA-256 |
|---|---|---|---|
| ignore-both | Neither boundary checked | Both glued classes fail; 26/30 | `6d6863e72c70f2da8d2a8554e7c49cba03b098d33836d939c525889328550117` |
| left-only | Calls `tok_left_ok` only | Glued-right fails; 28/30 | `af8b79f2b6a83da104a4bb9ee50104278ce189580686fbf399898a6b4066bfa4` |
| right-only | Calls `tok_right_ok` only | Glued-left fails; 28/30 | `ad7b0cc479ee2dee6b5ef44425d0359aa394b95273e0490ae8a13387a5635398` |

The expected detector follows the generated glued cases (`corpus/evidence/round34/c1-count.py:182-187`) and scoring (`:282-305`). Archived scored bytes are `A/ignore-both.sh`, `A/left-only.sh`, `A/right-only.sh`; their hashes above were printed by `timeout 15 sha256sum` (exit 0). Expectations were recorded before scoring in `A/probe-spec.json`.

## Commands, outputs and receipts

The exact detector argv, cwd, PID/PGID, return code, elapsed time and unmodified stdout/stderr are in every `A/run-<label>-s<seed>.json`. `A/run-counter.py` is the bounded supervisor, not a modified counter. The inner command is:

```sh
timeout --signal=TERM --kill-after=10s 1700s \
  prlimit --as=2147483648 --nproc=65536 --fsize=16777216 \
  env C1_TMP="$S" TMPDIR="$S" \
  python3 "$L/corpus/evidence/round34/c1-count.py" \
  --gate "$GATE" --seed "$SEED" --receipt "$A/$LABEL-s$SEED.json"
```

The supervisor was itself bounded by `timeout --signal=TERM --kill-after=10s 1740s python3 A/run-counter.py --label LABEL --gate GATE --seed SEED`. At most four counters ran concurrently. Two tool launches hit the host's 100-background-job cap; their supervisors were instead launched directly by Python eval, recording their PIDs. No extra counter was started by the rejected launches.

| Label | Seed | Gate under S | Frozen receipt under A | Counter rc | Gate rc | Elapsed seconds (counter receipt) | Verdict |
|---|---:|---|---|---:|---:|---:|---|
| pristine | 84931023 | base.sh | pristine-s84931023.json | 1 | 1 | 1007.416 | 19/30; baseline fails |
| ignore-both | 84931023 | ignore-both.sh | ignore-both-s84931023.json | 1 | 1 | 759.574 | **MISSES**, 26/30 |
| ignore-both | 84931071 | ignore-both-seed2.sh | ignore-both-s84931071.json | 1 | 1 | 1165.628 | **MISSES**, 26/30 |
| left-only | 84931023 | left-only.sh | left-only-s84931023.json | 1 | 1 | 747.910 | **MISSES**, 28/30 |
| left-only | 84931071 | left-only.sh | left-only-s84931071.json | 1 | 1 | 1165.565 | **MISSES**, 28/30 |
| right-only | 84931023 | right-only.sh | right-only-s84931023.json | 1 | 1 | 739.763 | **MISSES**, 28/30 |
| right-only | 84931071 | right-only.sh | right-only-s84931071.json | 1 | 1 | 1121.025 | **MISSES**, 28/30 |

Each receipt's lines 3-15 bind the counter and gate hashes, seed, gate rc and count. Each mutant receipt's lines 16-30 give the per-class counts; lines 31 onward identify the actual false supports. All six mutated runs report `gate_timed_out=false`, empty gate stderr and `predicate_holds=false`. These are genuine class failures, not harness-wide `none` outcomes.

### ignore-both — identical stdout on both seeds

```text
LONGSPAN_MATCH=26/30
  long-verbatim-ml 3/3
  long-verbatim-1l 2/2
  long-edge 2/2
  long-mut-head 2/2
  long-mut-tail 2/2
  long-mut-mid 3/3
  long-split 2/2
  long-glued-left 0/2
  long-glued-right 0/2
  long-line-bound 2/2
  long-line-wrong 2/2
  short-verbatim 3/3
  short-mut 3/3
```

### left-only — identical stdout on both seeds

```text
LONGSPAN_MATCH=28/30
  long-verbatim-ml 3/3
  long-verbatim-1l 2/2
  long-edge 2/2
  long-mut-head 2/2
  long-mut-tail 2/2
  long-mut-mid 3/3
  long-split 2/2
  long-glued-left 2/2
  long-glued-right 0/2
  long-line-bound 2/2
  long-line-wrong 2/2
  short-verbatim 3/3
  short-mut 3/3
```

### right-only — identical stdout on both seeds

```text
LONGSPAN_MATCH=28/30
  long-verbatim-ml 3/3
  long-verbatim-1l 2/2
  long-edge 2/2
  long-mut-head 2/2
  long-mut-tail 2/2
  long-mut-mid 3/3
  long-split 2/2
  long-glued-left 0/2
  long-glued-right 2/2
  long-line-bound 2/2
  long-line-wrong 2/2
  short-verbatim 3/3
  short-mut 3/3
```

## Findings and attribution limits

**No assigned control MEETS-TARGET.** Both seeds expose precisely the omitted boundary: glued claims incorrectly become `observed=supported` instead of `unsupported` (each mutated receipt's `misses`). Full adjacency is retained: every split and one-byte-mutation class matches.

**[INFERENCE] Raw-occurrence line binding is not independently distinguished by these fixtures.** All controls pass both line classes on both seeds despite their intentionally unfiltered `tok_span_all`. The generator places two delimited occurrences in both line classes (`corpus/evidence/round34/c1-count.py:188-199`); neither names a glued occurrence while a separate valid occurrence exists. Thus these results support rejection of the boundary-blind *whole controls*, not coverage of that independent line-binding distinction. No extra control was scored and the counter was not patched.

For the mutation-tester killed/survived taxonomy the verdict is **INCONCLUSIVE, not killed**: the shared pristine detector already fails at 19/30 (`A/pristine-s84931023.json:13-15`). It misses all seven long supported records and all four line records, while short classes match (`:16-30`). Its stderr receipt records `/usr/bin/grep: Argument list too long` (`:11`; accessed 2026-10-23). The negative-control verdicts above remain **MISSES** under the separately requested frozen 30/30 predicate.

An initial pristine launch with `--nproc=2000` exited 1 before starting the gate: `BlockingIOError: [Errno 11] Resource temporarily unavailable`. This is an inconclusive harness failure, not a detector result. Exact command and evidence: `A/initial-launch-failure.txt`. Subsequent commands used the explicit 65536 process cap plus the unchanged 2-GiB memory and 16-MiB file caps; they completed as listed above.

## Exact restoration and restored-byte detector

All operational scratch control paths were restored with `timeout 30 cp -- S/base.sh S/<file>` (exit 0). `timeout 15 sha256sum S/base.sh S/ignore-both.sh S/left-only.sh S/right-only.sh S/ignore-both-seed2.sh` exited 0 and printed the same exact base digest for **all five**:

```text
43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346
```

The first ignore-both path was restored after its first run; its second run used a separate scratch copy of the same mutant bytes. That second copy and both one-sided controls were restored after their final runs. `A/restoration.json` records every before/after hash. Archived mutants under A intentionally retain the scored bytes for reproduction; `A/base.sh` preserves the pristine snapshot.

The same frozen detector was also run on the restored `S/ignore-both.sh`, seed 84931023. To close within the seat time box, only its recorded detector process group **3543208** was sent SIGTERM after 1110.842 seconds. Actual result: counter rc **-15**, outer supervisor exit **241**, stdout/stderr empty, **no LONGSPAN_MATCH and no frozen receipt**. Evidence: `A/run-restored-s84931023.json:18-32`. This restored behavioral run is **inconclusive**; no restored count or behavioral equivalence is claimed. Exact-byte restoration is established separately by the hashes. All launched supervisors were collected; the only remaining active detector group was terminated by its recorded PGID, not by a process-name search.

This report is limited to the assigned negative controls. It neither judges a candidate nor claims the lane milestone is complete. No builds, selftests, linters, production repairs or other runtime were invoked.
