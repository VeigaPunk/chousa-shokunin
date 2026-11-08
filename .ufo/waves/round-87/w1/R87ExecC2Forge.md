# R87ExecC2Forge — C2 `C2-CURATION-R87` calibration counter forgery attempt (round 87, w1)

Seat: `R87ExecC2Forge` (leaf executor; the single assigned move is the C2 forge probe).
Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Subject tree: `git archive e6e920a4e6988287c31e89b3e920a118b569ae52`
(baseline, egress, freeze and landing revs taken from the assignment; counter bytes are the archive's own `corpus/evidence/round87/curation-r87.py`).
All probes ran on mirrors under `/fast/scratch/hyaku/chousa-r87/R87ExecC2Forge/mirrors/` built exactly as
`corpus/evidence/round87/curation-r87-controls.py:mirror()` builds them (real copies of `corpus/SOURCES.md` + the two routed
entries, symlinks for `corpus/captures` and `corpus/evidence/round57`). No lane file, sibling repo, fleet-root file or
`/home/vgpnk/Projects/shokunin/scripts` path was written; `git -C chousa-shokunin status --short -- corpus/` shows only
pre-existing untracked `after/`/`census-*` ephemera (not mine). Every receipt below was copied to
`.ufo/waves/round-87/w1/R87ExecC2Forge/receipts/` before the scratch tree was deleted.

Baseline (unmodified tree): `python3 -B "$TREE/corpus/evidence/round87/curation-r87.py" --root "$TREE"` exits 0 printing
`QUOTES_LOCATED=20/20 WARRANT_OK=17/17 … LEGS=7/7 CURATION_R87=PASS` (receipts/baseline.txt) — the frozen predicate holds at the
landing rev. The shipped `curation-r87-controls.py` battery was re-run for the record: `FORGERY_REFUSED=4/4 R86_ACCEPTED_FORGERY=4/4
CONTROLS=PASS` (receipts/receipt-controls-own-run.txt). Each finding names command → receipt → observed line + exit.

## A. Floors (13 / 7) — ONE ACCEPTED FORGERY (against C2's K3/K4)

Counter logic probed (`curation-r87.py:164-199`): a Located-quote row counts when `norm(quote) in cap`; the FLOOR leg requires
`located >= floor AND located == total` per entry; the WARRANT leg requires the row's named qid to resolve and some distinctive
(≥5-char, non-stopword) word to be shared with the quote.

- **A1-junk-add** (ADD only, no deletion): insert `| Q99 | S023 | "Specification" |` ("Specification" is verbatim in the S023
  capture `f5545a194c06ab421875b047.txt`) after the r84 quote-table header. Command → receipts/receipt-A1-junk-add.txt:
  `QUOTES_LOCATED=21/21 … Q_FLOORS=search-…-r84.md=14/14 floor13 … LEGS=7/7 CURATION_R87=PASS`, exit 0. **ACCEPTED — but
  benign as a shape**: an extra verbatim row is still a located quote (nothing real was lost), so the floor holding is correct.
- **A1b-delete-plus-junk** (delete real `Q11`, add junk `Q99 "Specification"` to restore the count): receipts/receipt-A1b-delete-plus-junk.txt
  prints `QUOTES_LOCATED=20/20 Q_FLOORS=…13/13… WARRANT_OK=16/17 LEG_FAIL WARRANT 16/17 CURATION_R87=FAIL`, exit 1. The `WARRANT_UNLINKED`
  line names `row=Recording when a resource is valid warrant=Q11 (S023) resolved=0/1`. **REFUSED, and note the mechanism: the FLOOR leg
  alone is NOT sufficient — FLOOR passed while WARRANT caught the hole**, because the orphaned qid no longer resolves.
- **A1c-strong-junk — the K3/K4 FORGERY (ACCEPTED)**: delete real `Q11` row; add `| Q99 | S023 | "validity" |` ("validity" is verbatim in
  the S023 capture — verified `norm("validity") in norm(cap) == True`); repoint the decision row's warrant `Q11 → Q99`. Receipts/receipt-A1c-strong-junk.txt:
  `QUOTES_LOCATED=20/20 Q_FLOORS=…13/13 floor13… WARRANT_OK=17/17 … LEGS=7/7 CURATION_R87=PASS`, exit 0. A 1-word junk quote, indistinguishable
  from evidence to every leg, fully replaces the real multi-word quote `Q11 "Date (often a range) of validity of a resource."`. The real quote's
  content (that the date is a validity range) is lost but no leg detects it: count restored (FLOOR), qid resolves (WARRANT-resolved), the
  distinctive word "validity" is shared (WARRANT-shares), and the quote is verbatim (K2 wording is met — `norm(quote) in cap`). The forged entry
  is at receipts/forged-entry/search-transparency-reporting-r84.A1c.md. This is precisely "a forgery the frozen predicate accepts" → fires K3.
- **A1d-truncate-to-junkword** (same idea, no qid change): replace `Q11`'s quote with the bare verbatim word `"range"` (also verbatim in the S023
  capture and a distinctive word of the row). receipts/receipt-A1d-truncate-to-junkword.txt: `QUOTES_LOCATED=20/20 … WARRANT_OK=17/17 …
  LEGS=7/7 CURATION_R87=PASS`, exit 0. **ACCEPTED (K3/K4)** — so even a per-row quote length/content floor does not exist: truncating a real row
  to a verbatim single-word prefix that keeps one distinctive word passes everything. (For contrast, truncating `Q13` to `"Date on which"` FAILS
  on DEF_CITED+WARRANT — receipts/receipt-A2-truncate-Q13.txt — because `Q13` is the `MODIFIED_DEF` quote; and truncating `Q11` to `"Date"` fails
  on WARRANT — receipts/receipt-A2b-truncate-Q11.txt — because "date" is a stopword-class word not shared. The counter is only accidentally safe
  wherever the distinctive word happens to be the row's whole distinction.)
- **A3-delete+old-add-count** (delete r85 `Q1`, add `Q99 "Provenance"` verbatim in the S215 capture `6e48bcc4a04d13b7b3ebb68e`): prints
  `QUOTES_LOCATED=20/20 WARRANT_OK=16/17 LEG_FAIL WARRANT … CURATION_R87=FAIL`, exit 1 (receipts/receipt-A3-delete+old-add-count.txt) — refused only
  via the dangling warrant, as in A1b; without the warrant repoint the floor is fully restored by junk.

## B. Warrant leg — HOLDS (no accepted forgery found)

- **B1-dup-qid** (`Q1 → Q1, Q1` in one warrant): `WARRANT_OK=17/17 … CURATION_R87=PASS`, exit 0 (receipts/receipt-B1-dup-qid.txt). **ACCEPTED — benign.**
  Both copies resolve to the same located quote and the share test is `any(...)` over resolved qids, so a duplicated qid is a no-op. No evasion value.
- **B1b-second-qid-unshared** (`Q1 → Q1, Q10`): `WARRANT_OK=17/17 … PASS`, exit 0 (receipts/receipt-B1b-second-qid-unshared.txt). **ACCEPTED — benign**: the
  second qid shares nothing distinctive, but the test is per-row `any`, not per-qid — a padding qid alongside a good warrant is not detected. Cosmetic only.
- **B2-repoint-Q13→Q10** (`Q13 → Q10`, same S-id, same entry): `WARRANT_OK=16/17 LEG_FAIL WARRANT 16/17 CURATION_R87=FAIL`, exit 1 (receipts/receipt-B2-repoint-Q13-to-Q10.txt).
  **REFUSED.** Verified by hand: row 9's distinctive set is `{changed}`; `Q10` shares none of it (repair to the E6 shape — the exact round-86 E6 move).
- **B2-stopword-only** (row 9's Do/Never replaced with words that are ALL stopword-class, e.g. `record`, which `distinctive()` excludes and which is a
  ≥5-char word appearing in the quote): `WARRANT_OK=16/17 LEG_FAIL WARRANT 16/17 CURATION_R87=FAIL`, exit 1 (receipts/receipt-B2-stopword-only.txt).
  **REFUSED** — the leg does NOT credit stopword-length sharing, as designed. No "share only a stopword word" bypass exists (a row whose distinctive set is
  empty can never satisfy `shares`).
- **B3-warrant-cross-Sid** (row "Recording when a resource changed", `Q13 (S023) → Q6 (S018)`, different S-id, same entry): `WARRANT_OK=16/17 LEG_FAIL WARRANT
  CURATION_R87=FAIL`, exit 1 (receipts/receipt-B3-warrant-cross-Sid.txt). **REFUSED.** **B3b-cross-Sid-entryB** (r85 row "Recording when content was last reviewed",
  `Q7 (S031) → Q1 (S215)`): same, exit 1 (receipts/receipt-B3b-cross-Sid-entryB.txt). The leg does not check S-id agreement at all, but the distinctive-word
  requirement kills these cross-S repoints anyway; no cross-S-id acceptance was found.

## C. Teaches leg — HOLDS both ways (no over-fire, no under-fire on the probed shapes)

- **C1-teaches-term-in-capture** (S023 `teaches` set to `"modified is separate from publication"`: contrast phrase + `modified`/`publication` both PRESENT
  in the S023 capture — verified counts `publication 1, published 4, modified 4, created 8, issued 5, modification 0`): prints
  `TEACHES_CHECKED=2 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7 CURATION_R87=PASS`, exit 0 (receipts/receipt-C1-teaches-term-in-capture.txt).
  **Leg passes — no over-fire.** The contrast row is checked and correctly NOT flagged because the term is readable in its own capture.
- **C2-teaches-term-absent-live** (S031 `teaches`: `no comparison to other date properties claimed → separate from modification dates`; S031 is mined and NOT
  superseded by anyone; `modification`/`publication`/`modified` etc. are all absent from the S031 capture — verified): prints
  `TEACHES_CHECKED=2 TEACHES_FLAGGED=2 TEACHES_UNRESOLVED=1 LEG_FAIL TEACHES … CURATION_R87=FAIL`, exit 1 (receipts/receipt-C2-teaches-term-absent-live.txt).
  **Leg fires — no under-fire.** The shared K4 duty ("the leg requires at least one flagged row") is trivially satisfiable by the live S024 instance.

## D. Supersession leg — HOLDS on the probed shapes

- **D1-rejected-superseder-mined-target** (S031 status `mined → rejected`, S024 status `queued → mined`, so the superseding row is `rejected` while its
  superseded target is `mined`): prints `SUPERSEDED_LIVE=1 LEG_FAIL SUPERSEDED S024 mined while S031 supersedes it CURATION_R87=FAIL`, exit 1
  (receipts/receipt-D1-rejected-superseder-mined-target.txt). **REFUSED.** The frozen registry already contains a rejected→rejected edge (S202→S198) which
  the leg correctly does not flag (neither side mined).
- **D2-rejected-superseder-queued-target** (S031 → `rejected`, S024 stays `queued`): `SUPERSEDED_LIVE=0 … CURATION_R87=PASS`, exit 0 (receipts/receipt-D2-rejected-superseder-queued-target.txt).
  **PASS — correct**: the leg's condition is `target mined AND superseder not mined`; a queued target is not a live citation, so no fire is correct.
- **D-extra-free-text** (`supersedes S024 —` → `superseded by S024 —`, free form): prints `TEACHES_UNRESOLVED=1 LEG_FAIL TEACHES … CURATION_R87=FAIL`,
  exit 1 (receipts/receipt-D-extra-free-text.txt). The counter keys only on the exact `supersedes (S\d+) —` prefix (`curation-r87.py:139`), so free-text
  supersession is **not** recognised and the row becomes unresolved → refused. Fail-closed. (Asymmetric note: S202's `REJECTED: …` teach line also starts with
  `REJECTED:` rather than the prefix; it is not a supersession edge and the counter treats it as such — same fail-closed direction.)

## Summary

Fired (accepted forgeries):
- **F1 (A1c)**: 1-word junk quote `Q99 "validity"` (verbatim in the S023 capture) replaces real `Q11`, warrant cell rewired to `Q99` → `CURATION_R87=PASS` (exit 0).
  Pins to the claim's K3 ("a control forgery the round-87 counter should refuse is still accepted" — the junk-quote restoration class) and K4's "dead detector"
  analogue for floors (a count floor with no per-quote minimum is satisfied by a 1-word verbatim string).
- **F2 (A1d)**: truncating real `Q11`'s quote in place to the bare verbatim word `"range"` → `CURATION_R87=PASS` (exit 0). Same class as F1, qid unchanged.

Refused (legs hold): B2 (Q13→Q10, the E6 shape), B2-stopword-only, B3/B3b (cross-S-id repoints), A2/A2b truncations that remove the distinctive/modified-def
content, A1b/A3 (dangling warrant), C2 (live absent-term teaches), D1 (rejected superseder over mined target), D-extra.
Benign accepts (no evasion): A1-junk-add (extra row), B1 dup qid, B1b padding qid, C1 (correct non-fire), D2 (correct non-fire).

Why F1/F2 work: `QUOTES_LOCATED` is a verbatim-substring test and the FLOOR leg checks only `located >= floor AND located == total`; neither the floor nor the
warrant leg imposes a minimum quote length or full-row word coverage. Any committed capture word that is also a distinctive word of the row satisfies both.
The pre-freeze plan's repair 6 claims per-entry floors close E5b/E5c2 — they do (receipts/receipt-F-delete-Q13.txt also shows FLOOR catching a bare deletion) —
but the routed defect 4 forgery class ("a deleted or truncated quote table fails", claims.md C2 sentence) survives in truncated-junk form. A repair would need a
per-quote minimum (e.g. ≥N words, or the quote must carry ≥2 distinctive words of its row) — reported, not implemented (leaf member, no production edits).

Tooling: no installs (operator directive read at `/home/vgpnk/.omp/agent/RULES.md`; `python3`/`git`/`tar` already present; pacman guard honoured — nothing installed).
Scratch: `/fast/scratch/hyaku/chousa-r87/R87ExecC2Forge` was deleted after copying receipts (verified removed before yield).

VERDICT: R87ExecC2Forge C2 fired — F1 (A1c 1-word junk quote restoring floor+warrant → PASS, exit 0) and F2 (A1d truncation to bare verbatim "range" → PASS, exit 0) are accepted forgeries the frozen C2 predicate should refuse.
