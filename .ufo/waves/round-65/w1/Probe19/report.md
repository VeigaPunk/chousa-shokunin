# Probe19 — round65 receipt no-body fixture (seat report)

## Scope
Isolated probe of one surface only: **no-body** receipt handling in the receipt-header
consistency validator. Reference control used (production `tools/receipt-pin.py` may not
exist yet): `corpus/evidence/round65/controls/ref-receipt-pin.py`, invoked unmodified with
its normal argv (`--receipt`, `--root`, `--revision`). No battery/counter run.

## Inputs
- Freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` (verified present via read-only
  `git -C <lane> cat-file -t`).
- Blob: `SKILL.md` at the freeze revision, digest bound per frozen format
  (`SHA256=<64 lowercase hex> <repo-relative path>`), digest recomputed from
  `git cat-file blob` bytes (sha256sum): `4355e16a5d8d16057496f005df7382ca287863712ed2e3abb25f61c60008ce1a`.
- `--root` was a scratch clone (one live clone, local source, no network); lane repo untouched.

## Independent expectation (derived from frozen format in claims.md)
Frozen format: `REVISION` line, `EXIT` line, `SHA256` + relative path line, **empty
separator**, **nonempty output**; exit `0 consistent, 1 invalid, 2 usage/environment`.
A receipt with no output body violates the mandatory "nonempty output" clause, with all
other header fields valid ⇒ malformed/invalid ⇒ **exit 1, `RECEIPT_PIN=FAIL` token**.

## Observed (actual runs, preserved in probe19-results.txt)
| case | receipt | expected | observed | verdict |
|---|---|---|---|---|
| no-body | headers + separator, then EOF | rc=1, `RECEIPT_PIN=FAIL header/body` | rc=1, `RECEIPT_PIN=FAIL header/body` | MATCH |
| ws-body (same surface: whitespace-only body) | headers + separator + `"   "` | rc=1, `RECEIPT_PIN=FAIL header/body` | rc=1, `RECEIPT_PIN=FAIL header/body` | MATCH |
| positive control | headers + separator + `measured output` | rc=0, `RECEIPT_PIN=PASS` | rc=0, `RECEIPT_PIN=PASS` | MATCH |

The positive control confirms the harness itself (clone, revision equality, blob/digest
binding) is sound, so the no-body failures are attributable solely to the absent body.

## Cross-check against frozen counter
`c1-count.py` freezes the no-body case as `('no-body', v.split('\n\n')[0]+'\n\n', 1)` —
byte-identical construction to my no-body receipt (modulo counter's BASE vs my seat's
freeze revision), expected exit 1. My independently derived expectation agrees; no
counter was executed (out of seat scope).

## Evidence in this folder
- `probe19-fixture-driver.sh` — fixture driver (exact receipts, argv, oracle)
- `probe19-results.txt` — full observed transcript incl. exact receipt bytes
- `probe19-nobody-receipt.txt`, `probe19-wsbody-receipt.txt`, `probe19-positive-receipt.txt`
- `probe19-{no-body,ws-body,positive}.stderr` — empty (no stderr noise)

## Risks / limits
- ws-body is my own boundary extension of the no-body surface, not one of the frozen 20.
- Probe validates reference behavior only; it does not score or implement the production tool.
- No installs were needed (used system `python3 3.14.8`, `git 2.56.0`); nothing added/updated.

Scratch `/fast/scratch/hyaku/chousa-r65/Probe19/` deleted after receipts were copied here.
