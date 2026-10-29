# MutC2Counter — mutation test of the frozen C2 counter (round 63, w1)

Scope: mutate `corpus/evidence/round63/c2-count.py` in scratch copies, run each mutant through the frozen control
runner `controls/run-c2-controls.py` (scratch copy, `COUNTER` pointed at the mutant lane), report which variants flip.
Nothing under `corpus/evidence/round63/`, `tools/`, `corpus/`, or `SKILL.md` was written. Scratch
`/fast/scratch/hyaku/chousa-r63/MutC2Counter/` is removed before yield.

## Result

- Mutants: 18 (M01–M17, with M12b as a second M12 variant). Each differs from the frozen counter by one or two lines;
  all compile (`ast.parse` ok).
- Killed by the frozen 24-line runner: **11/18** (M01, M02, M03, M04, M07, M09, M10, M11, M12, M12b, M14).
- SURVIVED the frozen runner: **7/18** (M05, M06, M08, M13, M15, M16, M17).
- Each survivor is killed by one candidate control (below), tested on a scratch mirror of the positive entry. With all 7
  candidates added, 18/18 are killed; the candidates are NOT frozen and are not committed (routed as supplements, see
  "Routing").

Verdict line: `C2_MUTANTS_KILLED=11/18 control_gaps=7`

## Baseline (unmutated counter)

- `python3 -B run-c2-controls.py --work <absent> --fleet /home/vgpnk/Projects/shokunin` on the scratch lane
  reproduces the committed receipt: `diff` of its output against `controls/c2-controls.txt` (minus the `exit=` and
  wall-time lines) prints nothing (`BASE_RECEIPT_IDENTICAL`), and `C2_CONTROLS_UNEXPECTED=0`.
- Count note: the runner prints 25 lines. 24 are scored (positive, non-sequitur, openat2-on-lane = PASS; 21 defect/absent
  variants = FAIL, matching claims.md "21 FAIL variants in all"); `git-on-lane-base` is informational. The assignment
  said "23 variants"; the scored count is 24, and I used that.
- Frozen tree unchanged: `git -C <lane> status --porcelain -- corpus/evidence/round63 corpus/knowledge corpus/SOURCES.md
  tools SKILL.md` prints nothing; `sha256sum c2-count.py | cut -c1-16` = `606207e224c0b7cf` (claims.md digest).

## Mutants and frozen-runner flips

| id | mutation (frozen line) | frozen flip (variant that flips, rc) | verdict |
|---|---|---|---|
| M01 | anchor check dropped (L233) | quote-wrong-anchor: rc=0 C2=PASS | KILLED |
| M02 | opened >= 2026-10-28 dropped (L214) | row-opened-old: rc=0 | KILLED |
| M03 | used-by check dropped (L215) | row-not-used-by: rc=0 | KILLED |
| M04 | quote word cap 25 dropped (L233) | quote-over-25: rc=0 | KILLED |
| M05 | COVERAGE minimums -> 1 (L240) | none (s144-one-quote is in candidates only) | SURVIVED |
| M06 | ECHO 30 % ratio dropped (L263) | none (echo-ratio-only is candidate only) | SURVIVED |
| M07 | live-git binding in LIMITS dropped (L272) | limits-no-git-version: rc=0 | KILLED |
| M08 | live-git binding in PROBE dropped (L288) | none | SURVIVED |
| M09 | probe-lines comparison dropped (L287) | probe-output-edited: rc=0 | KILLED |
| M10 | MAP check dropped (L301) | map-missing: rc=0 | KILLED |
| M11 | `[INFERENCE]` requirement dropped (L271) | limits-no-inference: rc=0 | KILLED |
| M12 | S143 resolves to the S142 page, cell ignored (L122) | s143-wrong-file: rc=0 C2=PASS | KILLED |
| M12b | S143 resolves to the lane probe output (L122) | positive: rc=1; non-sequitur: rc=1 | KILLED |
| M13 | claims >= 5 -> >= 1 (L243) | none | SURVIVED |
| M14 | CLAIMS shared-word check dropped (L259) | junk-claim: rc=0 C2=PASS | KILLED |
| M15 | probe exit code / PROBE_FACTS dropped (L289) | none | SURVIVED |
| M16 | CENSUS check ignored (L304) | none | SURVIVED |
| M17 | TRIO requires S142-S144 in `source:` dropped (L201) | none | SURVIVED |

Frozen flip detail for the killed rows: each named variant printed `rc=0 ... C2=PASS` (or `rc=1` for M12b on the
positive) against an expected FAIL/PASS, so the runner printed `UNEXPECTED`; `C2_CONTROLS_UNEXPECTED` read 1 (M01, M02,
M03, M04, M07, M09, M10, M11, M12, M14) or 2 (M12b).

## Survivors: the control that would kill each (tested on scratch, not frozen)

Each candidate is built on the positive mirror exactly as the runner builds variants. On the unmutated counter every
candidate prints FAIL (expected) and the positive prints PASS; on the survivor mutant the candidate prints `rc=0 C2=PASS`
(a flip). Script: `extra-controls.py` (scratch only, deleted).

- **M05 COVERAGE minimums -> 1** — candidate `s144-one-quote`: drop the S144 Q9 quote and its citations from Claims 2
  and 5 (S144 keeps 1 quote, min 2). Base: `COVERAGE=0/1 rc=1`. M05: `QUOTES=8/8 COVERAGE=1/1 C2=PASS rc=0`. Kill.
  Why it survived the frozen set: no frozen variant has every quote valid while a row sits under its minimum.
- **M06 ECHO ratio dropped** — candidate `echo-ratio-only`: Claim 5 with 3 fresh long words among 13 (23 %, under the
  30 % ratio, above the absolute 3). Base: `ECHO=0/1 rc=1`. M06: `ECHO=1/1 rc=0 C2=PASS`. Kill.
  Why it survived: the frozen `echo-claim` variant has only 2 fresh words, so the absolute clause already fails it.
- **M08 live-git binding in PROBE dropped** — candidate `probe-claims-other-git`: the probe prints `HEADER git=git
  version 2.55.0` and the committed output says the same, so the probe's own `same` comparison passes and only the
  `bound` check (committed HEADER contains the live `git --version`) catches it. Base: `PROBE=0/1 rc=1`. M08:
  `PROBE=1/1 rc=0 C2=PASS`. Kill. The binding is NOT redundant: it is the only check against a probe that self-reports an
  old git. (The frozen `probe-git-stale` variant edits only the committed text, so `same` already fails it.)
- **M13 claims >= 5 -> >= 1** — candidate `four-claims`: remove Claim 5 and its only quote Q6 (S142 keeps 2, min 2).
  Base: `CLAIMS=0/1 rc=1`. M13: `CLAIMS=1/1 rc=0 C2=PASS`. Kill. No frozen variant has fewer than 5 claims.
- **M15 probe exit code / PROBE_FACTS dropped** — candidate `probe-exit-fail`: the probe prints identical lines and exits
  1 (`sys.exit(main() or 1)`, the documented "cleanup failed" exit). Base: `PROBE=0/1 rc=1`. M15: `PROBE=1/1 rc=0
  C2=PASS`. Kill. The frozen set never tests a probe whose lines match but whose exit is 1.
- **M16 CENSUS ignored** — candidate `census-fails-other-row`: add a registry row S145 with `used-by` naming a missing
  file (census E11, exit 1), outside the ROWS ids. Base: `CENSUS=0/1 rc=1`. M16: `CENSUS=1/1 rc=0 C2=PASS`. Kill.
  The frozen set never makes the census fail.
- **M17 TRIO source-id requirement dropped** — candidate `source-line-no-S144`: remove `S144 ...` from the `source:` line.
  Base: `TRIO=0/1 rc=1`. M17: `TRIO=1/1 rc=0 C2=PASS`. Kill. The frozen `no-trio` variant breaks the `verified-at:` key,
  not the id list, so it does not test the id check.

Candidate-set summary: each of the 7 survivors is killed by its one named candidate (18/18 with the frozen kills). Among the 11 frozen kills, two also flip on candidate rows: M14 on `claim-no-shared-words` (rc=0, PASS) and M12b on `positive-control` (rc=1, its frozen positive flip). The other nine (M01 M02 M03 M04 M07 M09 M10 M11 M12) print the expected result on every candidate row. The candidate output was read from scratch and is not kept.

## Control gaps (count g = 7)

1. M05 — no variant with a row under its quote minimum and all other quotes valid (`s144-one-quote`).
2. M06 — no variant whose only failing check is the 30 % echo ratio (`echo-ratio-only`).
3. M08 — no probe whose own header and committed output agree on an old git (`probe-claims-other-git`).
4. M13 — no entry with fewer than 5 claims and all quotes cited (`four-claims`).
5. M15 — no probe whose lines match but whose exit code is 1 (`probe-exit-fail`).
6. M16 — no registry state that makes the census fail (`census-fails-other-row`).
7. M17 — no `source:` line missing one of S142–S144 with TRIO's other keys intact (`source-line-no-S144`).

Named limit, unchanged: `non-sequitur` passes every mutant that keeps the quote/claim structure. It is the frozen named
limit; no mutant of the counter's structure can catch it (INFERENCE: this is a property of the counter's design, not a
gap in mutation coverage).

## Routing (not edited into the frozen instruments)

Per claims.md, a finding against a frozen instrument is routed as a limit or supplement, never a rewrite. Suggested route
for the next round's battery: add `s144-one-quote`, `echo-ratio-only`, `probe-claims-other-git`, `four-claims`,
`probe-exit-fail`, `census-fails-other-row`, `source-line-no-S144` as supplementary variants. Each was checked to FAIL on
the unmutated counter and to flip under its survivor. The L1 decides.

## Scratch and tooling

- Scratch: `/fast/scratch/hyaku/chousa-r63/MutC2Counter/` (lane mirror, 18 mutant lanes, output files); removed before
  yield.
- Scratch-only edit: `run-c2-controls.py` in the scratch lane has `COUNTER` read from an env var (`C2_MUTANT`) with the
  default unchanged; the mutant runs used each mutant lane's own counter, so the env var was not needed. Otherwise the
  runner is byte-for-byte the frozen runner except that one line plus `import os`.
- No tools installed or upgraded. Read `/home/vgpnk/.omp/agent/RULES.md` (tooling directive); no installs were needed.
- Commands run (all from the scratch dir): `python3 -B run-c2-controls.py --work <dir> --fleet /home/vgpnk/Projects/shokunin`
  (18 mutant lanes, parallel, plus the baseline); `python3 -B extra-controls.py <counter...>` (9 candidate variants x 18
  mutants + baseline); `diff` and `ast.parse` checks on each mutant.

## Calibration notes

- The assignment lists 13 mutant items: M01–M13 cover them (M12 and M12b are the two forms of "resolve S143 to any file"; M07 and M08 are the two live-git bindings; M09 is the probe-lines comparison). M14–M17 are additional mutants (shared-word check, probe exit code, census, TRIO id list).
- A killed mutant is only as good as the variant that kills it. M12b is killed by the positive control, which the
  runner's `positive` line already guards; that is a weaker kill than M01/M02/M03/M04/M07/M09/M10/M11/M12/M14, which
  each flip a dedicated defect variant.
- Candidate variants were checked against the baseline counter only for the expected FAIL; their wording and quote
  choices were not reviewed by a non-author.

VERDICT: C2_MUTANTS_KILLED=11/18 control_gaps=7
