# PinFormat — round65 w1 scoped findings

Full report: `.ufo/waves/round-65/w1/PinFormat/report.md`. Freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd. Draft only; L1 owns integration and any commit.

Findings:
1. Specimen receipt drafted in the exact frozen header format (`PinFormat/pinformat-positive.receipt`). Reference validator returns `RECEIPT_PIN=PASS` on it (rc 0).
2. Reported `EXIT` is the measured child's exit, separate from tool invocation exit. A failing-child specimen (`EXIT=7`) validates with driver invocation rc 0 and validator rc 0; the validator's exit is consistency only.
3. Reference rejects tampered digest, wrong caller revision, uppercase revision (usage rc 2), absent receipt. As expected.
4. Limits: forged body under valid header passes; working-tree tamper with committed-blob receipt passes; CRLF headers pass (`splitlines` leniency, not covered by frozen cases).
5. No tools installed or updated. Scratch deleted after copying receipts and transcripts to `PinFormat/`.
