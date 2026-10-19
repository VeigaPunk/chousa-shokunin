# chousa — round 21 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 10). Work commit `bfc291ef…` (HEAD when filed).

## Work performed

- Opening: claims + before-receipts (selftest PASS 124/0-skip; drift none vs r12 baseline; r1 3/3; gate `49b36759…`) — commit `b057245`.
- Wave: one batched AgentSwarm call, 32 seats, **opencode-go-6 / deepseek-v4.1-flash** (devin 502 quota for all 32 seats; opencode-go-6 per the operator's directive). 32/32 seat reports — zero deficit.
- Parent integration: the canonicalized `ptr_resolves_meta` + cases 125–128 + receipts.

## Landed changes (each tied to LOG.md round-21 entry)

- `tools/research-gate.sh` (`49b36759…` → `bfc291ef…`): `ptr_resolves_meta` canonicalizes the candidate with `readlink -f`, checks `in_root` against both roots, applies the denylist to the canonical target. Cases 125–128 appended.
- `corpus/knowledge/pointer-boundary-r21.md`: the escape mechanics, the fix contract, the named limits.
- `corpus/evidence/ptr-r21-20261019T184000Z-{demo,selftest,battery,drift}.log`: the receipts.
- `corpus/README.md` + `corpus/evidence/README.md` + `SKILL.md` + `SCORECARD.md` + `LOG.md`: the records.

## Before → after measurements

- Pointer boundary: before CLEAN on a traversal pointer → after `POINTER_UNRESOLVED` warn + DRIFT (receipt `ptr-r21-…-demo.log`).
- Selftest: 124 → 128 (0 skipped); cases 1–124 `cmp` byte-identical vs `verify-r20-20261019T180000Z-selftest.log`.
- Battery: r1 `3/3`; drift `none` vs the r12 baseline; masked battery vs the pre-round gate ALL IDENTICAL.

## Cross-domain evidence

None. All work confined to the chousa province.

## SHONEN

- [ ] real decision tables / error patterns / checklists with cited sources — `[~]` (knowledge notes + gate finding registry + selftest fixture tables; fresh lane review not on file)
- [ ] end-to-end domain task executed and logged — `[~]` (42 rounds of gate development with receipts; fresh lane review not on file)
- [ ] instructions executable by an agent without oral context — `[~]` (SKILL.md + `--help` + corpus README self-contained; fresh lane review not on file)
- [ ] no cross-domain bleed with `PROVINCE.md` still accurate — `[~]` (PROVINCE.md unchanged; fresh lane review not on file)

## Seat roster (32; model opencode-go-6 / deepseek-v4.1-flash; one batched call)

| seat | role | verdict |
|---|---|---|
| 01 | GuardAnalyst | DEFECT — both arms confirmed live (traversal + lane-root false-refusal) |
| 02 | FixDesigner | DEFECT — canonicalization fix designed and validated |
| 03 | Adversary (traversal) | DEFECT — `..` forms measured |
| 04 | Adversary (symlink) | DEFECT — symlink escape measured |
| 05 | Adversary (lane-root) | DEFECT — false-refusal confirmed |
| 06 | Adversary (dot-slash) | DEFECT — `./` forms measured |
| 07 | FixtureDesigner | DEFECT — cases 125–128 spec validated |
| 08 | SemanticsChecker | DEFECT — behavior change confirmed for ptr-resolves cases |
| 09 | RegressionScout | ADMIT — no committed fixture would newly refuse |
| 10 | DenylistAuditor | DEFECT — `.config` path-start bypass + canonical-target check needed |
| 11 | DenylistAuditor | DEFECT — denylist-on-target confirmed necessary |
| 12 | FencedAnchorAuditor | DEFECT — chain heading anchor is a different function — named debt |
| 13 | Reviewer (claim 1) | ADMIT — acceptance criteria met |
| 14 | Reviewer (cross-claim) | ADMIT — no r15/r17/r19 interaction |
| 15 | KnowledgeNoteScribe | DEFECT — note draft ready |
| 16 | ScorecardScribe | DEFECT — verdict skeleton landed |
| 17 | LogScribe | DEFECT — admission skeleton landed |
| 18 | ReportScribe | DEFECT — skeleton + roster landed |
| 19 | ReceiptScribe | DEFECT — receipt spec validated |
| 20 | DemoScout | DEFECT — before/after pair validated |
| 21 | ManifestScribe | ADMIT — MANIFEST entry JSON ready |
| 22 | SHONENScribe | ADMIT — SHONEN lines + seed check |
| 23 | CorpusReadmeScribe | ADMIT — README update draft |
| 24 | IdiomMatcher | ADMIT — style checklist landed |
| 25 | GitGuardScout | ADMIT — git-state audit clean |
| 26 | HeaderRegistryScout | ADMIT — doc anchors identified |
| 27 | FallbackPlanner | ADMIT — provider ladder runbook |
| 28 | ScopeBoundaryScout | ADMIT — boundary scan clean |
| 29 | Verifier | DEFECT — consistency pass; contradictions found and resolved |
| 30 | Verifier | DEFECT — call chain re-derived; all callers confirmed |
| 31 | Verifier | DEFECT — claim_source_path interaction clean |
| 32 | Verifier | DEFECT — .config denylist canonical-target requirement confirmed |

## Deviations and honesty notes

- **Provider deviation**: devin deepseek-v4-1-flash-high failed on 502 quota for all 32 seats; opencode-go-6 per the operator's directive. Recorded per the standing fallback doctrine.
- **The `.config` path-start bypass** (`is_denylist_path` uses `*/.config/*`, missing `.config/foo` at path start) is partially closed by the canonical-target check — a direct `.config/foo` citation (not through a symlink) still bypasses. Named debt for round 22.
- **The fenced-heading anchor** (chain `heading` anchors match headings inside fences) is a different function (`chain_anchor_heading`, not `load_sections`) — named debt.
- The `ptr_resolves_meta` fix closes three arms in one change: traversal, symlink, and the lane-root absolute-pointer false-refusal — the wave's seat 01 proved all three live.
