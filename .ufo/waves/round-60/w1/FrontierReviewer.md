# FrontierReviewer — round 60 bounded review

## Findings by severity

### High — the C1 injection control is accepted rather than rejected (and the stated injection predicate is not measured)

`corpus/evidence/round60/c1-count.py:37-44,58-70` captures a child return code and checks whether the seeded foreign file stayed intact, but ignores captured stdout/stderr. The forged fixture at lines 60–63 prints `=PASS` and exits 0 without touching the foreign file. `run()` therefore labels it `candidate_safe` (line 41), not `forged_safe`; `forge_blocked = forge_state != "forged_safe"` then counts that as `INJECTION_REJECTED=1/1`. Thus the purported injection rejection is satisfied by the exact token-producing process, contrary to C1's falsifiable requirement that the output-injection mutant be scored as failure. The branches at lines 42 and 43 are identical predicates, and line 42 precedes line 43, making `forged_safe` unreachable; moreover no assertion tests the forged output token. This is an actionable defect in counter measurement integrity, independent of whether the production builder itself is safe.

Evidence: executed `python3 -B corpus/evidence/round60/c1-count.py --builder tools/build-spans.py --work /fast/scratch/hyaku/chousa-r60/FrontierReviewer/c1`; output was `INJECTION_REJECTED=1/1`, `BASELINE_DISCRIMINATES=1/1`, `CANDIDATE_REFUSAL=0/1`, `C1=FAIL` (exit 1). The PASS-looking injection receipt is vacuous even on this failing overall run. Prior committed R59Executor09 evidence independently establishes the actual threat model: `.ufo/waves/round-59/w1/R59Executor09.md:215-260` demonstrated output-token injection reaching `C1=PASS` / exit 0 in frozen round-58 bytes, and names typed per-leg state as necessary.

### High — the dispatched immutable-claim digest does not match the file reviewed

The assignment supplies immutable claim SHA-256 `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; observed `sha256sum corpus/evidence/round60-claims.md` is `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. The file is untracked at the inspected lane tip `b379919a873e7080a31ef92c7002f55f5374e2c6`. Therefore this review cannot attest that the on-disk claim bytes are the frozen, dispatched bytes. The report cites the actual observed digest, not the asserted immutable one; resolve identity against the retained dispatch/freeze receipt before treating any claim verdict as admitted.

## Residual risk

C1's `CANDIDATE_REFUSAL=0/1` means the current builder did not pass the narrow safe-path fixture in the exercised counter. This review did not infer that the entire C1 surface is secure or unsafe beyond that observation. The S101 offline capture at `.ufo/waves/round-60/s101-open.txt:5-13` grounds the specific bibliographic type/carrier text; the existing entry's limitations are recorded at `corpus/knowledge/citation-count-semantics-r37.md:74-86`. No claim is made here about current external validity or CNKI implementation.

## Verification gaps

No lsp device/server was available in the provided tool inventory, so no semantic references/definition/diagnostics queries were possible; findings are grounded in the cited source lines and the executed counter output. I did not run the C2 counter or inspect downstream integration verdicts. No source fetch, lane/fleet write beyond this report, or git/jj mutation was performed. Scratch used: `/fast/scratch/hyaku/chousa-r60/FrontierReviewer`; removed before completion.
