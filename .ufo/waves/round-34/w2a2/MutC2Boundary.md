# W2a2 MutC2Boundary — C2 boundary-blind controls (exact substring / left-only / right-only)

Seat: `chousa-r34-w2a2-MutC2Boundary-7` · lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`
· date 2026-10-23 · all experiments in `/fast/scratch/hyaku/chousa-r34-a2/w2/MutC2Boundary/`.

## Pins

- `sha256sum tools/research-gate.sh` = `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` (matches the
  brief; also `git show 707da818:tools/research-gate.sh | sha256sum` = same blob).
- `git rev-parse HEAD` = `fe3db76c0ae9fa18cfebcf127fec073354a1eb03`; HEAD ∖ 707da818 = three untracked-wave spec
  files only (`git diff --name-only 707da818..HEAD` → `w2a2-plan.json`, `w2a2-spec.json`, `w2a2-taskcall.json`),
  gate and counter blobs at HEAD equal those at 707da818. Counter `c2-count.py` sha256
  `8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173`, never edited by me.
- Committed after-receipts `.ufo/waves/round-34/measure-a2/c2-after-s{5011,5023,5033,5047}.json` (git-tracked,
  28 tracked files in that dir) each `DEADZONE_MATCH=37/37`, `gate_sha256=a6307edf…`; before-receipts s5011/s5023
  `21/37` on `772a1d8e4d94`. Re-derived independently below.

## Baseline (landed gate, scratch copy sha-verified as a6307edf…)

| command | result |
|---|---|
| `C2_TMP=… python3 corpus/evidence/round34/c2-count.py --gate …/gates/landed.sh --seed 6101 --receipt …/landed-s6101.json` | `DEADZONE_MATCH=37/37`, gate_rc=1, holds=true, 19.8 s |
| same, `--seed 6102` | `DEADZONE_MATCH=37/37`, gate_rc=1, holds=true, 30.0 s |

Fresh seeds 6101/6102 (not 5011/5023/5033/5047). P2's first limb re-derived.

## Controls built (scratch copies of the landed gate; 27 changed lines each)

Construction, identical shape for all three (diff in `ctlA.diff`, `ctlB.diff`, `ctlC.diff`):
1. new `tok_span_offsets_raw` — exact substring search, `bytes.find` over the hay read on stdin, **every start
   offset, overlapping included**, left to right (env `TOKRAW_SPAN` round-trips the span with
   `surrogateescape`); replaces *both* `tok_span_offsets` call sites in `tok_span_at` (:1680) and `tok_span_all`
   (:1701), so line binding also runs over all raw occurrences;
2. the boundary condition at :1674 and :1695 replaced per control:
   - **ctlA-blind** `if true; then` — `tok_left_ok`/`tok_right_ok` ignored entirely;
   - **ctlB-left** `if tok_left_ok "$before" "$span"; then`;
   - **ctlC-right** `if tok_right_ok "$after" "$span"; then`.

| control | sha256 | bash -n |
|---|---|---|
| ctlA-blind.sh | `0f9c70d00e1fc28287a51bfd2f0dde393e524ae0ff9b06a6a4d96d2f857d9acb` | OK |
| ctlB-left.sh | `4fab5d9b192116e4bd9bd256d99982320335bd65bba1a8306add686a022f97bb` | OK |
| ctlC-right.sh | `7904969f7f1fc6f66741b504ecb187a33121051b21c149885040da73b0d111e0` | OK |

Wiring probe (2-byte spans, `probe/`, verbatim in `transcript.txt`; gate exit codes measured directly):

| gate | p1 `qab` (left-glued) | p2 `abq` (right-glued) | p3 ` ab ` | p4 `qab ab` | exit / line |
|---|---|---|---|---|---|
| landed | `unsupported` | `unsupported` | `supported` | `supported` | 1, DRIFT |
| ctlA-blind | `supported` | `supported` | `supported` | `supported` | 0, CLEAN |
| ctlB-left | `unsupported` | `supported` | `supported` | `supported` | 1, DRIFT |
| ctlC-right | `supported` | `unsupported` | `supported` | `supported` | 1, DRIFT |

i.e. each control implements exactly the blindness it is named for (no silent fallback to the native matcher).

## Counter scores (frozen counter, `--receipt`, fresh seeds)

| control | seed | label | gate_rc | predicate_holds | dz-glued-left | dz-glued-right | counter exit |
|---|---|---|---|---|---|---|---|
| ctlA-blind | 6111 | **33/37** | 1 (DRIFT) | false | 0/2 | 0/2 | 1 |
| ctlA-blind | 6112 | **33/37** | 1 (DRIFT) | false | 0/2 | 0/2 | 1 |
| ctlB-left | 6121 | **35/37** | 1 (DRIFT) | false | 2/2 | 0/2 | 1 |
| ctlB-left | 6122 | **35/37** | 1 (DRIFT) | false | 2/2 | 0/2 | 1 |
| ctlC-right | 6131 | **35/37** | 1 (DRIFT) | false | 0/2 | 2/2 | 1 |
| ctlC-right | 6132 | **35/37** | 1 (DRIFT) | false | 0/2 | 2/2 | 1 |

Every other class is full marks in every run (17 classes; e.g. ctlA-s6111: `dz-verbatim-ml 3/3`,
`dz-decoys 5/5`, `dz-line-bound 2/2`, `dz-line-wrong 2/2`, `dz-decoys-line-wrong 2/2`,
`dz-glued-then-valid 1/1`, `short-verbatim 2/2`, `short-mut 2/2`). Measured MISS lines (receipt `misses[]`,
also printed): ctlA — `dz-glued-right truth=unsupported observed=supported` ×2 and
`dz-glued-left truth=unsupported observed=supported` ×2; ctlB — `dz-glued-right … observed=supported` ×2;
ctlC — `dz-glued-left … observed=supported` ×2.

**Verdicts: ctlA-blind MISSES (33/37), ctlB-left MISSES (35/37), ctlC-right MISSES (35/37).**
No control reaches 37/37, so this defect class is *not* let through by the counter.

## Why each control is killed — and what that says about the fixture

Fixture shape (`c2-count.py:build`): `dz-glued-left` = `filler + " " + letter + span + sep + filler` (one
occurrence, left edge glued), `dz-glued-right` = `filler + sep + span + letter + " " + filler` (mirror). Both
spans are drawn from the 32765..32767 window, so the kill happens on the C2 route (chunk matcher), not the
direct path. An exact search returns the glued occurrence as the first hit; a blind/one-sided gate calls it
delimited and prints `observed=supported` against truth `unsupported` — one MISS per record.

The other 33 records are exact-substring-invariant: verbatim/edge/decoy/mut/split classes produce the same
verdict under any boundary subset, and the line classes stay correct because *all* their occurrences are
delimited, so raw enumeration and native enumeration give the same line set.

Coverage findings (reported, contract untouched):
1. **All boundary discrimination lives in 4 of 37 records** — exactly `dz-glued-left` (2) + `dz-glued-right`
   (2). Each one-sided control loses only its own side's 2 records (35/37); the fully blind control loses 4
   (33/37). There is no redundant class: a future edit that moved either glued class out of the dead-zone
   window, or dropped it, would leave P2 at 37/37 with boundary blindness undetected.
2. **`dz-glued-then-valid` does not test boundary-blindness.** Truth is `supported` and a blind matcher also
   reports `supported`; it scored 1/1 in all three controls. It only catches "first occurrence reported with
   no search beyond it".
3. **Line binding is not a discriminator here.** `dz-line-bound`, `dz-line-wrong` and `dz-decoys-line-wrong`
   scored 2/2 in every control, i.e. raw-occurrence line binding is indistinguishable from native on this
   fixture (all occurrences delimited). The controls' line sets were built from *all* raw occurrences
   (overlapping included), which is at least as strong as the gate's non-overlapping enumeration.

Incidental P2 check (scan of every `chousa-r34-c2-receipt/v1` under `.ufo/waves/round-34/`, 70 receipts):
the 16 receipts whose `gate_sha256` is `a6307edf…` all print 37/37; no lower run exists on the landed gate.
Caveat: only the six `measure-a2` receipts are git-tracked; the wave-2 receipts (mine included) are untracked
files on disk — "committed after-run" should be read as the four `measure-a2` receipts.

## Limits

- Full counter runs (37 dead-zone records) are the dead-zone evidence; the 2-byte-span probe only proves each
  control is live.
- Controls replace the span enumerator for every caller, including chain quotes (:2077); the counter exercises
  `verify-claims` only, which is the claim's surface.
- Two seeds per control; I did not test prefix/partial-comparison or line-field-ignoring controls (other
  wave-2 seats hold those shapes).
- No network, no install; processes bounded with `timeout` (counter 900 s, gate internal 1500 s); none killed.

## Restoration / no-touch evidence

Lane read-only throughout: `git diff --stat -- .` empty, `git status --porcelain | grep -v '^?? .ufo/'` shows
only a pre-existing untracked `corpus/evidence/round34/__pycache__/` (no lane module was imported by my
commands); gate sha256 still `a6307edf…` and counter sha256 still `8c0def4d…`. Scratch copies remain at
`/fast/scratch/hyaku/chousa-r34-a2/w2/MutC2Boundary/`; no restoration was required (no lane bytes mutated).

Artifacts (this dir, all < 1 MiB; `sha256sums.txt`): `ctlA-blind.sh`, `ctlB-left.sh`, `ctlC-right.sh`,
`ctlA.diff`, `ctlB.diff`, `ctlC.diff`, `transcript.txt`, `claims.jsonl`, `receipts/` (6 control receipts +
2 logs + 2 landed baselines).
