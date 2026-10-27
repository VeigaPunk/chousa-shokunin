# CarryDebtCritic — frozen-claim counterexample

## Counterexample

C1's purported “same exact-token forge” does **not** test a failing refusal leg. The generated mutant at `corpus/evidence/round60/c1-count.py:58-63` only prints `=PASS` and exits 0. `run()` seeds a foreign file and classifies any successful builder that leaves that file byte-identical as `candidate_safe` (`:32-44`). Consequently the mutant is necessarily categorized as non-`forged_safe` (the latter requires deleting the foreign file), so `INJECTION_REJECTED=1/1` passes for the wrong reason. But when that same mutant is passed as `--builder`, it is classified `candidate_safe`; the counter's candidate leg therefore accepts this output-injection-only builder. This is an observable false assurance in the very counter which frozen C1 claims proves output injection cannot satisfy a failing leg.

The structural issue is broader than the literal code: `candidate_safe` and `forged_safe` differ only in the independently observed foreign-file outcome, not in any structured observation that a refusal/hazard leg was met. The one scenario neither establishes that the builder refused an unsafe operation nor exercises output bytes contaminating a refusal predicate. The counter also creates but never uses `forged_safe` for the predicate's intended mutant rejection except via that unrelated foreign-deletion distinction.

## Evidence

- Frozen target and kill rule: `corpus/evidence/round60-claims.md:7-11` require a “failing leg” not to pass by output injection and explicitly call for the same exact-token forge to be rejected.
- Counter mutant, classification, and verdict conjunction: `corpus/evidence/round60/c1-count.py:32-44,58-75`; in particular `:41-44` makes intact foreign file + rc 0 `candidate_safe`, and `:60` is the injected builder.
- Builder's actual contract: `tools/build-spans.py:150-153,186-213` refuses on malformed/unavailable text rows by stderr + exit 1; the counter's synthetic builder does none of this and exits 0.
- Prior committed demonstration of the class of defect: `.ufo/waves/round-59/w1/R59Executor09.md:215-260` reproduces `C1=PASS`, exit 0 with every refusal leg failing and token injected in stderr; its §7 (`:262-290`) also shows a refusal leg can be overwritten by an independent condition. Prior lesson explicitly said the refusal path needed an isolated verdict channel (`corpus/lessons/round-59.md:28,31-33`).
- Frozen artifact SHA checked read-only: `round60-claims.md` currently hashes to `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`, which does **not** equal the assignment-supplied expected SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`. Treat claims file as authoritative only after this provenance mismatch is resolved by the freeze owner; do not amend it or infer a new predicate. Observed lane HEAD is the declared base `b379919a873e7080a31ef92c7002f55f5374e2c6`; claim and round-60 counter are untracked at this checkout, so this is not a committed counter demonstration.

## Impacted axes

- **Operability:** C1's acceptance counter does not establish the claimed injection rejection; the verdict is not trustworthy on the frozen predicate.
- **Calibration:** reporting `INJECTION_REJECTED=1/1` as evidence of rejection overstates what this mutant tests.

## Smallest safe correction

Keep the frozen predicate unchanged. In the counter, make a mutant that actually returns the unsafe/refusal-leg failure state while printing the target token, then assert its independently observed structured refusal-leg result is failure and that it cannot satisfy the aggregate predicate. Separately validate the candidate's intended safe path and pinned destructive control with typed states bound to filesystem outcomes; do not count rc 0 or captured text alone as proof of a hazard refusal. Re-run and report against the frozen predicate only after its expected SHA is reconciled. This is a blocking counterexample to the C1 after-state, not evidence that the builder itself is fixed or that any hazard battery passes.
