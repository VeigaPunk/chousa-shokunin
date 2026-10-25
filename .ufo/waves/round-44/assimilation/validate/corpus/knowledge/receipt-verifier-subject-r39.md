# receipt-verifier-subject-r39

source: corpus/evidence/round39/claims.md (C2); own-work (the r38 verifier it extends is `corpus/evidence/round38/verify-receipts.py`)
verified-at: 2026-10-24 (receipts `corpus/evidence/round39/receipts/c2-after-s39101.json`, `c2-after-s39121.json`)
recheck: re-run `python3 corpus/evidence/round39/c2-count.py --gate tools/research-gate.sh --seed N --receipt F` and `verify-receipts.py --receipt F --gate tools/research-gate.sh --counter corpus/evidence/round39/c2-count.py`

Round-39 note: receipts bind WHICH verifier and WHICH subject-counter bytes
judged a run — the round-38 Erratum 2/11 carried debt, demonstrated live
twice, closed for this receipt family.

## Mechanism

Both r39 counters embed `verifier_sha256` (the digest of
`round39/verify-receipts.py`) in every receipt; c2-family receipts
additionally embed `subject_counter` + `subject_counter_sha256` (the counter
the c2 run measured). `verify-receipts.py` re-derives:

- `verifier_sha256 == sha256(its own bytes)` — else
  `VERIFY-FAIL: verifier-sha256-mismatch`. A replaced (weakened or doctored)
  verifier copy cannot silently re-adjudicate old receipts: its bytes hash
  differently and this fires before any other check.
- family c2 only: the named `subject_counter` path must resolve
  (`subject-counter-unreadable` otherwise) and its bytes must equal
  `subject_counter_sha256` (`subject-counter-sha256-mismatch` otherwise).

Family-specific required sets live in the verifier's `FAMILIES` table, so
receipts from earlier generations fail closed as `missing-field …` or
`predicate-mismatch` — each round's receipts stay verified by that round's
own committed verifier.

## Measured

- After (landed gate): `RECEIPT_BINDING_MATCH=8/8` on seeds 39101/39121;
  both receipts `VERIFY: ok`; the c2 receipt's `verifier_sha256` and
  `subject_counter_sha256` equal the committed file digests (`1b6e0de6…`,
  `91618e91…`).
- `verifier-subject-rebind` cell, live: honest subject receipt verifies;
  a census-weakened verifier copy refuses `verifier-sha256-mismatch`; a c2
  receipt re-pointed at a doctored subject copy (path moved, honest digest
  kept, re-sealed) refuses `subject-counter-sha256-mismatch`.
- `legacy-receipt-refused` cell, live: the committed r38 receipt
  (`corpus/evidence/round38/receipts/c1-after-s38001.json`) refuses
  `predicate-mismatch` (generation binding, verified against the r38
  expectation bytes); an r39 receipt with the verifier binding stripped
  refuses `missing-field verifier_sha256`.
- Before (the control): the r38 receipts carry neither binding, and the r38
  verifier accepted five of six weakened-verifier mutants (r38 Erratum 11) —
  the debt this round closes.

## Limits (named, per claims.md §Limits)

Integrity and self-consistency against committed bytes, NOT authorship: a
fabricator holding the public hashes who reproduces honest observations can
write a self-consistent receipt (the r37 F2 residual, narrowed not closed).
Re-pointing a c2 receipt WITH a re-derived subject digest is a new honest
receipt, not a forgery of an old one. The `_contains` annotations stay
producer-side. Path identity binds the receipt's NAMED path, not the
CLI-supplied `--counter` (family detection still keys on the basename).

## Construction note (the counter caught its own drafts)

The first construction run of this counter scored 6/8 and both failures were
real drafting defects the cells existed to catch: the verifier-weakening
doctor deleted a `return` line and left an empty if-body (syntax crash,
stderr-only — the observable was empty stdout, not a named refusal), and the
doctored-subject fixture replaced a string with its implicit-concatenation
twin (identical bytes, so the swap cell verified vacuously). Both fixes are
in the landed counter; the failure receipt from the first run was discarded
(not committed) and the class is recorded here.
