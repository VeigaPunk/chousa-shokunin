# R57W1ReviewReportShape — L1 filing checklist

Axes: freshness, depth, calibration. Sources opened: fleet `.ufo/prompts/chousa-round-57.md` §§4–6 (lines 99–129, 141–167, 399–473); `scripts/hyaku/lane-addendum.md` §§6–7; `MANIFEST.json` chousa round 55/56 closure notes; `corpus/lessons/round-55-verifier-spotcheck.md` and `round-56-verifier-spotcheck.md`.

## Numbered filing gates (tick in order)

1. **Wait for the wave to settle before filing.** Do not draft/commit the fleet report until the orchestrator sends `WAVE-DONE w1` and `.ufo/waves/round-57/w1-results.json` exists. Verify the handoff against the 65 dispatched items:
   ```sh
   python3 - <<'PY'
   import json
   p='/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-57/w1-results.json'
   d=json.load(open(p))
   print('seats=',d['seats'],'results=',len(d['results']))
   assert d['seats']==len(d['results'])==65
   PY
   ```
   Observed at this check: no r57 results file yet; dispatch `taskCall.tasks` = 65 and spec `items` = 65. Do not treat this as settled until WAVE-DONE + results handoff.
2. **Use the §4 required sections, in exactly this order:** `## Work performed`; `## Landed changes`; `## Before → after measurements`; `## Sources & frontier`; `## Trend verdicts`; `## SHONEN`. `Work performed` opens by naming 1–3 declared claims and their target axes/capability, then one evidence-backed bullet per work item. Landed changes map every change to a LOG.md entry and carrying commit. Measurements give one counting command + measured commit per claim. Sources & frontier gives SOURCES rows before→after/counting command, tier additions, old→new touched rows, frontier advances; if none, write `SOURCES: unchanged — main-repo lanes hold no corpus/` only for a main-repo lane (not this lane). Trend verdicts give separate expansion/quality/discernment verdicts (`improved|harmed|unchanged|unprovable-but-better`) with evidence; no scalar. Prompt source: round-57 §4 lines 101–119.
3. **Apply marker rules honestly.** A contentless/placeholder report, no evidence pointers, or omission of any required section *except* Sources & frontier and Trend verdicts is marker `failed` and causes same-round relaunch. Omitting only Sources & frontier and/or Trend verdicts is `ok` with a minimum-content conformance defect, not a failure marker. The watchdog checks the Sources & frontier marker and source-census gate, not trend verdicts or full claim admission; driver completion is not admission. Each SHONEN box gets exactly one report line: `[x]` only with a named non-author verifier; `[~]` only with a resolvable evidence pointer; `[ ]` if untouched. Do not mark `[x]` as author. Round-57 prompt §4 lines 121–129.
4. **Run the SHONEN heading gate immediately before report commit.** Exactly one heading, then one status line per lane checklist box (four boxes observed in lane `SHONEN.md`):
   ```sh
   grep -c '^## SHONEN' /home/vgpnk/Projects/shokunin/.ufo/reports/round-57/chousa.md
   ```
   Must print `1`. Count the report's checklist lines and compare with the lane boxes:
   ```sh
   grep -c '^- \[[x~ ]\]' /home/vgpnk/Projects/shokunin/.ufo/reports/round-57/chousa.md
   grep -c '^- \[[ x~]\]' /home/vgpnk/Projects/shokunin/chousa-shokunin/SHONEN.md
   ```
   Expected box count observed: `4`. Prompt §6 lines 472–473 requires the heading count and a `[~]`/`[ ]` line per box.
5. **Account for the whole wave and round in the report.** Include shape (one v2 wave), seat count, role mix, attack share, dead seats with last error, residual call (or none), round total, and L1-held planner mapping; derive seat/death facts from `w1-results.json`, not memory. Round-57 §6 lines 315–324, 341–348.
6. **Misroot sweep before report.** Inspect fleet-root changes without a pathspec (seat notes land there):
   ```sh
   git -C /home/vgpnk/Projects/shokunin status --porcelain
   ```
   For each *untracked seat-authored* file whose content names this lane/round: copy byte-exactly to the same relative path under `/home/vgpnk/Projects/shokunin/chousa-shokunin`, verify `cmp -s <fleet-path> <lane-path>`, then remove only that fleet copy; record it under report `## Mistakes`. Never touch another lane's file, `.ufo/state/*`, or fleet `.scratch/`. Round-57 §6 lines 405–412. At this check fleet status was empty; lane was mid-work (`tracked=2 untracked=50`), not a final clean-state result.
7. **Pre-report remote gate, before writing/committing the fleet report.** The lane branch is `master`; obtain the final full hash from the lane helper state, then:
   ```sh
   git -C /home/vgpnk/Projects/shokunin/chousa-shokunin ls-remote origin refs/heads/master
   ```
   It MUST print the final lane hash cited in the report. If remote is older, push the lane via the lane helper and repeat. Do not infer the pushed hash from detached `HEAD` or `@{u}`. This gate prevents the round-55/56 class of report/tip mismatch. Prompt §6 lines 468–471.
8. **Commit lane evidence only with the lane helper.** From L1, commit only intended lane paths (including wave evidence) and cite only its final `landed <hash>` after remote verification:
   ```sh
   /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh commit /home/vgpnk/Projects/shokunin/chousa-shokunin --as chousa -m 'round-57: <what>' -- <repo-relative-path>...
   /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/chousa-shokunin
   git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain
   ```
   Require `ahead=0`, no unexpected leftovers; re-run the pre-report ls-remote gate against final branch hash. Never use raw git/jj mutation in lane. Prompt §6 lines 413–461.
9. **Commit the report last, through fleet helper only.** The report is fleet path `.ufo/reports/round-57/chousa.md`; after gate 4 and gate 7:
   ```sh
   /home/vgpnk/Projects/shokunin/scripts/hyaku/fleet-commit.sh --as chousa -m 'round-57: chousa report' -- .ufo/reports/round-57/chousa.md
   git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-57/chousa.md
   ```
   Accept only helper's final `landed <hash>` after successful remote verification; report commit author must be lane identity. No raw `git add/commit/push`. Template commands: round-57 §6 lines 462–467; helper usage observed at `scripts/hyaku/fleet-commit.sh:17,32`.
10. **Close out the handoff.** Include the final lane/report hashes, wave settlement/counts, Stale-lane line, tool installs (or none), open L0 items, and scratch cleanup in the report. Remove `/fast/scratch/hyaku/chousa-r57` only after all wave receipts are committed; keep the round-one scratch contract (`trap 'rm -rf -- "$S"' EXIT`). Run the lane census gate required by §10 and report its exit/output; never claim an unrun check passed.

## Closure defects not to repeat

- **Round 56 closure D1 (status-neutral):** correction sweep missed `corpus/knowledge/grey-literature-field-china-r42.md:9`; its `recheck:` instruction still named the journal's 表 10 row after the correction to 表7. Round-56 verifier spotcheck lines 33–36 / 105–106; MANIFEST round-56 notes. Sweep every occurrence, including instructions, not just body/quote/SOURCES text.
- **Round 56 closure D2 (status-neutral):** three C1 driver attacks were unmeasured (`R56CritC1Forge` ENV, `R56MutC1Driver` inconclusive after cache deletion, `R56MutC2Counter` fragment) and disclosed as unrun, not survived. Round-56 verifier spotcheck lines 33–36; MANIFEST round-56 notes. Report every attack's evidence-backed outcome; never imply a failed-to-measure test survived.

Related report-filing precedents covered by gates 1, 4, 7: round-55 closure D1 filed before W1 settled (35/48 reports, no results handoff; W2 not dispatched); round-55 D3 cited C2/C3 at a revision different from receipt headers / no receipt for claimed rerun. Sources: fleet MANIFEST.json round-55 closure notes and `corpus/lessons/round-55-verifier-spotcheck.md:27–36`.

Commands actually run / observations: `grep -c '^## SHONEN'` on round-56 report → `1`; SHONEN lines → `4`; lane `jj-lane.sh state` → `branch=master local=remote=e0e73e0f… ahead=0 behind=0 head=detached tracked=2 untracked=50`; lane `ls-remote` → `e0e73e0f… refs/heads/master`; fleet `git status --porcelain` → empty. `w1-spec.json` items = 65; dispatch `taskCall.tasks` = 65; r57 results handoff absent when checked. Scratch directory removed before yield.

VERDICT: Built the R57 filing checklist; the report-shape gates are actionable, and the round-56 closure's D1/D2 must not recur.
