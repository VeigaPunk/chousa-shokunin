# Round 88 — the 203 class is bound to 203 and the curation counter closes its four routed defects; the wave fires both claims on their own reconciliation clauses (2026-11-08)

Base `f484d94f` (round-87 landing + its non-author spot-check). Frozen claims in `corpus/evidence/round88/claims.md`;
plan and pre-freeze repairs in `plans/round-88.md`. Round 87's non-author check routed four defects
(`round-87-verifier-spotcheck.md` `## Routed defects` 1–4); this round closes 1–4 and discharges the plan's flagged
freeze omissions as amendments 1 and 2 below. One v1 wave, 12 seats (4 executor, 1 reviewer, 1 critic,
1 mutation-tester, 1 sentinel, 1 scout, 1 connector, 1 scribe; attack share 6/12 = 50%: reviewer, critic,
mutation-tester, the two forge seats and the sentinel).

## Gate

No fetch this round; no registry row opened, re-anchored or re-opened. `git diff f484d94f 4ea9d008 -- corpus/SOURCES.md
corpus/captures/` is empty, the registry is 218 rows at both revisions, and `awk -F'\t' 'NR>1{print $5}'
corpus/evidence/round57/refetch.tsv | sort | tail -1` prints `2026-11-08T06:50:40Z` (round 87's fetch), so no
`url=` record is owed (QUALITY 173).

GATE-RECORD S218 rev=4ea9d008abfd2e09cb51649a42678a78f52ac530 path=corpus/QUALITY.md line=1120 words=11 quote=A frozen `teaches` cell is not evidence; the superseding row's is.

- **S218** (`own-work`, round 87): the round-87 non-author check routed this exact line — "Quote criterion 178's
  operative clause (≤25 words) in this round's lesson before any new row is admitted" (`round-87-verifier-spotcheck.md`
  `## Routed defects` 3). The quote is criterion 178's operative clause `corpus/QUALITY.md:1120` at `4ea9d008`
  (11 words ≤ 25). Verified by `python3 -B tools/gate-records.py verify --root . --repo <lane>
  corpus/lessons/round-88.md` → `GATE_RECORD ... S218 OK` / `GATE_RECORDS files=1 records=1 ok=1 fail=0`, rc 0;
  pinned at the freeze so the line number cannot move under the integration commit.
- **The provenance repair** (`corpus/knowledge/provenance-recording-r85.md` row "Naming what a resource derives
  from" `Q1, Q3 (S215)` → `Q1 (S215)`) is disclosed in `plans/round-88.md` §Pre-freeze repairs 6: `Q3`'s quote
  ("then we can say that the bar chart prov:wasDerivedFrom the dataset." — `R88ReviewerC2` §a7) shares zero terms
  with the row's cells under the counter's own rule, so the every-qid leg fails the base tree (`WARRANT_OK=16/17`,
  `WARRANT_UNLINKED … warrant=Q1, Q3 (S215) resolved=2/2`) until the repair lands. The counter on the base tree
  prints `CURATION_R88=FAIL`, and the wave's repro seat confirms the load-bearingness
  (`.ufo/waves/round-88/w1/R88CriticClaims/receipts/c2-on-base-tree.log`).

Registry changes, old→new (CORPUS rule 2): none. One entry cell edited, disclosed in `plans/round-88.md`.
Census exit 0 at start and end (same five pre-existing `W04` warnings);
`corpus/evidence/round88/census-start.txt` (`# computed_against=f484d94f...`) and
`corpus/evidence/round88/census-end.txt` (written at the integration tip, `# computed_against=<tip>`).

No egress table was required: `SKILL.md` `## Boundaries` says "A window without an approval table is
loopback-only", and this window was loopback-only (the sentinel's F1 receipt: zero refetch rows with
`fetched >= 2026-11-08T07:00:00Z`, zero captures newer than the freeze commit).

## Claim outcomes

Both claims are scored on the freeze bytes and then attacked by the round's wave. At the freeze `4ea9d008`:

- **C1 operability** — `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362
  EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3
  MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15` /
  `LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15` / `GATE_RECORDS_R88=PASS`, exit 0
  (`corpus/evidence/round88/after/c1-after.txt`). Before: the same battery pointed at the same
  tool also passes byte-identically (the tool is unchanged this round, sha256 `905f9da2…` at both revisions;
  `controls/receipts/c1-k0-donothing.txt`, the sentinel's F7), so C1's non-vacuity is carried by the mutant
  battery — `mutate-r88.py` prints `MUTANTS_KILLED=6/6 TOOL_MUTANTS_CAUGHT=2/2` (`c1-mutants.txt`), including
  `E1-joint-narrow` and `E4-setup-detached` — and by `c1-k0b-frozen-instrument.txt` (the round-87 counter line has
  no `LEG_REREAD` field and no width pin).
- **C2 calibration** — `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
  Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17
  TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7` / `CURATION_R88=PASS`, exit 0
  (`c2-after-freeze.txt`). Before: the frozen round-87 counter accepts all five routed forgeries
  (`FORGERY_REFUSED=5/5 R87_ACCEPTED_FORGERY=5/5`, `c2-controls.txt`) and prints `CURATION_R87=PASS` on the
  round-88 tree (`c2-d0-donothing.txt`) — it has no leg of the four new classes.

## What the instruments measure, and what they do not

C1's verdict re-reads each leg's own receipt file and reconciles the re-read value against the leg's detail string;
the two width derivations plus a third (`registry_rows_203`) must agree with `ROWS_203 = 3`. Named limits, unfixed
at the measured width: a counter edit that jointly rewrites the leg writer, the receipts and the reconciliation
survives (the `R88MutCounter` NAMED-LIMIT mutant), and the wave showed two wider survivals — a detached `ok` on any
leg whose detail carries no `n/m` ratio, and (for the width legs) any detachment, since the reconciliation reads
only the first `n/m` pair of `len/d1/div3 pinN`. Amendment 1 routes both to round 89.

C2's floor requires the pinned qid set and `MIN_TOKENS = 7` (the measured minimum over the 20 located quotes;
r84 `Q13` is exactly 7 words), the warrant leg requires every named qid to share a term, and the `TEACHES` leg
requires a `mined` superseder. Named limits: the warrant share is one incidental word; the counter has no
verdict-vs-field reconciliation and no duplicate-qid check; and the superseder-own-read clause is unreachable
(amendment 2 names the bug at `curation-r88.py:250`).

## Mistakes

1. **Class: a reconciliation that re-derives a leg's verdict only for one detail format.** `RECONCILED` searched
   `detail=(\d+)/(\d+)`, so three legs detached freely and the width legs detached behind the first `n/m` pair.
   **Evidence pointer:** `R88ReviewerC1.md` §(b) receipts `e4-m2-mutadmit-detached.txt`,
   `e4-m3-mutadmit-neverbuilt.txt`; `R88CriticClaims.md` `e7c-width-detached.log`, `e7b-mutant-detached.log`,
   `combined-width-mutant-detached.log`. **Captured-by:** the wave's reviewer and critic seats; QUALITY 187 (state
   whether the count guards appends or executions) covered the class but not the per-format requirement. **Fix:** a
   per-format reconciliation — `derived=x killed=y` legs require `derived == killed == 1`, width legs require
   `len == d1 == div3 == pin`, `TOOL` requires the file present — shown able to fail by the two detached-ok
   witnesses in `controls/receipts/c1-mutants.txt` (KILLED E4/E7 forms).
2. **Class: a claim clause that is dead code in the instrument that carries it.** C2's sentence required a
   superseding row's own `teaches` to read in its own capture, but `curation-r88.py:250` matches
   `supersedes (S\d{3,}) —` against a lowercased cell, which never matches (10 raw-cell matches, 0 lowercased over
   218 rows). **Evidence pointer:** `R88ScoutRegistry.md` finding 1 (`receipt-supclause-dead.txt`,
   `receipt-probe-run.txt`).
   **Captured-by:** none — no criterion required that every clause of a frozen claim be exercised by one run.
   **Fix:** match against the raw cell (the regex is case-sensitive), and add a control mirror that exercises it
   (S031 gains a contrast+term absent from its capture behind a mined superseder); shown able to fail by the
   scout's fixed-counter receipt.
3. **Class: a counter that prints PASS over its own honestly-printed failures.** `curation-r88.py`'s verdict is
   `all(ok)`, never reconciled against the printed fields, so a dead detector prints `TEACHES_FLAGGED=0 … PASS`.
   **Evidence pointer:** `R88CriticClaims.md` `c2-dead-teaches.log`, `c2-detached-teaches.log`,
   `c2-constants-on-broken.log`. **Captured-by:** the wave's critic seat; the same class C1's K4 names, but C2's
   kill rules did not name a detached-`ok` leg. **Fix:** derive `passed` from the printed fields (see amendment 1).
4. **Class: a freeze receipt filed under a failing expectation, with no gate between them.** `c1-k0-donothing.txt`
   is byte-identical to the landing run (the tool is unchanged, so the "do-nothing" case is the landing case) while
   `expected.tsv` expects exit 1; `c2-d0-donothing.txt` has no expectation row at all. **Evidence pointer:**
   `R88SentinelScope.md` F7/F7b. **Captured-by:** the wave's sentinel seat; QUALITY 172 (a criterion's cited
   receipt must exist) covers existence, not agreement. **Fix:** every control receipt is checked against its
   `expected.tsv` row before the freeze commits (amendment 2).
5. **Class: a plan that asserts freeze contents the freeze does not carry.** `plans/round-88.md` named `claims.json`
   and "the egress table"; neither exists. **Evidence pointer:** `R88SentinelScope.md` F4. **Captured-by:** the
   wave's sentinel seat. **Fix:** the plan's freeze paragraph is amended to name only the files the freeze carries;
   the next round's plan is checked against `git ls-tree` before the freeze commits.

Seat-trailer discipline: `R88ExecForge.md` shipped no `VERDICT:` line (28 probes, zero accepted forgeries — C1
held on content). The wave context requires the trailer; the scribe's tally counted the seat as held and named the
missing trailer as a finding (`.ufo/waves/round-88/w1/R88ScribeLesson/lesson-settlement-draft.md` pre-condition 7).

## Corrections

1. **`SCORECARD.md` round-87 header seat count corrected (13 → 12).** `w1-spec.json` items = 12,
   `w1-dispatch.json` `counts.spawn=12`, `w1-results.json` results = 12; the round-87 report and lesson both say 12.
   The header's "13" was a lane-authored heading error, fixed here per round-87 spot-check routed defect 1.
2. **The mined-criteria count corrected (five → eight, QUALITY 182–189).** `grep -cE '^18[2-9]\. '
   corpus/QUALITY.md` → 8; the base carried 180–181. The lesson's `## Trends` row and the SCORECARD's calibration row
   both said "five criteria mined (QUALITY 182–186)", which was true at `e6e920a4`; criteria 187–189 landed in the
   integration commit and the two sentences were not corrected with them. The round-87 lesson carries the append-only
   `## Corrections` row; the SCORECARD sentences are corrected in the integration commit. The attribution is
   182–184 pre-freeze probes, 185–186 round-86 routed defects, 187–189 wave findings (three / two / three) — for
   round-87 spot-check routed defect 2.
3. **The dispatched prompt's corrupted run-15 quote corrected.** The round-87 report's conformance note 1 quoted the
   fragment as ending "`…shokunin style bu…`"; the real bytes are `…on the hyaku style but using these models and
   conc` / `…re each` (cut mid-word at `conc`/`re each`), line 143 of `.ufo/prompts/chousa-round-87.md`. The
   substance stands (the operator-owned template carries a corrupted quote); the description now cites the real
   fragment. — round-87 spot-check routed defect 4.
4. **The census receipt pair's revision names corrected.** `census-end.txt` is written by the L1 at the integration
   tip and carries `# computed_against=<integration tip>`, not the freeze; both receipts are committed together so
   the pair is auditable, and the start receipt is derived from the `f484d94f` archive rather than captured before
   it (QUALITY 189's derived-not-captured labelling). The round-87 miscount "five criteria mined" in the lesson's
   Trends row is the same class: receipt written before its companion landed, asserted by name.

## Spot-check intake

Round 87's non-author check (`corpus/lessons/round-87-verifier-spotcheck.md`) routed four defects. Disposition,
one row each:

| routed item | disposition | pointer |
|---|---|---|
| 1. `SCORECARD.md` header says 13 seats | **fixed** — corrected to 12 in the integration commit | `SCORECARD.md` round-87 header; `w1-spec.json`, `w1-dispatch.json`, `w1-results.json` all 12 |
| 2. mined-criteria count stale (five vs eight) | **fixed** — append-only `## Corrections` row in the round-87 lesson plus corrected SCORECARD sentences; attribution 182–184 / 185–186 / 187–189 (three / two / three) | `corpus/lessons/round-87.md` `## Corrections` 1; `SCORECARD.md` round-87 verdict |
| 3. `S218` Gate record carries no quote | **fixed** — the ≤25-word located quote (criterion 178's operative clause, 11 words) lands in this round's `## Gate` above | `GATE-RECORD S218 rev=4ea9d008…` (this file); `tools/gate-records.py verify` exit 0 |
| 4. the template defect mis-quoted | **fixed (description)** — the real fragment (`conc`/`re each`) cited in `## Corrections` 3; the defect itself is operator-owned and carried | `corpus/lessons/round-88.md` `## Corrections` 3 |

## considerthese

No file under `considerthese/` was opened for a proposal this round: the newest entries (`2026-11-05.md`,
`2026-11-06.md`, `2026-11-07.md`) predate the latest landed round (round 87) and their still-unimplemented
proposals were already consumed or routed by rounds 85–87. The one piece of `considerthese` material this round
consumes is the daemon owner text in `considerthese/2026-11-07.md` §"A cross-tool 'duplicate wins' watch",
which names the exact failure class two counters fell into again this round (a counter whose verdict does not
reconcile with its fields). It is cited as the independent statement of the class, not as evidence: every such
class is measured by the wave's receipts above.

## Trends

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | `corpus/knowledge/*.md` 97 → 97; the registry is 218 rows at both revisions (no row added, none touched). The round's gain is in the instruments and the entry repair; nothing is counted as new ground. |
| quality | improved | two instruments carry four routed repairs; five round-87 forgeries are refused with named legs; `tools/gate-records.py` selftest and the lane preflight pass at the tip (integration commit). |
| discernment | improved | the wave fired both claims on their own reconciliation and wording clauses and the lane published the firings rather than arguing them away; the plan's focus items (per-format reconciliation, verdict-vs-field reconciliation, live superseder-own-read, K4 coverage of the mutant legs, the control-receipt discipline) are routed to round 89 in amendment 1. |
