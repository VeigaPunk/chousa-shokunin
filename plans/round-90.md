# chousa — round 90: plan and amendments

L1 `ChousaR90`. Base `f54a45ed197dd475af50d82e43a22df3d2e99782` (round-89 landing + its non-author spot-check).
Frozen claims: `corpus/evidence/round90/claims.md` (prose) and `.ufo/waves/round-90/claims.json` (machine form the
pre-file gate reads). A `narrowing` cell in `.ufo/waves/round-90/claim-falsification.tsv` resolves to a section here.

## Inputs — round 89's routed defects and the Gate-standard item

`corpus/lessons/round-89-verifier-spotcheck.md`:

1. C2's after-line quotes an unprinted token (`VERDICT fields_hold=1`) → C2 here appends the verdict leg before the
   summary and requires the whole line.
2. Attack-share arithmetic (7/12 vs 6/12) → conformance; this round states the ledger's count.
3. Work-performed frontier bullet undercount → conformance; this round states the counts it measured.
4. Amendment 8's `LEGS_MEASURED=8/9` vs printed `8/8` → conformance; the r90 summary prints the full leg set.
5. `SKILL.md` tallies at 275 vs the tool's 283 → C3.
6. Carried debt: (a) round-74 source-blind order oracle — **not touched** (a different instrument); (b) QUALITY 173's
   successful-refused record form — **not touched**; (c) r80 backlog Gate ids — **not touched**; (d) Amendment 7's
   control-driver discipline — C1; (e) Amendment 9's detector-substitution witness — C2.
7. Named limits stay named in the frozen claims (C1 limits 1–3, C2 limits 1–4, C3 limit 1).

Cross-checked against `considerthese/2026-11-07.md` proposal 1 (the "duplicate wins" watch): the receipt driver's
`DUPLICATE_KEY` leg is that proposal applied to the receipt surface, and the `C-duplicate-key` forgery is its
witness. No other proposal is acted on.

## Claim selection

- **C1 — operability (lowest scored non-retired axis, historical 3/10).** The control-receipt driver's four
  spot-checked defects (B1–B4) plus the duplicate-key class. The subject `tools/gate-records.py` is unchanged, so no
  domain record can move; the driver verifies receipts that already exist at the base.
- **C2 — calibration.** The curation counter's verdict leg is printed on the passing path, and each detector gains a
  two-directional witness that kills the two constant-substituted detectors round 89 left alive.
- **C3 — freshness.** The `SKILL.md` self-test tallies re-derive to the tool's own selftest verdict.

Rejected as claims: a new knowledge entry (the one source opened this round grounds C1's token rule, not a domain
fact); the round-74 order oracle and the r80 Gate-id backlog (carried debt, no instrument in this round touches
them); the `S217` successful-refused record form (QUALITY 173; carried).

## Pre-freeze repairs (before the first scored run, disclosed)

1. **C1 driver emits, then verifies.** `emit` writes the receipt with a four-line header; `verify` never writes under
   the receipts directory (B1). The token leg is exact-token, with `TOKEN_DETACHED` for a key carried with a
   different value (B2). `# computed_against=` is required and checked against `--rev`, and the driver/expectation
   bytes are self-pinned at that revision while the receipts are self-pinned at their carrier commit (B3). The harm
   row requires `records>=1` and a setup negative (`exit 2`) exists (B4).
2. **C2 verdict leg order.** The `VERDICT` leg is computed and appended before the summary; `LEGS_MEASURED` counts
   the same ten legs the verdict was taken over; the passing path prints `VERDICT fields_hold=1` (Amendment 8).
3. **C2 detector functions.** `locates`, `unentailed_row`, `teaches_miss`, `dup_qid` are named functions called by
   the legs and by `witness()`, which asserts each fires and stays silent (eight assertions). The witness is part of
   `fields_hold`, so a substituted detector refuses PASS (Amendment 9).
4. **C2 controls frame.** The seven tree-forgery classes were closed by round 89, so the frame is now regression
   (both counters must refuse) and the new detection credit is the mutant battery's prior-survivor leg.
5. **C3 check runs the tool.** The tally check runs `--selftest` itself; the expected number is never a literal in the
   check.
6. **Registry id.** The new row is `S220`, not `S219`: `S219` is the round-89 control fixture's mirror-row id, and a
   real row there renames the fixture's row inside the parsed registry (measured: the r89 control battery's SUP case
   stops being accepted by r88). `S219` stays reserved to the fixture; the failed gnu.org attempt is logged under
   `S219` in `refetch.tsv` and is not a registry row.

## Freeze

`corpus/evidence/round90/claims.md`, `.ufo/waves/round-90/claims.json`, the five instruments
(`control-driver-r90.py`, `control-forgeries-r90.py`, `harm-recheck-r90.py`, `curation-r90.py`,
`curation-r90-controls.py`, `curation-r90-mutants.py`, `skill-tally-r90.py`), `controls/expected.tsv`, the before
receipts under `controls/receipts/`, `instrument-pins.txt`, the egress table and the registry change (S220 row) are
committed as the freeze, before any scored run of the round-90 candidates and before the wave.

## Amendments after the freeze

None yet. An amendment is written here only when a wave artifact falsifies a claim's stated wording (addendum §8,
Amendment 59) and names the artifact plus the narrower property that may verify, or the honest stop.

## Amendment 1 — C3's prose label for the three historical occurrences is corrected; the predicate is unchanged

**Finding.** `R90ExecC3Tally` §(c) O1: the frozen C3 prose called the unbound occurrences "round-25/32/34/37
quotes"; the three the binding regex actually sees are L186 (256 cases, a round-34 quote inside the round-25
historical paragraph), L188 (161, round-25 final) and L640 (215, round-27). No round-37 two-number quote exists in
`SKILL.md` at `9bad1201`.

**Narrowed property.** `OTHER_OCCURRENCES=3` is the measured value and the three are historical quotations of earlier
selftest states; the correct labels are round-34 / round-25 / round-27. The predicate, counter and target are
unchanged; only the prose labels are corrected here. Named limit 2 already says historical recognition is shallower
than the binding rule.

## Amendment 2 — C1's "the re-run agrees" is narrowed to exit + required tokens + predicates, not body bytes

**Finding.** `R90ExecC1Repro` Observation 1: the committed `c1-harm-setup.txt` body names its emitting work path
(`/fast/scratch/hyaku/chousa-r90/emit2/absent-tool.py`) while a fresh run names its own; the driver's fresh leg
compares exit, required tokens and predicates, so the row passes and `FRESH_OK=6/6` holds. A reading of "agrees" as
body-byte equality is false for that row.

**Narrowed property.** The fresh leg asserts agreement on the **exit code, every required token and every predicate**
— the same values the row binds — and not on body bytes. The rest of the C1 sentence is unchanged.

## Amendment 3 — C1's "six committed receipts" names the six scored rows, not every file in the directory

**Finding.** `R90ExecC1Repro` Observation 4 / `R90ExecC2Repro` Observation 3: the receipts directory holds nine
files; the six rows of `controls/expected.tsv` are the scored set and `c1-prior-driver.txt`, `c2-subst-before.txt`,
`c3-before.txt` are before-state evidence cited by `claims.md` and not verified by the driver.

**Narrowed property.** "the six committed receipts" means the six rows of `controls/expected.tsv`; the other three
files are evidence and are not driver rows. The count 6/6 and every other clause are unchanged.

## Amendment 4 — C1's header, pin and fresh clauses are narrowed to what the driver enforces

**Finding.** `R90ExecC1Forge` (fired): the scored commands print the frozen tokens at exit 0, but the same driver
accepts three states the frozen sentence reads as refused —
(a) a receipt carrying a second `# computed_against=` header line naming another tree (`header_fields()` keeps the
last value; `PIN_OK` passes), (b) a receipt carrying `# exit=1` beside `# exit=0` (same last-wins read), and
(c) a measured tree in which the row's instrument file is replaced by a 9-line stub that prints the required tokens
(`FRESH_OK=6/6`; nothing binds the instrument bytes — `instrument-pins.txt` is not read by the driver), and
(d) duplicate `# case=`/`# exit=`/`# computed_against=` headers are read last-wins, with `HEADER_CASE` firing only
when the last value differs; `EXACT_OK` is a printed count recomputed in a second pass, not a term of `passed` (the
body codes reach `passed` through `findings`). Receipts: `w1/R90ExecC1Forge/forge-fixtures.txt`, `extra-fixtures.txt`;
`w1/R90ReviewerC1` F1/F2/F6.

**Narrowed property (what verifies).** (b) The receipt's exit is the **last** `# exit=` header value and it must equal
the row's expected exit; duplicate header lines are not refused (named limit 4). (f) `# computed_against=` is read the
same way and must equal `--rev`; with `--repo`, the driver file, the expectations file and every receipt must be
byte-identical to their blobs at the named carrier revisions — the **instrument files a row executes are not pinned**
(named limit 5). (g) "the instrument re-run agrees" means agreement on the exit code, every required token and every
predicate of the byte the row's command names, not on the instrument's identity and not on body bytes (Amendments 2).
K4 is not amended: its enumerated list (missing receipt, committed receipt not read, substring token match, pin
minted in `verify`) does not include these states, so it neither fires nor is narrowed; they are named limits 4–6,
and round 91 adds the legs that refuse them.

**What this amendment does not change.** The predicate, the six rows and every printed count are unchanged; the six
forgery classes of the scored battery are all refused and the positive accepted. Round 91 owns the repairs the firing
names: refuse duplicate header keys, bind the instrument bytes a row executes to a pin, and make the `SELF_PIN OK`
message name the two revisions it used.

## Amendment 5 — C2's "die on `LEG_FAIL WITNESS`" is a statement about the committed run, not the battery's detector

**Finding.** `R90ReviewerC2` F1/F2: at the committed bytes M6/M7 print `LEG_FAIL WITNESS 7/8 bad=1`, but the mutants
battery's detector is `returncode != 0 or verdict != CURATION_R90=PASS`; a counter edit that forces the WITNESS leg ok
still yields `MUTANTS_KILLED=10/10` while the two die on `LEG_FAIL VERDICT` (**F1**, receipt
`w1/R90ReviewerC2/c2-probe-witness-leg.txt`), and a counter whose `__main__` exits 3 with no verdict scores 10/10
(**F2**, `c2-probe-crash-kill.txt`).

**Narrowed property.** The clause asserts the **observed death line in the committed battery's run** — both
substitutions print `LEG FAIL WITNESS` — and that the battery counts them as killed by a non-zero exit or a non-PASS
verdict; it does **not** assert that the battery would catch a regression which relocates the death to another leg or
a counter that crashes. The committed transcript shows all ten genuine mutants printing `CURATION_R90=FAIL`.

## Amendment 6 — C2's before-receipt is a derived survival marker, not a raw verdict line

**Finding.** `R90ReviewerC2` F4: `controls/receipts/c2-subst-before.txt` carries `SURVIVOR_PRIOR r89-subst-0 rc=0` and
`…-1 rc=0`; `grep -c 'CURATION_R89=PASS'` on it is 0. `claims.md`'s "Before" sentence lists it beside
`c2-prior-landing.txt` as if it printed the verdict.

**Narrowed property.** The before-state is: `c2-prior-landing.txt` is the raw round-89 verdict
(`CURATION_R89=PASS`, `LEGS_MEASURED=8/8`), and `c2-subst-before.txt` is the mutants battery's derived marker that the
two substitutions survive (`SURVIVOR_PRIOR … rc=0`); the raw verdict of each substituted counter is reproduced
independently by `R90ExecC2Repro` §d2. No count moves.

## Amendment 7 — C1's frozen counting command gains its required `--work`; the predicate is unchanged

**Finding.** `R90MutBattery` F1: the frozen C1 command text omits `--work`, which the driver requires
(`argparse` → exit 2, stderr "the following arguments are required: --work", no `CONTROL_DRIVER_R90` line; receipts
`R90MutBattery/c1-frozen-command-absolute.txt`, `c1-frozen-command-no-work.txt`). Supplying `--work <scratch>` runs
the same predicate and prints `CONTROL_DRIVER_R90=PASS` (`c1-base-verify-repo.txt`). This is the QUALITY 195 class
(a frozen command that needs a preparatory value must carry it).

**Corrected literal command** (this is the form the report and the receipts use):

```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin; W=/fast/scratch/hyaku/chousa-r90/work
python3 -B "$L/corpus/evidence/round90/control-driver-r90.py" verify --root "$L" --repo "$L" \
  --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a --receipts-rev 9bad12011187d114ba2c4588c5df08a21ab28145 --work "$W"
python3 -B "$L/corpus/evidence/round90/control-forgeries-r90.py" --root "$L" --work "$W" \
  --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a
```

**What this does not change.** No instrument byte, no count, no predicate. The driver's `--work` is where its fresh
re-runs write; the receipts directory is still never written.

## Amendment 8 — C2 is an honest stop: its frozen K2 fires on two tree forgeries the full kit accepts

**Finding.** `R90ExecC2Forge` F1/F2 (receipts `w1/R90ExecC2Forge/t-nonq-row-r90.txt`, `t-nonq-row-mutants2.txt`,
`t-nonq-row-controls.txt`, `t-status-rejected-r90.txt`, `t-status-rejected-mutants2.txt`,
`t-status-rejected-controls.txt`): with the committed counter, mutants and controls, both trees print the full frozen
conjunction at exit 0 — (F1) a fabricated quote row whose first cell is not a `Q\d+` id, or a `Q`-id row with a
fourth cell, is dropped by the width/qid filter before counting, so a fabricated quote appears in no capture yet
`QUOTES_LOCATED=20/20`; (F2) flipping a cited source's registry status `mined` → `rejected` leaves every field and
every leg unchanged because only the supersession block reads `status`.

**Ruling.** C2's frozen kill rule K2 says "a tree forgery is accepted" kills the claim. Both are tree forgeries in
the claim's subject (the calibration counter's discrimination), and the full three-command kit accepts them. The
claim therefore **does not verify as frozen** — an honest stop, not a narrowed pass: a kill rule is not a wording
clause and cannot be rewritten after a seat has scored (§9). The deliverable is this narrowing: the enforceable
property of the round-90 counter is the printed fields plus the seven listed tree-forgery classes; it does **not**
refuse a quote row outside the parser's shape or a status flip on a cited source. Round 91 owns the repairs: count
every row in `## Located quotes` (or refuse a non-`Q`/non-3-cell row explicitly), cross-check every citation's
`status` and `used-by`, and re-derive the warrant share with a term-frequency guard.

## Amendment 9 — C1's named limits 4–6 record the accepted states the wave measured

**Finding.** `R90ExecC1Forge` (duplicate `# computed_against=`/`# exit=` headers accepted, instrument bytes
unpinned) and `R90MutBattery` F2/F3 (the one-point mutants `fresh-no-compare` and `empty-body-ok` survive the frozen
fixture set: no committed receipt passes while its fresh re-run disagrees, and no fixture carries an empty body;
targeted fixtures distinguish them, but those are not in the frozen set).

**Limits added.** (4) Header keys are last-wins: a receipt with two `# exit=` or two `# computed_against=` lines is
read by its last value and the duplicate is not refused. (5) The instrument files a row executes are not pinned; a
substituted instrument that prints the required tokens passes the fresh leg. (6) The claim's detector is the frozen
fixture set (six committed rows plus six forgery classes plus the positive), not a mutant battery: a driver edit that
makes the fresh comparison vacuous or accepts an empty body is invisible to it.

## Amendment 10 — C3's landing-revision PASS does not bind the expected number without its before leg

**Finding.** `R90MutBattery` C3 mutant `expected-count-read-from-file`: reading `EXPECTED_CASES` from `SKILL.md`
instead of the tool's verdict leaves the 283-tree PASS identical to baseline (`EXPECTED_CASES=283`), and is killed
only by the 275-tree before-state leg (`STALE_TALLIES=0/9 … PASS` against the frozen `9/9 … FAIL`). The claim's
`EXPECTED_CASES=283` clause is therefore bound by the pair of runs (before + landing), not by the landing run alone.

**Narrowed property.** The clause verifies over the frozen before-receipt pair: the before-state must print
`STALE_TALLIES=9/9 EXPECTED_CASES=283` and the landing run `STALE_TALLIES=0/9`. A single landing run is not
sufficient evidence for the expected-number clause.
