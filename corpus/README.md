# chousa-shokunin — corpus

## Coverage map

| Note | Holds | Sources |
|---|---|---|
| `lessons/round-1.md` | Round-1 gate lesson: real-CLI vs function-under-`set +e` entrypoint gap behind `VERDICT_BEARING_EXPORTS=0/3`, with the gate's candidates/admitted/rejected and the spot-check status | baseline commit `34774a1`; `LOG.md:72-83`; `SCORECARD.md:29`; anchors re-derived from `tools/research-gate.sh` sha256 `e8f07a06…` |
| `knowledge/archived-export-intake.md` | One filled research-record specimen: pinned archive identity, scoped local observations, unresolved external hops, kept rejections, and explicit semantic-verification limits | note opening metadata and integration errata; `.ufo/evidence/round-1/acceptance.json`; `final-intake.json` |
| `knowledge/claim-verification-r2.md` | Round-2 note: `verify-claims` mode design (CLI + JSONL schema, fail-closed source boundary, verbatim-span check, structural marker convention), honest limits, receipts and open items | note metadata (gate sha `03a3324455…`); `fixtures/claims-r2.README.md`; `evidence/README.md` and `evidence/claims-r2-*.log` |
| `fixtures/claims-r2.jsonl` | Pre-registered 17-claim span fixture (13 supported / 2 contradicted / 2 unsupported) whose spans are verbatim bytes of the three archived inputs, with fixed expected verdicts and an independent byte-check | the three archived inputs at fleet commit `0863746e…`; sha256 pins and provenance table in `fixtures/claims-r2.README.md` |
| `lessons/2026-10-15-claims-span-fidelity.md` | Round-2 lesson: span fidelity is not claim truth — the unchecked `claim` label, strace-measured bounds (no fetch, fail-closed refusals), byte-stable r1 behavior, named debt | gate sha `03a3324455…`; probes summarized in the note; `evidence/claims-r2-*.log` |

Count: 4 entries, two knowledge notes and two lessons — `functions.glob` pattern
`corpus/knowledge/*.md;corpus/lessons/*.md`, 2026-10-15. Fixture and evidence
files are coverage-listed but not additional knowledge entries.

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

## Known gaps

- CLEAN is structural acceptance (r1) plus byte-span identity (r2) only:
  `verify-claims` proves quoted bytes occur in the cited local file and that a
  declared marker co-occurs — not semantic support, location binding or the
  source's own truth. No original external source was fetched and none may be.
- The mode reads `id/source/span/expect[/marker]` only; the `claim` sentence is
  never compared with its span, so a claim label can assert the opposite of its
  span and still close CLEAN (`lessons/2026-10-15-claims-span-fidelity.md`).
- Round-2 span checks are single-source, text-only, and report first occurrence;
  chain-level and entailment-level claim verification are not built
  (`knowledge/claim-verification-r2.md`).
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
Neither observable saturates its axis. Still open and integrator/operator-owned:
receipt identity for mission acceptance (proven receipt-backed rounds remain 0;
operator target at least 100), the non-author admit/reject spot-check,
scope-refusal gate findings, and frozen-replay conformance. Semantic and
external-source verification remain out of scope by design.
