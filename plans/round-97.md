# Round 97 plan — chousa (L1 `ChousaR97`, attempt 1)

Base `c8087ac529003e667505bcc624f9a7bde0cffbce` (round-96 landing; the round-96 non-author spot-check
`corpus/lessons/round-96-verifier-spotcheck.md` is on the lane). Round-96 closure: admitted (operability improved,
depth improved). No fresh-start rule binds this round; the §9 rules do: each claim beats a committed do-nothing
control, scored by the frozen counter, before the freeze (`corpus/evidence/round97/before/`).

## Why these claims

- SCORECARD `## Planned — round 97` item 1 (operability, the lowest axis): close the self-test's measured blind
  spots — `R96MutantsC1` class C (signed hits, bad dates, uppercase hex, two-code rows, non-UTF-8, `//` globs,
  trailing commas, literal-filename static dirs, glob-longer-than-path) and class B (a fixture-breaking mutant
  crashes with a traceback instead of printing FAIL), and `R96SentinelC1` F1/F7 (`git_env` guards). C1 takes it,
  scored against those seats' own mutants read from committed round-96 bytes, so the target is set by a non-author
  and the base tool's 10/30 is the do-nothing score. Not taken: the F2 NO_WRITE baseline is rebuilt (battery-start
  status + diff digest) but is not a claim; the `verify`↔`evaluate` tie (§Aa) stays a named limit.
- Planned item 2 (depth): the PRESS 2015 checklist's own wording. Every primary route answered 403 from this host
  (CADTH E&E, CADTH Table 9 and 10, J Clin Epidemiol, core.ac.uk) and `web.archive.org` refused TCP; two reachable
  reprints were found (Cochrane editors' checklist PDF; Karolinska library page). C2 holds the checklist questions
  through the stronger reprint (S225, B) and measures how far the second (S226, C) agrees — the disagreement is
  itself a finding the round-96 abstract-level reading could not show.
- Item 3 (carried debt) stays carried; see `## Routed defects`.

## Pre-freeze fixes (before any seat scored)

- **P0** — the first battery run crashed in setup: `ast.literal_eval` cannot read `n08`'s old string, which the
  round-96 probe writes as `r'...' + "\n"`. The battery's reader now accepts `str + str` and nothing else; n08 is
  still excluded (it applied 0 times in round 96).
- **P1** — the first C2 controls run failed `g2`: the forged "line join" (L21 + the next words) is in fact on the
  same capture line, so the gate correctly accepted it. `g2` now joins capture line 36 to line 38 skipping 37
  (`QUOTE_ABSENT`). The run also showed `gate-records.py` would accept a quote joined across *adjacent* lines
  (it matches the whitespace-collapsed whole text), so a ONE_LINE binding was added inside POSITIVE.
- **P2** — a SKILL.md checklist item for the new entry was drafted at line 86 and removed: it shifted the Gates
  table by two lines and broke the round-96 correction's `SKILL.md:180` pointer. The round-97 note is a
  `correction:` line after the round-96 one instead, and adds no line above row 180.

## Routed defects from the round-96 spot-check

- D1 (refetch id collision: the J Clin Epidemiol 403 row carries id `S224`) → **not written this round**. The TSV is
  read by `tools/gate-records.py`, `tools/capture-fetch.py` and `tools/store-record-audit.py`; a correction row of
  a new shape has not been shown safe for all three. Recorded in `LOG.md` as an open correction with the parser
  question; S227 this round was registered before any `## Gate` record cites it, so the round-96 mistake does not
  repeat.
- D2 → C1.
- D3 (four gate-kind tools with no `--selftest`) → carried.

## Wave

One v1 wave of 12 seats, attack share ≥25 %. L1 holds the canonical planner seat.

## Amendments after the freeze — re-frozen at F2 (wave-forced; every one cites the seat artifact that forces it)

The claims are judged at F2 on the amended sentences and predicates in `.ufo/waves/round-97/claims.md`
§ Amendments; the F text stays as the F record. Seat artifacts are under `.ufo/waves/round-97/w1/`.

C1 (`tools/search-rerun.py`, `corpus/evidence/round97/selftest-controls-r97.py`):

- **A1 (`R97ConnectorSiblings` n30 witness, `R97ConnectorSiblings-n30-witness.txt`).** F excluded `n30-sep-row-lenient`
  as equivalent on `R96MutantsC1`'s word; a 7-cell separator is refused `TABLE` by the tool and parsed by the
  mutant, so the exclusion was false and n30 survived F's self-test. F2 adds case `r16-sep-width` and scores n30.
- **A2 (`R97ScribeLesson` F3, `R97ScribeLesson-unguarded-residue.txt`).** F guarded case bodies only; an exception in
  shared set-up (`git_env`, `st_row`) or in `case` after its guard still ended the run with a traceback and no
  summary. F2 moves every case and its fixtures into `_selftest_cases`, called inside an outer guard that records a
  `setup` FAIL; the seat's three set-up mutants are scored as `x1`-`x3` (x2 anchored on the return-line prefix that
  base and F share, so the do-nothing leg applies it too).
- **A3 (`R97ReviewerC1` finding 2).** "print no traceback" reads "print no `Traceback` on stderr" — what the kill rule
  checks.
- **A4 (`R97CriticClaims` F4, `R97CriticClaims-c1-hashself-standin-full.txt`).** A self-test that hashes its own
  source and prints only the summary passed every F tally. F2's POSITIVE requires the 48 named case lines in order,
  and a kill must name a failing case (or `setup`). The sentence says "prints 48 named case lines", not "runs 48
  cases"; a self-test that forges the case lines without computing them is named limit (g).
- **A5 (`R97CriticClaims` F5; `R97ReviewerC1` finding 1).** The battery docstring's "read from the committed round-96
  bytes (never retyped here)" covers the `R96MutantsC1` set only; s1, s2 and x1-x3 are transcriptions. The tool's
  module docstring still described the 32-case self-test; updated.

C2 (`corpus/knowledge/press-checklist-questions-r97.md`, `corpus/SOURCES.md` S225/S226, `entry-controls-r97.py`):

- **B1 (`R97ReviewerC2` F1, `R97ScoutSources` F-C1, `R97CriticClaims` F1).** The Citing row's Lane cell said 12 S225
  quotes are not found verbatim; it is 16 (12 is the *letters* miss count). Repaired, and the F2 controls check the
  Lane cell's numbers against the recount (CORROBORATION 3/3, with the F error as its forgery).
- **B2 (`R97ReviewerC2` F2-F3, `R97ScoutSources` F-C2, `R97CriticClaims` F2).** The 12 letters-misses are 6 headings,
  2 pointer/title lines and 4 wording differences (not 5/1/1/5), L26 is found under letters, and the headings miss
  only because of their numbers (20/26 with digits deleted). Paragraph rewritten.
- **B3 (`R97ReviewerC2` F4).** Row 2 Lane cell: `hits` counts files, not hits per line; the lane does not meet that
  question. Rewritten.
- **B4 (`R97ReviewerC2` F5).** Row 4 Lane cell: the capture store does hold text about controlled vocabularies;
  narrowed to the lane's searches, and "a record says so" withdrawn (no such record exists — a gap).
- **B5 (`R97ReviewerC2` F8, `R97ScoutSources` F-C6).** Never cells of rows 1, 2, 5 and 8 said more than their
  warrants; rows 1, 2, 5 now restate the warrant's question negatively, row 8 reads "(none stated by the sources)".
  No row withdrawn; the row count stays 8.
- **B6 (`R97ReviewerC2` F6, `R97ScoutSources` F-Q1).** L21/L22: one 30-word question on line 73 (`sed` count), not
  32 words on line 74 (Python `splitlines()` also breaks at the form feed, which is where 74 came from).
- **B7 (`R97ReviewerC2` F7).** S225's anchor cell: the checklist heading and element 1 are on text-form page 1, not
  page 2.
- **B8 (`R97ScoutSources` F-P1, F-C3, F-C5).** "the CADTH Table 9 that both reprints derive from" and "independent
  reprint" were unsupported: S225 cites the J Clin Epidemiol statement, S226 links CADTH's 2016 report; coverage is
  16 of S225's 33 question lines. Entry prose and S226's scope cell narrowed.
- **B9 (`R97MutantsC2` F2).** "never as a row's only support" exceeds SOLE_SUPPORT, which checks that a row names an
  S225 quote; the sentence now says that.
- **B10 (`R97CriticClaims` F3, `R97MutantsC2` F1).** Never cells are not instrument-checked and a Do cell that
  inverts its quote while sharing a word passes WARRANT_TERMS; both are named limits, faithfulness stays the
  reviewer's item (B5 is its repair).

Routed-defect correction (`R97RevenPrior` Q3): the plan's reason for not writing D1 ("a correction row of a new shape
has not been shown safe for all three readers") is wrong — a 9-field row under a fresh id breaks none of the
readers (scratch-tested). The refusal stands for a different reason: no append-only row withdraws the wrong `S224`
row, because `gate-records.py` accepts any matching row; D1 needs a reader rule, not a row.
