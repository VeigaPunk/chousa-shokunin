# Probe19 — round65 no-body receipt fixture

Scoped finding: the frozen reference control treats a **body-less receipt as invalid**.

- Method: isolated fixture in scratch clone at freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`,
  digest bound to `SKILL.md` blob at that revision; reference `controls/ref-receipt-pin.py`
  run unmodified (`--receipt/--root/--revision`). One surface only; no battery run.
- Independent expectation from frozen format ("empty separator, **nonempty output**";
  "0 consistent, 1 invalid"): no body ⇒ exit 1 with `RECEIPT_PIN=FAIL`.
- Observed: no-body receipt → rc=1 `RECEIPT_PIN=FAIL header/body` (MATCH); whitespace-only
  body → rc=1 same (MATCH); positive control with body → rc=0 `RECEIPT_PIN=PASS` (MATCH,
  harness sound).
- Cross-check: byte-identical to frozen counter case `('no-body', …, 1)`; counter not executed.
- Evidence: `.ufo/waves/round-65/w1/Probe19/` (driver, results transcript, exact receipts).
- No installs (python3 3.14.8, git 2.56.0 already present). Scratch deleted; lane untouched.
