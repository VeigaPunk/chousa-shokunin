# Probe17 — isolated duplicate-header receipt fixture (round65, freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd)

Seat: Probe17 (leaf, lane chousa round65). Scope: one surface only — **duplicate header lines** in the
frozen receipt format (claims.md C1). No battery, no production writes, no git mutations. Read-only
git via explicit `git -C` against the lane repo at frozen base `d6ed8155e9b4735639a2cf0a3e479c62f2056195`.

## Method

- Independently derived expected results from the frozen format spec (claims.md C1 + reference
  docstring): exactly one `REVISION=` / `EXIT=` / `SHA256=` header, in that order, then one blank
  separator, then nonempty body. Expected: any duplicate header rejected with exit 1 and a
  `RECEIPT_PIN=FAIL` token; valid control accepted with exit 0 and `RECEIPT_PIN=PASS`.
- Target under test: `corpus/evidence/round65/controls/ref-receipt-pin.py` (prefreeze reference,
  not the not-yet-existing production `tools/receipt-pin.py`). argv preserved:
  `--receipt <file> --root <repo> --revision <40-hex>`.
- Blob bound: `.ufo/evidence/round-1/receipt-blocker.json` at revision
  `d6ed8155e9b4735639a2cf0a3e479c62f2056195`, digest `git cat-file` + sha256 =
  `16b52ff4a9f5068aeed4404c62c8fa8908ee0753704206364f8f78c18cab2cb8`. No working-tree hashing.
- Driver: `dup_probe.py` (scratch, deleted on exit); receipts + `results.json` copied to this folder.

## Results (observed)

| variant | exit | stdout | expected | verdict |
|---|---|---|---|---|
| control-valid | 0 | `RECEIPT_PIN=PASS` | accept (0) | PASS |
| dup-revision (2nd REVISION after line 0) | 1 | `RECEIPT_PIN=FAIL header/body` | reject (1) | PASS |
| dup-exit (2nd EXIT line) | 1 | `RECEIPT_PIN=FAIL header/body` | reject (1) | PASS |
| dup-sha256 (same digest repeated) | 1 | `RECEIPT_PIN=FAIL header/body` | reject (1) | PASS |
| dup-sha256-diffval (2nd SHA256, zero digest) | 1 | `RECEIPT_PIN=FAIL header/body` | reject (1) | PASS |
| dup-in-body (valid 3-line header, body then repeats full header block) | 0 | `RECEIPT_PIN=PASS` | reject (1) | **FAIL — gap** |

## Findings

1. **Header-position duplicates are rejected for positional reasons, not by an explicit
   uniqueness check.** All four in-header duplicates exit 1 because the extra line shifts the
   strict positional parse (`lines[0]`/`lines[1]`/`lines[2]`/`lines[3]`), not because the
   reference counts occurrences of each header. The docstring's "Exactly one of each header, in
   that order" is enforced only at positions 0–2.
2. **Gap: duplicate headers inside the body are accepted.** A receipt with a valid 3-line header,
   blank separator, a nonempty body line, and then a second full `REVISION/EXIT/SHA256` block in
   the body returns exit 0 / `RECEIPT_PIN=PASS`. The reference never inspects body lines, so
   trailing duplicate header material is tolerated. If production `tools/receipt-pin.py` must
   honor the docstring claim strictly, it needs a body scan for header-shaped lines (e.g. reject
   any `^(REVISION|EXIT|SHA256)=` match in `lines[4:]`). This is a consistency/interface gap only;
   per claims.md this is not execution authentication.
3. Frozen-format boundary confirmed: revision equality is strict string match against
   `--revision`; no normalization observed (control depends on exact full-lowercase 40 hex).

## Evidence retained in this folder

- `results.json` — observed exit/stdout per variant.
- `control-valid.receipt`, `dup-{revision,exit,sha256,sha256-diffval,in-body}.receipt` — fixtures.

Scratch `/fast/scratch/hyaku/chousa-r65/Probe17/` deleted after copying receipts (no /tmp evidence).
No tools installed this seat. No production writes. git used read-only with explicit `-C`.
