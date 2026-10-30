# Probe20 — round65 isolated probe: upper-digest surface

Seat: Probe20 (leaf, chousa round65). Freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.
Scope: one surface only — the receipt `SHA256=<hex> <path>` digest header and its
binding to the git blob at the declared revision. No battery run; production
target `tools/receipt-pin.py` not touched (may not exist yet).

## Method

- Independent oracle: expectations derived from the frozen claims text
  (`corpus/evidence/round65/claims.md` round65): "SHA256 full lowercase 64 hex
  plus canonical relative POSIX path" and "Digest binds the Git blob at the
  declared revision". Expectations were written before running the reference
  and were not taken from the reference source.
- Fixture: `/fast/scratch/hyaku/chousa-r65/Probe20/probe_upper_digest.py`
  (copied here as `probe20-upper-digest-fixture.py`). It builds one scratch git
  repo (`repo/`, one blob `probe.txt`), asserts
  `git rev-parse --show-toplevel` prints the fixture dir before every git
  mutation, and fixes argv as
  `python3 <ref> --receipt <file> --root <repo> --revision <rev>`.
- Reference exercised: `corpus/evidence/round65/controls/ref-receipt-pin.py`.
- Scratch deleted after receipts/results were copied here.

## Results (7/7 match independent expectation)

| case | expected | actual | match |
|---|---|---|---|
| control-valid | exit 0 `RECEIPT_PIN=PASS` | exit 0 `RECEIPT_PIN=PASS` | yes |
| upper-digest-hex (all-uppercase 64 hex) | exit 1 `RECEIPT_PIN=FAIL digest header` | exit 1 same | yes |
| mixed-digest-hex (alternating case) | exit 1 `RECEIPT_PIN=FAIL digest header` | exit 1 same | yes |
| digest-63-hex | exit 1 `RECEIPT_PIN=FAIL digest header` | exit 1 same | yes |
| digest-65-hex | exit 1 `RECEIPT_PIN=FAIL digest header` | exit 1 same | yes |
| digest-nonhex (`g` at position 21) | exit 1 `RECEIPT_PIN=FAIL digest header` | exit 1 same | yes |
| digest-wrong-value (valid hex, wrong) | exit 1 `RECEIPT_PIN=FAIL blob/digest` | exit 1 same | yes |

Full machine-readable record: `probe20-upper-digest-results.json`; receipt
inputs kept as `probe20-*.receipt` in this folder.

## Interpretation / risks

- The reference enforces lowercase-only 64-hex digest fields and blob binding
  exactly as the frozen format states; upper-digest edges are unambiguous
  (format violation ⇒ exit 1, distinct `digest header` token; value violation ⇒
  `blob/digest` token). No ambiguity observed between exit-1 reasons.
- One surface probed; REVISION/EXIT/path/body edges belong to other seats.
- Fixture used a synthetic blob and a scratch repo only; no fleet repo or
  production file was read by the reference beyond its own argv paths.

## Tooling record

No installs or updates performed (python3 3.14.8 and git 2.56.0 already present;
no pacman transaction). Channels: none used.
