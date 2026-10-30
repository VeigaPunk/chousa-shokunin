# Counter03 — R64-C3 relocation counter

- Frozen claims read: `corpus/evidence/round64/claims.md` (C3 predicate at lines 194–239; instrument digest at line 265).
- Command, from lane root:
  `python3 corpus/evidence/round64/c3-count.py --work /fast/scratch/hyaku/chousa-r64/Counter03/c3-work --fleet /home/vgpnk/Projects/shokunin`
- Exit: **1**.
- Observed stdout (also retained verbatim in `c3-count.stdout`):
  ```
  SMOKE=3/3
  RELOC c1-battery-v3 rc=2 FAIL c1-battery-v3: MISSING_LANE_FILE: /fast/scratch/hyaku/chousa-r64/Counter03/c3-work/rel-c1-battery-v3/lane-copy/corpus/SO
  RELOC run-receipts-v3 rc=2 FAIL run-receipts-v3: MISSING_LANE_FILE: /fast/scratch/hyaku/chousa-r64/Counter03/c3-work/rel-run-receipts-v3/lane-copy/corpu
  RELOC c3-count rc=2 FAIL c3-count: MISSING_LANE_FILE: /fast/scratch/hyaku/chousa-r64/Counter03/c3-work/rel-c3-count/lane-copy/corpus/SOURCES.md
  RELOCATION_MATCH=0/3
  SHIFT_MUTANT_UNNAMED=1/1
  C3=FAIL
  ```
  The first two failure lines are truncated by the counter's own `[:120]` formatting; full subprocess stderr was not emitted by the instrument and is unavailable. `c3-count.stderr` is empty.
- Result: intact smoke legs and shift-mutant exhibit passed; all three relocation matching legs failed. C3 does not satisfy the frozen kill rule in this run. Relocation diagnostics identify the derived `MISSING_LANE_FILE` paths but did not meet the counter's expected path comparison.
- Scratch: `/fast/scratch/hyaku/chousa-r64/Counter03/` removed after run.
- No tools installed or updated.
