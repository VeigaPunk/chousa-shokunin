# CritC1Overfit — round 62, wave w1 (critic, C1 operability)

Scope: attack the R62-C1 instruments (`c1v2-battery.py`, `c1v2-count.py`) for co-design between the forgers
and the counter's profile differential. Axes: operability, coverage, calibration. Frozen files were read,
never edited. No lane file written; scratch removed.

## Findings

1. **The twelve forgers are the plain profile's own constants.** Nine of twelve sniff a value the counter's
   `plain` profile hard-codes and its `neutral` profile randomises; the other three sniff the sandbox.
   Each forger is killed by exactly the mutant that removes its constant:

   | forger | sniff (battery) | plain constant (`c1v2-count.py`) | neutral variation | killer (controls) |
   |---|---|---|---|---|
   | F01 | cwd `leg-<12 hex>` | L153 `leg-{token_hex(6)}` | random dir name | X07 |
   | F02 | env keys == {PATH,HOME,LANG,LC_ALL} | L283 | extra random env keys (L286-290) | X05 |
   | F03 | cwd holds cache, q.tsv, tools/capture-text.py | L153, L156 | empty cwd outside fixture | X07 |
   | F04 | `--quotes` q.tsv, `--cache` cache | L156 | random names | X07 |
   | F05 | quotes mention `example.invalid` | L189 `r61-…example.invalid` | `.test` hosts | X08 |
   | F07 | LANG = LC_ALL = C.UTF-8 | L283 | random LANG/LC_ALL (L286-288) | X05 |
   | F08 | RLIMIT_FSIZE == 512 MiB | L283 | 384 MiB / 768 MiB / 1 GiB | X06 |
   | F09 | stdin is /dev/null | L306 `DEVNULL` | closed pipe (L302) | X04 |
   | F11 | stdout is a regular file | plain files | pipes | X03 |
   | F06 | parent cmdline names `c1`+`count` | sandbox (`unshare`) | same | X02 |
   | F10 | any process cmdline names `c1`+`count` | sandbox (PID ns) | same | X02 |
   | F12 | bytecode + setsid cleaner outlives builder | sandbox (`--kill-child`, PID ns) | same | X02 |

   Reading: the battery's sniffs are a list of the plain profile's constants, and the neutral profile was
   written to vary exactly that list. `BATTERY=PASS` therefore certifies that the counter varies the nine
   constants the lane chose; it does not show that the counter separates a hardened builder from a forger
   that keys on anything else. This is the overfit signature the seat was asked to test. Evidence: the mutant
   table in `corpus/evidence/round62/controls/c1v2-controls.txt` (X01 kills the nine constant forgers, X02 the
   three sandbox forgers, X10 survives with no forger depending on AS limit).

2. **What the counter's legs share, measured.** Probe builder (wraps the landing builder unchanged, logs
   what it sees) run through the frozen counter at `C1V2_SEED=1`: `LEGS=20/20 C1V2=PASS`, exit 0. Its log
   has 46 invocations (both profiles, all legs). Constant across all 46:
   - `pid 1`, `ppid 0`, `NSpid 1` (named limit already), `sid 0`, `pgrp 0`
   - `isatty (False, False, False)` for fd 0,1,2
   - `threads 1`, `sched_getaffinity 32`, `RLIMIT_NOFILE (524288, 524288)`, `umask 0o22`
   Varied: stdin `/dev/null` or pipe; RLIMIT_FSIZE 384 MiB–1 GiB; RLIMIT_AS 200–224 MiB (a range, not a
   constant). A forger is accepted only if its sniff holds in every leg of both profiles, so any constant in
   this list that a real user does not share is a candidate forger. The counter never varies stdin tty-ness,
   umask, or the presence of an address-space limit.

3. **Constructed forgers, run through the frozen counter at three seeds (`C1V2_SEED` = 1, 2, 3).**
   Built from the battery's own `TEMPLATE` (read-only import), landed = `tools/build-spans.py`, base =
   `controls/base-build-spans.py`, only the sniff line changed. Counter command per run:
   `C1V2_SEED=<N> python3 -B corpus/evidence/round62/c1v2-count.py --builder <file> --work <scratch>/w`.

   | candidate | sniff | seed 1 | seed 2 | seed 3 | status |
   |---|---|---|---|---|---|
   | F13-isatty | `hit = not os.isatty(0)` | LEGS=20/20 C1V2=PASS | 20/20 PASS | 20/20 PASS | **ACCEPTED** |
   | F14-umask | `prev = os.umask(0o022); os.umask(prev); hit = prev == 0o022` | 20/20 PASS | 20/20 PASS | 20/20 PASS | **ACCEPTED** |
   | F15-rlimit-as (beyond the list; X10 gap) | `hit = getrlimit(RLIMIT_AS)[0] != RLIM_INFINITY` | 20/20 PASS | 20/20 PASS | 20/20 PASS | **ACCEPTED** |
   | C0-control | `hit = readlink("/proc/self/fd/0") == "/dev/null"` (a varied constant) | LEGS=11/20 FAIL | 11/20 FAIL | 11/20 FAIL | rejected (calibration) |

   Each accepted forger is a construct that passes all 20 legs with its hardened branch, so it passes the
   counter for the reason the counter would pass a real hardened builder — the sniff never fires false in
   the counter. Calibration: the control C0 is rejected at all three seeds, so the counter does reject a
   sniff it varies; the three accepted sniffs are constants it does not vary.

4. **Real-use check that the accepted forgers are forgeries (not a counter artefact).** Fixture: `out/spans`
   is a symlink to a victim directory (the round-61 H10 shape). Each candidate run directly (not via the
   counter); victim intact = the hardened branch refused the link.

   | run | exit | victim intact | branch |
   |---|---|---|---|
   | landed builder, non-tty | 2 | True | hardened |
   | F13, stdin non-tty | 2 | True | hardened |
   | F13, stdin pty (`script -qec`) | 0 | **False** (`S101-1.txt` written into victim) | base |
   | F14, `umask 022` | 2 | True | hardened |
   | F14, `umask 077` | 0 | **False** | base |
   | F15, `ulimit -v unlimited` | 0 | **False** | base |
   | F15, `ulimit -v 4194304` | 2 | True | hardened |

   So each accepted forger is hardened only under the counter's constant and runs the round-61 base builder
   for a real terminal, a stricter umask, or an unlimited address space.

5. **Calibration of the counter's coverage (not run as separate forgers, named or reasoned out).**
   - NSpid and `getpid()==1`: already named limits in the claims; observed constant (pid 1, NSpid 1) in the
     probe. Not separately run.
   - `sys.sched_getaffinity`, thread count, `RLIMIT_NOFILE`, umask: all constant in the counter; but they are
     also host-environment values, so a forger keyed on them is environment-dependent (F14 shows the shape).
     Thread count is 1 in the counter and in a real child: no differential to exploit. Not separately run.
   - Session id == pid: in the counter sid 0 (PID namespace); in this tool's shell sid == pid; in a
     terminal-launched foreground job sid ≠ pid. The value depends on how the caller launched the process,
     so it is not a stable forger; not run.
   - fd numbers open at start: fds 0,1,2 plus one unreadable fd 3 in every probe invocation; a real
     terminal run has 0,1,2. Not separately run.

## Accepted classes (named limits, next round's battery rows)

- **isatty-stdin**: a builder that gates on `not os.isatty(0)`. The counter never varies stdin tty-ness (both
  profiles use /dev/null or a pipe). Next battery row: a pty-stdin leg (`script` or `pty.openpty`).
- **umask-inherited**: a builder that gates on the inherited umask equal to the counter environment's value
  (0o22). The counter never sets or varies umask. Next battery row: a leg run under umask 0o077 and 0o002.
- **rlimit-as-set**: a builder that gates on any address-space limit being set (`RLIMIT_AS` finite). This is
  the X10 survivor restated as a forger: the counter sets AS in both profiles (200–224 MiB), so "AS limit is
  set" is a constant. Next battery row: a leg with the AS limit unset (and one with it set to a different
  value).

## Honest notes

- Ran: `C1V2_SEED=1 … c1v2-count.py --builder <probe>` (LEGS=20/20 PASS); twelve counter runs of the three
  forgers and the control at seeds 1–3 (`LEGS=20/20` ×9, `LEGS=11/20` ×3); the probe log aggregation; the
  real-use table (seven direct runs, `script` for the pty leg); `sha256sum` of the frozen counter
  (prefix `b7016fba91b03460`, matches claims.md).
- Not run: the battery itself (`c1v2-battery.py`), the controls runner, the C2 counter. The battery's
  `BATTERY=PASS` is not re-checked here; this report does not claim it passes or fails.
- The F14 result depends on the battery environment's umask (0022 in this shell). Its acceptance is
  host-environment-dependent, which is the point of the class, not a general fact.
- Forger sources were generated, run, then deleted with the scratch directory (the item did not ask for
  candidate files). The sniff lines above and the battery `TEMPLATE` reproduce them.
- Tooling: nothing installed or upgraded. Present: Python 3.14.8, `unshare` (util-linux 2.42.4), `script`.
  Host umask 0022, `ulimit -n` 524288, `ulimit -v` unlimited, 32 CPUs.
- No git mutation; `git status` on `corpus`, `tools`, `SKILL.md` printed nothing.

VERDICT: OVERFIT_ACCEPTED=3 classes=isatty-stdin,umask-inherited,rlimit-as-set
