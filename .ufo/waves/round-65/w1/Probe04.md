# Probe04 — R65-C1 receipt fixture, no-revision surface (round65)

Freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`. Claim probed: **C1** (frozen claims, round65).
Date: 2026-10-30. Seat: Probe04 (leaf, chousa lane). No production writes; no git/jj mutations;
read-only `git cat-file` only, via explicit `-C`.

## Scope

One surface only: receipts that violate the frozen format's `REVISION` header rule
("exactly ordered REVISION full lowercase 40 hex ... 0 consistent, 1 invalid, 2 usage/environment").
Reference tool: `corpus/evidence/round65/controls/ref-receipt-pin.py`. Production target
`tools/receipt-pin.py` does **not** exist at this freeze (before-state, consistent with
`controls/c1-before.txt` CASES=0/20).

## Method

1. Built the canonical valid receipt exactly as the frozen counter does
   (`git -C <lane> cat-file blob d6ed8155...:SKILL.md` → sha256 → header block + blank line + body).
2. Derived expected results **independently** from the frozen spec text in `claims.md` only
   (a standalone checker in the driver; no reference-tool logic reused).
3. Ran the frozen reference with the canonical argv shape
   `python3 -B ref-receipt-pin.py --receipt <f> --root <lane> --revision <BASE>`
   (timeout 20s, `TMPDIR` inside scratch), capturing exit/stdout/stderr verbatim.
4. Sanity control: the unmodified valid receipt run through the same driver must exit 0
   with `RECEIPT_PIN=PASS` (guards against a harness that only ever fails).

## Variants (all on the REVISION-header surface)

| case | mutation | independent expect | reference actual | agree |
|---|---|---|---|---|
| control-valid | none | 0 / PASS | 0 / PASS | yes |
| absent | drop `REVISION=` line (counter's `no-revision` case) | 1 | 1 FAIL | yes |
| empty-value | `REVISION=` bare | 1 | 1 FAIL | yes |
| upper-hex | revision uppercase | 1 | 1 FAIL | yes |
| mixed-hex | partial uppercase | 1 | 1 FAIL | yes |
| nonhex-40 | 40 `g` chars | 1 | 1 FAIL | yes |
| trailing-space | 40 hex + space | 1 | 1 FAIL | yes |
| short-8 | 8-char prefix | 1 | 1 FAIL | yes |

Driver verdict: `ALL_AGREE=True`, driver exit 0. Every malformed variant exits 1 with
stdout `RECEIPT_PIN=FAIL header/body`, empty stderr. The `absent` fixture is byte-identical
in construction to the counter's `no-revision` case (`v.split('\n',1)[1]`), so the frozen
counter's expectation (exit 1, `RECEIPT_PIN=FAIL ` prefix) is independently reproduced.

## Evidence (this folder)

- `probe04-no-revision-results.json` — machine-readable rows (expect/actual/stdout/stderr/agree).
- `probe04-fixture-*.txt` — the 8 receipts as written (including the valid control).
- `probe04-no-revision-driver.py` — the fixture driver (independent checker + runner).

## Risks / limitations

- Reference fail-message granularity is coarse (`header/body`): all revision-family defects
  share one token. The frozen counter only requires the `RECEIPT_PIN=FAIL ` prefix for rc=1
  cases, so this is within the frozen predicate; a future stricter oracle is out of scope here.
- One surface only, per seat spec; the other 19 frozen cases were not re-run by this seat.
- The independent checker mirrors the spec text, not the reference code; agreement on all 8
  rows is evidence, not proof, of spec conformance.
- No tools installed this seat (system `python3 3.14.8`, system `git` sufficed).

## Blockers

None.
