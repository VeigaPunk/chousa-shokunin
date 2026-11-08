# chousa — round 86: plan and amendments

L1 `ChousaR86`. Base `3bfb6885958ad4a674ad1896f70d1e836be609e4`. The frozen claims are in
`corpus/evidence/round86/claims.json` (machine form) and `corpus/evidence/round86/claims.md` (prose); this file records
the pre-freeze repairs and any post-freeze amendment the round needs. A `narrowing` cell in
`.ufo/waves/round-86/claim-falsification.tsv` resolves to a section here.

## Claim selection

- **C1 — operability (the lowest scored non-retired axis, historical 3/10).** It closes round-85 routed defect 3 and
  the round-85 critic/mutation findings: the battery had no forgery for the 200-only class, so the repaired REFETCH rule
  was witnessed only by a fixture beside the predicate, and mutant `M17-refetch-http-2xx-accepted` survived every leg.
  Round 86 moves the class *inside* the predicate (a 203-body admit built from the committed `S021` refetch row) and
  computes the mutant from the subject tool's bytes.
- **C2 — calibration.** It closes round-85 routed defect 1 (the `S024`/`S031` supersession inversion, and the two
  warrant cells that state a distinction their cited quotes refuse) plus round-85 routed defect 4's retraction duty
  (lesson correction). The axis is calibration because the repaired defects are the lane's own self-assessment of what
  is mined and what a quote entails.
- Rejected as claims this round: a new knowledge entry (the one candidate source fetched for it, `S217` DCMI Namespace
  Policy, served a stub — recorded `rejected`), and the twelve r80 backlog Gate ids (no new instrument; carried debt).

## Pre-freeze repairs (before the first scored run, disclosed)

1. **`curation-r86.py` supersession predicate narrowed to the live-vs-unadopted form.** The first bytes counted every
   edge whose target row was `mined` (5 on this tree: `S024`, `S070`, `S171`, `S196`, `S197`), which would have failed
   legitimate legacy two-row histories (`S073`/`S176`/`S200`/`S201` are themselves `mined`). The routed defect is the
   inversion where the superseded row is the live citation and the correction is unadopted; the counter now counts that
   (1 at base). No scored run used the earlier bytes.
2. **`curation-r86.py` case bug in `MODIFIED_DEF_CITED`.** The first bytes compared the lowercase definition string
   against the quote's original case and printed 0 on a tree that carries the quote; found while building the candidate
   in scratch (`/fast/scratch/hyaku/chousa-r86/l1/cand`), before the freeze and before any scored run. Fixed to compare
   lowercased; the counter's sha is pinned in `instrument-pins.txt` at the freeze.
3. **`gate-records-r86.py` D1 builder derives its quote from the capture**, not from a quoted literal, so no forgery
   text is hard-coded in the counter. The mutant leg derives `M17` by replacing `r[6] == "200"` with
   `r[6].startswith("2")` in the subject tool's own bytes and refuses to score a mutant that the subject bytes did not
   yield.

## Freeze

`corpus/evidence/round86/claims.md`, `claims.json`, both counters, `c2-positives.tsv`, the three control receipts and
`instrument-pins.txt` are committed together as the freeze, before the landing commit and before any scored run. The
subject tool `tools/gate-records.py` is not modified this round.

## Amendments after the freeze

None yet. An amendment is written here only when a wave artifact falsifies a claim's stated wording (addendum §8,
Amendment 59), and it names the artifact, the narrower property that may verify, or the honest stop.
