# R91RevPrior — round-91 before-state, independently reproduced

Seat `R91RevPrior` (leaf, round 91 wave 1). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Scratch `S=/fast/scratch/hyaku/chousa-r91/R91RevPrior` (created with `mkdir -p`, deleted before yield). No
production edits, no commits, no lane/fleet mutation, no subagents, no network, no sudo; no tool installed or
upgraded this round (python3 3.14.8 / git / coreutils were sufficient). Every run below reads committed bytes
from two `git clone --shared` copies:

- base `S/base`   — `git -C S/base checkout 265b8633b7e5d1da49da6fb948df9707373fb15c`, toplevel `= S/base`, clean;
- carrier `S/carrier` — `git -C S/carrier checkout 67954adc599bd605705d94a1ea7abb582491a907`, toplevel `= S/carrier`, clean.

Receipts for every command below are in
`.ufo/waves/round-91/w1/receipts/R91RevPrior/` (this report names them per finding). `commands.txt` in that
folder is the command→receipt→exit index.

## Pins the reproduction rests on (`receipts/R91RevPrior/pins-and-blobs.txt`)

Blob equality, base `265b8633…` vs carrier `67954adc…` (`git rev-parse <rev>:<path>`, both trees checked out):

| path | blob | base vs carrier |
|---|---|---|
| `corpus/evidence/round90/control-driver-r90.py` | `6f5118b39edb9787f54a9746899ad04acb9209d6` | SAME |
| `corpus/evidence/round90/curation-r90.py` | `fb7c4fac8049e8e8ab78f2a01e198fd420655530` | SAME |
| `corpus/evidence/round90/skill-tally-r90.py` | `b4973b7994817f743e89fcff7ac5666d5e3c35fe` | SAME |
| `corpus/evidence/round90/curation-r90-controls.py` | `06f66aa19d2f72b20e728f6a0c66fc8c09dea067` | SAME |
| `tools/research-gate.sh` | `3a4eabeb1e6f54445f36a4f547004bf1a5beaa52` | SAME |
| `tools/gate-records.py` | `dc7a4176129a42dc711ae62ceb72ba281fc5595d` | SAME |
| `SKILL.md` | `2506f84051022c50609277866c4c255629740cac` | SAME |

`ls S/base/corpus/evidence/round91` → `No such file or directory`: the whole round-91 instrument set is an
addition at the freeze, so every "before" run below is the unchanged r90 instrument reading committed bytes with
the round-91 arms (batteries / selftest receipt) supplied as separate committed files — the same arrangement the
frozen batteries use. `git status --porcelain` printed nothing in either clone after all runs; the batteries
wrote only under `S/`.

## (a) C1 before — the round-90 driver accepts all six forged classes

### a1. The frozen battery, run from the carrier clone

```
$ cd S/carrier && python3 -B corpus/evidence/round91/control-forgeries-r91.py --work S/forge
rc=0
```
Receipt `receipts/R91RevPrior/c1-forgeries.txt`; observed, all eight lines:

```
OK dup-header-exit: r91 rc=1 (HEADER_DUPLICATE:exit), r90 rc=0
OK dup-header-computed: r91 rc=1 (HEADER_DUPLICATE:computed_against), r90 rc=0
OK instrument-stub: r91 rc=1 (INSTRUMENT_PIN_MISMATCH:fx-tool.sh), r90 rc=0
OK expected-swap: r91 rc=1 (INSTRUMENT_PIN_MISMATCH:expected.tsv), r90 rc=0
OK missing-expected_exit: r91 rc=1 (MISSING_HEADER:expected_exit), r90 rc=0
OK extra-receipt: r91 rc=1 (UNSCORED_RECEIPT), r90 rc=0
OK positive: r90 rc=0 r91 rc=0
FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass
```

The fixture the battery builds (`S/forge/`) is a two-row tree (`fx-one` runs `fx-tool.sh`, `fx-two` runs
`fx-two.sh`); r91 `emit` writes the receipts at `--rev 265b8633…`, and the battery applies one mutation per tree:
duplicate `# exit=1` before `# exit=0`; duplicate `# computed_against=` (zero-rev first); a substituted
`fx-tool.sh` with identical output; a relaxed `expected.tsv` (`NUM>=1`→`NUM>=0`); the `# expected_exit=` header
deleted; and an extra `fx-extra.txt` receipt that no expected row scores.

### a2. r90's acceptance is a genuine PASS, not only rc 0

Direct `verify` with the unchanged r90 driver on the battery's own trees (seven trees; the six forgeries plus
the pristine positive). Command per tree:

```
$ python3 -B S/carrier/corpus/evidence/round90/control-driver-r90.py verify \
    --root S/forge/<tree> --work S/a-direct/w-<tree> --rev 265b8633b7e5d1da49da6fb948df9707373fb15c \
    --expected S/forge/<tree>/expected.tsv --receipts S/forge/<tree>/receipts
```
Receipt `receipts/R91RevPrior/c1-r90-direct.txt`; every one of the seven trees prints the identical verdict
line and exits 0:

```
RECEIPT fx-one OK committed+exact+pin+fresh
RECEIPT fx-two OK committed+exact+pin+fresh
COMMITTED_OK=2/2 EXACT_OK=2/2 PIN_OK=2/2 FRESH_OK=2/2 CONTROL_DRIVER_R90=PASS
RC=0
```
So the priors are accepted by the whole r90 predicate (committed, exact, pin, fresh) — this is not an rc-only
artefact.

### a3. r90's `header_fields` keeps the last header value — the exact lines

`corpus/evidence/round90/control-driver-r90.py:90-98`:

```
 90  def header_fields(text):
 91      out = {}
 92      for ln in text.splitlines():
 93          if not ln.startswith("# "):
 94              continue
 95          k, _, v = ln[2:].partition("=")
 96          if k and v:
 97              out[k.strip()] = v.strip()          # <-- last assignment wins
 98      return out
```

Line 97 is a plain dict assignment: a second `# exit=` (or `# computed_against=`) overwrites the first, so the
first value is unbindable — the last-wins class. r91's equivalent `header_multi`
(`corpus/evidence/round91/control-driver-r91.py:102-111`) accumulates instead
(`out.setdefault(k.strip(), []).append(v.strip())`, line 110) and `check_headers`
(`control-driver-r91.py:190-209`, `HEADER_DUPLICATE` at line 196) refuses `len(vals) > 1`.

Observed maps (`receipts/R91RevPrior/c1-header-maps.txt`), on the exact forged receipt bytes:

```
positive:            header_fields -> {... 'exit': '0' ...}
                     header_multi  -> {... 'exit': ['0'] ...}
dup-header-exit:     header_fields -> {... 'exit': '0' ...}                  # file carries exit=1 then exit=0
                     header_multi  -> {... 'exit': ['1', '0'] ...}
dup-header-computed: header_fields -> {... 'computed_against': '265b8633…'}  # first (all-zero) rev invisible
                     header_multi  -> {... 'computed_against': ['000…0', '265b8633…'] ...}
```

So on `dup-header-exit/fx-one.txt` (`# exit=1` on line 4, `# exit=0` on line 5) r90's map can only see `0`,
which equals the row's exit, and it prints PASS; r91 sees both and refuses `HEADER_DUPLICATE:exit`.

### a4. Positive control

`receipts/R91RevPrior/c1-r91-positive.txt`:
```
$ python3 -B corpus/evidence/round91/control-driver-r91.py verify --root S/forge/positive \
    --work S/a-direct/w-r91-positive --rev 265b8633… --expected S/forge/positive/expected.tsv \
    --receipts S/forge/positive/receipts --pins S/forge/positive/pins.txt
BASES root=…/forge/positive repo=…/forge/positive
RECEIPT fx-one OK committed+exact+pin+fresh
RECEIPT fx-two OK committed+exact+pin+fresh
RECEIPT PINS OK 3/3 pinned files byte-identical
COMMITTED_OK=2/2 EXACT_OK=2/2 PIN_OK=2/2 FRESH_OK=2/2 PINNED_FILES=3 CONTROL_DRIVER_R91=PASS
RC=0
```

## (b) C2 before — the round-90 counter accepts all four forged trees; the double-count is real

### b1. The frozen battery, run from the carrier clone

```
$ cd S/carrier && python3 -B corpus/evidence/round91/curation-r91-controls.py --root . --work S/cur2
rc=0
```
Receipt `receipts/R91RevPrior/c2-controls.txt`; observed, all eight lines:

```
OK positive: r90 CURATION_R90=PASS r91 CURATION_R91=PASS
OK nonq-row: r91 CURATION_R91=FAIL (LEG_FAIL QSHAPE), r90 CURATION_R90=PASS
OK status-rejected: r91 CURATION_R91=FAIL (LEG_FAIL SOURCE), r90 CURATION_R90=PASS
OK used-by-blank: r91 CURATION_R91=FAIL (LEG_FAIL SOURCE), r90 CURATION_R90=PASS
OK ubiquitous-warrant: r91 CURATION_R91=FAIL (LEG_FAIL TFREQ), r90 CURATION_R90=PASS
OK duplicate-count: r90 UNENTAILED_TERM=2 r91 UNENTAILED_TERM=1
OK regression: FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 rc=0
CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7
```

### b2. `curation-r90.py` prints `CURATION_R90=PASS` on each of the four forged trees

Direct runs on the battery's own mirrored trees (`receipts/R91RevPrior/c2-direct.txt`; the loop runs both
counters on each tree, six trees in all):

```
$ python3 -B S/carrier/corpus/evidence/round90/curation-r90.py --root S/cur2/<tree>     # rc, observed verdict
pristine            rc=0  CURATION_R90=PASS
nonq-row            rc=0  CURATION_R90=PASS     # r91: Q_SHAPE_FAIL=1, LEG_FAIL QSHAPE, rc=1
status-rejected     rc=0  CURATION_R90=PASS     # r91: SOURCE_STATUS_OK=15/20, LEG_FAIL SOURCE, rc=1
used-by-blank       rc=0  CURATION_R90=PASS     # r91: USED_BY_OK=15/20, LEG_FAIL SOURCE, rc=1
ubiquitous-warrant  rc=0  CURATION_R90=PASS     # r91: TFREQ_OK=17/18, LEG_FAIL TFREQ, rc=1
```

The four forged-tree PASS lines are full r90 verdicts (`LEGS_MEASURED=10/10 VERDICT fields_hold=1` +
`DETECTOR_WITNESS=8/8`), not exit-code-only. Confirms `PRIOR_ACCEPTED=4/4`.

### b3. Double-count: `UNENTAILED_TERM=2` vs `1`, with the round-90 loop

`corpus/evidence/round90/curation-r90.py:247-250` (plus `DEFECT_TERMS` at line 52,
`DEFECT_TERMS = ("modification", "modified")`):

```
247          for cells in table_rows(section_lines(text, "Decision table"), 4):
248              for term in DEFECT_TERMS:
249                  if unentailed_row(cells, joined):
250                      unentailed.append((rel, cells[0], term))
```

The `if` is inside the `for term` loop, so one offending row appends one record per defect term (2), not one per
(row, term-carried). Observed on the battery's `duplicate-count` tree (one decision row `Recording a modified
resource` carrying `modified`, absent from every quote):

```
r90: SUPERSEDED_LIVE=0 UNENTAILED_TERM=2 … LEGS_MEASURED=7/10 VERDICT fields_hold=0
     LEG_FAIL UNENTAILED … Recording a modified resource term=modification; … Recording a modified resource term=modified
     CURATION_R90=FAIL rc=1
r91: SUPERSEDED_LIVE=0 UNENTAILED_TERM=1 … LEGS_MEASURED=9/13
     UNENTAILED … row=Recording a modified resource term=modified
     CURATION_R91=FAIL rc=1
```

The claim's before value (`DUPCOUNT_R90=2`) is thus the duplicated label, and r91's `1` is the single record
carrying the term the row actually carries. Both counters refuse the tree; the numeric difference is the
evidence, exactly as frozen.

## (c) C3 before — the old prose passes r90 and is mislabelled under r91

### c1. On `265b8633…:SKILL.md` (blob `2506f840…`; the clause is `r39 bash-pin cases 273–275 and r82
bash-pin-override cases 276–283`)

Commands and observed lines (`receipts/R91RevPrior/c3-tally-base.txt`):

```
$ python3 -B S/carrier/corpus/evidence/round90/skill-tally-r90.py --root S/base \
    --selftest S/carrier/corpus/evidence/round91/controls/selftest-r91.txt
TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS
RC=0

$ python3 -B S/carrier/corpus/evidence/round91/skill-tally-r91.py --root S/base \
    --selftest S/carrier/corpus/evidence/round91/controls/selftest-r91.txt
CASE_RANGE_FINDING RANGE_MISMATCH:bash-pin-override claimed=276-283 derived=282-283
CASE_RANGE_FINDING MISLABELED=6 indices=276,277,278,279,280,281
TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 \
  CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=1/2 MISLABELED=6 LEGS=1/2
LEG_FAIL CASE-RANGE
SKILL_TALLY_R91=FAIL
RC=1
```

Both exact values the seat asked for re-derive: r90 `SKILL_TALLY_R90=PASS`; r91 `CASE_RANGE_OK=1/2
MISLABELED=6`.

### c2. The case names are the tool's own, read from the committed selftest receipt

`corpus/evidence/round91/controls/selftest-r91.txt`: 283 `ok-case` lines, verdict at line 285
`RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)`; indices 273–283:

```
273 pin-bashenv-echo   274 drift-bashenv-echo   275 pin-bashenv-root
276 pin-env-fn-echo-scrub  277 pin-env-fn-suppress  278 pin-env-fn-root
279 env-pin-override-missing  280 env-pin-override-fake  281 pin-bash-path-shim
282 bash-pin-override-missing  283 bash-pin-override-fake
```

`bashenv` family = 273–275, `bash-pin-override` family = 282–283 (`skill-tally-r91.py:37-38,91-92`), so the
prose's 276–283 claims six indices (276–281) whose names are not in the family — `MISLABELED=6`.

### c3. The discrimination is the range binding, not the tallies

On a scratch copy of the base `SKILL.md` with the frozen repair applied (`OLD_CLAUSE` from
`skill-tally-r91-controls.py:30-31`; the fixture is the deterministic substitution the battery itself performs —
see (d)):

```
receipts/R91RevPrior/c3-tally-repaired.txt
r90: … STALE_TALLIES=0/9 … SKILL_TALLY_R90=PASS  rc=0        # r90 never binds the range
r91: … CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2
     SKILL_TALLY_R91=PASS  rc=0
```

So r91 refuses the old prose and accepts the repaired prose; r90 accepts both.

## (d) Comparison with the committed before receipts at the carrier

`receipts/R91RevPrior/d-receipt-diffs.txt` — sha256 and `cmp` of each committed receipt against this seat's run:

| committed receipt (`corpus/evidence/round91/controls/receipts/`) | sha256 | this seat's run | cmp |
|---|---|---|---|
| `c1-before.txt` | `a0c69090541a51a2a6e89ea42ded151c85989bae6bef61fbf9f20419f86fd5b7` | `c1-forgeries.txt` | rc 0 (byte-identical) |
| `c2-before.txt` | `d9783e1a265c6fc329409fe66773db86f1d6b1cc9d74034bb40b4c296e5b4b4a` | `c2-controls.txt` | rc 0 (byte-identical) |
| `c3-before.txt` | `5728153dc065759048952d9dad59c4409db02f06b64a1cfc3338ffe31d993185` | `c3-controls-repaired.txt` | rc 0 (byte-identical) |

No line in any of the three committed before receipts fails to re-derive. Two reconstruction conditions must be
stated with c3:

1. **The committed tree does not carry the repaired clause.** Both `265b8633…` and `67954adc…` `SKILL.md` are
   blob `2506f840…` and carry the round-90 prose (`BAD_CLAUSE`); the repaired `OLD_CLAUSE` exists nowhere in
   git history (`git log --all -S 'of which bash-pin-override' -- SKILL.md` prints nothing; the commit range
   `265b8633..67954adc` does not touch `SKILL.md`). The battery therefore refuses to run against the carrier
   tree: `skill-tally-r91-controls.py --root S/carrier --work S/c3ctl-carrier` prints
   `SETUP repaired clause absent from SKILL.md — is this the landing tree?` and exits **2**
   (`receipts/R91RevPrior/c3-controls-carrier-setup.txt`). This matches the dispatch's own note that the C3
   repair lands after the wave; the C3 claim's `CONTROLS=PASS` is a landing-revision projection, not an
   observable at `C3`.
2. **`c3-before.txt` re-derives only through the frozen one-clause repair.** I rebuilt the fixture from the base
   `SKILL.md` by substituting the battery's own committed `OLD_CLAUSE` constant for `BAD_CLAUSE` (the exact
   substitution `skill-tally-r91-controls.py` performs), then ran the battery. The line itself is deterministic
   from committed bytes (constants + base tree), and the substantive before-state — old prose on the committed
   tree — was independently measured in (c1) without the fixture.

## Findings

**F1 (C1/C2: none).** No divergence: all six r90 acceptances, the four r90 `CURATION_R90=PASS` verdicts, the
2-vs-1 double-count, the r90 last-wins header behaviour and the r91 positive/refusals re-derive as frozen; the
two batteries reproduce their committed receipts byte-for-byte.

**F2 (C3, precondition, expected by the dispatch, not a counter divergence).** `skill-tally-r91-controls.py
--root .` at the tree under attack exits 2 `SETUP repaired clause absent from SKILL.md`; a verifier that runs the
C3 control command on pristine `C3` bytes will see SETUP, not `CONTROLS=PASS`. The C3 executor must apply the
frozen one-clause repair (prose 276–283 → 282–283, the `OLD_CLAUSE` text) before that command can print the
claimed line. Command, receipt and exit: `c3-controls-carrier-setup.txt`, rc 2.

**F3 (C1 prose, wording/provenance, no counter moves).** `claims.md` C1 **Before** parenthetical says "the r90
spot-check routed the same classes as defects 2 and 3". Reading the committed lesson
(`corpus/lessons/round-90-verifier-spotcheck.md:237-243`): routed defect **2** is the C1 residue list
(duplicate header keys, pin the instrument bytes, `SELF_PIN` both revisions, fresh-divergence/empty-body
fixtures, `--root`/`--repo` base) and routed defect **3** is the harm-row self-comparison. Of the six classes in
`c1-before.txt`, three map to defect 2 (the two duplicate-header classes and the substituted instrument), while
`expected-swap`, `missing-expected_exit` and `extra-receipt` are named in neither routed item, and the harm class
(defect 3) is exercised by `controls/expected.tsv` rows `c1-harm` / `c1-harm-setup`, not by `c1-before.txt`
(`grep -c harm c1-before.txt` → 0; `c1-before.txt` has the six forgery lines + positive + summary). The machine
form (`.ufo/waves/round-91/claims.json:51`) carries no such attribution. This is a citation-precision observation
for the integrator to adjudicate, not a before-state divergence; intent is inferred (referent ambiguous).
Commands and observations: `grep -c harm corpus/evidence/round91/controls/receipts/c1-before.txt` → `0` (rc 1, no
match); `grep -n 'Routed defects' -A 40 corpus/lessons/round-90-verifier-spotcheck.md` → items at lines 232–243
(2 at 237–239, 3 at 240–243); `grep -n 'c1-harm' corpus/evidence/round91/controls/expected.tsv` → rows
`c1-harm`/`c1-harm-setup` (the defect-3 class lives there, not in `c1-before.txt`).

## Confidence and limits of this observation

- High confidence on (a), (b), (c1) and (d): all commands are recorded, and the three committed before receipts
  are byte-identical (sha256 + `cmp rc 0`) to runs made from committed bytes in the named clones.
- The before-state is measured with the r90 instruments at the carrier blob (identical at base); no r91
  instrument was used to produce a before value except where the frozen battery does so by design.
- I did not run a fresh `bash tools/research-gate.sh --selftest` (not required by this item); the 283-case
  receipt was read and its 283 `ok-case` names counted from committed bytes.
- `c3-before.txt`'s re-derivation depends on the battery's own committed `OLD_CLAUSE` constant (F2/c2 above);
  the old-prose measurement on the committed `SKILL.md` does not.
- No network call was made; no host state, service, sysctl or PATH entry was touched.

## Receipts (copied into this wave folder)

`receipts/R91RevPrior/`: `commands.txt`, `pins-and-blobs.txt`, `c1-forgeries.txt`, `c1-r90-direct.txt`,
`c1-r91-positive.txt`, `c1-header-maps.txt`, `c2-controls.txt`, `c2-direct.txt`, `c3-tally-base.txt`,
`c3-tally-repaired.txt`, `c3-controls-repaired.txt`, `c3-controls-carrier-setup.txt`, `d-receipt-diffs.txt`,
`committed-c1-before.txt`, `committed-c2-before.txt`, `committed-c3-before.txt`, `committed-selftest-r91.txt`,
`manifest.sha256`.

VERDICT: R91RevPrior C1 held — the six forged classes each pass the full unchanged r90 predicate
(`CONTROL_DRIVER_R90=PASS`, `COMMITTED_OK/EXACT_OK/PIN_OK/FRESH_OK=2/2`, rc 0 on every tree), the battery prints
`FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`, and r90's `header_fields` last-wins assignment
(`control-driver-r90.py:97`) hides the first duplicate header while r91's `header_multi` keeps it and refuses.
VERDICT: R91RevPrior C2 held — `CURATION_R90=PASS` re-derives at rc 0 on each of the four forged trees the
battery builds (and the pristine mirror), `DUPCOUNT_R90=2` vs `DUPCOUNT_R91=1` re-derives from the one-row
probe with the `for term in DEFECT_TERMS:` loop at `curation-r90.py:248-250` producing the duplicate label, and
the controls receipt is byte-identical.
VERDICT: R91RevPrior C3 held — on `265b8633…:SKILL.md` r90 prints `SKILL_TALLY_R90=PASS` (rc 0) while r91 prints
`CASE_RANGE_OK=1/2 MISLABELED=6` (rc 1) with `CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283` derived
from the receipt's own case names; `c3-before.txt` re-derives byte-identically only on the frozen repaired
fixture, because the repair lands after the wave and the controls command on pristine C3 bytes exits 2 SETUP.
