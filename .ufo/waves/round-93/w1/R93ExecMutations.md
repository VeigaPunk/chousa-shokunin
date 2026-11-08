# R93ExecMutations — mutation battery on the three round-93 instruments

Seat `R93ExecMutations` (leaf, wave `round-93/w1`). Target tree: carrier `C2 = 754b62fb6adc60e44e12375af5461a0ebe302994`,
instrument freeze `F2 = b7241252c2358613d3b22b7d0454d98c56dab373`, per `.ufo/waves/round-93/claims.md` (read first)
and `claims.json`. Scratch `S=/fast/scratch/hyaku/chousa-r93/R93ExecMutations` (`git clone --shared … && git -C … checkout C2`,
`git -C $S/repo rev-parse --show-toplevel` = `$S/repo` before any git call). No lane file, no clone file and no sibling tree
was edited: every mutant is a **copy** under `$S/mut/<id>/`. Receipts cited below are copied to
`.ufo/waves/round-93/w1/R93ExecMutations-receipts/` (57 files, including `mutant-digests.txt`).
No tool was installed or upgraded; no network request was made; `pacman` untouched.

## Method (and why a frozen-rev mutant cannot be scored by the pin discipline)

Each mutant is exactly one textual edit (M8 and M12 are the two named multi-occurrence edits) to a copy of one
instrument; each detector then runs the **pristine** instrument and the **mutant** instrument on the *same* input bytes
and both results are recorded. Three detector families, all taken from the claims' own counting commands:

- C1: `control-driver-r93.py verify …` on extracted copies of `C2` (explicit `--expected/--receipts/--pins`, no `--repo`,
  which is the form `forgeries-r93.py` itself uses), plus one rev-split fixture for M3 (see M3).
- C2: `curation-r93.py --root .` and `curation-controls-r93.py --root . --work …` (the mutant's controls are run from a
  mirrored `corpus/evidence` tree so their `HERE`-relative siblings resolve).
- C3: `skill-tally-r93.py --root . --selftest …` and `skill-tally-r93-controls.py --root . --work …`.

**Kill criterion, stated up front.** A mutant is *killed* when any claim-predicate field or finding line, or the exit
code, differs from the pristine instrument's on the same input; *survivor* when every compared line and the exit code are
identical. Two tallies are reported because two readings are defensible:

- **predicate level** (headline): the claims' predicates are conjunctions over *printed fields* (`LEGS_MEASURED=15/15`,
  `Q_WSQUOT`, `PINNED_FILES`, `HIST_DERIVED`, …), so a changed field is a kill.
- **verdict level** (stricter): only the `…=PASS/FAIL` token and the exit code count.

Why the driver's own pin discipline cannot score a mutated driver against `F2`: `self_pin` compares `rel_for(root, __file__)`
to the blob at `--rev`, and `pin_at_rev` compares every pins row to the blob at the revision that carries it. Any mutant
driver byte therefore *must* drift at `F2`; a mutant that passes would have to be a coherent joint edit of instrument,
pin row, receipt and expectation row — claims.md **named limit (1)**, i.e. the harness. The mutation probes below
therefore run the driver as an out-of-tree instrument against fixture trees (the same posture `forgeries-r93.py` uses),
except M3, where a fixture git history is built so the pin table is coherent and the *only* possible inconsistency is
M3's own.

## Baselines (pristine bytes)

| claim | command | receipt | observed | rc |
|---|---|---|---|---|
| C1 verify | `cd $S/repo && python3 -B corpus/evidence/round93/control-driver-r93.py verify --root . --repo . --rev F2 --receipts-rev C2 --work $S/work/base-c1` | `c1-verify-baseline.log` | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS` + `RECEIPT SELF_PIN OK rev=b7241252… receipts_rev=754b62fb…` | 0 |
| C1 battery | `… forgeries-r93.py --root . --repo . --rev F2 --receipts-rev C2 --work …` | `c1-forgeries-crash-py314.log` | **no `FORGERY_REFUSED=` line at all**; `tarfile.AbsoluteLinkError: '.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep' is a link to an absolute path` | **1** |
| C1 battery (3.13) | `~/.local/bin/python3.13 -B … forgeries-r93.py …` | `c1-forgeries-py313.log` | `FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1 POSITIVE=fail` | 1 |
| C2 counter | `python3 -B corpus/evidence/round93/curation-r93.py --root .` | `C2-counter-pristine.log` | `CURATION_R93=PASS`, `LEGS_MEASURED=15/15 … Q_SHAPE_FAIL=0 Q_WSQUOT=0`, `VERDICT fields_hold=1 legs_ok=15/15` | 0 |
| C2 controls | `… curation-controls-r93.py --root . --work …` | `C2-controls-pristine.log` | `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7` | 0 |
| C3 counter | `… skill-tally-r93.py --root . --selftest corpus/evidence/round93/controls/selftest-r93.txt` | `C3-counter-pristine.log` | `SKILL_TALLY_R93=PASS … LEGS=4/4` | 0 |
| C3 controls | `… skill-tally-r93-controls.py --root . --work …` | `C3-controls-pristine.log` | `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1 HIST_REFUSED_BOTH=1/1 TAIL_REFUSED=2/2 TAIL_PRIOR_ACCEPTED=1/1 TAIL_ADDED_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1` | 0 |

## C1 — `control-driver-r93.py` mutants

### F1 (finding, claim-level): the C1 battery cannot print its claim predicate

1. **Host interpreter.** `python3 --version` = `Python 3.14.8`. `forgeries-r93.py:51` calls `tf.extractall(dest)` with no
   `filter=`, and 3.14's default data filter rejects the absolute symlink
   `.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep` → `/bin/false`, which `git ls-tree` shows committed at `C2`
   (mode `120000`). Observed: exit **1**, empty stdout, traceback
   `tarfile.AbsoluteLinkError: '.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep' is a link to an absolute path`
   (`c1-forgeries-crash-py314.log`). The claim's `FORGERY_REFUSED=2/2 …` line is never printed, so C1's second
   conjunct fails K1 outright on this host.
2. **Older interpreter does not rescue it.** Under `~/.local/bin/python3.13` the archive extracts and the battery runs,
   but the pristine archive scores `FRESH_OK=4/6`, so `positive` and `derive-from-root` both fail:
   `FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1 POSITIVE=fail`, exit **1** (`c1-forgeries-py313.log`). Cause is
   structural, not version-specific: the battery scores an archive tree that has **no `.git`**, while two expected rows
   need git history at `--root` (`c1-harm` runs `git -C @ROOT@ show 265b8633…:tools/gate-records.py`; `c1-mutants-r89`
   runs `mutate-r89.py --repo @ROOT@`). Independent seat `R93ExecC1Repro` reports the same two causes.
   So M4's canonical detector (the `DERIVE_OK` leg) is dead on this host, and the driver mutants below had to be probed
   directly.

### Mutant results

| id | edit (one point) | detector | pristine | mutant | verdict |
|---|---|---|---|---|---|
| M1 | `pin_report`: `PIN_MISSING` row becomes a silent `continue` | pinned-but-unexecuted instrument deleted from the tree | `RECEIPT PINS FINDING PIN_MISSING path=corpus/evidence/round93/curation-controls-r93.py`, `PINNED_FILES=21/22`, rc 1 | no `PIN_MISSING` line; `PINNED_FILES=21/22`, rc 1 | **killed** (predicate level) / survives verdict level |
| M2 | `receipt_pins`: receipt counted without comparing its bytes | one receipt body appended | `PIN_DISK_MISMATCH path=…/receipts/c2-prior-landing.txt,RECEIPT_MISMATCH:c2-prior-landing`, `RECEIPT_PINS=5/6`, rc 1 | only `PIN_DISK_MISMATCH …`, `RECEIPT_PINS=6/6`, rc 1 | **killed** (predicate level) / survives verdict level |
| M3 | `self_pin`: `pin_at_rev(repo, receipts_rev, at_carrier)` → `pin_at_rev(repo, rev, at_carrier)` | coherent rev-split fixture (receipts re-emitted at `A`, pins re-sealed, `--rev A --receipts-rev B`) | `RECEIPT SELF_PIN OK`, `PIN_OK=6/6`, `PINNED_FILES=22/22`, `CONTROL_DRIVER_R93=PASS`, rc 0 | `RECEIPT SELF_PIN FINDING SELF_DRIFT …receipts/{c1-gate-r89,c1-harm-setup,c1-harm,c1-mutants-r89,c2-prior-controls,c2-prior-landing}.txt@2d31008e…`, `PIN_OK=6/6`, `PINNED_FILES=22/22`, `CONTROL_DRIVER_R93=FAIL`, rc 1 | **killed** |
| M4 | `main()`: `--expected/--receipts/--pins` defaults revert to `HERE` | derive form (no explicit paths) on the pristine `C2` copy | `… PINNED_FILES=22/22 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS`, rc 0 | `CONTROL_DRIVER_R93=SETUP missing $S/mut/M4/controls/expected.tsv`, rc 2 | **killed** |

Exact commands (M1/M2/M4 first column; M3 second):

```
python3 -B $S/mut/<id>/control-driver-r93.py verify --root $S/tree/p_<kind>_<id> --work $S/wk/c1_<kind>_<id> \
  --rev F2 --receipts-rev C2 --expected <tree>/corpus/evidence/round93/controls/expected.tsv \
  --receipts <tree>/corpus/evidence/round93/controls/receipts --pins <tree>/corpus/evidence/round93/instrument-pins.txt
python3 -B $S/repo3c/corpus/evidence/round93/control-driver-r93.py verify --root $S/repo3c --repo $S/repo3c \
  --rev 03b7d4551c6f4c068905c3305c452e5132d67954 --receipts-rev 2d31008e543258d4b7d61b57789572ac411c095e \
  --work $S/wk/m3-clean --expected …/controls/expected.tsv --receipts …/controls/receipts --pins …/instrument-pins.txt
```

Receipts: `c1-clean-M1.log`, `c1-missing-pristine.log`, `c1-missing-M1.log`, `c1-receipt-pristine.log`,
`c1-receipt-M2.log`, `c1-derive-pristine.log`, `c1-derive-M4.log`, `m3-baseline.log`, `m3-clean.log`,
`c1-clean-M{2,3,4}.log` (all four clean-tree runs print `CONTROL_DRIVER_R93=PASS`, rc 0, i.e. no mutant degrades a clean
tree — the baseline for each is the same line from `c1-clean-pristine.log`).

M3 needed two fixtures; the first is kept as `c1-revsplit-M3.log` and is **superseded, not counted**: there the receipts
still carried `# computed_against=F2` while the probe passed `--rev A`, so `PIN_OK` fell 6/6→0/6 for a fixture reason and
the SELF_DRIFT label (`@{receipts_rev}`) was attached to entries actually compared at `rev`. The reported run re-emits
every receipt at `A` and re-seals their pins rows and the minus-self row, so `PIN_OK=6/6`, `PINNED_FILES=22/22`,
`RECEIPT_PINS=6/6`, `FRESH_OK=6/6` are all full and the single differing line is `RECEIPT SELF_PIN` — OK on the baseline,
`SELF_DRIFT` on the mutant.

### F2/F3 (findings): M1 and M2 lose their diagnostic, not the refusal

- M1: the refusal survives only because `passed` also requires `checked == len(pins)`; the mutant still prints
  `PINNED_FILES=21/22` and exits 1. The *class* the mutation attacks — a pinned file that vanishes — is refused, but no
  longer named. Nothing in the pins table pins the `PIN_MISSING` diagnostic itself.
- M2: the refusal survives only because the six receipts are *also* rows of the pins table, so `pin_report`'s file-level
  loop emits `PIN_DISK_MISMATCH` for the same bytes. `RECEIPT_PINS` is therefore double-covered; the receipt-level
  comparison is not load-bearing for the verdict (it is load-bearing for the field).
- M3's mutated code labels its drift entries `@{receipts_rev}` while comparing at `rev` — the mutated instrument would
  print a *false* revision in its own finding. Worth reproducing in the r94 mutant vocabulary: an instrument's diagnostic
  label is part of its evidence.

## C2 — `curation-r93.py` mutants

| id | edit (one point) | detector | pristine | mutant | verdict |
|---|---|---|---|---|---|
| M5 | `q_shape_violation`: `inner = cells[2].strip().strip('"')` (r92 ordering) | controls | `CONTROLS=PASS … WS_NAMED=2/2`; ws-space `shapes old=0 new=1 ws new=1` | `CONTROLS=FAIL … WS_NAMED=0/2`; ws-space `FAIL` `shapes old=0 new=0 ws new=1`, rc 1 | **killed** |
| M6 | WSQUOTE leg deleted, `EXPECTED_LEGS` left at 15 | counter on `C2` | `CURATION_R93=PASS`, `LEGS_MEASURED=15/15`, rc 0 | `CURATION_R93=FAIL`, `LEGS_MEASURED=14/14`, rc 1; controls `FAIL positive … r93 rc=1`, `CONTROLS=FAIL`, rc 1 | **killed** |
| M7 | ws population counted *after* the shape filter | controls + ws-space tree | ws-space: `Q_SHAPE_FAIL=1 Q_WSQUOT=1`, `LEG_FAIL WSQUOTE … Q2`, rc 1 | ws-space: `Q_SHAPE_FAIL=1 Q_WSQUOT=0`, **no** WSQUOTE leg failure (`legs_ok=11/14` vs `10/14`), rc 1; controls `CONTROLS=PASS … WS_NAMED=2/2` rc 0 | **survivor at verdict level; killed only at field level** |
| M8 | WSQUOTE leg deleted **and** `EXPECTED_LEGS = 14` (the r92 hole) | counter on `C2` + controls | `LEGS_MEASURED=15/15`, PASS, rc 0 | `LEGS_MEASURED=14/14`, `CURATION_R93=PASS`, rc 0; `CONTROLS=PASS`, rc 0 | **survivor at verdict level; killed only at field level** |
| M12 | local rename only (`witness_bad`→`witness_broken`) | counter + controls | `LEGS_MEASURED=15/15`, `CONTROLS=PASS`, rc 0 | byte-identical lines, rc 0 | **SURVIVOR (control)** |

Commands: `python3 -B $S/mut/<id>/corpus/evidence/round93/curation-r93.py --root $S/repo` and
`python3 -B $S/mut/<id>/corpus/evidence/round93/curation-controls-r93.py --root $S/repo --work $S/wk/C2_controls_<id>`,
plus `… curation-r93.py --root $S/wk/C2_controls_M7/ws-space` for the field-level probe.
Receipts: `C2-counter-M{5,6,7,8,12}.log`, `C2-controls-M{5,6,7,8,12}.log`, `C2-wstree-{pristine,M5,M7,M8}.log`.

### F4 (finding, C2): the claim's K4 whitespace clause is asserted nowhere

claims.md K4 requires that `Q_WSQUOT` "count the row on the forged tree and stay 0 on the clean one". M7 satisfies the
kill rule's defect exactly — it counts only rows the shape test already dropped — yet **both** the counter and the
controls stay green: `CONTROLS=PASS … WS_NAMED=2/2`, rc 0 (`C2-controls-M7.log`), because `case()` checks only
`r93 rc` and the `quote=<whitespace>` needle, and the needle is still satisfied by `LEG_FAIL QSHAPE`, while the field it
prints (`ws new=0`) is never asserted. Evidence: `C2-wstree-pristine.log` (`Q_SHAPE_FAIL=1 Q_WSQUOT=1`,
`LEG_FAIL WSQUOTE … Q2`) vs `C2-wstree-M7.log` (`Q_SHAPE_FAIL=1 Q_WSQUOT=0`, no WSQUOTE leg failure).
Routable fix for r94: make `WS_NAMED` also require `fl_new["Q_WSQUOT"] == "1"` and `LEG_FAIL WSQUOTE` on both trees.

### F5 (finding, C2): `EXPECTED_LEGS` is unpinned, so the r92 hole is only half-closed

M6 (leg deleted, constant untouched) is caught — `LEGS_MEASURED=14/14`, rc 1. M8 (both changed) is not: `CURATION_R93=PASS`
with `LEGS_MEASURED=14/14`, rc 0, and the controls also pass, because the controls mirror `NEW`'s own verdict. Only the
claim's literal `LEGS_MEASURED=15/15` conjunct distinguishes them, and no instrument or pins row carries that number.
This is claims.md named limit (1) if read as a joint edit of the counter, but K4's wording ("the leg can be deleted
without a verdict change (`EXPECTED_LEGS`)") presents `EXPECTED_LEGS` as the guard, and it is not: `EXPECTED_LEGS` only
catches a *half* edit. Routable fix for r94: have the controls assert `LEGS_MEASURED` = a literal they own.

## C3 — `skill-tally-r93.py` mutants

| id | edit (one point) | detector | pristine | mutant | verdict |
|---|---|---|---|---|---|
| M9 | the historical multiset is a frozen literal (`{'161','0'}`,`{'256','0'}`), receipt loop and scope-presence vacuous | controls | `CONTROLS=PASS … HIST_UNGROUNDED_REFUSED=1/1`, rc 0 | `FAIL ungrounded-historical … r93 rc=0`, `CONTROLS=FAIL … HIST_UNGROUNDED_REFUSED=0/1`, rc 1 | **killed** |
| M10 | receipt grounding deleted (`hist_derived = len(HIST_SOURCES)`) | controls | as above | `FAIL ungrounded-historical … r93 rc=0`, `CONTROLS=FAIL … HIST_UNGROUNDED_REFUSED=0/1`, rc 1 | **killed** |
| M11 | tail scan deleted (`tail_counts = dict(TAIL_DECLARED)`, `tail_ok = True`) | controls | `TAIL_REFUSED=2/2`, rc 0 | `FAIL deleted-tail … r93 rc=0`, `FAIL added-tail … r93 rc=0`, `CONTROLS=FAIL … TAIL_REFUSED=0/2 TAIL_PRIOR_ACCEPTED=0/1`, rc 1 | **killed** |

Commands: `python3 -B $S/mut/<id>/corpus/evidence/round93/skill-tally-r93.py --root $S/repo --selftest
$S/repo/corpus/evidence/round93/controls/selftest-r93.txt` and
`python3 -B $S/mut/<id>/corpus/evidence/round93/skill-tally-r93-controls.py --root $S/repo --work $S/wk/C3_controls_<id>`.
Receipts: `C3-counter-M{9,10,11}.log`, `C3-controls-M{9,10,11}.log`.
Note M9 and M10 are killed by the *same* control case (`D3 ungrounded-historical`): the frozen-literal defect (M9) is
only caught because the frozen `declared` multiset still equals the clean tree's scope counts; a M9 that also widened
`declared` to whatever the scope holds would survive, which is what named limit (2) admits. All three C3 mutants leave
the clean-tree counter line byte-identical (`HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_OK=1`, rc 0) — a clean tree cannot
distinguish them, by construction.

## Tallies

```
MUTANTS_KILLED=11/12 SURVIVORS=1/12            # predicate level: every printed field/finding line compared
MUTANTS_KILLED=7/12  SURVIVORS=5/12            # verdict level (…=PASS/FAIL + exit code only)
  verdict-level survivors: M1, M2, M7, M8, M12
  predicate-level survivors: M12
```

Survivor inventory: `M12` is the required do-nothing control and its output is byte-identical to pristine on both C2
detectors — the battery is not a blanket refusal. `M7` and `M8` are coverage findings against C2's own kill rules F4/F5.
`M1` and `M2` are defence-in-depth: the verdict is preserved by the `checked == len(pins)` gate and by the receipt rows
inside the pins table, so the two mutants cost diagnostics but not refusal.

## Restoration / cleanliness evidence

- Source bytes never mutated: all 12 mutant digests differ from the pristine pins-table digests only for the file under
  edit (`mutant-digests.txt`); pristine values are the pins rows of `C2`, e.g. `control-driver-r93.py ad0f60ee…`,
  `curation-r93.py d9aae45d…`, `skill-tally-r93.py e3ad8204…`.
- After every probe: `git -C $S/repo rev-parse HEAD` = `754b62fb6adc60e44e12375af5461a0ebe302994`,
  `git -C $S/repo status --porcelain` empty. The M3 fixtures live in separate clones (`$S/repo3*`) whose extra commits
  contain only the mutant bytes, the re-emitted receipts, the re-sealed pins table and the minus-self row the driver's own
  `pins_file_sha_minus_self` algorithm produced; nothing was pushed, and no other branch was touched.
- Scratch `$S` was removed before yielding; the only surviving artefacts are this report and
  `.ufo/waves/round-93/w1/R93ExecMutations-receipts/`.

VERDICT: R93ExecMutations C1 fired — the verify conjunct holds exactly at C2 (`CONTROL_DRIVER_R93=PASS`, rc 0) but the battery conjunct cannot print `FORGERY_REFUSED=2/2 … ` : host `python3` 3.14.8 dies in `tarfile` on the carrier's absolute symlink (rc 1, no predicate line) and 3.13 runs it to `FORGERY_REFUSED=0/2 DERIVE_OK=0/1 POSITIVE=fail` (rc 1) because the archived root has no git history; M3/M4 are killed when probed directly, M1/M2 only at diagnostic level.
VERDICT: R93ExecMutations C2 held — `CURATION_R93=PASS LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0 Q_WSQUOT=0` and `CONTROLS=PASS … WS_NAMED=2/2` reproduce at C2, and M5/M6/M12 behave as the claim says, but M7 (vacuous `Q_WSQUOT`) and M8 (`EXPECTED_LEGS=14` with the leg deleted) both survive every C2 instrument, routing two coverage defects to r94.
VERDICT: R93ExecMutations C3 held — `SKILL_TALLY_R93=PASS LEGS=4/4 HIST_DERIVED=2/2 TAIL_OK=1` and all eight control fields reproduce at C2, and M9/M10/M11 are each killed by the control case that names their defect (`HIST_UNGROUNDED_REFUSED=0/1`, `TAIL_REFUSED=0/2`), leaving only named limit (2) as residual.
