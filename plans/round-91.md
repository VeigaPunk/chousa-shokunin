# chousa — round 91: plan and amendments

L1 `ChousaR91`. Base `265b8633b7e5d1da49da6fb948df9707373fb15c` (round-90 landing + its non-author spot-check at
`265b8633`). Frozen claims: `corpus/evidence/round91/claims.md` (prose) and `.ufo/waves/round-91/claims.json`
(machine form the pre-file gate reads). A `narrowing` cell in `.ufo/waves/round-91/claim-falsification.tsv` resolves
to a section here.

## Inputs — round 90's routed defects and the SCORECARD r91 plan

`corpus/lessons/round-90-verifier-spotcheck.md` §Routed defects:

1. C2 reclaim: count every `## Located quotes` row (or refuse a non-`Q`/non-3-cell row explicitly), cross-check
   every cited source's `status`/`used-by`, and guard the warrant share with a term-frequency test → **C2**.
2. C1 residues: refuse duplicate header keys, bind the instrument bytes a row executes to a pin, make `SELF_PIN`
   name both revisions, add fixtures for fresh-divergence and empty-body (M6/M8), repair the `--root`/`--repo` path
   base (QUALITY 202) → **C1** (the two fixture classes land as `INSTRUMENT_PIN_MISMATCH` and `MISSING_HEADER`
   battery cases; a fresh-divergence case is not one of the six surviving forgery classes measured below).
3. Harm row is a self-comparison: give the sweep a base-versus-head delta that can fail → **C1** (`c1-harm` now
   reads `tools/gate-records.py` from the frozen base `265b8633`, not `master`).
4. Ledger classification and 5. freeze-pin plan entry → conformance; this round's ledger names each amendment by
   number and this plan records the freeze-pin state.
6. Citation precision → conformance; every before-line below names the receipt that carries the string.
7. Clause (a) is per row → named limit in C1.

`SCORECARD.md` §Planned — round 91: (1) operability — the C1 residues; (2) calibration — the C2 repairs and a
successor claim that names the classes; (3) freshness — bind the case-range prose to the tool's own case names and
delete the r90 unentailed double-count loop. The loop deletion is C2's instrument (R4 below); C3 carries the prose
binding.

Opened this round as a source: **S070 re-opened** (the installed `sha256sum(1)` page, `93c17dff…` bytes, quote
"Print or check SHA256 (256-bit) checksums.") grounds C1's digest-pin rule; the planned new row S221 (the IR
textbook's document-frequency definition) was attempted once and failed (`curl rc 28`, no bytes, `refetch.tsv` row
`S221 … 28 000 - -`), so no S221 row is written. One sourced claim: C1 cites S070.

`considerthese/2026-11-07.md` proposal 1 (the duplicate-wins watch) was applied in round 90 to body keys; this round
applies it to the receipt HEADER surface (C1 R1) and to the `## Located quotes` row shape (C2 R1). No other
proposal is acted on.

## Claim selection

- **C1 — operability (lowest scored non-retired axis, historical 3/10).** `corpus/evidence/round91/control-driver-r91.py`:
  duplicate header keys refused, `# expected_exit=` required and checked, every executed instrument and the
  expectations file pinned in `instrument-pins.txt` and verified on disk and at `--rev`, `SELF_PIN` names both
  revisions, unscored receipts refused, and the `--root`/`--repo` bases separated (QUALITY 202). The subject tools
  the rows execute are unchanged; no domain record can move.
- **C2 — calibration.** `corpus/evidence/round91/curation-r91.py`: every Located-quotes row counted or refused with
  its shape named; every cited source's `status`/`used-by` read; the warrant share guarded by a document-frequency
  test over the entry's own units (`DF_MAX=3`, measured); the unentailed double-count loop replaced by one record
  per offending (row, term).
- **C3 — freshness.** `corpus/evidence/round91/skill-tally-r91.py`: the `SKILL.md` case-range prose is derived from
  the tool's own `ok-case` names — the `bash-pin-override` family is 282–283, not the prose's 276–283, and the
  `r39 bash-pin` clause is the `bashenv` family 273–275. The repair is the one-clause SKILL.md edit.

Rejected as claims: a new knowledge entry (the one source opened this round grounds C1's digest rule, not a domain
fact — the attempted S221 row failed to fetch); the round-74 order oracle, QUALITY 173's record form and the r80
Gate-id backlog (carried debt, no instrument in this round touches them).

## Pre-freeze repairs (before the first scored run, disclosed)

1. **C1 header surface.** `header_multi()` returns every value per key; `check_headers()` requires exactly one
   `case`, `expected_exit`, `exit` and `computed_against`, each carrying the row's value (R1/R2).
2. **C1 pin surface.** `pin_report()` reads `instrument-pins.txt`, resolves each row's executed script and the
   expectations file against `--root`, and requires the pin to equal the on-disk sha256; `self_pin()` also checks
   every pinned blob at `--rev` and prints both revisions (R3/R4/R5). `pin_report()` is only required in `verify`;
   `emit` mints no pin.
3. **C1 battery.** `control-forgeries-r91.py` builds a two-row fixture and six forgeries (duplicate exit header,
   duplicate pin header, instrument stub, relaxed expectations, missing `expected_exit`, unscored receipt), runs
   the unchanged r90 driver on each (must accept) and r91 (must refuse), and keeps a positive control.
4. **C2 shape surface.** `q_shape_violation()` is a named detector; a non-`Q`/non-3-cell/empty-source/empty-quote/
   duplicate-qid row is a `QSHAPE` finding instead of a silent `continue` (R1).
5. **C2 source surface.** `source_link()` reads the cited row's `status` and `used-by`; every located quote's source
   must be `mined` and must name the entry (R2).
6. **C2 warrant surface.** The TFREQ documents are the entry's located quotes plus its decision rows' Do/Never
   cells; a shared term counts only at document frequency `<= DF_MAX` (R3). `DF_MAX` is measured, not chosen:
   the legitimate rows' selected terms are at most 3 (`source` alone reaches 7 and is no warrant).
7. **C2 loop.** `unentailed_terms()` returns the list; the caller appends one record per term with the term the row
   carries (R4).
8. **C1 harm row.** `controls/expected.tsv`'s `c1-harm` reads the base tool from `265b8633`, so the sweep compares
   the frozen base tool with the landed tool (routed defect 3).
9. **C3.** `skill-tally-r91.py` adds `CASE-RANGE`; the SKILL.md clause is repaired at the landing, not at the
   freeze, so the freeze tree still shows the defect (`MISLABELED=6`, `CASE_RANGE_OK=1/2`).

## Freeze

`corpus/evidence/round91/claims.md`, `.ufo/waves/round-91/claims.json`, the six instruments
(`control-driver-r91.py`, `control-forgeries-r91.py`, `curation-r91.py`, `curation-r91-controls.py`,
`skill-tally-r91.py`, `controls/selftest-r91.txt` receipt), `controls/expected.tsv`, the before receipts under
`controls/receipts/`, `instrument-pins.txt` and `corpus/evidence/round91/egress.tsv` are committed as the freeze,
before any scored run of the round-91 candidates and before the wave. The receipts are emitted at the freeze
revision and carried by the next commit (the carrier); `--rev` names the freeze and `--receipts-rev` the carrier.

## Amendments after the freeze

An amendment is written here only when a wave artifact falsifies a claim's stated wording (addendum §8,
Amendment 59) and names the artifact plus the narrower property that may verify, or the honest stop.
