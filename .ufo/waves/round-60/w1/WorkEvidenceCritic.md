# WorkEvidenceCritic — round-60 work-evidence review

## Counterexample

The round-60 C1 implementation does not satisfy the frozen output-injection discriminator: its synthetic `forged.py` only prints `=PASS` and exits 0, while `run()` classifies a run as `candidate_safe` from return code 0 plus an intact seeded foreign file. Thus the forge is not labeled `forged_safe`, `forge_blocked = forge_state != "forged_safe"` becomes true, and the top-level counter can credit this no-op as both rejected forge and safe candidate. This is a false positive in the test's evidence, not direct verdict authority from stdout: the output bytes are ignored, but the fixture's independent checks are insufficient. Independently, `baseline_bad` and `forged_safe` have identical conditions and the former branch wins, making the latter unreachable. (`corpus/evidence/round60/c1-count.py:22-44,58-75`; frozen requirement `corpus/evidence/round60-claims.md:7-11`.)

## Evidence

- Prior committed R59 counterexample establishes a distinct historical failure: candidate-controlled stderr containing `=PASS` let the R58 aggregate counter report `C1=PASS` while every refusal leg failed, including a symlink-output write (`.ufo/waves/round-59/w1/R59Executor09.md:215-260`). It motivates the new measurement-integrity claim but does not itself establish the current counter's verdict.
- Current code is inspectable at `corpus/evidence/round60/c1-count.py:32-44,58-75`; it captures output but state derives from return code and foreign-file bytes only. No expected output artifact or quote-processing result is checked.
- Independent W1 review reports an exact run of the no-op `=PASS` builder against this counter returning `INJECTION_REJECTED=1/1`, `CANDIDATE_REFUSAL=1/1`, `C1=PASS`, exit 0 (`.ufo/waves/round-60/w1/C1CounterCritic.md:5-19`). This is reported evidence, not a rerun by this reviewer.
- A separate W1 critique reaches the same source-level defect and identifies the unreachable/overlapping state (`.ufo/waves/round-60/w1/BuildControlCritic.md:5-7,11-23`).
- Frozen pre-work result is `C1=FAIL` because candidate and pinned R55 both delete the seeded foreign file (`.ufo/waves/round-60/c1-before.txt:2-8`); it is not after-work proof.
- Freeze identity caveat: assignment specifies immutable claim SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`, while the W1 connector reports observed file SHA `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` (`.ufo/waves/round-60/w1/PatternConnector.md:9`). Do not assert which identity is authoritative based on these conflicting records; frozen claims were not changed.

## Impacted axes

- **Operability (C1, lowest numeric axis):** the frozen predicate's injection-rejection clause is not established and has a demonstrated false-positive path, so the claimed counter correction cannot be credited as verified. The counter remains a runnable narrow probe; this evidence does not establish overall builder safety or the full seven-hazard matrix.
- **Calibration (secondary):** `INJECTION_REJECTED=1/1` and `CANDIDATE_REFUSAL=1/1` overstate what their predicates check: the former means only “not classified as destructive baseline,” while the latter means only “return code zero and sentinel intact.”

## Smallest safe correction

Require `candidate_safe` to include an independently observed expected result for the seeded quote (e.g. exact expected span/manifest output), not just preservation of the unrelated sentinel. Give the injection fixture an explicit expected invalid/missing-result state and require that exact state; make the output-only, zero-exit mutant fail the injection predicate and make the aggregate command fail when tested as candidate. Make control classifications mutually exclusive and assert each control's declared state. Keep child output diagnostic-only. Then rerun the frozen command with fresh work and preserve its output; do not infer broader hazard coverage from this narrow counter.

Scope: review only of frozen claims, local current counter and prior/current evidence. No external fetches, edits to claims, source changes, git/jj operations, or installs. Scratch `/fast/scratch/hyaku/chousa-r60/WorkEvidenceCritic` removed before yield.
