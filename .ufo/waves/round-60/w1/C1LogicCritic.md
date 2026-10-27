# C1LogicCritic — round 60 counterexample

## Counterexample

The new counter does not actually prove that the output-injection mutant is rejected. In `corpus/evidence/round60/c1-count.py`, `run()` computes `candidate_safe = p.returncode == 0 and intact` and `forged_safe = p.returncode == 0 and not intact` (lines 41–43), then tests `candidate_safe` first in its nested conditional (line 44). For the generated forged builder, which prints `=PASS` and exits 0 without touching the seeded foreign file (lines 58–62), `candidate_safe` is true and wins. The state is therefore `candidate_safe`, not `forged_safe`; `forge_blocked = forge_state != "forged_safe"` (line 63) incorrectly records this as a successfully blocked injection. The two states are effectively a mislabeled partition of return-code/filesystem outcomes, not distinct semantic outcomes: the forged process passes the safe leg solely because the only observed property is preserving this foreign file.

This directly contradicts the frozen predicate's requirement that the same exact-token output forge be scored as failure, and the claim's after-target that this counter rejects that forge (round60-claims.md:9–11). `INJECTION_REJECTED=1/1` is a false positive, not evidence of rejection.

## Evidence

- Current counter: `corpus/evidence/round60/c1-count.py:37-44,58-75`; in particular, the test forge only emits `=PASS` and returns 0, and the outcome check never examines stdout/stderr. Its third returned state is unreachable because `candidate_safe` and `forged_safe` are complementary when return code is zero and `intact` is boolean.
- Exercised command (scratch only): `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round60/c1-count.py --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --work /fast/scratch/hyaku/chousa-r60/C1LogicCritic/probe --seed 6001`
  Output: `INJECTION_REJECTED=1/1`, `BASELINE_DISCRIMINATES=1/1`, `CANDIDATE_REFUSAL=0/1`, `C1=FAIL`; process exit 1. The injection metric reports success despite the logic above. The overall failure is not a pass/fail verdict on this specific defect.
- The prior committed counterexample is independently documented in `.ufo/waves/round-59/w1/R59Executor09.md:215-260`: the round-58 counter credited an output-echoing, hazard-failing builder with `C1=PASS`, exit 0. That makes checking the forge leg semantically essential; merely keeping child output out of the verdict is insufficient if the forge's return code and seeded-file state are themselves classified as the ordinary safe-candidate leg.

## Impacted axes

- **Operability (direct, lowest numeric axis):** the claimed measurement-integrity correction has a false-positive control; its output does not establish the stated observable outcome.
- **Calibration (evidence/reporting risk):** the `INJECTION_REJECTED` label overstates what the counter verifies. No separate calibration change is claimed here.

## Smallest safe correction

Make the injection leg observably fail as a test candidate and assert that failure independently—for example, have `run()` return a structured result containing the process return code, foreign-file preservation, and an explicit eligibility/result category, then require the forge-specific expected failing outcome rather than `state != "forged_safe"`. Do not infer injection rejection from a state that the ordinary candidate-safe branch can produce. Keep captured prose diagnostic-only. Add a regression assertion that fails if the generated `=PASS` forge is classified `candidate_safe` or makes `INJECTION_REJECTED=1/1`.