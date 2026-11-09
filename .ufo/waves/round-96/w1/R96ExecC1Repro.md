# R96ExecC1Repro — frozen C1 falsification from a clean tree

Freeze `F = 2db151c5ea0883de0b9dc8d95c6fac1755e1056a`, base `bbf64970b6c73ca64bcc5f6de2f33b0550459813`,
lane root cloned to `/fast/scratch/hyaku/chousa-r96/R96ExecC1Repro/repo` at F.
Method: exact commands echoed below; receipts copied to this w1 directory with the `R96ExecC1Repro-` prefix.
No finds were converted into passes — every expected value was re-derived here.

## (a) Predicate 1 — selftest

Command: `cd $S/repo && python3 -B tools/search-rerun.py --selftest`
Observed: exit **0**; the tail is `SEARCH_RERUN_SELFTEST: PASS cases=32/32`.
Breakdown in the 32 case lines: 14 parse (`p01`-`p14`), 8 matching (`m01`-`m08`), 10 judgement (`j01`-`j10`), all `ok`.
Receipt: `R96ExecC1Repro-p1-selftest.txt` (32 case lines + PASS, exit recorded in command transcript).

## (b) Predicate 2 — battery (full, with regression leg)

Command: `python3 -B corpus/evidence/round96/selftest-controls-r96.py --root . --work <scratch>` (full, timed ~848 s)
Observed: exit **0**; 30 `CASE` lines, every one `ok`; final tally (last lines of receipt):
`POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1 REGRESSION_R95=2/2 CASES=32`
`SELFTEST_CONTROLS=PASS`.
Receipt: `R96ExecC1Repro-p2-battery-full.txt`. The `--no-regression` variant gives the matching
prefix `… NO_WRITE=1/1 CASES=32` + `SELFTEST_CONTROLS=PASS`, exit 0 (`R96ExecC1Repro-p2-battery-noreg.txt`).
23/23 mutants KILLED (m10, m11, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24, m25, m26, m27,
m28, m29, m30, m31, m32, m33 — one `rc=1` each with the named self-test cases); 3/3 oracle stand-ins rejected;
NO_WRITE `left=[] lane_status_same=True`; round-95 battery CASE lines both `rc=0 ok`.

## (c) Predicate 3 — SKILL.md gate row

Command: `grep -c '^| \`search-rerun\` (r96 re-registration' SKILL.md` → **1** (exit 0).
The row's kind cell (cell index 2 of the 10-cell pipe row) is exactly `gate`. Claimed row exists and is a gate.

## (d) Behaviour preservation vs base (K5) — base tool extracted, both run on both records

`git -C $S/repo show bbf64970…:tools/search-rerun.py > $S/base.py`; then, from the F tree:
`python3 -B base.py verify <record>` vs `python3 -B tools/search-rerun.py verify <record>` on
`corpus/fixtures/search-rerun-r95.md` and `corpus/knowledge/search-peer-review-dedup-r96.md`, each with and
without `--strict`. Command transcript in `R96ExecC1Repro-base-vs-F-comparison.txt`.

| record | mode | base exit | F exit | stdout diff |
|---|---|---|---|---|
| r95 | plain | 0, `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8 tree_same=3/8 findings=0`, `SEARCH_RERUN: CLEAN` | 0, identical | identical |
| r95 | --strict | 1, `… findings=5`, `SEARCH_RERUN: DRIFT` | 1, identical | identical |
| r96 entry | plain | 0, `… rev_match=8/8 tree_same=5/8 findings=0`, `SEARCH_RERUN: CLEAN` | 0, identical | identical |
| r96 entry | --strict | 1, `… findings=3`, `SEARCH_RERUN: DRIFT` | 1, identical | identical |

No difference in stdout or exit code on any leg. The base-vs-F source diff is exactly three things: (1) the
`parse_record`/`parse_text` split, (2) the `evaluate` extraction with `verify` rebuilt on closures and the same
lines/findings/tally logic, (3) the 114-line `--selftest` mode + argparse wiring + docstring lines. The judgement
code (`evaluate`) is shared; `verify`'s git/disk readers are unchanged.
Also: base `--selftest` exits 2 (`the following arguments are required: cmd`) — the round-95 "Before" behaviour.

## (e) Six one-cell forged records on both tools

Built from `corpus/fixtures/search-rerun-r95.md` (copied via `cp`, mutations by python text replace, each
asserted non-no-op). Seven records run: the six required classes plus one semantically meaningful engine swap.
The exit codes below were captured with `echo $?` per run and cross-checked with `cmp` on raw stdout; every
pair was byte-identical.

| # | class | base exit | F exit | verdict (both) | identical? |
|---|---|---|---|---|---|
| f1-count | Q1 `hits` 7→8 | 1 | 1 | `Q1 rev=DRIFT … COUNT_DRIFT` | yes |
| f2-path | Q2 one hit_set path altered | 1 | 1 | `SET_DRIFT` (Q2 row) | yes |
| f3-digest | Q1 sha256 digest last digit flipped | 1 | 1 | `Q1 rev=DRIFT … SET_DRIFT,TREE_CHANGED` | yes |
| f4-rev | Q1 rev `…e687`→`…e688` (nonexistent commit) | 2 | 2 | `SEARCH_RERUN_ERROR REV … is not a commit in …/repo` | yes |
| f5-glob | Q1 `corpus/captures/*.txt`→`corpus/*.txt` | 1 | 1 | `Q1 rev=DRIFT … COUNT_DRIFT,SET_DRIFT` | yes |
| f6-engine | Q1 `fixed`→`regex` (literal `PRISMA-S`) | 0 | 0 | `rev_match=8/8`, `SEARCH_RERUN: CLEAN` | yes |
| f7-engine | Q6 `regex`→`fixed` (pattern `[Ss]earch…`) | 1 | 1 | `Q6 rev=DRIFT … COUNT_DRIFT,SET_DRIFT` | yes |

Receipts: `R96ExecC1Repro-forged-verdicts.txt`, `R96ExecC1Repro-base-r95.txt`, `R96ExecC1Repro-f-r95.txt`.
No verdict differed between base and F on any forgery.
Note on f6: `fixed`→`regex` on a literal is a *meaningless* forgery (both engines match the same text), so
CLEAN from both is the correct answer, not a missed forgery — the meaningful engine swap is f7, which DRIFTs in
both. Counts align with the Named limits: f's self-test does not exercise `verify`'s readers, which is exactly
why the behavioural cross-check (d) uses the CLI on real records.

## (f) Named limits probed

* Limit (e) — m34 (drop `g.startswith("/")`) removed as equivalent. Re-derived: mutant with `False` in place of
  `g.startswith("/")` (exactly one occurrence in the source) still runs `--selftest` to exit 0,
  `SEARCH_RERUN_SELFTEST: PASS cases=32/32`. Why: on a `/`-glob `parts[0] == ""` so the empty-segment check in
  the same WHENCE clause refuses it (`tools/search-rerun.py:213-215`, `parts = g.split("/")` … `"" in parts`).
  Receipt: `R96ExecC1Repro-m34-equivalence.txt`. The removal is sound.
* Limit (a) — the self-test does not call the readers. Confirmed: the AST of `selftest()` (99 lines) contains no
  `open`, `subprocess`, `socket` Name/Call; the strings `run_at_rev`/`run_on_tree`/`tree_files` appear only in
  its docstring (one line). Called names are the pure helpers plus `evaluate`, `git_env`, `os` (one `GIT_DIR`
  save/restore around `git_env()`).
* K4 (`--selftest` writes a file, runs git, opens a socket). Observed: battery NO_WRITE = `left=[]`
  `lane_status_same=True ok`; a solo re-run with `HOME`/`TMPDIR` = an empty dir exits 0 and leaves it empty;
  mixed invocations behave as argparse errors (exit 2): `--selftest verify <record>` → `error: --selftest takes
  no subcommand`, bare invocation → `error: a subcommand (verify) or --selftest is required`, unknown flag →
  exit 2 `unrecognized arguments`. No write/git/socket observed.

## Tooling, scratch, environment

* No tool installs or upgrades were needed. grep semantics were taken with `/usr/bin/grep` (the interactive
  shell's `grep` may be a shim, per lane note); the `grep -c` predicate was run with plain `grep` and returned
  1/1 correctly. Python 3 system `python3`; no pacman transactions (orchestrator pause respected; nothing needed).
* Scratch: `/fast/scratch/hyaku/chousa-r96/R96ExecC1Repro/` (clone at F, fixtures, batteries). Deleted after
  receipt capture per lane rules.
* Fixing a seat bug, not the lane's: my first f4 record mutated the *prose* rev mention (line 9) instead of the
  `| Q1 |` row — the row still read `…e687`, so that run's CLEAN did not measure anything. Redone on the row;
  final f4 is the one in the table above.


## Addendum — timed-out batteries were first run concurrently; the tool, not the claim, is flake-free
(bg_342/bg_317 ran two 10-15 min batteries at once and each timed out mid-REGRESSION leg: m20/env-scrub
SURVIVED once, `REGRESSION_R95=1/2`, `SELFTEST_CONTROLS=FAIL`, exit 1; `R96ExecC1Repro-r95-mutants-flake.txt`).
Re-run solo now, all pass: `mutants-r95.py` → `MUTANTS_KILLED=10/10` (incl. m20 `KILLED … CONTAINMENT=1/2`, exit 0;
`R96ExecC1Repro-r95-mutants-rerun-pass.txt`), and the full selftest battery → exit 0, 30 CASE lines ok, 33-line receipt with both tally lines,
`POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1 REGRESSION_R95=2/2 CASES=32`,
`SELFTEST_CONTROLS=PASS` (`R96ExecC1Repro-battery-rerun.txt`). The flakes were load/timing under concurrent
10-minute batteries, not a tool defect — but the implication for the claim is real: a timed-out scheduler makes
the battery read as FAIL, and the instrument gives no partial credit. F's own battery output is complete and
clean when the REGRESSION leg is given its full time.

VERDICT: R96ExecC1Repro C1 held — all three predicates reproduce at F, base-vs-F verdicts are byte-identical (stdout + exit) on both records and on 7 independent one-cell forgeries, m34's removal re-derives as equivalent, and the self-test shows no file/git/socket activity.
VERDICT: R96ExecC1Repro C2 n/a — this seat executed the frozen-C1 reproduction scope only.
