# C1ReviewB — round 60 frozen-claim review

## Findings

### High — C1 injection control is accepted as a safe candidate

`corpus/evidence/round60/c1-count.py:41-44,58-64` classifies the generated forge (prints `=PASS`, exits 0, leaves the seeded foreign file intact) as `candidate_safe`: `candidate_safe` is tested before the complementary `forged_safe`. Therefore `forge_blocked = forge_state != "forged_safe"` returns true for the forge. The reported `INJECTION_REJECTED=1/1` is not evidence that the output-injection mutant was rejected; it is a false positive against the frozen C1 predicate (`corpus/evidence/round60-claims.md`, C1 frozen predicate and after-target). This is independently identified in `.ufo/waves/round-60/w1/C1LogicCritic.md:3-14` and aligns with the prior committed round-59 observation that output echoing could satisfy the round-58 aggregate verdict (`.ufo/waves/round-59/w1/R59Executor09.md:215-260`).

**Observed counter run:** `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round60/c1-count.py --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --work /fast/scratch/hyaku-r60/C1ReviewB/probe --seed 6001` printed `INJECTION_REJECTED=1/1`, `BASELINE_DISCRIMINATES=1/1`, `CANDIDATE_REFUSAL=0/1`, `C1=FAIL`; exit 1. Thus overall target does not pass, and the injection submetric itself is misleading.

### High — supplied immutable claim SHA does not match bytes

The assignment pins SHA-256 `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`, but `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round60-claims.md` observed `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. The local file therefore does not verify against the prescribed frozen claim identity. I did not modify it. Treat any assertion that this on-disk claim file has the pinned immutable identity as unverified until the discrepancy is resolved; no claim text is inferred from the expected digest.

## Verdict

C1 claim is **not established**: the exact counter run exits 1, and its injection metric passes the tested forge due to a classification defect. No conclusion that the builder itself is secure is made. Review was bounded to frozen claim bytes, the current counter/source, and prior committed C1 evidence; no external fetch or repository mutation was performed.