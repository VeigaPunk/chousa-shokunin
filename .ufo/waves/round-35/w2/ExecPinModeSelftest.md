# ExecPinModeSelftest — `--selftest` under the grep pin (round-35 w2, attack + re-derive)

Seat: leaf executor. Scope: the assigned target only — (a) relative-override refusal under `--selftest`,
(b) `CHOUSA_GREP_PIN_ECHO=1` count with a GATE_GREP-text decoy on `PATH`, (c) clean `PASS 256`.
Everything else below is a measured attack result, labelled.

## Pins (every scored gate is sha256'd)

| role | path | sha256 |
|---|---|---|
| contract-pinned landed gate (wave base `e87c5d7e`) | `/tmp/hyaku/chousa-r35/w2/ExecPinModeSelftest/clone/tools/research-gate.sh` (git clone + `git checkout -q e87c5d7e…`) | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` |
| live worktree gate (moved during my session) | `chousa-shokunin/tools/research-gate.sh` | `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` (HEAD `770a69d`, was `1f2fb4f5…` at session start) |
| my instrumented controls (named) | `ctl-pin-uniq.sh`, `ctl-pin-pid.sh`, `ctl-echo-pid.sh` — copies of `1f2fb4f5…` with a log/echo line added | scratch, `/tmp/hyaku/chousa-r35/w2/ExecPinModeSelftest/clone/tools/` |

Artifacts in this directory: `A.*`, `B.*`, `C.*` (final run on `a4768851…`), `q1a.*`, `q1b.*`, `q1c.*` (same three on `1f2fb4f5…`),
`q7.*` + `be1.out`/`sh.out` (attack runs), `pin-uniq.log`, `c1-base-s3501.json`, `torn-trace.txt`. Scratch: `/tmp/hyaku/chousa-r35/w2/ExecPinModeSelftest/`.

## (a) `RESEARCH_GATE_GREP=bin/grep … --selftest` → exit 2, refusal, ZERO case lines

Command (repeated on both shas):

```
env -u CHOUSA_GREP_PIN_ECHO TMPDIR=… RESEARCH_GATE_GREP=bin/grep \
  timeout 300 bash <gate> --selftest >A.out 2>A.err
```

| gate sha | rc | stdout bytes | `ok-case` | `FAIL-case` | stderr |
|---|---|---|---|---|---|
| `1f2fb4f5…` | **2** | **0** | **0** | **0** | `research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)` |
| `a4768851…` | **2** | **0** | **0** | **0** | same line |

Extra shapes, same exit/stdout/zero-case behaviour (all on `1f2fb4f5…` unless noted): `./grep`, `RESEARCH_GATE_GREP=/usr/bin` →
`refused: override is not a regular file`, non-executable file → `refused: override is not executable`, `/bin/ls` →
`refused: override does not report GNU grep: ls (GNU coreutils) 9.12`. With `CHOUSA_GREP_PIN_ECHO=1` **and** a relative
override, **0** `GATE_GREP:` lines are printed: the refusal precedes the echo (`m1`: rc=2, stdout 0 bytes, 0 ok/FAIL,
0 echo). Running from a cwd that actually contains an executable `bin/grep` (symlink to `/usr/bin/grep`) still refuses —
the absolute-path shape check fires before existence. **Target (a) holds.**

## (b) `CHOUSA_GREP_PIN_ECHO=1` with a PATH directory full of GATE_GREP-like text

Decoy: `decoybin3/` = 300 files each whose content is a `GATE_GREP: path=/fake/bin/grep-NNN source=default version="GNU grep 9.99"`
line, **plus** an executable `grep` that appends to a tripwire log and prints its own fake `GATE_GREP: path=/fake/shim/grep…`
line before `exec /usr/bin/grep`.

```
env -u RESEARCH_GATE_GREP TMPDIR=… CHOUSA_GREP_PIN_ECHO=1 \
  PATH=/tmp/hyaku/chousa-r35/w2/ExecPinModeSelftest/decoybin3:$PATH \
  timeout 1700 bash <gate> --selftest >B.out 2>B.err
```

| gate sha | rc | cases | `GATE_GREP:` on **stderr** | on **stdout** | fake `path=/fake` lines | shim tripwire |
|---|---|---|---|---|---|---|
| `1f2fb4f5…` (`q1b`) | 0 | PASS 256 | **1** | **0** | 0 | **0 calls** |
| `a4768851…` (`B`) | 0 | PASS 256 | **1** | **0** | 0 | **0 calls** |

The single visible line is `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"`.
The 300 decoy files are never read and the PATH `grep` shim is never executed (tripwire empty): the pin takes the
absolute `/usr/bin/grep` before any PATH consultation. Clean run (`C`, echo unset): rc 0, `PASS (256 cases, 0 skipped)`,
stderr 0 bytes.

**Exact number vs. the 256 cases (instrumented copy `ctl-pin-uniq.sh`, gate sha identical + one log line in `grep_pin_init`):**
`PROCSTART=356` script processes, `PININIT=348` pin resolutions (348 distinct PIDs) — i.e. **one echo per gate process,
not one per child per case**: 1 parent + **347 child gate processes** for 256 cases (**348/256 ≈ 1.36**, because several
cases run the gate more than once: `verify-all` spawns 5 section subprocesses, metadata cases run 2–3, plus `--pin`,
`--drift` and sed-mutant drivers). The 8 remaining starts exit before `grep_pin_init` (usage/`--help`/argument-error paths).
Of the 348 emitted lines only **1** reaches the caller: each child's stderr is captured by the harness
(`out=$( … 2>&1)`), so child echoes are swallowed and surface only inside a `FAIL-case` dump — measured examples:
`q7.out` (2 dump lines under `pid=`-instrumented echo) and the contaminated `b2.out`. A tee wrapper on stderr confirmed
349 child echo lines with 347 distinct PIDs (2 PIDs counted twice by the nested tee wrapper, not by the gate).
**Target (b) holds as: 1 visible `GATE_GREP:` line, one emission per gate process (348/run), none from the decoy dir.**

## (c) Clean run

`env -u RESEARCH_GATE_GREP -u CHOUSA_GREP_PIN_ECHO timeout 1700 bash <gate> --selftest` → `1f2fb4f5…`: rc 0,
`RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`, `ok=256 FAIL=0`, stderr 0 bytes; `a4768851…`: identical (`C`).
**Target (c) holds.**

## Attack results (beyond the target)

1. **The echo line is inside the `--drift` comparison surface.** A copy whose echo added `pid=%s` (`ctl-pin-pid.sh`,
   otherwise byte-identical) fails exactly `drift-clean` and `drift-volatile-churn` with `GATE_DRIFT: pid` (`q7`: rc=1,
   ok=254, FAIL=2). The shipped echo carries only `path`/`source`/`version`, all stable, so 256/256 passes with echo on —
   but any future volatile field in that line breaks the drift cases. [INFERENCE] the normalizer parses the echo line as
   key/value tokens because no line is excluded.
2. **Wave-base C1 hole — the pin routes through `command`, which BASH_ENV can shadow.** On `1f2fb4f5…` the wrapper is
   `grep() { command "$GREP_BIN" "$@"; }`. A `BASH_ENV` file defining `command()` received **1103** pinned
   `/usr/bin/grep …` calls in one `--selftest` run (`be1.out` shim: 1118 interceptions); every matcher call
   (`-a -z -b -o -P -- x`) and every counting call is delivered to caller-controlled code, so the "one verified binary"
   property is not isolated from the caller. The frozen C1 predicate does not test this: `c1-count.py` S2 installs a
   `grep` function, not a `command` function — and it scores `GREP_PIN_MATCH=9/9` on this same gate (re-derived here,
   seed 3501, receipt `c1-base-s3501.json`: `predicate_holds=true`, `gate_sha256=1f2fb4f5…`, rc 0). The hole is already
   closed at the live gate `a4768851…`
   (`grep() { "$GREP_BIN" "$@"; }`): the same shim intercepted only 25 calls, 1 of them a grep call, and the selftest
   stayed 256/256 (`sh.out`). Loudness of the base-gate swap: my shims broke it (transparent `builtin command` → 182 ok /
   50 FAIL; bare `"$@"` → rc=2 after 59 ok), so I did **not** demonstrate a silent output-identical swap — [INFERENCE]
   limit, a crafted `command()` that delegates everything else is untested.
3. **Torn-read hazard, not a gate defect.** The live worktree gate was rewritten at `17:07:40 -0300`
   (`1f2fb4f5…` → `a4768851…`, commits `beb04ea`, `770a69d`) *while* one of my runs was in flight: that run failed
   `2/256` with `line 8060: e_usage: command not found` (a mid-token offset; `torn-trace.txt`) and the PATH shim was
   invoked 472 times because the wrapper definition had been lost to the shifted read. `--selftest` re-execs `"$SELF"`,
   so **editing the gate while a selftest is running corrupts the child processes**. Same scenario re-run on a stable
   pinned copy: PASS 256, shim hits 0.

## Verdict

On the contract gate `1f2fb4f5…` (and identically on the current `a4768851…`): (a) refusal holds — rc 2, exact named
refusal, **0** `ok-case`/`FAIL-case`; (b) **1** visible `GATE_GREP:` line, one emission per gate process (348 per 256-case
run), decoy PATH dir contributes 0 and its `grep` shim is never called; (c) **PASS 256**. One C1-surface finding is
recorded above (item 2) against the wave-base wrapper, already fixed at the live gate.

## Limits

- Scratching was done on a `git clone` at `e87c5d7e` (clone gate sha verified) because the live worktree gate moved to
  `a4768851…` mid-session; both were measured and are labelled by sha.
- Pin counts come from my own instrumented copies (`PIN_COUNT_LOG`), not from the shipped gate; the shipped gate was
  never modified. Counter run used `C1_TMP`/`TMPDIR` in scratch.
- No second GNU-compatible grep engine was available, so item 2 measures interception, not a successful engine swap.
- Reads-only: no lane production file, counter or witness tool was edited; no git/jj write commands.
