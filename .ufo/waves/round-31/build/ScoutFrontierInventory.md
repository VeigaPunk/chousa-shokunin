# ScoutFrontierInventory — round 31 W1 build

Scout seat for the planning data-walk: open frontier outside `tools/quote-reopen.py`.
Read sources: `corpus/evidence/round31/claims.md` (frozen C1/C2), `corpus/README.md`
(§Known gaps lines 174–344, §Frontier lines 346–859, Round26/27/28/29/30 frontier
dispositions lines 861–952), `SCORECARD.md` (§Planned round 24–31, §Round 24–30
verdicts), `corpus/lessons/round-{24,25,26,27,28,29,30}.md` (spot-check intake tables,
mistakes, carried rows), `corpus/lessons/round-30-verifier-spotcheck.md:162-205`
(routed D1–D8 + carried list), `PROVINCE.md`. No files edited; report written once here.

## Inventory of open items (excluding quote-reopen surface)

Excluded as quote-reopen-owned (per target): L0 fetch-scope question; pages without a
`<head>` start tag; 2xx challenge pages; PDF sources; prefix/suffix disambiguation;
resolver time inside `DEADLINE`; IPv6; per-hop address provenance; TLS harness case;
surviving mutants (MutHeadNoText, verdict-order/script-head/case-insensitive);
uncancelled hop timers; resolver/dial time outside DEADLINE.

| # | Open item | Source pointers | R31 C1/C2 touches? | Size |
|---|---|---|---|---|
| 1 | Receipt identity for mission acceptance (receipt-backed rounds 0/10; operator target ≥100) | README Known gaps 330-333; Frontier 831-833; SCORECARD R1/R25 | no | L (operator/integrator-owned) |
| 2 | Non-author admit/reject spot-check (discernment unchanged) | README Known gaps 334-336; Frontier 831 | no | M (outside reviewer, process) |
| 3 | Frozen-replay conformance | README Frontier 831-833 | no | L (operator-owned) |
| 4 | Concurrent `--json` manifest appenders (`flock` unlanded; blank-line race 1/3 @16 writers r24, 2/6 seeded r25) | README R24 ¶846-847; R26 dis 875; lessons/round-25.md Spot-check row 1; SCORECARD Planned25 debt list, Planned26 item 1 | no | M (1 claim + counter/fixture; design already pre-registered) |
| 5 | Filesystem races / TOCTOU family (probe-to-read window, stat-fail open, same-device binds stat-invisible, overlay roots, glob-expansion-before-refusal) | README R13/R14/R19 named limits; R26 dis 875; lessons/round-27.md carried row | no | M–L (several subclasses, splittable) |
| 6 | Parent-root legacy rechecks (9 entries flagged `META_RECHECK_ROOT_PARENT` info; criterion 13) | lessons/round-25.md Spot-check row 2; lessons/round-27.md carried row | no | S–M |
| 7 | Receipt gaps (r10 sixth-control body absent; withdrawn cuts; r29 D5 wall-time disclosure) | README Known gaps 296-306; lessons/round-26.md; lessons/round-29.md D5 | no (round-31 D1–D8 repair other outside-check receipt defects) | S–M |
| 8 | Span ↔ named-pointer-line pairing (location binding; `A-r9.md:50` class) | README Known gaps 257-261; R26 dis 876; lessons/round-25.md M-6 ("source/span pairing remains uncovered"); claims.md C1 surface | **C1 touches (partial)**: binds the JSONL `line` field only; the in-record `## Claims` table `pointer`/`span` columns and `verify`-mode `path:N` pointers stay outside every gate check | M → residual S–M after C1 |
| 9 | Chain transitivity / entailment-level verification; exemption record-declared never verified; first-occurrence reporting; `nearest_line` heuristic | README Known gaps 324-328; lessons/2026-10-15-chain-hop-resolution.md | no | L (new-mode semantics) |
| 10 | Citation-chain fidelity (a resolved hop proves locator exists, not faithful relay; five-item per-hop comparison is manual) | knowledge/citation-chain-fidelity-r24.md; README R24 ¶842-849 | no | M (method → gateable check) |
| 11 | Sweeps depth: vacuous flip-conditions pass; recorded sweep command never executed; 0/0 CLEAN when no rejections/sweeps; non-local exempt-but-counted | README Known gaps 195-202; lessons/2026-10-16-sweeps-rejections-verdict-bearing.md | no | M |
| 12 | Integrity resolution depth: kind-blind (`claim_id` holding a source id resolves), case-sensitive, duplicates tolerated, lowercase/non-id shapes invisible, unscanned cells, companion-file ids unseen, exempt-token over-extraction | README Known gaps 203-214; knowledge/reference-integrity-r7.md | no | M |
| 13 | Omission semantics: fine-grained omission reporting, Chain-less case, absent-section-should-have-been-present, sweeps-with-only-rejections seam | README Known gaps 215-222; knowledge/verify-all-r6.md | no | S–M |
| 14 | Manifest never read back / no audit-trail guarantee; foreign lines preserved unvalidated | README Known gaps 223-228 | no | S–M |
| 15 | r8 baseline blind spots: exit-code-only regressions, behavior outside canonical invocation, oracle strength, per-row movement outside composed surface, timestamp-mask breadth | README Known gaps 229-244; SCORECARD Planned25 debt list | no | M |
| 16 | Boundary residuals: token-aligned shortening still passes; non-ASCII neighbours fail closed; `_` boundary by decision | README Known gaps 307-314 | no | S–M |
| 17 | Scope-screen limits: declaration-only detection, solo modes lack teeth, negations unparsed; `ai benchmark(s)` boundary; inflection gaps (bug bounties, dispatch mechanisms, llm evaluations); camelCase `llmbenchmark` | README R18 ¶687-693, R20 ¶746-748; SCORECARD Planned25 debt list | no | S–M |
| 18 | Denylist residual: pattern-list only; `.config-adjacent` non-hit by design; raw path-start vs canonical-target coverage | README R22 ¶799-802; knowledge/denylist-r22.md | no | S |
| 19 | Fenced-data-row `approved` suppression; CDATA/processing-instruction/other HTML constructs outside record contract (parser not a Markdown renderer) | README R17/R20 paragraphs; SCORECARD Planned25 debt list | no | S–M |
| 20 | Archive conversion custody limits: chain stops at export; absent section in archive ≠ "no"; `text` cells paraphrase; conversion authors structure | README Known gaps 251-269; lessons/2026-10-16-verifying-conversion-not-original.md | no | M (partly by-design) |
| 21 | Class-evidence breadth: controls are one-existence-proof-per-class; no multi-defect interaction; refusal classes not exercised at archive scale; false-sweep `hits=`/`listed=` are directory-at-runtime values | README Known gaps 276-295; lessons/2026-10-16-archive-scale-controls-and-ledger.md | no | M |
| 22 | SOURCES queued rows unmined (S008–S012, S017, S018; also queued S021–S024, S026–S028) | README R24 ¶848-849; corpus/SOURCES.md | no | S–M (method-note admission) |
| 23 | Path-denylist surface: R27 C3 complete-path-vs-prefix clause conflict; S045 ancestor over-refusal; Round-28 C1 not achieved/unprovable | SCORECARD R28/R29/R30 Planned; lessons/round-29.md routed 4 | no | M (blocked: parent approval withheld) |
| 24 | Metadata-screen depth: key presence and date shape only, not criterion-6 compliance; the criterion-6 verifier candidate (cited S-id exists + mined + used-by + what-was-checked text) | SCORECARD Planned26 item 3; knowledge/metadata-screen-r25.md named limits | no | M (design already pre-registered) |
| 25 | Registry grammar limits (first-named-line-pair scanner: fenced/indented/commented examples, duplicate header names/keys, body-row header shapes, escaped pipes, adjacent tables, Unicode whitespace) | lessons/round-27.md CriticRegistryGrammar carried | no | M |
| 26 | Source mutability / S025 quote quality (mutable URL/version drift; S025 403 gate; recheck limit) | lessons/round-26.md FSourceRejection; lessons/round-27.md carried | no | S |
| 27 | Operability score construct redesign (narrow 3/10 archived-input metric; M-11 "the narrow 3/10 construct itself is queued r25"; re-derived 3→3 ever since) | lessons/round-24.md M-11; SCORECARD R24/R25/R30 verdicts | no | M |
| 28 | 8 unasserted finding IDs (selftest/verdict surface does not assert every defined finding) | SCORECARD Planned25 debt list | no | S |
| 29 | Secret-scan source coverage (secret values in records → kagi; shape-only here) | SCORECARD Planned25 debt list; PROVINCE.md | no | S |
| 30 | bash-3 portability (scripts use bash 5 features) | SCORECARD Planned25 debt list | no | S |

## Proposed candidates for a "Planned — round 32" row

Three distinct-axis candidates, each with an existing pre-registration or named-debt
pointer (no new design needed), falsifiable before→after, sized ~M:

1. **Coverage — claims-table pointer-column location binding.** Close the residual of
   C1's edge class: bind the in-record `## Claims` table `pointer`/`span` columns
   (`path:N` form) to the span's occurrence line — the `A-r9.md:50` class C1 leaves
   open (README Known gaps 257-261; R26 dis 876). Natural continuation of this round's
   held ground; counter style mirrors `c1-count.py`.
2. **Operability (lowest scored axis) — serialize cooperating `--json` appenders**
   across the EOF probe plus append (`flock` candidate; ≥10×16-writer same-precondition
   runs, zero blank/invalid lines). Carried since r24, pre-registered as Planned26
   item 1 (SCORECARD 1373-1376; README R24 ¶846-847; lessons/round-25.md row 1).
3. **Calibration — criterion-6 metadata verifier** (not the r25 syntax screen): each
   cited S-id exists, is mined, used-by names the entry, and what-was-checked text is
   present; freeze r24+ population and semantic negative controls before data
   (SCORECARD Planned26 item 3; knowledge/metadata-screen-r25.md limits).

Items deliberately not proposed: #1/#2/#3 (operator-owned), #23 (parent-blocked),
quote-reopen surface (out of target), semantic/truth axes (out of province by design).
