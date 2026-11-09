# R97ExecC1Repro — frozen C1 reproduction (round 97)

Seat: R97ExecC1Repro. Tree attacked: `9a0ce2015fa0254848f2f32f612b20caf7dc5478` (claim freeze F).
Base: `c8087ac529003e667505bcc624f9a7bde0cffbce`. Shared clone at `/fast/scratch/hyaku/chousa-r97/R97ExecC1Repro/repo`, checked out at F. Axes: reproducibility of the frozen tally, K4 harm (verify equivalence base vs frozen), forgery sensitivity (six one-cell records), diff surface (anything outside `ST_*`/`st_row`/`selftest`).

Tooling: no install/upgrade; system python3, /usr/bin/grep (GNU 3.12). Command receipts in `R97ExecC1Repro-predicates.txt`, `R97ExecC1Repro-k4-verify.txt`, `R97ExecC1Repro-forged.txt`; diff in `R97ExecC1Repro-diff.txt`; forged records in `R97ExecC1Repro-forged-records.tgz`.

## (a) Predicate 1 — selftest tally

Command: `python3 -B tools/search-rerun.py --selftest` from `$S/repo` (frozen tree).

Observed: 47 case lines (p01–p13, r01–r15, m01–m08, j01–j10) all `ok`; final line `SEARCH_RERUN_SELFTEST: PASS cases=47/47`; **exit 0**. Stated tally reproduces.

## (a) Predicate 2 — battery

Command: `python3 -B corpus/evidence/round97/selftest-controls-r97.py --root . --work /fast/scratch/hyaku/chousa-r97/R97ExecC1Repro/work` from frozen tree (~8 min).

Observed tally: `POSITIVE=1/1 EXTERNAL_KILLED=30/30 DO_NOTHING_REFUSED=1/1 R96_MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1 REGRESSION_R95=2/2 BASE_KILLED=10/30 CASES=47` and `SELFTEST_CONTROLS_R97=PASS`, **exit 0**.

Per-mutant lines observed: all 30 external mutants KILLED by the frozen tool with rc=1 (n01–n29 minus n08, s1, s2); base tool kills exactly 10/30 (n01, n03–n06, n18, n19, n21, n24, n25) and lets 16 survive with PASS plus n11/n12/n13/n26 exit 1 with traceback (survivors by the battery rule); do-nothing `BASE_KILLED=10/30 setup=0 expect<30 ok`; all 23 R96 mutants KILLED; all 3 oracles rejected (constant-pass and hollow-selftest: `EXTERNAL_KILLED=0/30`, always-FAIL: `POSITIVE=0/1`, `NO_WRITE=0/1`); no-write `left=[] status_same=True diff_same=True ok`; both R95 regression legs rc=0.

## (b) K4 harm — verify equivalence (plain and `--strict`)

Base tool materialized: `git -C $S/repo show c8087ac5:tools/search-rerun.py > $S/base.py` (548 lines). Each `verify` run from `$S/repo` with `--root .` on correctly-typed records. Full stdout+exit in `R97ExecC1Repro-k4-verify.txt`.

Observed — no verdict difference on any file:

| file | new plain | base plain | new --strict | base --strict |
|---|---|---|---|---|
| `corpus/fixtures/search-rerun-r95.md` | `rev_match=8/8 CLEAN` exit 0 | identical | `rev_match=8/8 findings=5 DRIFT` exit 1 | identical |
| `corpus/knowledge/search-peer-review-dedup-r96.md` | `rev_match=8/8 CLEAN` exit 0 | identical | `findings=4 DRIFT` exit 1 | identical |
| `corpus/knowledge/press-checklist-questions-r97.md` | `rev_match=7/7 CLEAN` exit 0 | identical | `findings=7 DRIFT` exit 1 | identical |

Per-query lines (`SEARCH_RERUN Q<n> rev=MATCH tree=...`) byte-identical between tools. K4 harm leg holds for the two named K4 files; the third file matches too (as expected: r97 entry was authored against base rev).

## (c) Six one-cell forged records

Fixture repo `/fast/scratch/hyaku/chousa-r97/R97ExecC1Repro/tmp.ilsvQ49mLF` (toplevel assert pass; `corpus/captures/{alpha,beta}.txt`, one base commit `1eb52149183e14f664d428ddf29328b176431c12` committed with fixture identity). Truth at that rev: `quick` hits 1 file (alpha); `subject` (fixed, case-sensitive) hits 1 file (beta); regex `[Ss]ubject` hits 2 files. Controls: CTRL1 (count=1/alpha, `quick`), CTRL2 (digest of beta only, `subject`), CTRL3 (regex `[Ss]ubject`, 2 files). Each forged record differs from its control in exactly one cell. Both tools run `verify <file> --root <fixture>`; full output in `R97ExecC1Repro-forged.txt`.

| record | cell forged | new tool | base tool | verdict difference |
|---|---|---|---|---|
| F1-count | hits 2 vs true 1 | DRIFT `COUNT_DRIFT,SET_DRIFT` exit 1 | identical DRIFT exit 1 | none |
| F2-path | hit_set beta vs true alpha | DRIFT `SET_DRIFT` exit 1 | identical DRIFT exit 1 | none |
| F3-digest | one hex char flipped | DRIFT `SET_DRIFT` exit 1 | identical DRIFT exit 1 | none |
| F4-rev | rev all-zero (not a commit) | `SEARCH_RERUN_ERROR REV ... is not a commit` exit 2 | identical exit 2 | none |
| F5-glob | `corpus/*.txt` (no capture under corpus/) | DRIFT `COUNT_DRIFT,SET_DRIFT`, at_rev=0 exit 1 | identical DRIFT exit 1 | none |
| F6-engine | engine fixed vs regex | DRIFT `COUNT_DRIFT,SET_DRIFT`, at_rev=0 exit 1 | identical DRIFT exit 1 | none |

Controls CTRL1/CTRL2/CTRL3: both tools CLEAN, exit 0. **No verdict difference between the frozen tool and the base tool on any of the six one-cell forgeries, nor on the three controls.** The guard added in r97 does not change `verify` behaviour on count/path/digest/rev/glob/engine forgeries, consistent with the claim that the change is confined to `--selftest`.

Note: an initial CTRL2 draft used the digest of the wrong file (alpha+beta); recomputed to beta only and used as the filed record.

## (d) Diff surface outside ST_*, st_row, selftest

Command: `git -C $S/repo diff c8087ac5 9a0ce2015 -- tools/search-rerun.py` (171-line diff, filed as `R97ExecC1Repro-diff.txt`).

Changed lines outside the three named zones: **none.** Every `+`/`-` line falls within `ST_AC_DIGEST`/`ST_HEAD` adjacency, `st_row`'s `searched` parameter, or the `selftest` function (case guard, `refusal` helper, r01–r15/m08/r13 extensions, lambda thunking, `planted`/`saved` env expansion, `j10` refactor). No change to `parse_text`/`parse_record`, `matches`/`seg_match`, `lines_of`, `hit`, `run_at_rev`/`run_on_tree`, `evaluate`, `verify`, `git_env`, or `main` — verify is byte-identical in behaviour, as (b) and (c) confirm.

## Verdict trailer

VERDICT: R97ExecC1Repro C1 held — frozen tree reproduces predicate 1 (47/47, exit 0) and predicate 2 (30/30, 23/23, BASE_KILLED=10/30, exit 0), verify plain+strict byte-identical to base on K4 files plus r97 entry, six one-cell forgeries rejected identically by both tools, and the diff touches nothing outside ST_*/st_row/selftest.
