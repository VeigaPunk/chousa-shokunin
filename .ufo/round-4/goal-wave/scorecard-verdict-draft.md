# SCORECARD.md — round-4 draft sections (parent-owned file; [PARENT] binds)

<!-- SCRIBE DRAFT. Verdict vocabulary only: improved / unchanged / harmed /
     unprovable-but-better. No scalar scores. Measured at the settled gate
     tools/research-gate.sh sha256
     6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2
     (4 identical 30 s samples before the after-state battery, sha re-checked
     around and after it), lane HEAD 09153d19871158380f64b6f58a14b6912aab676f;
     the before-state is the lane's round-3 gate 67daf85e…. Scribe captures in
     /tmp/chousa-scribe-r4/ (declared ephemeral, cleaned at end of run; the
     report draft quotes every value verbatim). [PARENT] marks parent-only
     bindings. The report draft's debts section keeps the receipt-identity debt
     named, per the mission contract. -->

Round-1/2/3 sections stay as written. These are the round-4 sections to
append, plus the admission/`Planned` refresh.

## Round-4 per-axis verdicts

Measurements: both revisions measured fresh-process by the scribe seat —
before: gate `67daf85e…` (lane HEAD `09153d1`); after: gate
`6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2`; fixtures
`corpus/fixtures/claims-r2.jsonl` / `chain-r3.md` / `chain-r3-broken.md`
unchanged; no round-4 wave fixture had landed at draft time.

| Axis | Verdict | Evidence boundary |
|---|---|---|
| calibration | **improved** | Before: the attack class passes — three truncated/glued variants of real corpus text close 5/5 CLEAN as claims and 4/4 CLEAN as chain quotes, and the round-3 truncated-anchor CLEAN (`…kiwami semantic`) reproduces (`RESOLVED_HOPS=2/2`). After: the same bytes fail in both modes (claims 2/5, chain 2/4, DRIFT exit 1) with the existing line-aware `nearest_line`/`context` reports; word-internal hyphen/apostrophe truncations (`ryu`, `jin'i`, `jin`, `AI`) refused; legitimate spans keep passing (punctuation-followed, line-edge, paren-bounded, slash-delimited) and match the pre-fix results; a same-bytes cross-mode matrix shows identical verdicts in both modes. Boundary: matching semantics only — no semantic support, source truth or external verification claimed; non-ASCII/undecidable edges fail closed |
| coverage | unchanged | Same claims/chain surfaces re-judged under the hardened rule; the four new selftest cases are generated-fixture coverage, not new corpus ground |
| operability | improved | Selftest 40 → 44 cases all PASS with the first 40 case lines byte-identical; both fixtures, the broken control, A/B/C (`VERDICT_BEARING_EXPORTS=3/3`) and the intake record byte-identical modulo `ts=`; exit contract 0/1/2 unchanged; the new cases exercise both modes end-to-end through the public CLI |
| depth | improved [PARENT: r3 precedent — its admitted scorecard credited the landed note under depth; the scribe's stricter reading would be unchanged, since no independently verified domain fact was added and fixture spans/anchors remain byte controls] | `corpus/knowledge/anchor-boundaries-r4.md` (`668c1d1f…`) documents the boundary class, both call sites and the exact residual classes (token-aligned shortening still passes; non-ASCII-adjacent edges fail closed; `_` is a boundary), and `corpus/lessons/2026-10-15-anchor-token-boundaries.md` (`5bd90e21…`) distils it; their pins match this seat's independent measurements |
| freshness | unchanged | Pins re-checked at fixed revisions only; no cross-revision drift detector |
| adjacency | unchanged | Zero network (fetch-primitive scan = 0 matches); research corpus read-only; boundary/refusal classes untouched |

## Round-4 learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| quality | improved | An earlier admitted CLEAN that rested on substring semantics is now correctly re-judged: the round-3 documented one-byte-truncated anchor `…kiwami semantic` closed `RESOLVED_HOPS=2/2` CLEAN at `67daf85e…` and reads `anchor-missing` / `RESOLVED_HOPS=1/2` DRIFT at `6b83705b…`, while the real anchor still verifies. The gate's own documented limit closed instead of being carried |
| expansion | unchanged | No new admitted fixture/contract README landed at draft time (the selftest's `lib/boundary.md` is a generated fixture). [PARENT: re-judge if a wave fixture lands before integration] |
| discernment | unchanged | No non-author admit/reject spot-check; no criterion added |

## Admission and continuation (round-4 replacement text)

[PARENT: refresh the round-3 admission paragraphs after integration.]

Local axis result: calibration improved (truncation/padding/glue games now
fail in both modes with the line-aware reports; legitimate spans and every
pinned fixture unchanged); operability improved on the selftest/CLI surface;
depth improved if the r3 precedent is followed and the landed note counts
[PARENT: else unchanged]; coverage/freshness/adjacency unchanged; none harmed.
No scalar substitute, no promotion.
[PARENT: adjust the axis cells if integration finds a landed artifact
disagreeing with a measured value, or if the gate moves past `6b83705b…`.]

Mission acceptance is separate and remains blocked on the round-1 receipt
identity: the interactive launch has no authentic queue taskKey/expected
receipt bag, so no `task_…` value may be manufactured, no shape-only receipt
counted, and no Sighting marked complete. Receipt-backed verified rounds remain
**0**; the operator target remains at least 100. Routing for this wave was
satisfied by the operator's in-session direct dispatch; no Sighting was invoked.

Debt after round 4: receipt identity (integrator, still open), round-4 artifact
gaps — landed: gate hardening, note, lesson; still missing at draft time: an
attack-class fixture + contract README, `corpus/evidence/*r4*` receipts,
SKILL.md and `corpus/README.md` round-4 rows (lane, integrate only what
landed) — the named boundary-class residuals (lane, decide whether any is worth
a future move), scope-refusal finding IDs (lane, future move), non-author
spot-check (integrator/operator), frozen replay gate conformance (lane, if
required) — see `.ufo/round-4/goal-wave/report-draft.md` for owners and
unblocks.

## Planned (round-4 refresh)

[PARENT: replace the round-3 `Planned` paragraph.] Round 4's registered move
(token-boundary hardening of claims spans and chain quote anchors) has now run
in the operator's in-session wave; the routing precondition holds for
in-session waves, while receipt identity remains open. Any next round must
again declare its own falsifiable single move and genuine scope before
dispatch; do not rerun this round's wave. Standing lane candidates: the named
boundary-class residuals (ASCII-punctuation truncation, non-ASCII-adjacent
fail-closed edges, the substring-only marker co-occurrence), scope-refusal
finding IDs, and the frozen-replay comparator.