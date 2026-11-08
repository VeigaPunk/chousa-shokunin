# R94ReviewerC1 — C1 `C1-DRIVER-R94` attack (operability)

Seat: `R94ReviewerC1` (leaf reviewer, no subagents).
Target: carrier **C** `352924bbea624caf3771ef291be98fd4ec679dda` (freeze **F** `41038ed7c40cffc4cf86d649a6ba433c4b9eec1a`), read
from a `git clone --shared` at `C` with a clean working tree (S221: the clone has no objects of its own; it
was never repacked). Canonical runtime: `python3 -B` for the drivers, `bash -c` for the instruments
(`run_instrument`, `control-driver-r94.py:498`).
Frozen texts attacked: `.ufo/waves/round-94/claims.md` C1 (lines 25–31 role sentences, 42–50 predicate) and
`.ufo/waves/round-94/claims.json` C1 `sentence`/`predicate` (lines 12–38).
Scratch: `/fast/scratch/hyaku/chousa-r94/R94ReviewerC1` (deleted before yield). No lane file was edited.

## Canonical runs

1. `python3 -B corpus/evidence/round94/control-driver-r94.py verify --root . --repo . --rev 41038ed7… --receipts-rev 352924bb… --work <scratch>/work/verify`
   → **exit 0**
   `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=34/34 RECEIPT_PINS=6/6 PIN_ROLES_OK=14/14 CONTROL_DRIVER_R94=PASS`
   and `RECEIPT SELF_PIN OK rev=41038ed7… receipts_rev=352924bb…`.
   `git status --porcelain` empty afterwards → no write under the receipts or claims directories (K3).
   Receipt: `R94ReviewerC1-verify-canonical.txt`.
2. `python3 -B corpus/evidence/round94/forgeries-r94.py --root . --repo . --rev 41038ed7… --receipts-rev 352924bb… --work <scratch>/work/forgeries`
   → **exit 1**, last line
   `FORGERIES=FAIL FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass`.
   Receipt: `R94ReviewerC1-forgeries-canonical.txt`.

**The verify half of the frozen predicate holds. The battery half does not: it exits 1.** This falsifies
claims.md:49 (`prints FORGERIES=PASS … (exit 0)`) and claims.json:37 (`"exit": 0`); kill rule K1 fires.

## Findings

### F1 — HIGH — the battery's `s1-schema-two-column` fixture is unsatisfiable, so `FORGERIES=PASS` is unreachable at C

`forgeries-r94.py:171`:

```python
case("s1-schema-two-column", None, 2, ["SETUP PIN_SCHEMA"])
```

With `rows_mutator=None` the fixture rows are the committed rows, and `write_r94()` rewrites them in the
three-column shape with a recomputed self row. That table is **byte-identical to the committed pins table**
(`COMMITTED_SHA == WRITTEN_SHA == 6b2c5579794e0dc797671b49ef43b84b3848b7be2acac763501c1ebad294f1c4`,
`S1_FIXTURE_TABLE_IDENTICAL_TO_COMMITTED True`, receipt `R94ReviewerC1-s1-fixture.txt`), and the canonical
verify on exactly those bytes is **rc 0 / PASS with no `SETUP PIN_SCHEMA`**. The case therefore requires the
driver to refuse its own valid table; it can never pass.

Observed (receipt `R94ReviewerC1-forgeries-canonical.txt`):

```
FAIL s1-schema-two-column: r93 rc=0 r94 rc=0 needles=SETUP PIN_SCHEMA
  r94: RECEIPT PINS OK 34/34 pinned files byte-identical RECEIPT_PINS_OK=6/6
...
FORGERIES=FAIL FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass
```

`results["s1-schema-two-column"]` is `False` → `ok = all(results.values())` (`forgeries-r94.py:215`) is
`False` → `FORGERIES=FAIL`, `return 1`.

Two aggravations, both material to the claim:

* `SCHEMA_REFUSED=1/1` is computed from `schema_ok` of the **`s0-schema-prior`** block (`forgeries-r94.py:176–177`),
  not from `s1`; the failing case contributes only to the `all()` and prints no ratio of its own. So every
  printed ratio is full while the battery's own verdict is FAIL — precisely the "moves the number rather than
  hiding" failure mode C1 claims to have removed.
* `s1` is also redundant with `s0-schema-prior`, which performs the two-column test correctly (`r93 rc=0 →
  r94 rc=2 PIN_SCHEMA`). Removing the `s1` line, or making it the two-column write, restores
  `FORGERIES=PASS`; the frozen claim as written is not met at C.

Independent corroboration (not relied on): seat `R94ExecC1Repro` recorded the same
`FAIL s1-schema-two-column: r93 rc=0 r94 rc=0` and `FORGERIES=FAIL` at `C`; the lane working tree currently
carries an uncommitted deletion of this very line (`git diff -- corpus/evidence/round94/forgeries-r94.py`),
which is a post-C working-tree state, not C.

### F2 — LOW — `role=expectation` has no `PIN_ROLE_MISSING`/`PIN_ROLE_DANGLING` code

claims.md:30–31 says "a dangling or missing member of a covered role is `PIN_ROLE_DANGLING` /
`PIN_ROLE_MISSING` (exit 1)". `covered` includes the expectation row (`control-driver-r94.py:299`), but the
expectation branch emits a different code (`control-driver-r94.py:311–314`):

```python
exp_rows = {rel for rel, r in roles.items() if r == "expectation"}
if exp_rows != {exp_rel}:
    codes.append("PIN_ROLE_MISMATCH role=expectation pins=...")
```

Observed (probe `m2-drop-expectation`, receipt `R94ReviewerC1-probe-role.txt`):
`PIN_ROLE_MISMATCH role=expectation pins=none expected=corpus/evidence/round94/controls/expected.tsv`, exit 1.
The *set relation* is correct in both directions (one set equality); only the promised code vocabulary is
wrong for one of the five roles. No escape: the verdict still fails.

### F3 — LOW — `PRIOR_ACCEPTED` is not an independent measurement

`forgeries-r94.py:210–214` computes both aggregates from the same `results` dict with the same tuple:

```python
role_forgeries = sum(1 for n in ("d1-dangling-instrument", "d2-missing-claims",
                                 "d3-mis-role-expectation", "d4-unknown-role") if results.get(n))
prior = sum(1 for n in ("d1-…", "d2-…", "d3-…", "d4-…") if results.get(n))
```

Evaluated over all 16 possible `results` assignments the two numbers differ **0** times
(`OVER_16_RESULT_SETS_DIFFER=0`, receipt `R94ReviewerC1-probe-ratio.txt`). Because `results[name]` already
ANDs the r94 refusal with the r93 acceptance (`case()` builds `new_ok and old_ok`), a fixture whose r93
projection refuses lowers `FORGERY_REFUSED` as well: the claim prints four refusals and four prior
acceptances from one measurement. The r93 side *is* measured (`old_ok = rc_old == 0`, and r93 returns 0 iff
`CONTROL_DRIVER_R93=PASS`), so no false statement about r93 is made — only the claimed independence of the
two ratios is not there.

### F4 — OBSERVATION — `PIN_ROLES_OK` is a label, not a gate

`PIN_ROLES_OK` **can** be driven to 13/14 and the verdict does change (probe `M14`: the expectation row's
path renamed to `plans/round-94.md` with a truthful digest and the self row recomputed —

```
COMMITTED_OK=6/6 … PINNED_FILES=34/34 RECEIPT_PINS=6/6 PIN_ROLES_OK=13/14 CONTROL_DRIVER_R94=FAIL
PIN_ROLE_FINDING PIN_ROLE_MISMATCH role=expectation pins=plans/round-94.md expected=corpus/evidence/round94/controls/expected.tsv
```

). But the deciding term is `role_codes`, not the ratio: a scratch copy of the driver with the ratio
conjunct deleted (`roles_ok = not role_codes and role_total > 0`) prints **the identical** verdict and the
identical `CONTROL_DRIVER_R94` line on both the clean tree (rc 0, PASS) and the 13/14 tree (rc 1, FAIL)
(receipt `R94ReviewerC1-probe-ratio.txt`; the unpatched control was run without `--repo` for both, so the
comparison is like-for-like). The conjunct is algebraically redundant: each branch adds exactly the members
it covers to `ok`, so `role_codes == []` implies `role_ok == role_total`. Conversely a deleted *required*
row can leave the ratio full — dropping the expectation row gives `PIN_ROLES_OK=13/13` while the verdict is
FAIL (probe `m2`). The claim's wording ("a deleted or invented row moves the number") is literally true of
`m` (14 → 13) but the ratio stays full; the protection is the code, which does fire.

This is not a kill-rule violation. K4's two listed degeneracies are absent: `covered` excludes `driver`
(line 299), and the role sets are read from the table (`role_instr` line 302, `role_claims` line 329), not
from constants other than the by-design literal claims pair.

## The six questions

**(1) Does `role_report` compare the executed set, or a set derived from the table? — HOLD (executed side is
independent).** `pin_report` builds `executed` from the *expectation rows* (`control-driver-r94.py:351–357`),
and `role_report` compares the pins-side `role_instr` (line 302) against it (lines 303–309). Empirically, if
the executed side were derived from the table the deleted-instrument probe would pass; instead
`m3-drop-instrument-row` prints `PIN_ROLE_MISSING role=instrument path=corpus/evidence/round89/gate-records-r89.py`
(rc 1) and `m4-instrument-to-driver` prints the same code. Caveat: `executed` is the *declared* instrument-token
set of `expected.tsv`, not an observation of opened files; for the committed rows the two coincide because the
same `rows` drive `run_instrument` (line 498).

**(2) Is `driver` a loophole for a deleted instrument? — HOLD (no).** `read_pins` keeps one role per path;
`covered` excludes `driver` (299); a `driver`-labelled file that the expected rows still execute fires
`PIN_ROLE_MISSING role=instrument` (`m4`), and a `driver` row naming a missing file fires `PIN_MISSING`
(`m12`, rc 1). To make a driver label swallow a real instrument you must also stop `expected.tsv` from
executing it, i.e. the coherent joint edit of expectation row + pin row + receipt — named limit 1 — and even
then `UNSCORED_RECEIPT` (line 572) and the expectation row mis-match move.

**(3) Is `PIN_ROLES_OK` load-bearing? — 13/14 is reachable and the verdict changes, but the ratio is not the
deciding term.** See F4: the patched-driver pair and the `m2` 13/13 case. A ratio of 13/14 with `role_codes`
empty is impossible, because `role_codes == []` implies `ok == covered`.

**(4) Does `make-pins-r94.py` reproduce the table byte-for-byte, and does the self row bind the non-self rows?
— HOLD.** `python3 -B corpus/evidence/round94/make-pins-r94.py --root .` prints
`PINS_WRITTEN=34 roles=instrument=5,expectation=1,receipt=6,claims=2,driver=19`, `git status --porcelain`
is empty afterwards, and HEAD blob and working file both hash
`6b2c5579794e0dc797671b49ef43b84b3848b7be2acac763501c1ebad294f1c4` (34 data rows, 14 non-driver rows; receipt
`R94ReviewerC1-makepins.txt`). The self row binds the body: flipping one hex char of a non-self row while
keeping the stored self digest fires `INSTRUMENT_PIN_MISMATCH:corpus/evidence/round94/instrument-pins.txt`
*in addition to* `PIN_DISK_MISMATCH path=…curation-r94.py` (`m9`); flipping only the self row fires the same
code alone (`m10`); deleting the self row fires `PIN_SELF_ROW_ABSENT` (`m11`).

**(5) Does `PRIOR_ACCEPTED` measure the projection honestly? — HOLD on the projection, F3 on the aggregate.**
The projection is the same path set with the same digests and only the minus-self row recomputed in the r93
shape (`forgeries-r94.py:63–70`), and r93 honours `--pins/--expected/--receipts`
(`control-driver-r93.py:404–406,414`), so r93 scores the intended population; observed `r93 rc=0` on all four
fixtures. The projection does not differ in a way that matters *for what it claims* (r93 has no role
concept); what is weak is that the printed `PRIOR_ACCEPTED` is the same expression as `FORGERY_REFUSED`.

**(6) Is "both directions" true for all four covered roles, including `claims`? — HOLD on membership, F2 on
the code names.** Quoted sentence, claims.md:26–31: "the role sets are checked in both directions:
`role=instrument` is exactly the instruments the expected rows execute, `role=expectation` is exactly the
expectations file, `role=receipt` is exactly the committed receipts, and both claims files carry
`role=claims`. … a dangling or missing member of a covered role is `PIN_ROLE_DANGLING` / `PIN_ROLE_MISSING`
(exit 1)." `claims` is compared as a set in both directions against the literal pair (lines 329–335): a
missing row fires `PIN_ROLE_MISSING role=claims` (`m1`, rc 1: `PIN_ROLES_OK=12/13`) and a third row fires
`PIN_ROLE_DANGLING role=claims path=plans/round-94.md` (`m7`, rc 1); instrument and receipt likewise fire
both codes (`m3`/`m4`, `m5`). The only false clause is the code vocabulary for `expectation` (F2).

## Residual risk and verification gaps

* **Battery identity is not self-verified.** `forgeries-r94.py:22–23` resolves `NEW`/`OLD` from its own
  directory (`HERE`) and never compares those bytes to the pins rows it is testing, and it runs the drivers
  without `--repo`, so `self_pin` is skipped. Run from a dirty lane it can score unpinned driver bytes. In
  this session the lane's working tree already differs from `C` for `forgeries-r94.py`
  (`68294471…` vs C's `f7dd794e…`) — I ran the `C` bytes from a clean clone. The table still pins the
  battery and both drivers as `driver` rows, and `verify --repo` catches the drift, so the pair of counting
  commands covers it; the battery alone does not.
* **Instrument-token visibility.** `instrument_rels` only sees absolute `.py`/`.sh` tokens after `@ROOT@`
  substitution; an expectation row executing an in-tree script through a relative or `bash -c` token is
  invisible to the role leg. A row with *no* absolute token fires `INSTRUMENT_UNPINNED:<case>`, but a row
  mixing one absolute and one relative instrument is half-seen. No committed row has that shape
  (`c1-harm`'s `.py`-suffixed tokens are the absolute `@ROOT@/corpus/evidence/round90/harm-recheck-r90.py`,
  plus the non-absolute `265b8633…:tools/gate-records.py` and `@WORK@/harm/base-tool.py` — only the first is
  counted, the other two are skipped because `@ROOT@` is the only placeholder `instrument_rels` substitutes);
  exploiting it needs a committed joint edit of the pinned `expected.tsv`, i.e. named limit 1.
* Not re-measured: the r93 before-state receipt (`evidence-before/c1-prior-accepts.txt`) — outside C1's
  frozen predicate; the coherent joint edit end-to-end (named limit 1, owned by another attack seat); the
  individual fresh-instrument exit codes beyond `FRESH_OK=6/6`; any C2/C3 surface (not this seat's axis).
* K3 (no writes): `git status --porcelain` empty after the canonical verify; the fresh legs write only under
  `--work`; the pins self row was byte-checked before and after.

## Receipts copied into this directory

`R94ReviewerC1-verify-canonical.txt`, `R94ReviewerC1-forgeries-canonical.txt`,
`R94ReviewerC1-probe-role.txt`, `R94ReviewerC1-makepins.txt`, `R94ReviewerC1-s1-fixture.txt`,
`R94ReviewerC1-probe-ratio.txt`.

VERDICT: R94ReviewerC1 C1 fired — the frozen C1 battery predicate is not met at carrier C: `forgeries-r94.py` exits 1 with `FORGERIES=FAIL` because `case("s1-schema-two-column", None, 2, …)` asserts `PIN_SCHEMA` on a table byte-identical to the valid committed one; the verify half passes in full.
