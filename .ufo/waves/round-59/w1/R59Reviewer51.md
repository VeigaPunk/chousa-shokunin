# R59Reviewer51 — adversarial calibration review

## Findings (severity order)

### Blocker — no pre-data claim artifact to calibrate against

The required frozen input `corpus/evidence/round59/claims.md` is absent: the direct read returned “not found,” `corpus/evidence/round59/` has no such file, and `git ls-files corpus/evidence/round59/` lists 12 evidence files but no claims file. The sole commit touching that evidence directory is `026174e` (“round-59: preserve partial unadjudicated evidence”). The persisted wave contract still names the missing file in `.ufo/waves/round-59/w1-spec.json:10` and in this seat’s item at `:413-418`; lane `LOG.md:1919-1921` independently records that it was absent at `w1.ready` and no axis claim was validly frozen or scored.

**Impact.** There is no frozen round-59 proposition, threshold, or kill rule against which this seat can judge calibration. The later quarantine receipts and control results cannot retroactively supply a pre-data claim. This is a freeze/contract failure, not evidence that a particular verdict is false.

**Smallest falsifier:** a pre-data claims artifact with verifiable freeze identity and timestamp before the data/seat scoring. The current record instead requires a new properly frozen round; reconstructing claims now would not falsify the finding.

### High — the inherited C1 verdict path is not a valid positive calibration control

`corpus/evidence/round59/controls/c1-before.txt:1-16` records `SUMMARY OK=4/4 REFUSE=0/7 … C1=FAIL` and `EXIT=1`; its refusal legs include genuine non-refusals (`FOREIGN` deletes the foreign file, `SYMLINK_OUT` writes through the symlink, `MANY_QUOTES` accepts the excess rows) alongside refusals rejected for missing reason tokens (`FIFO_TXT`, `DEVZERO_TXT`, `FAT_RAW`). This is a before-state failure receipt, not evidence of a positive verdict path.

More fundamentally, the inherited `corpus/evidence/round58/c1-count.py:51,391,399` emits refusal-leg tokens with lowercase `PASS = "pass"` but aggregates only uppercase `"=PASS"`; honest passing refusal legs therefore cannot make the frozen counter pass. Round-59 `LOG.md:1926` additionally records the stronger post-dispatch finding: a forged builder can put `=PASS` in stderr and make the original counter emit `C1=PASS` while all seven refusal legs fail. Thus the result is unsound in both directions: unreachable for honest builders and forgeable for a failing builder. A receipt with a `C1=PASS` line from these frozen bytes is not a calibrated positive verdict.

**Smallest falsifier:** a re-frozen counter whose verdict aggregates structured per-leg outcomes (not substring matches over shared stdout/stderr), plus a positive builder and adversarial stderr-forgery control both scored against that exact counter hash. No such round-59 after-receipt appears in `controls/` (only `c1-before.txt`).

### High — persisted wave spec is not the dispatched task record

The persisted `.ufo/waves/round-59/w1-spec.json` contains 66 generic “review ready handoff requirements” item bodies; `.ufo/waves/round-59/w1-dispatch.json` contains 66 actual task bodies under `taskCall.tasks`. Comparing by seat name yields **0/66 body matches** (including this seat). `LOG.md:1930-1932` attributes this to a post-dispatch overwrite of the spec and records that its original bytes were not reconstructed. The current spec therefore cannot establish which claim wording or task instructions seats actually received; the assignment context still refers to the absent claims file.

**Smallest falsifier:** recover an authenticated pre-overwrite spec snapshot matching the dispatched task payloads. The current persisted spec and dispatch demonstrably do not match.

## Residual risk and verification gaps

- Source-scope boundary was respected: no external fetch was made; L0 `8d77e6c1` remains open (`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:136,140`). `s101-open.txt` is byte-identical to the already committed round-54 `S101-text-form.txt`; this is offline reopening, not evidence of a live fetch.
- The r59 quarantine receipt labels S080 `absent` against capture key `adf6ba934e813b2c326fa150`; its current bytes hash to `ed4dde2e…`, while round-42 `receipts/digests.txt:18` pins `4e46154f…`. The change is accounted for by round-57’s disclosed refetch/drift record (`round57/refetch.tsv:39,89`, S121, same URL/key; txt hash `ed4dde2e…`), and round-57 C2 records S121 among five DRIFTED captures with `absent=0`. I independently checked the register’s S080 quote against current bytes under NFKC plus whitespace-collapse; it remains absent. I therefore do **not** claim the S080 verdict is false. Round-59 itself does not include a full capture-digest receipt, so reproducing all 24 classifications still depends on the cross-round r57 refetch ledger and the capture store.
- S077 and S086’s old cache keys are missing from the current store; r59 correctly marks them `unverifiable` rather than `absent`. I did not reconstruct deleted cache bytes or independently run the full eleven-fold classifier.
- Census start and end are byte-identical. This only supports unchanged census output; it does not test the claims freeze or C1 verdict path.
- No counter, test suite, or runtime was run. No source, claims, or counter was modified; no scratch was created. This review is limited by the missing frozen claims artifact and the broken persisted spec record.

Report: `.ufo/waves/round-59/w1/R59Reviewer51.md`
