# ExecReproC1B — independent C1 measurement (round 61, w1)

## Findings
- Builders: base `tools/build-spans.py` (counter printed sha256 1ed2650a…c80bf6, matches claims) and reference
  `controls/ref-build-spans.py`. Seeds 7104 7105 7106, fresh `--work` per run, `TMPDIR=/fast/scratch/hyaku/chousa-r61/ExecReproC1B`.
- 25 counter runs total: per (builder,seed) 4 runs (idle1, idle2, load, load2); base/7104 has one extra idle run
  (the probe run). "load" runs = two parallel `python3 -c 'while 1: pass'` on 2 of 32 cores (uptime after: load avg 12.93 incl.
  the counter itself). Load was applied to ALL seeds, not just one.
- **BASE: LEGS=7/20 C1=FAIL, exit 1, in every run at all three seeds (13/13 runs).** Failing legs identical in every run:
  P03, H07, H08, H09, H10, H11, H12, H13, H14, H15, H16, H17, H20. Passing: P01 P02 P04 P05 P06 H18 H19.
  Same shape as the frozen before (7/20, same 13 failing legs).
- **REF: LEGS=20/20 C1=PASS, exit 0, in every run at all three seeds (12/12 runs).** No failing legs.
- **Verdict change between runs of the same seed: none.** Compared per leg, idle vs load, all 6 (builder,seed) groups: 0 legs changed.
- Only variation is RSS/rc detail text (not verdict-bearing), all far from thresholds:
  - REF H14/H15 peak RSS 19684–20932 KiB vs limit 98304 KiB; idle vs load indistinguishable.
  - BASE H14 RSS 411584–412776 KiB at 7104, 607396–609356 KiB at 7105/7106 (seed-dependent, ~±0.2% between runs); H15 414156–415224 KiB; fails by 4–6x.
  - H20 RSS 217–222k (7104/7105), 290–293k (7106) for both builders; H20 verdict is rc (REF rc=1 pass, BASE rc=0 fail), no RSS limit.
- No timeouts observed in any leg under load (runs finish ~1.5–3 s each; 60 s timeout).
- INFERENCE: the verdict-bearing margins are large (RSS 20 vs 96 MiB for REF; rc, tree), so load on 2 cores of a 32-core host
  does not threaten it; a loaded-to-saturation host was not tested.
- Observation (not a verdict change): base P03 fails with `tools=['__pycache__', ...]` — builder writes `__pycache__` even
  though counter is run with `python3 -B`; consistent with base failing P03 at freeze.

## Per seed LEGS (every run of the seed agreed)
| seed | BASE | BASE failing legs | REF | REF failing |
|---|---|---|---|---|
| 7104 | 7/20 (5 runs) | P03 H07-H17 H20 | 20/20 (4 runs) | none |
| 7105 | 7/20 (4 runs) | same | 20/20 (4 runs) | none |
| 7106 | 7/20 (4 runs) | same | 20/20 (4 runs) | none |

## Evidence
- Commands: `python3 -B <root>/corpus/evidence/round61/c1-count.py --builder <B> --work $S/w_<tag> --seed <N>` via
  `$S/drv.sh` (deleted with scratch). Exit codes recorded: base all `exit 1`, ref all `exit 0` (24 lines in exits.txt, +1 probe run exit 1).
- `grep -h LEGS= out_*.txt | sort | uniq -c` → `12 LEGS=20/20 C1=PASS` / `13 LEGS=7/20 C1=FAIL`.
- Nothing under round61/, tools/, corpus/, SKILL.md edited. No installs. No labrat spawned. Scratch removed before yield.

VERDICT: BASE=7-7/20 REF=20-20/20 flaky_legs=none
