# R89CriticClaims — falsification of C1 and C2 (round 89)

Seat: R89CriticClaims (godspeed). Lane: chousa round 89, L1 ChousaR89. Base f8fa55ec (round-88 landing + non-author spot-check). Freeze commit ac0a0892 (carries both counters, batteries, receipt driver, pins). Trees built at both revisions under scratch; live repo used for landing predicates. No network, no commits, no edits outside `.ufo/waves/round-89/w1/R89CriticClaims/` + scratch (deleted before yield).

Axes: (1) do-nothing test — would a stdout scorer accept an artifact that skips the claimed work? (2) claim-vs-instrument gap — which clause has no enforcing artefact? (3) prior-round survivors — do E7b/E7c/E7d/E7f now die on r89 and live on r88?

## Method

Trees: `S=/fast/scratch/hyaku/chousa-r89/R89CriticClaims`; `git archive <rev> | tar -x` at f8fa55ec (base) and ac0a0892 (freeze); live repo for landing runs (freeze bytes identical — pins verified with `sha256sum -c` at end). Every claim below names command + receipt + observed line + exit.

## Landing predicates (read-only)

- `python3 -B $L/corpus/evidence/round89/gate-records-r89.py --root $L --repo $L --work $W` on live repo: exit 0, `GATE_RECORDS_R89=PASS`, `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16`, round-88 fields unchanged (`POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=EXPECTED_CODE=362/362`, `D1_REFUSED=3/3 D2_REFUSED=3/3`, `MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1`, `DIV3=3`). Receipt: `.ufo/waves/round-89/w1/R89CriticClaims/c1-live.txt`.
- `mutate-r89.py`: exit 0, `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2 TOTAL=13/13`. Receipt: `c1-mutants.txt`.
- `curation-r89.py`: exit 0, `CURATION_R89=PASS`, 9 legs, `DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0`, `VERDICT fields_hold=1` (seen via LEG detail `fields_hold=1 legs_ok=8/8` on the VERDICT leg; summary field is the leg detail).
- `curation-r89-controls.py`: exit 0, `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7`. Receipt: `c2-controls.txt`.
- `curation-r89-mutants.py`: exit 0, `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1`. Receipt: `c2-mutants.txt`.
- `harm-recheck.py`: `moved=0`, exit 0. Tool sha256 `905f9da2…` identical at base and freeze (`git show <rev>:tools/gate-records.py | sha256sum` both `905f9da2fdf2…`). Registry diff base→freeze is exactly the two `used-by` cells: S216 gained `corpus/evidence/round89/claims.md`, S218 gained `corpus/evidence/round89/claims.md` (`git diff f8fa55ec ac0a0892 -- corpus/SOURCES.md`, 2 lines only). So C1-K1/K2/C2-K1/K3's registry arm HOLDS on live bytes — no predicate miss to falsify. The attacks below target K4 (skip-work) and clause-wording gaps, which is where a critic seat fires.

## (a) The do-nothing test

### a1. Echo wrapper (C1 and C2) — ACCEPTED by a stdout scorer, blocked only by instrument pins

Artifact: `do-nothing-c1.py` (7 lines): prints the frozen C1 summary + `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16` + `GATE_RECORDS_R89=PASS`, exit 0. A scorer that reads stdout alone accepts it. What stops it: `instrument-pins.txt` sha256 — the wrapper's sha256 is `0f3e317e…`, the pin for `gate-records-r89.py` is `f34f59c8…` (mismatch). The pin check is a wave/scribe step, NOT part of the counter's stdout. K4's "echo/printer replacement" clause therefore names an enforcer — the pin file — but that enforcer lives outside the counter. Verdict: **no fire** — K4's printer arm is enforced, but a lens claim "the counter rejects an echo wrapper" would be false-wordsed; the claim text says "(the instrument sha256 pins … are the check)" which is accurate. `mutate-r89.py` re-executes the counter from source each time, but a replaced file on disk would equally be re-executed — the defense is purely the pin comparison. A do-nothing counter whose legs are all constants with honest details is a different question — see a3.

### a2. Counter that runs the prior instrument and reprints its fields — ACCEPTED until the new fields are read

- C1: `gate-records-r88.py` on this tree prints `GATE_RECORDS_R88=PASS` exit 0 (`c1-prior-instrument.txt`) but prints NO `CROSSCHECK` field and NO `DIV3`. A scorer reading only for the round-88 field set accepts the prior instrument. The r89 predicate requires `CROSSCHECK=15/15` and `DIV3=3`, which the prior instrument cannot print — the do-nothing is defeated by the predicate's new fields, not by any in-counter guard. If a reprint wrapper emitted the r88 line plus the two forged fields, only the pins stop it (same as a1).
- C2: `curation-r88.py` on this tree prints `CURATION_R88=PASS` exit 0 (`c2-prior-instrument.txt`, reproduced exactly: `WARRANT_OK=17/17 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7`) with no `DUPQID` leg and no field-derived verdict. Same structure: defeated only by the predicate's new tokens (`DUP_QIDS=0` present, `SUP_CLAUSE_CHECKED=0`, `VERDICT fields_hold=1`).

### a3. Counter whose legs are all constants with honest details — KILLED in r89, and this is the K4 core

The substantive do-nothing: measurements run (or not) but each leg's `ok` is a constant `True` while its receipt detail still carries the measured number. r89's `rederive()` (lines 636–656) re-derives the verdict from the detail *per grammar*: `n/m` requires `n==m`; `len/d1/div3 pinN` requires all four equal (pin ≤ `ROWS_203` is not required by `rederive` alone — the four-equal bound comes from the width leg body `len(d1)==d1_expected==div3==ROWS_203` and the `crosscheck` pin arm `pin==ROWS_203`); `derived=x killed=y` requires both `==1`; `tool present` requires `os.path.isfile(tool)`. A constant-`ok` leg with an honest *failing* detail (`3/3/1 pin3`, `derived=0 killed=0`, `0/15`) gives `rederived != got_ok` → `UNRECONCILED` → `GATE_RECORDS_R89=FAIL`. A constant-`ok` leg with an honest *passing* detail on a healthy tree passes — but there is no measurement failure to hide, so nothing is skipped; the leg's agreement check is satisfied. The K4 attack must therefore *combine* a broken measurement with a detached `ok` — exactly what E7b/E7c do (multi-point edits), and exactly what dies in `c1-mutants.txt`. The r88 counter accepted this class because `rederive` only parsed `detail=(\d+)/(\d+)`, so `3/3/1 pin3` read as `3/3` and `derived=0 killed=0` fell to the tautology `n_ok = got_ok and ok`.

For C2 the same shape: a leg constant-`True` while `TEACHES_FLAGGED=0` (dead detector) prints PASS on r88 (probe `curation-r88-both.py`: detector killed + TEACHES leg forced `True` → `TEACHES_FLAGGED=0 … CURATION_R88=PASS`, exit 0 — receipt `probe-r88-dead-detached.txt`). On r89 the same joint edit prints `TEACHES_FLAGGED=0 … LEG_FAIL VERDICT fields_hold=0 legs_ok=8/8 CURATION_R89=FAIL`, exit 1 — receipt `probe-r89-dead-detached.txt`. The difference is `fields_hold` (lines 305–316), computed from the printed tallies, plus the `VERDICT` leg requiring `fields_hold == all(ok)`. Note the r88 dead-detector-ALONE proof: killing the detector without detaching the leg already FAILS on r88 (LEGS=6/7, `CURATION_R88=FAIL`) — so r88's hole was the *detachment*, not the dead detector per se, which matches routed defect 3's wording (`verdict was all(ok)`).

Boundary (joint rewrite, K4's own Named Limit 1): forging the detail AND the `ok` AND the summary field jointly survives r89 — probe `probe-joint`: `div3=1`, width details rewritten to `3/3/3 pin3`, summary `DIV3=3` → `GATE_RECORDS_R89=PASS`, exit 0 (receipt `probe-joint.txt`). The claim discloses this as a named limit ("forging that too is a joint rewrite"), so this is a confirmed tradeoff, not a fire. The falsification-ledger reading: K4 cannot fire on a joint rewrite because the rewrite *is* the counter; the writer/receipt/reader agreement is what is enforced, not measurement truth (Named Limit 3).

## (b) Claim-vs-instrument gap — per clause

What enforces each clause (artefacts: `gate-records-r89.py` line refs from freeze tree, `curation-r89.py` line refs, battery `mutate-r89.py` / `curation-r89-controls.py` / `curation-r89-mutants.py`, `instrument-pins.txt`):

**C1:**
| Clause | Enforcing artefact | Status |
|---|---|---|
| `GATE_RECORDS_R89=PASS` exit 0 with `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16` | `passed` conjunction lines 736–740 (counts + `summary_leg_ok` + `all(ok)`); `SUMMARY` leg appended lines 718–719 forces 16 = 15 measurement legs + summary | enforced — PASS only if every conjunct holds |
| `n/m` detail requires `n==m` | `rederive` lines 644–654 + agreement test lines 708–712 (`UNRECONCILED`) | enforced |
| `len/d1/div3 pinN` requires all four equal | `rederive` lines 640–643 (`a==b==c==pin`) | enforced for the leg |
| `pin == ROWS_203` | `crosscheck` line 668 — but ONLY as a *summary-vs-detail* agreement (`pin` from detail vs `ROWS_203` constant). If both `pin` in detail and the constant were lowered together, pass — but `ROWS_203=3` is itself pinned by the measurement body line 584 (`len(d1)==d1_expected==div3==ROWS_203`) and by the width-forgery batteries. The clause artefact is shared; no circularity beyond the disclosed joint-rewrite limit | enforced (with disclosed boundary) |
| `derived=x killed=y` both 1 | `rederive` lines 645–648 + `crosscheck` MUT arm lines 670–675 | enforced |
| `tool present` requires the tool to be a file | `rederive` lines 649–651 returns `tool_present = os.path.isfile(tool)`; absent-tool short-circuit line 607 prints `TOOL=absent … LEGS=0/16` and FAILs on `LEG_REREAD` | enforced — filesystem, not numeric (Named Limit 2, disclosed) |
| Re-derived numbers equal summary fields (`DIV3` printed for this reason) | `crosscheck` lines 657–682 compares every leg's nums to parsed summary tokens (`summ` from line 618); `UNCROSSCHECKED` printed on mismatch; `SUMMARY` leg requires `cross_ok == len(reread) == 15` | enforced |
| `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2` | `mutate-r89.py` `COUNTER_MUTANTS` (11, incl. the 4 E7 shapes) + `TOOL_MUTANTS` (2); each run's verdict must be non-PASS | enforced |
| Round-88 fields unchanged | Freezing is certified by `instrument-pins.txt` + `sha256sum -c` (all 9 pinned files + tool OK at end of run) and by the live summary line matching round-88 `POSITIVES/15, FRESH 5, FORGED 362/362` etc. | enforced extrinsically (pins) — in-counter, only via the summary line |
| `DIV3` is printed for cross-check | Line 597 `DIV3={div3}` in summary + crosscheck arm line 666 | enforced |

`falsifies-wording` candidates (clause with NO artefact, narrowed property): NONE found in C1. Every clause maps to code. One near-miss: the sentence "each leg's re-derived numbers must equal the fields the summary printed *for it*" — for `FRESH`, the detail carries trailing `fresh_err` text but `rederive` matches only the leading `n/m` (`re.match` line 652), and `crosscheck` maps FRESH→`FRESH_POSITIVE` (line 678). If `fresh_err` were nonempty while `fresh_ok==5`, `FRESH` detail would be `5/5 <err>` → `rederive` reads `5==5` → True, and `ok = fresh_ok==5 and not fresh_err` → False → `UNRECONCILED`. Safe direction. But if a counter printed `fresh_ok==5` with `ok=True` *detached from the `not fresh_err` term*, detail `5/5 <err>` re-derives True and crosscheck `FRESH_POSITIVE=5/5` agrees → PASS despite a non-empty `fresh_err`. Is there such an edit in the mutant battery? No — `mutate-r89.py` has no FRESH-detachment mutant. This is a genuine residual: the FRESH `ok` has a *conjunctive* condition (`fresh_ok==5 and not fresh_err`) but `rederive` only checks the numeric half. The sentence claims "each leg's receipt detail is re-derived in its own grammar" — for FRESH the grammar captures only the count, not the error flag. Is this `falsifies-wording`? The narrower property the instrument enforces: "FRESH's numeric count agrees receipt↔detail↔summary". A detached-`fresh_err` edit survives. Severity: low (the `fresh_err` originates from an in-process exception string `str(e)` line 425; an edit detaching `ok` from it requires touching the same line region the battery's M5/E4 shapes already cover with killed variants — but no battery entry exercises it). I mark this as a residual gap, not a K4 fire, because K4 requires "predicate met by an instrument that skips the claimed work" — here the claimed work (FRESH positive acceptance count) is still measured; only the error-flag conjunct is unchecked.

**C2:**
| Clause | Enforcing artefact | Status |
|---|---|---|
| `CURATION_R89=PASS` exit 0, 9 legs | `passed` line 318: `len(legs)==EXPECTED_LEGS (9) and all(ok) and fields_hold` | enforced |
| `DUP_QIDS=0` | `DUPQID` leg line 281 (`not dup_qids`) + `fields_hold` conjunct `len(dup_qids)==0` line 311 | enforced |
| `WARRANT_OK=17/17` | `WARRANT` leg line 275 + `fields_hold` conjuncts `warrant_total>0 and warrant_ok==warrant_total` line 310 | enforced |
| `QUOTES_LOCATED=20/20` | `FLOORS` leg code counts `norm(quote) in cap` (verbatim, whitespace-normalised, curly-folded via `norm` line 75) + `fields_hold` conjunct `located_all==total_all and total_all>0` line 307 | enforced |
| `TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0` | `TEACHES` leg line 277 + `fields_hold` conjuncts lines 313–314 (`teaches_checked>0 and len(teaches_flagged)>=1 and len(teaches_unresolved)==0`) | enforced |
| `SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0` | Raw-cell match line 255 (`re.match(r"supersedes (S\d{3,}) —", cells[6])` on the raw cell) + `fields_hold` conjunct `len(teaches_sup_unresolved)==0` line 315. Vacuity is disclosed (Named Limit 4) and non-vacuity is the battery's SUP-clause-mirror, refused by r89 (`sup_unresolved=1 unresolved=0`) and accepted by r88 | enforced + disclosed vacuity |
| Verdict from printed fields (`VERDICT fields_hold=1`) | `fields_hold` lines 305–315 (computed from the same values the summary prints) + `VERDICT` leg line 316 requiring `fields_hold == all(ok)` and `fields_hold` itself; `passed` requires `fields_hold` | enforced — a dead detector or detached leg moves `fields_hold` to 0 |
| `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7` | `curation-r89-controls.py` 7 tree forgeries (5 round-87 classes vs r87 + duplicate-qid vs r88 + SUP-clause-mirror vs r88), each asserted refused-by-r89 / accepted-by-prior | enforced |
| `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1` | `curation-r89-mutants.py` 6 counter mutants; 5 die on the field-derived verdict (`fields_hold=0`), the clause-death mutant dies on the battery's SUP mirror | enforced |
| Quote located ⇒ verbatim in its OWN row's committed capture | `capture_text` resolves the entry's row URL to its committed capture; `norm(quote) in cap` line 195. K2's verbatim arm enforced per-row, not cross-row | enforced |
| Registry diff is only the two `used-by` cells | `git diff` base→freeze: exactly 2 lines in `corpus/SOURCES.md` (S216, S218) | enforced extrinsically (no in-counter check) — K3 harm arm, measured at scribe time |

`falsifies-wording` candidates: the C2 sentence says "a verdict derived from the printed fields (`VERDICT fields_hold=1`) rather than from a separate `all(ok)`". The instrument does compute `fields_hold` from the tally values — but they are the *in-memory* values, not a parse-back of the printed summary line (unlike C1's `summ` parse). If a counter printed `TEACHES_FLAGGED=1` while the tally was 0 (or vice versa), `fields_hold` would follow the tally, `VERDICT` would require agreement with `all(ok)` — but the *printed* line would lie. Would the judge see it? Mutant M3 `verdict-legs` kills the `all(ok)` direction (`fields_hold=0 legs_ok=8/8`); there is no mutant that forges the *printed* summary against the tally. So the literal claim "verdict derived from the printed fields" is slightly stronger than the instrument: what is derived is `fields_hold` from the measurement tallies, and what is checked is `fields_hold == all(ok)`, not printed-line ↦ verdict. Narrower property: "the verdict follows the measurement tallies in both directions (dead detector and detached leg both FAIL)". This is the correct reading for the ledger: C2 K4's "verdict that no longer follows from the printed tallies" — the tallies ARE the printed numbers as long as the print is faithful (which the `TEACHES_FLAGGED`/`DU P_QIDS` print lines use directly). The falsification ledger should narrow not the claim, but the enforcement note: counter output is the tally; a print-path forgery is the joint-rewrite boundary (same class as C1 Named Limit 1, not disclosed for C2 — **smallest safe correction**: add a C2 named limit mirroring C1's "a joint rewrite of the tally and its print survives — that edit is the counter", or parse the printed summary back like C1's `summ`). I record this as `falsifies-wording` with the narrower property named, per the seat's charter; it is not a K4 fire because the mutant battery kills every non-joint detachment shape (M1–M4b) and the control battery kills every forgery class the claim enumerates.

Second near-miss (reported, not fired): `SETUP` leg is `("SETUP", True, "registry+entries present")` line 279 — a constant-True leg. It carries no measurement, so a detached-`ok` attack on it is meaningless; it exists for append-accounting (9 legs), not for a check. The claim's "nine legs" counts it. A leg that asserts nothing with `ok=True` is not a K4 instance (K4 requires a skipped *claimed* work; SETUP claims none). Noted for the ledger.

## (c) Prior-round survivors — confirmed killed on r89, accepted on r88

E7 shapes applied to the r88 counter via the r89 edit lists (anchors match r88 text; r88 summary lacks `DIV3`, adjusted). Runs on the live repo (same tree the r89 battery passes on):

| Shape | r89 (`mutate-r89.py`, `c1-mutants.txt`) | r88 (this seat, stdout-accept test) |
|---|---|---|
| `E7c` detached width ok over narrowed `div3=1` | `KILLED E7c-width-detached` — `UNRECONCILED D1_WIDTH detail=3/3/1 pin3 receipt_ok=True rederived=False` + `D2_WIDTH` same | `GATE_RECORDS_R88=PASS`, exit 0 (regex read `3/3`, reconciled) — receipt `r88-E7c.txt` |
| `E7b` detached mutant ok over zeroed measurements (`mut_*=0`, `if files` → `if False`) | `KILLED E7b-mutant-detached` — `UNRECONCILED MUT_ADMIT detail=derived=0 killed=0 receipt_ok=True rederived=False` + `MUT_UNREACH` same | `GATE_RECORDS_R88=PASS`, exit 0, with honest `MUT_ADMIT_DERIVED=0 MUT_ADMIT_KILLED=0` printed beside PASS — receipt `r88-E7b.txt` |
| `E7d` forged width detail (`3/3/3 pin3` regardless of `div3=1`) | `KILLED E7d-width-detail-forged` — `UNCROSSCHECKED D1_WIDTH detail=3/3/3 pin3 D1_FORGES=3 D1_EXPECTED=3 DIV3=1 pin=3/3` + `LEG_FAIL SUMMARY 13/15` | `GATE_RECORDS_R88=PASS`, exit 0 (nothing compared the detail `c` to the measured `div3`; no `DIV3` in summary) — receipt `r88-E7d.txt` |
| `E7f` printed field detached (`D1_EXPECTED=d1_expected+1`) | `KILLED E7f-summary-field-forged` — `UNCROSSCHECKED D1_WIDTH detail=3/3/3 pin3 … D1_EXPECTED=4 DIV3=3 pin=3/3` + `LEG_FAIL SUMMARY 13/15` | `GATE_RECORDS_R88=PASS`, exit 0, with `D1_EXPECTED=4` printed beside PASS — receipt `r88-E7f.txt` |

So the "four shapes round 88's wave left alive" characterization is CORRECT: all four were accepted (stdout-PASS, exit 0) by the pre-round-89 counter, and all four now die on r89 with named `UNRECONCILED`/`UNCROSSCHECKED` lines. The do-nothing evidence for whether the four shapes were truly alive on the r88 instrument is the r88 `c1-mutants.txt` receipt (6/6 killed, none of the E7 shapes enumerated) plus these stdout re-runs. Counterexample test passed: no shape survives r89; none of the four can be produced by r88's battery, which is why the r89 battery's multi-point edits were necessary (a single-point E7c edit would be killed even on r88 because the detached `ok` alone with an honest failing detail `3/3/1 pin3`… wait — r88's reconciliation re-derived `detail=(\d+)/(\d+)` and compared `n_ok == got_ok`; with `ok=True` detached and detail `3/3/1 pin3`, `n_ok` read `3==3 → True`, matching `got_ok=True` — consistent. So single-point detachment WAS a survivor shape on r88 too; E7c's `div3=1` narrowing is the honest-detail that makes the contradiction visible only under per-format `rederive` with `a==b==c==pin`. All consistent with routed defect 2.)

## Residual gaps (ledger entries, lowest-first)

1. C1 FRESH `fresh_err` conjunct not re-derived (see (b)). No battery mutant detaches `ok` from `not fresh_err`. Smallest safe correction: add a mutant `E7h-fresh-err-detached` that forces `ok=True` while `fresh_err` is non-empty and asserts `UNRECONCILED`; or scope `rederive` to reject any detail with trailing text after the numeric pair for FRESH. Not a K4 fire: predicate still met honestly at landing.
2. C2 verdict-tense gap (see (b)): verdict follows the tallies, not a parse-back of the printed line. Smallest safe correction: mirror C1's `summ` parse-back for the summary line, or add a named limit for the joint print-path rewrite. Recorded as `falsifies-wording` for the ledger; the narrower property ("dead detector and detached leg both FAIL via `fields_hold`") is the enforced, mutant-killed property (M1–M4b).
3. C2 `SETUP=True` constant leg — structural, not a measurement; counted in "nine legs" but asserts nothing. The claim counts legs, not measurements; no correction needed beyond this note.
4. Joint rewrite survives both counters (probe `probe-joint` `GATE_RECORDS_R89=PASS`, exit 0 with `div3=1` honestly hidden). Disclosed for C1, undisclosed for C2's print path — covered by gap 2.

## Registry / pins

- Tool `tools/gate-records.py` sha256 `905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60` at base and at freeze — unchanged, as claimed.
- `sha256sum -c instrument-pins.txt` at end of run: all 10 pinned files OK (9 instruments + tool).

## Receipts in wave output

`.ufo/waves/round-89/w1/R89CriticClaims/`: `c1-live.txt`, `c1-mutants.txt`, `c2-controls.txt`, `c2-mutants.txt`, `r88-E7b.txt`, `r88-E7c.txt`, `r88-E7d.txt`, `r88-E7f.txt`, `probe-joint.txt`, `probe-r88-dead-detached.txt`, `probe-r89-dead-detached.txt`, plus this report.

VERDICT: R89CriticClaims C1 held — all four r88 survivors now die with named UNRECONCILED/UNCROSSCHECKED lines, every clause maps to a rederive/crosscheck/pin artefact, and the only surviving shape is the disclosed joint rewrite.
VERDICT: R89CriticClaims C2 held — the field-derived verdict kills dead-detector and detached-leg shapes that passed r88 (probe-r88-dead-detached.txt PASS vs probe-r89-dead-detached.txt FAIL), with one wording narrowing recorded: the verdict follows the measurement tallies, not a parse-back of the printed line.

## Per-clause table (falsification ledger)

| Claim | Clause | Verdict | Narrower property / enforcement note |
|---|---|---|---|
| C1 | `GATE_RECORDS_R89=PASS` exit 0, 16/16/15/16 | held | `passed` conjunction (legs==16, reread==16, reconciled==16, cross==15, summary_leg_ok, all(ok)); SUMMARY is a leg |
| C1 | `n/m` requires `n==m` | held | `rederive` + `UNRECONCILED` guard |
| C1 | `len/d1/div3 pinN` all four equal, `pin==ROWS_203` | held | `rederive` + `crosscheck` pin arm; boundary is the disclosed joint rewrite |
| C1 | `derived=x killed=y` both 1 | held | `rederive` + `crosscheck` MUT arm |
| C1 | `tool present` requires a file | held | `os.path.isfile` + absent-path FAIL on `LEG_REREAD` (limit 2 disclosed) |
| C1 | Re-derived numbers equal summary fields (`DIV3` printed) | held | `crosscheck` compares every leg's nums to parsed summary; `SUMMARY` leg fails on any disagreement |
| C1 | `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2` | held | `mutate-r89.py`; E7b/E7c/E7d/E7f each die with a named line (receipt `c1-mutants.txt`) |
| C1 | Round-88 fields unchanged; tool unchanged | held | `905f9da2…` at both revisions; pins verify at end of run |
| C1 | FRESH (`fresh_ok==5 and not fresh_err`) | falsifies-wording (minor) | `rederive` reads the numeric pair only; `fresh_err` is not re-derived. A detached-`ok` `fresh_err` edit survives. Narrower: "FRESH count agrees receipt↔detail↔summary; the error flag is measured but not re-derived." Smallest correction: an `E7h` battery shape or a suffix-rejecting rederive arm. |
| C2 | `CURATION_R89=PASS`, 9 legs, field tokens | held | `passed` line 318 + `fields_hold` conjuncts |
| C2 | `DUP_QIDS=0` / `WARRANT_OK=17/17` / `QUOTES_LOCATED=20/20` / `TEACHES_FLAGGED=1` / `SUP_`=0 | held | Each has a leg and a `fields_hold` conjunct; verbatim check is `norm(quote) in cap` per row's own capture |
| C2 | Verdict from printed fields (`VERDICT fields_hold=1`) | falsifies-wording | `fields_hold` is computed from the in-memory tallies, not a parse-back of the printed summary. Narrower: "dead detector ⇒ `fields_hold=0` FAIL; detached leg ⇒ `VERDICT` fails both directions; both mutants killed (M1–M4b)". Smallest correction: C1-style summary parse-back or a C2 named limit mirroring C1 limit 1. |
| C2 | `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7` | held | 5 round-87 classes vs r87 + duplicate-qid and SUP-clause-mirror vs r88 (receipt `c2-controls.txt`) |
| C2 | `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1` | held | 5 die on the field-derived verdict; clause-death dies on the SUP mirror (receipt `c2-mutants.txt`) |
| C2 | Registry diff is only two `used-by` cells | held | `git diff` base→freeze: S216 + S218 only |
| C2 | `SETUP` leg (`True` constant) | reported | Constant-`True` leg counts toward "nine legs" but asserts nothing; not K4 (no claimed measurement is skipped). |
