# chousa — round 18 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 7). Work commit `6e694881…` (HEAD when filed).

## Work performed

- Opening: claims + before-receipts (selftest PASS 116/0-skip; drift none vs r12 baseline; r1 3/3; gate `c2915f24…`) — commit `e3c556e`.
- Wave: one batched AgentSwarm call, 16 seats, **openai-codex gpt-6-luna-max** (zai glm-5.3-flash quota exhausted; operator directed codex luna max for all zai-assigned rounds until tomorrow). 16/16 seat reports — zero deficit.
- Parent integration: the `SCOPE_KENGAKU` 3-phrase addition + cases 117–119 + receipts.

## Landed changes (each tied to LOG.md round-18 entry)

- `tools/research-gate.sh` (`c2915f24…` → `6e694881…`): `SCOPE_KENGAKU` gains `llm benchmark|llm benchmarks|llm scoring`; cases 117–119 appended.
- `corpus/knowledge/scope-phrase-gap-r18.md`: the gap mechanics, the conservative-vs-broad boundary, the dispositioned findings.
- `corpus/evidence/scope-r18-20261019T173000Z-{demo,selftest,battery,drift}.log`: the receipts.
- `corpus/README.md` + `corpus/evidence/README.md` + `SKILL.md` + `SCORECARD.md` + `LOG.md`: the records.

## Before → after measurements

- Phrase gap: before CLEAN on `domain: LLM benchmarks` → after `SCOPE_MODEL_QUALITY_ABSORBED` warn + DRIFT (receipt `scope-r18-…-demo.log`).
- Selftest: 116 → 119 (0 skipped); cases 1–116 `cmp` byte-identical vs `fence-r17-20261019T171200Z-selftest.log`.
- Battery: r1 `3/3`; drift `none` vs the r12 baseline; masked battery vs the pre-round gate ALL IDENTICAL.

## Cross-domain evidence

None. All work confined to the chousa province.

## SHONEN

- [ ] real decision tables / error patterns / checklists with cited sources — `[~]` (knowledge notes + gate finding registry + selftest fixture tables; fresh lane review not on file)
- [ ] end-to-end domain task executed and logged — `[~]` (39 rounds of gate development with receipts; fresh lane review not on file)
- [ ] instructions executable by an agent without oral context — `[~]` (SKILL.md + `--help` + corpus README self-contained; fresh lane review not on file)
- [ ] no cross-domain bleed with `PROVINCE.md` still accurate — `[~]` (PROVINCE.md unchanged; fresh lane review not on file)

## Seat roster (16; model openai-codex gpt-6-luna-max; one batched call)

| seat | role | verdict |
|---|---|---|
| 01 | KengakuAuditor | DEFECT — additional phrase gaps found (llm ranking, model ranking, alignment eval, capability eval) |
| 02 | KasegiAuditor | DEFECT — `bug bounties` plural not covered; `security bounty`/`vulnerability reward`/`exploit bounty`/`cve bounty`/`reward program` gaps |
| 03 | KumitateAuditor | DEFECT — `task dispatch`/`multi-agent system`/`agent management`/`agent coordination`/`agent scheduling` gaps |
| 04 | FixDesigner | DEFECT — confirmed 3-phrase minimal set validated |
| 05 | FixtureDesigner | DEFECT — cases 117–119 spec validated |
| 06 | Adversary (false-positive) | DEFECT — `ai benchmark(s)` too broad; `llm benchmark(s)`/`llm scoring` defensible |
| 07 | Adversary (scope_norm) | DEFECT — normalization chain verified; `llmbenchmark` camel-case gap found |
| 08 | Adversary (case-sensitivity) | DEFECT — normalization end-to-end verified |
| 09 | SemanticsChecker | DEFECT — no existing case declares benchmark domains; addition is safe |
| 10 | RegressionScout | ADMIT — no committed record would newly refuse |
| 11 | KnowledgeNoteScribe | DEFECT — addendum draft ready |
| 12 | ScorecardScribe | DEFECT — skeleton landed; `llm evaluations`/`llm evals` additional gap found |
| 13 | LogScribe | NOTE — no additional high-confidence gap in kasegi/kumitate beyond what seats 02/03 found |
| 14 | ReportScribe | DEFECT — report skeleton + roster landed; `SCOPE_BOUNTY` not `SCOPE_KASEGI` naming note |
| 15 | ReceiptScribe | DEFECT — receipt spec validated; `language model benchmark(s)` candidate noted |
| 16 | Verifier | DEFECT — consistency pass; additional contradictions found (gate header "before any read" overclaim; README r17 description wrong) |

## Deviations and honesty notes

- **Provider deviation**: zai glm-5.3-flash quota exhausted; operator directed codex luna max for all zai-assigned rounds until tomorrow. Recorded per the standing fallback doctrine.
- **Conservative fix boundary**: the wave's adversary seats measured `ai benchmark(s)` too broad (false-positive on AI-methodology research) — dropped from the fix, kept as named debt.
- **Additional findings absorbed**: seats 01/02/03 found more phrase gaps (`llm ranking`, `model ranking`, `bug bounties`, `task dispatch`, `agent management`, `agent coordination`, `agent scheduling`, `llm evaluations`, `language model benchmark(s)`, `llmbenchmark` camel-case) — all dispositioned as named debt for round 19 (the claim was the `LLM benchmarks` class, not the full phrase-list audit).
- **README erratum**: `corpus/README.md` described the r17 note as carrying the `LLM benchmarks` disposition — that text lives in `verification-r16.md`, not `fenced-heading-r17.md`. Corrected in this round's README update.
