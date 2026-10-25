# W2CritForge — the passing wave-1 log does not stop a hand-forged pid file

Seat: critic. Axes: operability, calibration, depth.
Bound: `corpus/evidence/round44/claims.md` C1 cheapest-gate paragraph. Not retuned. No production file edited. Forge files lived under `/tmp` only.

## Answer

No. The passing wave-1 log does not stop a hand-forged pid file.

Quoted sentence, `corpus/evidence/round44/claims.md` lines 41–42:

> This counter does not stop that forge.

"That forge" is the previous sentence in the same paragraph (lines 40–41): a hand-written log that copies the schema, the 64 names, and invented positive pids. The same admission is in `corpus/evidence/round44/c1-count.py` lines 9–12.

The paragraph's next sentence names what the counter does stop, and it is not that forge (lines 42–43):

> It stops the routed failure: a prose assertion, a `pids 0` waiter, and a log whose end pid is not the start pid.

## What was run

Default counter, which reads `corpus/evidence/round44/parent-lifetime.receipt` (`c1-count.py` line 23). That file is the wave-1 launcher log: start `parent_pid=3226659`, end `parent_pid=3226659` `n_spawned=64` `n_reaped=64`, 130 lines, seat names from `seat-names.txt` (not the `W2*` names). Command: `python3 corpus/evidence/round44/c1-count.py`. Stdout and exit:

```
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=PASS
EXIT:0
```

Hand-forged pid file, not written into the lane: `/tmp/w2critforge-hand-pids.receipt`. Schema copy only. Invented `parent_pid=424242`. Sixty-four frozen names. Invented `child_pid` values `900001`–`900064`. No spawn lines. Reap `epoch=9` after end `epoch=2`. Command: `python3 corpus/evidence/round44/c1-count.py --receipt /tmp/w2critforge-hand-pids.receipt`. Stdout and exit:

```
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=PASS
EXIT:0
```

The passing wave-1 log and the hand-forged file produce the same full-marks lines. Accepting the first file does not reject the second. The log is an input, not a gate.

Routed failures the paragraph says the counter stops, same counter, quoted:

`controls/prose.receipt` — `C1=FAIL prose`, exit 1.

`controls/pids0.receipt` — `C1=FAIL`, exit 1 (`N_SPAWNED=0/64`, `PARENT_PID_MATCH=0/1`).

`/tmp/w2critforge-pid-mismatch-named.receipt` — same 64 names and positive child pids, start pid 11, end pid 12. `PARENT_PID_MATCH=0/1`, `NAMES_MATCH=64/64`, `C1=FAIL`, exit 1.

A missing path prints `C1=FAIL receipt-missing` and exits 1.

## Calibration

- Do not read `C1=PASS` on the wave-1 log as proof those pids were live, and do not read it as proof the file was forged. This seat did not witness the write. `tools/parent-lifetime.sh` line 8 says the receipt is not proof against a later hand-edit. Claims lines 44–45 name the forge so a later round does not treat a schema-valid file as proof of a live wait.
- The non-stop is the counter's, not a property the log lacks by accident. `c1-count.py` checks a positive matching parent pid, `n_spawned`/`n_reaped`/reap-count equal to 64, name equality with `seat-names.txt`, and `child_pid > 0` (lines 85–105). It does not read `/proc`, does not compare spawn lines to reap lines, and does not hash the file.
- Wave-1 reap lines in the production receipt carry `exit_code=1`. Claims line 37: dead seats are not a miss. Seat death is not this forge, and it is not a C1 failure.
- QUALITY 60 (`corpus/QUALITY.md` lines 526–530) asks the frozen counter to name the cheapest full-marks gate and to check controls against that line. This round names the gate and states that the controls do not cover it. Naming is not the same as stopping. The controls that exit 1 are the routed failures above, not the invented-pid file.

## Depth, measured, not a retune

The predicate text (claims lines 18–24) also says every reap line was written before the end line. The counter never compares epochs or line order. `/tmp/w2critforge-end-before-reap.receipt` puts the end line first, then start, then the 64 reaps with later epochs. Same command with `--receipt` that path:

```
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=PASS
EXIT:0
```

That is a wider hole than the named forge. It is not a change to the bound. The asked sentence still governs: the counter does not stop a hand-written log of the 64 names and invented positive pids, and the passing wave-1 log does not stop one either.

Production bounds after these runs, unread as an instruction to edit: `parent-lifetime.receipt` still starts `start parent_pid=3226659 epoch=1792889279` and ends `end parent_pid=3226659 epoch=1792889282 n_spawned=64 n_reaped=64`, 130 lines. sha256 `573f8f770eee105b5301adb7fd115ac1578607619481a68c8a19cfaadd8a3d56`. Counter sha256 `9883df289447fbf52005f1fa6e1ca0ced44d1aba3b122b72345a6f0bf4043a6a`.
