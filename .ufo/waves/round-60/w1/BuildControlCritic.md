# BuildControlCritic — C1 counter control-path critique

## Counterexample

The frozen C1 claim says captured child output cannot establish a leg and that the injection mutant must be rejected (round60-claims.md:7–11). The new counter does not meet that condition: its `forged.py` prints `=PASS` and exits 0 (round60/c1-count.py:58–63), but `run()`'s returned state is derived only from return code and whether the seeded foreign file remains intact (round60/c1-count.py:32–44). Because that mutant leaves the seeded file intact, it is labeled `candidate_safe`, not `forged_safe`; `forge_blocked = forge_state != "forged_safe"` therefore reports success (`INJECTION_REJECTED=1/1`) for a mutant it never recognizes as injection. The output is genuinely excluded from derivation, but the injection test is vacuous with respect to output injection: it cannot demonstrate the specified rejection or distinguish a builder that emits the forged success token while satisfying this one filesystem predicate.

Also, `baseline_bad` and `forged_safe` have the identical condition (`p.returncode == 0 and not intact`, lines 42–43), and the `baseline_bad` branch precedes `forged_safe` (line 44); thus `forged_safe` is unreachable. The code's classification does not represent three distinct structured states as the claim calls for.

## Evidence and strongest available control

- Current counter: `corpus/evidence/round60/c1-count.py:22-45,58-75`.
- Frozen claim and its exact requirement: `corpus/evidence/round60-claims.md:5-11` (frozen SHA supplied by assignment: `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`).
- Pre-work receipt shows candidate and pinned r55 both delete the foreign file and the probe fails as expected: `.ufo/waves/round-60/c1-before.txt:2-8`; this is baseline state, not after-work verification.
- Prior committed R59 evidence demonstrates why a narrow real counterexample matters: `.ufo/waves/round-59/w1/R59Executor09.md:215-260` records exact `C1=PASS`, exit 0, from output-injected candidate despite seven refusal failures; lines 262–290 document additional leg/path weaknesses. It supports the risk but does not establish that the current counter fails its own final evaluation.
- The pinned r55 control is intended to distinguish destructive behavior (`.ufo/waves/round-60/c1-control-proof.txt:1-5`); the current code labels baseline destruction, but that does not repair the independent injection mutant test.

## Impacted axes / verdict relevance

**Operability (C1, lowest numeric axis): harmed/unverified against its frozen predicate.** The counter is runnable, but its purported injection-rejection result does not verify the claim's required property; it can provide a false positive for that subtest. This is a fixable counter defect, not a reason to reject the research task or a general objection to structured states. No after-work execution evidence was in my assigned current-counter/prior-evidence scope, so I do not assert the overall final `C1` verdict.

## Smallest safe correction

Make the injection mutant fail for the intended reason in a fixture with an independently known refusal outcome (e.g. return nonzero while emitting the exact forged success token), and assert that the counter's resulting verdict is failure—not merely that a state label differs. Ensure its state label cannot equal `candidate_safe`. Replace the overlapping `baseline_bad`/`forged_safe` conditions with mutually exclusive states, and add a direct assertion that each control maps to its declared state. Keep child output diagnostic-only; never reintroduce text matching as verdict authority.
