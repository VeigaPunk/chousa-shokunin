# SCORECARD.md — round-2 draft sections (parent-owned file; [PARENT] binds)

<!-- SCRIBE DRAFT. Verdict vocabulary only: improved / unchanged / harmed /
     unprovable-but-better. No scalar scores. Measured at frozen gate
     tools/research-gate.sh sha256 03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0,
     lane HEAD 6344569; evidence corpus/evidence/claims-r2-20261015T233027Z-*.log. -->

Round-1 sections stay as written. These are the round-2 sections to append, plus
the admission/`Planned` refresh.

## Round-2 per-axis verdicts

Measurements: frozen gate sha256
`03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0`; receipts
`corpus/evidence/claims-r2-20261015T233027Z-{fixture,gate,live,selftest}.log`
(corrected set; the 232752Z selftest line is the superseded quota false
negative); note `corpus/knowledge/claim-verification-r2.md`.

| Axis | Verdict | Evidence boundary |
|---|---|---|
| coverage | improved | The gate now checks claims against their cited sources. Before: structure-only, `claims=0` checked on the 17-claim fixture. After: 17/17 pre-registered claims over all three archived inputs checked with per-claim verdicts (13 supported, 2 contradicted by structural marker, 2 unsupported near-misses), plus refusals for external/session/out-of-corpus sources. Boundary: span byte identity inside the corpus roots, not semantics — the `claim` label is never compared with its span |
| operability | improved | New `verify-claims` mode runs end-to-end under the preserved exit contract (CLEAN 0 / DRIFT 1 / setup 2, stdout empty on setup); selftest 20 → 30 cases all PASS; r1 verify stdout on A/B/C and intake byte-identical. Boundary: the round-1 capped observable (`VERDICT_BEARING_EXPORTS=3/3`) is unchanged. [PARENT: keep `improved` (new runnable mode is the gain) or set `unchanged` if only the capped 3/3 count is read — the evidence supports either reading] |
| depth | unchanged | No independently verified domain fact; fixture spans are byte controls, not adopted knowledge |
| freshness | unchanged | Archive pins re-checked at fixed revisions only; no new cross-revision drift detector |
| calibration | unchanged | Structural limits explicit (CLEAN iff every observed status equals its expectation; marker check is literal, not semantic); no non-author discernment |
| adjacency | unchanged | Foreign-province material (B03 numerals, rank/governance text) kept as near-misses/rejections, never absorbed |

## Round-2 learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | Net-new admitted entry `corpus/knowledge/claim-verification-r2.md` on ground the coverage map did not hold (claim-vs-source verification), plus a new gate edge class; `corpus/README.md` carries the coverage rows (note, fixture, lesson) |
| quality | unchanged | The new CLEAN is structural; no older admitted entry was reverified or superseded (precedent: round-1 operability improved with quality unchanged) |
| discernment | unchanged | No non-author admit/reject spot-check; no `QUALITY.md` criterion added |

## Admission and continuation (round-2 replacement text)

[PARENT: refresh the round-1 admission paragraphs after integration.]

Local axis result: coverage improved (the declared move); operability improved on
the new runnable mode; the other four axes unchanged; none harmed. No scalar
substitute, no promotion. [PARENT: adjust if the operability row is read as
`unchanged`.]

Mission acceptance is separate and remains blocked on the round-1 receipt
identity: the interactive launch has no authentic queue taskKey/expected receipt
bag, so no `task_…` value may be manufactured, no shape-only receipt counted, and
no Sighting marked complete. Receipt-backed verified rounds remain **0**; the
operator target remains at least 100. Routing for this wave was satisfied by the
operator's in-session direct dispatch; no Sighting was invoked.

Debt after round 2: receipt identity (integrator), scope-refusal finding IDs
(lane, future move), non-author spot-check (integrator/operator), frozen replay
gate conformance (lane, if required), fleet `/tmp` quota (environment) — see
`.ufo/round-2/goal-wave/report-draft.md` for owners and unblocks.

## Planned (round-2 refresh)

[PARENT: replace the round-1 `Planned` paragraph.] Round 2's pre-registered move
(claim-vs-source verification) has now run in the operator's in-session wave; the
routing precondition it waited on is satisfied for this wave, while receipt
identity remains open. Any next round must again declare its own falsifiable
single move and genuine scope before dispatch; do not rerun this round's wave.
