# R90ExecC2Repro — C2 reproduction from a clean tree (round 90, wave 1)

Seat `R90ExecC2Repro`, leaf. Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Tree attacked: `9bad12011187d114ba2c4588c5df08a21ab28145` (freeze `8d9893b42eb22690ea5f920ab87fd7e1810b847a`
plus the committed control receipts). Frozen predicates read first:
`corpus/evidence/round90/claims.md` and `plans/round-90.md`.

Scratch (deleted before yield): `/fast/scratch/hyaku/chousa-r90/R90ExecC2Repro`.
Tree extracted with `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 9bad12011187d114ba2c4588c5df08a21ab28145 | tar -x -C $S`
(cwd `$S` for every run; `TMPDIR=$S/tmp`; network not used; no sudo, no pacman, no tool installs).
`python3 -V` → `Python 3.14.8`.

Instrument bytes exercised (sha256, from the extracted tree):

```
28dc1152b0ac1fb67dcca47ff618313c8d2268fecdb5d7967483f8ad128be90a  corpus/evidence/round90/curation-r90.py
58d64f793ad02da910bdf2f6317a4069a8adf1baf9f29d2de903069001a3d10b  corpus/evidence/round90/curation-r90-mutants.py
6f180ec1e3922766a29d5316ed4dd3ea8e37bec40cf9366c94ca0a3ff40eee7c  corpus/evidence/round90/curation-r90-controls.py
2c063f8bfab6922d199546494d2545f495b05ab9350a7379e1b7f4cde8939f4b  corpus/evidence/round89/curation-r89.py
```

---

## (a) `curation-r90.py` — passing path

Command (cwd `$S`):

```
python3 -B corpus/evidence/round90/curation-r90.py --root . > $S/out/a-transcript.txt 2>&1
```

Exit: **0**. Transcript copied to `a-transcript.txt` (this folder). Full output:

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=10/10 VERDICT fields_hold=1
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8
CURATION_R90=PASS
```

`grep -c 'VERDICT fields_hold=1' $S/out/a-transcript.txt` → **2** (exit 0). The two hits are the summary
line's tail and the verdict line; both print the same `fields_hold` variable, so the token pair is the
measured value, not a constant.

Token assertions over the transcript (scripted `in` test, all `HAS`):

```
HAS CURATION_R90=PASS          HAS LEGS_MEASURED=10/10      HAS VERDICT fields_hold=1
HAS DETECTOR_WITNESS=8/8       HAS DUP_QIDS=0               HAS WARRANT_OK=17/17
HAS QUOTES_LOCATED=20/20       HAS TEACHES_FLAGGED=1        HAS TEACHES_UNRESOLVED=0
HAS SUP_CLAUSE_CHECKED=0       HAS SUP_UNRESOLVED=0
LEG_FAIL lines: 0              CURATION_R90=PASS occurrences: 1
```

Matches the frozen sentence exactly.

Source cross-check (`curation-r90.py`, read at the extracted tree): `EXPECTED_LEGS = 10`; legs appended in
order FLOOR, SUPERSEDED, UNENTAILED, DEF_CITED, WARRANT, TEACHES, SETUP, DUPQID, WITNESS, then VERDICT
(`legs.append(("VERDICT", fields_hold and fields_hold == prior_ok, ...))` at line 348, before the summary
print at 355-357); `passed = (len(legs) == EXPECTED_LEGS and all(ok ...) and fields_hold)`. `witness()` has
eight assertions (locate/unentailed/teaches/dup × fire+silent) and `witness_bad` is inside `fields_hold`,
so `DETECTOR_WITNESS=8/8` is a term of the verdict.

## (b) `curation-r90-mutants.py` — mutation battery

Command (cwd `$S`):

```
python3 -B corpus/evidence/round90/curation-r90-mutants.py --root . --work $S/mut > $S/out/b-transcript.txt 2>&1
```

Exit: **0**. Transcript copied to `b-transcript.txt`. Full output:

```
KILLED M1-dead-teaches tree=base rc=1 CURATION_R90=FAIL
  LEG_FAIL TEACHES checked=1 flagged=0 unresolved=0 sup_unresolved=0
  LEG_FAIL VERDICT fields_hold=0 legs_ok=8/9
KILLED M2-detached-leg tree=s031-queued rc=1 CURATION_R90=FAIL
  LEG_FAIL VERDICT fields_hold=0 legs_ok=9/9
KILLED M3-verdict-legs tree=s031-queued rc=1 CURATION_R90=FAIL
  LEG_FAIL VERDICT fields_hold=0 legs_ok=9/9
KILLED M4a-dup-leg-forced tree=dup-qid rc=1 CURATION_R90=FAIL
  LEG_FAIL VERDICT fields_hold=0 legs_ok=9/9
KILLED M4b-dup-field-dropped tree=dup-qid rc=1 CURATION_R90=FAIL
  LEG_FAIL DUPQID provenance-recording-r85.md Naming what a resource derives from warrant=Q1, Q1 (S215)
  LEG_FAIL VERDICT fields_hold=1 legs_ok=8/9
KILLED M5-lowercase-clause tree=sup-mirror detector=battery rc=1
  CASE_DEVIATION SUP-clause-mirror: NOT refused by both counters
KILLED M6-locate-true tree=base rc=1 CURATION_R90=FAIL
  LEG_FAIL WITNESS 7/8 bad=1
  LEG_FAIL VERDICT fields_hold=0 legs_ok=8/9
KILLED M7-unentailed-empty tree=base rc=1 CURATION_R90=FAIL
  LEG_FAIL WITNESS 7/8 bad=1
  LEG_FAIL VERDICT fields_hold=0 legs_ok=8/9
KILLED M8-teaches-never-fires tree=base rc=1 CURATION_R90=FAIL
  LEG_FAIL TEACHES checked=1 flagged=0 unresolved=0 sup_unresolved=0
  LEG_FAIL WITNESS 7/8 bad=1
  LEG_FAIL VERDICT fields_hold=0 legs_ok=7/9
KILLED M9-dup-dead tree=base rc=1 CURATION_R90=FAIL
  LEG_FAIL WITNESS 7/8 bad=1
  LEG_FAIL VERDICT fields_hold=0 legs_ok=8/9
SURVIVOR_PRIOR r89-subst-0 rc=0
SURVIVOR_PRIOR r89-subst-1 rc=0
MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2
```

`KILLED ` lines: 10. `SURVIVOR_PRIOR` lines: exactly two, both `rc=0`. Summary is the frozen one:
`MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2`.

The two prior survivors are the round-89 constant substitutions the freeze names: `locates` forced true
(`if cap is not None and norm(quote) in cap:` → `… and True:`) and `unentailed_row` forced false
(`… and term not in joined:` → `… and False:`), applied by the battery at
`curation-r90-mutants.py:200-218`. The round-90 counterparts M6-locate-true and M7-unentailed-empty die on
`LEG_FAIL WITNESS 7/8 bad=1`.

## (c) `curation-r90-controls.py` — tree-forgery controls

Command (cwd `$S`):

```
python3 -B corpus/evidence/round90/curation-r90-controls.py --root . --work $S/ctl > $S/out/c-transcript.txt 2>&1
```

Exit: **0**. Transcript copied to `c-transcript.txt`. Every case line, plus the summary:

```
OK POSITIVE: positive accepted by both
  r90: rc=0 CURATION_R90=PASS
  prior: rc=0 CURATION_R89=PASS
OK A1c-junk-substitute: refused by r90 (LEG_FAIL FLOOR search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7), refused by the prior counter (regression held)
  r90: rc=1 CURATION_R90=FAIL
  prior: rc=1 CURATION_R89=FAIL
OK A1d-truncate: refused by r90 (LEG_FAIL FLOOR search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7), refused by the prior counter (regression held)
  r90: rc=1 CURATION_R90=FAIL
  prior: rc=1 CURATION_R89=FAIL
OK caseG-relabel: refused by r90 (LEG_FAIL FLOOR search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7), refused by the prior counter (regression held)
  r90: rc=1 CURATION_R90=FAIL
  prior: rc=1 CURATION_R89=FAIL
OK F2-rejected-superseder: refused by r90 (LEG_FAIL TEACHES checked=1 flagged=1 unresolved=1 sup_unresolved=0), refused by the prior counter (regression held)
  r90: rc=1 CURATION_R90=FAIL
  prior: rc=1 CURATION_R89=FAIL
OK B1b-padding-qid: refused by r90 (LEG_FAIL WARRANT 16/17), refused by the prior counter (regression held)
  r90: rc=1 CURATION_R90=FAIL
  prior: rc=1 CURATION_R89=FAIL
OK D1-duplicate-qid: refused by r90 (LEG_FAIL DUPQID provenance-recording-r85.md Naming what a resource derives from warrant=Q1, Q1 (S215)), refused by the prior counter (regression held)
  r90: rc=1 CURATION_R90=FAIL
  prior: rc=1 CURATION_R89=FAIL
OK SUP-clause-mirror: refused by r90 (LEG_FAIL TEACHES checked=2 flagged=2 unresolved=0 sup_unresolved=1), refused by the prior counter (regression held)
  r90: rc=1 CURATION_R90=FAIL
  prior: rc=1 CURATION_R89=FAIL
FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7
CONTROLS=PASS
```

`OK ` lines: 8 (the positive + seven forgeries). Summary and exit match the freeze:
`CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7`, exit 0.

## (d) Before-state re-derivation

### d1 — round-89 counter passing path prints no verdict token

Command (cwd `$S`):

```
python3 -B corpus/evidence/round89/curation-r89.py --root . > $S/out/d-prior-transcript.txt 2>&1
```

Exit: **0**. Transcript copied to `d-prior-transcript.txt`. Output:

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=8/8
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
CURATION_R89=PASS
```

`grep -c 'VERDICT fields_hold=1' $S/out/d-prior-transcript.txt` → **0** (grep exit **1**, no match; recorded as
the counter-bound observation, not a failure of the leg). `grep -c 'VERDICT'` → **0**. So the round-89 passing
path prints `CURATION_R89=PASS` with `LEGS_MEASURED=8/8` and no `VERDICT fields_hold=1` token — Amendment 8's
before-state re-derived.

### d2 — the two round-89 substitutions still survive

The battery's `SURVIVOR_PRIOR r89-subst-0 rc=0` and `SURVIVOR_PRIOR r89-subst-1 rc=0` are the reproduction;
independently re-derived outside the battery by writing the two edited copies under `$S/sub` and running them
on the same base tree (`d-subst-transcript.txt`):

```
r89-subst-0 rc=0 verdict=CURATION_R89=PASS
  repeats consistently: True
r89-subst-1 rc=0 verdict=CURATION_R89=PASS
  repeats consistently: True
```

Both substitutions are byte-identical to the battery's edits; both still print `CURATION_R89=PASS` at exit 0,
so the round-89 counter is blind to both constants, and the round-90 counter kills both via `WITNESS`.

## Reproducibility and tree immutability

- Second runs of (a), (b), (c) into fresh `--work` dirs (`$S/mut2`, `$S/ctl2`) produced **byte-identical**
  transcripts (`diff` → `IDENTICAL_A`, `IDENTICAL_B`, `IDENTICAL_C`); exits `A2_EXIT=0`, `B2_EXIT=0`,
  `C2_EXIT=0`. Copies: `a2.txt`, `b2.txt`, `c2.txt`.
- After all runs, `diff -r` of `$S` against a fresh extraction of `9bad1201…` printed **`TREE_UNCHANGED`**:
  no instrument wrote into the tree; only the explicit `--work` directories changed.
- `corpus/evidence/round90/controls/receipts/c2-prior-landing.txt` (committed, `# computed_against=8d9893b4…`,
  `# exit=0`) carries the same `CURATION_R89=PASS` + `LEGS_MEASURED=8/8` body observed in d1; its
  `# expected_exit=0` agrees with the observed exit.

## Observations (recorded, not scored)

1. `grep -c 'VERDICT fields_hold=1'` over the r90 passing transcript is **2**, not 1: the summary line ends
   with `… LEGS_MEASURED=10/10 VERDICT fields_hold=1` and the verdict line repeats it. Both are the same
   `fields_hold` variable (`curation-r90.py:335-366`), so this does not weaken the predicate; it is reported
   because the freeze's before/after contrast (`0` → “an output line containing”) leaves the multiplicity
   unstated.
2. `corpus/evidence/round90/controls/receipts/c2-subst-before.txt` is the full mutant-battery transcript
   (kill lines plus the two `SURVIVOR_PRIOR` lines), not two bare `CURATION_R89=PASS` lines. It is a superset
   of the cited content and lacks the `# case=/# exit=/# computed_against=` header block; it is **not** a row
   of `controls/expected.tsv` (the six driver rows are `c1-gate-r89`, `c1-mutants-r89`, `c1-harm`,
   `c1-harm-setup`, `c2-prior-landing`, `c2-prior-controls`), so no receipt-header contract is broken by it.
   C1's scope; flagged here only because C2's before-state cites the file.
3. The receipts directory holds nine files while the driver's expectation table holds six rows — the three
   extras (`c1-prior-driver.txt`, `c2-subst-before.txt`, `c3-before.txt`) are before-evidence, not driver
   rows. C1's scope; noted for the receipt-count wording.

## Named limits touched

C2 limit (3): the witness exercises each detector function on synthetic strings; M6/M7 and the battery's
`SURVIVOR_PRIOR` pair exercise function bodies, and a substitution in a *caller* that bypasses the function
remains unwitnessed — outside this reproduction. C2 limit (4): `SUP_CLAUSE_CHECKED=0` reproduces the
vacuity on the real registry; its non-vacuity is only shown by the battery's `M5` mirror case
(`CASE_DEVIATION SUP-clause-mirror`), which is what `BATTERY_DETECTED=1` counts.

## Verifications not run (main agent owns post-integration gate)

No build, lint, formatter or selftest was run beyond the three C2 commands and the round-89 prior counter;
`tools/research-gate.sh` (C3's leg) is not exercised by this seat.

VERDICT: R90ExecC2Repro C2 held — from a clean `9bad1201…` tree the r90 counter exits 0 printing `CURATION_R90=PASS` with `LEGS_MEASURED=10/10`, `VERDICT fields_hold=1 … DETECTOR_WITNESS=8/8` and every carried field, the mutant battery prints `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2` at exit 0, the controls battery prints `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` at exit 0, and the r89 before-state re-derives (`CURATION_R89=PASS`, `LEGS_MEASURED=8/8`, `VERDICT fields_hold=1` count 0, both substitutions surviving at rc=0).
