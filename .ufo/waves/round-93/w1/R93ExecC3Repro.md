# R93ExecC3Repro — frozen C3 (`C3-TALLY-R93`) reproduced from a clean tree

Seat: R93ExecC3Repro (executor, leaf). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Freeze `F2 = b7241252c2358613d3b22b7d0454d98c56dab373`; carrier `C2 = 754b62fb6adc60e44e12375af5461a0ebe302994`.
Attacked tree: `git clone --shared <lane> $S/repo` + `git -C $S/repo checkout 754b62fb…`;
`git rev-parse HEAD` → `754b62fb6adc60e44e12375af5461a0ebe302994`, `git rev-parse --show-toplevel`
→ `/fast/scratch/hyaku/chousa-r93/R93ExecC3Repro/repo` (receipt A, EXIT=0).
Scratch `S=/fast/scratch/hyaku/chousa-r93/R93ExecC3Repro`; every fixture, work dir and mini root lives
under it and is deleted before yield. No network access was made; no tool install or upgrade.

## (a) Counter on the clean tree — PASS

```
$ cd $S/repo
$ python3 -B corpus/evidence/round93/skill-tally-r93.py --root . \
    --selftest corpus/evidence/round93/controls/selftest-r93.txt
TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2
CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0
HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2 OTHERS_OK=1 TAIL_OK=1 LEGS=4/4
SKILL_TALLY_R93=PASS
EXIT=0
```
Receipt: `.ufo/waves/round-93/w1/R93ExecC3Repro-receipt-a-tally-clean.txt`.

Every field named in the frozen predicate matches the observed line:
`SKILL_TALLY_R93=PASS`, `LEGS=4/4`, `HIST_DERIVED=2/2`, `HIST_PRESENT=2/2`, `TAIL_OK=1`,
`TALLY_ROWS=8`, `STALE_TALLIES=0/8`, `CASE_RANGE_OK=2/2`, `MISLABELED=0`, `TAIL_TALLIES=2`,
`OTHERS_OK=1`. Exit 0. No deviation.

## (b) Controls battery — PASS

```
$ cd $S/repo
$ python3 -B corpus/evidence/round93/skill-tally-r93-controls.py --root . --work $S/ctl
OK positive: r92 rc=0 (SKILL_TALLY_R92=PASS), r93 rc=0 (SKILL_TALLY_R93=PASS)
OK old-prose-carried: r92 rc=1, r93 rc=1
OK stale-tally: r92 rc=1, r93 rc=1
OK deleted-historical: r92 rc=1, r93 rc=1
OK deleted-tail: r92 rc=0 (SKILL_TALLY_R92=PASS), r93 rc=1 (SKILL_TALLY_R93=FAIL)
OK added-tail: r92 rc=0 (SKILL_TALLY_R92=PASS), r93 rc=1 (SKILL_TALLY_R93=FAIL)
OK ungrounded-historical: r92 rc=0 (SKILL_TALLY_R92=PASS), r93 rc=1 (SKILL_TALLY_R93=FAIL)
CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1 HIST_REFUSED_BOTH=1/1
TAIL_REFUSED=2/2 TAIL_PRIOR_ACCEPTED=1/1 TAIL_ADDED_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1
EXIT=0
```
(Line-wrapped above; the receipt is verbatim.) Receipt:
`.ufo/waves/round-93/w1/R93ExecC3Repro-receipt-b-controls.txt`. All eight fields match the frozen
predicate exactly; the two tail trees are refused by r93 and accepted by r92 on identical bytes.

## (c) The derivation is not decorative — proven without the controls battery

Method: four mini roots under `$S/mini/<variant>`, each holding only `SKILL.md`, the two grounding
receipts at their repo-relative paths (`corpus/evidence/round25-final-measure.log`,
`corpus/evidence/round34/audit-dispositions.md`) and a copy of the committed selftest receipt. Each
variant mutates exactly one thing; nothing else is shared with the controls driver, which was not run
for this section. Both counters are then run on the *same* bytes.

Receipt: `.ufo/waves/round-93/w1/R93ExecC3Repro-receipt-c-derivation.txt`.

| variant | mutation | r93 observed | r93 rc | r92 rc |
|---|---|---|---|---|
| `base` (control) | none | `HIST_DERIVED=2/2 … LEGS=4/4`, `SKILL_TALLY_R93=PASS` | 0 | 0 (`SKILL_TALLY_R92=PASS`) |
| `fix161` (i) | `round25-final-measure.log:53` `PASS (161 cases, 0 skipped)` → `(162 cases, …)` | `HIST_FINDING HIST_UNGROUNDED 161 quote='PASS (161 cases, 0 skipped)' receipt=corpus/evidence/round25-final-measure.log`, `HIST_DERIVED=1/2`, `HIST_PRESENT=2/2`, `OTHERS_OK=0`, `LEG_FAIL OTHERS`, `SKILL_TALLY_R93=FAIL` | **1** | **0** (accepts) |
| `no215` (ii) | `SKILL.md:640` tally text `PASS (215 cases, 0 skipped)` → `PASS (215 cases)` | `TAIL_TALLIES=1`, `TAIL_OK=0`, `LEG_FAIL TAIL declared={('215','0'):1,('283','0'):1} observed={('283','0'):1}`, `SKILL_TALLY_R93=FAIL` | **1** | **0** (accepts) |
| `delline` (ii, literal) | `SKILL.md:640` deleted whole (`'`PASS (215 cases, 0 skipped)` under the host UTF-8 locale; original187'`) | `TAIL_TALLIES=1`, `TAIL_OK=0`, `LEG_FAIL TAIL observed={('283','0'):1}`, `SKILL_TALLY_R93=FAIL` | **1** | **0** (accepts) |
| `addtail` (iii) | appended `Undeclared tail probe: PASS (999 cases, 0 skipped)` at EOF | `HIST_SCOPE_BLEED line=999 cases tally=PASS (999 cases, 0 skipped)`, `TAIL_TALLIES=3`, `TAIL_OK=0`, `SKILL_TALLY_R93=FAIL` | **1** | **0** (accepts) |

(i) `HIST_DERIVED=1/2` and exit 1 exactly as frozen; the receipt is genuinely opened and the located
quote genuinely must appear in it. (ii) `TAIL_OK=0` and exit 1 while r92 exits 0 — both the textual
deletion and the whole-line deletion refuse identically. (iii) `HIST_SCOPE_BLEED` printed and exit 1
while r92 exits 0. The `base` control proves the mini-root construction itself is not what fails.

## (d) Hand re-derivation from `SKILL.md` alone

Derived by reading the committed `SKILL.md` (12 skipped-form occurrences in the whole file; the
mechanical confirmation is in `.ufo/waves/round-93/w1/R93ExecC3Repro-receipt-d-population.txt`).

Scope: `## Gates` opens at line **82**; the next ATX heading of depth ≤ 2 at column 0 is line **576**
`## Round26 metadata options and resource qualification`. Scope = lines 82–575. (Line 581 is a
depth-1 `#` line, but 576 bounds the scope first.)

Inside the scope, the population of `PASS (N cases, M skipped)` cells:

| line | tally | class |
|---|---|---|
| 86 | `PASS (283 cases, 0 skipped)` | current — row starts `` | `research-gate` `` |
| 87 | `PASS (283 cases, 0 skipped)` | current — `research-gate verify-claims` |
| 88 | `PASS (283 cases, 0 skipped)` | current — `research-gate verify-chain` |
| 89 | `PASS (283 cases, 0 skipped)` | current — `research-gate verify-sweeps` |
| 90 | `PASS (283 cases, 0 skipped)` | current — `research-gate verify-integrity` |
| 91 | `PASS (283 cases, 0 skipped)` | current — `research-gate verify-all` |
| 92 | `PASS (283 cases, 0 skipped)` | current — `research-gate verify-metadata` |
| 93 | `PASS (283 cases, 0 skipped)` | current — `research-gate --pin / --drift` |
| 186 | `PASS (256 cases, 0 skipped)` | non-current — prose "round 34: they now read …" |
| 188 | `PASS (161 cases, 0 skipped)` | non-current — prose "the final round-25 shared selftest was" (grounded at `round25-final-measure.log:53`) |

Outside the scope:

| line | tally | class |
|---|---|---|
| 640 | `PASS (215 cases, 0 skipped)` | tail — Round27 subsection prose |
| 781 | `PASS (283 cases, 0 skipped)` | tail — the host line ("Selftest … on this host") |

Hand multiset, current rows: `{(283,0): 8}` — matches the tool's own verdict `283 cases, 0 skipped`,
so the staleness population is empty.
Hand multiset, non-current rows: `{(161,0): 1, (256,0): 1}` (`OTHER_OCCURRENCES=2`).
Hand multiset, tail: `{(215,0): 1, (283,0): 1}` (`TAIL_TALLIES=2`).
Hand total: 10 in scope + 2 outside = 12 skipped-form occurrences.

Agreement with the instrument is exact on every count (`TALLY_ROWS=8`, `OTHER_OCCURRENCES=2`,
`HIST_PRESENT=2/2`, `TAIL_TALLIES=2`, `TAIL_OK=1`). Grounding lines re-read independently:
`corpus/evidence/round25-final-measure.log:53` = `RESEARCH_GATE_SELFTEST: PASS (161 cases, 0 skipped)`
(1 occurrence in the file) and `corpus/evidence/round34/audit-dispositions.md:5` contains
`PASS (256 cases, 0 skipped)` (1 occurrence).

## Extra probes against kill rule K4 (derivation vacuous) and named limit 3 (scope boundary)

Receipt: `.ufo/waves/round-93/w1/R93ExecC3Repro-receipt-k4-probes.txt`.

| probe | purpose | observed | rc |
|---|---|---|---|
| `sub215`: tail pair `(215,0)` → `(216,0)`, tail **count stays 2** | K4 "tail set compared by count only rather than by `(cases, skipped)` pairs" | `HIST_SCOPE_BLEED line=216 cases tally=PASS (216 cases, 0 skipped)`, `TAIL_TALLIES=2`, `TAIL_OK=0`, `LEG_FAIL TAIL observed={('216','0'):1,('283','0'):1}` — r92 on the same bytes `SKILL_TALLY_R92=PASS` rc 0 | r93 1 |
| `nohist`: the in-scope `161` tally rewritten to `PASS (161 cases)` | K4 "the tally is not required to be present in scope" | `HIST_FINDING HIST_MISSING PASS (161 cases, 0 skipped)`, `HIST_PRESENT=1/2`, `LEG_FAIL OTHERS` | r93 1 (r92 also 1, its frozen literal) |
| `noscopebound`: every depth ≤ 2 heading after line 82 removed | named limit 3 / `SCOPE_BLEED` | `SKILL_TALLY_R93=SETUP SCOPE_BLEED no next-## or #-level heading after ## Gates` | 2 (r92 identical, rc 2) |

The pair-vs-count probe is the decisive one: the tail count is unchanged at 2 and the tree is still
refused, so the leg compares `(cases, skipped)` pairs. `nohist` is recorded honestly as a
non-discriminating tree — r92 refuses it too, because its frozen literal names `161`; the r93 difference
there is the diagnostic (`HIST_MISSING` naming the tally) and the `HIST_PRESENT=1/2` counter, not a
refusal r92 lacks. The scope-boundary probe shows the unterminated-scope case is a setup diagnostic
(rc 2) in both counters, never a silent EOF bleed.

## Unchanged instruments checked at the tree I attacked

```
$ git -C $S/repo diff --stat 206226dc9d9baef620e7d3d30bdac5f9194a459f..754b62fb6adc60e44e12375af5461a0ebe302994 \
    -- tools/research-gate.sh tools/gate-records.py SKILL.md
(empty output, EXIT=0)
```
`git diff --name-status 206226dc..754b62fb` lists 17 additions only — the round-93 instruments, the
claims files and the control receipts — no modification of `tools/research-gate.sh`,
`tools/gate-records.py` or `SKILL.md`. C3 therefore reads the same gate surface r92 read.

## Observations (none fires a kill rule)

1. **Twelve in-scope `PASS (N cases)` forms are outside the cell grammar.** On 10 lines — 160
   (`PASS (3 cases)`), 161 (`PASS (10 cases)`), 186 (three: `PASS (228 cases)`, `PASS (241 cases)`,
   `PASS (251 cases)`), 250, 273, 309, 346, 393, 437, 489 (seven forms like
   `` `--selftest` is `PASS (30 cases)` ``) — the cell carries no `skipped` field, so
   `TALLY_RE = PASS \((\d+) cases, (\d+) skipped\)` does not see it in either counter
   (`grep -oE 'PASS \([0-9]+ cases\)' SKILL.md | wc -l` → 12, all twelve inside lines 82–575). This is
   inherited r92 grammar, not a round-93 regression, and it is not covered by a named limit —
   recorded as a residual for the L1: a *new* historical tally written without a skipped count inside
   the Gates scope would be invisible to the OTHERS leg. No existing value is affected: all 12
   skipped-form occurrences and all 8 current rows agree with the hand multiset and the instrument.
2. The four `research-gate`-prefixed table rows at 104, 105, 106, 117 carry no `PASS` tally at all, so
   `TALLY_ROWS=8` (not 12) is the correct current-row count and the hand derivation reproduces it.
3. Named limits 1–3 as frozen: the receipts are caught by quote (not digest) — confirmed by `fix161`;
   the tail set is a declared measurement, not a derivation — confirmed by `addtail`/`sub215`; the scope
   is the ATX depth ≤ 2 boundary with `SCOPE_BLEED` — confirmed by `noscopebound`.

## Receipts copied into this folder

- `R93ExecC3Repro-receipt-a-tally-clean.txt` — (a) counter on the clean tree + HEAD/toplevel pins.
- `R93ExecC3Repro-receipt-b-controls.txt` — (b) controls battery.
- `R93ExecC3Repro-receipt-c-derivation.txt` — (c) five variants × {r93, r92}.
- `R93ExecC3Repro-receipt-d-population.txt` — (d) raw population reads of `SKILL.md` and the two receipts.
- `R93ExecC3Repro-receipt-k4-probes.txt` — K4 pair/presence and named-limit-3 probes.

Scratch `/fast/scratch/hyaku/chousa-r93/R93ExecC3Repro` removed before yield. No production file, no
lane git state, no host sysctl, no service was touched; no tool was installed or upgraded.

VERDICT: R93ExecC3Repro C3 held — `SKILL_TALLY_R93=PASS` with `LEGS=4/4 HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_OK=1 TALLY_ROWS=8 STALE_TALLIES=0/8 CASE_RANGE_OK=2/2 MISLABELED=0` at exit 0 on carrier C2, controls `CONTROLS=PASS` at exit 0, and the derivation discriminates independently of them (receipt-mutated `HIST_DERIVED=1/2` rc 1, tail-deleted `TAIL_OK=0` rc 1, undeclared-tail `HIST_SCOPE_BLEED` rc 1, each accepted by r92 at rc 0).
