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

Each is a narrowing or a wired guard forced by the wave, applied before `C2`; the artifact that forced it
is named with its seat. The frozen sentence before → after is recorded in `claims.md` and the
claim-falsification ledger.

**Amendment 1 (R94RevPrior F1) — the C1 before-state basis.** §Damages 1 above says the r93 driver "refuses
the three-column row as `SETUP malformed pin row`". Measured: the committed r93 driver splits the row on the
first whitespace run, so the path becomes `instrument corpus/…`, the file is absent, and the run ends
`PINNED_FILES=0/…` at exit 1 — a mis-parse, not a setup refusal. The before state is therefore measured on
the **two-column projection** of the same rows (which is what `forgeries-r94.py` does and what
`evidence-before/c1-prior-accepts.txt` records); the sentence above is superseded by this paragraph, and no
claim sentence changes (it never relied on the malformed-row form).

**Amendment 2 (R94ReviewerC2 F1/F2/F3/F4) — C2 wording and class domain.** (a) `Q_PUNCTQUOT` is the
population of every three-cell quote row *before* qid/source/location resolution; the earlier phrase
"located-quote population" was wider than the code, and `claims.md` now says what the code counts. (b) The
class test was ASCII-only (`[A-Za-z0-9]`) while the sentence said "no alphanumeric character": a CJK quote
was refused as punctuation. The test is now `any(ch.isalnum() for ch in inner)` (Unicode), `witness()` gains
`punct-cjk-silent`, the battery gains `x3-cjk-quote` (a CJK quote must NOT be the class, and is refused
downstream as short), and `DETECTOR_WITNESS` is 18/18. (c) The predicate values are printed across two lines
(the summary line and the `VERDICT` line); the sentence now names both. (d) `locates()`'s guard is defense in
depth — the shape leg refuses the class first on the routed entries — and is declared as such in the named
limits; its force is measured by `witness()` only.

**Amendment 3 (R94ReviewerC3 F1–F4) — C3 coverage and wording.** (a) A tally declared in `TAIL_DECLARED`
with no `TAIL_OWNED` entry could be moved freely: `TAIL_OWNER_UNMAPPED` now binds the two halves of the
declaration. (b) Named limit 2's wording was wider than the code: the heading recognizer is a column-0
`^#{1,6} ` line (ATX with a space), not every ATX form. (c) The `moved-to-heading` case renamed the owner
heading rather than moving the tally; it is now `heading-alias` and says so. (d) `TAIL_OWNED_OK` is printed
observability: the verdict force is the owner codes feeding `TAIL_OK`, and the kill rule says that instead.

**Amendment 4 (R94ReviewerC1 F1, R94ExecC1Repro F1, R94ScoutSources F1, R94SentinelScope F1,
R94ExecMutations C1) — C1's battery case `s1-schema-two-column` was unsatisfiable.** It wrote the valid
three-column table and then demanded `SETUP PIN_SCHEMA` from the same table, so `FORGERIES=PASS` was
unreachable on every tree the driver accepts; the aggregate `SCHEMA_REFUSED` (read from `s0`) stayed green,
which is why only the `FORGERIES=` token moved. Fix at F2: `s1` dropped; the do-nothing measurement is
`s0-schema-prior` (r93 scores the two-column table, r94 refuses it). Residual: the wave's verdicts about the
C1 battery are about `C`'s bytes, and `after/c1-forgeries.txt` at F2/C2 is the green run.

**Amendment 5 (R94ReviewerC1 F2) — the expectation role's code vocabulary.** The sentence promised
`PIN_ROLE_DANGLING` / `PIN_ROLE_MISSING` for every covered role; the single-member `expectation` branch emits
`PIN_ROLE_MISMATCH` on either direction. The sentence now names that. The set relation itself is correct.

**Amendment 6 (R94ReviewerC1 F4, R94CriticClaims) — `PIN_ROLES_OK` is a ratio, not the gate, and a deleted
`driver` row is unobserved.** The verdict force is the role codes; the ratio is over the table's own
non-driver rows, so a deleted row shrinks both sides and can print `13/13` while the run FAILs. Named limit 2
no longer claims a `PIN_MISSING`-class code for a deleted `driver` row: the walk iterates the table, not the
tree, so that row is unobserved.

**Amendment 7 (R94ReviewerC1 F3, R94ExecC1Repro F2) — prior acceptance is its own measurement.** The first
F battery derived `PRIOR_ACCEPTED` from the same dict as `FORGERY_REFUSED` (over all 16 result sets the two
numbers never differed). At F2 each fixture records its r93 exit code (`old_rcs`) and `PRIOR_ACCEPTED` counts
those, so the two ratios can disagree.

**Amendment 8 (R94SentinelScope F2/F5/F6/F7) — containment and validation.** `--work` equal to a system root
is refused before any `rmtree`; a pin row whose real path leaves `--root` is `PIN_ROW_OUTSIDE` (symlink
included); `--expected`/`--pins` (and `--receipts` in verify) must resolve inside `--root` or the run is
`SETUP`; `--receipts-rev` is validated as 40-hex like `--rev`.

**Amendment 9 (R94SentinelScope F3/F4/F8/F9/F10) — host paths and leftovers.** `expected.tsv` no longer sets
`HOME=/home/vgpnk` (the driver's own scrub supplies the tree root) and the setup row passes a *relative*
`--base-tool`, so `receipts/c1-harm-setup.txt` no longer embeds the emitter's scratch path; the forgeries
battery removes its clone before exit. Still unobserved, declared: an instrument's unpinned inputs (F9), and a
setup-class failure inside an executed instrument surfacing as that instrument's exit rather than a `SETUP`
line (F10) — both are round-95 plan items.
