# Probe17 — round65 duplicate-header receipt probe (scoped findings)

Freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd. One surface: duplicate headers in the frozen
receipt format. Reference under test: `corpus/evidence/round65/controls/ref-receipt-pin.py`
(production `tools/receipt-pin.py` not yet present). argv preserved; read-only `git -C` at frozen
base `d6ed8155e9b4735639a2cf0a3e479c62f2056195`; blob-bound digest, no working-tree hashing.
Full detail + fixtures: `.ufo/waves/round-65/w1/Probe17/report.md` and same-folder receipts/results.json.

## Observed

- control-valid → exit 0 `RECEIPT_PIN=PASS` (matches expectation).
- dup-revision, dup-exit, dup-sha256 (same value), dup-sha256-diffval → all exit 1
  `RECEIPT_PIN=FAIL header/body` (matches expectation).

## Gap (independent derivation vs reference behavior)

- **dup-in-body → exit 0 `RECEIPT_PIN=PASS`, expected reject.** A receipt with a valid
  3-line header, blank separator, nonempty body, then a second full REVISION/EXIT/SHA256 block
  inside the body is accepted. The reference enforces "exactly one of each header" only
  positionally (lines[0..2]); body lines are never scanned for header-shaped duplicates.
- Root cause: rejection of in-header duplicates is a side effect of the strict positional parse,
  not an occurrence-count check. Docstring overstates enforcement.
- Suggestion for production target (if strict docstring semantics intended): reject
  `^(REVISION|EXIT|SHA256)=` matches in `lines[4:]`. Consistency/interface gap only — not an
  execution-authentication claim per claims.md C1.

No battery run. No production writes. Scratch deleted after receipts copied to this folder.
No tools installed this seat.
