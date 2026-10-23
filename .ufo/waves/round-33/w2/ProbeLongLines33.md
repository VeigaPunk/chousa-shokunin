# ProbeLongLines33 — operability cost of the landed C1 reader on long flat records (round 33, wave 2 = falsify)

Seat: executor, sole labrat = none. Scratch: `/fast/scratch/hyaku/chousa-r33/w2/ProbeLongLines33/`
(`bench/` holds the driver, fixtures, gate copies, raw logs). No lane file was written; the lane
`tools/`, `corpus/`, `SCORECARD.md`, `LOG.md` and jj/git state were only read. No install, no
network, no process signalled by name. One harness backgrounding occurred (`bg_4341`, the
two-record 64 KiB-span cell); it finished and its numbers are reported below.

Gates (pinned copies in this directory, hashed before and after use):
`gate-base.sh` = `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`
(`git show 2b9cc73aed30c2e2c95699db6617d9531ef49fb2:tools/research-gate.sh`);
`gate-landed.sh` = `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`
(`git checkout 0fb300b5c27900ab8bb3abeb5f54776d71e04beb`). Both are the committed blobs, not the
live working tree (see F2).

Environment: bash 5.3.20(1), Linux 7.2.11-arch1-1 x86_64, 32 vCPU, shared host (`loadavg` above 1
throughout), python3.14; locales `C` (ANSI_X3.4-1968) and `en_US.UTF-8` both present; every
fixture is ASCII. Each gate run: `timeout 300 bash <gate> verify-claims <claims.jsonl>` with
`CHOUSA_ROOT` at the fixture directory, `C1_TMP`/`C2_TMP`/`TMPDIR` in scratch; stdout and stderr
redirected to files. Wall = `time.monotonic` around `subprocess.run`; CPU = `resource.getrusage
(RUSAGE_CHILDREN)` delta (user+sys, gate and its children). 3 reps at 512 B, 2 at 4 KiB, 1 at
16/64 KiB; min per cell reported. 36 matrix runs + 6 probe runs + 2 two-record runs, none
timed out.

## Fixtures (flat: no nested object or array anywhere)

`gen.py` builds, under one directory per case (`spans/src.txt` + `claims.jsonl`):

| case | record line | line 1 bytes | source | verdict |
|---|---|---|---|---|
| `span512` | span = 512 B of space-separated `w` tokens, unique `L512` head | 582 | 1 span line | supported/match |
| `span4096` | span = 4,096 B | 4,167 | 1 span line | supported/match |
| `span16384` | span = 16,384 B | 16,456 | 1 span line | supported/match |
| `span65536` | span = 65,536 B | 65,608 | 1 span line | **unsupported/mismatch** (F1) |
| `pad65536` | 21-B span + 65,3xx B in a **non-read** member `note` | 65,630 | `heading`/span | supported/match |
| `many200` | 200 records, first line 995 B, total 199,000 B, 200-line source | 995 | 200 span lines | 200/200 match |

`pad65536` isolates the reader: the long bytes are in a member `json_str`/`claim_scan` never read,
so base pays nothing for them.

## Results — verify-claims, min of reps, CPU (s) and wall (s)

| case | locale | base CPU | landed CPU | **CPU ratio** | base wall | landed wall | wall ratio | rc |
|---|---|---|---|---|---|---|---|---|
| span512 | C | 0.044 | 0.050 | **1.13×** | 0.043 | 0.049 | 1.13× | 0 |
| span512 | en_US.UTF-8 | 0.046 | 0.051 | **1.11×** | 0.046 | 0.049 | 1.07× | 0 |
| span4096 | C | 0.117 | 0.168 | **1.43×** | 0.118 | 0.170 | 1.45× | 0 |
| span4096 | en_US.UTF-8 | 0.186 | 0.232 | **1.25×** | 0.191 | 0.234 | 1.22× | 0 |
| span16384 | C | 0.811 | 1.291 | **1.59×** | 0.817 | 1.311 | 1.61× | 0 |
| span16384 | en_US.UTF-8 | 1.871 | 2.373 | **1.27×** | 1.890 | 2.394 | 1.27× | 0 |
| span65536 | C | 11.416 | 18.295 | **1.60×** | 11.676 | 20.418 | 1.75× | 1 |
| span65536 | en_US.UTF-8 | 30.977 | 36.224 | **1.17×** | 33.376 | 37.330 | 1.12× | 1 |
| **pad65536** | **C** | **0.074** | **4.743** | **64.4×** | 0.077 | 4.768 | **62.2×** | 0 |
| **pad65536** | **en_US.UTF-8** | **0.597** | **5.186** | **8.7×** | 0.602 | 5.220 | **8.7×** | 0 |
| many200 | C | 8.299 | 11.155 | **1.34×** | 7.614 | 10.676 | 1.40× | 0 |
| many200 | en_US.UTF-8 | 10.733 | 13.893 | **1.29×** | 10.875 | 19.387 | 1.78× | 0 |

Raw rows: `results.jsonl` (36 lines; each row carries the gate path, exit, wall, CPU, the first
`CLAIM` line and the `RESEARCH_GATE:` roll); console log `run_matrix.log`; per-run stdout/stderr
under `bench/out/` in scratch (paths in `results.jsonl`).

**60 s question (one record per file, as specified):** no matrix run exceeded 60 s. Slowest:
span65536 UTF-8 landed 37.330 s wall / 36.224 s CPU; base 33.376 wall. No run hit `timeout 300`;
no `timeout` exit. The bar *is* crossed as soon as one file holds two 64 KiB-span records
(`results-span65536x2.jsonl`, `gate` hashes as above, `timeout 300` not fired):

| case | locale | base wall / CPU | landed wall / CPU | output |
|---|---|---|---|---|
| span65536×2 — two 64 KiB spans, one file, 131,218 B | en_US.UTF-8 | **60.751 s / 59.641 s** | **65.313 s / 64.878 s** | both records `observed=unsupported`, `VERDICT_BEARING_CLAIMS=0/2`, `RESEARCH_GATE: DRIFT`, rc=1; one `/usr/bin/grep: Argument list too long` per record (F1) |

So: landed/base on that file is 1.07× in wall, 1.09× in CPU — the 60-s exposure there is F1's
pattern build and value decode, which base already pays (60.8 s); the landed change moves a
borderline file over the bar rather than creating the crossing.

## F1 — spans at or above ~32.7 KiB are never located, on **both** gates (pre-existing, not a C1 regression)

At the 64 KiB span, both gates write to stderr (once per record)

- base: `gate-base.sh: line 1354: /usr/bin/grep: Argument list too long`
- landed: `gate-landed.sh: line 1504: /usr/bin/grep: Argument list too long`

then emit `CLAIM id=L65536 expected=supported observed=unsupported source=spans/src.txt at=-
verdict=mismatch`, `VERDICT_BEARING_CLAIMS=0/1`, `RESEARCH_GATE: DRIFT`, rc=1. Cause: `tok_span_at`
hex-escapes every span byte (4 chars per byte, `landed:1504`/`base:1354`) and passes the pattern as
**one argv string** to `grep -P`; 65,536 B → 262,144 B pattern > `MAX_ARG_STRLEN` (131,072).
Measured ceiling with the same construction, grep only, no gate:

| span chars | pattern bytes | grep rc | result |
|---|---|---|---|
| 32,700 | 130,796 | 0 | found (offset 0) |
| 32,766 | 131,060 | 2 | `grep: regular expression is too large` |
| 33,000 | 132,000 | — | `OSError: [Errno 7] Argument list too long` (grep never started) |

So `verify-claims` cannot verify any claim whose span is longer than ~32.7 KiB, whatever the
reader does; it costs 11.4 s (C) / 31.0 s (UTF-8) at base and 18.3 / 36.2 s landed to say
`mismatch` for one such record, and 60.8 / 65.3 s wall for a two-record file. The C1 counter's
fixture is 159–412 B per record, so no class can see this; the C1 contract bounds neither span nor
line length. Recorded as a pre-existing operability limit the landed change inherits, not as a
falsification of C1's field reading.

## F2 — counter receipts from the default `--gate` resolve to the live working tree and can name no committed gate (observed in my own run)

The kill rule binds runs of `c1-count-v2.py` on the landed gate `94a7be5a…`. My first run used the
default `--gate tools/research-gate.sh` from the lane root (stdout to
`counter-seed5187.out`, receipt `c1-v2-seed5187.json`):

```
$ python3 corpus/evidence/round33/c1-count-v2.py --seed 5187 --receipt .../c1-v2-seed5187.json
TOPLEVEL_FIELD_MATCH=156/156        rc=0
receipt: gate="tools/research-gate.sh"
         gate_sha256=45d76b4fc7c572c61a31b47608303c02e4c65b392b2824aa7561bda2834e3044
         seed=5187 utc=2026-10-23T09:10:30Z elapsed_s=7.808 gate_rc=1 predicate_holds=true
```

That `gate_sha256` matches no gate I can identify: not base `f4731885…`, not landed `94a7be5a…`
(committed gate of `0fb300b5` **and** of the new tip `4c076a0f`), not the worktree at any time I
sampled. The lane moved under the wave while seats ran — read-only observations, no lane edit by
me:

| local time | fact |
|---|---|
| 06:00 | `sha256sum tools/research-gate.sh` → `94a7be5a…` (= HEAD `0fb300b5` blob) |
| 06:09:25 | new commit `4c076a0f` ("L1 build of CriticControls33's fixture-keyed shortcut … 156/156 on seeds 3391/3392") |
| 06:10:30 (09:10:30Z) | my counter run's receipt records `45d76b4f…` |
| 06:11 | worktree `tools/research-gate.sh` = `220bcf17…` |
| 06:12 | worktree = `263ffb9d…`; `git diff --stat HEAD -- tools/research-gate.sh` = 78 insertions, 45 deletions; `git show 4c076a0f:tools/research-gate.sh` = `94a7be5a…` |

The counter hashes the argv path (`c1-count-v2.py:413-414`, `sha256_file(abspath(gate))`), so a
default-path run during integration scores whatever the worktree holds. Pinned instead to this
directory's `gate-landed.sh` (receipt `c1-v2-seed5188-pinned.json`):

```
$ python3 corpus/evidence/round33/c1-count-v2.py --gate /fast/.../bench/gate-landed.sh --seed 5188 --receipt .../c1-v2-seed5188-pinned.json
TOPLEVEL_FIELD_MATCH=156/156        rc=0
gate_sha256=94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e
seed=5188 elapsed_s=7.083 gate_rc=1 predicate_holds=true
```

Both runs printed 156/156 (no run on `94a7be5a…` printed lower; kill rule satisfied and reported
in full). Consequence for the L1: a receipt whose `gate_sha256` is not `94a7be5a…` (or another
declared candidate's committed hash) must not count as "on the landed revision", and default-path
runs during integration will not satisfy that test.

## Contract probes at 64 KiB (no C1 break found)

`probes.py`; all C locale; stdout/stderr in scratch `bench/probe/`; `probes.jsonl`.

- **A — string content is never structure (contract item 3).** Record `{"id":"D64",…,"note":"<64
  KiB of escaped `\"line\":\"9\"`, `\"sha256\":\"deadbeef\"` text>"}` (65,573 B line). landed:
  `CLAIM id=D64 … observed=supported … at=line:2 verdict=match`, CLEAN, rc=0. base identical
  (the escapes break the base regex, so this probes the landed reader, not a differential).
  Cost: base 0.066 s CPU, **landed 6.892 s** (104×).
- **B — duplicate top-level read field (contract item 2).** `{"id":"B64",…,"line":"1",…,"line":"2"}`
  in a 65,504 B line. landed: `observed=invalid … at=- verdict=invalid`, `RESEARCH_GATE: DRIFT`,
  rc=1 (fails closed as specified). base: `observed=mislocated`, rc=1 (first value wins).
  Cost: base 0.092 s, **landed 6.434 s** (70×).
- **C — additivity.** Two `pad65536`-shaped records in one file (130,954 B): no
  `CLAIM_RECORD_INVALID`, both `observed=supported`, 2/2, rc=0 on both gates. base 0.143 s CPU,
  **landed 12.956 s** — 2.7× the single-record 4.743 s, i.e. per-64 KiB-line cost is additive, not
  amortised.

## Verdict

**C1's field-reading contract HOLDS on long flat inputs — this seat found no falsifying input
there — so the failure this item measures is cost, not correctness.** Concretely:

1. No contract break was found at 64 KiB: item 2 (duplicate → invalid) and item 3 (string content
   is not structure) both hold on 65 KiB lines, and flat records verify identically in semantics;
   the landed gate only adds time.
2. Cost: the reader (`claim_scan`) is a per-character `${s:i:1}` walk, quadratic per line. On a
   flat 64 KiB line whose long bytes the reader actually sees, landed costs **4.7 s CPU vs 0.074 s
   at base (64×)** in the C locale and 5.2 s vs 0.60 s (8.7×) in UTF-8 — ~72 µs/byte, matching
   wave-1's standalone walk (52.99 µs/B at 64 KiB) plus gate work. Span-sized cells show only
   1.1–1.6× because base's own `json_unescape` is quadratic in the read value too.
3. The 60-s bar is not crossed by any one-record-per-file run (max 37.3 s wall, span65536 UTF-8
   landed), but it is crossed by a two-line claims file at that size on both gates (base 60.75 s,
   landed 65.31 s wall, CPU 59.6/64.9) and, by additivity (12.96 s per two 64 KiB lines in C), a
   128-record file of 64 KiB lines would cost ~10 min — past the counter's own 600-s gate timeout
   [INFERENCE from the measured additivity; only 1 and 2-record files were timed].
4. F1: spans ≥ ~32.7 KiB are unverifiable on **both** gates (argv length), reported as `mismatch`
   + drift after 11–37 s; a pre-existing limit, invisible to the counter's 159–412 B fixture.
5. F2: default-path counter receipts during integration record a `gate_sha256` that identifies no
   committed gate; pin `--gate` to a hashed copy for kill-rule runs.

## Limits

- ASCII fixtures only; UTF-8 locale exercised with ASCII bytes (the realistic claim-record case).
  Multibyte span or padding text untested (the same walk then indexes characters, and wave 1
  measured UTF-8 substrings 4.6× slower on ASCII).
- Shared host; CPU is min-of-reps only where reps>1 (1 rep at 16 KiB, 64 KiB, the two-record cell
  and the 200-record cell). Wall includes scheduling noise (many200 UTF-8: 19.4 s wall vs 13.9 s
  CPU); the two-record cell's 60.8 s base wall is corroborated by 59.6 s CPU.
- The 64 KiB span cell measures the failed-locate path (F1), not a located match; the located
  64 KiB measure is `pad65536`.
- The lane moved while I measured (`0fb300b5` → `4c076a0f`, dirty worktree); all timing used gate
  blobs extracted from git objects, so it describes `94a7be5a`/`f4731885` exactly, not the
  worktree.
- No `verify-all`, no selftest, no counter of D1–D5 was run: this item is one instrument.
- Timing noise: two rows report child CPU slightly above wall (many200 base 8.299 s CPU vs
  7.614 s wall), because `RUSAGE_CHILDREN` can reap a grandchild after the measured window; treat
  ratios within ~15% as equal. The 64× pad65536 ratio and the 60-s crossing sit far outside that.
- Cost attribution inside the 11–37 s span65536 cell (regex build + `json_unescape` +
  `claim_scan`) is [INFERENCE] from the two published per-char loops, not from a per-function
  timer.

## Artifacts (this directory, all < 1 MiB)

`gate-base.sh` f4731885… · `gate-landed.sh` 94a7be5a… · `gen.py` fe77d5ff… · `bench.py` c2d59df8… ·
`probes.py` 20897aaa… · `results.jsonl` (36 rows) · `results-span65536x2.jsonl` 486f5469… ·
`run_matrix.log` · `probes.jsonl` · `probes.log` · `counter-seed5187.out` / `.err` ·
`counter-seed5188.out` / `.err` · `c1-v2-seed5187.json` · `c1-v2-seed5188-pinned.json`.
Fixtures (up to 199 KB) and per-run stdout/stderr stay in scratch
`/fast/scratch/hyaku/chousa-r33/w2/ProbeLongLines33/bench/fx/`, `bench/out/`, `bench/probe/`.
