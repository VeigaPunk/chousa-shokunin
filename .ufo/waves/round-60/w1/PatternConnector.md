# PatternConnector — round 60 bounded proposal

## Evidence

- The frozen C1 predicate requires an exact-token injection mutant to be scored as a failure, a safe candidate path, and the pinned destructive baseline (`corpus/evidence/round60-claims.md:7-11`). The current counter's `run()` labels a builder `candidate_safe` solely from return code zero plus an intact seeded foreign file (`corpus/evidence/round60/c1-count.py:32-44`); its mutant gate is merely `forge_state != "forged_safe"` (`:58-70`).
- This creates a false-acceptance path: an output-only builder that prints `=PASS`, returns zero, and writes no valid result leaves the foreign file intact and satisfies the exact same `candidate_safe` predicate. C1CounterCritic reports reproducing this against the current counter: `INJECTION_REJECTED=1/1`, `CANDIDATE_REFUSAL=1/1`, `C1=PASS`, exit 0 (`.ufo/waves/round-60/w1/C1CounterCritic.md:5-19`). This is not a raw-output substring influence; it is a no-op misclassified as a successful candidate.
- Prior committed R59 evidence independently demonstrated the old counter's direct output-token spoof and its inaccurate leg acceptance (`.ufo/waves/round-59/w1/R59Executor09.md:215-260`). This round's counter avoids that exact substring scan, but the above classification gap means the frozen mutant-rejection requirement remains unproved.
- The current builder's actual normal path writes `spans.tsv` and span files (`tools/build-spans.py:197-212`), furnishing a concrete result surface to check. This scoped probe does not establish the broader seven-hazard matrix; C1 itself disclaims that (`round60-claims.md:7`).
- Freeze-integrity caveat: assignment gives immutable claim SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; observed `sha256sum` of the named file was `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. These contradict. Do not treat either digest as verified frozen identity until an authorized owner resolves it; no claim-file edit was made here.

## Affected axes

- **Operability (C1, primary):** required verdict predicate can accept a no-op output-injection mutant, so it does not currently measure the frozen condition it names.
- **Calibration (secondary):** `INJECTION_REJECTED=1/1` means only “not classified as destructive”; it overstates what the observation establishes.
- No evidence here supports a depth/C2 or builder-security improvement. Keep C1 measurement evidence and C2 source/QUALITY evidence causally separate, as the connector proposal also recommends (`PlanningConnector.md:17-30`).

## One bounded move

Replace the foreign-file-only `candidate_safe` classification with a typed result check that requires both (1) the sentinel remains byte-identical and (2) the expected output manifest/span bytes for the seeded quote are independently observed. Give the injection control an explicit expected `invalid/missing-result` state and require that exact state; do not define rejection as merely “not the destructive-baseline state.” Keep the pinned R55 control as its own destructive-state assertion. This is a single C1 predicate repair: it prevents an output-only no-op from being credited as safe without broadening the claim to all hazards. Preserve claim-local evidence fields (candidate result, baseline result, mutant result, exit code) rather than collapsing them into a shared PASS that could bleed into C2.

## Risks and contradictions

- The added artifact condition must be derived from fixture-known expected bytes, not builder stdout or builder-authored success labels; otherwise it recreates a forge channel.
- A wrong or over-specific expected manifest can reject a valid implementation. Pin the test fixture and expected bytes, and exercise both the real candidate and the mutant.
- The pinned destructive baseline proves discrimination for this sentinel scenario only, not general baseline provenance or full builder security.
- The observed claim digest mismatch is unresolved and blocks treating this analysis as bound to the assignment's asserted immutable claim bytes. Do not rewrite the frozen claim or silently reconcile the contradiction.

## Verification

On authorized, digest-confirmed frozen inputs, run the frozen C1 command in a fresh absolute work directory with three separately recorded outcomes: (a) candidate returns success, preserves foreign bytes, and produces exact expected fixture output; (b) pinned R55 returns success and deletes the sentinel; (c) print-`=PASS`/return-zero/no-output mutant preserves the sentinel but fails the candidate-output predicate and is explicitly rejected. Require nonzero top-level result when any condition is false; inspect stdout only as diagnostic. Reconfirm the claim SHA before calling this a verification of the frozen predicate. No tests were run by this seat.