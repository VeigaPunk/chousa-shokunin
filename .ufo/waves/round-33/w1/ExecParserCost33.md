# ExecParserCost33 — pure-bash character-walk cost (round 33, wave 1)

Seat: executor, target = falsifiable hypothesis (parser cost), not a C1 candidate. Scratch:
`/fast/scratch/hyaku/chousa-r33/w1/ExecParserCost33/`; artifacts copied to this directory.
No gate was run; `c1-count.py` was never run against any implementation (control rule). Nothing
installed, no network, no process signalled by name; the three long driver commands were
auto-backgrounded by the harness (bg_3143/bg_3210/bg_3293) and all completed within their cap.

Environment: bash 5.3.20(1), gawk 5.4.1, Linux 7.2.11-arch1-1, x86_64, 32 CPUs, loadavg1 42–49
during the runs (shared host). Locale probe inside every run: `LC_ALL=C` → `charmap=ANSI_X3.4-1968`,
`len(é)=2`; `LC_ALL=en_US.UTF-8` → `charmap=UTF-8`, `len(é)=1`.

## Method

Fixtures (`gen_fixtures.py`): one valid JSON claim record per line at exactly 500 / 4096 / 16384 /
65536 bytes (`wc -c` = 501/4097/16385/65537 incl. newline), each with the seven read keys once at
top level, a nested object/array carrying decoy `line`/`sha256`/`id`/`span` members, a
structure-looking string value, and a padding member.

Three standalone bash implementations in `bench.sh` (not the gate):
`parse_walk` (string-state + escape state + depth, records depth-1 member raw values, counts
duplicates of the seven read keys), `parse_growappend` (walk + `s+=$c` per char), `parse_grow`
(walk + `s+=$c` then `c=${s:i:1}` on the growing `s`). `slice` is the bare per-char
`c=${line:i:1}` loop; `fixed0`/`fixedend`/`smallloop` repeat `${line:0:1}` / `${line:last:1}` /
`${line:i%500:1}`.

Timing: `/proc/self/schedstat` field 1 (on-CPU runtime, ns) read immediately before/after each
block; calibration runs size `reps` to ~1.2 s CPU; 3 rounds per cell, min reported. Wall
(`EPOCHREALTIME`) is in the TSV but not used for the verdict (host load 42–49). Each cell ran under
`timeout 400`; no timeout fired. Raw rows: `matrix_main.tsv` (80 rows = 24 cells × 3 rounds +
8 64-KiB cells × 1 round, every cell present), `offsets_captured.txt`, `awk_results.tsv`,
`summary.txt`.

Correctness before timing: `parse_walk` reproduces python `json.loads` top-level values on all four
fixtures in both locales (`members=11`, id/source/span/expect/marker/line/sha256 exact), ignores
the nested `{"meta":{"line":"9"}}` decoy (`line=1`), flags the duplicated record
(`{"id":"a","line":"1","line":"2"}` → `dup=1`), and handles `\\"` and a trailing `\\` in strings.
gawk output on the same records matches (`awk -f walk.awk line_500.jsonl` →
`500 11 0 rec-0500 7 0123456789abcdef`).

## Results — min CPU ns per call (µs/byte in parentheses)

| mode | locale | 500 B | 4 KiB | 16 KiB | 64 KiB |
|---|---|---|---|---|---|
| slice (`${line:i:1}` only) | C | 1,018,742 (2.04) | 19,493,127 (4.76) | 232,628,640 (14.20) | 3,525,149,002 (53.79) |
| **walk** | **C** | **1,670,396 (3.34)** | **22,844,647 (5.58)** | **244,067,063 (14.90)** | **3,472,800,625 (52.99)** |
| walk | UTF-8 | 2,399,863 (4.80) | 66,858,876 (16.32) | 962,132,175 (58.72) | 16,080,665,230 (245.37) |
| growappend (`s+=$c`) | C | 2,077,250 (4.15) | 28,242,356 (6.90) | 269,241,115 (16.43) | 3,818,573,821 (58.27) |
| growappend | UTF-8 | 2,598,614 (5.20) | 70,154,708 (17.13) | 963,187,473 (58.79) | 14,595,591,854 (222.71) |
| grow (`s+=$c`; `${s:i:1}`) | C | 2,394,325 (4.79) | 34,514,257 (8.43) | 349,711,899 (21.34) | 5,313,185,465 (81.07) |
| grow | UTF-8 | 3,563,299 (7.13) | 110,674,985 (27.02) | 1,598,089,267 (97.54) | 25,907,956,464 (395.32) |

walk C 500 B, all three rounds: 1.673826 / 1.670396 / 1.688085 ms.

## Why it is superlinear: substring cost is O(len(s)), not O(i)

`offsets_captured.txt`, C locale, per extraction:

| string | `${s:0:1}` | `${s:last:1}` | `${s:(i%500):1}` |
|---|---|---|---|
| 65536 B | 52,800–55,300 ns | 53,208–55,118 ns | 53,125–53,669 ns |
| 4096 B | 4,344–4,483 ns | 4,428–4,511 ns | 4,923–4,986 ns |

Offset-independent, linear in string length. Least squares on `slice C` (per-extraction ns vs len):
`per_extraction_ns = 1445 + 0.7976 · len` — predicted 1844/4712/14513/53715 vs measured
2037/4759/14199/53790 at 500/4096/16384/65536 B. Independent minimal control (`mini.sh`, no
functions/fixtures): `LC_ALL=C bash mini.sh 65536 2000` → `cpu_ns_per_iter=51960`;
`LC_ALL=en_US.UTF-8 … 65536` → `128015`; at 500 B → 1350 / 1602 ns. Mechanism: bash 5.3.20
materialises the whole string per substring expansion [INFERENCE from the offset-independence and
the linear fit; bash source not read].

## gawk equivalent (same state machine, `walk.awk`)

`awk_results.tsv`; child CPU via bash `times` children line, startup 1.0–1.1 ms over the run:

| locale | 500 B ×4000 | 4 KiB ×500 | 64 KiB ×30 |
|---|---|---|---|
| C | 44,500 ns/line | 282,000 ns/line | 4,400,000 ns/line |
| UTF-8 | 45,250 ns/line | 308,000 ns/line | 4,500,000 ns/line |

Linear (~67–88 ns/byte at every size). gawk is 37× faster than the bash walk at 500 B and 789× at
64 KiB.

## Verdict on the hypothesis

1. **"Under 5 ms per 500-byte line under LC_ALL=C" — HOLDS.** 1.670 ms (min of 3; 3.34 µs/B),
   ~3× under the bar. UTF-8 also holds at this size (2.400 ms).
2. **"Stays linear to 64 KiB" — FALSIFIED.** 131.1× the bytes costs 2079× the time; per-byte cost
   rises 3.34 → 52.99 µs (15.9×). Local exponents 1.23 / 1.72 / 1.91 between successive sizes;
   the n² term dominates at 64 KiB. The bare slicing loop alone is 3.525 s of the 3.473 s walk
   (equal within noise): the walk's own machine is ~1.3 µs/char and negligible at large n.
3. **"UTF-8 locale is superlinear" — HOLDS, but it is not a contrast.** UTF-8 walk is superlinear
   (6700× for 131× bytes; per-byte 4.80 → 245.37 µs, 51.1×) and 4.63× slower than C at 64 KiB
   (16.081 s vs 3.473 s). The hypothesis's implied C-linear baseline is what fails: C is already
   quadratic.
4. **"`${s:i:1}` on a growing string is superlinear" — HOLDS.** `grow` C: 2.394 ms at 500 B and
   5.313 s at 64 KiB (+43 % / +53 % over `walk`). Append alone (`growappend` − `walk`) is
   +0.41 ms / +0.346 s (memcpy-bound, ~6 GB/s); indexing the growing string adds ~1.49 s at 64 KiB.

## Operability implication for C1 (measured, not scored)

The committed counter's fixture (built by importing its own `generate()`, seed 4242, no gate run):
144 records, 159–412 B, median 267 B, mean 276.1 B, total 39,756 B. At the measured 3.34–3.5 µs/B,
a pure-bash walk costs ~0.9–1.4 ms per record and ~0.13–0.24 s for the whole fixture — feasible
inside the counter's 600 s gate timeout. The risk is size, not count: one 64 KiB record costs
3.47 s (C) or 16.08 s (UTF-8), so 144 such records would take ~8.3 min / ~38.6 min, the UTF-8 case
exceeding 600 s. The C1 contract bounds neither line length nor total input; a `${s:i:1}`-based
reader therefore has a size-dependent timeout exposure [INFERENCE]. A linear reader is available:
gawk does 64 KiB in 4.4 ms.

## Limits

- Absolute CPU numbers are upper bounds: loadavg1 42–49 on the shared host. `schedstat` excludes
  preemption but not cache/SMT contention; min of 3 rounds is reported, and the verdict rests on
  ratios that are stable across rounds (≤2 % spread within a cell).
- bash 5.3.20 only; other bash versions may differ. ASCII fixtures; UTF-8 locale exercised with
  ASCII content (the realistic claim-record case) — multibyte content untested.
- The walk records raw values for the seven read keys (string-valued here); container-valued read
  fields are counted as members but their spans are not captured, and escaped key spellings (not
  claimed by C1) are not decoded.
- No wall-clock claim is made; wall is in the TSV only.

## Artifacts (this directory; all < 1 MiB)

`bench.sh` 85d88e0f3034dfefaad693128d6a15026de6664aa5923b6c739afcb5a0f153fc ·
`walk.awk` f445d2aa80bfe63eb1546e893b9f249ae373b00339095d6219ec4309f5a07468 ·
`mini.sh` 63c1c669a73ee2b918c175c37422fdfe0d61d56a4d13d74ab46fe6b94d0d4571 ·
`matrix_main.tsv` de37933b8db9156397c362e7dc4544e34ed6bda3e6c25bc8b711a70efd16e453 ·
`awk_results.tsv` a4ff32ebeafd1fbb84f91ec410eec9e8418653cb78999a8c81aaa8d5d3bc08ed ·
`summary.txt` f551cbe562f164bd2acb23a2a05fa30133cf47fdc16961336b6837b564478a69 ·
also `gen_fixtures.py`, `gen_awk_inputs.py`, `bench_awk.sh`, `matrix_main.sh`,
`matrix_offsets.sh`, `offsets_captured.txt`.
Large inputs stay in scratch: `/fast/scratch/hyaku/chousa-r33/w1/ExecParserCost33/line_*.jsonl`,
`awk_*.jsonl`, `fixture_probe/`.
