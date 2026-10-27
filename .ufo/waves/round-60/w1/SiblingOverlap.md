# SiblingOverlap — bounded cross-proposal analysis (round 60)

## Evidence and scope

This connector uses the frozen claims, current counters, and committed round-59 evidence/proposals only. The round-60 claim file currently hashes to `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`, not the assignment-specified immutable SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440` (observed `sha256sum`). Freeze-integrity discrepancy: do not silently treat either digest as authoritative; preserve the file untouched and reconcile provenance before claim admission.

- Frozen C1 is specifically a counter-integrity claim, requiring a safe candidate, destructive pinned control, and rejection of an exact-token injection mutant (`corpus/evidence/round60-claims.md:7-11`). It does not claim the builder meets all hazard legs.
- Prior round-59 evidence demonstrates the previous counter's output-substring false positive and broader hazard coverage problems (`.ufo/waves/round-59/w1/R59Executor09.md:215-260`). This is relevant context, not proof the new counter is fixed.
- Current C1's `run()` labels any zero-exit builder leaving the seeded foreign file intact `candidate_safe`, then uses that same classification for the forge (`corpus/evidence/round60/c1-count.py:35-44,57-75`). The dispatched C1 critic provides a measured exact-token-printing, exit-zero, no-op mutant that produces `C1=PASS`, exit 0 (`.ufo/waves/round-60/w1/C1CounterCritic.md:5-19`). Thus the apparent output-channel isolation is insufficient: a single filesystem sentinel establishes only non-destruction, not successful expected behavior.
- The pre-work receipt independently says injection/control pass but candidate safety fails (`.ufo/waves/round-60/c1-before.txt:3-8`). It cannot be presented as target success.
- C2 remains a separate depth/source claim (`round60-claims.md:13-16`). Its current counter's entry path targets an existing knowledge note, and the sibling audit reports base-state `C2=PASS`, contradicting the frozen base-fails requirement (`.ufo/waves/round-60/w1/C2CounterAudit.md:5-18`). A source-grounding receipt cannot validate C1 runtime behavior, and C1 evidence cannot validate C2's new-note/citation gate.

## One bounded move

Use a claim-local evidence ledger in the final round report, not a shared aggregate verdict: for C1 record frozen-file digest status, exact counter/builder/control identities, each required state, and exit code; for C2 record the exact new-entry identity, offline source pin/quote, metadata, and QUALITY disposition. Keep each claim's predicate and evidence independent. For C1, do not admit a PASS unless the output-only no-op mutant is separately rejected and the safe candidate has an independently observed expected artifact/result; the current one-file preservation observation is not sufficient. This is a bounded verification/reporting move that does not alter either frozen predicate or assert fixes.

## Axes, contradictions, risks

- **Operability:** improves auditability by keeping each required C1 leg and C2 gate independently inspectable, without letting shared PASS evidence conceal failure.
- **Depth:** preserves the distinction between the narrow foreign-file probe and the historical seven-hazard matrix; neither is overstated as the other.
- **Calibration/discernment:** current C1 emits `INJECTION_REJECTED=1/1` and `C1=PASS` for the no-op forge per the measured sibling counterexample, so that label contradicts the frozen requirement. Current C2 base PASS also contradicts the frozen base-fail requirement per sibling audit. Do not smooth these into round success.
- The assignment SHA differs from observed bytes; until provenance is resolved, claim-to-freeze binding is itself uncertain.
- A ledger can become another misleading aggregate if reduced to green checkmarks. Retain raw claim-local predicates, input identities, and explicit unknowns. No C1 result proves broad builder security; no C2 result proves current external validity.

## Verification

No tests or counters were run by this seat. Verify the frozen claim bytes against the required digest without editing them; re-run the exact C1 counter plus the no-op mutant and inspect all predicates; run C2 against the frozen base and target state while verifying root isolation and new-entry identity; preserve separate outputs and claim verdicts. This report is the only lane write by this seat; no installs or git/jj mutations.