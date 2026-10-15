# chousa — round 1: inherited survey integration and CLI operability

## Work performed

- Reconciled the interrupted round rather than advancing a launch counter. Starting lane HEAD was `34774a1777d4058ca8c2b4456ce2e6ccee9e24c5`; existing dirty gate/index/log and untracked scorecard/intake/lesson/pins were retained. Plan: `.ufo/plans/round-1-interactive-20261015T050057Z.md`. Evidence: `LOG.md:145-189`.
- Revalidated the preserved `Shokunin12hP5ChousaR1` spec through canonical `ufo-swarm-wave.mjs plan`: exit 0, spawn 32, resume 0, width 32. The original rendered `run.json`, response saying “Spawned 32,” 32 assigned members and all 32 report files are present. Distinct prompts/names and leading Godspeed prefixes each count 32. Local evidence: `.ufo/evidence/round-1/wave-plan.json` and `wave-reconciliation.json`; the latter pins every member report and records its disposition. **No new task call or second round-1 wave.**
- Read dispatch-time route metadata: content `m_composer`, audits `m_grok`, both connectors `m_antigravity`. The preserved registry omits the actual `-2` suffixes for CorpusMap, FindingIds and GateRegistryRow; local reconciliation records the response IDs without mutating shared artifacts. Later nine-seat calls described in LOG are extra advisory evidence, not replacement dispatch or native judgment. Spawn-time pending status is not represented as current liveness.
- Integrated the single operability improvement: `emit_finding` records severity effects then returns success, allowing the real CLI to reach its summary under errexit (`tools/research-gate.sh:71-82`). Fixtures invoke fresh public CLI processes (`:564-597`), covering normal/strict informational findings and continuation to structural findings. Corrected the inherited lenient fixture filename mismatch before acceptance. Evidence: `LOG.md:145-189`, committed gate below.
- Ran the local gate and actual archived-export/intake CLI paths. Input hashes matched committed expected pins before archive evaluation. Complete argv/stdout/stderr/verdict lines/exits: `.ufo/evidence/round-1/acceptance.json` and `acceptance.txt`; final integrated intake recheck: `final-intake.json`. These are real command outputs, not configuration or expected-output claims.
- Integrated one locally sourced method-form intake and the existing lesson, added opening source/recheck metadata, retained rejected domain material and unresolved external hops, and appended corrections rather than erasing inherited observations. Remeasured bounded heading/URL/search-label sweeps (`source-sweeps.json`). CLEAN is structural acceptance only; no external semantic source or live provenance is verified. See intake `:179-213`, lesson `:149-200` and `LOG.md:191-266`.
- Updated the single SKILL gate registry, actual corpus coverage map, all six per-axis verdicts and three learning trends. Kept QUALITY and PROVINCE unchanged; no promotion or non-author spot-check is claimed. `SKILL.md:61-85`, `SCORECARD.md:36-76`, `corpus/README.md`.
- Investigated the receipt boundary using only launch/wall metadata and canonical receipt code, not native transcript bodies or environment values. The direct interactive launch supplies no authentic taskKey/stored expected receipt bag; its configured canonical queue is absent. Evidence and exact unblock: `.ufo/evidence/round-1/receipt-blocker.json`. No fake mint or Sighting completion.

## Landed changes

Work HEAD when this report was written: **`cfb803a20ba6bf29ba977248bab41b939c7f2ea9`**. No cited commit was amended.

| Commit | Landed work | LOG connection |
|---|---|---|
| `31b46832e56a7f095092a4a6d62b74bfaf6933e8` | Verdict-preserving finding emitter, real-CLI regression harness, retained scorecard/input pins, WWKD plan and complete inherited-wave reconciliation | `LOG.md:145-189`, interactive integration entry |
| `cfb803a20ba6bf29ba977248bab41b939c7f2ea9` | Measured acceptance outputs, final intake and lesson with append-only errata, source sweeps, corrected skill/index/scorecard, explicit receipt-prerequisite evidence | `LOG.md:191-266`, local acceptance/corpus/receipt entry |

Both commits carry `chousa-shokunin <chousa@shokunin.local>`. No push. Native session files under `.ufo/interactive-sessions/` are intentionally excluded; no sibling/source/global configuration/fleet-ledger/shared-report writes were made. This report is lane-local as required by the current dispatch, not a shared fleet report.

## Before → after measurements

**One axis move: operability.** The known baseline at `34774a1777d4058ca8c2b4456ce2e6ccee9e24c5` is the previously executed `VERDICT_BEARING_EXPORTS=0/3` in `LOG.md:70-86,117-143`: each archive exited 1 without stdout/verdict. That reported failure was not rerun merely to confirm it.

After: committed gate `31b46832e56a7f095092a4a6d62b74bfaf6933e8`, script SHA-256 `08843552378071929c8b6abcd50be6613365691cfae4bf0d74fb03d86eb5b46e`. Exact counting command remains `SCORECARD.md:29`; L1 archive results satisfy its exit/summary predicate, **3/3**. Score 0 → 3 is deliberately capped by those three inputs, not an overall expertise score.

Full verdict lines and exits (raw commands/output retained in acceptance artifacts):

```text
bash tools/research-gate.sh --selftest
RESEARCH_GATE_SELFTEST: PASS (20 cases)
exit=0

verify ../research/deep-research-2026-09-28/A-shokunin-tradition.md --root ..
RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)
exit=1

verify ../research/deep-research-2026-09-28/B-multiagent-knowledge.md --root ..
RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)
exit=1

verify ../research/deep-research-2026-09-28/C-rank-taxonomy.md --root ..
RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)
exit=1

verify corpus/knowledge/archived-export-intake.md --root ..
RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=8 chains=8 claims=9 negatives=2 rejections=10 approvals=3)
exit=0
```

Archive content pins: `corpus/evidence/round-1/expected.json`, independently checked before invocation. Final integrated intake SHA-256: `33deaf93cec381509604db84e1b9c44d8ab3020998bf103eea7b720203fb62ec`; `final-intake.json` records its actual recheck after metadata/errata integration. The script was not changed by the later documentation commit.

The three archives correctly remain DRIFT: making a diagnostic emitter non-fatal does not make malformed research records CLEAN. Selftest also observes normal info exit 0, strict info exit 1, secret no-echo/session refusal, and setup exit 2 with no stdout verdict.

The actual knowledge/lesson inventory is two files, one each: `functions.glob` pattern `corpus/knowledge/*.md;corpus/lessons/*.md`. The new knowledge entry holds method-form observations, not externally verified terminology, ranks, benchmarks or provider/session facts.

## SHONEN

The checklist file remains unchanged; these are author assertions only, never promotion marks.

- [~] Decision table/error patterns/checklist are present at `SKILL.md:13-59`; hierarchy remains explicitly lane-authored/proposal where independently unsupported (`:23-31`). A non-author has not checked the promotion box.
- [~] Bounded end-to-end local intake was prepared, run through the actual CLI and handed off with full output: `LOG.md:191-266`, intake note and `final-intake.json`. It does not claim external semantic verification or completed mission acceptance.
- [~] Written commands were executed at the public entrypoint; `SKILL.md:61-85`, `acceptance.json` and the intake opening recheck. No independent agent-without-oral-context review is claimed.
- [~] PROVINCE remains accurate; foreign rank/model/orchestration findings are kept as rejections or pointers, not absorbed. The absent scope gate IDs remain named debt rather than a false executable-boundary claim.

## Per-axis and learning verdicts

| Axis | Verdict | Evidence boundary |
|---|---|---|
| operability | improved | 0/3 → 3/3 verdict-bearing archives; CLI selftest and final intake pass |
| depth | unchanged | No independently verified domain fact/broader expertise measurement |
| coverage | unchanged | Supporting specimen only, no measured province fraction |
| freshness | unchanged | Changed surface rechecked; no new drift detector |
| calibration | unchanged | Limits/debt explicit; no outside discernment or promotion claim |
| adjacency | unchanged | Existing boundary retained; foreign content not absorbed |

Learning: **expansion improved** (new held intake form/coverage row); **quality unchanged** (no older admitted knowledge entry reverified/superseded, no semantic gain from CLEAN); **discernment unchanged** (non-author admit/reject check absent). These are separate verdicts, not a scalar.

Local axis result: one improved, none harmed. No canonical Rust judgment is claimed. The prior fleet report records red Phase 0 contract-sync/self-iter; those reported failures were not rerun or repaired here. The initial interactive plan's round-1 route-blocker assessment is explicitly superseded: preserved dispatch-time metadata resolves this round, current defaults affect only a new wave.

## Debt, cross-domain handoff and admission

| Debt | Owner / concrete unblock |
|---|---|
| Applicable receipt identity absent | Fleet integrator binds this existing mission/identity to an authentic queue taskKey and stored prompt/config expected digests, uses this committed report as reportPath, mints with canonical create-receipt --out, validates --iterate against all six expected fields. Do not invent task_ values or relaunch another L1. `receipt-blocker.json` is not a receipt. |
| Current defaults cannot realize a new wave's route contract | Host/operator-owned bindings: content executor/scribe → @m_composer; audit/review/scout/critic/sentinel/revenger/mutation-tester → @m_grok; connector → @m_antigravity with @m_zfl fallback. Existing global roles instead select m_mid/m_strong/m_fast; the existing launch overlay has no role overrides. No lane routing change was made. |
| Refused-province gate IDs never landed | Future lane-owned single move: implement the catalogue's three scope findings with symmetric warn/exit-1 fixture evidence, including SCOPE_ORCHESTRATION_ABSORBED. Current documentary refusals are not executable enforcement. |
| Non-author spot-check missing | Integrator/operator samples at least one admit and one reject, records agree/disagree with reasons in the lesson; until then no discernment improvement/promotion. |
| No separate frozen replay gate | Expected archive digests/verdicts are persisted and L1 compared them. If stronger frozen-run gate conformance is required, a later lane move must ship a rerunnable pin-verifying comparator against committed inputs; this round does not claim one. |

Cross-domain evidence stays a report, never a fix: native Phase 0/dispatch/receipt machinery → kumitate/fleet integrator; general verification pattern → tameshi as an unconfirmed candidate; model-quality content → kengaku as export-unverified pointers only; credential custody → kagi without any value. No host/source/package remediation or protected Devin-owned lane was touched.

The current mission is progressing by owned commits and measured output after its recorded launch; this is not a silent-lane or fleet-wide liveness judgment. The stopped headless worker's launch counter was not promoted into a completed-round count.

## Fresh-session continuation

`.ufo/continuations/round-1.json` binds this report and work HEAD for the integrator. Current local round 1 work is integrated; **mission acceptance is blocked on authentic receipt binding**. No receipt was minted/validated and no Sighting complete command was invoked. Receipt-backed verified completed rounds proven here remain **0**, pending integrator acceptance; operator target remains **at least 100**. This is not saturation, an arbitrary stop, or a claim of three blocked rounds.

Once applicable receipt acceptance and authorized scheduling are available, release one fresh session for round 2. Its candidate single move is the explicitly authorized local-only claim-verification fixture with agreeing, disagreeing and silent sources. It must declare its own measurable delta and genuine 32-scope wave before a new dispatch; do not rerun round 1's completed wave or start a second actual round in this session.
