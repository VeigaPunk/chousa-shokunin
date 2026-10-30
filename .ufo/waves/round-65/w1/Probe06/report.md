# Probe06 — round65 short-revision receipt fixture

Date: 2026-10-30. Seat: Probe06 (leaf, chousa round65, freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd).
Surface: **short-revision handling of the R65-C1 receipt-pin reference, one surface only.**
Reference exercised: `corpus/evidence/round65/controls/ref-receipt-pin.py` (production `tools/receipt-pin.py` absent at probe time — verified `ls` no-such-file).
No installs this seat (git 2.56.0, python 3.14.8 preinstalled; no pacman/uv/npm transactions).

## Independent expectation (derived from frozen claims.md C1, not from reference source)

Frozen format: `REVISION` is exactly full lowercase 40 hex; revision must equal caller-supplied `--revision`; exits: 0 consistent / 1 invalid / 2 usage-environment. Therefore:

- A short `--revision` argument is outside the valid input domain → usage/environment → **exit 2** (regardless of whether the prefix resolves to a real object).
- A receipt whose `REVISION=` line carries a short prefix while `--revision` is the full 40-hex id can never satisfy the equality+format rule → **exit 1** (inconsistent receipt, not usage — the receipt itself is malformed relative to the format).
- Full revision on both sides with a correctly bound blob digest → **exit 0** (anchor).

## Fixture (built in scratch, since deleted)

- Fresh repo `/fast/scratch/hyaku/chousa-r65/Probe06/fixture/repo`, one commit `ac3407da7e1006fa29c49d9175d49dc6fc8ebb7c` adding `artifact.txt`; `git rev-parse --show-toplevel` asserted == fixture dir before mutations.
- Blob digest bound exactly as the reference binds it: `sha256(git cat-file blob ac3407…:artifact.txt)` = `1691be3eb31918531de22a709b79e10d16527cd2a820223e74dda2940dae30f7`.
- Receipts otherwise well-formed (EXIT=0, digest+`artifact.txt`, blank separator, nonempty body) so the short-revision axis is isolated.

## Results — 5/5 observed == independently derived

| case | argv `--revision` | receipt REVISION= | expected | observed | verdict |
|---|---|---|---|---|---|
| s1-arg-short12 | `ac3407da7e10` (12) | full | 2 usage | 2 (argparse usage on stderr) | match |
| s2-receipt-short12 | full | `ac3407da7e10` (12) | 1 invalid | 1, stdout `RECEIPT_PIN=FAIL header/body` | match |
| s3-arg-short39 | 39-hex prefix | full | 2 usage | 2 | match |
| s4-anchor-full | full | full | 0 | 0, stdout `RECEIPT_PIN=PASS` | match |
| s5-arg-short-nonexistent | `ffffffffffff` (12, no such object) | full | 2 usage | 2 | match |

Full transcripts with exact argv/stdout/stderr: `transcript.json`; per-case receipt files alongside this report.

## Findings

1. Reference rejects short revisions on both input surfaces with the frozen exit taxonomy: argument-side short revision → exit 2 (usage/environment, argparse `p.error`, message on stderr, empty stdout); receipt-header short revision → exit 1 (`RECEIPT_PIN=FAIL header/body` on stdout). The 39-hex boundary confirms the fullmatch is exactly 40, not "≥ some prefix length".
2. s5 shows the length/type check precedes any git lookup: a short prefix of a nonexistent object still exits 2 via the same usage path — no git invocation is reached for short revisions (read-only Git preserved; no fetch, no network).
3. Anchor s4 confirms the fixture's digest binding is faithful (`PASS` on the happy path), so the four rejections are attributable to the revision axis alone.
4. No discrepancy between independent derivation and reference behavior on this surface. Nothing here extends or narrows the frozen C1 claim (interface/consistency only, not execution authentication); numeric score untouched.

## Notes / risks

- One live fixture repo (not a clone); scratch `/fast/scratch/hyaku/chousa-r65/Probe06/` deleted after receipts were copied here. No /tmp evidence. No production, fleet-root, or sibling writes; no git/jj mutations outside the scratch fixture.
- argv and output preserved verbatim in `transcript.json`; reference is unchanged.
