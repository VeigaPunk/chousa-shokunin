# Round 48 — frozen claims (chousa)

author: chousa L1 (hyaku run 6)
date: 2026-10-25
freeze: before any round-48 candidate change or wave-2 scoring
base: `d4e6ef09b755a961bdae56566a7dcf0c9db0cfd7`

No external fetch or network egress: L0 `8d77e6c1` remains open. The R47 source/counter captures are local committed files. This single claim works the lowest-scored non-retired axis, operability (3/10; `SCORECARD.md:7`).

## R48-C1 — operability — the polarity check has a held-out precision floor and covers the five surviving refinements

**Frozen predicate (one sentence):** `python3 corpus/evidence/round48/c1-count.py` exits 0 only when the landed tool passes all five R48 refinement fixtures, passes at least 11 of the 12 R47 held-out correct-bullet cases, and passes the unchanged round-47 C1 counter; `python3 corpus/evidence/round48/mutation-check.py` exits 0 only when each of the five R47 surviving mutants is killed by one named R48 refinement case.

- Counting commands: `python3 corpus/evidence/round48/c1-count.py`; `python3 corpus/evidence/round48/mutation-check.py`.
- Before (`controls/before.txt`): current round-47 tool passes R47 C1 and all five feature fixtures, but the precision set is `CORRECT_BULLETS_PASS=9/12`, target 11/12; full C1 exits 1. The `/usr/bin/true` control yields `REFINEMENT_CASES=0/5`, exit 1. The frozen mutation probe is `MUTANTS_KILLED=5/5` on the landed control tool; the previous R47 counter, by contrast, passed all five mutants at full scores in `.ufo/waves/round-47/w2/MutC1Refined.md`.
- Target: `REFINEMENT_CASES=5/5`, `CORRECT_BULLETS_PASS>=11/12`, `LEGACY_R47=PASS`, `C1=PASS` exit 0, plus `MUTANTS_KILLED=5/5` exit 0.
- Controls: old tool 9/12, below the precision target; `/usr/bin/true` fails the five positive/negative refinement expectations; old C1's 3/3 junk and 3/3 positives remain required by the R47 counter. Counter/mutant byte transforms are in `mutation-check.py` and run only in a temporary directory.
- Kill rule: any missing/changed fixture, precision count below 11/12, failed legacy leg, fewer than five refinement cases, any mutant surviving, or nonzero harness error means C1 fails.
- Tag: plumbing. No semantic-entailment claim is made; human correctness of this fixed set remains outside this lexical counter and is a required closure spot-check.

## Admission rule

This claim is admitted only if its frozen counters meet all listed legs and no owned axis is harmed. A counter score does not overrule the external verification's verdict on the held-out examples.
