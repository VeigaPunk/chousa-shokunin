# R91ExecMutations — mutation battery on the three round-91 instruments

Seat `R91ExecMutations` (leaf; no `task`, no subagents, no `agent://all`, no lane edits, no commits, no network,
no sudo, no pacman). Revisions: base `265b8633b7e5d1da49da6fb948df9707373fb15c`, freeze
`F3 = 4d00d7519290569879f853d7122b82a927cda1f3`, carrier `C3 = 67954adc599bd605705d94a1ea7abb582491a907`.
Scratch (deleted before yield): `/fast/scratch/hyaku/chousa-r91/R91ExecMutations` — `repo` is
`git clone --shared <lane> repo && git -C repo checkout 67954adc…`; `fix/landing` is
`git -C repo archive C3 | tar -x -C fix/landing` plus the one-clause C3 SKILL.md repair; `mut/<id>` are
per-mutant instrument bundles (copies); `w/*.log` are the receipts copied to
`.ufo/waves/round-91/w1/R91ExecMutations-receipts/`.

Tooling: **no tool installed or upgraded** this round (the host pacman guard is in force and nothing was needed).
No network call was made; every check read committed bytes.

---

## 1. Baselines on pristine bytes (must PASS before any mutant counts)

| claim | exact command (cwd `<S>/repo`) | receipt | exit | observed |
|---|---|---|---|---|
| C1 verify | `python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . --work <S>/w/c1w --rev 4d00d7519290569879f853d7122b82a927cda1f3 --receipts-rev 67954adc599bd605705d94a1ea7abb582491a907` | `R91ExecMutations-receipts/c1-base.log` | 0 | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=6 CONTROL_DRIVER_R91=PASS`, `RECEIPT SELF_PIN OK rev=4d00d751… receipts_rev=67954adc…` |
| C1 battery | `python3 -B corpus/evidence/round91/control-forgeries-r91.py --work <S>/w/fbase` | `…/c1ctrl-base.log` | 0 | `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` |
| C2 counter | `python3 -B corpus/evidence/round91/curation-r91.py --root .` | `…/c2-base.log` | 0 | `LEGS_MEASURED=13/13`, `VERDICT fields_hold=1 legs_ok=13/13 DETECTOR_WITNESS=11/11`, `CURATION_R91=PASS` |
| C2 controls | `python3 -B corpus/evidence/round91/curation-r91-controls.py --root <S>/repo --work <S>/w/c2ctrl-base` | `…/c2ctrl-base.log` | 0 | `CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7` |
| C3 counter on **C3 tree** | `python3 -B corpus/evidence/round91/skill-tally-r91.py --root . --selftest corpus/evidence/round91/controls/selftest-r91.txt` | `…/c3-base.log` | **1** | `CASE_RANGE_FINDING RANGE_MISMATCH:bash-pin-override claimed=276-283 derived=282-283`, `CASE_RANGE_OK=1/2 MISLABELED=6`, `SKILL_TALLY_R91=FAIL` |
| C3 controls on **C3 tree** | `python3 -B corpus/evidence/round91/skill-tally-r91-controls.py --root <S>/repo --work <S>/w/c3ctrl-onrepo` | `…/c3ctrl-onrepo.log` | **2** | `SETUP repaired clause absent from SKILL.md — is this the landing tree?` |
| C3 counter on landing fixture (`fix/landing`, one SKILL.md clause repaired; diff in `…/c3-fixture-repair.diff`) | `python3 -B <S>/fix/landing/corpus/evidence/round91/skill-tally-r91.py --root <S>/fix/landing --selftest <S>/fix/landing/corpus/evidence/round91/controls/selftest-r91.txt` | `…/c3-landing.log` | 0 | `CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2`, `SKILL_TALLY_R91=PASS` |
| C3 controls on landing fixture | `python3 -B <S>/fix/landing/corpus/evidence/round91/skill-tally-r91-controls.py --root <S>/fix/landing --work <S>/w/c3ctrl-base` | `…/c3ctrl-base.log` | 0 | `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1` |

A baseline failure is inconclusive, so C3 was scored only after the landing fixture reproduced the claim's PASS
(`c3-landing.log`); the FAIL on committed C3 bytes is reported as finding F3, not as a mutant kill.

## 2. Method

* Each mutant is a **copy**: `mut/<id>/corpus/evidence/{round91,round90}` copied from `repo`; exactly one textual
  edit applied to the copy with an assertion that the pattern occurs once. Nothing under `repo` was written.
* **Detector for C2** = `curation-r91-controls.py` (the claim's own discrimination battery; `NEW` resolves to the
  mutated copy, `OLD`/`REG` to the unchanged round-90 files).
* **Detector for C3** = `skill-tally-r91-controls.py`, run with `--root <S>/fix/landing` because the battery
  hard-requires the repaired clause (proved above: on `repo` it exits 2 `SETUP`). The instrument copy under test is
  the mutated one; only the *tree* is the fixture.
* **Detector for C1** = `control-forgeries-r91.py` (the claim's clause-8 battery). `verify` is **not** a usable
  detector for driver mutants: its `SELF_PIN` leg compares the driver's own on-disk bytes with the blob at `--rev`,
  so *every* driver edit — including the rename-only control M11 — is refused:
  `RECEIPT SELF_PIN FINDING SELF_DRIFT ../mut/M11/corpus/evidence/round91/control-driver-r91.py@4d00d751…`,
  `CONTROL_DRIVER_R91=FAIL`, exit 1 (`…/M11-verify-with-repo.log`). A blanket refusal cannot discriminate, so
  `verify` is recorded per mutant only as an observation (all M1–M4/M11 print `PASS` on pristine receipts when the
  mutated driver is run without `--repo`).
* Kill rule applied: detector exits non-zero or its summary line is not `FORGERY_REFUSED=6/6 …` /
  `CONTROLS=PASS`.

## 3. Results — `MUTANTS_KILLED=10/11 SURVIVORS=1/11` (survivor M11)

`S=/fast/scratch/hyaku/chousa-r91/R91ExecMutations`. Commands below are literal with `$S` expanded; every run used
that bundle's instrument. Pristine driver `sha256=49102204…40c`, curation `c607c15c…25e`, skill-tally `cc2d5c3b…513`
(all equal to `instrument-pins.txt`).

| id | instrument | edit (old → new, one occurrence) | detector | detector rc | observed verdict line | verdict |
|---|---|---|---|---|---|---|
| M1 | control-driver | `if len(vals) > 1:` → `if len(vals) > 1 and False:` (duplicate header keys ignored) | `python3 -B $S/mut/M1/corpus/evidence/round91/control-forgeries-r91.py --work $S/w/M1` | 1 | `FAIL dup-header-exit: r91 rc=0 (HEADER_DUPLICATE:exit), r90 rc=0` · `FORGERY_REFUSED=4/6 PRIOR_ACCEPTED=4/6 POSITIVE=pass` | **killed** |
| M2 | control-driver | `pin_report` gains `return [], 0` before its body | `…/$S/mut/M2/…/control-forgeries-r91.py --work $S/w/M2` | 1 | `FAIL instrument-stub: r91 rc=0 (INSTRUMENT_PIN_MISMATCH:fx-tool.sh)` · `FAIL expected-swap: r91 rc=0 (INSTRUMENT_PIN_MISMATCH:expected.tsv)` · `FORGERY_REFUSED=4/6` | **killed** |
| M3 | control-driver | `for f in sorted(os.listdir(a.receipts)):` → `for f in ():` (UNSCORED_RECEIPT loop body disabled) | `…/$S/mut/M3/…/control-forgeries-r91.py --work $S/w/M3` | 1 | `FAIL extra-receipt: r91 rc=0 (UNSCORED_RECEIPT), r90 rc=0` · `FORGERY_REFUSED=5/6` | **killed** |
| M4 | control-driver | `HEADER_KEYS = ("case", "expected_exit", "exit", "computed_against")` → `("case", "exit", "computed_against")` | `…/$S/mut/M4/…/control-forgeries-r91.py --work $S/w/M4` | 1 | `FAIL missing-expected_exit: r91 rc=0 (MISSING_HEADER:expected_exit), r90 rc=0` · `FORGERY_REFUSED=5/6` | **killed** |
| M5 | curation | `q_shape_violation` gains `return None` before its body | `python3 -B $S/mut/M5/corpus/evidence/round91/curation-r91-controls.py --root $S/repo --work $S/w/M5` | 1 | `FAIL positive: r90 CURATION_R90=PASS r91 CURATION_R91=FAIL` · `FAIL nonq-row: r91 CURATION_R91=FAIL (LEG_FAIL QSHAPE)` · `CONTROLS=FAIL FORGERY_REFUSED=3/4 … PRIOR_REGRESSION=FAIL` | **killed** |
| M6 | curation | `source_link` gains `return True, True` before its body | `…/$S/mut/M6/…/curation-r91-controls.py --root $S/repo --work $S/w/M6` | 1 | `FAIL status-rejected: r91 CURATION_R91=PASS` · `FAIL used-by-blank: r91 CURATION_R91=PASS` · `CONTROLS=FAIL FORGERY_REFUSED=2/4` | **killed** |
| M7 | curation | `DF_MAX = 3` → `DF_MAX = 99` | `…/$S/mut/M7/…/curation-r91-controls.py --root $S/repo --work $S/w/M7` | 1 | `FAIL ubiquitous-warrant: r91 CURATION_R91=PASS (LEG_FAIL TFREQ)` · `CONTROLS=FAIL FORGERY_REFUSED=3/4` | **killed** |
| M8 | curation | r91 loop → r90 shape `for term in DEFECT_TERMS: if unentailed_terms(cells, joined): unentailed.append(...)` | `…/$S/mut/M8/…/curation-r91-controls.py --root $S/repo --work $S/w/M8` | 1 | `FAIL duplicate-count: r90 UNENTAILED_TERM=2 r91 UNENTAILED_TERM=2` · `CONTROLS=FAIL … DUPCOUNT_R91=2` | **killed** |
| M9 | skill-tally | `derived_env/derived_ovr` taken from `claimed_env/claimed_ovr` when present (range derived from the prose) | `python3 -B $S/mut/M9/corpus/evidence/round91/skill-tally-r91-controls.py --root $S/fix/landing --work $S/w/M9` | 1 | `FAIL old-prose: … r91 SKILL_TALLY_R91=PASS` · `CONTROLS=FAIL OLDPROSE_REFUSED=0/1` | **killed** |
| M10 | skill-tally | `ok_ranges = not range_codes and claimed_env == derived_env and claimed_ovr == derived_ovr` → `ok_ranges = True` (leg deleted) | `…/$S/mut/M10/…/skill-tally-r91-controls.py --root $S/fix/landing --work $S/w/M10` | 1 | `FAIL old-prose: … r91 SKILL_TALLY_R91=PASS` · `CONTROLS=FAIL OLDPROSE_REFUSED=0/1` | **killed** |
| M11 | control-driver | rename only: `normlines` → `normalized_lines` (2 sites) | `…/$S/mut/M11/…/control-forgeries-r91.py --work $S/w/M11` | **0** | `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` | **survived (control)** |

`MUTANTS_KILLED=10/11 SURVIVORS=1/11 M11` — the battery is not a blanket refusal: a behavior-preserving rename
passes it, and `verify` prints `PASS` for it on pristine receipts when run without `--repo`
(`…/M11-direct.log`).

Notable non-kill signals recorded per mutant (receipts `…/M<n>-direct.log`):

* M2: `verify` still prints `CONTROL_DRIVER_R91=PASS` with `PINNED_FILES=0` — the `passed` predicate does not
  require `checked > 0`, so a `pin_report` that checks nothing passes `verify`; only the battery kills M2.
* M7: the mutated counter still prints `TFREQ_MAX_DF=3` and `CURATION_R91=PASS` on the clean tree (`TFREQ_MAX_DF`
  is the maximum *min-DF per row*, not a function of `DF_MAX`); the forged 18th row raises `TFREQ_OK` to `18/18` and
  only the battery refuses the tree.
* M6/M7/M8: the round-90 regression leg in the controls battery printed `FORGERY_REFUSED=7/7` yet returned `rc=1`,
  and the battery scores `PRIOR_REGRESSION=FAIL`; the leg's verdict, not only its refusal count, is the signal.
* M1: the second duplicate-header forgery stays refused because the duplicated `computed_against` also trips the
  `PIN_MISMATCH` leg (`FAIL dup-header-computed: r91 rc=1 …`), so only the `exit` duplicate is the accepted one.

## 4. Findings

**F1 — C1's frozen counting command cannot run (claim wording vs code).**
Command (claims.md §C1 and `claims.json` `C1.counting_command[0]`, run at `<S>/repo`):
`python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . --rev 4d00d751… --receipts-rev 67954adc…`
→ **exit 2**, no `CONTROL_DRIVER_R91=` line at all:
`control-driver-r91.py: error: the following arguments are required: --work` (`…/c1-claim-literal.log`).
`--work` is `required=True` in the instrument and its own usage block names it. The substantive predicate is
reproduced only when `--work <scratch>` is added (`…/c1-base.log`, PASS 6/6). The claim's command as frozen is
unexecutable and its text drops a required input to a path that is written (`<work>/fresh-*.out`).

**F2 — C1's rule-2 coverage gap: no forgery class exercises `expected_exit` *value* (supplementary probe S1).**
S1 = the pristine driver with only the equality block removed (`EXPECTED_EXIT_MISMATCH`), presence check intact.
* six-class battery: `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`, exit 0 → **S1 survives the battery**
  (`…/S1-battery.log`).
* direct verify on a fixture receipt carrying `# expected_exit=1` with `# exit=0`: pristine driver refuses
  (`RECEIPT fx-one FINDING EXPECTED_EXIT_MISMATCH:1!=0`, exit 1), S1 accepts (`COMMITTED_OK=2/2 … CONTROL_DRIVER_R91=PASS`,
  exit 0) — `…/S1-S0-pristine.log`, `…/S1-S1-no-equality.log`.
So battery class 5 exercises the `MISSING_HEADER` half of rule 2 only; the "its value equals the row's" half for
`expected_exit` is unexercised by the six classes (claimed only by the fixture-free `verify` path). Finding, not a
contract change.

**F3 — C3's claim is not scorable on the wave tree.**
`skill-tally-r91.py --root . --selftest …` on committed `C3` bytes: exit **1**,
`CASE_RANGE_FINDING RANGE_MISMATCH:bash-pin-override claimed=276-283 derived=282-283`, `CASE_RANGE_OK=1/2 MISLABELED=6`,
`SKILL_TALLY_R91=FAIL` (`…/c3-base.log`); `skill-tally-r91-controls.py --root <lane> --work …` exits **2**
`SETUP repaired clause absent from SKILL.md — is this the landing tree?` (`…/c3ctrl-onrepo.log`). This matches
plans/round-91.md §9 ("the freeze tree still shows the defect") and the claim's "At the landing revision" —
but it means the C3 predicate cannot be run at `C3`/`F3` as written, and the battery must be pointed at a
reconstructed tree. My scored C3 runs use `fix/landing` (one clause changed, diff in `…/c3-fixture-repair.diff`);
the reconstruction is a fixture, never an instrument.

Corroboration (read-only, lane working tree, not written by this seat): the lane's uncommitted `SKILL.md`
(mtime `2026-11-08 08:04:20`, before this seat started at 08:21) already carries the repaired clause, and its
clause text is **byte-identical** to my fixture's (`git diff -U0 SKILL.md` vs `…/c3-fixture-repair.diff`, compared
programmatically: `IDENTICAL_CLAUSE: True`). So the landing revision that the claim names will satisfy C3; the
committed `C3` bytes do not.

**F4 — `verify` passes with zero pinned files checked (M2).** `M2-direct.log`:
`… PINNED_FILES=0 CONTROL_DRIVER_R91=PASS`. The claim's fields are `PIN_OK` (receipt `computed_against` headers),
not the pin leg's count, so this does not falsify C1 as worded; it is a hardening note: the `passed` predicate
accepts `checked == 0`. The battery covers it (M2 killed).

## 5. Restoration evidence

* Every mutant bundle was restored by copying the pristine instrument back and re-hashing:
  `restored == pristine` for all 11 (table above; `w/results.json` field `sha_restored`).
* The lane clone was never written: `git -C <S>/repo status --porcelain` is empty, `git rev-parse HEAD` =
  `67954adc599bd605705d94a1ea7abb582491a907`, and the six round-91 instrument hashes still equal
  `instrument-pins.txt` (`49102204…`, `f6218494…`, `5c4029be…`, `c607c15c…`, `69bddcb5…`, `cc2d5c3b…`).
  The only lane-path writes are the report and the receipts directory named in this file.
* The lane working tree carries three uncommitted modifications that are **not this seat's** (all older than the
  seat's first command: `SKILL.md` 08:04:20, `refetch.tsv` 08:05:29, `QUALITY.md` 08:14:13): the landing repair,
  the S221 refetch-ledger row and the QUALITY note. Nothing in this seat's runs targets the lane as a write root;
  every instrument run used `--root <S>/repo` or `--root <S>/fix/landing` and `--work` under `<S>/w`.
* Scratch `/fast/scratch/hyaku/chousa-r91/R91ExecMutations` deleted before yield (recreated once, after the first
  deletion, only to re-emit the C3 controls `SETUP` receipt whose copy had been lost, then deleted again; every
  `rm -rf` was of that one path inside the seat root, no `/tmp` use).

VERDICT: R91ExecMutations C1 fired — the frozen counting command omits the required `--work` and exits 2 (`…/c1-claim-literal.log`), while the executable form PASSes 6/6 and the six-class battery kills M1–M4 and survives only the rename control M11.
VERDICT: R91ExecMutations C2 held — counter and controls both PASS on committed bytes and the controls battery kills M5–M8 (10/11 killed overall).
VERDICT: R91ExecMutations C3 fired — on committed C3 bytes the counter prints `SKILL_TALLY_R91=FAIL` with `CASE_RANGE_OK=1/2 MISLABELED=6` and the controls exit 2 `SETUP`, so the frozen predicate is not runnable on the wave tree; on the reconstructed landing clause the counter and controls PASS and M9/M10 are killed.
