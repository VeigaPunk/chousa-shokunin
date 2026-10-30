# Probe02 — round-65 wave-1 scoped findings (trailer)

Lane: chousa round65. Seat Probe02 (leaf, labrat-only). Scope: isolated fixture
on the single frozen `nonzero-valid` surface of the C1 receipt-pin interface.
Oracle: `corpus/evidence/round65/controls/ref-receipt-pin.py`; target
`tools/receipt-pin.py` absent (pre-acquisition). Freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd.

**Result: assigned surface confirmed.** Independent derivation from the frozen
format (claims.md C1 only) agrees with the oracle:

- Receipt with `EXIT=1`, revision `d6ed8155e9b4735639a2cf0a3e479c62f2056195`,
  digest `4355e16a…08ce1a` binding blob `d6ed8155…:SKILL.md` (derived via two
  agreeing channels, sha256sum + hashlib) → **exit 0, `RECEIPT_PIN=PASS`**.
- Boundary `EXIT=255` likewise PASS; no leak of the reported exit into the
  validator's own exit code.
- Under nonzero exit, tampered digest → `FAIL blob/digest` (rc 1) and wrong
  revision → `FAIL header/body` (rc 1): the binding is exit-agnostic.
- Observed strictness beyond the frozen 20: `EXIT=01` rejected (canonical
  decimal required) — unscored, noted for interface fidelity.

Full seat report: `.ufo/waves/round-65/w1/Probe02/report.md`;
run log: `.ufo/waves/round-65/w1/Probe02/nonzero-valid-receipts.log`.
No production writes; no installs; scratch deleted; no blockers.
