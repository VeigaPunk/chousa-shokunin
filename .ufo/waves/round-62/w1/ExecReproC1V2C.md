# ExecReproC1V2C — independent C1v2 counter reproducibility (round 62, w1)

## Findings
- 100 counter runs, all exit 0, all `LEGS=20/20 C1V2=PASS`: 5 builders x 5 seeds (8107 8108 8109 8110, unset) x 2 repeats x 2 load states (idle, busy).
- Builders: landed `tools/build-spans.py` (sha256 prefix c366492005ce304a, printed by counter), pos-indep1, pos-indep2, pos-indep3, pos-ref (controls/).
- Per-leg verdicts: 0 legs with a non-pass verdict in any run; 0 legs whose verdict changed between repeats of the same (builder, seed, load). flaky_legs = none.
- Seed handling: `C1V2_SEED` set from env, unset-seed runs also 20/20 (the counter prints SEED in header; not compared across runs).
- Per (builder, seed, load) the two repeats gave identical summary line and identical leg-verdict vectors (all pass).
- Load: for the busy sweep two `python3 -c 'while True: pass'` loops were running on all seeds (superset of the one-seed ask), on a host already at load average ~12.4 on 32 cores (other fleet seats). Busy loops did not flip any leg.
- Wall time per run (seconds, min / mean / max, n=10 each):
  - landed: idle 2.50/5.90/12.99; busy 5.36/8.50/12.69
  - indep1: idle 2.54/5.54/12.42; busy 5.51/8.43/15.45
  - indep2: idle 2.55/5.28/9.87;  busy 5.72/8.81/15.83
  - indep3: idle 2.73/5.75/11.50; busy 5.84/7.98/12.92
  - ref:    idle 3.52/6.38/11.96; busy 5.87/7.66/10.55
  Spread is dominated by host contention from other seats; counter's own timer showed 2.46 s on a first idle-ish run (seed 8107, landed).
- Caveat (INFERENCE): leg verdict flakiness could still exist at lower rates than 2 repeats x 25 combos per builder detect; 0 flips in 10 runs per builder-load cell bounds it only coarsely. Detail text (rss_kib) varies run to run, verdicts don't.

## Evidence pointers
- Driver: scratch `drv.py` (deleted at close): per run `C1V2_SEED=<N> TMPDIR=/fast/scratch/hyaku/chousa-r62/ExecReproC1V2C python3 -B c1v2-count.py --builder <B> --work <fresh dir>`; fresh --work removed after each run; results parsed from `LEG <id> <name> pass|fail` lines and the `LEGS=` line. Raw run table was in `res.json` (100 records), drv.log 100 lines each `builder seed load rep rc wall LEGS=20/20 C1V2=PASS`.
- First manual run: `C1V2_SEED=8107 ... --builder tools/build-spans.py` -> 20 LEG lines pass (neutral+plain), `LEGS=20/20 C1V2=PASS`, wall 2.46 s.
- No tools installed. No frozen file touched. No labrat spawned.

VERDICT: LANDED=20-20/20 POSITIVES=20-20/20 flaky_legs=none
