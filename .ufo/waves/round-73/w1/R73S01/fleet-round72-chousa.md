# chousa — round 72 report

## Work performed

Claims (frozen at commit A `97b6ea754b2341cacdfeb29728de0e81c388ad29` in `corpus/evidence/round72/claims.md`, against base `7851c4ce29ef4c13d2c6ffd67b2ea1ea2646a536`):

- **C1 operability** (the lane's lowest-scored non-retired axis, 3/10) — the completing run re-pursued with the r71 timeout-wrap in force, the predicate carried unchanged from the r71 claims file: battery completes with verdict line (anchored `^RESEARCH_GATE_SELFTEST:` count 1) + preflight completes with `SKIPPED=none` → improved ON THAT PREDICATE; the bounded battery still dies before its verdict line → honest-stop. Budgets left at defaults on the measured quiet window (probe receipt frozen at A: `tprobe_rc=124`, the case-258 body 18.131 s CLEAN vs 16.333 s at r71 — the 900 s default ≈ 50x). Evidence: `corpus/evidence/round72/controls/probe-r72-sizing.txt`, `corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt`, `corpus/evidence/round72/controls/after-digest-derivations-r72.txt`.
- **C2 calibration** (sourced on S178, opened this round) — the four routed defects of the round-71 verifier spot-check corrected append-only: the 18→25 ok-case count across all three restating files with per-receipt counts (9 + 16); the ends-at-8 vs 9-lines honest statement; the LOG three-vs-four Mistakes rows; the SHONEN assessment re-filed under the heading (below). Evidence: `corpus/evidence/round72/controls/before-r72-greps.txt` (frozen at A), `corpus/evidence/round72/controls/after-r72-corrections.txt`, the round-71 lesson correction block, the LOG round-71 correction entry, the SCORECARD round-71 correction note.
- Process work this round: the opening census found the two orphaned sibling-lane souji lineages ALIVE and RESPAWNING (two fresh children at census time — the load is not a static two-process situation) — `corpus/evidence/round72/controls/census-selfmatch-r72.txt`, L0 follow-up appended; the first battery launch was orphaned mid-run by the session harness (the transcript pipe's reader died with it), the surviving lineage was killed by PID (two passes, recount 0 — the r71 discipline) and the run relaunched detached writing to its own file (mined as a lesson mistake; the receipt records the event).

## Landed changes

- Freeze `97b6ea754b2341cacdfeb29728de0e81c388ad29` (commit A): claims, before-receipt, probe receipt, census-start (exit 0).
- Landing `7f7ea19a945e0998f009f82b9c651cb08aec1c12` (commit B): SOURCES S178–S179 (registry 177 → 179; mined 144 → 146; B 44), the round-71 lesson correction block, the LOG round-71 correction entry, the SCORECARD planned section + round-71 correction note, the census-selfmatch receipt. No tool byte changes (in-tree gate sha256 = the r71 landing blob `d5d48128…41e2`, verified at A and re-derived at the verdicts tip in `after-digest-derivations-r72.txt`: `DIGESTS_IN_TREE=1/1 PASS`).
- Verdicts commit 6dd6c82405989083f16e101d6573656d39211879: the C1 defect-record receipt, the after-receipts, the round-72 lesson (Gate S178–S179, four Mistakes rows), the SCORECARD round-72 verdict section, the LOG round-72 entry, census-end (exit 0).
- Every landed change ties to a LOG entry (the round-71 correction entry and the round-72 entry).

## Before → after measurements

- C1: before `grep -c "^RESEARCH_GATE_SELFTEST:" corpus/evidence/round71/controls/battery-partial-r71.txt` → 0 (frozen in `before-r72-greps.txt` at commit A) → after `grep -c "^RESEARCH_GATE_SELFTEST:" corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt` → **0** — the battery ran to case ~260 of the canonical 275 (231 ok-case + 16 FAIL-case + 13 skip-case lines, SELFTEST_RC=2) and died at a new, never-before-reachable crash site (the unguarded grep on the never-written `r36-pin.txt` baseline after the flock-less `--pin` capture fails closed rc=2) — **the verdict line was never reached; arm 1 of the frozen predicate is not met; C1 lands honest-stop per the rule's own arm**. The r71 bound is PROVEN in production: `grep -c "^FAIL-case claims-locale-boundary"` → 1 (rc 124) and `grep -c "^case-note claims-locale-boundary"` → 1 (verdict unmeasured within the 900 s budget, never a pass) and `grep -c "^skip-case 259"` → 1 — the battery CONTINUED past case 258, the exact point where r70 and every earlier attempt died. The preflight was not run: arm 1's failure already decides C1 under the conjunctive frozen rule (disclosed; ~3–4 h under the measured rates buys no verdict). Measured at commit 6dd6c82405989083f16e101d6573656d39211879 (run executed at the landing tip; start epoch 1793579430, end 1793593780 = 14350 s, ~55 s/case average, the 19:21–20:00 stretch ~14 s/case — the quiet-window number r73's route is sized on).
- C2: before-greps frozen at A (restatement counts 1+1+1 across LOG/lesson/SCORECARD; per-receipt ok-case 9 and 16; ends-at-8 = 1 vs 9 lines; "Mistakes: three rows" = 1 vs 4 lesson rows; fleet-report `^## SHONEN` = 0 vs inline 1; registry 177) → after-counts in `after-r72-corrections.txt` at the verdicts tree: correction records present (lesson `^correction: R-71 counts` → 1; LOG `^## Round 71 correction entry` → 1; SCORECARD `^## Round 71 correction note` → 1), per-receipt counts re-derived (9 + 16), the r71 receipt byte-unchanged (diff vs base empty), registry 179 additions-only (deleted rows 0), the SHONEN heading below with 4 `[~]` boxes — with every correction-quotation collision disclosed per hit (each quoted token = original + quotation).

## Sources & frontier

SOURCES: 177 → 179 rows (`grep -c "^| S[0-9]" corpus/SOURCES.md`), additions-only (deleted-row count 0 vs base in the after-receipt); S178 = the round-71 verifier spot-check (B; the four routed defects + the binding honest-stop ruling), S179 = this round's sizing probe (B; timeout kills, body 18.131 s). Census before: exit 0 (`.ufo/waves/round-72/census-start.txt`, the five pre-existing W04 warnings); census after: exit 0 (`.ufo/waves/round-72/census-end.txt`). Mistake mining: four rows in `corpus/lessons/round-72.md` `## Mistakes` (census-self-match recurrence including this round's own battery wrapper; empty-result-trusted-as-negative on a mis-composed self-excluding pattern; transcribed-receipt-rows caught pre-commit; harness-owned-run orphaned — relaunched detached, recorded in the receipt). Sourced claim: C2 rests on S178.

## Trend verdicts

- expansion: unchanged — both new rows are own-work records inside ground the lane already holds; no new `corpus/knowledge/` file; PROVINCE.md untouched.
- quality: unchanged — the r71 bound landed and is now proven in production (case 258 bounded, named, counted; the battery passed the r70 stall for the first time), but the completing verdict line was still not reached (the new pin-zone crash site), so no operable-capability improvement is recorded; the defect record and the measured quiet-window rate (~14 s/case → a full battery ≈ 64–90 min) are the route, not padding.
- discernment: improved — the routed corrections are counted across every restating file with collisions disclosed; a disqualified SHONEN form was re-filed per the non-author routing; the round's own slips are mined (four classes, two caught pre-commit); the census gate re-validated the registry additions at both ends.

## SHONEN

SHONEN: lane has SHONEN.md — the four boxes re-filed under this heading per the round-71 spot-check routing (the r71 inline-line form is disqualified as promotion evidence; this heading form is the r69/r70 shape):

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  `SKILL.md` Gates table; `corpus/knowledge/metadata-screen-r25.md` (lane assertion; no non-author verifier)
- [~] At least one end-to-end domain task executed and logged in LOG.md
  `LOG.md` Round 9 archive verification; `corpus/fixtures/archives-r9/`; r25 explicit-root hold battery (lane assertion)
- [~] Instructions executable by an agent without oral context
  `bash tools/research-gate.sh --selftest`; `corpus/evidence/round25-measure-after.log` (lane assertion; the r72 full-run receipt is an honest-red defect record, not a passing run)
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  `PROVINCE.md`; `corpus/knowledge/metadata-screen-r25.md` Limits; `.ufo/waves/round-25/build/ConnectorMetaSiblings.md` (lane assertion)

All four remain lane assertions pending the operator-scheduled non-author promotion review (unchanged since r69/r70; no review was manufactured this round).

## Assimilation

considerthese/ checked: newest file is `2026-10-26.md`; nothing new since the r71 check. CT-20261026-4 (independent CJK quote spot-check) stays carried without implementation credit — it needs outside independence this host cannot supply. Assimilation: none — shokuknow unreachable.

## Routing

- Round 73's route is now fully measured: one guard for the newly-located pin-zone crash site (the unguarded grep on the never-written `r36-pin.txt` baseline after the designed rc=2 `--pin` failure — the same bare-statement class r70 guarded below case 258; this site sits above it and was unreachable until the bound worked), then the completing run sized on the measured quiet-window rate (~14 s/case → 64–90 min per battery; the preflight's G08 bounded by the 7200 s default or sized from the same measurement). The bound itself needs no further work — it is production-proven.
- The operator's flock(1) decision stays open (L0 since r70): on install the capture-zone cases flip to real runs and the gate can go honestly green with zero skips.
- Host load (L0 r71 → r72 follow-up): the lineages are ALIVE and RESPAWNING — killing two PIDs will not clear the window; the loop itself is the operator's to stop.
- The L2-floor template question stays with the operator/protocol lane; no wave dispatched (round-63 attempt-2 precedent, disclosed).
