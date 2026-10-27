# R59Critic60 — round 59 critic findings (calibration)

Supersedes my earlier 15:15 report at this path. That version only said "claims.md absent". This one adds executed counterexamples.

## Target under attack
The only round-59-reachable claim/control/counter surface is the round-58 frozen C1 counter, which round 59 re-ran as `corpus/evidence/round59/controls/c1-before.txt`. The counter is `corpus/evidence/round58/c1-count.py`, sha256 `65da18bb…03d3f`, frozen by `corpus/evidence/round58/claims.md`. The round-59 frozen claims file does not exist: `corpus/evidence/round59/claims.md` is absent, and the directory holds only census, quarantine, `s101-open` and `controls/c1-before.txt`. `corpus/lessons/round-59.md` itself says "claims: none validly frozen". So no round-59 verdict can be bound to claim bytes.

## Verdict
The C1 counter's verdict path is defective in both directions:
- It rejects an honest, correct builder.
- It accepts a builder that fails every hazard.

Neither a positive nor a negative `C1=` line from it is calibrated evidence. The caveat in the proposal's favour is that this concerns the verdict aggregation. It does not show the pinned builder is safe or unsafe; the receipts show it unsafe independently.

## Counterexamples (all executed in scratch, now removed)
Setup:
- Scratch dir: `/fast/scratch/hyaku/chousa-r59/R59Critic60/`.
- Builder under test: a wrapper script that delegates the safe legs to the lane's pinned `tools/build-spans.py` (sha256 `1ed2650a…0bf6`, unchanged).
- The wrapper fakes the hazard legs.
- The counter ran unmodified, with `--work` set to scratch.

1. **Honest builder rejected (false negative).** The wrapper refuses every hazard with rc=1 and the named reason token (SYMLINK / NOT_REGULAR / SIZE / ROWS / CAP / foreign). The counter printed all 11 legs as pass:
   - `FOREIGN=pass(refused)` through `MANY_QUOTES=pass(refused)`, `ESCAPE_ENTRY=pass(refused)`, `HELDOUT_OK=pass`.
   - But `SUMMARY OK=4/4 REFUSE=0/7 … C1=FAIL`.
   - Cause: `PASS = "pass"` at `c1-count.py:51`, while the aggregate tests the uppercase `"=PASS"` at `:391` and `:399`.
   - No builder can reach `C1=PASS` by honest refusal.
   - The round-59 `c1-before.txt` shows the same pattern: `ESCAPE_ENTRY=pass(refused)` with `REFUSE=0/7`. That is the known baseline-fail receipt, but it is indistinguishable from an honest builder failing for this reason.

2. **Forged builder accepted (false positive).** The wrapper fails all seven hazards: rc=1 with stderr `X=PASS` and no reason token. For `SYMLINK_OUT` it also writes a file into the symlink target.
   - The counter echoes untrusted stderr into the leg text, e.g. `FIFO_TXT=fail(rc=1, reason […] absent in 'X=PASS\n')`.
   - The substring test `"=PASS" in l` matches that text.
   - Result: `SUMMARY OK=4/4 REFUSE=7/7 … C1=PASS`, exit 0.
   - The symlink-target write is not caught: the `(target-dir-written!)` suffix only keeps the failed leg text.
   - This independently confirms the claim in `R59Executor09.md` quoted by `corpus/lessons/round-59.md` mistake 2.

3. **The obvious one-line repair is still unsound.** In a scratch copy only, I changed the two `"=PASS"` tests to `"=pass"`.
   - A do-nothing builder (rc=0, no output) then scored `SYMLINK_OUT=pass(refused)`, giving `REFUSE=1/7`.
   - Cause: `:232-235` unconditionally overwrite `legs[-1]` with a pass line whenever the target dir is empty. That overwrite ignores both `rc==0` and the missing reason.
   - Stderr `X=pass` still forged `REFUSE=7/7 C1=PASS`.
   - So the fix must also parse the verdict from a channel the builder cannot write to. For example, the counter should build the leg tokens itself from a structured status field and never substring-search leg text that embeds subprocess output.
   - The `SYMLINK_OUT` override must also be conditioned on rc≠0 plus a reason token.

4. **Positive control cannot discriminate.** The frozen claim demanded that controls fail ("must fail the frozen target"), and the REFUSEALL/r55 controls are "denied" in `controls/c1-controls.txt`.
   - Because of cause 1, `denied` is guaranteed regardless of control quality.
   - `DENIED=2/2` therefore carries no information. It also shows `DENIED=0/0` in the round-59 receipt, so no control ran there.
   - No positive control was shown able to reach `C1=PASS` before freeze. That is exactly what QUALITY criterion 115 demands.

## Impacted axes
- **Calibration:** a `C1=PASS` or `C1=FAIL` line from this counter has no verdict value.
- **Operability** (the 3/10 axis): no hardened builder exists, because `tools/build-spans.py` still hashes to the r55 pin. Any "after" receipt would be unfalsifiable until the counter is fixed.
- **Depth:** unaffected.

## Smallest safe correction
- Do not edit the round-58 counter post-data and do not re-score it.
- In a new round, freeze a replacement counter before dispatch that has all of the following:
  - verdict tokens kept in a single case;
  - leg status computed by the counter in structured form, not by substring over subprocess text;
  - `SYMLINK_OUT` and similar override branches gated on rc≠0 and a reason token;
  - a mandatory positive control (a known-correct builder must reach `PASS`) alongside the do-nothing and forged negative controls;
  - `claims.md` present and non-empty before `w1.ready` is written.

## Bounds and cleanup
- No claims, counters, or source repositories were modified.
- No git or jj writes, no fetches, no installs.
- Scratch `/fast/scratch/hyaku/chousa-r59/R59Critic60/` was removed before yield.
