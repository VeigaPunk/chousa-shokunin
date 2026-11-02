# Round 72 verifier spot-check — chousa (closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Closed 2026-11-01 against lane tip `6dd6c82405989083f16e101d6573656d39211879` (branch `master`, local == `ls-remote origin` == tip), base `7851c4ce29ef4c13d2c6ffd67b2ea1ea2646a536`, freeze A `97b6ea754b2341cacdfeb29728de0e81c388ad29`, landing B `7f7ea19a945e0998f009f82b9c651cb08aec1c12`. Report: `.ufo/reports/round-72/chousa.md` (committed in the fleet repo by the lane identity `chousa-shokunin`, fleet commit `f0bc129807d4f9814d2f036546c36b061cbddcde`). Dispatch digest: launch 14:43:46-08:00, complete 20:57:20-08:00 — the battery run window (epochs 1793579430 → 1793593780 = 16:30–20:29 local, 14350 s) sits inside it. Index-free git only; no mutating command; no lane gate executed.

## 1. Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report authored by lane identity | `git -C <fleet root> log --format='%an %H' -1 -- .ufo/reports/round-72/chousa.md` | `chousa-shokunin f0bc1298…` | PASS |
| SHONEN heading | grep on report file | `^## SHONEN` → 1; `^- \[~\]` → 4, each with resolvable pointers | PASS |
| cited commits exist | `git cat-file -t <hash>` for A, B, tip | commit × 3 | PASS |
| cited commits are ancestors | `merge-base --is-ancestor <hash> refs/heads/master` | yes × 3 | PASS |
| lane tip pushed | `ls-remote origin refs/heads/master` vs `rev-parse refs/heads/master` | both `6dd6c8240598…` | PASS |
| cited work in range | `git log --oneline 7851c4ce..master` | exactly the 3 cited commits (freeze, landing, verdicts) | PASS |
| census at both ends | committed receipts + this verifier's own run | `census_rc=0` both ends; verifier re-run exit 0 (same five pre-existing W04 warnings) | PASS |
| evidence timestamps | run-window epochs vs dispatch digest | 16:30–20:29 local inside 14:43–20:57 dispatch window; receipts dated 2026-11-01 ≤ commit date | PASS |
| frozen receipts unchanged | `diff-tree -r --stat A tip` on claims.md / probe-r72-sizing.txt / before-r72-greps.txt | empty × 3 (claims frozen before measurement) | PASS |
| append-only discipline | `diff-tree -r -p base tip` minus-lines on LOG.md / round-71 lesson / r71 receipt | 0 / 0 / 0 removed lines; corrections are new entries | PASS |
| write scope | `diff-tree -r --name-only base tip` | tools/ and PROVINCE.md and corpus/knowledge/ untouched; SCORECARD additions-only (0 removed lines) | PASS |

No marker predicate: the report names real work, real receipts and resolvable commits. Lane-round status **ok**; the honest-stop below is the verdict on the claim, not the lane-round.

## 2. Claim re-checks

### C1 operability — honest-stop per the frozen rule (verified, agreed)

The frozen predicate (claims.md at A, byte-identical to tip): battery completes with anchored `^RESEARCH_GATE_SELFTEST:` count 1 + preflight `SKIPPED=none` → improved; battery dies before its verdict line → honest-stop. No predicate edit after measurement.

Re-derived at the tip (every count below is this verifier's own run over committed bytes):

- `git show 6dd6c82…:corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt | grep -c "^RESEARCH_GATE_SELFTEST:"` → **0** (the honest-stop ground; matches the report).
- `grep -c "^ok-case"` → 231; `grep -c "^FAIL-case"` → 16; `grep -c "^skip-case"` → 13 — 260 case lines ≈ the reported ~260 of the canonical 275 (SKILL.md row 83 pins the canonical count: `PASS (275 cases, 0 skipped)` on a flock-capable host).
- `grep -n "^FAIL-case claims-locale-boundary"` → receipt line 319: `FAIL-case claims-locale-boundary       exit=124` — **the r71 timeout-wrap fired in production**; line 321 case-note: `reason=locale-boundary budget 900s exceeded (timeout); verdict unmeasured within budget` — a named FAIL-case, never a pass.
- `grep -n "^skip-case 259"` → receipt line 322 — **the battery continued past case 258, the exact r70/r71 stall point, for the first time in the chain**.
- Receipt line 329: `SELFTEST_RC=2`; the crash symptom bytes: `/usr/bin/grep: /tmp/chousa-research-gate-selftest.2rSINk/r36-pin.txt: No such file or directory`, then `FAIL-case pin-echo-isolation pin_rc=2 drift_rc=2` with the child's `--pin canonical capture failed (rc=2 …)` and `--drift baseline missing` lines, then exit — **the new, never-before-reachable pin-zone crash site, fully captured**.
- Tool bytes unchanged all round: `git show <tip>:tools/research-gate.sh | sha256sum` → `d5d48128509f77ed…41e2` = the r71 landing blob, re-derived by this verifier at base and tip independently of the lane's `DIGESTS_IN_TREE=1/1 PASS` receipt.
- Preflight not run: disclosed; arm 1's failure already decides C1 under the conjunctive frozen rule. Agreed — ~3–4 h more at measured rates buys no verdict.

**Crash-site byte-location — verified, with one precision correction routed (defect V72-1 below).** This verifier located the two unguarded sites in the committed tool (`set -euo pipefail` at `tools/research-gate.sh:292`): the unguarded grep `grep -q '^GATE_GREP: ' -- "$WORK/r36-pin.txt" && p36_ok=0` at **line 8426** prints the missing-file error into the receipt but does **not** kill the script (inside an `&&` list it is exempt from `set -e` — verified empirically by this verifier with an isolated 6-line harness: the script survives and prints the grep error); the actual kill is the next line's unguarded sub-run assignment `p36_out=$(bash "$SELF" --pin "$WORK/r36-pin2.txt" 2>&1)` at **line 8435**, which inherits the flock-less `--pin` child's designed rc=2 under `set -euo pipefail`. The receipt's byte order (FAIL-case printed *after* the grep error; death before any pin-drift-grep-token output) matches this analysis exactly. The lane's narrative ("the unguarded grep kills the script") names the right zone and the right symptom bytes; the killing line is 8435, and no tool line numbers are recorded anywhere — "byte-located" overstates what the receipt pins.

**Verdict: honest-stop per the frozen rule's own arm — verified and concurred.** The completing predicate was not met; no operability improvement is claimed or recorded; the operability score deliberately stays at the historical 3/10 (SCORECARD row, last numeric change round 1 — re-derived from the additions-only SCORECARD diff).

### C2 calibration — improved (verified, agreed)

The four routed defects of `corpus/lessons/round-71-verifier-spotcheck.md` §6 (re-read at base, S178's source) are exactly what C2 corrects. All before-side counts re-derived by this verifier at base 7851c4ce (14/14 match `before-r72-greps.txt`): "18 healthy" 1+1+1 across SCORECARD/LOG/round-71 lesson; per-receipt ok-case **9** + **16**; ends-at-8 header 1 vs 9 transcript lines; "Mistakes: three rows" 1 vs 4 lesson rows; fleet r71 report `^## SHONEN` 0 vs inline form 1; registry 177; r71 verdict-line count 0; no r71 preflight receipt; tool sha == r71 blob.

All after-side counts re-derived at the tip (16/16 with one benign drift named below): correction records `^correction: R-71 counts` (lesson) 1, `^## Round 71 correction entry` (LOG) 1, `^## Round 71 correction note` (SCORECARD) 1; per-receipt counts 9 + 16 re-derived; `The honest final count is 9 ok-case lines` present; r71 receipt `diff-tree --stat base tip` empty (bytes untouched); registry **179**, deleted rows 0 (additions-only); report `^## SHONEN` 1 with 4 `[~]` boxes; "Mistakes: three rows" correction names the fourth (prose-in-used-by E11) row; LOG/lesson append-only (0 removed lines each).

**Verdict: improved — verified.** Counted, append-only, every restating file corrected in one landing, quotation collisions disclosed per hit, the r71 honest-stop ruling undisturbed. Sourced on S178 as claimed.

### Re-measured vs evidence-verified

Re-measured by this verifier: every C1 and C2 count above (all over committed bytes), the tool sha identity, the census validate exit code, the SOURCES row quotes. Evidence-verified (lane-owned gate evidence read, never executed): the battery receipt as the gate's committed selftest output at the landing tip, and `after-digest-derivations-r72.txt`'s `DIGESTS_IN_TREE=1/1 PASS` (its object id `a5780cd6…` and digest re-derived independently; the runner itself not executed per the closure contract).

## 3. Per-axis verdicts

| axis | verdict | ground |
|---|---|---|
| operability | unchanged | C1 honest-stop; score row untouched (3/10, last-change round 1); additions-only SCORECARD diff |
| calibration | improved | C2 verified above (four counted corrections + SHONEN re-file) |
| depth | unchanged | no knowledge/ or SKILL.md change (diff-tree empty on both) |
| coverage | unchanged | PROVINCE.md untouched; both SOURCES rows are own-work records on held ground |
| freshness | unchanged | no re-verification claim beyond the receipts this round already carried |
| adjacency | unchanged | the orphaned souji lineages reported (census receipt + L0), never killed or absorbed from this lane |

No axis harmed: the SCORECARD diff base→tip removes nothing (0 `-` lines); no numeric score moved; no capability row (correctly not pre-claimed for an honest-stop measurement and a record correction).

## 4. Discernment spot-check (non-author; sample from `corpus/lessons/round-72.md` `## Gate`)

The round recorded **no fresh rejection** and says so in its Gate ("the reject sample stands at S177"); the sample below therefore re-opens both new admits and the standing reject — the ≥1 admit / ≥1 reject duty is met with the round's own disclosed sample.

| item | decision | re-opened source (this verifier's own command) | agree/disagree | reason |
|---|---|---|---|---|
| S178 (round-71 verifier spot-check) | admit, B, narrow | `git show 7851c4ce…:corpus/lessons/round-71-verifier-spotcheck.md` — §6 item 2 sentence matches the row's quote verbatim (11 words ≤ 25; location pinned) | **agree** | the routing record exists and says exactly what the row claims; the narrow admit scope (four routed defects + SHONEN re-file, nothing else the check re-derived) is the right tier for an own-work record; the binding honest-stop ruling is real |
| S179 (r72 sizing probe receipt) | admit, B | `git show 97b6ea7…:corpus/evidence/round72/controls/probe-r72-sizing.txt` — `tprobe_rc=124`, `real 0m18.131s`, `RESEARCH_GATE: CLEAN` all present at the pinned revision | **agree** | the probe is a real capability kill-probe (rc 124), not a mere existence check (the r70 python3-stub lesson applied); the one-host/one-moment limit is stated in the row; the 900 s default ≈ 50× the measured body justifies the sizing |
| S177 (SKILL.md Gates row 83, standing reject) | reject | `git show b2f88ec…:SKILL.md` — both quoted phrases verbatim in row 83; then `git show b2f88ec…:corpus/evidence/round70/controls/after-battery-completes-r70.txt | grep -c "^RESEARCH_GATE_SELFTEST:"` → **0** | **agree** | the row asserted "the battery completes and prints the FAIL verdict line" while its own cited receipt carries no verdict line — the rejection is grounded in committed bytes; the flip (corrected by r71) is on record |

`sources-census.sh validate --root <fleet root> chousa` re-run by this verifier: **exit 0**, five pre-existing W04 duplicate-url warnings (S051/S053/S073/S074/S075 — unchanged from both committed census receipts; warnings, not failures).

## 5. Trend verdicts

- **expansion: unchanged** — both new SOURCES rows are own-work records inside ground the lane already holds; `diff-tree base tip -- corpus/knowledge/` empty; PROVINCE.md untouched. Agreed with the report.
- **quality: unchanged** — the r71 bound is now production-proven and the r70 stall was passed for the first time (receipt-verified), but the completing verdict line was still not reached (anchored count 0), so no operable-capability improvement exists to record; the defect record and the measured quiet-window rate (~14 s/case → 64–90 min per battery) are the route, not a landed improvement. Agreed — the honest grade; the production proof alone does not complete the frozen predicate.
- **discernment: improved** — four routed defects corrected append-only with counted before/after receipts and disclosed collisions; a disqualified SHONEN form re-filed per the non-author routing; four own slips mined (two caught pre-commit); census re-validated at both ends. Agreed — this is the LEARNING.md improved shape (a routed disagreement became counted, grounded corrections).

## 6. Routed defects for round 73 (all status-neutral; none verdict-bearing)

1. **V72-1 (crash-site kill line, evidence-integrity precision).** The round's defect narrative (receipt header, LOG, SCORECARD, report) says "the unguarded grep on the missing file kills the script under `set -euo pipefail`". The grep (`tools/research-gate.sh:8426`, `grep -q '^GATE_GREP: ' -- "$WORK/r36-pin.txt" && p36_ok=0`) is `set -e`-exempt inside the `&&` list — this verifier reproduced the survival empirically; it supplies the receipt's visible symptom line only. The line that actually exits is the next unguarded sub-run assignment at **`tools/research-gate.sh:8435`** (`p36_out=$(bash "$SELF" --pin "$WORK/r36-pin2.txt" 2>&1)`), inheriting the flock-less child's designed rc=2. Neither line number is recorded in any r72 artifact, so "fully measured and byte-located" overstates: the zone and symptom bytes are receipt-pinned, the tool lines were re-derived only by this spot-check. **Route:** the r73 guard must cover both unguarded sites in the pin-echo-isolation zone (the grep is a genuine bare-statement of the same class r70 guarded; the 8435 assignment is the actual kill), and the guard landing should record the line numbers as r70 did.
2. **V72-2 (after-receipt measurement tree).** `after-r72-corrections.txt` records `$ git rev-parse HEAD` → `7f7ea19a…` (the landing tip), while the report and the SCORECARD verdict row say the after-counts are "at the verdicts tree" (`6dd6c82…`). The verdicts commit adds a third `"18 healthy"` hit in SCORECARD (the r72 verdict row's own quotation: 3 at the tip vs 2 recorded), consistent with the disclosed-collision arithmetic (original + quotation per hit) but not equal to the recorded count. **Route:** state the measurement tree exactly where the counts are recorded; a count line's tree is part of its re-derivation context. All 16 after-side counts otherwise re-derive at the tip.
3. **Carried (not charged):** the flock(1) operator decision (L0 since r70); the host-load lineage loop is ALIVE AND RESPAWNING — the L0 follow-up (fleet `.ufo/l0-questions.md` line "chousa | round-72", verified present; census-selfmatch receipt pass 2 shows two fresh children created at census time 15:33:42) correctly escalates that killing two PIDs will not clear the window; the L2-floor template question; the SHONEN promotion review and non-author entailment review remain operator-schedulable — no review was manufactured this round. Operator note (unchanged since r69/r70/r71): all four SHONEN boxes still look checkable by a non-author promotion review; the r72 re-file is conformant in form (heading + 4 `[~]` with resolvable pointers) but remains lane-assertion.

## 7. Closure ruling

`admitted=false`, verdict **`rejected-honest-stop`** — the frozen rule decides it: C1's completing predicate was not met (anchored verdict-line count 0, receipt-verified), the rule's own honest-stop arm applies to exactly this event, and admission requires every claim to verify. C2 verified and no axis is harmed, but "every claim" fails with C1.

**On the materially-different-posture question put to this closure:** the evidence posture is materially stronger than r70/r71 — the timeout-wrap is no longer a unit-tested patch but a production-proven bound (named FAIL-case at rc 124, verdict unmeasured, never a pass), the battery passed the chain's stall point for the first time (~260/275 cases, 14350 s), the new crash site is captured to the byte, and the r73 route is fully measured (~14 s/case quiet window → 64–90 min per battery). But the legal posture is identical: the one predicate C1 claimed — completion — was again unmet, the rule forbids editing the predicate after measurement, and production proof of the *bound* is route progress, not completion of the *claim*. The honest-stop ruling stands; the stronger posture is recorded here and in the closure notes and should shorten r73's route, not flip this round's admission.
