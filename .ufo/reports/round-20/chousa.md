# chousa — round 20 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 9 — second verification wave). Work commit `49b36759…` (HEAD when filed).

## Work performed

- Opening: claims + before-receipts (selftest PASS 122/0-skip; drift none vs r12 baseline; r1 3/3; gate `9f163807…`) — commit `d650872`.
- Wave: one batched AgentSwarm call, 64 audit seats, **openai-codex gpt-6-luna-max** (zai exhaustion directive). 64/64 seat reports — zero deficit.
- Parent integration: the `in_comment` tracking in `load_sections` + case 124 + receipts + absorbed prior-session work (tok_span_at rewrite, case 123, closure recheck).

## Landed changes (each tied to LOG.md round-20 entry)

- `tools/research-gate.sh` (`9f163807…` → `49b36759…`): `load_sections` tracks `in_comment` alongside `fence_char` — a `## ` inside `<!-- -->` is literal; case 124 appended. Absorbed: `tok_span_at` rewrite (grep PCRE), `claims-cap-eof` case 123.
- `corpus/knowledge/html-comment-r20.md`: the shadow class generalized.
- `corpus/evidence/verify-r20-20261019T180000Z-{demo,selftest,battery,drift}.log`: the receipts.
- `corpus/README.md` + `corpus/evidence/README.md` + `SKILL.md` + `SCORECARD.md` + `LOG.md`: the records.

## Before → after measurements

- HTML-comment shadow: before CLEAN on a shadowed refused domain → after `SCOPE_BOUNTY_ABSORBED` warn + DRIFT (receipt `verify-r20-…-demo.log`).
- Selftest: 122 → 124 (0 skipped); cases 1–119 `cmp` byte-identical vs `scope-r18-20261019T173000Z-selftest.log`.
- Battery: r1 `3/3`; drift `none` vs the r12 baseline; masked battery vs the pre-round gate ALL IDENTICAL.

## Cross-domain evidence

None. All work confined to the chousa province.

## SHONEN

- [ ] real decision tables / error patterns / checklists with cited sources — `[~]` (knowledge notes + gate finding registry + selftest fixture tables; fresh lane review not on file)
- [ ] end-to-end domain task executed and logged — `[~]` (41 rounds of gate development with receipts; fresh lane review not on file)
- [ ] instructions executable by an agent without oral context — `[~]` (SKILL.md + `--help` + corpus README self-contained; fresh lane review not on file)
- [ ] no cross-domain bleed with `PROVINCE.md` still accurate — `[~]` (PROVINCE.md unchanged; fresh lane review not on file)

## Seat roster (64; model openai-codex gpt-6-luna-max; one batched call)

| seat | role | verdict |
|---|---|---|
| 01 | AuditLead | DEFECT — HTML-comment heading shadow found (the round's fix) |
| 02 | InRootAuditor | ADMIT — in_root contract verified |
| 03 | InRootAuditor | DEFECT — ptr_resolves_meta boundary gap found |
| 04 | FenceAuditor | ADMIT — fence parser verified; mismatched-char and trailing-text closers handled |
| 05 | FenceAuditor | NOTE — unclosed-fence semantics confirmed |
| 06 | FenceAuditor | DEFECT — fenced-heading anchor false-positive found |
| 07 | ScopePhraseAuditor | DEFECT — llm evaluations/llm evals/ai benchmarks/language model benchmark(s) gaps |
| 08 | ScopePhraseAuditor | DEFECT — workflow dispatch/security bounty/vulnerability disclosure/responsible disclosure/bug bounties/dispatch mechanisms gaps |
| 09 | SweepsAuditor | ADMIT — per-match canonicalization verified; refuse-all semantic correct |
| 10 | SweepsAuditor | DEFECT — match path revealed in finding (doc mismatch, not a defect) |
| 11 | SweepsAuditor | DEFECT — exempt/non-local rows bypass correctly; literal `status=exempt` unrecognized |
| 12 | InteractionAuditor | NOTE — fenced Meta inside real Meta still scanned (documented limit) |
| 13 | InteractionAuditor | NOTE — in_root × per-match interaction clean |
| 14 | InteractionAuditor | ADMIT — pin fixture has no fences; no drift |
| 15 | ClaimsBoundaryAuditor | DEFECT — `.config` denylist bypass at path start; URI classification edge |
| 16 | ChainBoundaryAuditor | DEFECT — fenced-heading anchor false-positive; no out-of-root read |
| 17 | IntegrityAuditor | ADMIT — REF_UNRESOLVED classification verified |
| 18 | VerifyAllAuditor | DEFECT — claims file with `##` comment drifts in composition (format-precedence gap) |
| 19 | SelftestQualityAuditor | DEFECT — symlink cases accept extra findings; coverage gaps noted |
| 20 | SelftestQualityAuditor | ADMIT — case numbering invariant holds |
| 21 | FindingRegistryAuditor | DEFECT — no asserted-but-unemitted IDs; 8 unasserted IDs confirmed |
| 22 | SecretScanAuditor | DEFECT — cited source files not scanned; MINT.md format gaps |
| 23 | SecretScanAuditor | ADMIT — claims/chain files scanned; mismatch diagnostics noted |
| 24 | KnowledgeNoteAuditor | DEFECT — fenced-heading note's HTML claim was premature |
| 25 | KnowledgeNoteAuditor | DEFECT — mount-alias note overstatement; stale queued item |
| 26 | HardeningLedgerAuditor | DEFECT — count phantom confirmed |
| 27 | ReceiptAuditor | DEFECT — r15 battery receipt wrong paths (already fixed) |
| 28 | FixtureAuditor | DEFECT — full-r6 README sweeps-absent wrong (already fixed) |
| 29 | BoundaryAuditor | DEFECT — URI-like citations treated as local paths (named debt) |
| 30 | BoundaryAuditor | DEFECT — ptr_resolves_meta boundary gap confirmed |
| 31 | CodeQualityAuditor | DEFECT — `--` delimiter edge |
| 32 | CodeQualityAuditor | DEFECT — TOCTOU readability abort non-2 |
| 33 | ConcurrencyAuditor | NOTE — shared output paths caveat |
| 34 | DocumentationAuditor | DEFECT — SKILL.md case-count claims verified |
| 35 | DocumentationAuditor | DEFECT — corpus README index completeness |
| 36 | CrossRoundAuditor | DEFECT — allowed-roots consistent across modes |
| 37 | CrossRoundAuditor | DEFECT — canonicalization order correct; ptr_resolves_meta gap confirmed |
| 38 | EdgeCaseAuditor | ADMIT — empty inputs handled sanely |
| 39 | EdgeCaseAuditor | ADMIT — malformed inputs handled gracefully |
| 40 | EdgeCaseAuditor | ADMIT — large-input performance sane (tok_span_at rewrite landed) |
| 41 | PortabilityAuditor | DEFECT — bash-4+ constructs; no bash-3 fallback |
| 42 | PortabilityAuditor | ADMIT — command dependencies mapped; grep -P guarded |
| 43 | RegressionAuditor | ADMIT — r17-r19 changes: no uncovered breakage |
| 44 | RegressionAuditor | ADMIT — CHOUSA_ env vars documented |
| 45 | DebtAuditor | ADMIT — carried items still open |
| 46 | DebtAuditor | ADMIT — closed items verified |
| 47 | AdmissionAuditor | DEFECT — round verdicts match evidence; r15 battery defect noted |
| 48 | AdmissionAuditor | ADMIT — dispositions tracked; named debts carried |
| 49 | SHONENScribe | ADMIT — SHONEN lines + seed check |
| 50 | SaturationScribe | ADMIT — window/capability accounting |
| 51 | L0Scribe | ADMIT — L0 state check (r12 row still open; routed around) |
| 52 | ClosureScribe | ADMIT — closure checklist landed |
| 53 | ReceiptScribe2 | ADMIT — receipt spec validated |
| 54 | WaveArchivist | ADMIT — wave-shape paragraph landed |
| 55 | BaselineGuardScout | ADMIT — committed-receipt perturbation audit |
| 56 | ScorecardScribe | ADMIT — verdict block skeleton landed |
| 57 | LogScribe | ADMIT — admission skeleton landed |
| 58 | ReportScribe | ADMIT — skeleton + roster landed |
| 59 | LessonScribe | ADMIT — lesson draft ready |
| 60 | ManifestScribe | ADMIT — MANIFEST entry JSON ready |
| 61 | CorpusReadmeScribe | ADMIT — README update draft |
| 62 | IdiomMatcher | ADMIT — style checklist landed |
| 63 | GitGuardScout | ADMIT — git-state audit clean |
| 64 | SynthesisAuditor | ADMIT — loop-1 coherence assessment landed |

## Deviations and honesty notes

- The HTML-comment shadow is the same class as the fenced-heading shadow (r17) but a different syntax — the r17 fix handled fences only. The wave caught the generalization.
- The `ptr_resolves_meta` boundary gap is a real defect: relative paths check `-f` without canonicalization — `..` traversal and symlinks escape. Named debt for round 21.
- The denylist `.config` bypass: `*/.config/*` doesn't match `.config/foo` at path start. Named debt.
- The fenced-heading anchor: chain `heading` anchors match headings inside fences — a false positive in a different function than `load_sections`. Named debt.
- The `tok_span_at` rewrite and `claims-cap-eof` case 123 were uncommitted prior-session work — absorbed and verified.
- The wave's "refused unopened" wording in the r19 note overstated — the finding DOES include the match path (corrected in the note).
