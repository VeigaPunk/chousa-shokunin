# CtlC1JitterB — C1 timing controls, round 32 attempt 2 wave 1

## Axes and scoped result

- **Operability:** exclusion of the manifest last-byte probe and append while a cooperating writer holds `LOCK_EX`; preservation of valid append-only JSONL.
- **Coverage:** whether the frozen C1 counter rejects no-lock timing shortcuts, including shortcuts that happen to pass free-writer trials. C2 was read for context, not run or changed.
- **Result:** all three controls **MISSES** the frozen `24/24` target on both fresh seeds. No MEETS-TARGET control was observed. These are control measurements, not candidate/admission judgments; no candidate or canonical judge/runtime was invoked.

| Control | Fresh seed | APPEND_SERIALIZED | F_unterminated | L_empty | L_terminated | L_unterminated | Counter exit | Scoped verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| a: random 0–2 s before probe | 20261023320121 | 11/24 | 11/12 | 0/4 | 0/4 | 0/4 | 1 | MISSES |
| a: random 0–2 s before probe | 20261023320122 | 12/24 | 12/12 | 0/4 | 0/4 | 0/4 | 1 | MISSES |
| b: probe, sleep 0.2 s, re-probe | 20261023320131 | 7/24 | 7/12 | 0/4 | 0/4 | 0/4 | 1 | MISSES |
| b: probe, sleep 0.2 s, re-probe | 20261023320132 | 7/24 | 7/12 | 0/4 | 0/4 | 0/4 | 1 | MISSES |
| c: sync, embedded probe, single manifest printf | 20261023320141 | 1/24 | 1/12 | 0/4 | 0/4 | 0/4 | 1 | MISSES |
| c: sync, embedded probe, single manifest printf | 20261023320142 | 1/24 | 1/12 | 0/4 | 0/4 | 0/4 | 1 | MISSES |

All six receipts report `ref_rc=0` and `predicate_holds=false`. No timeout or harness error occurred. All 72 locked trials report `appended-under-cooperating-lock`.

## Counterexample, evidence, smallest safe correction

The strongest counterexample to timing-only serialization is control a, seed `20261023320122`: all 12 free-writer trials pass, yet all 12 locked trials fail. Trial 0 (`L_unterminated`) has exactly one failure, `appended-under-cooperating-lock`; apparent free-writer success does not establish the claimed exclusion. Control a also still races in seed `20261023320121`, free trial 16 (`blank-line,invalid-json-line`).

Control b's second observation does not protect the interval from that observation to the append. Seed `20261023320131`, free trial 7, reports `blank-line,invalid-json-line`; trial 8 (`L_unterminated`) reports only `appended-under-cooperating-lock`. Control c likewise fails both requirements: seed `20261023320141`, free trial 2 reports `blank-line,invalid-json-line`, and locked trial 5 additionally reports `appended-under-cooperating-lock`. These observations are in the receipt `trials` arrays reproduced below.

The counter did **not** let any complete shortcut through. Its locked-trial loop retains the cooperating lock until writers have either exited or become blocked flock waiters (`corpus/evidence/round32/c1-count.py:210-237`), rather than releasing after a fixed short pause. It then checks the unchanged seed. A random delay can reduce collisions among free appenders without excluding a lock holder; the observed 12/12 free result is consequently not enough to saturate P1. The counter also appends its own unterminated fragment under the lock for empty/terminated seeds, detecting the wrong ordering relative to that writer (`:227-234`).

Important evidence distinction: `prefix-rewritten` is the counter's failure label, not proof that these append-only controls overwrote earlier bytes. The counter compares against `seed + fragment`, but here gate output was already appended before the counter's fragment; the expected prefix therefore fails (`c1-count.py:157-167,227-245`). Do not claim destructive rewriting from that label alone.

**Smallest safe correction [INFERENCE]:** keep the original delimiter semantics, open the manifest for append, take exclusive `flock(2)` on that open file before the last-byte probe, and retain that lock through writing the JSON line. Timing spread, re-probing, `sync`, and a single append `printf` do not supply that mutual exclusion. This is a fixable implementation defect, not a tradeoff to admit against the frozen contract (`claims.md:23-28,36-40`). No correction was implemented or candidate-scored in this seat.

## Provenance and exact scratch changes

Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Scratch root: `/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB`.
Receipt root: `.ufo/waves/round-32/w1/CtlC1JitterB/` relative to the lane.

Read `corpus/evidence/round32/claims.md` first, then both counter docstrings. Relevant frozen predicate/evidence locations: `claims.md:14-47`; C1 trial/check contract `c1-count.py:2-46`; per-trial serialization and manifest checks `:157-247`; output and receipt construction `:298-326`.

Identity commands, each exit 0:

```sh
timeout 15s sha256sum tools/research-gate.sh corpus/evidence/round32/c1-count.py corpus/evidence/round32/c2-count.py
timeout 15s git show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c1-count.py | timeout 15s sha256sum
```

Observed hashes:

- Base gate: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`, matching `claims.md:3-4`.
- C1 counter, working file and frozen commit: `9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885`. Every receipt carries this hash.
- C2 counter, read only: `b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c`.

Each control began with `timeout 15s cp -- /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh <scratch-path>` (exit 0), followed only by the append-block change below. No locks were added and no other gate behavior was intentionally changed.

### a — `/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/a-random-sleep.sh`

Inserted immediately before the original last-byte probe, now lines 3192–3193:

```bash
    local jitter_ms=$((RANDOM % 2001))
    sleep "$((jitter_ms / 1000)).$(printf '%03d' "$((jitter_ms % 1000))")"
```

The interval is 0.000–2.000 seconds at millisecond granularity. Original probe and append remain afterward. SHA-256: `2b1f52fdf5284459a5808c83ebcb2bb812bb1350f1366d52956845c3515c776d`.

### b — `/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/b-second-probe.sh`

Inserted after the original probe and before its delimiter decision, lines 3196–3200:

```bash
    sleep 0.2
    jlast=''
    if [[ -s $JSON_ARG ]]; then
      jlast=$(tail -c1 -- "$JSON_ARG" 2>/dev/null | od -An -tx1 | tr -d ' \n' || true)
    fi
```

The existing decision uses this second value, not the first. SHA-256: `591cc341c5080c9a84d5f0675c536ad1c017d5d709dbb17a3cbdaacb4c1ce6e9`.

### c — `/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/c-sync-printf.sh`

Replaced the probe/decision/append statement with the following, lines 3192–3202; existing append-error handling remains:

```bash
    sync
    if ! printf '%s\n' "$(
      local jlast=''
      if [[ -s $JSON_ARG ]]; then
        jlast=$(tail -c1 -- "$JSON_ARG" 2>/dev/null | od -An -tx1 | tr -d ' \n' || true)
      fi
      if [[ -n $jlast && $jlast != 0a ]]; then
        printf '\n'
      fi
      printf '%s' "$line"
    )" >>"$JSON_ARG"; then
```

There is one `printf` redirected to the manifest; the inner `printf`s construct its argument after `sync`. The inserted delimiter is not stripped by command substitution because JSON follows it. This does not claim an atomic probe-and-write syscall. SHA-256: `46a6e487a42358cb45195ea7509460de5176c5e802cebf56bf030213fa3dbbb8`.

Control hashes were recorded with:

```sh
timeout 15s sha256sum /fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/a-random-sleep.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/b-second-probe.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/c-sync-printf.sh
```

Exit 0; receipt `gate_sha256` fields match the recorded values.

## Exact scoring commands and receipts

All six calls were issued concurrently, with lane-root cwd, no background jobs or subagents. Each command exited **1** (counter miss). The wrapper limits were 850 seconds, 2 GiB address space per process, 2,000 processes, and 1 MiB per file. `C1_TMP` and `TMPDIR` both named this seat's scratch directory; inherited Git-location variables were removed.

```sh
timeout --signal=INT --kill-after=30s 850s prlimit --nproc=2000 --as=2147483648 --fsize=1048576 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/a-random-sleep.sh --seed 20261023320121 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1JitterB/a-s20261023320121.json

timeout --signal=INT --kill-after=30s 850s prlimit --nproc=2000 --as=2147483648 --fsize=1048576 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/a-random-sleep.sh --seed 20261023320122 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1JitterB/a-s20261023320122.json

timeout --signal=INT --kill-after=30s 850s prlimit --nproc=2000 --as=2147483648 --fsize=1048576 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/b-second-probe.sh --seed 20261023320131 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1JitterB/b-s20261023320131.json

timeout --signal=INT --kill-after=30s 850s prlimit --nproc=2000 --as=2147483648 --fsize=1048576 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/b-second-probe.sh --seed 20261023320132 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1JitterB/b-s20261023320132.json

timeout --signal=INT --kill-after=30s 850s prlimit --nproc=2000 --as=2147483648 --fsize=1048576 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/c-sync-printf.sh --seed 20261023320141 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1JitterB/c-s20261023320141.json

timeout --signal=INT --kill-after=30s 850s prlimit --nproc=2000 --as=2147483648 --fsize=1048576 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1JitterB/c-sync-printf.sh --seed 20261023320142 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1JitterB/c-s20261023320142.json
```

The count/per-class lines printed by these commands are represented verbatim in value by the result table above. Receipt elapsed times, in command order: 57.425, 49.009, 9.241, 9.274, 6.826, 4.721 seconds.

## Per-trial lines

The following lines are a rendering of each named receipt's complete `trials` array. Trial ids are zero-based; PASS means an empty failure array. Failure names are copied exactly.

### a-s20261023320121.json — APPEND_SERIALIZED=11/24 — MISSES

```text
trial=0 F_unterminated PASS
trial=1 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=2 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=3 F_unterminated PASS
trial=4 F_unterminated PASS
trial=5 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=6 L_unterminated FAIL appended-under-cooperating-lock
trial=7 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=8 F_unterminated PASS
trial=9 F_unterminated PASS
trial=10 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=11 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=12 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=13 F_unterminated PASS
trial=14 F_unterminated PASS
trial=15 F_unterminated PASS
trial=16 F_unterminated FAIL blank-line,invalid-json-line
trial=17 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=18 L_unterminated FAIL appended-under-cooperating-lock
trial=19 F_unterminated PASS
trial=20 F_unterminated PASS
trial=21 L_unterminated FAIL appended-under-cooperating-lock
trial=22 L_unterminated FAIL appended-under-cooperating-lock
trial=23 F_unterminated PASS
```

### a-s20261023320122.json — APPEND_SERIALIZED=12/24 — MISSES

```text
trial=0 L_unterminated FAIL appended-under-cooperating-lock
trial=1 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=2 F_unterminated PASS
trial=3 F_unterminated PASS
trial=4 F_unterminated PASS
trial=5 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=6 F_unterminated PASS
trial=7 F_unterminated PASS
trial=8 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=9 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=10 F_unterminated PASS
trial=11 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=12 F_unterminated PASS
trial=13 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=14 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=15 F_unterminated PASS
trial=16 L_unterminated FAIL appended-under-cooperating-lock
trial=17 L_unterminated FAIL appended-under-cooperating-lock
trial=18 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=19 F_unterminated PASS
trial=20 F_unterminated PASS
trial=21 F_unterminated PASS
trial=22 L_unterminated FAIL appended-under-cooperating-lock
trial=23 F_unterminated PASS
```

### b-s20261023320131.json — APPEND_SERIALIZED=7/24 — MISSES

```text
trial=0 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=1 F_unterminated PASS
trial=2 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=3 F_unterminated PASS
trial=4 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=5 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=6 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=7 F_unterminated FAIL blank-line,invalid-json-line
trial=8 L_unterminated FAIL appended-under-cooperating-lock
trial=9 F_unterminated PASS
trial=10 F_unterminated FAIL blank-line,invalid-json-line
trial=11 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=12 F_unterminated FAIL blank-line,invalid-json-line
trial=13 F_unterminated FAIL blank-line,invalid-json-line
trial=14 F_unterminated PASS
trial=15 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=16 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=17 F_unterminated FAIL blank-line,invalid-json-line
trial=18 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=19 F_unterminated PASS
trial=20 F_unterminated PASS
trial=21 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=22 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=23 F_unterminated PASS
```

### b-s20261023320132.json — APPEND_SERIALIZED=7/24 — MISSES

```text
trial=0 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=1 F_unterminated PASS
trial=2 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=3 F_unterminated FAIL blank-line,invalid-json-line
trial=4 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=5 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=6 F_unterminated FAIL blank-line,invalid-json-line
trial=7 F_unterminated FAIL blank-line,invalid-json-line
trial=8 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=9 F_unterminated PASS
trial=10 F_unterminated PASS
trial=11 L_unterminated FAIL appended-under-cooperating-lock
trial=12 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=13 F_unterminated FAIL blank-line,invalid-json-line
trial=14 F_unterminated FAIL blank-line,invalid-json-line
trial=15 F_unterminated PASS
trial=16 L_unterminated FAIL appended-under-cooperating-lock
trial=17 F_unterminated PASS
trial=18 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=19 F_unterminated PASS
trial=20 L_unterminated FAIL appended-under-cooperating-lock
trial=21 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=22 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=23 F_unterminated PASS
```

### c-s20261023320141.json — APPEND_SERIALIZED=1/24 — MISSES

```text
trial=0 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=1 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=2 F_unterminated FAIL blank-line,invalid-json-line
trial=3 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=4 F_unterminated FAIL blank-line,invalid-json-line
trial=5 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=6 F_unterminated FAIL blank-line,invalid-json-line
trial=7 F_unterminated PASS
trial=8 F_unterminated FAIL blank-line,invalid-json-line
trial=9 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=10 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=11 F_unterminated FAIL blank-line,invalid-json-line
trial=12 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=13 F_unterminated FAIL blank-line,invalid-json-line
trial=14 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=15 F_unterminated FAIL blank-line,invalid-json-line
trial=16 F_unterminated FAIL blank-line,invalid-json-line
trial=17 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=18 F_unterminated FAIL blank-line,invalid-json-line
trial=19 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=20 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=21 F_unterminated FAIL blank-line,invalid-json-line
trial=22 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=23 F_unterminated FAIL blank-line,invalid-json-line
```

### c-s20261023320142.json — APPEND_SERIALIZED=1/24 — MISSES

```text
trial=0 F_unterminated FAIL blank-line,invalid-json-line
trial=1 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=2 F_unterminated PASS
trial=3 F_unterminated FAIL blank-line,invalid-json-line
trial=4 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=5 F_unterminated FAIL blank-line,invalid-json-line
trial=6 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=7 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=8 F_unterminated FAIL blank-line,invalid-json-line
trial=9 F_unterminated FAIL blank-line,invalid-json-line
trial=10 F_unterminated FAIL blank-line,invalid-json-line
trial=11 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=12 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=13 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
trial=14 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=15 F_unterminated FAIL blank-line,invalid-json-line
trial=16 F_unterminated FAIL blank-line,invalid-json-line
trial=17 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=18 L_unterminated FAIL appended-under-cooperating-lock,blank-line,invalid-json-line
trial=19 L_terminated FAIL appended-under-cooperating-lock,prefix-rewritten
trial=20 F_unterminated FAIL blank-line,invalid-json-line
trial=21 F_unterminated FAIL blank-line,invalid-json-line
trial=22 F_unterminated FAIL blank-line,invalid-json-line
trial=23 L_empty FAIL appended-under-cooperating-lock,prefix-rewritten
```

## Limits, safety, and cleanup evidence

- `timeout 15s df -h /fast` exited 0 before fixture writes: 804G size, 568G used, 236G available, 71% utilization.
- `timeout 15s stat --printf='%n %s bytes\n' <the three control paths and six receipt paths listed above>` exited 0. Controls are 306731, 306770, and 306665 bytes; receipts are 3842, 3795, 4155, 4069, 4479, and 4479 bytes. Every artifact is below 1 MiB.
- After all scoring calls completed, `timeout 15s pgrep -af /fast/scratch/hyaku/chousa-r32/w1/CtlC1Jitter[B]` exited 1 with no output: no matching owned counter/gate process remained. Counter cleanup is also explicit at `c1-count.py:246-247,296-297`.
- All six calls requested a PTY; the tool reported it unavailable and ran without a terminal. Each call completed within 60 seconds. The parameter/behavior mismatch was reported through `xd://report_issue`; no background jobs were started by this seat.
- Gate controls are scratch-only. No production file, counter, Git index, jj state, fleet file, or sibling artifact was edited. No network access, installs, service changes, candidate scoring, selftest, or additional verification suite was performed.
- Counts describe these exact concurrent runs, not stable probabilities or a controlled performance comparison. Sleep randomness and scheduling are not fixed by the counter seed. No claim is made about C2 or unmeasured no-harm surfaces.
