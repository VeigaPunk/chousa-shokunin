# chousa — round 19 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 8). Work commit `9f163807…` (HEAD when filed).

## Work performed

- Opening: claims + before-receipts (selftest PASS 119/0-skip; drift none vs r12 baseline; r1 3/3; gate `6e694881…`) — commit `5499cef`.
- Wave: one batched AgentSwarm call, 16 seats, **openai-codex gpt-6-luna-max** (zai exhaustion directive). 16/16 seat reports — zero deficit.
- Parent integration: the per-match canonicalization fix + cases 120–122 + receipts.

## Landed changes (each tied to LOG.md round-19 entry)

- `tools/research-gate.sh` (`6e694881…` → `9f163807…`): `verify_sweeps` canonicalizes every glob match against `in_root` for both roots; any match outside both roots refuses the whole sweep (`SWEEP_LOCATION_OUT_OF_CORPUS` crit). Cases 120–122 appended.
- `corpus/knowledge/sweep-symlink-r19.md`: the escape mechanics, the fix contract, the named limits.
- `corpus/evidence/symlink-r19-20261019T174500Z-{demo,selftest,battery,drift}.log`: the receipts.
- `corpus/README.md` + `corpus/evidence/README.md` + `SKILL.md` + `SCORECARD.md` + `LOG.md`: the records.

## Before → after measurements

- Symlink escape: before `SWEEP_CLAIM_FALSE` hit on an outside symlink → after `SWEEP_LOCATION_OUT_OF_CORPUS` crit + refused (receipt `symlink-r19-…-demo.log`).
- Selftest: 119 → 122 (0 skipped); cases 1–119 `cmp` byte-identical vs `scope-r18-20261019T173000Z-selftest.log`.
- Battery: r1 `3/3`; drift `none` vs the r12 baseline; masked battery vs the pre-round gate ALL IDENTICAL.

## Cross-domain evidence

None. All work confined to the chousa province.

## SHONEN

- [ ] real decision tables / error patterns / checklists with cited sources — `[~]` (knowledge notes + gate finding registry + selftest fixture tables; fresh lane review not on file)
- [ ] end-to-end domain task executed and logged — `[~]` (40 rounds of gate development with receipts; fresh lane review not on file)
- [ ] instructions executable by an agent without oral context — `[~]` (SKILL.md + `--help` + corpus README self-contained; fresh lane review not on file)
- [ ] no cross-domain bleed with `PROVINCE.md` still accurate — `[~]` (PROVINCE.md unchanged; fresh lane review not on file)

## Seat roster (16; model openai-codex gpt-6-luna-max; one batched call)

| seat | role | verdict |
|---|---|---|
| 01 | GuardAnalyst | DEFECT — escape confirmed live; leaf + dir shapes measured |
| 02 | FixDesigner | DEFECT — per-match canonicalization fix designed |
| 03 | Adversary (nested-symlinks) | DEFECT — chain resolution measured; `readlink -f` resolves whole chain |
| 04 | Adversary (glob-edge-cases) | DEFECT — dir-only, leaf, hidden, character-class escapes measured |
| 05 | Adversary (performance) | DEFECT — 10K match cost measured; batch canonicalization recommended |
| 06 | Adversary (broken-symlinks) | DEFECT — dangling symlink escape measured |
| 07 | FixtureDesigner | DEFECT — cases 120–122 spec validated |
| 08 | SemanticsChecker | NOTE — no existing case affected; fix compatible |
| 09 | RegressionScout | ADMIT — no committed fixture would newly refuse |
| 10 | Reviewer (claim 1) | DEFECT — acceptance criteria met |
| 11 | Reviewer (cross-claim) | DEFECT — no r15/r16 interaction; in_root unchanged |
| 12 | KnowledgeNoteScribe | DEFECT — note draft ready |
| 13 | ScorecardScribe | DEFECT — verdict skeleton landed |
| 14 | LogScribe | DEFECT — admission skeleton landed |
| 15 | ReceiptScribe | DEFECT — receipt spec validated |
| 16 | Verifier | DEFECT — consistency pass; escape confirmed at match level |

## Deviations and honesty notes

- The check is post-expansion: bash already traversed the symlinked directory during glob expansion (names only, never content). The "refused unopened" contract covers the match list, not the expansion traversal — a named limit recorded in the note.
- The demo fixture required the outside dir to be outside the declared root (not just outside `$WORK` inside it) — the first demo run used a sibling inside the root and produced identical output; corrected.
- No provider deviation this round — luna max per the zai-exhaustion directive.
