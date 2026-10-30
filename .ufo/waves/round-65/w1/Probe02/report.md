# Probe02 — nonzero-valid receipt fixture (round 65, C1 surface)

Seat: Probe02 (leaf). Scope: one isolated fixture surface — the frozen `nonzero-valid`
case for `tools/receipt-pin.py` (target does not exist yet; oracle is the prefreeze
reference `corpus/evidence/round65/controls/ref-receipt-pin.py`). No full battery run;
no production writes; read-only git with explicit `-C`.

## Independent derivation (from frozen format in claims.md only)

Frozen format: ordered headers `REVISION=<40 lc hex>` / `EXIT=<decimal 0..255>` /
`SHA256=<64 lc hex> <canonical relative POSIX path>`, empty separator, nonempty
body. Exit legend: 0 consistent, 1 inconsistent/malformed, 2 usage/environment.
Digest binds the Git blob at the declared revision; revision must equal
`--revision`; no working-tree hashing.

Derived expectation for `nonzero-valid`: EXIT is bound data in range, not the
validator's own status. A receipt with `EXIT=1`, matching revision, and a digest
that binds the named blob at that revision is consistent → **exit 0, token
`RECEIPT_PIN=PASS`**. The validator's exit must not propagate the receipt's
reported exit.

Digest derived independently of counter internals, two agreeing channels
(`sha256sum` over `git cat-file blob`; `hashlib.sha256` over the same bytes):
`4355e16a5d8d16057496f005df7382ca287863712ed2e3abb25f61c60008ce1a` for
`d6ed8155e9b4735639a2cf0a3e479c62f2056195:SKILL.md` (object type verified `blob`).

## Fixture and argv

Argv identical to the counter's tool invocation:
`python3 -B <tool> --receipt <fixture> --root /home/vgpnk/Projects/shokunin/chousa-shokunin --revision d6ed8155e9b4735639a2cf0a3e479c62f2056195`

Core fixture (`nonzero-valid-exit1.txt`): headers with `EXIT=1`, correct revision
and digest binding, blank separator, nonempty body.

## Results (reference as tool)

| fixture | receipt EXIT | rc | stdout |
|---|---|---|---|
| nonzero-valid-exit1 | 1 | 0 | `RECEIPT_PIN=PASS` |
| nonzero-valid-exit255 | 255 | 0 | `RECEIPT_PIN=PASS` |
| nonzero-exit-bad-digest | 1 | 1 | `RECEIPT_PIN=FAIL blob/digest` |
| nonzero-exit-wrong-revision | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| nonzero-valid-exit01 | 01 | 1 | `RECEIPT_PIN=FAIL header/body` |

## Findings

1. **Assigned surface confirmed**: nonzero-valid → exit 0 + `RECEIPT_PIN=PASS`.
   Independent derivation from the frozen format matches the oracle; a production
   `tools/receipt-pin.py` must accept a fully consistent receipt whose reported
   EXIT is nonzero (the reported exit is data, not verdict).
2. **No exit-code leak**: validator exit stays 0 for consistent nonzero-exit
   receipts at EXIT=1 and the 255 boundary; the receipt's reported exit never
   becomes the validator's own exit code.
3. **Binding is exit-agnostic**: under EXIT=1, a tampered digest still fails
   (`blob/digest`) and a mismatched revision still fails (`header/body`) —
   nonzero reported exit does not weaken the revision/digest binding.
4. **Observed strictness beyond frozen 20**: `EXIT=01` (leading zero) is rejected
   by the reference (`header/body`), i.e. EXIT must be canonical decimal. Not one
   of the frozen 20 cases; noted for interface fidelity, not scored.

## Evidence

- `nonzero-valid-receipts.log` — run log with both digest-derivation channels,
  argv, and per-fixture outcomes (this folder).
- Fixtures lived in scratch and were deleted on exit per seat spec.

## Risks / notes for L1

- The strict canonical-decimal EXIT reading (leading zeros rejected) comes from
  the reference implementation, not an explicit frozen case; if production
  diverges here it is unscored but observable.
- No installs this seat (python3 3.14.8 and git already present; nothing added,
  so tooling-directive record is empty).
- No blockers. Scratch `/fast/scratch/hyaku/chousa-r65/Probe02` deleted after
  copying receipts here.
