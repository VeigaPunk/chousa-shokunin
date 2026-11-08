# chousa — round 88: plan and amendments

L1 `ChousaR88`. Base `f484d94f` (round-87 landing + the non-author spot-check at `f484d94f`, whose four routed
defects are this round's input). The frozen claims are in `corpus/evidence/round88/claims.json` (machine form) and
`corpus/evidence/round88/claims.md` (prose); this file records the pre-freeze repairs and any post-freeze amendment.
A `narrowing` cell in `.ufo/waves/round-88/claim-falsification.tsv` resolves to a section here.

## Inputs — the four defects round 87's non-author check routed

`corpus/lessons/round-87-verifier-spotcheck.md` `## Routed defects` 1–4 (the closure's list; spot-check table agrees
on every sampled gate decision):

1. **`SCORECARD.md` round-87 header says the wave was 13 seats.** The committed evidence says 12 everywhere else
   (`w1-spec.json` items = 12, `w1-dispatch.json` `counts.spawn=12`, `w1-results.json` results = 12; the report and
   the lesson both say 12). Fix the count in this round's landing.
2. **The mined-criteria count in the lane's own files is stale.** `corpus/QUALITY.md` carries criteria 182–189
   (eight) while the lesson's `## Trends` row and the SCORECARD's calibration row both say "five criteria mined
   (QUALITY 182–186)". Land a `## Corrections` row in the lesson carrying the real split (182–184 pre-freeze probes,
   185–186 round-86 routed defects, 187–189 wave findings — three / two / three), and correct the SCORECARD sentence.
3. **`S218`'s Gate record carries no ≤25-word located quote.** Quote criterion 178's operative clause (≤25 words)
   in this round's lesson before any new row is admitted.
4. **Carried template defect, mis-quoted.** The report's conformance note 1 cites the corrupted run-15 quote as
   ending "`…shokunin style bu…`"; the real fragment is `…on the hyaku style but using these models and conc` /
   `…re each` (cut mid-word). Record the correction here and in the report; the defect itself is operator-owned.

## Claim selection

- **C1 — operability (the lowest scored non-retired axis, historical 3/10).** It closes `plans/round-87.md`
  Amendment 4's three routed items on the battery: bind the class to `http == "203"` in both derivations, have each
  leg write its own receipt under `--work` and re-read the count, names and values from that file, and compare the
  width legs against a 203-only third derivation rather than against each other. The subject tool is unchanged.
- **C2 — calibration.** It closes Amendments 1, 2, 3 and 6 on the curation counter: every named qid must share a
  term (A1), the floor gains a per-row token floor at the measured minimum (A2), a superseder disposes only when
  `mined` (A3), and the per-entry qid set is pinned (A6). The calibration row repair (`Q1, Q3` → `Q1`) lands in this
  round because the every-qid leg fails on the landing tree until it does — the repair is the counted row's own
  warrant becoming true.
- Rejected as claims this round: a new knowledge entry (no candidate source was opened for one; the round's
  capability gain is in the instruments and the frontier step's registry curation); the r80 backlog Gate ids and the
  `S217` successful-refused record form (carried debt, QUALITY 173, no new instrument this round); the
  SCORECARD/count corrections above (routed-defect fixes land as part of the claims' revisions, not as a third claim).

## Pre-freeze repairs (before the first scored run, disclosed)

1. **The class is bound to `203` in both independent derivations.** `_qualifying_203` and `count_203_rows` both
   require a 3-character `http` equal to `"203"`; the old non-200 bound and the 3-digit-only bound are gone.
2. **The verdict re-reads and reconciles the legs' own receipts.** Each leg writes `<work>/legs/<name>.txt` with
   `name=ok|fail detail=<detail>`; the predicate re-reads the file, requires the re-read set to equal
   `EXPECTED_LEGS` with every value `ok`, *and* reconciles the leg's detail string against its value (`RECONCILED`).
   The `R87ReviewerC1` E4 shape (the `ok` expression detached, the detail still honest) now fails `RECONCILED=14/15`;
   the joint-narrowing E1 shape fails the width legs against the third pin.
3. **A third derivation pins the width.** `registry_rows_203` counts distinct `(sid, url)` pairs with `http == "203"`
   through its own filter; the width legs require `len(d1) == d1_expected == div3 == ROWS_203` with `ROWS_203 = 3`
   frozen (S021, S032 share one URL; S022 a second — three pairs, two URLs). `T4-truncate`, `T4-record-keyed` and the
   joint `E1` narrowing all fail it (`1/3/3 pin3`).
4. **The mutation battery carries the two new shapes as killed mutants.** `E1-joint-narrow` and `E4-setup-detached`
   are in `mutate-r88.py`; the round-87 `N-deny-width` equivalent is retired (it is no longer degenerate: the third
   pin catches it).
5. **The curation counter gains the four routed legs.** `WARRANT` now requires *every* named qid to share a term;
   `FLOOR` requires the pinned qid set and a per-row token floor `MIN_TOKENS = 7` (the measured minimum over the 20
   located base quotes: r84 `Q13` "Date on which the resource was changed.": 7 words); `TEACHES` disposes a flagged
   row only via a `mined` superseder and also requires the superseding row's own `teaches` to read in its own
   capture. The five-control battery (`curation-r88-controls.py`) refuses `A1c`, `A1d`, `caseG`, `F2` and `B1b`,
   all accepted by the frozen round-87 counter.
6. **The calibration row repair.** `corpus/knowledge/provenance-recording-r85.md` row "Naming what a resource
   derives from" names `Q1, Q3 (S215)`; `Q3`'s quote shares no distinctive term with the row's cells (the row's
   terms are `chain, derivation, entities, known, property, provenance`; `Q3`'s are `then, bar, chart, derived,
   dataset`), so the every-qid leg would fail the *landing* tree on a row the entry itself asserts. The warrant is
   narrowed to `Q1 (S215)`, whose quote does share (`provenance, entities, property`). Landed ledger:
   `corpus/knowledge/provenance-recording-r85.md` is re-cited by no counter, so the repair is not a counter change;
   it is the entry's own sentence becoming true under the new leg, and it is disclosed here, not buried.

## Freeze

`corpus/evidence/round88/claims.md`, `claims.json`, both counters, the control batteries, their receipts, the
instrument pins and the egress table are committed together as the freeze, before the landing commit and before any
scored run of the round-88 candidates. The provenance entry repair above is committed with the freeze so the
landing tree's `CURATION_R88=PASS` is re-derivable at the landing revision.

## Amendments after the freeze

None yet. An amendment is written here only when a wave artifact falsifies a claim's stated wording (addendum §8,
Amendment 59) and names the artifact plus the narrower property that may verify, or the honest stop.
