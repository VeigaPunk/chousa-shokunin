# Probe10 — word-exit receipt fixture probe (round65)

Seat: Probe10 (leaf probe). Date: 2026-10-30. Lane freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.

## Scope

One surface only: the `EXIT=` word of the receipt header, probed against the frozen
reference `corpus/evidence/round65/controls/ref-receipt-pin.py`. No full battery was run;
no production path was written or executed (the production `tools/receipt-pin.py` does not
exist yet — only the prefreeze reference was exercised).

## Frozen format (claims.md, round65, C1)

`REVISION=<40 lowercase hex>` / `EXIT=<0..255 decimal>` / `SHA256=<64 lowercase hex> <repo-relative path>` /
empty separator line / nonempty output. Exits: 0 consistent, 1 invalid, 2 usage/environment.

## Independent oracle (derived from the frozen text, not from reference code)

Accept the EXIT word iff it is a canonical ASCII decimal numeral for an integer in `[0,255]`:
nonempty, all ASCII digits, no leading zero unless the word is exactly `"0"`, at most 3 digits,
value ≤ 255. Everything else in the receipt was held fixed and valid, so a disagreement can
only be attributable to the EXIT word. Expected: accepted word → exit 0 with exactly
`RECEIPT_PIN=PASS`; rejected word → exit 1 with a `RECEIPT_PIN=FAIL` line; never exit 2
(receipt exists, `--revision` well-formed, so usage/environment does not apply).

## Fixture (isolated, scratch-only)

Fresh one-commit git repo created in scratch (`git init`, user `probe10@local`); no clone of
any source tree. Blob `pin.txt` at revision `070c12f9d4f6204b4543b1141024214f2f57b262`, digest
`8282330369248662097b58153cf36fddbe27220c3ba1925d6a78a2cb39131519` (via
`git cat-file blob <rev>:pin.txt` piped to `sha256sum`, matching the reference's binding rule).
Every generated receipt declares that revision and digest, so REVISION equality and blob
binding stay satisfied across all cases. argv preserved exactly:
`python3 ref-receipt-pin.py --receipt <case> --root <fixture> --revision <rev>`.

## Result

35/35 AGREE, 0 mismatches (see `probe10-word-exit-matrix.tsv`):

- Accepted (exit 0, `RECEIPT_PIN=PASS`): `0, 1, 9, 42, 127, 200, 255` (7 cases).
- Rejected (exit 1, `RECEIPT_PIN=FAIL header/body`): 28 cases across
  - leading zeros: `00, 01, 09, 042, 0255, 000`
  - out of range: `256, 257, 300, 999`
  - overlong: `1000, 10000`
  - empty, signed, whitespace-padded, internal space: `"" , -1, +1, " 42", "42 ", "\t42", "42\t", "4 2"`
  - non-decimal notation: `0x2a, 0b101010, 2.5, 2a, 4_2`
  - Unicode digit lookalikes: Arabic-Indic `٤٢`, fullwidth `４２`, `4²` (all isdigit()-true but non-ASCII/non-numeral)
- Exit code 2 never observed; rejected words always fail with exit 1, as frozen.

The reference enforces canonical decimal with no leading zeros and a hard ≤255 bound — exactly
the frozen "EXIT decimal 0..255" wording. Boundary behavior at 255/256 and 999/1000 is sharp
and matches the independent oracle.

## Evidence retained (this folder)

- `probe10-word-exit-matrix.tsv` — full 35-case matrix (word, expected, actual exit, actual stdout, verdict)
- `probe10-receipt-w00.txt` — exemplar accepted receipt (`EXIT=0`)
- `probe10-receipt-w11.txt` — exemplar rejected receipt (`EXIT=0255`, leading zero)
- `probe10-receipt-w13.txt` — exemplar rejected receipt (`EXIT=256`, out of range)
- `probe10-receipt-w32.txt` — exemplar rejected receipt (`EXIT=٤٢`, Arabic-Indic digits)
- `probe10-word-exit-probe.py` — driver (fixture-independent; regenerates all receipts and reruns the reference)
- `probe10-fixture-meta.env` — tool versions and fixture rev/digest

## Environment / installs

- python3 3.14.8, git 2.56.0 — preinstalled, no installs or upgrades performed (nothing needed).
- Pacman untouched (host-wide pause respected). No network fetches. No git mutations outside the scratch fixture.
- Scratch `/fast/scratch/hyaku/chousa-r65/Probe10/` deleted after evidence copy; no /tmp evidence.

## Risks / notes

- Single surface probed by design; other header surfaces (REVISION word, SHA256 word, path
  grammar, separator/body shape, usage vs invalid split) are out of this seat's scope.
- All findings are behavior of the frozen reference on an isolated fixture; L1 integration
  verifies against production once it exists.
