# ExecWitnessTiming — witness cost bound (round 35, w2)

Seat: `ExecWitnessTiming` (executor, leaf). Scope: the **cost bound** of
`tools/mechanism-witness.py` and whether it is safe to run in a receipt loop.
No lane production file was edited; no git/jj write command was run.

Gate under test: clone of the wave base revision `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`,
`tools/research-gate.sh` sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
(= the landed gate named in the round brief; re-derived with `sha256sum`).
Witness tool sha256 `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3`.

Scratch: `/tmp/hyaku/chousa-r35/w2/ExecWitnessTiming/` (clone, probes, traces).
Artifacts copied into this seat's own directory
`.ufo/waves/round-35/w2/ExecWitnessTiming/` (68 KB total; the multi-hundred-MiB
trace files stay in `/tmp` and are cited by path + sha256).

---

## 1. Verdict

**The tool is safe to run in a receipt loop only under three stated conditions,
and one of them is a correction to the runbook.**

1. **Cost is modest in time and memory, large in disk.** Per witness run:
   wall 3.4–9.3 s, peak RSS ~22–24 MiB, but a **166–299 MiB** stderr trace file
   that is written to the temp dir and deleted on normal exit. The runbook row
   `SKILL.md:94` says "trace file bounded by the fixture (9 records with 32 KiB
   spans)"; measured, the trace is **335× the fixture bytes** and varies **1.8×**
   with the seed. The runbook must cite a number, not a bound.
2. **Reserve ≥ ~320 MiB free per concurrent witness run** in `WITNESS_TMP` /
   `TMPDIR` (measured peak for the largest seed: 299.4 MiB). Under a
   space-constrained temp filesystem the tool **does not report an error**: the
   trace is silently truncated and the run prints `WITNESS=fail` with a reduced
   stamp count while `OUTPUT=9/9` stays correct. That direction is fail-closed
   for the landed gate, but the C2 counter itself dies with an **unhandled
   `OSError` (exit 1 + traceback)** rather than the documented harness exit 2.
3. **Never SIGKILL/SIGTERM the witness mid-run.** The temp dir is then leaked
   (257 MiB observed) and the orphaned `bash -x` gate child keeps running and
   keeps writing the trace. Cleanup is `finally`-based and only covers normal
   exits.

Recommended receipt-loop recipe: run the witness with an explicit `WITNESS_TMP`
on a filesystem with ≥ 512 MiB free per parallel slot, one witness per slot
(4 parallel → 700.4 MiB peak measured), and treat `WITNESS=fail` with a
**reduced stamp count** as "the environment ran out of room", not as a
mechanism verdict.

---

## 2. Cost measurements

### 2.1 The requested run — `mechanism-witness.py --gate <clone> --seed 3569 --json w.json`

```
$ cd /tmp/hyaku/chousa-r35/w2/ExecWitnessTiming
$ export WITNESS_TMP=/tmp/hyaku/chousa-r35/w2/ExecWitnessTiming/wit_tmp
$ /home/vgpnk/.local/bin/time -v python3 clone/tools/mechanism-witness.py \
      --gate clone/tools/research-gate.sh --seed 3569 --json w.json
WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)      # exit 0
```

`/usr/bin/time` does **not** exist on this host
(`ls: cannot access '/usr/bin/time': No such file or directory`); GNU time
1.9 is installed at `/home/vgpnk/.local/bin/time` and was used instead — no
package was installed for this measurement.

`time -v` (full output copied to `.ufo/waves/round-35/w2/ExecWitnessTiming/time-v-witness-3569.txt`):

| quantity | value |
|---|---|
| Elapsed (wall clock) | **0:03.65** |
| User time | 3.43 s |
| System time | 0.24 s |
| **Maximum resident set size** | **22724 kB (22.2 MiB)** |
| File system outputs | 389648 (blocks) |
| Exit status | 0 |

The tool's own `elapsed_s` in the receipt: `3.61`
(`witness-3569.json`). Peak RSS across the whole tree is dominated by the
`bash -x` gate child: `resource.getrusage(RUSAGE_CHILDREN).ru_maxrss =
19796 kB` for the gate alone (`child_rss.py` run, wall 5.18 s). The Python
driver itself is a few MiB.

### 2.2 Trace file size — instrumented by hand with the same PS4

The tool deletes its temp root, so the trace was reproduced independently with
the identical invocation and PS4 (`@@WITNESS@@${BASH_SOURCE}:${LINENO} `), keeping
the stderr file (`trace_probe.py`, copied into the seat directory):

```
$ python3 trace_probe.py clone/tools/research-gate.sh 3569 keep3569
{"gate": ".../clone/tools/research-gate.sh", "seed": 3569, "gate_rc": 1,
 "wall_s": 4.405, "trace_bytes": 198868470, "trace_mib": 189.656,
 "trace_lines": 91568, "fixture_bytes": 593498, "fixture_files": 10, ...}
```

| seed | trace bytes | MiB | trace lines | fixture bytes | amplification |
|---|---|---|---|---|---|
| 3569 | 198868470 | 189.7 | 91568 | 593498 | **335×** |
| 3570 | 313288273 | 298.8 | 151785 | — | — |
| 3571 | 176224480 | 168.1 | 80569 | — | — |
| 3572 | 174059925 | 166.0 | 79965 | — | — |

Trace sha256 (files kept in `/tmp`, >1 MiB so not copied into the seat dir):

- `/tmp/hyaku/chousa-r35/w2/ExecWitnessTiming/keep3569/_trace.log` — `70bd1379ceb5067886eb42cea29dc92af159389e0c66d7bf1b21c9632eabf711`
- `/tmp/hyaku/chousa-r35/w2/ExecWitnessTiming/keep-3570/_trace.log` — `04826d516c1493b2c7f1bafc7d09d2c41245a23757b11ed56887eec5f7527811`
- `/tmp/hyaku/chousa-r35/w2/ExecWitnessTiming/keep-3571/_trace.log` — `1914388158592e43c29b162a3f1c3997f536488c04c68193e30e40c9cdc8e4cb`
- `/tmp/hyaku/chousa-r35/w2/ExecWitnessTiming/keep-3572/_trace.log` — `05e69cf893d6df3f9b3313eda51ad42553121c5a0ba7bfce99a5b5564291d966`

Why the trace is so large: the long spans are 32765–32767 bytes and `bash -x`
echoes the whole payload on every traced line. Measured composition of the
seed-3569 trace: 4543 lines longer than 20 KB hold **67.0 %** of all bytes;
median line 99 B, p90 3599 B, max 102779 B. The trace is therefore a function
of *span bytes × traced-line count*, not of the number of records — a runbook
that says "bounded by the fixture" understates it by two orders of magnitude.

### 2.3 Cost across seeds, repeats and parallelism

```
seed=3569 WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1   wall=5.91 maxrss=23836 kB
seed=3570 WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1   wall=8.33 maxrss=23708 kB
seed=3571 WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1   wall=4.79 maxrss=23660 kB
seed=3572 WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1   wall=4.23 maxrss=22960 kB
```

Repeatability: seed 3569 run twice → byte-identical verdicts
(`WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1`).

Peak temp-disk occupancy, sampled by a 20 Hz walker over the witness's own
temp dir:

| scenario | wall | peak temp bytes | peak MiB | leftover |
|---|---|---|---|---|
| 1 witness (seed 3570) | 6.29 s | 313892266 | **299.4** | `[]` (clean) |
| 4 witnesses concurrently (3569–3572) | 6.36 s | 734472228 | **700.4** | `[]` (clean) |
| C2 counter, seed 3569 (3 witness runs) | 15.32 s | 199489998 | 190.2 | `[]` (clean) |
| C2 counter, seed 3570 (3 witness runs) | 16.58 s | 314395455 | **299.8** | `[]` (clean) |

So the C2 counter's own temp peak is ≈ one live trace (the witness removes its
root per run), and the whole C2 unit costs **15.3–16.6 s** for
`WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass`
(`c2-3569.json`, `c2-3570-poll3.json`). For contrast the C1 counter is
negligible: `c1 wall=0.51 rss_kb=21308`, `GREP_PIN_MATCH=9/9`.

Traced vs untraced, same fixture (cost attribution): plain `bash gate` → wall
3.315 s, child maxrss 20040 kB; `bash -x gate` → wall 5.176 s, child maxrss
19796 kB. **The `bash -x` trace costs ~1.9 s and ~190–300 MiB of writes; the
matching itself is unaffected.**

---

## 3. Failure modes a receipt loop must know about

### 3.1 Disk exhaustion is silent and shows up as a mechanism verdict

With `WITNESS_TMP` on a bounded tmpfs:

| tmpfs size | witness stdout | exit | receipt |
|---|---|---|---|
| 64 MiB (seed 3569) | `WITNESS=fail OUTPUT=9/9 STAMPS chunk=2 direct=1` | 1 | `witness-3569-tmpfs64M.json` |
| 150 MiB (seed 3570) | `WITNESS=fail OUTPUT=9/9 STAMPS chunk=4 direct=1` | 1 | `witness-3570-tmpfs150M.json` |
| 200 MiB (seed 3570) | `WITNESS=fail OUTPUT=9/9 STAMPS chunk=5 direct=1` | 1 | `witness-3570-tmpfs200M.json` |
| 320 MiB (seed 3570) | `WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1` | 0 | `witness-3570-tmpfs320M.json` |

The bash stderr write hits ENOSPC and the trace is cut short; the tool does
not detect it (no write-error string in the truncated trace, `grep -c` = 0).
`OUTPUT=9/9` stays correct because stdout is a separate pipe, so the *only*
signal is a low stamp count. **A truncated trace therefore looks exactly like a
gate that skipped the chunk matcher.** For the landed gate this is fail-closed
(`LANDED_WITNESS=fail` → P2 false), but the receipt carries no field
distinguishing "no room" from "no mechanism".

**Margin note (calibration-adjacent):** the predicate is
`stamps["chunk"] >= long_records` (8), and the landed gate produces **9**
stamps, i.e. a margin of exactly one stamp. Stamp offsets in the seed-3569
trace are at 14.07 %, 27.71 %, 41.65 %, 54.47 %, 68.32 %, 68.97 %, 71.32 %,
85.25 %, 99.76 % of the file. Truncating the trace to 85–99 % of its bytes
still yields 8 stamps and still reads `WITNESS=pass`; below 85 % it reads
`fail`. This is the aggregate-threshold limit already recorded in the claims
erratum (`corpus/evidence/round35/claims.md:143-146`), re-derived here from
byte offsets.

### 3.2 The C2 counter does not degrade gracefully under ENOSPC

```
$ C2_TMP=<64 MiB tmpfs> python3 corpus/evidence/round35/c2-count.py --gate … --battery … --seed 3569
Traceback (most recent call last):
  File ".../corpus/evidence/round35/c2-count.py", line 210, in <module>
  File ".../corpus/evidence/round35/c2-count.py", line 172, in main
    f.write(patch_gate(gate_text, helper, branch))
OSError: [Errno 28] No space left on device
EXIT=1
```

`c2-count.py:172` is unguarded; the documented contract is "harness error exit
`2`" (`SKILL.md:93`). The receipt is written but incomplete
(`predicate_holds` absent, `variants` empty —
`c2-3569-tmpfs64M-crash.json`). Exit 1 is still "not a pass", so P2 is not
falsified, but the receipt is unreadable as evidence.

### 3.3 A killed witness leaks its temp dir and orphans the gate child

`SIGKILL` of the witness process: the temp dir survived with a **257 MiB**
`_trace.log`, and the orphaned `bash -x <gate> verify-claims …` child kept
running (two such orphans observed via `pgrep -af`; both killed by PID, no
pattern kill). A `SIGTERM` variant left a **220 MiB** temp dir behind
(`term/w35wit-00000df2-aa988e0e/_trace.log`). Normal exits clean up
completely (`leftover: []` in every table above). The witness's own `finally`
does `shutil.rmtree(root)` (`tools/mechanism-witness.py:309-313`) — that is
Python-level cleanup, so it does not run on SIGKILL.

### 3.4 Minor: an unwritable `--json` path loses the receipt after a full run

```
$ python3 clone/tools/mechanism-witness.py --gate … --seed 3569 --json /nonexistent/dir/x.json
WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)
Traceback (most recent call last):
  File ".../mechanism-witness.py", line 311, in main
    with open(a.json, "w", encoding="utf-8") as f:
FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/dir/x.json'
EXIT=1
```

The whole 4 s run is spent and then the receipt is lost; the exception escapes
`main` (the `finally` block re-raises) so the exit code is 1 rather than the
documented 2. Same shape for a missing gate (`exit 2`, clean message) and a
missing `WITNESS_TMP` (`exit 2`, clean message) — those two are correct.

### 3.5 Write scope

Nothing is written outside the witness's temp dir and the `--json` path: a
`find /home/vgpnk /root /var/tmp /tmp -xdev -newer <marker>` sweep after a
witness run listed only unrelated host activity (other lanes' git/jj writes,
chromium, tracker3). The witness also honours `TMPDIR` when `WITNESS_TMP` is
unset (`tools/mechanism-witness.py:241`).

---

## 4. Numbers the runbook can cite

Per witness run (landed gate, GNU time 1.9 at `~/.local/bin/time`):

- wall **3.4–9.3 s** (5 s median; the spread is host contention — 60+ seats
  were running concurrently during this wave, not witness variance)
- peak RSS **22.7–23.8 MiB** (`Maximum resident set size`, kbytes 22724–23836);
  gate child alone 19.8 MiB
- stderr trace **166–299 MiB** (1.8× spread across four seeds; 335× the
  566 KiB fixture); 80 k–152 k lines
- peak temp-disk **299 MiB** for one run, **700 MiB** for four concurrent runs
- CPU: user 3.43 s / sys 0.24 s for seed 3569; the `bash -x` trace adds
  ~1.9 s over the untraced gate

Per C2 counter run: **15.3–16.6 s**, peak temp **190–300 MiB**.
Per C1 counter run: **0.51 s**, peak RSS ~21 MiB.

Receipt-loop requirements: ≥ 512 MiB free per parallel slot (measured peak
299.8 MiB, 1.7× headroom), explicit `WITNESS_TMP`, no hard kill, and
`WITNESS=fail` with `stamps.chunk < 9` treated as an environment fault.

---

## 5. Limits of this report

- All timings were taken on a host running 60+ concurrent wave seats; wall
  times are therefore an upper bound on an idle host, and the 4×-parallel
  numbers are contention-limited too.
- The disk-pressure rows use tmpfs mounts I created and unmounted under my own
  scratch dir; they are the only privileged action taken (`sudo mount/umount
  tmpfs`).
- I did not modify `tools/mechanism-witness.py`, `c1-count.py` or `c2-count.py`
 ; the ENOSPC crash and the receipt-loss traceback are **findings**, not fixes,
  and are left for the owning seat.
- The trace-byte amplification (335×) explains the disk cost but I did not
  attempt to reduce it; a `PS4` that does not echo the span payload would be a
  design change outside this seat's scope.
- The seed-3569 trace offsets used for the truncation-margin table come from
  one seed; other seeds shift the stamp positions, though the 9-stamps-for-8-
  records margin is structural (`witness_ok = stamps["chunk"] >= long_records`,
  `tools/mechanism-witness.py:295`).
