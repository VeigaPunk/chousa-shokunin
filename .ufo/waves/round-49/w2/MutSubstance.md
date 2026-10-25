# MutSubstance — R49 W2 (FALSIFY) mutation probe: quote-substance-check + capture-age-check

Attacked item: the two W1-review behavioral checks
`corpus/evidence/round49/quote-substance-check.py` and `corpus/evidence/round49/capture-age-check.py`
(lane checkout clean vs tip: `git status --porcelain -- corpus/evidence/round49/` → empty; blobs at master
87e93353: quote-substance `1aa3a5d809f17cb428c3f4e7b94a08b640b1eb0c`, capture-age `37722c8625dcada63b9d20ac79d8e407b6d4714a`).
Method: all scripts run from /dev/shm copies; lane bytes only hashed. Mutants built by exact-once
`str.replace` (asserted unique) on copies — smallest behavior-bearing points: thresholds, overwide
test, exit conjunction, per-line conjunction terms, case-insensitivity. Detector = the scripts
themselves on fixed scratch inputs; pristine runs are the baseline (all baselines behaved as
documented, so no run is inconclusive).

## Scratch fixtures (all in /dev/shm/chousa-r49-MutSubstance/, deleted after)
Manifests: `id url sha off span_file quote entry` TSV with header. Quote `q`="Aggregator page cited
no source." (32 raw chars / 28 non-space). s_small=60B, s_wide=200B, s_bound=194B (=32+2·80+2 exact bound).
- m_all.tsv: S_HOL(" "+q), S_TWO("ab"+q), S_SHORT("abcdefgh" 8ns only), S_WIDE(q, s_wide) — one defect class per id
- m_edge.tsv (clean control, pristine exit 0): S_THREE("abc"+q), S_TWELVE("abcdefghijkl" exactly 12ns), S_BOUND(q, s_bound), S_OK(q, s_small)
- single-defect: m_hol, m_two, m_short, m_wide (one id each)
Reports: r_nodate("freshness: newest capture reviewed this week" + "Report compiled 2026-10-25."),
r_nocapture("freshness: newest fetch 2026-01-15"), r_nofresh("newest capture 2026-10-25"),
r_ok("freshness: newest capture 2026-10-25"), r_case("Freshness: newest capture 2026-10-25").

## Pristine baselines (harness echoes; scripts are byte-copies of the lane files)
```
$ python3 harness.py
$ python3 qs_pristine.py m_all.tsv   -> exit=1 :: HOLLOW_QUOTE S_HOL; HOLLOW_QUOTE S_TWO; OVERWIDE_SPAN S_WIDE; NO_SUBSTANTIVE_QUOTE S_SHORT :: IDS=4 QUOTES=6 FAILURES=4
$ python3 qs_pristine.py m_edge.tsv  -> exit=0 :: (no failure lines) :: IDS=4 QUOTES=5 FAILURES=0
$ python3 qs_pristine.py m_hol.tsv   -> exit=1 :: HOLLOW_QUOTE S_HOL :: IDS=1 QUOTES=2 FAILURES=1
$ python3 qs_pristine.py m_two.tsv   -> exit=1 :: HOLLOW_QUOTE S_TWO :: IDS=1 QUOTES=2 FAILURES=1
$ python3 qs_pristine.py m_short.tsv -> exit=1 :: NO_SUBSTANTIVE_QUOTE S_SHORT :: IDS=1 QUOTES=1 FAILURES=1
$ python3 qs_pristine.py m_wide.tsv  -> exit=1 :: OVERWIDE_SPAN S_WIDE :: IDS=1 QUOTES=1 FAILURES=1
verbatim m_all.tsv:
HOLLOW_QUOTE S_HOL ' '
HOLLOW_QUOTE S_TWO 'ab'
OVERWIDE_SPAN S_WIDE s_wide.txt len=200
NO_SUBSTANTIVE_QUOTE S_SHORT longest=8
IDS=4 QUOTES=6 FAILURES=4
exit=1
$ python3 ca_pristine.py r_nodate.txt    -> exit=1 :: FRESHNESS_CAPTURE_AGE=FAIL
$ python3 ca_pristine.py r_nocapture.txt -> exit=1 :: FRESHNESS_CAPTURE_AGE=FAIL
$ python3 ca_pristine.py r_nofresh.txt   -> exit=1 :: FRESHNESS_CAPTURE_AGE=FAIL
$ python3 ca_pristine.py r_ok.txt        -> exit=0 :: FRESHNESS_CAPTURE_AGE=PASS
$ python3 ca_pristine.py r_case.txt      -> exit=0 :: FRESHNESS_CAPTURE_AGE=PASS
verbatim r_nodate.txt:
FRESHNESS_CAPTURE_AGE=FAIL
exit=1
```
Baseline note: all four W1 CritForgeC2 defect classes are caught by pristine (single-space quote →
HOLLOW_QUOTE S_HOL `' '`; whole-capture span → OVERWIDE_SPAN; all-short id → NO_SUBSTANTIVE_QUOTE).

## Mutants — quote-substance-check.py (line refs to lane file)
| mutant (old→new) | verdict | misclassified inputs |
|---|---|---|
| QM1 `MIN_CHARS = 3`→`1` (:26) | KILLED | m_two: exit 1→0 — accepts the 2-char quote; m_all: HOLLOW S_HOL line silently dropped |
| QM2 `MIN_CHARS = 3`→`4` (:26) | KILLED | m_edge: exit 0→1, false `HOLLOW_QUOTE S_THREE` on the 3-char boundary quote |
| QM3 `LONG_CHARS = 12`→`1` (:27) | KILLED | m_short: exit 1→0 — accepts id whose longest quote is 8 chars; m_all: NO_SUBST line dropped |
| QM4 `LONG_CHARS = 12`→`13` (:27) | KILLED | m_edge: exit 0→1, false `NO_SUBSTANTIVE_QUOTE S_TWELVE` (exactly 12) |
| QM5 `CONTEXT = 80`→`400` (:28) | KILLED | m_wide: exit 1→0 — accepts the 200B overwide span; m_all: OVERWIDE line dropped |
| QM6 overwide `>`→`>=` (:56) | KILLED | m_edge: exit 0→1, false `OVERWIDE_SPAN S_BOUND` at the exact 194B bound |
| QM7 `return 1 if bad else 0`→`1 if bad > 2 else 0` (:64) | KILLED | m_hol/m_two/m_short/m_wide: exit 1→0 with the failure line still printed — every single-leg defect passes |

Observed evidence for the conjunction mutant (representative kills):
```
QM7 exit-conjunction bad>2  KILLED
   m_hol.tsv: pristine exit=1 -> mutant exit=0 [ACCEPTS-DEFECT] :: HOLLOW_QUOTE S_HOL
   m_short.tsv: pristine exit=1 -> mutant exit=0 [ACCEPTS-DEFECT] :: NO_SUBSTANTIVE_QUOTE S_SHORT
```

## Mutants — capture-age-check.py (conjunction at :24-25)
| mutant | verdict | misclassified inputs |
|---|---|---|
| CA1 capture term→`True` | KILLED | r_nocapture: FAIL→PASS — freshness+date line passes without "capture" |
| CA2 freshness term→`True` | KILLED | r_nofresh: FAIL→PASS — capture+date line passes without "freshness" |
| CA3 date term→`True` | KILLED | r_nodate: FAIL→PASS — freshness+capture line passes with no ISO date |
| CA4 all three terms scoped to whole text, not per-line | KILLED | r_nodate: FAIL→PASS — line 1 has freshness+capture, line 2 carries the date; the same-line conjunction is load-bearing |
| CA5 drop `(?i)` on freshness | KILLED | r_case ("Freshness:"): PASS→FAIL — false rejection of a correct report |

Observed evidence:
```
CA4 per-text not per-line  KILLED
   r_nodate.txt: pristine exit=1 -> mutant exit=0 [ACCEPTS-DEFECT] :: FRESHNESS_CAPTURE_AGE=PASS
CA5 drop (?i) on freshness  KILLED
   r_case.txt: pristine exit=0 -> mutant exit=1 [REJECTS-CLEAN] :: FRESHNESS_CAPTURE_AGE=FAIL
```

## Survivors
None. All 12 mutants killed by at least one scratch input; no input left a mutant
indistinguishable from pristine.

## Findings
1. Both checks hold under this probe: every probed mutation point (both thresholds, the overwide
   comparison, the exit conjunction, all three per-line terms, case-insensitivity) changes the
   verdict on at least one of the required input classes, and pristine classifies all fixtures
   exactly as documented (docstring lines 8-12 / capture-age lines 4-7).
2. Calibration caveat (QM7): the QS exit verdict collapses three independent legs into one `bad`
   counter. On a multi-defect manifest (m_all, 4 failures) the broken-conjunction mutant is
   invisible (exit stays 1); only isolated single-defect fixtures kill it. Any future detector
   that judges this script by exit code alone should keep per-leg fixtures.
3. Boundary semantics confirmed: the overwide test compares raw `len(quote)` (spaces included),
   bound = len(quote)+2·80+2; a span of exactly 194B for a 32-char quote passes (`>` strict, :56)
   and is only rejected by the `>=` mutant.
4. Scope note: this check is a substance floor, not entailment — W1's "self-consistent anchor"
   class is explicitly out of its contract (docstring: "a long quote can still be beside the
   point"); not a defect.

## Restoration evidence
```
BEFORE sha256 quote-substance-check.py=801cb32b60c72b2d0cff066668fb6c92331733363756a6278595bac4c1f98c10
BEFORE sha256 capture-age-check.py=81009fafb1238ab20ed8d66c6c5611ed487aac44baffefe053ee664201f12b45
AFTER  sha256 quote-substance-check.py=801cb32b60c72b2d0cff066668fb6c92331733363756a6278595bac4c1f98c10
AFTER  sha256 capture-age-check.py=81009fafb1238ab20ed8d66c6c5611ed487aac44baffefe053ee664201f12b45
LANE-BYTES-UNCHANGED=True
```
Mutants lived only at /dev/shm/chousa-r49-MutSubstance/{QM1..QM7,CA1..CA5,qs_pristine,ca_pristine}.py;
scratch removed at end (`rm -rf /dev/shm/chousa-r49-MutSubstance`, verified absent). No installs
performed (RULES.md channels noted; none needed). No network, no counters run, no subagents.
