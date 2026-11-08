# Round 93 — frozen claims (chousa, L1 ChousaR93, 2026-11-08)

Base: lane branch tip `206226dc9d9baef620e7d3d30bdac5f9194a459f` (in sync with origin before the round).
Census at round start, exit 0 (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin chousa`): five pre-existing `W04` duplicate-url warnings, `chousa ok`,
registry 219 rows. Pinned in `corpus/evidence/round93/census-start.txt`.

Claims come from the scorecard's round-93 plan (`SCORECARD.md` lines 4134–4146) and from the r92
non-author spot-check's three routed residuals (`corpus/lessons/round-92-verifier-spotcheck.md`
"Routed defects for next round"). Three claims, three axes, no exploratory claim. Freeze commit `F`
carries the instruments; carrier `C` carries the receipts and the completed pins table.

## C1 `C1-DRIVER-R93` — operability (lowest scored non-retired axis; historical 3/10 held)

**Before** (r92 driver, `corpus/evidence/round92/control-driver-r92.py`, on the round-93 fixture set):
`RECEIPT PINS OK 7/16 pinned files byte-identical`, `PINNED_FILES=7` — nine pinned instruments are
never compared on disk and the committed receipts are read but pinned nowhere. Measured in
`corpus/evidence/round93/evidence-before/c1-prior-accepts.txt`: a tampered copy of an unexecuted pinned
instrument and a tampered committed receipt each verify `CONTROL_DRIVER_R92=PASS` (rc 0).

**After** (`corpus/evidence/round93/control-driver-r93.py`):
`CONTROL_DRIVER_R93=PASS` (exit 0) with `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6
PINNED_FILES=22/22 RECEIPT_PINS=6/6` and `RECEIPT SELF_PIN OK rev=<F> receipts_rev=<C>`, where PASS
requires `findings==0` AND every row committed/exact/pin/fresh AND `checked==len(pins)` AND
`rchecked==rtotal>0`. The pins table is the population: every one of its rows is byte-checked on disk
(`PIN_DISK_MISMATCH path=<rel>` per row, `PIN_MISSING path=<rel>` for an absent file), the sixteen
r92-set rows plus one row per committed receipt (six). `--expected`, `--receipts` and `--pins` default
under `<root>/corpus/evidence/round93/`, so the driver's own directory never decides a scored fixture
(the r92 driver-directory defaults are gone); instrument rows are pinned at `--rev`, receipt rows and
the pins table at `--receipts-rev`.

**Counting command** (from the lane root):

```bash
python3 -B corpus/evidence/round93/control-driver-r93.py verify --root . --repo . \
  --rev <F> --receipts-rev <C> --work "$HYAKU_SCRATCH/chousa-r93/c1/verify"
python3 -B corpus/evidence/round93/forgeries-r93.py --root . --repo . --rev <F> --receipts-rev <C> \
  --work "$HYAKU_SCRATCH/chousa-r93/c1/forgeries"
```

**Predicate.** The verify command prints `CONTROL_DRIVER_R93=PASS` with those five fields and exits 0;
the battery prints `FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 POSITIVE=pass` and exits 0,
where the two refusals are `PIN_DISK_MISMATCH` on an unexecuted pinned instrument and `RECEIPT_MISMATCH`
on a receipt body, each accepted (rc 0) by the r92 driver on the same bytes, and `DERIVE_OK` is the
r92 driver refusing the derived-default form (`SETUP` on a copy tree) that the r93 driver scores
normally.

**Kill rules.** K1 the predicate not met at the landing revision. K2 a battery forgery accepted by the
r93 driver, the positive refused, or the r92 driver refusing both forgeries (no discrimination).
K3 a genuine row moved by the pin walk (a clean tree must still PASS) or the verify path writing under
the receipts directory. K4 the PASS skips the work: a pin row equal to itself by construction (the
pins file's own row is the minus-self digest, never a whole-file sha), a receipt counted without its
pin row, or `--root` ignored in favour of the driver's directory.

**Named limits.** (1) A coherent joint edit of an instrument, its pin row, its receipt and its
expectation row survives — that edit is the harness. (2) The minus-self digest binds the table's
coherence, not its authority: the self row itself cannot be protected. (3) Pinned bytes are compared
at `F`/`C`; an instrument that reads data outside its own bytes is unseen. (4) The receipt set is
pinned as one row per file; a receipt added after `C` is `RECEIPT_UNPINNED`, but a *removed* receipt
row simply stops being scored if the expected row also goes.

**Sources.** `S070` (the installed `sha256sum(1)` page: the digest text and `--check` input this pin
discipline rests on).

## C2 `C2-CURATION-R93` — calibration

**Before** (r92 counter, `corpus/evidence/round92/curation-r92.py`, on the round-93 tree):
`CURATION_R92=PASS` with `LEGS_MEASURED=14/14` and `Q_SHAPE_FAIL=0`; on the whitespace-quote tree — one
Located-quotes row whose quote cell is `" "` — r92 reports `Q_SHAPE_FAIL=0` and refuses the tree only
downstream (`LEG_FAIL FLOOR`, `LEG_FAIL WARRANT`, `LEG_FAIL TFREQ`), so the cause is never named
(`corpus/evidence/round93/evidence-before/c2-prior-accepts.txt`): the shape test strips whitespace
before stripping quotes, so the inner space survives its cell.

**After** (`corpus/evidence/round93/curation-r93.py`): `CURATION_R93=PASS` (exit 0) with
`LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_ROWS=20 Q_FLOORS=<per-entry> WARRANT_OK=17/17
TFREQ_OK=17/17 DUP_QIDS=0 SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20`
and `VERDICT fields_hold=1 legs_ok=15/15 DETECTOR_WITNESS=11/11`. The fifteenth leg is `WSQUOTE`: a
located quote that normalises to the empty string is counted from the located-quote population and
refused, independently of the cell parser, while `q_shape_violation` refuses the same row with
`quote=<whitespace>`; a wrong-width decision row additionally prints one
`DECISION_WIDTH <entry> row=<line> cells=<n>` line (it was already a WARRANT conjunct, now legible
per row). `EXPECTED_LEGS` moves 14 → 15, so deleting the new leg breaks the verdict.

**Counting command** (from the lane root):

```bash
python3 -B corpus/evidence/round93/curation-r93.py --root .
python3 -B corpus/evidence/round93/curation-controls-r93.py --root . --work "$HYAKU_SCRATCH/chousa-r93/c2/controls"
```

**Predicate.** The counter prints `CURATION_R93=PASS` with `LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0
Q_WSQUOT=0` and exits 0; the controls print `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2
WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7` and exit 0, where `WS_NAMED` are the two
whitespace trees (space and tab inside the quotes) that r93 refuses at the shape leg as
`quote=<whitespace>` with `Q_WSQUOT=1` while r92 reports `Q_SHAPE_FAIL=0` on the same bytes, and
`CARRIED_REFUSED_BOTH` are the four round-92 classes still refused by both counters (this is
classification, not a refusal r92 lacks: r92 fails those trees downstream).

**Kill rules.** K1 predicate not met at the landing revision. K2 a whitespace tree whose shape leg
stays green under r93, the positive refused, or an r93 field absent from the printed verdict. K3 a
genuine entry moved: all 20 located quotes, the 17 warranted decision rows and the two quote floors
must hold at the landing revision. K4 the new leg is vacuous: `Q_WSQUOT` counts only rows the shape
test already dropped (it must count the row on the forged tree and stay 0 on the clean one), or the
leg can be deleted without a verdict change (`EXPECTED_LEGS`).

**Named limits.** (1) `Q_WSQUOT` reads the located-quote population, so a whitespace quote whose
source does not resolve is reported by FLOOR instead. (2) The decision-width print is observability,
not a new gate; the WARRANT conjunct is unchanged. (3) The eight legs are still the r92 vocabulary;
no decision-row *count* change is added beyond `DECISION_COUNTS`.

**Sources.** `S001` re-open (own-work chain row, tier A) — the counter's leg vocabulary rule.

## C3 `C3-TALLY-R93` — freshness

**Before** (r92 counter, `corpus/evidence/round92/skill-tally-r92.py`, on the round-93 tree): the
historical (non-current) tally multiset is the frozen literal
`EXPECTED_OTHERS = {("161","0"):1, ("256","0"):1}` over the `## Gates` scope only; the two tail
tallies outside that scope (`215` in the Round27 subsection, `283` at the host line) are invisible, so
deleting the `215` tail line leaves `SKILL_TALLY_R92=PASS` (rc 0) — measured in
`corpus/evidence/round93/evidence-before/c3-prior-accepts.txt`.

**After** (`corpus/evidence/round93/skill-tally-r93.py`): `SKILL_TALLY_R93=PASS` (exit 0) with
`TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 OTHER_OCCURRENCES=2 CASE_RANGE_OK=2/2
MISLABELED=0 HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2 OTHERS_OK=1 TAIL_OK=1 LEGS=4/4`.
Each historical tally is *derived* from the committed receipt that grounds it — `161` from
`corpus/evidence/round25-final-measure.log` (`PASS (161 cases, 0 skipped)` at line 53), `256` from
`corpus/evidence/round34/audit-dispositions.md` (`PASS (256 cases, 0 skipped)` at line 5) — and must
also be *present* in the Gates scope, so deleting it fires `HIST_MISSING`; a missing or unstating
receipt fires `HIST_UNGROUNDED`. Tally occurrences outside the Gates scope are enumerated against a
declared tail set (`TAIL_DECLARED = {215:1, 283:1}`), and an undeclared tail tally fires
`HIST_SCOPE_BLEED line=<cases>` — the r82 clip/215 tail can no longer drift out of view. Four legs
(TALLY, CASE-RANGE, OTHERS, TAIL) replace r92's three.

**Counting command** (from the lane root):

```bash
python3 -B corpus/evidence/round93/skill-tally-r93.py --root . --selftest corpus/evidence/round93/controls/selftest-r93.txt
python3 -B corpus/evidence/round93/skill-tally-r93-controls.py --root . --work "$HYAKU_SCRATCH/chousa-r93/c3/controls"
```

**Predicate.** The counter prints `SKILL_TALLY_R93=PASS` with `LEGS=4/4 HIST_DERIVED=2/2
HIST_PRESENT=2/2 TAIL_OK=1` and exits 0; the controls print `CONTROLS=PASS OLDPROSE_REFUSED=1/1
PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1 HIST_REFUSED_BOTH=1/1 TAIL_REFUSED=2/2
TAIL_PRIOR_ACCEPTED=1/1 TAIL_ADDED_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1` and exit 0, where the two
tail trees (the `215` tally changed, and an undeclared tally appended below the scope) are refused by
r93 and accepted by r92, and an ungrounded receipt is refused with `HIST_DERIVED=1/2`.

**Kill rules.** K1 predicate not met at the landing revision. K2 the positive tree refused, or the
r92 counter refusing the tail-deleted tree (no discrimination). K3 a historical tally or a tail tally
moves on the clean tree (all four tallies must hold). K4 the derivation is vacuous: the receipt is
not opened, the located quote is not required to appear in it, the tally is not required to be
present in scope, or the tail set is compared by count only rather than by `(cases, skipped)` pairs.

**Named limits.** (1) The two receipts are historical captures; a rewritten receipt is caught by the
quote test, not by a digest. (2) The tail set is a declared measurement, not a derivation: a third
legitimate tail tally must be declared in the same commit. (3) The `## Gates` scope is the r92 ATX
boundary (depth ≤ 2 at column 0) and a `SCOPE_BLEED` setup diagnostic still terminates an unterminated
scope.

**Sources.** `S001` (own-work chain row) — the selftest verdict line the tally legs read.

## Round shape

One v1 wave of 12 seats (8 attack: 3 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 revenger,
1 labrun) under `ufo-wave-policy.json` band 8–16; one connector seat, three executors, one scout, one
scribe. The L1 holds the planner seat (validator rejects `planner`); a bounded planning data-walk
rides the scout. Residual: none.

## Frontier step (§2b)

- `corpus/SOURCES.md`: no append — no claim admits a new knowledge entry. Two rows re-opened:
  `S070` (installed `sha256sum(1)`, sha256 `93c17dff…` unchanged, line 11 quote re-read) and `S001`
  (the own-work chain row; its `recheck` cell moves round 92 → round 93, logged old→new in the
  round-93 lesson). Census exit 0 before and after.
- Mistake mined into `corpus/lessons/round-93.md` `## Mistakes`: the fixture-path self-pin class
  (`captured-by`: QUALITY 202; fix: the `--root` derivation, shown able to fail by `DERIVE_OK`).
- Sourced claim: C1 rests on `S070` (opened this round), C2/C3 on `S001` (re-opened this round).
