# R79ExecC — structure-identity limit measurement (C1 limit, not a claim failure)

Seat: R79ExecC · Python 3.14.8 (/usr/bin/python3) · no tools installed, no network, no lane/fleet writes.
Matrix: `.ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py` (sha256 2614b116…06428db).

## Observed (battery scored the structure matrix)

- `python3 -B corpus/evidence/round79/matrix-battery-v6.py --matrix <matrix> --work <scratch>/bat-v6` → exit **0**; final line `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` (receipt line 165; `EXIT=0`). Receipt: `R79ExecC/receipt-v6-structure-matrix.txt`.
- Positives: `SUBJECT POSITIVE successor-counter ACCEPTED`, `ref-counter ACCEPTED`; every run `marks=12/12/PASS content=ok`.
- Forgers: all 11 `REJECTED`; `MATRIX RUN content=bad` count = 0.
- `python3 -B corpus/evidence/round78/matrix-battery-v5.py --matrix <matrix> --work <scratch>/bat-v5` → exit **0**, identical verdict line. Receipt: `R79ExecC/receipt-v5-structure-matrix.txt`.
- Answer: **yes, the structure channel is a full forgery of both batteries** (12 contract lines at full marks, exit 0), not a partial one. The recorded limit is confirmed by measurement.

## Mechanism (why it passes)

1. Decodes the v6 wrapper (`b85decode` + `marshal.loads`) or, for v5 text copies, parses and compiles; both paths produce a code-object digest.
2. Canonicalises: drops unrecognised module-level `LOAD_CONST int`/`IMPORT_NAME` + `STORE_NAME` pairs whose name occurs once (the v5/v6 salt), renames every identifier to `vN` in first-use order.
3. Table of 13 digests built from `compile()` of the committed subjects (13 distinct, no collision). Positive identity → prints the frozen 12 `CASE` cells and `LOADER_MATRIX=12/12 MATRIX=PASS`, exit 0; any other identity → `0/12 FAIL`, exit 1.

It is an identity lookup, not a counter evaluation: a one-integer semantic change to `correction-count.py` (`+7`) scores `LOADER_MATRIX=0/12 MATRIX=FAIL`, rc=1 (`R79ExecC/control-semantic-altered-subject.txt`). The battery cannot distinguish this from a real evaluator because its subjects are fixed committed identities. Consistent with the v6 docstring Limits clause.

## Self-tests (receipts in wave folder)

- Probe copies, 13/13 (`selftest-probe-copies.txt`): the 2 positives → rc 0, the 11 forgers → rc 1.
- Comment-only append (`control-altered-subject.txt`) → rc 0: bytecode-identical, expected, not a finding.

Canonicaliser defects found and fixed while building (for the record): regex class lacked `{}` (payload truncation at `}`); PEP 649 `__annotate__` string keys carry renamed parameter names; `MAKE_CELL` order follows renamed cellvar sort order. None is a battery defect.

Limit to keep open: the battery's identity legs are textual/structural only against committed bytes; a matrix that embeds the committed digests and the frozen contract scores full marks on both v5 and v6.

Frozen artifacts untouched. Scratch `/fast/scratch/hyaku/chousa-r79/R79ExecC/` deleted at close.
