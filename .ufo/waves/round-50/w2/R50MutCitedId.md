# R50MutCitedId — mutation test: cited-id-check.py + name-collision-check.py (round 50, wave 2)

2026-10-25. Detectors under test (read-only, never modified in the lane):
- `corpus/evidence/round50/cited-id-check.py` sha256 before `e51bc4603c662d641983d9fca88fcd452b43c29fa20f076d7898d415c40169bb` == after.
- `corpus/evidence/round50/name-collision-check.py` sha256 before `caf7517a9d9296d740a33e9fabe77e49a0978b650737726547e49ee43a35acbd` == after.
All mutants were copies under `/dev/shm/chousa-r50-R50MutCitedId/` (deleted before finishing). No tool installed or
upgraded (none needed); pacman untouched.

## Inputs and baselines (pristine, run before any mutant; a baseline failure would be inconclusive)
- as-staged table: `sed -n '20,27p' .ufo/waves/round-50/w1/ExecAdopt.md` → header + 7 rows (S109,S111,S118,S124,S135,S136,S145), sha256 `923f36f6…`.
- cleaned table: `.ufo/waves/round-50/assimilation/renumber.tsv` → header + 5 rows (S118→S104, S124→S105, S135→S105 held, S136→S106, S145→S107), sha256 `2a421d9d…`.
- entries: the three staged entries from `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/`, arg order r40, r41, r39 (`source:` lines: r40 S124 · r41 S135,S136,S145 · r39 S118).
- spec: `.ufo/waves/round-50/w1-spec.json` (42 items), run with `--lane /home/vgpnk/Projects/shokunin/chousa-shokunin`.

```
$ python3 cited-id-check.py as-staged.tsv r40.md r41.md r39.md          # pristine
BODY_CROSSREF S109->S104
BODY_CROSSREF S111->S105
CITED_IDS=FAIL rows=7                                                      exit=1
$ python3 cited-id-check.py cleaned.tsv r40.md r41.md r39.md            # pristine
CITED_IDS=PASS rows=5                                                      exit=0
$ python3 name-collision-check.py w1-spec.json --lane <lane>            # pristine
13 × NAME_COLLISION (MineConsider, ExecMirrorCensus→round-47/w1, ExecInfStaged, ExecReplayC1, ExecFormProbe,
  CritForgeC1, CritForgeC2, ReviewProvince, ReviewQuarMap, CritTheme, ConnSiblings, ConnCrossClaim, ScoutCoverage)
NAME_COLLISIONS=13 ITEMS=42                                                exit=1
```
B1/B2 reproduce `cited-id-before.txt` verbatim; B3 reproduces the lesson's 13-seat collision list. Baselines valid.

## Kill matrix (K = killed, S = survived on the named corpus)
| # | mutant (one-line diff) | pristine | mutant observed | verdict |
|---|---|---|---|---|
| 1 | `re.search(rf"^source: {staged}\b"…)` → `re.search(rf"{staged}\b"…)` | FAIL rc1 / PASS rc0 | as-staged `CITED_IDS=PASS rows=7` rc0 (cleaned PASS rc0) | K — misses S109+S111 |
| 2 | `entries = "\n".join(… argv[2:])` → `pathlib.Path(sys.argv[2]).read_text()` | FAIL rc1 / PASS rc0 | as-staged 6×BODY_CROSSREF (adds S118→S106, S135→S107, S136→S108, S145→S109) FAIL rc1; cleaned `BODY_CROSSREF S118->S104, S135->S105, S136->S106, S145->S107; FAIL rows=5` rc1 | K |
| 3 | `rf"^source: {staged}\b"` → `rf"^source: {staged}"` | FAIL rc1 / PASS rc0 | byte-identical to pristine on BOTH legs | **S** → probe P3 |
| 4 | `.splitlines()[1:] if l.strip()` → `.splitlines() if l.strip()` | FAIL rc1 / PASS rc0 | as-staged adds `BODY_CROSSREF staged_id->lane_id`, `FAIL rows=8` rc1; cleaned `BODY_CROSSREF staged_id->lane_id; FAIL rows=6` rc1 | K |
| 5 | `if r and int(r.group(1)) != rnd:` → `if r:` | `NAME_COLLISIONS=13` rc1 | `NAME_COLLISIONS=42 ITEMS=42` — flags all 40 names via their own round-50 w1 reports | K |
| 6 | `waves.glob("round-*/*/*.md")` → `waves.glob("round-*/w1/*.md")` | 13 rc1 | identical 13 lines, `NAME_COLLISIONS=13 ITEMS=42` rc1 | **S** → probe P6 |
| 7 | `if n in seen:` → fold lookup `k.lower() == n.lower()` | 13 rc1 | identical 13 lines rc1 | **S** → probe P7 |
| 8 | exact match → `hit = next(k for k in seen if k.startswith(n))` | 13 rc1 | 14 lines: adds `MutSelftest .ufo/waves/round-31/build/MutSelftestClaims31.md` and re-points `ScoutCoverage → .ufo/waves/round-46/w1/ScoutCoverageGround.md` (masks the true round-49/w1 path) | K |

Mutant-2 note: the kill depends on arg order (r40 first here); with any order the flagged set differs from pristine
because r40 alone does not carry all five `source:` lines.

## Survivors — each proven a real behavioral difference by a probe (coverage finding, no contract change proposed)
- **P3, mutant 3 (`\b` drop)**: the frozen tables contain no id that is a proper prefix of an id on a `source:` line.
  Probe: table row `S10→S999`, entry line `source: S109 — https://x.example — a longer id line`:
  `[pristine] rc=1 BODY_CROSSREF S10->S999 / FAIL rows=1` vs `[mutant] rc=0 PASS rows=1`.
- **P6, mutant 6 (w1-only glob)**: all 13 cross-round collision stems live in other rounds' `w1/` dirs
  (verified per name: `only_w1=True` for each of the 13), so w1-narrowing loses nothing here.
  Probe: synthetic lane with `.ufo/waves/round-49/w2/MineConsider.md` (exact case):
  `[pristine] rc=1 NAME_COLLISION MineConsider .ufo/waves/round-49/w2/MineConsider.md` vs `[mutant] rc=0 NAME_COLLISIONS=0 ITEMS=42`.
- **P7, mutant 7 (case fold)**: no spec name differs from a cross-round stem only by case
  (programmatic scan of all 23 round dirs / ~1,400 report stems: 0 case-only pairs).
  Probe: synthetic lane with `.ufo/waves/round-49/w1/mineconsider.md` (lowercase):
  `[pristine] rc=0 NAME_COLLISIONS=0 ITEMS=42` vs `[mutant] rc=1 NAME_COLLISION MineConsider .ufo/waves/round-49/w1/mineconsider.md`.
  (First instantiation also folded the print key and raised `KeyError` on this probe; rebuilt to fold the lookup only —
  verdict unchanged: survivor on the shipped corpus, killed by probe.)

## Restoration evidence
- Mutants lived only in scratch; lane files re-hashed after all runs: `e51bc460…` and `caf7517a…` — equal to before.
- Pristine rerun after the mutant series (restored-bytes leg): as-staged `BODY_CROSSREF S109->S104 / S111->S105 /
  CITED_IDS=FAIL rows=7` rc1 · cleaned `CITED_IDS=PASS rows=5` rc0 · spec `NAME_COLLISIONS=13 ITEMS=42` rc1 — identical to baselines.
- `/dev/shm/chousa-r50-R50MutCitedId` deleted before finishing (verified absent).

VERDICT: attacked the round-50 cited-id and name-collision checks with 8 assigned mutants — 5 killed (anchor-drop, first-entry-only, header-row, round-exclusion, suffix-match; each on the shipped as-staged/cleaned tables or w1 spec), 3 survived the shipped evidence but died on probes (word-boundary drop, w1-only glob, case folding), which is a coverage finding: the round's own tables/spec never exercise prefix ids, non-w1 cross-round collisions, or case-only collisions.

Report: .ufo/waves/round-50/w2/R50MutCitedId.md
