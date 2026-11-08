# chousa — round 92: plan and amendments

L1 `ChousaR92`. Base `d7780feff6e39ae74a2fd77fc9773c671b33da95` (round-91 landing + its non-author spot-check at
`d7780fef`). Frozen claims: `corpus/evidence/round92/claims.md` (prose) and `.ufo/waves/round-92/claims.json`
(machine form the pre-file gate reads). A `narrowing` cell in `.ufo/waves/round-92/claim-falsification.tsv` resolves
to a section here.

## Inputs — round 91's routed defects and the SCORECARD r92 plan

`corpus/lessons/round-91-verifier-spotcheck.md` §8 routed defects:

1. **operability** — gate `passed` on `EXACT_OK`; strip leading whitespace in the header test; pin the executed
   script (a `script=` column or execute only the pinned path); make `instrument-pins.txt` self-pinned and refuse a
   duplicated path (`PIN_DUPLICATE`); resolve `--expected`/`--receipts`/`__file__` against the base they are read
   from; add `--work` with a `TMPDIR` default; move Amendment 10's external pre-step into the procedure text; make
   `emit` require an explicit `--receipts`; run the fresh legs under `bash -c` with a scrubbed environment.
2. **calibration** — run QSHAPE before the shared first-cell filter; pin decision-row width and count per entry;
   tokenise the `used-by` cell; add two-directional `source_link` assertions; correct the docstring df numbers
   (5 and 8 under 24 units).
3. **freshness** — scope both regexes to the Gates-table cell; bind the r82 block range or drop it; pin the
   historical multiset so a deleted quote changes the verdict; bind exact case names and the case count; add selftest
   receipt to the on-disk pin set; make the controls accept the landing clause by regex.
4. **carried debt** — the round-74 source-blind order oracle, QUALITY 173's successful-refused record form, the r80
   backlog Gate ids. Untouched this round (named in the report, not silently dropped).

## What is frozen and what is not

* **Frozen (claim sentences, predicates, kill rules):** `corpus/evidence/round92/claims.md` + `.ufo/waves/round-92/claims.json`.
  Predicate tokens are the same sentence in the plan, the same condition in the counter's code and the same label in
  the receipt.
* **Not frozen:** the prose restatements in the SCORECARD; any measurement not named in a claim sentence.
* **Before states:** measured by the r92 batteries themselves (`FORGERY_REFUSED=3/3` with r91 mechanism
  attestation for C1 — the r91 verifier cannot PASS a fixture because it pin-checks against the real table,
  so no PRIOR_ACCEPTED=6/6 is claimed for C1; `PRIOR_ACCEPTED=4/4` for C2; `PRIOR_ACCEPTED=1/1` + carried
  refusals for C3). Before receipts land in `corpus/evidence/round92/controls/receipts/c{1,2,3}-before.txt`.

## Damages found while building (before the freeze)

These were built and tested in scratch before anything was committed; no measurement was taken on an unfrozen
instrument.

1. **A self-referential sha pin is unsatisfiable as a whole-file hash.** The first fixture design ("write a
   placeholder, hash, rewrite") cannot verify (`sha(file-with-digest) != digest`). The frozen design is the
   minus-self-row digest: the pins file pins the sha256 of its own rows with the self row removed. A rewritten
   non-self row breaks it; the self row is outside its own hash by construction (battery case pins-rewrite).
2. **The fixture battery's prior control cannot PASS for r91.** r91's `verify` always pin-checks and, in the
   lane, reads the real pins table; in a probe layout the default file is absent. The r92 battery therefore
   attests the prior mechanism (source-level: last-wins `read_pins`, first-token `instrument_rel`, no pins-file
   entry in `pin_report`) instead of printing a fabricated `PRIOR_ACCEPTED=6/6`.
3. **The do-nothing control fired.** A first C1 design kept the six r91 classes as the claimed discrimination;
   the probe showed r91 already refuses all six (its own round's work). They were removed from the frozen
   battery and the claim says so.
4. **C2's regression reference pointed at a battery that does not take `--counter`.** The r91 controls have no
   `--counter` flag (only the r90 controls do, via its own alias writer). The frozen controls replay the r90
   battery with a verdict-token alias, exactly as r91 did.
5. **A fifth C2 leg was missing from the count.** The counter grew from 13 to 14 legs (USED_BY); the first
   run printed `LEGS_MEASURED=13/14`-style failures before the freeze. `EXPECTED_LEGS=14` is frozen.
6. **C3's others multiset initially counted document-wide.** The 215 tail tally sits after `## Round26` (outside
   `## Gates`); the first draft pinned `{161,215,256}` and failed on the clean tree. The frozen multiset is the
   in-section two `{161,256}` and the 215 tally is a named limit.

## Amendments

*(None yet — amendments are added here when a wave artifact fires on a claim's wording; each names the
artifact, the constraint, and the narrower property it narrows to. The closure reads this file for `narrowing`
pointers.)*

## Do-nothing control (must not reach the after-state)

* C1: the r91 driver on the three S fixtures accepts each (mechanism attestation: `read_pins` last-wins,
  `instrument_rel` first-only, no pins-file entry in `pin_report`); no receipt/PASS is claimed from it.
* C2: the r91 counter prints `CURATION_R91=PASS` on all four S forged trees.
* C3: the r91 counter prints `SKILL_TALLY_R91=PASS` on the deleted-161 tree.
