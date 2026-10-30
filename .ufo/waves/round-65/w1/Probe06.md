# Probe06 — round65 scoped findings (short-revision receipt surface)

Full detail + evidence: `.ufo/waves/round-65/w1/Probe06/report.md` (with `transcript.json` and five `.receipt` fixtures).

- Seat probed one surface only: short-revision handling of `corpus/evidence/round65/controls/ref-receipt-pin.py`. Production `tools/receipt-pin.py` absent (verified). No installs (git 2.56.0 / python 3.14.8 preinstalled).
- Independent derivation from frozen C1 format (REVISION = full lowercase 40 hex; 0 consistent / 1 invalid / 2 usage-environment): short `--revision` → exit 2; short receipt-header revision (with full `--revision`) → exit 1; full/full anchor → exit 0.
- Fixture: fresh scratch repo, commit `ac3407da7e1006fa29c49d9175d49dc6fc8ebb7c`, blob sha256 `1691be3e…30f7` bound via `git cat-file` exactly as the reference binds it; toplevel asserted before mutations.
- Result: 5/5 cases observed == independently derived (12-hex arg → 2; 12-hex receipt header → 1 `RECEIPT_PIN=FAIL header/body`; 39-hex arg → 2; full/full anchor → 0 `PASS`; 12-hex arg of a nonexistent object → 2, proving the length check precedes any git lookup).
- No discrepancy found on this surface; claim boundary untouched (interface/consistency, not execution authentication). Scratch `/fast/scratch/hyaku/chousa-r65/Probe06/` deleted after evidence copy. No production/fleet-root/sibling writes; no network.
