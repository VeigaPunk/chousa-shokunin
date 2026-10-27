# R53MutAdopter — C1 candidate mutation test (round 53, wave 1)

Seat: R53MutAdopter (leaf, no subagent dispatch). Claim: frozen R53-C1 (`corpus/evidence/round53/claims.md`; freeze a6ff732c70011f11c9beb681d832cedc6e75f566). Candidate: `tools/assimilate-rows.py` v4 at commit 32aab5edd70e43145cae72ec872278f3bc6efba7; the working-tree blob sha256 `32628bbc33d1d293e789b7d8f44cd769996e56678c40fd5f3943b50b8d8ed636` equals the committed blob (`git -C <lane> show 32aab5e:tools/assimilate-rows.py | sha256sum` → same). Detector: `corpus/evidence/round53/c1-count.py` (8 legs; REAL pin 8e6484ed…689b). Skill: godspeed. Tooling: no installs (RULES.md read; pacman paused — nothing needed).

## Method
Pristine copy → scratch `base.py` (same hash). 14 mutants, one per frozen class, each an isolated scratch copy (`/fast/scratch/hyaku/chousa-r53/R53MutAdopter/mXX/assimilate-rows.py`); the lane file was never touched. Detector run per mutant: `TMPDIR=$S python3 c1-count.py --tool $S/mXX/assimilate-rows.py --work $S/work-mXX > $S/out-mXX.txt 2>&1` (unseeded). Survivors rerun with `--per-leg 10`.

## Baseline — pristine bytes
```
SEED=unseeded
TWIN=PASS HELD=PASS MIX=PASS RECHECK=PASS ORDER=PASS NOENTRY=PASS
REAL PASS rc=0 map=ok rows=5 count-line=['CITED=6 APPEND=5 HELD=0 TWIN=1']
REGRESS PASS r50-pin=ok r51-counter=LEGS=5/5
LEGS=8/8  C1=PASS  rc=0
```

## Kill matrix (14 mutants; defect → failing legs → LEGS → verdict)
| id | defect (mutation site in base.py) | failing legs, unseeded run | LEGS | per-leg 10 | verdict |
|---|---|---|---|---|---|
| m01 | twin mapped `held` (line 488: `mapping[sid] = (by_url[u], "held")`) | TWIN, MIX, REAL | 5/8 | — | KILLED |
| m02 | twin by first-seen order; 2nd staged row of a Registry-carried URL labelled twin (`seen_url` prepended to the mapping loop) | HELD, MIX | 6/8 | HELD, MIX | KILLED |
| m03 | `TWIN=` printed +1 (line 574) | TWIN, HELD, MIX, REAL | 4/8 | — | KILLED |
| m04 | `HELD=` also counts twins (line 572: `v[1] in ("held","twin")`) | TWIN, MIX, REAL | 5/8 | — | KILLED |
| m05 | recheck pre-pass skips held rows (`if mapping[sid][1] == "held": continue`) | none | 8/8 | RECHECK | KILLED @ per-leg 10 (see note) |
| m06 | recheck pre-pass skips twin rows | RECHECK | 7/8 | RECHECK | KILLED |
| m07 | recheck refusal printed but exit 0 (line 519 `return 0`) | RECHECK (3/3) | 7/8 | — | KILLED |
| m08 | recheck refusal after `renumber.tsv` written (write inserted before return 1) | RECHECK (3/3, `renumber=True`) | 7/8 | — | KILLED |
| m09 | registry refusals appended after entry refusals (refused list starts `[]`; `refused += reg_bad` after entry loop) | ORDER (3/3, `registry-first=False`) | 7/8 | — | KILLED |
| m10 | no-`--entry` registry refusal removed (`if not a.entry: return 0`) | NOENTRY (3/3, `broken-rc=0`) | 7/8 | — | KILLED |
| m11 | no-`--entry` refuses a sound registry too (extra `return 1` after reg_bad check) | NOENTRY (3/3, `sound-rc=1`) | 7/8 | — | KILLED |
| m12 | `url_of` no host lower-casing (line 141: `u[:n] + u[n:]`) | TWIN, MIX | 6/8 | TWIN, HELD, MIX | KILLED |
| m13 | `url_of` keeps trailing slash (line 138: fragment strip only) | TWIN, HELD, MIX | 5/8 | TWIN, HELD, MIX | KILLED |
| m14 | registry heading accepts only space, not tab (`##[ \t]` → `## ` in registry_rows + registry_problems) | TWIN, HELD, MIX, RECHECK, NOENTRY | 3/8 | same | KILLED |

## Observed outputs (representative failing case lines, verbatim from out-mXX.txt)
```
m01 TWIN case1 FAIL rc=0 held=0 twin=2 append=4 map=differs rows=4
m01 REAL FAIL rc=0 map={… 'S195': ('S118', 'held')} count-line=['CITED=6 APPEND=5 HELD=1 TWIN=0']
m02 MIX case1 FAIL rc=0 held=2 twin=1 append=2 map=differs rows=2
m03 TWIN case1 FAIL rc=0 held=0 twin=1 append=2 map=ok rows=2        # map ok, count wrong
m04 TWIN case1 FAIL rc=0 held=0 twin=1 append=3 map=ok rows=3        # count wrong
m05 (per-leg 10) RECHECK case1 FAIL on=held rc=0 refused-line=False renumber=True append=True
m06 RECHECK case2 FAIL on=twin rc=0 refused-line=False renumber=True append=True
m07 RECHECK case1 FAIL on=twin rc=0 refused-line=True renumber=False append=False
m08 RECHECK case1 FAIL on=twin rc=1 refused-line=True renumber=True append=False
m09 ORDER case1 FAIL kind=row-outside rc=1 refused=2 registry-first=False
m10 NOENTRY case1 FAIL kind=no-heading broken-rc=0 sound-rc=0
m11 NOENTRY case1 FAIL kind=no-heading broken-rc=1 sound-rc=1
m12 MIX case1 FAIL rc=0 held=4 twin=1 append=1 map=differs rows=3
m13 HELD case2 FAIL rc=0 held=2 twin=0 append=1 map=differs rows=2
m14 HELD case1 FAIL rc=1 held=1 twin=0 append=2 map=differs rows=-1   # refused: tab heading unseen
```
m03/m04 REAL (counts): `m03 REAL FAIL … count-line=['CITED=6 APPEND=5 HELD=0 TWIN=2']`; `m04 REAL FAIL … count-line=['CITED=6 APPEND=5 HELD=1 TWIN=1']`. REGRESS passed for all 14 mutants (the pinned round-50 suite and round-51 counter do not exercise twin/labels/count-line/no-entry refusals).

## Survivors
None: 13 killed on the first unseeded run; m05 (recheck pre-pass skips held rows) survived only because each of its 3 RECHECK cases drew `on=twin` (bad recheck on the twin row; P=1/8), and was killed at `--per-leg 10` (RECHECK FAIL 6/10: `on=held rc=0 refused-line=False renumber=True append=True`). Generator change that would make the kill deterministic: run `case_recheck` once per variant (force `on` over {"held","twin"}) instead of one random choice — a coverage gap in the counter's case generator, not a surviving defect.

## Hashes (before/after, sha256)
```
base.py (pristine = lane blob)        32628bbc33d1d293e789b7d8f44cd769996e56678c40fd5f3943b50b8d8ed636
m01 3a79362737d3945eeb95dd612b8c03f6a5777004744911e1da3fafbe1979cb1b  m02 0a98794ae0171645db5b3296f747c82c1be2560068baaa5e8022a3c6cbb95848
m03 fe6e4650cef948695a6fd2b1ed047a2e71570fb65936d4af6bbc030418c96e23  m04 6526069c182803241bc78cd328853dd3ddbe1e6a2d5d29775232f957f9b72226
m05 347c92d6f8852dfc976601d1b1d241015eb1708308dfe48ffdb2cb637dfafb1d  m06 94a70caec83ad3a7ad49b79fa6ac2f8b16d2e1b5d23e85aff2e867f41af7f764
m07 a3c59417f3966da6dce586b4d0b23d4e00ad240877376f5edfbd371d420b1589  m08 144cbdecc3f76039ff1a9fbbc27ace01785f40ef8b67c81530f5f933febced21
m09 7aaaedc6b7ae634ed405c57e2b2ed7eba657767be81962d7c27c8c6365bacbf6  m10 38104470c682f4d2fe48159537ff4827ada33a0d475a7ddac0a2f1b19ca5976b
m11 2134fb3708a6a6fbc029959c2ce8d74c53f77dddbe8699b7efef994a889c42e0  m12 4f83473464a1920ef3155b0b4c621d998a88e611d27fa0e4ad3653d25048afb6
m13 de592ee549124f2eca1e3ec78b3243ca3bc9a5f8a84686680153df666f844979  m14 4c6f55b9ef195e2fe4b3da9936a9b8526483a8612405d6583e4037e70a20b279
```

## Restoration evidence
All mutations confined to scratch copies. The lane tool's bytes are unchanged: post-run `sha256sum tools/assimilate-rows.py` → `32628bbc…` (same as before and as commit 32aab5e). No git/jj mutation anywhere; no production/lane file written except this report. Scratch dir `R53MutAdopter/` removed on finish.

VERDICT: Built 14 mutants across the frozen C1 classes (twin/held labelling, counts, recheck pre-pass, refusal order/exit/no-entry, URL normalisation, heading separator) and ran c1-count against each: baseline PASS 8/8; 13 killed on the first unseeded run, m05 killed at --per-leg 10; zero survivors — the counter detects every seeded defect, with one case-generator gap (held-row recheck cases drawn randomly) noted.
