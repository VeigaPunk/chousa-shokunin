# W2ReviewC1Log

Seat: W2ReviewC1Log (reviewer, leaf). Axes: operability, calibration, depth.
Milestone: Round 44 wave 2 — genuine seats after the usage-error wave.
Receipt `corpus/evidence/round44/parent-lifetime.receipt` was not edited. No `--receipt` override. No fetch. No commit.

## Operability — counter run

Command (no arguments; default receipt and seat-names paths inside `c1-count.py`):

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/c1-count.py
```

Stdout (script only; the exit line below is the shell, not the script):

```
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=PASS
```

Exit code: `0`.

That is the counting command named in `corpus/evidence/round44/claims.md` (predicate R44-C1, target block). The printed target is `C1=PASS` with those five ratios and exit 0. This run hit that target.

Default input, from `c1-count.py` (`LANE = Path(__file__).resolve().parents[3]`, then `corpus/evidence/round44/parent-lifetime.receipt`). Not `.ufo/waves/round-44/w2-parent-lifetime.receipt`. That wave-2 file was not passed and is not scored here.

Receipt lines this run's PASS is consistent with (read only):

```
start parent_pid=3226659 epoch=1792889279
end parent_pid=3226659 epoch=1792889282 n_spawned=64 n_reaped=64
```

`rg -c 'exit_code='` on that receipt: 64. `rg -c 'exit_code=1'`: 64. `rg 'exit_code=0'`: no matches. Every reap is nonzero. Claims kill rule: "Dead seats (nonzero exit codes) are not a miss. This predicate does not grade seat success." PASS here is a lifetime-count result, not a seat-success result.

## Calibration — shape log is not a C1 miss

`corpus/evidence/round44/seat-logs/ReviewC1Shape.log` is one line (`wc -l` = 1). The last line is the only line, and it is an error line. Last error line, quoted:

```
error: Cannot combine --prompt with --auto.
```

Same string is the sole line of each of the 64 logs under `corpus/evidence/round44/seat-logs/` (`rg` count: 64 files, 64 matches). Wave 1 died at spawn on that usage error. Those names stay dead. This seat does not replace `ReviewC1Shape`.

Receipt rows for that name (read only):

```
spawn name=ReviewC1Shape child_pid=3226666 epoch=1792889279
reap name=ReviewC1Shape child_pid=3226666 exit_code=1 epoch=1792889281
```

`ReviewC1Shape` is line 1 of `seat-names.txt`. The counter's `NAMES_MATCH=64/64` includes that name. It does not open `ReviewC1Shape.log`. A usage-error log and `C1=PASS` can both be true: the log records a dead seat; the counter records a matched parent pid, 64/64 spawn and reap, no non-positive child pid, and the frozen name list.

What the wave-1 prompt asked and did not get: `ReviewC1Shape.prompt` told that seat to read `c1-count.py` and `tools/parent-lifetime.sh`, say whether wait is in a pipeline, and run the counter on `controls/pids0.receipt` and `controls/prose.receipt`. The log contains none of that. This wave-2 seat did not re-run those two controls. An unrun check has not passed. Claims says both must exit 1; that is the frozen predicate text, not a result of this seat.

## Depth — what PASS does not prove

`c1-count.py` sets `ok = pid_ok and count_ok and names_ok` (source lines 95–105). `count_ok` is `n_spawned == 64 and n_reaped == 64 and len(seats) == 64 and zero == 0`. It does not read reap `exit_code`. It does not compare reap epoch to end epoch. Claims also says "every reap line was written before the end line." This run's `C1=PASS` does not measure that clause. End epoch `1792889282` is after the ReviewC1Shape reap epoch `1792889281` on the two lines quoted above; that is a spot read, not a 64-line order check, and it is not a counter result.

Docstring and claims cheapest-gate paragraph agree: a hand-written log with the 64 names and invented positive pids would still print `C1=PASS`. This counter stops a prose assertion, a pids-0 waiter, and a parent-pid mismatch. It does not stop that forge. This seat does not treat the passing file as proof of a live wait.

`.ufo/waves/round-44/w2-parent-lifetime.receipt` exists and was not the input. Scoring it would mix a live wave-2 launcher log with the frozen wave-1 receipt the predicate names.
