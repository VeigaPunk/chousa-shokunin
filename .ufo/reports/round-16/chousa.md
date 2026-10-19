# chousa — round 16 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 5 — verification wave). Work commit `2b64a1c8…` (HEAD when filed).

## Work performed

- Opening: claims + before-receipts (selftest PASS 110/0-skip; drift none vs r12 baseline; r1 3/3; gate `dd0951d7…`) — commit `6d28975`.
- Wave: one batched AgentSwarm call, 64 read-only audit seats, **openai-codex gpt-6-luna-max** (liveness-probed at opening; fallback ladder devin → token-plan → opencode-go-6 not needed). 64/64 seat reports — zero deficit.
- Parent integration: dispositioned every wave finding — 2 fixes landed (`--root //` in_root strip-all + corrected battery receipt), ~15 absorbs (record corrections), ~12 named debts (round-17 queue). Disposition table: `corpus/knowledge/verification-r16.md`.

## Landed changes (each tied to LOG.md round-16 entry)

- `tools/research-gate.sh` (`dd0951d7…` → `2b64a1c8…`): `in_root()` strips all trailing slashes (loop, not single `${r%/}`); selftest case 111 pins `--root //`.
- `corpus/evidence/root-r15-20261019T152000Z-battery.log`: replaced — corrected fixture paths (`archives-r9/`, `--root ..`), masked diff IDENTICAL.
- `corpus/knowledge/verification-r16.md`: the full disposition table.
- `corpus/knowledge/mount-alias-r14.md`: unmeasurable-stat corrected (`wc -c` reads to measure); queued `--root /` item closed.
- `corpus/knowledge/scope-refusal-r12.md`: coverage overstatement corrected.
- `corpus/fixtures/full-r6.README.md`: sweeps-absent claim corrected.
- `corpus/README.md`: verification-r16 row added.
- `SKILL.md`: 110→111 cases; r15 paragraph updated for `//`.
- `SCORECARD.md`: round-16 verdict + round-17 registration.
- `LOG.md`: round-16 admission.

## Before → after measurements

- `--root //`: before `CLAIM_SOURCE_OUT_OF_CORPUS` crit on `/etc/hostname` → after `CLEAN` `1/1` (case 111).
- Selftest: 110 → 111 (0 skipped); cases 1–110 `cmp` byte-identical vs r15 receipt.
- Battery: r1 `3/3`; drift `none` vs r12 baseline; corrected masked battery vs pre-round gate ALL IDENTICAL.
- Boundary soundness: no out-of-corpus read found across 64 audit seats; all refusal classes held.

## Cross-domain evidence

None. All work confined to the chousa province.

## SHONEN

- [ ] real decision tables / error patterns / checklists with cited sources — `[~]` (verification-r16.md is itself a cited audit table; fresh lane review not on file)
- [ ] end-to-end domain task executed and logged — `[~]` (37 rounds of gate development with receipts; fresh lane review not on file)
- [ ] instructions executable by an agent without oral context — `[~]` (SKILL.md + gate `--help` + corpus README self-contained; fresh lane review not on file)
- [ ] no cross-domain bleed with `PROVINCE.md` still accurate — `[~]` (PROVINCE.md unchanged; fresh lane review not on file)

## Seat roster (64; model openai-codex gpt-6-luna-max; one batched call)

| seat | role | key deliverable | verdict |
|---|---|---|---|
| 01 | AuditLead | audit matrix; 52 emitted IDs, 8 unasserted | DEFECT |
| 02 | ScopeAuditor | fenced-heading shadow; `LLM benchmarks` gap | DEFECT |
| 03 | ScopeAuditor | `wc -c` fallback reads oversized files; measurement-failure bypass | DEFECT |
| 04 | CapAuditor | same `wc -c` finding (cross-confirmed) | DEFECT |
| 05 | MultilinkAuditor | hardlink refusal correct; stale-status notes found | ADMIT |
| 06 | MultilinkAuditor | no hardlink escape; named limit honest | ADMIT |
| 07 | CrossDeviceAuditor | device probe correct; longest-prefix unpinned edge | NOTE |
| 08 | CrossDeviceAuditor | stat-failure conditional fail-open (fault-injection) | DEFECT |
| 09 | RootSlashAuditor | `--root //` still refused; in_root single-strip defect | DEFECT |
| 10 | RootSlashAuditor | `--root //` confirmed; ptr_resolves_meta untested | DEFECT |
| 11 | HarnessAuditor | CHOUSA_ classifier correct; no want-token hijack | ADMIT |
| 12 | HarnessAuditor | case-numbering invariant holds; coverage gap only | ADMIT |
| 13 | FindingRegistryAuditor | 8 unasserted IDs enumerated | DEFECT |
| 14 | FindingRegistryAuditor | severity assignments audited; consistent | DEFECT |
| 15 | ClaimsAuditor | expect-vocab + span-matching verified | ADMIT |
| 16 | ClaimsAuditor | no path-traversal escape; `--root //` defect confirmed | DEFECT |
| 17 | ChainAuditor | undeclared source IDs rejected; anchor ambiguity ok | ADMIT |
| 18 | ChainAuditor | claim-ID in `to` kind-blindness (already carried) | DEFECT |
| 19 | SweepsAuditor | 3 classification/boundary mismatches | DEFECT |
| 20 | SweepsAuditor | symlink-escape through wildcard | DEFECT |
| 21 | IntegrityAuditor | REF_UNRESOLVED classification verified | DEFECT |
| 22 | IntegrityAuditor | multi-token cells; duplicate IDs | DEFECT |
| 23 | VerifyAllAuditor | per-section applicability verified | DEFECT |
| 24 | VerifyAllAuditor | `--json` delimiter edge; outside-root append | DEFECT |
| 25 | PinDriftAuditor | manifest timestamp mask too broad | DEFECT |
| 26 | PinDriftAuditor | truncated-baseline ambiguity | DEFECT |
| 27 | KnowledgeNoteAuditor | root-slash note claims reproduced | DEFECT |
| 28 | KnowledgeNoteAuditor | mount-alias note overstatement; stale queued item | DEFECT |
| 29 | KnowledgeNoteAuditor | scope-refusal coverage overstatement | DEFECT |
| 30 | HardeningLedgerAuditor | count phantom in E3 confirmed | DEFECT |
| 31 | LedgerConsistencyAuditor | count drift across files found | DEFECT |
| 32 | ReceiptAuditor | r15 battery receipt wrong paths | DEFECT |
| 33 | ReceiptAuditor | r14 receipts verified; baseline header correct | DEFECT |
| 34 | FixtureAuditor | full-r6 README sweeps-absent wrong | DEFECT |
| 35 | FixtureAuditor | selftest staleness: PASS 110/110 current | ADMIT |
| 36 | BoundaryAuditor | URI-like citation classification edge | DEFECT |
| 37 | BoundaryAuditor | pointer boundary held | DEFECT |
| 38 | BoundaryAuditor | ephemeral/URL pointer refusals verified | DEFECT |
| 39 | SecretScanAuditor | 11 regex branches verified; MINT.md gaps | DEFECT |
| 40 | SecretScanAuditor | cited source files not scanned | DEFECT |
| 41 | SelftestIntegrityAuditor | FAIL-summary skip asymmetry | DEFECT |
| 42 | SelftestIntegrityAuditor | hermeticity verified; cleanup correct | DEFECT |
| 43 | CodeQualityAuditor | `--` delimiter edge | DEFECT |
| 44 | CodeQualityAuditor | TOCTOU readability abort non-2 | DEFECT |
| 45 | ConformanceAuditor | rounds partially conformant; exploratory-claim scope | NOTE |
| 46 | ConformanceAuditor | lane-identity commits clean | ADMIT |
| 47 | ConcurrencyAuditor | shared output paths caveat | NOTE |
| 48 | ConcurrencyAuditor | parallel selftest safe; counters scoped | DEFECT |
| 49 | DocumentationAuditor | SKILL.md case-count claims verified | DEFECT |
| 50 | DocumentationAuditor | corpus README index completeness | DEFECT |
| 51 | CrossRoundAuditor | allowed-roots consistent across modes | DEFECT |
| 52 | CrossRoundAuditor | canonicalization order correct; `--root //` + relative-root defects | DEFECT |
| 53 | EdgeCaseAuditor | empty inputs handled sanely | DEFECT |
| 54 | EdgeCaseAuditor | malformed inputs handled gracefully | DEFECT |
| 55 | EdgeCaseAuditor | large-input performance sane | DEFECT |
| 56 | PortabilityAuditor | bash-4+ constructs; no bash-3 fallback | DEFECT |
| 57 | PortabilityAuditor | command dependencies mapped | DEFECT |
| 58 | RegressionAuditor | r15 changes: no uncovered breakage | DEFECT |
| 59 | RegressionAuditor | CHOUSA_ env vars documented | DEFECT |
| 60 | DebtAuditor | carried items still open | DEFECT |
| 61 | DebtAuditor | closed items verified | DEFECT |
| 62 | AdmissionAuditor | round verdicts match evidence; r15 battery defect | DEFECT |
| 63 | WaveIntegrityAuditor | roster internally complete; raw wave unverifiable | NOTE |
| 64 | SynthesisAuditor | loop-1 coherence assessment | ADMIT |

## Deviations and honesty notes

- The `--root //` defect is a real escape of the r15 fix — the wave caught it because the r15 note claimed `//` heals but the selftest only pinned `/`. The fix (strip all trailing slashes) is landed and pinned by case 111.
- The r15 battery receipt is replaced with a corrected run — the original ran `verify` on nonexistent `corpus/fixtures/A-r9.md` paths with `--root .`, producing identical refusal output from both gates but exercising nothing. The corrected run uses `archives-r9/` paths and `--root ..`.
- Most "DEFECT" seat verdicts are findings for disposition, not admissions — the verification wave's claim is that every finding gets a disposition (fix/absorb/debt), not that the codebase is defective. The ~12 named debts are the round-17 queue.
- Seat verdict labels are approximate — many seats report a primary finding type (DEFECT/NOTE/ADMIT) but also list secondary findings. The disposition table in `corpus/knowledge/verification-r16.md` is the authoritative record.
