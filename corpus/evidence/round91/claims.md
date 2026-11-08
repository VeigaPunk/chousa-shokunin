# chousa — round 91 frozen claims (freeze `F`, carrier `C`)

Base `265b8633b7e5d1da49da6fb948df9707373fb15c` (round-90 landing + its non-author spot-check). Machine form:
`.ufo/waves/round-91/claims.json`. Plan, pre-freeze repairs and amendments: `plans/round-91.md`. In every counting
command below, `F` is the freeze commit that carries this file and `C` the carrier commit that carries the emitted
receipts; both are named concretely in the round report and in `corpus/lessons/round-91.md`.

## C1 — operability (lowest scored non-retired axis, historical 3/10)

**Statement.** At the landing revision,
`python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . --rev F --receipts-rev C` prints
`CONTROL_DRIVER_R91=PASS` (exit 0) with `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6` over the six
committed receipts of `controls/expected.tsv`, and each of these holds:

1. every receipt is read from disk before any fresh run, and `verify` writes nothing under `controls/receipts/`;
2. every required header key — `case`, `expected_exit`, `exit`, `computed_against` — appears exactly once, and its
   value equals the row's (`HEADER_DUPLICATE`, `MISSING_HEADER`, `EXIT_MISMATCH`, `EXPECTED_EXIT_MISMATCH`);
3. `# computed_against=` equals `--rev`;
4. every required `K=V` equals one whole whitespace-delimited body token (a differing value under the same key is
   `TOKEN_DETACHED`) and every `K>=N` predicate holds (`DUPLICATE_KEY` for one key with two values);
5. the first file each row's command names as its script, and the expectations file, is listed in
   `instrument-pins.txt`, its on-disk sha256 equals the pin, and (with `--repo`) its blob at `--rev` hashes to the pin
   (`INSTRUMENT_UNPINNED`, `INSTRUMENT_PIN_MISMATCH`);
6. a `.txt` file that parses as a receipt (a `# case=` header) and that no expected row scores is
   `UNSCORED_RECEIPT`;
7. `SELF_PIN` prints both revisions (`rev=F receipts_rev=C`) and every scoring file is byte-identical to its blob
   at the base it is read from (`--root` for reads, `--repo` for blobs);
8. `python3 -B corpus/evidence/round91/control-forgeries-r91.py --work <scratch>` prints
   `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`: the six classes (duplicate exit header, duplicate pin
   header, substituted instrument, relaxed expectations, missing `expected_exit`, unscored receipt) are refused by
   r91 and accepted by the unchanged r90 driver, and the pristine fixture is accepted by both.

Source: **S070** (the installed `sha256sum(1)` page, re-opened this round, quote "Print or check SHA256 (256-bit)
checksums.") grounds rule 5's digest check: the page's own text says the tool prints or checks a digest, which is
what the pin leg does with the pinned bytes.

**Before.** The round-90 driver on the same fixture: `PRIOR_ACCEPTED=6/6` — it accepts all six classes
(`controls/receipts/c1-before.txt`, emitted by the r91 battery; the r90 spot-check routed the same classes as
defects 2 and 3).

**Kill rules.** K1 the predicate is not met at the landing revision. K2 any forgery is accepted by r91, the positive
is refused, or r90 refuses a forgery (the discrimination is dead). K3 a genuine row moves or the verification path
writes the receipts directory (a post-verify byte comparison of `controls/receipts/`). K4 the pass skips the work:
a missing receipt is accepted, a committed receipt is not read, a substring satisfies a token, or the pin is
minted inside `verify`.

**Named limits.** (1) A coherent joint edit of instrument, pin, receipt and expectation row survives — that edit is
the harness, not a forgery. (2) Whole-token matching binds one field per token, not its semantic role. (3) The pin
names the script a row's command mentions first; a command that executes a second, unpinned script is not seen.
(4) The self-pin detects a moved byte inside a named commit, not a rewritten history. (5) The driver cannot see a
pinned script that reads data outside its own bytes.

## C2 — calibration

**Statement.** At the landing revision, `python3 -B corpus/evidence/round91/curation-r91.py --root .` prints
`CURATION_R91=PASS` (exit 0) with `LEGS_MEASURED=13/13`, `Q_ROWS=20 Q_SHAPE_FAIL=0`,
`SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20`, `TFREQ_OK=17/17 TFREQ_MAX_DF=3`, `UNENTAILED_TERM=0`,
`WARRANT_OK=17/17`, `DUP_QIDS=0`, `VERDICT fields_hold=1` and `DETECTOR_WITNESS=11/11`; and
`python3 -B corpus/evidence/round91/curation-r91-controls.py --root . --work <scratch>` prints
`CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7`:

1. every data row of `## Located quotes` is a `Q<n>` row with exactly three cells, a registry-shaped source id and
   a non-empty quote, and no qid repeats (`QSHAPE`);
2. every located quote's cited source is a registry row with `status=mined` whose `used-by` names the entry
   (`SOURCE`);
3. every decision row's warrant qid shares with that quote at least one content term whose document frequency over
   the entry's located quotes plus decision rows is `<= 3` (`TFREQ`, the measured maximum over the legitimate
   rows);
4. one decision row carrying a defect term that no quote carries is appended once, with the term it carries
   (`UNENTAILED_TERM=1` for the probe, not 2); and
5. the four tree forgeries (non-`Q` quote row, `rejected` status, emptied `used-by`, a warrant sharing only
   `source`, df 7) are refused by r91 and accepted by the unchanged r90 counter; the seven round-90 tree forgeries
   are still refused; the pristine tree is accepted by both.

**Before.** `curation-r90.py` on the same four forged trees prints `CURATION_R90=PASS` on each
(`PRIOR_ACCEPTED=4/4`), prints `UNENTAILED_TERM=2` for the one-row probe, and its own spot-check recorded the two
silent classes (`controls/receipts/c2-before.txt`).

**Kill rules.** K1 the predicate is not met at landing. K2 any of the four forgeries is accepted by r91, the
positive is refused, or r90 refuses one (no discrimination). K3 the clean tree's PASS changes or the counter writes
the tree. K4 the pass skips the work: a non-`Q` row is dropped, a cited source's status is unread, a term above
`DF_MAX` is accepted as a warrant, or the double-count loop is restored.

**Named limits.** (1) The two routed entries and their pinned qid sets only. (2) Document frequency is measured
over the entry's own units (its located quotes plus its decision rows), not the world. (3) The stopword list is a
fixed list; a frequent word on it is not a warrant. (4) A verbatim-located quote used for the wrong proposition
still passes. (5) A coherent joint edit of entry, registry and capture survives.

## C3 — freshness

**Statement.** At the landing revision,
`python3 -B corpus/evidence/round91/skill-tally-r91.py --root . --selftest corpus/evidence/round91/controls/selftest-r91.txt`
prints `SKILL_TALLY_R91=PASS` (exit 0) with `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0
OTHER_OCCURRENCES=3 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2`;
the two case-range clauses are derived from the tool's own `ok-case` names (`bashenv` at 273–275,
`bash-pin-override` at 282–283), and `python3 -B corpus/evidence/round91/skill-tally-r91-controls.py --root .
--work <scratch>` prints `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1` — the
pre-round prose (`bash-pin-override cases 276–283`) is refused by r91 with `CASE_RANGE_OK=1/2 MISLABELED=6` and
accepted by the unchanged r90 counter, and a stale tally is refused by both.

**Before.** `skill-tally-r90.py` on the base `SKILL.md` prints `SKILL_TALLY_R90=PASS` — the range was never bound;
the prose attached `bash-pin-override` to 276–283 while six of those cases (276–281) carry other names
(`controls/receipts/c3-before.txt`).

**Kill rules.** K1 the predicate is not met at landing. K2 r91 accepts the old prose, refuses the repaired prose, or
derives the range from the prose rather than the tool's names. K3 a historical tally or quote moves
(`OTHER_OCCURRENCES=3` unchanged; the diff touches only the one clause). K4 the pass skips the work: no case names
are read, an absent clause is tolerated, or the selftest is not run/read.

**Named limits.** (1) Case names are the tool's debug strings; a rename changes the binding loudly, by design.
(2) The round that added a case is not derived — only the name family the prose claims. (3) The tally leg binds
current cells structurally (r90's rule); historical quotations stay unbound and counted.
