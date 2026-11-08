# R90ExecC2Forge — C2 forgery probe (round 90, wave 1)

Seat `R90ExecC2Forge`, leaf. Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Tree attacked: `9bad12011187d114ba2c4588c5df08a21ab28145` (freeze `8d9893b42eb22690ea5f920ab87fd7e1810b847a`
plus the committed control receipts), extracted with
`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 9bad12011187d114ba2c4588c5df08a21ab28145 | tar -x -C $S`.
Frozen predicates read first: `corpus/evidence/round90/claims.md` and `plans/round-90.md`.

Scratch `/fast/scratch/hyaku/chousa-r90/R90ExecC2Forge`, deleted before yield. `TMPDIR` was never needed
(every `--work` was passed explicitly under the scratch dir); no network, no sudo, no pacman, no tool installs.
`python3 -V` → `Python 3.14.8`. Instrument bytes exercised (sha256, all four equal to the repro seat's reading):

```
28dc1152b0ac1fb67dcca47ff618313c8d2268fecdb5d7967483f8ad128be90a  corpus/evidence/round90/curation-r90.py
58d64f793ad02da910bdf2f6317a4069a8adf1baf9f29d2de903069001a3d10b  corpus/evidence/round90/curation-r90-mutants.py
6f180ec1e3922766a29d5316ed4dd3ea8e37bec40cf9366c94ca0a3ff40eee7c  corpus/evidence/round90/curation-r90-controls.py
2c063f8bfab6922d199546494d2545f495b05ab9350a7379e1b7f4cde8939f4b  corpus/evidence/round89/curation-r89.py
```

## Method

Content trees were mirrored exactly as `curation-r90-controls.py::mirror()` does it (`corpus/SOURCES.md` and the
two entries as real copies; `corpus/captures/` and `corpus/evidence/round57/` symlinked). For a whole-kit run the
mirror also carries `corpus/evidence/round90/{curation-r90.py,curation-r90-mutants.py,curation-r90-controls.py}`
(the committed bytes, or the named forged counter) and `corpus/evidence/round8{7,8,9}` symlinks, so the three
frozen commands are executed out of the attacked tree with `--root .`. Every receipt retains its `# cmd:`,
`# cwd:` and `# exit=` header.

Baseline (clean kit, committed bytes): `clean-counter.txt`, `clean-mutants.txt`, `clean-controls.txt`.

```
CURATION_R90=PASS  … LEGS_MEASURED=10/10 VERDICT fields_hold=1
VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8
MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2   (exit 0)
FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7
CONTROLS=PASS                                                                        (exit 0)
```

The four `t-*` kits below each print the same three blocks byte-for-byte on the forged tree.

---

## F1 — quote-table rows outside the parser's shape are invisible to both counters and to all three commands

**Attack (d): a tree forgery both counters accept, and the frozen kit stays green.** Two shapes; the parsers are
identical in `curation-r90.py:118-146` and `curation-r89.py:186-201`:

* `table_rows(lines, 3)` drops any row whose cell count is not 3 (`if len(cells) != width: continue`), and the
  located-quote loop then drops any row whose first cell is not `Q\d+$` (`if not re.match(r"Q\d+$", cells[0]): continue`).
* Therefore a fabricated row in `## Located quotes` that carries a non-`Q` qid, or a real-looking qid with a fourth
  cell, is neither counted in `total`, nor in `located`, nor in `qids_seen`; `located == total` and the Amendment-6
  qid-set pin both stay true while the entry contains a quote that appears in no capture.

Tree edits (diffs: `tree-diffs.txt`):

```
+ | X1 | S023 | "A sentence that no captured page contains, invented for this fixture." |
+ | Q14 | S023 | "Another invented sentence absent from every capture." | note |
```

Command (cwd = the kit tree; identical in all three kit receipts):

```
python3 -B corpus/evidence/round90/curation-r90.py --root .
python3 -B corpus/evidence/round90/curation-r90-mutants.py --root . --work <scratch>/wk-…
python3 -B corpus/evidence/round90/curation-r90-controls.py --root . --work <scratch>/wk-…
```

Receipts: `t-nonq-row-r90.txt`, `t-nonq-row-r89.txt`, `t-nonq-row-mutants2.txt`, `t-nonq-row-controls.txt`
(and the four `t-fourcell-row-*` files).

Observed (`t-nonq-row-r90.txt`, exit 0; `t-nonq-row-r89.txt`, exit 0):

```
QUOTES_LOCATED=20/20 … LEGS_MEASURED=10/10 VERDICT fields_hold=1
VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8
CURATION_R90=PASS
CURATION_R89=PASS
```

`t-nonq-row-mutants2.txt` (exit 0): `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2`.
`t-nonq-row-controls.txt` (exit 0): `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` + `CONTROLS=PASS`.
`t-fourcell-row-*`: the same five lines with the same exits. So the `Q14` row bypasses the Amendment-6 qid-set pin
through the width filter, and the `X1` row bypasses both the count and the pin through the qid regex; the whole
frozen C2 conjunction reproduces on a tree that fabricated evidence inside the entry it counts.

## F2 — a cited source's status is read by no leg: `mined` → `rejected` leaves the whole kit green

**Attack (c): a registry edit that keeps `DETECTOR_WITNESS=8/8` while moving a real field.** `curation-r90.py`
reads a registry row's status (`cells[7]`) only in the supersession block (`target[7] == "mined"` / `cells[7] ==
"mined"` at `:161-173`). `capture_text()` reads only `cells[1]` (the URL). A row that is merely *cited* by a
knowledge entry is never asked for its status, and its `used-by` cell is never cross-checked against the entry.

Tree edit (`tree-diffs.txt`): S023 — the source of five of entry A's thirteen located quotes (Q9–Q13) and of four
decision rows — flipped from `mined` to `rejected`. Nothing else changes.

Receipts: `t-status-rejected-r90.txt`, `t-status-rejected-r89.txt`, `t-status-rejected-mutants2.txt`,
`t-status-rejected-controls.txt`.

Observed:

```
t-status-rejected-r90.txt: exit 0
  … QUOTES_LOCATED=20/20 … WARRANT_OK=17/17 … LEGS_MEASURED=10/10 VERDICT fields_hold=1
  VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8
  CURATION_R90=PASS
t-status-rejected-r89.txt: exit 0   CURATION_R89=PASS
t-status-rejected-mutants2.txt: exit 0  MUTANTS_KILLED=10/10 … PRIOR_R89_SURVIVORS=2/2
t-status-rejected-controls.txt: exit 0  FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 / CONTROLS=PASS
```

The frozen sentence is reproduced with a rejected row carrying `used-by corpus/knowledge/search-transparency-
reporting-r84.md`; the entry's five S023 quotes are still "located" because the capture hangs off the URL, not the
status.

## F3 — a padding warrant qid is refused only when its quote shares *no* term; one incidental shared word passes

**Attack (c)/(d).** The round-87 A1b defect was "a padding qid whose quote shares nothing with the row passed
beside a good one"; the round-90 rule is one shared distinctive word per named qid
(`shares = all(terms & set(...))`, `curation-r90.py:293-299`). The control battery's `B1b-padding-qid` case adds
`Q3` to the `Q1 (S215)` cell and shares nothing, so it is refused 16/17.

Tree edit (`tree-diffs.txt`): entry B row `Recording a derivation's direction` gains `Q1` beside `Q2` —
`| Q2, Q1 (S215) |`. Q1's quote shares exactly one distinctive word with the row's Do/Never cells: `entities`
(from "compose two unrelated **entities** a derivation").

Receipts: `t-pad-q1-r90.txt`, `t-pad-q1-r89.txt`, `t-pad-q1-mutants2.txt`, `t-pad-q1-controls.txt`.

Observed:

```
t-pad-q1-r90.txt: exit 0
  … WARRANT_OK=17/17 … LEGS_MEASURED=10/10 VERDICT fields_hold=1
  VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8
  CURATION_R90=PASS
t-pad-q1-r89.txt: exit 0   CURATION_R89=PASS
t-pad-q1-mutants2.txt: exit 0  MUTANTS_KILLED=10/10 … PRIOR_R89_SURVIVORS=2/2
t-pad-q1-controls.txt: exit 0  FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 / CONTROLS=PASS
```

The row now cites a quote about provenance chains for a row about derivation direction; `WARRANT_OK` does not move
and no leg names the extra citation. This is the same forgery class `B1b` tests, one shared word away from refusal;
the frozen rule as written ("shares a distinctive content word") is satisfied, so the finding is about rule
strength, not rule violation.

## F4 — the two-directional witness is satisfied by detector bodies that are dead on real input

**Attack (a), K4: "any forced detector body must fail WITNESS" is false for four bodies, each of which passes the
two synthetic assertions and then prints `DETECTOR_WITNESS=8/8` while a real field is wrong.** The four bodies are
in `counter-diffs.txt`; each is a one-body substitution in `curation-r90.py` (no caller change, so named limit 3 is
not used).

| variant | substituted body | witness pair | real-input effect |
|---|---|---|---|
| `forge-a1.py` | `locates`: `if norm(quote) == "date on which the resource was deleted": return False` then `return cap is not None` | fire `locates("date on which the resource", cap)` → True; silent string → False | any quote from a source with a capture is "located"; a fabricated Q10 prints `QUOTES_LOCATED=20/20` |
| `forge-a2.py` | `locates`: `return cap is not None and norm(quote)[-12:] in cap` | fire tail `the resource` ∈ cap → True; silent tail ` was deleted` ∉ cap → False | a fabricated quote whose last 12 characters are replayed from the real quote prints `20/20` |
| `forge-a3.py` | `unentailed_row`: `return len(joined.split()) < 3` | fire joined `"other words"` (2 tokens) → True; silent joined 6 tokens → False | dead on the real entry (`joined` is the whole quote corpus); a decision cell carrying `modification` absent from all quotes prints `UNENTAILED_TERM=0` |
| `forge-a4.py` | `dup_qid`: `return len(qids) > 1 and qids[0] == qids[-1]` | fire `["Q1","Q1"]` → True; silent `["Q1","Q2"]` → False | a non-adjacent duplicate `Q2, Q1, Q1` prints `DUP_QIDS=0` |

Commands and receipts (each forged counter run with `--root .` on the base mirror or on the named tree):

* `forge-a1.py` on the fabricated-Q10 tree: `fake-q10-forge-a1.txt` (exit 0) —
  `QUOTES_LOCATED=20/20 … LEGS_MEASURED=10/10 VERDICT fields_hold=1`, `DETECTOR_WITNESS=8/8`, `CURATION_R90=PASS`.
  The committed counter on the same tree: `fake-q10-committed.txt` (exit 1), `QUOTES_LOCATED=19/20`,
  `LEG_FAIL FLOOR`, `LEGS_MEASURED=8/10`.
* `forge-a2.py` on the replayed-tail tree: `replay-q10-forge-a2.txt` (exit 0) — same frozen lines, `20/20`,
  `DETECTOR_WITNESS=8/8`, `CURATION_R90=PASS`; committed: `replay-q10-committed.txt` (exit 1), `19/20`.
* `forge-a3.py` on the unentailed tree: `a3-unentailed-forged.txt` (exit 0) — `UNENTAILED_TERM=0`,
  `VERDICT fields_hold=1`, `DETECTOR_WITNESS=8/8`, `CURATION_R90=PASS`; committed: `a3-unentailed-committed.txt`
  (exit 1) — `UNENTAILED_TERM=2`, `LEG_FAIL UNENTAILED`, `fields_hold=0`.
* `forge-a4.py` on the `Q2, Q1, Q1` tree: `a4-dup-forged.txt` (exit 0) — `DUP_QIDS=0`, `fields_hold=1`,
  `DETECTOR_WITNESS=8/8`, `CURATION_R90=PASS`; committed: `a4-dup-committed.txt` (exit 1) — `DUP_QIDS=1`,
  `LEG_FAIL DUPQID`.

What the *kit* does with these counters (stated exactly, because it bounds the finding):

* controls battery on the clean content with the forged counter installed: `a1-clean-controls.txt` (exit 0) and
  `a4-clean-controls.txt` (exit 0) print `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` + `CONTROLS=PASS` — the seven
  cases do not exercise the substituted behaviour and stay green.
* mutant battery: `a1-clean-mutants.txt` (exit 2) stops at `SETUP_MISS M6-locate-true: anchor not found`;
  `a4-clean-mutants.txt` (exit 2) stops at `SETUP_MISS M9-dup-dead: anchor not found`. The battery's detection of a
  body edit is its exact source anchor (a setup failure), not `LEG_FAIL WITNESS`; a body written to keep the anchor
  text is not available, but the point stands: `DETECTOR_WITNESS=8/8` is not what refuses these bodies.
* on the fabricated trees themselves the control battery's positive leg refuses (`a3-controls.txt`, exit 1,
  `CASE_DEVIATION POSITIVE: positive not accepted`: the unchanged r89 prior also refuses the tree), so these
  counter states do **not** keep the full three-command conjunction green.

So: the witness itself admits four constant-on-real-input bodies (K4's literal claim), the counter prints the
frozen token set on the forged trees, but the kit as a whole is refused by the battery's anchor and by the r89
prior's independent field checks.

## F5 — `VERDICT fields_hold=1` can be satisfied by a truncated fields_hold plus a constant leg (counter-level)

**Attack (b).** `forge-f1.py` (`counter-diffs.txt`) makes two one-line edits: the `UNENTAILED` leg is
`legs.append(("UNENTAILED", True, …))`, and `and len(unentailed) == 0` is deleted from the `fields_hold`
conjunction. No mutant anchors the `UNENTAILED` leg line or the `fields_hold` expression.

Tree edit (`tree-diffs.txt`): entry A `Recording when a resource changed` Do cell →
`state the modification date of the resource` (`modification` is carried by no located quote).

Receipts: `f1-counter.txt`, `f1-mutants.txt`, `f1-controls.txt`.

```
f1-counter.txt (exit 0):
  … UNENTAILED_TERM=2 … LEGS_MEASURED=10/10 VERDICT fields_hold=1
  VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8
  CURATION_R90=PASS
```

The printed `VERDICT fields_hold=1` is not the value measured over the counter's own ten legs: one leg is a
literal and the conjunct that would have made the verdict false is gone. The kit as a whole does not print the
frozen conjunction, however: `f1-mutants.txt` exits 1 with
`PRIOR_R89_SURVIVORS=1/2` (`KILLED_PRIOR r89-subst-0 rc=1` — the unchanged prior's honest UNENTAILED check
refuses the tree), and `f1-controls.txt` exits 1 with
`CASE_DEVIATION POSITIVE: positive not accepted` (prior rc=1). So F5 is a counter-level verdict-mechanism fire
(`the printed line and the verdict are the same measured value` is false for the unentailed field), not a
whole-kit forgery; the catch is the embedded r89 oracle, not the verdict mutants M2/M3 (both still print KILLED).

---

## Observations, named limits and non-findings

1. **Double-count quirk (pre-existing in r89 and r90):** `curation-r90.py:254-257` tests `unentailed_row()` once
   per `DEFECT_TERMS` entry but appends the loop's `term`; one row is appended twice. Measured on the committed
   counter over the unentailed tree: `UNENTAILED_TERM=2` for one row (`a3-unentailed-committed.txt`,
   `LEG_FAIL UNENTAILED … term=modification; … term=modified`). The leg is pass/fail, so this only inflates the
   printed count; recorded because the carried-field reading of that token is twice the row count.
2. **Quote-content swap is refused, not silently accepted:** swapping Q11's and Q13's quote texts (both `S023`,
   both located) is refused by both counters on `LEG_FAIL WARRANT 15/17` (`swap-q11-q13-r90.txt`, exit 1) because the
   warrant shares are broken; the C2 named limit 2 (qid-set pin guards label identity, not quote content) was not
   needed to explain it.
3. **Named limit 3 (caller substitution) was not used;** every detector attack in F4 substitutes the function body.
   The `capture_text`/`joined`-caller route was deliberately not taken.
4. **The joint instrument/receipt edit** is C1's named limit 1, not touched here.
5. **Scratch deleted:** `/fast/scratch/hyaku/chousa-r90/R90ExecC2Forge` was removed after the receipts below were
   copied to this folder. No host sysctl, service, sudo, pacman, fleet git/jj mutation or network operation was
   performed.

## Retained evidence in this folder

`clean-counter.txt`, `clean-mutants.txt`, `clean-controls.txt`; `tree-diffs.txt`, `counter-diffs.txt`;
`t-nonq-row-{r90,r89,mutants2,controls}.txt`, `t-fourcell-row-{r90,r89,mutants2,controls}.txt`;
`t-status-rejected-{r90,r89,mutants2,controls}.txt`; `t-pad-q1-{r90,r89,mutants2,controls}.txt`;
`fake-q10-{committed,forge-a1}.txt`, `replay-q10-{committed,forge-a2}.txt`;
`a3-unentailed-{committed,forged}.txt`, `a3-{mutants,controls}.txt`, `a4-dup-{committed,forged}.txt`;
`a1-clean-{controls,mutants}.txt`, `a4-clean-{controls,mutants}.txt`;
`f1-{counter,mutants,controls}.txt`; `unentailed-committed.txt`; `swap-q11-q13-r90.txt`;
the forged counter sources `forge-a1.py` … `forge-a4.py`, `forge-f1.py`.

VERDICT: R90ExecC2Forge C2 fired — three tree forgeries (fabricated quote rows outside the parser's Q/3-cell shape, a cited source flipped to `rejected`, and a padding warrant qid sharing one incidental term) reproduce every frozen C2 line including all three commands at exit 0, and the two-directional witness admits four detector bodies that are constant on real input while printing `DETECTOR_WITNESS=8/8`, with the battery's refusal of those bodies being an exact-anchor setup failure rather than `LEG_FAIL WITNESS`.
