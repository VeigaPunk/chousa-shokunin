# MutC2Counter — counter-of-counter for C2 (round 34, attempt 2, wave 2a2)

Seat: mutation tester. Read-only on lane production files. All experiments in
`/fast/scratch/hyaku/chousa-r34-a2/w2/MutC2Counter/`; artifacts in
`.ufo/waves/round-34/w2a2/MutC2Counter/`. Date 2026-10-23.

## Pins (read before any experiment)

- `sha256sum chousa-shokunin/tools/research-gate.sh` → `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`
  (matches the wave pin; used for every "committed gate" run).
- `sha256sum chousa-shokunin/corpus/evidence/round34/c2-count.py` → `8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173`
  (copied to scratch; never edited in the lane).
- Before-gate extracted read-only: `git show 3026a4e:tools/research-gate.sh` →
  sha256 `772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58`,
  `TOK_DIRECT_SPAN_MAX=32767` at line 1582. This is the real pre-fix gate, not a stub.
- Lane HEAD observed at `fe3db76` ("wave-2a2 spec/plan/taskcall re-frozen at tip
  707da818"); `git rev-parse 707da818…` resolves. Production gate/counter hashes are
  the frozen ones, so scoring is against the frozen bytes.

## Method

Eight control ("wrong") gates, each otherwise contract-shaped (one `CLAIM` line per
record, `FINDING CLAIM_LINE_MISMATCH ... obs=id=`, `RESEARCH_GATE: DRIFT`, exit 1):

| id | defect |
|---|---|
| g-accept | always `observed=supported`, no findings |
| g-trunc | prefix-only matcher: first 4096 B of the span, no boundary check; line-claimed records use exact whole-span binding (findings correct) |
| g-chunk | both halves of the span present in order, non-adjacent (no whole-span confirmation) |
| g-dup | real gate output, every `CLAIM` line printed twice (wrong `supported` first, real line last) |
| g-clean | real gate output, no `RESEARCH_GATE:` line, exit 0 |
| g-nofind | real gate output, all `CLAIM_LINE_MISMATCH` findings stripped |
| g-lookup | runs the real gate only when `sha256(claims)` equals one fixed fixture; otherwise blindly accepts |
| before-gate | the committed pre-fix gate `772a1d8e` (real defect, not a stub) |

Seven scratch copies of the counter, one requirement removed each (R1..R7, edits in
`var/c2-R*.py`). Each run: `python3 <counter> --gate <gate> --seed 3401 --receipt …`,
`C2_TMP`/`TMPDIR` in scratch, bounded by `timeout 900`. Exit codes: label run `rc=0`
when full, `rc=1` otherwise. Every command and output is in `runs/{A,B,C}/`.

## Re-derived baselines (committed counter, seed 3401 unless noted)

- committed gate: `DEADZONE_MATCH=37/37`, rc 0 (seed 3402 also 37/37).
- before-gate `772a1d8e`: **21/37**, rc 1 — independently reproduces the claim's
  before-state (`measure-a2/c2-before-s5011.json` = 21/37, seed 5011).
- wrong gates: accept 14/37, trunc 22/37, chunk 28/37, dup 0/37, clean 0/37,
  nofind 33/37, lookup 14/37. All rc 1 (label rc), i.e. every defect is detected at
  least once by the committed counter.

## Ablation matrix (removal → wrong gate)

| removal (scratch copy) | targeted gate | result | verdict |
|---|---|---|---|
| R1 `ok = obs != "none" and (finding-iff)` (equality removed) | g-trunc | **37/37** | load-bearing |
| R1 (same) | g-accept | 33/37 | equality alone is not enough; finding-iff still rejects accept |
| R2 drop `(cid in f_line) == (t == "mislocated")` | g-nofind | **37/37** | load-bearing |
| R3 drop `for cid in dup: observed[cid]="none"` | g-dup | **37/37** | load-bearing |
| R4 drop `rc == 1 and drift` guard | g-clean | **37/37** | load-bearing |
| R5 `random.Random(seed)` → `random.Random(0)` | g-lookup | **37/37** (seeds 222, 5011) | load-bearing |
| R6 `DZ_MIN/DZ_MAX` 32765/32767 → 64/4096 | before-gate 772a1d8e | **37/37** | load-bearing |
| R7 class count `dz-split` 2→0 (TOTAL 35; `assert TOTAL == 37` also removed) | g-chunk | 26/35 | **not sufficient** — 5 decoy + 4 glued records still catch the gate; the missing assertion aborts a naive ablation with `AssertionError` before any run |

Sanity: each R1–R7 copy against the committed gate scores full (R7: 35/35); no
removal accidentally breaks detection. See `matrix.json` here.

Evidence that R5's defect is real: with the seed fixed, seeds 111 and 222 produced
byte-identical `claims.jsonl`
(`7fafe905…` both; `keep/fixed111`, `keep/fixed222`). The g-lookup gate then returns
the real gate's answers (37/37) on two different "fresh" seeds, while the committed
counter scores 14/37 against the same gate on a genuinely fresh seed.

## Assessment

- Every parse-level requirement tested (observed equality, finding iff, duplicate→none,
  rc/DRIFT) is individually load-bearing for at least one plausible wrong gate; the
  window-enforcement and per-seed-generation requirements are load-bearing for the
  before-gate and for an answer-table gate respectively. Defense is layered: the pure
  accept gate needs two removals (R1+R2), so no single ablation flips it.
- The class-count ablation is **not** load-bearing by itself for the halves-only chunk
  gate: decoy and glued records remain. A class-count ablation also trips
  `assert TOTAL == 37` (counter refuses to run), so coverage cannot silently shrink.
- Therefore the committed counter's 37/37 on the committed gate is not vacuous: the
  same counter scores below full on every control in this set, and removing any single
  check (except the class count) lets at least one control reach full score.
- Limits: g-trunc/g-chunk are independent but simplified matchers, and g-dup/g-clean/
  g-nofind/g-lookup are output-surface wrappers around the committed gate; they model
  defect behavior, not complete alternate gate implementations. Only one seed (3401)
  per control; probabilities of the decoy classes are seed-dependent. C2's operability
  claim itself (the gate fix) was not re-scored beyond the 37/37 reproduction.
- No production byte was modified: gate and counter hashes re-checked unchanged at the
  end; `git status` shows only the untracked `.ufo/waves/round-34/w2a2/` artifact dirs.

## Artifacts

- `matrix.json` (this dir) — clean matrix, sha256 `92bb1c14627d60561fb66503556b9f17306ab6510a5f1805b23d16646c8810bf`.
- Scratch: `runs/A`, `runs/B`, `runs/C` logs + receipts; `var/c2-R*.py`; `gates/g-*.sh`;
  kept fixtures `keep/s3401`, `keep/fixed111`, `keep/fixed222`.
