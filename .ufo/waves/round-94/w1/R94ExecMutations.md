# R94ExecMutations — mutation battery on the three r94 instruments

Seat: mutation-tester (leaf). Lane `chousa-shokunin`. Anchors given to this seat: base
`0f3f84dab3a094ec0a2fe8ae9ae59d3326e1a9b6`, claim freeze `F=41038ed7c40cffc4cf86d649a6ba433c4b9eec1a`,
attacked carrier `C=352924bbea624caf3771ef291be98fd4ec679dda`, predicate set
`.ufo/waves/round-94/claims.md` (read before the battery). No network. The lane was never edited; every
mutant is a copy under `/fast/scratch/hyaku/chousa-r94/R94ExecMutations/` (deleted before yield; the
compact receipts are copied under `.ufo/waves/round-94/w1/R94ExecMutations/`).

## Method

* Shared clone at the carrier (S221: a `--shared` clone starts without objects of its own; never repacked):
  `git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo && git -C $S/repo checkout C`.
  Asserted `git -C $S/repo rev-parse --show-toplevel` = `$S/repo`; `$S/repo` was read-only for the whole
  battery (before/after hashes below).
* Twelve one-point mutants under `$S/mut/M<n>/`, each a copy of a `round93+round94` mirror of C with one
  instrument replaced; every anchor was asserted to occur exactly once and every mutant byte-compiles.
  Mutant hashes: `R94ExecMutations/R94ExecMutations-hashes.txt`.
* **C1 `--repo` note (measured, not assumed).** The driver's own self-pin binds its bytes to `--rev` and
  refuses a driver outside `--repo` (`rel_for`). An identity copy of the driver (M0) with the landing
  command and `--repo .` exits 1 with `SETUP path escapes base: .../mut/M0/control-driver-r94.py vs .`
  (`R94ExecMutations/c1-m0-repo-refusal.log`); with the same command **without** `--repo` M0 prints the
  landing line, `PIN_ROLES_OK=14/14 ... CONTROL_DRIVER_R94=PASS` rc 0
  (`R94ExecMutations/c1-m0-norepo.log`). With `--repo` every byte-changing mutant (including the
  pure-rename control) is killed identically by the self-pin, i.e. a blanket refusal, not a detector.
  The C1 logic mutants below therefore run the landing command **minus `--repo`** (this is also how the
  claim's own `forgeries-r94.py` invokes the driver), and the role discrimination is measured twice:
  the claim's forgeries battery with the mutant driver, and four targeted pins-table fixtures in a
  second shared clone (`$S/fixtree` at C) run against the pristine and the mutant driver.
* C2/C3 instruments have no self-pin. C2 controls resolve `round93`/`round90` siblings from their own
  directory, so each C2 mutant was placed in a full shared clone of C and the controls run in-tree
  (a `round93+round94` mirror is **not** faithful for the round-90 regression component: the pristine
  mirror run prints `CONTROLS=FAIL ... PRIOR_REGRESSION=FAIL` while the in-tree pristine run prints
  `CONTROLS=PASS ... PRIOR_REGRESSION=7/7`; the mirror's regression failure is a harness-layout artefact,
  not a claim finding). C3 controls were run from the mirror, whose pristine run prints
  `CONTROLS=PASS ... MOVED_REFUSED=2/2` (`R94ExecMutations/c3ctl-base-mirror.log`).
* Pristine baselines, all reproduced at C: C1 verify PASS + `RECEIPT SELF_PIN OK rev=F receipts_rev=C`
  (`c1-base-restored.log`); C2 `CURATION_R94=PASS ... LEGS_MEASURED=16/16` (`c2-base.log`, and in-tree
  controls `CONTROLS=PASS ... PRIOR_REGRESSION=7/7` in `c2ctl-base-intree.log`); C3
  `SKILL_TALLY_R94=PASS ... LEGS=4/4` (`c3-base.log`).
* Restoration: `$S/repo` was never written. sha256 after the battery equals the before record
  (`control-driver-r94.py=5ee9c1f9…`, `curation-r94.py=4b9ce115…`, `skill-tally-r94.py=da49d068…`,
  `instrument-pins.txt=6b2c5579…`) and `git -C $S/repo status --porcelain` is empty. All mutant bytes
  live only under `$S/mut/` and the whole scratch tree is removed before yield.

## C1 — `control-driver-r94.py` (four mutants)

Commands are from `$S/repo` (clone at C); `F`/`C` as above; `$D` = the mutant driver copy.
Base logic command (all M1–M4):

```
python3 -B $D verify --root . --rev $F --receipts-rev $C --work $S/w/verify-M<n>
```

| Mutant | Change (one semantic point) | Verdict line | rc | Verdict |
|---|---|---|---|---|
| M1 | instrument comparison one-directional: the `PIN_ROLE_DANGLING` loop deleted and `role_instr == executed` relaxed to `executed <= role_instr` (two text points, one comparison) | clean: `... PIN_ROLES_OK=14/14 CONTROL_DRIVER_R94=PASS`; D1 fixture: `... PIN_ROLES_OK=15/15 CONTROL_DRIVER_R94=PASS` (pristine D1: `PIN_ROLE_FINDING PIN_ROLE_DANGLING role=instrument path=corpus/evidence/round94/control-driver-r94.py`, `PIN_ROLES_OK=9/15`, rc 1) | 0 / 0 | **KILLED** — the D1 forgery is accepted |
| M2 | `CLAIM_PATHS` shrinks to the `.json` path | clean: `PIN_ROLE_FINDING PIN_ROLE_DANGLING role=claims path=.ufo/waves/round-94/claims.md`, `PIN_ROLES_OK=12/14 CONTROL_DRIVER_R94=FAIL`; D2md fixture (only `claims.md` row deleted): `... PIN_ROLES_OK=13/13 CONTROL_DRIVER_R94=PASS` (pristine: `PIN_ROLE_MISSING role=claims path=…claims.md`, 12/13, rc 1) | 1 / 0 | **KILLED** — predicate fails on the landing table and the missing-claims forgery is accepted |
| M3 | `PIN_ROLE_UNKNOWN` is a warning (`continue`) instead of `raise SystemExit(2)` | clean: PASS 14/14 rc 0 (identical); D4 fixture: rc 1, `SETUP PIN_ROLE_UNKNOWN role=witness path=corpus/evidence/round89/curation-r89-controls.py` printed twice, row skipped → `PIN_ROLE_MISSING role=instrument…`, `PIN_ROLES_OK=9/13` (pristine D4: rc 2, one `SETUP PIN_ROLE_UNKNOWN`) | 0 / 1 | **KILLED** — schema exit contract 2 → 1 |
| M4 | `covered` includes `driver` rows and `ok` adds `len(driver rows)` (driver rows count as covered) | clean: `... PINNED_FILES=34/34 ... PIN_ROLES_OK=34/34 CONTROL_DRIVER_R94=PASS`; frozen predicate fixes `PIN_ROLES_OK=m/m` with m = non-driver rows = 14; deleted-driver-row fixture: PASS 33/33 (pristine also PASS 14/14 — named limit 2) | 0 / 0 | **KILLED** — predicate deviation, not an acceptance difference (see finding F3) |

Fixture commands (targeted, `$S/fixtree` at C, no `--repo`):

```
python3 -B $D verify --root $S/fixtree --pins $S/fixtree/corpus/evidence/round94/pins-<d1|d2md|d4|dropdrv>.txt \
  --rev $F --receipts-rev $C --work $S/w/fx-<tag>
```

The four fixture tables differ from C's table by exactly one row edit plus the recomputed minus-self
row (same construction as `forgeries-r94.py`'s `write_r94`): D1 = the driver row re-labelled
`instrument`; D2md = only the `claims.md` row removed; D4 = the first row's role set to `witness`;
dropdrv = the driver row removed. Receipts: `fx-d1-*.log`, `fx-d2md-*.log`, `fx-d4-*.log`,
`fx-dropdrv-*.log`.

The claim's own role battery, run with the mutant driver (its `NEW` resolves next to the script):

```
python3 -B $S/mut/M<n>/corpus/evidence/round94/forgeries-r94.py --root . --repo . --rev $F \
  --receipts-rev $C --work $S/w/fg-M<n>
```

* M1: `FORGERIES=FAIL FORGERY_REFUSED=3/4 PRIOR_ACCEPTED=3/4 SCHEMA_REFUSED=1/1
  SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass`, rc 1 — `FAIL d1-dangling-instrument:
  r93 rc=0 r94 rc=0 needles=PIN_ROLE_DANGLING role=instrument` (`R94ExecMutations/fg-M1.log`).
* M3: same aggregate, rc 1 — `FAIL d4-unknown-role: r93 rc=0 r94 rc=1 needles=SETUP PIN_ROLE_UNKNOWN`
  (`R94ExecMutations/fg-M3.log`).
* Pristine baseline of the same battery at C: `FORGERIES=FAIL FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4
  SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass`, rc 1, because of
  `FAIL s1-schema-two-column: r93 rc=0 r94 rc=0 needles=SETUP PIN_SCHEMA`
  (`R94ExecMutations/fg-base.log`). See C-state deviation D1.

## C2 — `curation-r94.py` (four mutants)

Each mutant was placed at `corpus/evidence/round94/curation-r94.py` in its own full clone of C
(`$S/c2tree/M<n>`); clean and controls commands are from that clone root:

```
python3 -B corpus/evidence/round94/curation-r94.py --root .
python3 -B corpus/evidence/round94/curation-controls-r94.py --root . --work $S/w/c2clone-ctl-M<n>
```

| Mutant | Change | Clean run | Controls | Verdict |
|---|---|---|---|---|
| M5 | `punct_quote_cell` returns False for three-cell rows (leg dead) | rc 1, `VERDICT fields_hold=0 legs_ok=14/16 DETECTOR_WITNESS=16/17`, `LEG_FAIL WITNESS 16/17 bad=1`, `CURATION_R94=FAIL` | rc 1, `FAIL positive: r94 rc=1`, `PUNCT_NAMED=0/2` | **KILLED** |
| M6 | leg 16 (`PUNCTQUOT`) append deleted, `EXPECTED_LEGS` stays 16 | rc 1, `LEG_FAIL ARITY expected=16 measured=15`, `LEG_FAIL LEGSET missing=PUNCTQUOT extra=none`, `CURATION_R94=FAIL` | rc 1, `FAIL positive: r94 rc=1`, `PUNCT_NAMED=0/2` | **KILLED** |
| M7 | `locates()` drops the punctuation guard (r93 form) | rc 1, `DETECTOR_WITNESS=16/17`, `LEG_FAIL WITNESS 16/17 bad=1`, `CURATION_R94=FAIL` | rc 1, `FAIL positive: r94 rc=1` | **KILLED** |
| M8 | `fields_hold` drops `not punct_quote_rows` (shape branch and leg 16 untouched) | rc 0, `VERDICT fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=17/17`, `CURATION_R94=PASS` | rc 0, `CONTROLS=PASS ... PUNCT_NAMED=2/2 PRIOR_REGRESSION=7/7` | **SURVIVOR** (finding F1) |

M8 equivalence probe on the controls' X1 tree (`$S/w/c2clone-ctl-M8/x1-punct-dash`): pristine and M8
print the identical line set — `VERDICT fields_hold=0 legs_ok=11/16 DETECTOR_WITNESS=17/17`,
`LEG_FAIL QSHAPE … quote=<punctuation>`, `LEG_FAIL PUNCTQUOT … Q2`, `CURATION_R94=FAIL`
(`probe-x1-pristine.log`, `probe-x1-M8.log`). Receipts: `c2clone-clean-M5..M8.log`,
`c2clone-ctl-M5..M8.log`.

## C3 — `skill-tally-r94.py` (four mutants)

Mutant copies under `$S/mut/M<n>/corpus/evidence/round94/`; commands from `$S/repo`:

```
python3 -B $S/mut/M<n>/corpus/evidence/round94/skill-tally-r94.py --root . \
  --selftest corpus/evidence/round94/controls/selftest-r94.txt
python3 -B $S/mut/M<n>/corpus/evidence/round94/skill-tally-r94-controls.py --root . --work $S/w/c3ctl-M<n>
```

| Mutant | Change | Clean run | Controls | Verdict |
|---|---|---|---|---|
| M9 | owner failure condition is vacuous (`if False:`), i.e. the owner comparison can never refuse | rc 0, `TAIL_OWNED_OK=2/2 … LEGS=4/4`, `SKILL_TALLY_R94=PASS` (identical to pristine) | rc 1, `CONTROLS=FAIL ... MOVED_REFUSED=0/2 MOVED_PRIOR_ACCEPTED=2/2` (both moved trees accepted) | **KILLED** |
| M10 | `owned_ok = len(TAIL_OWNED)` forced after the loop (ratio constant) | rc 0, `TAIL_OWNED_OK=2/2 … TAIL_OK=1 LEGS=4/4`, `SKILL_TALLY_R94=PASS` | rc 0, `CONTROLS=PASS ... MOVED_REFUSED=2/2` | **SURVIVOR** (finding F2) |
| M11 | nearest-heading tracker never updates (`heading` stays `<none>`) | rc 1, `TAIL_OWNER_FINDING TAIL_OWNER_MISMATCH tally=215 ... owner=<none> declared=Round27 repair/status correction` (×2), `TAIL_OWNED_OK=0/2 … TAIL_OK=0 LEGS=3/4`, `SKILL_TALLY_R94=FAIL` | rc 1, `CONTROLS=FAIL ... HEADING_ALIAS_ACCEPTED=0/1` | **KILLED** |
| M12 | pure local-variable rename (`owned_ok` → `owned_hits`, 3 occurrences), control | rc 0, `TAIL_OWNED_OK=2/2 … LEGS=4/4`, `SKILL_TALLY_R94=PASS` | rc 0, `CONTROLS=PASS ... MOVED_REFUSED=2/2` | **SURVIVOR** (required control) |

M10 observable probe on the controls' moved tree (`$S/w/c3ctl-M10/moved-tail-215`): pristine prints
`TAIL_OWNED_OK=1/2 … TAIL_OK=0 … SKILL_TALLY_R94=FAIL`; M10 prints `TAIL_OWNED_OK=2/2 … TAIL_OK=0 …
SKILL_TALLY_R94=FAIL` — the ratio lies, the verdict does not move (`probe-moved-pristine.log`,
`probe-moved-M10.log`). Receipts: `c3-M9-b.log`, `c3-M10.log`, `c3-M11.log`, `c3-M12.log`,
`c3ctl-M9-b.log`, `c3ctl-M10.log`, `c3ctl-M11.log`, `c3ctl-M12.log`.

## Battery total

`MUTANTS_KILLED=9/12 SURVIVORS=3/12` (killed: M1, M2, M3, M4, M5, M6, M7, M9, M11; survivors: M8, M10,
M12). M12 is the required pure-rename control and survives, so the battery is not a blanket refusal.

## Coverage findings (survivors are findings, not contract changes)

* **F1 — M8 survivor (C2).** The `not punct_quote_rows` conjunct in `fields_hold` is redundant while the
  shape branch (`q_shape_violation`) and leg 16 exist: a punctuation row is always a shape violation, so
  `len(shape_violations)==0` and `LEG_FAIL PUNCTQUOT` already carry the verdict; on the X1 tree M8 is
  byte-identical in output to pristine (`fields_hold=0`, `legs_ok=11/16`) and controls pass. Not a refusal
  gap, and consistent with C2's stated force (K4 names the arity tripwire, not this conjunct); it is
  defense-in-depth with no independent force.
* **F2 — M10 survivor (C3).** `TAIL_OWNED_OK` is observability only: the verdict force is
  `owner_codes → tail_ok`, which M10 does not touch. On the moved tree the printed ratio moves 1/2 → 2/2
  with the same refusal. C3 K4's second clause ("`TAIL_OWNED_OK` computed from the declarations instead of
  the observed headings") is therefore not detectable by any shipped detector — the shipped bytes are
  correct, but the harness does not defend that line's derivation.
* **F3 — M4 nuance (C1).** A deleted `driver` row is accepted by the *pristine* driver
  (`PINNED_FILES=33/33 PIN_ROLES_OK=14/14 CONTROL_DRIVER_R94=PASS`, `fx-dropdrv-pristine.log`) — this is
  exactly named limit 2, measured, not hidden. M4 is killed by the frozen ratio (`PIN_ROLES_OK=34/34`
  where the predicate fixes the non-driver count 14), i.e. a predicate-text kill, not a new acceptance.
* **F4 — M1/M3 invisibility (C1).** The landing-tree `verify` cannot see M1 or M3: both print the exact
  landing line (`PIN_ROLES_OK=14/14`, PASS). They are killed only by a forged table (D1 accepted: PASS
  15/15 vs pristine PIN_ROLE_DANGLING 9/15; D4: exit 1 vs pristine exit 2). The two-command C1 structure is
  load-bearing: `verify` alone would leave both alive.
* **F5 — M9 invisibility (C3).** The clean counter cannot see M9 (identical PASS); the controls kill it
  (`MOVED_REFUSED=0/2`). The discrimination is carried by the moved-tree battery, as claimed.
* **F6 — M2 is noisy (C1).** Shrinking `CLAIM_PATHS` also *refuses* the landing table
  (`PIN_ROLE_DANGLING role=claims path=…claims.md`, 12/14). Its real defect is the accepted table with the
  `claims.md` row removed (`PIN_ROLES_OK=13/13`, PASS); both are recorded.

## C-state deviations observed in the required baselines (not mutations; no lane edit)

* **D1 — the carrier's `forgeries-r94.py` prints `FORGERIES=FAIL` at C (C1 K1).** Pristine run at C,
  rc 1: `FAIL s1-schema-two-column: r93 rc=0 r94 rc=0 needles=SETUP PIN_SCHEMA`; the case calls
  `case("s1-schema-two-column", None, 2, [...])`, and `case()` writes the **r94** (three-column) table
  with `write_r94` before the r94 run, so the r94 driver correctly returns 0 and the case can never pass;
  the two-column form is only written afterwards for the r93 run. The claim's frozen forgeries line
  (`FORGERIES=PASS …`) is therefore not reproduced at C, while the substantive counts are
  `FORGERY_REFUSED=4/4 … CARRIED_REFUSED=2/2 POSITIVE=pass`.
* **D2 — `PRIOR_ACCEPTED` at C is not an independent measurement.** In the C blob,
  `prior = sum(… if results.get(n))` is the same expression as `role_forgeries` (the claim describes it as
  the r93 driver's own rc on the two-column projection). The two numbers agreed only because they are the
  same count.
* Both are already addressed in the lane's committed HEAD `4cbaed6cc15f4cd1008b6ab6294ffe6894f3dfec`
  ("freeze F2 — … s1 dropped, prior acceptance measured", committed 12:50:45 after this seat's clone at
  C): the read-only diff `C..HEAD` drops the s1 case and adds `old_rcs` for an independent prior
  measurement. This seat did not edit the lane and reports the C state it was assigned.

## Tooling

No installs or upgrades; `python3` and the installed `git` were used, no network, no pacman. (Operator
tooling authorization read; nothing to record.)

## Restoration evidence

Pristine `$S/repo` hashes before and after the battery are identical (see Method); `git status` empty;
mutant copies only under `$S/mut/`; `$S` (including the two shared clones and the fixture tree) is removed
with `rm -rf` before yield. The lane's bytes were read-only for this seat except the report and the
receipts copied under `.ufo/waves/round-94/w1/`.

VERDICT: R94ExecMutations C1 fired — at C the frozen forgeries predicate is not met (`FORGERIES=FAIL` on pristine bytes, s1 case; `PRIOR_ACCEPTED` duplicates the refusal count), although all four C1 logic mutants are killed and the driver `verify` predicate is reproduced exactly; the lane HEAD F2 already drops s1 and measures prior acceptance.
VERDICT: R94ExecMutations C2 held — M5/M6/M7 are killed (witness, arity, witness) and controls keep `PUNCT_NAMED=2/2`; M8 survives only because the dropped `fields_hold` conjunct is redundant with the shape branch and leg 16 (identical output on the X1 tree).
VERDICT: R94ExecMutations C3 held — M9 (moved trees accepted) and M11 (owner `<none>`) are killed, the required pure-rename control M12 survives, and M10 survives because `TAIL_OWNED_OK` is observability only while the verdict-bearing owner derivation is intact.
