# chousa — round 94: plan and amendments

L1 `ChousaR94`. Base `0f3f84dab3a094ec0a2fe8ae9ae59d3326e1a9b6` (round-93 landing + its non-author
spot-check at `af917ae6`, admitted). Frozen claims: `.ufo/waves/round-94/claims.md` (prose) and
`.ufo/waves/round-94/claims.json` (the machine form the pre-file gate reads). A `narrowing` cell in
`.ufo/waves/round-94/claim-falsification.tsv` resolves to a section here.

## Inputs — round 93's routed defects and the SCORECARD r94 plan

`corpus/lessons/round-93-verifier-spotcheck.md` §"Routed defects for next round":

1. **D1 pre-file ledger absent** — `--init` the ledger, one row per claim × attack seat, iterate to exit 0,
   paste the line. **Addressed** (§Ledger below).
2. **D2 stale `22/22` in `SCORECARD.md`** — the round-93 block's *operability* bullet still says "22/22
   rows byte-checked" while the landing population is 23. Corrected in the round-94 block, naming the
   superseded text (append-only discipline; the round-93 block is not rewritten).
3. **D3 "eleven amendments" vs 12** — routed as an erratum: the round-94 report's *Landed changes* names
   the superseded sentence and the twelfth amendment, rather than editing the filed round-93 report.
4. **D4 landing/wave hashes not cited** — every landing commit of this round is cited by hash in the
   report's *Landed changes*.
5. **D5 receipts lack `computed_against`** — the r94 driver writes `# computed_against=<rev>` in `emit` and
   `PIN_MISSING`/`PIN_MISMATCH` when it does not match `--rev`; every scored receipt in
   `corpus/evidence/round94/after/` therefore carries the measured revision, and the pins table pins them.
6. **D6 r82 clip residual** — re-flagged here as still unbound (the 215-tail half was closed by round-93
   C3; the *range* clause is not measured by any counter). It stays a routed item; it is not silently
   dropped and not claimed as fixed.

## What is frozen and what is not

* **Frozen (claim sentences, predicates, kill rules):** `.ufo/waves/round-94/claims.md` +
  `.ufo/waves/round-94/claims.json`. Predicate tokens are the same sentence in the plan, the same
  condition in the counter's code and the same label in the receipt.
* **Not frozen:** the prose restatements in `SCORECARD.md`; any measurement not named in a claim sentence.
* **Before states:** measured by the r94 batteries and committed in
  `corpus/evidence/round94/evidence-before/` **before** any scored run: `c1-prior-accepts.txt` (r93 driver
  on a clone at base, `--rev 3789608d`, PASS with the claims rows removed), `c2-prior-accepts.txt` (r93
  counter on the punctuation tree: `Q_SHAPE_FAIL=0`, downstream FLOOR/WARRANT only),
  `c3-prior-accepts.txt` (r93 counter on the moved-tail tree: `TAIL_OK=1`, PASS).

## Freeze and carrier

* **F** — this commit: the six r94 instruments (`control-driver-r94.py`, `curation-r94.py`,
  `skill-tally-r94.py`, `forgeries-r94.py`, `curation-controls-r94.py`, `skill-tally-r94-controls.py`), the
  copied expectations table and its 16-name leg table, `controls/selftest-r94.txt` (re-captured this
  round), the claims (prose + machine), this plan, and the three before receipts.
* **C** — the carrier: the six control receipts emitted against `F`, the pins table generated from the tree
  at `C` (non-receipt rows pinned at `F`, receipt rows at `C`), and the scored receipts under
  `corpus/evidence/round94/after/`.
* Any amendment the wave forces is applied in a **new** freeze commit before `C`; the superseded pair is
  named here, never rewritten.

## Pre-freeze measurements (before the wave, by the L1)

| instrument | command | observed |
|---|---|---|
| curation counter, clean tree | `curation-r94.py --root .` | `CURATION_R94=PASS`, `LEGS_MEASURED=16/16`, `Q_PUNCTQUOT=0`, `DETECTOR_WITNESS=17/17` |
| curation controls | `curation-controls-r94.py --root . --work <scratch>` | `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 PRIOR_REGRESSION=7/7` |
| tally counter, clean tree | `skill-tally-r94.py --root . --selftest …/selftest-r94.txt` | `SKILL_TALLY_R94=PASS`, `TAIL_OWNED_OK=2/2`, `LEGS=4/4` |
| tally controls | `skill-tally-r94-controls.py --root . --work <scratch>` | `CONTROLS=PASS CARRIED_REFUSED=6/6 MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1` |
| driver + role legs | `control-driver-r94.py verify --root . --repo . --rev F --receipts-rev C` | measured at `C` (needs the receipts and the pins table) |
| driver forgeries | `forgeries-r94.py --root . --repo . --rev F --receipts-rev C --work <scratch>` | measured at `C`; the four role fixtures + the do-nothing two-column form + two carried refusals |

## Damages found while building (before the freeze)

1. **The r93 projection is not the same bytes.** The role defect cannot be measured by handing the r93
   driver the r94 table: it refuses the three-column row as `SETUP malformed pin row`, which is a schema
   refusal, not the defect. The battery therefore writes the **two-column projection** of each fixture's
   row set (with the self row re-digested under r93's own minus-self rule), so the prior driver scores the
   same population and its PASS is the before state. Recorded as the round's `## Mistakes` row.
2. **`legs.txt` lives at a per-round path.** The round-90 regression battery mirrors only the r93 leg
   table; the alias shim now writes the r94 table into the mirrored tree, so `CONTROLS=PASS` rather than a
   `SETUP` refusal is what the regression line measures (first run: `CONTROLS=FAIL`, two `CASE_DEVIATION`
   lines with `CURATION_R90=SETUP missing …/round94/controls/legs.txt`).
3. **`TAIL_OWNER` needed a count code.** A duplicated tail tally failed only the multiset comparison, so the
   owner leg stayed silent; `TAIL_OWNER_COUNT` was added and is bound by the `double-tail-215` case.

## Round shape and wave

One v1 wave of 12 seats (policy `ufo-wave-policy.json`, band 8–16): 3 executors, 3 reviewers, 1 critic,
1 mutation-tester, 1 sentinel, 1 revenger, 1 connector, 1 scout. Attack share 7/12 (58 %). The L1 holds the
planner seat; the scout carries the bounded planning data-walk. Spec, dispatch and results under
`.ufo/waves/round-94/`.

## Amendments

*(none yet — every amendment the wave forces is appended below with the artifact that forced it, before
`C`)*
