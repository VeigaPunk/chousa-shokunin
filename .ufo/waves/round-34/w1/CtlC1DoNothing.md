# Round 34 W1 — C1 do-nothing control

Date/access date: 2026-10-23. Seat: ChousaR34.CtlC1DoNothing.
Axes: operability; detector discrimination; byte/process isolation.

## Verdict

**MISSES: the unchanged base gate scored `LONGSPAN_MATCH=19/30` on all three fresh seeds.** Every receipt has `predicate_holds=false`, gate exit 1, and no timeout. The requested 18/30 ceiling is **refuted**: 13 long unsupported records plus all 6 short records give 19. The frozen design already corrects the earlier 18 to 19 (`corpus/evidence/round34/claims.md:65-71`); the counter's class counts agree (`corpus/evidence/round34/c1-count.py:36-49`). No do-nothing control passed 30/30.

Mutation-kill verdict: **INCONCLUSIVE as a kill test**, not a killed mutant. This assignment explicitly requested an unmodified base control; no defect was introduced, and the pristine baseline already fails C1. These are baseline-control receipts, not candidate or repair scores.

## Control and byte identity

Read the frozen claims first, then the counter docstring. Copied only the base gate, using these commands (both exit 0):

```sh
timeout 30s cp -p /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /fast/scratch/hyaku/chousa-r34/w1/CtlC1DoNothing/base-gate.sh
timeout 30s cp -p /fast/scratch/hyaku/chousa-r34/w1/CtlC1DoNothing/base-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-34/w1/CtlC1DoNothing/base-gate.sh
```

Gate SHA-256 **before and after all runs**, identical for production source, scratch control, and retained control copy:

```text
43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346
```

Frozen counter SHA-256 **before and after**:

```text
5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565
```

Recorded with bounded `sha256sum` commands. Post-run exact-byte comparisons also both exited 0:

```sh
timeout 30s cmp -s tools/research-gate.sh /fast/scratch/hyaku/chousa-r34/w1/CtlC1DoNothing/base-gate.sh
timeout 30s cmp -s tools/research-gate.sh .ufo/waves/round-34/w1/CtlC1DoNothing/base-gate.sh
```

No bytes required restoration: the control remained pristine throughout. The retained gate is 357537 bytes, below 1 MiB. No candidate implementation was scored.

## Three completed detector runs

All paths in the following table are relative to `.ufo/waves/round-34/w1/CtlC1DoNothing/`. Exact commands, captured counter stdout/stderr, PIDs and exit codes are preserved in `run-evidence.json`. All three ran concurrently, with fresh randomly selected seeds outside 3401–3409.

| Seed | PID/PGID | Counter exit | Gate exit | Gate timed out | Receipt elapsed seconds | Output | Receipt |
| --- | ---: | ---: | ---: | --- | ---: | --- | --- |
| 2093244058 | 1557066 | 1 | 1 | false | 983.690 | LONGSPAN_MATCH=19/30 | base-s2093244058.json |
| 2718675710 | 1557067 | 1 | 1 | false | 1130.908 | LONGSPAN_MATCH=19/30 | base-s2718675710.json |
| 3025057612 | 1557070 | 1 | 1 | false | 1042.773 | LONGSPAN_MATCH=19/30 | base-s3025057612.json |

Receipt evidence: each file's lines 3–15 bind the frozen counter, base gate, seed, elapsed time, exit status, stderr tail and predicate; lines 16–30 give class counts; lines 31–98 give individual misses.

Actual first completed command, cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`:

```sh
C1_TMP=/fast/scratch/hyaku/chousa-r34/w1/CtlC1DoNothing TMPDIR=/fast/scratch/hyaku/chousa-r34/w1/CtlC1DoNothing timeout --signal=TERM --kill-after=10s 1650s prlimit --nproc=65536 --as=2147483648 --fsize=16777216 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round34/c1-count.py --gate /fast/scratch/hyaku/chousa-r34/w1/CtlC1DoNothing/base-gate.sh --seed 2093244058 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-34/w1/CtlC1DoNothing/base-s2093244058.json
```

The other two commands differ only in seed and matching receipt filename; their full literal command lines are in `run-evidence.json`. The counter's internal gate timeout remained the frozen 1500 seconds (`c1-count.py:73,275-277`). Outer bounds were 1650 seconds plus a 10-second kill grace, 2 GiB address space per process, 65536 processes per UID, and 16 MiB per written file. Only three counter runs were active at once.

Actual stdout below was identical on all three completed runs; counter stderr was empty:

```text
LONGSPAN_MATCH=19/30
  long-verbatim-ml 0/3
  long-verbatim-1l 0/2
  long-edge 0/2
  long-mut-head 2/2
  long-mut-tail 2/2
  long-mut-mid 3/3
  long-split 2/2
  long-glued-left 2/2
  long-glued-right 2/2
  long-line-bound 0/2
  long-line-wrong 0/2
  short-verbatim 3/3
  short-mut 3/3
```

## Every missing class

All eleven misses in each receipt have `observed=unsupported`. The five missing classes are below; example IDs and line ranges refer to `CtlC1DoNothing/base-s2093244058.json` beside this report.

| Missing class | Misses per seed | Truth | Observed | Example ID and receipt lines |
| --- | ---: | --- | --- | --- |
| long-verbatim-ml | 3 | supported | unsupported | cdf2fc94fd8, 44–48 |
| long-verbatim-1l | 2 | supported | unsupported | c3415b2daba, 38–42 |
| long-edge | 2 | supported | unsupported | cb4067442e0, 50–54 |
| long-line-bound | 2 | supported | unsupported | cdad68208dc, 32–36 |
| long-line-wrong | 2 | mislocated | unsupported | c2551a04d4f, 68–72 |

For **each of those classes**, the shared run-level stderr symptom is `/usr/bin/grep: Argument list too long` (located quote: each receipt `:11`, accessed 2026-10-23). The actual diagnostic names `base-gate.sh: line 1553`. The first receipt's complete 2000-character tail was opened; all three receipts preserve repeated instances of the same diagnostic. The stderr tail has no claim IDs, so it is not an independently captured per-record error trace.

The unchanged behavior explains the misses:

- `tok_span_at` constructs four pattern bytes per span byte and passes the entire pattern as one grep argument (`tools/research-gate.sh:1553-1579`). This affects multi-line, single-line and near-threshold verbatim classes alike; at 32768 span bytes the pattern alone is 131072 bytes before its terminating NUL.
- [INFERENCE from source plus receipts] Failed grep execution supplies no occurrences; `tok_span_at` returns 1, and `verify_claims` takes its not-found branch, setting `observed=unsupported` and emitting `CLAIM_SPAN_NOT_FOUND` (`research-gate.sh:1803-1806,1854-1874`). The receipts directly preserve the unsupported verdict, not the full finding stdout.
- [INFERENCE from source plus receipts] Both line classes fail the initial `tok_span_at`, so the later line-binding enumeration is not reached (`research-gate.sh:1811-1827`). Consequently the valid line-bound records never become supported, and the wrong-line records never reach the mislocated/`CLAIM_LINE_MISMATCH` branch (`:1850-1852`).

The 19 matching records are the 13 long negatives (2 head mutations + 2 tail + 3 middle + 2 split + 2 left-glued + 2 right-glued) and all 6 short records. The long negatives match their truth despite the broken long-span search; their matching count is not evidence that those long cases were actually searched successfully. The 9 long supported records and 2 long mislocated records account for the 11 misses. Three seeds reproduce the corrected design-v1 ceiling without altering the counter or contract.

## Initial harness failures, not scores

Before the completed runs, three simultaneous attempts used `--nproc=2000` with seeds 3789900215, 3425570118 and 3684575081 (PIDs/PGIDs 1462348, 1462351 and 1462353). Each counter exited 1 before launching the gate, printed no LONGSPAN_MATCH line and produced no receipt. Actual traceback ended with `BlockingIOError: [Errno 11] Resource temporarily unavailable` (located quote: `CtlC1DoNothing/aborted-attempts.json`, captured stderr, accessed 2026-10-23). Full literal commands, captured tracebacks, PIDs and exits are preserved in that artifact. These attempts are **inconclusive harness failures**, never counted as killed mutants or baseline C1 misses.

The current inherited NPROC soft/hard limit was 122865 (`timeout 30s prlimit --nproc`, exit 0). [INFERENCE] The initial 2000 per-UID cap was unsuitable for the shared host: increasing it to 65536 while retaining the memory/time/file caps allowed all three subsequent fresh-seed runs to complete. No counter or gate edits were made to handle this. Auxiliary diagnostics: querying PID 1's NPROC failed with permission denied (exit 1); `ps -L` was unsupported, so no process-count result is claimed.

## Artifact binding, cleanup and limits

Receipt SHA-256 values, obtained with bounded `sha256sum` (exit 0):

```text
a958523ccbfc745fc4fc56e2445d3a2ac280e97240b42527767f05e095dd9429  base-s2093244058.json
7715e56427d2097bab08e6e3319b4480fc2adfdc8cc48ed717148db71ab86528  base-s2718675710.json
a52654a737176141f65d247f15a80e32344210e054f586b63273573fef8135a0  base-s3025057612.json
```

All extra retained artifacts are in `.ufo/waves/round-34/w1/CtlC1DoNothing/`: the unchanged gate, three receipts, `run-evidence.json` (4300 bytes), and `aborted-attempts.json` (7401 bytes). Receipt sizes are 4207, 4209 and 4209 bytes respectively; all artifacts are below 1 MiB. Experiments used only `/fast/scratch/hyaku/chousa-r34/w1/CtlC1DoNothing/`; the frozen counter removed its temporary fixtures normally. Initial `timeout 30s df -h /fast` exited 0 and reported 88 GiB available.

All six launched processes were awaited. Numeric process-group existence probes found all six recorded groups absent; `run-evidence.json` records those results. No termination signal was needed, and no owned run remains. No subagents, network access, installations, git/jj writes, production-file edits or candidate tests were performed. Only the assigned base-gate control was scored. Full gate stdout was not separately retained by the frozen counter; the report distinguishes receipt observations from source-based inference.
