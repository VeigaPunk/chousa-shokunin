# S101LineReview — round 60

## Findings by severity

### High — C1 injection check treats an injected `=PASS` builder as a successful safe candidate

The frozen claim requires the exact-token output-injection mutant to print `=PASS` but be scored as a failure, and its kill rule says any child-output injection passing target is a failure (`corpus/evidence/round60-claims.md:9-11`). In `corpus/evidence/round60/c1-count.py:37-44`, `run()` discards the child output when deriving states: it scores any return-code-0 builder that leaves the planted foreign file intact as `candidate_safe`. The injected fixture at lines 58-63 prints `=PASS`, emits `all seven hazards accepted`, returns 0, and leaves the foreign file intact, so it gets `candidate_safe`; nevertheless `forge_blocked = forge_state != "forged_safe"` becomes true. Thus the counter calls this exact injected builder "blocked" and allows it to contribute to PASS rather than counting it as a failed leg. Also, `baseline_bad` and `forged_safe` have identical predicates (`returncode == 0 and not intact`, lines 42-43), so the labels do not distinguish the baseline-control case from the forged case. This violates the frozen predicate independently of whether the real candidate passes.

Prior evidence: `corpus/evidence/round59/controls/c1-before.txt:3-5,13-16` records the foreign-file destructive behavior and prior counter failure; frozen r58 claim text is at `corpus/evidence/round58/claims.md` (not rerun here). This is a counter logic defect, not evidence that the builder itself is secure.

### High — C2 quote sentinel disagrees with its pinned offline source text

The frozen C2 predicate requires the counter to establish the exact observation against the committed S101 raw capture and its pinned capture-text form (`corpus/evidence/round60-claims.md:13-17`). The counter hard-codes `EXPECTED='c. 文献类型及载体类型标志；'` (`corpus/evidence/round60/c2-count.py:9`) and requires exactly one occurrence in the form (`:15-21`). But the round-60 offline reopening at `.ufo/waves/round-60/s101-open.txt:5-8` records the relevant source as `c. 文献类型及载体类型标识；` at line 7: the capture says **标识**, not the counter's **标志**. Therefore the required expected string is absent from the supplied text form and the quote-location leg cannot pass. The raw capture wording is also reflected in the existing entry's S101 discussion at `corpus/knowledge/citation-count-semantics-r37.md:23-27` (which quotes “文献类型及载体类型标志” in a different source passage), making precise locator selection important: the cited line 7 in the reopening is “标识”, whereas the existing entry's quotation concerns a phrase elsewhere in the document.

## Freeze / review boundaries

The requested immutable claim SHA is `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`, but the observed SHA-256 of `corpus/evidence/round60-claims.md` is `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` (`sha256sum`); they do not match. I did not modify the claim file. Review used the present claim bytes, current round-60 counters and offline S101 text form, plus committed round-58/59 evidence. No external fetch or code execution of the counters was performed.

## Residual risk / verification gaps

- I did not run the counters or independently verify their output/exit codes; the findings above follow the inspected code paths and captured source text.
- This is a bounded line review, not a full audit of the span builder, all C1 hazards, or present-day CNKI behavior.
