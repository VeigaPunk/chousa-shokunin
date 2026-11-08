# R94ExecC3Repro — C3 freshness, reproduced from a clean carrier clone

Seat `R94ExecC3Repro` (executor, round 94). Leaf seat: no dispatch, no production edits, no git/jj mutation in
the lane, no network, no tool installs or upgrades, no pacman, no sudo.

- Base `0f3f84dab3a094ec0a2fe8ae9ae59d3326e1a9b6`; freeze `F 41038ed7c40cffc4cf86d649a6ba433c4b9eec1a`;
  carrier `C 352924bbea624caf3771ef291be98fd4ec679dda` (the tree attacked here).
- Scratch `S=/fast/scratch/hyaku/chousa-r94/R94ExecC3Repro`; clone
  `git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo` (S221: a `--shared` clone starts
  without objects of its own; it was never repacked), then
  `git -C $S/repo checkout 352924bbea624caf3771ef291be98fd4ec679dda`.
  `git -C $S/repo rev-parse --show-toplevel` printed `/fast/scratch/hyaku/chousa-r94/R94ExecC3Repro/repo` and
  `git -C $S/repo rev-parse HEAD` printed `352924bbea624caf3771ef291be98fd4ec679dda` (exit 0 in both).
  `git -C $S/repo status --porcelain` printed nothing after every run: no counter or fixture wrote into the clone.
- All commands below ran **from `$S/repo`** (`cd` into it), `TMPDIR=$S/tmp`, and every work dir under `$S`.
- Receipts cited here are copied to `.ufo/waves/round-94/w1/R94ExecC3Repro-receipts/` (same names as below).

## (a) the C3 counter on the clean carrier tree — PASS

Command (exactly the frozen counting command, lane root = `$S/repo`):

```bash
python3 -B corpus/evidence/round94/skill-tally-r94.py --root . \
  --selftest corpus/evidence/round94/controls/selftest-r94.txt
```

Observed line (receipt `R94ExecC3Repro-receipts/c3-a-counter.txt`):

```text
TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2 TAIL_OWNED_OK=2/2 OTHERS_OK=1 TAIL_OK=1 LEGS=4/4
SKILL_TALLY_R94=PASS
```

Exit code `0`. Every token of the frozen predicate is present
(`LEGS=4/4 TAIL_OK=1 TAIL_OWNED_OK=2/2 HIST_DERIVED=2/2 HIST_PRESENT=2/2 STALE_TALLIES=0/8 CASE_RANGE_OK=2/2
MISLABELED=0 TALLY_ROWS=8 TAIL_TALLIES=2`); `EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2
CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283` are extra observability fields, not deviations.

Independent census of the same scope (receipt `c3-gates-census.txt`):
`sed -n '82,575p' SKILL.md | grep -nE 'PASS \([0-9]+ cases, [0-9]+ skipped\)'` returns ten lines in the Gates
scope — the eight `| `research-gate…` rows (scope-relative lines 5–12 = SKILL.md 86–93) and the two historical
groundings at SKILL.md 186 (`256`) and 188 (`161`). That is exactly `TALLY_ROWS=8` and `OTHER_OCCURRENCES=2`,
measured without the counter. `sed -n '1,81p' SKILL.md | grep …` returns nothing, matching `HEAD_DECLARED={}`
(receipt `c3-head-tail.txt`).

## (b) the C3 controls battery — PASS

Command:

```bash
python3 -B corpus/evidence/round94/skill-tally-r94-controls.py --root . --work $S/ctl
```

Observed line (receipt `c3-b-controls.txt`), exit `0`:

```text
CONTROLS=PASS CARRIED_REFUSED=6/6 MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1 TAIL_ADDED_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1
```

The frozen subset (`CONTROLS=PASS CARRIED_REFUSED=6/6 MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2
DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1`) is present verbatim; the three trailing fields are extra cases.
The per-case log records the discrimination directly: `moved-tail-215` and `moved-tail-283` are
`r93 rc=0 (SKILL_TALLY_R93=PASS), r94 rc=1 (SKILL_TALLY_R94=FAIL)`, and `moved-to-heading` is `r93 rc=0,
r94 rc=0`.

## (c) independent owner-binding measurement (not the battery)

Fixture driver `R94ExecC3Repro-receipts/fixture-owner-binding.py` (copy of `$S/owner_binding.py`); heading
derivation `R94ExecC3Repro-receipts/fixture-scope.py`. Each fixture is a fresh directory under `$S/fix/<name>/`
holding only the carrier `SKILL.md`, the two grounding receipts
(`corpus/evidence/round25-final-measure.log`, `corpus/evidence/round34/audit-dispositions.md`) and the committed
`corpus/evidence/round94/controls/selftest-r94.txt`; both counters were invoked from `$S/repo` with
`--root <fixture> --selftest <fixture>/corpus/evidence/round94/controls/selftest-r94.txt`, so only the fixture's
`SKILL.md` varies. Full transcript: `R94ExecC3Repro-receipts/owner-binding.txt`; per-fixture tail ownership:
`c3-fixture-ownership.txt`.

| fixture | mutation (tail multiset unchanged: 1×`215`, 1×`283`) | r93 | r94 |
|---|---|---|---|
| `positive` | none (construction control) | rc 0, `SKILL_TALLY_R93=PASS`, `TAIL_OK=1`, `LEGS=4/4` | rc 0, `SKILL_TALLY_R94=PASS`, `TAIL_OWNED_OK=2/2`, `TAIL_OK=1`, `LEGS=4/4` |
| `both-moved-into-round36` | BOTH tally lines moved into the Round 36 section (nearest heading line 717 in the fixture) | rc 0, `TAIL_OK=1`, `LEGS=4/4`, PASS | rc 1, `TAIL_OWNED_OK=0/2`, `TAIL_OK=0`, `LEGS=3/4`, FAIL |
| `alias-heading` | `283` tally moved under `### Round 37 — the claim-pin provenance — carried notes (2026-11-08)` | rc 0, PASS | rc 0, `TAIL_OWNED_OK=2/2`, `TAIL_OK=1`, PASS |
| `swapped-owners` | `215` under the Round 37 heading and `283` under the Round 27 heading (each under the *other* declared owner) | rc 0, `TAIL_OK=1`, PASS | rc 1, `TAIL_OWNED_OK=0/2`, `TAIL_OK=0`, FAIL |
| `third-tail` | one undeclared `PASS (999 cases, 0 skipped)` appended in the tail | rc 1, `TAIL_TALLIES=3`, `LEG_FAIL TAIL` | rc 1, `TAIL_TALLIES=3`, `TAIL_OWNED_OK=2/2`, `LEG_FAIL TAIL` |

Exact `TAIL_OWNER_*` lines, `both-moved-into-round36` (r94, rc 1):

```text
TAIL_OWNER_FINDING TAIL_OWNER_MISMATCH tally=215 cases tally=PASS (215 cases, 0 skipped) owner=### Round 36 — the engine-swap canary and per-record attribution (2026-10-23) declared=Round27 repair/status correction
TAIL_OWNER_FINDING TAIL_OWNER_MISMATCH tally=283 cases tally=PASS (283 cases, 0 skipped) owner=### Round 36 — the engine-swap canary and per-record attribution (2026-10-23) declared=Round 37 — the claim-pin provenance
TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2 TAIL_OWNED_OK=0/2 OTHERS_OK=1 TAIL_OK=0 LEGS=3/4
LEG_FAIL TAIL declared={('215', '0'): 1, ('283', '0'): 1} observed={('215', '0'): 1, ('283', '0'): 1}
SKILL_TALLY_R94=FAIL
```

`swapped-owners` (r94, rc 1) — the sharper case, because both headings ARE the two declared owners and only the
pairing is wrong:

```text
TAIL_OWNER_FINDING TAIL_OWNER_MISMATCH tally=215 cases tally=PASS (215 cases, 0 skipped) owner=### Round 37 — the claim-pin provenance and the pin-capture environment (2026-10-23) declared=Round27 repair/status correction
TAIL_OWNER_FINDING TAIL_OWNER_MISMATCH tally=283 cases tally=PASS (283 cases, 0 skipped) owner=### Round27 repair/status correction — 2026-10-21 declared=Round 37 — the claim-pin provenance
```

`alias-heading` (r94, rc 0) — **named limit 1 confirmed by measurement**: the moved tally's nearest heading is a
*different* heading that only contains the declared owner substring, and r94 accepts it:

```text
TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2 TAIL_OWNED_OK=2/2 OTHERS_OK=1 TAIL_OK=1 LEGS=4/4
SKILL_TALLY_R94=PASS
```

No `TAIL_OWNER_FINDING` line is emitted for any of its three runs; r93 also passes it (`TAIL_OK=1`, rc 0).
`third-tail` confirms named limit 4 in the refusal direction: an undeclared third tail tally prints
`HIST_SCOPE_BLEED line=999 cases tally=PASS (999 cases, 0 skipped)` and `LEG_FAIL TAIL` under r94 (rc 1), i.e.
the declarations are measured pairs, not a derivation.

Reading of the evidence: the multiset is byte-for-byte preserved in `both-moved-into-round36` and
`swapped-owners` (the fixture script asserts one tail occurrence of each tally before writing), r93 is green on
both, and r94 is red on both with the observed headings named — so `TAIL_OWNED_OK` is computed from the observed
nearest headings, not from the declarations (C3 K4). Because the swap is refused even when each tally sits under
a *declared-owner* heading (the other one's), the binding is per tally, not merely "inside the declared set".

## (d) the exact heading each declared tally sits under (from `SKILL.md` alone)

Derived by `fixture-scope.py` (nearest preceding column-0 `^#{1,6} ` heading), receipt `c3-headings.txt`, carrier
`SKILL.md` = sha256 `dcdf92341b25553ba84fd3f6c0178161fa2f0e6c74c76b8a7cc92bb1f1c789bc`:

| tally | line | nearest heading | heading line |
|---|---|---|---|
| `PASS (215 cases, 0 skipped)` | 640 | `### Round27 repair/status correction — 2026-10-21` | 634 |
| `PASS (283 cases, 0 skipped)` | 781 | `### Round 37 — the claim-pin provenance and the pin-capture environment (2026-10-23)` | 758 |

`## Gates` is at line 82 and the Gates scope ends at the next `#`/`##` heading, line 576
(`## Round26 metadata options and resource qualification`), so both tallies are tail tallies. Those are the only
two tallies after line 576 (receipt `c3-head-tail.txt`); the head (lines 1–81) holds none. The line numbers the
counter's own comment cites (`SKILL.md:640`, `SKILL.md:781`) match this measurement exactly.

## Cross-checks against the carrier and the pins table

- Base invariance (receipt `c3-invariants.txt`): `git diff --stat 0f3f84da…352924bb -- SKILL.md
  tools/research-gate.sh tools/gate-records.py` printed nothing, rc 0; `git rev-parse
  0f3f84da…:SKILL.md` and `git rev-parse 352924bb…:SKILL.md` both print
  `743f3e3f4bb5f929e04deaf04ed14318e9cf4629` — `SKILL.md` is byte-identical from base to C, and the two gate
  tools are untouched this round, as the round states.
- The two C3 instruments and their selftest receipt are unchanged between F and C:
  `git diff --stat F..C -- corpus/evidence/round94/skill-tally-r94.py
  corpus/evidence/round94/skill-tally-r94-controls.py corpus/evidence/round94/controls/selftest-r94.txt` printed
  nothing, rc 0.
- Digest/pin agreement (receipt `c3-digests.txt`): `sha256sum` at C gives
  `da49d068…d8cd880` (`skill-tally-r94.py`), `76840a41…065a6` (`skill-tally-r94-controls.py`),
  `9c294281…5bb37` (`controls/selftest-r94.txt`), `54dfdd39…98f07` (`round93/skill-tally-r93.py`),
  `6cc56191…b0ef0` (`round93/skill-tally-r93-controls.py`) — each equals its `corpus/evidence/round94/instrument-pins.txt`
  row verbatim (rows 17, 20, 23, 29, 32). The five C3-relevant rows carry `role=driver`, so under C1's design the
  role-coverage leg byte-checks but does not cover them (C1 named limit 2); C3's own predicate does not depend on
  the role leg.
- `instrument-pins.txt` self row 34 is `498873a9…`, while the file's own sha256 is `6b2c5579…`; this matches
  `make-pins-r94.py` line 14/110 ("the self row is the minus-self digest"), so it is the declared self-pin rule,
  not a mismatch. Recorded only as a cross-check; the self-pin verdict belongs to C1's driver.

## Findings

1. **No deviation from the frozen C3 predicate.** (a) and (b) printed every required token with exit 0 on the
   carrier clone; nothing was rerun to confirm a user-reported failure (there was none).
2. **Observation O1 — the measured subject is not pinned.** `SKILL.md` has no row in
   `corpus/evidence/round94/instrument-pins.txt` (`grep -nE 'SKILL.md' …` printed nothing). The clean-tree
   verdict is therefore bound by the git revision C alone, not by the pins table. This is outside C3's frozen
   predicate (its kill rules do not require a `SKILL.md` pin) and outside C1's covered roles (data subject, not
   harness), but it means a working-tree edit of `SKILL.md` is caught only by the counter's own legs, never by a
   pin walk. Not a claim failure; routed as an observation for the reviewer.
3. **Observation O2 — named limit 1 is real, not decorative.** A tally under a heading that merely contains the
   declared owner string is accepted (`alias-heading`, rc 0, `TAIL_OWNED_OK=2/2`). The claim states this
   (`HEADING_ALIAS_ACCEPTED` measures it); this seat measured it independently and it is not hidden.
4. **Observation O3 — the tail set is one-directional about section identity.** `both-moved-into-round36` and
   `swapped-owners` both preserve the multiset and are refused only through the owner leg (`TAIL_OWNED_OK=0/2`,
   `LEGS=3/4`), while `TAIL_TALLIES=2` stays at 2. That is the intended r93→r94 delta, reproduced.

Named limits 2 (any column-0 `#`…`######` heading, no setext/indented parse) and 3 (a tally inside a fenced code
block is attributed to the preceding heading) were **not** independently measured by this seat; the frozen
predicate does not require them and no claim sentence depends on them beyond the declaration.

## Residual risk / blockers

- None material for C3. The reproduction used the committed selftest receipt (283 cases, 0 skipped, 283 `ok-case`
  lines counted by `grep -c`) rather than re-running `tools/research-gate.sh --selftest`; the frozen counting
  command takes `--selftest`, and the gate tools are verified unchanged base→C above.
- Scratch `$S` was deleted after the receipts were copied; nothing under `/tmp`, `~/.local/bin`, the fleet root,
  `MANIFEST.json`, `considerthese/` or any sibling repo was touched. No tool install or upgrade was performed.

VERDICT: R94ExecC3Repro C3 held — on a clean `--shared` clone at carrier `352924bbea624caf3771ef291be98fd4ec679dda` the counter printed `SKILL_TALLY_R94=PASS` with `LEGS=4/4 TAIL_OK=1 TAIL_OWNED_OK=2/2 HIST_DERIVED=2/2 HIST_PRESENT=2/2 STALE_TALLIES=0/8 CASE_RANGE_OK=2/2 MISLABELED=0` (rc 0) and the controls `CONTROLS=PASS CARRIED_REFUSED=6/6 MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1` (rc 0), while an independent both-moved fixture and a swapped-owner fixture are refused only by r94 (`TAIL_OWNER_MISMATCH` for both tallies, `TAIL_OWNED_OK=0/2`) and a containing heading is accepted (named limit 1), with the declared tallies at `SKILL.md:640` under `### Round27 repair/status correction — 2026-10-21` (line 634) and `SKILL.md:781` under `### Round 37 — the claim-pin provenance and the pin-capture environment (2026-10-23)` (line 758).
