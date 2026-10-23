# Round 29 — routed-items audit (read-only): what the two spot-check notes asked for, and where each item stands

Seat `ScoutSpotcheckRoutes`, leaf, read-only. Judged axis: operability. No file outside this
directory was written; no git or jj write command ran; nothing was installed or updated
(no tool installs this seat). Network: none.

## Method and evidence commands (all bounded, all exit 0 unless noted)

- `read corpus/lessons/round-28-verifier-spotcheck.md`, `read corpus/lessons/round-27-verifier-spotcheck.md`.
- `git -C <lane> log --oneline 6c5eb146 -5` → exit 0: `6c5eb14`, `7c87b97`, `11d7c5d`, `457fbb0`, `4f48419`.
- `git -C <lane> rev-parse HEAD` → `8026fe6010804720ad10dbd4e4c8b1d7ae9ec490` (round-29 v2 control
  receipts, committed `2026-10-22T22:22:45-03:00`, before this seat started). Every status below
  names the revision read: `8026fe6`.
- `git -C <lane> diff --name-only 6c5eb14 HEAD` → the 3 round-29 commits plus one `considerthese/`
  file. **No** legacy file named by the round-28 routing (LOG.md, SCORECARD.md, SKILL.md,
  `corpus/README.md`, `corpus/SOURCES.md`, `corpus/lessons/round-28.md`, `corpus/evidence/round28-safe/*`)
  is in that list.
- `git -C <lane> log --oneline 6c5eb14..HEAD -- LOG.md corpus/lessons/round-28.md` → empty (D3 unlanded).
- `git -C <lane> log --oneline 457fbb0..HEAD -- corpus/evidence/round27-claims.md corpus/evidence/round27` → empty.
- `git -C <lane> log --oneline 6c5eb14..HEAD -- tools/` → empty (no baseline re-pin).
- `grep -rEn '\b[a-z]{2,}[0-9]{2,}\b'` over the named files; digit-glued counts cross-checked against
  the sibling sweep `.ufo/waves/round-29/build/ScoutCustodyVocab/sweep.tsv` (read-only) and my own
  recomputation. Raw regex counts include identity and path tokens (`sha256`, `r24`, `round29`,
  `corpus/evidence/round29/…`); the prose subset is the smaller number quoted per row.
- `find . -name "operator*" -not -path "./.git/*"` → empty (see the operator-teaching row).
- Witness read: `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/chousa28-negative-records/parent-census.json`
  → `exit: 0`, `at: 2026-10-22T02:49:09.859760+00:00`, `actual_safe_commit: 7c87b973…`, stdout
  `chousa\tok\t…/corpus/SOURCES.md`.
- Counter read: `grep -n "secrets.randbits" corpus/evidence/round29/c1-count.py` → lines 231 and 250.

## Table 1 — round-28 spot-check defects D1–D5 and its routed items 1–5

| Item | Routing text (path:line) | Later lane commit status | Proposed disposition this round |
|---|---|---|---|
| D1 run-together tokens (r28 line 42–45) | "**D1, run-together tokens.** The report contains 23 distinct digit-glued tokens, for example `all69`, `proposal64`…" (line 42) | **Unaddressed in committed bytes.** Legacy files unchanged since `6c5eb14`. Live counts at HEAD: LOG.md 158 (66 distinct), SCORECARD.md 91, SKILL.md 31, `corpus/README.md` 64, `corpus/SOURCES.md` 59, `corpus/lessons/round-28.md` 9 (prose subset 3: `all69`, `most25`, `proposal64`). Round-29 new prose is clean: `corpus/evidence/round29/claims.md` 0; the 8 control reports show only `round29` (60) and `r29` (14), all path or round-identity tokens | **QUALITY criterion (proposed 23): "New prose separates digits from words; a digit-glued count is reported with identity/path tokens excluded, and legacy files are corrected only by an append-only dated note when touched."** Legacy bytes: **carried with reason** — the routing itself says not to rewrite old entries (line 125) |
| D2 custody vocabulary (r28 line 46–49) | "**D2, custody vocabulary outside the canonical round.** The report, LOG, SKILL, README and lesson use [approval-source phrase], `CURRENT_MAIN_DIRECTIVE …`, private original hashes and [publication-order phrase] publication." (line 46) — offending phrases elided here per the round-29 prose rule | **Unaddressed in committed bytes.** Live at HEAD: LOG.md:1179, `corpus/SOURCES.md:85`, `corpus/evidence/round28-safe/provenance.json:3`, `corpus/evidence/round28-safe/claims.md:21`, `…/qualifiers.md:7`, `corpus/lessons/round-28.md:26,53,57,63`. Round-29 committed drafts carry none (only "the parent of `tools/`", `claims.md:68`, a filesystem relation) | **QUALITY criterion (proposed 24): "Lane records state the round, its prompt and its receipts; approval-source, directive-ID and private-hash prose stay out."** Legacy bytes: **carried with reason** (append-only record) |
| D3 stale end-census statement (r28 line 50–54) | "**D3, stale statement in committed lane files.** `corpus/lessons/round-28.md` says "No end census has been run"… The fleet-committed witness … records exit 0 against `7c87b973` at 2026-10-22T02:49:09Z." (line 50) | **Unaddressed at HEAD `8026fe6`**: `git log 6c5eb14..HEAD -- LOG.md corpus/lessons/round-28.md` empty; LOG.md:1177 and `corpus/lessons/round-28.md:57` still read as if no census ran. Round-29 BUILD has a seat assigned to the witness check (`.ufo/waves/round-29/build-spec.json:58`) | **Fixed this round (in flight, must land before the report):** append a dated correction to LOG.md and the round-28 lesson or the round-29 lesson naming the witness path, `exit 0`, revision `7c87b973` and time `2026-10-22T02:49:09Z`; do not rewrite the old lines. I re-read the witness myself and it matches the routing text |
| D4 no re-run in the report (r28 line 55–56) | "**D4, no re-run in the report.** … "not a command rerun for this draft". PROTOCOL §Evidence standard says "Claimed ≠ re-executed"." (line 55) | **Frozen record, not rewritable.** No later commit touches the round-28 files. Round-29 practice already complies: `corpus/evidence/round29/claims.md:39,42` give before and target as one re-runnable command; the before receipt carries `cmd`, `exit`, `wall_s`, `at`; each control report quotes its command, verbatim output and both exits (e.g. `CtlRawGrep/report.md:42,46`) | **QUALITY criterion (proposed 25): "Every before→after count in a report is the output of a re-run command, quoted with cwd, exit code and seed."** Nearest existing rules 13 and 15 do not state this (13 governs `recheck:` placement, 15 governs digest/revision pinning) |
| D5 long wall time (r28 line 57–59) | "**D5, long wall time.** 8 h 21 min passed from launch to the driver completion line. The report commit landed 4 h 59 min before the driver completion line." (line 58) | **Unaddressed.** `grep -rniE "wall time"` over the round-27/28 lessons and LOG.md returns only that line. Round-29 control reports do record per-command `wall_s`; no round-level wall-time statement exists. Round-29 driver launch: `.ufo/watchdog.log:796`, `2026-10-22T22:03:00-03:00`; no completion line at my read time | **QUALITY criterion (proposed 26): "The round record states launch-to-complete wall time from `.ufo/watchdog.log` and the report's own lag; the criterion is disclosure, not a speed target."** The lane cannot shorten driver time |
| Routed 4, C1 open and surface rotation (r28 line 132–134) | "4. C1 stays open. Next round: declare an after-state that one command over committed bytes can re-derive. The R27 C3 complete-path versus prefix-control conflict and the ancestor over-refusal (S045) are still unresolved. This is the same axis and surface for the second round running, so a third round on it would trip the frontier-rotation sentinel." (lines 132–134) | **Partly satisfied by round 29's own design.** `corpus/evidence/round29/claims.md:28` states the claim "is a different surface from the path-denylist and ancestor work of rounds 26 to 28", and `:42` declares the after state as one command. The R27 C3 conflict and the S045 over-refusal remain **untouched** — `git log 457fbb0..HEAD -- corpus/evidence/round27*` empty | **Carried with reason** for the C3 conflict and S045 (operator-owned; no round-29 claim covers them, so the rotation sentinel is not tripped). The after state is one command but **not** byte-derivable only: the v2 counter draws 48 items from live pages at run time (`claims.md:47–56`). See the appendix row for the seed-replay caveat |

## Table 2 — round-27 spot-check decision and "Trends and routing" items

| Item | Routing text (path:line) | Later lane commit status | Proposed disposition |
|---|---|---|---|
| R27 decision, harm retained | "**Not admitted; rejected-harmed.** … C3 calibration's original complete-filesystem-path clause remains falsified, and r27 introduces a new canonical-path over-refusal. Do not net that harm against green counts, relabel it as a control, weaken frozen expectations or admit the union of incompatible rules." (line 8) | **Held.** C3 text unchanged (`corpus/evidence/round27-claims.md:15` at HEAD matches the original clause). SCORECARD.md tail (round-28 section) states "The original R27 C3 clause, controls and rejected-harmed result remain unchanged" and keeps the claim "**not achieved / unprovable**". No commit re-pins a baseline | **Held, carried.** Existing criterion 5 ("A rejection is kept, not silently dropped") is the capture rule; the round-29 record must restate the red rather than net it. No new criterion |
| R27 decision, root accounting | "Native root accounting still requires the malformed-round repair/executable status proof; this note does not publish a MANIFEST row or grant a whole-ledger pass." (line 9) | **Untouched.** `find . -maxdepth 2 -name "MANIFEST*"` → empty; no round-28/29 commit touches root accounting | **Carried with reason:** operator-owned, outside the C1 surface |
| R27 routing, keep the red visible | "Next authorized round must keep the original C3 text, frozen negative controls and current red visible; do not pre-empt L0 by inverting expectations." (line 67) | **Satisfied so far.** C3 text and round-27 evidence untouched; round 29 declares a different surface (`claims.md:28`) and inverts no expectation | **Held / carried.** No new criterion; criterion 5 plus the SCORECARD retention line |
| R27 routing, ancestor over-refusal | "If addressing the new ancestor-wide canonical over-refusal under a separately declared claim, preserve actual denied-path identity and the old counterexamples." (line 67) | **Not addressed** by round 29 (different surface). Condition never triggered | **Carried with reason** (open, operator-owned L0). If ever triggered, criteria 20 and 22 are the capture rules |
| R27 routing, parser and identity boundaries | "Keep parser errors distinct from no-match, exact token/width boundaries and original187/legacy161 identities." (line 67) | **Encoded in round 27** as criteria 19 ("A diagnostic phrase is not a verdict record") and 22 ("Matcher failure is not zero matches"). Identities persist: `original187`/`legacy161` appear in SKILL.md, SCORECARD.md and LOG.md, and the SCORECARD tail states the ordinals "are held, not repinned". Round-29's frozen tool contract states an exact block-element list (`claims.md:87–90`), a 25-word limit (`:76`) and an alnum boundary rule (`:97–98`) | **QUALITY criterion (already exists: 19, 22)** — record as covered, not new. **Carried** for the gate surface |
| R27 routing, authority bounds | "No live target, credential custody, sibling change, baseline re-pin or cleanup authority follows from this note." (line 67) | **Held.** `git log 6c5eb14..HEAD -- tools/` empty; no sibling or credential action. Round-29 does fetch live registry URLs, but that bound comes from the round-29 prompt and `claims.md:81–84`, not from the round-27 note | **Held / carried** as a standing bound; record the source of the round-29 network authorization explicitly |
| R27 trend verdicts | "**Expansion unchanged:** no new admitted knowledge/capability. **Quality harmed:** new canonical over-refusal is not offset by C1/C2 repair. **Discernment unchanged:** …" (line 65) | The `quality harmed` verdict is retained in the round-28 spot-check and the SCORECARD tail | **Carried** — same item as the R27 decision row; the round-29 record must carry "quality harmed" forward until an authorized repair lands |
| Operator teaching files | n/a — existence check only | `find . -name "operator*" -not -path "./.git/*"` inside the lane → **empty**. Fleet-wide, the only `operator-*.md` files are `.ufo/scopes/shokunin-12h-20261014/operator-demand.md` and `.ufo/scopes/souji-mint-20261018/operator-demand.md`, outside this lane | **No rows to audit.** The one operator-owned item inside the audited text is L0 complete-path versus prefix-policy adjudication (r27 line 61) — **carried** |

## Appendix — round-29 in-flight item found while auditing routed item 4 (not from the audited lists)

| Item | Evidence | Status | Proposed disposition |
|---|---|---|---|
| Committed-seed replay reaches the frozen target | `.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2-warmed.json` and `-warmed-seed2.json`: `match 130`, `total 130`, `predicate_holds: true`, seeds 2901 and 2902, `wall_s 0.03`, at `2026-10-23T01:21:20Z`, no fetch. Unchanged control: `106/130` on both seeds; fresh seed 2848469338: `106/130`, `predicate_holds: false`. Frozen rule, `corpus/evidence/round29/claims.md:150–151`: "Any control that reaches 130/130 voids v2 too" | **Live disagreement.** The commit message at HEAD reads "max 106/130 under fresh seed; seed-replay cheat 130/130 only on committed seeds". The mitigation is real and checkable: `c1-count.py:250` defaults the seed to `secrets.randbits(32)`, and the frozen predicate command (`claims.md:32`) passes no `--seed`, so the after run cannot be replayed. But the rule text as frozen is unconditional, and the two committed seeds now have published labels | **Record, do not net.** Proposed criterion 27: "A predicate's after run uses a seed that was never published together with its labels, and the receipt names the seed." Either the L1 states the fresh-seed reading in the round record, or the design is voided under its own frozen text — silently calling the cheat "only on committed seeds" is not enough |

## Limits

- Statuses are as of HEAD `8026fe6` (committed `2026-10-22T22:22:45-03:00`); the round-29 branch is
  still open, so a later commit may land the D3 correction and the criteria.
- Counts are raw-regex and prose-subset counts, not semantic verdicts; the sibling sweep
  (`ScoutCustodyVocab/sweep.tsv`) uses a slightly different exclusion set, so its per-file numbers
  are larger (LOG.md 158 vs my 127). Both agree on the files that carry genuine prose tokens.
- I did not run any lane tool, counter or control; every control value above is read from committed
  receipts, not re-measured. No source page was opened by this seat, so no quote is cited here.
- The D2 row elides two custody phrases; the routing line itself is at
  `corpus/lessons/round-28-verifier-spotcheck.md:129`.
- Inference markers: the "must land before the report" clause for D3 and the criterion numbers
  23–27 are proposals, not observed lane state.

Report: .ufo/waves/round-29/build/ScoutSpotcheckRoutes.md
