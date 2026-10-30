# Probe20 — round65 scoped findings (upper-digest probe)

Freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`. Isolated single-surface probe
of the receipt `SHA256=<hex> <path>` header + blob binding against reference
`corpus/evidence/round65/controls/ref-receipt-pin.py`, with expectations
derived independently from the frozen claims text. argv preserved
(`--receipt/--root/--revision`); scratch repo built under
`/fast/scratch/hyaku/chousa-r65/Probe20/` with toplevel assertions before every
git mutation; scratch deleted after evidence copy.

7/7 cases match:

- control-valid → exit 0 `RECEIPT_PIN=PASS`
- upper-digest-hex → exit 1 `RECEIPT_PIN=FAIL digest header`
- mixed-digest-hex → exit 1 `RECEIPT_PIN=FAIL digest header`
- digest-63-hex → exit 1 `RECEIPT_PIN=FAIL digest header`
- digest-65-hex → exit 1 `RECEIPT_PIN=FAIL digest header`
- digest-nonhex → exit 1 `RECEIPT_PIN=FAIL digest header`
- digest-wrong-value (valid hex, wrong) → exit 1 `RECEIPT_PIN=FAIL blob/digest`

Upper-digest edges are unambiguous: lowercase-64-hex format violations and
blob-binding violations are distinguished by exit-1 token. No production
writes; full detail and evidence in `.ufo/waves/round-65/w1/Probe20/report.md`
(+ `probe20-upper-digest-results.json`, `probe20-*.receipt`,
`probe20-upper-digest-fixture.py`). No tool installs needed.
