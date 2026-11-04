# Round 74 lesson draft — author-lane scribe

Date: 2026-11-04. Assignment freeze: `1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb`. Integration owner: ChousaR74. Draft only; no independent admission or promotion judgment.

Axes: operability (C1); source discernment and mistake prevention support that claim, not an additional calibration improvement.

## Gate

Opened local sources on 2026-11-04; no network or external source adoption.

- **Admit S182, own-work B**, narrowly as grounds for the loader repair and real-public-path controls. Source: `corpus/lessons/round-73-verifier-spotcheck.md`, section 5 item 1, line 67; registry anchor: `8a28732b3c1591b52449a982849b758cda6f4c45`. Located quote (≤25 words): “Before any successor calibration freeze, exercise a real committed append and a real deletion through `load()`”. Reason: the closure identifies both reversed outcomes and the missing adapter coverage. Reopening `corpus/evidence/round73/c2-count.py:125–134,162–179` supports that narrow diagnosis: line 131 reads `parts[0]`; the selftest directly calls `check()`. **Flip/reconsider:** if revision-bound public-path evidence refutes the diagnosed append/deletion reversal, withdraw this source as grounds for that diagnosis; do not extend its B tier to arbitrary correction prose or general counter soundness.
- **Reject S183, own-work C**, specifically helper-only selftest as evidence of Git loader correctness. Source: `corpus/evidence/round73/c2-count.py:163`, with context at lines 125–134 and 162–179; registry anchor: the same revision. Located quote (≤25 words): `base = check({k: v for k, v in FIXTURE.items()}, {}, set())`. Reason: synthetic dictionaries bypass `load()`; line 157 injects a deletion count instead of obtaining it from Git, and line 173 again invokes `check()` directly. This tests helper behavior, not the adapter that reads numstat. **Flip:** independently expected public-CLI outcomes on real committed append/deletion fixtures, including required exits and failed check IDs. New successor evidence may satisfy that requirement; it does not make the unchanged historical helper-only selftest certify the old loader or retroactively admit r73.

Spot-check status: this is author-lane reopening only. A non-author judgment on the admit and reject is not supplied by this seat.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| helper-only selftest bypasses defective input adapter | S182, r73 closure §5 item 1 line 67; S183, original loader line 131 and selftest lines 157,163,173 | existing helper mutations test `check()` but never `load()`; a real committed-input positive/deletion control would expose the gap | preserve frozen r73 bytes and honest-stop; successor reads deletion column `parts[1]` and treats nonnumeric deletion cells as nonzero; require frozen nine-case public-CLI matrix and historical-landing conjunct; QUALITY 134 |

Source observation, not a new run: `corpus/evidence/round74/before-matrix.txt:3–59` records all three append rejections and all three deletion acceptances, ending `LOADER_MATRIX=3/9 C1=FAIL`; line 60 records `EXIT=1`. `positive-matrix.txt:2–12` records nine expected outcomes, `LOADER_MATRIX=9/9 C1=PASS`, `EXIT=0`. These prefreeze records are not this seat's execution evidence or the historical-landing conjunct.

Limits: the nine fixed cases do not establish substring semantic entailment, arbitrary-counter unforgeability, or the runtime behavior of a nonnumeric deletion cell. No historical r71/r72/r73 rejection, numeric score, host question, or promotion status changes.
