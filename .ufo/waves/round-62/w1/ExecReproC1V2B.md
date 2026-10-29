# ExecReproC1V2B — Round 62 w1 — independent repeat of the C1 v2 counter on five builders

Claims file sha256 checked: a3193ebd...866bc (`sha256sum claims.md`, matches). Counter `c1v2-count.py` run unmodified, `python3 -B`,
TMPDIR and --work under /fast/scratch/hyaku/chousa-r62/ExecReproC1V2B-2/ (fresh `--work` per run, deleted at the end).

## Findings
1. 55 counter runs in total, 5 builders x 11 conditions: landing `tools/build-spans.py` (sha256 prefix c366492005ce304a, as printed by the
   counter), `controls/pos-indep1.py`, `pos-indep2.py`, `pos-indep3.py`, `pos-ref.py`. Every run printed `LEGS=20/20 C1V2=PASS`, exit 0.
   All 55 runs show 20 legs, every leg `pass` in both the `neutral` and `plain` profiles (parsed from the `LEG` lines). No run below 20/20.
2. Flaky legs: none. Same builder + same seed run 2 or 3 times (seeds 8104, 8105, 8106, and seed 8105 five times in total including three
   load conditions): the per-leg verdict set was identical in every group. Unset-seed runs get a random seed per run, so only their LEGS line is
   comparable: 20/20 on all 10 (2 repeats x 5 builders).
3. Load did not change any verdict. Wall time is 3x-6x higher under load, which is a timing effect only (see the caveat below).

## Runs (driver /fast/scratch/hyaku/chousa-r62/ExecReproC1V2B-2/drv.py, result res.json; deleted with the scratch)
| condition | seeds | runs | LEGS (all builders) | wall s min / mean / max |
|---|---|---|---|---|
| idle1 (first pass) | 8104 8105 8106 unset | 20 | 20/20 x 20 | 2.58 / 4.43 / 6.68 |
| idle2 (second fresh pass) | 8104 8105 8106 unset | 20 | 20/20 x 20 | 2.81 / 5.11 / 12.72 |
| load2: two `python3 -c "while True: pass"` | 8105 | 5 | 20/20 x 5 | 9.74 / 11.52 / 13.19 |
| load2b: same, repeated | 8105 | 5 | 20/20 x 5 | 10.36 / 11.32 / 12.48 |
| load32: 32 busy loops (extra, beyond the item) | 8105 | 5 | 20/20 x 5 | 14.63 / 15.81 / 16.92 |
Per-run lines (builder seed condition LEGS rc wall) are in the driver's stdout; the first single run, landing at 8104, took 2.52 s
(real 0m2.520s, user 5.0 s, sys 0.9 s) and printed `LEGS=20/20 C1V2=PASS`.

## Caveats (stated, not inferred away)
- The host was not idle. `uptime` after the runs: load average 108.02 / 67.02 / 36.35 on a 32-thread machine (fleet seats running). So the
  "idle" conditions already ran under fleet load; the first single run (2.5 s) is the quietest wall observed. The wall spread, such as 12.72 s for
  pos-ref unset idle2, follows the fleet load: the same builder and seed ran in 4.5 s at another moment. Two busy loops added
  about 5-7 s on top of that background load [INFERENCE: the extra cost is from the loops, since idle1/idle2 means are 4.4/5.1 s].
- Scope: this measures only the five positive builders. I ran no forgers and no stubs, so it says nothing on the 12/12 and 4/4 parts of the battery.
- Only these seeds were tried: 8104, 8105, 8106 and random unset seeds (10 unset runs, each with its own random seed). A seed-dependent leg that
  fails elsewhere would not show here.
- Receipts not kept by this seat beyond this report; the scratch tree was deleted as instructed.

VERDICT: LANDED=20-20/20 POSITIVES=20-20/20 flaky_legs=none
