# R89ReviewerC1 — C1 wording vs. instrument (round 89)

Seat: `R89ReviewerC1`. Scope: C1 `C1-BATTERY-R89` only. Bytes attacked: archive of
`ac0a0892c15de11fb28d3208f2b287687c00477e` (`git archive | tar -x` into the seat scratch), plus the live
lane worktree for the drift comparison. No network, no production edit, no git/jj mutation.
Scratch `/fast/scratch/hyaku/chousa-r89/R89ReviewerC1` (removed before yield). Tooling: nothing installed;
Python 3.14.8. All receipts under `w1/R89ReviewerC1/`; every forged/variant instrument kept byte-identical
under `w1/R89ReviewerC1/variants/`.

## 0. Baseline — the predicate holds, on the freeze archive and on the live tree

```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin; S=/fast/scratch/hyaku/chousa-r89/R89ReviewerC1
mkdir -p $S/tree $S/w-c1 && git -C $L archive ac0a0892c15de11fb28d3208f2b287687c00477e | tar -x -C $S/tree
python3 -B "$L/corpus/evidence/round89/gate-records-r89.py" --root "$L" --repo "$L" --work "$S/w-c1"
python3 -B "$L/corpus/evidence/round89/mutate-r89.py" --root "$L" --repo "$L" --work "$S/w-mut"
python3 -B "$S/tree/corpus/evidence/round89/gate-records-r89.py" --root "$S/tree" --repo "$L" --work "$S/w-arch"
```

- `predicate-pass.txt` — exit `0`; `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362
  EXPECTED_CODE=362/362 … DIV3=3 D1_REFUSED=3/3 … MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1
  LEGS_MEASURED=15/15`; `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16`;
  `GATE_RECORDS_R89=PASS`. Every enumerated predicate field is present with the frozen value.
- `mutate-pass.txt` — exit `0`; `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2 EQUIVALENT_ON_TREE=0/0
  TOTAL=13/13`. All four round-88 survivor shapes die with the claimed named lines: `E7c` → `UNRECONCILED
  D1_WIDTH detail=3/3/1 pin3` + `UNRECONCILED D2_WIDTH`; `E7b` → `UNRECONCILED MUT_ADMIT detail=derived=0
  killed=0` + `UNRECONCILED MUT_UNREACH`; `E7d` → `UNCROSSCHECKED D1_WIDTH … DIV3=1 pin=3/3` (×2);
  `E7f` → `UNCROSSCHECKED D1_WIDTH … D1_EXPECTED=4 DIV3=3`.
- `archive-tree-counter.txt` — the freeze archive reproduces the same line and `PASS`, exit `0`: the predicate
  is a property of the frozen bytes, not of the live worktree.
- Pins: every `instrument-pins.txt` row matches its file (`f34f59c8…` counter, `10b43d8a…` mutants,
  `3c3768ad…` harm) and `tools/gate-records.py` is `905f9da2…` at `f8fa55ec`, at `ac0a0892` and on disk —
  the subject tool is unchanged, as the claim states.
- Harm: `archive-tree-harm.txt` — `HARM_RECHECK files=13 records=29 moved=0 base_rc=0 r88_rc=0`, exit `0`,
  with `--base-tool` = the `f8fa55ec:tools/gate-records.py` blob (sha `905f9da2…`). On the live worktree
  (`harm2.txt`) `files=14 records=31 moved=0`, exit `0` — the extra file/2 records are the untracked
  `corpus/lessons/round-89.md` (not in the freeze commit; `git cat-file -e ac0a0892:corpus/lessons/round-89.md`
  → absent). No genuine record moves on either tree.

## 1. Findings, by severity

### F1 — MEDIUM — `LEGS_MEASURED` is a printed summary field bound to nothing; a one-point counter edit forges it and `GATE_RECORDS_R89=PASS` survives (K4 third clause; the sentence's fourth survivor shape)

C1's sentence says the fourth shape the round-88 wave left alive — "a printed field detached from its
measurement" — dies with a named `UNRECONCILED`/`UNCROSSCHECKED` line. The guard that kills `E7f` is the
`crosscheck()` map, and the map has no entry for the one printed cell that summarises the legs: `LEGS_MEASURED`.

```sh
# variants/legs-measured-14of15.py: only the rendered cell changes
-                  f"LEGS_MEASURED={sum(1 for _, ok, _ in legs if ok)}/{len(legs)}")
+                  f"LEGS_MEASURED=14/15")
python3 -B $S/lg-legs-measured-14of15/gate-records-r89.py --root $L --repo $L --work $S/w-lg-legs-measured-14of15
```

- `legs-measured-forge.txt` (`variants/lg-legs-measured-14of15.py`) — exit `0`; `… DERIVE_NEG=1 LEGS_MEASURED=14/15`; `LEG_REREAD=16/16 RECONCILED=16/16
  CROSSCHECK=15/15 LEGS_APPENDED=16`; `GATE_RECORDS_R89=PASS`. No `UNRECONCILED`, no `UNCROSSCHECKED`.
- Same with `LEGS_MEASURED=0/15`: exit `0`, `PASS`, and the SUMMARY leg's own receipt still reads
  `SUMMARY=ok detail=15/15` — **two printed totals that should agree (15/15 vs 0/15) coexist under PASS.**
- The one-field-at-a-time sweep (`probe2.py`, `probe-crosscheck.txt`) changes each of the 20 printed cells and
  records which leg catches it: 19 are caught; `change LEGS_MEASURED (15/15->16/15) caught by []`. The
  crosscheck map reads exactly `summ.get("TOOL")` plus `_ints` over `D1_EXPECTED D1_FORGES DIV3 D1_REFUSED
  D2_FORGES D2_REFUSED POSITIVE FRESH_POSITIVE FORGED_REFUSED EXPECTED_CODE EMPTY_REFUSED RC SETUP DERIVE_NEG`
  and the dynamic `MUT_{ADMIT,UNREACH}_{DERIVED,KILLED}` — `LEGS_MEASURED` is the only hole.
- `mutate-r89.py` has no mutant of this shape (`E7f` forges `D1_EXPECTED`), so `MUTANTS_KILLED=11/11` does not
  cover it: the battery's `E7f` is instance-specific while the sentence's fourth shape is field-generic.

Frozen kill rule **K4** reads: "the predicate is met by an instrument that skips the claimed work: … or a
summary field that disagrees with the leg it summarises." Here the predicate is met (`PASS`, exit 0) by an
instrument whose printed `LEGS_MEASURED` disagrees with the legs and the SUMMARY leg it summarises. That is the
K4 shape, so C1 is falsified as written. Scope of the fire: **only** this cell — the tool-binding, the
per-format reconciliation, the cross-check of the other 19 cells, and both tool mutants all hold.

### F2 — MEDIUM — the frozen counting command cannot produce the predicate's `moved=0`: `$W/base-tool.py` is never created

`claims.md` C1 "Counting command" line 3 (and `claims.json` `predicate.harm_stdout = ["moved=0"]`):

```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin; W=/fast/scratch/hyaku/chousa-r89/c1
mkdir -p "$W" && python3 -B "$L/corpus/evidence/round89/gate-records-r89.py" --root "$L" --repo "$L" --work "$W"
python3 -B "$L/corpus/evidence/round89/mutate-r89.py" --root "$L" --repo "$L" --work "$W"
python3 -B "$L/corpus/evidence/round89/harm-recheck.py" --root "$L" --repo "$L" --base-tool "$W/base-tool.py"
```

Nothing in the command sequence writes `$W/base-tool.py`. Run verbatim, with a fresh `$W`:

- `harm-counting-command-verbatim.txt` — exit `1`; `HARM_RECHECK files=14 records=31 moved=31 base_rc=2
  r88_rc=0`, with 31 `HARM … ABSENT() -> OK()` lines. `moved=0` is unreachable from the frozen command.
- The recipe that does work is the `expected.tsv` `c1-harm` row (`git show master:tools/gate-records.py >
  …/base-tool.py`); I reproduced `moved=0` that way (`archive-tree-harm.txt`, `harm2.txt`, exit 0). `master:`
  exists and yields the same blob (`905f9da2…`).

So the claim is true but its own counting command is not the one that verifies it; an operator running the
frozen three lines gets a FAIL on the harm conjunct. This is a reproducibility defect in the frozen predicate
set, not a measurement hole.

### F3 — LOW — "every round-88 field unchanged" is literally false: `LEGS=` was renamed to `LEGS_MEASURED=`, and the counter still prints the old name on its fail path

`field-diff.txt` (extracted from both counters' summary `print` templates):

```
R88: TOOL POSITIVE FRESH_POSITIVE FORGED_REFUSED EXPECTED_CODE EMPTY_REFUSED RC SETUP D1_EXPECTED D1_FORGES
     D1_REFUSED D2_FORGES D2_REFUSED MUT_ADMIT_DERIVED MUT_ADMIT_KILLED MUT_UNREACH_DERIVED
     MUT_UNREACH_KILLED DERIVE_NEG LEGS
R89: … D1_EXPECTED D1_FORGES DIV3 D1_REFUSED … DERIVE_NEG LEGS_MEASURED
R89-R88 = ['DIV3','LEGS_MEASURED']   R88-R89 = ['LEGS']
```

- `DIV3` and `LEGS_MEASURED` are additions (fine; `DIV3` is the cross-check witness the claim names).
- `LEGS` is **removed**, not preserved: the round-88 `LEGS={sum(ok)}/{EXPECTED_LEGS}` became
  `LEGS_MEASURED={sum(ok)}/{len(legs)}` — a different expression (constant denominator → live leg count) under
  a different name.
- The counter is internally inconsistent about the name: the tool-absent branch still prints
  `TOOL=absent D1_EXPECTED=3 D1_FORGES=3 D2_FORGES=3 LEGS=0/16` (`tool-absent-in-tree.txt`, exit `1`), while the
  healthy branch prints `LEGS_MEASURED=15/15`. Anything that parses `LEGS=` (round-88's contract, and that
  fail line) sees the field only on the failure path.

The claim's parenthetical enumeration (`POSITIVE`, `FRESH_POSITIVE`, `FORGED_REFUSED=EXPECTED_CODE`,
`D1_REFUSED`, `D2_REFUSED`, `MUT_ADMIT_KILLED`, `MUT_UNREACH_KILLED`, `DERIVE_NEG`) is satisfied in full; the
universal quantifier over "every round-88 field" is what fails.

### F4 — LOW — named limit 1's first sentence names the wrong edit surface (its boundary claim is exact)

Limit 1: "A counter edit that jointly rewrites the leg writer, the receipt files and the reconciliation
survives — that edit *is* the counter. … forging both the detail and the `ok` coherently is caught only
because the summary still carries the measured `DIV3`; forging that too is a joint rewrite."

- Reproduced the second half exactly: `variants/cl-e7d-plus-summary-DIV3.py` = `div3 = 1` + both width `ok`s
  detached + both details forged to `3/3/3 pin3` + the summary's `DIV3` rendered as `{ROWS_203}`. Result
  (`c-limits.txt`, section `e7d-plus-summary-DIV3`): exit `0`, `DIV3=3`, `LEG_REREAD=16/16 RECONCILED=16/16
  CROSSCHECK=15/15`, `PASS`. And without the summary forge the same shape dies solely on
  `UNCROSSCHECKED D1_WIDTH … DIV3=1 pin=3/3` + `UNCROSSCHECKED D2_WIDTH …` (`c-limits.txt`, section
  `e7d-forged-detail-only`, exit `1`). So "forging that too is a joint rewrite [and survives]" is
  **exactly right**.
- What is not exact: the surviving edit never touches "the leg writer, the receipt files [or] the
  reconciliation". Receipts are rendered by `write_leg` from the leg tuples, so forging the tuple's `ok` and
  `detail` *is* forging the receipt; the reconciliation then agrees by construction. The real boundary is
  "an edit that forges a measurement and every rendering of it", which is a strictly larger and cheaper class
  than the sentence's enumeration. Direction of the error: the limit **understates** how little machinery a
  surviving edit needs.

### F5 — LOW — named limit 2's "skips the whole measurement block" is wider than the code

Limit 2: "A tree where the tool is absent skips the whole measurement block and fails on `LEG_REREAD`."

`tool-absent-in-tree.txt` (archive tree with `tools/gate-records.py` deleted), exit `1`:

```
TOOL=absent D1_EXPECTED=3 D1_FORGES=3 D2_FORGES=3 LEGS=0/16
UNCROSSCHECKED TOOL detail=tool present TOOL=- want=absent
LEG_REREAD=0/2 RECONCILED=2/2 CROSSCHECK=0/1 LEGS_APPENDED=2
LEG_FAIL TOOL tool present
LEG_FAIL SUMMARY 0/1
GATE_RECORDS_R89=FAIL
```

- The operative claim is exact: it fails on `LEG_REREAD=0/2`, the structural guard, as stated.
- "The whole measurement block" is not skipped: the four width derivations still execute and print
  (`D1_EXPECTED=3 D1_FORGES=3 D2_FORGES=3`) because they never call the tool. Only the tool-run block is
  skipped. The limit overstates the blankness of the fail path.

### F6 — INFO — `CROSSCHECK=15/15` is agreement, not goodness, and two conjuncts are redundant

- A leg can be `ok=False`, honestly reconciled and cross-checked: `c-limits.txt` section `E7b-measure-zeroed-only` (zeroed mutant
  measurements, legs untouched) prints `LEG_REREAD=14/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16`
  and `FAIL`. This matches the claim's wording ("each leg's re-derived numbers must equal the fields the
  summary printed for it"), but the tally must not be read as "15 legs verified good" — only `all(ok)` and
  `LEG_REREAD` carry that.
- `DERIVE_NEG`'s crosscheck conjunct `nums[0]==nums[1]` is implied by `rederive` (which already returns
  `a==b`); it can never add information.
- `TOOL`'s summary cell is the **literal** `'present'` (`f"TOOL={'present'}"`), not a rendering of
  `tool_present`; the crosscheck binds it to a second `os.path.isfile` call, so the forge is caught, but the
  cell is the one printed field that is a constant.
- `rederive`'s `n/m` branch is `re.match` (prefix), not `re.fullmatch`: `"3/3 x"` re-derives `(3,3)`/True
  (`probe-rederive.txt`). That is *required* for FRESH's `"0/5 FRESH_BUILD=FAILED"` detail, and the claim's
  grammar list ("an `n/m` detail requires `n == m`") does not claim exhaustiveness, so this is a tolerance, not
  a deviation.

### F7 — INFO — the sixteenth leg is load-bearing, but its own re-derivation is self-referential

Both asked experiments, run separately (`a-loadbearing.txt`, variants under `variants/`):

| variant | edit | observed (exit / lines) |
|---|---|---|
| `var-no-receipt.py` | `DERIVE_NEG` receipt never written (`E7g` shape) | `1`; `UNRECONCILED SUMMARY detail=14/14 receipt_ok=False rederived=True`; `LEG_REREAD=14/15 RECONCILED=14/16 CROSSCHECK=14/14 LEGS_APPENDED=16`; `LEG_FAIL SUMMARY 14/14`; `FAIL` |
| `var-setup-detached.py` | `setup_ok` forced `0` **and** `SETUP`'s `ok` forced `True` | `1`; `UNRECONCILED SETUP detail=0/1 receipt_ok=True rederived=False`; `LEG_REREAD=16/16 RECONCILED=15/16 CROSSCHECK=15/15`; `FAIL` |
| `lb-no-summary-leg.py` | SUMMARY leg deleted entirely | `1`; `LEG_REREAD=15/15 RECONCILED=15/15 CROSSCHECK=15/14 LEGS_APPENDED=15`; `FAIL` |
| `lg-no-summary-receipt.py` | SUMMARY's own receipt never written | `1`; `LEG_REREAD=15/15 RECONCILED=15/16 CROSSCHECK=15/14 LEGS_APPENDED=16`; `FAIL` |

`SUMMARY` is not self-recomputing: a missing receipt shrinks `len(reread)` and `cross_ok` and the leg's `ok`
goes False while its rendered `n/m` stays a true fraction, which is exactly the `UNRECONCILED` line. Two
residual notes: (i) `SUMMARY`'s `detail` is rendered from `cross_ok/len(reread)`, the same two values its `ok`
compares, so its re-derivation can only detect receipt/detail divergence — never measurement truth; the
independent teeth are the `len(reread) == EXPECTED_LEGS - 1` conjunct, `LEG_REREAD`, and `all(ok)`.
(ii) On the two paths where a receipt is missing, `CROSSCHECK` prints a numerator above its own denominator
(`15/14`) — a nonsense diagnostic on a FAIL path.

## 2. Answers to the four direct questions

**(a) `RECONCILED=16/16` — is the sixteenth leg load-bearing, or does the count recompute itself?**
Load-bearing, on both tests asked. Removing one receipt changes the verdict through three independent counts
(`LEG_REREAD=14/15`, `RECONCILED=14/16`, `LEG_FAIL SUMMARY`), and detaching one leg's `ok` while its detail
still records the measurement (`SETUP 0/1` with `ok=True`) is caught by `RECONCILED=15/16` alone. The leg's
own detail is a rendering of the count it checks, so its reconciliation is self-referential — but it cannot
launder a missing receipt, because `cross_ok` drops with `len(reread)` and the two then disagree.

**(b) `CROSSCHECK=15/15` — which summary fields are compared, which are not, and is any check vacuous?**
Compared (19 cells): `TOOL`, `POSITIVE`, `FRESH_POSITIVE`, `FORGED_REFUSED`, `EXPECTED_CODE`, `EMPTY_REFUSED`,
`RC`, `SETUP`, `D1_EXPECTED`, `D1_FORGES`, `DIV3`, `D1_REFUSED`, `D2_FORGES`, `D2_REFUSED`, `MUT_ADMIT_DERIVED`,
`MUT_ADMIT_KILLED`, `MUT_UNREACH_DERIVED`, `MUT_UNREACH_KILLED`, `DERIVE_NEG`. **Not compared: `LEGS_MEASURED`**
(F1). No check compares a field to itself: every `crosscheck` reads a summary cell and compares it to a number
re-derived from the receipt text, and the sweep proves each of the 19 can fail. The honest caveat is that the
receipt text and the summary cell are both rendered from the same live variables in the same process, so the
comparison detects an edit that breaks one rendering (the `E7c`/`E7d`/`E7f` class), not measurement truth —
which is named limit 3. `D1_EXPECTED` and `DIV3` are each read by both width legs (doubly bound, not vacuous).
`SUMMARY` is excluded from the crosscheck loop by construction (`CROSSCHECK={cross_ok}/{len(reread)-1}`).

**(c) The three named limits — counterexample built for each.**
1. **Limit 1** — boundary reproduced exactly: `E7d` dies only because the summary carries the measured `DIV3`;
   forging that cell too (`variants/cl-e7d-plus-summary-DIV3.py`, where `div3 = 1` internally) yields
   `PASS`, exit `0` (`c-limits.txt`). The limit's *consequence* is exactly right; its edit-surface enumeration is too narrow (F4).
2. **Limit 2** — reproduced: tool absent from the tree → `LEG_REREAD=0/2`, exit `1` (`tool-absent-in-tree.txt`).
   The guard is exactly as advertised; "skips the whole measurement block" overstates it (F5).
3. **Limit 3** — reproduced twice (`c-limits.txt`): `honest-constant-div3` (`div3 = ROWS_203`, no
   derivation at all) and `honest-constant-d1` (`d1_expected = ROWS_203`) both print honestly and `PASS`
   (exit `0`), proving agreement-only. The limit is also not *wider* than reality in
   the useful direction: a wrong constant that moves the number is caught by the pin (`wrong-constant-moves-number`, `ROWS_203 = 1` → exit `1`,
   `LEG_FAIL D1_WIDTH 3/3/3 pin1`, `LEG_FAIL D2_WIDTH`). So the wording "a leg computed from a wrong constant
   and printed honestly passes" is true precisely for constants that still agree with the measurement, which is
   what the sentence means; no deviation found.

**(d) Round-88 field set unchanged?** No, literally: `DIV3` and `LEGS_MEASURED` are added and `LEGS` is
renamed away (`field-diff.txt`). Every field the claim enumerates is present with the frozen value, and the
absent-tool path still prints `LEGS=0/16` (F3).

## 3. Residual risk / verification gaps

- I attacked the counter's *guard map*, not its measurement expressions; a jointly consistent forgery of a
  measurement and all of its renderings survives by design (limit 1, F4) and I did not attempt to enumerate
  that class.
- `LEGS_MEASURED` is cosmetic in the predicate (`claims.json` does not require it), so F1's practical exposure
  is a false printed tally at `PASS`, not a wrong tool verdict. I rate it MEDIUM on that basis; a reader who
  treats K4 as covering only per-leg cells would downgrade F1 to a sentence-wording defect, but it does not
  become a pass either way.
- I did not run `controls/run-controls.sh`: its `expected.tsv` rows write receipts into
  `corpus/evidence/round89/controls/receipts/` (tracked bytes, no production edits allowed). I verified the
  same rows individually instead, with my own `--work` dirs, and all of them reproduce (`predicate-pass.txt`,
  `mutate-pass.txt`, `archive-tree-harm.txt`, `archive-tree-counter.txt`). The `c1-harm` row's recipe works;
  the `claims.md` counting command does not (F2).
- The live worktree differs from the freeze by untracked `corpus/lessons/round-89.md` (and modified
  `LOG.md`/`SCORECARD.md`/`corpus/QUALITY.md`/`plans/round-89.md`, not C1's concern); the counter's predicates
  reproduce on both, so the drift moves no C1 field.
- The `CROSSCHECK=15/14` diagnostic (F7) is only reachable on a FAIL path and does not affect any verdict.

VERDICT: R89ReviewerC1 C1 fired — the predicate, the 11/11+2/2 battery and all four named survivor shapes hold at `ac0a0892`, but K4 is met: the printed `LEGS_MEASURED` cell is bound to nothing and a one-point counter edit forges it to `0/15` while `GATE_RECORDS_R89=PASS` exits 0, and the claim's own counting command cannot produce the `moved=0` harm conjunct it requires.
