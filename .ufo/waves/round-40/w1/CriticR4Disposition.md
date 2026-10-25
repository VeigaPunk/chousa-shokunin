# CriticR4Disposition — adversarial audit of the R4 `not-reproduced` disposition

seat: CriticR4Disposition (leaf L2, chousa round 40, wave 1)
assigned attack: seek an alternate committed validated spec or plan carrying the
spot-check's contrary counts (reviewer 8 / revenger 0); state whether the current
evidence supports the R4 closure note.
lane root: /home/vgpnk/Projects/shokunin/chousa-shokunin (all paths absolute)
disposition under test: `corpus/evidence/round40/routed-defect-dispositions.json` →
R4 `"status": "not-reproduced"`, decision "Committed r39 spec, plan, and report agree
on reviewer 6 and revenger 2 (32 seats); the spot-check's reviewer 8 and revenger 0
assertion does not match those artifacts."
contrary claim: `corpus/lessons/round-39-verifier-spotcheck.md` R4 line — "the
validated spec (`w1-spec.json`: reviewer 8 / revenger 0; totals 32 both)".

## Verdict

**Disposition SUPPORTED — attack fails.** No committed artifact in any ref, orphan
commit, or working tree carries reviewer 8 / revenger 0 for round 39. Every readable
authority — spec `items[].role`, plan `tasks[].agent`, plan `registry.members[].role`,
the committed `DISPATCH-README.md`, the generator `gen-w1-spec.py`, and the fleet
report prose — agrees on reviewer 6 / revenger 2 / 32 seats. The counter's R4
conditions all hold (`R4_DISPOSITION=ok`, observed live). The closure note stands.

## Commands and outputs

1. Role mixes, working tree vs committed revisions (python3 + `git show`):

   - `w1-spec.json` items→role at working tree, tip `6ac1007e6a5d…`, and orphan
     commits `35e10b9a…`, `7180206b…` (the only other objects containing the path,
     `git log --all --oneline -- <both paths>`): all identical —
     `{executor:6, reviewer:6, critic:5, scout:3, scribe:3, mutation-tester:3,
     sentinel:2, revenger:2, connector:1, simplifier:1}`, n=32.
   - `w1-plan.json` tasks→agent: identical mix at all revisions; `counts
     {spawn:32, resume:0, total:32}`; `registry.members` role field: identical mix;
     `w1-plan.err` = 0 bytes (validator accepted; the plan is the *validated* plan).
   - `BASE39 8c7c867b…`: both paths absent — the wave was authored inside round 39;
     no earlier committed spec exists to conflict.

2. Full-lane JSON sweep for the alternate mix (every `*.json` under the lane,
   counting `items[].role`, `tasks[].agent`, `seats[].role`, `items[].agent`,
   `tasks[].role`): **zero files with reviewer==8 and revenger==0.** The only spec
   anywhere with reviewer 8 is `round-33/w2-spec.json` (reviewer 8, no revenger
   field, 34 seats, wrong round, wrong total) — it cannot be the cited
   `w1-spec.json` and the spot-check pins `totals 32`, which excludes it.

3. Fleet-repo provenance check: `git grep` in /home/vgpnk/Projects/shokunin finds
   no copy of the r39 spec; round-39 references exist only in `.ufo/prompts/` and
   `.ufo/reports/round-39/chousa.md`. Report lines 169–170 state
   "reviewer 6 … revenger 2" — matching the spec, not the spot-check. No
   `w1-dispatch.json` exists under `.ufo/waves/round-39/` (the wave was prepared
   and validated but not dispatched, per DISPATCH-README.md) — so there is no
   dispatched-variant plan that could carry different counts.

4. `git status --porcelain -- .ufo/waves/round-39/` → empty; working tree equals
   committed bytes. `git stash list` → empty.

5. `python3 corpus/evidence/round40/c2-count.py` →
   `R2_DISPOSITION=ok R3_DISPOSITION=ok R4_DISPOSITION=ok R5_DISPOSITION=ok
   R39_CALIBRATION_DISPOSITIONS=4/4` (rc 0). All three R4 code conditions
   (spec_mix == plan_mix, reviewer==6, revenger==2, report strings present,
   spotcheck contrary string present, disposition status `not-reproduced`)
   verified satisfied.

## Provenance of the wrong counts (why the spot-check failed this way)

The spec's 32 seat names include eight `Rev*` names: six reviewers
(`RevClaims, RevSeparability, RevCounters, RevGate, RevRoutedDefects, RevReceipts`)
plus the **two revengers, named `RevErrataCtx` and `RevTextOverreach`**. Counting
seat names by `Rev*` prefix instead of the `role` field yields exactly the
spot-check's "reviewer 8 / revenger 0" while preserving "totals 32". This is a
concrete, benign mechanism for the contrary claim — it requires no alternate
committed artifact, which is why none exists.

## Counterexample search — negative results

- No committed spec/plan/dispatch/registry file anywhere in the lane carries
  reviewer 8 / revenger 0 (sweep, item 2 above).
- No committed version of `w1-spec.json`/`w1-plan.json` differs across
  `git log --all` (three commits, identical mixes).
- The spot-check's own evidence row cites `w1-spec.json` — the file it names
  refutes its numbers when counted by the `role` field.

## Residual risk note (smallest safe correction: none required)

The disposition's decision text already preserves the conflict verbatim and cites
all four artifacts; the frozen kill rule ("R4 must not be changed to a positive
'fixed' label while its cited spec/plan/report agree") is respected. Optional
hardening only: the disposition `decision` string could name the `Rev*`-prefix
miscount mechanism to make the not-reproduced call self-evidently grounded, but
this is cosmetic — the cited evidence pointers resolve and agree as written.

## Artifact pointers

- `corpus/evidence/round40/routed-defect-dispositions.json` (R4 block, lines 20–30)
- `.ufo/waves/round-39/w1-spec.json` / `w1-plan.json` / `DISPATCH-README.md` /
  `gen-w1-spec.py:63-64,118-156,270-277`
- `corpus/lessons/round-39-verifier-spotcheck.md` (R4 routed-defect line)
- `fleet:.ufo/reports/round-39/chousa.md:168-170`
- `corpus/evidence/round39/claims.md` errata R4 entry

Tool installs this seat: none (read-only git/python3 over committed bytes;
pacman pause respected).
