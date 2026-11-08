# Round 93 — frozen claims (chousa, L1 ChousaR93, 2026-11-08)

Base: lane branch tip `206226dc9d9baef620e7d3d30bdac5f9194a459f` (in sync with origin before the round).
Census at round start, exit 0 (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin chousa`): five pre-existing `W04` duplicate-url warnings, `chousa ok`,
registry 219 rows. Pinned in `corpus/evidence/round93/census-start.txt`.

Claims come from the scorecard's round-93 plan (`SCORECARD.md` lines 4134–4146) and from the r92
non-author spot-check's three routed residuals (`corpus/lessons/round-92-verifier-spotcheck.md`
"Routed defects for next round"). Three claims, three axes, no exploratory claim. Freeze `F4` carries the
instruments; carrier `C5` carries the receipts and the completed pins table. Earlier pairs
(`F 84998563`, `F2 b7241252`/`C2 754b62fb`, `F3 d5c19c5`/`C4 94fbf892`) were superseded before filing —
each defect is named in `corpus/lessons/round-93.md` `## Mistakes` and in the round report's amendments.
The wave attacked `F2/C2`; every wave finding that changed a sentence is applied below and marked as an
amendment, and the numbers here are the landing-instrument numbers re-measured after the fixes.

## C1 `C1-DRIVER-R93` — operability (lowest scored non-retired axis; historical 3/10 held)

**Before** (r92 driver, `corpus/evidence/round92/control-driver-r92.py`): its pin walk covers only the
instruments its six expected rows execute plus the expectations and pins files —
`RECEIPT PINS OK 7/16 pinned files byte-identical`, `PINNED_FILES=7` — and its pins table pins no receipt.
In the tree-only `verify` form (`--repo` absent, the default form) a tampered copy of an unexecuted pinned
instrument and a tampered receipt body each verify `CONTROL_DRIVER_R92=PASS` (rc 0,
`corpus/evidence/round93/evidence-before/c1-prior-accepts.txt`); with `--repo` it binds the receipts to the
named revision but still pins none of them in the table, and it resolves its own inputs from the driver's
directory, so `--root <other tree>` without explicit paths exits with `SETUP path escapes base`.

**After** (`corpus/evidence/round93/control-driver-r93.py`): `CONTROL_DRIVER_R93=PASS` (exit 0) with
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6` and
`RECEIPT SELF_PIN OK rev=F4 receipts_rev=C5`, where PASS requires `findings==0`, every row
committed/exact/pin/fresh, `checked==len(pins)` AND `rchecked==rtotal>0`. The pins table is the population:
each of its 22 rows is byte-checked on disk (`PIN_DISK_MISMATCH path=<rel>` per row, `PIN_MISSING path=<rel>`
for an absent file, `RECEIPT_MISMATCH <case>` / `RECEIPT_UNPINNED <case>` for the six receipt rows), the
pins file's own row stays the minus-self digest. `--expected`, `--receipts` and `--pins` derive from
`--root`; the driver's own bytes are resolved against `--repo` (the tree the driver lives in), so the
dispatch form `--root <clone> --repo <lane>` scores normally instead of refusing.

**Counting command** (from the lane root):

```bash
python3 -B corpus/evidence/round93/control-driver-r93.py verify --root . --repo . \
  --rev <F4> --receipts-rev <C5> --work "$HYAKU_SCRATCH/chousa-r93/c1/verify"
python3 -B corpus/evidence/round93/forgeries-r93.py --root . --repo . --rev <F4> --receipts-rev <C5> \
  --work "$HYAKU_SCRATCH/chousa-r93/c1/forgeries"
```

**Predicate.** The verify command prints `CONTROL_DRIVER_R93=PASS` with those fields and exits 0; the
battery prints `FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 POSITIVE=pass` and exits 0, where the
two refusals are `PIN_DISK_MISMATCH` on an unexecuted pinned instrument and `RECEIPT_MISMATCH` on a receipt
body, each accepted (rc 0) by the r92 driver in the tree-only form on the same bytes, and `DERIVE_OK` is
the r92 driver refusing the derived-default form (`escapes base`) that the r93 driver scores normally.

**Kill rules.** K1 the predicate not met at the landing revision. K2 a battery forgery accepted by the r93
driver, the positive refused, or the r92 driver refusing both forgeries. K3 a genuine row moved by the pin
walk, or `verify` writing under the receipts directory. K4 the PASS skips the work: a pin row equal to
itself by construction, a receipt counted without its pin row, or `--root` ignored in favour of the
driver's directory.

**Named limits.** (1) A coherent joint edit of an instrument, its pin row, its receipt and its expectation
row survives — that edit is the harness. (2) The minus-self digest binds the table's coherence, not its
authority: the self row itself cannot be protected. (3) Pinned bytes are compared at `F4`/`C5`; a script
that reads data outside its own bytes is unseen. (4) A receipt added after `C5` is `RECEIPT_UNPINNED`; a
removed receipt row stops being scored only if its expected row also goes. (5) The battery's `PRIOR_ACCEPTED`
is measured in the tree-only r92 form — a `--repo` r92 run binds receipts to a revision, which is a
different mechanism, not a pin.

**Sources.** `S070` (installed `sha256sum(1)`: the digest text and `--check` input this pin discipline rests
on).

## C2 `C2-CURATION-R93` — calibration

**Before** (r92 counter, `corpus/evidence/round92/curation-r92.py`): `CURATION_R92=PASS` with
`LEGS_MEASURED=14/14 Q_SHAPE_FAIL=0`. On a whitespace-quote tree — one Located-quotes row whose quote cell
is `" "` — r92 prints `Q_SHAPE_FAIL=0` and refuses only downstream (`LEG_FAIL FLOOR`, `LEG_FAIL WARRANT`,
`LEG_FAIL TFREQ`): the class is never named, and no `Q_WSQUOT` field exists
(`corpus/evidence/round93/evidence-before/c2-prior-accepts.txt`).

**After** (`corpus/evidence/round93/curation-r93.py`): `CURATION_R93=PASS` (exit 0) with
`LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_ROWS=20 Q_FLOORS=<per-entry> WARRANT_OK=17/17
TFREQ_OK=17/17 DUP_QIDS=0 SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20`
and `VERDICT fields_hold=1 legs_ok=15/15 DETECTOR_WITNESS=13/13`. The fifteenth leg is `WSQUOTE`: every
three-cell Located-quotes row whose quote strips to empty is counted (`Q_WSQUOT`) and `q_shape_violation`
refuses the same row with `quote=<whitespace>`; the leg and the shape branch share one expression
(`ws_quote_cell`), so the leg is a second witness of the class and its verdict-bearing force is the
`EXPECTED_LEGS` arity check, which now prints `LEG_FAIL ARITY expected=15 measured=<n>` when a leg is
removed. A wrong-width decision row prints one `DECISION_WIDTH <entry> row=<line> cells=<n>` line.

**Counting command** (from the lane root):

```bash
python3 -B corpus/evidence/round93/curation-r93.py --root .
python3 -B corpus/evidence/round93/curation-controls-r93.py --root . --work "$HYAKU_SCRATCH/chousa-r93/c2/controls"
```

**Predicate.** The counter prints `CURATION_R93=PASS` with `LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0
Q_WSQUOT=0 DETECTOR_WITNESS=13/13` and exits 0; the controls print `CONTROLS=PASS
CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7` and
exit 0, where `WS_NAMED` are the two whitespace trees (space and tab inside the quotes) that r93 refuses at
the shape leg as `quote=<whitespace>` with `Q_WSQUOT=1` while r92 reports `Q_SHAPE_FAIL=0` on the same
bytes, and `CARRIED_REFUSED_BOTH` are the four round-92 classes still refused by both counters. This is a
classification claim: r92 fails those trees too, but it cannot name the cause, and `WS_SHAPE_GREEN_R92`
re-derives that blindness on every run.

**Kill rules.** K1 the predicate not met at the landing revision. K2 a whitespace tree whose shape leg
stays green under r93, the positive refused, or `DETECTOR_WITNESS` not full. K3 a genuine entry moved: all
20 located quotes, the 17 warranted decision rows and the two quote floors must hold at the landing
revision. K4 the new leg is vacuous: it must count the row on both forged trees and stay 0 on the clean
tree, and deleting it must change the verdict through the named `LEG_FAIL ARITY` line.

**Named limits.** (1) `Q_WSQUOT` counts every three-cell quote row BEFORE source resolution, so an
unresolvable-source whitespace row is counted by the leg *and* fails FLOOR — the leg is stronger than a
located-only count, not weaker. (2) The leg shares its expression with the shape branch: it is a second
witness, not an independent detector, and its own verdict force is the arity tripwire. (3) The
decision-width print is observability; the WARRANT conjunct is unchanged. (4) The `witness()` rows cover
`locates`, `unentailed_terms`, `teaches_miss`, `dup_qid`, `q_shape_violation` and the WSQUOTE class — not
`used_by_tokens` or the decision-width rule.

**Sources.** `S001` (own-work chain row, re-opened this round) — the counter's leg vocabulary rule.

## C3 `C3-TALLY-R93` — freshness

**Before** (r92 counter, `corpus/evidence/round92/skill-tally-r92.py`): the historical (non-current) tally
multiset is the frozen literal `EXPECTED_OTHERS = {("161","0"):1, ("256","0"):1}` over the `## Gates` scope
only, and nothing outside that scope is read; changing the `215` tail tally or appending an undeclared tail
tally leaves `SKILL_TALLY_R92=PASS` (rc 0), and a tally planted *above* `## Gates` is invisible
(`corpus/evidence/round93/evidence-before/c3-prior-accepts.txt`).

**After** (`corpus/evidence/round93/skill-tally-r93.py`): `SKILL_TALLY_R93=PASS` (exit 0) with
`TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 OTHER_OCCURRENCES=2 CASE_RANGE_OK=2/2 MISLABELED=0
HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2 OTHERS_OK=1 TAIL_OK=1 LEGS=4/4`. Each historical tally is
*derived* from the committed receipt that grounds it — `161` from
`corpus/evidence/round25-final-measure.log` (`PASS (161 cases, 0 skipped)` at line 53), `256` from
`corpus/evidence/round34/audit-dispositions.md` (`PASS (256 cases, 0 skipped)` at line 5) — and must also be
present in the Gates scope, so deleting it fires `HIST_MISSING`; a missing or unstating receipt fires
`HIST_UNGROUNDED`. Tallies outside the scope are declared on both sides: `TAIL_DECLARED = {215:1, 283:1}`
after the section and `HEAD_DECLARED = {}` before it, so an undeclared tally on either side fires
`HIST_SCOPE_BLEED` (with `head`/`tail` named). The case-range leg requires the claimed range to be exactly
the family's index set for both families (endpoints, interior holes and `MISLABELED`), and the family
population is every `ok-case` line, not only the ones printing `exit=`.

**Counting command** (from the lane root):

```bash
python3 -B corpus/evidence/round93/skill-tally-r93.py --root . --selftest corpus/evidence/round93/controls/selftest-r93.txt
python3 -B corpus/evidence/round93/skill-tally-r93-controls.py --root . --work "$HYAKU_SCRATCH/chousa-r93/c3/controls"
```

**Predicate.** The counter prints `SKILL_TALLY_R93=PASS` with `LEGS=4/4 HIST_DERIVED=2/2 HIST_PRESENT=2/2
TAIL_OK=1` and exits 0; the controls print `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1
STALE_REFUSED_BOTH=1/1 HIST_REFUSED_BOTH=1/1 TAIL_REFUSED=2/2 TAIL_PRIOR_ACCEPTED=1/1
TAIL_ADDED_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1 HEAD_REFUSED=1/1 INTERIOR_REFUSED=1/1` and exit 0,
where the tail, head and interior-hole trees are refused by r93 and accepted by r92 on the same bytes.

**Kill rules.** K1 the predicate not met at the landing revision. K2 the positive tree refused, or the r92
counter refusing any of the four discriminating trees. K3 a historical, tail or head tally moves on the
clean tree. K4 the derivation is vacuous: the receipt is not opened, the located quote is not required in
it, the tally is not required to be present in scope, or the tail set is compared by count only rather than
by `(cases, skipped)` pairs.

**Named limits.** (1) The two grounding receipts are historical captures: a rewrite is caught by the quote
test, not by a digest, and the `256` quote is a round-34 disposition sentence naming the banner form rather
than a run capture. (2) No line binding: the quote must appear in the receipt, not at a named line, and a
symlink at the receipt path passes. (3) The declarations are measured sets, not derivations: a third
legitimate tally on either side must be declared in the same commit. (4) The scope boundary is any
column-0 `#`/`##` line (the r92 ATX form), not a full ATX parser.

**Sources.** `S001` (own-work chain row) — the selftest verdict line the tally legs read.

## Round shape

One v1 wave of 12 seats (8 attack: 3 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 revenger, plus
1 mutation seat counted as attack; 3 executors, 1 scout, 1 scribe-class connector) under
`ufo-wave-policy.json` band 8–16. The L1 holds the planner seat (the validator rejects `planner`); a bounded
planning data-walk rides the scout. Residual: none.

## Frontier step (§2b)

- `corpus/SOURCES.md`: no append, no cell change — no claim admits a new knowledge entry, and the two
  re-opened rows (`S070` installed `sha256sum(1)`, `S001` own-work chain row) keep their `status`,
  `recheck` and `used-by` cells. Census exit 0 before and after, registry 219 rows.
- Mistake mined into `corpus/lessons/round-93.md` `## Mistakes`: the fixture-path self-pin class
  (`captured-by`: QUALITY 202; fix: the `--root`/`--repo` derivation, shown able to fail by `DERIVE_OK`),
  plus the before-state-asserted-not-measured class from this round's own C2 first draft.
- Sourced claims: C1 rests on `S070` (opened this round), C2/C3 on `S001` (re-opened this round).
