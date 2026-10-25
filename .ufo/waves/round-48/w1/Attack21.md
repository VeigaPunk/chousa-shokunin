# Attack21 — R39/R40 active-receipt drift (#4)

## Verdict

**Expected revision drift, not evidence corruption.** The gate hash captured in the active receipts is internally consistent with the gate committed at R39/R40 closure. The tip mismatch is caused by the subsequent R41 gate edit. The receipts remain byte-preserved evidence of runs against the earlier gate; they are not evidence that the current tip gate was run. A safe byte-preserving verification is possible by supplying the historical gate bytes to the existing verifier, without modifying receipts. Do not “repair” receipt hashes or treat the old receipts as current-tip measurements.

## Evidence and reproductions

Commands run from `/home/vgpnk/Projects/shokunin/chousa-shokunin`; no fetch/network used.

- Read `corpus/evidence/round40/active-r39-receipts.tsv`, `corpus/knowledge/receipt-binding-r38.md`, `corpus/knowledge/receipt-verifier-subject-r39.md`, `corpus/knowledge/receipt-expectation-digests-r40.md`, and `corpus/evidence/round39/verify-receipts.py` (especially lines 208–216). The committed R40 manifest has six active receipt rows; it explicitly says three R40 reruns replace the R39 originals while originals remain preserved.
- `git log --oneline -- corpus/evidence/round39 corpus/evidence/round40` shows R40 repair `d164f88`, freeze `6c01a41`, and measurement/lesson `282dc76`. `git log --oneline --follow -- tools/research-gate.sh` shows the next gate-changing commit is `1bd9001` (R41).
- Gate bytes: `sha256sum` of `git show 6d914e9:tools/research-gate.sh` and `git show 282dc76:tools/research-gate.sh` both gives `4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3`, matching the R39/R40 receipts. `git show 1bd9001:tools/research-gate.sh` hashes to `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34`; current tip/worktree gate has the same digest. Thus the recorded digest changes exactly at R41, not within the receipt's run interval.
- `git diff 6d914e9 1bd9001 -- tools/research-gate.sh` shows the R41 change adds capture-tool pins (round-41 C1), wrappers and pinned child invocation handling, and updates a stat selftest path. R41 `corpus/evidence/round41/measure-after-c1.txt` reports `CAPTURE_PIN_MATCH=12/12`, consistent with an intentional measured gate revision.
- Reproduced the committed R40 counter against tip: `python3 corpus/evidence/round40/c1-count.py` prints `R39_ACTIVE_RECEIPTS=2/6`, exit 1. Four gate-path rows fail `VERIFY-FAIL: gate-sha256-mismatch`; two control-gate receipts verify. This is the verifier's explicit exact-file hash check (`verify-receipts.py:208–216`), not a self-digest or parse failure.
- For a byte-preserving historical check, extracted only the three gate blobs from commit `282dc76` to `/tmp/chousa-r48-attack21/` (no tracked files changed), then invoked the committed round-39 verifier for each manifest row with that snapshot gate. Result: all six `VERIFY: ok`, `R39_ACTIVE_RECEIPTS_AT_R40_GATES=6/6`. The r40 regenerated receipts' own `receipt_sha256` values also independently recompute as `SELF-OK`.
- R40 regenerated receipts differ from their R39 originals only in `expect_sha256` and the derived `receipt_sha256` (verified for each of the three pairs). This is the documented R40 expectation-table reissue, not gate evidence tampering. The current expectations hash is `01cbdc3a…`; R39 originals for these three had stale `3abd2dcb…`, as described in `receipt-expectation-digests-r40.md`.

## Safe handling / residual risk

The safe recovery is historical verification against the exact committed gate blob from the receipt's revision (here R40 commit `282dc76`, whose gate SHA matches the receipt), while preserving the receipt bytes. A temporary extracted file or a read-only `git show` stream suffices; keep the original `--gate` path/hash semantics and label the result historical. Do not overwrite the R39/R40 receipts, substitute the R41 gate while claiming their old run measured it, or use the R40 active counter's tip failure as proof of corruption. For current-tip evidence, a new run/receipt would be needed; that would be new evidence, not a repair.

No receipt or production file was edited. The worktree already contained unrelated changes; only `Attack21.md` was written by this task. Verification was performed with the commands and outputs reported above; no tests/builds were run.