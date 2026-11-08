# R90CriticClaims — falsification of C1, C2, C3 (round 90)

Seat R90CriticClaims (godspeed), leaf. Lane chousa, L1 `ChousaR90`. Base `f54a45ed197dd475af50d82e43a22df3d2e99782`; claim
freeze `8d9893b42eb22690ea5f920ab87fd7e1810b847a`; tree attacked `9bad12011187d114ba2c4588c5df08a21ab28145` (freeze + the six
committed control receipts pinned to the freeze). Frozen predicate set read first: `corpus/evidence/round90/claims.md`,
`plans/round-90.md`, `.ufo/waves/round-90/claims.json`.

Method. Scratch `S=/fast/scratch/hyaku/chousa-r90/R90CriticClaims`; `git clone --shared` checked out at `9bad1201…` (`repo`),
`git archive` trees at base (`base`) and 9bad1201 (`tree`); every fixture under `S`; the clone is the only git tree mutated
(one receipt byte, restored; `git status --porcelain` clean afterwards); no network except C3's local `--selftest`; no lane,
fleet, sibling-repo, script or state edits; no installs. Every row names the command shape, the receipt written under
`.ufo/waves/round-90/w1/R90CriticClaims/`, the observed line and the exit code. "Fields that catch" is the column a stdout
scorer would read.

## Landing predicates (read-only, measured)

| # | Check | Command (abbreviated) | Receipt | Observed line | rc |
|---|---|---|---|---|---|
| L1 | C1 committed set, `--root . --repo .` inside the 9bad1201 tree | `control-driver-r90.py verify --root . --work <S>/wland --repo . --rev 8d9893b4 --receipts-rev 9bad1201` | `c1-landing-verify.txt` | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` + `RECEIPT SELF_PIN OK all scoring bytes equal their blobs at --rev` | 0 |
| L2 | C1 forgery battery | `control-forgeries-r90.py --root <tree> --work <S>/fland --rev 8d9893b4` | `c1-landing-forgeries.txt` | `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` / `CONTROL_FORGERIES_R90=PASS` | 0 |
| L3 | C1 with `--root <lane>` and `--repo <clone>`, driver invoked from the clone | `python3 -B repo/…/control-driver-r90.py verify --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work <S>/wlane --repo <S>/repo …` | `c1-lane-root.txt` | the L1 line, `SELF_PIN OK` | 0 |
| L4 | C1 two-path form, driver taken from the lane and `--repo` the clone | `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round90/control-driver-r90.py verify --root <lane> --work <S>/w-other --repo <S>/repo …` | `c1-lane-driver-other-repo.txt` | `RECEIPT SELF_PIN FINDING SELF_DRIFT ../../../../../../home/vgpnk/…/control-driver-r90.py,…,c3-before.txt` then `… FRESH_OK=6/6 CONTROL_DRIVER_R90=FAIL` | 1 |
| L5 | C2 counter | `curation-r90.py --root <tree>` | `c2-landing-counter.txt` | `… LEGS_MEASURED=10/10 VERDICT fields_hold=1` / `VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8` / `CURATION_R90=PASS` | 0 |
| L6 | C2 mutant battery | `curation-r90-mutants.py --root <tree> --work <S>/c2m2` | `c2-landing-mutants.txt` | `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2`; M6/M7 print `LEG_FAIL WITNESS 7/8 bad=1` | 0 |
| L7 | C2 controls frame | `curation-r90-controls.py --root <tree> --work <S>/c2c2` | `c2-landing-controls.txt` | `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` / `CONTROLS=PASS` | 0 |
| L8 | C3 before, at the attacked tree | `skill-tally-r90.py --root <tree>` | `c3-before-9bad1201.txt` | `TALLY_ROWS=9 STALE_TALLIES=9/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=FAIL` (expected by the task: `SKILL.md` still 275) | 1 |
| L9 | C3 discrimination leg: nine current cells 283, tool's own verdict | `skill-tally-r90.py --root <tree283>` | `c3-landing-283.txt` | `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS` | 0 |

L4 is a command-shape finding, not a claim miss: the claim's own sentence is `--root . --repo .` in one tree (L1). The
self-pin resolves `__file__`, `expected.tsv` and every receipt with `relpath(..., repo)`; when the driver lives outside
`--repo` those paths escape the repo and `git show` fails for all eleven scoring files (`SELF_DRIFT`), although the four
counted fields are 6/6. The command is therefore coherent only when the instrument and receipts are inside `--repo` (as in
L1/L3). Smallest safe correction: freeze the command as the dot form (or resolve driver/expected against `--root` and pin
only receipt bytes at `--receipts-rev`).

## (a) C1 — the driver's four counted fields, and what each artefact leaves blind

Mutant reference: `mut/…/control-driver-r90.py` copies with one-point edits; artefacts 1–4 replace the driver, artefacts
5–7 mutate receipts only; driver sha256 of every substituted copy differs from the pinned `3a64f377894a0736bd103e6a63493745c09faf4eb5a799b8b56f6e5cfabd086a`
(`instrument-pins.txt`), which is the enforcer outside the counter.

| # | Artefact (skips the claimed work) | Command | Receipt | Observed line | rc | Fields that catch |
|---|---|---|---|---|---|---|
| C1-1 | fresh-only, honest counters: verify never reads the committed receipt | `mut/freshonly-honest/…/control-driver-r90.py verify --root <repo> --rev 8d9893b4 --expected <tree>/…/expected.tsv --receipts <tree>/…/receipts` | `c1-m1a-verify.txt` | `COMMITTED_OK=0/6 EXACT_OK=6/6 PIN_OK=0/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=FAIL` | 1 | `COMMITTED_OK`, `PIN_OK` (the checked-in receipt read is the only source of the header/pin) |
| C1-2 | the same driver through the battery | `control-forgeries-r90.py …` (NEW = the mutant) | `c1-m1a-forgeries.txt` | `CASE_DEVIATION POSITIVE: NOT accepted by both` / `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=FAIL` | 1 | `POSITIVE` leg — a receipt-blind driver refuses the correct fixture |
| C1-3 | fresh-only, lying counters: never reads the receipt and forces `this_committed/this_pin` true | `mut/freshonly-lying/… verify --root <repo> …` | `c1-m1b-verify.txt` | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` | 0 | none of the four; the landing string is blind |
| C1-4 | the same lying driver through the battery | `control-forgeries-r90.py …` (NEW = the mutant) | `c1-m1b-forgeries.txt` | `CASE_DEVIATION B1-committed … B3-no-pin … B3b-stale-pin` / `FORGERY_REFUSED=3/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` | 1 | `FORGERY_REFUSED` (B1/B3/B3b accepted) |
| C1-5 | pin minted in `verify`, unconditional, on a receipt set carrying no pin | `mut/mint-uncond/… verify --root <repo> --expected … --receipts <S>/pinless-receipts` | `c1-m2-uncond-verify-pinless.txt`; `PINLESS receipts carrying computed_against: 0` | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` | 0 | `PIN_OK` is blind by construction; the battery catches it: `FORGERY_REFUSED=5/6` (B3 accepted), rc 1 — `c1-m2-uncond-forgeries.txt` |
| C1-6 | pin minted in `verify`, gated on `--receipts-rev`, against a scratch carrier commit whose receipts carry no pin (`git grep computed_against <carrier> -- receipts` rc 1, no output) | `mintrepo/… verify --root <repo> --repo <S>/mintrepo --rev <freeze 8c1a8ddb…> --receipts-rev <carrier f017bb1e…>` | `c1-m2b-gated-verify-repo.txt`, `c1-m2b-gated-forgeries.txt` | `RECEIPT SELF_PIN OK all scoring bytes equal their blobs at --rev` + `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS`; the battery (which never passes `--repo`/`--receipts-rev`) prints `FORGERY_REFUSED=6/6 … POSITIVE=pass` | 0 / 0 | **none**; only the instrument sha256 pin (substituted driver) and the fixed `--receipts-rev=9bad1201` (substituted receipt set) stand outside the counter |
| C1-7 | token leg back to substring (`if any(want in t for t in toks)`) | `mut/substring/… verify --root <repo> --expected … --receipts <tree>/…/receipts` | `c1-m3-verify.txt`, `c1-m3-forgeries.txt` | verify: `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 …=PASS` (blind); battery: `CASE_DEVIATION B2-substring` / `FORGERY_REFUSED=5/6` | 0 / 1 | `EXACT_OK` alone is blind; `FORGERY_REFUSED` catches B2 |
| C1-8 | receipt carrying two `# exit=` headers, decoy `1` before the correct `0` | `control-driver-r90.py verify … --receipts <S>/duphead-exit` | `c1-m4-duphead-exit.txt` | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` with the receipt still carrying `# exit=1` then `# exit=0` | 0 | none of the four; `header_fields` is last-wins and `DUPLICATE_KEY` is body-only |
| C1-9 | receipt carrying two `# computed_against=` headers, decoy `000…` before the correct freeze | `control-driver-r90.py verify … --receipts <S>/duphead-pin` | `c1-m4-duphead-pin.txt` | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` | 0 | none; same last-wins hole |
| C1-10 | the C1-8 duplicate on the frozen carrier (clone working tree, one byte changed) | `control-driver-r90.py verify --root <repo> --work <S>/w-sp --repo <repo> --rev 8d9893b4 --receipts-rev 9bad1201` | `c1-m5-dupheap-selfpin.txt` | `RECEIPT c1-gate-r89 OK committed+exact+pin+fresh` … `RECEIPT SELF_PIN FINDING SELF_DRIFT corpus/evidence/round90/controls/receipts/c1-gate-r89.txt` / `… CONTROL_DRIVER_R90=FAIL` | 1 | `SELF_PIN` at the frozen carrier; receipt bytes are restored (`git status --porcelain` clean) |

C1 do-nothing (instrument not landed): on the base tree the unchanged round-89 driver prints
`CONTROL_RECEIPTS=PASS` (8×`RECEIPT_OK`) exit 0 (`dn-c1-base.txt`), and the round-89 driver accepts all six forgery fixtures
(`prior rc=0` on each row of `c1-landing-forgeries.txt`). So the round leaves the operability surface exactly at the r89
state — committed receipts checked by the prior driver only, six forgery classes accepted — if the r90 driver is not landed.

C1 result: the landed driver meets its sentence at 9bad1201 (L1) and its battery refuses all six classes (L2). The
fresh-only/substring/ungated-mint artefacts are caught (C1-1…C1-7). Two classes survive the four fields only with
substituted bytes: gated minting (C1-6) and duplicate headers (C1-8/9), both blocked at the scored surface by
`instrument-pins.txt` + `SELF_PIN` + the fixed carrier revision. Recorded as counter-coverage gaps below; C1 itself holds.

## (b) C2 — the printed verdict, the witness, and the control frame

Mutants are one-point edits of `curation-r90.py` (or of the control frame); receipts name the mutated copy run.

| # | Artefact | Command | Receipt | Observed line | rc | Fields that catch |
|---|---|---|---|---|---|---|
| C2-1 | `fields_hold` replaced by a constant `True`, legs honest | `mut2/const-verdict/…/curation-r90.py --root <tree>` / `--root <s031-queued>` | `c2-a-base.txt`, `c2-a-queued.txt` | base: claimed PASS line; queued: `… LEGS_MEASURED=8/10 VERDICT fields_hold=1` / `VERDICT fields_hold=1 legs_ok=8/10 DETECTOR_WITNESS=8/8` / `LEG_FAIL VERDICT fields_hold=1 legs_ok=8/9` / `CURATION_R90=FAIL` | 0 / 1 | the `VERDICT` cross-check `fields_hold == prior_ok` plus `LEGS_MEASURED=10/10`: the constant token cannot turn a failing leg set into PASS |
| C2-2 | always-pass counter: constant `fields_hold` (`True or (…)`), `prior_ok=True`, every leg forced ok after the verdict append | `mut2/always-pass/…/curation-r90.py --root <tree>` / `--root <s031-queued>` | `c2-b4-base.txt`, `c2-b4-queued.txt` | base: claimed PASS 10/10; queued: `… TEACHES_UNRESOLVED=1 … LEGS_MEASURED=10/10 VERDICT fields_hold=1` / `CURATION_R90=PASS` | 0 / 0 | none of the counter's own fields at the landing tree; the mutant battery catches it: `MUTANTS_KILLED=1/10 COUNTER_DETECTED=0 BATTERY_DETECTED=1` (`c2-b4-mutants.txt`, rc 1; only M5 is battery-detected) |
| C2-3 | witness result hardcoded (`witness_bad, witness_detail = [], "8/8"`), detector bodies intact | `mut2/witness-const/…/curation-r90.py --root <tree>`; mutants | `c2-c-base.txt`, `c2-c-mutants.txt` | base: claimed PASS with `DETECTOR_WITNESS=8/8`; mutants: `SURVIVOR M6-locate-true`, `SURVIVOR M7-unentailed-empty`, `SURVIVOR M9-dup-dead`, `MUTANTS_KILLED=7/10 COUNTER_DETECTED=6 BATTERY_DETECTED=1` | 0 / 1 | `MUTANTS_KILLED` (the three constant-body substitutions survive when the witness is not consulted) |
| C2-4 | caller bypass: legs call `if cap is not None:` / `if False:` instead of `locates`/`unentailed_row`; functions and witness intact | `mut2/caller-bypass2/…/curation-r90.py --root <tree>` / `--root <nonverbatim2>`; mutants | `c2-d2-real.txt`, `c2-d2-bypass.txt`, `c2-d2-mutants.txt` | real counter on the forged tree (`Q11` quote not in the capture): `QUOTES_LOCATED=19/20 … LEG_FAIL FLOOR … LEG_FAIL WARRANT 16/17 … CURATION_R90=FAIL`; bypass: `QUOTES_LOCATED=20/20 … LEGS_MEASURED=10/10 VERDICT fields_hold=1` / `CURATION_R90=PASS`; mutants: `MUTANTS_KILLED=10/10 …` rc 0 | 1 / 0 / 0 | **none** of the three frozen C2 commands; this is C2's declared Named Limit 3 (a caller that bypasses the function is not witnessed) |
| C2-5a | control frame that passes with the seven forgeries accepted (non-positive `want=True`; literal `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7`), real counter | `mut2/controls-const/…/curation-r90-controls.py --root <tree>` | `c2-e-controls.txt` | every forged case prints `refused by r90 (…), refused by the prior counter (regression held)`; the frame still prints `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` / `CONTROLS=PASS` | 0 | the frame no longer reports acceptance or refusal; only the battery catches it (C2-5c) |
| C2-5b | the same constant frame with the always-pass counter, so all seven forgeries are **accepted** | `control-frame-const.py --root <tree> --counter <always-pass>` | `c2-e-controls-alwayspass.txt` | eight lines `r90: rc=0 CURATION_R90=PASS` (POSITIVE + the seven classes), then `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` / `CONTROLS=PASS` | 0 | none in the frame; the acceptance is real and the summary is a constant |
| C2-5c | the mutant battery with the constant frame | `curation-r90-mutants.py` with the constant frame as `BATTERY` | `c2-e-mutants.txt` | `SURVIVOR M5-lowercase-clause … detector=battery rc=0` / `MUTANTS_KILLED=9/10 COUNTER_DETECTED=9 BATTERY_DETECTED=0` | 1 | `MUTANTS_KILLED`'s battery leg (M5 is the only detector of the frame) |

C2 do-nothing: on the base tree the unchanged round-89 counter prints `CURATION_R89=PASS` with `LEGS_MEASURED=8/8` and no
`VERDICT fields_hold=1` token (`grep -c` → 0; `dn-c2-base.txt`), and both constant substitutions survive the r89 counter
(`PRIOR_R89_SURVIVORS=2/2` in `c2-landing-mutants.txt`). Without the round-90 counter the calibration surface stays at the
r89 state: no printed field-derived verdict, and the two substitutions that motivated Amendment 9 still live.

C2 result: the landed counter and both batteries meet the sentence (L5–L7). The constant `VERDICT` line is not a free pass
(it is cross-checked against the leg set, C2-1); a fully constant counter is caught only by the mutant battery (C2-2), which
is the round's claimed detector; hardcoding the witness is caught by the battery (C2-3); a constant control frame is caught
by the battery leg M5 (C2-5c). The caller bypass survives all three frozen commands and is the declared Named Limit 3
(C2-4): a tradeoff the judge must accept, not a fire.

## (c) C3 — the tally discovery rule and the tool's own verdict

| # | Artefact | Command | Receipt | Observed line | rc | Note |
|---|---|---|---|---|---|---|
| C3-1 | before, the attacked tree | `skill-tally-r90.py --root <tree>` | `c3-before-9bad1201.txt` | `TALLY_ROWS=9 STALE_TALLIES=9/9 EXPECTED_CASES=283 … SKILL_TALLY_R90=FAIL` | 1 | expected by the task (the repair lands after the wave) |
| C3-2 | nine current cells set to 283, live tool | `skill-tally-r90.py --root <tree283>` | `c3-landing-283.txt` | `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS` | 0 | the claim's landing predicate on its discrimination leg |
| C3-3 | a tenth current Gates-table row, backticked first cell, stale 275 | `skill-tally-r90.py --root <tree283> --selftest <selftest-283-fixture.txt>` | `c3-tenth-tb.txt` | `STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0` / `TALLY_ROWS=10 STALE_TALLIES=1/10 … SKILL_TALLY_R90=FAIL` | 1 | caught (and `TALLY_ROWS=10` alone breaks the frozen line) |
| C3-4 | the same tenth current row with first cell `research-gate extra` (no backticks) | same | `c3-tenth-tn.txt` | `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=4 SKILL_TALLY_R90=PASS` | 0 | **missed**: the claim says "first cell names `research-gate`"; `current()` requires `lstrip().startswith("| \`research-gate")` |
| C3-5 | text-only check vs the tool's verdict: tree cells 283, supplied verdict 275 | real: `skill-tally-r90.py --root <tree283> --selftest <selftest-275-fixture.txt>`; mutant: selftest block replaced by `cases, skipped = 283, 0` | `c3-textonly-real.txt`, `c3-textonly-mutant.txt`, `c3-textonly-mutant-notool.txt` | real: `STALE_TALLY PASS (283 cases, 0 skipped) != tool 275/0` ×9 / `TALLY_ROWS=9 STALE_TALLIES=9/9 EXPECTED_CASES=275 … SKILL_TALLY_R90=FAIL`; mutant: `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 … SKILL_TALLY_R90=PASS` | 1 / 0 | the real check binds the supplied tool verdict; only the literal-283 mutant is text-only |

C3 do-nothing: on the base tree `SKILL.md` still carries nine `PASS (275 cases, 0 skipped)` tallies
(`grep -c` → 9), the base tree has no `corpus/evidence/round90` instrument (`ls` → no such directory), and running the
round-90 check against the base prints `STALE_TALLIES=9/9 … SKILL_TALLY_R90=FAIL` (`c3-donothing-base.txt`, rc 1). If the
instrument is not landed, nothing in the round reports the nine stale tallies.

C3 result: the discrimination leg meets the sentence (C3-2); the tool-verdict binding is real (C3-5); the discovery rule is
narrower than the sentence for a tenth row whose first cell names `research-gate` without the backticks (C3-4) — a wording
gap, not a landing miss (the attacked tree has no tenth row and the frozen `TALLY_ROWS=9` line passes on the discrimination
tree). C3 holds with that narrowing recorded.

## Gap ledger — fixable defect vs named limit

1. **C1 command shape (fixable, spec wording).** `self_pin` resolves the driver, expectations and every receipt with
   `relpath(..., --repo)`; with the lane's driver and a separate clone the command prints `SELF_DRIFT` for all eleven
   scoring files (L4) although the four counted fields are 6/6. Smallest safe correction: freeze the command as the
   claims.md dot form (one tree), or resolve instrument/expected against `--root` and pin only receipt bytes at
   `--receipts-rev`.
2. **C1 gated-mint coverage (fixable).** The six forgery classes never pass `--repo`/`--receipts-rev`, so a driver that mints
   the pin only under the scored invocation passes both frozen commands on a carrier commit whose receipts carry no pin
   (C1-6: `SELF_PIN OK`, all four 6/6, battery 6/6). At the frozen surface the instrument sha256 pin and the fixed carrier
   revision are the enforcers, so no scored skip occurs; the counter gap is latent. Smallest safe correction: one more
   forgery leg run in the scored invocation shape against a pinless fixture carrier commit (B3 is its ungated seed).
3. **C1 duplicate header keys (fixable).** `header_fields` keeps the last value per key and `DUPLICATE_KEY` is applied only
   to body tokens; a receipt carrying a contradicting `# exit=` or `# computed_against=` is accepted (C1-8/9: PASS 6/6).
   On the frozen carrier `SELF_PIN` refuses the on-disk edit (C1-10: `SELF_DRIFT`); a duplicate committed at a substituted
   carrier would pass. Smallest safe correction: collect header values as lists and refuse a required header key
   (`case`, `exit`, `computed_against`) carried twice with different values.
4. **C2 always-pass counter (caught by design).** Only `MUTANTS_KILLED` distinguishes it (C2-2: 1/10); the frozen C2 command
   set includes the battery, so it does not pass the round. A bare stdout scorer reading only the counter's summary would
   accept it — the round's accepted design is "the battery is the detector", and it works here.
5. **C2 caller bypass (Named Limit 3, confirmed).** The bypass survives the counter (10/10), the mutants (10/10, rc 0) and
   the controls (7/7) while accepting a tree the real counter refuses (C2-4); the limit text discloses it. If the limit is
   ever to be withdrawn, the smallest correction is a control case with a non-verbatim quote (the forged tree here) that the
   counter must refuse; today no frozen fixture exercises that caller path.
6. **C3 discovery backtick (fixable, wording).** `current()` requires the backticked first-cell form; the sentence says
   "first cell names `research-gate`". A tenth stale row without backticks is unbound (C3-4: `OTHER_OCCURRENCES=4`, PASS).
   Smallest safe correction: match ``^\| *`?research-gate`` in `current()` (keeping the `Selftest `PASS (` arm), or amend
   the sentence to the backticked form.
7. **C3 text-only check (no gap).** The real check binds the supplied verdict (C3-5); a literal-283 check is a different
   instrument and is not what landed.

## Invariance (checked, read-only)

- `tools/research-gate.sh` sha256 `b23301b6dc141968edc33e838733df9cc3b3ecc2ab815e6d0acffd7efb546065` at both
  `f54a45ed…` and `9bad1201…`; `tools/gate-records.py` sha256 `905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60`
  at both — unchanged this round, as the task states.
- `git diff --stat f54a45ed… 9bad1201… -- tools/ corpus/SOURCES.md SKILL.md` → `corpus/SOURCES.md | 1 +` (one inserted
  row, S220, and its `used-by` cell; the 218→219 registry change); `SKILL.md` unchanged in that diff (the repair is
  post-wave, as the task states).
- No network this round; C3's `--selftest` is local; the clone's one-byte receipt edit was restored and
  `git -C repo status --porcelain` is clean.

## Receipts in the wave output

`.ufo/waves/round-90/w1/R90CriticClaims/`: `c1-landing-verify.txt`, `c1-landing-forgeries.txt`, `c1-lane-root.txt`,
`c1-lane-driver-other-repo.txt`, `c1-m1a-verify.txt`, `c1-m1a-forgeries.txt`, `c1-m1b-verify.txt`, `c1-m1b-forgeries.txt`,
`c1-m2-uncond-verify-pinless.txt`, `c1-m2-uncond-forgeries.txt`, `c1-m2b-gated-verify-repo.txt`,
`c1-m2b-gated-forgeries.txt`, `c1-m3-verify.txt`, `c1-m3-forgeries.txt`, `c1-m4-duphead-exit.txt`,
`c1-m4-duphead-pin.txt`, `c1-m5-dupheap-selfpin.txt`, `dn-c1-base.txt`, `c2-landing-counter.txt`,
`c2-landing-mutants.txt`, `c2-landing-controls.txt`, `c2-a-base.txt`, `c2-a-queued.txt`, `c2-b4-base.txt`,
`c2-b4-queued.txt`, `c2-b4-mutants.txt`, `c2-c-base.txt`, `c2-c-mutants.txt`, `c2-d2-real.txt`, `c2-d2-bypass.txt`,
`c2-d2-mutants.txt`, `c2-e-controls.txt`, `c2-e-controls-alwayspass.txt`, `c2-e-mutants.txt`, `dn-c2-base.txt`,
`c3-before-9bad1201.txt`,
`c3-landing-283.txt`, `c3-tenth-tb.txt`, `c3-tenth-tn.txt`, `c3-textonly-real.txt`, `c3-textonly-mutant.txt`,
`c3-textonly-mutant-notool.txt`, `c3-donothing-base.txt`, `selftest-275-fixture.txt`, `selftest-283-fixture.txt`
(the two `--selftest` fixtures are verdict-line captures: `selftest-283-fixture.txt` is the line the live tool printed in
`c3-landing-283.txt`; `selftest-275-fixture.txt` is the tool's older 275 verdict used for the text-only discrimination).
Scratch `S` is deleted before yield.

VERDICT: R90CriticClaims C1 held — the landed driver prints the claimed line at 9bad1201 (both dot-tree and lane-root forms) and the battery refuses the six classes; the fresh-only/substring/ungated-mint artefacts are caught, while gated minting and duplicate header keys survive only with substituted instrument/receipt bytes that `instrument-pins.txt` + `SELF_PIN` + the fixed carrier revision refuse (two counter-coverage gaps recorded with corrections).
VERDICT: R90CriticClaims C2 held — the counter and both batteries print the claimed lines; the constant VERDICT line is cross-checked and a fully constant counter or hardcoded witness is caught only by `MUTANTS_KILLED` (1/10, 7/10), the constant control frame by the M5 battery leg (9/10), and the surviving caller bypass is the declared Named Limit 3.
VERDICT: R90CriticClaims C3 held — the nine-cell 283 discrimination leg prints `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283`, a tenth backticked stale Gates row is caught (`10` / `1/10` / FAIL), and the one miss — a tenth current row naming `research-gate` without the backticks — is a wording narrowing of the discovery rule, not a landing miss.
