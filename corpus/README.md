# chousa-shokunin — corpus

## Coverage map

| Note | Holds | Sources |
|---|---|---|
| `lessons/round-1.md` | Round-1 gate lesson: real-CLI vs function-under-`set +e` entrypoint gap behind `VERDICT_BEARING_EXPORTS=0/3`, with the gate's candidates/admitted/rejected and the spot-check status | baseline commit `34774a1`; `LOG.md:72-83`; `SCORECARD.md:29`; anchors re-derived from `tools/research-gate.sh` sha256 `e8f07a06…` |
| `knowledge/archived-export-intake.md` | One filled research-record specimen: pinned archive identity, scoped local observations, unresolved external hops, kept rejections, and explicit semantic-verification limits | note opening metadata and integration errata; `.ufo/evidence/round-1/acceptance.json`; `final-intake.json` |
| `knowledge/claim-verification-r2.md` | Round-2 note: `verify-claims` mode design (CLI + JSONL schema, fail-closed source boundary, verbatim-span check, structural marker convention), honest limits, receipts and open items | note metadata (gate sha `03a3324455…`); `fixtures/claims-r2.README.md`; `evidence/README.md` and `evidence/claims-r2-*.log` |
| `knowledge/chain-resolution-r3.md` | Round-3 note: `verify-chain` mode design (CLI + hop citation grammar, `heading`/`quote`/`line` anchors, fail-closed source boundary, exempt-but-counted statuses, per-hop verdicts + `RESOLVED_HOPS=N/M` under the CLEAN/DRIFT/exit contract), what anchor existence does not establish, receipts and open items | note metadata (gate sha `67daf85e…`); `fixtures/chain-r3.README.md`; `evidence/README.md` and `evidence/chain-r3-*.log` |
| `fixtures/claims-r2.jsonl` | Pre-registered 17-claim span fixture (13 supported / 2 contradicted / 2 unsupported) whose spans are verbatim bytes of the three archived inputs, with fixed expected verdicts and an independent byte-check | the three archived inputs at fleet commit `0863746e…`; sha256 pins and provenance table in `fixtures/claims-r2.README.md` |
| `fixtures/chain-r3.md` + `chain-r3-broken.md` | Pre-registered chain-hop pair built from real chains in the three archived inputs: a 22-hop positive control (17 resolved / 5 exempt → `RESOLVED_HOPS=17/22`, CLEAN) and a tampered 2-hop control (1/2, DRIFT, `CHAIN_ANCHOR_NOT_FOUND`); the round-1 hole live — `verify` closes both CLEAN, exit 0 | the three archived inputs at fleet commit `0863746e…`; sha256 pins, hop provenance table and the gate-free byte-check in `fixtures/chain-r3.README.md` |
| `lessons/2026-10-15-claims-span-fidelity.md` | Round-2 lesson: span fidelity is not claim truth — the unchecked `claim` label, strace-measured bounds (no fetch, fail-closed refusals), byte-stable r1 behavior, named debt | gate sha `03a3324455…`; probes summarized in the note; `evidence/claims-r2-*.log` |
| `lessons/2026-10-15-chain-hop-resolution.md` | Round-3 lesson: `RESOLVED_HOPS`/chain CLEAN counts anchor existence only — a numeral tamper drifts; URL and out-of-corpus sources are refused unopened; exemption is record-declared and never checked (a marked hop can hide a resolvable citation); `nearest_line` is a heuristic; carried cosmetic banner item | gate sha `67daf85e…`; probes summarized in the lesson; `evidence/chain-r3-*.log` |

Count: 6 entries, three knowledge notes and three lessons — `functions.glob`
pattern `corpus/knowledge/*.md;corpus/lessons/*.md`, 2026-10-15. Fixture and
evidence files are coverage-listed but not additional knowledge entries.

## Round-1 evidence

- `evidence/round-1/expected.json`: archive content digests and expected CLI verdicts.
- `../.ufo/evidence/round-1/acceptance.json`: committed gate revision, all full CLI outputs/exits, and draft-intake digest.
- `../.ufo/evidence/round-1/final-intake.json`: final integrated note's structural recheck.
- `../.ufo/evidence/round-1/wave-reconciliation.json`: all 32 preserved member report hashes, routes, runtime-ID errata and integration dispositions.

## Round-2 evidence

- `evidence/README.md`: index of these receipts with pinned gate/fixture shas and a self-contained re-run recipe.
- `evidence/claims-r2-20261015T233027Z-live.log`: r1-gate before-state on the claims file; the frozen fixture run (`VERDICT_BEARING_CLAIMS=17/17`, `RESEARCH_GATE: CLEAN`, exit 0); four negative controls (tampered span, external URL, out-of-corpus path, contradicted-without-marker), each exit 1.
- `evidence/claims-r2-20261015T233027Z-fixture.log`: fixture inventory, pinned inputs, and two independent byte-checks (`bad []`; span check `ok=17 mismatch=0`).
- `evidence/claims-r2-20261015T233027Z-gate.log`: round-1 regression at the frozen gate — A/B/C exits and outputs byte-identical to the r1 baseline; `VERDICT_BEARING_EXPORTS=3/3`.
- `evidence/claims-r2-20261015T233027Z-selftest.log`: `RESEARCH_GATE_SELFTEST: PASS (30 cases)`, exit 0; first 20 case lines byte-identical to the r1 baseline (run under a `TMPDIR` scratch while the host `/tmp` quota was intermittent).

## Round-3 evidence

- `evidence/README.md`: index of both receipt sets (round 2 and round 3) with pinned gate/fixture shas and self-contained re-run recipes.
- `evidence/chain-r3-20261015T235623Z-live.log`: before-state on the shipped r2 gate (both chain records CLEAN under `verify`, exit 0 — the tampered control's anchor-missing hop passes structurally); live `verify-chain` (positive `RESOLVED_HOPS=17/22` CLEAN exit 0; broken `1/2` DRIFT exit 1 with `CHAIN_ANCHOR_NOT_FOUND`); four negative controls (appended-byte anchor tamper `semanticsX` → 16/22 DRIFT; out-of-corpus `/etc/hostname` and external URL refused crit, never fetched, 16/22 DRIFT each; an existing-anchor hop re-marked `unresolved` stays exempt but counted, 16/22 CLEAN); zero network (0 socket/connect syscalls); r2 `verify-claims` stdout byte-stable.
- `evidence/chain-r3-20261015T235623Z-selftest.log`: `RESEARCH_GATE_SELFTEST: PASS (40 cases)`, exit 0; case lines 1–30 byte-identical to the r2 selftest.
- `evidence/chain-r3-20261015T235623Z-gate.log`: round-1 regression byte-identical to the frozen baseline (A/B/C each exit 1 with one DRIFT summary; `VERDICT_BEARING_EXPORTS=3/3`).
- `evidence/chain-r3-20261015T235623Z-fixture.log`: fixture inventory and two independent gate-free checks (README byte-check `17/22 bad_hops=[]` and `1/2 bad_hops=['2']`, exit 0; the seat's record checker success, exit 0).
- An earlier cut (`chain-r3-20261015T235411Z-*`) was superseded and removed in this wave: its fixture log recorded a checker `FAIL` summary and a quote-truncation control that still resolved (substring containment). The standing cut re-derives both cleanly; references to the removed names are historical samples, not standing receipts.

## Known gaps

- CLEAN is mode-dependent, not semantic: `verify` checks record structure (r1);
  `verify-claims` checks byte-span identity plus a declared marker (r2);
  `verify-chain` checks that each unmarked resolved hop's source canonicalizes
  under the boundary and its `heading`/`quote`/`line` anchor occurs in the
  target (r3). None of the three proves semantic support, location binding,
  uniqueness or the source's own truth; chain CLEAN additionally does not prove
  agreement (hop 6 resolves across disagreeing statements) or authorship
  (cross-input hops are co-anchors). No original external source was fetched
  and none may be.
- The mode reads `id/source/span/expect[/marker]` only; the `claim` sentence is
  never compared with its span, so a claim label can assert the opposite of its
  span and still close CLEAN (`lessons/2026-10-15-claims-span-fidelity.md`).
- Round-3 chain checks are single-hop, single-target, text-only, and report
  first occurrence; transitivity and entailment-level verification remain
  unbuilt, the `verify-claims` `claim` label stays unchecked, and exemption is
  the record's own declaration, never verified
  (`knowledge/chain-resolution-r3.md`).
- Carried residuals stand from rounds 2–3: in-root hardlinks bypass path
  canonicalization, there is no size cap on source reads, and the banner still
  reads `research-gate-r1` (cosmetic) (`knowledge/chain-resolution-r3.md`).
- Receipt identity for mission acceptance is still open (round 1): no authentic
  queue taskKey or expected receipt bag exists, so proven receipt-backed rounds
  remain 0. Integrator/operator-owned; this wave ran on the operator's
  in-session direct dispatch, not a fleet wave render.
- Discernment is unchanged: a non-author has not sampled an admit and a reject
  (`lessons/round-1.md` and `lessons/2026-10-15-claims-span-fidelity.md`,
  Spot-check sections). No promotion marks are granted.
- Scope-refusal finding IDs proposed in the old wave never landed in the
  gate; the documentary province boundary is not executable enforcement yet.
- `SKILL.md` now supersedes the old “unchecked grep” cause with the informational
  emitter's false status under CLI errexit. Old corpus/log references remain
  historical and their integration errata identify the superseded assertions.
- The expected-input file pins inputs but is not a separate frozen-run gate.
  Input integrity was checked by the L1 acceptance; no stronger conformance
  or semantic-verification claim is made.

## Frontier

Round 2 ran its pre-registered local-only claim-verification move; routing was
satisfied by the operator's in-session direct dispatch (no fleet render, no
Sighting). It measures span identity, not semantics: the fixture closes
`VERDICT_BEARING_CLAIMS=17/17` CLEAN with four negative controls drifting, and
the r1 archive observable stays byte-stable at `VERDICT_BEARING_EXPORTS=3/3`.
Neither observable saturates its axis.

Round 3 ran its pre-registered chain-hop move on the same direct-dispatch
routing: the r1 structural check closes the tampered chain control CLEAN,
exit 0, while `verify-chain` reports `anchor-missing` and drifts it
(`RESOLVED_HOPS=1/2`), and the 22-hop positive control closes
`RESOLVED_HOPS=17/22` CLEAN with five exempt hops counted. That observable is
not saturated either — exemption is record-declared and unverifiable, one hop
at a time, no transitivity — and the r3 receipts are lane-local logs (no queue
taskKey), so the receipt-identity debt is unchanged.

Still open and integrator/operator-owned:
receipt identity for mission acceptance (proven receipt-backed rounds remain 0;
operator target at least 100), the non-author admit/reject spot-check,
scope-refusal gate findings, and frozen-replay conformance. Semantic and
external-source verification remain out of scope by design.
