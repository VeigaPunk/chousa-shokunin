# Probe18 — round65 chousa, receipt-pin no-separator probe

Seat: Probe18 (leaf). Round: 65 chousa. Freeze: f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd.
Lane root: /home/vgpnk/Projects/shokunin/chousa-shokunin. Date: 2026-10-30.
Scope: one surface only — a receipt with **no empty separator line** between the
header block and the output body, against the frozen reference
`corpus/evidence/round65/controls/ref-receipt-pin.py`. No full battery run.

## Preconditions (read-only checks)

- Production target `tools/receipt-pin.py`: **absent at the freeze commit**
  (`git -C <lane> cat-file -e f99de3bd...:tools/receipt-pin.py` → does not exist).
  Seat made no production writes.
- Freeze commit `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` verified present in lane repo
  (`git -C` rev-parse).
- One live scratch clone of the lane at the freeze used as `--root`
  (`/fast/scratch/hyaku/chousa-r65/Probe18/lane`, HEAD == freeze; deleted after evidence copy).
- Interpreter `python3` 3.14; no tools installed or updated this seat.

## Independent derivation from the frozen format (claims.md C1)

Format rules read directly from the frozen claims text (not from reference code):
`REVISION=<full lowercase 40 hex>` (must equal caller `--revision`),
`EXIT=<decimal 0..255>`, `SHA256=<full lowercase 64 hex> <canonical relative POSIX path>`,
**empty separator**, nonempty output. Verdicts: 0 consistent, 1 invalid/malformed,
2 usage/environment. A receipt whose fourth line is not empty violates the frozen
format on its face, independently of any implementation: with all argv valid the
receipt is malformed → exit **1** (invalid class), stdout `RECEIPT_PIN=FAIL`.

Independent oracle `probe18-derive.py` (scratch; shares no code with the reference)
evaluated the frozen rules per receipt:

    v0-valid-separator: DERIVED: consistent -> EXPECTED_EXIT=0 EXPECTED_STDOUT_PREFIX="RECEIPT_PIN=PASS" PROBLEMS=none
    v1-nosep-2body:     DERIVED: malformed   -> EXPECTED_EXIT=1 EXPECTED_STDOUT_PREFIX="RECEIPT_PIN=FAIL"  PROBLEMS=separator-line-not-empty
    v2-nosep-1body:     DERIVED: malformed   -> EXPECTED_EXIT=1 EXPECTED_STDOUT_PREFIX="RECEIPT_PIN=FAIL"  PROBLEMS=fewer-than-5-lines,separator-line-not-empty

## Fixtures

All fields other than the separator are fully valid, so the separator defect is the
only variable under test. Digest `b9dbca57f4ca1af351459410e1fb7793668fe647c20278d26765b85485ab2fc5`
= sha256 of `git -C <clone> cat-file blob f99de3bd...:corpus/evidence/round65/claims.md`
(frozen blob; no working-tree hashing). `--revision f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.

- `v0-valid-separator.receipt` — control WITH blank separator, 2-line body (harness sanity).
- `v1-nosep-2body.receipt` — no separator, 2-line body (isolates the separator rule; len=5).
- `v2-nosep-1body.receipt` — no separator, 1-line body (len=4, conflated short-form variant).

Exact bytes of each receipt are recorded with `cat -A` in `probe18-nosep-run.log`
(v1 line 4 is `first output line$`, not `$` — separator provably absent).

## Reference runs (argv preserved verbatim in run log)

    python3 corpus/evidence/round65/controls/ref-receipt-pin.py \
        --receipt <scratch>/<case>.receipt --root <scratch>/lane \
        --revision f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd

Observed:

| case | exit | stdout | stderr |
|---|---|---|---|
| v0-valid-separator | 0 | `RECEIPT_PIN=PASS` | empty |
| v1-nosep-2body | 1 | `RECEIPT_PIN=FAIL header/body` | empty |
| v2-nosep-1body | 1 | `RECEIPT_PIN=FAIL header/body` | empty |

## Comparison

Observed reference behavior matches the independently derived expectation on every
case: exit codes exact (0/1/1), FAIL-class token on the no-separator surface, stderr
empty, no exit-2 usage/environment involvement. The control (v0) proves the harness
digest/path/revision are sound, so the v1/v2 failures are attributable solely to the
missing separator. The exact diagnostic suffix `header/body` is reference output text,
not a frozen-format requirement; the frozen contract fixes exit 1 + `RECEIPT_PIN=FAIL`,
which is exactly what was observed.

## Evidence (this folder)

- `probe18-nosep-fixture.sh` — fixture driver (receipt construction + reference runs).
- `probe18-nosep-run.log` — full run log: exact receipt bytes (`cat -A`), argv, exit, stdout, stderr per case.
- `v0-valid-separator.receipt`, `v1-nosep-2body.receipt`, `v2-nosep-1body.receipt` — exact fixture bytes.
- `v*.stdout` / `v*.stderr` — raw per-case captures.
- `probe18-derive.py` / `probe18-derive.out` — independent frozen-format oracle and its derivations.

## Risks / limits

- Only the no-separator surface probed per seat scope (plus one paired valid control);
  the remaining 19 malformed/usage surfaces are L1's integration battery, not run here.
- The frozen format does not pin the exact FAIL message suffix; only the exit code and
  `RECEIPT_PIN=FAIL` class are frozen-contract assertions. Reported suffix is observed.
- Scratch `/fast/scratch/hyaku/chousa-r65/Probe18` deleted after evidence copy; TMPDIR
  confined to scratch; no /tmp evidence; no production or fleet-root writes.
