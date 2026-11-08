# R88ExecC2Forge — C2 curation counter forgery report

Seat: R88ExecC2Forge (labrat, leaf). Counter: `corpus/evidence/round88/curation-r88.py` at
`4ea9d008abfd2e09cb51649a42678a78f52ac530`. Tree built via `git archive` into scratch; mirrors
copy the registry + `search-transparency-reporting-r84.md` + `provenance-recording-r85.md` as real
copies and `corpus/captures` + `corpus/evidence/round57` as symlinks (the `curation-r88-controls.py`
discipline), never writing in the lane. No tool was installed (none needed; pacman paused host-wide,
no network used — all checks read committed bytes).

Baseline (unmodified tree): `QUOTES_LOCATED=20/20 WARRANT_OK=17/17 TEACHES_FLAGGED=1
TEACHES_UNRESOLVED=0 LEGS=7/7 CURATION_R88=PASS`, exit 0 — the frozen predicate holds at the freeze
(see `receipts/baseline.txt`).

## Findings — forgeries ACCEPTED (against C2's K3/K4 shape)

1. **(b) 8-token verbatim substitution passes.** Q1 of r84 replaced by the verbatim substring
   "Specify all databases, registers, websites, organisations, reference lists" (8 tokens, verbatim
   in the S214 capture, still sharing distinctive terms with its row): `CURATION_R88=PASS`, exit 0,
   `WARRANT_OK=17/17 QUOTES_LOCATED=20/20` (`receipts/run2b.log`).
2. **(b) 8-token verbatim substitution passes on Q2.** "reference lists and other sources searched
   or consulted" (8 tokens, verbatim in S214, shares `consulted` with its row): PASS, exit 0
   (`receipts/run2b.log`).
3. **(c2) Same qid cited twice on one warrant cell passes.** `Q1, Q1 (S215)` on "Naming what a
   resource derives from": `CURATION_R88=PASS`, exit 0, `WARRANT_OK=17/17` (`receipts/run1.log`).
   The warrant leg's qid list is never checked for duplicates.
4. **(a4) Swapping the quote texts under Q10 and Q11 passes.** Both rows keep their qids and
   7+-token verbatim quotes (Q10 now carries Q11's validity text, Q11 now carries Q10's
   recommended-practice text): `CURATION_R88=PASS`, exit 0 (`receipts/run2b.log`). The qid-set pin
   guards label identity, not quote content — the two rows' contents are interchanged while every
   leg stays green.
5. **(a2) Reordering the qid quote rows passes** (Q10/Q13 lines swapped): `PASS`, exit 0
   (`receipts/run1.log`). Benign as content, but it confirms the pin is set-based and row order is
   unchecked — consistent with the sentence's wording ("per-entry qid set"), reported, not claimed away.

All five are ACCEPTED forgeries: tree shape changed, checks green. The token floor bites only below
7 tokens — a 6-token verbatim quote fails FLOOR (`receipts/run2b.log` b3); ≥7-token substitutions are
indistinguishable from genuine rows, and the qid set + warrant share are satisfied by the splices.

## Probes the counter refused (hits, not findings)

- (a1) Rename Q10→Q99 + new Q10 with a different quote: refused (`LEG_FAIL FLOOR`, 14/14 — count guard).
- (a3) caseG restore (delete Q10, add Q14 duplicating Q13): refused (`LEG_FAIL FLOOR`, set mismatch).
- (b4) 8-token verbatim quote sharing no distinctive term with its row (Q5): refused
  (`LEG_FAIL WARRANT 16/17`) — isolation proof that the warrant share, not the floor, rejects it.
- (c1) Padding qid Q3 added to the repaired "Q1" row: refused (`LEG_FAIL WARRANT 16/17`, B1b shape).
- (c1b) Stopword-only share (Q7's `which` cited on the "Recording when a resource changed" row):
  refused (`LEG_FAIL WARRANT`) — a 5-letter stopword cannot pass `distinctive()`, verified by hand
  (intersection empty) and by run.
- (d1) S031 status `mined`→`queued`: refused (`LEG_FAIL TEACHES ... unresolved=1`).
- (d2) S031 teaches gains `separate from publication dates` (term absent from its capture): refused
  (`LEG_FAIL TEACHES`), but via the main loop (`S031 UNRESOLVED`, `sup_unresolved=0`), not the
  `teaches_sup_unresolved` check. Isolating it — a fresh mined superseder S099 behind S031 so the
  main loop resolves S031 — still ends with `sup_unresolved=0` and refusal arriving through the
  main-loop path instead (`receipts/run3.log` d2c). The counter as committed never populated
  `teaches_sup_unresolved` in any run of mine; whether any tree can set it is untested (see risk).

## Risks / blockers

- The `teaches_sup_unresolved` branch (claims.md C2: "the superseding row's own teaches must read in
  its own capture") was never observed populated; every d-shaped refusal arrived via the main
  teaches loop. The claim-alignment of that branch remains unverified by this seat.
- Findings 3 and 4 are C2 K4 overlaps (legs green on malformed evidence, not specifically K3's five
  round-87 forgeries); severity is L1's call. Findings 1–2 are expected boundary behaviour of a
  `MIN_TOKENS = 7` floor and are reported as calibration limits, not as K3 kills.
- Scratch deleted; all trees were under `/fast/scratch/hyaku/chousa-r88/R88ExecC2Forge/` and were
  removed after their logs were copied to `receipts/`.

VERDICT: R88ExecC2Forge C2 fired — one forged tree shape per (a)(c)(a4) class passed the counter green (duplicate-qid cite, quote-content swap under pinned qids, row reorder), and ≥7-token verbatim substitutions pass the floor by design, while every leg held on the harmful shapes.
