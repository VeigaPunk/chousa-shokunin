# Round 94 — frozen claims (chousa, L1 ChousaR94, 2026-11-08)

Base: lane branch tip `0f3f84dab3a094ec0a2fe8ae9ae59d3326e1a9b6` (round-93 landing + its non-author
spot-check, admitted). Census at round start, exit 0
(`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`):
five pre-existing `W04` duplicate-url warnings, `chousa ok`, registry 219 rows. Pinned in
`corpus/evidence/round94/census-start.txt`.

Claims come from the scorecard's round-94 plan (`SCORECARD.md` "Planned — round 94") and the round-93
non-author spot-check's routed defects D1–D6 (`corpus/lessons/round-93-verifier-spotcheck.md`). Three
claims, three axes, no exploratory claim. Three axes at once, each causally separable: none of the three
instruments imports another.

## C1 `C1-DRIVER-R94` — operability (lowest scored non-retired axis; historical 3/10)

**Before** (r93 driver, `corpus/evidence/round93/control-driver-r93.py`): the pins table is a flat list of
`<sha256>  <path>` rows with no role. Measured at the r93 freeze `3789608d` on a clone of this base
(`corpus/evidence/round94/evidence-before/c1-prior-accepts.txt`):

- the landed 23-row table scores `CONTROL_DRIVER_R93=PASS` — but 18 of its rows carry no role, so a row for
  a file nothing executes (`curation-controls-r93.py`) is indistinguishable from an instrument row;
- with the two round-93 claims rows **removed** the same driver prints `PINNED_FILES=21/21` and still
  `CONTROL_DRIVER_R93=PASS`: nothing requires the round's claims to be pinned at all.

**After** (`corpus/evidence/round94/control-driver-r94.py`): every row is `<sha256>  <role>  <path>` with
`role ∈ {instrument, expectation, receipt, claims, driver}`, and the role sets are checked in both
directions: `role=instrument` is exactly the instruments the expected rows execute, `role=expectation` is
exactly the expectations file, `role=receipt` is exactly the committed receipts, and both claims files carry
`role=claims`. A two-column row is `SETUP PIN_SCHEMA` (exit 2), an unknown role `SETUP PIN_ROLE_UNKNOWN`
(exit 2), and a dangling or missing member of a covered role is `PIN_ROLE_DANGLING` / `PIN_ROLE_MISSING`
(exit 1). `driver` rows are byte-checked but carry no coverage invariant (named limit 2).

**Counting command** (from the lane root, `<F>` the freeze and `<C>` the carrier the receipts pin):

```bash
python3 -B corpus/evidence/round94/control-driver-r94.py verify --root . --repo . \
  --rev <F> --receipts-rev <C> --work "$HYAKU_SCRATCH/chousa-r94/c1/verify"
python3 -B corpus/evidence/round94/forgeries-r94.py --root . --repo . --rev <F> --receipts-rev <C> \
  --work "$HYAKU_SCRATCH/chousa-r94/c1/forgeries"
```

**Predicate.** The verify command prints `CONTROL_DRIVER_R94=PASS` (exit 0) with
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 RECEIPT_PINS=6/6`, `PINNED_FILES=n/n` and
`PIN_ROLES_OK=m/m` where `n` is the data-row count of the committed pins table
(`grep -cE '^[0-9a-f]{64}' corpus/evidence/round94/instrument-pins.txt`) and `m` its non-`driver` row count
— both printed as full ratios, so a deleted or invented row moves the number rather than hiding; plus
`RECEIPT SELF_PIN OK rev=<F> receipts_rev=<C>`. PASS requires `findings==0`, every row
committed/exact/pin/fresh, `checked==len(pins)`, `rchecked==rtotal>0`, and `role_codes` empty. The battery
prints `FORGERIES=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1
SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass` (exit 0), where the four refusals are the
dangling-instrument, missing-claims, mis-role-expectation and unknown-role fixtures, each scored PASS by the
r93 driver on the two-column projection of the same rows, and the do-nothing form is the whole table written
in the r93 two-column shape (`SCHEMA_PRIOR_ACCEPTED`, r93 rc 0 → r94 `PIN_SCHEMA` rc 2).

**Kill rules.** K1 the predicate not met at the landing revision. K2 a role forgery accepted by r94, the
positive refused, or the r93 projection refusing any of the four fixtures for a reason other than the role.
K3 a genuine row moves under the pin walk, or `verify` writes under the receipts or claims directories.
K4 the PASS skips the work: a role leg that reads a constant instead of the table, `driver` rows counted as
covered members, or the role check passing when the executed set is empty.

**Named limits.** (1) A coherent joint edit of an instrument, its pin row, its receipt and its expectation
row survives; that edit is the harness. (2) `driver` rows (the driver, the batteries, the leg table, the
selftest capture) are byte-checked but not coverage-checked: the harness is not a case instrument, so a
deleted driver row is `PIN_MISSING`-class only. (3) Roles are a claim about the table's own membership, not
about what a file does: a script that reads another file is invisible to the role leg. (4) The role names
are a closed enum in this file; a new kind of pinned artefact needs a code change in the same commit.

**Sources.** `S070` (installed `sha256sum(1)`, re-opened: the digest text the pin discipline rests on);
`S221` (installed `git-clone(1)`, opened this round: a `--shared` clone "starts out without any object of
its own", which is why every battery fixture is a shared clone and never a citable archive).

## C2 `C2-CURATION-R94` — calibration

**Before** (r93 counter, `corpus/evidence/round93/curation-r93.py`): on a tree whose Q2 quote cell is `"—"`,
r93 prints `Q_SHAPE_FAIL=0`, has no `Q_PUNCTQUOT` field, and refuses the tree only downstream
(`LEG_FAIL FLOOR`, `LEG_FAIL WARRANT`) — the punctuation-only class has no name
(`corpus/evidence/round94/evidence-before/c2-prior-accepts.txt`). Its `locates()` compares the quote as a
substring, so `"—"` "locates" any capture that contains an em dash.

**After** (`corpus/evidence/round94/curation-r94.py`): `q_shape_violation` refuses a quote cell with no
alphanumeric character as `quote=<punctuation>`; the class is counted on every three-cell quote row before
the shape filter (`Q_PUNCTQUOT`; pre-qid, pre-source, pre-location, and Unicode-aware via
`str.isalnum`, so a CJK quote is not the class); `locates()` returns False for a punctuation-only quote; and leg 16
(`PUNCTQUOT`) makes deleting the class change the verdict through the `EXPECTED_LEGS` arity tripwire
(15 → 16). `witness()` grows to 18 rows with both directions of the class, the CJK silence direction, and
`locates("—", "before — after") is False`.

**Counting command** (from the lane root):

```bash
python3 -B corpus/evidence/round94/curation-r94.py --root .
python3 -B corpus/evidence/round94/curation-controls-r94.py --root . --work "$HYAKU_SCRATCH/chousa-r94/c2/controls"
```

**Predicate.** The counter prints `CURATION_R94=PASS` (exit 0) with `LEGS_MEASURED=16/16 Q_SHAPE_FAIL=0
Q_WSQUOT=0 Q_PUNCTQUOT=0 Q_ROWS=20 WARRANT_OK=17/17 TFREQ_OK=17/17 DUP_QIDS=0` and
`VERDICT fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=18/18`. The controls print `CONTROLS=PASS
CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 CJK_SILENT=1/1
PRIOR_REGRESSION=7/7`
(exit 0), where `PUNCT_NAMED` are the dash and dots trees: r94 refuses each at the shape leg with
`quote=<punctuation>`, `Q_PUNCTQUOT=1` and `LEG_FAIL PUNCTQUOT`, while r93 reports `Q_SHAPE_FAIL=0` on the
same bytes (`PUNCT_SHAPE_GREEN_R93`, re-derived every run), and `CJK_SILENT` shows a CJK quote is refused
downstream as a short quote, never as the punctuation class. This is a classification claim: r93 fails those
trees too, but it cannot name the cause.

**Kill rules.** K1 the predicate not met at the landing revision. K2 a punctuation tree whose shape leg stays
green under r94, the positive refused, or `DETECTOR_WITNESS` not full. K3 a genuine entry moves (all 20
located quotes, the 17 warranted decision rows and the two quote floors must hold). K4 the new leg is
vacuous: it must count the row on both forged trees and stay 0 on the clean tree, and deleting it must
change the verdict through the named `LEG_FAIL ARITY` line.

**Named limits.** (1) `Q_PUNCTQUOT` counts every three-cell quote row before qid/source/location resolution,
so an unresolvable-source punctuation row is counted and also fails FLOOR — the count is the class
population, not the located population (Amendment 2, R94ReviewerC2 F1). (2) The leg shares its expression with
the shape branch (`punct_quote_cell`): a second witness, not an independent detector; its own verdict force
is the arity tripwire. (3) `locates()`'s guard is defense in depth: on the two routed entries the shape leg
refuses the class first, so the guard's force is only measured by `witness()` (Amendment 2, R94ReviewerC2 F4).
(4) A digits-only quote passes the shape leg (digits are alphanumeric) and is refused downstream as short;
the class is exactly "no alphanumeric character" (R94ExecC2Repro measured this). (5) The decision-width print
is observability; the WARRANT conjunct is unchanged.

**Sources.** `S001` (own-work chain row, re-opened: the leg vocabulary and its arity rule).

## C3 `C3-TALLY-R94` — freshness

**Before** (r93 counter, `corpus/evidence/round93/skill-tally-r93.py`): the tail set is the frozen multiset
`TAIL_DECLARED = {("215","0"):1, ("283","0"):1}` over everything after `## Gates`. Moving the `215` tally out
of its Round27 section into the Round 36 section — same count, same file, same bytes — leaves
`TAIL_OK=1` and `SKILL_TALLY_R93=PASS` (`corpus/evidence/round94/evidence-before/c3-prior-accepts.txt`).

**After** (`corpus/evidence/round94/skill-tally-r94.py`): each tail tally is declared with the substring of
the heading that owns it (`TAIL_OWNED`), the nearest preceding ATX heading of every occurrence is recorded,
and a moved tally fires `TAIL_OWNER_MISMATCH` (a duplicated or deleted one `TAIL_OWNER_COUNT`, a declared
tally with no owner entry `TAIL_OWNER_UNMAPPED`), so `TAIL_OK` now requires both the multiset and the owners.
`TAIL_OWNED_OK` is printed observability over the same codes; the verdict force is `owner_codes → TAIL_OK`
(Amendment 3, R94ReviewerC3 F4).

**Counting command** (from the lane root):

```bash
python3 -B corpus/evidence/round94/skill-tally-r94.py --root . --selftest corpus/evidence/round94/controls/selftest-r94.txt
python3 -B corpus/evidence/round94/skill-tally-r94-controls.py --root . --work "$HYAKU_SCRATCH/chousa-r94/c3/controls"
```

**Predicate.** The counter prints `SKILL_TALLY_R94=PASS` (exit 0) with `LEGS=4/4 TAIL_OK=1 TAIL_OWNED_OK=2/2
TAIL_TALLIES=2 TALLY_ROWS=8 STALE_TALLIES=0/8 HIST_DERIVED=2/2 HIST_PRESENT=2/2 CASE_RANGE_OK=2/2
MISLABELED=0`. The controls print `CONTROLS=PASS CARRIED_REFUSED=6/6 MOVED_REFUSED=2/2
MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1` (exit 0): the two moved trees are
refused by r94 and accepted by r93 on the same bytes, `double-tail-215` fires `TAIL_OWNER_COUNT`, and the
`heading-alias` fixture (it RENAMES the owner heading, it does not move the tally) measures named limit 1.

**Kill rules.** K1 the predicate not met at the landing revision. K2 the positive tree refused, or r93
refusing either moved tree (that would make the discrimination vacuous). K3 a historical, tail or head tally
moves on the clean tree. K4 the derivation is vacuous: a declared owner never read, `TAIL_OWNED_OK` computed
from the declarations instead of the observed headings, or the tail compared by count only.

**Named limits.** (1) The owner declaration binds a heading *substring*: a heading that contains the
declared string satisfies it (`HEADING_ALIAS_ACCEPTED` measures this, it is not hidden). (2) The nearest
preceding heading is a column-0 line matching `^#{1,6} ` (ATX with a space), not a full ATX parse of setext,
indented or space-less `##X` headings (R94ReviewerC3 F2: the wording, not the code, was wider).
(3) A tally inside a fenced code block that follows a heading is attributed to that heading. (4) The
declarations are measured pairs, not derivations: a third legitimate tail tally must be declared in the same
commit.

**Sources.** `S001` (own-work chain row, re-opened: the selftest verdict line the tally legs read).

## Round shape

One v1 wave of 12 seats under `ufo-wave-policy.json` (band 8–16): 3 executors, 3 reviewers, 1 critic, 1
mutation-tester, 1 sentinel, 1 revenger, 1 connector, 1 scout. Attack seats = 3 reviewers + critic +
mutation-tester + sentinel + revenger = 7/12 (58 %, floor 25 %). One connector (the few-connector rule).
The L1 holds the canonical planner seat (the validator rejects `planner`); a bounded planning data-walk
rides the scout. Residual: none.

## Frontier step (§2b)

- `corpus/SOURCES.md`: one new row `S221` (installed `git-clone(1)`, tier A, opened this round, quote and
  location in `corpus/lessons/round-94.md` `## Gate`); `S001` and `S070` re-opened, their cells unchanged.
  Census exit 0 before and after.
- Mistake mined into `corpus/lessons/round-94.md` `## Mistakes` (the round's own C1 first draft measured the
  role defect on a table the prior driver refuses for a schema reason — a before-state that cannot be
  compared, caught by the battery's projection form).
- Sourced claims: C1 cites `S070` + `S221`, C2 and C3 cite `S001`.
