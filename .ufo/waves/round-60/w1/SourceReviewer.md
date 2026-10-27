# SourceReviewer — Round 60 source review

Scope: frozen claims, prior committed evidence, and current round-60 counter/source only. No external fetches, code changes, installs, or repository mutations. LSP status/device was unavailable in this seat; conclusions below are direct source/evidence reads, not semantic-search results.

## Findings

### High — supplied immutable-claim digest does not match the file

Assignment supplied SHA-256 `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; the current frozen claims file hashes to `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` (`sha256sum corpus/evidence/round60-claims.md`). Its header names base `b379919a873e7080a31ef92c7002f55f5374e2c6`, but that revision does not contain this path (`git show <base>:corpus/evidence/round60-claims.md` reported absent). Thus the claimed identity/freeze provenance is not corroborated by either the supplied digest or the named base. Do not treat this file as verified immutable bytes without reconciling the authoritative dispatch freeze receipt. This review did not modify it.

### High — C1 injection test accepts an output-forging successful no-op as the safe candidate

Current source `corpus/evidence/round60/c1-count.py:37-44,58-70`: `run()` calls a supplied builder, then classifies any `returncode == 0` with unchanged sentinel bytes as `candidate_safe` (line 41). The generated `forged.py` (lines 60-62) only prints `=PASS` / `all seven hazards accepted` and exits 0; it leaves the seeded sentinel untouched. Therefore its `forge_state` becomes `candidate_safe`, not `forged_safe`; `forge_blocked = forge_state != "forged_safe"` nevertheless evaluates true (lines 62-63). The counter can consequently print `INJECTION_REJECTED=1/1` and accept this forged-output builder as the candidate if supplied with `--builder forged.py`. The code’s `forged_safe` state is unreachable in this path because it requires the sentinel to be deleted, exactly the same condition as `baseline_bad` (lines 42-44). The receipt `.ufo/waves/round-60/c1-before.txt:3-8` reports the injection attempt rejected but does not expose this classification defect. This leaves the frozen clause “the output-injection mutant prints `=PASS` but is scored as a failure” unproven: stdout is ignored, but the mutant is scored safe, not failed. A failing mutant must be constructed to fail a required leg (e.g. nonzero exit) while forging output, and the counter must distinguish that failure from the valid safe path.

### Medium — claimed safe-path observation is weaker than the criterion

`c1-count.py:38-44,68-70` regards a zero-exit builder that leaves only the foreign sentinel unchanged as candidate-safe. It does not check that the builder produced/updated expected output or reached the independently observed safe path; the fixture establishes only the sentinel invariant. Thus a successful no-op can meet `candidate_ok`, even though the claim’s safe-path clause requires the candidate to reach the safe path. The round-60 baseline receipt (`.ufo/waves/round-60/c1-before.txt:5-8`) only demonstrates candidate refusal due to deleting the sentinel; it does not demonstrate positive safe-path output.

## Prior evidence context

Committed `corpus/evidence/round59` seat evidence includes `R59Executor09.md:215-260`, which directly reproduces the old counter accepting all seven failing hazard legs as `C1=PASS` / exit 0 when the builder injects `=PASS` into captured stderr. This supports why the new counter must test a failing injection mutant, not merely show that captured text is excluded from its own boolean expression. The current counter does exclude output from the state calculation, but its successful-no-op injection probe does not test rejection of a failing leg.

## Verification gaps / residual risk

- No post-change round-60 receipt was reviewed; no claim verdict is inferred here.
- The given expected digest and the named claim-base revision cannot establish the frozen file’s identity. Authoritative dispatch-time freeze provenance remains unresolved.
- This is a bounded source review; no counter execution was performed. Current counter digest observed: `66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7`.
- No tools installed or updated.
