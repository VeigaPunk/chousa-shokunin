# R59Reviewer41 — round 59 claim design, controls, source grounding, scope, report contract

Seat: reviewer (leaf), axis calibration. No edits; no scratch created (nothing to
remove); no installs; no pacman; no live external fetch; L0 `8d77e6c1` untouched and
still open. Only read-only git (`status`, `log`) was run; no git/jj/index writes.
All times 2026-10-27, local -03:00. Lane root below = `chousa-shokunin/`.

Verified identity pins (my own sha256sum runs):

- `corpus/evidence/round58/c1-count.py` = `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`
- `tools/build-spans.py` = `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`
  (still the pinned r55 builder — no r58 hardening landed, per LOG round-58 close)
- `corpus/evidence/round59/controls/c1-before.txt` is byte-identical to
  `corpus/evidence/round58/controls/c1-before.txt` (`cmp` rc 0; both `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe`)
- `corpus/evidence/round59/s101-open.txt` = `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`
  = byte-identical to `corpus/evidence/round54/S101-text-form.txt`

## Findings, by severity

### S1 — CRITICAL: the "frozen claims" named by the wave context never existed; the freeze-before-dispatch contract is void

Every seat's shared context (identical string in `w1-dispatch.json` `taskCall.context`
and `w1-spec.json` `context`) orders: "Frozen claims:
`/…/chousa-shokunin/corpus/evidence/round59/claims.md`; read before work."

- That file does not exist. `corpus/evidence/round59/` holds exactly three entries:
  `census-start.txt` (15:12:21), `controls/c1-before.txt` (15:14:30),
  `s101-open.txt` (15:26:09). No `claims.md` (directory read + glob).
- It never existed in any ref: `git log --all --oneline -- corpus/evidence/round59`
  is empty; `git status --porcelain` shows `?? corpus/evidence/round59/` and
  `?? .ufo/waves/round-59/` (untracked working-copy bytes only). Lane HEAD is
  `af8c0a4` ("round-58 verifier spot-check").
- Precedent: every round 29–58 has a committed `claims.md`, and r58's own sequence
  is `9e73a03` "freeze claims and before controls" → `718e8d2` control results →
  `5da0a63` S101 pin → `c9b08e9` W1 findings (git log). Round 59 skipped the first
  step entirely and dispatched at 15:12:11.

Falsifier: a pre-dispatch commit, or any mtime ≤ 15:12:11, for `round59/claims.md`.
None exists in the worktree or any ref.

Consequence: all 66 seats were pointed at a mandatory, nonexistent precommitment.
Several seats (e.g. `w1/R59Executor07.md` "Blocker" section) bound themselves to
the round-58 counter instead — defensible improvisation, but it means the wave is
running with no round-59 claim object at all, and seat outputs cannot be verdicts
against a frozen claim because there is none.

### S2 — CRITICAL: the round's named deliverable (positive-verdict-path calibration) has no frozen predicate, and the staged "before" receipt cannot support one

The milestone is "build and falsify controls for positive verdict-path calibration".
Verified in committed bytes of the only counter in play (`round58/c1-count.py`,
sha `65da18bb…`):

- Line ~390–391: `ok_pass = all(("=pass" in l) for l in ok_legs)` (lowercase) but
  `ref_pass = all(("=PASS" in l) for l in ref_legs)` (uppercase); line ~399 summary
  numerator `REFUSE={sum('=PASS' in l for l in ref_legs)}/…`.
- Refusal legs emit lowercase via the `PASS` constant: `FOREIGN={PASS}(refused)`
  (line ~223), `SYMLINK_OUT={PASS}(refused)` (line ~234). Hence `REFUSE=0/7` and
  `C1=FAIL` for every possible builder, including a fully compliant one — the
  positive verdict is structurally unreachable as frozen.
- This is not new knowledge: `corpus/QUALITY.md:974` criterion 115 states exactly
  "A frozen counter must demonstrate its positive verdict path before it binds
  round data; a deny-only control set cannot prove that the target is reachable."

Round 59's response so far violates that freshly written criterion:

- `round59/controls/c1-before.txt` (15:14:30 — after the 15:12:11 dispatch) is
  byte-identical to r58's receipt: same counter, same builder, same unreachable
  oracle. It re-evidences the r58 defect; it is not a baseline under any corrected
  oracle.
- No round-59 `claims.md` or counter exists that freezes the repaired predicate
  (case-normalized aggregate + summary, totality on early-leg failure, explicit
  containment root). Any later "C1=PASS" would rest on a post-hoc, unfrozen
  predicate — precisely the failure class QUALITY 115 prohibits. Independent
  runs corroborate the unreachable/one-token-repair/both-tokens sequence
  (`w1/R59Executor07.md` F1–F3: case-fix of line 391 alone yields `C1=PASS` with a
  self-contradicting `REFUSE=0/7` receipt).

Falsifier: a round-59 counter/claims.md frozen before wave data that demonstrates
its positive path (per QUALITY 115). Absent — see S1.

### S3 — HIGH: the on-disk wave spec is not the dispatch source; `w1-spec.json` postdates the dispatch and matches nothing that was sent

- `w1-dispatch.json` / `w1/swarm-registry.json`: 15:12:11 (registry
  `createdAt 2026-10-27T18:12:11.203Z`). `census-start.txt`: 15:12:21.
  `controls/c1-before.txt`: 15:14:30. `w1-spec.json`: 15:14:46 — written after the
  wave was already dispatched.
- Registry items are role-differentiated and match received seat texts (verified:
  executor item at `swarm-registry.json:14-21` "inspect and run exact round58
  frozen counter/tool or controls relevant to positive-verdict-path defect";
  `R59Reviewer41` at `:408-415` "Adversarially assess round59 claim design…
  No edits."; `R59Critic55` at `:548-555`; `R59MutationTester62` at `:618-625`).
- `w1-spec.json` items are 66 byte-identical placeholders ("For round 59, review
  ready handoff requirements. Read …claims.md… do not write lane files."), carrying
  no role-differentiated work, and self-contradictory ("do not write lane files"
  vs the mandatory lane report path).

Falsifier: any one seat whose `w1-spec.json` item equals its
`w1/swarm-registry.json` item. I compared executor, reviewer, critic and
mutation-tester entries: all differ. An auditor diffing spec ↔ registry gets 66/66
mismatches, so the spec file of record for this wave does not exist on disk.

### S4 — HIGH: two dispatch trees resolve the same seat names to shared scratch roots and report paths; evidence is not attributable by path

- `w1.ready` names `"l1":"ChousaR59"`; `w1.ready.partial` (mtime 15:27:54, mid-wave)
  rebinds seats to `-2`-suffixed agents (e.g. `"R59Executor07": "R59Executor07-2"`).
  The live peer roster simultaneously shows `R59Executor01` and
  `ChousaR59.R59Executor01`, `R59Executor07-2` and `ChousaR59.R59Executor07`,
  `R59Scribe17` and ChousaR59-prefixed siblings — two agent populations for one
  seat-name space (66 seats dispatched per `w1-dispatch.json` `counts.spawn`).
- Concrete collision: at 15:23 foreign probe bytes
  (`positive-path/poison-base.py`, `positive-path/c2-poison-zh.stdout`) appeared in
  `/fast/scratch/hyaku/chousa-r59/R59Executor07/` — the bound seat's scratch root —
  reported by the bound agent (`R59Executor07-2`, IRC 15:2x; `w1/R59Executor07.md`
  hygiene section) as not-mine and unattributable by path; the second instance
  claimed the same seat, scratch root and report path and asked that the bytes stay.
  Sibling task titles ("Removing scratch again and checking",
  "Rebuilding scratch after sibling wipe") evidence mutual scratch wipes.
- Registry `agentId` fields are all `null`, so the registry itself cannot
  disambiguate.

Falsifier: exactly one live agent per seat name with a unique scratch root. The
roster, the mid-wave rebind file, and the 15:23 collision contradict this.
Consequence: any round-59 counter receipt or probe output under
`/fast/scratch/hyaku/chousa-r59/<seat>/` is contestable provenance, and report
files under `w1/` have two prospective writers per collided seat.

### S5 — MEDIUM: post-dispatch lane writes into the round-evidence namespace; the S101 receipt is a provenance-free duplicate

- `corpus/evidence/round59/s101-open.txt` (15:26:09, post-dispatch) is
  byte-identical (sha `a8e3e7ad…`) to `corpus/evidence/round54/S101-text-form.txt`.
  It carries no header at all: no producing-tool pin (the r58 claims pin
  `tools/capture-text.py` = `2c0140bc…` as the defined-form maker), no S101 raw
  sha256 (`6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` per
  r58 claims), no extraction timestamp, no `source:/verified-at:/recheck:` trio.
  As offline source reconnaissance it is therefore unbindable: an anonymous copy of
  an r54-era derivation. Content is consistent with the committed S101 capture's
  subject (中国学术期刊(光盘版)检索与评价数据规范 text), so this is a grounding/
  provenance defect, not a fabrication indicator.
- `controls/c1-before.txt` (15:14:30) is likewise post-dispatch: the "before"
  receipt is not pre-data in time either.
- Both files sit in the lane's frozen-evidence namespace while the dispatched
  contract says "Never edit lane files" (registry items). Writer attribution is
  undetermined from my seat (L1 planner act vs a seat breach); existence, mtimes,
  byte-identity and hashes are the evidence.

Falsifier: a committed, headered provenance attestation for either file, or a
pre-dispatch mtime. Both are untracked; `git log --all` for the round59 path is
empty.

### S6 — LOW: residual r58 counter defects that any round-59 predicate must freeze into its kill rules (currently frozen nowhere)

Verified directly in `round58/c1-count.py` (`65da18bb…`):

- Vacuous control gate: `denied_pass = (denied == total) if total else True`
  (line ~393) — without `--controls`, `DENIED=0/0` passes trivially.
- Dead line: the first `ok_pass` assignment (line ~389) is overwritten by line 390.
- Non-totality and denial-accounting: corroborated by `w1/R59Executor07.md` F4 —
  `foreign.write_bytes(...)` (line ~212) assumes the first safe leg created
  `<out-empty>/spans/`; a refusing candidate crashes with `FileNotFoundError`, no
  `C1=` line, and the control loop credits "no C1=PASS line" as `denied`,
  conflating counter crash with evaluated control denial.
- Containment scope: `w1/R59Executor07.md` F5 shows the snapshot basis is
  `out.parent` (the work dir), so writes outside `--work` are invisible; an
  escaping candidate reaches PASS once the case defect is repaired.

These match the r58 close (LOG round-58: counter defects recorded, "no post-data
counter edit or production builder patch was made"). They are the concrete content
a round-59 frozen claims.md must pin; none of it is pinned anywhere for round 59.

## What checks out

- `round59/census-start.txt` matches the long-standing baseline: five pre-existing
  W04 duplicate-URL rows (S051, S053, S073, S074, S075) over `corpus/SOURCES.md`,
  `chousa ok …/SOURCES.md`, `exit=0`. No new census defect. No `census-end.txt`
  exists yet for round 59.
- L0 fetch-scope `8d77e6c1` remains open and was honored: I performed no external
  fetch; the round's only source artifact is lane-held capture-derived bytes.

## Residual risk and verification gaps

1. Writer attribution for `round59/s101-open.txt` and `round59/controls/c1-before.txt`
   (L1 vs seat) is undetermined; my evidence stops at existence/mtime/hash.
2. I did not execute the r58 counter myself; the unreachability claim rests on the
   committed bytes I read (lines ~389–402, ~217–236) plus two peers' independent
   runs and QUALITY 115's recorded r58 finding. The byte-identities and hashes are
   my own commands.
3. Dual-tree accounting is incomplete: the visible roster omits 144+ live peers; I
   evidenced the collision class with the R59Executor07 and R59Executor01 pairs;
   other seats may collide likewise.
4. If the L1 intends to freeze `claims.md` only after wave data, no artifact says
   so, and it would contradict the rounds 29–58 precedent (freeze commit before
   wave-data commits) and QUALITY 115; as evidenced, the pointer was void at
   dispatch.
5. Reports are still arriving; `w1-results.json` does not exist yet, so no
   settle/dead-seat verdict is possible from this seat.

Report: .ufo/waves/round-59/w1/R59Reviewer41.md
