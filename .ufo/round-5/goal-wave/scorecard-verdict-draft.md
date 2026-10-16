# SCORECARD.md — round-5 draft sections (parent-owned file; [PARENT] binds)

<!-- SCRIBE DRAFT — MEASURED FINAL. Verdict vocabulary only: improved /
     unchanged / harmed / unprovable-but-better. No scalar scores.
     Before: round-4 gate sha256
     6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2
     (== `git show HEAD:tools/research-gate.sh`; also run as a lane-shaped
     mirror `r4mimic` so LANE_ROOT resolved). After: round-5 gate sha256
     55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2
     (stable >2 min; identical before and after the battery). Lane HEAD
     45f8f65. Fixtures (revised bytes): sweeps-r5.md 025352b7…,
     sweeps-r5-broken.md f74ea324…, sweeps-r5-hit.md 89650988… (rewritten
     by its author mid-wave; existence-only re-check). Scribe
     scratch /tmp/chousa-scribe-r5/ (declared ephemeral, cleaned at end of
     run). [PARENT] marks parent-only bindings. The report draft's debts
     section keeps the receipt-identity debt OPEN, per the mission contract. -->

Round-1/2/3/4 sections stay as written. These are the round-5 sections to
append, plus the admission/`Planned` refresh.

## Round-5 per-axis verdicts

Measurements: both revisions measured fresh-process by the scribe seat.
Falsifiable claim: at the r4 gate a kept rejection needs only a reason (no
flip-condition) and a negative sweep only needs to exist — nothing checks
where it looked or whether its emptiness claim is true. **Before** (same
probe bytes at `6b83705b…`): `verify` closed CLEAN, findings=0 drift=0,
exit 0 on a record whose rejection had no flip-condition, whose Claims-row
sweep named `anywhere`, and whose Negatives-row sweep claimed
`swept lib/ for ghost, no hits` while `lib/ghost.md` exists; `verify-sweeps`
did not exist (exit 2, `multiple record paths`). The pre-registered fixture
pair (revised bytes) also passed r1 `verify` CLEAN, exit 0, both files.
**After** (`55adb92d…`): the same fixture bytes under `verify-sweeps` —
positive CLEAN exit 0 `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`; broken DRIFT
exit 1 with `SWEEP_REJECTION_INCOMPLETE` (R1, missing=flip) and
`SWEEP_CLAIM_FALSE` naming `chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md`
(hits=1); selftest `PASS (54 cases)` with the first 44 case lines
byte-identical; all prior-mode outputs byte-identical modulo `ts=`; r1
observable 3/3; zero network (strace, 0 lines); exit contract 0/1/2 held.
Scribe's independent probes add the refusal classes (traversal →
`SWEEP_LOCATION_OUT_OF_CORPUS` crit; undeclared S-id →
`SWEEP_LOCATION_UNRESOLVED`; `where=lib/` existing dir → `SWEEP_CLAIM_FALSE`)
and one named hole (below).

| Axis | Verdict | Evidence boundary |
|---|---|---|
| coverage | **improved** | The last r1 structural surface is now verdict-bearing: rejections carry reason+flip or `SWEEP_REJECTION_INCOMPLETE`, sweeps re-check their named local location set (`SWEEP_CLAIM_FALSE` names the hit; zero hits verify), non-local sets exempt-but-counted, exact counting `VERIFIED_SWEEPS=N/M REJECTIONS_OK=K/L` under CLEAN\|DRIFT. Before/after measured on the same fixture bytes and on same-bytes probe records; broken control flips CLEAN(exit 0)→DRIFT(exit 1). Boundary: what is verified is presence + the named set's emptiness, not the flip text's quality nor that the named set is the right one |
| depth | **improved** [PARENT: r2–r4 precedent — each admitted scorecard credited the landed knowledge note under depth; scribe's stricter reading would be unchanged] | `corpus/knowledge/sweeps-rejections-r5.md` (16.6 KB) documents the mode's frozen revision, the exact flip-cell key search, the token classes, the boundary guard, the 12-probe presence-vs-quality class table and the exempt routes; its receipts match this seat's independent runs line for line (this seat re-derived the two fixture runs, selftest 54, the regressions and the exit/strace checks) |
| operability | **improved** | selftest 44 → 54 (+10: `sweeps-pass`, `sweeps-fail-planted-hit`, `sweeps-fail-rejection-incomplete`, `sweeps-fail-unnamed`, `sweeps-fail-out-of-corpus`, `sweeps-fail-unresolved-id`, `sweeps-fail-counting`, `sweeps-pass-cell-command`, `setup-sweeps-no-path`, `setup-sweeps-missing-file`); cases 1–44 byte-identical; claims 17/17, chain 17/22, broken 1/2, A/B/C 3/3 all byte-identical modulo `ts=`; exit contract 0/1/2 held (`verify-sweeps` no-record and missing-file both 2) |
| freshness | unchanged | Pins re-checked at fixed revisions only; no cross-revision drift detector |
| calibration | unchanged [PARENT: re-judge if integration counts the note's presence-vs-quality class table as a calibration gain; this seat reads it as documentation of the new mode's own boundary, not a re-measurement of a prior surface] | The note + README name the limit plainly: a vacuous-but-non-empty flip string passes (12-row class table, `-`/`TBD`/`none`/never-fires all complete); a sweep can be empty because the wrong glob was named; the recorded command is never executed and its prose never compared |
| adjacency | unchanged | Zero network (strace `-f -e trace=network`: 0 socket/connect/sendto/recvfrom lines on the positive run); corpus read-only; boundary policy shared with claims/chain (canonicalization, URL/session/out-of-corpus refusal); seats committed nothing |

Scribe-found limits (measured; candidates for `Planned`/future rounds):
- **Claims-row sweep references are invisible to `verify-sweeps`.** A
  negative in `## Claims` whose `sweep` cell names an undefined id (`W9`,
  no `## Sweeps` section) closes BOTH `verify` and `verify-sweeps` CLEAN,
  exit 0 (probe `after-p3b-dangling-withchain.md`: r1 CLEAN findings=0;
  sweeps `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`). Likewise a record with no
  sweeps at all closes `0/0` CLEAN in this mode (`after-p6-nosweep.md`).
  The note names the section-absence variant of this; the Claims-cell variant
  is this seat's measurement.
- **A `where` naming a non-existent directory verifies** (`lib/no-such-dir/`
  → `hits=0 observed=verified`): zero-hit emptiness cannot distinguish "looked
  in an empty/nonexistent place".
- `where=lib/` (an existing directory as the glob) counts as a hit →
  `SWEEP_CLAIM_FALSE` naming `lib/`; consistent with the glob contract but
  surprising for r1-style description cells. The W1 `where=` display is
  truncated at 80 chars by `chain_disp` (cosmetic; the check uses the full
  set).

## Round-5 learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| quality | improved | The pre-move hole is now caught on the lane's own pre-registered bytes: `sweeps-r5-broken.md` passed r1 `verify` CLEAN (exit 0) at both revisions and now DRIFTs exit 1 under `verify-sweeps` naming both defects; the positive fixture still passes. Same-bytes before/after, not a restated criterion |
| expansion | improved | New admitted specimen + contract: `corpus/fixtures/sweeps-r5.md` / `-broken.md` / `-hit.md` + `sweeps-r5.README.md` (source pins re-derived, expected outputs frozen) — the fourth fixture family |
| discernment | unchanged | No non-author admit/reject spot-check; no criterion added |

## Admission and continuation (round-5 replacement text)

[PARENT: refresh the round-4 admission paragraphs after integration.]

Local axis result: coverage improved (the last r1 structural axis is
verdict-bearing with a pre-registered positive/broken pair); operability
improved (selftest 44→54, prior modes byte-stable, exit contract held); depth
improved if the r2–r4 note precedent is followed [PARENT]; freshness/
calibration/adjacency unchanged; none harmed. Accepted limits, named rather
than hidden: flip-condition presence ≠ quality; emptiness of the named set ≠
goodness of the search; Claims-cell sweep references are not read by the new
mode. No scalar substitute, no promotion. [PARENT: adjust the axis cells if
integration finds a landed artifact disagreeing with a measured value, or if
the gate moves past `55adb92d…`.]

Mission acceptance is separate and remains blocked on the round-1 receipt
identity: the interactive launch has no authentic queue taskKey/expected
receipt bag, so no `task_…` value may be manufactured, no shape-only receipt
counted, and no Sighting marked complete. Receipt-backed verified rounds
remain **0**; the operator target remains at least 100. Routing for this wave
was satisfied by the operator's in-session direct dispatch; no Sighting was
invoked.

Debt after round 5: receipt identity (integrator, still open); the
Claims-cell/section-absence evaluation gap in sweeps mode (lane, named
above); non-vacuous flip screening (lane, the note's candidate: reject a
small explicit placeholder set — not built); non-author spot-check
(integrator/operator); carried residuals (in-root hardlinks, no source size
cap, token-aligned shortening, non-ASCII-adjacent fail-closed edges,
scope-refusal finding IDs, frozen-replay comparator). Artifact ledger at
draft time — landed: gate, fixtures + README, note, 4 receipts under
`corpus/evidence/`, `SKILL.md` row + prose, lesson
`2026-10-16-sweeps-rejections-verdict-bearing.md` (all uncommitted). Not seen
at draft time: a `corpus/README.md` round-5 row — integrate only what lands.
See `.ufo/round-5/goal-wave/report-draft.md` for owners.

## Planned (round-5 refresh)

[PARENT: replace the round-4 `Planned` paragraph.] Round 5's registered move
(kept rejections and negative sweeps become verdict-bearing — the last r1
structural axis) ran in the operator's in-session wave and is measured. Any
next round must again declare its own falsifiable single move and genuine
scope before dispatch; do not rerun this round's wave. Standing lane
candidates: the swept-evaluation gap named above (Claims-cell sweep
references; section-absence handling inside the mode), non-vacuous
flip-condition screening, and the carried residuals listed under Debt.