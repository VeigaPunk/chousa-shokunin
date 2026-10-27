# PlanningConnector — bounded cross-proposal analysis (round 60)

## Scope and axes

This connector considers only the frozen round-60 claims, the current C1 counter/source, and prior committed evidence cited below. The relevant declared axis is **operability**: the C1 claim explicitly targets measurement integrity, not builder security. C2 is an independent **depth** claim. The narrow synthesis below is a testable way to keep those scopes distinct while joining verification surfaces; it does not assert either claim has passed.

## Evidence and cross-effects

- Frozen claims fix C1's target: structured per-leg states based on observed child status/filesystem state, not captured output; an unsafe pinned r55 control; safe candidate behavior; and rejection of an exact-token forge (claims `round60-claims.md:7-11`). They explicitly disclaim that this establishes all builder hazards. C2 is a separately gated source-grounded note and must not be admitted without its quote/capture and QUALITY checks (`round60-claims.md:13-16`).
- Prior committed evidence establishes why the narrow boundary matters: R59Executor09 reports that round-58's prose-substring verdict credited a builder that injected `=PASS` while failing all seven refusal legs, and that the symlink escape could still be labeled as passing (`.ufo/waves/round-59/w1/R59Executor09.md:215-260`). That record also identifies a leg overwrite that discards a failed refusal result (`:262-290`). This is a counter-verdict defect, not proof of current builder security.
- The current C1 counter's `run()` returns only three classifications (`candidate_safe`, `baseline_bad`, `forged_safe`) based on return code and foreign-file bytes (`corpus/evidence/round60/c1-count.py:22-44`). Its top-level probe scores `forge_blocked`, `baseline_discriminates`, and `candidate_ok` separately (`:57-75`). This severs stdout/stderr from the boolean verdict, addressing the known echo channel, but the probe exercises only the foreign-file case; it is not a substitute for round-58's seven hazard legs.
- The recorded before receipt says the baseline counter run rejected the injection and discriminated the pinned control, while candidate refusal failed because both candidate and r55 deleted the foreign file (`.ufo/waves/round-60/c1-before.txt:1-8`). Thus a passing injection/control pair alone is insufficient: the safe candidate result is an independent required conjunct, exactly as the frozen predicate states.
- The counter derives `R55` from the round-58 evidence directory and invokes that pinned builder, whereas candidate resolution is supplied by the caller (`c1-count.py:17-20,66-69`). The control is therefore part of the test's reproducibility substrate; it demonstrates that this particular fixture can distinguish a destructive implementation, not broad correctness or provenance independently of the pinned bytes.

## One bounded move: shared evidence ledger, disjoint claim predicates

If synthesizing the executor and source-gate proposals, use one **read-only round evidence index** (a small report table, not a new runtime abstraction) that maps each claim to its own predicate, input pins, observed result, and evidence path. Keep C1's counter result strictly the three typed legs above and C2's admission strictly the source quote/capture + metadata + QUALITY gate. Do not let a shared receipt, aggregate `PASS`, source-grounding status, or C1's success promote the other claim. In particular:

1. C1 row records the frozen claim SHA and counter/builder/control identities, then the three independent outcomes and exit status; captured diagnostics remain explicitly non-authoritative.
2. C2 row records the offline S101 capture digest, exact located quote and Gate metadata, entry/citation checks, and QUALITY disposition. If any component is unavailable, record unprovable rather than using C1 evidence as support.
3. Report the claims separately, including an explicit limitation that the C1 counter covers only its designated foreign-file fixture and does not attest the builder's full hazard matrix.

This is a procedural synthesis only; no counter/source/test/report files besides this connector report were changed. It improves **operability** by making claim-specific evidence independently auditable, without changing the frozen predicates or merging distinct claims. It does not establish a measured axis delta.

## Risks and contradictions

- A compact shared ledger can obscure rather than clarify if it collapses typed leg results into one green status. Preserve per-claim and per-leg fields; never treat overall round success as evidence that each claim passed.
- The frozen C1 contract's phrase “safe path” concerns the foreign-file fixture in the current counter, while prior R59 evidence concerns seven separate refusal hazards. These scopes differ; the current counter must not be described as repairing the builder's seven-hazard behavior.
- C1's claimed injection mutant is the exact target-token behavior; rejecting it is evidence against that attack class only, not against every possible candidate-controlled influence on measurement. Any broader claim would require separate tests and is outside this bounded proposal.
- C2's “source-grounded” status and C1's runtime-measurement integrity are causally independent. A citation cannot validate runtime behavior; a passing runtime probe cannot validate bibliographic or current-validity claims.

## Verification suggestion

For C1, independently confirm the frozen input digest, rerun the exact frozen command using a fresh absolute work directory, and check that stdout contains the three leg states plus `C1=PASS` iff all required states hold and process exit is zero. Retain separate evidence for the safe candidate, destructive pinned baseline, and exact-token forge. For C2, independently open only the committed offline S101 capture, verify digest and quote location against the new entry and its Gate, then check the declared QUALITY disposition. Confirm neither claim's status is inferred from the other's evidence. No tests were run by this seat.
