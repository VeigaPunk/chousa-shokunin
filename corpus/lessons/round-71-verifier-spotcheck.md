# Round 71 verifier spot-check — chousa (closure, non-author)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))
Date: 2026-11-01. Round closed at lane tip `211130ddff232863825bc8faee3ad0ec46db35ec` (base `11b51988d3878cd33b826295304f6f266718ba86`). I did not author this round; everything below was re-derived in a fresh session from committed bytes (`git show <tip>:<path>`, `git diff-tree`, `git merge-base --is-ancestor`, `sha256sum`) — no sibling gate was executed, per the closure contract.

**Round verdict: not admitted — C1 honest-stop per its frozen rule, concurred; C2 verifies (improved); no axis harmed. Every reported count re-derived exactly; three minor number/record drifts found (status-neutral, routed to round 72).**

## 1. Step-1 conformance

| check | method | result |
|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H' -1 -- .ufo/reports/round-71/chousa.md` (fleet repo) | PASS — `chousa-shokunin <chousa@shokunin.local> cef6ad99386f40a56dedd6c11a6de7b186617eda` |
| SHONEN assessment | read report bytes | DEFECT (minor) — the four `[~]` lines with resolvable pointers are present, but under the inline line `SHONEN: lane has SHONEN.md —` (report line 36), not the `## SHONEN` markdown heading used by the r69/r70 reports. Per PROTOCOL this is a conformance defect and this round's assessment is disqualified as promotion evidence — re-file under `## SHONEN` in the round-72 report. Status-neutral; does not affect the round outcome (all boxes are lane assertions; the promotion review remains operator-scheduled). |
| cited commits exist + are ancestors | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> refs/heads/master` for 58232b27, e5458b35, 211130dd (+ b2f88ecc cited by S177) | PASS — all exist and are ancestors of master |
| lane tip pushed | `git ls-remote origin refs/heads/master` vs local `rev-parse` | PASS — both `211130ddff232863825bc8faee3ad0ec46db35ec` |
| cited work in round range | `git log 11b51988..211130dd` | PASS — exactly the three round commits (freeze 58232b27, landing e5458b35, verdicts 211130dd), all authored `chousa-shokunin` |
| dispatch/complete digest | `.ufo/watchdog.log` lines 270/281 | PASS — `2026-11-01T12:27:56-08:00 launch chousa round=71 base=11b51988d387 (zcode run14)`; `2026-11-01T14:08:50-08:00 complete chousa round=71 head=211130ddff23 pushed=True` — matches the closure digest verbatim |
| marker vs report | content read | PASS — real report: work performed with evidence pointers, landed changes tied to the LOG round-71 entry, paste-able counting commands with measured commits; not a marker |
| frozen-claim discipline | `git rev-parse A:<f>` vs `tip:<f>` for claims.md, before-r71-defect-greps.txt, probe-timeout-capability-r71.txt, census-start.txt | PASS — all four blob ids byte-identical between commit A `58232b27` and the tip: no predicate or before-receipt was edited after measurement |

## 2. Per-claim re-check (commands I ran, output I observed)

### C1 — operability (honest-stop per the frozen rule) — CONCUR

- **Do-nothing control re-derived:** `git show <tip>:corpus/evidence/round70/controls/after-battery-completes-r70.txt | grep -c "^RESEARCH_GATE_SELFTEST:"` → **0**. The r70 battery has no verdict line on committed bytes.
- **Honest partial re-derived:** `git show <tip>:corpus/evidence/round71/controls/battery-partial-r71.txt | grep -c "^RESEARCH_GATE_SELFTEST:"` → **0**; the receipt discloses the kill (case 8/9, wrapper died in the same pass, **no EXIT line — disclosed as the kill's record**), rate samples 331s→3, 429s→5, 850s→8 lines.
- **The repair is as described:** `git diff-tree -r -p <base> <tip> -- tools/research-gate.sh` shows exactly 3 hunks (new-file lines 4404, 8356, 8371 — report said 4405/8342–8372, same hunks), 21 insertions + 1 deletion, all inside `run_selftest`: (h1) the one-time `HAVE_TIMEOUT` capability probe requiring `timeout 1 sleep 5` → rc 124 (capability, not existence) + `LC_BOUNDARY_BUDGET_S="${LC_BOUNDARY_BUDGET_S:-900}"`; (h2) the case-258 invocation wrapped in `timeout "$LC_BOUNDARY_BUDGET_S"` only when `HAVE_TIMEOUT=1`, else base behavior verbatim; (h3) on rc 124 the FAIL-case line is followed by `case-note %-29s reason=locale-boundary budget %ss exceeded (timeout); verdict unmeasured within budget`, and the case still counts `failures=$((failures + 1))` — never a pass. No case input, expected rc, or expected token changed.
- **Unit verification evidence-verified (gate not executed):** `timeout-arm-focus-test.txt` (committed) shows the patched block's own lines with a forced 1 s budget: `PROBE HAVE_TIMEOUT=1 tprobe_rc=124 budget=900`, `CASE_RC=124`, `CASE_OUT_LINES=1`, the case-note bytes, `script_rc=0` — the bound fires and names itself. Its pinned tool sha256 `d5d48128509f77edf161e4d8b10b833e6e00f822906460fa049f27d1244d41e2` I re-derived myself: `git show e5458b35:tools/research-gate.sh | sha256sum` and `git show <tip>:tools/research-gate.sh | sha256sum` both print exactly that digest (the same bytes at landing and tip; the diff index `a5780cd6` matches the digest-receipt's blob oid). The same pin is carried by `battery-partial-r71.txt`; `after-digest-derivations-r71.txt` records `DIGESTS_IN_TREE=1/1 PASS` twice over both receipts.
- **Freeze probe (the sizing ground):** `probe-timeout-capability-r71.txt` (frozen at A, byte-unchanged since) shows `tprobe_rc=124` and the case-258 body uncontended `real 0m16.333s` … `case_rc=0`, `RESEARCH_GATE: CLEAN` — so 900 s ≈ 55x the uncontended duration, and the r70 >70-min hang reads as contention variance.
- **Frozen rule applied faithfully:** the rule froze "battery verdict line (anchored count 1) + preflight `SKIPPED=none` → improved; battery still dies before its verdict line, **or the preflight cannot complete within its budget** → honest-stop with red receipts committed and residual routed". Neither completing receipt exists (no `after-battery-completes-r71.txt`, no `preflight-final`); the honest-stop is the rule's own arm, not a negotiation. **CONCUR.** The lane claims no operability improvement and leaves the score at its historical value — consistent.

### C2 — calibration (improved) — VERIFIES, every count re-derived exactly

All commands run by me over `git show <tip>:<path>`:

| count | observed | reported |
|---|---|---|
| `grep -c "dcCFup"` over `round70/controls/recon-run-r70.txt` | 0 | 0 ✓ |
| `grep -c "dcCFup"` over `round70/controls/before-g08-selftest-partial.txt` | 7 | 7 ✓ |
| `grep -c "K1Yhut"` over `recon-run-r70.txt` | 19 | 19 ✓ |
| `grep -c "supersedes S171" corpus/SOURCES.md` | 1 (0 before) | 0 → 1 ✓ |
| `grep -c "^correction: corpus/lessons/round-70.md D-70" corpus/lessons/round-70.md` | 1 (0 before) | 0 → 1 ✓ |
| `grep -c "^RESEARCH_GATE_SELFTEST:"` over the r70 transcript | 0 (unchanged, the true fact) | 0 ✓ |
| `grep -c "reason=no flock(1): append fails closed"` over the r70 transcript | 5 | 5 ✓ |
| `grep -c "257/269" corpus/lessons/round-70.md` | 3 (2 before; third hit is the correction block's own quotation, disclosed) | 2 → 3 ✓ |
| `grep -c "the battery completes and prints" SKILL.md` | 0 (1 before) | 1 → 0 ✓ |
| `grep -c "the battery does NOT complete into a verdict line" SKILL.md` | 1 | 1 ✓ |
| `grep -c "^| S17[3-7] " corpus/SOURCES.md` | 5 | 5 ✓ |
| `grep -c "^| S[0-9]" corpus/SOURCES.md` | 177 | 172 → 177 ✓ |
| rejected rows | 14 | 13 → 14 ✓ |

Append-only discipline verified by diff: `corpus/lessons/round-70.md` additions-only (the 8-line correction block); `corpus/SOURCES.md` additions-only (S173–S177; no held cell of any pre-existing row changed); `SKILL.md` row 83 corrected in place exactly as the frozen fix prescribed; **no `corpus/evidence/round70/*` receipt byte changed** (absent from the round diff). The r70 closure ruling (honest-stop, not admitted) is undisturbed. D-70-6 is answered by S177 (below). **VERDICT: improved — CONCUR.**

## 3. Discernment spot-check (non-author, ≥1 admit + ≥1 reject)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S173 (admit, tier B, scoped to the routed defects + ruling) | admit | `corpus/lessons/round-70-verifier-spotcheck.md` line 84 | **agree** | the ≤25-word quote — `correct the row to the measured state (runs truthfully through case 257, ended at case 258, no verdict line; honest-stop)` (20 words) — is verbatim at §5 D-70-5; the tier-B scope (the six routed defects and the ruling, nothing more) is honest |
| S174 (admit, tier B, the honest-red state + D5 sizing ground) | admit | `corpus/evidence/round70/controls/after-battery-completes-r70.txt` RUN-END ADDENDUM (lines 308–309) | **agree** | the quote — `the run was ended by the round at case 258 (claims-locale-boundary) - its gate ran >70 minutes without emitting the case line` (22 words) — is verbatim (spanning the ADDENDUM's line wrap); the row is admitted for the red state, explicitly *not* as a completing run |
| S176 (admit, tier B, location-attribution correction superseding S171) | admit | both r70 crash captures re-grepped | **agree** | dcCFup lives in `before-g08-selftest-partial.txt` (7) and not in `recon-run-r70.txt` (0; 19 K1Yhut) — same crash site (line 5548), different capture, exactly what S176 records; the supersedes scope (location only, teaching and tier stand) is correctly narrow |
| S177 (REJECT, tier C, post-open) | reject | `SKILL.md` at `b2f88ecc` (ancestor, verified) | **agree** | at `b2f88ecc` row 83 reads `the battery completes and prints` + `RESEARCH_GATE_SELFTEST: FAIL (k/N cases, 6 skipped)` — the very assertion S177 records — while its own cited receipt (`after-battery-completes-r70.txt`) shows anchored verdict-line count 0 and the ended-at-258 ADDENDUM. A genuine post-open rejection with a flip that landed (the D-70-5 correction). This is exactly the reject sample D-70-6 asked a future round to surface |

New-row quote rule: S173's quote is 20 words (≤25) and located (§5, D-70-5, at the named commit). `bash scripts/sources-census.sh validate --root <fleet root> chousa` → **exit 0** with only the five pre-existing W04 duplicate-url warnings — identical to the committed `census-end.txt`.

## 4. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | **unchanged** (C1 honest-stop per its frozen rule) | the timeout-wrap lands, is unit-verified (focus test rc 124 + case-note; pinned sha re-derived), but the frozen completing predicate was not met and none is claimed; score deliberately unmoved; gate stays red without flock, disclosed |
| calibration | **improved** (C2) | all six routed D-70 items closed; every count re-derived exactly by this check (§2); append-only discipline held; the r70 ruling undisturbed |
| depth | **unchanged** | all five new rows are own-work tier B/C records; no externally-grounded entry |
| freshness | **unchanged** | no drift surface measured; S173–S177 are `on-release` own-work records |
| coverage | **unchanged** | PROVINCE.md untouched (absent from the round diff); repair stays inside the lane's gate/records ground |
| adjacency | **unchanged** | the two orphaned sibling-lane `souji-verify.sh` lineages are identified with start times/CPU-seconds/args and filed to the L0 queue (`.ufo/l0-questions.md` line 254, `chousa | round-71 | Host load relief…`), explicitly **not killed from this lane** ("adjacency: report, never absorb"), never treated as answered — lane-local scope discipline held |

No axis is harmed: SCORECARD diff is additions-only (planned + verdict sections); every verdict cell is unchanged/improved/honest-stop.

## 5. Trend verdicts

- **expansion: unchanged** — CONCUR. All five rows are own-work records inside ground the lane already holds; no new `corpus/knowledge/` file and no PROVINCE.md in the round diff.
- **quality: unchanged** — CONCUR. The repair lands and is unit-verified but its completing verification is routed; no operable-capability improvement is recorded; the measured contended rate (~86–110 s/case, three samples) is committed as the route instead of padding the verdict.
- **discernment: improved** — CONCUR (checked from outside). The gate's admits and the reject all survive re-opening (§3: 4/4 agree); the corrections are counted and append-only; an over-assertion was caught against its own cited receipt (S177/D-70-5); the round's own slips are mined (four `## Mistakes` rows, including the census E11 the gate itself caught — exit 1, fixed, re-run to exit 0; my validate re-run reproduces exit 0).

## 6. Defects routed to round 72 (all status-neutral; none verdict-bearing)

1. **SHONEN heading form (conformance).** The report carries the four `[~]` box lines with pointers under the inline line `SHONEN: lane has SHONEN.md —` instead of the `## SHONEN` heading (the r69/r70 form). Per PROTOCOL the assessment is disqualified as promotion evidence; **re-file the SHONEN assessment under `## SHONEN` in the round-72 report.**
2. **Number drift: "18 healthy ok-case lines … across two runs"** (report Work-performed, SCORECARD verdict row, lesson Trends line, LOG round-71 entry). The committed receipts carry **9** (`battery-partial-r71.txt`) + **16** (`killtest-partial-scratch-copy.txt`) = **25** ok-case lines; 18 is not re-derivable from the committed bytes (direction is conservative — under-count — but a count must re-derive). Correcting entry owed in the append-only LOG; state the per-receipt counts.
3. **Internal drift in `battery-partial-r71.txt`:** the header says "the transcript below ends at case 8" while the transcript shows **9** ok-case lines (the rate sample "850 -> 8 (killed)" is consistent with a 9th line printing before the kill). One honest statement of the final line count owed (correction block, per the D-70 precedent).
4. **LOG.md round-71 entry says "Mistakes: three rows"** and lists three; `corpus/lessons/round-71.md` `## Mistakes` carries **four** (the prose-in-used-by E11 row is missing from the LOG list). Append-only file — a new LOG correction entry naming the superseded text is owed next round.

Carried (not new, not charged): the completing run under a quiet window / host relief with `G08_SELFTEST_BUDGET_S` sized from the measured quiet duration (L0 line names the orphaned lineages); the operator's flock(1) decision (L0 since r70); the L2-floor template question (operator/protocol lane); the non-author entailment review and SHONEN promotion review remain operator-schedulable — no review was manufactured this round. Operator note: all four SHONEN boxes still look checkable by a non-author promotion review (the r69/r70 note stands, unchanged by this round's honest-stop).
