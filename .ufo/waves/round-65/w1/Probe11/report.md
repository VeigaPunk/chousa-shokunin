# Probe11 — round65 receipt-pin `no-digest` isolated probe

Seat: Probe11 (leaf, lane chousa round65). Freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.
Scope: single frozen surface `no-digest` from `corpus/evidence/round65/c1-count.py` case table.
Reference under test: `corpus/evidence/round65/controls/ref-receipt-pin.py` (production
`tools/receipt-pin.py` absent prefreeze — confirmed `is_file() == False`, no production writes).

## Independent expectation (derived from frozen claims.md format, not from the reference)

Frozen format: `REVISION=<40 lowercase hex>`; `EXIT=<0..255>`; `SHA256=<64 lowercase hex> <repo-relative path>`;
empty separator; nonempty output. Exactly one of each header, in order. Digest binds the Git blob at the
declared revision; `0 consistent, 1 invalid, 2 usage/environment`.

`no-digest` removes the entire `SHA256=...` line from an otherwise valid receipt, leaving
`REVISION=...\nEXIT=0\n\nmeasured output\n` → 4 lines. The format requires the three header lines plus
separator plus body, so the receipt no longer satisfies the frozen shape → expect validator exit `1`
with a `RECEIPT_PIN=FAIL ` token (per c1-count.py negative-case contract: `rc==1 and
stdout.startswith('RECEIPT_PIN=FAIL ')`). The exact message text is not frozen.

## Fixture (isolated, scratch-only)

- Scratch: `/fast/scratch/hyaku/chousa-r65/Probe11/` — fixture git repo created there only; git mutations
  guarded by asserting `git rev-parse --show-toplevel == <fixture repo>` before commit. Deleted on exit.
- Fixture blob: commit `20970fae61c6cbccc3e4bc83befa99f60070217e`, path `artifact-r65.txt`,
  sha256 `9dd6d3c8e49d69c3c02514830defccfdf34d6a378e5b8c8711e780e80d720bda` (from `git cat-file blob`, raw bytes).
- Receipt argv preserved: `--receipt <no-digest.txt> --root <repo> --revision <rev>`; run via
  `python3 -B controls/ref-receipt-pin.py`.
- Cross-check substrate: same no-digest receipt shape bound to frozen `BASE=d6ed8155...:SKILL.md`
  (lane repo, read-only `git -C cat-file`).

## Results

| substrate | receipt | rc | stdout | expected |
|---|---|---|---|---|
| fixture repo | no-digest | 1 | `RECEIPT_PIN=FAIL header/body` | rc1 + FAIL prefix — match |
| lane repo (frozen BASE blob) | no-digest | 1 | `RECEIPT_PIN=FAIL header/body` | match |
| fixture repo | valid control | 0 | `RECEIPT_PIN=PASS` | match |

Probe verdict: **PASS** (all three rows match independent expectation).

## Note on failure token

The reference reports `header/body`, not `digest header`: removing the SHA256 line collapses the receipt
to 4 lines, so the `len(lines)<5` header/body gate fires before the `SHA256=` regex is ever evaluated.
This is exactly what the frozen counter exercises and permits (negative cases freeze only exit code and
the `RECEIPT_PIN=FAIL ` prefix).

## Environment

- git 2.56.0, Python 3.14.8 (system). No tool installs needed or performed.
- Read-only lane git use only (`cat-file`, `rev-parse`); no commits/pushes/mutations outside the scratch fixture.

## Evidence (this folder)

- `probe11-transcript.txt` — captured run transcript.
- `probe11-no-digest-fixture.txt`, `probe11-no-digest-frozen-base.txt` — the probed receipts.
- `probe11-valid-control.txt` — valid-receipt control.
- `probe11-run-fixture.py` — the isolated fixture driver (rerunnable, scratch-only).

## Risks / blockers

None. Production target intentionally absent (prefreeze state per claims C1 before-control). Single-surface
probe; full 20-case battery intentionally not run (L1 owns integration verification).
