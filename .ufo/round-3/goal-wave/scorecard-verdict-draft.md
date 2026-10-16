# SCORECARD.md — round-3 draft sections (parent-owned file; [PARENT] binds)

<!-- SCRIBE DRAFT. Verdict vocabulary only: improved / unchanged / harmed /
     unprovable-but-better. No scalar scores. Measured at frozen gate
     tools/research-gate.sh sha256 67daf85e… (green + stable), lane HEAD
     0aa794d; fixture shas chain-r3.md 06115f2f…, chain-r3-broken.md
     b66222a1…, chain-r3.README.md 72dbee4e… (revised in-wave); note
     corpus/knowledge/chain-resolution-r3.md 9f16c7e7…. The report draft's
     debts section keeps the receipt-identity debt named. -->

Round-1/round-2 sections stay as written. These are the round-3 sections to
append, plus the admission/`Planned` refresh.

## Round-3 per-axis verdicts

Measurements: frozen gate sha256
`67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084` (identical
across 4+ samples; selftest PASS); fixtures
`corpus/fixtures/chain-r3.md` / `chain-r3-broken.md` (+ README); scribe
captures under `/home/vgpnk/.cache/chousa-r3/`.

| Axis | Verdict | Evidence boundary |
|---|---|---|
| coverage | improved | The gate now resolves each chain hop's citation. Before: hop checks were structural only — `verify` passes the round's own broken-anchor record CLEAN exit 0 (and a phantom `:999` hop passes at `03a33244…`). After: 22 real hops over the three archived inputs resolved with per-hop verdicts — `RESOLVED_HOPS=17/22` CLEAN (17 verified, 5 exempt), broken control `1/2` DRIFT with `CHAIN_ANCHOR_NOT_FOUND`. Boundary: anchor byte existence inside the corpus boundary, not semantics — cross-input hops are co-anchors (bytes present in the target, never authorship/endorsement), exempt hops counted but unproven |
| operability | improved | New `verify-chain` mode runs end-to-end under the preserved exit contract (CLEAN 0 / DRIFT 1 / setup 2, stdout empty on setup); selftest 30 → 40 cases all PASS with cases 1-30 byte-identical; `verify`/`verify-claims` outputs byte-stable on all pinned inputs; `VERDICT_BEARING_EXPORTS=3/3` and `VERDICT_BEARING_CLAIMS=17/17` unchanged. Boundary: the capped observables are unchanged; [PARENT: keep `improved` (new runnable mode is the gain) or set `unchanged` if only the capped counts are read — evidence supports either] |
| depth | unchanged | No independently verified domain fact; fixture anchors are byte controls, not adopted knowledge |
| freshness | unchanged | Archive pins re-checked at fixed revisions only; no new cross-revision drift detector |
| calibration | unchanged | Structural limits explicit (existence, not semantics; exempt ≠ verified; the record's own marking is the only exemption route); no non-author discernment |
| adjacency | unchanged | Foreign-province material kept as exemptions/rejections; zero network (no fetch primitive; URLs refused unopened); research corpus read-only |

## Round-3 learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | Net-new admitted fixtures + contract README on ground the coverage map did not hold (chain-hop resolution), plus new gate edge classes (`CHAIN_SOURCE_*`, `CHAIN_ANCHOR_NOT_FOUND`, `CHAIN_CITATION_INVALID`); `corpus/README.md` coverage rows [PARENT: verify landed before claiming the rows] |
| quality | unchanged | The new CLEAN is structural (anchor bytes); no older admitted entry was reverified or superseded (round-1/2 precedent) |
| discernment | unchanged | No non-author admit/reject spot-check; no `QUALITY.md` criterion added |

## Admission and continuation (round-3 replacement text)

[PARENT: refresh the round-2 admission paragraphs after integration.]

Local axis result: coverage improved (the declared move — chain-hop resolution
lands verdict-bearing); operability improved on the new runnable mode; the
other four axes unchanged; none harmed. No scalar substitute, no promotion.
[PARENT: adjust if the operability row is read as `unchanged`.]

Mission acceptance is separate and remains blocked on the round-1 receipt
identity: the interactive launch has no authentic queue taskKey/expected
receipt bag, so no `task_…` value may be manufactured, no shape-only receipt
counted, and no Sighting marked complete. Receipt-backed verified rounds remain
**0**; the operator target remains at least 100. Routing for this wave was
satisfied by the operator's in-session direct dispatch; no Sighting was invoked.

Debt after round 3: receipt identity (integrator, still open), round-3
artifact gaps if the `corpus/README.md` coverage rows and the
`corpus/evidence/README.md` index did not land (lane, integrate only what
landed), scope-refusal finding IDs (lane, future move), non-author spot-check
(integrator/operator), frozen replay gate conformance (lane, if required),
fleet `/tmp` quota (environment) — see `.ufo/round-3/goal-wave/report-draft.md`
for owners and unblocks. The fixture-README pin inconsistency found mid-wave
was corrected by its author in the revised README (sha256 `72dbee4e…`).

## Planned (round-3 refresh)

[PARENT: replace the round-2 `Planned` paragraph.] Round 3's registered move
(chain-hop resolution) has now run in the operator's in-session wave; the
routing precondition holds for in-session waves, while receipt identity remains
open. Any next round must again declare its own falsifiable single move and
genuine scope before dispatch; do not rerun this round's wave. Round 1's
registered debt (scope-refusal finding IDs) and the frozen-replay comparator
remain unimplemented and are the standing lane candidates.