# MutC2Counter — mutation probe of the frozen C2 counter (round 61, w1)

Scope: `corpus/evidence/round61/c2-count.py` mutated in scratch copies; the frozen control runner
`controls/run-c2-controls.py` run against each mutant. Nothing under the frozen paths, `tools/`, `corpus/`
or `SKILL.md` was written. Lane `git status` shows only other seats' files; none from this seat. No installs.
Scratch `/fast/scratch/hyaku/chousa-r61/MutC2Counter/` deleted before yield.

## Findings

1. **Harness fidelity.** Pinned harness = frozen runner unmodified except three scratch-placement pins
   (counter `LANE`, runner `HERE`/`COUNTER` env, `python3 -B`). Pinned original output matches
   `controls/c2-controls.txt` line for line; the only differences are the `OK` suffix and the shell's `exit=0`.
   `C2_CONTROLS_UNEXPECTED=0`, rc 0.
2. **Frozen matrix kills 12 of 29 non-equivalent mutants** (legitimately: a control's expected verdict flips).
3. **16 mutants survive the frozen matrix** (missing controls, named below). **1 (M11) is killed only by an
   artifact**: the fleet `corpus/SOURCES.md` is absent, so census exits 2 (`ERROR: --file not found`, exit 2 per
   the census selftest `validate-missing-exit-2`) and the positive control fails for an unrelated reason.
4. **CENSUS leg never fails under any frozen variant.** No frozen control makes census exit non-zero while
   the other legs pass, so the census call is unexercised as a failing leg (M10 survives).
5. **Two mutants are verdict-equivalent** under the frozen counter (not gaps): M21 (row-resolves check)
   and M23 (opened date-format regex). Excluded from the denominator.
6. **Calibration.** Positive control kills M24, M29, M30 (intended). `echo-claims` PASS reproduces the
   recorded limit: a claim that echoes its quote passes.
7. **Candidate controls exist for every gap** (not in the frozen runner; scratch only). Each was run against
   the pinned original (expected FAIL) and against the mutant it targets (expected PASS = kill).

## Mutant table (31 mutants; M00 = pinned original baseline)

Mutants are exact single-substring replacements of `c2-count.py`, each asserted to match once and
compiled. Frozen column = which frozen variant flips the verdict (`-` = none).

| id | mutation | frozen | candidate control (run) |
|---|---|---|---|
| M01 | drop anchor-cell membership, keep text check | survives | G01 anchor `ELOOP` (not in cell): orig FAIL, M01 PASS |
| M02 | drop opened-date lower bound | KILL row-opened-old | - |
| M03 | drop used-by check | KILL row-not-used-by | - |
| M04 | drop quote word cap (<=25) | KILL quote-over-25 | - |
| M05 | drop quote word floor (>=4) | survives | G11 3-word quote Q9: orig FAIL (words=3), M05 PASS |
| M06 | quote cap 25 -> 26 | survives | G12 26-word quote: orig FAIL (words=26), M06 PASS |
| M07 | drop COVERAGE (forced 1/1) | survives | G05 no S136 quote: orig FAIL (COVERAGE 0/1 only), M07 PASS |
| M08 | drop claim/quote overlap check | KILL junk-claim | - |
| M09 | overlap threshold 2 -> 1 | survives | G03 one shared word: orig FAIL ("shares 1 words"), M09 PASS |
| M10 | drop census call (CENSUS forced 1/1) | survives | G04 unrelated malformed row S900: orig CENSUS=0/1, M10 PASS |
| M11 | census reads fleet SOURCES, not root's | KILL positive,echo (ARTIFACT) | none isolates target; fleet file absent |
| M12 | S136 resolves to any lane `.md` (ignores cell) | survives | G14 S136 cell -> `corpus/SOURCES.md`: orig FAIL (Q7,Q8 not found), M12 PASS |
| M13 | S134/S135 resolve ignores source cell | survives | G15 S134 cell without man path: orig FAIL, M13 PASS |
| M14 | drop duplicate-quote-id check | survives | G13 duplicate Q1 line: orig FAIL (QUOTES 8/9), M14 PASS |
| M15 | S136 coverage floor 1 -> 0 | survives | G05 (as M07): M15 PASS |
| M16 | drop every-quote-cited check | KILL quote-uncited | - |
| M17 | claim-count floor 4 -> 1 | survives | G06 three claims: orig FAIL (CLAIMS 0/1), M17 PASS |
| M18 | drop TRIO source-line IDs check | survives | G07 source line without S136: orig TRIO=0/1, M18 PASS |
| M19 | drop tier A/B check | survives | G08 S134 tier B: orig ROWS 2/3, M19 PASS |
| M20 | drop status=mined check | KILL row-queued | - |
| M21 | drop row-resolves check | EQUIVALENT | G15: orig FAIL, M21 FAIL (ROWS differs, verdict same) |
| M22 | drop anchor-in-resolved-text check | survives | G02 anchor in cell, not in page: orig FAIL, M22 PASS |
| M23 | drop opened date-format regex | EQUIVALENT | G09 `2026-10-28x`: orig FAIL, M23 FAIL (census E08) |
| M24 | MIN_OPENED strict (> not >=) | KILL positive,echo | - |
| M25 | LIMITS floor 2 -> 1 | survives | G10 one Limits bullet: orig LIMITS 0/1, M25 PASS |
| M26 | LIMITS forced pass | KILL no-limits | - |
| M27 | section() ignores heading | KILL no-limits | - |
| M28 | drop located-text (found) check | KILL fabricated,cross-row | - |
| M29 | overlap uses first cited quote only | KILL positive,echo | - |
| M30 | S136 tier A (calibration) | KILL positive,echo | - |
| M31 | drop whole anchor check | survives | G01 (as M01): M31 PASS |

Counts: frozen legit kills 12 (M02 M03 M04 M08 M16 M20 M24 M26 M27 M28 M29 M30); artifact 1 (M11);
survivors 16 (M01 M05 M06 M07 M09 M10 M12 M13 M14 M15 M17 M18 M19 M22 M25 M31); equivalent 2 (M21 M23).

## Missing controls (name them; each has a run candidate above)

- **G01** anchor string absent from the row's anchor cell (kills M01, M31). Frozen runner has no anchor variant.
- **G02** anchor present in cell but absent from the resolved page (kills M22).
- **G03** claim sharing exactly one 5+-letter word with its quotes (kills M09; threshold never sits at the boundary).
- **G04** census-failing row outside the C2 legs (kills M10). Also the only route by which CENSUS can fail; none in the frozen set.
- **G05** entry with zero S136 quotes and otherwise valid (kills M07, M15; COVERAGE is never the sole failing leg).
- **G06** three claims (kills M17; no claim-count-below-4 variant).
- **G07** TRIO source line that omits S136 (kills M18).
- **G08** registry tier B on an S134/S135 row (kills M19).
- **G10** one Limits bullet (kills M25; only the zero-bullet case is frozen).
- **G11** 3-word quote (kills M05; no lower-bound variant).
- **G12** 26-word quote (kills M06; the 25/26 boundary is untested; the frozen 32-word quote only proves >25 fails).
- **G13** duplicate quote id (kills M14).
- **G14** S136 source cell naming another lane file (kills M12; S136 resolution is never varied).
- **G15** S134 source cell without the man path (kills M13).
- **G-census-target** (artifact gap, M11): no control shows the census target is the root's file. A control
  needs a clean SOURCES at the fleet path with a broken root SOURCES (G04 shape), so M11 passes while the
  original fails.

## Recorded limit (confirmed)

`echo-claims` PASS: a claim that echoes its quote shares 2+ words and passes. Frozen-matrix limit, as claimed.

## Equivalence notes

- M21: an unresolved row makes its quotes fail `found`, so FAIL regardless of ROWS (G15 output: orig
  `ROWS=2/3 QUOTES=5/8`; M21 `ROWS=3/3 QUOTES=5/8`, both FAIL).
- M23: census `E08 opened not a past/present ISO date` rejects malformed dates, so CENSUS=0/1 (G09 output:
  both FAIL). The counter's regex is redundant given CENSUS; CENSUS, not C2's own ROWS, carries the date-format check.

## Evidence pointers

- Baseline: `M00` pinned original reproduces `controls/c2-controls.txt` (diff: `OK` suffix and `exit=0` only).
- M11 kill cause: `census on absent fleet SOURCES.md: rc = 2 | ERROR: --file not found`.
- Census on the lane file, cwd=lane: `rc=0 {'W': 5, 'o': 1} file ok`. [INFERENCE] census takes its root as the parent of `corpus/` of `--file`: a copy outside the lane gives `E11 missing used-by`, so used-by checks are root-relative.
- Candidate-control results G01–G15 and G-census are quoted per row above, from counter runs on the pinned original (`C2=FAIL`, reason in detail lines) and on each mutant.

VERDICT: COUNTER_MUTANTS_KILLED=12/29 control_gaps=17
