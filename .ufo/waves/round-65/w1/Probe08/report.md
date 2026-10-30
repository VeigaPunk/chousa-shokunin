# Probe08 — isolated negative-exit receipt fixture (round65, freeze f99de3b)

## Seat scope
Single surface: the reference validator's handling of a negative `EXIT` header
field. No battery run; no production writes; production target
`tools/receipt-pin.py` untouched (may not exist yet — not checked, out of scope).

## Independent expectation (derived from frozen claims.md only)
Round65 claims freeze the receipt format as:
`REVISION=<40 lowercase hex>; EXIT=<decimal 0..255>; SHA256=<64 lowercase hex> <repo-relative path>;`
blank separator, nonempty output. Exit semantics: `0 consistent, 1 invalid,
2 usage/environment`. Therefore `EXIT=-1` is outside the declared grammar
(unsigned decimal 0..255), the receipt is malformed/invalid, and the required
result is **exit code 1** with a `RECEIPT_PIN=FAIL` token on stdout — not exit 2
(reserved for usage/environment) and not exit 0.

## Fixture
- Driver: `probe08-negative-exit.py` (this folder; copy of scratch original).
- Receipts built against the frozen lane base `d6ed8155e9b4735639a2cf0a3e479c62f2056195`,
  digest binding the real blob `git -C <lane> cat-file blob d6ed8155…:SKILL.md`
  (read-only git). Invocation preserves the counter's argv:
  `python3 -B <ref> --receipt <file> --root <lane> --revision d6ed8155…`.
- Reference under test: `corpus/evidence/round65/controls/ref-receipt-pin.py`.
- Fixture-integrity controls interleaved: `EXIT=0` → PASS, `EXIT=255` → PASS
  (proves the rejections below are caused by the minus sign, not magnitude).

## Results (probe08-run.log, verbatim)
```
CASE positive-exit0         EXIT=0     want_rc=0 got_rc=0 stdout='RECEIPT_PIN=PASS' OK
CASE boundary-exit255       EXIT=255   want_rc=0 got_rc=0 stdout='RECEIPT_PIN=PASS' OK
CASE negative-exit-frozen   EXIT=-1    want_rc=1 got_rc=1 stdout='RECEIPT_PIN=FAIL header/body' OK
CASE negative-zero          EXIT=-0    want_rc=1 got_rc=1 stdout='RECEIPT_PIN=FAIL header/body' OK
CASE negative-255           EXIT=-255  want_rc=1 got_rc=1 stdout='RECEIPT_PIN=FAIL header/body' OK
CASE negative-256           EXIT=-256  want_rc=1 got_rc=1 stdout='RECEIPT_PIN=FAIL header/body' OK
CASE sign-space             EXIT=- 1   want_rc=1 got_rc=1 stdout='RECEIPT_PIN=FAIL header/body' OK
CASE minus-minus            EXIT=--1   want_rc=1 got_rc=1 stdout='RECEIPT_PIN=FAIL header/body' OK
NEGATIVE-EXIT-SURFACE 8/8 CONSISTENT
```

## Findings
1. The frozen battery case `negative-exit` (`EXIT=-1`) behaves exactly as the
   frozen format dictates: exit 1, `RECEIPT_PIN=FAIL header/body`.
2. The whole minus-sign family (-1, -0, -255, -256, `- 1`, `--1`) is rejected
   identically at rc=1 — consistent with the claims grammar `EXIT decimal 0..255`.
3. Boundary `EXIT=255` passes, confirming 255 is in-grammar and the negative-exit
   rejections are sign-driven, not magnitude-driven.
4. Token/exit discipline observed: invalid receipts return exactly 1 with a
   `RECEIPT_PIN=FAIL ` prefix; no case leaked exit 2 or a PASS token.

## Evidence retained in this folder
- `probe08-run.log` — verbatim driver output.
- `negative-exit-frozen.receipt.txt` — exact frozen-case receipt (EXIT=-1).
- `probe08-negative-exit.py` — fixture driver (reproducible; scratch deleted).

## Risks / notes for L1
- Single-seat, single-surface probe; 8 receipt variants, one read-only git surface.
- No tools installed; python3 stdlib + system git only.
- Production `tools/receipt-pin.py` behavior is not established by this seat;
  this validates only the reference control's negative-exit semantics.
