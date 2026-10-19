# chousa — round 17 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 6). Work commit `c2915f24…` (HEAD when filed).

## Work performed

- Opening: claims + before-receipts (selftest PASS 111/0-skip; drift none vs r12 baseline; r1 3/3; gate `2b64a1c8…`) — commit `eaa3bbd`.
- Wave: one batched AgentSwarm call, 32 seats, **opencode-go / deepseek-v4.1-flash** — xai-oauth grok-4.7-fast failed on 403 quota for all 48 seats; zai glm-5.3-flash interrupted at 14/48 before re-dispatch landed on opencode-go. 27/32 seat reports — 5 failed on provider 400 `reasoning_content` errors; deficit recorded, not backfilled.
- Parent integration: the two-pass fence-aware `load_sections` + cases 112–116 + receipts.

## Landed changes (each tied to LOG.md round-17 entry)

- `tools/research-gate.sh` (`2b64a1c8…` → `c2915f24…`): `load_sections` pairs fences in two passes — same char must close, closing length >= opening, 0–3 literal-space indent; unclosed opener = fence to EOF (fail closed). Cases 112–116 appended.
- `corpus/knowledge/fenced-heading-r17.md`: the shadow mechanics, the naive-vs-two-pass measured shape matrix, the call-site audit, named limits.
- `corpus/evidence/fence-r17-20261019T171200Z-{demo,selftest,battery,drift}.log`: the receipts.
- `corpus/README.md` + `corpus/evidence/README.md` + `SKILL.md` + `SCORECARD.md` + `LOG.md`: the records.

## Before → after measurements

- Fenced shadow: before CLEAN on a refused domain shadowed by a fenced `## Meta` → after `SCOPE_BOUNTY_ABSORBED` warn + DRIFT (receipt `fence-r17-20261019T171200Z-demo.log`).
- Selftest: 111 → 116 (0 skipped); cases 1–109 `cmp` byte-identical vs `root-r15-20261019T152000Z-selftest.log` (r16 inserted case 110 — the cmp boundary is 109).
- Battery: r1 `3/3`; drift `none` vs the r12 baseline; masked battery vs the pre-round gate ALL IDENTICAL.
- Shape matrix (measured): naive `^``` ` toggle fixes only the simple shadow; the two-pass shape closes all five variants (simple, phantom, nested, indented, unclosed).

## Cross-domain evidence

None. All work confined to the chousa province.

## SHONEN

- [ ] real decision tables / error patterns / checklists with cited sources — `[~]` (the knowledge notes + gate finding registry + selftest fixture tables; fresh lane review not on file)
- [ ] end-to-end domain task executed and logged — `[~]` (38 rounds of gate development with receipts; fresh lane review not on file)
- [ ] instructions executable by an agent without oral context — `[~]` (SKILL.md + `--help` + corpus README self-contained; fresh lane review not on file)
- [ ] no cross-domain bleed with `PROVINCE.md` still accurate — `[~]` (PROVINCE.md unchanged; fresh lane review not on file)

## Seat roster (32; model opencode-go / deepseek-v4.1-flash; one batched call)

| seat | role | verdict |
|---|---|---|
| 01 | CallSiteAuditor | failed (provider 400) |
| 02 | FixtureDesigner | ADMIT — cases 112–114 designed, measured on shadow-tree copies |
| 03 | Adversary (unclosed-fence) | ADMIT — unclosed-fence semantics measured |
| 04 | Adversary (fence-in-fence) | ADMIT — nested/tilde/language-tag coverage measured |
| 05 | Adversary (pin-fixture) | ADMIT — zero fences in canonical fixture; no drift |
| 06 | Adversary (other-sections) | failed (provider 400) |
| 07 | Adversary (scope-not-trigger) | failed (provider 400) |
| 08 | HarnessScout | ADMIT — heredoc fence encoding clean |
| 09 | ByteIdentityAnalyst | ADMIT — head-109 cmp spec correct (r16 inserted case 110) |
| 10 | SemanticsChecker | ADMIT — fenced-only Meta → CLEAN (declaration-only contract) |
| 11 | RegressionScout | ADMIT — only scope cases affected on scratch copy |
| 12 | ReceiptScout | ADMIT — before-battery verbatim + live demo |
| 13 | Reviewer (claim 1) | failed (provider 400) |
| 14 | Reviewer (claim 2) | ADMIT — depth criteria met |
| 15 | Reviewer (cross-claim) | ADMIT — kill-checks passed |
| 16 | Reviewer (protocol) | ADMIT — conformance checks passed |
| 17 | Reviewer (evidence) | ADMIT — receipt set complete |
| 18 | Critic (round-level) | ADMIT — fix over named debt recommended |
| 19 | Critic (claim 1) | ADMIT — two-pass over naive toggle |
| 20 | SkillRowDesigner | ADMIT — SKILL.md spec landed |
| 21 | KnowledgeNoteDesigner | failed (provider 400) |
| 22 | LedgerScribe | ADMIT — E5 addendum draft ready |
| 23 | ScorecardScribe | ADMIT — verdict block skeleton landed |
| 24 | LogScribe | ADMIT — admission skeleton landed |
| 25 | ReportScribe | ADMIT — skeleton + roster landed |
| 26 | LessonScribe | ADMIT — lesson draft ready |
| 27 | DemoScout | ADMIT — before/after pair validated |
| 28 | ManifestScribe | ADMIT — MANIFEST entry JSON ready |
| 29 | SHONENScribe | ADMIT — SHONEN lines + seed check |
| 30 | CorpusReadmeScribe | DEFECT — naive toggle still reopens shadow; robust shape validated |
| 31 | IdiomMatcher | ADMIT — style checklist landed |
| 32 | Verifier | DEFECT — fix shape has bash parse error + three bypasses; corrected shape built |

## Deviations and honesty notes

- **Provider deviation**: xai-oauth grok-4.7-fast failed on 403 quota for all 48 seats; zai glm-5.3-flash was interrupted at 14/48; the wave landed on opencode-go / deepseek-v4.1-flash (32 seats). Recorded per the standing fallback doctrine.
- **Seat deficit**: 5/32 seats failed on provider 400 `reasoning_content` errors — recorded, not backfilled (r14 precedent).
- **Wave-critical finding**: the naive `^``` ` toggle the first wave proposed still reopens the shadow on nested 4-backtick, indented closers, and unclosed fences (seats 30/32 measured). The landed two-pass shape closes all five variants — the wave's adversarial seats caught a fix that would have shipped broken.
- **Unclosed fence semantics**: the seat-30 design treated an unclosed opener as plain text (letting the shadow through); the landed form treats it as a fence to EOF — fail closed.
- **`LLM benchmarks` phrase gap**: stays named debt for round 18 (not silently absorbed).
