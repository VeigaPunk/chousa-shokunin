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
