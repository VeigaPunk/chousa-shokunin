# MutC2V2Counter — round 62 w1 — mutation test of `c2v2-count.py` against the 20-control matrix

Seat: mutation-tester (leaf). Target: `corpus/evidence/round62/c2v2-count.py`, sha256 prefix `817d5fc0b94e9fc8`, unchanged after the run. Matrix: `corpus/evidence/round62/controls/run-c2v2-controls.py`, prefix `f4b175c0056c134a`, unchanged. Each mutant ran in a scratch lane copy (corpus minus evidence, plus controls, plus mutant counter); the lane was read-only. No tool installed. Scratch removed.

## Findings

1. **The matrix kills 13 of 40 non-equivalent mutants; 27 survive.** Kill = at least one of the 20 FAIL-expected variants (`absent`, `no-entry-rows`, 18 single-defect variants) reads PASS. The two PASS-expected variants (`positive`, `non-sequitur`) did not change the count. Line numbers below refer to the frozen counter.

2. **23 of the 27 survivors are demonstrated gaps.** For each, I built a witness tree: the positive entry and rows with one targeted edit. Frozen counter: FAIL. Single-check mutant: PASS. Only the mutated check differs, so the divergence is attributable to it. The frozen controls contain no input that exercises that check alone. The frozen counter is not shown wrong: each mutant departs from the docstring predicate, and the matrix does not pin the predicate. Example W01 (4 claims): frozen `CLAIMS=0/1 ECHO=0/1 C2=FAIL`; mutant `C2=PASS`.

3. **Redundant sub-checks hide each other from the matrix.** `echo-claim` has 1 fresh word of 6, so ECHO's ratio test and its absolute-3 test each fail it alone; removing either keeps the control at FAIL (M14, M16 survive). `quote-wrong-anchor` fails both anchor checks (row cell, text) (M02, M03 survive). The probe leg's exit-code check (M17) and PROBE_FACTS k=n check (M20) survive: no control has a nonzero probe exit or a k≠n line.

4. **Whole check families have no control.** COVERAGE per-row minima (M11–M13), CLAIMS and LIMITS minima (M26–M28), CENSUS (M31), TRIO (M32, M33), ROWS tier (M34), word-length (M40) and S138 binding (M37) have no failing control. The S139 "any file" mutant (M36) survives because `s139-wrong-file` fails on quotes, not on the binding.

5. **Operability: one unexplained transient in the positive control.** In the first parallel run (8 matrices at once), M29's `positive` read `PROBE=0/1`, `UNEXPECTED`. Not reproduced: M29 rerun serially, 0 unexpected and `positive` PASS; 8 identity matrices run in parallel, 8/8 with `C2V2_CONTROLS_UNEXPECTED=0`; 16 concurrent direct runs of `candidate-openat2-probe.py`, all `PROBE_FACTS=14/14`. Detail lines for that run were not kept, so cause is unknown. Rate: 1 failure in about 51 positive-control runs. I do not count it as a kill for M29. INFERENCE: load- or timing-sensitive probe output. L1 should watch for PROBE flips in the positive control.

6. **Harness calibration gap.** `run-c2v2-controls.py` line 78 maps any nonzero exit to FAIL (`got = "PASS" if p.returncode == 0 else "FAIL"`), so a counter that crashes on a control reads as a correct FAIL. INFERENCE from code; I did not run a crash mutant.

7. **Equivalent mutant, excluded.** M39 (claims may cite unknown quote ids): any unknown cite puts it into `cited`, so `cited == set(quotes)` fails in both versions. C2 verdict is identical. Only the ECHO sub-result differs.

## Mutant table

Killed by the 20 FAIL-expected controls (13):

| id | frozen line | mutation | killing control(s) |
|---|---|---|---|
| M01 | 176 | quote anchor not checked | quote-wrong-anchor |
| M04 | 157 | opened lower bound dropped | row-opened-old |
| M05 | 60 | MIN_OPENED 2026-10-27 | row-opened-old |
| M06 | 158 | used-by check dropped | row-not-used-by |
| M08 | 176 | quote upper cap dropped | quote-over-25 |
| M18 | 224 | probe line comparison dropped | probe-output-edited, probe-output-stale |
| M19 | 223 | probe live output replaced by committed file | probe-output-edited, probe-output-stale |
| M21 | 121 | HEADER lines dropped from probe compare | probe-output-stale |
| M23 | 237 | MAP always passes | map-missing |
| M25 | 213 | [INFERENCE] requirement dropped | limits-no-inference |
| M30 | 209 | every-quote-cited check dropped | quote-uncited |
| M35 | 100 | S139 cell binding dropped | s139-wrong-file |
| M41 | 174 | quote found checks first word only | fabricated-quote |

Survived all 20 (27 non-equivalent). Witness column: original FAIL, mutant PASS on a one-edit tree.

| id | frozen line | mutation | witness |
|---|---|---|---|
| M02 | 175 | anchor row-cell check dropped | W18 DEMO (anchor `RESOLVE_NO_XDEV` in text only) |
| M03 | 175 | anchor resolved-text check dropped | W19 DEMO (anchor `round` in row only) |
| M07 | 156 | used-by basename only | W15 DEMO (used-by names `old-openat2-resolve-r62.md`) |
| M09 | 176 | quote cap 25 → 30 | W03 DEMO (29-word quote) |
| M10 | 176 | quote minimum 4 → 1 | W04 DEMO (2-word quote) |
| M11 | 183 | COVERAGE per-row minima dropped | W05 DEMO (S139 has zero quotes) |
| M12 | 59 | S138 minimum 3 → 1 | W16 DEMO (S138 has two quotes) |
| M13 | 59 | S140 minimum 2 → 0 | not witnessed (same line as M12) |
| M14 | 206 | ECHO ratio dropped | W10 DEMO (4 fresh of 18 = 22%) |
| M15 | 206 | ECHO ratio 0.3 → 0.2 | W10 DEMO (22%) |
| M16 | 206 | ECHO absolute-3 dropped | W11 DEMO (2 fresh of 6 = 33%) |
| M17 | 225 | probe exit code ignored | W21 DEMO (probe exits 3, output correct) |
| M20 | 225 | PROBE_FACTS k=n dropped | W20 DEMO (14/15, live and committed) |
| M22 | 224 | probe compare order-insensitive | W13 DEMO (P01/P02 swapped) |
| M24 | 237 | MAP matches basename only | W14 DEMO |
| M26 | 213 | LIMITS 3 → 2 | W02 DEMO (2 bullets) |
| M27 | 186 | CLAIMS 5 → 4 | W01 DEMO (4 claims) |
| M28 | 186 | CLAIMS 5 → 1 | not witnessed (same line as M27) |
| M29 | 202 | claim shared-word minimum 2 → 1 | W17 DEMO (1 shared word) |
| M31 | 240 | CENSUS always passes | W06 DEMO (malformed registry row) |
| M32 | 144 | TRIO requires S138 only | W08 DEMO (source line without S140) |
| M33 | 141 | TRIO head 12 lines → whole file | W22 DEMO (`source:` at line 13) |
| M34 | 157 | ROWS tier check dropped | W07 DEMO (S138 tier B) |
| M36 | 99 | S139 resolves to any /usr/include header | not witnessed |
| M37 | 97 | S138 cell binding dropped | W12 DEMO (S138 cell lacks man path) |
| M38 | 176 | duplicate quote ids accepted | W09 DEMO (Q2 twice) |
| M40 | 117 | word length 5 → 6 letters | not witnessed |

Not witnessed (4): M13, M28, M36, M40. Coverage by analogy to witnessed lines is INFERENCE.

Identity (unmutated copy): `C2V2_CONTROLS_UNEXPECTED=0`, 22 variants read as expected.

## Reproduction

Per mutant: copy `corpus/` minus `evidence`, `captures`, `fixtures`; copy `controls/` to `corpus/evidence/round62/controls/`; write the mutant (one `str.replace` with count 1 on the frozen source, at the line above) to `corpus/evidence/round62/c2v2-count.py`; give a fleet dir containing a `scripts` symlink. Run `python3 -B corpus/evidence/round62/controls/run-c2v2-controls.py --work <absent dir>`. Mutant kill = any FAIL-expected variant reading `UNEXPECTED`. Witness = copy of positive tree with one edit, run through original and mutant with `--root`.

## Limits of this seat

Single-point mutants only; no combinations. Witnesses are authored by this seat and test one check each. The probe ran on one host. The `non-sequitur` named limit is untouched. Entailment is not tested. The one transient in finding 5 is not explained.

VERDICT: C2_MUTANTS_KILLED=13/40 control_gaps=27
