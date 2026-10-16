# chousa — Scorecard

## Axes

| Axis | Score (0–10) | Evidence | Last-change round |
|---|---:|---|---:|
| operability | 3 | Gate commit `31b46832e56a7f095092a4a6d62b74bfaf6933e8`: A/B/C each exit 1 with exactly one full DRIFT summary; `.ufo/evidence/round-1/acceptance.json`; baseline `34774a1777d4058ca8c2b4456ce2e6ccee9e24c5` was 0/3 | 1 |

This missing-at-baseline scorecard starts with the one measured axis, operability
(AXES.md's runnable-artifact axis). No expertise scores are invented for the
other five axes. Score = the number of the three named archived inputs that
exit 1 **and** emit exactly one `RESEARCH_GATE: DRIFT` summary, one point each;
this deliberately narrow observable can award at most 3/10, not field readiness.

## Planned

Round 1's one move is integrated: informational findings no longer abort the
CLI before its verdict, and fresh-process fixtures exercise the public path.
No second round runs here. Fresh round 2 must pre-register its local-only
claim-verification fixture after receipt identity and new-wave routing exist.

Baseline inputs, read-only under the fleet root:
`research/deep-research-2026-09-28/A-shokunin-tradition.md`,
`B-multiagent-knowledge.md`, and `C-rank-taxonomy.md`.

Counting command (run from this lane; no fetch):

```bash
python3 -c 'import subprocess; names=("A-shokunin-tradition.md","B-multiagent-knowledge.md","C-rank-taxonomy.md"); rows=[subprocess.run(["bash","tools/research-gate.sh","verify","../research/deep-research-2026-09-28/"+n,"--root",".."],capture_output=True,text=True) for n in names]; print("VERDICT_BEARING_EXPORTS=%d/3" % sum(r.returncode==1 and sum(s.startswith("RESEARCH_GATE: DRIFT (") for s in r.stdout.splitlines())==1 for r in rows))'
```

## Retired

None. The unmeasured axes are not retired or asserted saturated.

## Round-1 per-axis verdicts

Measurements: committed gate `31b46832e56a7f095092a4a6d62b74bfaf6933e8`,
`.ufo/evidence/round-1/acceptance.json` and `final-intake.json`.
The earlier baseline is the observed failure preserved in LOG.md, not a
failure rerun in this continuation. The 3/10 score remains the narrow count
above, never a scalar replacement for these verdicts.

| Axis | Verdict | Evidence boundary |
|---|---|---|
| operability | improved | 0/3 → 3/3 verdict-bearing archives; real CLI selftest PASS (20 cases), normal/strict info paths and setup exits checked; intake CLEAN |
| depth | unchanged | No independently verified domain fact or broader expertise measurement added |
| coverage | unchanged | One supporting intake specimen, not a measured fraction of the province |
| freshness | unchanged | Changed surface rechecked; no new drift detector or cross-revision freshness claim |
| calibration | unchanged | Structural/semantic limits retained; no non-author discernment or promotion claim |
| adjacency | unchanged | Existing province refusals retained; foreign findings reported, not absorbed |

## Round-1 learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | New held archive-intake specimen, `corpus/README.md` coverage row for `knowledge/archived-export-intake.md`; source pins and structural acceptance attached |
| quality | unchanged | No older admitted knowledge entry was reverified or superseded; no semantic-quality gain claimed from a structural CLEAN |
| discernment | unchanged | Non-author admit/reject spot-check unavailable; L2 reviews remain author-lane evidence |

## Admission and continuation

Local axis result: one improved, none harmed. The inherited 32-member
rendered wave is reconciled; later nine-seat calls are advisory only.
No second round-1 wave or round-2 work was started.

Mission acceptance is separate: the interactive launch has no authentic
queue taskKey/expected receipt bag. Do not manufacture `task_...`, count a
shape-only receipt as applicable, or mark the Sighting complete. Proven
receipt-backed completed rounds remain 0 pending integrator receipt binding
and acceptance. The operator's target remains at least 100, not reduced.

Debt and concrete unblocks: the continuation records missing receipt identity,
current role-to-alias bindings needed before a new wave, outside spot-check,
and absent scope-refusal gate findings. The narrow archive observable is
exhausted, not the operability axis or province; no saturation is declared.

## Round 2 verdict — 2026-10-15 (goal wave; evidence commit `c3df458`)

Selected axis: **coverage** — the lane's core method (claim-vs-source
verification), registered in round 1 as "fresh round 2 must pre-register its
local-only claim-verification fixture." Routing is satisfied by the
operator's in-session direct dispatch; **receipt identity remains open** (see
the report's debt section). Wave: one 32-seat flash call, 24/24 reports.
Report: `.ufo/round-2/chousa-goalwave.md`.

**Before** (gate `0884355…`, selftest 20): the gate validated record
STRUCTURE only — no claim was ever checked against its source; the claim
machinery of the declared method was unmeasured.

**After** (gate `03a33244…`, selftest 30 = +10, first 20 byte-identical;
fixture `corpus/fixtures/claims-r2.jsonl` with 17 provenance-carrying claims;
parent acceptance 2026-10-15T23:45Z): `verify-claims <file> --root ..`
verifies each claim's span appears VERBATIM in its source under the corpus
boundary (canonicalized; out-of-corpus/URL/session paths refused unopened),
line-aware miss reports, the contradicted structural marker, per-claim
verdicts + exact counting + the existing CLEAN|DRIFT/exit contract. Fixture:
`VERDICT_BEARING_CLAIMS=17/17`, `RESEARCH_GATE: CLEAN (13 supported / 2
contradicted / 2 unsupported)`. Round-1 observable intact: 3/3
verdict-bearing exports. Boundary escapes refused (absolute, traversal,
symlink, named pipe); strace-confirmed zero network; the r1 verify path
byte-stable.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | claim-vs-source verification lands as a verdict-bearing gate mode with a pre-registered 17-claim fixture (provenance README, span-fidelity independently re-verified); the method's core move is now executable and measured. |
| depth | **improved** | `corpus/knowledge/claim-verification-r2.md`: verbatim-span semantics + the honest limits (does NOT prove semantics, location binding, source truth, external verification); lesson `2026-10-15-claims-span-fidelity.md`. |
| operability | **improved** | selftest 20 → 30 (+10: positive/tampered/out-of-corpus/external/session/marker/counting); existing cases byte-identical; exit contract 0/1/2 held. |
| freshness | **unchanged** | four receipts + fixture log at the new SHA; no drift detector (mori-style pins are a sibling lane's pattern, not adopted here). |
| calibration | **unchanged** | the contradicted marker is structural by design; the note names what the check does not prove. |
| adjacency | **unchanged** | zero network (strace); research corpus read-only; seats wrote only in-lane; scope-sentinel clean. |

Honest residuals (named in the note + seat reports): in-root hardlinks bypass
path canonicalization (critic); no size cap on claim-source reads
(boundary-tester recommendation); the banner still says `research-gate-r1`
(cosmetic). Admission: **ADMIT** (coverage/depth/operability improved, none
harmed). No scalar score. Learning trends: expansion/quality **improved**,
discernment **unchanged** (no outside spot-check exists). Round 3
registered: chain-hop resolution — each hop's citation must resolve to a real
corpus location, making citation chaining verdict-bearing.

## Round 3 verdict — 2026-10-15 (goal wave; evidence commit `cc9fe8f`)

Selected axis: **coverage** — citation chaining becomes verdict-bearing (the
round-2-named continuation). Wave: one 32-seat flash call, 24/24 reports.
Report: `.ufo/round-3/chousa-goalwave.md`. Environmental note: the host's
per-user /tmp quota exhausted mid-acceptance (all prior waves' scratch);
the parent freed 727 MB of stale declared-ephemeral scratch and re-ran the
battery clean — no artifact was affected.

**Before** (gate `03a33244…`, selftest 30): chain hops were checked
STRUCTURALLY only — a hop could cite an anchor that does not exist in the
target and still pass.

**After** (gate `67daf85e…`, selftest 40 = +10, first 30 byte-identical;
parent acceptance 2026-10-16T00:15Z): `verify-chain <record> --root ..`
verifies each resolved hop's citation — source must be a declared Sources id
or in-corpus path (same canonicalization as verify-claims; unknown ids and
out-of-corpus/URL/session sources refused unopened), anchor must exist
(heading trimmed-equality, quote verbatim line-aware, whole-line) with
`at=line:N` reporting; unresolved/marked hops stay exempt but counted;
`RESOLVED_HOPS=N/M` + the CLEAN|DRIFT/0-1-2 contract. Fixture:
`RESOLVED_HOPS=17/22`, `RESEARCH_GATE: CLEAN` (17 verified / 5 exempt);
the broken control fixture DRIFTs exit 1 naming `anchor-missing`.
verify-claims held byte-identical (17/17 CLEAN); the r1 archive observable
intact (3/3).

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | citation chaining is now resolution-verified end to end (source id or path + anchor existence), the third verdict-bearing mode; per-hop line reporting makes misses actionable. |
| depth | **improved** | `corpus/knowledge/chain-resolution-r3.md` (anchor semantics, exempt classes, the named limit: anchors are SUBSTRING semantics — a truncated quote still resolves; round-4 hardening candidate). |
| operability | **improved** | selftest 30 → 40 (+10: positive/missing-anchor/out-of-corpus/unresolved-exempt/counting/exits); all r1+r2 cases byte-identical; three modes compose with one boundary policy. |
| freshness | **unchanged** | r3 receipts at the new SHA. |
| calibration | **unchanged** | the substring-semantics limit is documented as a named candidate, not hidden. |
| adjacency | **unchanged** | zero network; corpus read-only; scope-sentinel clean. |

Admission: **ADMIT** (coverage/depth/operability improved, none harmed). No
scalar score. Learning trends: expansion/quality **improved**, discernment
**unchanged**. Round 4 registered: anchor hardening — token-boundary
semantics so truncated-quote games cannot resolve, plus the claim-span
truncation class from round 2's note.

## Round 4 verdict — 2026-10-16 (goal wave; evidence commit `a6f3118`)

Selected axis: **calibration** of the matching semantics — the round-3-named
truncation limit. Wave: one 32-seat flash call, 25/25 reports. Report:
`.ufo/round-4/chousa-goalwave.md`.

**Before** (gate `67daf85e…`): anchors and claim spans matched as raw
substrings — a citation truncated mid-phrase (or padded with an extra word)
still resolved.

**After** (gate `6b83705b…`, selftest 44 = +4; parent acceptance
2026-10-16T00:55Z): ONE shared token-boundary matcher serves both verify-claims
spans and verify-chain quote anchors (the rule cannot drift between modes;
verified by the cross-mode seat): an occurrence counts only when both outer
edges are boundaries — file/line edge, ASCII whitespace, ASCII punctuation —
with `-`/`'` as boundaries only when not joining two word characters, `_`
punctuation (Markdown emphasis), non-ASCII bytes NOT boundaries (fail closed),
byte-exact, case-sensitive; misses keep the line-aware reports. All r1-r3
cases byte-identical PASS (1-40 cmp-clean against the r3 receipt); claims
17/17 and chain 17/22 still CLEAN; the broken control still DRIFTs naming
anchor-missing; the r1 observable intact (3/3); the attack seat's
truncation/padding/glue games all FAIL, controls PASS.

| axis | verdict | evidence (before → after) |
|---|---|---|
| calibration | **improved** | the matching semantics went from substring (truncation-vulnerable, demonstrated) to documented token boundaries, with the exact character class in the header and shared logic across modes. |
| depth | **improved** | `corpus/knowledge/anchor-boundaries-r4.md`: the rule, the catches, and what hardening still cannot do (semantic/context limits — a real quote reused in a wrong context still resolves); lesson `2026-10-15-anchor-token-boundaries.md`. |
| operability | **improved** | selftest 40 → 44 (+4: boundary pass/fail pairs running the SAME fixture bytes through both modes); zero regression across all modes. |
| coverage | **unchanged** | no new measured surface; both fixtures held. |
| freshness | **unchanged** | five receipts at the new SHA. |
| adjacency | **unchanged** | zero network; quota-sentinel-held /tmp; corpus read-only. |

Admission: **ADMIT** (calibration/depth/operability improved, none harmed). No
scalar score. Learning trends: expansion/quality **improved**, discernment
**unchanged**. Round 5 registered: the last unmeasured structural axis —
kept rejections and negative sweeps become verdict-bearing (`verify-sweeps`:
each rejection cites reason + flip-condition; each sweep names where it
looked, with local emptiness checkable).

## Round 5 verdict — 2026-10-16 (goal wave; evidence commit `e7ab39a`)

Selected axis: **coverage** — the last r1 structural axis: kept rejections and
negative sweeps become verdict-bearing. Wave: one 32-seat flash call, 27/27
reports. Report: `.ufo/round-5/chousa-goalwave.md`.

**Before** (gate `6b83705b…`): rejections and sweeps existed structurally — a
rejection with no flip-condition passed; a sweep naming nowhere (or a false
emptiness) passed.

**After** (gate `55adb92d…`, selftest 54 = +10, cases 1-44 byte-identical;
parent acceptance 2026-10-16T02:00Z): `verify-sweeps <record> --root ..`
requires every kept rejection to carry a non-empty reason AND flip-condition
(`SWEEP_REJECTION_INCOMPLETE` on miss), and every sweep to name where it
looked: local path sets are re-run for emptiness (any hit =
`SWEEP_CLAIM_FALSE` naming the hit; zero hits = verified), non-local namings
exempt-but-counted (the unresolved-hop idiom), unnamed = `SWEEP_LOCATION_ABSENT`,
boundary escapes refused unopened. Fixture: `VERIFIED_SWEEPS=1/2
REJECTIONS_OK=3/3` CLEAN; broken control DRIFT naming both classes (incomplete
rejection + a planted hit listed by path). claims 17/17 and chain 17/22 held
CLEAN; selftest 54/54 x2.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | all four r1 structural axes are now verdict-bearing (structure, claims, chains, rejections+sweeps); every record element that asserts something now gets checked against something. |
| depth | **improved** | `corpus/knowledge/sweeps-rejections-r5.md`: flip-condition semantics, the local-emptiness re-check, the exempt class, and the named limits (vacuous flip-conditions, narrow-sweep triviality — as exercised by the adversarial seats). |
| operability | **improved** | selftest 44 → 54 (+10, 1-44 byte-identical); five modes under one boundary + exit contract. |
| freshness | **unchanged** | receipts at the new SHA. |
| calibration | **unchanged** | the critic's vacuous-flip and narrow-sweep classes are documented limits, not silently closed. |
| adjacency | **unchanged** | zero network; corpus read-only; quota held. |

Admission: **ADMIT** (coverage/depth/operability improved, none harmed). No
scalar score. Learning trends: expansion/quality **improved**, discernment
**unchanged**. Round 6 registered: composition — a `verify-all` deep mode
running all four checks as one verdict, plus the fleet-ledger/manifest step
that records a record's full verification state.

## Round 6 verdict — 2026-10-16 (goal wave; evidence commit `74c533d`)

Selected axis: **operability/composition** — one record, one deep verdict.
Wave: one 32-seat flash call, 26/26 reports. Report:
`.ufo/round-6/chousa-goalwave.md`.

**Before** (gate `55adb92d…`): a record's full verification state required
running four modes manually and eyeballing; no durable manifest.

**After** (gate `0c3d51ed…`, selftest 64 = +10, cases 1-54 byte-identical;
parent acceptance 2026-10-16T03:20Z): `verify-all <record> [--claims PATH]
[--json PATH] --root ..` runs every applicable section as a fresh solo-mode
invocation (section tallies equal the solo runs BY CONSTRUCTION), composes one
`RESEARCH_GATE: CLEAN|DRIFT` (DRIFT iff any section drifts), reports absent
sections (claims/chains/sweeps optional; absent != drift — the omission limit
is a named r7 candidate), and `--json` APPENDS the verification state
(record+gate SHAs, UTC, per-section tallies, composed verdict) to
`corpus/evidence/verify-all-manifest.jsonl` (>> only, no rewrite path). Full
fixture: CLEAN, sections=4 run=4; broken fixture: DRIFT with drift-sections=2
naming chain + sweeps; strace-confirmed zero network; all solo modes held.

| axis | verdict | evidence (before → after) |
|---|---|---|
| operability | **improved** | composed verification with solo-equal tallies, absent-not-drift semantics, and a durable append-only manifest — a record's verification state is now one command + one manifest line. |
| depth | **improved** | `corpus/knowledge/verify-all-r6.md`: composition semantics, the omission limit, the manifest schema; the omission-hunter demonstrated the named hole (claims-heavy record with no ## Claims verifies CLEAN) and the r7 candidate (cross-section reference integrity / record-type obligations). |
| coverage | **unchanged** | no new measured surface; all five modes intact. |
| freshness | **improved narrowly** | the manifest is the lane's first durable, append-only verification-state ledger. |
| calibration | **unchanged** | absent!=drift is a declared semantic, not a hidden relaxation. |
| adjacency | **unchanged** | zero network; corpus read-only; quota held. |

Admission: **ADMIT** (operability/depth/freshness improved, none harmed). No
scalar score. Learning trends: expansion/quality **improved**, discernment
**unchanged**. Round 7 registered: binding integrity — every cross-section
reference (sweep/companion bindings) must resolve to a declared row or source,
fail-closed, closing the dangling-claim/unbound-companion class demonstrated
this round.

## Round 7 verdict — 2026-10-16 (goal wave; evidence commit `a1948c3`)

Selected axis: **coverage-of-integrity** — the round-6 demonstrated hole:
dangling cross-section references. Wave: one 32-seat flash call, 24/24
reports. Report: `.ufo/round-7/chousa-goalwave.md`.

**Before** (gate `0c3d51ed…`): a record's sweep cell could name a claim id no
`## Claims` row declares, a hop could cite an undeclared source id — and every
mode passed it (demonstrated: `CLEAN` on a record with 3 dangling refs).

**After** (gate `3ba718bf…`, selftest 74 = +10; parent acceptance
2026-10-16T04:15Z): seventh mode `verify-integrity`, composed as verify-all's
fifth section: every reference token (claim/source/sweep ids in chain, claims,
negatives, sweeps, rejections cells) must resolve to a declared id —
`REF_UNRESOLVED` (drift) when not, resolved counted, exempt classes
(non-local namings, blocked-no-fetch) exempt-but-counted. Fixture: 16 refs /
15 resolved / 0 unresolved CLEAN; broken control DRIFT naming exactly
`S9` (chain from-cell) and `C9` (sweeps claim_id). Solo holds intact
(claims 17/17, chain 17/22); quota-sentinel clean 28 samples.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | every cross-section reference is now resolution-checked; the record's internal consistency is as verdict-bearing as its external citations. |
| depth | **improved** | `corpus/knowledge/reference-integrity-r7.md`: the reference model (declared ids, reference cells, token splitting), fail-closed semantics, exempt classes, the critic's extraction limits (substring-looking ids, quoted-span tokens) dispositioned. |
| operability | **improved** | selftest 64 → 74 (+10); seven modes; verify-all now runs five sections as fresh solo invocations (tally-equal by construction). |
| freshness | **unchanged** | receipts + manifest lines at the new SHA. |
| calibration | **unchanged** | warn-severity REF findings drift the record (visibility) — severity semantics documented. |
| adjacency | **unchanged** | zero network; corpus read-only; quota held. |

Admission: **ADMIT** (coverage/depth/operability improved, none harmed). No
scalar score. Learning trends: expansion/quality **improved**, discernment
**unchanged**. Round 8 registered: the gate's own behavioral baseline
(`--pin`/`--drift` adapted from the sibling lane's proven pattern) — the
verification tool's drift becomes detectable.

## Round 8 verdict — 2026-10-16 (goal wave; evidence commit `27b55c3`)

Selected axis: **freshness/operability** — the gate's own drift becomes
detectable (the mori lane's proven pattern, lineage declared). Wave: one
32-seat flash call, 23/23 reports. Report: `.ufo/round-8/chousa-goalwave.md`.

**Before** (gate `3ba718bf…`): a gate regression (a mode silently skipped, an
output field changed) was catchable only by reading receipts after the fact;
no baseline existed anywhere in the lane.

**After** (gate `46f5ddb3…`, selftest 85 = +11; parent acceptance
2026-10-16T05:10Z): `--pin` captures a canonical invocation (verify-all on a
self-built temp fixture, relative paths, byte-stable anywhere) with a declared
VOLATILE contract (`ts gate_sha256` shape-masked; changing the list is itself
drift); `--drift` reports `GATE_DRIFT: none` exit 0 / named tokens exit 1 /
missing-malformed exit 2 — never a false none. Measured catches: a one-field
mutant names `+finds -findings`; a silently-skipped mode names
`-REJECTIONS_OK -SECTION:sweeps`; a volatile-list rewrite names
`volatile_fields`. The lane committed its baseline
(`corpus/evidence/gate-baseline-r8-20261016T033757Z.json`); the parent's
drift re-run: `GATE_DRIFT: none` exit 0. All 74 prior cases byte-identical;
all seven modes byte-stable; hermetic (pin from lane, drift from `/`); zero
network.

| axis | verdict | evidence (before → after) |
|---|---|---|
| freshness | **improved** | the verification tool's behavior is now pinned and drift-detecting; the r7 selftest-flake class of surprise has a detector. |
| operability | **improved** | selftest 74 → 85 (+11); --pin/--drift join the 0/1/2 contract; canonical invocation documented in the header. |
| depth | **improved** | `corpus/knowledge/gate-baseline-r8.md`: design, the mori lineage, the volatile contract, catches (field/mode/volatile drift) and cannot-catches (semantic drift inside stable fields). |
| coverage | **unchanged** | no new measured research surface. |
| calibration | **unchanged** | the volatile list was measured before declared (3-run field diff). |
| adjacency | **unchanged** | zero network; corpus read-only; sibling-lane files read-only (lineage cited). |

Admission: **ADMIT** (freshness/operability/depth improved, none harmed). No
scalar score. Learning trends: expansion/quality **improved**, discernment
**unchanged**. Round 9 registered: fixture-depth coverage — the three archived
inputs themselves run through verify-all end-to-end as records, with expanded
claim/hop fixtures where the archives support them.

