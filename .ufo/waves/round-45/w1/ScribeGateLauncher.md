# ScribeGateLauncher — round 45 wave 1

## Assignment and axes

Draft the missing SKILL.md Gates row for `tools/parent-lifetime.sh` as specified for the post-C1 contract; read the frozen claims and current pre-fix launcher; read the Gates conventions and each listed counter's docstring/argparse and claims/verdict; run each listed counter once read-only from lane root; record exact command output and exit code. Axes: operability (C1), calibration (C2), depth (C3).

## Provenance and commands

All source paths below are absolute. No installs, network access, product changes, or lane writes were performed by this seat. The only writes were this report. Counter commands were run with cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

- `read skill://godspeed`: returned the Godspeed posture and action guidance.
- `read /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh`: observed pre-fix script. It defaults `TIMEOUT=420`, does not require `--timeout`, writes start without `timeout_s`, and exits 0 after end regardless of zero tasks or timeout exit status. It checks captured child PID and parent PID. Relevant ranges 11–15, 17–38, 40–50, 51–84, 87–108.
- `read /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round45/claims.md`: frozen R45-C1 target, control, and target result at lines 19–39; C2 at lines 41–69; C3 at lines 71–107. C1 requires cases a–e and `CASES_MATCH=5/5`, `C1=PASS`, exit 0; control is round44 tool `CASES_MATCH=1/5`, exit 1. C2 target `UNREGISTERED=0`, `C2=PASS`, exit 0; freeze control has 26 unregistered, while claim notes freeze-tree count 29 after all three new counters exist. C3 targets are recorded below.
- `read /home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md:75-105`: Gates heading/table at lines 75–78, canonical examples including `research-gate round-37 counters` at line 95. Table has eight columns; rows use backtick paths, `exit 0` etc., control/measurement and write scope, owner `chousa`.
- `read /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round45/c1-count.py`: docstring gives frozen C1 predicate and return mapping; argparse `--tool`; implementation prints individual cases, total, then C1 verdict.
- `read /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round45/c2-count.py`: docstring gives C2 predicate and return mapping; argparse `--root`, `--skill`, `--list`; output reports entry points, Gates rows, registered, unregistered, verdict.
- `read /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round45/c3-count.py`: docstring gives C3 predicate, `--lane-only`, and return mapping; argparse `--root`, `--cache`, `--lane-only`; output includes all counts and verdict.
- `glob /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round45/*SCORECARD*`: no files found. Directory listing confirmed round45 has claims, counters, controls, and no SCORECARD.md. Thus there is no separate SCORECARD verdict to consult; frozen claims provide the target/control verdicts.
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --short && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log -1 --format='%H %s'` output began with measured HEAD `d82cec904bf0fb8736886b9f17be913c7807427a`; subject `round-45: freeze three claims (launcher exit contract, Gates-registry mismatches, AVeriTeC archive-field adoption) and score their controls before any seat`. Status listed pre-existing modifications/untracked artifacts; none were changed by this seat.

### Counter run evidence

1. Command: `python3 corpus/evidence/round45/c1-count.py; printf 'EXIT=%s\\n' "$?"`

Verbatim output:
```text
CASE a_empty_exits_3=FAIL
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=FAIL
CASE d_no_timeout_exits_2=FAIL
CASE e_start_timeout_s=FAIL
CASES_MATCH=1/5
C1=FAIL
EXIT=1
```

2. Command: `python3 corpus/evidence/round45/c2-count.py --list; printf 'EXIT=%s\\n' "$?"`

Verbatim output:
```text
UNREGISTERED_PATH corpus/evidence/round31/c1-count-v3.py
UNREGISTERED_PATH corpus/evidence/round31/c1-count.py
UNREGISTERED_PATH corpus/evidence/round31/c2-count-v3.py
UNREGISTERED_PATH corpus/evidence/round31/c2-count.py
UNREGISTERED_PATH corpus/evidence/round32/c1-count.py
UNREGISTERED_PATH corpus/evidence/round32/c2-count.py
UNREGISTERED_PATH corpus/evidence/round33/c1-count-v3.py
UNREGISTERED_PATH corpus/evidence/round33/c1-count.py
UNREGISTERED_PATH corpus/evidence/round34/c1-count-v2.py
UNREGISTERED_PATH corpus/evidence/round34/c1-count.py
UNREGISTERED_PATH corpus/evidence/round40/c1-count.py
UNREGISTERED_PATH corpus/evidence/round40/c2-count.py
UNREGISTERED_PATH corpus/evidence/round41/c1-count.py
UNREGISTERED_PATH corpus/evidence/round41/c2-count.py
UNREGISTERED_PATH corpus/evidence/round42/c1-count.py
UNREGISTERED_PATH corpus/evidence/round42/c2-count.py
UNREGISTERED_PATH corpus/evidence/round43/c1-count.py
UNREGISTERED_PATH corpus/evidence/round43/c2-count.py
UNREGISTERED_PATH corpus/evidence/round43/c3-count.py
UNREGISTERED_PATH corpus/evidence/round44/c1-count.py
UNREGISTERED_PATH corpus/evidence/round44/c2-count.py
UNREGISTERED_PATH corpus/evidence/round44/c3-count.py
UNREGISTERED_PATH corpus/evidence/round44/errata-count.py
UNREGISTERED_PATH corpus/evidence/round45/c1-count.py
UNREGISTERED_PATH corpus/evidence/round45/c2-count.py
UNREGISTERED_PATH corpus/evidence/round45/c3-count.py
UNREGISTERED_PATH tools/absent-split.py
UNREGISTERED_PATH tools/parent-lifetime.sh
UNREGISTERED_PATH tools/quarantine-check.py
ENTRY_POINTS=54
GATES_ROWS=18
REGISTERED=25/54
UNREGISTERED=29
C2=FAIL
EXIT=1
```

3. Command: `python3 corpus/evidence/round45/c3-count.py; printf 'EXIT=%s\\n' "$?"`

Verbatim output:
```text
ENTRIES=0/2
CITES_BOUND=0/3
QUOTES_IN_SPAN=0/4
QUOTES_IN_ENTRY=0/4
COUNTS_IN_ENTRY=0/7
CAPTURE_BOUND=0/4
COUNTS_REDERIVED=0/7
C3=FAIL
EXIT=1
```

4. Command: `python3 corpus/evidence/round45/c3-count.py --lane-only; printf 'EXIT=%s\\n' "$?"`

Verbatim output:
```text
ENTRIES=0/2
CITES_BOUND=0/3
QUOTES_IN_SPAN=0/4
QUOTES_IN_ENTRY=0/4
COUNTS_IN_ENTRY=0/7
CAPTURE_BOUND=skipped
COUNTS_REDERIVED=skipped
C3=FAIL
EXIT=1
```

## Draft row (not applied)

The requested C1 row is drafted below using the specified post-C1 behavior and observed control. Its C1 expected target is a forecast from the frozen claim, not a measured landed-C1 execution; current pre-fix counter observation is recorded above. All three round45 counters appear in the entry cell so this single row registers them for C2. C3's measured current state is fail as shown above; no successor supersedes these round45 counters. `SCORECARD.md` was absent.

```text
| `parent-lifetime.sh` / round-45 counters | gate | `bash tools/parent-lifetime.sh --dispatch JSON --receipt PATH --agent FILE --timeout SECS` · `bash tools/parent-lifetime.sh --selftest --receipt PATH` · `python3 corpus/evidence/round45/c1-count.py` · `python3 corpus/evidence/round45/c2-count.py --list` · `python3 corpus/evidence/round45/c3-count.py` · `python3 corpus/evidence/round45/c3-count.py --lane-only` | `parent-lifetime.sh`: exit 0 only when `n_spawned>0`, `n_spawned=n_reaped` and no seat exited 124/137; exit 3 after end line if zero tasks spawned or a seat timed out; exit 1 if child PID not captured or parent PID changed; exit 2 usage (including dispatch without `--timeout`), start `start parent_pid=… epoch=… timeout_s=…`. `c1-count.py`: exit 0 `CASES_MATCH=5/5 C1=PASS`; exit 1 otherwise; exit 2 usage/env. `c2-count.py`: exit 0 `UNREGISTERED=0 C2=PASS`; exit 1 any entry point unregistered; exit 2 usage/env. `c3-count.py`: exit 0 default `ENTRIES=2/2 CITES_BOUND=3/3 QUOTES_IN_SPAN=4/4 QUOTES_IN_ENTRY=4/4 COUNTS_IN_ENTRY=7/7 CAPTURE_BOUND=4/4 COUNTS_REDERIVED=7/7 C3=PASS`, `--lane-only` same first five values, capture lines `skipped`, `C3=PASS`; exit 1 count failure; exit 2 usage/env. | Self-test `python3 corpus/evidence/round45/c1-count.py` target `CASES_MATCH=5/5 C1=PASS`; control `corpus/evidence/round45/controls/c1-control-r44-tool.txt` observed `CASES_MATCH=1/5 C1=FAIL`, exit 1. C2 control `corpus/evidence/round45/controls/c2-control-base.txt` reports `UNREGISTERED=26 C2=FAIL`, exit 1; C3 control `corpus/evidence/round45/controls/c3-control-do-nothing.txt` reports all-zero counts, `C3=FAIL`, exit 1. | measured lane commit `d82cec904bf0fb8736886b9f17be913c7807427a` (pre-C1; frozen claims); measured current: C1 `1/5`, C2 `UNREGISTERED=29`, C3 default/`--lane-only` `C3=FAIL` | `tools/parent-lifetime.sh` writes the caller-supplied receipt and sibling `seat-logs/`; counters use temporary directories/read-only lane inputs; no network | chousa |
```

## Verdict and limits

Current pre-fix launcher is not compliant with frozen C1 and the C1 counter observes `1/5` (only successful two-seat case). The measured frozen tree is C2 `UNREGISTERED=29`; C3 counter observes no adopted entries and fails in both modes. The row is a draft only, not written to `SKILL.md`; this seat did not run the requested post-fix launcher self-test because the launcher is still pre-fix. Explicit assignment scope here was the draft/research/report, not production editing. No report claim upgrades expected post-fix behavior into execution evidence.
