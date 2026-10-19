# chousa — round 12 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 1). Work commit `5691bf531086dd435006cd9d6157df00933973a3`; records commit `2dfaeeb19a56385f1576991cfd1039aa4c0270c5` (HEAD when this report is filed; both lane-identity, local only, no push).

## Work performed

- Pre-registration, before-receipts, /tmp quota unblock (6.4G stale wave scratch, lsof-verified), and three provider deviations — commits `ba8ce4e`, `8684348`, `c6c0d2a`, `cb2d65a`, `931fed6`, `26b556e` (all LOG.md/SCORECARD.md only, append-only).
- Key liveness program: keys 3/4/5 dead with `402 Insufficient account funds` (64/64 seats instant-fail on 3/4; single-agent probe on 5); **opencode-go-6 alive → the wave ran there, 64/64 seat reports in 776s** (standing operator directive: stick with key 6 until it fails).
- Wave (one batched AgentSwarm call, 64 read-only seats): claim designs, gate archaeology, adversarial review (21 adversaries), 3 reviewer BLOCKs that lifted once their plan fixes were folded (observable amendments: `id=SCOPE_` count, namespaced cap ids, near-miss fixtures, calibration-as-debt-closure, re-pin-first sequencing).
- Parent integration: 11 gate edits (scope screen + cap + banner + linear count_nl + pin-fixture domain row + 13 selftest cases), the A-r9 C3 correction + full pin cascade + two append-only errata, SKILL/corpus-README/note corrections sweeps, re-pin, receipts.

## Landed changes (each tied to a LOG.md entry)

- `tools/research-gate.sh` (gate `46f5ddb3…` → `91a01695…`): scope screen; 8 MiB cap; `VERSION=v2`; `count_nl` linear; 13 cases appended (85 → 98); pin fixture domain row; header/usage docs.
- `corpus/fixtures/archives-r9/A-r9.md`: C3 `:76` → `:86` (sha → `dfd2ae1a…`); controls stay pre-fix byte-copies (desync note in `controls/README.md`).
- New: `corpus/knowledge/scope-refusal-r12.md`, `corpus/knowledge/gate-baseline-r12.md`, `corpus/evidence/gate-baseline-r12-20261019T115519Z.json`, four `scope-r12-…` receipts.
- Errata: `hardening-r10.md` §6 (rows 9/10/56/70 → 71 rows 38·23·7·0·3, queue 26); `audit-r11.md` erratum; pin/known-gaps updates across `corpus/README.md`, `corpus/evidence/README.md`, `SKILL.md`, `claims-r9.README.md`, `archives-verified-r9.md`, five knowledge-note dispositions.
- `SCORECARD.md`: round-12 verdict block, capabilities (3 rows), §Saturation declaration (line 8.0, window N=3, dormant), §Planned round 13.

## Before → after measurements (counting commands in SCORECARD §Round 12 verdict)

- Scope: emitting assignments 0 → 3 (`grep -c 'id=SCOPE_'`); B-r9 canary 0 findings; cases 86–92 pass.
- Banner: `research-gate-r1` → `v2` at six sites; mutant drifts `GATE_DRIFT: GATE`; r12 baseline `GATE_DRIFT: none`.
- Cap: 8388608 reads / 8388609 refuses, `observed=refused at=-` (never partially searched); claims+chain+verify-all binding via one chokepoint.
- A-r9: 18/19 → 19/19 cite-vs-span (parent re-measured, swept all 19 claim rows); verify-all CLEAN at `dfd2ae1a…`.
- Battery: selftest 98 (1–85 byte-identical `cmp`); r1 3/3; 18-fixture battery identical (masked banner/ts); zero network.

## Cross-domain evidence

None absorbed: three SCOPE findings route bounty scope → kasegi, model-quality claims → kengaku, orchestration/dispatch → kumitate (report-never-absorb is the screen's disposition rule).

## SHONEN

- [~] SKILL.md decision tables/error patterns/checklists with cited sources — `SKILL.md` gate registry + round-12 paragraphs; pointer: SKILL.md (this commit)
- [~] End-to-end domain task executed and logged — rounds 2–12 each logged in LOG.md with receipts; pointer: LOG.md
- [~] Instructions executable without oral context — `bash tools/research-gate.sh --selftest` reproduces every claim; pointer: SCORECARD §Round 12 verdict
- [~] No cross-domain bleed — PROVINCE.md refusals now gate-enforced for declared scope; pointer: `corpus/knowledge/scope-refusal-r12.md`

No `[x]` without a named non-author verifier; the non-author spot-check remains operator-owned (L0 row re-filed this round).

## Seat roster (round 11 correction: counts without rosters were unverifiable)

Model for all 64 seats: opencode-go-6 / deepseek-v4.1-flash. One batched AgentSwarm call; 64/64 completed. Verdicts: 61 ADMIT (with conditions, folded), 3 BLOCK-as-pre-registered (conditions folded: seats 46, 49, 50). Output file: session tool-results `AgentSwarm-tool_2p6cvwSisS3EeIUsVxa3nLOd-…txt` (595 KB, 64 reports).

| seat | role | deliverable (one line) | verdict |
|---|---|---|---|
| 01 | RoundPlanner | integration sequence + acceptance commands A1–A5 | ADMIT |
| 02 | ScopeSemanticsPlanner | declaration contract + decision table + patch sketch | ADMIT |
| 03 | FleetConnector | sibling scope-gate prior art (kagi scope-gate.sh) + conditions | ADMIT |
| 04 | HistoryConnector | quoted carried-limit requirements with pointers | ADMIT |
| 05 | GateMapScout | function/line patch atlas | ADMIT |
| 06 | SeverityAnalyst | warn-drift mechanics + hook point | ADMIT |
| 07 | MetaParseAnalyst | Meta parse idiom + minimal parser path | ADMIT |
| 08 | ReadPathAnalyst | chokepoint + refusal semantics | ADMIT |
| 09 | ReceiptScout | before-battery verbatim reproduction | ADMIT |
| 10 | ByteIdentityAnalyst | byte-identity guard design + pin-fixture verdict | ADMIT |
| 11 | ArchiveCanaryScout | canary outputs for 5 fixtures | ADMIT |
| 12 | FixtureAnalyst | naming/layout for new fixtures | ADMIT |
| 13 | A50Scout | C3 re-derivation + 19-row sweep (C3-only) | ADMIT |
| 14 | ScopeImplDesigner | screen patch + 4 cases + 9 risks | ADMIT |
| 15 | ScopeFixtureDesigner | province fixture designs | ADMIT |
| 16 | ScopeTestDesigner | cases 86–96 + guard recipes | ADMIT |
| 17 | BannerImplDesigner | v2 convention + affected-surface list | ADMIT |
| 18 | SizeCapImplDesigner | cap patch + timing measurements | ADMIT |
| 19 | SizeCapFixtureDesigner | boundary-pair design + 4 cases | ADMIT |
| 20 | A50FixDesigner | correction + 3 errata text blocks | ADMIT |
| 21 | KnowledgeNoteDesigner | scope-refusal-r12.md draft | ADMIT |
| 22 | SkillRowDesigner | registry row update + sweep list | ADMIT |
| 23 | ScorecardDesigner | verdict block skeleton | ADMIT |
| 24 | LogEntryDesigner | admission entry skeleton | ADMIT |
| 25 | ReportScribe | report skeleton | ADMIT |
| 26 | Adversary (false-positives) | declaration-only trigger audit | ADMIT |
| 27 | Adversary (gaming) | 6 declaration games + fixes | ADMIT |
| 28 | Adversary (severity-exit) | warn-drift proof, all 4 paths | ADMIT |
| 29 | Adversary (composition) | verify-all interaction check | ADMIT |
| 30 | Adversary (pin-drift) | r8-baseline-survives verdict | ADMIT |
| 31 | Adversary (cross-mode) | entry-point routing audit | ADMIT |
| 32 | Adversary (selftest-churn) | churn hazards + cmp guard | ADMIT |
| 33 | Adversary (banner-usage) | 194-hit surface census | ADMIT |
| 34 | Adversary (threshold) | measured threshold attack | ADMIT |
| 35 | Adversary (toctou) | TOCTOU assessment + archive sizes | ADMIT |
| 36 | Adversary (finding-semantics) | namespaced-id recommendation | ADMIT |
| 37 | Adversary (bypass) | uncapped-read census | ADMIT |
| 38 | Adversary (interaction) | receipt-churn walk | ADMIT |
| 39 | Adversary (wrong-line-class) | gate-vs-audit detectability | ADMIT |
| 40 | Adversary (fix-shape) | :86 fix simulation | ADMIT |
| 41 | Adversary (ripple) | C3 reference census | ADMIT |
| 42 | Adversary (ledger-append) | erratum formats for both files | ADMIT |
| 43 | Adversary (repro) | at= field impact analysis | ADMIT |
| 44 | Adversary (sibling-mismatch) | independent 19-row sweep | ADMIT |
| 45 | Adversary (honesty) | calibration-must-not-overclaim case | ADMIT |
| 46 | Reviewer (claim 1) | acceptance criteria; BLOCK→ADMIT after amendments | BLOCK→folded |
| 47 | Reviewer (claim 2) | cap/banner criteria | ADMIT |
| 48 | Reviewer (claim 3) | fix criteria | ADMIT |
| 49 | Reviewer (cross-claim) | 16 hazards + kill-checks; 2 false observables named | BLOCK→folded |
| 50 | Reviewer (protocol) | conformance amendments S1–S6 | BLOCK→folded |
| 51 | Reviewer (evidence) | two-evidences receipt set | ADMIT |
| 52 | Reviewer (scope) | boundary-risk scan | ADMIT |
| 53 | Critic (round-level) | reject-steelman + kill-checks | ADMIT |
| 54 | Critic (claim 1) | Meta-row enumeration | ADMIT |
| 55 | Critic (claim 2) | minimal-edit challenge | ADMIT |
| 56 | Critic (claim 3) | debt-closure verdict case | ADMIT |
| 57 | ReceiptScribe | receipt runbook | ADMIT |
| 58 | ScorecardScribe | fill-in verdict table | ADMIT |
| 59 | LogScribe | MANIFEST entry draft | ADMIT |
| 60 | RosterScribe | this roster's format | ADMIT |
| 61 | ConformanceScribe | SHONEN lines + canonical-form check | ADMIT |
| 62 | SaturationScribe | 8.0/N=3 declaration text | ADMIT |
| 63 | ManifestScribe | integrator entry JSON | ADMIT |
| 64 | L0Scribe | receipt-identity L0 row (re-filed) | ADMIT |

## Deviations and honesty notes

- Provider: keys 1–2 interrupted pre-report (operator), keys 3/4/5 `402 Insufficient account funds`; key 6 per the standing "stick with it" directive.
- Observable amendments (folded from reviewers): `id=SCOPE_` count for emitting sites; namespaced cap ids; calibration verdict "unchanged (debt closure)".
- MANIFEST/L0: the round-12 `rounds[]` row and the receipt-identity L0 row are appended at the fleet root but deliberately NOT committed by the lane (the fleet `MANIFEST.json` worktree already carried an uncommitted integrator row; lanes never sweep integrator state). Integrator sweep requested via the L0 row.
- Receipt identity: OPEN since round 1, re-filed to the fleet L0 queue (`../.ufo/l0-questions.md`) this round with the measured blocker and a decide-(a)-or-(b) ask.
- Push state: 8 local commits unpushed; push is operator/integrator-owned (goal boundary: no pushes).
