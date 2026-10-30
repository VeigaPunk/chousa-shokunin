# Probe16 — round65 receipt absolute-path probe (trailer)

Scoped result: isolated fixture probed the single surface of the `SHA256=` header path field
against the frozen reference `corpus/evidence/round65/controls/ref-receipt-pin.py`
(production `tools/receipt-pin.py` absent at freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd).

Outcome: **PROBE16_ABS=11/11 PASS** — every expectation independently derived from the frozen
round65 format in `corpus/evidence/round65/claims.md` (C1). Absolute paths are always exit 1
even when they name a real file whose content hashes to the declared digest (strongest case:
`abs-real-file`); `//x`, `./x`, `x/../y`, `x/`, empty path, and missing path field all exit 1;
canonical relative path with a wrong digest also exits 1, proving path acceptance alone never
passes a receipt. Positive control `valid-relative` exits 0 PASS.

Two findings recorded for L1:
1. Exit-2 taxonomy anchor: invalid `--revision` (uppercase) → exit 2 (argparse usage), but an
   unreadable receipt file → **exit 1** (`RECEIPT_PIN=FAIL [Errno 2] ...`), contradicting the
   reference docstring's "2 usage/environment"; in this reference exit 2 is usage-only. Frozen
   C1 cases never exercise it, so the 20/20 predicate is unaffected; decide before production
   scoring whether docstring or behavior is authoritative.
2. Error-class text (e.g. `digest header` vs `path` for a space-with-empty-path) is reference
   detail; only exit codes and the `RECEIPT_PIN=PASS` / `RECEIPT_PIN=FAIL ` tokens are frozen.

Evidence (receipts, driver, full run log): `.ufo/waves/round-65/w1/Probe16/`
(`report.md`, `probe16-abs-fixture.py`, `probe16-abs-results.txt`, `probe16-abs-cases/*.txt`).
No installs used (system python3 3.14.8 + git only). Scratch
`/fast/scratch/hyaku/chousa-r65/Probe16/` deleted after receipts were copied. No production
writes, no fleet/sibling writes, no network fetches, no git mutations in the lane (fixture
repo lived and died in scratch behind a toplevel assertion).

Seat return: notes/draft only — integration and C1 scoring remain with L1.
