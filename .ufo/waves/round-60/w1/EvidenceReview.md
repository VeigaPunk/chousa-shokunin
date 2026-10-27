# EvidenceReview — round 60

## Findings

### High — frozen C1 counter still misclassifies the output-injection control

`corpus/evidence/round60/c1-count.py:41-44` sets both `candidate_safe` and `forged_safe` from the same predicate (`returncode == 0`), distinguished only by whether the seeded foreign file is intact. The forge generated at lines 58-62 only prints `=PASS` and exits 0; it leaves the seeded file intact, so it is classified `candidate_safe`. Consequently `forge_blocked = forge_state != "forged_safe"` at line 63 is true, despite the forge being accepted by the ordinary candidate-safe branch. This does not satisfy frozen claim C1's requirement that the exact-token forge be scored as failure (`corpus/evidence/round60-claims.md:7-11`), and the `INJECTION_REJECTED` label is unsound. W1 `C1LogicCritic.md:5-14` independently describes the same classification and records a scratch execution yielding `INJECTION_REJECTED=1/1` while `C1=FAIL`; the counter's label cannot establish rejection.

The counter's independent filesystem observation is useful for detecting the pinned r55 deletion control, but it does not distinguish a forged no-op from a successful safe candidate. The output bytes remain excluded from verdicts, yet no forge-specific failure state is actually required. Thus the narrow measurement-integrity claim is not established, irrespective of whether the candidate and baseline legs behave as expected.

### Evidence integrity — supplied immutable SHA does not match present file

Assignment specified frozen claim SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`. SHA-256 of the present `corpus/evidence/round60-claims.md` is `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`; `git status --short -- corpus/evidence/round60-claims.md` reports it untracked, and the claimed base `b379919a873e7080a31ef92c7002f55f5374e2c6` has no such path. I did not alter it. Therefore I cannot authenticate this on-disk text against the supplied immutable SHA or base commit; findings above are explicitly against the bytes currently present. This discrepancy warrants freeze-provenance review, not a claim about when the bytes changed.

## Residual risk and verification gaps

This is a bounded evidence review, not a full run of either round-60 counter or a review of the remaining C2 claim. I did not run further commands or mutate the frozen claim file. The report's C1 conclusion follows directly from the counter's predicates and generated forge; the reported execution is cited from the independent W1 critic, not represented as my execution.