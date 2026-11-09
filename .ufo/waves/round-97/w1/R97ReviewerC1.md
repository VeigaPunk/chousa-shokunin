# R97ReviewerC1 — correctness review of C1 at freeze F (round 97)

Seat: `R97ReviewerC1` (leaf scorer-review, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Attacked tree: shared clone at `/fast/scratch/hyaku/chousa-r97/R97ReviewerC1/repo`, checked out `9a0ce2015fa0254848f2f32f612b20caf7dc5478`
(freeze F), diffed against base `c8087ac529003e667505bcc624f9a7bde0cffbce`.
What was read first: `.ufo/waves/round-97/claims.md` (C1 sentence, predicate, kill rules, named limits) and `plans/round-97.md`.
Scope was C1 only: (1) r01–r15 truth, (2) case guard + summary, (3) battery mutant source + exclusions, (4) KILLED rule crash path, (5) `os.environ` restore after r13. C2 not touched.

Tools: system Python 3.14, GNU grep 3.12. No installs/upgrades (none needed). No network.

## Verdict in brief

No falsification of the C1 sentence, predicate, kill rules, or named limits. All five scoped questions hold on direct re-execution.
Two low-severity defects (both falsify nothing) and one residual note.

## (1) r01–r15 assert what the real tool does — HOLDS

Each new case was re-run against the real parser/matcher extracted from `tools/search-rerun.py` at F (not against the
self-test's own expectations): `R97ReviewerC1-check1-r-cases.txt`.

- r01 signed hits → `HITS`, r02 `2026-11-9` → `DATE`, r03 `A*40` → `REV`, r04 `Q0` → `ROW`, r05 empty expression → `EXPRESSION`,
  r06 `corpus//*.txt` → `WHERE`, r07 trailing comma → `HIT_SET`: all match the code that produces them
  (`HITS_RE` `(0|[1-9][0-9]*)\Z`, `DATE_RE` `[0-9]{4}-[0-9]{2}-[0-9]{2}\Z`, etc.; parse order hits-before-hit-set verified).
- r08: upper-case `sha256:AAA…` parses as a path, not a digest — true because `DIGEST_RE` is `[0-9a-f]{64}` lower-case only.
- r09: glob longer than path matches nothing — true under `matches`' segment-length check; this is exactly the direction
  `n22` breaks (zip truncation).
- r10/r11: regex is unanchored (`pattern.search`) and decodes with `surrogateescape` — `hit(b"x PRESS\n")` true,
  `hit(b"x press\n")` false, `hit(b"\xff\xfe PRESS\n")` true, all observed.
- r12: `static_dir("corpus/a.txt")=="corpus"`, `static_dir("a.txt")==""` — observed from the real function.
- r13: after planting 7 `GIT_*` vars, `git_env()` leaves exactly the 3 guards with `GIT_NO_REPLACE_OBJECTS=1`,
  `GIT_TERMINAL_PROMPT=0` — observed.
- r14: two-code row yields `(3, 0, 0, ["COUNT_DRIFT","SET_DRIFT","TREE_CHANGED"])` — recomputed from `evaluate`; matches.
- r15: digest judged at rev, tree change reported separately — `(0,1,0,["TREE_CHANGED"])`, matches; `ST_AC_DIGEST`
  independently verified as sha256 of `corpus/a.txt\ncorpus/c.txt\n`.

Intended-kill mapping confirmed on the F tool (`R97ReviewerC1-check6-external30.txt`): r01→n09, r02→n10, r03→n14,
r04→n15, r05→n27, r06→n28, r07→n29, r08→n16, r09→n22, r10+r11→n17, r11→n20, r12→n23, r13→s1/s2/n25, r14→n02, r15→n07.
r10's second half and r09's two halves are mutually checking (an always-false matcher fails `m03`), so no vacuous pass.

## (2) Guard and summary — HOLDS

- `case()` (`tools/search-rerun.py:431-438`) catches `Exception` and forces `ok=False`. Replicated semantics
  (`R97ReviewerC1-check2-guard.txt`): raising bodies → FAIL; 1-tuple/3-tuple → `ValueError` on unpack → caught → FAIL;
  string/list returns follow Python truthiness, but all 47 actual bodies return `bool` or `(bool, str)`, so no
  vacuous-pass case exists. A case cannot pass while its body raised an `Exception`.
- Summary prints PASS iff `k == n` (`:567-570`); each call appends exactly one entry, so PASS-with-failure is
  impossible by construction.
- Nuance (not a kill-rule fire): the guard catches `Exception`, not `BaseException`. `KeyboardInterrupt`/`SystemExit`
  inside a body would escape and produce no summary (hence battery scores it SURVIVED — the strict direction).
  No real tool path or 30-mutant raises `BaseException` (all 30 reached the summary; observed stderr length 0).
  The claim's "an exception" is consistent with the docstring parenthetical "(a parse that raises, a decode error)".

## (3) Battery mutant source and exclusions — HOLDS

- The battery reads `git show BASE:.ufo/waves/round-96/w1/R96MutantsC1-mutprobe.py.txt`, `BASE:tools/search-rerun.py`,
  and `BASE:corpus/evidence/round96/selftest-controls-r96.py` — content-addressed, so the worktree cannot substitute
  different bytes. `_lit()` reproduces Python evaluation of all 30 probe entries exactly (0 mismatches) including the
  `n08` `str + str` form (`R97ReviewerC1-check8-literal-fidelity.txt`).
- All 28 post-exclusion `old` strings occur exactly once in both BASE and F sources; `s1`/`s2` old strings occur
  exactly once in both. The `git_env` target lines are byte-identical across BASE, the round-96 freeze, and F, so
  the Sentinel transcription (Finding 1 → `s1`, Finding 7 → `s2`) is faithful; Sentinel's own F-numbering checked
  against `R96SentinelC1.md` Findings 1 and 7 (reference copied beside this report).
- Exclusions match the seat's own verdicts: `n08` applied 0 times (`R96MutantsC1.md:34`), `n30` equivalent
  (`:154-159`). `n22` is correctly *not* excluded (seat called it equivalent-on-fixtures, not equivalent) and is
  killed by r09. The battery fails setup unless exactly 28 remain.
- The 23 R96 mutants (`MUTANTS` dict, count 23) all apply once to the F tool and are all killed; BASE-tool scoring of
  the same 30 reproduces the frozen do-nothing exactly: `BASE_KILLED=10/30` with survivors 16 PASS + n11/n12/n13/n26
  traceback-without-FAIL (`R97ReviewerC1-check11-r96-base.txt`). Predicate tallies re-run (`--no-regression`):
  `POSITIVE=1/1 EXTERNAL_KILLED=30/30 DO_NOTHING_REFUSED=1/1 R96_MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3
  NO_WRITE=1/1 BASE_KILLED=10/30 CASES=47` → `SELFTEST_CONTROLS_R97=PASS`
  (`R97ReviewerC1-check17-battery-noreg.txt`).

## (4) KILLED-rule crash path — HOLDS (no path lets a crash count)

`killed()` requires exit 1 + `SEARCH_RERUN_SELFTEST: FAIL` in stdout + no `Traceback` in stderr
(`selftest-controls-r97.py:98-102`). All 30 mutants on F print no traceback on either stream (stderr length 0,
`Traceback` in neither stdout nor stderr). A Python traceback's header always contains the ASCII token `Traceback`,
and nothing in the tool after the summary print can raise (return → `sys.exit`), so a FAIL-line-plus-crash sequence
cannot occur. The only formal gap is `stdout`: a hypothetical mutant printing its traceback to stdout would evade
the stderr-only check — none of the 30 does, and the claim's named limit (a) covers fresh mutants. The battery is
fail-closed elsewhere: any setup failure zeroes the leg (`0/N`) instead of counting partial kills, and a crashed
recursive oracle battery lacks the `SELFTEST_CONTROLS_R97=FAIL` marker, so it is *not* counted as rejected.

## (5) `os.environ` restore after r13 — HOLDS

`try: env = git_env() finally: …` (`:511-518`) restores all 7 planted keys. Simulated failure paths
(`R97ReviewerC1-check7-environ.txt`): `git_env()` raising still restores; pre-existing values restored (old `GIT_DIR`
kept, absent keys deleted); `del` cannot hit `KeyError` because `update()` just set the keys and `git_env()` never
mutates `os.environ`. The `m08`/`r13` assertions close over the returned `env` copy, unaffected by restore order.

## Defects found (low, non-firing)

1. **Stale module docstring** — `tools/search-rerun.py:48-54` still describes the 32-case self-test
   ("14 parse cases … 8 matching … 10 judgement"). At freeze the composition is 22/13/12 = 47. The `selftest()`
   docstring (`:422`) is updated; `claims.md` correctly says 47, so no sentence is false, but the user-facing
   `Usage` docstring misdescribes the shipped instrument. Command: `/usr/bin/grep -n "14 parse cases" …/tools/search-rerun.py` → line 48.
2. **KILLED-rule stream wording** — claims say "print no traceback"; the battery enforces stderr only
   (`selftest-controls-r97.py:100`). No named mutant prints a stdout traceback, and Python tracebacks go to stderr by
   default, so this is a wording gap, not a kill-rule leak.

## Residual risk / verification gaps

- Fresh-site survivors exist outside the 30 and are, correctly, under named limit (a). Probe beyond the 30
  (`R97ReviewerC1-check14-novel-mutants.txt`): separator-width loosening (`-{3,}`→`-{2,}`) and `SPLIT_RE` `\|`→`\|+`
  survive the F self-test. A third novel mutant (keeping caller's `GIT_TERMINAL_PROMPT`) is equivalent — `git_env`'s
  `update()` overwrites it — and correctly not killed. Guard/summary-line mutants are outside the 30 per limit (b).
- Battery's "Read-only on the lane" docstring inherits round-96 Finding 4 (`git status` refreshes `.git/index`); it
  does not affect the claimed `status --porcelain`/`git diff` equality, so C1 wording holds.
- Regression leg (`REGRESSION_R95=2/2`) was not re-run (~8 min); independent runs covered POSITIVE/EXTERNAL/
  DO_NOTHING/R96/ORACLES/NO_WRITE and matched every claimed tally.
- Scratch removed before yield; receipts copied to `.ufo/waves/round-97/w1/` as `R97ReviewerC1-*.txt`.

VERDICT: R97ReviewerC1 C1 held — all five scoped checks hold on re-execution; only a stale 32-case docstring and an stderr-only Traceback wording gap remain, neither falsifying any stated sentence, number, or kill rule.
