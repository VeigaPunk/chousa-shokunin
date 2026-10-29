# ExecReproBattery — round 62 w1 — independent battery measurement

Nothing edited under frozen paths. Counter sha256 prefix at run time: c1v2-count.py b7016fba91b03460 (matches claims),
c1v2-battery.py 9afe00b917fb95e2, round61 c1-count.py f1d8b6fde8dedd88. Scratch /fast/scratch/hyaku/chousa-r62/ExecReproBattery (TMPDIR set, --work per run).
Command shape: `python3 -B corpus/evidence/round62/c1v2-battery.py --counter <K> --work <scratch>/b_<n>` (absolute paths), run
sequentially in one shell job (total wall 557.02 s for all 8 runs, measured by the tool). No C1V2_SEED set.

## Findings
1. v2 counter, three runs, all identical summary, exit 0:
   `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`
   - run a (~89 s), run b (~104 s), run c (~265 s; host heavily loaded by ~100 peer seats). Per-run walls are derived from
     out-file mtimes minus the 557.02 s total (my `bc` timer failed: `command not found: bc`) — INFERENCE-grade (+-2 s), not a direct stopwatch.
   - 0 MISS lines in each of the 3 outputs (23 SUBJECT lines each). Landed x3 and positives x4 read LEGS=20/20 C1V2=PASS in run a.
   - Forgers: every one exit 1, LEGS 10-13/20 (F12: 19/20 in run a). Stubs: exit 1, LEGS 10-11/20 for base stubs (run c: 10 and 11).
     Forger/stub LEGS counts vary between seeds (e.g. stub-base 11,11,10) — the counter's pass/fail is stable, the legs tally is not.
2. v1 counter (corpus/evidence/round61/c1-count.py), exit 1 (~94 s):
   `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=4/4 BATTERY=FAIL` — 12 MISS lines; all 12 forgers accepted.
   Equals committed controls/c1v2-before.txt final line exactly (stub LEGS 7/20 matches there too).
3. Null counters, each exit 1, summary lines (each run 1-2 s; mtime-derived):
   - null-pass:     `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=0/4 BATTERY=FAIL` (16 MISS)
   - null-fail:     `LANDED=0/3 POSITIVES=0/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=FAIL` (7 MISS)
   - null-hashlist: `LANDED=0/3 POSITIVES=0/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=FAIL` (7 MISS)
   All three byte-match the three summary lines in controls/null-counters.txt. 3/3 fail the battery; no do-nothing counter passes.
4. Comparison to receipts: c1v2-before.txt summary line and null-counters.txt lines reproduced exactly; sub-lines differ only in
   salted sha256 values (random salt per run), as expected.

## Limits (what this does not show)
- Three runs at unset seed share the counter's frozen forger set; no new forger tried (named limits in claims unchanged).
- Wall times for the individual runs are approximate (see 1); load from peer seats inflated run c.
- Battery removes its --work b_* subdirs itself; kept only out_*.txt, deleted with scratch.

VERDICT: BATTERY_V2=PASS x3 V1=FORGERS_REJECTED 0/12 NULLS_FAIL=3/3
