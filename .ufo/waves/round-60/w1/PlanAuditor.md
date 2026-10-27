# PlanAuditor — round 60

Scope: plan/predicate audit of the assigned frozen claims, prior committed evidence, and current C1/C2 counters/source. No edits to claims, counters, or source; no counter execution or external fetch.

## Findings (severity order)

### High — Frozen-claim identity is not reproducible from the assigned file

The assignment pins SHA-256 `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; `sha256sum corpus/evidence/round60-claims.md` returned `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. `git status --porcelain -- corpus/evidence/round60-claims.md` returned `?? corpus/evidence/round60-claims.md`; `git show b379919a873e7080a31ef92c7002f55f5374e2c6:corpus/evidence/round60-claims.md` reported that the path is absent from the named base. Thus the reviewed bytes neither match the supplied immutable identity nor have provenance in the stated base. Cause/timing is not established. Leave the file untouched and do not treat this as permission to redefine the predicates; the freeze owner must reconcile identity before a verdict can rely on those bytes.

### High — C1's injection control cannot fail the way its frozen predicate requires

The frozen C1 predicate requires the output-injection mutant to print `=PASS` and be scored as failure (`corpus/evidence/round60-claims.md:7-11`). The current counter's `run()` marks any zero-exit child that preserves the sentinel `candidate_safe` (`corpus/evidence/round60/c1-count.py:38-44`). Its control prints `=PASS` and exits 0 without modifying the fixture (`:58-63`), so it is assigned `candidate_safe`; `forge_blocked = forge_state != "forged_safe"` is therefore true (`:62-63`). Moreover, `forged_safe` duplicates the `baseline_bad` condition and is unreachable because `baseline_bad` is tested first (`:41-44`). The mutant is counted rejected without being scored as failure; the counter can report `INJECTION_REJECTED=1/1` for the exact success-token output the claim says must fail. The control also does not exercise any hazard, unlike the prior committed counterexample: `R59Executor09.md:215-260` records `C1=PASS`, exit 0 while all seven refusal legs fail after token injection. This is a direct mismatch between the frozen target and the current test design, not evidence that the production builder is safe or unsafe.

### High — C2 counter does not test the claimed round-60 note or disposition

The frozen C2 predicate requires a new scoped note, exact observation/no-overreach checks, citation/metadata checks, and the scorecard disposition; it says the base must fail because no round-60 entry exists (`corpus/evidence/round60-claims.md:15-19`). The counter instead binds `ENTRY` to the existing `citation-count-semantics-r37.md` (`corpus/evidence/round60/c2-count.py:8,13`) and only tests generic metadata/scope substrings (`:17-21`); it neither locates a round-60 entry nor reads/checks the scorecard disposition. Consequently the stated base-fail condition and the claimed new-entry after-state are not measured. Also, although the CLI accepts `--root`, the capture form path is fixed to script `ROOT`, not the supplied lane-copy root (`:5-8,13`), so a copy-based measurement does not fully measure the requested root. The C2 predicate is therefore not implemented by this counter; a passing result would not establish the claim.

## Residual risk and verification gaps

- The current counters were inspected, not executed; runtime verdicts are unverified.
- The LSP device is not mounted (`xd://lsp` returned “No such tool”), so no semantic references/diagnostics pass was available. Findings above are grounded in the frozen-claim text and direct counter control flow.
- Offline S101 evidence in `corpus/evidence/round59/s101-open.txt:242-267` supports only the bounded bibliographic type/carrier observation; it does not cure the C2 counter/claim mismatch or establish present-day validity/CNKI implementation.

## Recommendation

Do not admit either claim on these counter predicates as currently implemented. Reconcile the frozen-claim byte identity first; then require C1's injection mutant to be distinguishable and rejected by the asserted state predicate, and require C2 to measure the new entry and declared disposition through the supplied root. No claim or counter was changed by this review.