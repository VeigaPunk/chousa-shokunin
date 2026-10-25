# ReviewC1Rerun — C1 operability rerun (round 43, wave 1)

- seat: reviewer, leaf (`ReviewC1Rerun`); no subagent was dispatched
- date: 2026-10-24
- lane (read-only): `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- measured commit: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (`git rev-parse HEAD` matched; subject `round-43: split the absent class and adopt one locally re-opened search-log entry`)
- writes: this report only. No lane production file, lane git index, jj state, fleet repo, sibling repo, or `/home/vgpnk/Projects/shokuknow` was modified. No network. No tool install. Pacman not invoked. No model alias passed or hardcoded.
- search limit: content search was ripgrep regex (`Grep`), not a semantic index. Hits were then read. `Glob **/absent-split.py` returned one path: `tools/absent-split.py`.

## Axes

- operability: the frozen command runs, exits 0, and prints `C1=PASS` only if it executes `tools/absent-split.py` and that command's ids equal an independent read of the round-42 absent rows
- calibration: `C1=PASS` means the frozen C1 predicate, not ratio agreement (C2) and not "a mutant process was executed"
- depth: one canonical tool path, no same-file reroute, error preflight does not write, success path does not mutate the inputs it reads

## Verdict

**C1=PASS.** Exit code of the assigned command was **0**.

## Assigned command

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py; echo "EXIT_CODE=$?"
```

Interpreter: `/usr/bin/python3`, version `3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]`.

Full combined stdout (the `EXIT_CODE=` line is the wrapper, not the counter):

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=9 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
EXIT_CODE=0
```

Counter stdout is byte-identical to `corpus/evidence/round43/receipts/c1-after.txt` (sha256 `9553c682d8db8e7e367ad35d41e3636b70ee6f660b902557546362ce0527653c`). A later `subprocess` rerun of the same counter printed no stderr and exited 0 (`C1_EXIT 0`, `RECEIPT_MATCH True`).

`git status --porcelain` on `corpus/evidence/round43/c1-count.py`, `tools/absent-split.py`, `corpus/evidence/round42/quarantine-verdicts.tsv`, `corpus/evidence/round43/claims.md`, and `corpus/evidence/round43/receipts/c1-after.txt` was empty. The scored files are the measured commit, not a dirty overlay.

## What the pass is

Predicate R43-C1 (`corpus/evidence/round43/claims.md`) is: execute `tools/absent-split.py`, enumerate exactly the 15 absent ids of the committed round-42 table, each id exactly one of `{misquote, not-carried}`, both classes nonempty, two runs byte-identical. The 1/2 bound is not part of this predicate.

Independent read of `corpus/evidence/round42/quarantine-verdicts.tsv` (same split as `c1-count.py` `absent_ids` and `tools/absent-split.py` `absent_ids`: column 2 equals `absent`, header skipped):

```
ABSENT_COUNT 15
ABSENT_IDS S080 S082 S084 S086 S088 S093 S094 S104 S105 S108 S110 S111 S112 S114 S116
UNIQUE True
```

Two direct runs of `python3 tools/absent-split.py` (same `sys.executable`):

```
RUN1_EXIT 0
RUN1_STDERR_LEN 0
RUN1_STDOUT_LINES 15
RUN2_EXIT 0
RUN2_STDERR_LEN 0
RUN2_STDOUT_LINES 15
STDOUT_IDENTICAL True
STDERR_IDENTICAL True
STDERR_EMPTY True
IDS_EQUAL_TABLE True
CLASS_COUNTS {'not-carried': 6, 'misquote': 9}
```

Labels, table order: S080 not-carried, S082 not-carried, S084 misquote, S086 not-carried, S088 not-carried, S093 misquote, S094 misquote, S104 not-carried, S105 misquote, S108 misquote, S110 misquote, S111 misquote, S112 misquote, S114 not-carried, S116 misquote.

That is the frozen target: `ABSENT_ENUMERATED=15/15`, `CLASSED=15/15`, `BOTH_NONEMPTY=1/1`, `REPRODUCIBLE=1/1`, `MUTANT_DETECTED=1/1`, exit 0.

## Contract checks

Canonical runtime. The assigned absolute path is the only scorer invoked. `c1-count.py` sets `LANE` to `Path(__file__).resolve().parents[3]` (lane root for `corpus/evidence/round43/c1-count.py`) and runs `[sys.executable, str(LANE / "tools" / "absent-split.py")]`. The tool sets its own `LANE` to `parents[1]` of `tools/absent-split.py`, the same root. `Glob **/absent-split.py` found no second copy. The assimilation counter at `.ufo/waves/round-43/assimilation/validate/corpus/evidence/round43/c1-count.py` was not executed; it would resolve `parents[3]` to the validate tree, not reroute onto the lane tool. No same-identity reroute occurred on this run.

Callers. The only subprocess executor of `tools/absent-split.py` in the round-43 scoring surface is `c1-count.py` `run` (lines 45-48). `c2-count.py` line 10 states it does not require the tool; it reads `corpus/evidence/round43/absent-split.tsv` and does not call `subprocess`. `corpus/lessons/round-43.md` names the tool; it does not invoke it. Import of `tools/quarantine-check.py` is function definitions and constants only; `main` is guarded by `if __name__ == "__main__"`.

Error / preflight paths (source, not a second control run). Missing table: `c1-count.py` lines 65-67 print `C1=FAIL table-missing` and return 2 before `run`. Missing tool: lines 70-73 print `TOOL_PRESENT FAIL` and return 1 before `run`. Tool env failure: `absent-split.py` lines 114-116 write stderr and return 2 before the classify loop. Those branches contain no file write. This seat did not execute `--tool /tmp/no-such-absent-split.py`; that control is not claimed here. The committed control file `corpus/evidence/round43/controls/c1-control-before.txt` was read only.

Resume. Dispatch `counts.resume` is 0. This seat is `kind: spawn`. Neither counter nor tool has a resume/continuity path. A failed preflight returns before the child process and does not write. Success-path mutation check, measured around one more `absent-split.py` run (exit 0): register sha256 stayed `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` (size 83621); table, tool, and cache-directory `stat` unchanged; all 15 capture `.txt` and `.raw` pairs unchanged (sha256 and mtime_ns). Kinds were `page+text` or `page+pdf-text` for every id, so the tool's non-page reject (lines 131-133) did not drop a row. `absent-split.py` file writes found by regex are `sys.stderr.write` / `sys.stdout.write` only. `hashlib` is imported and unused.

## Findings by severity

No high or medium defect. The assigned command's `C1=PASS` and exit 0 match the frozen predicate and an independent enumeration.

### Low — `MUTANT_DETECTED` is not a mutant execution

`corpus/evidence/round43/c1-count.py` lines 89-91:

```python
short = ids[:-1]
check("MUTANT_DETECTED", short != expected, "short=%d expected=%d" % (len(short), len(expected)))
```

The live detail `short=14 expected=15` is that length compare on the successful 15-id list. A 14-element prefix cannot equal a 15-element expected list, so the check passes by construction whenever the tool emits 15 rows. It does not spawn a 14-row tool and does not feed a prefix to an acceptor. It also stays `1/1` on most failed enumerations (any id-list length other than 16). The comment above the check overclaims. This does not flip C1: the kill rule in `claims.md` is a missing id, an empty class, or two runs that differ, and those checks passed on real tool output. Do not read `MUTANT_DETECTED=1/1` as evidence a mutant was rejected.

## Residual risk

- `C1=PASS` is not a pure function of commit `737f40b` alone. Ids come from the lane table (clean at HEAD). Labels come from the absolute shokuknow register and `.qcache` named in `tools/absent-split.py` lines 40-45. A label swap that keeps both classes nonempty is defined not to fail C1. Ratio truth is C2.
- `REPRODUCIBLE` compares `first.stdout == second.stdout` only (`c1-count.py` line 88) and records only the first return code (line 76). On this host both direct runs also had empty identical stderr and exit 0, so the live runs are byte-identical on both streams. A future stderr-only divergence would still print `REPRODUCIBLE PASS`.
- `--table` on the counter is not forwarded by `run()`. The assigned command did not pass `--table`, and both sides default to the committed round-42 table. An alternate `--table` would score the tool's default table against a different expected set.
- `CLASSED` requires `len(labels) == 15` and `set(labels) <= {misquote, not-carried}`. It does not re-check pairing beyond `ids == expected` plus a second column. Live output had one in-vocab label per expected id, in table order.

## Verification gaps

- Missing-tool and missing-table controls were not executed in this seat. Source shows they return before `run()` and do not write; that failure-path zero-mutation claim is not a runtime measurement here.
- Cache pin is the 15 consulted `.txt`/`.raw` pairs, not a hash of every file under `.qcache`.
- No semantic reference index was available. Caller closure is the ripgrep hit list plus the reads above.
- C2 (`--flip S086`) and C3 were not run. They are out of this seat's command.

Stop: no further actionable C1 defect in scope. Recommendation: accept the rerun as `C1=PASS`, exit 0; do not treat `MUTANT_DETECTED` as a separate kill.
