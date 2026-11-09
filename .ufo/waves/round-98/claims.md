# Round 98 — frozen claims (chousa, L1 `ChousaR98`)

Base `98b8177c1e8b39cdf1167928e4f5d609f6fa81b6` (round-97 landing plus its non-author spot-check). The freeze F is
the lane commit that first carries this file; machine form `claims.json`. Two claims, two axes, no exploratory
claim. C2 is the round's sourced claim (S231, opened this round). Each claim beat a committed do-nothing control
before the freeze (`corpus/evidence/round98/before/`), scored by its frozen counter.

## C1 `C1-SELFTEST-R97MUTANTS-R98` — operability (lowest axis, historical 3/10)

**Sentence.** `python3 -B tools/search-rerun.py --selftest` prints 67 named case lines (round 97's 48, a guard
canary `g00` that runs the guard and summary code on fixed case sets, and cases `r17`-`r34`) and
`SEARCH_RERUN_SELFTEST: PASS cases=67/67`; scored by `corpus/evidence/round98/selftest-controls-r98.py`, it kills 35
of the 37 mutants written by round-97 seat `R97MutantsC1` (all except the named survivors `u01-verify-return-0` and
`u05-tree-files-jj`), read from the committed probe `.ufo/waves/round-97/w1/R97MutantsC1-mutprobe.py.txt`, where the
round-97 tool kills 12 of them; it still kills the round-97 battery's 34 external mutants and the round-96 battery's
23; three mutants that do not change what the tool computes survive it; and the battery refuses five stand-ins,
among them a guard-blind self-test and a self-test that fails on any change to its own bytes (round-97 routed limit
(g)).

**Counting commands and predicate (both exit 0):**

    python3 -B tools/search-rerun.py --selftest
      → last line `SEARCH_RERUN_SELFTEST: PASS cases=67/67`
    python3 -B corpus/evidence/round98/selftest-controls-r98.py --root . --work <scratch>
      → `POSITIVE=1/1 KILL_REQUIRED=35/35 DO_NOTHING_REFUSED=1/1 PRIOR_R97_KILLED=34/34 R96_MUTANTS_KILLED=23/23 EQUIVALENT_SURVIVED=3/3 ORACLES_REJECTED=5/5 NO_WRITE=1/1 REGRESSION_R95=2/2 EXTERNAL_R97_KILLED=35/37 BASE_KILLED=12/37 CASES=67`
      → `SELFTEST_CONTROLS_R98=PASS`

**Before (do-nothing control, committed before F):** the base tool scored by the same battery
(`corpus/evidence/round98/before/c1-base.txt`): `KILL_REQUIRED=12/35`, `SELFTEST_CONTROLS_R98=FAIL`.

**Kill rules.**
- K1: either predicate line differs at F.
- K2: a non-author seat shows a mutant that does not change what the tool computes on any input, and the F
  self-test kills it (the self-test then detects bytes, not behaviour).
- K3 (harm): `verify` output or exit code differs from the base tool, plain or `--strict`, on
  `corpus/fixtures/search-rerun-r95.md`, `corpus/knowledge/search-peer-review-dedup-r96.md`,
  `corpus/knowledge/press-checklist-questions-r97.md` or `corpus/knowledge/press-2015-statement-questions-r98.md`.
- K4: the battery or the self-test writes outside `--work` (self-test: anywhere), or changes the lane's
  `git status --porcelain` / `git diff`.

**Named limits.**
- (a) Mutants elsewhere in the tool may survive; the claim is about the 37 named ones, the 34 + 23 prior ones and
  three equivalents.
- (b) `u01-verify-return-0` and `u05-tree-files-jj` survive: the self-test does not run `verify` or the disk reader
  (`tree_files`, `run_on_tree`); the round-95 battery catches `u01`, nothing in the lane catches `u05`.
- (c) The EQUIVALENT leg has three equivalent mutants; a self-test that recognises those three (or the 37 scored
  mutants) by content and reports accordingly would pass the battery. Hash-of-self is refused; content
  recognition is not ruled out.
- (d) The guard canary checks `_collect` and `_summary` on two fixed case sets; a mutation that misbehaves only for
  particular case ids is caught only through those ids' own cases.
- (e) The self-test reads /dev/null and runs `git -C /dev/null` twice (r29, r34); "no write, no socket" is
  observed (NO_WRITE leg for writes), not enforced for sockets.

## C2 `C2-ENTRY-R98` — depth (sourced: S231)

**Sentence.** A new entry, `corpus/knowledge/press-2015-statement-questions-r98.md`, holds the PRESS 2015 Guideline
Statement's own published abstract (S231, Europe PMC's record of PMID 27005575, opened this round) in 15 located
quotes — the statement's four documents, its development method, its review's finding about the elements, the six
retained elements and the removed seventh by name — compares the element names with the reprint's headings, and
quotes the 20 question lines of S225's checklist that the round-97 entry did not, so that the S225 checklist lines
carrying a question mark are quoted whole across the two entries 36/36 (16/36 at the base).

**Counting commands and predicate (all exit 0):**

    python3 -B tools/gate-records.py verify --root . corpus/knowledge/press-2015-statement-questions-r98.md
      → `GATE_RECORDS files=1 records=38 ok=38 fail=0`
    bash tools/research-gate.sh verify-metadata corpus/knowledge/press-2015-statement-questions-r98.md --root .
      → `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`
    python3 -B tools/search-rerun.py verify corpus/knowledge/press-2015-statement-questions-r98.md --root .
      → `rev_match=5/5`, `SEARCH_RERUN: CLEAN`
    python3 -B corpus/evidence/round98/entry-controls-r98.py --root .
      → `POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 NEW_ONLY=1/1 FORGERY_REFUSED=7/7 QUESTION_LINES_HELD=36/36 BASE_HELD=16/36 ELEMENTS=7+6/7+6 WARRANTS_OK=10/10 LANE_FILLED=10/10`
      → `ENTRY_CONTROLS_R98=PASS`

**Before (do-nothing control):** entry absent at base, `gate-records.py` exit 2; base held 16/36
(`corpus/evidence/round98/before/c2-base.txt`).

**Kill rules.**
- K1: any predicate line differs at F.
- K2: a quote (M or K row) is not in its capture as `gate-records.py` normalizes it, or an S231 quote is not inside
  the record's `abstractText`.
- K3: a decision row's Do cell says something its warranting quotes do not say (a reviewer quotes the overreaching
  words), or a Never cell states a prohibition other than the negation of its own Do clause or "(none stated by the
  sources)".
- K4: the `## Element names compared` paragraph misstates a difference between S231 and S225 (re-derivable from
  the two captures).
- K5: S231's record is not the PRESS 2015 Guideline Statement (title, authors, DOI, PMID differ from S225's
  "Derived from" citation).

**Named limits.**
- (a) S231 is the abstract, read through Europe PMC's index record, not the statement's body or the publisher's page.
- (b) The questions are a reprint's wording (S225, tier B).
- (c) "36/36" counts lines, not questions (lines 64, 65, 78 carry several; 66-67 one).
- (d) Do and Never cells are checked by the controls only for naming existing quotes of the right source;
  faithfulness is the reviewer's item (K3).

## Amendments — re-frozen at F2 (wave-forced; each cites the seat artifact that forces it)

The claims are judged at F2 on the sentences and predicates below; the F text above stays as the F record. Seat
artifacts are under `.ufo/waves/round-98/w1/`. Plan record: `plans/round-98.md` § Amendments.

### C1 at F2

- **A1 (`R98MutantsC1` S02, S03, X4).** The canary's docstring said a summary that "returns 0 for one [failure]"
  fails it, but its only failing set had three failures: a summary returning 0 when exactly one case failed (S03,
  X4) or listing at most three failed ids (S02) survived. F2 adds two fixed sets (one failure among two cases; four
  failures). Both mutants now die under the frozen kill rule (L1 re-score in `plans/round-98.md`).
- **A2 (`R98MutantsC1` D01-D04, X3).** The direct FAIL path in `selftest()` never ran. F2's battery adds
  DIRECT_PATH: the tool under test with its canary call forced to return False, and forced to raise, must exit 1
  with the exact direct line and no traceback.
- **A3 (`R98MutantsC1` B1, B3, B5).** The battery's kill rule was never scored, and its denominators came from the
  literals they count. F2 adds KILL_RULE (four planted stand-ins) and pins the set sizes (35, 34, 23, 3, 5) as a
  SETUP refusal.
- **A4 (`R98MutantsC1` G01-G03, D05; `R98ScribeLesson` F1).** Not repaired, named: a weakened comparison inside the
  canary itself, a changed `g00` label, and a `return 0` after `_summary` in `selftest()` survive the self-test; they
  are mutants of the checker, outside the scored sets (limit (d) rewritten below).
- **A5 (`R98RevenPrior` (1)).** The plan said the guard mutants were caught by no lane instrument; at BASE the
  round-97 *battery*, run with `--tool <mutant>`, already fails on g01, g03 and g04 (its EXTERNAL legs collapse).
  The C1 sentence speaks of the *self-test*, which killed none of g01-g05 at BASE; the plan's sentence is corrected.

**C1 sentence at F2.** `python3 -B tools/search-rerun.py --selftest` prints 67 named case lines (round 97's 48, a
guard canary `g00` that runs the guard and summary code on four fixed case sets, and cases `r17`-`r34`) and
`SEARCH_RERUN_SELFTEST: PASS cases=67/67`; scored by `corpus/evidence/round98/selftest-controls-r98.py`, it kills 35
of the 37 mutants written by round-97 seat `R97MutantsC1` (all except the named survivors `u01-verify-return-0` and
`u05-tree-files-jj`), where the round-97 tool kills 12 of them; it still kills the round-97 battery's 34 external
mutants and the round-96 battery's 23; three mutants that do not change what the tool computes survive it; its
direct FAIL path exits 1 when the canary is forced to fail or to raise; and the battery, whose own kill rule is
scored on four planted stand-ins, refuses five stand-ins, among them a guard-blind self-test and a self-test that
fails on any change to its own bytes.

**C1 predicate at F2 (both exit 0):** self-test last line `SEARCH_RERUN_SELFTEST: PASS cases=67/67`; battery

    POSITIVE=1/1 KILL_RULE=4/4 DIRECT_PATH=2/2 KILL_REQUIRED=35/35 DO_NOTHING_REFUSED=1/1 PRIOR_R97_KILLED=34/34 R96_MUTANTS_KILLED=23/23 EQUIVALENT_SURVIVED=3/3 ORACLES_REJECTED=5/5 NO_WRITE=1/1 REGRESSION_R95=2/2 EXTERNAL_R97_KILLED=35/37 BASE_KILLED=12/37 CASES=67
    SELFTEST_CONTROLS_R98=PASS

Before at F2: the base tool under the F2 battery (`corpus/evidence/round98/before-f2/c1-base.txt`).
Kill rules K1-K4 unchanged. Named limit (d) at F2: the canary checks `_collect` and `_summary` on four fixed case
sets; it does not check itself — a weakened comparison inside `_guard_canary` (G01-G03), a changed `g00` label (D05)
or a wrong exit code after `_summary` returns (`R98ScribeLesson` F1) is not killed by the self-test; the direct FAIL
path is checked by the battery's DIRECT_PATH leg, not by the self-test. Limits (a), (b), (c), (e) unchanged.

### C2 at F2

- **B1 (`R98ReviewerC2` F1, `R98ExecC2Repro`, `R98ScoutSources`, `R98CriticClaims`; K2 fired).** M1 is the record's
  `title`, not a substring of `abstractText`; the entry said every S231 quote is inside `abstractText`. F2: the
  entry says M2-M15 are in `abstractText` and M1 is the title; the controls add FIELD (each S231 quote is the title
  or inside `abstractText`, no `<h4>` inside it) with forgery f11 (an S231 quote from the journal field).
- **B2 (`R98ReviewerC2` F2, `R98ScoutSources`; K3 fired).** Row 2's Never cell was neither its Do's negation nor
  "(none stated by the sources)". F2: Never is "(none stated by the sources)"; the elements-not-questions point
  moves to the Lane cell; the Do cell names the systematic review as one of three methods and keeps M4's scope.
- **B3 (`R98ReviewerC2` F3).** Named limit (c) omitted line 53 and misdescribed lines 66-67; rewritten, with the
  `sed` vs `splitlines()` line-numbering note.
- **B4 (`R98ReviewerC2` F4, `R98ConnectorSiblings` R4/R5).** S225 prints the pages as "40-6"; the entry now says
  so. The controls add IDENTITY (hitCount, pmid, doi, title, volume, pages) with forgery f12 (pmid changed); the
  JSON is not byte-stable across fetches, so a recheck compares fields.
- **B5 (`R98ConnectorSiblings` R6, `R98ReviewerC2` F5).** S231 tier A → B: the lane's carrier rule grades a
  third-party carrier B, and kotodama grades the same Europe PMC shape B. Registry cell, entry and lesson
  GATE-RECORDs changed together.
- **B6 (`R98MutantsC2` m08, m12, m13).** Three controls mutants survived because no forgery reached their checks;
  F2 adds forgeries f8 (an element cell that is part of a line), f9 (an extra 26-word quote) and f10 (an extra quote
  spanning two lines), and an ACCEPT leg (two benign edits must pass). `m10` (forced forgery tally) still survives:
  every forgery is refused, so forcing the tally changes nothing on these bytes.
- **B7 (`R98MutantsC2` E3).** Not repaired, named: an inverted Do cell passes the controls (limit (d), unchanged).

**C2 sentence at F2.** A new entry, `corpus/knowledge/press-2015-statement-questions-r98.md`, holds the PRESS 2015
Guideline Statement's own published abstract (S231, Europe PMC's record of PMID 27005575, opened this round, tier B)
in 14 located quotes from the abstract plus its title — the statement's four documents, its development method,
its review's finding about the elements, the six retained elements and the removed seventh by name — compares the
element names with the reprint's headings, and quotes the 20 question lines of S225's checklist that the round-97
entry did not, so that the S225 checklist lines carrying a question mark are quoted whole across the two entries
36/36 (16/36 at the base).

**C2 predicate at F2 (all exit 0):** `GATE_RECORDS files=1 records=38 ok=38 fail=0`; `METADATA_COMPLETE=1/1`,
`RESEARCH_GATE: CLEAN`; `rev_match=5/5`, `SEARCH_RERUN: CLEAN`; controls

    POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 NEW_ONLY=1/1 FORGERY_REFUSED=12/12 IDENTITY=1/1 FIELD_SCOPED=15/15 ACCEPTED=2/2 QUESTION_LINES_HELD=36/36 BASE_HELD=16/36 ELEMENTS=7+6/7+6 WARRANTS_OK=10/10 LANE_FILLED=10/10
    ENTRY_CONTROLS_R98=PASS

Kill rules K1-K5 unchanged; K2 now reads "an S231 quote other than M1 is not inside `abstractText`, or M1 is not the
record's title". Named limits unchanged except (a): S231 is the abstract and title, read through Europe PMC's index
record, tier B.
