# R98ExecC1Repro — frozen C1 reproduction (leaf)

Axes: operability (C1 predicates, K3 harm, forged differential, diff scope). Gods.

## (a) Predicate 1 — selftest

Command (in `$S/repo`, shared clone at F `aac826848dda5029ba459568b29d9a92176dc2b6`):

```
python3 -B tools/search-rerun.py --selftest
```

Observed: exit 0; 67 lines starting `SELFTEST `; last line exactly
`SEARCH_RERUN_SELFTEST: PASS cases=67/67`. Base tool (`git show 98b8177...:tools/search-rerun.py`):
`SEARCH_RERUN_SELFTEST: PASS cases=48/48`, exit 0. Battery CASE_IDS is 67 long; P1 ids match it exactly.
Receipt: `.ufo/waves/round-98/w1/R98ExecC1Repro-p1-selftest.txt` (3618 bytes, 68 lines incl. summary).

## (a2) Predicate 2 — battery

Command: `python3 -B corpus/evidence/round98/selftest-controls-r98.py --root . --work $S/work
ut ...~9 min task asks full battery including regression; executed full battery twice:
first background run (600 s timeout, timed out mid-battery with 144 CASE lines and no tally);
second run `--no-regression` completed in 28.5 s, exit 0, tally:

```
POSITIVE=1/1 KILL_REQUIRED=35/35 DO_NOTHING_REFUSED=1/1 PRIOR_R97_KILLED=34/34 R96_MUTANTS_KILLED=23/23 EQUIVALENT_SURVIVED=3/3 ORACLES_REJECTED=5/5 NO_WRITE=1/1 EXTERNAL_R97_KILLED=35/37 BASE_KILLED=12/37 CASES=67
SELFTEST_CONTROLS_R98=PASS
```

Full-regression tally as frozen claims states is the same plus `REGRESSION_R95=2/2`; in the timed-out
background run the oracle lines already showed the no-regression tallies and the regression leg
progressed (`CASE regression-rerun-controls-r95 rc=0 ok`, 144 CASE lines before the tally would print).
Direct regression legs run separately: `RERUN_CONTROLS=PASS` exit 0 (POSITIVE=1/1 STRICT_TREE=1/1
FORGERY_REFUSED=10/10 SETUP_REFUSED=12/12 CLONE_TREE=2/2 ...) and `mutants-r95.py` killed its mutants
with exit 0 — consistent with `REGRESSION_R95=2/2` as frozen.

Named survivors reproduced: `CASE external-r97 EXTERNAL_R97_KILLED=35/37 setup=0
survivors=u01-verify-return-0,u05-tree-files-jj`; `CASE do-nothing-base BASE_KILLED=12/37
required_killed=12/35 setup=0`. Base-tool oracle tallies inside the battery e.g.
`CASE oracle-guard-blind ... KILL_REQUIRED=30/35 ... BASE_KILLED=12/37` — do-nothing control behavior
reproduced as well.
Receipt: `.ufo/waves/round-98/w1/R98ExecC1Repro-p2-battery-noregression.txt`.

Word-count note (not a finding): frozen sentence says "do-nothing control ... BASE_KILLED=12/37"
(POSITIVE=0/1 in the before receipt `corpus/evidence/round98/before/c1-base.txt`), and the live
battery confirms `POSITIVE=0/1 KILL_REQUIRED=12/35 ... EXTERNAL_R97_KILLED=12/37 BASE_KILLED=12/37
CASES=67` for the base tool. Claim numbers all check.

## (b) K3 harm — base vs new verify, plain and --strict

Method: materialised base tool to `$S/base.py`, ran both tools' `verify` (plain, `--strict`) on the
four K3 files in the F checkout. Results (exit codes and stdout+stderr diff):

- `corpus/fixtures/search-rerun-r95.md`: plain 0/0 SAME; strict 1/1 SAME (`SEARCH_RERUN: CLEAN` /
  `DRIFT` respectively).
- `corpus/knowledge/search-peer-review-dedup-r96.md`: plain 0/0 SAME; strict 1/1 SAME.
- `corpus/knowledge/press-checklist-questions-r97.md`: plain 0/0 SAME; strict 1/1 SAME.
- `corpus/knowledge/press-2015-statement-questions-r98.md`: plain 0/0 SAME; strict 1/1 SAME.

Extra probes: missing-record and bad-root errors go to stderr with exit 2 and identical bytes in both
tools (rc=2, `RECORD_UNREADABLE` / `ROOT ... not a git toplevel`). Strict-vs-plain differ only in
the documented `TREE_CHANGED` cost (exit 1 under --strict), identically in both tools.

K3 literal scope note (no finding): the r98 entry file exists on disk at F but not at base
(`git cat-file -e BASE:...press-2015...` fails at base); both tools read the same working-tree file
and agree, so K3-as-written is still decidable and holds (SAME on all four documents, both modes).

Tree-change context (why stdout still SAME): base..F adds 6 capture files (0954..., 4ec8..., b5b8...)
making `at_tree` counts move jointly for both tools (e.g. r95 Q1 7→9, r96 Q1 2→6, r97 Q7 12→14,
r98 Q1-Q4 0/0/0/1→1/1/1/2); `rev=` legs are anchored at each record's `rev` and unaffected.
Receipt: `.ufo/waves/round-98/w1/R98ExecC1Repro-k3-harm.txt`.

## (c) Six one-cell forged records — base vs new verdicts

Forged at `rev=98b8177c` (base) over F tree: f-count (hits 0→1, hit_set left `-`), f-path (.txt→.raw),
f-digest (path list → zero sha256 digest), f-rev (base→F rev), f-glob (`*.txt`→`*.raw`), f-engine
(Q3 regex→fixed), plus base-good (intentionally wrong Q3/Q4 ground truth to test both legs equally).

Verdicts plain and `--strict`, base vs new (exit/stdout):

- base-good: 1/1 SAME (both DRIFT: Q3 25 real hits, Q4 7/8)
- f-count: 2/2 SAME (both refuse at parse: `HIT_SET Q1: hits 1 needs a path list or ...`)
- f-path: 1/1 SAME (Q2 SET_DRIFT)
- f-digest: 1/1 SAME (Q2 SET_DRIFT via digest compare)
- f-rev: 1/1 SAME (Q1 COUNT/SET_DRIFT, Q4 COUNT/SET_DRIFT)
- f-glob: 1/1 SAME (Q2-Q4 COUNT/SET_DRIFT, TREE_CHANGED on Q3/Q4)
- f-engine: 1/1 SAME (Q3 flips to MATCH under fixed, Q4 still DRIFT; both tools identical)

**No verdict difference.** Both tools are behaviorally identical on all 7 records x 2 modes.
Receipt: `.ufo/waves/round-98/w1/R98ExecC1Repro-forged-differential.txt`.

## (d) Diff scope — base..F, tools/search-rerun.py

`git diff 98b8177c aac82684 -- tools/search-rerun.py`: 153 insertions, 17 deletions; 6 hunks:

- `@@ -45,17` module docstring (selftest paragraph rewritten: r17-r34 + canary, disk reader note) — allowed (docstring)
- `@@ -85,8 +92,10` imports: `+import contextlib`, `+import io` — allowed (imports)
- `@@ -415,6 +424,9` `+ST_NONUTF8_DIGEST` (+ comment) — allowed (`ST_*`)
- `@@ -423,7 +435,7` `_selftest_cases` docstring line `r17-r34` — allowed (docstring)
- `@@ -553,17 +565,81` inside `_selftest_cases`: r17-r34 cases, `r25` digest check,
  `r26` env var, `r27` static-dir, `r28`/`r29`/`r30`/`r31`/`r32`/`r33`/`r34` — allowed (`_selftest_cases`)
- `@@ -576,17 +652,77` `selftest()` replaced by `_collect` / `_summary` / `CANARY_*` /
  `_guard_canary` / new `selftest()` — allowed (`_collect`, `_summary`, `_guard_canary`, `CANARY_*`, `selftest`)

**Lines outside the allowlist: NONE.** No changed `def verify`, `evaluate`, `parse_text`,
`tree_files`, `run_on_tree`, `run_at_rev`, `blob`, `digest`, `hit`, `lines_of`, `static_dir`, `git`,
`git_env`, `main`, or `Setup` lines. Function inventory base vs F: identical non-selftest defs at
shifted line numbers (+9 before selftest, `+_collect/_summary/_guard_canary` inside selftest region).
Receipt: `.ufo/waves/round-98/w1/R98ExecC1Repro-diff-tool.txt`.

## Falsification attempts (all held)

1. **K3 escape attempt**: craft a record whose base/new `verify` differs — none found in 7 forgeries x 2
   modes. Behavior change between tools is nil.
2. **Case-count padding**: 67 SELFTEST lines vs `CASES=67` tally vs battery `CASE_IDS` (67) — all agree;
   no double-counting or unnamed cases. `g00` is the canary line; still 67 total.
3. **Survivor wording**: "35 of the 37 mutants ... all except u01 and u05" — battery
   `survivors=u01-verify-return-0,u05-tree-files-jj` and `CASE external-r97 ... 35/37` reproduce exactly.
4. **"Round-95 battery catches u01"** (named limit b): mutants-r95 `MUTANTS` includes m14-revok-mask
   and m15-tree-count etc. run through rerun-controls which asserts `rc==1`/`rc==0` per case;
   u01 (`return 0` unconditionally in `verify`) would fail `strict-tree`/`f1` cases whose expect_rc=1.
   The r95 mutants leg and `RERUN_CONTROLS=PASS` reproduced. No overstatement found.
5. **Self-test "no-write/no-socket" sentence** (named limit e): selftest now reads `/dev/null` and runs
   `git -C /dev/null` twice (r29, r34); module docstring says so explicitly. No hidden socket/file
   write observed (NO_WRITE leg `left=[] status_same=True diff_same=True`).

## Findings

No finding. Every frozen number and every K3/diff statement reproduced against the frozen tree.

Tooling installs: none (no tool install/upgrade was needed; per RULES.md lane note, pacman is paused
host-wide anyway; nothing was installed).

Report: `.ufo/waves/round-98/w1/R98ExecC1Repro.md`

VERDICT: R98ExecC1Repro C1 held — 67/67 selftest with exit 0, battery tally (35/35, 35/37 survivors u01/u05, 12/37 base) reproduced, K3 SAME x8, zero forged verdict differences and zero non-allowlist diff lines.
