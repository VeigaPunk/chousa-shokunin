# CritC1Flaky — round 63, wave w1 — C1 battery flakiness and vacuity

Scope: the frozen battery `corpus/evidence/round63/c1-battery.py` run on the reference candidate
`corpus/evidence/round63/controls/pos-ref-preflight.py`. Nothing in the lane, the frozen instruments, `tools/`, or
`SKILL.md` was written. No install or upgrade was made. Scratch `/fast/scratch/hyaku/chousa-r63/CritC1Flaky/` is removed
before yield.

Frozen bytes checked (`sha256sum | cut -c1-16`): `c1-battery.py` = `0073fba73c89aaf8`, reference =
`07683086fd6c6b41`. Both match `claims.md`.

## Findings

1. **No leg failed at any seed.** Ten full runs, seeds 1–5 twice (passes a and b), `--jobs 2`, `C1_SEED` set in the
   environment. Every run printed 22 `LEG … ok` lines and `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, exit 0.
   Receipts: `grep -c ' ok ' full-*.txt` = 22 for each; `grep FAIL` empty for each.
2. **Flaky legs: 0. Seed-dependent legs: 0.** The second pass (b1–b5) is the one-more-rerun that separates the two; it
   reproduced the first pass exactly. Note the per-run wall time under load (host load average 45–60 on 32 cores):
   a1 54 s, a2 83 s, a3 64 s, a4 84 s, a5 168 s, b1 107 s, b2 145 s, b3 159 s, b4 180 s, b5 240 s. No `timeout` reason
   appeared. INFERENCE: the only wall-clock-dependent verdicts are the subprocess timeouts (G06/G07 at 300 s inside the
   tool, legs at 600 s in the battery); a heavier load spike than observed could turn a leg into `timeout`. Not observed.
3. **Vacuous legs: none possible.** A seed is a string; the choice a leg makes is `random.Random(f"{seed}/{leg}")`'s
   first `choice`. Because the seed space is open, I enumerated every value of each leg's random choice instead of
   sampling seeds, applying each change with the frozen `apply` function and running the reference tool with
   `--only G01,G02,G03,G04,G05`. Each choice must produce exactly the leg's expected FAIL set, with no ENV.
   Results (`enum/out.txt`, `enum/out2.txt`, `enum/out3.txt`, scratch):

   | leg | choice space | choices giving the expected FAIL set | expected |
   |---|---|---|---|
   | D01 duplicate registry row | 141 rows | 141/141 | G01 |
   | D02 used-by missing | 107 mined rows | 107/107 | G01 |
   | D03 status `watch` | 115 mined rows | 115/115 | G01 |
   | D05 unindexed README name | 84 knowledge names | 84/84 | G02 |
   | D06 lesson loses `## Gate` | 40 round-N lessons | 40/40 | G03 |
   | D08 capability pointer gone | 72 pointers | 72/72 | G05 |
   | D11 = D01 + D04 | — | not enumerated, see below | G01,G02 |
   | D14 = D06 with `--only G03` | same 40 choices | (G03 result identical to D06) | G03 |
   | B01 new registry row | `randrange(50)`: 50 values | 50/50 no FAIL, rc 0 | none |
   | B03 new lesson | `randrange(90)`: 90 values | 90/90 no FAIL, rc 0 | none |

   D11 is not enumerated: its first change is D01's choice (141/141 give G01 FAIL), and its second change, D04, adds
   `zz-<tag>-r63.md` that the README cannot name, so G02 always FAILs. Argued, not run. The enumeration used
   `--only G01…G05`; G06/G07 are not touched by any D-leg change except the deterministic D09/D10, which the battery's
   own full runs already exercise.

4. **The four named constructions, checked against the lane.**
   - *README entry name that is a substring of another entry name.* The lane has 0 such pairs (84 names;
     `python3 -B` check). Would it matter? D05 replaces every occurrence of the name, so the longer name also loses
     its mention and G02 still FAILs. Not vacuous.
   - *Lesson with two `## Gate` headings.* Present: `round-27.md` and `round-34.md` each carry two. D06 uses
     `re.sub(..., flags=re.M)`, which rewrites all of them, so G03 still FAILs. Both lessons are inside the 40/40.
   - *Registry row whose census does not flag.* No such row: D01/D02/D03 are 141/107/115 of 141/107/115 with the
     expected FAIL set. The census flags E03 (duplicate id), E11 (used-by missing, mined rows only) and E07 (status
     `watch` is not in `queued|mined|rejected`, per `scripts/sources-census.sh` header).
   - *Capability pointer in two cells.* D08 rewrites only the first occurrence in the evidence cell (cell 3). If the
     pointer also sits in the What cell, that copy is untouched and G05 still FAILs. The one construction that would
     make D08 vacuous is a pointer whose first occurrence is inside an earlier non-pointer token of the same evidence cell
     (e.g. `scripts/tools/x.py` before `tools/x.py`), because the rewrite then hits the wrong token and the real pointer
     still resolves. INFERENCE from the code; the enumeration covers the lane's actual 72 pointers and none is in that
     shape.

5. **Calibration note for the battery, not a defect.** The battery's random legs draw from frozen RNG streams keyed
   by `seed/leg`, so every verdict is reproducible for a given seed string. That makes the five-seed result a
   reproducible receipt, not a sample of a distribution. Enumeration is the stronger check for vacuity.

## Seed to choice map (the seeds the task named, for the frozen legs that draw)

| leg | seed 1 | seed 2 | seed 3 | seed 4 | seed 5 | space |
|---|---|---|---|---|---|---|
| D01 | 105 | 107 | 6 | 41 | 97 | 141 |
| D02 | 9 | 41 | 79 | 76 | 4 | 107 |
| D03 | 59 | 75 | 99 | 78 | 101 | 115 |
| D05 | 29 | 55 | 2 | 76 | 57 | 84 |
| D06 | 30 | 27 | 4 | 24 | 9 | 40 |
| D08 | 7 | 62 | 22 | 8 | 43 | 72 |

Every seed-mapped choice above is one of the choices enumerated in Finding 3, and each of those gave the expected FAIL set.

## Commands run (lane root as cwd unless stated)

- `C1_SEED=1 python3 -B corpus/evidence/round63/c1-battery.py --tool corpus/evidence/round63/controls/pos-ref-preflight.py --fleet /home/vgpnk/Projects/shokunin --work <scratch>/w-only1 --jobs 2 --only CLEAN,D12,D13,B03`
  → `CLEAN=1/1 DEFECTS=2/15 BENIGN=1/6 BATTERY=PARTIAL`, exit 0, 16 s wall.
- Same command without `--only`, `C1_SEED` = 1..5, pass a then pass b → ten runs, all `BATTERY=PASS`, exit 0 (see
  Finding 1).
- `python3 -B c1enum.py` (scratch) → D01, D02, D03 enumerated (bad=0). The deadline of 3000 s killed the run during D05;
  this is the one slip in the wave run, and it is why the remaining legs were re-run in `c1enum2.py`
  (D05, D06, D08: bad=0) and `c1enum3.py` (B01, B03 sweeps: 0 non-clean). Nothing from the killed run was used
  beyond the three completed legs.
- Read-only checks: `grep`/`python3 -B` scan of `corpus/knowledge` names and `corpus/lessons` `## Gate`
  counts; `scripts/sources-census.sh` header and `usedby_findings` / E-code rules (read, not run).

No git, jj or index command was run. No package was installed. The only interpreter runs against lane files were `python3 -B` reads of `corpus/knowledge`, `corpus/lessons` and `corpus/README.md`; nothing was written there.

## Limits

- The enumeration ran G01–G05 only; G06 and G07 were exercised by the ten full runs, not by the enumeration.
- D11 and D14 are argued from D01/D06 (see above), not enumerated one by one.
- Seeds 1–5 are the ones asked for; the enumeration covers all seeds in effect, not a sample.
- Load-dependent timing is observed on one host at one load (45–60); no stress run was made.

VERDICT: FLAKY_LEGS=0 seed_dependent=0 vacuous_possible=0
