# C1AlternateControl — alternate-control analysis

## Scope and immutability

I analyzed only the frozen C1 claim, the current C1 counter/source, and prior committed evidence. The claim text requests structured per-leg states and specifically requires a success-output injection mutant to be scored as failure; it does not assert that the span builder meets all hazards (`corpus/evidence/round60-claims.md:5-11`; assignment-provided immutable SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`). I did not modify that frozen file. A local digest observed during this investigation was `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`, which differs from the assignment-provided SHA; this discrepancy is unresolved and means I cannot independently affirm the on-disk bytes match the supplied immutable digest. The stated claim text was present as read.

## Independent alternate control

The counter's test mutant is not discriminating: it prints the exact success token and exits zero, but does not implement a builder or produce expected output. `run()` assigns `candidate_safe` whenever the process exits 0 and the seeded foreign file remains intact (`corpus/evidence/round60/c1-count.py:22-44`). Thus this mutant maps to the candidate-safe state. Yet `forge_blocked` is defined as `forge_state != "forged_safe"` (`:58-63`), so that same candidate-safe mapping counts as injection rejection. The candidate leg uses the identical loose condition (`:68-70`). Consequently the top-level pass can coexist with the output-only mutant being accepted as safe; merely excluding stdout/stderr from classification does not establish the claimed mutant rejection.

The labels themselves are not distinct: `baseline_bad` and `forged_safe` have identical predicates, with baseline checked first, making `forged_safe` unreachable (`c1-count.py:41-44`). This is direct source evidence that the supposed per-leg structured classifications do not encode distinct control outcomes.

A prior independent replay against this counter records the executable counter command, all three 1/1 lines, `C1=PASS`, exit 0 for a builder that only prints `=PASS` and exits successfully (`.ufo/waves/round-60/w1/C1CounterCritic.md:5-19`). This demonstrates the alternate control's observable false acceptance, rather than only a theoretical concern. Prior committed R59 evidence documented output-forged C1 pass in the earlier counter (`.ufo/waves/round-59/w1/R59Executor09.md:215-260`), useful context but not a substitute for testing this counter.

## Verdict and limits

**C1 counter claim: not established / fails its frozen injection-rejection predicate** with high confidence. The cited replay and source logic show an output-only, success-returning mutant can be counted as rejected while the counter passes. No conclusion here establishes whether a newer counter revision, if one exists outside this inspected source, closes the defect; nor does this narrow probe determine the builder's full hazard behavior. The appropriate control must be independently known to be invalid (for example, return nonzero while emitting the forged token) and its expected state asserted distinctly; candidate-safe should additionally require an independently observed expected artifact/result. These are analytical recommendations, not edits made by this seat.

## Evidence integrity

Observed claim digest disagrees with the assignment's expected immutable SHA; no attempt was made to repair or rewrite it. No external fetches, source changes, git/jj operations, or tool installs were performed. Scratch `/fast/scratch/hyaku/chousa-r60/C1AlternateControl` was created for the seat and removed before completion.
