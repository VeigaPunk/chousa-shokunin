# chousa — round 92 frozen claims (freeze `F`, carrier `C`)

Base `d7780feff6e39ae74a2fd77fc9773c671b33da95` (round-91 landing + its non-author spot-check). Machine form:
`.ufo/waves/round-92/claims.json`. Plan, pre-freeze repairs and amendments: `plans/round-92.md`. In every counting
command below, `F` is the freeze commit that carries this file and `C` the carrier commit that carries the emitted
receipts; both are named concretely in the round report and in `corpus/lessons/round-92.md`.

## C1 — operability (lowest scored non-retired axis, historical 3/10)

**Statement.** At the landing revision,
`python3 -B corpus/evidence/round92/control-driver-r92.py verify --root . --repo . --rev F --receipts-rev C
--work <scratch>` prints `CONTROL_DRIVER_R92=PASS` (exit 0) with
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6` over the six committed receipts of
`controls/expected.tsv`, where `PASS` requires `findings==0 AND committed_ok==len(rows) AND
exact_ok==len(rows) AND pin_ok==len(rows) AND fresh_ok==len(rows)`; and
`python3 -B corpus/evidence/round92/forgeries-r92.py --work <scratch>` prints
`FORGERY_REFUSED=3/3 POSITIVE=pass` (three classes, one traced recipe each):

1. every receipt is read from disk before any fresh run, and `verify` writes nothing under `controls/receipts/`;
2. every required header key — `case`, `expected_exit`, `exit`, `computed_against` — appears exactly once after
   leading whitespace is stripped, and its value equals the row's
   (`HEADER_DUPLICATE`, `MISSING_HEADER`, `EXIT_MISMATCH`, `EXPECTED_EXIT_MISMATCH`);
3. `# computed_against=` equals `--rev`;
4. every required `K=V` equals one whole whitespace-delimited body token and every `K>=N` predicate holds;
5. Every file a row's command string names as its script (every in-tree `.py`/`.sh` token, not just the first),
   the expectations file, and the pins file itself are byte-checked on disk against their pins (the pinned set
   of executed scripts + expected + pins = 7 files; the pins file's own pin is the sha256 of its
   non-comment, non-blank rows minus its own row — the self-pin, Amendment 3); every one of the remaining pins
   (the 16-row table) is blob-checked at `--rev` by the SELF_PIN leg only, not on disk (see Named limit 7)
6. a repeated pin path is `SETUP PIN_DUPLICATE` exit 2 before any receipt is scored (`read_pins` last-wins is gone);
7. `SELF_PIN` prints both revisions (`rev=F receipts_rev=C`) and every scoring file is byte-identical to its blob
   at the base it is read from;
8. `emit` without an explicit `--receipts` exits 2 (`emit requires an explicit --receipts`); `--work` defaults to
   `$TMPDIR` else `/fast/scratch/hyaku`; fresh legs run `bash -c` with a scrubbed env (PATH + HOME only);
9. the forgery battery refuses, with the named codes above, the three S3/S4/S5 classes (duplicate pins file,
   second unpinned script, rewritten pins table) and passes its pristine positive control.

Source: **S070** (the installed `sha256sum(1)` page, re-opened this round, quote "Print or check SHA256 (256-bit)
checksums.") grounds rule 5's digest check, including the self-pin: the page's own text says the tool prints or
checks a digest, which is what the pin leg does with the pinned bytes.

**Before.** The round-91 driver on the corresponding fixtures: `read_pins` keeps the last of two rows for one
path (accepts the duplicate), `instrument_rel` returns the first file token only (a second script is unchecked),
and the pins file has no entry in the pin set (a rewritten table with coherent rows passes); receipts with
whitespace-indented headers are read as missing headers. There is no r91 battery number to quote: the 6 classes
r91 already refuses are prior work, not new catches (see the battery header).

**Kill rules.** K1 the predicate is not met at the landing revision. K2 a battery forgery is accepted by r92 or
the positive is refused. K3 a genuine row moves or the verification path writes the receipts directory. K4 the
pass skips the work: a missing receipt is accepted, a committed receipt is not read, a substring satisfies a
token, a duplicate pin path is scored, or the self-pin is minted inside `verify`.

**Named limits.** (1) A coherent joint edit of instrument, pin, receipt and expectation row survives — that edit
is the harness, not a forgery. (2) Whole-token matching binds one field per token, not its semantic role.
(3) The self-pin detects a moved byte inside a named commit, not a rewritten history. (4) The minus-self digest
binds the table's coherence, not its authority — a fully recomputed rewrite survives. (5) A pinned script that
reads data outside its own bytes is unseen. (6) The exact-gate repair (r91 routed defect: `passed` did not
require `exact_ok`) is stated as a code change but is vacuous-in-practice (committed_ok already implies exact_ok
row-for-row, since a detached token fails both), and is not cited as a gain. (7) Only tokens in the command
string are pinned: a pinned script that executes a second script is unseen. (8) On-disk pinning covers the
executed scripts + expected + pins file (7 of the 16 pinned rows); a tampered copy of any of the other nine
pinned bytes is unseen on disk and is caught only via the SELF_PIN blob leg when run with `--repo`.

## C2 — calibration

**Statement.** At the landing revision, `python3 -B corpus/evidence/round92/curation-r92.py --root .` prints
`CURATION_R92=PASS` (exit 0) with `LEGS_MEASURED=14/14`, `Q_ROWS=20 Q_SHAPE_FAIL=0`,
`SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20`, `TFREQ_OK=17/17 TFREQ_MAX_DF=3`, `UNENTAILED_TERM=0`,
`WARRANT_OK=17/17`, `DUP_QIDS=0`; and
`python3 -B corpus/evidence/round92/curation-controls-r92.py --root . --work <scratch>` prints
`CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=7/7`:

1. every pipe-leading data row of `## Located quotes` is a `Q<n>` row with exactly three cells, a
   registry-shaped source id and a non-empty quote; the only structural skips are the literal header row
   (`qid|source|quote`) and all-dash (non-empty, dash/colon/space) separator rows — a forged row whose first
   cell is `qid`, `Situation` or empty reaches the shape test (`QSHAPE`); a forged row occupying the first
   table line is a data row, not the header, unless it IS the literal header row;
2. every decision row the table holds has exactly four cells and the per-entry device count of data rows (the
   pipe-leading rows after the structural header/separator, 11 + 6 = 17) equals the pinned count; a wrong-width
   row is a `DECISION_WIDTH` finding, never a silent drop (`WARRANT`); an empty-first-cell row reaches the
   width check, it is not a separator;
3. every located quote's cited source is a registry row with `status=mined` whose tokenised `used-by` carries
   the entry as an exact token, not merely a containing substring (`SOURCE`);
4. every mined registry row that names an entry in `used-by` is cited by at least one Located-quote row of that
   entry (`USED_BY`);
5. every decision row's warrant qid, for rows whose named qids all resolve, shares with that quote at least one
   content term of document frequency `<= 3` over the entry's quotes plus decision rows (`TFREQ`); a row with
   an unresolved qid is a `WARRANT` failure and leaves TFREQ's universe;
6. the four S-classes (forged header-cell quote row, five-cell decision row, substring-only used-by match,
   mined-but-uncited used-by) are refused by r92 and accepted by the unchanged r91 counter; the r91 battery's
   four classes and the r90 battery's seven tree forgeries are still refused; the pristine tree is accepted by
   both.

**Before.** The round-91 counter accepts all four S-classes: it drops a `qid`-first-cell forged quote row before
the shape test, silently drops five-cell decision rows, joins `used-by` by substring, and has no leg from the
registry side.

**Kill rules.** K1 the predicate is not met at landing. K2 any of the four S-forgeries is accepted by r92, the
positive is refused, or r91 refuses one (no discrimination). K3 the clean tree's PASS changes or the counter
writes the tree. K4 the pass skips the work: a non-structural row is dropped, a substring used-by match is
accepted, a mined row naming an entry is left uncited, or a wrong-width decision row is dropped.

**Named limits.** (1) The two routed entries and their pinned qid/decision-count sets only. (2) Document
frequency is measured over the entry's own units, not the world. (3) The stopword list is a fixed list. (4) A
verbatim-located quote used for the wrong proposition still passes. (5) A coherent joint edit of entry, registry
and capture survives. (6) The tokenised used-by join reads the registry row only; an entry that cites a row
whose used-by names it, but whose used-by also names a sibling, is joined on the entry's exact token only.

## C3 — freshness

**Statement.** At the landing revision,
`python3 -B corpus/evidence/round92/skill-tally-r92.py --root . --selftest
corpus/evidence/round92/controls/selftest-r92.txt` prints `SKILL_TALLY_R92=PASS` (exit 0) with
`TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2
CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 OTHERS_OK=1 LEGS=3/3`;
the tally search and the two case-range searches run over the `## Gates` section only (case-sensitive bytes,
up to the next ATX heading of depth <= 2 at column 0 — `# ` or `## `; a second-level heading, a third-level
heading, or any indented heading is not a boundary),
and the non-current occurrences INSIDE that section form the pinned multiset `{(161,0):1, (256,0):1}` —
deleting either changes the verdict; and
`python3 -B corpus/evidence/round92/skill-tally-r92-controls.py --root . --work <scratch>` prints
`CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1` — the r91-bad clause
(`276–283`) is refused by both counters (carried from r91), a stale current tally is refused by both (carried),
and deleting one historical occurrence inside `## Gates` is refused by r92 (`LEG_FAIL OTHERS`) and accepted by
r91 (document-wide, unpinned).

**Before.** The round-91 counter searches the whole document and counts non-current occurrences without pinning
their multiset: changing `PASS (161 cases, 0 skipped)` inside `## Gates` to 160 leaves it passing
(`controls/receipts/c3-before.txt`, emitted by the r92 battery).

**Kill rules.** K1 the predicate is not met at landing. K2 r92 accepts the deleted-other forgery or refuses the
clean tree, or derives any bound from `SKILL.md` prose rather than the tool's own `ok-case` names. K3 a
historical tally or quote outside `## Gates` moves (the r215 tail tally is deliberately out of scope under the
section scoping and is named as a limit, not silently unbound). K4 the pass skips the work: no case names are
read, an absent clause is tolerated, the selftest is not run/read, or the others multiset is not compared.

**Named limits.** (1) The section boundary is the next ATX heading of depth <= 2 at column 0; a clause moved
outside `## Gates` leaves the leg and the counter prints `CLAUSE_MISSING`. (2) The pinned others multiset
holds the two in-section historical tallies (161, 256); the 215 tail tally sits after `## Round26` and is
unbound by design. (3) Case names are the tool's debug strings; a rename changes the binding loudly, by
design. (4) The tally leg binds current cells structurally; historical quotations stay unbound and counted.
(5) The case-enumeration leg trusts the verdict line's `cases` figure and requires every `^ok-case` line (including
the six `accepted=` lines) to be distinct; it does not reconcile the verdict count against the tool's own
universe of cases beyond the enumerated lines in the supplied selftest output.
