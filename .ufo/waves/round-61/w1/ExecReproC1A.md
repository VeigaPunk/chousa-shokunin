# ExecReproC1A — independent C1 measurement (round 61, w1)

## Findings
- Base `tools/build-spans.py` (sha256 1ed2650a…c80bf6) reads LEGS=7/20 C1=FAIL (exit 1) at seeds 7101, 7102, 7103, in both of two runs per seed.
- Reference `controls/ref-build-spans.py` (sha256 86d64c31…eccfd) reads LEGS=20/20 C1=PASS (exit 0) at 7101, 7102, 7103, in both of two runs per seed.
- Failing legs of base, identical at all 3 seeds and both runs: P03, H07, H08, H09, H10, H11, H12, H13, H14, H15, H16, H17, H20 (13 failing; passes P01 P02 P04 P05 P06 H18 H19 = 7). Matches the frozen `controls/c1-before.txt` description (P03, H07–H17, H20).
- Reference: no failing legs at any seed/run.
- Flaky legs: none. Per-leg pass/fail diff between run A and run B of the same seed was empty for all 6 (builder, seed) pairs.

## Method (what I ran)
Script `/fast/scratch/hyaku/chousa-r61/ExecReproC1A/run.sh` (scratch, deleted before yield): for each builder x seed in 7101 7102 7103, run `TMPDIR=<scratch> python3 -B c1-count.py --builder B --work <scratch>/w-<tag>-<seed>-<round> --seed S`, fresh --work each, 2 rounds (A, B) = 12 runs total.
- Round A: host unloaded (load avg ~0.9 at start, 32 cores).
- Round B: repeat of all six; during seed 7102 (BASE then REF) two parallel `python3 -c` busy loops (600 s cap, 2 cores) were running; killed afterwards (`pgrep` shows no leftover). 7101 and 7103 in round B ran unloaded.
- Load covered only seed 7102 as the item asked; I did not confirm per-core saturation (INFERENCE: two spinning python procs on a 32-core host occupy two cores; other cores stay free, so contention on the builder's own core is unlikely — the load test is weak by that measure).

## RSS legs (peak kiB, from outputs `out-*-{A,B}.txt`)
- BASE H14: 609120/606768 (7101 A/B), 608520/608344 (7102 A/B, round B loaded), 412528/412816 (7103) — limit 98304; fail every time. H15: 413.9–415.5 MiB-ish kiB (~414000) fail. H20: 220–221k (7101,7102), 292k (7103), fail.
- REF H14: 18384–20664; H15: 20016–20932 (limit 98304); pass. H20: 220044–221372 (7101/7102), 291960…293520 (7103) — pass. Loaded 7102 B values (20252/20396/220044) lie inside the unloaded range of the other runs.
- Spread between A and B of same seed: <1% in every RSS leg; no leg near its threshold on REF (H14/H15 ~20% of 98304 limit). INFERENCE: RSS legs are not load-sensitive at this n=2 per seed; H20 limit is not printed, so I can't state its margin from outputs.
- Timeouts: none observed in any of the 12 runs (no leg line showed a timeout; run completes in ~20 s per BASE run on first measured run).

## Limits
n=2 runs per (builder, seed); load only on one seed, two cores; no leg verdict changed, which bounds but does not exclude flakiness. Did not read the counter's source (no need), did not use the labrat.
No installs.

VERDICT: BASE=7-7/20 REF=20-20/20 flaky_legs=none
