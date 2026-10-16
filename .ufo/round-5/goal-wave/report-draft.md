# chousa — round 5: kept rejections and negative sweeps become verdict-bearing (coverage move)

<!-- SCRIBE DRAFT — MEASURED FINAL. Before: gate sha256 6b83705b… (==
     `git show HEAD:tools/research-gate.sh`; fixture before-side through a
     lane-shaped mirror so LANE_ROOT resolved), lane HEAD 45f8f65. After:
     gate sha256 55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2,
     stable >2 min and identical before/after the battery. Every after-value
     below is a verbatim fresh-process receipt from this seat. Scribe scratch
     /tmp/chousa-scribe-r5/ (declared ephemeral, cleaned at end of run).
     [PARENT] markers mark parent-only bindings. The Debt section keeps
     receipt identity OPEN per the mission contract. -->

Status: **DRAFT — measured, awaiting parent integration/admission**. Baseline:
lane HEAD `45f8f65` (round-4 records). Wave: one 32-seat flash call. Report
time: 2026-10-16 ~01:20Z.

## Work performed

- Round 5 selects the move round 4 registered: **coverage** — the last r1
  structural axis. Kept rejections and negative sweeps previously only had to
  EXIST; neither their flip-conditions nor their locations/emptiness were
  checked.
- The wave shipped `verify-sweeps <record> --root ..` and a pre-registered
  fixture family. Scribe independent work: before-state probes + fixture
  before-side at the r4 gate; after-state battery (fixtures, 10 probes,
  selftest byte-stability, all prior-mode regressions, exit contract, strace)
  at the settled gate; note/receipt cross-checks; drafts.

## Landed changes (all uncommitted, at draft time)

- `tools/research-gate.sh` → sha256 `55adb92d…` (+582/−0 vs HEAD): fourth mode
  `verify-sweeps` (`:2666` dispatch; header/`usage` contract) with helpers
  `sweep_where_tokens` `:1339`, `sweep_flip_cell` `:1380`, `sweep_raw_where`
  `:1388`, `sweep_path_guarded` `:1397`, `sweep_glob_matches` `:1432`
  (literals take an `-e`/`-L` existence test; globs use `nullglob`+`globstar`),
  `verify_sweeps` `:1444`; selftest 44 → 54.
- Fixtures `corpus/fixtures/sweeps-r5.md` (`025352b7…`), `-broken.md`
  (`f74ea324…`), `-hit.md` (`89650988…`, rewritten by its author at 22:13
  after this seat's first battery — the re-check is existence-only, and the
  broken control was re-run at the new bytes with identical findings),
  `sweeps-r5.README.md` (updated to the settled contract; this seat
  re-checked no stale `https?://`/`hit.md:4` text remains).
- `corpus/knowledge/sweeps-rejections-r5.md` (`sweeps-r5` note, 16.6 KB);
  receipts `corpus/evidence/sweeps-r5-20261016T011103Z-{live,fixture,broken,selftest}.log`
  (91e89fc2…/f831e65f…/4278f90a…/5e7fcd6e…); `SKILL.md` gate row + prose;
  lesson `corpus/lessons/2026-10-16-sweeps-rejections-verdict-bearing.md`
  (`ecd8dd33…`). Not seen at draft time: `corpus/README.md` round-5 row.

## Before → after measurements

**Before (this seat, fresh process, gate `6b83705b…`):**

```text
probe (scratch): rejection no flip + sweep "anywhere" + sweep claiming
"swept lib/ for ghost, no hits" while lib/ghost.md EXISTS
  verify → RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=2
  chains=1 claims=2 negatives=2 rejections=1 approvals=0), exit 0
same with explicit empty flip_condition column + "nowhere"/"looked
everywhere, found nothing" → CLEAN, findings=0 drift=0, exit 0
verify-sweeps <probe> --root root → exit 2 "multiple record paths" (no mode)
frozen fixture bytes under r4 verify: sweeps-r5.md CLEAN findings=0 drift=0
exit 0; sweeps-r5-broken.md CLEAN findings=0 drift=0 exit 0
baselines: selftest PASS (44); claims 17/17 CLEAN; chain 17/22 CLEAN;
broken 1/2 DRIFT; A/B/C each DRIFT exit 1 (3/3)
```

**After (gate `55adb92d…`, sha identical before/after battery, stable >2 min;
fresh processes; verbatim):**

```text
$ verify-sweeps corpus/fixtures/sweeps-r5.md --root ..        (exit 0)
SWEEP id=W1 where=research/deep-research-2026-09-28/kotobank-*,research/deep-research-2026-09-28/s looked=local hits=0 at=- observed=verified verdict=match
SWEEP id=W2 where=https://kotobank.jp/ looked=non-local hits=- at=- observed=exempt verdict=exempt
REJECTION id=R1 ref=research/README.md:12 reason=present flip=present observed=complete verdict=match
REJECTION id=R2 ref=research/deep-research-2026-09-28/B-multiagent-knowledge.md:79 reason=present flip=present observed=complete verdict=match
REJECTION id=R3 ref=research/deep-research-2026-09-28/B-multiagent-knowledge.md:63 reason=present flip=present observed=complete verdict=match
VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3
RESEARCH_GATE: CLEAN (sweeps=2 verified=1 exempt=1 hit=0 refused=0 invalid=0 rejections=3 rejections-ok=3 findings=0 drift=0)

$ verify-sweeps corpus/fixtures/sweeps-r5-broken.md --root ..  (exit 1)
SWEEP id=W1 where=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md looked=local hits=1 at=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md observed=hit verdict=mismatch
REJECTION id=R1 ref=research/README.md:12 reason=present flip=absent observed=incomplete verdict=mismatch
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R1 missing=flip
FINDING SWEEP_CLAIM_FALSE severity=warn surface=sweeps obs=id=W1 where=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md hits=1 first=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md listed=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md
VERIFIED_SWEEPS=0/1 REJECTIONS_OK=0/1
RESEARCH_GATE: DRIFT (sweeps=1 verified=0 exempt=0 hit=1 refused=0 invalid=0 rejections=1 rejections-ok=0 findings=2 drift=2)

$ verify corpus/fixtures/sweeps-r5.md --root ..  and  …-broken.md …  (same bytes, r1 surface)
both: RESEARCH_GATE: CLEAN (findings=0 drift=0 …), exit 0  — identical under
the r4 gate and the r5 gate
```

The W1 `where=` display is truncated at 80 chars by `chain_disp`; the check
uses the full two-glob set (note's wording; this seat confirmed by the
`hits=0` verdict and the cell contents).

Regression battery (this seat):

| Check | Before (`6b83705b…`) | After (`55adb92d…`) | Exit |
|---|---|---|---|
| selftest | `PASS (44 cases)` | `PASS (54 cases)`, first 44 lines byte-identical; +10 sweeps cases | 0 |
| claims fixture | 17/17 CLEAN | 17/17 CLEAN, byte-identical modulo `ts=` | 0 |
| chain fixture | 17/22 CLEAN | 17/22 CLEAN, byte-identical modulo `ts=` | 0 |
| broken control | 1/2 DRIFT | 1/2 DRIFT, byte-identical modulo `ts=` | 1 |
| r1 observable A/B/C | 3/3 DRIFT | 3/3 DRIFT, byte-identical modulo `ts=` | 1 |
| verify-chain on positive fixture | (before-side not run on revised bytes) | `RESOLVED_HOPS=2/3` CLEAN | 0 |
| exit contract | mode absent → 2 | CLEAN 0 / DRIFT 1 / missing 2 / no-path 2 | 0/1/2 |
| zero network | — | strace `-f -e trace=network`: 0 network lines on the positive run | 0 |

Scribe probes at `55adb92d…` (scratch; each one controlled variable):
`after-p1` healthy → CLEAN `1/2 + 1/1`; `after-p2` no-flip + named-file hit →
DRIFT both findings; `after-p5` traversal → DRIFT `SWEEP_LOCATION_OUT_OF_CORPUS`
crit refused unopened; `after-p7` undeclared `S7` → DRIFT
`SWEEP_LOCATION_UNRESOLVED`; `after-p9` Negatives-carried r1-style cell
(`test ! -f lib/ghost.md`, file present) → DRIFT `SWEEP_CLAIM_FALSE`;
`after-p4` `where=lib/no-such-dir/` → CLEAN `1/1` (limit); `before-a`/`before-b`
(before-side probes) flip CLEAN → DRIFT under the new mode.

## Defects found by the scribe seat

1. **Claims-row sweep references are invisible to `verify-sweeps`** (evaluation
   gap, not a regression): a negative `## Claims` row whose `sweep` cell names
   an undefined id (`W9`, no `## Sweeps` section) passes BOTH modes CLEAN exit
   0 — r1 `verify` (findings=0) and `verify-sweeps`
   (`VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`) on the same bytes
   (`/tmp/chousa-scribe-r5/probes/after-p3b-dangling-withchain.md`; with a
   Chain section so no unrelated finding fires). `verify_sweeps`
   (`tools/research-gate.sh:1500-1513` at `55adb92d…`) reads `## Sweeps` rows
   and `## Negatives` rows only; the `## Claims` sweep cell is never read.
   The note names the adjacent section-absence variant; this Claims-cell
   variant is this seat's independent finding. Owner: lane (future move) —
   the round's "sweep naming nowhere" class is closed only where the sweep is
   visible to the mode.
2. **Zero-hit verification cannot distinguish an empty search from a wrong
   one**: `where=lib/no-such-dir/` verifies (`hits=0`); the recorded command is
   never executed and its prose never compared (note: "design, not debt").
   `where=lib/` (an existing directory as the glob) counts as a hit →
   `SWEEP_CLAIM_FALSE listed=lib/` — consistent with the glob contract,
   surprising for r1-style description cells. Cosmetic: 80-char `where=`
   display truncation.
3. **Flip-condition screening is presence, not quality** (`-`, `TBD`, `none`,
   restated reason, never-fires all pass — note's 12-row class table; this
   seat cross-checked the mechanism, not the table).
4. No cross-mode or regression defects found: all prior observables held
   byte-stable; the r1 surface on the fixture bytes is identical at both
   revisions; zero network.

## SHONEN

[PARENT: re-check against SHONEN.md at integration.] All four tripwires
remain `[ ]` (no named non-author verifier; wave seats are the lane per
protocol).

Boundaries held: zero network (strace); corpus read-only; seats committed
nothing; /tmp quota respected (no EDQUOT; scratch cleaned at end of run by
this seat).

## Per-axis and learning verdicts

See `.ufo/round-5/goal-wave/scorecard-verdict-draft.md` (verdict vocabulary
only, no scalar scores): coverage **improved**; operability **improved**;
depth **improved** under the r2–r4 note precedent [PARENT: else unchanged];
freshness/calibration/adjacency **unchanged**; none harmed. Trends: quality
**improved**, expansion **improved**, discernment **unchanged**.

## Debt, cross-domain handoff and admission

- **Receipt identity (round 1) — STILL OPEN** (integrator/operator side). No
  authentic queue taskKey/expected receipt bag exists; no `task_…` value may
  be manufactured, no shape-only receipt counted, no Sighting marked
  complete. Proven receipt-backed completed rounds remain **0**; operator
  target unchanged (≥100). Routing for this wave was the operator's
  in-session direct dispatch; no Sighting was invoked.
- r5 artifact ledger at draft time: landed — gate `55adb92d…`, fixtures +
  README, note, 4 evidence receipts, `SKILL.md` row/prose, lesson
  `2026-10-16-sweeps-rejections-verdict-bearing.md` (`ecd8dd33…`); not seen —
  `corpus/README.md` round-5 row. Integrate only what lands.
- No cross-domain handoff changes known at draft time.

## Fresh-session continuation

Measured state: gate `55adb92d…` (uncommitted; round-4 revision still
recoverable as `git show HEAD:tools/research-gate.sh` = `6b83705b…`).
Open items for a next round (all named with evidence above): the Claims-cell
sweep-reference gap and section-absence handling inside the mode; non-vacuous
flip screening; and carried residuals — token-aligned shortening,
non-ASCII-adjacent fail-closed edges, in-root hardlinks, no source size cap,
scope-refusal finding IDs, frozen-replay comparator. Any next round must
declare its own falsifiable single move; do not rerun this wave. Receipt
identity remains the standing integrator-side blocker (target ≥100).