# R75ExecB — independently derived matrix expectations (source: frozen r74 contract only)

Derivation basis, read before any run and without consulting `loader-matrix-v2.py`'s CASES table:
`corpus/evidence/round74/correction-count.py` at the frozen revision
(43a7a0db52c8aabdf32735f58e09610e05200e79) — its docstring check list C2-1..C2-7 plus the
`check()`, `anchored_count()`, `section()` semantics, and its `load()` loader path
(`git show rev:path` for content; `git diff --numstat base rev -- <three paths>` column 2
(deletions) for C2-6; `git diff --name-only base rev -- <two receipts>` for C2-7).

Contract recap relevant to derivation:
- C2-1: LOG.md anchored count of `## Round 72 correction entry` (exact line, rstrip) == 1.
- C2-2: section from the LAST such heading to next `## `/EOF contains 8426, 8435, exempt.
- C2-3: lesson anchored count of `## Correction — round-72 spot-check` == 1 AND its last-section
  contains V72-1, V72-2, 8426, 8435, 7f7ea19a, 6dd6c82.
- C2-4: SCORECARD anchored count of `## Round 72 correction note` == 1 AND last-section contains
  V72-1, V72-2.
- C2-5: the lesson last-section contains all three tree phrases ("measured at the landing tip
  7f7ea19a", "three at the verdicts tree 6dd6c82", "two recorded").
- C2-6: numstat deletions == 0 for all three protected paths base->rev.
- C2-7: neither receipt path changed base->rev.
Exit 0 iff all 7 pass; the counter always prints exactly 7 CHECK lines plus a
`C2=<PASS|FAIL> checks=<n>/7` line (output shape guaranteed by main()).

Base fixture consequence (from the contract alone): any fixture whose three protected files equal
the compliant base bytes and whose receipts are untouched passes 7/7 at rc 0; the base bytes in
the matrix's FILES satisfy every substring/count requirement (verified by reading the FILES dict
content in the matrix — file identity only, not its expected columns).

## Derived table (rc, failed set)

| case | mutation | derivation | expected rc | expected failed |
|---|---|---|---|---|
| unchanged | none | empty commit ⇒ numstat empty ⇒ C2-6 pass; receipts untouched ⇒ C2-7; compliant bytes pass C2-1..5 | 0 | {} |
| append-0 | LOG.md + "\nadditional evidence\n" | pure append: heading count stays 1 (appended line ≠ heading); last-section still holds 8426/8435/exempt ⇒ C2-1,2 pass; other files untouched ⇒ C2-3,4,5; numstat +2/−0 ⇒ C2-6 pass; receipts ⇒ C2-7 pass | 0 | {} |
| append-1 | lesson + "\nadditional evidence\n" | same: lesson count 1, names and tree phrases still in last-section ⇒ C2-3,5 pass; C2-6 +2/−0 | 0 | {} |
| append-2 | SCORECARD + "\nadditional evidence\n" | card count 1, V72-1/V72-2 present ⇒ C2-4; C2-6 +2/−0 | 0 | {} |
| delete-0 | LOG.md sentinel line removed | content checks unaffected (line precedes heading) ⇒ C2-1..5 pass; numstat +0/−1 ⇒ deleted=1 ⇒ C2-6 fail | 1 | {C2-6} |
| delete-1 | lesson sentinel line removed | same ⇒ only C2-6 fail | 1 | {C2-6} |
| delete-2 | SCORECARD sentinel line removed | same ⇒ only C2-6 fail | 1 | {C2-6} |
| replace-equal | LOG.md "removable sentinel"→"replacement sentinel" (1 line → 1 line) | replaced line precedes heading; entry intact ⇒ C2-1..5 pass; numstat +1/−1 ⇒ deleted=1 ⇒ C2-6 fail | 1 | {C2-6} |
| receipt-change | receipt 1 + "\nadditional evidence\n" | protected files untouched ⇒ C2-1..6 pass; `diff --name-only` over receipts non-empty ⇒ C2-7 fail | 1 | {C2-7} |
| dup-log-heading | LOG.md + "\n## Round 72 correction entry\n" | anchored count = 2 ⇒ C2-1 fail; section() reads from the LAST heading, which is the appended final line ⇒ empty section ⇒ 8426/8435/exempt all missing ⇒ C2-2 fail; lesson/scorecard untouched ⇒ C2-3,4,5 pass; numstat pure append +2/−0 ⇒ C2-6 pass; receipts ⇒ C2-7 pass. NOT decidable from numstat (pure append). | 1 | {C2-1, C2-2} |
| dup-lesson-heading | lesson + "\n## Correction — round-72 spot-check\n" | count = 2 and empty last-section misses all six names ⇒ C2-3 fail; empty block misses all three tree phrases ⇒ C2-5 fail; others pass; pure append ⇒ C2-6 pass | 1 | {C2-3, C2-5} |
| dup-card-heading | SCORECARD + "\n## Round 72 correction note\n" | count = 2 and empty last-section misses V72-1/V72-2 ⇒ C2-4 fail; C2-5 reads the lesson block, still intact ⇒ pass; pure append ⇒ C2-6 pass | 1 | {C2-4} |

Additional output-shape expectations implied by the contract for every case: exactly 7 CHECK
lines, and the `C2=` summary line's PASS/FAIL token follows rc (all-pass ⇔ PASS). The matrix's
ok-predicate (rc match ∧ 7 checks ∧ failed-set match ∧ C2= token) is therefore fully determined
by the contract, not by matrix-internal choice.

## Flags

- Cases NOT derivable from the frozen contract: none — 12/12 derivable.
- Cases whose expectation is decided by the diff (observed run) alone: none. Every printed
  expected_rc/expected_failed equals the contract-derived value above, computed before running.
- Distinction kept explicit: five case verdicts (unchanged, append-*, delete-*, replace-equal,
  receipt-change) are also decidable by a diff-only COUNTER, but their EXPECTATIONS are
  contract-derived; the three dup-* verdicts are counter-decidable only from protected-file
  content. Expectation provenance and counter decidability are independent axes; both are clean.
