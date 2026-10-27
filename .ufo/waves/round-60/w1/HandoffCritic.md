# HandoffCritic — round-60 bounded counterexample review

## Counterexample

Both frozen claims can be falsely reported as passing without establishing their specified predicate. For C1, `corpus/evidence/round60/c1-count.py:37-44,60-75` marks any successful builder that preserves one seeded foreign file as `candidate_safe`. A no-op or the test's forged builder (`print('=PASS'); return 0`) preserves that sentinel, so the forged mutant is classified as safe, `forge_blocked` becomes true, and it can yield `C1=PASS`. This is not merely child-output-token parsing: the counter's replacement state predicate confuses “did not delete this sentinel” with “reached the safe builder path.” The frozen claim requires output-injection mutant failure and the actual independently observed safe path (`corpus/evidence/round60-claims.md:7-11`). A peer's local attack report reproduces this precise case and reports `INJECTION_REJECTED=1/1`, `CANDIDATE_REFUSAL=1/1`, `C1=PASS`, exit 0 (`.ufo/waves/round-60/w1/C1CounterCritic.md:5-19`).

C2 has an independent false-positive. Its frozen predicate explicitly requires base failure absent a round-60 note, and checking the new note's exact source-grounded observation (`corpus/evidence/round60-claims.md:15-16`). The current audit reports `c2-count.py` exits 0 on existing base state, because it checks the already-present `corpus/knowledge/citation-count-semantics-r37.md` for generic scope/metadata substrings rather than requiring a new round-60 artifact; it also reads the pinned form from script-global `ROOT` rather than CLI `--root` (`.ufo/waves/round-60/w1/C2CounterAudit.md:5-18`). Thus a pass does not establish round-specific change or a lane-copy-isolated source chain.

## Evidence limits / provenance

I read the frozen claims and current C1 source plus the two peer attack reports. The assignment-specified frozen SHA is `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; the C2 audit records a locally observed SHA mismatch (`C2CounterAudit.md:22`). I did not recompute or modify the frozen file, and cannot reconcile that discrepancy from these observations. Treat the assignment's frozen SHA as required identity and have the freeze owner resolve any observed conflicting digest before admission. No direct executions were performed for this review; C2 reproduction and SHA observation are attributed to the cited peer report, not presented as my own runs. Neither counter PASS should be interpreted as proof of the broader builder hazards or present-day bibliographic truth.

## Impacted axes

- **Operability (C1, lowest claimed axis):** false positive allows a no-op/output-only builder to satisfy the claimed refusal regression.
- **Depth (C2):** a generic pre-existing entry can substitute for the claimed new scoped reasoning.
- **Discernment/calibration:** verdict labels overstate the evidence; C2 additionally risks mixed-root provenance.

## Smallest safe correction

C1: independently assert the candidate's expected successful artifact/result in addition to sentinel preservation; add the exact print-token/zero-exit/no-output builder as a control and require it to fail the injection predicate and make the top-level counter exit nonzero. Do not credit “not destructive in this one fixture” as success.

C2: bind the check to the specific new round-60 note (or a frozen base-vs-target identity/diff), check its exact observation and prohibited overreach against pinned quote locations, and require the absent-note base fixture to exit nonzero. Resolve every input, including the pinned form, beneath the supplied `--root`. Until these predicates are exercised and pass, report the relevant claim unproven; do not infer whole-builder safety or current external truth.
