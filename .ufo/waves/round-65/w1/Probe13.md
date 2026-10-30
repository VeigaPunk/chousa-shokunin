# Probe13 — round65 short-digest probe (trailer)

Scoped surface: short SHA256 digest header in a receipt fixture, reference `corpus/evidence/round65/controls/ref-receipt-pin.py` (production tool absent). One isolated git fixture in scratch; frozen-format-derived expectation independently confirmed.

**Result: short digests (32- and 63-hex) → exit 1, `RECEIPT_PIN=FAIL digest header`; full 64-hex control → exit 0, `RECEIPT_PIN=PASS`.** Matches frozen-format derivation ("SHA256 full lowercase 64 hex"; "1 invalid" class). No leniency at the 63-hex boundary. No production writes, no network, no battery run. Token-portability note for L1: exact failure reason strings are implementation wording, not format-pinned — exact-token C1 scoring is sensitive to rewording in any production reimplementation.

Full finding + evidence: `.ufo/waves/round-65/w1/Probe13/report.md` (receipts, `.out` transcripts, `facts.env`, driver script).
