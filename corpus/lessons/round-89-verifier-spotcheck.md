# Round 89 — non-author verifier spot-check (hyaku closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane `chousa`, lane-round `89`. Base `f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8` (round-88 landing + its
non-author spot-check), lane HEAD at filing `a72f204bfeea10fc59497e23bcbda021a1a2ced5`. This file is the
non-author verification of record; the lane's own verdicts live in `corpus/lessons/round-89.md` and
`.ufo/reports/round-89/chousa.md`. I authored nothing in this round. I did not execute a sibling's gate as a
verification substitute: the two claim instruments were re-run directly against the committed tip tree (as in the
round-88 spot-check), and the lane-owned `research-gate` selftest and `lane-preflight` were re-run to confirm the
committed tallies.

Dispatch/complete digest (copied from the closure brief; `.ufo/watchdog.log` is mutable):
`2026-11-08T05:31:37-03:00 launch chousa round=89 pgid=2396342 driver=hyaku-inline attempt=1`;
`2026-11-08T06:27:54-03:00 complete chousa round=89; hyaku-inline attempt=1`.

## Step-1 conformance

1. Report committed in the fleet repo by the lane identity:
   `git log --format='%an %H' -- .ufo/reports/round-89/chousa.md` in
   `/home/vgpnk/Projects/shokunin` → `chousa-shokunin 3ad1062003c11ef5670c619e35345feffbc23d50`
   (`round-89: chousa report`, 2026-11-08T06:27:12-03:00). `git show --name-only 3ad1062` lists exactly
   `.ufo/reports/round-89/chousa.md` (pathspec-limited, no sibling sweep). Ancestor of `origin/master`
   (`git merge-base --is-ancestor 3ad1062 origin/master` → 0). Pass.
2. `SHONEN` heading present (report line 115) with one line per box: four `[~]` marks, each with a resolvable
   evidence pointer, no `[x]` — correct for a lane-authored assessment. All required sections present in order
   (Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN,
   Process notes). Real report, not a marker. Pass.
3. Every cited lane commit exists and is an ancestor of the branch ref `master` (never `@{u}`, the repo is
   jj-colocated and HEAD is detached):
   `ac0a0892c15de11fb28d3208f2b287687c00477e`, `976d422cd63fd4bcf3fb04cf8b5060a349e76382`,
   `a72f204bfeea10fc59497e23bcbda021a1a2ced5` → `git cat-file -e` OK and
   `git merge-base --is-ancestor <hash> master` → 0 for each. Lane `master` = `a72f204b`. Pass.
4. Lane repo pushed, no uncommitted round work:
   `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/chousa-shokunin` →
   `state branch=master local=a72f204b remote=a72f204b ahead=0 behind=0 head=detached tracked=0 untracked=0`;
   `git status --porcelain` in the lane repo prints nothing;
   `git ls-remote origin refs/heads/master` → `a72f204b…`. Pass.
5. Prompt carries the template contract: `diff templates/round-prompt.md .ufo/prompts/chousa-round-89.md`
   (lines 1–140) shows only the substitutions `{{LANE}}`=chousa, `{{ROUND}}`=89, `{{FLEET_ROOT}}`,
   `{{AXES}}`; the hyaku addendum §6 follows from line 141. Present: mission/axes binding (§1), 1–3 falsifiable
   claims (§2), frontier step (§2b), L2 floor ≥8 in one batched swarm with role split (§3), report contract +
   marker rule (§4), commit-then-push + push scope + L0 (§5). All five child-lane items are carried: report path
   (§4), commit-before-report ordering (§5 line 133), `SHONEN` heading (§4 line 118), commit-hash citation
   (Landed changes, §4), lane write scope (§5). The addendum's planner-seat ruling (L1 holds the canonical §3
   planner seat; `planner` is a frozen-topology validator rejection) is at line 393–397 and the report records
   that mapping. Pass.
6. Landed-last ordering: lane commits `ac0a0892` 05:45:24 -03:00, `976d422c` 06:26:32, `a72f204b` 06:26:40;
   report `3ad1062` 06:27:12 -03:00 — the report lands after the work it cites. Pass.
7. Wave / L2 floor: one v1 wave, 12 seats in the committed spec (`.ufo/waves/round-89/w1-spec.json` items=12:
   4 executor, 2 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 scout, 1 connector, 1 scribe), above the
   ≥8 floor; `w1-results.json` records `seats=12`, 12 seat reports on disk under `w1/`, 0 dead; every seat
   report carries a `VERDICT:` trailer (round-88 routed defect 7 met as a requirement). Pass.
8. Marker test: the report names real committed work with resolvable hashes, a checkable commit citation and the
   full section contract → status `ok`.

## Prefile falsification (addendum §8, Amendment 59)

Command (re-run by this closure, unedited):
`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane chousa --round 89` →
`PREFILE-FALSIFICATION: pass claims=2 rows=17 attack_seats=6 findings=0`, exit **0**.

Coverage and adjudication. The ledger `.ufo/waves/round-89/claim-falsification.tsv` covers both claims in
`claims.json` (C1 8 rows, C2 9 rows) and reads all six attack seats (`R89ReviewerC1`, `R89ReviewerC2`,
`R89CriticClaims`, `R89SentinelScope`, `R89MutBattery`, `R89ConnectorSiblings`). Six rows are
`falsifies-wording`; each names a narrowing that resolves to `plans/round-89.md`:

| row | firing | real? | adjudication |
|---|---|---|---|
| C1 `R89ReviewerC1` | F1 unbound `LEGS_MEASURED`; F2 non-runnable counting command; F3 universal "every round-88 field"; F4 edit-surface wording | yes — the round-88 token `LEGS` is renamed `LEGS_MEASURED` and `DIV3`/`CROSSCHECK` are added, and the frozen harm command omitted the base-tool step | reconciled by Amendments 4–6 (one-line comparison `LEGS_MEASURED` vs the `SUMMARY` receipt; the literal command including the base-tool step; the universal narrowed to the enumerated measurement fields). The narrowed C1 is what I re-measured below; the claim does not verify on its un-narrowed universal. |
| C1 `R89SentinelScope` | B1–B4 control-receipt driver discipline (overwrites the receipt before grepping it; substring match; no revision pin; the harm row would accept `records=0`) | yes — read in `controls/run-controls.sh` and `expected.tsv` | reconciled by Amendment 7: the C1 predicate does not rest on the driver; the driver's own repairs are routed, and the driver's executed claim (`RECEIPT_OK` ×8, `CONTROL_RECEIPTS=PASS`) is reproduced below. |
| C2 `R89CriticClaims` | the frozen verdict phrasing reads as a parse-back of the rendered line | yes | reconciled by Amendment 1: the verdict conjoins the printed-field derivation with the leg accounting; the failure side is observable (M1–M3 print `LEG_FAIL VERDICT fields_hold=0`). |
| C2 `R89ReviewerC2` | B1 same conjunct; B3/B4 by-construction seams; B2 registry-count finding | B1/B3/B4 yes; B2 refuted | reconciled by Amendments 1–3. Amendment 3's refutation is grounded: S218's `used-by` cell differs between `f8fa55ec` and `ac0a0892` and the registry diff is two ± pairs (verified independently below). |
| C2 `R89SentinelScope` | B5 the frozen sentence names `VERDICT fields_hold=1`, a token the counter never prints on the passing path | yes | reconciled by Amendment 8, which narrows the observable to the failure side and routes the print to round 90. The narrowed property holds (M1–M4a print `fields_hold=0`). The report's pasted after-line still echoes the unprinted token — a presentation defect routed below, not an unreconciled claim. |
| C2 `R89MutBattery` | two constant-substituted detectors keep every printed field honest | yes (a named limit, not a wording falsification) | reconciled by Amendment 9 as C1 named limit 3 restated for C2. The classification is conservative (the claim as written survives it); the narrowing is honest and does not weaken the measured predicate. |

No `falsifies-number` row; the pass is not a green-washed FAIL. The lane's prefile line is reproduced exactly.

## Claims — re-measured vs evidence-verified

Every number below is from a command run by this closure against the committed tip tree
(`a72f204b`, working tree clean). Nothing is quoted from the lane's receipts unless marked
"evidence-verified".

**C1 `C1-BATTERY-R89` (operability).** Re-measured.

```
$ python3 -B corpus/evidence/round89/gate-records-r89.py --root . --repo . --work /tmp/chousa-r89-c1
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1
RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 DIV3=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3
MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS_MEASURED=15/15
LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16
GATE_RECORDS_R89=PASS                                             # exit 0
$ python3 -B corpus/evidence/round89/mutate-r89.py --root . --repo . --work /tmp/chousa-r89-c1m
MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2 EQUIVALENT_ON_TREE=0/0 TOTAL=13/13   # exit 0
$ git show master:tools/gate-records.py > /tmp/base-tool.py
$ python3 -B corpus/evidence/round89/harm-recheck.py --root . --repo . --base-tool /tmp/base-tool.py
HARM_RECHECK files=14 records=31 moved=0 base_rc=0 r88_rc=0        # exit 0
```

The four round-88 survivors die on named lines, reproduced: `E7c-width-detached` →
`UNRECONCILED D1_WIDTH detail=3/3/1 pin3 receipt_ok=True rederived=False`; `E7b-mutant-detached` →
`UNRECONCILED MUT_ADMIT detail=derived=0 killed=0 receipt_ok=True rederived=False`; `E7d-width-detail-forged` and
`E7f-summary-field-forged` → `UNCROSSCHECKED … DIV3=1` / `D1_EXPECTED=4`. All four `KILLED`, exit 1 in the mutant
tree. **Before**, re-measured: `gate-records-r88.py` on the same tree prints `GATE_RECORDS_R88=PASS`,
`LEGS=15/15`, `LEG_REREAD=15/15`, no `CROSSCHECK` (grep for `CROSSCHECK|rederive` in the r88 battery → 0 matches);
the wave's committed receipts `w1/R89CriticClaims/r88-E7{b,c,d,f}.txt` each print `GATE_RECORDS_R88=PASS` while
carrying the detached/forged detail. C1 verifies **as stated on Amendments 4–5** (the universal narrowed to the
enumerated fields; the counting command replaced by the runnable form). Verdict: verified, narrowed.

Field delta, prior→landing (my own parse of the two receipts): renamed `LEGS`→`LEGS_MEASURED`,
`GATE_RECORDS_R88`→`GATE_RECORDS_R89`; added `DIV3=3`, `CROSSCHECK=15/15`; the three totals rose by one leg
(`LEG_REREAD`/`RECONCILED` 15/15→16/16, `LEGS_APPENDED` 15→16) because `SUMMARY` is now a leg; every enumerated
measurement field is byte-identical. That is exactly the Amendment 5 narrowing, and it is why the un-narrowed
"every round-88 field" is false in the letter.

**C2 `C2-CURATION-R89` (calibration).** Re-measured.

```
$ python3 -B corpus/evidence/round89/curation-r89.py --root .
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7
WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0
SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=8/8
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
CURATION_R89=PASS                                                 # exit 0
$ python3 -B corpus/evidence/round89/curation-r89-controls.py --root . --work /tmp/chousa-r89-c2c
CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7       # exit 0
$ python3 -B corpus/evidence/round89/curation-r89-mutants.py --root . --work /tmp/chousa-r89-c2m
MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1          # exit 0
```

The verdict's field derivation is observable on the failure side, reproduced: `M1-dead-teaches` →
`LEG_FAIL VERDICT fields_hold=0`; `M2-detached-leg`/`M3-verdict-legs` → `LEG_FAIL VERDICT fields_hold=0
legs_ok=8/8`; `M4a-dup-leg-forced` killed; `M5-lowercase-clause` killed through the battery's SUP mirror
(`BATTERY_DETECTED=1`). **Before**, re-measured: `curation-r88.py` on the same tree prints `CURATION_R88=PASS`,
`LEGS=7/7`, and contains no `DUPQID`/`fields_hold`/`VERDICT` token (grep → 0); the controls reproduce
`PRIOR_ACCEPTED_FORGERY=7/7`. C2 verifies **as stated on Amendments 1 and 8** (verdict from the printed tallies
plus leg accounting; the `VERDICT fields_hold=1` parenthetical narrowed to the failure-side observable). The
`SUP_CLAUSE_CHECKED=0` vacuity is disclosed and its mirror mutant carries the non-vacuity witness. Verdict:
verified, narrowed.

**Control-receipt driver (round-88 routed defect 5).** Re-measured in a throwaway copy of the tip
(`git archive a72f204b | tar -x -C /tmp/lane-r89`, so the lane tree is not rewritten):
`bash corpus/evidence/round89/controls/run-controls.sh <lane> /tmp/lane-r89-ctl` → `RECEIPT_OK` ×8,
`CONTROL_RECEIPTS=PASS`, exit 0. All ten committed receipts under `controls/receipts/` are byte-identical to a
fresh run (`diff` → SAME for each). The freeze revision's `c1-harm` receipt reads `records=29` (13 files); the tip
receipt reads `records=31` (14 files) because the two `GATE-RECORD` lines this round appends are themselves
records — both receipts are in history, `moved=0` at both, so SCORECARD's `over records=29` is a freeze-revision
value, not a contradiction.

**Gate evidence (Gate standard, closure consequence).** Evidence-verified and re-run:
`bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)`, exit 0;
`python3 -B tools/lane-preflight.py` → `PREFLIGHT=8/8 FAILED=none ENV=none SKIPPED=none`, exit 0. `tools/gate-records.py`
is byte-identical at base and tip (`git diff f8fa55ec a72f204b -- tools/gate-records.py` → empty), so the round's
harm claim cannot hide a subject-tool edit.

**Harm / no-axis-moved.** Re-measured: `git diff f8fa55ec a72f204b -- corpus/knowledge/` → empty;
`ls-tree` knowledge `.md` count 97 at `f8fa55ec`, `ac0a0892`, `a72f204b`; `corpus/SOURCES.md` rows 218 at all
three; `git diff --stat f8fa55ec ac0a0892 -- corpus/SOURCES.md` → `1 file changed, 2 insertions(+), 2 deletions(-)`,
both in the last (`used-by`) cell (S216, S218), no other cell moved; `PROVINCE.md`, `SKILL.md`, `SHONEN.md`,
`AGENTS.md`, `corpus/README.md` unchanged; `tools/gate-records.py` unchanged; `HARM_RECHECK … moved=0`.

**Source census.** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin chousa` → exit 0, `chousa ok …/corpus/SOURCES.md`, same five pre-existing `W04`
duplicate-URL warnings (S051, S053, S073, S074, S075), rows 218. Matches both committed census files.

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** | C1 re-measured green with per-format reconciliation (`LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15`), 11/11 + 2/2 mutants killed, four named round-88 survivors dead, `moved=0` over 31 records. The subject tool is unchanged, so no domain record could move. |
| calibration | **improved** | C2 re-measured green with field-derived verdict, duplicate-qid guard (`DUP_QIDS=0`), raw-cell superseder clause (`SUP_CLAUSE_CHECKED=0` disclosed, mirror mutant kills it), 7/7 forgeries refused by r89 and accepted by the preceding counter, 6/6 mutants killed. |
| depth | unchanged | `corpus/knowledge/*.md` 97 → 97; no entry added or deepened. |
| coverage | unchanged | registry 218 → 218 rows; two `used-by` cells extended; `PROVINCE.md` untouched; no frontier row advanced (disclosed as such). |
| freshness | unchanged | no fetch this round; refetch ledger's newest row is `2026-11-08T06:50:40Z` (round 87's S216 fetch), before the 08:31Z launch; no capture newer than the freeze. Registry/criterion freshness repair not attempted (the stale 275-case tally is routed below). |
| adjacency | unchanged | `R89ConnectorSiblings` reports zero sibling ownership overlap for both instruments; nothing absorbed; the superseder settlement note stays with kotodama. |

## Discernment spot-check (LEARNING.md, from outside)

The round's `## Gate` records two admits (both re-opened rows) and no new registry rejection; the reject half of the
sample is therefore the live S217 rejection plus the round's gate-level refusals (the seven tree forgeries). Every
source below was re-opened and re-read by this closure.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S216 RFC 9110 §15.3.4 | admit (tier A) | `corpus/captures/b1b13a12aee75c6ecc20fb91.txt`, sha256 `ec14fa34…` (matches the row and the refetch row), anchor at line 12261 | agree | the 22-word quote is present after whitespace normalisation; the sentence defines 203 as a successful response whose content a transforming proxy modified from the origin's 200 — it grounds the row's scope and the two-203-class binding. |
| S218 own-work rule 2 + QUALITY 178 | admit (tier A) | `git show ac0a0892:corpus/QUALITY.md` line 1120; `CORPUS.md` rule 2 | agree | the 11-word quote is verbatim at the freeze revision; rule 2 does restrict in-place changes to `status`/`recheck`/`used-by`, which is the rule the clause enforces. |
| S217 DCMI Namespace Policy | reject | `corpus/captures/52db06f9e0e2eaf35bbdb321.txt` (9 lines, 88 bytes) | agree | the capture is the URL alone with no policy prose, so no quotable sentence grounds the row; the flip condition names a concrete re-open trigger. |
| seven C2 tree forgeries | reject | my re-run of `curation-r89-controls.py` and `curation-r89-mutants.py` | agree | `FORGERY_REFUSED=7/7` with `PRIOR_ACCEPTED_FORGERY=7/7` on the same tree, each refusal naming a leg; the detection is not vacuous. |
| S214 (newest written spec row) | admit | `corpus/captures/a640b15abf781e5c583d7088.txt` | agree | the 17-word checklist quote is present (≤25 words) and grounds the row's search-transparency scope. |
| S215 (newest written spec row) | admit | `corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt` | agree | the 12-word PROV-O quote is present (≤25 words); the teaches sentence's `wasDerivedFrom`/time properties are in the capture. |

No disagreement. The round wrote no new registry row (disclosed), so no row's `## Gate` quote needed a freshness
re-check; the two re-opened rows and the two most recently written rows are the sample above.

## Trend verdicts (for MANIFEST)

- **expansion: unchanged** — 97 knowledge entries at base and tip, 218 registry rows at base and tip; no row added,
  none re-anchored; the two `used-by` extensions are provenance bookkeeping. Counts re-measured with
  `git ls-tree … | grep -c '\.md$'` and the census row grep.
- **quality: improved** — seven routed repairs across two instruments, each with a red-before witness reproduced
  here (E7b/E7c/E7d/E7f, M1–M5, the 7/7 forgery battery); six criteria landed (QUALITY 190–195, each citing its
  mistake); the batch receipts reproduce byte-identically from a fresh run. Nothing admitted was found false and
  left unmarked: the two dead/forged observables the wave found (`LEGS_MEASURED` unbound, `VERDICT` unprinted) are
  marked in Amendments 4 and 8 and routed, and the claim text was narrowed rather than reset.
- **discernment: improved** — the wave fired sentence-level wording six times and the lane narrowed each in the
  plan before filing (`PREFILE-FALSIFICATION … findings=0`); one reviewer finding was refuted against committed
  bytes and I independently confirmed the refutation; four of the round's own mutant-design errors are mined with
  fixes shown able to fail; the outside spot-check agrees on every sampled admit and reject above.

## Routed defects (lane must fix next round)

1. **C2's after-line quotes an unprinted token.** The report's Before → after C2 block and `LOG.md`'s after line
   both print `VERDICT fields_hold=1`, which `curation-r89.py` never prints on the passing path (the lane's own
   Amendment 8 and the wave-firing bullet say so). Fix: append a `LOG.md` correction entry naming the superseded
   text (LOG is append-only), and land Amendment 8's routed repair — print `VERDICT fields_hold=1` in the summary
   or move the leg before it — so the observable the frozen sentence names exists on both paths. Quote only
   printed tokens in the next report.
2. **Attack-share arithmetic.** The report and the `w1` commit message say `7/12 = 58%`; the committed ledger has
   six attack seats (`R89ReviewerC1`, `R89ReviewerC2`, `R89CriticClaims`, `R89SentinelScope`, `R89MutBattery`,
   `R89ConnectorSiblings`) and the lesson says `6/12`. Fix the figure (the ≥25 % floor holds at 6/12 = 50 %);
   the ledger is the checkable value.
3. **Work-performed frontier bullet undercounts its own round.** It says "four mistakes mined … four criteria
   (QUALITY 190–193)" while `## Mistakes` has seven rows and QUALITY landed 190–195 — as the same report's Landed
   changes row states. Fix the count/range.
4. **Amendment 8's finding prints the wrong summary value.** It says the summary prints `LEGS_MEASURED=8/9`; the
   counter prints `8/8` (the ninth, `VERDICT`, is appended after the summary is built). Correct the number where
   the amendment is cited.
5. **Registry freshness.** `SKILL.md`'s `research-gate` rows still carry `PASS (275 cases, 0 skipped)` although the
   tool has printed 283 cases since round 82 (cases 276–283, `bash-pin-override-*`); this round's 283-case tally is
   truthful and the registry is stale. Bump the registry tallies and case ranges at the registry home.
6. **Carried debt, re-flagged.** (a) the round-74 source-blind order oracle; (b) QUALITY 173's
   successful-refused record form; (c) the r80 backlog Gate ids; (d) Amendment 7's control-driver discipline
   (driver overwrites its receipt before grepping it; `grep -qF` substring matching; no revision pin; the harm row
   would accept `records=0`); (e) Amendment 9's detector-substitution witness for C2 and C1 named limit 3.
   Round 90 must land or re-flag each; a claim is never rescued by a post-scoring repair.
7. **Named limits stay named.** The joint leg+receipt+DIV3 rewrite survives C1 (named limit 1) and the
   quote-content swap / ≥7-token substitution survive C2 (named limits 1–2). If round 90 does not add witnesses,
   the successor claim must keep the limits in its frozen text rather than let them read as closed.

## Conformance defects (status-neutral)

1. Report C2 after-line and `LOG.md` after-line quote `VERDICT fields_hold=1` — not output of the printed command
   (evidence-presentation defect; the claim itself verifies on Amendment 8's narrowing).
2. Attack share stated as 7/12 in the report and `w1` commit message vs 6 attack seats in the ledger and 6/12 in
   the lesson.
3. Work-performed frontier bullet: "four mistakes … four criteria (QUALITY 190–193)" vs seven mistakes and
   QUALITY 190–195.
4. Plan Amendment 8's `LEGS_MEASURED=8/9` vs the printed `8/8`.
5. `SKILL.md` registry `research-gate` rows at 275 cases vs the tool's 283 since round 82 (stale expected value;
   Gate standard registry freshness).

None of the five bars admission; each is a downstream repair. A sixth item is disclosure, not defect: the wave's
`w1-results.json` `output` fields are `null` because the orchestrator kernel restarted mid-wave; every seat's report
and receipts are committed under `w1/`, so the adversarial record is the files, and the report says so rather than
hiding it.

## Promotion note (operator-owned)

All four `SHONEN.md` boxes look checkable by a non-author from the pointers the report names: box 1's SKILL registry
and decision tables resolve; box 3's commands re-ran green here (`RESEARCH_GATE_SELFTEST: PASS (283 cases)`, exit 0;
`PREFLIGHT=8/8`, exit 0); box 4's connector scan reports zero sibling overlap and `PROVINCE.md` is untouched; box 2's
LOG evidence is named. This closure writes no mark: promotion is operator-owned, `[x]` requires the named non-author
verifier the operator designates, and none is written here.
