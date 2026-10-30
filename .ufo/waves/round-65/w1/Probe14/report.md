# Probe14 — round65 missing-blob receipt fixture

Seat: Probe14 (leaf probe). Surface: missing-blob behavior of the round65 receipt-pin
contract. Reference exercised: `corpus/evidence/round65/controls/ref-receipt-pin.py`
(production `tools/receipt-pin.py` confirmed absent — matches C1 before-control).
Freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` = lane HEAD ("round-65: freeze receipt
identity claims and controls"). No production writes, no git/jj mutations, no network.

## Independent expectation (derived before running)

From the frozen format (claims.md C1): `REVISION=<40 lowercase hex>; EXIT=<0..255>;
SHA256=<64 lowercase hex> <canonical relative POSIX path>`; empty separator; nonempty
output. "Digest binds the Git blob at the declared revision"; exit legend
`0 consistent, 1 invalid, 2 usage/environment`. A receipt naming a path with **no blob
at `<revision>:<path>`** has nothing to bind → invalid → **exit 1**.
Reference contract maps that failure to token **`RECEIPT_PIN=FAIL blob/digest`**
(nonzero `git cat-file` returncode). Missing-revision funnels to the same check.

## Fixture (scratch-only, deleted after receipt copy)

Fresh `git init` repo at `/fast/scratch/hyaku/chousa-r65/Probe14/repo` (no clone, no
fetch), one commit `5ced04cdb686adf249f1c9ae7b877342b27461fa` containing `hello.txt`
(blob sha256 `b95f233d…912aa`). Receipts written in the frozen format; missing-blob
receipts carry the empty-blob digest `e3b0c442…2b855` as a worst-case plausible value so
only the blob lookup can fail. Driver invoked the reference verbatim
(`--receipt/--root/--revision`), preserving argv and output. `TMPDIR` pinned inside
scratch. Python 3.14.8, git 2.56.0.

## Results — 4/4 match independent expectation

| case | root / revision | expectation | observed | match |
|---|---|---|---|---|
| A positive control | fixture repo @ `5ced04cd…` | exit 0, `RECEIPT_PIN=PASS` | exit 0, `RECEIPT_PIN=PASS` | yes |
| B missing path | fixture repo @ `5ced04cd…`, `no/such/file.txt` | exit 1, `RECEIPT_PIN=FAIL blob/digest` | exit 1, `RECEIPT_PIN=FAIL blob/digest` | yes |
| C missing revision | fixture repo @ freeze id (absent object) | exit 1, `RECEIPT_PIN=FAIL blob/digest` | exit 1, `RECEIPT_PIN=FAIL blob/digest` | yes |
| D lane freeze repo | lane @ `f99de3bd…`, missing controls path | exit 1, `RECEIPT_PIN=FAIL blob/digest` | exit 1, `RECEIPT_PIN=FAIL blob/digest` | yes |

Underlying `git cat-file blob` evidence (rc 128 in all missing-blob cases):

- B: `fatal: path 'no/such/file.txt' does not exist in '5ced04cd…'`
- C: `fatal: path 'hello.txt' exists on disk, but not in 'f99de3bd…'` (freeze id unknown to fixture repo)
- D: `fatal: path 'corpus/evidence/round65/controls/no-such-blob-probe14.txt' does not exist in 'f99de3bd…'`

Full machine-readable evidence: `probe14-missing-blob-results.json` (this folder);
input receipts `A-positive.receipt`, `B-missing-path.receipt`, `C-missing-revision.receipt`,
`D-lane-missing.receipt`.

## Findings

1. Missing-blob is classified **invalid (exit 1)**, never usage/environment (exit 2) and
   never consistent: header regexes pass, the failure is isolated to the blob/digest bind.
2. Missing-path, missing-revision, and lane-freeze-repo missing-path are
   indistinguishable at the token level — all `RECEIPT_PIN=FAIL blob/digest`, exit 1.
   A battery case asserting that exact pair is robust across all three constructions.
3. Positive control confirms the fixture harness itself binds correctly (exit 0 PASS), so
   the B/C/D failures attribute to the missing blob, not harness error.
4. The reference never hashes working-tree bytes for these cases; the cat-file nonzero
   rc short-circuits before digest comparison.

## Tooling record

No installs or updates. Used preinstalled python 3.14.8 and git 2.56.0 only.

## Risks / notes for L1

- Token/exit pair for missing-blob (`1` / `RECEIPT_PIN=FAIL blob/digest`) is verified
  against the reference only; claims.md freezes exits but not per-case tokens.
- Case C's git stderr mentions the on-disk file; cosmetic, does not affect exit/token.
- Receipt bodies/digests for missing-blob cases are arbitrary by construction (no real
  blob exists); this mirrors adversarial receipt construction, not an honest receipt.
