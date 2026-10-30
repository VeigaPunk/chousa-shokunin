# Probe11 — round65 receipt-pin no-digest probe

- Scope: one surface (`no-digest`) against reference `controls/ref-receipt-pin.py`; production `tools/receipt-pin.py` confirmed absent (prefreeze). No production writes.
- Independent expectation from frozen claims.md format: with the `SHA256=` line removed the receipt is malformed (4 lines < required header+separator+body shape) → validator exit `1` with `RECEIPT_PIN=FAIL ` prefix (negative-case contract in `c1-count.py`).
- Observed: `rc=1`, stdout `RECEIPT_PIN=FAIL header/body` on both (a) an isolated scratch fixture repo (commit `20970fae61c6...`, path `artifact-r65.txt`) and (b) the same no-digest receipt shape bound read-only to frozen `BASE=d6ed8155...:SKILL.md`. Valid control receipt → `RECEIPT_PIN=PASS` rc 0.
- Note: failure token is `header/body` (line-count gate fires before the SHA256 regex); the frozen counter freezes only exit code + FAIL prefix for negative cases, so this matches.
- Verdict: PASS on the single assigned surface.
- Evidence: `.ufo/waves/round-65/w1/Probe11/` (`report.md`, `probe11-transcript.txt`, receipts, driver).
- Env: git 2.56.0, Python 3.14.8; no installs. Scratch `/fast/scratch/hyaku/chousa-r65/Probe11/` deleted after copying receipts.
