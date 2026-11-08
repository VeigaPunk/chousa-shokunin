# R92ReviewerC2 — frozen C2 wording vs the code (carrier C5)

Seat: leaf reviewer, round 92 L1. Canonical tree: clone of
`/home/vgpnk/Projects/shokunin/chousa-shokunin` at `16ccf7693c61b8ffe392fc757352304f239bfcad`
(`git -C <scratch>/repo rev-parse --show-toplevel` = scratch clone; no mutation, no commit, no network).
Frozen claim read first: `corpus/evidence/round92/claims.md` §C2 (lines 60-99); instrument:
`corpus/evidence/round92/curation-r92.py` (pinned `81310bba…644166`), battery
`corpus/evidence/round92/curation-controls-r92.py` (pinned `aeac03d6…b8134f3`).
All receipts below are in `.ufo/waves/round-92/w1/receipts-c2/`. Scratch `/fast/scratch/hyaku/chousa-r92/R92ReviewerC2`
deleted at yield. Tool installs: none. Network: none.

## Baseline (the predicate as written, pristine bytes)

```
$ python3 -B corpus/evidence/round92/curation-r92.py --root .        # cwd = clone@C5
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_ROWS=20 Q_SHAPE_FAIL=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TFREQ_OK=17/17 TFREQ_MAX_DF=3 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=14/14
CURATION_R92=PASS                                                     # EXIT=0
```
Receipt `P0-pristine.txt`. The stated numbers are real **on the pristine tree**; every finding below is a
tree that still prints this line byte-for-byte (verified by string equality against the line above, not by eye)
with a defect the claim says cannot survive.

---

## Findings by severity

### F1 — CRITICAL: the claim's control script does not exist at C5; the stated command cannot run

Claim (claims.md:66-67) names `corpus/evidence/round92/curation-r92-controls.py`. C5 carries
`curation-controls-r92.py` (pins line 4). The literal command:

```
$ python3 -B corpus/evidence/round92/curation-r92-controls.py --root . --work <scratch>
python3: can't open file '.../round92/curation-r92-controls.py': [Errno 2] No such file or directory
EXIT=2
```

`ls corpus/evidence/round92/*.py` → `control-driver-r92.py curation-controls-r92.py curation-r92.py
forgeries-r92.py skill-tally-r92-controls.py skill-tally-r92.py tally-controls-r92.py tally-r92.py`;
`test -e .../curation-r92-controls.py` → MISSING. This is claim K1 as written ("the predicate is not met"):
a reader executing the frozen text gets exit 2 and none of the four tokens. Narrowing to record: state the
pinned path `curation-controls-r92.py` (or rename the file and re-pin; the pin table is authority).

### F2 — CRITICAL: an empty first cell is skipped at **any** position in both tables; the full frozen line still prints

Claim 1 (claims.md:69-72) enumerates the skips as "the structural header row (first table line, `qid` first
cell) and all-dash separator rows" and asserts "a forged row whose first cell is `qid`, `Situation` or
**empty** reaches the shape test (`QSHAPE`)". The instrument skips empty-first-cell rows twice over:

- `quote_lines` (curation-r92.py:168-169): `if cells and set(cells[0]) <= set("-: "): continue` — `set("")`
  is the empty set, so `"" <= {"-",":"," "}` is vacuously true; an empty first cell is treated as a separator.
- `data_lines` (curation-r92.py:152): `cells[0] in ("Situation", "qid", "")` — same skip for `## Decision table`.

Probes (each a full copy of C5 with one row inserted; receipt name → result):

| probe | inserted row | observed | exit |
|---|---|---|---|
| P1b | `| | S018 | "a forged quote row with no qid at all here" |` after the separator | `Q_ROWS=20 Q_SHAPE_FAIL=0 … LEGS_MEASURED=14/14` / `CURATION_R92=PASS` | 0 |
| P1c | same row **before** the header | same frozen line, `CURATION_R92=PASS` | 0 |
| P1g | `| | S018 | "a four cell forged quote row" | extra |` (4 cells, empty first) | `Q_SHAPE_FAIL=0`, `CURATION_R92=PASS` | 0 |
| P3b | `| | state a thing | never a thing | Q1 (S215) |` (4-cell decision row) | `WARRANT_OK=17/17`, `CURATION_R92=PASS` | 0 |
| P3d | `| | state an unlinked thing | never a thing | Q99 |` | `WARRANT_OK=17/17`, `CURATION_R92=PASS` | 0 |
| P3e | `| | a | b | c | d |` (5-cell decision row) | `Q_SHAPE_FAIL=0`, `CURATION_R92=PASS` | 0 |

For P1b/P1c/P1e/P3b/P3d/P3e the receipt's `SUPERSEDED_LIVE=…` line is **string-equal** to the pristine line
above (verified programmatically), and `# exit: 0`.

P3d is the sharpest: the fixture file holds one more decision row than pristine (16 vs 15 `^| ` rows in
`provenance-recording-r85.md`), that row's warrant is `Q99` — which P3 proves fires `LEG_FAIL WARRANT 16/17`
when the row is visible — yet the instrument scores 6 decision rows and prints `WARRANT_OK=17/17`.

Narrowing to record: the sentence must say the shape test sees rows whose first cell is non-empty and
non-separator, i.e. "an empty first cell is skipped as a separator at any position (and any width)" — or the
filter must distinguish a separator (`cells[0]` non-empty and all `-:`/space) from an empty cell.

### F3 — CRITICAL: a forged `qid`-first row **is** a data row when it occupies the first table line, and is dropped; the S1 class is accepted

Claim 1 says a forged row whose first cell is `qid` reaches the shape test, and claim 6 (claims.md:81-84) says
the "forged header-cell quote row" class is refused by r92. `quote_lines` swallows it positionally
(curation-r92.py:165-167): the *first* pipe-leading line with `cells[0] == "qid"` is consumed as the header,
whoever wrote it.

Probe P1e — the genuine header line `| qid | source | quote |` replaced by
`| qid | S018 | "a forged quote row pretending to be the header" |`:

```
Q_ROWS=20 Q_SHAPE_FAIL=0 … LEGS_MEASURED=14/14
CURATION_R92=PASS                                                     # EXIT=0
```
Receipt `P1e-header-replaced-by-qid-row.txt`; line string-equal to pristine. Control P1h (the identical
forged row placed **after** the separator, i.e. the battery's own S1 insertion point,
`curation-controls-r92.py:43` + `:149-151`) does fire: `Q_SHAPE_FAIL=1`, `LEG_FAIL QSHAPE … qid=qid`,
`CURATION_R92=FAIL` exit 1 (`P1h-qid-row-after-sep.txt`). So refusal is positional, and the forger controls
the position by deleting the real header. This is the round-91 routed defect ("drops a `qid`-first-cell forged
quote row before the shape test") surviving at C5 for first-table-line rows; the battery's S1 never tests it.

Narrowing to record: the skip must be keyed to the *structural* header (e.g. the row that immediately follows
`## Located quotes` **and** whose cells are `qid|source|quote`), not to "first `qid`-first line"; otherwise the
claim must say the first table line is trusted and drop the "reaches the shape test" clause.

### F4 — HIGH: the "per-entry decision-row count equals the pinned count" is a count of *surviving* rows, not decision rows

Claim 2 (claims.md:73-74): "the per-entry decision-row count equals the pinned count (11 + 6 = 17) … never a
silent drop". `decision_counts_seen[rel] = len(rows)` (curation-r92.py:343) is taken after the `data_lines`
filter, so a dropped row lowers neither counter nor `warrant_total`. P3d (above) is the witness: file holds 7
decision rows for `provenance-recording-r85.md`, the instrument counts 6, `count_bad=0`, `WARRANT_OK=17/17`.
The claim's number is reproduced while the document contains an extra, unscored decision row.

Narrowing: "the count of rows that survive the table filter equals the pinned count" — currently the pin
cannot detect a drop, only a row that survives at the wrong width.

### F5 — MEDIUM: TFREQ's "every decision row's warrant qid shares …" is false for an unresolvable qid; the row leaves the denominator

Probe P3 — one decision row's warrant changed `Q7 (S031)` → `Q99 (S031)` (4 cells intact):

```
WARRANT_OK=16/17 TFREQ_OK=16/16 TFREQ_MAX_DF=3 … LEGS_MEASURED=12/14
WARRANT_UNLINKED corpus/knowledge/provenance-recording-r85.md row=Recording when content was last reviewed warrant=Q99 (S031) resolved=0/1
LEG_FAIL WARRANT 16/17 width_fail=0 count_bad=0
LEG_FAIL VERDICT fields_hold=0 legs_ok=12/13
CURATION_R92=FAIL                                                     # EXIT=1
```
Receipt `P3-warrant-unresolvable.txt`. WARRANT fires as the claim says (probe 3 answered: yes), but
`tfreq_total` is incremented only when every qid resolves (curation-r92.py:364-365), so the same defect row
is **absent from TFREQ's universe** and the leg prints 16/16 on a 17-row sheet. Claim 5's "every decision
row's warrant qid" is therefore an overstatement: TFREQ covers the rows whose qids resolve; the rest are
WARRANT's. Narrowing: say so, or count unresolved rows in `tfreq_total` as failures.

### F6 — MEDIUM: the quoted control output line is not the line the battery prints

Claim (claims.md:66-67) quotes
`CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=7/7`.
Observed (receipt `C2-controls-actual.txt`, EXIT=0, after substituting the real filename — see F1):

```
CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 CARRIED_F1_F4=refused-by-both DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=4/4
```
`PRIOR_REGRESSION=7/7` is printed on a **different** line (`OK regression: FORGERY_REFUSED=7/7
PRIOR_REGRESSION=7/7 rc=1`), and the `CONTROLS` line carries an unclaimed token `CARRIED_F1_F4=refused-by-both`
and the value `4/4`. A token-grep reading is satisfied; a line reading is not. Narrowing: quote the two lines
verbatim, or state "fields appear across the output".

### F7 — LOW: a whitespace-only quote passes QSHAPE and is counted as located

Probe P4b — `| Q8 | S031 | " " |`: `Q_SHAPE_FAIL=0`, `QUOTES_LOCATED=21/21`, `Q_ROWS=21`,
`Q_FLOORS=…provenance-recording-r85.md=8/8 floor7`, refused only by `LEG_FAIL FLOOR` (`short_rows`,
MIN_TOKENS at curation-r92.py:332, 380) — exit 1. Receipt `P4b-quoted-space.txt`. The shape test's emptiness
`not cells[2].strip().strip('"')` (curation-r92.py:223) admits quoted whitespace, and `locates()`'s substring
test (`norm(" ") in cap`) then counts it. Claim 1's "non-empty quote" is not enforced by QSHAPE; the tree is
still refused, but by a leg whose name does not describe the defect. Narrowing: "non-blank quote after
stripping quotes and whitespace".

---

## The five assigned probes, answered

1. **Stray pipe-leading line before the header row.** `quote_lines` reaches it and the header too: P1a
   (`| stray |` inserted before `| qid | source | quote |`) → `Q_SHAPE_FAIL=2`, with
   `Q_SHAPE … cells=1 row=| stray |` **and** `Q_SHAPE … qid=qid row=| qid | source | quote |`;
   `CURATION_R92=FAIL` exit 1. So a stray itself reaches the test, but the real header is demoted into a
   violation — the pass/narrowing is that the header identity is purely positional. Held, with the positional
   caveat that F3 turns into a bypass.
2. **Mined used-by = full path + trailing words.** Exact-token match: P2a (`S026` used-by
   `corpus/knowledge/provenance-recording-r85.md quoted`) → `SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20`,
   `CURATION_R92=PASS` exit 0; P2c (bare basename token) → PASS; P2b (`.md.bak` substring) →
   `USED_BY_OK=18/20`, `LEG_FAIL SOURCE status_fail=0 used_by_fail=2 rows=20`, FAIL exit 1; P2d (a row that
   names r85 with trailing words but is not cited) → `LEG_FAIL USED_BY S018 not cited by
   provenance-recording-r85.md`, FAIL exit 1. Mechanism: `used_by_tokens` splits on
   `[^A-Za-z0-9._/-]+` (curation-r92.py:230) so whitespace and commas drop out and the path stays one token;
   `source_link` accepts `entry in tokens or entry_rel in tokens` (line 240). **Neutral** — wording holds.
3. **Decision row (4 cells) whose warrant qid is not among the quote rows.** WARRANT fires: P3 →
   `WARRANT_OK=16/17`, `WARRANT_UNLINKED … resolved=0/1`, `LEG_FAIL WARRANT`, `LEGS_MEASURED=12/14`,
   `CURATION_R92=FAIL` exit 1. **Neutral**, with F5's denominator note.
4. **Located-quotes row, 3 cells, valid `Qn` and `S-id`, empty quote.** QSHAPE fires: P4a
   (`| Q8 | S031 |  |`) → `Q_SHAPE provenance-recording-r85.md quote=<empty>`, `CURATION_R92=FAIL` exit 1;
   P4c (`| Q8 | S031 | "" |`) → same, exit 1. **Neutral**, with F7's whitespace caveat.
5. **Does `LEGS_MEASURED=14/14` survive a tree where WARRANT fails?** No. P3 → `LEGS_MEASURED=12/14` (WARRANT
   and VERDICT fail); P3d/P3e/P1b/P1c/P1e/P1g → 14/14 only because the row never enters any count. And a tree
   where the legs pass but `fields_hold` fails **cannot exist**: every conjunct of `fields_hold`
   (curation-r92.py:476-492) is also a leg condition (380-470; TFREQ's `tfreq_max<=DF_MAX` is implied by
   `good = [d for d in dfs if 0 < d <= DF_MAX]`, 369), and the VERDICT leg (493-494) is
   `fields_hold and fields_hold == prior_ok`, i.e. false whenever `fields_hold` is false. Hence
   all-14-legs-ok ⟺ `fields_hold` ⟺ `passed` (519). **Held**, but the corollary is the finding: because
   VERDICT mirrors `fields_hold`, `LEGS_MEASURED` cannot detect a *dropped* row — both the leg count and the
   fields stay pristine (F2/F3/F4).

## Residual risk / verification gaps

- Severity of F2/F3 is about *claim honesty and kill rule K4* ("a non-structural row is dropped"), not about a
  false claim entering the scored 20: a dropped row adds nothing to `quotes`, so it cannot inflate a located
  quote. It does hide decision rows from WARRANT/TFREQ entirely (P3d) — that is a scoring escape for the
  Do/Never half of the entry.
- Battery coverage: the four S-classes are real and refused as executed (`FORGERY_REFUSED=4/4`), but S1 and S2
  are insertion-position shapes; P1e and P3e show both class *names* are defeated by forger-controlled first
  cells. The battery's pristine positive is sound.
- Not tested (out of assignment): C1/C3 instruments. Cross-reference observation for the C1 seat: the C1
  statement names `corpus/evidence/round92/control-forgeries-r92.py`, which is likewise MISSING at C5
  (actual: `forgeries-r92.py`, EXIT=2 on the literal path, same defect shape as F1); `skill-tally-r92-controls.py`
  (C3) does exist. Not counted in my verdict.
- No semantic LSP was available/needed: this is Python executed as a script; findings are execution receipts,
  not grep inference. Every claim above is backed by a run and a receipt.

## Trailer

```
VERDICT: R92ReviewerC2 C1 n/a — not my axis; observation recorded that the C1 statement's named
control-forgeries-r92.py is absent at C5 (forgeries-r92.py exists, literal path exits 2).
VERDICT: R92ReviewerC2 C2 fired — the claim's control script is missing (exit 2), an empty first cell is
silently skipped in both tables so the full frozen line reproduces byte-for-byte PASS with forged/undecided
rows (P1b/P1c/P1g/P3b/P3d/P3e), a first-position `qid`-first forgery is swallowed so the S1 class is accepted
(P1e), and the decision-row count/TFREQ denominator measure only surviving rows.
```
