# R94RevPrior — BEFORE-state reproduction, C1/C2/C3 (round 94 revenger seat)

Seat `R94RevPrior`, leaf. Lane `chousa-shokunin`. Evidence tree: carrier
`C = 352924bbea624caf3771ef291be98fd4ec679dda`, reached by
`git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin <scratch>/repo` and
`git -C <scratch>/repo checkout C` (S221: a shared clone starts without objects of its own; never repacked).
Every scorer below read bytes from a clone checked out at `C`; no network, no production edits, no lane/fleet git
mutation, nothing installed. Scratch `S=/fast/scratch/hyaku/chousa-r94/R94RevPrior` (removed before yield).
All receipts cited here are copied into this folder as `R94RevPrior-*`.

Scope note: the r93 driver runs are invoked **without `--repo`**, matching the `evidence-before` methodology (its
receipts quote no `RECEIPT SELF_PIN` line); the git-blob legs (`pin_at_rev` / `self_pin`) were therefore not
exercised in this seat. The fresh legs and the disk pin walk were exercised in full.

---

## C1 before — the r93 control driver has no role notion

Fixture: `R94RevPrior-c1-fixture-projection.py` (copied here). `proj34` / `proj32` read the committed 34-row
three-column table, drop the role column, and re-digest the table's own row under r93's minus-self rule; this is
the same projection form `forgeries-r94.py::write_r93` uses (`corpus/evidence/round94/forgeries-r94.py`).
`r93-drop-claims` does that to the r93 two-column table at `C`.

### (a-i) the landed r93 table (23 rows, no role column) scores PASS

Command (cwd `<S>/c1tree`):

```
python3 -B corpus/evidence/round93/control-driver-r93.py verify --root <S>/c1tree --work <S>/c1work/r93-landed \
  --rev 3789608dc8c0eded67f1e5d3840caf0a27522a88 \
  --expected <S>/c1tree/corpus/evidence/round93/controls/expected.tsv \
  --receipts <S>/c1tree/corpus/evidence/round93/controls/receipts \
  --pins <S>/c1tree/corpus/evidence/round93/instrument-pins.txt
```

Receipt `R94RevPrior-c1-r93-landed.out`, rc file `…-c1-r93-landed.rc` = `0`. Observed lines:

```
RECEIPT PINS OK 23/23 pinned files byte-identical RECEIPT_PINS_OK=6/6
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=23/23 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS
```

(The last line of the receipt, `ELAPSED=58.17s`, is the `/usr/bin/time` wrapper, not driver output.) Shape
receipt `R94RevPrior-c1-r93-table-shape.out`:

```
rows with a role column = 0; executed instruments = 5 (['curation-r89-controls.py','curation-r89.py','gate-records-r89.py','mutate-r89.py','harm-recheck-r90.py']); pinned rows = 23
rows not executed by any expected row = 18
```

### (a-ii) the same table with the two round-93 claims rows deleted (21 rows) still scores PASS

```
python3 -B <S>/fixture-c1-projection.py r93-drop-claims <S>/c1tree/corpus/evidence/round93/instrument-pins.txt
```
then the same verify command (cwd `<S>/c1tree`) with `--work <S>/c1work/r93-drop-claims`.

Receipt `R94RevPrior-c1-r93-drop-claims.out`, rc `0`. Observed:

```
RECEIPT PINS OK 21/21 pinned files byte-identical RECEIPT_PINS_OK=6/6
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=21/21 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS
```

Nothing requires the round's claims files to be pinned. This is exactly the `c1-prior-accepts.txt` 21/21 line.

### (a-i') the current 34-row population projected to r93's two-column shape scores 34/34

```
python3 -B <S>/fixture-c1-projection.py proj34 <S>/c1b/corpus/evidence/round94/instrument-pins.txt
```
then (cwd `<S>/c1b`) the same verify with `--rev 41038ed7c40cffc4cf86d649a6ba433c4b9eec1a`,
`--expected …/round94/controls/expected.tsv`, `--receipts …/round94/controls/receipts`,
`--pins …/round94/instrument-pins.txt`, `--work <S>/c1work/proj34`.

Receipt `R94RevPrior-c1-proj34.out`, rc `0`:

```
RECEIPT PINS OK 34/34 pinned files byte-identical RECEIPT_PINS_OK=6/6
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=34/34 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS
```

"The same population at the after-number, with no role read": the r93 driver contains the token `role` **zero**
times (`R94RevPrior-c1-r93-driver-role-tokens.out` = `0`; the r94 driver contains it 55 times), and every data row
of the projection has exactly **2** whitespace fields (`R94RevPrior-c1-projection-field-counts.out` = `2`). The
r93 PASS therefore carries no information about what a row *is*.

### (a-ii') the projected 34-row table with the two r94 claims rows deleted (32 rows) still scores PASS

```
python3 -B <S>/fixture-c1-projection.py proj32 <S>/c1c/corpus/evidence/round94/instrument-pins.txt
```
then the same verify against `<S>/c1c`, `--work <S>/c1work/proj32`.

Receipt `R94RevPrior-c1-proj32.out`, rc `0`:

```
RECEIPT PINS OK 32/32 pinned files byte-identical RECEIPT_PINS_OK=6/6
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=32/32 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS
```

For classification only (direct function calls, no fresh legs; receipt `R94RevPrior-c1-r94-role-report.out`), the
r94 role legs over the **intact** committed table are `codes=[] PIN_ROLES_OK=14/14`, and over the same table with
the two claims rows deleted they are
`codes=['PIN_ROLE_MISSING role=claims path=.ufo/waves/round-94/claims.json', 'PIN_ROLE_MISSING role=claims path=.ufo/waves/round-94/claims.md'] PIN_ROLES_OK=12/12`.
So both (i) and (ii) are defects the r94 claim covers.

### (a-iii) a three-column row is NOT refused with `SETUP malformed pin row` — the brief's premise does not hold

Command (cwd `<S>/c1d`, the committed table untouched):

```
python3 -B corpus/evidence/round93/control-driver-r93.py verify --root <S>/c1d --work <S>/c1work/threecol \
  --rev 41038ed7c40cffc4cf86d649a6ba433c4b9eec1a \
  --expected <S>/c1d/corpus/evidence/round94/controls/expected.tsv \
  --receipts <S>/c1d/corpus/evidence/round94/controls/receipts \
  --pins <S>/c1d/corpus/evidence/round94/instrument-pins.txt
```

Receipt `R94RevPrior-c1-threecol.out`, rc file `…-c1-threecol.rc` = `1`. There is **no** `SETUP malformed pin row`
line and no exit 2. The driver accepts every row and mis-keys it: `read_pins` returns 34 keys, each of the form
`'instrument  corpus/evidence/round89/curation-r89-controls.py'` with `DISK EXISTS: False` and
`SELF ROW PRESENT: False` (receipt `R94RevPrior-c1-read-pins-3col.out`). The verdict lines are:

```
RECEIPT PINS FINDING INSTRUMENT_UNPINNED:corpus/evidence/round89/curation-r89-controls.py,…,PIN_SELF_ROW_ABSENT path=corpus/evidence/round94/instrument-pins.txt,PIN_MISSING path=claims  .ufo/waves/round-94/claims.json,…
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=0/34 RECEIPT_PINS=0/6 CONTROL_DRIVER_R93=FAIL
```

Cause, from the committed parser (`corpus/evidence/round93/control-driver-r93.py:79`, identical at the r93 freeze
`732e6dff…`): `parts = ln.split(None, 1)` — maxsplit 1 always yields two fields for any row with ≥2 whitespace
tokens, so `parts[1]` becomes the whole `"role  path"` string. The `SETUP malformed pin row` message is reachable
only for a line with **fewer than two** fields (or a first field that is not 64-hex). Demonstrated: a pins file
holding the single line `corpus/evidence/round94/make-pins-r94.py` gives
`SETUP malformed pin row: 'corpus/evidence/round94/make-pins-r94.py'` with rc `1` (receipt
`R94RevPrior-c1-onetoken.out` / `.rc`), not the documented setup rc 2.

The reverse direction is deliberate and does refuse at setup: r94's `read_pins` on a two-column row prints
`SETUP PIN_SCHEMA row is not \`<sha256>  <role>  <path>\`: '…'` with `SystemExit: 2` (receipt
`R94RevPrior-c1-r94-read-pins-2col.out`).

### C1 classification

- **(i) role-blindness — the defect C1 covers.** r93 has no role concept at all (0 `role` tokens) and scores the
  same 34-row population 34/34; a row for a file no expected row executes is the same line as an instrument row.
- **(ii) deletable claims rows — the defect C1 covers.** 21/21 at the r93 table and 32/32 on the projected current
  population; the frozen claim's own words are "nothing requires the round's claims to be pinned at all". r94's
  claims role refuses the same 32-row table with `PIN_ROLE_MISSING role=claims` (two codes), which r93 cannot
  express.
- **(iii) three-column vs two-column — a schema difference, not a defect the claim covers.** r94's table is a new
  row schema; r93 cannot represent it. That is why the battery scores a two-column projection. The plan's
  provenance sentence (`plans/round-94.md:66`, "it refuses the three-column row as `SETUP malformed pin row`") is
  contradicted by the committed driver: the observed mechanism is silent acceptance into `"role␠␠path"` keys and
  a 0/34 FAIL, exit 1. The practical conclusion (the projection is required to compare the same population) still
  holds; the stated mechanism and exit class do not. **Finding F1.**

---

## C2 before — r93's punctuation-blind shape leg and `locates()`

Fixture: `R94RevPrior-c2-fixture-punct.py` on a clone at `C` (`<S>/c2tree`), replacing the exact Q2 row of
`corpus/knowledge/search-transparency-reporting-r84.md`
(`| Q2 | S214 | "date when each source was last searched or consulted." |`) with `| Q2 | S214 | "—" |` (dash tree)
or `| Q2 | S214 | "..." |` (dots tree). Clean baselines first, both trees restored with
`git -C <S>/c2tree checkout -- corpus/knowledge/search-transparency-reporting-r84.md`.

Clean tree: `R94RevPrior-c2-clean-r93.out` rc `0` (`CURATION_R93=PASS`, `VERDICT fields_hold=1 legs_ok=15/15
DETECTOR_WITNESS=13/13`) and `R94RevPrior-c2-clean-r94.out` rc `0` (`CURATION_R94=PASS`,
`VERDICT fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=17/17`). The counters discriminate on the same bytes.

Commands (cwd `<S>/c2tree`):

```
python3 -B corpus/evidence/round93/curation-r93.py --root <S>/c2tree
python3 -B corpus/evidence/round94/curation-r94.py  --root <S>/c2tree
```

### dash tree

`R94RevPrior-c2-dash-r93.out` rc `1`:

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=19/20 Q_ROWS=19 Q_SHAPE_FAIL=0 Q_WSQUOT=0 SOURCE_STATUS_OK=19/19 USED_BY_OK=19/19 Q_FLOORS=search-transparency-reporting-r84.md=12/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=16/17 TFREQ_OK=16/16 TFREQ_MAX_DF=3 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=12/15
LEG_FAIL FLOOR search-transparency-reporting-r84.md=12/13 floor13,provenance-recording-r85.md=7/7 floor7
LEG_FAIL WARRANT 16/17 width_fail=0 count_bad=0
LEG_FAIL VERDICT fields_hold=0 legs_ok=12/14
CURATION_R93=FAIL
```

Downstream legs that fired: **FLOOR** (r84 entry 12/13 against floor 13) and **WARRANT** (16/17), plus the
VERDICT leg; `Q_SHAPE_FAIL=0` — the shape leg never sees the punctuation cell because the cell is non-empty.
`Q_PUNCTQUOT` does not exist in r93.

The full r93 stdout also carries three diagnostic lines the `evidence-before` capture filtered out
(`TEACHES_FLAGGED S024 …`, `WARRANT_UNLINKED … row=Reporting when a source was searched warrant=Q2 (S214)
resolved=0/1`, and a non-`LEG_FAIL` `VERDICT fields_hold=0 legs_ok=12/15 DETECTOR_WITNESS=13/13`); they are in the
receipt and do not change any cited value.

`R94RevPrior-c2-dash-r94.out` rc `1`, same tree, same bytes: `Q_SHAPE_FAIL=1 Q_PUNCTQUOT=1`, and

```
Q_SHAPE search-transparency-reporting-r84.md quote=<punctuation> row=| Q2 | S214 | "—" |
LEG_FAIL QSHAPE search-transparency-reporting-r84.md quote=<punctuation>
LEG_FAIL PUNCTQUOT search-transparency-reporting-r84.md Q2
CURATION_R94=FAIL
```

r94 names the class that r93 could only refuse downstream.

### dots tree

`R94RevPrior-c2-dots-r93.out` rc `1` — the same r93 field values, `Q_SHAPE_FAIL=0`, `QUOTES_LOCATED=19/20`,
`LEG_FAIL FLOOR`, `LEG_FAIL WARRANT`, `CURATION_R93=FAIL`. `R94RevPrior-c2-dots-r94.out` rc `1` —
`Q_SHAPE_FAIL=1 Q_PUNCTQUOT=1`, `Q_SHAPE … quote=<punctuation> row=| Q2 | S214 | "..." |`,
`LEG_FAIL PUNCTQUOT`, `CURATION_R94=FAIL`.

### `locates()` has no punctuation guard in r93

`R94RevPrior-c2-locates-defs.out` (grep of the committed bytes at `C`):

```
corpus/evidence/round93/curation-r93.py:210:def locates(quote, cap):
corpus/evidence/round93/curation-r93.py-211-    return cap is not None and norm(quote) in cap
corpus/evidence/round94/curation-r94.py:219:def locates(quote, cap):
corpus/evidence/round94/curation-r94.py-220-    """A punctuation-only quote is never a located quote (round 94) …
corpus/evidence/round94/curation-r94.py-222-    return cap is not None and bool(PUNCT_RE.search(quote)) and norm(quote) in cap
```

`R94RevPrior-c2-locates-behavior.out` (modules loaded from committed bytes):

```
quote='—' cap='before — after' r93=True r94=False
quote='...' cap='wait ... really' r93=True r94=False
quote='a real quote' cap='before a real quote after' r93=True r94=True
```

r93's substring test "locates" an em dash or dots in any capture that contains them; r94 refuses both and still
locates a real quote.

---

## C3 before — r93's declared tail multiset accepts a moved tally

Literal (committed, `corpus/evidence/round93/skill-tally-r93.py:155`; receipt `R94RevPrior-c3-tail-declared.out`):

```
    TAIL_DECLARED = {("215", "0"): 1, ("283", "0"): 1}
```

vs r94's owner-bound declarations (`corpus/evidence/round94/skill-tally-r94.py:166-169`):

```
    TAIL_OWNED = (
        (("215", "0"), 1, "Round27 repair/status correction"),
        (("283", "0"), 1, "Round 37 — the claim-pin provenance"),
    )
```

Fixture `R94RevPrior-c3-fixture-move.py` on `<S>/c3tree` (clone at `C`): deletes the exact line
`` `PASS (215 cases, 0 skipped)` under the host UTF-8 locale; original187 `` from under
`### Round27 repair/status correction — 2026-10-21` (SKILL.md line 640 in the clean tree) and re-inserts the same
bytes under `### Round 36 — the engine-swap canary and per-record attribution (2026-10-23)` (clean-tree line 718).
Clean placement receipt: `R94RevPrior-c3-tail-placement-clean.out`; after the move the line is at 719.

Commands (cwd `<S>/c3tree`):

```
python3 -B corpus/evidence/round93/skill-tally-r93.py --root <S>/c3tree --selftest <S>/c3tree/corpus/evidence/round94/controls/selftest-r94.txt
python3 -B corpus/evidence/round94/skill-tally-r94.py  --root <S>/c3tree --selftest <S>/c3tree/corpus/evidence/round94/controls/selftest-r94.txt
```

Clean tree calibration: `R94RevPrior-c3-clean-r93.out` rc `0` (`TAIL_OK=1`, `SKILL_TALLY_R93=PASS`) and
`R94RevPrior-c3-clean-r94.out` rc `0` (`TAIL_OWNED_OK=2/2`, `TAIL_OK=1`, `SKILL_TALLY_R94=PASS`).

Moved tree, `R94RevPrior-c3-moved-r93.out` rc `0`:

```
TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_TALLIES=2 OTHERS_OK=1 TAIL_OK=1 LEGS=4/4
SKILL_TALLY_R93=PASS
```

Same bytes under r94, `R94RevPrior-c3-moved-r94.out` rc `1`:

```
TAIL_OWNER_FINDING TAIL_OWNER_MISMATCH tally=215 cases tally=PASS (215 cases, 0 skipped) owner=### Round 36 — the engine-swap canary and per-record attribution (2026-10-23) declared=Round27 repair/status correction
TALLY_ROWS=8 … TAIL_OWNED_OK=1/2 … TAIL_OK=0 LEGS=3/4
LEG_FAIL TAIL declared={('215', '0'): 1, ('283', '0'): 1} observed={('215', '0'): 1, ('283', '0'): 1}
SKILL_TALLY_R94=FAIL
```

A moved tally leaves `TAIL_OK=1` at rc 0 under r93 and is refused by r94 by owner, with the multiset unchanged.

---

## Comparison with `corpus/evidence/round94/evidence-before/*.txt`

`R94RevPrior-before-line-comparison.out` checks every non-comment, non-timestamp line of the three before files
against my receipts: **`DIFFS=0`**.

| before file | cited line(s) | result |
|---|---|---|
| `c1-prior-accepts.txt` | `RECEIPT PINS OK 23/23 … RECEIPT_PINS_OK=6/6`; `… PINNED_FILES=23/23 … CONTROL_DRIVER_R93=PASS` | MATCH |
| `c1-prior-accepts.txt` | `RECEIPT PINS OK 21/21 …`; `… PINNED_FILES=21/21 … CONTROL_DRIVER_R93=PASS` | MATCH |
| `c1-prior-accepts.txt` | `rows with a role column = 0; executed instruments = 5 ([…]); pinned rows = 23` | MATCH (identical list order and formatting) |
| `c2-prior-accepts.txt` | the full `SUPERSEDED_LIVE=… LEGS_MEASURED=12/15` line; `LEG_FAIL FLOOR …`; `LEG_FAIL WARRANT 16/17 …`; `LEG_FAIL VERDICT fields_hold=0 legs_ok=12/14`; `CURATION_R93=FAIL`; rc `1` | MATCH |
| `c3-prior-accepts.txt` | the full `TALLY_ROWS=8 … LEGS=4/4` line; `SKILL_TALLY_R93=PASS`; rc `0` | MATCH |

Precision note, not a disagreement: the 23-row "as landed" table at the base/carrier is the r93 freeze's 17-row
table plus the six round-93 receipt rows added at the r93 carrier (`git diff 3789608d C --
corpus/evidence/round93/instrument-pins.txt` adds exactly those six rows and re-digests the self row). The before
receipt scores the table as landed, which is what my clone at `C` carries.

---

## Findings

**F1 (deviation, material to C1 provenance).** The seat brief's item (iii) and `plans/round-94.md:66` state that
the r93 driver refuses a three-column pins row as `SETUP malformed pin row`. Committed bytes do not do that.
Exact command and receipt: `R94RevPrior-c1-threecol.out` / `.rc`, command at §(a-iii); observed
`PINNED_FILES=0/34 RECEIPT_PINS=0/6 CONTROL_DRIVER_R93=FAIL`, exit `1`, with the rows mis-parsed into
`"role␠␠path"` pin keys (`R94RevPrior-c1-read-pins-3col.out`). The message is reachable only for a line with
fewer than two fields: `SETUP malformed pin row: 'corpus/evidence/round94/make-pins-r94.py'`, exit `1`
(`R94RevPrior-c1-onetoken.out` / `.rc`). This does not weaken the projection argument — the unprojected r93 run
still cannot score the table (0/34, FAIL) — but the plan's `## Mistakes` row records the wrong mechanism and exit
class, and a claim that quotes it would be quoting an unrun behaviour. Classification is unchanged: the
two-column/three-column mismatch is a schema difference, not a defect C1 covers.

**F2 (environment note for the integrator, out of seat scope).** At the lane root, `git rev-parse HEAD` is
`6ae736ea` (wave spec) and `git status --porcelain` shows ` M corpus/evidence/round94/forgeries-r94.py` plus
untracked `.ufo/waves/round-94/w1.ready.dispatched`. My checks read only the committed bytes of a clone at `C`;
I did not read, score, or write the modified worktree file.

---

VERDICT: R94RevPrior C1 held — both before defects reproduce exactly (23/23 and 21/21 on the landed r93 table, 34/34 and 32/32 on the projected current population, with no role read), while the brief's third item is a schema difference whose stated `SETUP malformed pin row` mechanism the committed r93 driver does not exhibit (it mis-parses the row and scores 0/34 at exit 1; finding F1).
VERDICT: R94RevPrior C2 held — on my own dash and dots trees r93 prints `Q_SHAPE_FAIL=0` and refuses only downstream (`LEG_FAIL FLOOR` 12/13, `LEG_FAIL WARRANT` 16/17) with an unguarded `locates()` that returns True for `"—"` and `"..."` in any capture, exactly as claimed, while r94 names the class (`Q_PUNCTQUOT=1`, `quote=<punctuation>`, `LEG_FAIL PUNCTQUOT`).
VERDICT: R94RevPrior C3 held — r93's literal `TAIL_DECLARED = {("215","0"):1,("283","0"):1}` passes the moved 215 tally with `TAIL_OK=1` at rc 0, exactly as claimed, while r94 refuses the same bytes with `TAIL_OWNER_MISMATCH` and `TAIL_OK=0`.
