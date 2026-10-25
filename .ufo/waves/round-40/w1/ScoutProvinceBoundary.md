# ScoutProvinceBoundary — chousa round 40, wave 1

**Assigned attack:** Read chousa `PROVINCE.md` and relevant sibling province boundaries; determine whether the receipt-reconciliation work remains within deep-research method and identify any cross-domain evidence to route.

**Read-only:** no production file edited; only this report written.

## Verdict

**IN-PROVINCE, with two cross-domain items to route out (one explicit, one advisory).** Every committed round-40 artifact — the R1 receipt-integrity predicate, the active manifest, the three regenerated c1 receipts, the R2–R5 disposition record and both frozen counters — exercises claim-vs-source verification, evidence-set curation, and calibration of the lane's own self-assessments against committed bytes. Each of those is a verb `PROVINCE.md` **Owns** (`PROVINCE.md:5-8`). No clause of `PROVINCE.md` **Refuses** (`PROVINCE.md:10-15`) is absorbed by this work; nothing becomes a credential-, model-quality-, bounty-, or orchestration-domain claim.

## Evidence read (commands and observations)

| Command / read | Observation |
|---|---|
| `read chousa-shokunin/PROVINCE.md` (17 lines, whole file) | Owns: question framing, source hierarchy, citation chaining, **claim-vs-source verification**, search taxonomy, external-target approval table, lane corpus/gates. Refuses: kasegi (bounty), kengaku (model quality), kumitate (orchestration/dispatch/lifecycle), external live-target without approval, secret values (kagi custody; shape-only). Closing rule: "Out of province → report, never absorb." |
| `read corpus/evidence/round40/claims.md` | Frozen C1/P1 = six-row manifest receipts verify against committed gate/counter/verifier/expectation bytes; frozen C2/P2 = four routed r39 findings R2–R5 dispositioned from committed evidence. Separability note: counters never read each other's surfaces. |
| `read c1-count.py`, `active-r39-receipts.tsv`, `c2-count.py` | c1 counter re-runs committed verifier per manifest row, expects `VERIFY: ok`; c2 counter re-derives each disposition from committed sources (git `ls-tree`/`ls-files` history counts, role Counter over `w1-spec.json`/`w1-plan.json`, string evidence in committed claims/lesson/SCORECARD/report). |
| `read round39/verify-receipts.py`, three regenerated receipts, `expectations.jsonl` | Receipts bind sha256 of gate/counter/verifier/expectation/self bytes plus scenario rows; expectation rows are gate-output facts (`drift_line`, `pin_rc`, `echo_lines`). No credential material. |
| `read routed-defect-dispositions.json`, `round-39-verifier-spotcheck.md` (R1–R5), `claims.md:194-200` errata | R2/R3/R5 corrected, R4 not-reproduced with the spec-vs-spot-check conflict preserved verbatim rather than rewritten. |
| `head -12` on sibling PROVINCE.md: kagi, kumitate, kake, kasegi, kengaku, mado, kotodama, tameshi, mori | kagi = secrets/vault custody; kumitate = orchestration/dispatch (Adjacent: "Research method → chousa"); kake = web properties (Adjacent: chousa owns method); kasegi = bounty/security research; kengaku = LLM eval; tameshi = honest-check/mutation-fixture method; mori = fleet/wave observability. |
| `grep -iE 'token|secret|password|api_?key|PRIVATE'` over `corpus/evidence/round40/` + `round39/receipts/` | **0 matches** — no secret-shaped content in any receipt or disposition. |
| `read .ufo/waves/round-40/DISPATCH-README.md`, `corpus/lessons/round-40.md`, `corpus/knowledge/receipt-expectation-digests-r40.md` | Lesson discloses "wave prepared for the orchestrator, not dispatched"; knowledge entry limits digest identity to bytes (not authorship/truth); README:1038 calls round-40 ground "evidence-provenance method, not a new gate mode or claim-truth proof." |

## Per-boundary findings

1. **Digest binding is method, not secrets.** The verifier's sha256 use is evidence input-binding; the knowledge entry (`receipt-expectation-digests-r40.md:17-19`) explicitly denies authorship/truth claims. Nothing approaches kagi custody; the secret grep is empty, consistent with the SKILL.md:62 "shape-only" clause.
2. **R4's role counting stays claim-vs-source.** `c2-count.py:72-79` counts `role`/`agent` fields in committed `w1-spec.json`/`w1-plan.json` to check whether an *outside* assertion (the r39 verifier spot-check's "reviewer 8 / revenger 0") reproduces. That is verification of a claim about committed artifacts — the work Product Type `PROVINCE.md` owns — not dispatch, lifecycle, or wave mechanics, which are kumitate's.
3. **Supersession/receipt-set curation is citation-chaining practice.** R2's "committed despite 'not committed' wording" is a claim-vs-source mismatch (committed bytes vs prose), corrected append-only — standard chousa erratum discipline, same idiom as r39's Errata chain.
4. **Fleet-read is citation, not absorption.** `c2-count.py` reads `fleet:.ufo/reports/round-39/chousa.md` and mori's jurisdiction (`.ufo` settlement state, lane counters) only as committed evidence sources; mori's own PROVINCE cedes dispatch mechanism to kumitate and nothing here adjudicates fleet observability.
5. **Mutant/env fixtures are provenance evidence, not security research.** `c1-mutenv-*` receipts measure `PATH`/`bash` provenance drift; they are gate-behavior expectations, not vulnerability or bounty material → kasegi untouched.

## Cross-domain evidence to route

- **R4 unresolved contradiction → kumitate (dispatch/agent-lifecycle) and/or mori (wave observability), never absorbed here.** The r39 committed `w1-spec.json` + `w1-plan.json` + report agree reviewer 6 / revenger 2; the non-author spot-check asserts reviewer 8 / revenger 0. `routed-defect-dispositions.json:20-30` correctly preserves the conflict rather than inventing a spec correction, but the question "which artifact is wrong" concerns how the wave spec/plan were *generated* — dispatch-mechanism provenance. Chousa has no authority to adjudicate spec-authorship; the row must stay routed, not resolved in-lane.
- **Advisory adjacency → tameshi.** `verify-receipts.py` (strict-schema receipts, named-refusal digests, mutation-test items `MutateExpectDigest`/`MutateGateDigest`/`MutateVerifierSubject` in `w1-spec.json`) is honest-check fixture craft. Lane-scoped it remains chousa's own gate (Owned), so nothing routes today; if anyone generalizes "receipt verifier + mutation control" as reusable method beyond chousa, that claim is tameshi's province.
- **Nothing routes to kagi, kasegi, kengaku, kake, mado, kotodama.** Empty secret scan; no credential custody, bounty scope, model-quality claim, web property, compositor, or worldbuilding surface appears anywhere in the r40 evidence set.

## Remaining unknowns / limits of this audit

- I did not re-execute `c1-count.py`/`c2-count.py` (leaf scout scope: committed artifacts audited by inspection; executor seats run the commands). The in-province verdict rests on artifact contents, not a fresh run.
- The R4 artifact-provenance route is named but owner-adjudication (kumitate vs mori) is left to the integrator; chousa's disposition correctly limits itself to "not reproduced from committed artifacts."
- Whether `git ls-tree` history reads inside `c2-count.py` should be declared a "lane-fallback" surface (kagi-style) is a calibration nuance, not a boundary breach — committed-history re-derivation is chousa's normal source check.

## Confidence

**High** on the in-province verdict: the Owned list verbatim covers every operation performed, and the Refuses list is checked clause-by-clause with negative scans. **Medium** on the routing severity for R4 — the evidence is clearly out-of-province for adjudication but correctly *held* as a preserved conflict inside chousa's evidence record, which is itself in-province behavior ("report, never absorb" is satisfied by routing, not by resolving).

**Tool installs:** none. No pacman transaction attempted (host-wide pause honored); all reads used provided tools.
