# R34RerunC1v3 — independent re-run of frozen counter v3 on the landed gate (residual falsify seat)

## What I ran

Scratch clone of the lane at the landed revision, no network, no installs:

```
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
git clone -q /home/vgpnk/Projects/shokunin/chousa-shokunin /fast/scratch/hyaku/chousa-r34/w2/R34RerunC1v3/clone
git -C clone checkout -q 3026a4e5bb4c44c01982fd67bd0140df36384942   # -> 3026a4e5bb4c44c01982fd67bd0140df36384942
sha256sum clone/tools/research-gate.sh clone/corpus/evidence/round34/c1-count-v3.py
# 772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58  tools/research-gate.sh   (matches frozen candidate)
# 970cf9a709d72ed8b3ec91eeabc2b1778831f695b5ea18b40f026489f7f2da2a  corpus/evidence/round34/c1-count-v3.py (matches frozen v3)
```

One run per seed, form: `LC_ALL=C C1_TMP=<scratch>/tmp-s<seed> TMPDIR=<same> timeout 1800 python3
corpus/evidence/round34/c1-count-v3.py --gate tools/research-gate.sh --seed <seed>
--receipt .ufo/waves/round-34/w2/R34RerunC1v3/c1v3-s<seed>.json` (run from the clone). Seeds
4211, 5177 (LC_ALL=C) and 6301 (no LC_ALL; ambient `LANG=en_US.UTF-8`, so this is a UTF-8-locale
run — `locale` showed `LC_ALL=` empty and all categories `en_US.UTF-8`). None of 3601–3603 reused.

Incident: the first launch of s4211/s5177 exited rc=127 — `error: command not found: /usr/bin/time`
— my wrapper, not the counter; both were re-run without it and succeeded. s6301 was unaffected.

## Results — all three runs 42/42, zero misses

| seed | locale      | label                | gate_rc | timed_out | elapsed_s | counter rc | receipt |
|------|-------------|----------------------|---------|-----------|-----------|------------|---------|
| 4211 | LC_ALL=C    | LONGSPAN_MATCH=42/42 | 1       | false     | 40.448    | 0          | `.ufo/waves/round-34/w2/R34RerunC1v3/c1v3-s4211.json` |
| 5177 | LC_ALL=C    | LONGSPAN_MATCH=42/42 | 1       | false     | 40.832    | 0          | `.ufo/waves/round-34/w2/R34RerunC1v3/c1v3-s5177.json` |
| 6301 | UTF-8 ambient (no LC_ALL) | LONGSPAN_MATCH=42/42 | 1 | false | 57.505 | 0 | `.ufo/waves/round-34/w2/R34RerunC1v3/c1v3-s6301.json` |

Every receipt: `schema=chousa-r34-c1-receipt/v3`, `counter_sha256=970cf9a7…2a2a`,
`gate_sha256=772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58`,
`predicate_holds=true`, `misses=[]`, empty `gate_stderr_tail`. gate_rc=1 is the designed
`RESEARCH_GATE: DRIFT` exit; no run approached the 1500 s gate bound.

Per-class lines (identical for all three runs, all full — quoted from run stdout):

```
long-verbatim-ml 3/3    long-verbatim-1l 2/2    long-edge 2/2          long-mut-head 2/2
long-mut-tail 2/2       long-mut-center 2/2     long-decoys 7/7        long-decoys-exact 2/2
long-decoys-line-wrong 2/2  long-split 2/2      long-glued-left 2/2    long-glued-right 2/2
long-glued-then-valid 2/2   long-line-bound 2/2 long-line-wrong 2/2    short-verbatim 3/3
short-mut 3/3
```

## Committed-run check (kill rule: no committed run of counter v3 on the landed gate below 42)

`git grep -l 970cf9a709d72ed8b3ec91eeabc2b1778831f695b5ea18b40f026489f7f2da2a -- .` over the lane
worktree returns exactly: `controls/L1-base-v3/` (3), `controls/L1-v3-rescore/` (7),
`controls/L1-v3/` (26), `measure/c1v3-s3601.json`, `c1v3-s3602.json`, `c1v3-s3603-utf8.json`,
`claims.md`. Of these, the only receipts with `gate_sha256=772a1d8e…` (the landed gate) are the
three `measure/` runs: 42/42, 42/42, 42/42, all `predicate_holds=true` (rc=1, no timeout;
elapsed 38.9 / 58.3 / 90.5 s). **No committed run of counter v3 on the landed gate prints below
42.** For context, the committed do-nothing base-gate controls (`controls/L1-base-v3/`,
gate `43a1af35…`) score 25/42 (s3493, LC_ALL=C) and 0/42 on two 1501 s timeouts (s3491/92) —
the E2BIG surface the candidate repairs.

## Verdict (this seat's recommendation only)

The falsification attempt produced **no miss**: on two fresh seeds under LC_ALL=C and one UTF-8
run, the landed gate reads every record class correctly (42/42, `predicate_holds=true`), and my
scan found no committed counter-v3/landed-gate run below 42. Both fresh-seed per-run conditions of
P1 v3 are independently reproduced. Whether C1 advances remains the orchestrator's call under the
declared held-controls exclusion; nothing here rescues or substitutes held work.

## Limits

- Single machine, load average ~28 on 32 cores during the runs; elapsed figures include
  contention but are ~35× under the 1500 s bound, so the verdict is insensitive to it.
- The "without LC_ALL" slot is an en_US.UTF-8 run (ambient locale), not a C-locale-absent run.
- Two elapsed-inflating wrapper failures (rc=127, `/usr/bin/time` missing) occurred before the
  successful runs; the counter itself never errored (rc 0/1 only, `gate_timed_out=false`).
- No tools installed; no network; writes confined to my scratch dir, the three receipt files
  in my w2 directory, and this report.
