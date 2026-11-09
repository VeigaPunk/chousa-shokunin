# R98MutantsC1 — mutation test of C1 beyond its scored sets

Attacked tree: F = `aac826848dda5029ba459568b29d9a92176dc2b6` (fresh `git clone --shared` of the lane, `checkout -q F`,
`rev-parse --show-toplevel` = the clone). Scratch `/fast/scratch/hyaku/chousa-r98/R98MutantsC1` (removed before yield).
Tools installed: none. No network, no sudo, no lane or fleet mutation.

## 0. Pristine anchors at F (observed, not assumed)

| command (cwd = clone) | exit | observed |
|---|---|---|
| `python3 -B tools/search-rerun.py --selftest` | 0 | last line `SEARCH_RERUN_SELFTEST: PASS cases=67/67`, 68 lines, stderr empty (`R98MutantsC1-pristine-selftest-out.txt`) |
| `python3 -B corpus/evidence/round98/selftest-controls-r98.py --root <clone> --work <scratch>` (full, with regression, ~620 s) | 0 | `POSITIVE=1/1 KILL_REQUIRED=35/35 DO_NOTHING_REFUSED=1/1 PRIOR_R97_KILLED=34/34 R96_MUTANTS_KILLED=23/23 EQUIVALENT_SURVIVED=3/3 ORACLES_REJECTED=5/5 NO_WRITE=1/1 REGRESSION_R95=2/2 EXTERNAL_R97_KILLED=35/37 BASE_KILLED=12/37 CASES=67` then `SELFTEST_CONTROLS_R98=PASS`; `CASE external-r97 ... survivors=u01-verify-return-0,u05-tree-files-jj`; `CASE do-nothing-base BASE_KILLED=12/37 required_killed=12/35` (`R98MutantsC1-battery-pristine-F-full.txt`) |

The frozen predicate and the named survivors hold at F. Everything below is about what the instruments do *beyond* that.

## 1. Tool mutants (one site each, `probe98.py`; killed = the frozen rule: exit 1, `SEARCH_RERUN_SELFTEST: FAIL`, a case id or `setup` in `failed=`, no Traceback)

Run: `cd /fast/scratch/hyaku/chousa-r98/R98MutantsC1 && python3 -B probe98.py` (exit 0).
Receipt: `R98MutantsC1-probe98.py.txt`, `R98MutantsC1-probe98-out.txt`, `R98MutantsC1-probe98-stderr.txt` (empty).
Summary line (verbatim): `PROBE killed=23 survived=13 applied=36 listed=37`.
R28 is listed but its old string applies 2 times (`SETUP R28-at-rev-one-top applies 2 times SKIP`), so it is not a one-site mutant; 36 applied.

Killed (23): G04, G05, G08, G09, G10, G11 (canary wiring and text), K01-K04 (`_collect`), S01 (`_summary` PASS rule), R17, R18, R19, R20, R22, R25, R27, R29, R30, R31, R33, R34 (cases r17-r34).

Survivors (13), with classification:

| mutant | site | observed | class |
|---|---|---|---|
| G01 | canary compare `[:len(want)]` (extra trailing lines ignored) | `SURVIVED failed=- rc=0` | uncovered: both fixed sets print exactly the expected lines, so no extra line is ever produced |
| G02 | canary compare `sorted(...)` (order ignored) | `SURVIVED` | uncovered: no fixed set prints lines out of order |
| G03 | canary drops `rc == want_rc` | `SURVIVED` | uncovered alone; combined with a summary fault it survives too (X1) |
| G06 | `return any(seen)` instead of `all` | `SURVIVED` | uncovered: `all`/`any` differ only when exactly one set is wrong, and no single fault does that (X2 shows the combined case) |
| G07 | canary detail hard-coded `fail_set=ok pass_set=ok` | `SURVIVED` | uncovered by design: the detail text is printed but never asserted; the battery reads only the id and `ok` |
| S02 | `_summary` lists at most 3 failed ids | `SURVIVED` | uncovered: the canary failing set has exactly 3 failures, so truncation is invisible to it; `failed=` can under-report with 4+ failures |
| S03 | `_summary` returns 0 when `k >= n-1` | `SURVIVED` | uncovered: the canary failing set has k=1, n=4, so `k >= n-1` is false there; no fixed set has exactly one failure (X4) |
| D01 | direct FAIL path prints `failed=setup` | `SURVIVED` | uncovered: the direct path (`if not guard_ok:` in `selftest()`) is executed only when the canary fails; nothing in the tool or battery forces that |
| D02 | direct FAIL path `return 0` | `SURVIVED` | uncovered (same reason); with G04 it survives the frozen rule (X3) |
| D03 | canary `except Exception` narrowed to `except Setup` | `SURVIVED` | uncovered: the canary never raises |
| D04 | `if not guard_ok:` → `if False:` | `SURVIVED` | uncovered (same reason as D01) |
| D05 | prints `SELFTEST g00-guard-canary-x` | `SURVIVED`, last line still `PASS cases=67/67` | uncovered by the kill rule: the self-test does not assert its own label; the battery checks ids only on the pristine tool |
| R32 | `verify` line gets a double space (`SEARCH_RERUN  <id>`) | `SURVIVED` | self-test uses `split()`, so whitespace is invisible to it; **covered by round-95**: see §3 |

No survivor is an equivalent mutant in the strict sense: each changes output or behaviour on some input the fixed sets never supply.

## 2. Combined tool mutants (`probe98b.py`, same frozen kill rule)

Run: `python3 -B probe98b.py`. Receipts `R98MutantsC1-probe98b.py.txt`, `R98MutantsC1-probe98b-out.txt`.

| combo | faults | observed | reading |
|---|---|---|---|
| X1 | G03 + `return 0 if k == n or k == 1 else 1` | `COMBO X1 rc=0 SURVIVED failed=- last='...PASS cases=67/67'` | the canary's exit-code compare is not an enforced property: a wrong exit code on the failing set passes the canary, and the real run never reaches it |
| X2 | G06 + `return 0 if k == n and n > 1 else 1` (only the 1-case pass set is wrong) | `COMBO X2 rc=0 SURVIVED` | `any()` lets a broken pass set through |
| X3 | G04 (drop pass set) + direct FAIL `return 0` | `COMBO X3 rc=0 SURVIVED failed=g00-guard-canary last='SEARCH_RERUN_SELFTEST: FAIL guard-canary failed=g00-guard-canary'` | a broken guard prints FAIL with exit 0; the frozen rule requires exit 1, so it counts as SURVIVED |
| X4 | R17 (one real case fails) + `return 0 if k >= n-1 else 1` | `COMBO X4 rc=0 SURVIVED failed=r17-row-no-end-pipe last='SEARCH_RERUN_SELFTEST: FAIL cases=66/67 failed=r17-row-no-end-pipe'` | the self-test prints FAIL with exit 0 when one case fails; the frozen rule kills nothing with exit 0 |

## 3. Round-95 leg on R32 (`R98MutantsC1-r95-on-R32-*`)

`python3 -B corpus/evidence/round95/rerun-controls-r95.py --root <clone> --work <scratch> --tool <R32 mutant>` → exit 1,
`RERUN_CONTROLS=FAIL` (stdout 50 lines; `CASE clone-edit rc=0/1 expect=0/1 FAIL`, `CASE f1-count ... FAIL`, oracle lines `ok`).
So R32 is caught by round-95, not by the round-98 self-test. Wall 77 s.

## 4. Battery mutants (`corpus/evidence/round98/selftest-controls-r98.py`, one site each, `--no-regression --work <scratch>`)

Receipts: `R98MutantsC1-probe98b-out.txt` (lines `BATTERY ...`), `R98MutantsC1-battery-B6-oracle-run.txt`.

| mutant | edit | observed | verdict |
|---|---|---|---|
| B1 kill rule loosened | `dead = rc == 1 and ...` → `dead = "SEARCH_RERUN_SELFTEST: FAIL" in out and ...` | rc 0, `SELFTEST_CONTROLS_R98=PASS`, tally identical to pristine | **SURVIVED** — the battery does not enforce exit 1 for mutants; no current mutant prints FAIL with exit 0, so the printed counts are unchanged |
| B2 EQUIVALENT leg inverted | `surv += 1 if ok else 0` → `surv += 0 if ok else 1` | rc 1, `EQUIVALENT_SURVIVED=0/3`, `SELFTEST_CONTROLS_R98=FAIL` | KILLED |
| B3 NAMED_SURVIVORS widened | adds `u02-run-at-rev-tops-0` | rc 0, `KILL_REQUIRED=34/34`, `SELFTEST_CONTROLS_R98=PASS` | **SURVIVED** — the denominator is `len(external) - len(NAMED_SURVIVORS)` computed from the same literal; the printed `35/35` is not pinned |
| B4 DO_NOTHING flipped | `breq < len(required)` → `breq >= len(required)` | rc 1, `DO_NOTHING_REFUSED=0/1`, FAIL | KILLED |
| B5 oracle dropped | removes `"hash-of-self": hos,` | rc 0, `ORACLES_REJECTED=4/4`, `SELFTEST_CONTROLS_R98=PASS` | **SURVIVED** — the denominator is `len(stubs)`; the printed `5/5` is not pinned |
| B6 required from survivors | `required = [m for m in required if res.get(m)]` before `k_req` | rc 1, FAIL; `KILL_REQUIRED=35/35` still printed; `ORACLES_REJECTED=4/5` | KILLED, but **not by the KILL_REQUIRED leg**: the guard-blind oracle run prints `KILL_REQUIRED=30/30 ... EXTERNAL_R97_KILLED=30/37` and rc 0, so it is accepted; the oracle leg fails (`R98MutantsC1-battery-B6-oracle-run.txt`) |

Summary: 3 of 6 battery mutants survive as written (B1, B3, B5); the printed numerals `35/35`, `5/5` and `3/3` are not enforced by the exit code.

## 5. Findings, ranked

1. **Exit code of the canary and the one-failure path are not enforced.** The tool's canary docstring and the lane's brief say the canary "compares every printed line and the exit code" and that a summary which "returns 0 for one ... fails this check". G03 (drop the rc compare), X1, S03 and X4 all survive. The canary's failing set has three failures, so no fixed set tests the rc for a single failure; and nothing ever runs the direct FAIL path (D01-D05 survive, X3 survives). Wording over-claims enforcement.
2. **The battery's printed numbers are self-referential.** `KILL_REQUIRED`, `ORACLES_REJECTED` and `EQUIVALENT_SURVIVED` take their denominators from the same literals they count (B3, B5 survive). The frozen predicate lines (`35/35`, `5/5`, `3/3`) are checked only against the battery's own copy; the exit code does not pin them. At F they hold (pristine run above).
3. **The battery's kill rule is looser than its docstring for mutants** (B1 survives). It has no current effect on the 37/34/23 sets, but the rule as written would count a mutant that prints FAIL with exit 0 as killed.
4. **R32 (verify output whitespace) is not seen by the self-test**, only by round-95. Not a C1 sentence; relevant to the scope of "the self-test kills".

## 6. C1 sentence check

- The frozen sentence and its numbers hold at F: 67 case lines (48 + g00 + 18), `PASS cases=67/67`, pristine battery `SELFTEST_CONTROLS_R98=PASS`, survivors exactly `u01-verify-return-0,u05-tree-files-jj`, `BASE_KILLED=12/37`, `ORACLES_REJECTED=5/5` (pristine).
- None of the 13 survivors of the 36 new tool mutants, nor the combos, falsifies the frozen sentence's wording, which speaks of the 37 named mutants, the 34 + 23 prior ones, three equivalents and five oracles. Named limit (a) covers the rest.
- The canary wording in the tool docstring and the brief does overreach (finding 1).

VERDICT: R98MutantsC1 C1 fired — the frozen sentence and predicate held at F (pristine battery PASS, 5/5 oracles, survivors u01/u05), but the canary's stated checks ("compares ... the exit code", "returns 0 for one ... fails this check") are not enforced: G03, X1, S03, X4 survive and the direct FAIL path is never executed (D01-D05, X3 survive); the battery's printed denominators are self-referential (B3, B5 survive).

## Receipts (all under .ufo/waves/round-98/w1/, prefix R98MutantsC1-)

probe98.py.txt, probe98-out.txt, probe98-stderr.txt, probe98b.py.txt, probe98b-out.txt, probe98b-out-file.txt, probe98b-stderr.txt, pristine-selftest-out.txt, pristine-selftest-err.txt, battery-pristine-F-full.txt, battery-pristine-F-stderr.txt, battery-B6-oracle-run.txt, r95-on-R32-stdout.txt, r95-on-R32-stderr.txt, mutant-R32-tool.py.txt, mutant-R32-check.py.txt.
