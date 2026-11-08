# R89ExecRepro — frozen-claim reproduction, round 89

Seat: R89ExecRepro (leaf; no subagents dispatched beyond the assigned labrat scope).
L1: ChousaR89. Freeze: `ac0a0892c15de11fb28d3208f2b287687c00477e` (base `f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8` + landing + non-author spot-check). Tree: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive ac0a0892c15de11fb28d3208f2b287687c00477e | tar -x -C $S/tree` under `/fast/scratch/hyaku/chousa-r89/R89ExecRepro/`. No network. No host mutation. Tooling: `python3 --version` = Python 3.14.8 (`/usr/bin/python3`), system already present; nothing installed or upgraded (official-channel rule read in `/home/vgpnk/.omp/agent/RULES.md`; no installs needed, pacman untouched per orchestrator pause).

## (b) C1 — gate-records battery

Command: `python3 -B $S/tree/corpus/evidence/round89/gate-records-r89.py --root $S/tree --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work $S/work`
Observed (`receipts/c1-battery.txt`, exit 0):
`TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 DIV3=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS_MEASURED=15/15` then `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16` then `GATE_RECORDS_R89=PASS` exit 0. Matches the frozen C1 predicate and the committed `controls/receipts/c1-landing.txt` byte-for-byte modulo the appended `EXIT_C1=` line (diff clean, receipt `pins-check` noted).

Independent re-derivation (`receipts/width-rederive.txt`):
- 203 width: parsed `$S/tree/corpus/evidence/round57/refetch.tsv` (185 data lines): rows with `http_code==203` = 3 (S021, S032, S022). `ROWS_203=3` re-derived; both width legs' `pin3` equal it, and all four numbers equal (`3/3/3 pin3` in `D1_WIDTH.txt` and `D2_WIDTH.txt` under `$S/work/legs/`).
- Leg receipts verified in own grammar: `n/m` legs (`POSITIVE`, `FRESH`, `FORGED`, `CODES`, `RC`, `SETUP`, `D1_REFUSED`, `D2_REFUSED`, `DERIVE_NEG`, `EMPTY`, `SUMMARY`) all satisfy n==m; width legs satisfy len==d1==div3==pin==ROWS_203; mutant legs (`MUT_ADMIT`, `MUT_UNREACH`) satisfy derived==killed==1; `TOOL` leg's `tool present` holds (tool file exists). `SUMMARY.txt` = `SUMMARY=ok detail=15/15`, matching its own n/m grammar and the 15 measured legs.
- Hand CROSSCHECK for three legs: `D1_WIDTH` detail `3/3/3 pin3` vs summary `D1_EXPECTED=3 D1_FORGES=3 DIV3=3`; `MUT_ADMIT` detail `derived=1 killed=1` vs summary `MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1`; `FRESH` detail `5/5` vs summary `FRESH_POSITIVE=5/5`. All agree.
- Source S216 capture: `corpus/captures/b1b13a12aee75c6ecc20fb91.txt` contains the quoted sentence (grep count 1); quoted sentence is 22 words as claimed. (RFC 9110 §15.3.4 context verified in capture head.)
- Harm: `python3 -B $S/tree/corpus/evidence/round89/harm-recheck.py --root $S/tree --repo <lane> --base-tool $S/work/harm/base-tool.py` (base blob extracted via `git show f8fa55ec...:tools/gate-records.py`; both blobs sha256 `905f9da2…`) → `HARM_RECHECK files=13 records=29 moved=0 base_rc=0 r88_rc=0`, exit 0 (`receipts/c1-harm.txt`). Matches committed `controls/receipts/c1-harm.txt`.
- Note: the first harm invocation without `--base-tool` (tool path absent) exited 1 with 29 spurious moves; that was a harness error, not a finding — rerun with the correct base blob gives `moved=0`. Recorded here so the record is honest.

Mutants (`receipts/c1-mutants.txt`, exit 0): `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2 TOTAL=13/13`. The four round-88 survivor shapes die as claimed:
- `E7c-width-detached` → `UNRECONCILED D1_WIDTH detail=3/3/1 pin3` + D2 twin;
- `E7b-mutant-detached` → `UNRECONCILED MUT_ADMIT detail=derived=0 killed=0` + MUT_UNREACH twin;
- `E7d-width-detail-forged` → `UNCROSSCHECKED D1_WIDTH … DIV3=1 pin=3/3` + D2 twin;
- `E7f-summary-field-forged` → `UNCROSSCHECKED D1_WIDTH … D1_EXPECTED=4` + D2 twin.
No hits missed; all 11/11 named mutants plus both tool mutants are listed KILLED/CAUGHT.

Challenge (tightest attempt, `receipts/challenge-joint-run.txt`): built the joint rewrite the claim names as limit 1 — E7d (narrowed div3 + forged width detail + detached ok) **plus** forged summary `DIV3` field — applied 4/4 edits to a scratch copy, ran the battery: `GATE_RECORDS_R89=PASS` with all fields clean, exit 0. This confirms the claim's named-limit disclosure is accurate (the joint rewrite survives because reconciliation guards receipt-vs-detail agreement only; this is the counter-itself, not a bypass of the frozen instrument). Not a kill — the claim explicitly disclaims this class. Challenge is a genuine attempt that improved no other axis and harmed none: it confirms the frontier's stated boundary.

## (c) C2 — curation counter

Command: `python3 -B $S/tree/corpus/evidence/round89/curation-r89.py --root $S/tree`
Observed (`receipts/c2-counter.txt`, exit 0):
`SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=8/8` plus `TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031` plus `CURATION_R89=PASS` exit 0. Matches the frozen C2 counter fields. Nine legs: LEGS_MEASURED=8/8 printed before VERDICT appends the ninth (VERDICT) leg — EXPECTED_LEGS=9 enforced and met (passed requires `len(legs)==EXPECTED_LEGS and all ok and fields_hold`).
- `QUOTES_LOCATED=20/20` re-derived per-entry (`receipts/c2-rederive2.txt`): 13 located in search-transparency-reporting-r84.md (Q1–Q13), 7 in provenance-recording-r85.md (Q1–Q7); all 20 quotes verified verbatim (whitespace-normalised, curly quotes folded) in the committed capture of their own row's URL. Token floor minimum re-derived over the 20 located quotes = 7 at Q13 ("Date on which the resource was changed.", S023) — equals frozen `MIN_TOKENS=7`, which is therefore the measured minimum, not a choice.
- Per-entry qid sets re-derived: r84 = Q1..Q13, r85 = Q1..Q7 — both equal the pinned `QID_SETS` exactly.
- `WARRANT_OK=17/17`: hand-checked 5 of 17 rows (e.g. r84 "Reporting which sources were searched" Q1, r84 "Linking a claim to its source" Q6,Q7, r84 "Recording what a resource derives from" Q9, r85 "Naming what a resource derives from" Q1, r85 "Recording when content was last reviewed" Q7) — all resolve and share distinctive terms; full re-derivation counts 17 warrant rows ok out of 17 decision rows with qids (the two "Situation / Warrant" header rows correctly excluded by the qid-resolution check as the counter does).
- One flagged row: S024 (teaches: "property separate from publication or modification dates") — terms `publication,modification` absent from its own capture (schema.org/lastReviewed, capture `11d6cc56bb24adfc61eea2b4`), so flagged; disposition `superseded by S031` (mined, same URL), hence `TEACHES_UNRESOLVED=0`. DEF_CITED: S023 modified-definition quote cited (MODIFIED_DEF_CITED=1).
- `SUP_CLAUSE_CHECKED=0` confirmed as true population: 10 superseding rows exist in the registry, but none carries a contrast phrase plus a date term in its own teaches (S031 carries "no comparison" but no date term) — the clause is genuinely vacuous on real rows; non-vacuity is the battery's SUP-clause-mirror, which the round-88 counter accepts and this one refuses (`sup_unresolved=1 unresolved=0`). Matches the claim's named limit 4.
- Verdict: `fields_hold` computed from the printed tallies (all eleven conjuncts); VERDICT leg also requires `fields_hold == all(legs ok)`. PASS is therefore derived from the fields, not a separate `all(ok)`. `VERDICT fields_hold=1` is the emitted line (in mutant receipts where legs fail as `LEG_FAIL VERDICT fields_hold=0 …`).

Controls (`receipts/c2-controls.txt`, exit 0): `FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7`, `CONTROLS=PASS`.
Mutants (`receipts/c2-mutants.txt`, exit 0): `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1`; the clause-death mutant (M5-lowercase-clause) is detected through the battery's SUP mirror (`CASE_DEVIATION … detector=battery`), and five others through the counter's field-derived verdict.

## (d) Pins & registry

`corpus/evidence/round89/instrument-pins.txt` vs tree (`receipts/pins-check.txt`): 10/10 OK, 0 mismatches (gate-records-r89 `f34f59c8…`, curation-r89 `2c063f8b…`, mutate-r89 `10b43d8a…`, curation-r89-controls `fd54ab3c…`, curation-r89-mutants `8b4f56b6…`, harm-recheck `3c3768ad…`, controls/expected.tsv `d5f58452…`, controls/run-controls.sh `974007a8…`, c1-positives.tsv `8c089828…`, tools/gate-records.py `905f9da2…`). The subject tool is the landed blob (`905f9da2` full `905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60`). Registry diff `f8fa55ec..ac0a0892` on `corpus/SOURCES.md` touches exactly two cells: S216's `used-by` gains `corpus/evidence/round89/claims.md` and S218's `used-by` gains the same — nothing else.

## Findings

- None. Every command matched its frozen predicate exactly, including every named field (`LEG_REREAD=16/16`, `RECONCILED=16/16`, `CROSSCHECK=15/15`, `LEGS_APPENDED=16`, `QUOTES_LOCATED=20/20`, `DUP_QIDS=0`, `WARRANT_OK=17/17`, `TEACHES_FLAGGED=1`, `TEACHES_UNRESOLVED=0`, `SUP_CLAUSE_CHECKED=0`, `SUP_UNRESOLVED=0`, `VERDICT fields_hold=1`, `CONTROLS=PASS`, `FORGERY_REFUSED=7/7`, `PRIOR_ACCEPTED_FORGERY=7/7`, `MUTANTS_KILLED=11/11`, `TOOL_MUTANTS_CAUGHT=2/2`, `MUTANTS_KILLED=6/6`, `COUNTER_DETECTED=5`, `BATTERY_DETECTED=1`) and world checks (no harness errors or spurious moves once the base tool path was supplied correctly). Axis scorecards, kill-rule residual checks, verdict discipline, and the detailed receipts are in `receipts/`.

VERDICT: R89ExecRepro C1 held — battery, mutants, harm and pins all reproduce exactly; the E7d+DIV3 joint forgery passed as the claim's named limit 1 discloses, so that mutant was exercised and not killed.
VERDICT: R89ExecRepro C2 held — counter, controls and mutants reproduce exactly; QUOTES_LOCATED, token floor, qid sets, WARRANT_OK, the single flagged row and the vacuous SUP clause were independently re-derived.
