# S101RejectReview — round 60

Scope: frozen C1/C2 predicates, committed prior evidence, and current counters/source only. No external fetch or repository mutation.

## Findings

### High — C1 forged-output control does not exercise a failing leg

`corpus/evidence/round60/c1-count.py:36-45` creates the purported injection mutant as a program that only prints `=PASS` and `all seven hazards accepted`, then exits 0. `run()` seeds `foreign` and defines `candidate_safe` solely as return code 0 plus intact foreign file (`:21-25`). Therefore that forge returns state `candidate_safe`, not a failure; `forge_blocked = forge_state != "forged_safe"` becomes true (`:40-41`) and is counted as `INJECTION_REJECTED=1/1` (`:45-50`). The `forged_safe` state is unreachable: it is assigned on exactly the same `p.returncode == 0 and not intact` condition as `baseline_bad` (`:23-25`), and the preceding conditional captures that condition first. This means the counter's claimed injection rejection can pass without testing “a failing leg ... exact PASS predicate by output injection,” violating frozen C1 predicate/kill rule. The round-58 prior counter claim/evidence identifies the original target-token failure mode (`corpus/evidence/round58/claims.md`; see the round-60 frozen claim `corpus/evidence/round60-claims.md`, C1). Recommendation: reject C1 PASS/admission unless the injection mutant demonstrably fails the independently observed leg while emitting the exact forged token, and its resulting state is asserted as failure.

### Medium — C2 counter does not establish the frozen “new entry” condition

Frozen C2 requires a new entry and explicitly says base must fail because no round-60 entry exists (`corpus/evidence/round60-claims.md`, C2). Current `corpus/evidence/round60/c2-count.py:8,13,17-20` always reads the already-existing `corpus/knowledge/citation-count-semantics-r37.md`; its metadata/limit checks are generic substrings and do not require a round-60 entry or a newly added note. Thus the proposed target cannot be falsified by absence of a new entry using this counter; existing entry already contains S101 metadata and the “Unknown” version-limit language (`corpus/knowledge/citation-count-semantics-r37.md:5,74-80`). The existing note also contains older S101 material, while the round-60 opened text/receipt locates the distinct 14.2(c) quote (`.ufo/waves/round-60/s101-receipt.txt:4-6`). This is a counter/predicate mismatch; do not accept C2 from this counter absent evidence that a distinct new note satisfying the frozen observation and exact quote gate was committed.

## Source-boundary check

The offline capture supports only its own wording: the receipt records the reopened raw capture digest and located quote `c. 文献类型及载体类型标志；` at line 245 (`.ufo/waves/round-60/s101-receipt.txt:1-6`; `.ufo/waves/round-60/s101-open.txt:245`). The existing note appropriately labels current-version validity unknown (`corpus/knowledge/citation-count-semantics-r37.md:79-80`); neither this offline evidence nor the counter establishes present-day validity or CNKI implementation. This review made no live-fetch claim.

## Verification gaps

I did not run counters or modify fixtures. No LSP device is available in this session (`read xd://lsp` returned “No such tool”); findings cite directly read source lines, not semantic LSP proof. Claim SHA supplied by assignment: `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`.
