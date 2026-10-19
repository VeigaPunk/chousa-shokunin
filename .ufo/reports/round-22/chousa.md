# chousa — round 22 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 11). Work commit `dfb798b4…` (HEAD when filed).

## Work performed

- Opening: claims + before-receipts (selftest PASS 128/0-skip; drift none vs r12 baseline; r1 3/3; gate `bfc291ef…`) — commit `10083e1`.
- Wave: one batched AgentSwarm call, 32 seats, **openai-codex gpt-6-luna-max** (antigravity gemini-3.8-flash failed 24 seats on provider errors + 8 aborted; luna per the fallback ladder). 32/32 seat reports — zero deficit.
- Parent integration: the bare-start denylist patterns + cases 129–132 + receipts.

## Landed changes (each tied to LOG.md round-22 entry)

- `tools/research-gate.sh` (`bfc291ef…` → `dfb798b4…`): `is_denylist_path` gains bare-start alternatives `'.config/'*`, `'.omp/'*`, `'.local/state/'*`. Cases 129–132 appended.
- `corpus/knowledge/denylist-r22.md`: the path-start bypass mechanics, the fix contract, the named limits.
- `corpus/evidence/deny-r22-20261019T190000Z-{demo,selftest,battery,drift}.log`: the receipts.
- `corpus/README.md` + `corpus/evidence/README.md` + `SKILL.md` + `SCORECARD.md` + `LOG.md`: the records.

## Before → after measurements

- Denylist path-start: before CLEAN on `.config/agent-token.txt` (no `./` prefix) → after `CLAIM_SOURCE_SESSION` crit + refused (receipt `deny-r22-…-demo.log`).
- Selftest: 128 → 132 (0 skipped); cases 1–128 `cmp` byte-identical vs `ptr-r21-20261019T184000Z-selftest.log`.
- Battery: r1 `3/3`; drift `none` vs the r12 baseline; masked battery vs the pre-round gate ALL IDENTICAL.

## Cross-domain evidence

None. All work confined to the chousa province.

## SHONEN

- [ ] real decision tables / error patterns / checklists with cited sources — `[~]` (knowledge notes + gate finding registry + selftest fixture tables; fresh lane review not on file)
- [ ] end-to-end domain task executed and logged — `[~]` (43 rounds of gate development with receipts; fresh lane review not on file)
- [ ] instructions executable by an agent without oral context — `[~]` (SKILL.md + `--help` + corpus README self-contained; fresh lane review not on file)
- [ ] no cross-domain bleed with `PROVINCE.md` still accurate — `[~]` (PROVINCE.md unchanged; fresh lane review not on file)

## Seat roster (32; model openai-codex gpt-6-luna-max; one batched call)

| seat | role | verdict |
|---|---|---|
| 01 | DenylistAnalyst | DEFECT — path-start gap confirmed live on all three patterns |
| 02 | FixDesigner | DEFECT — bare-start alternatives designed and validated |
| 03 | Adversary (path-forms) | DEFECT — `.config`/`.omp`/`.local/state` all share the gap |
| 04 | Adversary (norm-ptr) | DEFECT — `norm_ptr` strips backticks only, not `./` |
| 05 | Adversary (denylist-symlink) | DEFECT — path-start check not redundant with canonical check |
| 06 | Adversary (other-patterns) | DEFECT — other patterns use `*` not `*/X/*` — no shared gap |
| 07 | FixtureDesigner | DEFECT — cases 129–132 spec validated |
| 08 | SemanticsChecker | DEFECT — behavior change confirmed for denylist cases |
| 09 | RegressionScout | ADMIT — no committed fixture would newly refuse |
| 10 | FencedAnchorAuditor | DEFECT — chain heading anchor is a different function — named debt |
| 11 | Reviewer (claim 1) | ADMIT — acceptance criteria met |
| 12 | Reviewer (cross-claim) | ADMIT — no r21 interaction |
| 13 | KnowledgeNoteScribe | DEFECT — note draft ready |
| 14 | ScorecardScribe | DEFECT — verdict skeleton landed |
| 15 | LogScribe | DEFECT — admission skeleton landed |
| 16 | ReportScribe | DEFECT — skeleton + roster landed |
| 17 | ReceiptScribe | DEFECT — receipt spec validated |
| 18 | DemoScout | DEFECT — before/after pair validated |
| 19 | ManifestScribe | ADMIT — MANIFEST entry JSON ready |
| 20 | SHONENScribe | ADMIT — SHONEN lines + seed check |
| 21 | CorpusReadmeScribe | ADMIT — README update draft |
| 22 | IdiomMatcher | ADMIT — style checklist landed |
| 23 | GitGuardScout | ADMIT — git-state audit clean |
| 24 | HeaderRegistryScout | ADMIT — doc anchors identified |
| 25 | FallbackPlanner | ADMIT — provider ladder runbook |
| 26 | ScopeBoundaryScout | ADMIT — boundary scan clean |
| 27 | Verifier | DEFECT — consistency pass; contradictions resolved |
| 28 | Verifier | DEFECT — call chain re-derived; all callers confirmed |
| 29 | Verifier | DEFECT — norm_ptr interaction clean |
| 30 | Verifier | DEFECT — all modes share the denylist benefit |
| 31 | Verifier | DEFECT — existing .config case uses `./` form — path-start was uncovered |
| 32 | Verifier | DEFECT — path-start fix not redundant with canonical check |

## Deviations and honesty notes

- **Provider deviation**: antigravity gemini-3.8-flash failed 24 seats on provider errors + 8 aborted; luna per the fallback ladder. Recorded per the standing doctrine.
- **Redundancy check**: the r21 canonical-target check covers `.config` through a symlink but not the raw path-start form — the two checks complement each other, not redundant.
- **The `.config-adjacent` control** proves the fix doesn't over-refuse — the `'/` after the directory name is the discriminator.
