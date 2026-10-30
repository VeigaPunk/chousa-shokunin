# Probe12 — R65-C1 receipt fixture, wrong-digest surface (round65)

Freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`. Claim probed: **C1** (frozen claims, round65).
Date: 2026-10-30. Seat: Probe12 (leaf, chousa lane). No production writes; no git/jj mutations;
read-only `git cat-file` only, via explicit `-C`.

## Scope

One surface only: receipts whose declared `SHA256` digest does not match the Git blob at the
declared revision ("Digest binds the Git blob at the declared revision ... 0 consistent,
1 invalid, 2 usage/environment", frozen `claims.md` C1). Reference tool:
`corpus/evidence/round65/controls/ref-receipt-pin.py`. Production target
`tools/receipt-pin.py` does **not** exist at this freeze (before-state, consistent with
`controls/c1-before.txt` CASES=0/20).

## Method

1. Independently derived the blob digest: `git -C <lane> cat-file blob
   d6ed8155e9b4735639a2cf0a3e479c62f2056195:SKILL.md` → 172,749 bytes →
   `sha256 = 4355e16a5d8d16057496f005df7382ca287863712ed2e3abb25f61c60008ce1a`,
   computed two ways (GNU `sha256sum` CLI and Python `hashlib`), agreeing byte-for-byte.
2. Built the canonical valid receipt exactly as the frozen counter does
   (`REVISION=<BASE>\nEXIT=0\nSHA256=<h> SKILL.md\n\nmeasured output\n`).
3. Derived expected results **independently** from the frozen spec text in `claims.md` only
   (standalone driver; no reference-tool logic reused for expectations): a well-formed
   receipt whose declared digest ≠ blob digest is *inconsistent* → exit 1, stdout starting
   `RECEIPT_PIN=FAIL ` (the frozen counter's rc=1 predicate).
4. Ran the frozen reference with the canonical argv shape
   `python3 -B ref-receipt-pin.py --receipt <f> --root <lane> --revision <BASE>`
   (timeout 20s, `TMPDIR` inside scratch), capturing exit/stdout/stderr verbatim.
5. Sanity control: the unmodified valid receipt run through the same driver must exit 0
   with `RECEIPT_PIN=PASS` (guards against a harness that only ever fails), plus an
   assertion that each wrong digest truly differs from the true digest.

## Variants (all on the digest-binding surface)

| case | mutation | independent expect | reference actual | agree |
|---|---|---|---|---|
| control-valid | none | 0 / PASS | 0 / PASS | yes |
| wrong-digest-zeros | true digest → `0`*64 (counter's `wrong-digest` construction) | 1 / FAIL prefix | 1 / `RECEIPT_PIN=FAIL blob/digest` | yes |
| wrong-digest-flip | true digest, last nibble flipped | 1 / FAIL prefix | 1 / `RECEIPT_PIN=FAIL blob/digest` | yes |

Driver verdict: `ALL_AGREE=True`, driver exit 0. Both wrong-digest variants exit 1 with
stdout `RECEIPT_PIN=FAIL blob/digest`, empty stderr. The `wrong-digest-zeros` fixture is
byte-identical in construction to the frozen counter's `wrong-digest` case
(`v.replace(h,'0'*64)`), so the frozen counter's expectation (exit 1, `RECEIPT_PIN=FAIL `
prefix) is independently reproduced. The flip variant shows the trigger is the
digest/blob mismatch itself, not the specific all-zeros value.

## Evidence (this folder)

- `probe12-wrong-digest-results.json` — machine-readable rows (expect/actual/stdout/stderr/agree),
  true blob digest, argv shape.
- `probe12-fixture-*.txt` — the 3 receipts as written (including the valid control).
- `probe12-wrong-digest-driver.py` — the fixture driver (independent checker + runner).

## Risks / limitations

- Reference fail-message granularity is coarse (`blob/digest`): header-format digest defects
  (short/uppercase/missing, counter cases `short-digest`, `upper-digest`, `no-digest`) share
  the same rc=1 family but were not re-probed here — one surface only, per seat spec.
- The frozen counter only requires the `RECEIPT_PIN=FAIL ` prefix for rc=1 cases; the exact
  reason token is reference implementation detail, not frozen text.
- The independent checker mirrors the spec text, not the reference code; agreement on all 3
  rows is evidence, not proof, of spec conformance.
- No tools installed this seat (system `python3 3.14.8`, system `git 2.56.0` sufficed).

## Blockers

None.
