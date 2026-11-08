# Round 88 — non-author verifier spot-check (hyaku closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane `chousa`, lane-round `88`. Base `f484d94fedec3685a3a052a65bc57cd3eb46b7d7`, lane HEAD
`bb21673b97eaa71a2bb8cd648240e094fbd14119`. This file is the non-author verification of record;
the lane's own verdicts live in `corpus/lessons/round-88.md` and the report at
`.ufo/reports/round-88/chousa.md`. I ran no sibling gate; lane-owned gate receipts are
evidence-verified below (self-test / frozen-run verdicts re-checked against committed bytes),
and the two counters were re-run directly against the committed tip tree.

## Step-1 conformance

1. Report committed in the fleet repo by the lane identity:
   `git log --format='%an %H' -- .ufo/reports/round-88/chousa.md` in
   `/home/vgpnk/Projects/shokunin` → `chousa-shokunin 99c0fca1ceaafbe5c49c934e856706176b4bee18`
   (`round-88: chousa report`). Pass.
2. `SHONEN` heading present in the report with one line per box (`[~]` × 4, each with a
   resolvable evidence pointer). The report carries Work performed, Landed changes,
   Before → after, Sources & frontier, Trend verdicts, SHONEN, and Process notes — a real
   report, not a marker. Pass.
3. Every cited lane commit exists and is an ancestor of the lane branch ref `master`:
   `f484d94f`, `bb21673b`, `4ea9d008`, `f7cedcad`, `f84286d5` — all
   `git merge-base --is-ancestor <hash> master` → YES (tested against the branch ref, never
   `@{u}`, per the jj-colocation rule). Pass.
4. Lane repo pushed, no uncommitted round work:
   `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/chousa-shokunin`
   shows `ahead=0 behind=0` with `local=remote=bb21673b…`; `git status --porcelain` in the
   lane repo is empty. Pass.
5. Prompt template contract: `.ufo/prompts/chousa-round-88.md` carries the mission/axes
   binding (SSOT), 1–3 falsifiable claims, the frontier step (SOURCES.md curation, census,
   mined mistake, sourced claim), the L2 floor (≥8 in one batched swarm with role split),
   the report contract (Landed changes, SHONEN, marker rule), the commit-then-push scope,
   and the L0 side channel, plus the hyaku addendum (§6, lines 141 onward). Pass.

Marker check: the report names real committed work with resolvable hashes and a complete
contract — not a marker. Status `ok`.

Dispatch/complete digest (copied from the closure brief; `.ufo/watchdog.log` is mutable):
`2026-11-08T04:30:51-03:00 launch chousa round=88 pgid=3397389 driver=hyaku-inline attempt=1`;
`2026-11-08T05:26:58-03:00 complete chousa round=88; hyaku-inline attempt=1`.

## Prefile falsification (addendum §8, Amendment 59)

`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane chousa --round 88`
→ `PREFILE-FALSIFICATION: SETUP findings=1` with `FINDING claims-missing
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-88/claims.json`, exit 2.
The lane's own falsification ledger is `.ufo/waves/round-88/claim-falsification.tsv` (17 rows,
every attack seat; head verified: `R88ExecRepro C1 held`, `R88ReviewerC1 C1 fired`,
`R88CriticClaims C1/C2 fired`, etc., each `falsifies-wording` row naming an Amendment-1 route
to round 89). The checker looks for a `claims.json` beside the ledger; the round filed
`corpus/evidence/round88/claims.md` as the frozen predicate set instead, and the report's
conformance note 1 discloses that no `claims.json` exists for round 88 (wording carried from
round 87; plan amendments 1–2 correct the freeze sentences). I adjudicate: the SETUP finding is
a real conformance defect (the round's own ledger script was not run against the lane's file
layout), but it does not leave any claim unverified — I read every attack-role seat's artifact
myself and reconcile each firing below. No ledger row is spurious; each `fired` row names its
narrowing/route. No unreconciled firing stands against a verified claim (see per-claim
verdicts).

## Claims — re-measured vs evidence-verified

Both claims rest on lane-owned gates. I re-ran each counter myself against the committed tip
bytes and cross-checked the frozen-run receipts; the prefile ledger (lane-owned,
`claim-falsification.tsv`) confirms per-seat firings. Verdicts are graded on the measured
property, with the wave's firings treated as routed repairs, not as rejections: the round's
sentence for each claim is met on the landing tree, and the wave's `fired` rows name the
reconciliation/wording clauses the next round repairs — the report states this honestly
("verified as stated on the measured property; fired on K4 by two seats").

### C1 — operability — re-measured

Claim: the successor battery binds the 203 class to `http == "203"` in both derivations,
pins the width against a third derivation plus `ROWS_203 = 3`, and re-reads each leg's
receipt file, reconciling its detail against its value; at landing
`GATE_RECORDS_R88=PASS` with `FORGED_REFUSED=EXPECTED_CODE=362`, `LEG_REREAD=15/15
RECONCILED=15/15 LEGS_APPENDED=15`, `D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3
D2_REFUSED=3/3`, `MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1`.

Commands run by me (against the committed tip tree
`/home/vgpnk/Projects/shokunin/chousa-shokunin`):

```
python3 -B corpus/evidence/round88/curation-r88.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
# → SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
#   Q_FLOORS=… floor13 … floor7 WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1
#   TEACHES_UNRESOLVED=0 LEGS=7/7 / TEACHES_FLAGGED S024 … superseded by S031 / CURATION_R88=PASS
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round88/gate-records-r88.py \
  --root /home/vgpnk/Projects/shokunin/chousa-shokunin --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work /tmp
# → TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362
#   EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3
#   D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1
#   DERIVE_NEG=1 LEGS=15/15 / LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15 / GATE_RECORDS_R88=PASS
```

Observed: both counters print exactly the reported lines (exit 0) on the committed tree.
The pre-freeze receipts match: `after/c1-after.txt` is the `GATE_RECORDS_R88=PASS` line pair
above; `c1-k0-donothing.txt` is byte-identical (the subject tool is unchanged this round,
sha256 `905f9da2…` at both revisions) — disclosed in the report ("C1's non-vacuity is carried
by the mutants"); `c1-k0b-frozen-instrument.txt` shows the round-87 battery has no `LEG_REREAD`
field and no width pin; `c1-mutants.txt` shows `MUTANTS_KILLED=6/6 TOOL_MUTANTS_CAUGHT=2/2`
including `E1-joint-narrow` and `E4-setup-detached`; `c1-harm.txt` shows
`HARM_RECHECK files=11 records=28 moved=0` (no genuine committed record harmed).
No owned axis is harmed: `git diff f484d94… bb21673… -- SCORECARD.md` is the round-87
correction pair only (13→12 seats, five→eight criteria), and `corpus/knowledge/*.md` is
97 files at both revisions (the one entry-cell edit in
`corpus/knowledge/provenance-recording-r85.md` is the disclosed C2 repair, see below).
Claim verdict: **verified as stated** on the measured property (re-measured). The wave's
`fired` rows (`R88ReviewerC1`, `R88CriticClaims`, corroborated by `R88ExecC2Forge` and the
scribe's concur) name the per-format reconciliation gap — a detached `ok` on the three
non-`n/m` legs survives the `RECONCILED` conjunct (K4) — honestly published in the lesson's
`## Mistakes` 1 and routed to round 89 in plan amendment 1. That is a routed repair for the
reconciliation clause, not an unreconciled kill of the measured 203-binding property; C1
verifies on its measured predicate.

### C2 — calibration — re-measured

Claim: the curation counter closes the four round-87 routed defects — the warrant leg
requires every named qid to share a term, the floor pins the per-entry qid set and a
per-row token floor of 7, and a superseder disposes only when `mined`; at landing
`CURATION_R88=PASS` with `WARRANT_OK=17/17`, `QUOTES_LOCATED=20/20`, `LEGS=7/7`,
`TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0`, and the disclosed entry repair
(`provenance-recording-r85.md` row "Naming what a resource derives from" `Q1, Q3 (S215)` →
`Q1 (S215)`).

Commands run by me: the curation counter re-run above reproduces the exact frozen line
(`CURATION_R88=PASS`, exit 0, `WARRANT_OK=17/17`, `QUOTES_LOCATED=20/20`, `LEGS=7/7`).
Cross-checks against committed bytes (no sibling gate executed; control receipts read):

- `controls/receipts/c2-controls.txt`: `FORGERY_REFUSED=5/5 R87_ACCEPTED_FORGERY=5/5` —
  each forgery (A1c junk substitute, A1d truncate, caseG relabel, F2 rejected superseder,
  B1b padding qid) is refused by the round-88 counter (`LEG_FAIL FLOOR …` / `LEG_FAIL
  WARRANT 16/17` / `LEG_FAIL TEACHES … unresolved=1`) and accepted by the round-87 counter.
- `c2-d0-donothing.txt`: the round-87 counter prints `CURATION_R87=PASS` on the round-88
  tree (before-state control), while the repaired entry is load-bearing — without the
  `Q1 (S215)` repair the base tree prints `WARRANT_OK=16/17` (`WARRANT_UNLINKED … Q1, Q3
  (S215) resolved=2/2`), confirmed in the lesson's `## Gate` and the repro seat's
  `c2-on-base-tree.log`. Verified at the tip: the row reads `Q1 (S215)`.
- The `TEACHES` leg fires once on `S024` (`terms=publication,modification`, disposition
  superseded by mined `S031`) and resolves to 0 unresolved.

Claim verdict: **verified as stated** (re-measured). The wave's `fired` rows name the
duplicate-qid / verdict-vs-field / superseder-own-read gaps (`R88ExecC2Forge`,
`R88CriticClaims`, `R88ScoutRegistry` — the last notes the own-read clause is unreachable
at `curation-r88.py:250`); all are published in the lesson's `## Mistakes` 2–3 and routed
to round 89 (per-format floor, duplicate-qid guard, live superseder-own-read). No axis is
harmed by the disclosed entry repair: it is one cell in one knowledge entry, aligned with
the counter's own term-share rule, and it closes a documented round-87 routing.

### Axis verdicts (per claim)

| axis | claim | verdict | basis |
|---|---|---|---|
| operability | C1 | **improved** | 203 class now bound in both derivations + third pin; leg-receipt re-read reconciles; 362/362 forgeries refused; mutants killed; `moved=0`. |
| calibration | C2 | **improved** | every-qid warrant, qid-set + token-7 floor, mined-superseder disposal; five round-87 forgeries refused with named legs; load-bearing entry repair. |
| depth | — | **unchanged** | `corpus/knowledge/*.md` 97 → 97; no new entry; the one cell edit is a repair, not deepening. |
| coverage | — | **unchanged** | registry 218 → 218 rows; no PROVINCE move. |
| freshness | — | **unchanged** | no fetch this round; `refetch.tsv` tail still round 87's `2026-11-08T06:50:40Z`. |
| adjacency | — | **unchanged** | assimilation honestly recorded as none; no cross-domain absorption. |

## Discernment spot-check (LEARNING.md, from outside)

The lesson's `## Gate` records one GATE-RECORD (S218): the plan quotes QUALITY criterion 178's
operative clause with its location, and asks for a non-author re-open of the quote. Sample:

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `GATE-RECORD S218 rev=4ea9d008… path=corpus/QUALITY.md line=1120` — quote "A frozen `teaches` cell is not evidence; the superseding row's is." (11 words ≤ 25) | admit | `corpus/QUALITY.md:1120` at the tip: `178. **A frozen `teaches` cell is not evidence; the superseding row's is.**` | agree | The quote is verbatim at the cited line, 11 words, located corpus-body correctly; the lesson's committed `verify` receipt records `GATE_RECORD … S218 OK`, and I re-resolved the line number from the tip tree so the locator is auditable independent of that receipt. |
| No new registry row (round claims no curation this round; 218 → 218) | reject (no new row opened) | `corpus/SOURCES.md` census: `grep -cE '^\|[[:space:]]*S[0-9]{3,}…'` → 218; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0 with the same five pre-existing W04 warnings | agree | No row was opened, re-anchored, or touched; the "no new row" decision is correct and consistent with the absence of any fetch. |
| The disclosed `Q1, Q3 (S215)` → `Q1 (S215)` cell repair as a knowledge-entry correction, not a registry-row edit | admit (repair) | `corpus/knowledge/provenance-recording-r85.md:34` reads `Q1 (S215)`; `git diff f484d94… bb21673… -- corpus/knowledge/` is that single cell; `git diff … -- corpus/SOURCES.md` is empty | agree | The repair is disclosed in `plans/round-88.md` §Pre-freeze repairs 6, keeps the registry append-only (no `SOURCES.md` cell touched), and is load-bearing for C2. |
| Admit the HARM control (`moved=0`) and the five-forgery refusal as genuine safety evidence | admit | `controls/receipts/c1-harm.txt` (`HARM_RECHECK files=11 records=28 moved=0`); `controls/receipts/c2-controls.txt` (`FORGERY_REFUSED=5/5`) | agree | Both controls name the rounded-out population and the moved/refused counts are consistent with the counters I re-ran. |

Trend verdicts (mine, checked against the lesson's table):

- **expansion: unchanged** — corroborated: 97 knowledge files at both revisions (my `ls | wc -l`
  → 97), registry 218 rows (my census count), no `SOURCES.md` diff. The lane's "unchanged"
  agrees with my count.
- **quality: improved** — corroborated: two instruments carry four routed repairs each with
  failable witnesses (203 binding, leg-receipt reconciliation, every-qid warrant, qid-set +
  token-7 floor, mined-superseder disposal) and the committed receipts show red-before states
  (`CURATION_R88=FAIL` on the unrepaired tree; round-87 counter `CURATION_R87=PASS` over the
  forged tree).
- **discernment: improved** — corroborated: 6 of 17 ledger rows are `fired`/`fired (concur)`
  (the wave fired both claims on their own reconciliation/wording clauses), the lane
  published the firings plus the dead clause and the control-receipt defects in its own
  lesson rather than arguing them away, and each firing names a round-89 route. The report's
  discernment verdict matches the ledger.

Spot-check agreement: 4/4 (one admit of a quoted gate record, one reject of the no-new-row
decision, one admit of the disclosed entry repair, one admit of the harm/forgery controls).

## Trend verdicts table for MANIFEST

`expansion: unchanged`, `quality: improved`, `discernment: improved`.
`verdicts`: `operability: improved`, `calibration: improved`, `depth: unchanged`,
`coverage: unchanged`, `freshness: unchanged`, `adjacency: unchanged`.
`admitted: true`, verdict `admitted`.

## Routed defects (lane must fix next round)

1. **Prefile ledger file layout (this closure).** The prefile checker expects
   `.ufo/waves/round-88/claims.json` beside the ledger; the round filed
   `corpus/evidence/round88/claims.md` and disclosed the missing `claims.json` in the report.
   Next round, emit the claims file in the layout the checker reads (or pin the checker's
   expected path in the plan) so the `PREFILE-FALSIFICATION:` line can run clean instead of
   `SETUP findings=1`.
2. **Per-format reconciliation (C1).** The `RECONCILED` conjunct searched only a `n/m` shape,
   so a detached `ok` on `MUT_ADMIT`/`MUT_UNREACH` and the width legs survived with `PASS`
   (ledger rows `R88ReviewerC1`, `R88CriticClaims`; receipts `e4-m2-mutadmit-detached.txt`,
   `e7c-width-detached.log`). Routed: per-format reconciliation (plan amendment 1).
3. **Verdict-vs-field reconciliation (C2).** `curation-r88.py`'s verdict is `all(ok)` over
   the legs, never reconciled with its printed fields, so a dead detector prints
   `TEACHES_FLAGGED=0 … PASS` (ledger rows `R88CriticClaims`, `R88ExecC2Forge`; receipts
   `c2-dead-teaches.log`, `c2-detached-teaches.log`). Routed: derive `passed` from the
   printed fields (plan amendment 1).
4. **Dead superseder-own-read clause (C2).** `curation-r88.py:250` matches a case-sensitive
   pattern against a lowercased cell (0 lowercased matches over 218 rows), so the clause the
   frozen sentence requires never fires (ledger row `R88ScoutRegistry`, receipt
   `receipt-supclause-dead.txt`). Routed: match the raw cell and add a control mirror that
   exercises it (plan amendment 1).
5. **Control-receipt discipline.** `expected.tsv` `c1-do-nothing` expects exit 1 while its
   receipt prints PASS (the subject tool is unchanged, so the case is unsatisfiable as
   written) and `c2-d0-donothing.txt` has no expectation row (ledger rows `R88SentinelScope`
   F7/F7b). Routed: every control receipt checked against its `expected.tsv` row before the
   freeze commits (plan amendment 2).
6. **Duplicate-qid / swapped-quote forgeries.** Five in-class forgeries pass the C2 counter
   green (ledger row `R88ExecC2Forge`). Routed: duplicate-qid guard + per-format floor
   (plan amendment 1).
7. **Seat discipline.** `R88ExecForge.md` shipped no `VERDICT:` line (content reads C1 held;
   tallied so by the scribe). Not a claim defect; noted as a finding. Fix: require the
   trailer before WAVE-DONE.
8. **Operator-owned prompt corruption.** `.ufo/prompts/chousa-round-88.md:143` (the addendum's
   run-15 quote, not lane-authored) cuts mid-word (`…these models and conc` / `…re each`).
   Substance unchanged; routed to the operator, not the lane. The lane's description now cites
   the real bytes (lesson `## Corrections` 3).

## Conformance defects (status-neutral)

All of the following are conformance defects: they stay in notes and do not bar admission.
- The prefile SETUP finding (defect 1) is a conformance defect in the round's filing layout.
- Report conformance note 1 (no `claims.json` / no egress table for round 88; egress waived
  because the window was loopback-only per `SKILL.md`) — disclosed, status-neutral.
- Report conformance note 2 (the unsatisfiable `c1-do-nothing` expectation above) — routed as
  defect 5, status-neutral.
- Report conformance note 3 (the prompt's corrupted run-15 quote) — operator-owned,
  status-neutral.
- The SCORECARD round-87 header's 13→12 and five→eight corrections were disclosed as
  append-only corrections in the lane's own lesson `## Corrections` and propagated to
  `SCORECARD.md` in the integration commit (`git diff f484d94… bb21673… -- SCORECARD.md`
  shows exactly those two sentences). The frozen `ccsp.cadvise` class is untouched by this
  closure; the promotion-read flag in `EVEN_ROWS` is not a lane-file defect of this round.

## Promotion note

The report's SHONEN boxes are all `[~]` (lane-asserted, no named non-author verifier). The
four boxes read fully checkable by a non-author from artifacts alone (a SKILL decision table,
a logged end-to-end task, runnable-selftest commands, and a provenance-accurate PROVINCE.md);
promotion is operator-owned, so I name the checkability here only, per the closure brief.

— hyaku closure (non-author integrator, @m_zfl), 2026-11-08.
