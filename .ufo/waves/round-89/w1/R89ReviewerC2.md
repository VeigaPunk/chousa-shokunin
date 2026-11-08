# R89ReviewerC2 — C2 calibration, wording attack against `curation-r89.py`

Seat: `R89ReviewerC2` (leaf). Freeze `ac0a0892c15de11fb28d3208f2b287687c00477e` (HEAD).
Instrument sha256 `2c063f8b…` matches `instrument-pins.txt`. No production edits; all runs in `/fast/scratch/hyaku/chousa-r89/R89ReviewerC2/`.
Registry diff `f8fa55ec..ac0a0892 -- corpus/SOURCES.md`: `1 file changed, 2 insertions(+), 2 deletions(-)` (S216 + S218 `used-by` cells) — the only registry change.

Base run (receipt `m_bb-real.txt`, exit 0):
```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=8/8
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
CURATION_R89=PASS
```
Controls `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7`; mutants `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1` (receipts `m_b-controls.txt`, `m_b-mutants.txt`).

## (a) “the verdict is computed from the printed fields” — per leg

Nine legs. `fields_hold` (`curation-r89.py:305-315`) reads the SAME local variables the summary line prints — so technically “printed fields” only in the sense of “the variables behind the printed tallies”, and `VERDICT` (`:316-317`) additionally refuses divergence with `all(ok)`. `passed` (`:318`) requires `len(legs)==9 and all(ok) and fields_hold`. Verdict table (each row forced `ok=True` alone on a tree where that leg’s quantity is honestly broken; stock result shown, then forced-leg result — receipt `m_aa-A3.txt`, and `m_aa-A2-firstpart.txt` for the TEACHES/meta-mutants):

| Leg | `fields_hold` reads | Verdict when leg forced | Blind spot? |
|---|---|---|---|
| `SUPERSEDED` | printed `SUPERSEDED_LIVE=0/0` via `len(superseded_live)==0` — recomputes from a variable the summary prints | No PASS (`LEG_FAIL VERDICT fields_hold=0 legs_ok=8/8` on S031-queued? — see bug B2 below: `v-a4` printed `SUPERSEDED_LIVE=0` even queued, because S024 is `queued` not `mined`; the live-superseded case needs target `mined` + sup not `mined`. The claim's own `s031-queued` tree is the same shape? — see (c)/B3) | blind only via B3 (leg has no trigger in measured trees) |
| `UNENTAILED` | `UNENTAILED_TERM` print — `v-a6`/`v-A6`: forced leg still `CURATION_R89=FAIL` (`VERDICT fields_hold=0 legs_ok=8/8`) | seen | no |
| `DEF_CITED` | `MODIFIED_DEF_CITED` print (`modified_def_cited>=1`) — `v-a5`/`v-A5`: forced DEF leg still FAIL (also WARRANT fails) | seen | no (dual causation noted) |
| `FLOOR` | NOT via the `13/13` string — recomputes `loc>=fl and loc==tot and set(qs)==set(QID_SETS) and not short` over `floor_rows` — `v-a3`/`v-A3`: forced leg still FAIL (`VERDICT fields_hold=0 legs_ok=8/8`) | seen | **prints `12/12` but floor check is on recomputed vars, not the printed string — string and verdict can diverge silently if the formula moves** (formula is in `fields_hold` itself) |
| `WARRANT` | `WARRANT_OK=n/n` ratio (`warrant_ok==warrant_total`) — `v-a7`/`v-A7`: forced leg still FAIL | seen | no |
| `TEACHES` | `TEACHES_CHECKED/FLAGGED/UNRESOLVED` prints (`checked>0 and flagged>=1 and unresolved==0`) — `u-A2`: forced leg still FAIL; dead-teaches mutant (`v-A1b`) FAIL via `flagged=0` | seen | no |
| `SETUP` | constant `True` (leg is `SETUP; True`) — missing registry/entry returns `SETUP` exit 2 before legs | n/a | no (by construction) |
| `DUPQID` | `DUP_QIDS` print — `v-a8`/`v-A8`: forced leg still FAIL | seen | no |
| `VERDICT` | `fields_hold` vs `all(ok)` — `u-A9` (VERDICT forced True, `passed` still needs `fields_hold`): FAIL; `u-A9b` (TEACHES forced + `fields_hold` dropped from `passed`, i.e. pre-r89 verdict): FAIL via `LEG_FAIL VERDICT fields_hold=0 legs_ok=8/8` because VERDICT leg itself still compares | seen | **yes — one way** (see below) |

Residual blindness (concrete, measured):

1. **`SETUP` leg is `True` unconditionally** (`:279`). `fields_hold` never checks it — correct, since setup failures return exit 2 before the verdict block. But the claim sentence “its verdict computed from the fields the summary printed (`VERDICT fields_hold=1`)” is only true for the 8 non-SETUP legs; SETUP is an assertion, not a measured field. Cosmetic for the verdict, but the claim's “computed from printed fields” blanket covers it.
2. **FLOOR formula duplication**: the FLOOR leg (`:228-229`) and `fields_hold` (`:309-310`) carry two literal copies of the same conjunctive formula. The verdict sees a forced FLOOR leg only because the second copy exists. A single-copy refactor is fine; a formula edit that changes one copy and not the other silently reopens the detach. The claim says “computed from the printed fields” — it is actually computed from a recomputed copy of the leg's own logic, printed only in part (`Q_FLOORS` prints `located/total floorN`, not the qid-set or token-floor conjuncts).
3. **`sup_unresolved` scope**: `fields_hold` requires `teaches_sup_unresolved==0` but does NOT require `teaches_sup_checked>0` (or `SUP_CLAUSE_CHECKED>0`). A dead superseder clause (M5 shape) prints `SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0` and `fields_hold` is satisfied — the counter cannot see its own dead clause. This is disclosed in `curation-r89-mutants.py` (“the counter alone cannot see its own dead clause … detector is the battery”) and in claims.md Named limit 4, so it is not a hidden finding — but the C2 sentence “five through the counter's field-derived verdict and the clause-death mutant through the battery's mirror” must be read as: the field-derived verdict is NOT complete by itself. A reader who trusts “verdict computed from printed fields” alone over-claims.

## (b) The `DUPQID` guard

Code: `qids = re.findall(r"Q\d+", cells[3]); if len(set(qids)) != len(qids): dup_qids.append(...)` — per warrant cell, one decision row at a time.

- **One row only: YES, catches `Q1, Q1`.** `t-b1`/`v-a8`: `DUP_QIDS=1`, `LEG_FAIL DUPQID … warrant=Q1, Q1 (S215)`, FAIL. The committed battery's `D1-duplicate-qid` case is this exact shape (`controls.txt`: `OK D1-duplicate-qid … LEG_FAIL DUPQID … Q1, Q1 (S215)`).
- **`Q1, Q1, Q3`: YES, catches it — but WARRANT also fails.** `t-b2`: `DUP_QIDS=1`, `LEG_FAIL WARRANT 16/17`, `LEG_FAIL DUPQID … warrant=Q1, Q1, Q3 (S215)`, FAIL. (WARRANT fails because Q3's quote shares no distinctive term with the “Naming what a resource derives from” row; Q1 dup itself would pass WARRANT.)
- **Cross-row duplicate: NO, by design.** `t-b3`: Q2 cited on two different decision rows (first row `Q1→Q2`, fourth row `Q4→Q2`), no single cell repeats a qid: `DUP_QIDS=0`, `CURATION_R89=PASS`. The guard is per-cell only; the claim sentence “a warrant cell citing `Q1, Q1` (one qid counted twice)” scopes exactly to this, so no overclaim — but “one qid counted twice” as a phrase reads broader than the per-cell check.
- **`Q1, Q1, Q99`: caught by both** (`t-b4`: `DUP_QIDS=1`, WARRANT 16/17).
- Mutants `M4a` (leg forced) killed by VERDICT; `M4b` (field dropped from `fields_hold`) killed by the DUPQID *leg* — both in `m_b-mutants.txt`.

## (c) The superseder clause and `SUP_CLAUSE_CHECKED=0`

What the claim guarantees on real bytes: NOTHING fires. Real registry has **zero** superseding rows with a contrast phrase + a date term (measured over 218 rows, receipt `m_cc-scan.txt`: all 10 superseders listed, `superseder contrast+date count 0`; only S031 has a contrast phrase, with `named=[]`). `SUP_CLAUSE_CHECKED=0` is therefore not a coincidence — the clause body never runs on real registry data. The clause lives as: (i) code paths `:253-267` / `:315`, and (ii) the battery's `SUP-clause-mirror` (S031 + `distinct from publication dates` + mined S219 mirror), where `teaches_sup_checked=1`, `sup_unresolved=1`, `TEACHES_UNRESOLVED=0` — `v-a10`: `SUP_CLAUSE_CHECKED=1 SUP_UNRESOLVED=1`, `LEG_FAIL TEACHES checked=2 flagged=2 unresolved=0 sup_unresolved=1`.

Sentence check. claims.md C2 (lines 80-88): “`TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0`, `SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0`, and its verdict computed from the fields the summary printed” + Named limit 4: “The superseder-own-read clause is **vacuous on the real registry** (`SUP_CLAUSE_CHECKED=0` …). Its non-vacuity is the battery's `SUP-clause-mirror`, which the round-88 counter accepts and this one refuses … A vacuous leg plus a measured mirror is the honest shape; claiming the clause fires on real rows would be false.” **The phrasing is exactly the vacuity, no more.** plans/round-89.md repair 4 (defect 4): “Fixed: the raw cell is matched; non-vacuity is the battery's `SUP-clause-mirror`, because no real superseding row names a date term” + repair 6: “reports `SUP_CLAUSE_CHECKED` so its vacuity … is visible rather than implied.” Both match. No finding here beyond the disclosed limit.

## (d) The four named limits — counterexamples built and run (receipt `m_cc-limits.txt`)

1. **`MIN_TOKENS = 7` floor (claims.md §1).** Measured: Q11 (`"Date (often a range) of validity of a resource."`, 9 tokens, S023) replaced by the **9-token verbatim fragment** `(often a range) of validity of a resource. Comment` (from the S023 capture, shares distinctive term `validity`) — `w-l1`: `CURATION_R89=PASS`, `QUOTES_LOCATED=20/20`. Confirmed: a ≥7-token verbatim substitution sharing a distinctive term passes. Wording confirmed (it also passes `WARRANT_OK=17/17`).
2. **Qid-set pin guards label identity, not content (§2).** Measured: Q1/Q2 texts swapped under their pinned labels in r85 (`w-l2`) — `CURATION_R89=PASS`, `WARRANT_OK=17/17`. The swap happens to still satisfy term-sharing (Q2's text shares `derivation` with row 1; Q1's shares `provenance` with row 2), so the wording “swapping the quote texts under two pinned qids passes” holds on this instance; whether it passes for *arbitrary* swaps depends on term overlap, but the claim's instance-shape (label swap undetected) stands.
3. **Row reorder (§3).** Measured: all six r85 decision-table rows reversed (`w-l3`) — `CURATION_R89=PASS`. Benign, confirmed.
4. **Superseder-clause vacuity (§4).** Measured above and below: `SUP_CLAUSE_CHECKED=0` on every real-registry run; the mirror is the only firing instance (`SUP_CLAUSE_CHECKED=1`). Confirmed.

## Findings (concrete, with receipts)

**B1 (wording, low).** C2 sentence: “its verdict computed from the fields the summary printed (`VERDICT fields_hold=1`) rather than from a separate `all(ok)`”. The counter still computes `all(ok)` and *conjoins* it: `VERDICT` leg is `fields_hold == all(ok) and fields_hold`, and `passed` needs `all(ok) and fields_hold`. The repair is additive (round-88's `all(ok)`-only verdict closed), but the sentence's “rather than” overstates: the verdict is `field-derived AND leg-derived`, not “fields instead of legs”. Receipt: `u-A9b` — even the pre-r89 shape (fields dropped from `passed`) still FAILs through the VERDICT leg, i.e. the current PASS depends on both conjuncts.

**B2 (registry/commit nuance, low).** The “two cells” registry change claim: `git diff f8fa55ec ac0a0892 -- corpus/SOURCES.md` shows the S216 `used-by` cell gaining `corpus/evidence/round89/claims.md` — and the S218 row greps identically old/new (diff line 231 shows both) — i.e. S218's `used-by` already contained `corpus/evidence/round89/claims.md` at base `f8fa55ec`. The `2 insertions(+), 2 deletions(-)` are two row rewrites; only S216's cell materially gains. C2's “both rows' `used-by` gained … and that is the ONLY registry change (two cells)” is one cell too strong on these bytes. (S218 `used-by` at HEAD: `corpus/evidence/round87/claims.md, corpus/evidence/round89/claims.md`.)

**B3 (structural, low — disclosed limit, recorded here for the frontier).** `fields_hold`'s `SUPERSEDED_LIVE` conjunct can never fire on any registry where every superseded target is `queued` (as S024 is) — `superseded_live` needs target `mined` + sup not `mined`. On the real registry it is a satisfied-by-construction `0`, same family as the superseder-clause vacuity. The claim does not name this one; the TEACHES leg (not SUPERSEDED) is what catches the S031-queued shape (`TEACHES_UNRESOLVED=1`).

**B4 (formulation, info).** FLOOR's `fields_hold` conjunct re-runs the formula rather than reading the printed `Q_FLOORS` string; a formula edit split across the two copies reopens a detach. Recipe `v-A3` shows the current cross-check works; the duplication is the residual seam (item (a).2).

Status: none of B1–B4 falsifies the C2 predicate (`CURATION_R89=PASS`, nine legs, `DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0`, `VERDICT fields_hold=1`; `CONTROLS=PASS 7/7`; `MUTANTS_KILLED=6/6`) — all reproduced at the freeze. B1 penalises the *sentence*, B2 the registry-cell count, B3/B4 note residual seams the claim already half-discloses.

Tooling: no installs; stdlib `python3` only.
Results grid, axis (a)–(d) (commands + receipts + observed lines/exit codes): see `m_bb-real.txt`, `m_b-controls.txt`, `m_b-mutants.txt`, `m_bb-dup.txt`, `m_aa-A3.txt`, `m_cc-limits.txt`, `m_cc-scan.txt` (copies in this folder).

VERDICT: build R89ReviewerC2 C2 fired
