# CritC2Scope — what `UNREGISTERED=0` means, and the executables it does not contain
seat: critic (leaf), round-46 wave 2. no fetch, no production write, no subagent.
Bytes: `git -C <lane> archive d09fc8e7 | tar -x -C /tmp/chousa-r46w2-CritC2Scope/land`; every figure is from that export unless marked **live** (uncommitted worktree).

## Verdict
`UNREGISTERED=0` is true of the counter's selector and false of three properties the row's words reach: (i) **one 8-pipe line** scores full marks regardless of which cell holds the paths — and the round's own committed controls file already records such a line PASSING (`c2-controls.txt:50-56`); (ii) the declared kill clause `ENTRY_POINTS below 71` has **no carrier** — 69/69 prints `C2=PASS`, exit 0; (iii) frozen leg C says "every existing repo-relative `*.py`/`*.sh` path named in `SCORECARD.md` or a claims file", but `c2-count.py:40` silently requires a `tools/`|`corpus/` prefix — 8 named existing executables (5 with no Gates row) sit outside the set; read literally the frozen predicate gives `UNREGISTERED=5`, `C2=FAIL`.

## 1. Cheapest gate: one line, eight pipes, every path in one cell
```
$ python3 corpus/evidence/round46/c2-count.py --list      # landing, unmodified
ENTRY_POINTS=72 (tools=8 counters=50 named=70) GATES_ROWS=35
REGISTERED=72/72 UNREGISTERED=0 C2=PASS                  exit 0
```
`## Gates` body replaced by ONE row, `| x | gate | x | x | x | x | x | <all 72 paths> exit |` (8 pipes, 7 cells; paths only in the last cell):
```
GATES_ROWS=1 REGISTERED=72/72 UNREGISTERED=0 C2=PASS exit 0
```
Escaped pipes defeat the "eight separators" rule at the exact shape whose control is refused — a SIX-content-cell row padded with `\|` (raw pipes 12, rendered cells 6, the `SKILL-6cell.md` shape):
```
GATES_ROWS=1 REGISTERED=72/72 UNREGISTERED=0 C2=PASS exit 0
```
Bracketing: 6 content cells (7 pipes) → `UNREGISTERED=72 FAIL exit=1`; 7 content cells → PASS. The docstring's cheapest-gate line (`c2-count.py:25-27`: "pasting the bare paths … or into a one-cell row — both are refused, because … a row needs eight separators and an exit-code verdict") is falsified: any eight pipes plus the substring `exit` suffices; cell roles are never read. So QUALITY 60's cheapest gate is a one-row paste, strictly cheaper than the 35 honest rows. The round's committed control receipt records that class passing:
```
corpus/evidence/round46/controls/c2-controls.txt:50-56
$ ... --skill <SKILL-7pipe.md>
GATES_ROWS=31 REGISTERED=71/71 UNREGISTERED=0 C2=PASS exit=0
```
`claims.md:69-71` describes four controls that "stay unregistered"; the file has seven blocks and the seventh is a PASS; neither claims.md nor the SCORECARD row names it. (`find -name 'SKILL-*'` = 0 in the landing export and the lane — control fixtures uncommitted.)

## 2. The declared kill floor is not implemented
`claims.md:72`: "Kill rule: `UNREGISTERED>0`, or an `ENTRY_POINTS` below 71, fails the claim as declared." Deleting three registered leg-B counters (`round43/c3-count.py`, `round41/c2-count.py`, `round40/c2-count.py`) and re-running:
```
ENTRY_POINTS=69 (tools=8 counters=47 named=67)
REGISTERED=69/69 UNREGISTERED=0 C2=PASS                  exit 0
```
`c2-count.py:119-125`: `unreg = [p for p in eps if not any(names(r,p) …)]; ok = not unreg` — the only failure test. Losing three verifiers cannot fail the claim; the floor is a reader's comparison, yet the SCORECARD row reports it as measured.

## 3. The counter is narrower than the frozen predicate
Frozen leg C (`claims.md:62`): "every existing repo-relative `*.py`/`*.sh` path named in `SCORECARD.md` or a `corpus/evidence/round*/claims*.md`" — no prefix restriction. `NAMED` (`c2-count.py:40`) requires `(?:tools|corpus)/`. Eight existing, tracked paths named in exactly those documents are dropped; five have no Gates row:
```
LITERAL_SET=80  COUNTER_SET=72  LITERAL_UNREGISTERED=5
.ufo/waves/round-35/controls/ctl-c1-hardcoded-grep.sh   round35/claims.md:55
.ufo/waves/round-36/controls/base-gate-r36.sh           SCORECARD.md:2038; round36/claims.md:13,61
.ufo/waves/round-36/controls/ctl-c2-stub-pass.py        round36/claims.md:115
.ufo/waves/round-37/controls/base-gate-r37.sh           SCORECARD.md:2080; round37/claims.md:15
.ufo/waves/round-39/controls/mut-gate-path-env.sh       round39/claims.md:76
(already registered yet still omitted: round-38/…-r38.sh, round-39/…-r39.sh, round-41/…-r41.sh)
```
All five are `#!/usr/bin/env bash|python3`, tracked at `d09fc8e7`, 14–8 722 lines (the r36/r37 control gates are byte-exact copies of `tools/research-gate.sh`). Report, not rescale: as frozen, C2 fails with `UNREGISTERED=5`.

## 4. Count and paths: executables a receipt executes that the frozen set lacks
Method: `*.py`/`*.sh` + shebang/exec-bit under the three roots; frozen set = `entry_points()`; "a receipt depends on it" = a committed receipt/measure log/report invokes it (`(python3|bash|sh) <path>`, plus `VAR=/dir/<name>` resolution for `$SCRIPT_DIR`).
```
corpus/evidence .py/.sh=74 outside=10 | tools=8 outside=0 | .ufo/waves=965 outside=965
EXECUTABLES_TOTAL=1047  OUTSIDE_FROZEN_SET=975
receipt-invoked and outside the set: 36  (corpus/ 10, .ufo/waves 26)
  of the 36: with a Gates row 3, with NO row 33
```
Strict tier — executed by a committed `corpus/evidence` receipt (both registered, both invisible to the counter): `corpus/evidence/round45/tag-count.py` (round45/measure-after-5e8c7ad2.txt:37), `corpus/evidence/round46/build-spans.py` (round46/measure-after.txt:44). Transitive tier — an in-set, registered script executes an unregistered one: `round25-meta-differential.sh:40` → `corpus/evidence/round25-meta-oracle.py`; `round26-registry-differential.sh:9,74` → `corpus/evidence/round26-registry-oracle.py` (neither has a row).

The 10 under `corpus/evidence/` (none a member; `row=Y` only for the two above):
```
corpus/evidence/round25-holds/battery.sh       corpus/evidence/round25-meta-oracle.py
corpus/evidence/round25-sources-census.sh      corpus/evidence/round26-registry-oracle.py
corpus/evidence/round29/prose-check.py         corpus/evidence/round30/rerun-check.py
corpus/evidence/round32/q33-check.py           corpus/evidence/round45/build-spans.py
corpus/evidence/round45/tag-count.py row=Y     corpus/evidence/round46/build-spans.py row=Y
```
The 26 under `.ufo/waves/` (all `row=N` except r38): r29 build/ExecOfflineTest/quote-reopen-offline-test.py, r29 build/ExecProseCheck/prose-check.py, r29 build/ExecToolB/quote-reopen-b.py, r29 falsify/DiffToolB/{mutation-detector,run-differential}.py, r30 build/ExecRerunCount/rerun-check.py, r31 build/ExecD4Rerun/rerun-after-enum.py, r31 build/ExecD5Controls/tally_v4_receipts.py, r31 falsify/ReviewCorrD4D6/rederive.py, r31 measure/c1only-build.sh, r32 w1/ExecR2CounterV3/r31-c1-count-v3.py, r33 w1/ExecD2Census/census.py, r33 w1/ExecNoHarmBase33/battery.sh, r33 w2/FuzzDiff33/fuzz_c1.py, r34 w1/{CtlC1DoNothing/base-gate.sh, CtlC1Truncate/run-control.py, ExecE2Counter/c1-count-v3.py, ExecE4Census/receipt-binding.py, ExecNoHarmBase34/battery.sh}, r35 repairs/{base-gate.sh,slen-probe.sh}, r36 controls/base-gate-r36.sh, r37 controls/base-gate-r37.sh, r38 controls/base-gate-r38.sh **row=Y**, r39 controls/mut-gate-path-env.sh, r45 assimilation/map-staged.py. (Wave instrumentation; the SCORECARD's "verifiers" word does not reach them, and no gate row claims them.)

## 5. The SCORECARD row's wording (working tree, SCORECARD.md:2460)
Row: "C2 calibration: the gate registry covers the executable verifiers the lane's verdicts name outside the frozen name pattern" … "REGISTERED=72/72 UNREGISTERED=0 … `REGISTERED=73/73` once `SCORECARD.md` names `build-spans.py` (both `ENTRY_POINTS ≥ 71`); forges refused: prose paste, six-cell row, eight-pipe row without `exit`, row after the next `## `, fenced row, `.pyc`-suffix row"; verdict cell: "limit named: the set samples on MENTION … not on DEPENDENCE".
**Overstated** on four counts: (a) "covers the executable verifiers the lane's verdicts name" — only those spelled `tools/`|`corpus/`; 5 named ones have no row; (b) 33 receipt-executed executables are neither members nor rows; (c) the six refused forges omit the control that PASSED and the one-line/escaped-pipe forges above; (d) "both `ENTRY_POINTS ≥ 71`" is presented as measured although the counter cannot fail on it. Also the row exists only in the worktree: `git show d09fc8e7:SCORECARD.md | grep -c 'Round 46'` = 0.

**One-sentence limit the row should carry:** *`UNREGISTERED=0` means every path the counter's own selector emits — `tools/*`, the round-45 counter names, and `tools/`- or `corpus/`-prefixed `*.py`/`*.sh` named in `SCORECARD.md` or a claims file — occurs somewhere in a `## Gates` line with eight pipes and the word `exit`; it does not mean the registry covers the executables a receipt runs (36 outside, 33 rowwise), that a single row or escaped pipes cannot score full marks, or that the declared `ENTRY_POINTS ≥ 71` floor was enforced.*

Adjacent: `gates_rows()` drops the three real gate rows `verify-claims`, `verify-chain`, `verify-metadata` because their verdict maps say clean/drift, not the token `exit` (raw `|` lines 40, counted rows 35). Latent — no entry point currently depends on them.

## Pointers
`corpus/evidence/round46/c2-count.py:25-27` (cheapest-gate line), `:40` (NAMED prefix), `:69-73` (row rule), `:119-125` (no floor) · `claims.md:59-63` (predicate), `:69-71` (controls), `:72` (kill rule) · `controls/c2-controls.txt:50-56` (passing control) · `controls/c2-before.txt:27-43` (tree B labelled "no round-46 counters" yet `counters=50` and round46 counters listed) · `SCORECARD.md:2460` (row, uncommitted) · `SKILL.md:77-78` (8-column schema) · `round45/c3-count.py:108-118` / `round45/build-spans.py` (builder outside the set).
sha256: c2-count `60ad448e99b15cb6691e48ce…`, c2-controls `a44c50c3e6ee66316e01130a…`, claims.md `60098dfffeee7581f2c047f6…`. Scratch `/tmp/chousa-r46w2-CritC2Scope` removed. Tooling: nothing installed or upgraded.
