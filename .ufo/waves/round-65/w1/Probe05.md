# Probe05 — round65 wrong-revision probe (trailer)

Scoped findings; full detail + evidence in `.ufo/waves/round-65/w1/Probe05/`.

- Ran an **isolated** wrong-revision fixture (one surface, no battery) against the frozen
  reference `corpus/evidence/round65/controls/ref-receipt-pin.py`, argv preserved from the
  C1 counter shape (`--receipt/--root/--revision`).
- Expectations derived independently from the frozen format contract in `claims.md`
  (REVISION full lowercase 40 hex; must equal caller `--revision`; 0 consistent / 1 invalid /
  2 usage-environment). Valid-arm digest computed directly via
  `git cat-file blob d6ed8155…:SKILL.md | sha256sum` = `4355e16a…08ce1a`.
- **Result: 5/5 fixtures match.** valid-control → exit 0 `RECEIPT_PIN=PASS`. All four
  wrong-revision arms (zeros, real alternate commit FREEZE `f99de3bd…` with internally
  consistent digest, caller-side mismatch, uppercase hex) → exit 1 `RECEIPT_PIN=FAIL header/body`.
- Confirms: revision equality is enforced against the caller-supplied value in both
  directions before blob/digest binding; mismatches are class 1 (invalid), never 2.
- Observation for L1: invalid arms share one reason string (`header/body`); within the
  frozen counter's contract (rc≠0 needs only the `RECEIPT_PIN=FAIL ` prefix), but
  wrong-revision is not distinguishable from other header/body defects by token.
- No installs (system python3/git/sha256sum only), no network, no production writes, no git
  mutations (read-only `git -C` lane only). Scratch `/fast/scratch/hyaku/chousa-r65/Probe05/`
  deleted; receipts copied to the seat folder above. Probe05 closed.
