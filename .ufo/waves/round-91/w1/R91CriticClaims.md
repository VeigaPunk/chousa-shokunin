# R91CriticClaims — freeze and shared-assumption attack (round 91)

Seat: critic. Tree attacked: carrier `C3 67954adc599bd605705d94a1ea7abb582491a907`; freeze `F3
4d00d7519290569879f853d7122b82a927cda1f3`; base `265b8633b7e5d1da49da6fb948df9707373fb15c`. Scratch
`S=/fast/scratch/hyaku/chousa-r91/R91CriticClaims` (archive trees at C3, `--shared` clones at C3); every fixture
lives under `S`, none of the lane's files was edited. No tool installed, upgraded or removed this seat. No network
request was made. Receipts cited below are copied to
`.ufo/waves/round-91/w1/receipts/R91CriticClaims/` (path prefix `R:` in this report).

Findings that falsify the frozen wording: **F1 (C1 command), F2 (C1 instrument trust), F3 (C1 pin surface, clause 7)**,
**F4 (C2 silent empty-cell drop)**. One narrowing without a falsification: **F5 (C3 controls' unfrozen landing
clause)**. Six attacks were refused or held (N1–N6). All commands below were run from the named tree; the lane was
never the cwd of a mutating command.

---

## 1. Freeze integrity

**Command** (clone at C3):
```
cd S/repo && F=4d00d751…; C=67954adc…; while read -r pin path; do f=$(git show "$F:$path" | sha256sum | cut -d' ' -f1); c=$(git show "$C:$path" | sha256sum | cut -d' ' -f1); d=$(sha256sum "$path" | cut -d' ' -f1); …; done < corpus/evidence/round91/instrument-pins.txt
```
**Observed**: all 16 rows `ok` — `R:freeze_pins_f3.tsv` (one row per pin with pin / F3 blob / C3 blob / disk hash /
verdict), summary `ok 16`. The same check against each freeze's *own* pins file and blobs: F1 `160b658b` ok=16
bad=0, F2 `37831ce8` ok=16 bad=0, F3 `4d00d751` ok=16 bad=0 (`R:freeze_pins_selfcheck.txt`). So the F2→F3 re-cut did
not leave a stale pin, and each freeze is internally consistent.

**Carrier pins F3**: all six scored receipts carry `# computed_against=4d00d7519290569879f853d7122b82a927cda1f3`
(`grep -H computed_against corpus/evidence/round91/controls/receipts/*.txt`, `R:freeze_history_audit.txt`); the three
`*-before.txt` are raw evidence, not receipts. The C1 baseline verify confirms the carrier binding from git:
`RECEIPT SELF_PIN OK rev=4d00d751… receipts_rev=67954adc…` (`R:C1_baseline_verify.out`).

**Result: held** — 16/16 at F3; C3 receipts pin F3; F1/F2/F3 each self-consistent. The one integrity hole is not in
the pin *values* but in the pin *file*, reported as F3 below.

---

## 2. No-work controls

### 2.1 C1 — three falsifications, all before any scored run

**F1 (fired). The frozen counting command cannot print PASS: `--work` is required and the sentence omits it.**

**Command** (clone at C3, verbatim frozen form):
```
cd S/repo && python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . \
  --rev 4d00d7519290569879f853d7122b82a927cda1f3 --receipts-rev 67954adc599bd605705d94a1ea7abb582491a907
```
**Observed** `rc=2`:
```
control-driver-r91.py: error: the following arguments are required: --work
```
(`R:C1_literal_command.out`.) The driver declares `--work` `required=True`; `claims.md` C1, `.ufo/waves/round-91/claims.json`
(`counting_command`) and the dispatch context all print the command without it. With `--work <scratch>` the same
command prints the frozen predicate exactly: `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=6
CONTROL_DRIVER_R91=PASS`, `rc=0` (`R:C1_baseline_verify.out`). This is the same class as pre-wave repairs 1–2
(transcription narrower/wider than the instrument) and it is cheap to fix before the landing.
**Impacted axis**: C1 operability. **Smallest safe correction**: add `--work <scratch>` to the C1 statement in
`claims.md`, to `claims.json`'s `counting_command`, and to the wave context (or give `--work` a default that is not
under the tree); re-cut or amend as `C1-a`.

**F2 (fired). The predicate is satisfied by a stub at the instrument's path; the driver's own pin is never consulted
by anything but the driver.**

**Command** (clone `S/P_stub` at C3; the instrument replaced by a 3-line file that prints the predicate lines):
```
printf 'import sys\nprint("COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R91=PASS")\nprint("RECEIPT SELF_PIN OK rev=4d00d751… receipts_rev=67954adc…")\nsys.exit(0)\n' > corpus/evidence/round91/control-driver-r91.py
python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . --rev 4d00d751… --receipts-rev 67954adc… --work <scratch>
```
**Observed** `rc=0`:
```
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R91=PASS
RECEIPT SELF_PIN OK rev=4d00d7519290569879f853d7122b82a927cda1f3 receipts_rev=67954adc599bd605705d94a1ea7abb582491a907
```
while the stub's hash is `d02842ce…` and the frozen pin is `49102204…` (`R:P_stub_c1.out`; the pin row is in
`instrument-pins.txt`). Nothing in the counting command compares the instrument to its pin: `pin_report()`'s
`wanted` set is the rows' scripts plus `expected.tsv` only, and `self_pin()` — the only code that would have caught
this — is *inside the replaced file*. Named limit 1 ("a coherent joint edit of instrument, pin, receipt and
expectation row survives") does not cover this state: the pin, receipts and expectations were not edited and the pin
is inconsistent with the stub, so the edit is not coherent. K4 ("the pass skips the work") is therefore reachable
in the cheapest possible way.
**Impacted axis**: C1 operability (and, because C2/C3's counters have no pin leg of their own, the same hole covers
them — see F3/2.2).
**Smallest safe correction** (one line, from outside the instrument, using the freeze C3 already names):
`git -C . diff --quiet 4d00d751… -- corpus/evidence/round91/control-driver-r91.py corpus/evidence/round91/instrument-pins.txt`
must exit 0 before `verify`; or declare the limit "the instrument's self-report is the measurement and a replaced
instrument is outside the predicate" — which guts K4, so the external line is the honest repair.

**F3 (fired). `instrument-pins.txt` is a scoring input that is not pinned; deleting a row is invisible, and it removes
the only check on 10 of the 16 frozen files.**

**Command** (clone `S/P_trim` at C3; delete the `claims.md` row from `instrument-pins.txt`, then verify):
```
python3 - <<'EOF'  # keep all rows except the one naming claims.md
EOF
python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . --rev 4d00d751… --receipts-rev 67954adc… --work <scratch>
```
**Observed** `rc=0`:
```
RECEIPT PINS OK 6/15 pinned files byte-identical
RECEIPT SELF_PIN OK rev=4d00d7519290569879f853d7122b82a927cda1f3 receipts_rev=67954adc599bd605705d94a1ea7abb582491a907
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=6 CONTROL_DRIVER_R91=PASS
```
while `git diff --stat` shows the pins file one line shorter and its bytes differ from F3
(`git show F3:…/instrument-pins.txt | sha256sum` = `b3908ee2…`, disk = `5fbd2260…`; `R:T_pintrim2.out`). C1 clause 7
says "every scoring file is byte-identical to its blob at the base it is read from": the pins file is read from
`--root` and drives the PIN findings, yet its blob is never compared. Deleting a row drops that file from
`pin_at_rev()` for good; `pin_report()` only requires the six `wanted` files. The same edit admitted a substituted C2
counter: clone `S/P_attack` with `curation-r91.py` replaced by a stub and its pin row deleted →
C1 verify `rc=0`, `… CONTROL_DRIVER_R91=PASS`, `PINNED_FILES=6` (`R:P_attack_c1.out`) and
`python3 -B corpus/evidence/round91/curation-r91.py --root .` `rc=0` printing the full C2 field line and
`CURATION_R91=PASS` (`R:P_attack_c2.out`). Two claims' predicates reached with a non-frozen instrument.
**Impacted axes**: C1, and the freeze's cross-claim integrity (C2/C3 instruments are in the deletable ten).
**Smallest safe correction**: pass the pins path into `self_pin()` and add `(rel_for(root, pins_path), rev)` to its
`base` list (one line + signature), so the pins file is compared to its F3 blob like `expected.tsv` is; or narrow
clause 7 to the files `pin_report()` actually checks and declare the rest advisory. `C1-c`.

**N1 (neutral). r90-driver substitution with r91 receipts.**
`S/T_r90` = C3 archive + `corpus/evidence/round90/control-driver-r90.py` at the r91 path;
`… control-driver-r91.py verify --root . --repo <clone> --rev F3 --receipts-rev C3 --work <scratch>` →
`rc=1`, `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=4/6 CONTROL_DRIVER_R90=FAIL` (`R:T_r90.out`). Not
reachable. Note for the record: the r90 driver prints the *same* `COMMITTED/EXACT/PIN=6/6` counters on r91 receipts
(only `FRESH_OK` and the `R90` tag kill it), so a predicate that checked counters without the exact
`CONTROL_DRIVER_R91=PASS` token would have been reachable — the frozen predicate's tag is load-bearing, keep it.

### 2.2 C2 — one falsification

**F4 (fired). A non-`Q`, 3-cell data row in `## Located quotes` is silently dropped; every frozen field still
matches.** The row filter in `data_lines()` skips `cells[0] == ""` *and* the separator test `set(cells[0]) <=
set("-: ")` is vacuously true for an empty cell, so `q_shape_violation()`'s own `qid=<empty>` branch is unreachable
in the counter path.

**Command** (C3 archive copy; insert `| | S070 | "A phantom quote that is not a Q row and must not pass." |` after
the `|---|---|---|` separator inside `## Located quotes` of `corpus/knowledge/search-transparency-reporting-r84.md`,
line 22):
```
python3 -B corpus/evidence/round91/curation-r91.py --root .
```
**Observed** `rc=0`:
`Q_ROWS=20 Q_SHAPE_FAIL=0 … WARRANT_OK=17/17 … LEGS_MEASURED=13/13` and `CURATION_R91=PASS`
(`R:T_phantom.out`). The claim says "every data row of `## Located quotes` is a `Q<n>` row with exactly three
cells…", and the plan says "every `## Located quotes` row counted or refused with its shape named"; this row is
neither counted nor refused. The same filter hides a decision row: insert `| | do a phantom thing | never do it | Q1 |`
after the decision-table separator → `CURATION_R91=PASS` (`R:T_decphantom.out`), i.e. a decision row whose warrant
shares nothing is invisible to WARRANT/TFREQ.
**The one-line repair** (patched copy `R:curation-r91-emptyfix2.py`; change the skip to
`cells[0] in ("Situation","qid") or (cells[0] and set(cells[0]) <= set("-: "))`) makes the clean tree still PASS
(`R:fix2_T3.out`) and both phantoms FAIL with the named shape: `Q_SHAPE … qid=<empty> row=| | S070 | …`,
`Q_SHAPE_FAIL=1` (`R:fix2_T_phantom.out`), and `WARRANT_OK=17/18` (`R:fix2_T_decphantom.out`).
**Impacted axis**: C2 calibration. **Smallest safe correction**: the one-line `data_lines()` change plus a fifth
forgery (`empty-qid` row) in `curation-r91-controls.py` so the class is in the battery; mirror the decision-table
case in the same forgery tree. `C2-a`.

**N2 (neutral). Duplicate qid keeping the row count.** Change `| Q5 |` to `| Q4 |` in the r84 table (20 rows stay) →
`rc=1`, `LEG_FAIL QSHAPE … duplicate`, `Q_SHAPE_FAIL=1`, `LEG_FAIL FLOOR` (pinned qid set), `WARRANT_OK=16/17`
(`R:T_dup.out`). Refused.

### 2.3 C3 — held, one narrowing

**N4 (neutral). The ranges are derived from the tool's names, not from the prose.** Old prose at C3:
`rc=1`, `CASE_RANGE_FINDING RANGE_MISMATCH:bash-pin-override claimed=276-283 derived=282-283`,
`CASE_RANGE_OK=1/2 MISLABELED=6 indices=276,…,281`, `SKILL_TALLY_R91=FAIL` (`R:C3_baseline_oldprose.out`). Rename
`ok-case 282 bash-pin-override-missing` → `other-pin-missing` in a copy of the committed receipt: derived moves to
`283-283`, `MISLABELED=7`, `rc=1` (`R:T_c3name2.out`) — so the code reads the names, not the prose.

**N5 (neutral → held for the post-repair state).** On a C3 copy whose one clause is the repair the controls encode,
the command prints the frozen line exactly:
`TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 CASE_RANGE_BASHENV=273-275
CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2`, `SKILL_TALLY_R91=PASS`, `rc=0`
(`R:T_c3fix_tally.out`); `skill-tally-r91-controls.py --root <repaired tree> --work <scratch>` `rc=0`,
`CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1` (`R:T_c3fix_controls.out`).

**F5 (narrowing, not a falsification). The controls' precondition is prose that the freeze does not carry.** The
controls require the exact sentence `r39 bash-pin cases 273–275 (pin-bashenv, drift-bashenv) and r82 pin-override
cases 276–283, of which bash-pin-override cases 282–283` (`skill-tally-r91-controls.py:31`). That string appears
nowhere in `plans/round-91.md`, `claims.md` or `claims.json` (grep count 0 in each); at C3 the controls print
`SETUP repaired clause absent from SKILL.md — is this the landing tree?` and exit 2 (`R:C3_controls_on_C3.out`).
A landing repair that is correct but worded differently makes the C3 controls half unmeasurable at the landing,
while the tally half still passes. **Smallest safe correction**: record the exact replacement clause in
`plans/round-91.md` §C3 (or in a C3 named limit), or make the control locate the old prose via the two regexes
instead of full-sentence equality. `C3-a`.

**N6 (note, named-limit candidate).** `CASE_RE` (`^ok-case\s+(\d+)\s+(\S+)\s+exit=`) parses 277 of the receipt's 283
`ok-case` lines; six lines use `accepted=` (`ok-case 196`–`200`, `223`) and are not in the name map. Both bound
families parse, so the frozen fields hold; but "the tool's own ok-case names" is 277/283, and a future family in the
`accepted=` shape would be invisible to the derivation. Worth a C3 named limit rather than a repair.

---

## 3. Cross-claim coupling: the heading

**N3 (neutral). Renaming `## Located quotes` to `## Located Quotation` in one entry** →
`rc=1`, `Q_ROWS=7`, `Q_FLOORS=…r84.md=0/0 floor13,…`, `LEG_FAIL FLOOR`, `CURATION_R91=FAIL`
(`R:T_head.out`). The code's literal (`section_lines(text, "Located quotes")`) is the heading the sentence names,
and the FLOOR leg refuses the empty section, so an absent/renamed table cannot be silently skipped. Not exploitable.
The exploitable coupling is not the heading but the row filter (F4), which keeps the section visible while hiding a
row inside it.

---

## 4. "No scored run preceded F2" — verified, with one provenance note

**Commands**: `git log --oneline 265b8633..4d00d751`; for each commit, `git ls-tree -r --name-only <rev> --
.ufo/waves/round-91`; `git log --oneline 67954adc..master`; `git merge-base --is-ancestor 0c85c9ac 67954adc`.
**Observed** (`R:freeze_history_audit.txt`): before `37831ce8` (F2) the wave dir holds only `claims.json`
(F1 and both carriers); the wave *outputs* first appear nowhere in history through C3. No commit before F2 runs or
scores a candidate. The superseded pairs pin their own freezes (`d02a950f` receipts `computed_against=160b658b…`,
`b8fc99a1` receipts `…=37831ce8…`). **Note, not a scored-run violation**: the first dispatch payload
(`.ufo/waves/round-91/w1-dispatch.json`) was committed at `c52ccc74` (08:12:11, *before* F3 at 08:17:39) and names
`C2 b8fc99a1…` for all 12 seats; the re-render at `0c85c9ac` (after C3) names `F3/C3` and is *not* an ancestor of C3
(rc=1) — it is the tip the live seats' context matches. So the plan's "the wave is dispatched only after the F3/C3
verify prints PASS" is consistent with the payload that was used, but a complete pre-F3 dispatch artifact remains in
history and the plan does not disclose it. Recommend one line in `plans/round-91.md` (pre-wave repair 2 or an
amendment): the pre-F3 render was superseded before dispatch, as F1/C1 and F2/C2 were.

---

## 5. Ledger pre-shape for `.ufo/waves/round-91/claim-falsification.tsv`

Schema from round 89/90: `claim<TAB>artifact<TAB>verdict<TAB>narrowing<TAB>note`, one row per (claim, attack seat),
artifact relative to `.ufo/waves/round-91/`. Round 90's header named six attack seats; this wave's non-executor,
non-scout seats are **eight** — every one must appear, for every claim:

| attack seat | role | artifact expected |
|---|---|---|
| R91ReviewerC1 | reviewer | `w1/R91ReviewerC1.md` |
| R91ReviewerC2 | reviewer | `w1/R91ReviewerC2.md` |
| R91ReviewerC3 | reviewer | `w1/R91ReviewerC3.md` |
| R91CriticClaims | critic | `w1/R91CriticClaims.md` |
| R91ExecMutations | mutation-tester | `w1/R91ExecMutations.md` |
| R91SentinelScope | sentinel | `w1/R91SentinelScope.md` |
| R91ConnectorSiblings | connector | `w1/R91ConnectorSiblings.md` |
| R91RevPrior | revenger | `w1/R91RevPrior.md` |

Not attack seats, and say so in the header: `R91ExecC1Repro`, `R91ExecC2Repro`, `R91ExecC3Repro` (reproduction; a K
they fire goes to `plans/round-91.md`, as round 90 put `R90ExecC2Forge` in Amendment 8) and `R91ScoutRegistry` (pre-file
gate on `claims.json`). That is 3 claims × 8 seats = **24 rows**; a seat whose artifact does not touch a claim is
`neutral` with `-` in `narrowing`, exactly as round 90 did.

My three rows:

```
C1	w1/R91CriticClaims.md	falsifies-wording	plans/round-91.md §Amendments after the freeze (C1-a, C1-b, C1-c)	counting command omits required --work (rc=2); a stub at the instrument path prints the predicate (rc=0) while the driver's pin 49102204… is not compared; deleting a pin row leaves PASS and unbinds 10/16 pins
C2	w1/R91CriticClaims.md	falsifies-wording	plans/round-91.md §Amendments after the freeze (C2-a)	empty-first-cell data row in ## Located quotes and in the decision table is silently dropped; CLEAN passes with the phantom present; one-line data_lines() fix + fifth forgery
C3	w1/R91CriticClaims.md	neutral	plans/round-91.md §Amendments after the freeze (C3-a)	name-derived ranges confirmed (old prose CASE_RANGE_OK=1/2 MISLABELED=6; renamed name moves derived to 283-283); repaired-tree tally+controls PASS; controls' exact clause is frozen nowhere — landing must use skill-tally-r91-controls.py:31's wording or the controls half SETUPs
```

Suggested amendment pointers (the L1 chooses numbers): C1-a (add `--work <scratch>` to C1's statement and
`counting_command`), C1-b (external driver-pin line in the counting command, or an explicit named limit), C1-c (pin
the pins file in `self_pin`'s `base`), C2-a (empty-cell filter + fifth forgery), C3-a (freeze the exact repaired
clause text). These resolve in `plans/round-91.md` §Amendments after the freeze, as the ledger's `narrowing` cells
require.

---

## Findings summary

| id | claim | counterexample | evidence | correction |
|---|---|---|---|---|
| F1 | C1 | frozen command exits 2 without `--work` | `R:C1_literal_command.out` | add `--work <scratch>` to claim text + counting_command |
| F2 | C1 | 3-line stub at the instrument path prints the predicate, `rc=0`, while its hash ≠ frozen pin | `R:P_stub_c1.out` | external `git diff --quiet F3 -- driver pins` before verify |
| F3 | C1 | pins row deleted → PASS; pins file differs from F3; a stubbed C2 counter then also PASSes | `R:T_pintrim2.out`, `R:P_attack_c1.out`, `R:P_attack_c2.out` | add the pins path to `self_pin()`'s `base` |
| F4 | C2 | empty-qid located row and empty-first-cell decision row → PASS | `R:T_phantom.out`, `R:T_decphantom.out`, fix `R:fix2_T_phantom.out` | one-line `data_lines()` filter + fifth forgery |
| F5 | C3 | controls' exact repair clause is unfrozen; controls SETUP at C3 | `R:C3_controls_on_C3.out`, `R:T_c3fix_controls.out` | freeze the clause text (or derive old prose by regex) |

Neutral, with evidence: N1 r90 substitution (`R:T_r90.out`), N2 duplicate qid (`R:T_dup.out`), N3 heading rename
(`R:T_head.out`), N4 name-derived ranges (`R:C3_baseline_oldprose.out`, `R:T_c3name2.out`), N5 repaired tree
(`R:T_c3fix_tally.out`, `R:T_c3fix_controls.out`), N6 `CASE_RE` 277/283 parse (`R:freeze_history_audit.txt` section
"receipts" plus the raw receipt).

VERDICT: R91CriticClaims C1 fired — the frozen counting command exits 2 without the required `--work`, a stub at the instrument's path satisfies the predicate with the driver's own pin never consulted, and the pins file itself is unpinned so a deleted row silently unbinds 10 of 16 pins.
VERDICT: R91CriticClaims C2 fired — a non-Q data row with an empty first cell (in `## Located quotes` and in the decision table) is dropped by `data_lines()` and the counter prints PASS; a one-line filter change plus a fifth forgery closes it.
VERDICT: R91CriticClaims C3 held — on a tree with the one-clause repair the tally and controls print the frozen fields, and a renamed case moves the derived range, proving name-derivation; only the controls' exact unfrozen repair clause needs narrowing before landing.
