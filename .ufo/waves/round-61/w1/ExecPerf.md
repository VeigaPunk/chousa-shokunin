# ExecPerf — round 61 w1 — performance no-harm, base builder vs reference

## Findings
1. No ratio above 1.25 on the 5-run protocol (wall ref/base max 1.150 on r57c3, RSS max 1.096 on r57c3). Reference is correct on all four inputs: exit 0 on every run, output tree (relative names + bytes, sha256) byte-identical to base on every set.
2. Reference costs ~1-2 MiB more peak RSS (4-10%) on every set: a constant-size overhead (larger source module / extra imports) — INFERENCE, I did not profile it. Not data-proportional: synthetic 5000-row/1 MiB case is +1.0 MiB (4.1%).
3. Wall differences on the three real sets are 31-47 ms runs dominated by interpreter start-up; ratios there (0.99-1.15) are noise-scale (+2..+5 ms). On the only input with real work (syn5000, ~3 s) ref/base is 0.96 (5 runs) and 1.03 (21 runs): no measurable slowdown.
4. The first protocol attempt (in-process `os.wait4` from the driver) was discarded for RSS: the child's `ru_maxrss` read a constant 29532 KiB on all small sets (fork-inherited parent floor, INFERENCE), and its r55 wall ratio 1.279 was a single-order 5-run artifact (later interleaved 21 runs: 1.038). The reported numbers use a minimal launcher (`python3 -S` doing `os.wait4` on the builder) and alternate base/ref order each iteration. `/usr/bin/time` is not installed; nothing was installed.
5. Hazard of the synthetic case, not a ref regression: 5000 rows over 1 MiB takes ~3 s in both builders (per-row cost scales with form size — claims.md Named limit iv). Both builders identical in this respect.

## Method (all run by me)
- Builders copied beside `tools/capture-text.py` into `/fast/scratch/hyaku/chousa-r61/ExecPerf/{base,ref}/tools/` (base = `tools/build-spans.py`, ref = `controls/ref-build-spans.py`).
- Command per run: `python3 -B <b>/tools/build-spans.py --quotes <Q> --cache <C> --out <fresh dir>`, build mode (not --check), stdout discarded.
- Sets: round55 (19 rows), round56 (23), round57/c3 (10), each `--cache corpus/captures`; syn5000 = 5000 rows, ids S001..S999 cycled (`S\d{3}` id rule), one 1 048 576-byte `.txt` capture (unique tokens `w0000000x`), each quote one whole token, so exactly-once holds; cache dir synthetic.
- Median of 5 (primary, `drv2.py 5`), repeated median of 21 (`drv2.py 21`) as noise check. Order alternates base/ref.

## Results (median; wall seconds; peak RSS KiB)
Primary, N=5:
| set | rows | wall base | wall ref | ratio | RSS base | RSS ref | ratio |
|---|---|---|---|---|---|---|---|
| r55 | 19 | 0.047 | 0.047 | 0.992 | 22904 | 24404 | 1.065 |
| r56 | 23 | 0.033 | 0.034 | 1.055 | 19884 | 21268 | 1.070 |
| r57c3 | 10 | 0.031 | 0.036 | 1.150 | 19308 | 21160 | 1.096 |
| syn5000 | 5000 | 3.050 | 2.931 | 0.961 | 24748 | 25772 | 1.041 |
Repeat, N=21 (noise check): r55 1.038/1.038; r56 1.077/1.060; r57c3 1.111/1.048; syn5000 1.031/1.035 (wall/RSS). Max wall 1.111, max RSS 1.060.
Earlier in-process wait4 run (discarded for RSS, output equality only): outputs equal on all four sets (hashes 008f77d90734, cbc42a7869af, 25acb7ac9fa8, 639910d6c8bd).

## Flags
Ratios above 1.25: none in the reported protocols. (Discarded first run: r55 wall 1.279, not reproduced.)
Limits: three real sets are ~10-23 rows, so only syn5000 exercises row-proportional cost; one synthetic shape (single .txt capture; no OLE/zip path, no large `.raw`) and a single host; the hazard guards' cost on 64 MiB inputs was not measured.

Scratch deleted at exit. Max over sets used for the verdict.

VERDICT: WALL_RATIO=1.150 RSS_RATIO=1.096
