# ExecParallelLoad — concurrency/load robustness of c1v2-count.py (round 62 w1)

Findings
1. 8 concurrent counters on tools/build-spans.py, distinct --work dirs, seeds C1V2_SEED=1001..1008 (run A) and 2001..2008 (run B): every one printed `LEGS=20/20 C1V2=PASS`, exit 0. 16/16 runs, min LEGS = 20/20.
2. Battery `--only LANDED`, two at once (run B): each printed `LANDED=3/3 ... BATTERY=FAIL`, exit 1 and each landed-1..3 line read `counter_exit=0 want=0 ok | LEGS=20/20 C1V2=PASS`. The exit 1 is by design, not load: c1v2-battery.py:176-177 sets `full = not a.only`, so verdict is False whenever --only is given (the other groups read 0/0). The meaningful signal under --only is LANDED=3/3 plus the `ok` lines. Anyone scripting `--only LANDED` must not treat exit 0 as success. Reported as a calibration note, not a defect of the frozen file.
3. No timeout, ENOSPC, EAGAIN or Errno in any output (`grep -l -iE "timeout|ENOSPC|EAGAIN|Errno" out/*.txt` matched nothing; the only output was the exit-1 notice from grep). The sandbox precheck (`unshare -Ufp ... true`, 30 s) never failed, so no exit-2 "sandbox unavailable".
4. No false FAIL from the 200 MiB address-space limit: every H20 BIGFORM leg passed in both profiles with rss_kib 167216..231364 (below the limit's effect; leg rc=1 as required). No leg reported a timeout.

Evidence (run B, python driver /fast/scratch/hyaku/chousa-r62/ExecParallelLoad/drv.py, `python3 -B`, TMPDIR=scratch)
- host: 32 cores, loadavg at start 92.37 (other fleet seats running), 99.4 after the counters, 108 after the battery; free mem 3.3 GB at launch of run A (22.8 GB used by others).
- counters x8: total wall 18.1 s; per run 16.3, 18.0 x7 s (60 s timeout is 3.3x the slowest whole run; per-leg well below).
- battery x2 (3 landed copies x 20 legs x 2 profiles each, sequential inside a process): both 48.1 s.
- peak disk: sampled `du -sk` every 2 s over the whole scratch dir: 15728 KB (15.4 MiB) in run B; 17008 KB (16.6 MiB) in run A. Guard before start: /fast/scratch/hyaku 33% used, 543.4G free, status OK; no disk-guard action required.
- run A (bash driver) completed all 8 counters PASS but its wall timing was lost (container lacked `bc`; my driver also hung on a bare `wait` after the sampler), so run A contributes only LEGS/exit/peak-disk; run B is the timed run. Run A battery phase never ran; run B ran it.

Not exercised: more than 8 parallel counters, memory pressure below host's 3 GB free (the host happened to be loaded, which is a favourable stress but not a controlled one), non-landing subjects (forgers/stubs) under load.
Cleanup: scratch /fast/scratch/hyaku/chousa-r62/ExecParallelLoad removed before yield. No tools installed.

VERDICT: PARALLEL_LEGS_MIN=20/20 false_fail=no peak_disk=16.6MiB
