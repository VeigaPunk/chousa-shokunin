# LOG.md — round-5 entry draft (parent-owned file; integrate under [PARENT] markers)

<!-- SCRIBE DRAFT — MEASURED FINAL. Before: round-4 gate sha256
     6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2
     (== `git show HEAD:tools/research-gate.sh`; fixture before-side re-run
     through a lane-shaped mirror so LANE_ROOT resolved). After: round-5 gate
     sha256
     55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2
     (stable >2 min, identical before and after the battery). Lane HEAD
     45f8f65; no commits by any seat. Scribe scratch /tmp/chousa-scribe-r5/
     (declared ephemeral, cleaned at end of run). [PARENT] marks parent-only
     bindings. The debts section keeps the receipt-identity debt OPEN per the
     mission contract. -->

## 2026-10-15 — round-5 coverage: kept rejections and negative sweeps become verdict-bearing (`verify-sweeps`)

Round 5 executes the move round 4 registered: the last r1 structural axis —
rejections and negative sweeps currently only have to EXIST; nothing checks
that a rejection says when it would flip, that a sweep names where it looked,
or that its emptiness claim is true. The operator dispatched this wave
directly in-session (same routing as rounds 2–4; **no Sighting step was
invoked**); receipt identity from round 1 remains open and untouched by this
round.

**Before.** At the round-4 revision (sha256 `6b83705b…`, lane HEAD `45f8f65`),
`verify` checks rejections only for a non-empty reason (`:605-620` at that
revision) and negatives only for a non-empty sweep cell (`:525-538`,
`:555-564`); sweep CONTENT is never interpreted and no sweep is ever re-run.
Measured by this seat at that revision, fresh-process CLI runs:

- Probe records (scratch, root with `lib/ghost.md` present): a record whose
  rejection has a reason but no flip-condition column, whose Claims-row sweep
  says `anywhere`, and whose Negatives-row sweep claims `swept lib/ for ghost,
  no hits` while `lib/ghost.md` EXISTS → `RESEARCH_GATE: CLEAN (findings=0
  drift=0 questions=1 sources=2 chains=1 claims=2 negatives=2 rejections=1
  approvals=0)`, exit 0. A second probe with an explicit EMPTY
  `flip_condition` column and sweeps `nowhere` / `looked everywhere, found
  nothing` → CLEAN, findings=0 drift=0, exit 0.
- `bash tools/research-gate.sh verify-sweeps <probe> --root root` at
  `6b83705b…` → exit 2 (`research-gate: multiple record paths` — the mode does
  not exist; the r4 CLI reads `verify-sweeps` as a positional record path).
- The frozen round-5 fixture bytes (fixture-author seat; `sweeps-r5.md`
  sha256 `025352b7…`, `sweeps-r5-broken.md` `f74ea324…`) under the r4 gate's
  `verify` (re-run through a lane-shaped mirror so `LANE_ROOT` resolved; sha
  verified == `6b83705b…`): both CLEAN, exit 0 — `sweeps-r5.md` `findings=0
  drift=0 questions=1 sources=4 chains=3 claims=3 negatives=2 rejections=3
  approvals=1`; `sweeps-r5-broken.md` `findings=0 drift=0 questions=1
  sources=1 chains=1 claims=1 negatives=1 rejections=1 approvals=1`.
- Regression baselines at `6b83705b…`: selftest `PASS (44 cases)` exit 0;
  `verify-claims corpus/fixtures/claims-r2.jsonl --root ..` → 17/17 CLEAN
  exit 0; `verify-chain corpus/fixtures/chain-r3.md --root ..` → 17/22 CLEAN
  exit 0; `chain-r3-broken.md` → 1/2 DRIFT exit 1; A/B/C each DRIFT exit 1
  (3/3).

**The move.** `tools/research-gate.sh` (uncommitted working tree, +582 lines
vs HEAD, gate `55adb92d…`): a fourth mode `verify-sweeps <record> --root ..`
(dispatch `:2666`; contract in the header and `usage`). Every `## Rejections`
row needs non-empty `reason` AND a flip cell — an exact-key search
(`flip`/`flip_condition`/`would_flip`/`falsifier`/…) or any column whose key
matches `flip|falsif|reversal|counter` — else `SWEEP_REJECTION_INCOMPLETE`
(warn) and `observed=incomplete verdict=mismatch`. Every sweep item — a
`## Sweeps` row, or a `## Negatives` row carrying a where-like column or a
clean `sweep` cell — must name where it looked: a whitespace-free value is a
comma/semicolon path set; a value with whitespace is read as a
command/description whose structured words (URLs, source ids, path/glob
tokens) are extracted (`test ! -f lib/ghost.md` names `lib/ghost.md`). Local
path/glob tokens are re-expanded from `--root` (`nullglob`+`globstar`;
literals take an `-e`/`-L` existence test): any match is `SWEEP_CLAIM_FALSE`
(warn) naming the hit and listing up to five; zero matches is
`observed=verified verdict=match`. URLs/`external:`/`web:`/`live:`/`chat:`/
`session:` forms and declared source ids are exempt-but-counted; a row marked
`unresolved|blocked-no-fetch|labelled-dead|not-applicable` is exempt; `..`
components or a resolved ancestor outside ROOT/LANE_ROOT are refused unopened
(`SWEEP_LOCATION_OUT_OF_CORPUS`, crit); an undeclared S-id is
`SWEEP_LOCATION_UNRESOLVED` (warn); an empty/unjunked location is
`SWEEP_LOCATION_ABSENT` (warn). Summary: `VERIFIED_SWEEPS=N/M
REJECTIONS_OK=K/L` and one `RESEARCH_GATE:` line; CLEAN iff
`verified+exempt=M` and `K=L` and no drift; exit 0/1/2 contract unchanged.
The recorded command is never executed and its `observed` prose never
compared — the re-check is a location/existence test.

**Fixtures.** `corpus/fixtures/sweeps-r5.md` (positive: 3 rejections with
reason+flip_condition; W1 local where-globs `…/kotobank-*,…/saved-*`
genuinely empty; W2 `https://kotobank.jp/` non-local) and
`sweeps-r5-broken.md` (R1 no flip; W1 names
`chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md`, which exists) plus the
planted-hit file `sweeps-r5-hit.md` and `sweeps-r5.README.md` with the frozen
expected outputs. The fixtures were revised mid-wave from a `command`-cell
grep form to the settled `where`-glob form; the README was updated to match
(no stale `https?://`/`hit.md:4` text remains; this seat re-checked).

**Selftest.** 44 → 54 cases, all PASS; the first 44 case lines byte-identical
(diff empty). New cases 45–54: `sweeps-pass` (exit 0), `sweeps-fail-planted-hit`
(1), `sweeps-fail-rejection-incomplete` (1), `sweeps-fail-unnamed` (1),
`sweeps-fail-out-of-corpus` (1), `sweeps-fail-unresolved-id` (1),
`sweeps-fail-counting` (1), `sweeps-pass-cell-command` (0),
`setup-sweeps-no-path` (2), `setup-sweeps-missing-file` (2).

**Measurements after the move** (gate `55adb92d…`, sha identical before and
after the battery, stable >2 min; all fresh-process by this seat; regression
outputs byte-identical to `6b83705b…` modulo `ts=`):

```text
positive fixture  verify-sweeps sweeps-r5.md        → VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3 ; CLEAN ; exit 0
broken control    verify-sweeps sweeps-r5-broken.md → VERIFIED_SWEEPS=0/1 REJECTIONS_OK=0/1 ; DRIFT ; exit 1
                                                      FINDING SWEEP_REJECTION_INCOMPLETE obs=id=R1 missing=flip
                                                      FINDING SWEEP_CLAIM_FALSE obs=id=W1 hits=1 first=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md
same bytes r1     verify sweeps-r5.md / -broken.md  → both CLEAN findings=0 drift=0 ; exit 0 (unchanged surface)
chain on positive verify-chain sweeps-r5.md         → RESOLVED_HOPS=2/3 ; CLEAN ; exit 0
selftest                                            → RESEARCH_GATE_SELFTEST: PASS (54 cases) ; exit 0
claims fixture                                      → VERDICT_BEARING_CLAIMS=17/17 ; CLEAN ; exit 0
chain fixture / broken                              → RESOLVED_HOPS=17/22 CLEAN exit 0 / 1/2 DRIFT exit 1
r1 archives A/B/C                                   → each DRIFT exit 1 (3/3), identical modulo ts=
exit contract                                       → missing-file 2, no-path 2, CLEAN 0, DRIFT 1
zero network (strace -f -e trace=network, positive) → 0 socket/connect/sendto/recvfrom lines ; exit 0
```

Scribe probes at `55adb92d…` (scratch, outside the lane):
`after-p1` (healthy) CLEAN 1/2+1/1; `after-p2` (no flip + named-file hit)
DRIFT naming both findings; `after-p5` (traversal `../../…`) DRIFT
`SWEEP_LOCATION_OUT_OF_CORPUS` crit; `after-p7` (undeclared `S7`) DRIFT
`SWEEP_LOCATION_UNRESOLVED`; `after-p9` (r1-style `test ! -f lib/ghost.md`
cell, planted file exists) DRIFT `SWEEP_CLAIM_FALSE`; `after-p4`
(`lib/no-such-dir/`) verifies — a limit; `before-a`/`before-b` flip to DRIFT
under the new mode.

**Named limits (measured by this seat; the note names the first two).**
Flip-condition screening is presence, not quality — `-`, `TBD`, `none`,
reason-restatement, never-fires and vague strings all pass (note's 12-row
class table; this seat did not re-run it, only its mechanism). Emptiness of
the named set does not mean the set was the right place to look; a
non-existent directory verifies (`hits=0`). **New here:** a Claims-row
`sweep` cell referencing an undefined id (`W9`, no `## Sweeps` section) is
invisible to the new mode — both `verify` and `verify-sweeps` close CLEAN,
exit 0 (probe `after-p3b` with a Chain section: r1 CLEAN findings=0,
sweeps `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`); the mode reads `## Sweeps`
rows and `## Negatives` rows only, never `## Claims` sweep cells. A record
with no sweeps at all also closes `0/0` CLEAN in this mode. `where=lib/`
(a directory glob) counts as a hit. The W1 `where=` display truncates at 80
chars (cosmetic).

**Admission.** [PARENT: ADMIT/REJECT line + commit hashes; no scalar; axis
verdicts live in SCORECARD.md's round-5 sections.]

**Debt.** Receipt identity (round 1) STILL OPEN — no authentic queue
taskKey/expected receipt bag exists; mission acceptance is integrator-owned,
no `task_…` value was invented, proven receipt-backed completed rounds remain
0, operator target unchanged (≥100). Round-5 artifacts at draft time
(uncommitted): gate `tools/research-gate.sh` (+582; sha `55adb92d…`),
fixtures + README, note `corpus/knowledge/sweeps-rejections-r5.md`, receipts
`corpus/evidence/sweeps-r5-20261016T011103Z-{live,fixture,broken,selftest}.log`
(shas 91e89fc2…/f831e65f…/4278f90a…/5e7fcd6e…), `SKILL.md` gate row + prose,
lesson `corpus/lessons/2026-10-16-sweeps-rejections-verdict-bearing.md`
(`ecd8dd33…`; landed after this seat's first battery). The planted-hit file
was rewritten by its author at 22:13 (`4f07f906…` → `89650988…`); the
existence-only re-check is byte-independent, and the broken control was
re-run at the new bytes with identical findings. Not seen at draft time: a
`corpus/README.md` round-5 row — integrate only what lands. Lane hygiene: no
commits by seats.