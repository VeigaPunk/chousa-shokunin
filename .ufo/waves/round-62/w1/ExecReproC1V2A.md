# ExecReproC1V2A — C1 v2 counter reproducibility (round 62 w1)

## Findings
- 45 counter runs (5 builders x 9 configs), every run exit 0, `LEGS=20/20 C1V2=PASS`; each run printed 20 `LEG` lines, all `pass`.
- Builders: landed `tools/build-spans.py` (sha256 prefix c366492005ce304a, matches claim), `pos-indep1..3.py`, `pos-ref.py`.
  Counter `c1v2-count.py` sha256 prefix b7016fba91b03460 (matches claim).
- Configs per builder (fresh `--work` each, `TMPDIR` = my scratch): seeds 8101, 8102, 8103 twice each (tags a, b);
  `C1V2_SEED` unset twice; seed 8101 once under load (two `python3 -c "while True: pass"` busy loops
  alongside the host's existing load average ~10 on 32 cores).
- Same builder + same seed, run twice: no leg verdict changed (all 20 legs `pass` every time). Loaded 8101 run
  vs unloaded 8101 a/b: no verdict changed.
- Flaky legs: none. (Only the verdict column was compared; per-leg detail strings such as `rss_kib` were not diffed.)
- Not run: unset-seed runs have random seeds not printed back-to-back comparable; seed value printed in the
  `BUILDER ... SEED=` line of each output.

## Wall time per run (s)
- Unloaded: 2.22-2.94 for all builders, one outlier ref unset-a 4.61 (host load, no verdict effect), ref 8103 b 3.16.
  Landed: 2.24-2.41. indep1: 2.22-2.50. indep2: 2.36-2.59. indep3: 2.36-2.94. ref: 2.44-4.61.
- Loaded 8101 (2 busy loops): landed 2.75, indep1 2.72, indep2 4.37, indep3 4.53, ref 5.68.
  Load roughly doubled wall time for three builders; no verdict change and no timeout.

## Evidence
- Driver: `/fast/scratch/hyaku/chousa-r62/ExecReproC1V2A/drv.py` (deleted with scratch); per-run outputs `out_<builder>_<seed>_<tag>.txt`
  parsed with regex `^LEG (\S+ \S+) (pass|FAIL|fail\S*)`; set of verdicts across all 45 runs = {pass}; set of leg counts = {20}.
- Example single run (pos-ref, seed 8101): `LEGS=20/20 C1V2=PASS`, real 2.339 s, exit 0.
- No tool installs.

VERDICT: LANDED=20-20/20 POSITIVES=20-20/20 flaky_legs=none
