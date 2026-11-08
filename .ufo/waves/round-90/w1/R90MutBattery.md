# R90MutBattery — round-90 mutation probe

Seat `R90MutBattery` (leaf, mutation tester). Lane `chousa-shokunin`, root
`/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Base `f54a45ed197dd475af50d82e43a22df3d2e99782`; claim freeze
`8d9893b42eb22690ea5f920ab87fd7e1810b847a`; attacked tree
`9bad12011187d114ba2c4588c5df08a21ab28145`.

**Scratch** `/fast/scratch/hyaku/chousa-r90/R90MutBattery/` (deleted before yield). Tree construction:

* `lane-repo` — `git clone --shared` of the lane, `git checkout 9bad1201…` (history needed: the
  C1 expectations call `git -C @ROOT@ show master:tools/gate-records.py`). `git rev-parse
  --show-toplevel` = the clone; worktree clean at start and after every mutation.
* `tree` — `git archive 9bad1201… | tar -x` (C2/C3 read plain files).
* `tree283` — `tree` with the nine **current** tally cells changed `PASS (275 cases, 0 skipped)` →
  `PASS (283 cases, 0 skipped)` (the C3 discrimination leg; exactly 9 replacements, historical
  occurrences untouched).

Every fixture and work dir lives under the scratch dir. No network. No tool installs.

## Detectors (the instruments' own frozen predicates)

| axis | detector leg | command | expected |
|---|---|---|---|
| C1 | positive, frozen shape | `python3 -B <clone>/corpus/evidence/round90/control-driver-r90.py verify --root <clone> --repo <clone> --rev 8d9893… --receipts-rev 9bad1201… --work <scratch>/work/…` | exit 0, `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` |
| C1 | positive, behavioural arm | same **without `--repo`** (the self-pin is a byte tripwire; removing it is what makes a check mutation observable) | same PASS line |
| C1 | forgery leg | `python3 -B <clone>/corpus/evidence/round90/control-forgeries-r90.py --root <clone> --work <scratch>/work/… --rev 8d9893…` | exit 0, `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` |
| C2 | counter | `python3 -B <tree>/corpus/evidence/round90/curation-r90.py --root <tree>` | exit 0, `LEGS_MEASURED=10/10`, `VERDICT fields_hold=1`, `DETECTOR_WITNESS=8/8`, `CURATION_R90=PASS` |
| C2 | mutant battery | `python3 -B <tree>/corpus/evidence/round90/curation-r90-mutants.py --root <tree> --work <scratch>/work/…` | exit 0, `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2` |
| C2 | controls | `python3 -B <tree>/corpus/evidence/round90/curation-r90-controls.py --root <tree> --work <scratch>/work/…` | exit 0, `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` |
| C3 | landing leg | `<tool> --root <tree283> --selftest <receipt>` | exit 0, `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS` |
| C3 | before-state leg | same on `<tree>` (committed `SKILL.md` still says 275) | exit 1, `TALLY_ROWS=9 STALE_TALLIES=9/9 EXPECTED_CASES=283 … FAIL` |

The frozen C1 counting text does **not** carry `--work` (`claims.md` C1 and
`.ufo/waves/round-90/claims.json` `/C1/counting_command`); the exact text is tested as its own
fixture below (F1), and all behavioural runs add the required flag.

## Baseline (pristine bytes)

| receipt (`R90MutBattery/…`) | command | exit | observed |
|---|---|---|---|
| `c1-frozen-command-absolute.txt` | frozen text, exactly as claimed (no `--work`) | **2** | `control-driver-r90.py: error: the following arguments are required: --work` — no `CONTROL_DRIVER_R90` line |
| `c1-base-verify-repo.txt` | verify, `--work` + `--repo <clone>` | 0 | `RECEIPT SELF_PIN OK all scoring bytes equal their blobs at --rev` · `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` |
| `c1-base-verify-norepo.txt` | verify, `--work`, no `--repo` | 0 | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` |
| `c1-base-forgeries.txt` | forgeries, `--rev 8d9893…` | 0 | `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` · `CONTROL_FORGERIES_R90=PASS` |
| `c2-base-counter.txt` | counter | 0 | `… LEGS_MEASURED=10/10 VERDICT fields_hold=1` · `VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8` · `CURATION_R90=PASS` |
| `c2-base-mutants.txt` | mutant battery | 0 | `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2` |
| `c2-base-controls.txt` | controls | 0 | `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` · `CONTROLS=PASS` |
| `c3-base-275.txt` | landing tool on `9bad1201` tree | 1 | `TALLY_ROWS=9 STALE_TALLIES=9/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=FAIL` |
| `c3-base-283-receipt.txt` | landing tool on `tree283`, `--selftest` | 0 | `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS` |
| `c3-base-283-live.txt` | landing tool on `tree283`, live `bash tools/research-gate.sh --selftest` (143 s; the gate verdict is consumed inside the tool) | 0 | `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS` |

The C3 live run and the captured receipt agree (283/0). The capture
`corpus/evidence/round90/controls/selftest-r90.txt` is **untracked** at 9bad1201
(`git status` → `?? corpus/evidence/round90/controls/selftest-r90.txt`); it is used only through the
tool's documented `--selftest` interface and is corroborated by the live run above.

## Mutants

One point each, applied by exact string replacement with a uniqueness assertion, then reverted.
Full commands are in `R90MutBattery/logs/<id>/{cmd.txt,out.txt}`; the summary table with hashes is
`R90MutBattery/mutants.tsv`. C1's tree is `lane-repo` (driver `3a64f377…`), C2/C3's is `tree` /
`tree283` (`28dc1152…` / `c8018d1b…`).

### C1 — `control-driver-r90.py` (8 mutants)

| id | one-point change | detector leg that observed it | observed line(s) | verdict |
|---|---|---|---|---|
| M1-substring-token | `if want in toks:` → `if any(want in t for t in toks):` | forgeries | `CASE_DEVIATION B2-substring: NOT refused by r90 or NOT accepted by the prior driver` · `FORGERY_REFUSED=5/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` · rc 1 | **killed** |
| M2-skip-committed-read | committed body read replaced by the fresh output (`text = run_instrument(...)`; header still read from the committed receipt) | forgeries | `CASE_DEVIATION B1-committed: …` · `FORGERY_REFUSED=5/6` · rc 1 | **killed** |
| M3-drop-pin | the five-line `computed_against` block → `this_pin = True` | forgeries | `CASE_DEVIATION B3-no-pin` **and** `CASE_DEVIATION B3b-stale-pin` · `FORGERY_REFUSED=4/6` · rc 1 | **killed** |
| M4-drop-records-predicate | `for pred in row["predicates"]:` → `for pred in []:` | forgeries | `CASE_DEVIATION B4-harm-vacuity: …` · `FORGERY_REFUSED=5/6` · rc 1 | **killed** |
| M5-dupkey-unreachable | token-branch guard `if len(set(vals)) > 1:` → `if False:` | forgeries | `CASE_DEVIATION C-duplicate-key: …` · `FORGERY_REFUSED=5/6` · rc 1 | **killed** |
| M6-fresh-no-compare | fresh leg reduced to `this_fresh = True` (no exit compare, no `fcodes`) | behavioural verify + forgeries + pin arm | verify `… FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS`; forgeries `6/6`; pin arm `RECEIPT SELF_PIN FINDING SELF_DRIFT corpus/evidence/round90/control-driver-r90.py` (byte tripwire, not this check). Targeted fixture: pristine `FRESH_TOKEN_DETACHED:X=2 … FAIL` rc 1 vs mutant `RECEIPT FI OK … PASS` rc 0 | **survived** the behavioural detector; killed only by `SELF_PIN` on the mutated bytes |
| M7-self-pin-no-drift | `if open(disk, "rb").read() != blob:` → `if False:` | frozen `--repo` arm + targeted pin fixture (append one byte to `controls/receipts/c3-before.txt`) | **frozen arm:** `RECEIPT SELF_PIN OK all scoring bytes equal their blobs at --rev` + `COMMITTED_OK=6/6 … CONTROL_DRIVER_R90=PASS` rc 0 (receipt `logs/c1-M7-self-pin-no-drift-repo/out.txt`). **Targeted fixture:** pristine `RECEIPT SELF_PIN FINDING SELF_DRIFT corpus/evidence/round90/controls/receipts/c3-before.txt` + `FAIL` rc 1 vs mutant `SELF_PIN OK … PASS` rc 0 | **survived** the frozen predicate; killed by the targeted pin fixture (not in the frozen set) |
| M8-check-body-empty-ok | `check_body` returns `([], True, True)` when the body has no non-comment line | behavioural verify + forgeries + pin arm | verify `PASS 6/6`; forgeries `6/6`; pin arm `SELF_DRIFT`. Targeted fixture (header-only receipt): pristine `TOKEN_MISSING:X,FRESH_TOKEN_MISSING:X … FAIL` rc 1 vs mutant `RECEIPT EB OK … PASS` rc 0 | **survived** the behavioural detector; killed only by `SELF_PIN` |

### C2 — `curation-r90.py` (6 mutants beyond the committed M6–M9)

| id | one-point change | detector leg that observed it | observed line(s) | verdict |
|---|---|---|---|---|
| B1-witness-blind | `bad = [n for n, ok in rows if not ok]` → `bad = []` | mutant battery | `SURVIVOR M6-locate-true … PASS`, `SURVIVOR M7-unentailed-empty … PASS`, `SURVIVOR M9-dup-dead … PASS`, `MUTANTS_KILLED=7/10 COUNTER_DETECTED=6 BATTERY_DETECTED=1` rc 1. Counter PASS, controls `7/7` PASS | **killed** (battery only) |
| B2-fields-hold-ignores-witness | `and not witness_bad` removed from `fields_hold` | all three legs | counter `PASS`; battery `10/10`; controls `7/7` — identical to baseline. Composition B2+M6: `LEG_FAIL WITNESS 7/8 bad=1` · `LEG_FAIL VERDICT fields_hold=1 legs_ok=8/9` | **survived** |
| B3-witness-leg-forced-ok | WITNESS leg `not witness_bad` → `True` | all three legs | counter `PASS`; battery `10/10`; controls `7/7`. Under M6/M7/M9 the printed failure is `LEG_FAIL VERDICT fields_hold=0 legs_ok=9/9` — the baseline `LEG_FAIL WITNESS 7/8 bad=1` **disappears**, battery still counts the mutant killed | **survived** |
| B4-verdict-preleg-snapshot | `prior_ok = all(ok for _, ok, _ in legs)` → `legs[:-1]` (snapshot excluding the last, WITNESS, leg) | all three legs | counter `PASS`; battery `10/10`; controls `7/7` — equivalent while `fields_hold` gates on `witness_bad` and `passed` requires every leg | **survived** |
| B5-warrant-share-dropped | `if qids and len(resolved) == len(qids) and shares:` → `if qids:` | controls | `CASE_DEVIATION B1b-padding-qid: NOT refused by both counters` · `r90: rc=0 CURATION_R90=PASS` · `FORGERY_REFUSED=6/7 PRIOR_REGRESSION=7/7` · `CONTROLS=FAIL` rc 1 | **killed** |
| B6-detector-witness-constant | printed `DETECTOR_WITNESS={witness_detail}` → `8/8` | all three legs | counter `PASS` (prints 8/8); battery `10/10`; controls `7/7`. Composition B6+M6: `LEG_FAIL WITNESS 7/8 bad=1` **and** `VERDICT … DETECTOR_WITNESS=8/8` in the same run | **survived** |

### C3 — `skill-tally-r90.py` (2 mutants)

| id | one-point change | detector leg that observed it | observed line(s) | verdict |
|---|---|---|---|---|
| C1-current-widened-to-every-occurrence | `current(line)` → `return True` (historical occurrences bound too) | both trees | 275-tree: `TALLY_ROWS=12 STALE_TALLIES=12/12 … FAIL` rc 1 (baseline 9/9); 283-tree: `TALLY_ROWS=12 STALE_TALLIES=3/12 … FAIL` rc 1 (baseline PASS) | **killed** |
| C2-expected-count-read-from-file | before the stale comparison, `cases, skipped = int(rows[0][0]), int(rows[0][1])` (file, not the tool) | before-state leg only | 275-tree: `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=275 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS` rc 0 where baseline is `9/9 … FAIL`; 283-tree: `EXPECTED_CASES=283 … PASS` (identical to baseline) | **killed** by the before-state leg; **survives the landing-revision leg in isolation** |

## Findings

### F1 — C1 frozen counting command exits 2 (missing required `--work`)

Command (exactly the frozen text; cwd `lane-repo`):

```
/usr/bin/python3 -B corpus/evidence/round90/control-driver-r90.py verify \
  --root /home/vgpnk/Projects/shokunin/chousa-shokunin \
  --repo /fast/scratch/hyaku/chousa-r90/R90MutBattery/lane-repo \
  --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a \
  --receipts-rev 9bad12011187d114ba2c4588c5df08a21ab28145
```

Observed (receipt `R90MutBattery/c1-frozen-command-absolute.txt`; second copy
`c1-frozen-command-no-work.txt`): exit **2**, stderr
`control-driver-r90.py: error: the following arguments are required: --work`; no
`CONTROL_DRIVER_R90=…` line. The instrument passes the same predicate once `--work <scratch>/work/…`
is supplied (`c1-base-verify-repo.txt`, `c1-base-verify-norepo.txt`). C1's "Counting command" in
`claims.md` and `/C1/counting_command` in `claims.json` therefore cannot produce the claimed line;
the defect is in the frozen command text, not in the driver's checks.

### F2 — C1 M6 (`fresh-no-compare`) is invisible to the frozen fixture set (six committed rows + six forgery classes + positive)

Command (exact argv in `R90MutBattery/logs/c1-M6-fresh-no-compare-norepo/cmd.txt`; forgeries argv in `R90MutBattery/logs/c1-M6-fresh-no-compare-forgeries/cmd.txt`):
`… control-driver-r90.py verify --root <clone> --rev 8d9893… --receipts-rev 9bad1201… --work <scratch>/work/mut-M6-fresh-no-compare-norepo`
(receipt `R90MutBattery/logs/c1-M6-fresh-no-compare-norepo/out.txt`): exit 0,
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS`.
Forgeries (receipt `logs/c1-M6-fresh-no-compare-forgeries/out.txt`): exit 0,
`FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`. None of the six forgery classes has a
committed receipt that passes while its fresh re-run disagrees, so claim item (g) ("the instrument
re-run … agrees with the committed receipt") is not exercised by the frozen fixtures.
Targeted fixture (non-equivalence evidence, not part of the frozen set): pristine
`logs/c1-fixture-fresh-diverges-pristine.txt` → `RECEIPT FI FINDING FRESH_TOKEN_DETACHED:X=2` +
`FAIL`, exit 1; M6 `logs/c1-fixture-fresh-diverges-m6.txt` → `RECEIPT FI OK …` + `PASS`, exit 0.

### F3 — C1 M8 (`check-body-empty-ok`) is invisible to the frozen fixture set

Same commands with `…/work/mut-M8-check-body-empty-ok-norepo` (exact argv in
`R90MutBattery/logs/c1-M8-check-body-empty-ok-norepo/cmd.txt`,
`…/c1-M8-check-body-empty-ok-forgeries/cmd.txt`; receipt
`logs/c1-M8-check-body-empty-ok-norepo/out.txt`): exit 0, `PASS 6/6`; forgeries
`logs/c1-M8-check-body-empty-ok-forgeries/out.txt`: `6/6`. No fixture carries a header-only receipt.
Targeted fixture: pristine `logs/c1-fixture-empty-body-pristine.txt` →
`RECEIPT EB FINDING TOKEN_MISSING:X,FRESH_TOKEN_MISSING:X` + `FAIL`, exit 1; M8
`logs/c1-fixture-empty-body-m8.txt` → `RECEIPT EB OK …` + `PASS`, exit 0. (The call site's
`check_body(row, text) if text else (…False…)` only guards empty *text*, not a header-only body, so
this branch is reachable — the coverage gap is the fixture set, not dead code.)

### F4 — C1's `--repo` arm kills by byte drift, and the self-pin is vacuous on the committed set (M7 survives)

For seven of the eight mutants the frozen `--repo` run fails with
`RECEIPT SELF_PIN FINDING SELF_DRIFT corpus/evidence/round90/control-driver-r90.py`
(e.g. `logs/c1-M6-fresh-no-compare-repo/out.txt`, `logs/c1-M8-check-body-empty-ok-repo/out.txt`:
`COMMITTED_OK=6/6 … FRESH_OK=6/6 CONTROL_DRIVER_R90=FAIL`, exit 1). Any edit to the driver is
therefore "killed" by the pin regardless of which check it breaks; M6 and M8 are the two whose own
checks are not witnessed by a fixture.

M7 is the exception and the sharper finding: `if False:` suppresses the drift append, so the
**frozen command itself returns PASS** (`logs/c1-M7-self-pin-no-drift-repo/out.txt`:
`RECEIPT SELF_PIN OK all scoring bytes equal their blobs at --rev` … `CONTROL_DRIVER_R90=PASS`,
exit 0) even though the on-disk driver differs from its blob. The committed set has no drifted byte,
so the self-pin is a vacuously passing leg under the frozen predicate; no forgery class covers it.
A targeted fixture (append one byte to `controls/receipts/c3-before.txt`) proves the mutation is
non-equivalent: pristine `RECEIPT SELF_PIN FINDING SELF_DRIFT …c3-before.txt` + `FAIL` rc 1
(`logs/c1-pin-fixture-pristine/out.txt`) vs mutant `SELF_PIN OK … PASS` rc 0
(`logs/c1-pin-fixture-mutant/out.txt`). Exact `--repo` argv for every mutant is in
`R90MutBattery/logs/c1-<id>-repo/cmd.txt` (and the pin-fixture argv in
`logs/c1-pin-fixture-{pristine,mutant}/cmd.txt`).

### F5 — C2 printed fields and the witness leg are not bound on a failing path (4 survivors)

All four mutants reproduce the three frozen legs byte-for-byte in their key lines (counter `PASS`,
battery `10/10`, controls `7/7`). The masks:

* **B2** (`fields_hold` ignores `witness_bad`): the VERDICT leg's `fields_hold == prior_ok` and
  `passed`'s `all(ok)` still fail, but the failing path prints `fields_hold=1`: composition B2+M6,
  receipt `R90MutBattery/logs/c2-compose-b2-m6.txt`, lines
  `LEG_FAIL WITNESS 7/8 bad=1` and `LEG_FAIL VERDICT fields_hold=1 legs_ok=8/9`.
* **B3** (WITNESS leg forced `True`): the battery still kills M6/M7/M9, but only through the
  VERDICT leg; receipt `logs/c2-B3-witness-leg-forced-ok-mutants/out.txt` has
  `LEG_FAIL VERDICT fields_hold=0 legs_ok=9/9` and **no** `LEG_FAIL WITNESS` line, against baseline
  `logs/c2-base-mutants.txt` `LEG_FAIL WITNESS 7/8 bad=1`. The C2 sentence "die … on `LEG_FAIL
  WITNESS`" is not machine-asserted by the frozen battery.
* **B4** (pre-leg snapshot): equivalent while `fields_hold` includes `witness_bad`; no frozen leaf
  can distinguish it.
* **B6** (constant `DETECTOR_WITNESS=8/8`): composition B6+M6, receipt
  `logs/c2-compose-b6-m6.txt`, prints `LEG_FAIL WITNESS 7/8 bad=1` and
  `VERDICT fields_hold=0 legs_ok=8/10 DETECTOR_WITNESS=8/8` in one run; no frozen leg parses
  `DETECTOR_WITNESS` on a failing path.

### F6 — C2 B1 (`witness-blind`) is caught only by the mutant battery

Receipts: counter `logs/c2-B1-witness-blind-counter/out.txt` exit 0 `CURATION_R90=PASS`; controls
`logs/c2-B1-witness-blind-controls/out.txt` exit 0 `FORGERY_REFUSED=7/7 … CONTROLS=PASS`; battery
`logs/c2-B1-witness-blind-mutants/out.txt` exit 1
`SURVIVOR M6-locate-true …`, `SURVIVOR M7-unentailed-empty …`, `SURVIVOR M9-dup-dead …`,
`MUTANTS_KILLED=7/10 COUNTER_DETECTED=6 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2`.
The round-90 battery is the only leaf that observes a dead witness.

### F7 — C2 B5 (`warrant-share-dropped`) is caught by the controls battery

Receipt `logs/c2-B5-warrant-share-dropped-controls/out.txt`: exit 1,
`CASE_DEVIATION B1b-padding-qid: NOT refused by both counters`, `r90: rc=0 CURATION_R90=PASS`,
`FORGERY_REFUSED=6/7 PRIOR_REGRESSION=7/7`, `CONTROLS=FAIL`. The counter alone and the mutant
battery alone stay green on this mutant; the tree-forgery mirrors are what bind the warrant rule.

### F8 — C3 discrimination is carried by the two-tree pair, not the landing leg alone

`C2-expected-count-read-from-file` prints a PASS at `tree283` identical to baseline
(`logs/c3-C2-expected-count-read-from-file-tree283/out.txt`: `EXPECTED_CASES=283 … PASS`, exit 0);
its only kill is the before-state tree (`logs/c3-C2-expected-count-read-from-file-tree275/out.txt`:
`EXPECTED_CASES=275 … PASS` where the committed "Before" receipt `c3-base-275.txt` is
`STALE_TALLIES=9/9 … FAIL`). The "expected from the file instead of the tool" class named in K2 is
therefore bound by the before-state assertion, not by the landing-revision command in isolation.

## Non-equivalence evidence for the surviving mutants

| survivor | fixture | pristine | mutant |
|---|---|---|---|
| C1 M6 | committed receipt `X=1`, fresh stub prints `X=2` (`fixtures/fresh-diverges/`) | `RECEIPT FI FINDING FRESH_TOKEN_DETACHED:X=2` · `FRESH_OK=0/1` · rc 1 (`logs/c1-fixture-fresh-diverges-pristine.txt`) | `RECEIPT FI OK committed+exact+pin+fresh` · `PASS` · rc 0 (`…-m6.txt`) |
| C1 M8 | header-only receipt, silent stub (`fixtures/empty-body/`) | `RECEIPT EB FINDING TOKEN_MISSING:X,FRESH_TOKEN_MISSING:X` · rc 1 (`logs/c1-fixture-empty-body-pristine.txt`) | `RECEIPT EB OK committed+exact+pin+fresh` · rc 0 (`…-m8.txt`) |
| C1 M7 | committed set with one appended byte in `controls/receipts/c3-before.txt` | `RECEIPT SELF_PIN FINDING SELF_DRIFT …c3-before.txt` · `CONTROL_DRIVER_R90=FAIL` · rc 1 (`logs/c1-pin-fixture-pristine/out.txt`) | `RECEIPT SELF_PIN OK …` · `PASS` · rc 0 (`logs/c1-pin-fixture-mutant/out.txt`) |
| C2 B2 / B6 | one-point combos with the committed M6 (`locates` forced true) | — | `…/logs/c2-compose-b2-m6.txt`, `…/logs/c2-compose-b6-m6.txt` (lines quoted in F5) |

## Restoration evidence

Pristine file hashes equal `corpus/evidence/round90/instrument-pins.txt` exactly:
driver `3a64f377894a0736bd103e6a63493745c09faf4eb5a799b8b56f6e5cfabd086a`,
curation `28dc1152b0ac1fb67dcca47ff618313c8d2268fecdb5d7967483f8ad128be90a`,
tally `c8018d1b34ba61601868eaaa0679d0df1e6e5d0cfc4646f0c745610aa7ebb950`.
Every mutant row's `sha256_restored` equals its `sha256_pristine` (`R90MutBattery/mutants.tsv`);
the clone worktree is clean (`git -C lane-repo status --porcelain` printed nothing), and
`controls/receipts/c3-before.txt` was restored to
`4ea066814ec3a268502e362f4a20e9d5e75c3fc3198bacb421054d1ecd25a6d3` (equal to the archive copy).
Post-restore reruns reproduce the baselines: `logs/post-restore-c1-verify.txt`
(`… CONTROL_DRIVER_R90=PASS` rc 0), `logs/post-restore-c1-forgeries.txt`
(`CONTROL_FORGERIES_R90=PASS` rc 0), `logs/post-restore-c2-counter.txt` (`CURATION_R90=PASS` rc 0),
`logs/post-restore-c2-mutants.txt` (`MUTANTS_KILLED=10/10 …` rc 0),
`logs/post-restore-c2-controls.txt` (`CONTROLS=PASS` rc 0), `logs/post-restore-c3-275.txt`
(`STALE_TALLIES=9/9 … FAIL` rc 1), `logs/post-restore-c3-283.txt`
(`STALE_TALLIES=0/9 … PASS` rc 0).

| axis | mutant | sha256 pristine | sha256 mutant | sha256 restored |
|---|---|---|---|---|
| C1 | M1-substring-token | 3a64f377894a0736bd103e6a63493745c09faf4eb5a799b8b56f6e5cfabd086a | d10c78e0845d29d5d6eed566413bbebd17f0c566d087a1c83642f0a02f4159c0 | 3a64f377894a0736bd103e6a63493745c09faf4eb5a799b8b56f6e5cfabd086a |
| C1 | M2-skip-committed-read | 3a64f377… (as above) | 8b3a745102a3a2e22453e10ad0ed27d53a02e0afd057dff8d2342188144faa1e | 3a64f377… |
| C1 | M3-drop-pin | 3a64f377… | e3bce842ba8d8db399463be9f4d776267b449cc03bc1f06e4f2599fb77cba267 | 3a64f377… |
| C1 | M4-drop-records-predicate | 3a64f377… | 6b92514afd0af71cc0f351618a4c1c049ae6a3cabee7f05ca554bed43ca714fd | 3a64f377… |
| C1 | M5-dupkey-unreachable | 3a64f377… | 4a5c30faacb33758db0d190b15a1364b512f1a6447a12fd6000297bd22404c4b | 3a64f377… |
| C1 | M6-fresh-no-compare | 3a64f377… | 9d96c86ddb725a0f99d92fb2540022c88d15e1871158c2007325262b6b4177d6 | 3a64f377… |
| C1 | M7-self-pin-no-drift | 3a64f377… | bf94de64358e0111a494a582dcf3d9d2aa086deded02cbf570e2985b30c13aeb | 3a64f377… |
| C1 | M8-check-body-empty-ok | 3a64f377… | 35934cde4b1f2741e226d7b2689b19e123a9c46cc0b8cd4967175f51b6fcda57 | 3a64f377… |
| C2 | B1-witness-blind | 28dc1152… | 0bc2c22c97000337f9deb14ee69820848bdd17c21a2aa63492b044febc6aaecb | 28dc1152… |
| C2 | B2-fields-hold-ignores-witness | 28dc1152… | 9b4600de94abea77c7addb8d433e31a46a77538578ddab7990b2351ab2552d54 | 28dc1152… |
| C2 | B3-witness-leg-forced-ok | 28dc1152… | 021023aa882f443f93d797f725f6109b88170e70fa6879138977a89988f79cf0 | 28dc1152… |
| C2 | B4-verdict-preleg-snapshot | 28dc1152… | 92c3ef4829db6608217cb3585552f04fc729aeccd8cb8ecd4bbf19c1953d5e4a | 28dc1152… |
| C2 | B5-warrant-share-dropped | 28dc1152… | 4dabc9810dea75c1da4c48bc43e3b3ccfe1a1ff126334b8e1c7e430bc4d085b9 | 28dc1152… |
| C2 | B6-detector-witness-constant | 28dc1152… | ea0218e5017dac55a09121aff0a5ce022f2a771ed5a832bb95e2a028ed224973 | 28dc1152… |
| C3 | C1-current-widened-to-every-occurrence | c8018d1b… | 82e819da61a9287dd9a626fc9f00ef8557d414c6994a8b81af705ec35f270638 | c8018d1b… |
| C3 | C2-expected-count-read-from-file | c8018d1b… | 231881c84b85985f20a69b5caf465915106b3ebd7dd81c08a3dd4cbd05ee2bf0 | c8018d1b… |

(`…` in the restored/pristine columns is the literal full hash given once per axis above; the
unabbreviated 16×3 table is `R90MutBattery/mutants.tsv`.)

## Limits of this probe

- One-point edits, single mutants; no coupled edits. The C1 M2 edit replaces the committed-read
  block (still one behaviour point), because a forward reference to the later fresh output was
  required to make "ignore the committed body" runnable.
- The C1 behavioural arm omits `--repo`; with `--repo` every driver edit is refused by `SELF_DRIFT`
  before the check under test is reached (F4). M7 is the exception whose own leg is the fixture.
- C2 detector credit is given only for a leg token deviation. `B5` needs the controls battery; `B1`
  needs the mutant battery; the counter alone passes both mutants.
- C3 mutant runs use the `--selftest` receipt (documented interface) for determinism; the live
  selftest was run once on `tree283` (143 s) and agreed. The receipt file is untracked at the
  attacked revision (see Baseline).
- Surviving mutants are coverage findings only; none was used to alter the frozen contract, the
  instruments, or the tree.
- No network; no host state touched; no lane/fleet git or jj mutation (the only git repo written is
  the scratch `--shared` clone, verified by `git rev-parse --show-toplevel` and left clean).

## Tooling

None installed or upgraded.

VERDICT: R90MutBattery C1 fired — the frozen counting command omits the required `--work` and exits 2 with no `CONTROL_DRIVER_R90` line (the instrument with `--work` prints PASS 6/6), three mutants survive the frozen fixtures (`fresh-no-compare` and `empty-body-ok` die only by `SELF_PIN` byte drift; `self-pin-no-drift` survives the full `--repo` command), and targeted fixtures show all three change acceptance.
VERDICT: R90MutBattery C2 held — all three frozen legs reproduce exactly at the landing tree (PASS / 10-10 / 7-7) and the committed counter kills both round-89 survivors on `LEG_FAIL WITNESS`; four one-point mutants survive only as printed-field / leg-name coverage gaps, not as frozen-predicate deviations.
VERDICT: R90MutBattery C3 held — the two-tree predicate reproduces (275-tree `STALE_TALLIES=9/9` FAIL; 283-tree `STALE_TALLIES=0/9` PASS) and kills both mutations, though the expected-from-file class is bound only by the before-state leg.
