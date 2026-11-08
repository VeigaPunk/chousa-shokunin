# R91ReviewerC2 — C2 (calibration) wording-vs-code review

Seat `R91ReviewerC2`, lane chousa round 91. Frozen claim `C2-CURATION-R91` at freeze **F3 `4d00d7519290569879f853d7122b82a927cda1f3`**,
tree attacked **carrier C3 `67954adc599bd605705d94a1ea7abb582491a907`** (clone:
`git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo && git -C $S/repo checkout 67954adc…`).
`S=/fast/scratch/hyaku/chousa-r91/R91ReviewerC2`; every tree/fixture under `$S`; scratch deleted before yield.

Method: the claim's words, item by item, against `corpus/evidence/round91/curation-r91.py` as executed. Each forgery is applied to a
minimal mirror of the tree the two counters read (`corpus/SOURCES.md`, the two routed entries, `corpus/captures` symlink, `corpus/evidence/round57`
symlink — the same mirror `curation-r91-controls.py:43-53` builds), built by `$S/probe*.py`; every observed line below is from a real run.
The lane was not edited; nothing was written outside `S` and `.ufo/waves/round-91/w1/`.

No LSP server answered a Python file for this lane (`lsp` has no Python server registered here), so all caller/definition checks are
literal reads of the counter plus executable reproducers — recorded as a verification gap, not presented as semantic proof.

## Baseline: the predicate reproduces exactly at C3

```
$ cd $S/repo && python3 -B corpus/evidence/round91/curation-r91.py --root .
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_ROWS=20 Q_SHAPE_FAIL=0
SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,
provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TFREQ_OK=17/17 TFREQ_MAX_DF=3 DUP_QIDS=0 TEACHES_CHECKED=1
TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=13/13
VERDICT fields_hold=1 legs_ok=13/13 DETECTOR_WITNESS=11/11
CURATION_R91=PASS      exit 0
```
receipt `R91ReviewerC2-receipts/clean-r91.txt`. Every field the C2 sentence pins is reproduced (`LEGS_MEASURED=13/13 Q_ROWS=20 Q_SHAPE_FAIL=0
SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 TFREQ_OK=17/17 TFREQ_MAX_DF=3 UNENTAILED_TERM=0 WARRANT_OK=17/17 DUP_QIDS=0
VERDICT fields_hold=1 DETECTOR_WITNESS=11/11`).

```
$ python3 -B repo/corpus/evidence/round91/curation-r91-controls.py --root repo --work $S/ctl      exit 0
OK positive: r90 CURATION_R90=PASS r91 CURATION_R91=PASS
OK nonq-row / status-rejected / used-by-blank / ubiquitous-warrant: r91 FAIL (LEG_FAIL QSHAPE / SOURCE / SOURCE / TFREQ), r90 PASS
OK duplicate-count: r90 UNENTAILED_TERM=2 r91 UNENTAILED_TERM=1
OK regression: FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 rc=0
CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7
```
receipt `R91ReviewerC2-receipts/controls-r91.txt` — the C2 item-5 line reproduces character for character at C3.

K3's write clause holds: `sha256sum` of `corpus/SOURCES.md` and both entries is unchanged after a counter run over the mirror
(`sha256sum -c before.sha` → 3 × `OK`, exit 0; no file added), receipt `R91ReviewerC2-receipts/k3-no-write.txt`. The counter opens read-only.

## Findings

### HIGH — F1. A `## Located quotes` data row whose first cell the filter dislikes is dropped *before* QSHAPE; the tree passes

Claim text (claims.md C2 item 1): “**every data row of `## Located quotes`** is a `Q<n>` row with exactly three cells … (`QSHAPE`)”;
machine K4: “the pass skips the work: **a non-`Q` row is dropped**”.

Code: `curation-r91.py:133`
```python
if cells and (cells[0] in ("Situation", "qid", "") or set(cells[0]) <= set("-: ")):
    continue
```
`data_lines()` is shared by both sections and runs *before* `q_shape_violation()`, so the R1 repair ("a row outside the shape is dropped
by `continue` BEFORE the row is counted") is applied one layer too late: the row is dropped before the shape check exists.

Reproducer (harness `probe.py::a2b`, `probe4.py`): insert one data row in `provenance-recording-r85.md` before `## Decision table`:

| injected row | r91 result |
|---|---|
| `\| \| S023 \| "Date on which the resource was changed." \|` (empty qid) | `CURATION_R91=PASS Q_SHAPE_FAIL=0 Q_ROWS=20 LEGS_MEASURED=13/13` **exit 0** |
| `\| : \| S023 \| "Date on which the resource was changed." \|` | `CURATION_R91=PASS Q_SHAPE_FAIL=0 Q_ROWS=20 LEGS_MEASURED=13/13` **exit 0** |
| `\| Situation \| S023 \| "Date on which the resource was changed." \|` | `CURATION_R91=PASS Q_SHAPE_FAIL=0 Q_ROWS=20 LEGS_MEASURED=13/13` **exit 0** |

Command: `python3 -B repo/corpus/evidence/round91/curation-r91.py --root $S/work/A2b-empty-qid` (mirror built by `probe.py::mirror`).
Receipt `R91ReviewerC2-receipts/probe-A1-A10.txt`, `R91ReviewerC2-receipts/probe-firstcell.txt`.
`curation-r90.py` also accepts these (`CURATION_R90=PASS`, exit 0) — inherited, not a regression, but the item-1 wording claims the class closed.

**Classification: falsifies wording; K4 fires as machine-written.** The predicate is “data row”, the code reads “pipe-leading line whose
first cell is not one of `Situation`/`qid`/empty/all-`-: `”.
**Narrowing to record:** either (a) exempt only the literal header row and separator in `data_lines`, and let every other pipe-leading
line reach `q_shape_violation` in the Located-quotes section; or (b) narrow item 1 to “every pipe-leading line whose first cell is not
`Situation`, `qid`, empty, or dash-only”.

### HIGH — F2. `table_rows(…, 4)` silently discards decision rows of any other width; a row carrying **both** defect terms passes clean

Claim text (item 4): “**one decision row carrying a defect term that no quote carries is appended once**, with the term it carries”;
docstring leg 5: “no decision-table cell carries a frozen defect term that no located quote carries”.

Code: `curation-r91.py:141` — `if len(cells) != width: continue`. Nothing pins the decision table's width or row count; QSHAPE
(leg 2) covers only `Located quotes`.

```
$ python3 -B repo/corpus/evidence/round91/curation-r91.py --root $S/work/A7-five-cell        exit 0
CURATION_R91=PASS … UNENTAILED_TERM=0 … WARRANT_OK=17/17 TFREQ_OK=17/17 … LEGS_MEASURED=13/13
```
row injected before `## Inference` in `provenance-recording-r85.md`:
`| Recording a modified resource | state the modified value | leave the modified value unstated | Q13 (S023) | extra |`
— five cells, both defect terms in Do/Never, no quote carries either. `UNENTAILED_TERM=0`, exit 0. The three-cell variant
(`| Recording a modified resource | state the modified value | Q13 (S023) |`) is identical: PASS, `UNENTAILED_TERM=0`.
A decision row with an **empty first cell** carrying both terms (`| | state the modification of the value | record the modified value |
Q13 (S023) |`) also passes (`probe4.py`), the F1 filter and the width filter composing.
Receipts `R91ReviewerC2-receipts/probe-A1-A10.txt`, `R91ReviewerC2-receipts/probe-firstcell.txt`. r90 accepts all three as well.

**Classification: falsifies wording** — “appended once” is observed as appended **zero** times, and the row is a decision-table row.
**Narrowing to record:** extend QSHAPE (or a pinned per-entry decision-row count with a width check) to the decision table; state that
item 4 holds only over 4-cell decision rows.

### HIGH — F2b. No decision-row count is pinned: deleting a curated row still prints PASS with a smaller denominator

```
$ python3 -B repo/corpus/evidence/round91/curation-r91.py --root $S/work/A9-row-deleted   exit 0
CURATION_R91=PASS … WARRANT_OK=16/16 TFREQ_OK=16/16 … LEGS_MEASURED=13/13
```
(one legitimate `provenance-recording-r85.md` decision row removed; receipt `R91ReviewerC2-receipts/probe-A1-A10.txt`). Moving the same row under
`## Inference` gives the same PASS. So the sentence's own `WARRANT_OK=17/17 TFREQ_OK=17/17` is a property of the clean tree, not of the
counter: a forged tree prints 16/16 and passes. Only the quote side is pinned (`QID_SETS`, `FLOORS`).
**Classification: neutral on the sentence, finding on the enforcement** — item 3's “every decision row” is vacuously true when the row is
gone. **Narrowing to record:** pin the decision-row count per entry the way `QID_SETS` pins qids, and require equality.

### MEDIUM — F3. `used-by` “names the entry” is a substring test on the basename; a different file with the same basename satisfies it

Claim text (item 2): “a registry row with `status=mined` **whose `used-by` names the entry**”.

Code: `curation-r91.py:199` — `return cells[7] == "mined", (entry in used or entry_rel in used)`, `entry = os.path.basename(entry_rel)`
(free-text cell, index 10; header confirmed at `corpus/SOURCES.md:9-10`).

```
$ python3 -B repo/corpus/evidence/round91/curation-r91.py --root $S/work/A3_prior         exit 0
CURATION_R91=PASS … SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 … LEGS_MEASURED=13/13
```
With `corpus/knowledge/stale/provenance-recording-r85.md` present on disk (a real sibling copy) and S031's `used-by` set to
`corpus/knowledge/stale/provenance-recording-r85.md` — a **different file**, same basename — `USED_BY_OK=20/20`. Setting it to the
sentence `not used in provenance-recording-r85.md` is also accepted (`USED_BY_OK=20/20`, exit 0). Receipt `R91ReviewerC2-receipts/probe-A3-prior.txt`,
`R91ReviewerC2-receipts/probe-A1-A10.txt`. The four controls' `used-by-blank` case empties the cell only, so `FORGERY_REFUSED=4/4` does not cover this class.
**Classification: falsifies wording.** **Narrowing to record:** tokenise the `used-by` cell (split on `,`/`;`/whitespace, strip anchors)
and require a path whose normalised form equals the entry path or its basename; or state that `used-by` is a substring test.

### MEDIUM — F4. The frozen document's measured `df` values are wrong (`source` df 7, `resource` 6/20)

Item 3 says “at least one content term whose document frequency … is `<= 3` (`TFREQ`, the measured maximum over the legitimate rows)” and
item 5 names “a warrant sharing only `source`, df 7”; `curation-r91.py:67` says “here `source`, df 7”, `:14` says “`resource`, document
frequency 6/20”.

Measured with the counter's own doc units on the pristine mirror (`probe2.py`, `dfvariants.py`; ENTRY_A = 13 located quotes + 11 decision
rows = 24 docs):

| unit | docs | df(source) | df(resource) |
|---|---|---|---|
| coded (`quotes + "Do Never"` per row) | 24 | **5** | **8** |
| quotes + Do and Never as separate docs | 35 | 5 | 10 |
| quotes only | 13 | 1 | 4 |
| row Do cells only | 11 | 3 | 4 |
No unit definition produces 7 or 6/20. `provenance-recording-r85.md`: df(source)=2, df(resource)=5.
Receipt `R91ReviewerC2-receipts/probe-dfvariants.txt`.

The predicate survives — 5 > `DF_MAX=3` — and attack 4 still discriminates: widening `| Q3 (S214) |` to `| Q3 (S214), Q2 (S214) |`
(Q2 shares only `source` with that row) gives
```
$ python3 -B repo/corpus/evidence/round91/curation-r91.py --root $S/work3/A4b        exit 1
LEG_FAIL TFREQ 16/17 max_df=3<=3
```
with `WARRANT_OK=17/17` — TFREQ fires for that qid while WARRANT stays silent, exactly as item 3 asserts. Receipt `R91ReviewerC2-receipts/probe-A4p-A5p-prior.txt`.
**Classification: falsifies the parenthetical, not the predicate.** **Narrowing to record:** replace 7/6 with the measured 5/8 (or say
“df 5, above DF_MAX”), so the frozen margin is stated against the tree the counter reads.

### LOW — F5. TFREQ's denominator excludes rows citing an unresolved qid (the sentence's “every decision row” is measured on fewer)

Code: `curation-r91.py:314` — `if qids and len(resolved) == len(qids): tfreq_total += 1`.
```
$ … --root $S/work/A6-unresolved-qid        exit 1
CURATION_R91=FAIL … WARRANT_OK=16/17 TFREQ_OK=16/16 … LEG_FAIL WARRANT 16/17
WARRANT_UNLINKED … warrant=Q7 (S031), Q99 (S031) resolved=1/2
```
On the clean tree `tfreq_total = 17 = 11 + 6` = every decision row, so `TFREQ_OK=17/17` is honest at landing; but the TFREQ *leg* passes
with `16/16` on the forged tree because the offending row is out of scope for that leg (WARRANT catches it). Receipt
`R91ReviewerC2-receipts/probe-A1-A10.txt`. **Classification: neutral (covered by WARRANT) with a narrowing** — say “every decision row whose cited qids
all resolve”, and note the denominator is not pinned (F2b).

### LOW — F3b. `source_link` is not witnessed; `DETECTOR_WITNESS=11/11` does not cover the detector with the hole

`curation-r91.py:160` comment: “Named detectors: each is exercised in both directions by `witness()`.” The `witness()` list (`:203-218`)
holds 11 assertions over `locates` (2), `unentailed_terms` (2), `teaches_miss` (2), `dup_qid` (2), `q_shape_violation` (3) — and **zero**
over `source_link`, the R2 repair's own predicate and the one F3 falsifies. `11 = 2+2+2+2+3`.
**Classification: neutral on the number (`11/11` is literally true), finding on the sentence it implies.** The two-direction discipline was
not applied to the leg that carries a substring leniency. **Narrowing to record:** add `source_link` fire/silent assertions (accepted
basename, refused sibling path, refused negated text) and let the count follow.

### LOW — F6. Item 4's unit is (row, term); the single-term probe does not cover a two-term row

```
$ … --root $S/work3/A5b        exit 1
UNENTAILED search-transparency-reporting-r84.md row=Recording a modified resource term=modification
UNENTAILED search-transparency-reporting-r84.md row=Recording a modified resource term=modified
UNENTAILED_TERM=2
```
One row carrying both unentailed terms appends two records, each labelled with **its own** term (the R4 defect — one record labelled
twice with the loop's label — is gone). `DUPCOUNT_R91=1` for the single-term probe reproduces. Receipt `R91ReviewerC2-receipts/probe-A4p-A5p-prior.txt`.
**Classification: neutral.** **Narrowing to record:** item 4 should say “one record per (row, term)”, not “appended once”, and the witness
should carry a two-term case. (Note this row also fails WARRANT/TFREQ because `Q13`'s quote shares no term; that is unrelated and correct.)

### LOW — F7. Item 4 reads only the Do/Never cells; a defect term in the Situation cell is invisible

`A11`: a decision row whose *Situation* cell reads “Recording a modified resource when it changed”, with no unentailed term in Do/Never →
`CURATION_R91=PASS … UNENTAILED_TERM=0 WARRANT_OK=17/17 TFREQ_OK=17/17`, exit 0 (receipt `R91ReviewerC2-receipts/probe-cells0.txt`). r90 behaves the same.
**Classification: neutral** (a scenario label is not an assertion of practice) **with a narrowing:** the sentence says “one decision row
carrying a defect term”, the code says “the row's Do/Never cells carry it” (`unentailed_terms`, `:154-157`).

### LOW — F8. Item 1's scope is broader than “data row”: any pipe-leading line in the section is a row

```
$ … --root $S/work/A2-prose-pipe        exit 1
LEG_FAIL QSHAPE provenance-recording-r85.md cells=1
Q_SHAPE provenance-recording-r85.md cells=1 row=| see Q3 above for the derivation wording
```
A prose line beginning with `|` inside `## Located quotes` **is** counted and refused (`cells=1`), so the seat's attack 2 answers
“counted”, and the direction is stricter than the claim, not more lenient. Consequence: a documentation prose edit that starts a line with
`|` turns a green tree red — a false-positive class that K3's “the clean tree's PASS changes” would report as the counter's fault.
Receipt `R91ReviewerC2-receipts/probe-A1-A10.txt`. **Classification: neutral; wording understates the code.** **Narrowing to record:** say “every
pipe-leading line in the section”.

## Answer table for the six named attacks

| # | attack | observed | class |
|---|---|---|---|
| 1 | `\| Q14 \| S023 \| "x" \| extra \|` in `## Located quotes` | `exit 1`; `LEG_FAIL QSHAPE provenance-recording-r85.md cells=4`; `Q_SHAPE_FAIL=1`; row also leaves `total` so `Q_ROWS` stays 20 | **holds** (falsifies a lenient reading only) |
| 2 | prose line starting `\|` in `## Located quotes` | `exit 1`; `LEG_FAIL QSHAPE … cells=1` — counted, and refused | neutral, *stricter* than “data row” (F8) |
| 3 | `used-by` names a sibling file with the same basename / a negation | `exit 0`, `CURATION_R91=PASS`, `USED_BY_OK=20/20` | **falsifies item 2** (F3) |
| 4 | row with two qids, one sharing only `source` | `exit 1`; `LEG_FAIL TFREQ 16/17` with `WARRANT_OK=17/17` | predicate **holds**; the “df 7” parenthetical is wrong — measured df 5 (F4) |
| 5 | row carrying both defect terms | `exit 1`; two `UNENTAILED` records, `term=modification` and `term=modified`, `UNENTAILED_TERM=2` | neutral; unit is (row, term) (F6) |
| 6 | `tfreq_total` and unresolved qids | clean tree `TFREQ_OK=17/17` = 11+6 decision rows; with `Q99` cited: `TFREQ_OK=16/16`, `WARRANT_OK=16/17` | rows with unresolved qids are **not** counted (F5) |

Additional, outside the six: a non-`Q` quote row whose first cell is empty/`:`/`Situation` passes (F1, K4-named); decision rows of width
≠ 4 are dropped and a row carrying both defect terms passes (F2); a curated decision row deleted or moved passes at `16/16` (F2b).

## Residual risk

- All three HIGH findings are **inherited** from r90 (`CURATION_R90=PASS` on each fixture): the r91 sentence promises “every data row” and
  “no decision-table cell”, which r90 never promised, so the wording is the new risk even where the code is not.
- Beyond the claim's five named limits, the unclosed classes are: (i) first-cell filtering of both tables; (ii) decision-table width and row
  count unpinned; (iii) `used-by` substring matching; (iv) `source_link` unwitnessed.
- F2/F2b mean the printed `WARRANT_OK`/`TFREQ_OK` denominators are diagnostic, not constraining: any receipt reader should treat
  `17/17` as a clean-tree property, not as a count the counter enforces.

## Verification gaps

- No LSP server for Python in this environment: caller/definition checks are literal code reads at the cited lines plus executable
  reproducers; no semantic reference query was possible.
- The clean-tree and controls runs were executed against a `git clone --shared` at `67954adc…`; the C3 receipts were not re-derived (C1's
  predicate, not C2's, pins them), so the C2 sentence was scored against the bytes in the clone only.
- `curation-r91.py` derives `df` from located quotes plus 4-cell decision rows; the “df 7 / 6-of-20” prose was not reproduced under four
  unit definitions, so its origin is unknown rather than explained.

## Tooling

No install or upgrade was performed (nothing was needed; `python3`, `git`, coreutils sufficed). No network request made.

## Receipts (copied into this wave folder)

- `R91ReviewerC2-receipts/clean-r91.txt`, `R91ReviewerC2-receipts/controls-r91.txt`, `R91ReviewerC2-receipts/k3-no-write.txt`
- `R91ReviewerC2-receipts/probe-A1-A10.txt`, `R91ReviewerC2-receipts/probe-df.txt`, `R91ReviewerC2-receipts/probe-A4p-A5p-prior.txt`, `R91ReviewerC2-receipts/probe-firstcell.txt`,
  `R91ReviewerC2-receipts/probe-cells0.txt`, `R91ReviewerC2-receipts/probe-dfvariants.txt`, `R91ReviewerC2-receipts/probe-A3-prior.txt`
- harnesses: `R91ReviewerC2-receipts/harness/probe.py`, `probe2.py`, `probe3.py`, `probe4.py`, `probe5.py`, `dfvariants.py`

VERDICT: R91ReviewerC2 C2 fired — item 1 (a `|`-row with an empty/`:`/`Situation` first cell is dropped before QSHAPE and the tree passes:
`Q_SHAPE_FAIL=0`, exit 0 — the machine's K4-named class), item 2 (`used-by` is a basename substring test: a stale sibling copy or a
negation prints `USED_BY_OK=20/20`), and item 4 (a 5-cell or empty-first-cell decision row carrying both defect terms prints
`UNENTAILED_TERM=0` and PASS) are falsified as written, while the pinned numbers, the four controls, the write-free path, TFREQ's
discrimination for a `source`-only qid, and the one-record-per-term repair all hold.
VERDICT: R91ReviewerC2 C1 n/a — not this seat's claim; the driver, forgeries and six receipts were not exercised.
VERDICT: R91ReviewerC2 C3 n/a — not this seat's claim; `skill-tally-r91.py` and its prose controls were not exercised.
