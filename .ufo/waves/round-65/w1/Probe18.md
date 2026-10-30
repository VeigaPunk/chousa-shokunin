# Probe18 — receipt-pin no-separator probe (round65 chousa)

Seat: Probe18 (leaf, single labrat). Freeze: f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd.
Date: 2026-10-30. Scoped findings: `.ufo/waves/round-65/w1/Probe18/report.md`.

## Result

The no-separator surface is **confirmed against the frozen format and reference**:

- Production `tools/receipt-pin.py` is absent at the freeze (as expected pre-implementation);
  probe ran the frozen reference `corpus/evidence/round65/controls/ref-receipt-pin.py`.
- Independent oracle derived from claims.md format text alone (no shared code):
  a receipt with header lines 1–3 valid but **line 4 not empty** is malformed →
  expected exit **1**, stdout prefix `RECEIPT_PIN=FAIL`.
- Observed on two no-separator variants (2-line body, 1-line body): exit 1,
  stdout exactly `RECEIPT_PIN=FAIL header/body`, stderr empty — matches derivation.
- Paired valid control (blank separator present, same digest/path/revision): exit 0,
  `RECEIPT_PIN=PASS` — isolates the missing separator as sole cause of failure.
- Digest binds the frozen blob `f99de3bd...:corpus/evidence/round65/claims.md`
  (`b9dbca57…2fc5`); git-plumbing-only, no working-tree hashing.

## Evidence

`.ufo/waves/round-65/w1/Probe18/`: `report.md`, `probe18-nosep-fixture.sh`,
`probe18-nosep-run.log` (exact receipt bytes via `cat -A`, argv, exit/stdout/stderr),
three `.receipt` fixtures, raw `v*.stdout`/`v*.stderr` captures, `probe18-derive.py` /
`probe18-derive.out`.

## Hygiene

No production/fleet-root writes; scratch clone at `/fast/scratch/hyaku/chousa-r65/Probe18`
deleted after evidence copy; TMPDIR confined to scratch; no /tmp evidence; no tools
installed; no git mutations (lane repo used read-only via explicit `-C`; one scratch clone).

## Risks / notes for L1

- Exact FAIL suffix `header/body` is reference output text, not a frozen-format
  requirement; frozen contract asserts exit 1 + `RECEIPT_PIN=FAIL` only.
- One surface probed per seat scope (plus one paired valid control); the remaining
  malformed/usage surfaces await the integration battery.
