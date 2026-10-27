# R57W2MutC3Counter — mutation probe of the frozen C3 counter

Target: `corpus/evidence/round57/c3-count.py` (frozen; live sha256 `c565ce4a78b439411dc6e088bc5f8a92781888fe895f2ee9b43170867c1e6e33`).
Kill rule per seat spec: every mutant must print `C3=PASS` on the after-state; any `C3=FAIL` / nonzero exit = kill (the leg names the killed leg).

## State pinned

- Named lane tip `1c9626efba2455d513b6b18df9b3df291e66556f`; live HEAD at probe time `3010e7537d16…`.
- `git log --oneline 1c9626e..3010e75` shows exactly one commit (the W2 dispatch); `git diff --stat … -- corpus` empty → for every file the counter reads, live root ≡ tip.
- Fixture: `git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin /fast/scratch/hyaku/chousa-r57/R57W2MutC3Counter/lane-clone`, `git checkout 1c9626e` inside clone (toplevel asserted = clone dir). Mutants written as `corpus/evidence/round57/mN.py` inside the clone only — `LANE=parents[3]` stays the clone; each run also repeated with `--root /home/vgpnk/Projects/shokunin/chousa-shokunin` on the live tree.
- `TMPDIR=$SCRATCH`, `PYTHONDONTWRITEBYTECODE=1`. Frozen file never edited; verified post-run, same sha256.

## Baseline (frozen bytes, live root)

`python3 corpus/evidence/round57/c3-count.py` →
`ENTRY=yes S127_CITED=yes NEW_GROUND=yes CLAUSE=yes / BOUND=4/7 (min 4) R1:S131 R2:S132 R3:S133 R7:S118 / SWEPT=3/3 R4 R5 R6 / QUOTE_ROWS=10 IN_SPAN=10 IN_ENTRY=10 IN_LESSON=10 SHORT=10 CONTEXT=10 CAPTURE_BOUND=10 / SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=yes STRAY_IDS=- / C3=PASS`, rc=0, ~0.10 s.

## Mutants — all single `str.replace` edits, each applied to pristine source, one occurrence asserted

| Mut | Edit | sha256[:16] | BOUND= | C3= | Verdict |
|-----|------|-------------|--------|-----|---------|
| M1 | `MIN_BOUND = 4` → `3` | e7f76d3dff3dd134 | `4/7 (min 3)` unchanged set | PASS (rc 0, both roots) | SURVIVED |
| M2 | drop `heading_title(form, title)` leg from binding `if` | e6f3cf99c928bb9e | `4/7` identical | PASS | SURVIVED |
| M3 | drop `token in nows(form)` leg | b4bc671140945139 | `4/7` identical (R3 stays S133) | PASS | SURVIVED |
| M4 | drop `len(qs) >= MIN_PER_ID` leg | d864aad9ce56bf9c | `4/7` identical | PASS | SURVIVED |
| M5 | drop `EXCLUDED`/`EXCLUDED_URLS` + mined/held gate (keeps url, `used_by`, `cites`) | c4754c1f98af3b00 | `4/7` identical | PASS | SURVIVED |
| M6 | drop `not stray` from `ok` conjunction | 03bd808831b3e962 | `4/7`, `STRAY_IDS=-` | PASS | SURVIVED |
| M7 | drop `anchors == len(anchors_need)` | 564405cde89ac986 | `4/7`, `ANCHOR_BOUND=3/3` | PASS | SURVIVED |
| M8 | drop `cites(rid, url)` regex leg from candidate filter | bf8db0533049c616 | `4/7` identical | PASS | SURVIVED |

Observed output identical on clone@tip and live root for all eight; full metric lines byte-identical to baseline except M1's printed `(min 3)`.

## Why each survives (state-bound masking, all grounded in the run above)

- M1: `BOUND=4/7` sits exactly at the threshold; lowering the floor cannot flip `>=` on a state that meets the old floor exactly — detectable only on a 3-bound counterexample (the frozen HELD control is 1/7).
- M2/M4/M8: the surviving AND-legs cover the removed one on this state — every bound row satisfies heading/2-rows/cites anyway; every rejected candidate (e.g. S130, see below) is already excluded by other legs.
- M3: dropping the token check does NOT mis-bind S130→R3 because S130 never reaches the binding `if`: `grep '^| *S130 *|' corpus/SOURCES.md` row 140 shows its `used-by` lacks the entry and the entry holds no `source: S130` line (grep over `corpus/knowledge/normative-reference-chain-china-r57.md` = 0 hits) → fails `used_by`/`cites`; it also has no manifest rows → fails `MIN_PER_ID`. Token leg is the *only* leg claims.md says excludes S130 for R3, but on this state the other legs mask it.
- M5: opening candidacy to EXCLUDED/mined-ungated rows adds no binder — excluded rows still fail `used_by`+`cites`, and no non-candidate row has manifest coverage.
- M6/M7: `STRAY_IDS=-` and `ANCHOR_BOUND=3/3` on the live state — both legs vacuously true here; only exercisable on states with stray S-ids / bad anchors.

## Boundary & restoration evidence

- Writes: clone-scratch only (`/fast/scratch/hyaku/chousa-r57/R57W2MutC3Counter/`), plus this report. `git status --porcelain` on the lane at end shows no writes of mine (`M SCORECARD.md`, `M corpus/lessons/round-57.md` are sibling mid-wave edits; counter reads were consistent throughout).
- `sha256sum corpus/evidence/round57/c3-count.py` after all runs = `c565ce4a…33`, unchanged; `rm -rf` of the scratch dir verified empty before this file was written.

VERDICT: all 8 single-edit mutants of the frozen C3 counter SURVIVE (each still prints C3=PASS on the after-state at tip 1c9626e and live 3010e75) — every weakened leg is masked by sibling AND-legs on the passing state, so the predicate legs are individually unexercised here; a coverage finding, not a falsification.
