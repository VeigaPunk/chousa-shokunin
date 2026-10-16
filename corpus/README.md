# chousa-shokunin — corpus

## Coverage map

| Note | Holds | Sources |
|---|---|---|
| `lessons/round-1.md` | Round-1 gate lesson: real-CLI vs function-under-`set +e` entrypoint gap behind `VERDICT_BEARING_EXPORTS=0/3`, with the gate's candidates/admitted/rejected and the spot-check status | baseline commit `34774a1`; `LOG.md:72-83`; `SCORECARD.md:29`; anchors re-derived from `tools/research-gate.sh` sha256 `e8f07a06…` |
| `knowledge/archived-export-intake.md` | One filled research-record specimen: pinned archive identity, scoped local observations, unresolved external hops, kept rejections, and explicit semantic-verification limits | note opening metadata and integration errata; `.ufo/evidence/round-1/acceptance.json`; `final-intake.json` |
| `knowledge/claim-verification-r2.md` | Round-2 note: `verify-claims` mode design (CLI + JSONL schema, fail-closed source boundary, verbatim-span check, structural marker convention), honest limits, receipts and open items | note metadata (gate sha `03a3324455…`); `fixtures/claims-r2.README.md`; `evidence/README.md` and `evidence/claims-r2-*.log` |
| `knowledge/chain-resolution-r3.md` | Round-3 note: `verify-chain` mode design (CLI + hop citation grammar, `heading`/`quote`/`line` anchors, fail-closed source boundary, exempt-but-counted statuses, per-hop verdicts + `RESOLVED_HOPS=N/M` under the CLEAN/DRIFT/exit contract), what anchor existence does not establish, receipts and open items | note metadata (gate sha `67daf85e…`); `fixtures/chain-r3.README.md`; `evidence/README.md` and `evidence/chain-r3-*.log` |
| `knowledge/anchor-boundaries-r4.md` | Round-4 note: the token-boundary matching semantics now shared by `verify-claims` spans and `verify-chain` quote anchors — one matcher (`tok_span_at`), the documented boundary class (file/line edge, ASCII whitespace, ASCII punctuation; word-internal hyphens/apostrophes not boundaries; non-ASCII fails closed; outer edges only), before→after attack-class measurements, residual limits (token-aligned shortening, non-ASCII neighbours, `_` gluing), receipts and open items | note metadata (gate sha `6b83705b…`, replacing `67daf85e…`); fixtures `claims-r2.jsonl`/`chain-r3.md`/`chain-r3-broken.md` at their pinned shas; `evidence/README.md` and `evidence/boundary-r4-*.log`; the seat's gate-free python re-derivation (86 probes, `INDEPENDENT_CHECK: AGREE`) |
| `knowledge/sweeps-rejections-r5.md` | Round-5 note: `verify-sweeps` mode design (rejection reason + flip-condition presence, sweep `where` tokenization classes, local glob/existence re-run with exempt-but-counted non-local/source-id classes, boundary guard, per-item verdicts + `VERIFIED_SWEEPS=N/M REJECTIONS_OK=K/L` under the CLEAN/DRIFT/0-1-2 contract), the measured flip presence-vs-quality class table, what a CLEAN sweep does not prove, receipts and open items | note metadata (gate sha `55adb92d…`, replacing `6b83705b…`); fixtures `sweeps-r5.md`/`sweeps-r5-broken.md`/`sweeps-r5-hit.md` at their pinned shas; `evidence/README.md` and `evidence/sweeps-r5-20261016T011543Z-*.log`; the seat's gate-free flip-class/exempt-class probes |
| `fixtures/claims-r2.jsonl` | Pre-registered 17-claim span fixture (13 supported / 2 contradicted / 2 unsupported) whose spans are verbatim bytes of the three archived inputs, with fixed expected verdicts and an independent byte-check | the three archived inputs at fleet commit `0863746e…`; sha256 pins and provenance table in `fixtures/claims-r2.README.md` |
| `fixtures/chain-r3.md` + `chain-r3-broken.md` | Pre-registered chain-hop pair built from real chains in the three archived inputs: a 22-hop positive control (17 resolved / 5 exempt → `RESOLVED_HOPS=17/22`, CLEAN) and a tampered 2-hop control (1/2, DRIFT, `CHAIN_ANCHOR_NOT_FOUND`); the round-1 hole live — `verify` closes both CLEAN, exit 0 | the three archived inputs at fleet commit `0863746e…`; sha256 pins, hop provenance table and the gate-free byte-check in `fixtures/chain-r3.README.md` |
| `fixtures/sweeps-r5.md` + `sweeps-r5-broken.md` (+ `sweeps-r5-hit.md`) | Pre-registered rejection/sweep pair: a positive control (3 kept rejections with reason + flip_condition, W1 local glob set genuinely empty, W2 non-local → `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`, CLEAN, exit 0) and a tampered control (R1 without flip-condition; W1 naming a planted hit file) that DRIFTs, exit 1, naming `SWEEP_REJECTION_INCOMPLETE` + `SWEEP_CLAIM_FALSE`; the round-1 hole live — r1 `verify` closes both CLEAN, exit 0 | the three archived inputs at fleet commit `0863746e…`; sha256 pins, provenance tables and the gate-free re-run in `fixtures/sweeps-r5.README.md` |
| `lessons/2026-10-15-claims-span-fidelity.md` | Round-2 lesson: span fidelity is not claim truth — the unchecked `claim` label, strace-measured bounds (no fetch, fail-closed refusals), byte-stable r1 behavior, named debt | gate sha `03a3324455…`; probes summarized in the note; `evidence/claims-r2-*.log` |
| `lessons/2026-10-15-chain-hop-resolution.md` | Round-3 lesson: `RESOLVED_HOPS`/chain CLEAN counts anchor existence only — a numeral tamper drifts; URL and out-of-corpus sources are refused unopened; exemption is record-declared and never checked (a marked hop can hide a resolvable citation); `nearest_line` is a heuristic; carried cosmetic banner item | gate sha `67daf85e…`; probes summarized in the lesson; `evidence/chain-r3-*.log` |
| `lessons/2026-10-15-anchor-token-boundaries.md` | Round-4 lesson: a quote is not any substring — before→after probe partitions on byte-identical anchors (claims 18/18 → 8/18; chain 17/17 → 8/17) with identical miss sets across both modes, the first 40 selftest case lines byte-identical, a gate-free analysis showing every matched r2/r3 fixture span/anchor sits on a line-edge/whitespace/ASCII-punctuation edge, and the class choices with visible consequences (non-ASCII fail-closed, `_` boundary, token-aligned shortening still passing) | gate sha `6b83705b…`; probes summarized in the lesson; `evidence/README.md` and `evidence/boundary-r4-*.log` |
| `lessons/2026-10-16-sweeps-rejections-verdict-bearing.md` | Round-5 lesson: existence is not falsifiability — the structural before-state (both fixtures CLEAN under r1 `verify`), the landed presence/glob checks, what a CLEAN `verify-sweeps` establishes and what it cannot (flip-condition quality, command re-run, rightness of an empty location set), defect notes and named follow-ups | gate sha `55adb92d…`; probes summarized in the lesson; `evidence/sweeps-r5-20261016T011543Z-*.log` |

Count: 10 entries, five knowledge notes and five lessons — `functions.glob`
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

## Round-4 evidence

- `evidence/README.md`: index extended to round 4 with pinned gate/fixture shas, the seven single-delta attack controls and a self-contained re-run recipe.
- `evidence/boundary-r4-20261016T002701Z-live.log`: r3-gate structural state (the broken chain record still closes CLEAN under `verify`, exit 0 — the hole this round closes); r1 archive observable each exit 1 with `VERDICT_BEARING_EXPORTS=3/3` and stdout byte-identical to the round-3 gate receipt; intake `CLEAN (… chains=8 …)` exit 0; claims/chain stdout byte-identical to the round-2/3 live receipts; zero network syscalls under `strace`.
- `evidence/boundary-r4-20261016T002701Z-attacks.log`: on the same attack copies, `67daf85e…` closes each CLEAN exit 0 and `6b83705b…` drifts each exit 1 — seven single-delta claims/chain controls (mid-token truncation and padding, hyphen/apostrophe cuts, glued start, glued extra word); the boundary helpers and both call sites printed verbatim; a gate-free checker classifies all 11 copies with `BOUNDCHECK_SUMMARY: all copies agree`, exit 0. Attack copies are ephemeral scratch sha-pinned inside the receipt.
- `evidence/boundary-r4-20261016T002701Z-claims.log`: canonical `VERDICT_BEARING_CLAIMS=17/17` CLEAN exit 0 (unchanged); three claims attacks each `16/17` DRIFT with one `CLAIM_SPAN_NOT_FOUND` at the line-aware report; legit controls `19/19` CLEAN (span followed by `,`; span bounded by `(`/`)` with slashes/apostrophe/hyphen inside).
- `evidence/boundary-r4-20261016T002701Z-chain.log`: canonical `RESOLVED_HOPS=17/22` CLEAN and broken control `1/2` DRIFT (both unchanged); four chain attacks each `16/22` DRIFT with `CHAIN_ANCHOR_NOT_FOUND`; legit control `18/23` CLEAN (quote followed by `,`).
- `evidence/boundary-r4-20261016T002701Z-selftest.log`: `RESEARCH_GATE_SELFTEST: PASS (44 cases)`, exit 0; case lines 1–40 byte-identical to the round-3 selftest; new cases 41–44 = `claims-boundary-pass`/`-fail` and `chain-pass-boundary`/`-fail` on the gate's own `lib/boundary.md` fixture.

## Round-5 evidence

- `evidence/README.md`: index extended to round 5 with pinned gate/fixture shas, the seven single-delta negative controls and a self-contained re-run recipe.
- `evidence/sweeps-r5-20261016T011543Z-live.log`: before-state (the r4 CLI has no `verify-sweeps` — exit 2 — and passes both fixtures structurally, CLEAN exit 0); live canonical run `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` CLEAN exit 0; broken control DRIFT exit 1 naming `SWEEP_REJECTION_INCOMPLETE` and `SWEEP_CLAIM_FALSE`; seven negative controls (flip emptied, reason emptied, false-emptiness hit, non-local exempt-but-counted, nowhere, out-of-corpus refused crit, undeclared source id); cross-round stdout pairs byte-identical to the round-4 receipts (claims 17/17, chain 17/22, chain-broken 1/2, archives 3/3); zero network (`strace`: 0 syscalls, 992 trace lines).
- `evidence/sweeps-r5-20261016T011543Z-broken.log`: the tampered control under both revisions — r4 `verify` CLEAN exit 0 (the hole) → landed `verify-sweeps` DRIFT exit 1 with both named findings.
- `evidence/sweeps-r5-20261016T011543Z-selftest.log`: `RESEARCH_GATE_SELFTEST: PASS (54 cases)`, exit 0; the first 44 ok-case lines byte-identical to the round-4 receipt (`cmp` YES); new cases 45–54 = the eight `sweeps-*` cases plus two setup exits.
- `evidence/sweeps-r5-20261016T011543Z-fixture.log`: fixture inventory (3 rejections + 2 sweeps; 1 + 1 broken), the archive-set URL emptiness census (zero matches), the record's own W1 glob re-run (zero hits), the planted hit on disk, export pins matching the fixture README, and an independent gate-free re-derivation (`canonical=CLEAN broken=DRIFT`).

## Known gaps

- CLEAN is mode-dependent, not semantic: `verify` checks record structure (r1);
  `verify-claims` checks byte-span identity at token boundaries plus a declared
  marker (r2 mode, r4 boundary rule); `verify-chain` checks that each unmarked
  resolved hop's source canonicalizes under the boundary and its
  `heading`/`quote`/`line` anchor occurs in the target — `quote` at token
  boundaries (r3 mode, r4 rule), `heading`/`line` by trimmed equality (r3);
  `verify-sweeps` checks rejection reason/flip-condition presence and re-runs
  each named local sweep location set as a glob/existence test (r5). None of
  the four proves semantic support, location binding, uniqueness or the
  source's own truth; chain CLEAN additionally does not prove agreement (hop 6
  resolves across disagreeing statements) or authorship (cross-input hops are
  co-anchors); sweep CLEAN proves the named location set re-measured empty, not
  that it was the right place to look. No original external source was fetched
  and none may be.
- The round-5 sweep/rejection check is presence- and location-level: a
  non-empty but vacuous flip-condition (placeholder, tautology, never-fires,
  vague) passes, the recorded sweep command is never executed and its prose
  never compared (a sweep can be empty because the wrong glob was named), and
  a record with no rejections/sweeps at all closes `VERIFIED_SWEEPS=0/0`
  CLEAN — section existence stays r1 `verify`'s check. Non-local and
  declared-source-id sweeps stay exempt-but-counted
  (`knowledge/sweeps-rejections-r5.md`).
- The round-4 boundary class is syntactic and ASCII-anchored: an occurrence
  whose outer edge abuts a non-ASCII character (`”`, `’`, `—`, `。`, `→`) is a
  miss even when its bytes are real, `_` is a boundary by decision, and
  token-aligned shortening — whole words dropped at genuine edges — still
  resolves; the hardening closes glued truncation/padding, not quoting less
  than the sentence (`knowledge/anchor-boundaries-r4.md`,
  `evidence/boundary-r4-20261016T002701Z-attacks.log`). The r2/r3 marker,
  uniqueness, exemption-truth and external-source limits stand unchanged.
- `knowledge/chain-resolution-r3.md` cites the superseded
  `chain-r3-20261015T235411Z-live.log` for its one-byte-truncated-anchor
  example (that cut was removed in-wave; Round-3 evidence above) — the
  surviving live receipt's control 1 is a padded `semanticsX` variant that
  drifted. The substring-truncation fact itself is re-established by the
  round-4 before-state (`knowledge/anchor-boundaries-r4.md`).
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

Round 4 ran the calibration move round 3 registered, on the same
direct-dispatch routing: the pinned observables hold byte-stable (selftest
40 → 44 with case lines 1–40 identical, `VERDICT_BEARING_CLAIMS=17/17`,
`RESOLVED_HOPS=17/22`, broken control `1/2` DRIFT, r1 archive observable
`3/3`), while the attack class flips — truncated/padded/glued copies that
closed CLEAN under `67daf85e…` now drift under `6b83705b…` with the
line-aware reports, and the two modes miss on identical probe sets (claims
5/5 → 2/5 and chain 8/8 → 5/8 in the note's attack fixtures; 86-probe
battery 86/86 → 71/86). That observable is not saturated either: the
boundary class is ASCII-anchored (non-ASCII neighbours fail closed), `_` is a
boundary, and token-aligned shortening still passes, so quote integrity
stays partial and location binding, uniqueness and semantics remain
unverified. The r4 receipts are lane-local logs (no queue taskKey), so the
receipt-identity debt is unchanged.

Round 5 ran the last registered r1 structural move — kept rejections and
negative sweeps become verdict-bearing — on the same direct-dispatch routing:
both fixtures closed CLEAN structurally under `verify` at `6b83705b…` (the
hole), while at `55adb92d…` the canonical record closes
`VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` CLEAN and the tampered control DRIFTs
naming `SWEEP_REJECTION_INCOMPLETE` + `SWEEP_CLAIM_FALSE`, with the pinned
observables byte-stable (selftest 44 → 54, case lines 1–44 identical; claims
17/17; chain 17/22; broken control 1/2; r1 archives 3/3). That observable is
not saturated either: flip-condition presence is screened, not quality
(vacuity passes); the sweep re-run is a glob/existence check over the named
locations, never the recorded command; section absence is still r1's to flag;
and non-local sweeps stay exempt-but-counted. The r5 receipts are lane-local
logs (no queue taskKey), so the receipt-identity debt is unchanged.

Still open and integrator/operator-owned:
receipt identity for mission acceptance (proven receipt-backed rounds remain 0;
operator target at least 100), the non-author admit/reject spot-check,
scope-refusal gate findings, and frozen-replay conformance. Semantic and
external-source verification remain out of scope by design.
