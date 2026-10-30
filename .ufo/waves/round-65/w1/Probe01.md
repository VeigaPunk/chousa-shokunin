# Probe01 — round65 chousa, receipt valid-surface probe

Seat: Probe01 (leaf). Round: 65 chousa. Freeze: f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd.
Lane root: /home/vgpnk/Projects/shokunin/chousa-shokunin. Date: 2026-10-30.
Scope: one surface only — a *valid* receipt against the frozen reference
`corpus/evidence/round65/controls/ref-receipt-pin.py`. No full battery run.

## Preconditions (read-only checks)

- Production target `tools/receipt-pin.py`: **absent** (expected pre-implementation; seat made no production writes).
- Base commit `d6ed8155e9b4735639a2cf0a3e479c62f2056195` present in lane repo (`git -C` rev-parse).
- Blob `d6ed8155...:SKILL.md` present (`git -C` cat-file -t → blob).
- Interpreter `/usr/bin/python3` = Python 3.14.8; git 2.56.0. No tools installed or updated this seat.

## Independent derivation from the frozen format (claims.md C1)

Format rules read directly from the frozen claims (not from reference code):
`REVISION=<full lowercase 40 hex>` (must equal caller `--revision`),
`EXIT=<decimal 0..255>`, `SHA256=<full lowercase 64 hex> <canonical relative POSIX path>`,
empty separator line, nonempty output body. Digest binds the Git blob at the declared
revision; revision must equal `--revision`; no working-tree hashing. Verdict codes:
0 consistent, 1 invalid, 2 usage/environment. Counter contract on rc=0 cases requires
stdout token `RECEIPT_PIN=PASS`.

Fixture `valid.txt` (155 bytes) built with `EXIT=0`, path `SKILL.md`, digest
`4355e16a5d8d16057496f005df7382ca287863712ed2e3abb25f61c60008ce1a` = sha256 of
`git -C <lane> cat-file blob d6ed8155...:SKILL.md`, body `measured output`.
Independent oracle `probe01-derive.py` (scratch, no code shared with the reference)
evaluated the frozen rules and derived:

    DERIVED: consistent -> EXPECTED_EXIT=0 EXPECTED_STDOUT="RECEIPT_PIN=PASS\n"

## Reference run (argv shape preserved from c1-count.py invocation)

    /usr/bin/python3 -B corpus/evidence/round65/controls/ref-receipt-pin.py \
        --receipt <scratch>/valid.txt \
        --root /home/vgpnk/Projects/shokunin/chousa-shokunin \
        --revision d6ed8155e9b4735639a2cf0a3e479c62f2056195

Observed: exit **0**; stdout exactly `RECEIPT_PIN=PASS\n` (17 bytes, od -c verified);
stderr empty.

## Comparison

Observed reference behavior on the valid surface matches the independently derived
expectation exactly (exit 0, token `RECEIPT_PIN=PASS` + newline, empty stderr).
The reference treats a well-formed receipt whose digest binds the blob at the declared
base revision as consistent, per the frozen format. This supports C1's `valid` case
behavior; it is interface/consistency coverage only — no execution-authenticity claim.

## Evidence (this folder)

- `probe01-valid-receipt.txt` — the 155-byte valid fixture receipt (exact bytes).
- `probe01-ref.stdout` / `probe01-ref.stderr` / `probe01-ref.exit` — raw reference run capture.
- `probe01-derive.py` / `probe01-derive.out` — independent frozen-format oracle and its derivation.

## Risks / limits

- Only the valid surface probed per seat scope; the 19 invalid/malformed surfaces and
  usage/environment exit-2 paths are left to L1's c1-count integration battery.
- Digest was computed with `sha256sum` over git plumbing output and cross-checked by the
  oracle's hashlib path; both agree with the reference's binding.
- Scratch `/fast/scratch/hyaku/chousa-r65/Probe01` deleted after evidence copy; no /tmp evidence; TMPDIR confined to scratch.
