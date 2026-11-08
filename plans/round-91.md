# chousa — round 91: plan and amendments

L1 `ChousaR91`. Base `265b8633b7e5d1da49da6fb948df9707373fb15c` (round-90 landing + its non-author spot-check at
`265b8633`). Frozen claims: `corpus/evidence/round91/claims.md` (prose) and `.ufo/waves/round-91/claims.json`
(machine form the pre-file gate reads). A `narrowing` cell in `.ufo/waves/round-91/claim-falsification.tsv` resolves
to a section here.

## Inputs — round 90's routed defects and the SCORECARD r91 plan

`corpus/lessons/round-90-verifier-spotcheck.md` §Routed defects:

1. C2 reclaim: count every `## Located quotes` row (or refuse a non-`Q`/non-3-cell row explicitly), cross-check
   every cited source's `status`/`used-by`, and guard the warrant share with a term-frequency test → **C2**.
2. C1 residues: refuse duplicate header keys, bind the instrument bytes a row executes to a pin, make `SELF_PIN`
   name both revisions, add fixtures for fresh-divergence and empty-body (M6/M8), repair the `--root`/`--repo` path
   base (QUALITY 202) → **C1** (the two fixture classes land as `INSTRUMENT_PIN_MISMATCH` and `MISSING_HEADER`
   battery cases; a fresh-divergence case is not one of the six surviving forgery classes measured below).
3. Harm row is a self-comparison: give the sweep a base-versus-head delta that can fail → **C1** (`c1-harm` now
   reads `tools/gate-records.py` from the frozen base `265b8633`, not `master`).
4. Ledger classification and 5. freeze-pin plan entry → conformance; this round's ledger names each amendment by
   number and this plan records the freeze-pin state.
6. Citation precision → conformance; every before-line below names the receipt that carries the string.
7. Clause (a) is per row → named limit in C1.

`SCORECARD.md` §Planned — round 91: (1) operability — the C1 residues; (2) calibration — the C2 repairs and a
successor claim that names the classes; (3) freshness — bind the case-range prose to the tool's own case names and
delete the r90 unentailed double-count loop. The loop deletion is C2's instrument (R4 below); C3 carries the prose
binding.

Opened this round as a source: **S070 re-opened** (the installed `sha256sum(1)` page, `93c17dff…` bytes, quote
"Print or check SHA256 (256-bit) checksums.") grounds C1's digest-pin rule; the planned new row S221 (the IR
textbook's document-frequency definition) was attempted once and failed (`curl rc 28`, no bytes, `refetch.tsv` row
`S221 … 28 000 - -`), so no S221 row is written. One sourced claim: C1 cites S070.

`considerthese/2026-11-07.md` proposal 1 (the duplicate-wins watch) was applied in round 90 to body keys; this round
applies it to the receipt HEADER surface (C1 R1) and to the `## Located quotes` row shape (C2 R1). No other
proposal is acted on.

## Claim selection

- **C1 — operability (lowest scored non-retired axis, historical 3/10).** `corpus/evidence/round91/control-driver-r91.py`:
  duplicate header keys refused, `# expected_exit=` required and checked, every executed instrument and the
  expectations file pinned in `instrument-pins.txt` and verified on disk and at `--rev`, `SELF_PIN` names both
  revisions, unscored receipts refused, and the `--root`/`--repo` bases separated (QUALITY 202). The subject tools
  the rows execute are unchanged; no domain record can move.
- **C2 — calibration.** `corpus/evidence/round91/curation-r91.py`: every Located-quotes row counted or refused with
  its shape named; every cited source's `status`/`used-by` read; the warrant share guarded by a document-frequency
  test over the entry's own units (`DF_MAX=3`, measured); the unentailed double-count loop replaced by one record
  per offending (row, term).
- **C3 — freshness.** `corpus/evidence/round91/skill-tally-r91.py`: the `SKILL.md` case-range prose is derived from
  the tool's own `ok-case` names — the `bash-pin-override` family is 282–283, not the prose's 276–283, and the
  `r39 bash-pin` clause is the `bashenv` family 273–275. The repair is the one-clause SKILL.md edit.

Rejected as claims: a new knowledge entry (the one source opened this round grounds C1's digest rule, not a domain
fact — the attempted S221 row failed to fetch); the round-74 order oracle, QUALITY 173's record form and the r80
Gate-id backlog (carried debt, no instrument in this round touches them).

## Pre-freeze repairs (before the first scored run, disclosed)

1. **C1 header surface.** `header_multi()` returns every value per key; `check_headers()` requires exactly one
   `case`, `expected_exit`, `exit` and `computed_against`, each carrying the row's value (R1/R2).
2. **C1 pin surface.** `pin_report()` reads `instrument-pins.txt`, resolves each row's executed script and the
   expectations file against `--root`, and requires the pin to equal the on-disk sha256; `self_pin()` also checks
   every pinned blob at `--rev` and prints both revisions (R3/R4/R5). `pin_report()` is only required in `verify`;
   `emit` mints no pin.
3. **C1 battery.** `control-forgeries-r91.py` builds a two-row fixture and six forgeries (duplicate exit header,
   duplicate pin header, instrument stub, relaxed expectations, missing `expected_exit`, unscored receipt), runs
   the unchanged r90 driver on each (must accept) and r91 (must refuse), and keeps a positive control.
4. **C2 shape surface.** `q_shape_violation()` is a named detector; a non-`Q`/non-3-cell/empty-source/empty-quote/
   duplicate-qid row is a `QSHAPE` finding instead of a silent `continue` (R1).
5. **C2 source surface.** `source_link()` reads the cited row's `status` and `used-by`; every located quote's source
   must be `mined` and must name the entry (R2).
6. **C2 warrant surface.** The TFREQ documents are the entry's located quotes plus its decision rows' Do/Never
   cells; a shared term counts only at document frequency `<= DF_MAX` (R3). `DF_MAX` is measured, not chosen:
   the legitimate rows' selected terms are at most 3 (`source` alone reaches 7 and is no warrant).
7. **C2 loop.** `unentailed_terms()` returns the list; the caller appends one record per term with the term the row
   carries (R4).
8. **C1 harm row.** `controls/expected.tsv`'s `c1-harm` reads the base tool from `265b8633`, so the sweep compares
   the frozen base tool with the landed tool (routed defect 3).
9. **C3.** `skill-tally-r91.py` adds `CASE-RANGE`; the SKILL.md clause is repaired at the landing, not at the
   freeze, so the freeze tree still shows the defect (`MISLABELED=6`, `CASE_RANGE_OK=1/2`).

## Freeze

`corpus/evidence/round91/claims.md`, `.ufo/waves/round-91/claims.json`, the six instruments
(`control-driver-r91.py`, `control-forgeries-r91.py`, `curation-r91.py`, `curation-r91-controls.py`,
`skill-tally-r91.py`, `controls/selftest-r91.txt` receipt), `controls/expected.tsv`, the before receipts under
`controls/receipts/`, `instrument-pins.txt` and `corpus/evidence/round91/egress.tsv` are committed as the freeze,
before any scored run of the round-91 candidates and before the wave. The receipts are emitted at the freeze
revision and carried by the next commit (the carrier); `--rev` names the freeze and `--receipts-rev` the carrier.

## Pre-wave freeze repair 1 (2026-11-08, before any scored run and before the wave)

`F` = `160b658bffa2d2bee8bbf469537f1e512b6712c5` and `C` = `d02a950f0f22a79dd0898a4ea463550ee6dc407f` are
superseded and stay in history. Two defects were measured by the first emit/verify against `F` and fixed before the
wave:

1. `controls/expected.tsv`'s `c1-harm-setup` row omitted `--repo`, so argparse exited 2 before the tool printed
   `HARM_RECHECK_ERROR` (the round-90 row carries `--repo`; this round's transcription dropped it). The instrument
   is unchanged; the row now names `--repo @ROOT@`.
2. `UNSCORED_RECEIPT` flagged every raw `.txt` evidence file in the receipts directory. A file is an unscored
   receipt only when it carries a `# case=` header; the six forged classes'receipt still does, and the before
   receipts do not. The `extra-receipt` forgery remains refused.

The freeze is re-cut as `F2` (this commit) and the receipts re-emitted at `F2` as carrier `C2`. No scored run of a
candidate preceded `F2`; the wave is dispatched only after the `F2`/`C2` verify prints `CONTROL_DRIVER_R91=PASS`.

## Pre-wave freeze repair 2 (2026-11-08, before any scored run and before the wave)

Two clauses of C1's sentence were wider than the code, found by reading the code against the sentence before the
wave (no seat had scored anything):

1. "every file a row's command names as its script" -> "the first file each row's command names as its script". The
   driver's `instrument_rel()` takes the first `.py`/`.sh` token; C1's named limit 3 already says a second unpinned
   script is not seen.
2. "a `.txt` receipt that no expected row scores" -> "a `.txt` file that parses as a receipt (a `# case=` header)
   and that no expected row scores" — the R6 repair after freeze attempt 1 made the header the parse test.

The predicate, counters and kill rules are unchanged. The freeze is re-cut as `F3`/`C3`; `F2`/`C2` stay in history,
and the wave is dispatched only after the `F3`/`C3` verify prints `CONTROL_DRIVER_R91=PASS`.

## Amendments after the freeze

### Amendment 23 — C3 binds two families; the clause's "r82 pin-override cases 276–283" is provenance prose

**Finding.** `R91SentinelScope` F-3: the repaired landing clause reads "… r82 pin-override cases 276–283, of which
bash-pin-override cases 282–283". The counter binds `bashenv` (273–275) and `bash-pin-override` (282–283); the block
range 276–283 and its label are not derived, and a reader cannot tell the block range is unbound.

**Narrowed property.** "The two case-range clauses" are the `r39 bash-pin` family (273–275, names carry `bashenv`) and
the `bash-pin-override` family (282–283, name prefix). The r82 block range is provenance prose, unbound; a r92 repair
adds a third regex over the r82 block (`pin-env-fn`, `env-pin-override`, `pin-bash-path`, `bash-pin-override`) with its
derived family {279, 280, 282, 283}. The landing clause is the frozen controls' `OLD_CLAUSE` and is not edited after
the freeze.

### Amendment 24 — C3's selftest receipt is pinned by the external pre-step, not by `pin_report`

**Finding.** `R91SentinelScope` F-2: `controls/selftest-r91.txt` is listed in `instrument-pins.txt` but is not in
`pin_report()`'s wanted set (the six row scripts plus the expectations file); its on-disk integrity is checked by
Amendment 10's `git diff --quiet F3` pre-step and by `self_pin()` at `--rev`.

**Narrowed property.** The receipt's bytes are bound by the external pre-step and the at-rev pin, not by the driver's
on-disk pin leg; adding it to the on-disk set is a routed r92 repair.


### Amendment 22 — `read_pins()` is last-wins on a duplicated path

**Finding.** `R91ConnectorSiblings` (C1 line): `read_pins()` assigns `pins[path] = sha` per line, so a file listed
twice with different digests keeps the last row and no finding is printed — the same duplicate-wins class C1 R1
closes for receipt headers, now on the pin table.

**Narrowed property.** The pin table is read as a mapping from path to one digest; a duplicated path is outside the
claim's clause 5 (which says a file "is listed", not that it is listed once) and is a routed r92 repair (refuse a
duplicate path row, `PIN_DUPLICATE`), together with Amendment 10's self-pin of the pins file.


### Amendment 15 — C1 clause 1's ordering is per row; SELF_PIN is the cross-row protection

**Finding.** `R91ReviewerC1` F3: verify reads row `i`'s receipt and then runs row `i`'s instrument in the same
iteration, so row 2..n are read after row 1's fresh run. With `--repo`, a row's fresh command that rewrites another
receipt is caught by `SELF_PIN` (A10b) or leaves `EXACT_OK=1/2` (A10a, not gated); **without `--repo`**, the overwritten
committed receipt is never read and the run still prints `CONTROL_DRIVER_R91=PASS` (A10c).

**Narrowed property.** Each row's receipt is read from disk immediately before **that row's** fresh run; the driver
itself writes only under `--work`. The cross-row protection is `SELF_PIN` with `--repo`, which compares every
`receipts/*.txt` to its blob at `--receipts-rev` after the fresh legs. Without `--repo` the ordering is not
guaranteed; C1's command carries `--repo .`.

### Amendment 16 — C1 clause 2's "header line" is a column-0 line beginning `# `

**Finding.** `R91ReviewerC1` F8: `header_multi()` treats only lines that begin `# ` at column 0 as headers; an indented
`  # exit=1` is body text, so a duplicate header hidden with indentation is not a `HEADER_DUPLICATE`.

**Narrowed property.** A header line is a line that begins `# ` at column 0; an indented `#` line is body content and
is outside clause 2 (routed r92 repair: strip leading whitespace before the header test).

### Amendment 17 — C1 clause 5's pin rule is lexical, not "the executed script"

**Finding.** `R91ReviewerC1` F4/A13: `instrument_rel()` returns the first whitespace token that, after `@ROOT@`
substitution, is absolute and ends `.py`/`.sh` — whether it is executed, a data operand or a redirect target. A row
`cat @ROOT@/data.py && bash @ROOT@/real.sh` pins `data.py`; a same-output stub at `real.sh` still prints PASS. A script
without a `.py`/`.sh` suffix is `INSTRUMENT_UNPINNED` even when listed (A5).

**Narrowed property.** The pinned file is the **first whitespace token** in the row's instrument that becomes absolute
after `@ROOT@` substitution and ends `.py` or `.sh`; the executed script can be unpinned when such a data operand
precedes it (named limit 3 is extended to that state), and a script token without either suffix is
`INSTRUMENT_UNPINNED`.

### Amendment 18 — C1 clause 6's unscored test is the literal substring `# case=`

**Finding.** `R91ReviewerC1` F5: the driver tests `"# case=" in body`, not a parsed header; a file whose body mentions
the string in a code block is treated as a receipt.

**Narrowed property.** A `.txt` file is treated as a receipt when its text contains the literal substring `# case=`;
that is the parse test.

### Amendment 19 — C1's value equality is numeric, not string

**Finding.** `R91ReviewerC1` F9: exit/pin values are matched with `-?[0-9]+` and compared as integers, so `00` and
`-0` are accepted and `+0` is refused (`EXIT_MISMATCH`).

**Narrowed property.** "Its value equals the row's" means numeric equality under the `-?[0-9]+` grammar; a leading
`+`, a space or a non-ASCII digit is refused.

### Amendment 20 — C1's `CONTROL_DRIVER_R91=PASS` is not gated on `EXACT_OK` inside the driver

**Finding.** `R91ReviewerC1` F2: `passed` does not include `exact_only == len(rows)`, so a run can print `EXACT_OK=1/2`
beside `PASS` (A10a). The frozen predicate itself lists `EXACT_OK=6/6` among the required printed fields, so the
claim's check is external and holds; the internal gate is a routed r92 repair.

**Narrowed property.** The claim's after-state is the printed field set, `EXACT_OK=6/6` included; `PASS` alone is not
the claim. The driver's internal `passed` not reading that counter is a named limit and a routed repair.

### Amendment 21 — C1's external pre-step includes the r90 prior driver and the battery

**Finding.** `R91ReviewerC1` F7: clause 8's "the unchanged r90 driver" is asserted, not enforced — the battery runs
`../round90/control-driver-r90.py` and no pin covers it.

**Narrowed property.** The external pre-step of Amendment 10 covers the r91 instruments, the battery, the pins file,
`controls/expected.tsv` **and** `corpus/evidence/round90/control-driver-r90.py`; with that pre-step, "unchanged" is
checked before the battery runs.


### Amendment 10 — the instrument's own bytes are checked outside the driver; the pins file is not self-pinned

**Finding.** `R91CriticClaims` F2: replacing `control-driver-r91.py` with a three-line stub that prints the predicate
gives `CONTROL_DRIVER_R91=PASS`, exit 0, while the frozen pin is `49102204…` and the stub's hash is `d02842ce…`
(`R:P_stub_c1.out`). F3: deleting the `instrument-pins.txt` row for a file removes it from `pin_at_rev()`, and the
driver still prints `PASS` with `PINS OK 6/15` (`R:T_pintrim2.out`, `R:P_attack_c1.out`). The driver cannot certify
its own bytes, and the pins file is an input it never compares. This is the epistemic limit of every counter whose
predicate is its own output.

**Narrowed property.** The measurement procedure carries the external check its predicate needs: before each scored run,
`git -C . diff --quiet F3 -- <the claim's six instruments, its controls, the selftest receipt, instrument-pins.txt,
controls/expected.tsv and corpus/evidence/round90/control-driver-r90.py>` must exit 0, and
`git -C . diff --quiet C3 -- corpus/evidence/round91/controls/receipts` must exit 0. With
that pre-step, a substituted instrument or a trimmed pins file is outside the predicate; the driver's own clause 7
covers the six files `pin_report()` checks plus the driver, expectations and receipts, and names the pins file as
covered by the external pre-step (not by the driver). The amendment adds the pre-step to the counting procedure; the
predicate's tokens, targets and kill rules are unchanged.

### Amendment 11 — C3 named limit 1: a prefix-preserving rename is invisible

**Finding.** `R91ReviewerC3` probe 2e: renaming `ok-case 282 bash-pin-override-missing` to
`bash-pin-override-renamed` leaves `CASE_RANGE_BASH_PIN=282-283`, `MISLABELED=0`, PASS (`…/p2e-rename-only.txt`); a
renumber (2c) and an out-of-span family addition (2a) are refused.

**Narrowed property.** The binding is the family predicate (`bashenv` substring; `bash-pin-override` prefix) and the
family's min/max index; a rename that preserves the family token changes nothing, a rename that removes it or a
renumber changes the binding. Named limit 1 is corrected to that statement.

### Amendment 12 — C3's clause binding is the first matching occurrence in SKILL.md, not the Gates row

**Finding.** `R91ReviewerC3` probe 3/p6: the regexes search the whole document. A document whose Gates-row clause is
absent but which carries `bash-pin-override cases 282–283` in a prepended historical line prints
`CASE_RANGE_OK=2/2 MISLABELED=0`, exit 0; a document with no occurrence anywhere prints `CLAUSE_MISSING` and fails
(`…/p3-absent.txt`, `…/p6-absent-row-quote.txt`).

**Narrowed property.** The two clauses are the **first occurrence** of each phrase in `SKILL.md`; row-scoped binding
is a routed r92 repair (read the Gates-table cell only). K4's "an absent clause" is the no-occurrence state, which
fails; a phrase carried elsewhere is a scope gap in the sentence, not a tolerated absence.

### Amendment 13 — C3's `OTHER_OCCURRENCES=3` is a landing-state value, not a refusal the counter enforces

**Finding.** `R91ReviewerC3` probe 4b: deleting one historical quotation prints `OTHER_OCCURRENCES=2` and still exits
0 with `SKILL_TALLY_R91=PASS` (`…/p4b-hist-delete.txt`). K3 is written as a condition on the landing tree ("a
historical tally or quote moves (OTHER_OCCURRENCES=3 unchanged…"), not as a counter refusal. The frozen line is
enforced by the claim's printed value, and the r92 repair can pin the historical multiset.

**Narrowed property.** K3 is a condition on the landing revision: `OTHER_OCCURRENCES=3` and the diff touches only the
one clause. A forged tree that deletes a historical quotation is outside the claim; the counter is not claimed to
refuse it.

### Amendment 14 — C2's witness count covers five detectors, not `source_link`

**Finding.** `R91ReviewerC2` F3b: `DETECTOR_WITNESS=11/11` is 11 assertions over `locates`, `unentailed_terms`,
`teaches_miss`, `dup_qid` and `q_shape_violation`; `source_link` (the R2 repair's predicate, and the detector F3
falsifies) has no two-directional assertion.

**Narrowed property.** The printed `11/11` is true of the five detectors it names; the claim does not assert that
`source_link` is witnessed, and the missing assertions are a routed r92 repair together with the tokenised `used-by`
match of Amendment 2.


### Amendment 9 — the dual-base form is asymmetric: the driver must be read from `--root`

**Finding.** `R91ExecC1Repro` F1: `verify --root <lane> --repo <clone>` prints `CONTROL_DRIVER_R91=FAIL` when the
**driver is executed from the clone** (`--expected`/`--receipts` default to the clone's `HERE`, and `rel_for(lane, …)`
produces root-escaping `../../..` paths → `INSTRUMENT_UNPINNED` + `SELF_DRIFT`; `receipts/a-verify-…`, F1 lines). The
same triple prints PASS when the driver is executed from the `--root` tree (my own run at F3/C3, 35 s, PASS). So the
QUALITY-202 repair is half-closed: reads and pins are separated, but the instrument's own location must be inside
`--root`.

**Narrowed property.** The report's path-base item means: with `--root` and `--repo` distinct, a driver **read from
`--root`** resolves every scoring path against the base it reads from and passes on correct bytes; a driver executed
from `--repo` while `--root` is elsewhere is outside the claim and is a routed r92 repair (`--expected`, `--receipts`
and `__file__` should resolve against the base they are read from, not against the driver's own location). C1's own
command is `--root . --repo .` inside one tree and is unaffected.


### Amendment 1 — C2 item 1's "every data row" excludes the rows the shared first-cell filter drops

**Finding.** `R91ReviewerC2` F1/§Answer table item 1: a pipe-leading row inside `## Located quotes` whose first cell is
empty, `:`, or `Situation` is skipped by `data_lines()` before `q_shape_violation()` runs, so the tree prints
`Q_SHAPE_FAIL=0` and `CURATION_R91=PASS` (`probe-firstcell.txt`, `probe-A1-A10.txt`, three injected rows). The claim
read "every data row", which those rows satisfy. Inherited from r90; K4's "a non-`Q` row is dropped" is the named class.

**Narrowed property.** QSHAPE covers every pipe-leading line of the section **whose first cell is not the literal header
token `qid`, not empty, not `Situation`, and not composed only of `-`/`:` characters**; a row the header/separator filter
drops is outside the claim and is a routed repair (r92: let every other pipe-leading line reach the shape check). The
count and every other clause are unchanged.

### Amendment 2 — C2 item 2's "names the entry" is the substring test the counter runs

**Finding.** `R91ReviewerC2` F3: `source_link()` accepts the cell when the entry's **basename or repo-relative path occurs
as a substring** of the free-text `used-by` cell. A sibling path with the same basename (`corpus/knowledge/stale/provenance-recording-r85.md`)
and a negated sentence (`not used in provenance-recording-r85.md`) both print `USED_BY_OK=20/20` (`probe-A3-prior.txt`).

**Narrowed property.** SOURCE requires `status=mined` and the entry's basename or repo-relative path to occur in the
`used-by` cell as a substring; tokenising the cell and matching a whole path is a routed repair. The count 20/20 is
unchanged on the routed entries.

### Amendment 3 — C2 item 4's unit is (row, term) and its scope is 4-cell decision rows

**Finding.** `R91ReviewerC2` F2/F6/F7: a decision row of width ≠ 4 is dropped by `table_rows(..., 4)` before
`unentailed_terms()` runs (a 5-cell row carrying both defect terms prints `UNENTAILED_TERM=0`, `CURATION_R91=PASS`), a
row carrying both terms appends **two** records each labelled with its own term (`UNENTAILED_TERM=2`), and the detector
reads the Do/Never cells only (a term in the Situation cell is invisible). `witness()` has no two-term case.

**Narrowed property.** The UNENTAILED leg appends one record per **(row, term)** for the terms the row's **Do and Never**
cells carry and its entry's quotes do not, over **4-cell decision rows**; a row of another width or a term in another cell
is outside the claim and is a routed repair (r92: pin the decision-row width/count per entry and extend the witness). The
single-term probe's `UNENTAILED_TERM=1` is unchanged.

### Amendment 4 — C2 item 5's "df 7" is corrected to the measured df 5

**Finding.** `R91ReviewerC2` F4: under the counter's own documents (13 located quotes + 11 decision rows = 24 for the r84
entry), `df(source) = 5`, not 7; `df(resource) = 8`, not 6/20 (the 6/20 figure counts quotes only). The predicate
(`df > DF_MAX=3` → TFREQ fails) is unchanged and still discriminates: the `source`-only warrant prints
`LEG_FAIL TFREQ 16/17 max_df=3<=3` with `WARRANT_OK=17/17` (`probe-A4p-A5p-prior.txt`).

**Narrowed property.** The forgery shares only `source`, whose measured document frequency over the counter's 24 units
is **5**, above `DF_MAX=3`. The instrument's docstring text ("df 7", "6/20") is stale and is corrected in the r92
successor, not in these frozen bytes.

### Amendment 5 — C2 item 3's "every decision row" is measured over the rows whose qids all resolve

**Finding.** `R91ReviewerC2` F5: `tfreq_total` counts only rows whose cited qids all resolve (`len(resolved) == len(qids)`);
a row citing `Q99` prints `TFREQ_OK=16/16` and `WARRANT_OK=16/17`, and WARRANT fails the tree. On the clean tree the
denominator is 17 = 11 + 6, so the frozen `TFREQ_OK=17/17` is honest at landing.

**Narrowed property.** TFREQ requires every decision row **whose cited qids all resolve** to share a term at
`df <= DF_MAX`; a row with an unresolved qid is caught by WARRANT, not TFREQ. The count on the clean tree is unchanged.

### Amendment 6 — C2 item 1's scope is every pipe-leading line, after the filter of Amendment 1

**Finding.** `R91ReviewerC2` F8: a prose line beginning with `|` inside the section is counted and refused (`Q_SHAPE …
cells=1`, exit 1), i.e. the code is stricter than "data row" in that direction.

**Narrowed property.** "Every data row" means every pipe-leading line the filter of Amendment 1 does not drop; the
stricter prose-line case is the code's behaviour and is not a claim of a different scope.

### Amendment 7 — C1's counting command carries its required `--work`

**Finding.** `R91ExecMutations` F1: the frozen `claims.md`/`claims.json` C1 command omits `--work`, so run verbatim it
prints `CONTROL_DRIVER_R91=SETUP` and exits 2 (`c1-claim-literal.log`); the executable form with `--work <scratch>`
prints the frozen line at exit 0 (`c1-base.log`). This is QUALITY 195's class repeating.

**Narrowed property.** C1's counting command is
`python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . --work <scratch> --rev F3 --receipts-rev C3`.
The predicate, target and kill rules are unchanged.

### Amendment 8 — C3's controls and counter are scored at the landing revision, not at C3

**Finding.** `R91ExecMutations` (C3) and `R91RevPrior` F2: on pristine C3 bytes the C3 counter prints
`CASE_RANGE_OK=1/2 MISLABELED=6` (the repair lands after the wave, as the claim's "at the landing revision" and the plan
state) and `skill-tally-r91-controls.py --root <carrier>` exits 2 `SETUP` because its `OLD_CLAUSE` pattern is absent.
Both are expected by the claim's own revision clause; neither is a predicate failure.

**Narrowed property.** The C3 predicate and its controls are scored at the landing revision, which carries the one-clause
repair; on the carrier the counter's FAIL and the controls' SETUP are the documented pre-landing state.

An amendment is written here only when a wave artifact falsifies a claim's stated wording (addendum §8,
Amendment 59) and names the artifact plus the narrower property that may verify, or the honest stop.
