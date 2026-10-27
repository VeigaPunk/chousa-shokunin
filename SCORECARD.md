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

## Round 9 verdict — 2026-10-16 (goal wave; evidence commit `ebd04d2`)

Selected axis: **coverage** — the archive corpus gets its first full deep
verification (fixture-led round; the gate correctly stayed unchanged).
Wave: one 32-seat flash call, 24/24 reports. Report:
`.ufo/round-9/chousa-goalwave.md`.

**Before** (gate `46f5ddb3…`): the three archived inputs had only the r1
structural observable (3/3) and ~17 pointwise fixture claims; no archive had
ever passed through verify-all as a record.

**After** (parent acceptance 2026-10-16T06:20Z): the three archives exist as
gate-format records under `corpus/fixtures/archives-r9/` (spans machine-
extracted from archive bytes, never retyped): verify-all CLEAN on each with
zero findings — A: 6/7 hops resolved, 13 integrity refs / 0 unresolved, 4/4
rejections, 1/1 sweeps; B: 6/7, 14/0, 3/3, 1/1; C: 7/8, 15/0, 4/4, 1/1.
`claims-r9.jsonl` adds 10 new verbatim claims (10/10 CLEAN, 7 supported / 2
contradicted / 1 unsupported). Premise correction recorded honestly: the
archives do NOT literally cross-cite — the hops are intra-archive/conceptual,
authored as such. The reframing risk (record-format distortion of what an
archive claims) is named and mitigated in the record READMEs. All holds:
selftest 85/85, `GATE_DRIFT: none` vs the r8 baseline, claims-r2 17/17.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the lane's whole research corpus is now deep-verifiable end to end; claim coverage grew 17 -> 27 with archive-scale records. |
| depth | **improved** | `corpus/knowledge/archives-verified-r9.md`: coverage stats, the reframing-risk analysis, honest premise correction. |
| operability | **unchanged** | the gate unchanged (a fixture-led round as designed); every hold green. |
| freshness | **unchanged** | receipts + three archive manifest lines at the current SHA. |
| calibration | **improved narrowly** | the no-cross-citation finding is a calibration of the corpus map (prior records implied inter-archive chains that do not exist). |
| adjacency | **unchanged** | archives quoted read-only; zero network. |

Admission: **ADMIT** (coverage/depth/calibration improved, none harmed). No
scalar score. Learning trends: expansion/quality **improved**, discernment
**unchanged**. Round 10 registered: residual hardening — negative controls at
archive scale (broken archive records per defect class), the exempt-hop audit,
and disposition of every r2-r9 named limit.

## Round 10 verdict — 2026-10-16 (goal wave; evidence commit `5f99fa3`)

Selected axis: **hardening/calibration** — archive-scale negative controls +
the final limit-disposition ledger (the round-11 audit's starting map).
Wave: one 32-seat flash call, 23/23 reports. Report:
`.ufo/round-10/chousa-goalwave.md`.

**Before**: defect classes were covered only by small fixtures; the archive
records' exempt items were unaudited; rounds 2-9's named limits had no single
disposition ledger.

**After** (parent acceptance 2026-10-16T07:20Z): six archive-scale controls —
one per class (span-not-found, anchor-missing, rejection-missing-flip,
false-sweep, dangling-ref, structure-break), each a minimal scripted byte-edit
of its clean record — every one DRIFTs verify-all with exactly ONE finding
naming its class (parent re-ran all six verbatim); the clean records stay
CLEAN; the exempt audit justified every exemption against source bytes;
`corpus/knowledge/hardening-r10.md` carries the complete r2-r9 limit
disposition ledger. Gate byte-unchanged (the round's standing rule held).
Named non-coverage: `RECORD_SCHEMA_INVALID` cannot fire alone (it drags
companion structural findings) — documented in the controls README.

| axis | verdict | evidence (before → after) |
|---|---|---|
| calibration | **improved** | the tool's trust is now earned at archive scale: six classes, one finding each, parent-reproduced; every r2-r9 limit dispositioned in one ledger. |
| coverage | **improved** | negative controls at the scale the lane actually verifies. |
| depth | **improved** | `hardening-r10.md` = the audit map; the schema-invalid non-coverage documented. |
| operability | **unchanged** | selftest 85/85; gate unchanged; `GATE_DRIFT: none` held. |
| freshness | **unchanged** | receipts at the current SHA. |
| adjacency | **unchanged** | zero network; corpus read-only; quota held. |

Admission: **ADMIT** (calibration/coverage/depth improved, none harmed). No
scalar score. Learning trends: expansion/quality **improved**, discernment
**unchanged**. Round 11 registered (capstone): the chousa deep audit —
evidence chains, receipt integrity, verdict consistency, limit-ledger
reconciliation, SHONEN readiness, and re-execution of the load-bearing claims.

## Round 11 verdict — 2026-10-16 (capstone audit; evidence commit `2e414ec`)

Selected axis: **calibration** — deep discernment: the chousa capstone audit,
the lane's final goal round. Wave: one 32-seat flash call, 31/31+ reports.
Report: `.ufo/round-11/chousa-goalwave.md`; consolidated findings:
`corpus/knowledge/audit-r11.md`.

**What the audit confirmed (measured, re-executed):** round 2's entire
evidence chain re-runs at the frozen bytes and matches (15/15 claims
supported: commits resolve, receipt SHAs match, the 17/17 CLEAN, the boundary
refusals, strace-zero-network); the per-round auditors verified rounds 2-10's
chains; the battery at today's bytes: selftest 85/85, `GATE_DRIFT: none`,
all fixtures/records/controls reproducing their verdicts; the gate
byte-unchanged through the round.

**Corrections folded at admission:** (1) the wave-seat-count claims in earlier
reports ("24/24", "32/32") are **unverifiable without wave rosters** — my
in-session swarms leave no fleet `.ufo/waves/` roster; the audit could only
verify the ARTIFACTS, not the roster claims — recorded, and future rounds
should log seat rosters; (2) `audit-r11.md` §5/§7 carries the record-text
defects with `[PARENT]` markers and recommended moves; (3) SHONEN: 0/4, hold
promotion — readiness assessed without self-attestation (same conclusion as
the sibling lane).

| axis | verdict | evidence |
|---|---|---|
| calibration | **improved** | the lane knows with measured coverage what is verified (chains re-executed at frozen bytes; receipts match; limits reconciled) and what is not (roster claims, operator-side receipt identity). |
| depth | **improved** | `audit-r11.md`: findings tables, the final debt register, SHONEN readiness, operator recommendations. |
| coverage / operability / freshness / adjacency | **unchanged** | the audit measured the measuring; battery green; gate untouched. |

Admission: **ADMIT-with-correction** (calibration/depth improved; corrections
named; none harmed). No scalar score. Learning trends: expansion/quality
**improved**, discernment **improved** (the audit is the lane's first
discernment-product round, externally probed). chousa rounds 2-11: ten
admitted rounds — the goal's second half complete.

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| — none yet — | | | |

Rows enter only through a round that demonstrates the capability running (`AXES.md` §Capabilities); none enter through this rollout.

## Saturation

Saturation line: **8.0 on this Scorecard's six axes** (0–10 scale; a threshold,
never a score). Rationale: fleet precedent `../souji-shokunin/SCORECARD.md:44`
("Saturation line: 8 per axis; stagnation window 3 rounds"); this lane has no
rubric of its own that derives 8.0, and none is claimed.

Stagnation window: **N = 3 landed lane rounds** — rounds that produced an
admitted report, never dispatch attempts (the 2026-10-19 key-1/2 interruptions
and key-3/4/5 402s produced zero reports; LOG.md round-12 opening). Declared
prospectively at round 12 (kotoba reading, `../SCORECARD.md:172-174`): the
Capabilities table entered this file at the 2026-10-16 conformance rollout and
held no row before this round, so the clock starts at this declaration round;
no retroactive window is claimed.

Computability (fail closed) — the `AXES.md` §The stagnation nudge predicate is
decidable from this file alone:
1. "Every axis sits at or above 8.0": operability is the only scored axis — 3
   (round 1, SCORECARD.md:7); the other five are deliberately unscored
   (:9-13; rounds 2–11 all refuse a scalar score). An unscored axis is NOT
   counted as at/above the line, so condition 1 fails.
2. "No capability entered within N=3": three capability rows entered this
   round (below), so the window resets at round 12.
Nudge verdict: **dormant** — the waiver does not apply, the lowest-axis
obligation stands, and by the only recorded score the lowest non-retired axis
is operability, which round 12 claim 2 works. This declaration creates or
changes no axis score and asserts no axis saturated.

## Planned — round 12 (pre-registered 2026-10-19, goal turn 1)

Wave: one 64-seat AgentSwarm call, opencode-go key 1 / deepseek-v4.1-flash (curriculum loop 1, round 1; opencode-go keys rotate between rounds). Seat roster is logged in the round-12 report. Before-receipts (2026-10-19): selftest `PASS (85 cases)` exit 0; `--drift` vs the r8 baseline `GATE_DRIFT: none` exit 0; r1 counting command `VERDICT_BEARING_EXPORTS=3/3`; `grep -c SCOPE_ tools/research-gate.sh` → 0; `VERSION=research-gate-r1` at `tools/research-gate.sh:227`; A-r9.md C3 cites `A-shokunin-tradition.md:76`, span verified at `:86`.

1. **coverage — scope-refusal teeth** (the r1 landing requirement, open since 2026-10-15): the structure check gains a DECLARED-scope screen — only a record's `## Meta` `domain:`/`scope:` row triggers it (prose is never keyword-scanned, so the B archive on multi-agent knowledge cannot trip it); a refused declaration (bounty-program scope → kasegi; model-quality claims → kengaku; orchestration/dispatch → kumitate) emits its named finding — `SCOPE_BOUNTY_ABSORBED` / `SCOPE_MODEL_QUALITY_ABSORBED` / `SCOPE_ORCHESTRATION_ABSORBED` — at warn severity, which drifts (exit 1). One symmetric selftest fixture per province asserting exit 1 + one clean/absent control. Observable: `SCOPE_` emitting sites 0 → 3; selftest 85 → 85+N (N≥4, settled at landing); scope-less records byte-identical (canary: archives-r9 A/B/C + r6/r7 fixtures re-run unchanged).
2. **operability — r2-carried residuals**: (a) `VERSION=research-gate-r1` corrected to a mode-agnostic version string with a selftest case pinning the banner; (b) claim/chain source reads gain a size cap (8 MiB default; oversized source → named refusal `SOURCE_READ_TOO_LARGE`, refused never partially read) with just-under/over boundary fixtures. Observable: selftest grows by the landed case count; every prior case byte-identical (cmp against `corpus/evidence/pin-r8-20261016T033757Z-selftest.log`); `--drift` vs the r8 baseline stays `none` or a re-pin lands with a recorded reason.
3. **calibration — close the r11 open finding**: A-r9.md row C3 citation `:76` → `:86` (span re-verified at `:86` 2026-10-19); `hardening-r10.md` ledger row dispositioned closed; append-only errata to `audit-r11.md` and the ledger naming the superseded text. Observable: the ledger's one open finding → 0 open; verify-all on A-r9 CLEAN at the corrected bytes; no other A/B/C-r9 row carries the same cite-vs-span mismatch (mechanically swept).

Conformance (not an axis claim): §Saturation (SCORECARD.md:469) is amended at this landing to declare the line + window the 2026-10-16 rollout deferred to this round; the declaration creates or changes no axis score.

## Round 12 verdict — 2026-10-19 (goal wave; evidence commits this landing)

Selected claims (pre-registered, SCORECARD.md §Planned — round 12): coverage =
scope-refusal teeth (the r1 landing requirement); operability = the two
r2-carried residuals (banner + source-read size cap); calibration = close the
r11 open finding. Wave: one 64-seat AgentSwarm call on **opencode-go-6 /
deepseek-v4.1-flash** (operator directive: stick with the first working key;
keys 1–2 interrupted pre-report, keys 3/4/5 dead 402 insufficient funds — all
recorded in LOG.md), 64/64 seat reports. Reports: the wave output file
(session tool-results, 64 seats); consolidated verdicts this block. Seat
roster: the round-12 report (`.ufo/reports/round-12/chousa.md`) — the r11
correction (seat counts unverifiable without rosters) is satisfied.

**Before** (gate `46f5ddb3…`, re-measured 2026-10-19 after the /tmp quota
unblock): `grep -c SCOPE_ tools/research-gate.sh` → 0 (no scope machinery);
`VERSION=research-gate-r1` at `tools/research-gate.sh:227`; no size cap on
claim/chain source reads; the r11 audit's one open finding live (A-r9.md C3
cites `A:76`, span verified at `A:86`); selftest `PASS (85 cases)`;
`GATE_DRIFT: none` vs the r8 baseline; r1 observable `3/3`.

**After** (gate `91a01695…`, selftest `PASS (98 cases)` = 85+13, cases 1–85
byte-identical per `cmp` against `pin-r8-…-selftest.log`):
- scope screen: `scope_decl_screen` reads only `## Meta` rows keyed
  `domain`/`scope` (table + `key: value` forms); refused-province declarations
  emit `SCOPE_BOUNTY_ABSORBED` / `SCOPE_MODEL_QUALITY_ABSORBED` /
  `SCOPE_ORCHESTRATION_ABSORBED` at warn (drift, exit 1), one finding per
  matched province per declaration row; cases 86–92 (3 provinces, both clean
  grammars, declared near-miss, prose decoy). Observable:
  `grep -c 'id=SCOPE_' tools/research-gate.sh` → 3 (the three emitting
  assignments; the pre-registered bare `grep -c SCOPE_` over-counts header/
  fixture mentions after documentation — amendment recorded, conformance
  reviewer D3); canary: `verify B-r9 --root ..` → 0 `SCOPE_` findings.
- banner: `VERSION=v2` (revision token alone; six banner sites), pinned by
  cases 93–94 (literal + `GATE_DRIFT: GATE` mutant arm). Forced consequence,
  pre-registered: `--drift` vs the r8 baseline reads `GATE_DRIFT: GATE
  record_sha256` exit 1 (version token + the pin fixture's new clean domain
  row, both unmasked by design); ONE recorded re-pin at final bytes:
  `corpus/evidence/gate-baseline-r12-20261019T115519Z.json`, `GATE_DRIFT:
  none` at pin time.
- size cap: `SOURCE_READ_MAX_BYTES` = 8 MiB (inclusive) at the shared
  `claim_source_path` chokepoint (claims + chain + verify-all claims binding);
  `CLAIM_SOURCE_READ_TOO_LARGE` / `CHAIN_SOURCE_READ_TOO_LARGE` (warn),
  refused before any read — the pre-registered bare id `SOURCE_READ_TOO_LARGE`
  was namespaced to the mode idiom (amendment recorded, seats 18/36); cases
  95–98 straddle 8388608/8388609 with the over-cap span on line 1 (a partial
  read would have matched — `observed=refused at=-` proves it was never
  searched). Companion deviation (recorded): `count_nl` was quadratic
  (>60 s at 8 MiB — the cap would be operability theatre); now linear via
  `tr -dc '\n' | wc -c` (~3 ms), behavior-identical.
- A-r9 C3: pointer `:76` → `:86` (one cell; new sha `dfd2ae1a…` exactly as
  the wave predicted); post-fix `verify-all` CLEAN (receipt
  `scope-r12-20261019T115519Z-A-fix.log`); parent re-sweep 19/19; the two
  A-derived controls stay byte-copies of the pre-fix base (desync note in
  `controls/README.md`); append-only errata to `audit-r11.md` and
  `hardening-r10.md` §6 (rows 9/10/56/70 dispositioned; 71 rows now
  38·23·7·0·3, queue 26); the class (pointer-line vs span-line) stays a named
  non-coverage.
- battery: r1 `3/3`; selftest PASS; fixture battery (A/B/C-r9, r6 trio, r7
  pair, claims-r2, chain-r3, sweeps-r5, six controls) byte-identical vs the
  pre-round gate modulo the masked banner/ts (receipt
  `scope-r12-20261019T115519Z-battery.log`); zero network throughout.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the r1 scope-teeth requirement lands: declared out-of-province scope is verdict-bearing (0 emitting sites → 3; 7 selftest cases; B-archive canary clean); A-r9's corpus is corrected (19/19 cite-vs-span) |
| operability | **improved** | selftest 85 → 98 with 1–85 byte-identical; the two r2-carried residuals land (banner pinned by a drift arm; 8 MiB cap with boundary + never-partially-read teeth); `count_nl` linear; re-pin battery green at HEAD |
| freshness | **improved narrowly** | the lane's behavioral baseline is re-pinned at the round's final bytes with the reason recorded; the stale A-r9 pin cascade (2 READMEs, 2 notes, index) is corrected same-commit |
| depth | **improved** | `corpus/knowledge/scope-refusal-r12.md` (contract, phrase lists, not-triggers, disposition rule, limits) + `gate-baseline-r12.md` (re-pin reason) |
| calibration | **unchanged (debt closure, per the wave reviewers)** | the finding closed is bookkeeping the r11 audit already surfaced; the gate stays blind to the class (pointer-line vs span-line), now a named non-coverage; claiming "improved" here would double-count the audit's discernment (seats 45/56) |
| adjacency | **unchanged** | the screen ROUTES to kasegi/kengaku/kumitate rather than absorbing; zero network; fleet research corpus read-only; no sibling files touched (the MANIFEST/L0 appends are integrator-queue rows, recorded below) |

Honest residuals (named by the wave, dispositioned): solo verify-claims/
chain/sweeps/integrity modes lack scope teeth (enforcement via verify/
verify-all only); declaration-only detection cannot catch undeclared absorbed
scope; negations unparsed; record + claims-surface reads uncapped (row 9
partial); unmeasurable-size stat failure silently bypasses the cap
(documented); the pin baseline covers only the canonical invocation (a
pattern-widening regression outside the clean-path fixture stays invisible —
the r12 pin fixture's domain row closes this for the screen itself).
Admission: **ADMIT** (coverage/operability/freshness/depth improved;
calibration unchanged as debt-closure; none harmed). No scalar score.
Learning trends: expansion **improved** (two knowledge notes, three
capability rows, seven receipt files), quality **improved** (corrections
sweep across SKILL/corpus README/notes; errata append-only), discernment
**unchanged** (L2 reviews remain author-lane evidence; no non-author
spot-check exists). Round 13 registered: closure of the last r2 residual —
in-root hardlink canonicalization (ledger row 8) — plus receipt-runbook
automation if the operator answers the re-filed receipt-identity L0 row.

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| scope-refusal screening | refuses declared out-of-province scope (`## Meta` domain/scope rows) with three named warn findings, exit 1 | selftest cases 86–92; `corpus/knowledge/scope-refusal-r12.md` | 12 |
| source-read size cap | refuses claim/chain sources over 8 MiB before any read, never partially searched | selftest cases 95–98 | 12 |
| banner drift contract | the version token is non-volatile; renaming it drifts the baseline (`GATE_DRIFT: GATE`) | selftest cases 93–94 | 12 |

## Planned — round 13 (pre-registered 2026-10-19)

Wave per the curriculum (loop 1, round 2): one 64-seat AgentSwarm call,
**opencode-go-6 / deepseek-v4.1-flash** (standing operator directive: stick
with key 6 until it fails). Registered claim: **operability/coverage — in-root
hardlink canonicalization** (ledger row 8, the last open r2 residual): a
claims/chain source reachable in-root via a hardlink alias is canonicalized
to its inode-true path (or refused), so the r2 critic's bypass class closes;
before: `grep -c samefile tools/research-gate.sh` → 0 with a demonstrated
bypass; after: bypass refused/canonicalized + symmetric selftest fixtures +
hold battery green. Secondary (only if the operator answers the L0 row):
receipt-runbook automation. Seats: 64, roster logged in the round-13 report.

## Round 13 verdict — 2026-10-19 (goal wave; evidence commit this landing)

Selected claims (SCORECARD.md §Planned — round 13): coverage = close the last
r2 residual (ledger row 8), the in-root hardlink canonicalization bypass;
depth = the alias-semantics knowledge note + SKILL sweep. Wave: one 64-seat
AgentSwarm call on opencode-go-6 / deepseek-v4.1-flash, 64/64 seat reports
(roster: the round-13 report). The wave BLOCKed partner enumeration as
unsound (two independent seats) and the reviewers re-scoped the claim: the
landing is a one-probe `nlink != 1` refusal — the HARDLINK class closes; bind
mounts, TOCTOU and legit in-root families are named limits, not silently
closed.

**Before** (gate `91a01695…`, re-measured at opening `0b0a133`): no inode
logic (`grep -c samefile tools/research-gate.sh` → 0); 0 multi-linked files
across corpus/tools/research (so no fixture could perturb); the bypass live:
a claim through an in-root hardlink alias of an out-of-root file read
`observed=supported` CLEAN (receipt `alias-r13-20261019T123621Z-bypass-before.log`);
selftest 98; drift none vs the r12 baseline; r1 3/3.

**After** (gate `6b17e50cc9b61dda…`, selftest `PASS (102 cases)` = 98+4,
cases 1–98 `cmp` byte-identical vs `scope-r12-…-selftest.log`): one
`stat -c '%s %h'` probe at the shared `claim_source_path` chokepoint (claims,
chain, verify-all's claims binding alike) refuses `nlink != 1` unread —
`CLAIM_SOURCE_MULTILINKED` / `CHAIN_SOURCE_MULTILINKED`, crit, per-item
`observed=refused`; the same probe serves the r12 size cap unchanged. Cases
99–102: claims-alias refused, chain-alias refused (CHAIN id + crit severity
arms), in-root two-alias family refused (case 101 pins the named trade),
single-link control CLEAN. Bypass after: crit refusal (receipt
`-bypass-after.log`). Battery: r1 3/3; drift `none` vs the r12 baseline (no
re-pin — the canonical invocation is unchanged); masked battery (banner/ts)
vs the pre-round gate with LANE_ROOT intact (temp copy inside `tools/` —
the /tmp-copy form breaks lane-root-relative pointers, a recorded method
artifact): A/B/C-r9, full-r6, integrity-r7, claims-r2, chain-r3, sweeps-r5,
six controls ALL IDENTICAL (receipt `alias-r13-20261019T123621Z-battery.log`).

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the r2 bypass class is closed at the one content-read chokepoint: before CLEAN `1/1` on an out-of-root alias → after crit refusal `0/1` (both live receipts); 4 symmetric cases |
| operability | **improved** | selftest 98 → 102 with 1–98 byte-identical; one probe serves two checks (no double stat); no re-pin needed; the gate's failure modes refuse rather than read |
| depth | **improved** | `corpus/knowledge/hardlink-alias-r13.md`: the symlink/hardlink asymmetry, the refusal semantics, why enumeration was rejected, four named limits; lesson `2026-10-19-hardlink-alias-boundary.md` |
| freshness | **improved narrowly** | the r12-baseline drift check stays green at the r13 gate (behavior-pinned); the r2-residual documentation chain (ledger row 8, corpus README, 5 note dispositions) is corrected same-landing |
| calibration | **unchanged** | the claim was honestly narrowed by the wave (hardlink class only; bind mounts/TOCTOU/families named); no overclaim made or admitted |
| adjacency | **unchanged** | zero network; read-only wave; sweeps confirmed content-free (no scope creep into sweeps mode); no sibling/fleet writes beyond the recorded MANIFEST/L0 queue rows |

Admission: **ADMIT** (coverage/operability/depth/freshness improved; none
harmed; the case-101 family refusal is a pinned, documented trade, not a
hidden one). No scalar score. Learning trends: expansion improved (note +
lesson + capability row + 4 receipts), quality improved (battery artifact
recorded; errata append-only), discernment unchanged. Round 14 registered:
curriculum round 3 (zai glm-5.3-flash per the curriculum; key 6 fallback if
zai is out); claim TBD from the named-limit queue (bind-mount boundary or
receipt-runbook automation), pre-registered at the round-14 opening.

## Capabilities (addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| hardlink-alias refusal | refuses multi-linked claim/chain sources unread before any read | selftest cases 99–102; `corpus/knowledge/hardlink-alias-r13.md` | 13 |

## Round 14 verdict — 2026-10-19 (goal wave; evidence commit this landing)

Selected claims (LOG.md round-14 opening): coverage/operability = the
mount-alias (bind) boundary — refuse sources whose st_dev differs from the
resolving root's device; depth = the mount/alias note + registry sweep.
Wave: one 64-seat AgentSwarm call on **alibaba-token-plan /
deepseek-v4.1-flash** (operator directive: token-plan lanes for the
deepseek-v4.1-flash waves), 63/64 seat reports — seat 54 (OverflowScout)
failed on a provider content-filter 400; the deficit is recorded here and in
the report, not backfilled. The wave validated the fixture unprivileged on
this host (user+mount namespace tmpfs forge; a repo bind inside the ns is
refused, rc=2, measured) and BLOCKed the mount-free "absolute-path"
fallback as unsound.

**Before** (gate `6b17e50c…`): `grep -c CROSS_DEVICE tools/research-gate.sh`
→ 0; device logic absent; the bypass live — a tmpfs mounted over an in-root
dir read `observed=supported` CLEAN (receipt
`mount-r14-20261019T132025Z-bypass-before.log`); selftest 102; drift none vs
the r12 baseline; r1 3/3.

**After** (gate `d8bbd0bf…`, selftest `PASS (106 cases, 0 skipped)`,
cases 1–102 `cmp` byte-identical): the chokepoint tracks the RESOLVING root
(longest prefix — a ROOT-only compare would false-refuse the live sweeps-r5
S4 lane-fallback and the selftest itself, devices 57 vs 30 measured), one
`stat -c '%s %h %d'` probe serves nlink → size → device (a combined source
reports the earliest class), refusing `CLAIM_SOURCE_CROSS_DEVICE` /
`CHAIN_SOURCE_CROSS_DEVICE` (crit) unread. Cases 103–106: ns-mounted
claims/chain refusal, same-device true-positive control, and the
lane-fallback control that defeats a naive implementation. Bypass after:
crit refusal (receipt `-bypass-after.log`). Battery: r1 3/3; drift `none`
vs the r12 baseline (no re-pin); masked battery vs the pre-round gate
(LANE_ROOT intact) ALL IDENTICAL (receipt `mount-r14-20261019T132025Z-battery.log`).

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the bind-alias class is closed at the one content-read chokepoint: before CLEAN `1/1` on a mounted alias → after crit refusal `0/1`, both live; claims + chain + verify-all binding refuse alike |
| operability | **improved** | selftest 102 → 106 (1–102 byte-identical); one probe serves three checks; namespace fixtures run unprivileged with zero host residue; no re-pin |
| depth | **improved** | `corpus/knowledge/mount-alias-r14.md`: the bind gap, the resolving-root rule, the probe order, and five measured named limits (same-device binds, overlay roots, TOCTOU, unmeasurable-stat, legit subtree trade) + the discovered `--root /` dead-arm (queued) |
| freshness | **unchanged** | the r12 baseline holds unchanged (no re-pin needed); no stale pins moved this round |
| calibration | **improved narrowly** | the claim landed exactly as narrowed (cross-device only) with the same-device-bind limit stated verbatim; the unsound mount-free fixture was BLOCKed, not fudged; the seat-54 deficit is recorded, not backfilled |
| adjacency | **unchanged** | zero network; sweeps' unclaimed glob surface named as a limit, not absorbed; no sibling/fleet writes beyond the recorded queue rows |

Admission: **ADMIT** (coverage/operability/depth/calibration(narrow)
improved; none harmed). No scalar score. Learning trends: expansion
improved, quality improved, discernment unchanged. Round 15 registered:
curriculum round 4 — **zai glm-5.3-flash**, 32–64 seats (fallback ladder per
the standing directives: token-plan deepseek → devin deepseek → opencode-go-
6); claims from the r14 queue (the `--root /` boundary dead-arm fix and/or
the same-device-bind mountinfo candidate), pre-registered at the round-15
opening.

## Capabilities (addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| cross-device refusal | refuses sources whose st_dev differs from the resolving root's device (bind aliases) | selftest cases 103–106; `corpus/knowledge/mount-alias-r14.md` | 14 |

## Round 15 verdict — 2026-10-19 (goal wave; evidence commit this landing)

Selected claims (LOG.md round-15 opening): coverage/operability = the
`--root /` boundary dead-arm (r14 discovery): `"$root_r"/*` renders `//*`
when the root resolves to `/`, matching nothing, so every absolute in-`/`
source refuses `CLAIM_SOURCE_OUT_OF_CORPUS` crit; depth = the
root-normalization note + registry sweep. Wave: one 48-seat AgentSwarm call
on **zai glm-5.3-flash** (curriculum loop 1, round 4), 48/48 seat reports.
Seat roster: the round-15 report.

**Before** (gate `d8bbd0bf…`, selftest 106): the prefix tests at
`tools/research-gate.sh:1051/:1055` (claims chokepoint), `:548`
(`ptr_resolves_meta`), and `:1742` (sweeps resolver) all render `//*` under
`--root /`. A claim citing `/etc/hostname` (dev 31 = `stat -c %d /`, nlink 1,
9 B — a legitimate read) refuses `OUT_OF_CORPUS` crit (receipt
`root-r15-20261019T152000Z-demo.log`, before half). Selftest `PASS (106
cases, 0 skipped)`; drift `none` vs the r12 baseline; r1 `3/3`.

**After** (gate `dd0951d7…`, selftest `PASS (110 cases, 0 skipped)`, cases
1–106 `cmp` byte-identical vs `mount-r14-20261019T132025Z-selftest.log`): the
`in_root()` helper (`tools/research-gate.sh` ~:612) strips the trailing slash
for the prefix test only — `${r%/}` on `/` yields `""`, `""/*` renders `/*`,
which matches `/` and every descendant. All three same-class sites converted
(`claim_source_path`, `ptr_resolves_meta`, `sweep_path_guarded`); `src_root`
keeps the un-normalized root so the r14 device probe still stats the declared
root. The materialized helper is mandatory — inline
`case "$canon" in "${root_r%/}"/*)` is itself dead when the expansion strips
to empty (measured, bash 5.3.15). Cases 107–110 pin the healed arm:
ghost-missing (`/chousa-r15-absent`), `/etc/hostname` read (span derived
from the file's first line), tmpfs cross-device (`$WORK` dev 57 ≠ 31),
sweeps absolute glob (`/chousa-r15-absent/*.md`). The `CHOUSA_ROOT=` override
rides a new harness channel — six runners gained a `^CHOUSA_[A-Z_]+=`
env-override classifier; `tcase`'s override placement corrected to last-wins.
Receipts `root-r15-20261019T152000Z-{demo,selftest,battery,drift}.log`.
Masked battery vs the pre-round gate: ALL IDENTICAL.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | before `OUT_OF_CORPUS` crit on a legitimate /-root absolute read → after `CLEAN` `1/1` through all three probe arms (receipts live); the `ptr_resolves_meta` and `sweep_path_guarded` same-class sites also healed |
| operability | **improved** | selftest 106 → 110 (1–106 byte-identical); six runners gained the `CHOUSA_`-prefixed env-override channel; no re-pin needed |
| depth | **improved** | `corpus/knowledge/root-slash-boundary-r15.md`: the `//*` glob mechanics (measured), the four-outcome pre-fix table, the `in_root` contract, the 3-site registry, the inline-strip quirk |
| freshness | **unchanged** | the r12 baseline holds unchanged (no re-pin needed — the canonical invocation uses a non-/ temp root where normalization is a no-op); no stale pins moved |
| calibration | **improved narrowly** | the fix landed exactly at the discovered class; the `ptr_resolves_meta` third site was found by this round's own audit, not the pre-registered claim — dispositioned explicitly; the `17 B`→`9 B` stat erratum corrected in receipts |
| adjacency | **unchanged** | zero network; corpus read-only; /-root reads confined to the named fixture paths; no sibling/fleet writes beyond the recorded queue rows |

Admission: **ADMIT** (coverage/operability/depth/calibration(narrow)
improved; none harmed). No scalar score. Learning trends: expansion
improved, quality improved, discernment unchanged. Round 16 registered:
curriculum round 5 — §Planned below.

## Planned — round 16 (pre-registered 2026-10-19, at the round-15 landing)

Wave per the curriculum (loop 1, round 5): one 64-seat AgentSwarm call,
**gpt-6-luna-max** — a verification wave: adversarially re-audit the current
loop's rounds 1–4 (lane rounds 12–15) for correctness defects and missed
coverage; every finding lands as a dispositioned item (fix, absorb, or named
debt). Provider liveness probed before spending the wave; fallback ladder
per the standing doctrine (devin → token-plan → opencode-go-6), recorded at
the round-16 opening. Claims pre-registered at the round-16 opening from the
named-limit queue: candidates — verify-sweeps' mount-alias-blind glob
surface (r14 note), the same-device-bind mountinfo walk, the overlay-fstype
guard. Seats: 64; roster logged in the round-16 report.

## Round 16 verdict — 2026-10-19 (goal wave; evidence commit this landing)

Selected claims (LOG.md round-16 opening): coverage/calibration =
adversarially re-audit loop-1 rounds 1–4 (lane rounds 12–15) for correctness
defects and missed coverage; every finding lands as a dispositioned item
(fix, absorb, or named debt). Wave: one 64-seat AgentSwarm call on
**openai-codex gpt-6-luna-max**, 64/64 seat reports. Seat roster: the
round-16 report.

**Before** (gate `dd0951d7…`, selftest 110): the boundary stack as landed
through rounds 12–15, unaudited by an independent model. The r15 battery
receipt carried wrong fixture paths (A/B/C-r9 under `corpus/fixtures/` not
`archives-r9/`; `--root .` vs `--root ..`). The `--root //` spelling still
refused in-corpus absolute paths (`in_root` stripped only one `/`).

**After** (gate `2b64a1c8…`, selftest `PASS (111 cases, 0 skipped)`, cases
1–110 `cmp` byte-identical): two fixes landed — `in_root` strips all
trailing slashes (`//` → `/` → `""`, `""/*` renders `/*`); the r15 battery
receipt re-run with correct fixture paths (`archives-r9/`, `--root ..`) and
replaced. ~15 findings absorbed as record corrections (the `wc -c` fallback
pre-read claim, the scope-refusal coverage overstatement, the full-r6
README sweeps-absent claim, the mount-alias "queued" item now closed, the
stale hardlink status in older notes, the hardening-r10 count phantom).
~12 findings named as debt for round 17 (scope-screen fenced-heading
shadow, `LLM benchmarks` phrase gap, sweeps symlink-escape, `--drift`
truncated-baseline ambiguity, `--json` delimiter edge, manifest timestamp
mask breadth, secret-scan source coverage, URI-like citation
classification, `--` delimiter handling, TOCTOU readability, bash-3
portability, 8 unasserted finding IDs). The full disposition table is
`corpus/knowledge/verification-r16.md`.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **unchanged** | the audit found no out-of-corpus read; two fixes landed (`--root //` healed, battery receipt corrected) but the boundary's refusal classes are unchanged — the wave verified coverage, it did not expand it |
| operability | **improved** | selftest 110 → 111 (1–110 byte-identical); the `//` edge is now pinned; the battery receipt is honest |
| depth | **improved** | `corpus/knowledge/verification-r16.md`: the full disposition table with seat citations; the `wc -c` pre-read correction; the corrected battery |
| freshness | **unchanged** | the r12 baseline holds (no re-pin); no stale pins moved |
| calibration | **improved** | the audit measured every claim against live behavior; the `//` defect was found because the wave tested what the r15 note claimed but didn't verify; every finding has a named disposition |
| adjacency | **unchanged** | zero network; corpus read-only; no sibling/fleet writes beyond the recorded queue rows |

Admission: **ADMIT** (operability/depth/calibration improved; none harmed).
No scalar score. Learning trends: expansion improved, quality improved,
discernment improved. Round 17 registered: curriculum round 6 —
§Planned below.

## Planned — round 17 (pre-registered 2026-10-19, at the round-16 landing)

Wave per the curriculum (loop 1, round 6): one 32–64-seat AgentSwarm call,
**xai-oauth grok-4.7-fast**. Claims pre-registered at the round-17 opening
from the named-debt queue: candidates — the scope-screen fenced-heading
shadow fix, the `LLM benchmarks` phrase gap, the sweeps symlink-escape
guard, the `--drift` truncated-baseline detection. Seats: 32–64; roster
logged in the round-17 report.

## Round 17 verdict — 2026-10-19 (goal wave; evidence commit this landing)

Selected claims (LOG.md round-17 opening): coverage/operability = fix the
scope-screen fenced-heading shadow (round-16 named debt): `load_sections`
resets on every `## ` line without recognizing fenced code blocks, so a
fenced `## Meta` shadows the real declaration — the scope screen checks the
wrong body. depth = the fenced-heading mechanics note + the `LLM
benchmarks` phrase-gap disposition. Wave: one 32-seat AgentSwarm call on
**opencode-go / deepseek-v4.1-flash** (fallback from xai-oauth 403 — all
48 seats failed on quota; provider deviation recorded in LOG.md), 27/32
seat reports (5 failed on provider 400 `reasoning_content` errors; deficit
recorded, not backfilled). Seat roster: the round-17 report.

**Before** (gate `2b64a1c8…`, selftest 111): `load_sections` splits on every
`## ` line — a fenced `## Meta` inside a code block resets the real Meta
body. A record whose real Meta declares `domain: bounty program scope` but
carries a fenced `## Meta` with `domain: deep-research method` passes
CLEAN (receipt `fence-r17-20261019T171200Z-demo.log`, before half).

**After** (gate `c2915f24…`, selftest `PASS (116 cases, 0 skipped)`, cases
1–109 `cmp` byte-identical vs the r15 receipt — r16 inserted case 110, so
the cmp boundary is 109): `load_sections` pairs fences in two passes —
same char must close, closing length >= opening, 0–3 literal-space indent;
an unclosed opener IS a fence (fail closed — everything after it is
literal). Cases 112–116 pin the five shadow variants: simple shadow,
fenced-only phantom (no real Meta → CLEAN by the declaration-only
contract), nested 4-backtick, indented closer, unclosed fence. The naive
`^``` ` toggle fixes only the simple shadow (measured shape matrix in
`corpus/knowledge/fenced-heading-r17.md`). Masked battery vs the
pre-round gate: ALL IDENTICAL. Drift `none` vs the r12 baseline (no
re-pin); r1 `3/3`.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the fenced-heading shadow class is closed at the parser: before CLEAN on a shadowed refused domain → after `SCOPE_BOUNTY_ABSORBED` warn + DRIFT (receipts live); five variants pinned |
| operability | **improved** | selftest 111 → 116 (1–109 byte-identical); two-pass fence pairing is deterministic; no re-pin needed |
| depth | **improved** | `corpus/knowledge/fenced-heading-r17.md`: the shadow mechanics, the naive-vs-two-pass shape matrix, the call-site audit, the named limits |
| freshness | **unchanged** | the r12 baseline holds (no re-pin); no stale pins moved |
| calibration | **improved narrowly** | the fix landed at the discovered class only; the `LLM benchmarks` phrase gap stays named debt (not silently absorbed); the provider fallback is recorded, not hidden |
| adjacency | **unchanged** | zero network; corpus read-only; no sibling/fleet writes beyond the recorded queue rows |

Admission: **ADMIT** (coverage/operability/depth/calibration(narrow)
improved; none harmed). No scalar score. Learning trends: expansion
improved, quality improved, discernment improved. Round 18 registered:
curriculum round 7 — §Planned below.

## Planned — round 18 (pre-registered 2026-10-19, at the round-17 landing)

Wave per the curriculum (loop 1, round 7): one 16–32-seat AgentSwarm call,
**zai glm-5.3-flash** (fallback ladder per the standing doctrine: devin →
token-plan → opencode-go-6). Claims pre-registered at the round-18 opening
from the named-debt queue: candidates — the `LLM benchmarks` phrase gap,
the sweeps symlink-escape guard, the `--drift` truncated-baseline
detection, the fenced-data-row `approved` suppression. Seats: 16–32;
roster logged in the round-18 report.

## Round 18 verdict — 2026-10-19 (goal wave; evidence commit this landing)

Selected claims (LOG.md round-18 opening): coverage = close the `LLM
benchmarks` phrase gap (round-16 named debt): `SCOPE_KENGAKU` has `model
benchmark(s)` but not `llm benchmark(s)`/`llm scoring`/`ai benchmark(s)` —
a record declaring `domain: LLM benchmarks` passes CLEAN despite the
model-quality boundary. operability = the phrase-gap selftest cases. Wave:
one 16-seat AgentSwarm call on **openai-codex gpt-6-luna-max** (zai glm-5.3-
flash quota exhausted; operator directed codex luna max for all zai-assigned
rounds until tomorrow), 16/16 seat reports. Seat roster: the round-18
report.

**Before** (gate `c2915f24…`, selftest 116): `SCOPE_KENGAKU` has `model
benchmark(s)` and `model scoring` but not `llm benchmark(s)`/`llm
scoring` — a record declaring `domain: LLM benchmarks` passes CLEAN
(receipt `scope-r18-20261019T173000Z-demo.log`, before half).

**After** (gate `6e694881…`, selftest `PASS (119 cases, 0 skipped)`, cases
1–116 `cmp` byte-identical vs the r17 receipt): `SCOPE_KENGAKU` gains `llm
benchmark|llm benchmarks|llm scoring` — the conservative 3-phrase set the
wave's adversary seats validated. `ai benchmark(s)` stays named debt (too
broad — "AI benchmark methodology research" is not model-quality scope).
The plural form needs a separate entry (`scope_hit` matches literal phrases,
never stems). Cases 117–119 pin the new phrases (llm-benchmarks refusal,
llm-scoring refusal, prose-only control CLEAN). Masked battery vs the
pre-round gate: ALL IDENTICAL. Drift `none` vs the r12 baseline; r1 `3/3`.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the `llm benchmark(s)`/`llm scoring` gap is closed: before CLEAN on `domain: LLM benchmarks` → after `SCOPE_MODEL_QUALITY_ABSORBED` warn + DRIFT (receipts live) |
| operability | **improved** | selftest 116 → 119 (1–116 byte-identical); the plural-form rule (literal-phrase match, no stemming) is now pinned |
| depth | **improved** | `corpus/knowledge/scope-phrase-gap-r18.md`: the gap mechanics, the conservative-vs-broad fix boundary, the audit's other inflection findings dispositioned |
| freshness | **unchanged** | the r12 baseline holds (no re-pin); no stale pins moved |
| calibration | **improved narrowly** | the fix landed exactly the validated set (3 phrases, not 5 — `ai benchmark(s)` kept as named debt per the wave's adversary measurement); the provider deviation (zai → luna) is recorded |
| adjacency | **unchanged** | zero network; corpus read-only; no sibling/fleet writes beyond the recorded queue rows |

Admission: **ADMIT** (coverage/operability/depth/calibration(narrow)
improved; none harmed). No scalar score. Learning trends: expansion
improved, quality improved, discernment improved. Round 19 registered:
curriculum round 8 — §Planned below.

## Planned — round 19 (pre-registered 2026-10-19, at the round-18 landing)

Wave per the curriculum (loop 1, round 8): one 16–32-seat AgentSwarm call,
**openai-codex gpt-6-luna-max** (zai exhaustion directive). Claims
pre-registered at the round-19 opening from the named-debt queue:
candidates — the `ai benchmark(s)` boundary decision, `bug bounties`/
`dispatch mechanisms`/`llm evaluations` inflection gaps, the sweeps
symlink-escape guard, the `--drift` truncated-baseline detection, the
fenced-data-row `approved` suppression, the 8 unasserted finding IDs.
Seats: 16–32; roster logged in the round-19 report.

## Round 19 verdict — 2026-10-19 (goal wave; evidence commit this landing)

Selected claims (LOG.md round-19 opening): coverage/operability = the
sweeps symlink-escape guard (round-16 named debt): `sweep_path_guarded`
canonicalizes the glob's BASE but not each match, so a wildcard inside an
in-root dir can match a symlink whose target is outside the allowed roots.
depth = the symlink-escape mechanics note + the remaining named-debt
dispositions. Wave: one 16-seat AgentSwarm call on **openai-codex
gpt-6-luna-max** (zai exhaustion directive), 16/16 seat reports. Seat
roster: the round-19 report.

**Before** (gate `6e694881…`, selftest 119): the guard canonicalizes only
the glob's base — `dir/*.md` matching an outside leaf symlink or
`dir/*/*.md` traversing an outside dir symlink reports `SWEEP_CLAIM_FALSE`
hit, not a boundary refusal (receipt `symlink-r19-20261019T174500Z-demo.log`,
before half).

**After** (gate `9f163807…`, selftest `PASS (122 cases, 0 skipped)`, cases
1–119 `cmp` byte-identical vs the r18 receipt): `verify_sweeps` now
canonicalizes every glob match and refuses the whole sweep if any match
resolves outside both allowed roots — `SWEEP_LOCATION_OUT_OF_CORPUS` crit,
`observed=refused`, no match paths reported. Cases 120–122 pin the escape
class (outside leaf symlink, outside dir symlink, in-root symlink control
unaffected). Masked battery vs the pre-round gate: ALL IDENTICAL. Drift
`none` vs the r12 baseline; r1 `3/3`.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the symlink-escape class is closed at the match level: before `SWEEP_CLAIM_FALSE` hit on an outside symlink → after `SWEEP_LOCATION_OUT_OF_CORPUS` crit + refused (receipts live) |
| operability | **improved** | selftest 119 → 122 (1–119 byte-identical); per-match canonicalization is deterministic; no re-pin needed |
| depth | **improved** | `corpus/knowledge/sweep-symlink-r19.md`: the escape mechanics (leaf + dir shapes), the fix contract, the named limits (post-expansion check, TOCTOU) |
| freshness | **unchanged** | the r12 baseline holds (no re-pin); no stale pins moved |
| calibration | **improved narrowly** | the fix landed at the discovered class only (match-level, not the guard's base contract); the remaining named debts are recorded |
| adjacency | **unchanged** | zero network; corpus read-only; no sibling/fleet writes beyond the recorded queue rows |

Admission: **ADMIT** (coverage/operability/depth/calibration(narrow)
improved; none harmed). No scalar score. Learning trends: expansion
improved, quality improved, discernment improved. Round 20 registered:
curriculum round 9 — §Planned below.

## Planned — round 20 (pre-registered 2026-10-19, at the round-19 landing)

Wave per the curriculum (loop 1, round 9): one 64–128-seat AgentSwarm call,
**openai-codex gpt-6-luna-max** (zai exhaustion directive). Claims
pre-registered at the round-20 opening from the named-debt queue:
candidates — the `ai benchmark(s)` boundary decision, `bug bounties`/
`dispatch mechanisms`/`llm evaluations`/`llmbenchmark`/`language model
benchmark(s)` inflection gaps, the `--drift` truncated-baseline detection,
the fenced-data-row `approved` suppression, the 8 unasserted finding IDs,
the secret-scan source coverage gap, the `--json` delimiter edge, the
manifest timestamp mask breadth, bash-3 portability. Seats: 64–128; roster
logged in the round-20 report.

## Round 20 verdict — 2026-10-19 (goal wave; evidence commit this landing)

Selected claims (LOG.md round-20 opening): coverage/calibration =
adversarially re-audit the expanded boundary stack (rounds 15–19's fixes)
for correctness defects, missed coverage, and interactions. operability =
the audit's own receipts + any fixes that land. Wave: one 64-seat AgentSwarm
call on **openai-codex gpt-6-luna-max** (zai exhaustion directive), 64/64
seat reports. Seat roster: the round-20 report.

**Before** (gate `9f163807…`, selftest 122): the boundary stack as landed
through rounds 15–19. The wave found a new same-class defect the r17 fix
missed: `load_sections` has no HTML-comment state — a `## Meta` inside
`<!-- -->` still shadows the real Meta (live demo: pre-round gate → CLEAN;
landed → `SCOPE_BOUNTY_ABSORBED` + DRIFT; receipt
`verify-r20-20261019T180000Z-demo.log`).

**After** (gate `49b36759…`, selftest `PASS (124 cases, 0 skipped)`, cases
1–119 `cmp` byte-identical vs the r18 receipt): `load_sections` now tracks
`in_comment` alongside `fence_char` — comment state checked after fence
state, before heading; a `## ` inside `<!-- -->` is literal. Case 124 pins
the HTML-comment arm. The wave's other findings dispositioned: the
`ptr_resolves_meta` boundary gap (relative paths check `-f` without
canonicalization — `..` traversal and symlinks escape), the denylist
bypass (`.config/foo` at path start misses `*/.config/*`; benign symlink
to `.config` target passes), the fenced-heading anchor (chain `heading`
anchors match headings inside fences), and ~10 more scope/inflection gaps
(`workflow dispatch`, `security bounty`, `vulnerability disclosure`,
`responsible disclosure`, `bug bounties`, `llm evaluations`, `dispatch
mechanisms`, `language model benchmark(s)`, `llmbenchmark`, `ai
benchmark(s)`) — all named debt for round 21. The uncommitted
`tok_span_at` performance rewrite (grep PCRE — fixes a 240s stall on
8MiB sources) and `claims-cap-eof` case 123 from a prior session are
absorbed and recorded. Masked battery vs the pre-round gate: ALL
IDENTICAL. Drift `none` vs the r12 baseline; r1 `3/3`.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the HTML-comment shadow class is closed at the parser: before CLEAN on a shadowed refused domain → after `SCOPE_BOUNTY_ABSORBED` warn + DRIFT (receipts live); the wave confirmed no out-of-corpus read |
| operability | **improved** | selftest 122 → 124 (1–119 byte-identical); the `tok_span_at` rewrite lands a measured performance fix; case 124 pins the new arm |
| depth | **improved** | `corpus/knowledge/html-comment-r20.md`: the shadow class generalized (fence → comment), the fix contract, the named limits |
| freshness | **unchanged** | the r12 baseline holds (no re-pin); no stale pins moved |
| calibration | **improved narrowly** | the fix landed at the discovered class only; the `ptr_resolves_meta` and denylist findings are named debt, not silently absorbed |
| adjacency | **unchanged** | zero network; corpus read-only; no sibling/fleet writes beyond the recorded queue rows |

Admission: **ADMIT** (coverage/operability/depth/calibration(narrow)
improved; none harmed). No scalar score. Learning trends: expansion
improved, quality improved, discernment improved. Round 21 registered:
curriculum round 10 — §Planned below.

## Planned — round 21 (pre-registered 2026-10-19, at the round-20 landing)

Wave per the curriculum (loop 1, round 10): one 32–64-seat AgentSwarm call,
**devin deepseek-v4.1-flash** (fallback ladder per the standing doctrine:
opencode-go-6 → token-plan → devin). Claims pre-registered at the round-21
opening from the named-debt queue: candidates — the `ptr_resolves_meta`
boundary gap, the denylist `.config` bypass, the fenced-heading anchor
false-positive, the `ai benchmark(s)` boundary decision, the `bug
bounties`/`dispatch mechanisms`/`llm evaluations`/`workflow dispatch`/
`security bounty`/`vulnerability disclosure`/`responsible disclosure`/
`language model benchmark(s)`/`llmbenchmark` inflection gaps, the `--drift`
truncated-baseline detection, the fenced-data-row `approved` suppression,
the 8 unasserted finding IDs, the secret-scan source coverage gap, the
`--json` delimiter edge, the manifest timestamp mask breadth, bash-3
portability. Seats: 32–64; roster logged in the round-21 report.

## Round 21 verdict — 2026-10-19 (goal wave; evidence commit this landing)

Selected claims (LOG.md round-21 opening): coverage/operability = the
`ptr_resolves_meta` boundary gap (round-20 named debt): relative pointer
paths check `-f` without canonicalization — `..` traversal and symlinks
escape. depth = the pointer-boundary mechanics note + the denylist `.config`
bypass disposition. Wave: one 32-seat AgentSwarm call on **opencode-go-6 /
deepseek-v4.1-flash** (devin 502 quota fallback per the standing record),
32/32 seat reports. Seat roster: the round-21 report.

**Before** (gate `49b36759…`, selftest 124): `ptr_resolves_meta` checks
`-f "$ROOT/$f"` or `-f "$LANE_ROOT/$f"` without canonicalization — a
`lib/../../etc/passwd` or a symlink to outside passes if the file exists
under the raw path (live demo: pre-round gate → CLEAN; landed →
`POINTER_UNRESOLVED` warn + DRIFT; receipt `ptr-r21-20261019T184000Z-demo.log`).

**After** (gate `bfc291ef…`, selftest `PASS (128 cases, 0 skipped)`, cases
1–124 `cmp` byte-identical vs the r20 receipt): the candidate is
canonicalized with `readlink -f` (resolving `..` and symlinks), then checked
with `in_root` against BOTH roots. The denylist applies to the canonical
target too — a benign symlink to `.config/passwd` is refused. Cases 125–128
pin the escape class (traversal, symlink, lane-root absolute pointer,
`.config` symlink). Masked battery vs the pre-round gate: ALL IDENTICAL.
Drift `none` vs the r12 baseline; r1 `3/3`.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the pointer-boundary escape class is closed: before CLEAN on a traversal pointer → after `POINTER_UNRESOLVED` warn + DRIFT (receipts live); the `.config` canonical-target check closes the benign-symlink arm |
| operability | **improved** | selftest 124 → 128 (1–124 byte-identical); canonicalization is deterministic; no re-pin needed |
| depth | **improved** | `corpus/knowledge/pointer-boundary-r21.md`: the escape mechanics, the fix contract, the named limits |
| freshness | **unchanged** | the r12 baseline holds (no re-pin); no stale pins moved |
| calibration | **improved narrowly** | the fix landed at the discovered class only; the denylist `.config` path-start form and the fenced-heading anchor are named debt, not silently absorbed |
| adjacency | **unchanged** | zero network; corpus read-only; no sibling/fleet writes beyond the recorded queue rows |

Admission: **ADMIT** (coverage/operability/depth/calibration(narrow)
improved; none harmed). No scalar score. Learning trends: expansion
improved, quality improved, discernment improved. Round 22 registered:
curriculum round 11 — §Planned below.

## Planned — round 22 (pre-registered 2026-10-19, at the round-21 landing)

Wave per the curriculum (loop 1, round 11): one 32–64-seat AgentSwarm call,
**antigravity gemini-3.8-flash**. Claims pre-registered at the round-22
opening from the named-debt queue: candidates — the `.config` path-start
denylist bypass (direct citation, not through a symlink), the fenced-heading
anchor false-positive, the `ai benchmark(s)` boundary decision, the
inflection gaps (`bug bounties`, `dispatch mechanisms`, `llm evaluations`,
`workflow dispatch`, `security bounty`, `vulnerability disclosure`,
`responsible disclosure`, `language model benchmark(s)`, `llmbenchmark`),
the `--drift` truncated-baseline detection, the fenced-data-row `approved`
suppression, the 8 unasserted finding IDs, the secret-scan source coverage
gap, the `--json` delimiter edge, the manifest timestamp mask breadth,
bash-3 portability. Seats: 32–64; roster logged in the round-22 report.

## Round 22 verdict — 2026-10-19 (goal wave; evidence commit this landing)

Selected claims (LOG.md round-22 opening): coverage/operability = the
`.config` path-start denylist bypass (round-20 named debt):
`is_denylist_path` uses `*/.config/*` which requires a leading component —
`.config/foo` (no `./` prefix) passes CLEAN while `./.config/foo` is
refused `CLAIM_SOURCE_SESSION` crit. depth = the denylist-pattern note +
the fenced-heading anchor disposition. Wave: one 32-seat AgentSwarm call
on **openai-codex gpt-6-luna-max** (antigravity gemini-3.8-flash failed
24 seats on provider errors + 8 aborted; luna per the fallback ladder),
32/32 seat reports. Seat roster: the round-22 report.

**Before** (gate `bfc291ef…`, selftest 128): `is_denylist_path` uses
`*/.config/*`, `*/.omp/*`, `*/.local/state/*` — the `*/X/*` pattern needs
a leading path component; bare-start forms (`.config/foo`, `.omp/foo`,
`.local/state/foo`) pass CLEAN while `./.config/foo` refuses (live demo:
pre-round gate → CLEAN on `.config/agent-token.txt`; landed →
`CLAIM_SOURCE_SESSION` crit + refused; receipt
`deny-r22-20261019T190000Z-demo.log`).

**After** (gate `dfb798b4…`, selftest `PASS (132 cases, 0 skipped)`, cases
1–128 `cmp` byte-identical vs the r21 receipt): `is_denylist_path` gains
bare-start alternatives `'.config/'*`, `'.omp/'*`, `'.local/state/'*` —
checked after the existing `*/X/*` forms. Cases 129–132 pin the
path-start class (`.config` start, `.omp` start, `.local/state` start,
`.config-adjacent` over-refusal control). Masked battery vs the pre-round
gate: ALL IDENTICAL. Drift `none` vs the r12 baseline; r1 `3/3`.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the denylist path-start class is closed: before CLEAN on `.config/foo` (no `./` prefix) → after `CLAIM_SOURCE_SESSION` crit + refused (receipts live); `.omp/` and `.local/state/` share the fix |
| operability | **improved** | selftest 128 → 132 (1–128 byte-identical); the `.config-adjacent` over-refusal control proves the fix doesn't over-reach |
| depth | **improved** | `corpus/knowledge/denylist-r22.md`: the path-start bypass mechanics, the fix contract, the named limits |
| freshness | **unchanged** | the r12 baseline holds (no re-pin); no stale pins moved |
| calibration | **improved narrowly** | the fix landed at the discovered class only; the `.config-adjacent` control proves the boundary is precise; the fenced-heading anchor stays named debt |
| adjacency | **unchanged** | zero network; corpus read-only; no sibling/fleet writes beyond the recorded queue rows |

Admission: **ADMIT** (coverage/operability/depth/calibration(narrow)
improved; none harmed). No scalar score. Learning trends: expansion
improved, quality improved, discernment improved. Round 23 registered:
curriculum round 12 — §Planned below.

## Planned — round 23 (pre-registered 2026-10-19, at the round-22 landing)

Wave per the curriculum (loop 1, round 12): one 16-seat AgentSwarm call,
**devin swe-2** (fallback ladder per the standing record: devin exhausted
→ token-plan → opencode-go-6). Claims pre-registered at the round-23
opening from the named-debt queue: candidates — the fenced-heading anchor
false-positive, the `ai benchmark(s)` boundary decision, the inflection
gaps, the `--drift` truncated-baseline detection, the fenced-data-row
`approved` suppression, the 8 unasserted finding IDs, the secret-scan
source coverage gap, the `--json` delimiter edge, the manifest timestamp
mask breadth, bash-3 portability. Seats: 16; roster logged in the
round-23 report.

## Round 23 verdict — 2026-10-19 (goal wave; evidence commit this landing)

Selected claims (LOG.md round-23 opening — direct integration, no wave:
the claim was pre-registered and the fix landed before a wave could
dispatch): coverage/operability = the fenced-heading anchor false-positive
(round-20 named debt): `chain_anchor_at` scanned raw lines with `^#+` and
matched headings inside fences — a `## Phantom Heading` inside a code
block verified as a real anchor. depth = the fenced-anchor mechanics note.
Wave: none — the fix landed directly (the claim's falsifiable before→after
was already measured by the round-20 wave's live reproduction).

**Before** (gate `dfb798b4…`, selftest 132): `chain_anchor_at` scanned
raw lines for `^#+[[:space:]]+` — no fence state; a `## Phantom Heading`
inside a fence matched as a real heading, making the hop `verified`
(receipt `fanchor-r23-20261019T192000Z-demo.log`, before half).

**After** (gate `b5d0f93d…`, selftest `PASS (133 cases, 0 skipped)`, cases
1–128 `cmp` byte-identical vs the r22 receipt): the heading arm tracks
fence state inline — a `# ` inside a fence is literal, not an anchor
target. Case 129 pins it. Masked battery vs the pre-round gate: ALL
IDENTICAL. Drift `none` vs the r12 baseline; r1 `3/3`.

| axis | verdict | evidence (before → after) |
|---|---|---|
| coverage | **improved** | the fenced-heading anchor class is closed: before `verified` on a fenced heading → after `anchor-missing` + `CHAIN_ANCHOR_NOT_FOUND` warn (receipts live) |
| operability | **improved** | selftest 132 → 133 (1–128 byte-identical); inline fence tracking is deterministic |
| depth | **improved** | `corpus/knowledge/fenced-anchor-r23.md`: the false-positive mechanics, the fix contract, the named limits |
| freshness | **unchanged** | the r12 baseline holds (no re-pin); no stale pins moved |
| calibration | **improved narrowly** | the fix landed at the discovered class only; the quote/line anchor kinds are unaffected (correct — literal text is literal inside or outside a fence) |
| adjacency | **unchanged** | zero network; corpus read-only; no sibling/fleet writes beyond the recorded queue rows |

Admission: **ADMIT** (coverage/operability/depth/calibration(narrow)
improved; none harmed). No scalar score. Learning trends: expansion
improved, quality improved, discernment improved. Round 24 registered:
loop 2 begins — §Planned below.

## Planned — round 24 (pre-registered 2026-10-19, at the round-23 landing)

Loop 2 begins (curriculum loop 2, round 1): one 64-seat AgentSwarm call on
**opencode-go key 7 / deepseek-v4.1-flash** (per the curriculum's
key-rotation directive — keys rotate BETWEEN rounds; R1 uses the next
unused key lane). Claims pre-registered at the round-24 opening from the
named-debt queue: candidates — the `ai benchmark(s)` boundary decision,
the inflection gaps, the `--drift` truncated-baseline detection, the
fenced-data-row `approved` suppression, the 8 unasserted finding IDs,
the secret-scan source coverage gap, the `--json` delimiter edge, the
manifest timestamp mask breadth, bash-3 portability. Seats: 64; roster
logged in the round-24 report.

## Round 24 verdict — 2026-10-19 (kaika campaign landing; self-verdicts pending non-author verification)

Disposition of the pre-registration (round-24 criterion 11): planned one
64-seat AgentSwarm call on opencode-go key 7; the round-24 opening
(`LOG.md` :816-820) recorded opencode-go-7 interrupted at 17 seats and a
64-seat luna dispatch. That dispatch produced no seat report in this lane or
in the fleet `.ufo/reports/round-24/` — nothing from it is used here. This
landing ran under the orchestrator's kaika binding (tower worktree
`kaika/round`): one batched 10-member L2 call (planner, connector, scout,
4 executors, scribe, reviewer, critic; models by the session route table,
none passed). The first attempt was refused whole by the session's
100-job cap and retried unchanged as one batch; 10/10 completed.

Selected claims: the pre-registered `--json` delimiter edge (operability)
first; the pre-registered depth slot (the manifest-format note) lands as
claim 1's record and is NOT separately claimed — its before→after is claim
1's, so a separate depth claim would not be causally separable (round
critic, finding 7). Campaign slots: coverage (source registry + three
current-art method entries, one claim) and calibration (mistakes → criteria).

| # | axis | claim | counting command | before (ab19cff) | after | verdict |
|---|---|---|---|---|---|---|
| 1 | operability (lowest scored) | `--json` append onto a manifest whose last byte is not `\n` glued two objects; the write-only and NUL variants found mid-round | `bash corpus/evidence/round24-measure.sh <tree>` §claim 1 (also verbatim in `json-r24-20261019T213117Z-demo.log`) | `MANIFEST_LINES=1 INVALID_JSON_LINES=1` | `MANIFEST_LINES=2 INVALID_JSON_LINES=0`; selftest 133 → 136 (1–133 byte-identical); mutants m1/m2/m3 killed | **improved** |
| 2 | coverage + capability `source registry` | `corpus/SOURCES.md` (contract v1) and 3 method entries admitted through it | `bash corpus/evidence/round24-measure.sh <tree>` §claim 2: per-entry header + every cited row `mined` with `used-by` naming the entry + coverage-map row; then the 7 contract census commands | `EXPANSION_ADMITTED=0/3`; registry absent | `EXPANSION_ADMITTED=3/3`; 18 rows, malformed 0, A=14 B=1 C=3, mined=8 queued=7 rejected=3, no dup/enum/missing, 4/4 sections | **improved** |
| 3 | calibration | the lane's own 14 mistake classes mined; unlearned classes get a criterion citing its lesson | `bash corpus/evidence/round24-measure.sh <tree> [<bar>]` §claim 3 over `corpus/lessons/round-24.md` | 3/14 captured (bar `ab19cff:corpus/QUALITY.md`) | 13/14 (M-8 stays `none`, by reason) | **improved** |

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** (claim 1) | receipts `json-r24-20261019T213117Z-*`; score re-derived per criterion 12: round-1 counting command → `VERDICT_BEARING_EXPORTS=3/3` → **3**, unchanged (the score measures a narrow 3/10 construct, not this round's arm) |
| coverage | **improved** (claim 2) | first method entries since round 2 off gate-hardening ground; `corpus/README.md` coverage rows + Frontier round-24 paragraph |
| calibration | **improved** (claim 3) | `corpus/lessons/round-24.md` `## Mistakes`; `corpus/QUALITY.md` criteria 6–12 |
| depth | **unchanged** (not claimed) | the manifest note and method entries add detail, but no depth before→after was measured |
| freshness | **unchanged** | drift `none` vs the r12 baseline (no re-pin); README count re-derived as an appended correction |
| adjacency | **unchanged** | benchmark results in S006/S007 kept out of admitted knowledge (kengaku); routed in the report |

No axis harmed: battery ALL IDENTICAL, drift `none`, r1 `3/3`, cases 1–133
byte-identical. Admission is the operator's after non-author verification.

## Capabilities (round-24 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| source registry | keeps where the lane learns as opened, scope-tiered rows with kept rejections, study paths and a search log; every contract census command runs clean | `corpus/SOURCES.md`; census outputs in the round-24 report | 24 |

Not backfilled here: the 8 capability acquisitions `LOG.md` claims for
rounds 15 and 17–23 still have no row (`lessons/round-24.md` M-14) —
queued below.

## Planned — round 25 (pre-registered 2026-10-19, at the round-24 landing)

Claims, 1–3, distinct axes, each falsifiable; wave per the binding in force
at dispatch:

1. **operability — metadata screen.** A gate check for the `source:` /
   `verified-at:` / `recheck:` header (`QUALITY.md` 6). Before: the 3 legacy
   notes lacking `recheck:` (`archives-verified-r9.md`, `audit-r11.md`,
   `gate-baseline-r8.md`) are invisible to every mode; after: each names
   its finding, the 28 others stay clean, selftest cases 1–136 byte-identical.
2. **freshness — re-derive the indexes and ledgers.** Index the 2 unindexed
   files, add Frontier rows r11–r23 and evidence-index sections r12–r23,
   backfill the 8 capability rows. Before/after by the commands in
   `corpus/README.md` (round-24 correction) and `lessons/round-24.md` M-12, M-14.
3. **calibration — close stale restatements append-only.** `SKILL.md`'s
   open A-r9 C3 finding, the three divergent ledger totals, the `${GSHA}`
   placeholder, hardening addenda r16–r23 (M-3, M-4, M-5, M-6).

Remaining round-20 named debt, unclaimed: manifest concurrency (`flock`),
manifest timestamp mask breadth, `ai benchmark(s)` boundary, inflection
gaps, fenced-data-row `approved` suppression, 8 unasserted finding IDs,
secret-scan source coverage, bash-3 portability.

## Capabilities (round-25 reconciliation of earlier LOG claims)

These eight rows reconcile `LOG.md`'s `Capabilities +1` claims for rounds 15
and 17–23 (round-24 lesson M-14). First-working rounds are the historical
rounds, not new acquisitions in round 25. Each demonstration was re-run at
`b820e4e` this round (`--selftest` PASS 136 cases; the case-level outputs and
row review are `.ufo/waves/round-25/build/CapRowR{15,17..23}.md`); the final
landing selftest also carries the same cases byte-identically.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| root-slash source resolution | reads a same-device absolute claim source under `--root /` rather than falsely refusing it as out-of-corpus | round-15 receipt cases 107–110, current cases 107–109 and 111; `corpus/knowledge/root-slash-boundary-r15.md` | 15 |
| fence-aware scope screening | ignores fenced `## Meta` headings while parsing sections, so a fake in-province declaration cannot shadow the real refused domain | selftest cases 112–116; `corpus/knowledge/fenced-heading-r17.md` | 17 |
| LLM benchmark-phrase scope screening | flags declared `llm benchmark(s)` / `llm scoring` scope with `SCOPE_MODEL_QUALITY_ABSORBED` warn; prose-only control stays CLEAN | selftest cases 117–119; `corpus/knowledge/scope-phrase-gap-r18.md` | 18 |
| sweep symlink-escape refusal | refuses the whole sweep when an expanded match canonicalizes outside both allowed roots | selftest cases 120–122; `corpus/knowledge/sweep-symlink-r19.md` | 19 |
| HTML-comment heading-shadow detection | treats headings inside HTML comments as literal text, so a fake `## Meta` cannot shadow the real scope declaration | selftest case 124 (`scope-comment-shadow`); `corpus/knowledge/html-comment-r20.md` | 20 |
| canonical pointer-boundary screening | canonicalizes pointer targets and checks both roots, refusing traversal/symlink escapes and denylisted canonical targets | selftest cases 125–128; `corpus/knowledge/pointer-boundary-r21.md` | 21 |
| denylist path-start refusal | refuses claim sources beginning `.config/`, `.omp/`, or `.local/state/`, while allowing `.config-adjacent/` | selftest cases 130–133 (current; round-22 receipt 129–132); `corpus/knowledge/denylist-r22.md` | 22 |
| fenced-heading chain anchors | rejects a heading inside a fenced block as a chain `heading` anchor, reporting missing-anchor drift | selftest case 129; `corpus/knowledge/fenced-anchor-r23.md` | 23 |

## Capabilities (round-25 acquisition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| knowledge-entry metadata screen | names absent source/verified-at/recheck keys and undated verification values, reports command-only and parent-root rechecks as info, and refuses denylisted/oversized/NUL-bearing entries | `bash tools/research-gate.sh verify-metadata corpus/knowledge --root .`; selftest cases 137–154; `corpus/knowledge/metadata-screen-r25.md` | 25 |

## Round 25 verdict — 2026-10-21 (recovery attempt 2, pending outside closure)

Claims and frozen populations: `corpus/evidence/round25-claims.md`, registered
at `b820e4e` against base `d730ae4` before implementation. Counting command:
`bash corpus/evidence/round25-measure.sh <tree-root>` (from any cwd); receipts
`corpus/evidence/round25-measure-{before,after}.log`. The measured integration
revision is the round-25 checkpoint carrying this section (its landed hash is
recorded in the fleet report); a commit cannot embed its own hash. Attempt 1
left no output and spawned 0 seats; no dead identity was respawned.

| claim / canonical axis | before → after | verdict / score delta |
|---|---|---|
| C1 operability — metadata-screen capability | mode absent, rc 2 and no named legacy-header findings → rc 1, `METADATA_COMPLETE=25/28`, exactly `archives-verified-r9`, `audit-r11`, `gate-baseline-r8` each `META_RECHECK_ABSENT`; 27-fixture differential 54/54; cases 1–136 identical | **improved** (syntactic screen, not full QUALITY 6); operability score **3→3, delta 0** on its original r1 construct, re-derived 3/3 this landing; capability row above |
| C2 freshness — re-derived indexes | `STALE_INDEX_ITEMS=66` (2 unindexed +13 Frontier gaps +43 misfiled receipt rows +8 missing capability rows) → 0 | **improved** (index freshness, not a coverage score); no numeric freshness score invented |
| C3 calibration — stale restatements | `STALE_RESTATEMENTS=15` → 0 (one closed finding, three stale tuples, two queue sizes, one template slot, eight missing addenda) | **improved**, qualified: lexical count plus cited replacements, not semantic proof of mistake→criterion mapping; no numeric calibration score invented |

C3 also found the owning ledger's E4 tuple was wrong (sum 72 over 71 rows),
so `hardening-r10.md` has an append-only erratum and a reproducible recount:
`python3 corpus/evidence/round25-ledger-recount.py` → rows=71, 38/22/8/0/3,
queue_committed=24 versus queue_true=25. SKILL now points to that owner and
command instead of duplicating totals. The r13 template substitution is
recorded in the same erratum; history is not silently rewritten.

Holds at the integration checkpoint: `PASS (154 cases, 0 skipped)` (136→154),
`GATE_DRIFT: none` versus the r12 baseline, r1 `VERDICT_BEARING_EXPORTS=3/3`.
The explicit-root hold battery and final suite are recorded separately at the
round-25 landing. Depth and adjacency: **unchanged** (no claim). Coverage:
**unchanged** as a measured axis; a new entry/capability supports the qualified
expansion trend, not an invented domain-coverage fraction. Freshness and
calibration remain unscored (only operability has a numeric construct).

Trends (lane assessment, outside closure remains separate): **expansion
improved** — `metadata-screen-r25.md` is uncovered metadata-screen ground,
mined S019/S020, indexed; **quality improved** — stale index/ledger claims
reconciled, relative-root recheck superseded, legacy headers made visible;
**discernment improved** — prior outside-check debts become shown-to-fail
criteria 13/14 and the S006 quote error is corrected. Neither source-row growth
nor `STALE_INDEX_ITEMS=0` by itself is an expansion verdict. SHONEN stays `[~]`
(no self-attested `[x]`). No historic misrooted-battery hold is relabelled green.

## Planned — round 26 (not started)

1. **operability (lowest measured, 3/10):** serialize cooperating `--json`
   appenders across the EOF probe plus append (`flock` candidate remains
   unlanded in r25 wave evidence); reproduce seeded-unterminated race before,
   then ≥10×16-writer same-precondition runs with no blank/invalid lines.
2. **freshness:** compute due dates from verified-at + recheck cadence with
   an explicit as-of date; before no due-date output, after one planted
   past-due control caught and current entries reported with due/unknown.
3. **calibration:** a criterion-6 verifier (not the r25 syntax screen) checks
   each cited S-id exists, is mined and used-by names the entry, plus the
   what-was-checked text; freeze r24+ population and semantic negative controls
   before implementation. Legacy entries remain distinct from prospective bar.

### Round-25 measured-revision erratum (2026-10-21)

The initial `0fc037e` checkpoint had prose/fixtures but omitted the gate from
the helper path list: old gate SHA752e4e38/selftest136. The corrected measured
checkpoint is `d8c8cff3923f10481ac9ced66d0af7c41d38130c` (gate landed, 154
cases); original working-tree counts are not proof for `0fc037e`. Fresh
falsifiers were steered to the corrected commit, same identities. Final
measurement receipts and the fleet report cite the final helper landing.
See lesson R25-M13 and QUALITY15; no numeric score changes from this erratum.

### Round-25 final recovery measurements (same attempt, 2026-10-21)

Replacement L1 `ChousaR25` inherited the two validated 68-seat waves, their
landed checkpoints and uncommitted falsifier-driven corrections. No wave was
rerun and no dead identity replaced. Final counting command remains
`bash corpus/evidence/round25-measure.sh <lane-tree>`:
`round25-final-measure.log` records C1 25/28 with exactly the three legacy
drifts, C2 0 stale index items and C3 0 unresolved stale restatements.
The historical `${GSHA}` token is restored (raw count 1); its explicit
append-only disposition makes unresolved count 0. The original raw-zero
prediction is withdrawn, not fulfilled by editing history.

Final holds: selftest 161/161, legacy cases 1–136 identical, r12 drift none,
r1 3/3; differential 54/54. See `round25-final-holds.log`,
`round25-final-differential.log` and `round25-final-ledger.log`.
Operability score stays 3→3 (delta 0); C1/C2/C3 retain the qualified improved
verdicts above. The final pushed lane revision is identified by the report's
helper `landed` hash; these receipts measure its executable/index bytes.
S029/S033, not superseded S019/S020, are the mined rows grounding the new
entry. No outside admission or SHONEN verification is self-awarded.

Counter qualification from residual review: `round25-measure.sh` is a probe,
so exit0 is not a verdict. The actual printed values plus retained content
reviews support the claims. C3 now rejects slot/marker/addendum/recount
deletions; `round25-final-counter-controls.json` preserves failing controls.
C2 remains a bounded syntax/population count, not a complete semantic index
validator. README's old handoff tuple is explicitly dated, outside the
frozen C3 population rather than silently counted as an original claim item.

**Measured commit for all three final claims:**
`c125d8bc20e5433947df26fe0af3d3b58d0b37d3`.
`corpus/evidence/round25-measured-revision.json` binds all 11 measured
executable/counting/index/ledger input blobs to that landed revision.
Final counting receipt: `round25-landed-measure.log`; final differential:
`round25-landed-differential.log`. C1 improved, score3→3/delta0; C2 freshness
improved, 66→0; C3 calibration improved with lexical/content-review limits,
15→0 unresolved (historical raw slot1 retained). No other numeric score
is invented. The following bookkeeping landing does not change the gate.

Packaging erratum: explicit helper path selection still omitted the gate
from `c2a6e338`; this was caught by QUALITY15's actual blob comparison,
not assumed from the helper's success. A gate-only helper retry landed
`c125d8bc` with all11 hashes matching. Cause unresolved; no direct VCS
mutation or blind repeated retry was used (lesson R25-M15).

Baseline comparability recheck: the exact final counting probe, run over
`git archive d730ae4c33989ad9c8535764d4cae77b4db869f6` in an isolated tree,
records the same absent-mode rc2, 66 stale index items and 15 unresolved
restatements (`round25-final-before.log`, probe exit0). Thus the later
anti-deletion guards do not manufacture the before→after reduction.

## Round26 recovery verdict — 2026-10-21, same attempt1

**NOT ADMITTED.** This closes the author-lane record, not the fleet's outside
closure. The earlier `Planned — round 26 (not started)` heading is historical:
the actual preregistration is `f361d12e44687841e30ec35710ddb366c6f795e0`
against base `ba3333254dd337658a4f25e7a9471f9cf4e4567e`. Its appender-race
item was carried, not implemented or claimed. C1 instead exercised the
round25 closure's reader-allocation risk on the lowest measured axis.

Measured production revision: `0e9784bd52eca456b24d0bc40921480a47f91a2b`;
gate SHA-256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.
Command: `bash corpus/evidence/round26-measure.sh TREE all`, with TREE an
isolated archive of that revision. The inherited author-lane critic actually
executed it; its exact output is retained in
`corpus/evidence/round26-inherited-after.log`, with command/record provenance
and the seat's verification-scope violation in
`round26-inherited-measurement.json`. Recovery did not repeat failed checks.
Before: the identical probe at the base, `round26-measure-before.log`.

| claim / axis | before → after observed | final author-lane verdict |
|---|---|---|
| C1 operability — metadata entry-reader allocation | `C1_AMPLIFIED=4/4 → 0/4`; frozen29 SHA `3f83ba4844cac8d2057b47661be225f84a5945fc7c1db739ec2070b6aa2a4a37`, rc1 unchanged | **improved narrowly**, but not verified under the complete claim contract: shared PASS hold fails and 31 falsifier seats returned no report |
| C2 freshness — computed due dates | classified `0/29 → 29/29`, oracle `0/29 → 29/29`, controls `0/6 → 6/6` | **harmed / falsified** beyond frozen controls: cadence-input termination and locale-dependent usage exit; `FDateHugeCadence.md`, `FDateAsOfUsage.md` |
| C3 calibration — registry relationships | controls `0/5 → 5/5`, positive `0/1 → 1/1`, frozen r24+ clean `0/5 → 5/5` | **harmed / falsified**: stale table-header state, incorrect source-token rescan and refused-path guarantee failure; `FRegistryHeaderless.md`, `FRegistryIdBoundary.md`, `FRegistryRegistryDeny.md` |

All named falsifier reports are under `.ufo/waves/round-26/falsify/`.
No frozen threshold or oracle was relaxed to erase those counterexamples.
The registry comparator's set-of-finding-code comparison misses some
occurrence/whitespace differences; frozen agreement is not grammar equivalence.

Shared hold: base `PASS (161 cases, 0 skipped)` → target
`FAIL (3/187 cases)`, exit1. Legacy161 case SHA remains
`5eac4a7e2af964f6e81631f66990426e5c8ef58fb41ba6ec6d0054ef819e01cb`;
drift remains none, rc0; archived-input observable remains3/3.
`FNoTrade.md:115-137` explains the three new unsatisfiable usage assertions.
Probe exit0 is not a PASS. The operability scalar stays **3→3, delta0**
on the original narrow r1 construct; the inherited probe used its explicit
fleet-root equivalent, and FNoTrade also exercised the original sibling-layout
form. Neither form measures resource safety or general field readiness.

No round26 capability is admitted to the repertoire table. The three new
knowledge files are retained with explicit candidate/withdrawal qualifications;
their presence and six mined source rows do not count as admitted expansion.
Trends: **expansion unchanged; quality harmed; discernment unchanged**.
The lane recorded and learned from falsification but has no outside round26
admit/reject judgment. No new numeric freshness/calibration score is invented.

Wave accounting: inherited build64 + falsify68 = **132 distinct seats**.
Final reconciliation: build39 reports/25 no-report; falsify37 reports/31
aborted no-report. Every seat transcript is terminal. Earlier death manifests
describe earlier recovery snapshots; errors and reports can coexist.
`build-final-reconciliation.json` and `falsify-final-reconciliation.json`
retain per-seat report hashes, last errors, terminal records and dispositions.
Recovery spawned/resumed/replaced zero seats. It does not claim full
falsification, no-harm, promotion, or admission.

## Round27 recovery verdict — 2026-10-21, same attempt1

**NOT ADMITTED: C3 partially falsified; no-harm condition not met.**
Frozen claims: `corpus/evidence/round27-claims.md`, base
`64eec5d41c7cf7f17f5ce1e968e28b3769952596`.
Final measured production revision:
`4f48419425f5165a8f950e1db4c0a781cf845d40`;
gate SHA-256 `ac1315ddaa12e79b68069d1a9866b9b1b55e3a43efef3ba0cb5ca5e665835765`.
The receipt owner is `.ufo/waves/round-27/final/identity.json`, not the
historical `corpus/evidence/round27-*-after.*` files (dd72641e, PASS210).

| claim / distinct axis | measured before → after | verdict / score delta |
|---|---|---|
| C1 operability, lowest measured axis | accepted r26 `FAIL3/187` → `PASS215/215`, no skips; original187 retained and first210 identities unchanged from dd72641e; original161 line SHA unchanged; original C1 controls6/6 plus final added5/5 | **improved bounded repair**; original r1 scalar3→3, delta0, re-derived3/3 (not a general resource/readiness score) |
| C2 freshness | accepted r26 locale/input-normalization failures → original synthetic21/21 + final added8/8 match; date differential9024/9024; 4 MiB representable cadence completes (timeout-sensitive historical baseline, not a semantic mismatch) | **improved bounded repair**; no invented numerical axis score |
| C3 calibration | accepted r26 stale-header/rescan/hidden-denylist defects → original31/31 + final added19/19 match, registry differential48/48; complete-path hidden-denylist failure class repaired; frozen negative no-prefix clause still fails | **partially falsified / harmed**: prefix matching retained, including a new claims-canonical over-refusal; no axis score or capability admitted |

Commands (run in an isolated archive of the measured revision; every command
below exits0):

- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`
  →58 controls,0 mismatches (C1=6,C2=21,C3=31);
  `final/regressions.json`.
- `python3 corpus/evidence/round27-falsify-controls.py --gate tools/research-gate.sh`
  →32 controls,0 mismatches (C1=5,C2=8,C3=19);
  `final/falsify-controls.json`.
- `bash tools/research-gate.sh --selftest` →PASS215,0 skipped, host
  LANG=en_US.UTF-8 and LC_ALL unset; `final/selftest.log`.
- `python3 corpus/evidence/round27-mechanisms.py tools/research-gate.sh`
  →C1=0,C2=0,C3=0 versus non-executing base counts1/2/5. This is only a
  lexical mechanism count, not a behavioral admission gate.
- `bash corpus/evidence/round26-date-differential.sh TREE/tools/research-gate.sh`
  →9024/9024;
  `bash corpus/evidence/round26-registry-differential.sh TREE` →48/48;
  `bash corpus/evidence/round25-meta-differential.sh` →54/54 (27 fixtures).
- `bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json`
  →`GATE_DRIFT: none`. The r1 explicit-fleet-root A/B/C invocations each
  exit1 and emit one DRIFT summary →3/3; argv and per-input outcomes in identity.json.

All abbreviated `final/` paths above mean `.ufo/waves/round-27/final/`.
Legacy161 ok-line SHA remains
`5eac4a7e2af964f6e81631f66990426e5c8ef58fb41ba6ec6d0054ef819e01cb`.
Neither suite covers the entire frozen C3 claim: ResC3Clause demonstrates
that actual filesystem inputs still pass through citation-prefix denial,
including the new `plain.md -> k.env:1` canonical refusal. The negative
compatibility expectations were not weakened or deleted to manufacture green.

Post-falsify checkpoints remain distinct: dd72641e PASS210/58 controls;
cb895a2 PASS215/26 controls but false CLEAN on shifted escaped columns and
scanner failure; final4f484194 fixes those two counterexamples with shared
cell splitting and separately checked scanner stages. Source-method
counts1/2/5→0/0/0 and green frozen suites do not erase that history.
Residual8 seats independently attacked cb895a2; candidate followups bind
the exact final gate digest (scanner) and unchanged shared-split form (width).

Sources39→43 (A33→37,B1→1,C5→5; mined16→20,queued19→19,rejected4→4);
four new own-work rows, no new knowledge/capability admission. Source census
exit0→0; rows S040–S043, Gate quotes and mistakes are owned by the round27
lesson. Quality criteria19–22 mine real rejected/falsified behavior.
Trends: **expansion unchanged; quality harmed; discernment unchanged**
(no self-awarded outside admit/reject spot-check). No promotion or round28.
Wave accounting: inherited build64 + falsify64 + new residual8 =136 seats;
7 inherited no-report dead seats, none replaced.

## Round28 — DERIVED full-claim honest negative

One full proposed C1 targeted operability, the lowest active measured
axis: canonical claim-source ancestor over-refusal plus actual complete
denied-path attribution, preserving original consumer/usage/legacy/
no-harm obligations. It is **not achieved / unprovable**.
`corpus/evidence/round28-safe/claims.md` retains its full negative scope.

Parent did not approve the proposed default/nested-root relaxation;
denylist not waived. No implementation or new measurement was authorised.
There is no after value, new scalar/delta, capability, Core graduation,
promotion or admission. Prior metric and original187/legacy161 ordinals
are held, not repinned or remeasured. The original R27 C3 clause, controls
and rejected-harmed result remain unchanged.

The only before is the old committed grouped receipt; cb→BASE transfer
is explicitly inferential. Procedural native counts and two VOID
contributions are qualified in `corpus/evidence/round28-safe/native-seats.json`
and `corpus/evidence/round28-safe/qualifiers.md`, not behaviour/no-harm proof.
Full raw/private bodies and the unapproved executable are excluded from
the safe Git set; custody is in `corpus/evidence/round28-safe/provenance.json`.
No Root report/end census or continuation is authorised at this stage.

### 2026-10-23 correction to the round-28 section (routed defect D3)

The round-28 section says no end census was run at that stage. The fleet witness `.ufo/waves/hyaku/chousa28-negative-records/parent-census.json` (fleet commit `b4b338e9`) records `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`, run at 2026-10-22 02:49:09 UTC against lane commit `7c87b9734eb71985e19767af36d57dff89536521`. It exited 0 and printed `chousa ok` for `chousa-shokunin/corpus/SOURCES.md`. This corrects the run-status record only; the earlier text is kept as written. Routed as defect D3 by `corpus/lessons/round-28-verifier-spotcheck.md:50-54,125-126`; witness re-read in round 29 by seat ScribeRepairD3 (`.ufo/waves/round-29/build/ScribeRepairD3.md`).

## Round 29 — quote re-open capability (one claim, C1 operability)

Base `6c5eb1466f2b8abbd3de576389037f435016d07b`. Frozen claim, counter, fixture
and design history: `corpus/evidence/round29/claims.md` (design v3,
`aa5e1a3187955fa923de14e11c150bf1c526efc6`). The tool landed at
`30c9d24da1815e01e161ed2f52d5f951005cc2b8` (tool SHA-256 `72a3ad47…54fea`,
counter SHA-256 `cd509650…175d`).

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 operability, lowest scored axis; capability acquisition | `QUOTE_REOPEN_MATCH=0/130` (tool absent, `.ufo/waves/round-29/controls/before-do-nothing-v3.json`) → `130/130` twice on `30c9d24d` (`.ufo/waves/round-29/measure/after-run1.json`, `after-run2.json`) | `python3 corpus/evidence/round29/c1-count.py -- python3 tools/quote-reopen.py verify` | measured: met. Re-derived by wave 2: 130/130 in 6 further runs (RerunCounterA, RerunCounterB x2, ScoutFreshnessH x3) |

The round-1 operability scale is unchanged: score 3 → 3. Its counting
command (lines 28-30) still prints `VERDICT_BEARING_EXPORTS=3/3`, and
`tools/research-gate.sh` is byte-identical (SHA-256 `ac1315dd…5835765`). The
new observable sits beside that score and does not replace it.

Pre-data controls under v3 (28 committed receipts, best 126/130 from
casefold without a boundary; the best no-fetch label cheat reached 115/130)
are in `.ufo/waves/round-29/controls/`. Designs v1 (a label replay met 82/82)
and v2 (a seed replay met 130/130) were voided before data; the lesson records
both as mistakes.

Falsify-wave limits (reported, not re-scaled):
- The counter does not prove a live fetch. A cache-only verifier built from
  page snapshots taken 27 minutes earlier scored 130/130 twice
  (`.ufo/waves/round-29/falsify/CriticClaimDesign.md`). Liveness rests on the
  loopback harness, which counts server hits (65/65 with only the address
  guard disabled, `falsify/OfflineConformance.md`), and on code review.
- Mutants: boundary removal (126), quote-map removal (126) and inline-as-block
  (117) are killed. Three mutants survive at 130: verdict order, script and
  head text, and case-insensitive matching. The fixture lacks those classes.
- Security review: open findings on DNS rebinding between check and connect
  (T1) and on a slow-drip read that outlasts the 30 s deadline (T4)
  (`falsify/SentinelTool.md`). The tool fetches only registry URLs.
- Pages that omit `</head>` (S047, 1 of 32 HTML registry pages) and 2xx
  challenge pages (S021, S022) read as `ABSENT`.

## Capabilities (round-29 acquisition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| quote re-open | re-opens each located quote against the live URL of its `corpus/SOURCES.md` row and returns `VERBATIM`, `ABSENT`, `TOO_LONG`, `NO_SOURCE` or `UNREACHABLE` | `python3 tools/quote-reopen.py verify --items <tsv>`; `python3 corpus/evidence/round29/c1-count.py -- python3 tools/quote-reopen.py verify` → `QUOTE_REOPEN_MATCH=130/130`; `corpus/knowledge/quote-reopen-r29.md` | 29 |

Sources 45 → 49 rows (tier A 39 → 43; mined 22 → 26). New rows S046 to S049,
each mined and used by `corpus/knowledge/quote-reopen-r29.md`. QUALITY criteria
23 to 25 were added. Trends, author view: expansion improved, quality improved,
discernment unchanged.

### 2026-10-23 correction — capabilities-row wording (routed defect D1)

The phrase “live URL” in the round 29 capabilities row is not shown by the round 29 counter. The counter can be met without a network fetch: the cache-only verifier described in `.ufo/waves/round-29/falsify/CriticClaimDesign.md` scored 130/130. Separate network evidence is `.ufo/waves/round-29/falsify/DiffToolB/landed-fixture.network.json`, bound by `.ufo/waves/round-29/falsify/DiffToolB/differential-receipt.json`: the `landed-fixture` network record has 8 allowed request events with `"method": "GET"` and 8 response entries with `"status": 200`. The bound run records `"production_bytes_unchanged": true`, 40 expected and 40 observed items, and the command and exit shown below. Its verdict summary is `verbatim=14 absent=20 too_long=3 no_source=3 unreachable=0`. This is evidence for those GETs and HTTP 200 responses in that one fixture run, not evidence that the counter itself fetches or that every registered URL is reachable. [INFERENCE] Keep the row's counter result distinct from this bounded network observation.

Recorded command (from `differential-receipt.json`; not rerun by this seat):

```text
timeout --kill-after=5s 590s python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/DiffToolB/guarded-run.py /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/DiffToolB/landed-fixture.network.json tools/quote-reopen.py verify --items corpus/fixtures/quote-reopen-r29/items.tsv --registry corpus/SOURCES.md
```

The receipt records `cwd` `/home/vgpnk/Projects/shokunin/chousa-shokunin`, `exit_code` 1, `expected_count` 40, `observed_count` 40, and `production_bytes_unchanged` true. The exit and mixed verdict summary are reported as recorded, not interpreted as a pass.

The word "live" in the round-29 lesson, knowledge entry, this file and `corpus/README.md` (inventory: `.ufo/waves/round-30/build/ScribeD1Liveness/drafts.md` section B) is read the same way: backed for that one DiffToolB run only, never by the counter. QUALITY criterion 26 now requires this. Routed by `corpus/lessons/round-29-verifier-spotcheck.md:143-147`.

### 2026-10-23 correction — second DiffToolB network run (routed D8)

The D1 correction above says the network evidence is “that one DiffToolB run only”; this omits a second recorded run of the landed tool. `corpus/lessons/round-30-verifier-spotcheck.md:197-198` routes this finding. The `landed-heldout` record in `.ufo/waves/round-29/falsify/DiffToolB/differential-receipt.json` binds the command below to `.ufo/waves/round-29/falsify/DiffToolB/landed-heldout.network.json`; the receipt records exit 1, 33 expected and 33 observed items, and `QUOTE_REOPEN_SUMMARY verbatim=26 absent=3 too_long=0 no_source=0 unreachable=4`:

```text
timeout --kill-after=5s 590s python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/DiffToolB/guarded-run.py /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/DiffToolB/landed-heldout.network.json tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/DiffToolB/held-out-3col.tsv --registry corpus/SOURCES.md
```

The bound network record contains 32 allowed GETs and 2 refused GET requests; its responses are 27 HTTP 200, 2 HTTP 203, 2 HTTP 301 and 1 HTTP 403 (`.ufo/waves/round-30/falsify/ReviewCorrections.md:25`). This is a second bounded network observation, not evidence that the counter itself fetches or that every registered URL is reachable. The recorded exit is not characterized as a pass. The earlier text remains intact.

### 2026-10-23 correction to the Round 29 re-derivation count (routed defect D2)

The Round 29 table says wave 2 re-derived C1 in 6 further runs. The committed outputs support 5 further runs, each scoring 130/130:

- `.ufo/waves/round-29/falsify/RerunCounterA/receipt.json` — seed `16442982337510174646`.
- `.ufo/waves/round-29/falsify/RerunCounterB/receipt-1.json` — seed `5392061795029416258`.
- `.ufo/waves/round-29/falsify/RerunCounterB/receipt-2.json` — seed `1932010155184684229`.
- `.ufo/waves/round-29/falsify/ScoutFreshnessH/rederive-receipt.json` and `rederive.out` — run 1, seed `13173258806708832500`.
- `.ufo/waves/round-29/falsify/ScoutFreshnessH/rederive3.out` — run 3, seed `3497534629407128034`.

`ScoutFreshnessH.md` labels run 2 with seed `12970099299958901445` but cites `rederive3.out`; that file records seed `3497534629407128034` (run 3). No separate committed output or receipt for the run 2 seed is in the falsify artifacts, so it is not included in the count of 5. This corrects the count and its evidence trail only; the earlier text is retained. Routed by `corpus/lessons/round-29-verifier-spotcheck.md:148-150`.

## Planned — round 30 (not started)

Candidates, not commitments: close the three surviving mutants with fixture
classes declared before data (an unreachable over-long item, a hidden-text-only
item, a case-only edit); handle a missing `</head>` and 2xx challenge pages in
a new contract version; close sentinel T1 and T4; get the L0 ruling on the
fetch scope. Round-28 C1 (path-denylist surface) stays open and is
operator-owned.

## Round 30 — quote re-open head boundary and fetch bounds (two claims; D-list only)

Base `a3a3710e3d0adf2f95882292f17b5093e3baf97c`. Frozen design:
`corpus/evidence/round30/claims.md` (design v4 at `abfdf93274d0c70e02465e22abcf029dea59efb9`;
earlier designs were changed before data after the control wave found leaks, see the
lesson). Landed tool `49b2aa3006d3c44a29b171ab30df09776c21405d` (tool SHA-256 `47a657e7…1201`).

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 coverage: edge class of pages that omit `</head>` | `QUOTE_REOPEN_HEADLESS_MATCH=78/106` (round-29 tool, `.ufo/waves/round-30/controls/before-c1-v4-run{1,2}.json`) → `106/106` twice on `49b2aa30` (`.ufo/waves/round-30/measure/after-c1-run{1,2}.json`) | `python3 corpus/evidence/round30/c1-count.py` | measured: met; re-derived 106/106 in every falsify-wave run (RerunC1A/B/C 9 runs, SeparabilityRevs, CriticClaimsAfter) |
| C2 operability (lowest scored axis): stated fetch bounds hold under slow senders and DNS rebinding | `QUOTE_REOPEN_FETCH_BOUND_MATCH=12/27` (`before-c2-v4-run{1,2}.json`) → `27/27` twice on `49b2aa30` (`measure/after-c2-run{1,2}.json`); revision `33dd643f` scored 24/27 once and was fixed at `bd43bd53` | `python3 corpus/evidence/round30/c2-count.py` | **not met (miss under the kill rule)**: the landed tool printed 26/27 on 3 of 44 fresh-seed runs (`.ufo/waves/round-30/falsify/RerunC2B/run2.json`, `run4.json`, `extra16.json`); each miss is a slow-ok item refused about 0.07 s after its own DEADLINE. The seat's diagnosis points at the frozen harness's listen queue (backlog 5), not the tool; the counter is not re-scaled and the claim is reported as a miss |

The round-1 operability scale is unchanged: score 3 → 3; `tools/research-gate.sh` is not
touched by this round. The C2 observable sits beside that score.

Controls (all under `.ufo/waves/round-30/controls/`): C2 v2 was met 20/20 by a DNS- and
header-keyed shortcut and re-designed before data; under v4 no control met either
counter (best C1 no-reader 84/106, best C2 control 18/27, a fixed 3.8 s cutoff).

Not claimed: liveness, TLS (counters are plain HTTP), per-hop address provenance,
resolver time, IPv6, pages without a `<head>` start tag, 2xx challenge pages, PDFs.

Sources 49 → 56 rows (S050 to S056, tier A, mined, used by
`corpus/knowledge/quote-reopen-r30.md`). QUALITY criteria 26 to 29 added. Census at the
end: `chousa ok`, exit 0, with two W04 warnings (two pairs of rows share a page URL).

### 2026-10-23 correction — routed D4

The Round 30 C1 re-derivation is corrected: 32 of 35 distinct committed after-receipts carrying the landed tool SHA `47a657e7…` and frozen C1 counter SHA `5b312d84…` scored 106/106. The other three (`falsify/ConnectorKagiPin/c1-run2.json`, `falsify/MutR29Order/baseline.json`, and `falsify/MutR29SkipScript/baseline.json`) scored 0/106 under resource caps and are inconclusive, not support for 106/106. `CriticClaimsAfter`'s 14/14 is a combined count of its 3 C1 receipts, the 9 `RerunC1A/B/C` receipts, and the 2 measurement receipts; it is not a separate 14-run bucket. `SeparabilityRevs` contributes 2 distinct C1 receipts. This corrects the duplicate count routed by `corpus/lessons/round-30-verifier-spotcheck.md:178-181`.

Evidence: `.ufo/waves/round-31/build/ExecD4Rerun/enum-output.txt:1-57` and `.ufo/waves/round-31/build/ExecD4Rerun.md:11-18,22-46` (recorded command exit 0).

## Capabilities (round-30 change)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| quote re-open (contract v2, C1 part) | as round 29, and also reads pages that omit `</head>` (C1 measured). The fetch-layer change (one validated address per hop; one `DEADLINE` over header and body reads) landed, but C2 missed its predicate and the deadline does not cover name resolution or dialing (`falsify/SentinelFetchLayer.md`) | `python3 corpus/evidence/round30/c1-count.py` → 106/106; `python3 corpus/evidence/round30/c2-count.py` → 27/27 (loopback harness); `corpus/knowledge/quote-reopen-r30.md` | 29 (contract v2 in 30) |

### 2026-10-23 correction — capabilities evidence pointer (routed defect D1)

The `27/27` C2 pointer above is not the round's frozen-predicate verdict. Although the two measurement runs scored 27/27, C2 missed its kill rule: 3 of 44 fresh-seed runs printed 26/27 (`corpus/lessons/round-30-verifier-spotcheck.md:109`; this correction was routed at `:165-168`). The three miss receipts record `n=26`, `t=27`, and `predicate_holds=false`: `.ufo/waves/round-30/falsify/RerunC2B/run2.json:478-480`, `.ufo/waves/round-30/falsify/RerunC2B/run4.json:478-480`, and `.ufo/waves/round-30/falsify/RerunC2B/extra16.json:478-480`. Keep the earlier row as history; its C2 evidence must be read as a miss, not as held ground.

### 2026-10-23 correction (round 31, D2)

The backlog-5 explanation in the Round 30 C2 row above is **[INFERENCE]**, not an established cause. `RerunC2B.md:45,57` labels it `[INFERENCE]` and states that no per-connection record shows a dropped or delayed SYN. The 18/18 backlog-128 control is consistent with the explanation but not conclusive (`.ufo/waves/round-30/falsify/RerunC2B.md:49-50`). Round-31 copies: `.ufo/waves/round-31/build/ExecD2Backlog/bl/`. The C2 verdict remains “not met (miss under the kill rule)”; the control does not re-scale it or change the frozen v4 bytes. Any future C2 counter version that sets `request_queue_size` must be declared before data as a new version; never edit the frozen v4 bytes. This append-only correction answers D2 in `corpus/lessons/round-30-verifier-spotcheck.md:169-174`.

## Planned — round 31 (not started)

Candidates, not commitments: pages without a `<head>` start tag; 2xx challenge pages;
resolver time inside `DEADLINE`; a TLS case in the harness; per-hop address provenance;
IPv6; the L0 fetch-scope answer. Round-28 C1 (path-denylist surface) stays open and
operator-owned.

## Round 31 — claim location binding and revision pin (two claims)

Base `be7b8d8d54962286417465a305fd9a1a7b3b1525`. Frozen design `corpus/evidence/round31/claims.md`
(v1 `d78d1889`, v2 `8070f92b`; v2 was frozen after the control wave and before any candidate was
scored; v2 control re-score committed at `86188116`). Landed: C1 at
`c17948a776ad0389d47f2f15ec68f204adad5c8d` (gate SHA-256 `3b5279eb…bc3b`), C2 on top at
`6d0ae19f240c1b5c0e62dffc06e57d28a2af1efd` (gate SHA-256 `c23d7537…823c`). `tools/quote-reopen.py`
is not touched (anti-loop: rounds 29 and 30 worked it).

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 coverage: edge class "a claim names a line or range" in `verify-claims` (frontier item: pairing a span's occurrence with a named pointer line, README Round26 disposition) | `LINE_BINDING_MATCH=50/120` (base gate, `.ufo/waves/round-31/controls/CtlBaselineJunk/c1_base_seed*.json`) → `120/120` twice on `c17948a7` (`.ufo/waves/round-31/measure/after-c1-run{1,2}.json`) and twice on `6d0ae19f` (`after-c1-run{3,4}-tip.json`) | `python3 corpus/evidence/round31/c1-count.py` | measured: met under P1 |
| C2 operability (lowest scored axis: the only scored axis, `SCORECARD.md:7`): `SKILL.md` checklist item 1's revision clause made runnable for every claim that carries a `"sha256"` pin | `REVISION_BINDING_MATCH=50/120` (base gate, `controls/CtlBaselineJunk/c2_base_seed*.json`) → `120/120` twice on `6d0ae19f` (`measure/after-c2-run{1,2}.json`) | `python3 corpus/evidence/round31/c2-count.py` | measured: met under P2 |

The round-1 operability scale is unchanged: score 3 → 3 (delta 0); the C2 observable sits beside
it, as in rounds 25 and 29. Separability: the C2 counter on the C1-only build prints 50/120
(`measure/sep-c2-on-c1only.json`), the C1 counter on the C2-only build prints 50/120
(`measure/sep-c1-on-c2only.json`).

Controls (v2, all under `.ufo/waves/round-31/controls/`): no control met either counter. Best C1
control 116/120 (start-line-only binding), best C2 control 118/120 (whitespace-trimming
validator); no-reader C1 88/120, C2 86/120; do-nothing 50/120 each; disclosed full-contract
oracles 120/120 (feasibility only). v1 was broken by three control findings before data
(`corpus/lessons/round-31.md`, Design history).

Selftest: `RESEARCH_GATE_SELFTEST: PASS (228 cases)` (base 215; C1 cases 216–219, C2 cases
220–228). Not claimed: semantics or truth of a span; that the named line is the right line for
the meaning; that every claim carries a pin; git-revision binding; `## Claims` table pointers in
`verify`; chain hops; races between hashing and reading.

Sources 56 → 59 rows (S057 RFC 5147, S058 W3C SRI, S059 Python hashlib; tier A, mined, used by
`corpus/knowledge/line-binding-r31.md` and `revision-binding-r31.md`). QUALITY criteria 30 to 32
added. Routed defects D1 to D8 of the round-30 outside spot-check are repaired append-only (see
the lesson's intake table).

## Capabilities (round-31 change)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| claim location and revision binding (`verify-claims`) | a claim may name the line or line range its span sits on (`"line"`) and the SHA-256 of the exact source bytes it was made against (`"sha256"`); a span found elsewhere reads `mislocated`, a changed source reads `stale` | `python3 corpus/evidence/round31/c1-count.py` → 120/120; `python3 corpus/evidence/round31/c2-count.py` → 120/120; `corpus/knowledge/line-binding-r31.md`, `corpus/knowledge/revision-binding-r31.md` | 31 |

## Planned — round 32 (not started)

Candidates, not commitments: line binding for records' `## Claims` table pointers (`path:N`) in
`verify` mode (the C1 residual); a selftest case for end-line-only binding (a mutant the counter
kills but the selftest does not, `falsify/MutC1Binding.md`); `--json` appender serialization
(Planned26); the L0 fetch-scope answer. Round-28 C1 (path-denylist surface) stays open and
operator-owned.

### Round 31 — post-falsify gate revisions (same round)

The falsify wave found C2 contract violations outside the counter's fixture space
(`.ufo/waves/round-31/falsify/CriticEdgeC2.md`): a pin with an escaped trailing newline or NUL
decoded into a match, and a source whose file name holds `\` or a newline read `stale` because
`sha256sum` escapes such names. Fixed at `65d00cfc` (hash via stdin) and in the round's final gate
commit (exact JSON decoding that keeps trailing newlines; an escaped NUL is malformed), final gate
SHA-256 `0bc318b3…1258`. On the final gate both counters print 120/120 twice
(`.ufo/waves/round-31/measure/after-c{1,2}-run{7,8}-final.json`) and the selftest prints
`PASS (228 cases)`. Open, not fixed: a present non-string `"line"` or `"sha256"` treated as absent
would still score 120/120 on both counters (no fixture class; `falsify/MutC1Grammar.md`,
`falsify/MutC2Parse.md`, `falsify/CriticClaimsAfter31.md`); nested `"line"`/`"sha256"` keys are
read as the record's (flat-key parser, `falsify/ReviewIntegrationDiff31.md`); fail-open hashing
and span-before-stale are killed by the counter but not the selftest (`falsify/MutC2Hash.md`,
`falsify/MutSelftestNew31.md`). Planned round 32 adds these as fixture classes before data
(QUALITY 28).

## Round 32 — serialized manifest appends and the exempt-hop audit (two claims)

Base `7a7259f0ad41a68068131bfa422a829db9fd1b55` (gate SHA-256 `0bc318b3…1258`). Frozen design
`corpus/evidence/round32/claims.md`: v1 `4111607c` (attempt 1), v2 `3d586d3a` (after the pre-data
control wave broke both v1 counters; before any candidate receipt). Control evidence committed at
`f43dd5a3` and `a065845a`; candidate `0f96bc1c` (gate `10f2fe12…`); post-falsify C1 repairs
`53cf649c` (final gate SHA-256 `f4731885ac0f8307…03f0`). `verify-claims` and
`tools/quote-reopen.py` are not changed by either claim (anti-loop).

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 operability (lowest scored axis): the `verify-all --json` manifest append is one flock-held critical section on the manifest | `APPEND_SERIALIZED=0/24` (base gate, `.ufo/waves/round-32/controls/L1-design-v2/c1-base-s3201.json`) → `24/24` on the final gate, seeds 32101 and 32102 (`.ufo/waves/round-32/measure/final/c1-s3210{1,2}.json`); committed receipts on landed gates: `10f2fe12` ×18, `f4731885` ×3, all 24/24 (plus ×2 on the uncommitted intermediate `d13a76e3`, also 24/24) | `python3 corpus/evidence/round32/c1-count-v2.py --seed N --receipt F` | P1 v2 met; no run of the counter on a landed gate below 24 |
| C2 coverage: hops marked `unresolved` / `blocked-no-fetch` / `labelled-dead` are read in `verify-chain` | `EXEMPT_AUDIT_MATCH=0/132` (base, record checks fail; raw hop matches 96/132, R1–R3 0/36) → `132/132` on the final gate, seeds 32111 and 32112 (`measure/final/c2-s3211{1,2}.json`) (committed receipts: `10f2fe12` ×36, `f4731885` ×2, all 132/132; ×2 on the uncommitted intermediate `d13a76e3`, also 132/132) | `python3 corpus/evidence/round32/c2-count-v2.py --seed N --receipt F` | **not verified**: P2 v2 is met numerically, but a control that never opens a cited source (ranks source files by mtime/inode) also scores 132/132 on two seeds (`.ufo/waves/round-32/w2/CriticAxis32/control-metadata-s3232002{1,2}.json`), so the frozen counter does not discriminate (§9); found post-data, counter not amended |

The round-1 operability scale is unchanged: score 3 → 3 (delta 0); the C1 observable sits beside
it, as in rounds 25, 29 and 31. Separability (v2): C2 counter on the C1-only gate 0/132, C1 counter
on the C2-only gate 0/24 (`.ufo/waves/round-32/w2/SepAudit32/`).

Controls under v2 (`.ufo/waves/round-32/w1/*/v2/`): best C1 non-oracle 12/24 (sibling-file flock,
lockf, mkdir lock); best C2 pre-data control 126/132 (boundary skip, case-insensitive, whitespace
collapse); oracles C1 24/24, C2 132/132. Post-data, the metadata-order control above meets P2.

No-harm on the final gate (`measure/final/battery.out`): selftest `PASS (241 cases, 0 skipped)`,
first 228 case lines byte-identical to base (sha256 `a8873064…`); claims-r2 17/17 CLEAN; chain-r3
17/22 CLEAN, chain-r3-broken 1/2 DRIFT (`--root` fleet root; summaries gain `resolvable=0`);
round-1 observable 3/3; round-31 counters v2 120/120 each, v3 132/132 each. No corpus chain record
changes verdict (NoHarmCorpus32, 19/19). Declared behaviour changes: a host without flock(1) is
refused with exit 2 before the report (the gate's existing convention when sha256sum is missing);
a non-empty manifest unreadable under the lock is refused with exit 2.

Sources 59 → 61 rows (S060 Python fcntl, S061 RFC 9110; tier A, mined). QUALITY 33 to 35 added.
Round-31 routed defects R1–R6 repaired (`corpus/evidence/round32/r31-repairs.md`).

## Capabilities (round-32 change)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| serialized manifest appends (`verify-all --json`) | concurrent `verify-all` runs and any writer that flocks the manifest append without blank or glued lines; the probe reads the locked file even if the path is retargeted | `python3 corpus/evidence/round32/c1-count-v2.py` → 24/24 (`measure/final/`); `corpus/knowledge/manifest-append-lock-r32.md` | 32 |
| exempt-hop audit (`verify-chain`) | a hop marked "could not be followed" whose local citation resolves drifts with `CHAIN_EXEMPT_RESOLVABLE` | landed and reviewed (ReviewC2Probe32, MutC2Gate, CriticAxis32 witness), but its frozen counter is met by a no-reader control, so no counter verifies it; `corpus/knowledge/exempt-hop-audit-r32.md` | 32 (unverified measure) |

## Planned — round 33 (not started)

Candidates, not commitments: a C2 measure whose fixture decouples file metadata (creation order,
mtime, inode) from truth, scored against the metadata-order control before freezing; the nested
`"line"`/`"sha256"` key defect (unanchored `json_str`/`json_has_key`); a selftest case for a NUL
last byte through the locked-fd probe; the L0 fetch-scope answer. This supersedes the round-32
planned list above, whose `--json` serialization item is now landed and whose "end-line-only"
selftest case landed as case 237.

### 2026-10-23 correction (round 33, routed D2)

The round-32 C1 row above says committed receipts on `10f2fe12` ×18; the outside spot-check said
20. The count is **21**, all `APPEND_SERIALIZED=24/24`, counter `e6bf9531…`:
`python3 corpus/evidence/round33/d2-census.py --lane .` prints `C1 receipts on gate 10f2fe12: 21`
(and 3 on `f4731885`). The receipts that take the count from 18 to 21 are RerunC1b's load runs
(`w2/RerunC1b/rerunc1b-landed-load{1,2}.json`, 07:51:22Z) and its tmpfs run
(`rerunc1b-landed-fs.json`, 07:56:21Z), not critic re-scores. The C1 verdict does not change.
Evidence: `.ufo/waves/round-33/w1/ExecD2Census.md`, re-run by ReviewRepairsD2D3D5 (jq recount
identical).

## Round 33 — claim fields from the top-level object only (one claim)

Base `2b9cc73aed30c2e2c95699db6617d9531ef49fb2` (gate SHA-256 `f4731885…03f0`). Frozen design
`corpus/evidence/round33/claims.md`: v1 `3b528b9a`, v2 `e3e24ec8` (after the pre-data critic,
before any candidate receipt). Controls committed `96be7925`; candidate `eb179ec3` (gate
`52f07c74…`); integration `0fb300b5` (`94a7be5a…`); post-falsify repairs `0cad05eb` (`165acd5f…`)
and the final gate `43a1af35ca668fe5…4346`.

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 operability (lowest scored axis): `verify-claims` reads claim fields from the record's top-level JSON object only; nested members ignored; repeated top-level read fields invalid; string content never structure | `TOPLEVEL_FIELD_MATCH=60/156` (base, `.ufo/waves/round-33/controls/L1-design-v2/c1v2-base-s3311.json`) → `156/156` on every committed v2 run on a landed gate (`52f07c74` ×2, `94a7be5a` many, `165acd5f`, `43a1af35` seeds 3701/3702 in `measure/final/`; none below, ReceiptCensus33) | `python3 corpus/evidence/round33/c1-count-v2.py --seed N --receipt F` | **P1 v2 met; not verified by its counter for clause 3**: a gate that masks the counter's six fixed confuser literals, regex-strips nested containers and counts repeats also scores 156/156 (`.ufo/waves/round-33/w2/L1ShortcutMask/mask-s339{1,2}.json`, post-data). Non-counter evidence on the reader: differential fuzz 1950/1950 on the final gate (`measure/final/fz-9021{2,3,4}.json`), base 313/750 |

The round-1 operability scale is unchanged: score 3 → 3 (delta 0); the C1 observable sits beside
it. Controls under v2 (pre-data): best non-oracle 142/156; do-nothing 60/156; oracles 156/156.

Repairs (not claims): D1 exempt-hop counter v3 (`corpus/evidence/round32/c2-count-v3.py`): the
round-32 metadata-order control 132/132 under v2 → 87–98/132 under v3; landed audit 132/132 on
`f4731885`, `94a7be5a`, `165acd5f`, `43a1af35`. D2 above. D3 battery revision header
(`measure/final/battery.out`). D5 `corpus/evidence/round33/no-name-signals.sh`. QUALITY 36–41.

No-harm on the final gate: selftest `PASS (251 cases, 0 skipped)`, first 241 case lines identical
to base; claims-r2 17/17 CLEAN; chain-r3 17/22 CLEAN; broken 1/2 DRIFT; round-1 observable 3/3;
round-31 counters v3 132/132; round-32 C2 v2 132/132 (`measure/final/battery.out`). 35 committed
claims JSONL files: exit codes identical to base, every changed line a nested or duplicate record
(NoHarmCorpus33). Declared behaviour changes (fail closed): malformed lines (bare non-JSON tokens,
FF/VT whitespace, invalid escapes, unbalanced brackets, trailing bytes), an escaped NUL in a read
string field, and marker_default rows with repeated read fields now read `invalid`.

Sources 61 → 63 rows (S062 RFC 8259, S063 Python `json`; tier A, mined).

## Capabilities (round-33 change)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| top-level claim-field reader (`verify-claims`) | reads claim fields from the record's top-level object only, refuses repeated read fields and malformed lines | `python3 corpus/evidence/round33/c1-count-v2.py` → 156/156 (counter met by a fixture-literal shortcut too, so clause 3 rests on the fuzz evidence); `corpus/knowledge/claim-record-fields-r33.md` | 33 |

## Planned — round 34 (not started)

Candidates, not commitments: a counter whose confuser content is generated per seed (QUALITY 40);
member grammar inside nested values; raw control bytes in strings; spans of 32 KiB or more
(`tok_span_at` argv limit); the L0 fetch-scope answer.

### 2026-10-23 correction (round 34, routed E1) — round-33 capabilities row

The round-33 capabilities row says clause 3 "rests on the fuzz evidence"; the three fuzz receipts it
leaned on (`.ufo/waves/round-33/measure/final/fz-9021{2,3,4}.json`) bind gate `b2c07eda…`, which
matches no committed blob. Re-run on the committed landed bytes `43a1af35…4346`: 650/650 ×3,
calibration 60/60 (`.ufo/waves/round-34/w1/ExecE1Fuzz/fz-9021{2,3,4}-landed-43a1af35.json`). The
per-seed confuser counter (`corpus/evidence/round33/c1-count-v3.py`, E2) does not close clause 3: the
mask gate misses on seeds 9401/9402 (155/156) but meets 156/156 on seed 61111 (R34ReviewRepairs).
E3: `SKILL.md` metadata range corrected to cases 137–208 and 210–215.

## Round 34 — long claim spans (one claim)

Base `b80539005176ac6ce39bc1c7afb846cb1f2f7c75` (gate `43a1af35…4346`). Frozen design
`corpus/evidence/round34/claims.md`: v1 `70feb5ea`, v2 `ef16afb1`, v3 `f20aeaa7` (all before any
candidate receipt). Pre-data control evidence `a92b9f43`; candidate `3026a4e5` (gate
`772a1d8e4d94dbf3…3e58`); measurement `934d7cb7`.

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 operability (lowest scored axis): `verify-claims` verifies spans of 32768..65536 bytes (surface: `tok_span_at` / `tok_span_all`, the argv/PCRE-limited span matcher) | `LONGSPAN_MATCH=25/42` (base, `LC_ALL=C`, `.ufo/waves/round-34/controls/L1-base-v3/base-v3-C-s3493.json`; 0/42 ×2 by the 1500 s bound in the UTF-8 locale) → `42/42` on seeds 3601, 3602 (`LC_ALL=C`) and 3603 (UTF-8) (`.ufo/waves/round-34/measure/`); 42/42 on five more fresh seeds by R34RerunC1v3 and R34ReviewPatchC; no committed v3 run on the landed gate below 42 | `LC_ALL=C python3 corpus/evidence/round34/c1-count-v3.py --seed N --receipt F` | **unverified (required controls held)** — numerical P1 v3 met; five wave-1 seats ended on provider holds (CtlC1Shortcut, CtlC1Windows, CtlC1Halves, MutC1Counter, CritC1AxisFit), their controls may not be substituted, and the frozen design declared C1 unverified before data (`claims.md`, "Held controls and exclusions") |

The round-1 operability scale is unchanged: score 3 → 3 (delta 0). Non-held controls under v3
(pre-data): best seat control 40/42 (partial fixes, boundary left-only; `controls/L1-v3-rescore/`);
L1 diagnostic shapes 33–38/42; feasibility oracle 42/42. Excluded (held-shape re-authoring):
`controls/L1-keyed/`, `L1-windows/`, window/fraction/halves/shoulder helpers and their receipts.

No-harm on the landed gate: battery PASS, 11 rows (`measure/battery/battery.out`): selftest
`PASS (253 cases)`, first 251 case lines identical to base (sha256 `46c9c092…` both); claims-r2 17/17;
chain-r3 17/22; broken 1/2 DRIFT; round-1 observable 3/3; r31 v3 132/132 ×2; r32 C2 v2 and v3
132/132; r33 C1 v2 156/156. Disclosed: under `LC_ALL=C` the selftest fails on base (11 cases) and
landed gate (10 cases) alike (`measure/selftest-env/`); the default-locale selftest passes.

Repairs (not claims): E1 (fuzz re-run on committed bytes; corrections above and in
`knowledge/claim-record-fields-r33.md`), E2 (per-seed confuser counter; not closed), E3 (SKILL range),
E4 (`w1/ExecE4Census/receipt-binding.py`; QUALITY 42), E5 (QUALITY 43). QUALITY 42–44.

Sources 63 → 66 rows (S064 execve(2), S065 pcre2limits(3), S066 grep(1); tier A, mined; opened
from installed man pages).

## Round 34 attempt 2 — dead zone + self-audit (two claims)

Attempt 1 died lane-dead-no-report after its commits landed; attempt 2 inherits C1 unchanged
(verdict `unverified (required controls held)` stands — the frozen exclusion is not re-opened)
and declares two new claims on distinct axes. Frozen design v4
`corpus/evidence/round34/claims-a2.md` (`7c7eb3a6`), before any attempt-2 candidate receipt.

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C2 operability (lowest scored axis): `verify-claims` verifies spans of 32765..32767 bytes (the PCRE dead zone: the 4N-byte pattern fits argv but PCRE2 refuses it, "regular expression is too large", S065) | `DEADZONE_MATCH=21/37` (unfixed gate `772a1d8e`, seeds 5011/5023, `measure-a2/c2-before-s*.json`) → `37/37` on seeds 5011, 5023, 5033, 5047 on gate `a6307edf…` (`measure-a2/c2-after-s*.json`); no committed run below 37 | `LC_ALL=C python3 corpus/evidence/round34/c2-count.py --seed N --receipt F` | **verified (measured)** — do-nothing 21/37, four 37/37 receipts (seeds 5011/5023/5033/5047), re-derived by wave seats ExecC2Rerun (fresh 7311/7417/7589), RevC2Receipts and MutC2Counter; no-harm battery 11 rows PASS; selftest 256. Disclosures: the frozen design's predicted before-ceiling of 4/37 was wrong (true 21/37 — erratum in `claims-a2.md`); window controls that compare every byte at these lengths (positional 16384-byte edge windows) correctly meet 37/37 as exact-verifier equivalents (MutC2Windows); a fixture-keyed engine that implements the exact semantics is output-equivalent and no output-only counter can exclude it (MutC2Keyed 2/6) — routed as r35 hardening (work-proof battery), not a kill: the landed gate is not keyed and P2 is gate-scoped |
| C3 calibration: self-assessment text vs observed repo state, counted | no committed count existed (E4/E5 were point repairs); the first counted run printed `SELF_AUDIT_MISMATCHES=0` over 43 checks (`measure-a2/audit-first-run.txt`) → reshaped to a bounded structural-audit acquisition after wave criticism (CritC3Claim's shallow-set do-nothing reproduced identical 0/0 under planted drift): the auditor deepened to 62 checks (content pins of the self-assessment documents, 9/9 measurement-receipt bindings + a receipt_gate_file kind for control receipts, HEAD-byte reads so a dirty worktree cannot move the count, SET_SHA256 per run); identical before/after measurement — 3 counted at the pre-integration tree (2 real: the SKILL.md banner vs the gate's exact output form, found by ScoutSkillTally; 1 superseded-pin artifact) with 1 undispositioned (`measure-a2/audit-v3-prelim.txt`), at the landed tree the count is 1 (the superseded tool pin, dispositioned) over 62 checks with the set digest printed (`measure-a2/audit-v3-final.txt`); the SCORECARD count string the set pins is the first-run `SELF_AUDIT_MISMATCHES=0` literal above; assessment-derived controls: committed negative control 5/5 lies killed exactly (MutC3Inject), junk auditor killed by re-derivation, do-nothing unreachable (MutC3Bypass) | `python3 corpus/evidence/round34/self-audit.py` | **verified (reshaped, bounded acquisition)** — wave verdicts: MutC3Inject/MutC3Bypass/RevC3Set (set valid; shallow-as-written) + CritC3Claim (counterexample stands against the written form; its prescription is the landed reshape); r35 candidates named in the lesson |

Per-axis: operability improved (C2: three span lengths moved from false-unsupported to
verdict-bearing; C1's capability stands unverified); calibration improved (C3: the lane's
round-34 self-description is now machine-audited, 43 checks, count-committed). No axis harmed:
the no-harm battery holds every prior row (selftest 256 with first 253 case lines identical,
claims 17/17, chain 17/22, broken 1/2, observable 3/3, five counters hold). The disclosed
behaviour change: 32765..32767-byte quote anchors in `verify-chain` now resolve instead of
reading `anchor-missing` (same class as C1's false-negative closure). Depth improved
(`corpus/knowledge/dead-zone-pcre-r34.md`); freshness improved narrowly (S065 re-opened, pins
unchanged); adjacency unchanged.

## Capabilities (round-34 change)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| long-span verification (`verify-claims`) | locates and binds spans of 32768..65536 bytes by a 4096-byte probe plus whole-span confirmation, instead of failing on the argv/PCRE pattern limit | `LC_ALL=C python3 corpus/evidence/round34/c1-count-v3.py` → 42/42 (`.ufo/waves/round-34/measure/`); `corpus/knowledge/long-span-argv-r34.md` | 34 (unverified measure: required controls held) |
| dead-zone span verification (`verify-claims`) | locates and binds spans of 32765..32767 bytes — between the PCRE2 compiled-pattern ceiling and the argv per-string limit — via the same probe-and-confirm matcher | `LC_ALL=C python3 corpus/evidence/round34/c2-count.py` → 37/37 ×4 seeds (`.ufo/waves/round-34/measure-a2/`); `corpus/knowledge/dead-zone-pcre-r34.md` | 34 (attempt 2, verified) |

## Planned — round 35 (not started)

Candidates, not commitments: E2 (a clause-3 counter every lexer-less mask fails on every seed);
the selftest's `LC_ALL=C` dependence; the L0 fetch-scope answer. (Landed by round 34 attempt 2
and removed from this list: the PCRE dead zone — measured as exactly the 3 lengths 32765–32767,
not "about 28000–32767", C2; chunk-matcher selftest cases 254–256.)

## Round 35 — the pinned binary and the routing witness (two claims)

Base `08be4c9e3a4ebe55d915ce4761c81854286c23ae` (gate `a6307edf…2995b`). Frozen design
`corpus/evidence/round35/claims.md` (`0e167649`, P1/P2 + kill rules + pre-data controls;
post-data §Erratum is append-only). First landing `e87c5d7e` (gate `1f2fb4f5…c617`); the pin was
then hardened on the three vectors the wave reported (`command`-keyword dispatch, `head` in the
version probe, the dead `command -v grep` fallback) and the final gate is
`a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`; both claims re-measured on the
final bytes (`.ufo/waves/round-35/final/`).

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 operability (lowest scored axis): `research-gate.sh` resolves, verifies and pins ONE absolute grep binary at startup and refuses an unverifiable pin with a named exit-2 refusal, instead of resolving bare `grep` through `PATH` at each matcher call | `GREP_PIN_MATCH=0/9` (base gate `a6307edf`, `controls/c1-base-s3501.json`) → `9/9` on seeds 3529 and 3539 on the final gate (`final/c1-s3529.json`, `final/c1-s3539.json`); cheapest non-oracle control (hardcoded pin, no provenance/override/echo) 3/9 (`controls/c1-hardcoded-s3501.json`) | `python3 corpus/evidence/round35/c1-count.py --gate tools/research-gate.sh --seed N` | **met under P1; reading narrowed** — the counter proves path+version pinning, refusal shape and output equality. It does **not** measure per-call engine identity: a read-before-refusal mutant (`147ded03…`), correct-output engines replacing `tok_span_offsets_direct` (`fd6d5a8e…`, `9040dcba…`) and a `BASH_ENV` `command()` swap all score 9/9 (wave seats MutPinRefusals, MutGrepPinEngines, MutGrepShimEnv; claims.md §Erratum 3). The ordering claim rests on strace (0 opens vs 2). |
| C2 calibration: the lane's receipts can separate an output-equivalent keyed engine from the landed dead-zone routing (mechanism witness), where output counters cannot | `WITNESS_SEPARATED=0/2 battery=absent` (base tree; `controls/c2-before-s3501.json`) → `WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass` on seeds 3529 and 3539 (`final/c2-s3529.json`, `final/c2-s3539.json`); witness stubs fail both ways (`controls/c2-stub-{pass,fail}-s3501.json`) | `python3 corpus/evidence/round35/c2-count.py --seed N` | **met under P2 as a ROUTING witness** — it proves the routed matcher was entered, not that its body ran: a one-record shortcut (8 stamps for 8 records), a length-keyed engine (6/31 seeds), a chunk call with a discarded result and a body-replaced matcher (`3e5648b8…`) all pass (wave seats MutC2KeyedBattery, MutWitnessBypass1/2, MutWitnessThreshold; QUALITY 49 is the r36 requirement). Axis caveat recorded (wave critic CritC2AxisFit): P2 measures receipt strength, not the lane's self-assessment accuracy. |

The round-1 operability scale is unchanged: score 3 → 3 (delta 0); the C1 observable sits beside
it, as in rounds 25, 29, 31–34.

Repairs (not claims): R1 `slen` reads its own parameter (probe: base `offsets=0` / landed
`offsets=1 first=5`; `repairs/slen-probe.sh`, wave seats MutSlenScope and RevSlenSweep re-derived);
R2 case-range comments 252-253 and 254-256 (all 14 gate case-number comments verified by
RevCaseRanges); R3 round-34 wave-debris count reconciled (26 tracked `w2a2/*.md`; the three
`ExecC2Oracle` texts tracked since `6a3cc32`); R4 runbook rows in `SKILL.md` + three knowledge
entries with metadata headers.

No-harm on the final gate: `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`; case ranges
252-253/254-256 confirmed from the run's own `ok-case` labels; the wave re-derived C1 9/9 on the
pre-hardening landed gate (ExecC1Fresh1) and the prior counters were exercised in the wave.
Wave: one v2 wave, 65 seats (attack 27 = 42%), `1f2fb4f5` attacked, final gate re-measured;
one dead seat (CritWitnessBlind, provider `cyber_policy` refusal, not retried).
Sources 66 → 68 rows (S067 exec(3), S068 bash(1); tier A, both opened 2026-10-23). QUALITY 45–49
added.

## Capabilities (round-35 change)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| pinned-binary resolution (`research-gate.sh`) | resolves ONE absolute grep (`/usr/bin/grep` → `/bin/grep`; `RESEARCH_GATE_GREP` override, absolute + GNU-reporting), refuses an unverifiable pin with `GREP_PROVENANCE` and exit 2 before reading a record, runs every grep call through a direct-path wrapper (never `command`, never `head`), and can name the pin for a receipt (`CHOUSA_GREP_PIN_ECHO=1`) | `python3 corpus/evidence/round35/c1-count.py` → 9/9 (`final/c1-s*.json`); `corpus/knowledge/grep-pin-r35.md` | 35 (scope: path + version, not engine identity) |
| output-vs-routing witness (`tools/mechanism-witness.py`) | scores a candidate gate on output AND on whether the routed matcher function was entered, with a per-seed randomized fixture; separates two output-equivalent keyed engines while the landed gate passes both, and reports the trace-stamp counts | `python3 corpus/evidence/round35/c2-count.py` → 2/2 separated (`final/c2-s*.json`); `corpus/knowledge/keyed-engine-output-equivalence-r35.md` (survivor table) | 35 (scope: routing, not computation) |

## Planned — round 36 (not started)

Candidates, not commitments: a **semantic canary** that belongs to both counters — a pinned needle
set whose match results differ between a correct matcher and an exact-search substitute (or a
verified GNU-reporting recorder that must log ≥1 `-z -P` 4N-hex query) — the class three wave seats
converged on (QUALITY 45, 49); per-record witness attribution + per-record fixture id-shape
diversity; C1 receipt `counter_sha256` binding; witness tolerance to a matcher rename (currently
`WITNESS=unparseable` → a spurious C2 kill); the `chousa`-root key class; the L0 fetch-scope answer;
the carried C1 debt (spans ≥ 32768, `unverified (required controls held)`) stays open.

## Round 36 — the engine-swap canary and per-record attribution (two claims)

Gate bytes landed at `700bd5fcbf9abc118a6a0f078d51a2e7460c2878` (inherited attempt-1 freeze:
counters, witness, gate edits, controls, receipts), gate
`a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`; before-state control
`.ufo/waves/round-36/controls/base-gate-r36.sh`
(`a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`). Frozen design
`corpus/evidence/round36/claims.md` (P1/P2 + kill rules + limits; §Erratum appended after the
data, 13 entries).

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 operability (lowest scored axis, 3/10): the gate and its counter separate an output-equivalent engine swap in fourteen scenarios — pin resolution and refusals, distinct-path override honoured and observed, live `--version` identity, per-record argv attribution, manifest hash identity under a hostile `sha256sum`, C-locale decode, and the two pin echo/drift cells | `ENGINE_SWAP_CANARY=10/14` (base gate, `measure/c1-before-s36001.json`, re-derived seed 36321 by `w1/ExecC1BaseCtl`) → `14/14` `predicate_holds=true` on seeds 36001/36011 (construction, `measure/c1-after-s36001.json`, `c1-after-s36011.json`) and 36301/36311/36331/36341/36351/36361 on landed-gate receipts (wave + L1: `w1/*/c1-*.json` with `gate_sha256=a7d3922c…`, `measure-l1/c1-s36361.json`; the same seeds also appear in variant/control receipts under `w1/RevCounterHonesty/` whose gates are NOT the landed gate) | `python3 corpus/evidence/round36/c1-count.py --gate tools/research-gate.sh --seed N --receipt F` | **met under P1; reading narrowed** — the four failures (S11-S14) are this round's separations; S1-S10 also pass on the base control, S7-S9 assert the echo/refusal contract rather than per-call engine identity (QUALITY 52), and S10 is what keeps a no-call gate from scoring 14/14 (§Erratum 5) |
| C2 calibration: the lane's per-record witness separates the five output-equivalent engines the round-35 witness admitted, through the pinned engine's out-of-band argv channel, while a renamed matcher passes | `WITNESS_PER_RECORD=2/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=absent RENAMED=fail` (base gate + `tools/mechanism-witness.py`, `measure/c2-before-legacy-s36001.json`, re-derived seed 36321 by `w1/ExecC2LegacyCtl`) → `5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass` on seeds 36001/36011 (construction) and 36301/36311/36371 (wave + L1: `w1/*/c2-*.json`, `measure-l1/c2-s36371.json`); witness stubs fail 0/5 and landed-fail | `python3 corpus/evidence/round36/c2-count.py --gate tools/research-gate.sh --witness tools/argv-witness.py --seed N --receipt F` | **met under P2 as a query witness** — it proves the pinned matcher was queried per record, not that the answer was used; the call-for-show and read-the-recorder limits are stated (§Limits, §Erratum 2-3) |

The round-1 operability scale is unchanged: score 3 → 3 (delta 0); the C1 observable sits beside
it, as in rounds 25, 29, 31-35.

Repairs (not claims): R1 `--pin` capture environment scrubs `CHOUSA_GREP_PIN_ECHO`; R2 the drift
diagnostic names `GATE_GREP`; R3 one absolute `sha256sum` with a 64-lowercase-hex contract for
`verify-all --json` and `--pin` (S070); R4 `json_unescape` decodes UTF-8 by hand in a `LC_ALL=C`
scope; R5 selftest cases 257-261 (256 → 261); R6 pin-coverage ledger in `SKILL.md` (verified:
`verify-integrity`/`verify-sweeps` make 1 recorder call, `--version`, 0 matcher calls —
`w1/ExecModeCoverage/`); R7 both counters' docstring counts corrected to their receipts.

No-harm on the landed gate: `RESEARCH_GATE_SELFTEST: PASS (261 cases, 0 skipped)` under default,
`LC_ALL=C` and a scratch `TMPDIR` (`w1/ExecSelftest/`); pinned observables unchanged — claims
17/17, chain 17/22, broken control 1/2, archives 3/3 (`w1/SentNoHarm.md`); the wave's
scenario-isolation probe found no falsification (`w1/LabScenarioIsolation.md`, 14/14 twice on
seed 36351).

Wave: one v1 wave, 36 seats (attack roles 10 = 28%; planner seat held by the L1, its data-walk on
the LabScenarioIsolation seat), one dead seat (`CritC1Swap`, provider `cyber_policy` refusal, not
retried). Sources 68 → 70 rows (S069 grep(1) `-o`+`-b`, S070 sha256sum(1); tier A, both opened
2026-10-23). QUALITY 50-52 added. Lesson `corpus/lessons/round-36.md`.

## Capabilities (round-36 change)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| engine-swap canary (`corpus/evidence/round36/c1-count.py`) | scores a candidate gate on fourteen swap/contract scenarios with per-scenario fixtures and receipts, separating the round-35 gate's four open holes (manifest hash shim, C-locale decode, pin echo isolation, drift token) | `python3 corpus/evidence/round36/c1-count.py` → 14/14 (`measure/c1-*.json`, `measure-l1/c1-s36361.json`); `corpus/knowledge/engine-swap-canary-r36.md` | 36 (scope: fourteen asserted behaviours, four newly discriminated) |
| per-record argv attribution (`tools/argv-witness.py`) | separates output-equivalent engines per record through the pinned engine's NUL-delimited argv log, writes the channel outside the gate's environment, and does not false-kill a renamed matcher | `python3 corpus/evidence/round36/c2-count.py` → 5/5 + renamed pass (`measure/c2-*.json`, `measure-l1/c2-s36371.json`); `corpus/knowledge/per-record-argv-attribution-r36.md` | 36 (scope: query, not use) |

## Round 37 — claim-pin provenance and pin-capture environment (two claims)

Freeze commit `b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65` (inherited attempt-4 freeze: counters,
gate fixes, selftest 262-267, frozen `corpus/evidence/round37/claims.md`, base control
`.ufo/waves/round-37/controls/base-gate-r37.sh` = `a7d3922c…f54e8`); landed gate
`9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39`. Before-state controls committed at the freeze. Round shape: v1,
wave 1 (39 seats, inherited dispatch, 8 returned, 31 dead by orchestrator death — never
replaced) + one residual reviewer/critic call. Attempt 5 of the round (5 watchdog
`lane-dead-no-report` lines).

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 operability (lowest scored axis, 3/10): a claim's `sha256` revision pin is hashed through one pinned absolute `sha256sum` and never through the caller's PATH (`sha256sum`/`cut`), so no PATH shim can move a pin verdict in either direction | `CLAIM_PIN_PROVENANCE_MATCH=2/7` (base gate, `receipts/c1-base-s37001.json`; wave re-derivation seeds 37101/37123 under `w1/ExecC1BaseRederive/`) → `7/7` `predicate_holds=true` on seeds 37001/37111/37133 (construction + wave) and 37701 (L1, `receipts/c1-after-s37701.json`), 37901/37921 (wave, `receipts/c1-after-s379{01,21}.json`), 41377/52819 (residual, `residual/RevC1FreshSeed.md`), every after-receipt `gate_sha256=9fcac047…` | `python3 corpus/evidence/round37/c1-count.py --gate tools/research-gate.sh --seed N --receipt F` | predicate **verified**; claim text **falsified** beyond PATH-independence — unprivileged `LD_PRELOAD` interposition into the pin child (inherits the caller's loader env at `research-gate.sh:442`; host coreutils 9.12 `sha256sum` imports OpenSSL `SHA256_Update`) moved verdicts 4/7 and 3/7 on the landed gate (`residual/CritC1Kill.md` C27/C18); narrowed + fix direction in claims §Erratum 6; the defect pre-exists the round (base gate equally vulnerable), so no axis is harmed by the round's changes |
| C2 freshness: a `--pin` baseline is independent of the caller's `BASH_ENV` — the capture child runs `env -u BASH_ENV` (S071), so a startup file re-exporting a scrubbed variable or moving `CHOUSA_ROOT` cannot change the pinned capture, embed a receipt line, or make a later plain `--drift` report phantom drift | `PIN_CAPTURE_ENV_MATCH=3/7` (base gate, `receipts/c2-base-s37021.json`; wave re-derivation seeds 37201/37223) → `7/7` `predicate_holds=true` on seeds 37021/37211/37311 (construction + wave) and 37721 (L1, `receipts/c2-after-s37721.json`), 37941/37961 (wave, `receipts/c2-after-s379{41,61}.json`), 38101 (residual, `residual/RevC2FreshSeed.md`), every after-receipt `gate_sha256=9fcac047…` | `python3 corpus/evidence/round37/c2-count.py --gate tools/research-gate.sh --seed N --receipt F` | predicate **verified**; claim text **narrowed** — function exports defeat the variable-only reading: a startup file's `export -f date` reaches the capture child through `BASH_FUNC_date%%` (not scrubbed) and embeds a receipt line with phantom drift, demonstrated on the landed gate (`residual/RevC2FreshSeed.md`; independently reproduced `residual/CritC2Kill.md` finding 1); narrowed + fix direction in claims §Erratum 5; 28 adjacent vectors otherwise held or confirmed named limits (`residual/CritC2Kill.md`) |

Separability: each counter reads the other's surface not at all; the wave's single-hunk gate
mutants isolate each fix (`w1/ExecMutGateC1.md` C1 2/7 while C2 7/7; `w1/ExecMutGateC2.md` C2
3/7 while C1 7/7); the counter-expectation mutants both score 6/7 exit 1
(`w1/ExecMutC1Counter.md`). No-harm on the landed gate: selftest PASS 267 cases 0 skipped
(L1, default env); claims 17/17 CLEAN, chain 17/22 CLEAN, broken control 1/2 DRIFT, archives
3/3 (L1 re-run with the recorded commands; the wave seat's `--root .` mis-invocation that read
refusals as harm is a lesson mistake, not gate harm).

| axis | verdict | evidence (before → after) |
|---|---|---|
| operability | **improved** | C1: the pin digest channel is PATH-independent by measurement (2/7 → 7/7 across six seeds, three independent runners); selftest 261 → 267 cases held. |
| freshness | **improved** | C2: pin/drift re-derivation is independent of the caller's `BASH_ENV` (3/7 → 7/7 across six seeds); the mechanism source is pinned (S071). |
| depth | **improved** | `corpus/knowledge/claim-pin-provenance-r37.md` and `pin-capture-env-r37.md`: the fix, the scenario tables, the frozen limits (PATH-independence not tamper-proof hashing; gate-process `BASH_ENV` still sourced; `--posix`/`ENV`/`SHELLOPTS`/`TMPDIR` named debt). |
| coverage | **unchanged** | no new measured surface; both r36 observables held on the new bytes. |
| calibration | **unchanged** | the no-harm mis-invocation was caught by re-running the pinned commands, and is recorded as a lesson mistake with QUALITY 53. |
| adjacency | **unchanged** | zero network (all sources opened from installed man pages); corpus read-only; wave seats wrote only in-lane. |

Admission: **ADMIT-with-errata, operator rules** — both frozen predicates verify on every
committed receipt and no axis is harmed (the two falsified claim-text clauses describe
defects that pre-exist the round's changes), but the residual wave falsified both claims'
general wordings beyond their counters' cells, so the claims as first written do not stand;
the narrowings and fix directions are frozen as claims §Errata 5-6 and carried to round 38.
No scalar score. Learning trends: expansion/quality **improved**, discernment **improved**
(the residual wave's two claim-text kills are the lane's first in-round falsifications of
its own frozen claims). Round 38 candidates below.

## Planned — round 38 (not started)

Candidates, not commitments: the prefix-64 attribution bypass (a stricter span rule plus a V7
prefix-query variant; r36 claims §Erratum 8); per-scenario counter assertions tightened to
their names (S7-S9, QUALITY 52); three dead fields in `tools/argv-witness.py` (`_stderr.log`
write, `fixture_root_prefix`, `channel` — SimpDiff D1-D3); the verdict-flipping locale seam in
the metadata screener (`research-gate.sh:1015`, 1019, 762/1083 — `[[:space:]]`/`-i` under the
caller's locale; r36 claims §Erratum 13); `counter_sha256` bound into every receipt (carried
debt); a call-for-show engine measurement (the stated C2 limit, r36 §Erratum 9); the S068
anchor-label supersede row (r36 spot-check defect 8, carried by the round-37 lesson); the
witnessed `SHELLOPTS=noexec` false pin success (pin exits 0 with no baseline; operability
defect inside the named shell-option limit — `residual/CritC2Kill.md`) and the exported-`env`
function witness (pinning one absolute `env` closes that one witness, not the parent-function
class); the r37 claim-text kills — pin-child loader-environment scrub (`env -u LD_PRELOAD
-u LD_LIBRARY_PATH …`, `residual/CritC1Kill.md`) plus an LD_PRELOAD counter cell, and the
capture-side `BASH_FUNC_*` scrub (or minimal `env -i` channel) plus a genuinely-exported
counter scenario (`residual/RevC2FreshSeed.md`, claims §Errata 5-6); counter-strength debt
(receipts bind `gate_sha256` post-run and score gate self-report — `residual/RevC1FreshSeed.md`
F1/F2, `residual/RevC2FreshSeed.md` trust analysis; `counter_sha256` still carried); the
carried C1 debt (spans ≥ 32768) stays open.

## Round 38 — env-pin capture and receipt binding (two claims)

Freeze commit `504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f` (counters, gate fix, frozen
`corpus/evidence/round38/claims.md`, base controls, construction receipts); wave-1
integration `1f0add702232903f959c8bc9a15acabd8439a033`; SentScope integration
`8e93bc916527b3c21f0f702967fa65c3b4c31699`; final bytes land with this entry (gate
`0447ad14b613…`, counters `6a9600ea6b1f…`/`93bf06daac30…`, verifier `33c7c87e7a5f…`).
Round shape: v1 two waves (32+32 seats, 2 dead per wave by provider `cyber_policy`;
§3 floor inside wave 1; planner seat held by the L1 with the data-walk on the
ScoutCounters/RevClaims seats). Landed gate selftest: PASS (272 cases, 0 skipped).

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 operability (lowest scored axis, 3/10): the canonical pin capture's child runs through ONE pinned absolute `env` (RESEARCH_GATE_ENV override, GNU-reporting, refused exit 2 `ENV_PROVENANCE`), so a caller-exported function `env` (BASH_FUNC_env%%) cannot interpose on the capture — narrowed by §Erratum 6 to function-export interposition + override shape | `ENV_PIN_CAPTURE_MATCH=2/7` on BOTH base gates (`a7d3922c…` pre-round-37, `9fcac047…` pre-round-38) → `7/7` `predicate_holds=true` on the landed gate: construction seeds 38001/38011 (receipts `c1-after-s38001/s38011.json`), wave-1 seeds 38211/38231/38251 (`w1/ExecC1Rederive.md`, `w1/ScribeKnowledgeC1.md`), wave-2 seeds 38411/38431 (`w2/W2ExecC1Final.md`); every committed receipt `VERIFY: ok` | `python3 corpus/evidence/round38/c1-count.py --gate tools/research-gate.sh --seed N --receipt F` | **met under the narrowed reading; narrowing frozen as §Erratum 6** (PATH half, sibling-name witnesses, bash vectors: named and demonstrated, not measured by the seven cells) |
| C2 calibration: every round-38 counter receipt binds gate_sha256_pre==post (changed gate refuses exit 2, NO receipt), counter_sha256, expect_sha256, receipt_sha256; verify-receipts re-derives from committed bytes and fails closed — narrowed by §Errata 2/10/11 to integrity + self-consistency, NOT authorship | `RECEIPT_BINDING_MATCH=0/7` (the r37-counter pipeline, `receipts/c2-base-s38101.json`) → `7/7` on the landed gate: construction 38101/38111, wave-1 38221/38241, wave-2 38421/38441/38461 (base gate 7/7 — separability, `w2/W2ExecC2Final.md`); the four wave-1 verifier kills refuse by name in wave 2 (`w2/W2CritLaundering.md`, `w2/W2ScribeKnowledgeC2.md`) | `python3 corpus/evidence/round38/c2-count.py --gate tools/research-gate.sh --seed N --receipt F` | **met under the narrowed reading; kill-class fixtures closed by Errata 2/3/4/9, the verifier-binding gap named as §Erratum 11 with verifier_sha256 carried** |

The round-1 operability scale is unchanged: score 3 → 3 (delta 0); the C1/C2
observables sit beside it, as in rounds 25, 29, 31–37.

Separability (measured, `w1/RevSeparability.md`, `w2/W2RevSeparabilityFinal.md`): gate-side
single hunk (capture `"$ENV_BIN"` → bare `env`) drops c1 to 4/7 while its receipt still binds;
counter-side hunk (the subject counter's pre!=post refusal disabled) drops c2 to 6/7 while c1
stays 7/7; c2 on the unfixed base gate is 7/7 post-Erratum-4 (its control is the r37 counter,
not the gate). No-harm on the final bytes: selftest PASS 272; claims 17/17 CLEAN; chain 17/22
CLEAN; broken control DRIFT drift-sections=2; archives 3/3 (`w2/W2ExecNoHarmFinal.md`).

| axis | verdict | evidence (before → after) |
|---|---|---|
| operability | **improved** | C1: the capture's env invocation is pinned, verified GNU-reporting, refused before any mode; 2/7 → 7/7 across both base gates and five+ independent seed runners; selftest 267 → 272 |
| calibration | **improved** | C2: receipts now bind counter/expect/receipt digests and pre==post gate hashes with a census-tied verifier; the lane's first in-round kills of its own frozen claims are frozen as errata, not absorbed; 0/7 → 7/7 |
| depth | **improved** | `knowledge/env-pin-capture-r38.md` and `knowledge/receipt-binding-r38.md`: the mechanism, BOTH delivery mechanisms, the wave-kill record, the narrowed readings, the r39 cell list |
| coverage | **unchanged** | no new measured verification surface; the seven modes and fixtures held byte-stable |
| freshness | **improved narrowly** | the r37 knowledge docs' stale "7/7 on every committed receipt" corrected (receipt-audit L1); S070's anchor-label defect dispositioned via the S073 supersede row |
| adjacency | **unchanged** | zero network (strace, both waves); sibling-overlap scans (w1/w2) confirm in-province; the loader-env channel stays tsukuroi's, named as debt |

Admission: **ADMIT-with-errata, operator rules** — both frozen predicates verify on every
committed receipt and no axis is harmed (the falsified general clauses name pre-existing or
out-of-surface defects, each demonstrated and dispositioned); the claims as first written do
not stand un-narrowed; §Errata 1–13 freeze the narrowings and the r39 fix directions.
No scalar score. Learning trends: expansion/quality **improved**, discernment **improved**
(the lane's first self-kills of its own frozen claims, honestly frozen).

Attribution correction (routed defect D4, appended round 39): the wave-2
seeds named above (38411/38431/38421/38441) and the no-harm battery ran at
integration revision `8e93bc91…` (gate `37e2b996…`), not at the final bytes;
the tip-byte evidence is the regenerated receipt set (nine receipts binding
`0447ad14…`, statically verified 9/9 by the r38 closure) plus the one-hunk
diff `8e93bc91…→870074e8…` and the one seat-observed tip-byte counter run
(`w2/W2MutGateFinal.md` set C). The candidate-hash supersession itself is
named as round-38 claims Erratum 14.

## Planned — round 39 (superseded by the round-39 verdict below)

Candidates, not commitments: the pre-registered measurement cells from Errata 5/6/11 —
an eighth c1 scenario family covering the PATH `env` shim, the PATH `bash` shim, hostile
drift, the positive override-honoured witness and the relative-override refusal (a new
frozen 8-scenario table for both counters); the loader scrub (`env -u LD_PRELOAD -u
LD_LIBRARY_PATH …` on the capture child and the claim-pin child, with an LD_PRELOAD counter
cell); `verifier_sha256` + `subject_counter_sha256` bound into c2 receipts (the debt
demonstrated live twice this round); refusal-label re-derivation in verify; the SimpCounters
dead-field deletions (subject_counter reader, --tmp plumbing, path strings, BASH fallback
arm); the SHELLOPTS=noexec pre-startup boundary only if separately specified; the carried
spans-≥32768 debt; the metadata-screener locale seam; the argv-witness D1-D3 dead fields;
the S068-scope second-row question remains settled (S072 uses the info file).

## Round 39 — capture bash pin and verifier/subject binding (two claims)

Freeze disclosure: the L1's construction runs on seeds 39001/39011 (C1) and
39101 (C2) preceded the freeze of `corpus/evidence/round39/claims.md` and are
disclosed as such; the orchestrator-dispatched wave and the closure re-derive
on fresh seeds. Host mapping this round: the seat holds no live L2 dispatch —
the round's swarm is PREPARED under `.ufo/waves/round-39/` (validated spec)
and itemized as prepared-but-undispatched in the report; the L1's own
construction runs supply the measurement evidence below. Round shape: v1,
wave 1 prepared (32 seats), 0 dispatched this seat, 0 dead. Landed gate
selftest: `PASS (275 cases, 0 skipped)`.

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 operability (lowest scored axis, 3/10): the canonical capture's grandchild and the verify-all section children run through ONE pinned absolute `bash` (default `/usr/bin/bash`, GNU-reporting; `RESEARCH_GATE_BASH` override, absolute + GNU-reporting, refused exit 2 `BASH_PROVENANCE` before any mode runs), so a caller PATH `bash` shim cannot interpose (echo re-add / suppress / hostile drift) | `ENV_PIN_CAPTURE_MATCH=7/8` on the pre-round gate `0447ad14…` (`.ufo/waves/round-39/controls/base-gate-r39.sh`, receipt `receipts/c1-base-s39001.json`, seed 39001; the eighth family fails live: `GATE_DRIFT: -GATE_GREP`, suppress kills the capture, relative override ignored) → `8/8` `predicate_holds=true` on the landed gate, seeds 39011/39111 (`receipts/c1-after-s39011.json`, `receipts/c1-after-s39111.json`), both `VERIFY: ok`; discrimination: the PATH-`env` mutant `e1251030…` scores `4/8` (seed 39013, `receipts/c1-mutenv-s39013.json`) | `python3 corpus/evidence/round39/c1-count.py --gate tools/research-gate.sh --seed N --receipt F` | **met** |
| C2 calibration: a round-39 receipt binds `verifier_sha256` (the digest of `round39/verify-receipts.py`) and, for c2-family receipts, `subject_counter_sha256`; the verifier re-derives both, refusing `verifier-sha256-mismatch` / `subject-counter-sha256-mismatch` / `subject-counter-unreadable` / `missing-field …` | before = the r38 pipeline: its receipts carry neither binding (committed bytes) and its verifier accepted five of six weakened-verifier mutants (r38 Erratum 11); under the r39 verifier the committed r38 receipt refuses `predicate-mismatch` and a stripped r39 receipt refuses `missing-field verifier_sha256` (both run live in the counter's legacy cell) → `RECEIPT_BINDING_MATCH=8/8` `predicate_holds=true` on the landed gate, seeds 39101/39121 (`receipts/c2-after-s39101.json`, `receipts/c2-after-s39121.json`), both `VERIFY: ok` with `verifier_sha256`/`subject_counter_sha256` equal to the committed file digests | `python3 corpus/evidence/round39/c2-count.py --gate tools/research-gate.sh --seed N --receipt F` | **met** |

The round-1 operability scale is unchanged: score 3 → 3 (delta 0); the C1/C2
observables sit beside it, as in rounds 25, 29, 31–38.

Separability: C1's predicate touches the gate bytes only; C2's predicate runs
the receipt pipeline against any gate bytes (gate-agnostic, the r38
Erratum-4 reading — the r39 c1 receipts bind and verify against the base and
mutant control gates). The discrimination controls isolate each direction
(base gate 7/8; env mutant 4/8; r38 receipts refuse under the r39 verifier).
No-harm on the landed bytes: selftest PASS 275 (L1, clean env); claims 17/17
CLEAN, chain 17/22 CLEAN, broken control 1/2 DRIFT, archives 3/3,
integrity-r7 composed CLEAN (L1 re-run with the pinned commands).

| axis | verdict | evidence (before → after) |
|---|---|---|
| operability | **improved** | C1: the capture's bash resolution is PATH-independent by measurement (7/8 → 8/8 across two seeds, two independent runners); selftest 272 → 275; the section-child call site (`verify_all_section`) is pinned as well as the capture grandchild. |
| calibration | **improved** | C2: receipts now bind which verifier and which subject bytes judged a run, re-derived with named refusals (r38 receipts and stripped bindings fail closed live); the first in-round self-catches of vacuous fixtures are frozen as QUALITY 56. |
| depth | **improved** | `corpus/knowledge/capture-bash-pin-r39.md` and `receipt-verifier-subject-r39.md`: mechanism, both delivery mechanisms, the kill record, the narrowed readings, the r40 cell list. |
| coverage | **unchanged** | no new measured verification surface; all seven modes and the fixtures held. |
| freshness | **improved narrowly** | S071 re-opened this round (quote re-located, sha match) and re-cited by C1's entry; the r38 lesson's stale wording/counts corrected (D3/D6). |
| adjacency | **unchanged** | zero network (strace class: all sources opened from installed man pages/info); the loader-env channel stays tsukuroi's, named as debt. |

Admission: **ADMIT** — both frozen predicates verify on every committed
receipt and no axis is harmed; the claims stand as first written (their
limits enumerate every demonstrated vector class; no errata needed). No
scalar score. Learning trends: expansion/quality **improved**, discernment
**improved** (three vacuous-fixture self-catches mined with fixes shown able
to fail; the routed-defect repairs D1–D6 landed). Routed-defect dispositions:
D1 → r38 claims Erratum 14; D2 → Erratum 15; D3 → count corrections in
LOG/SCORECARD/lesson; D4 → SCORECARD attribution note; D5 → SKILL.md r37 row
restored; D6 → r38 lesson correction block; D7 (the debt itself) → closed by
C2. Round 40 candidates: the `mktemp`/`sed` bare names in the capture path;
the loader scrub (`env -u LD_PRELOAD …`); the refusal-label re-derivation in
verify; the argv-witness dead fields; the metadata-screener locale seam; the
spans-≥32768 debt.

## Round 40 — closure corrections to r39 (R2–R5)

- R2: the committed `c1-mutenv-s39003.json` is a superseded draft, not an uncommitted file; r39's “six receipts” count omits it. See `corpus/evidence/round40/routed-defect-dispositions.json`.
- R3: the r39 report's knowledge count `29 → 31` is superseded by the historical `50 → 52` count re-derived in `corpus/evidence/round39/claims.md`.
- R4: not reproduced from the committed r39 spec, plan, and report: each reports reviewer 6 / revenger 2. The contrary 8/0 statement remains attributed to the spot-check; no source artifact is rewritten.
- R5: the r39 phrase “two independent runners” is superseded. The frozen claim design records two seeds as L1 construction runs; the prepared wave was not dispatched by this seat. Correct wording: **two seeds, both L1 construction runs**.

## Round 40 — measured claims (work commit `d164f88eb71a6c48a66ae1e7abfcb5fef82219d9`)

Freeze: `corpus/evidence/round40/claims.md` (commit `6c01a4144b3637cc57a989ab464f71b8ae69595a`). Both predicates were measured on the committed work tree below.

| Claim / axis | Axis score delta | Before → after | Counting command | Measured commit | Verdict |
|---|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; receipt evidence integrity) | 3/10 → 3/10; the legacy score counts only the three archive exports and was not redefined | active receipts 3/6 → 6/6 verify | `python3 corpus/evidence/round40/c1-count.py` | `d164f88eb71a6c48a66ae1e7abfcb5fef82219d9` | improved |
| C2 calibration (R2–R5 disposition alignment) | unscored → unscored; no numeric baseline is invented | evidence-backed dispositions 0/4 → 4/4; R4 is explicitly not reproduced | `python3 corpus/evidence/round40/c2-count.py` | `d164f88eb71a6c48a66ae1e7abfcb5fef82219d9` | improved |

No axis was harmed. Depth and coverage improved narrowly through the sourced receipt-digest note; freshness improved narrowly by re-opening S059 and updating its used-by path; adjacency is unchanged. No capability claim or scalar score is added.

Learning trends: **expansion improved** — one new knowledge entry records the previously unheld receipt-expectation-digest subground and cites reopened S059; **quality improved** — the active receipt set verifies against the committed expectations bytes and the source census exits 0; **discernment unchanged** — the round's admit/reject sample has no non-author spot-check yet.

## Planned — round 41 (not started)

Candidates carried from round 39: the capture path's bare `mktemp`/`sed` names, loader-environment scrubbing, refusal-label re-derivation, and the spans-≥32768 boundary. No round-41 work is started here; freeze only 1–3 separately falsifiable claims after scoring their do-nothing controls.


## Round 41 — measured claims (work commit `1bd9001330f19d89ec36592010d4218881ea5941`)

Freeze: `corpus/evidence/round41/claims.md` (freeze commit `b173b0943e647f7e3a365689df19debe40fd9dd2`). Both predicates measured on the committed work tree; L1 construction ran before the freeze commit (disclosed, same pattern as round 39).

| Claim / axis | Axis score delta | Before → after | Counting command | Measured commit | Verdict |
|---|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; canonical-capture invocation surface) | 3/10 → 3/10; the legacy score counts only the three archive exports and was not redefined | `CAPTURE_PIN_MATCH=1/12` → `12/12` (12-cell frozen scenario table: trap inventory, sed/mktemp/cat/rm/sort/mkdir shim cells, override refusals, child-tr, loader-env) | `python3 corpus/evidence/round41/c1-count.py --gate tools/research-gate.sh` (control: `--gate .ufo/waves/round-41/controls/base-gate-r41.sh`) | `1bd9001330f19d89ec36592010d4218881ea5941` | improved |
| C2 calibration (W04 duplicate-URL disposition alignment) | unscored → unscored; no numeric baseline invented | `W04_DISPOSITIONED=0/5` → `5/5` (S051/S053 same-page distinct-section, S073 required supersede, S074 retained rejected duplicate, S075 added this round on the coreutils page) | `python3 corpus/evidence/round41/c2-count.py` | `1bd9001330f19d89ec36592010d4218881ea5941` | improved |

No axis was harmed. Depth and coverage improved narrowly (sourced `capture-path-pin-r41.md`, the invocation-pinning subground); freshness improved narrowly (S075/S076 opened from installed copies; S067/S071/S072 re-cited); adjacency unchanged. No capability claim; the pinned-tool-table mechanism is gate infrastructure, not a repertoire-table entry. Selftest PASS 275/275 on the landed gate.

Learning trends: **expansion improved** — one new admitted knowledge entry on unheld subground citing mined S075/S076; **quality improved** — the capture's invocation surface now fails closed on caller-PATH and loader-env interposition with a do-nothing control at 1/12, and the selftest's only regression was repaired through the documented override; **discernment unchanged** — the admit/reject sample has no non-author spot-check yet (pending, as in round 40).

## Round 40 — routed wave findings (dispositions, append-only)

- R40-W1 (SentinelFetchScope F1/F2/F3): an egress-ordering seat item ran unapproved; the 2026-10-24 access claim had no committed receipt; the report's no-external-research line contradicted the gate record. Dispositioned in `corpus/lessons/round-41.md` (r41 spec hardened; QUALITY 57; fleet side integrator-owned).
- R40-W2 (ReviewActivePopulation/ReviewReplacementBindings/ReviewC2Bindings): r40 counter returns 6/6 on committed HEAD but 2/6 on a worktree carrying r41's in-flight gate edits — measurement-target defect in the counter lineage (QUALITY 58), routed to the counter's next owner; not a falsification of round 40.

## Planned — round 42 (not started)

Candidates carried: exported-function (`BASH_FUNC_*`) interposition into the captured child (named limit, needs a measured delivery cell); the `spans-≥32768` boundary debt; metadata-screener locale seam; argv-witness dead fields; REFUSAL-label re-derivation in verify; the legacy operability observable's retirement/split decision (r40 routed item). No round-42 work is started here; freeze only 1–3 separately falsifiable claims after scoring their do-nothing controls.

## Round 42 verdict — 2026-10-24 (wave-4 quarantine-first; work commit below)

Selected claims (frozen in `corpus/evidence/round42/claims.md` at
`dd63b6cfec5e1eafddb6662fc343e2ff6ab6aedc`): C1 = the lane's quarantine scope becomes a
runnable, re-derived surface (operability — the lowest scored non-retired axis, 3/10);
C2 = every row of the slice carries one rule-consistent verdict with a reason and a flip
condition (calibration). This round adopts NOTHING from the shokuknow package (fleet
lane-addendum item 10) and made no external fetch (fetch-scope L0 `8d77e6c1` open).

| claim / axis | before → after | counting command | verdict |
|---|---|---|---|
| C1 operability (lowest scored axis, 3/10) | the lane had no command that yields its quarantine scope: the slice (24 rows) was a line of a prompt, the examination did not exist. After: `SLICE_REDERIVE_MATCH=24/24`, `QUOTES_EXAMINED=43/43`, `REPRODUCIBLE=1/1`, `POSITIVE_CONTROL=1/1`, `NEGATIVE_CONTROL=1/1`, `MUTANT_DETECTED=1/1`, exit 0; the do-nothing control (tree without the tool) exits 1 | `python3 corpus/evidence/round42/c1-count.py` (control: `corpus/evidence/round42/controls/c1-control-before.txt`) | **improved** |
| C2 calibration | no adjudication existed for the slice. After: `VERDICTED=24/24`, `CLASS_CONSISTENT=24/24`, `REASON_NONEMPTY=24/24`, `FLIP_NONEMPTY=24/24`, `VOCAB_OK=24/24`, `DUPLICATE_ROWS=0`, `ROWS_OUTSIDE_SLICE=0`, exit 0; the do-nothing control (one row's verdict flipped away from the evidence) → `CLASS_CONSISTENT=23/24`, exit 1 | `python3 corpus/evidence/round42/c2-count.py` (control: `corpus/evidence/round42/controls/c2-control-before.txt`) | **improved** |

The round-1 operability scale is unchanged: score 3 → 3 (delta 0). Its counting command
still prints `VERDICT_BEARING_EXPORTS=3/3`, and `tools/research-gate.sh` is not touched
by this round. The C1/C2 observables sit beside that score, as in rounds 25, 29 and 31–41.

Adjudication: 24 rows — 15 `absent` (the quoted span is not in the capture that was
actually read), 9 `unverifiable` (1 bot-wall capture, 4 binary office documents never
rendered to text, 4 register rows naming no locator), 0 `present`, 0 `mixed`. No row is
called a fabrication on absent evidence; nothing is adopted.

| axis | verdict | evidence (before → after) |
|---|---|---|
| operability | **improved** (C1) | the slice and the examination are one committed command; three controls (positive, negative, mutant) hold; the do-nothing control fails |
| calibration | **improved** (C2) | 24/24 verdicts, each with a reason and a flip condition, graded by an independent re-examination; the flipped-row control fails at 23/24 |
| depth | **improved narrowly** | `corpus/lessons/round-42.md`: the frozen decision rule, the capture-form ground (S077), the two failure modes the `absent` class spans, four mined mistakes |
| coverage | **improved narrowly** | a new measured surface: the lane's quarantine scope (24 rows, 43 quotes) now has a command, a receipt and a per-row verdict — a surface the lane did not hold at all |
| freshness | **improved narrowly** | S077 opened this round from an installed copy (sha256 recorded); the register and every consulted capture are digested by `tools/quarantine-check.py digests` |
| adjacency | **unchanged** | nothing absorbed from a sibling lane; the campaign tree and every sibling repo stayed read-only; zero egress |

Learning trends, lane view (the outside closure is separate): **expansion improved**
(one opened source, one lesson, one runnable surface on ground the lane did not hold);
**quality improved** (both counters verified against do-nothing controls, and the
register's own class column was shown to be unreliable — the lane's rule now checks the
capture's FORM); **discernment unchanged** — the round's admit/reject sample still has
no non-author spot-check, so it is not claimed as externally verified.

## Planned — round 43 (not started)

Candidates, not commitments: split the `absent` class into "the source carries the text
and the row quotes it wrongly" and "the source does not carry the text" (the round-42
lesson names the split as a debt, and the measured longest-common-run evidence supports
it); the round-40 counter lineage's successor design (routed from r41's D1); a
per-capture provenance receipt (which capture, which form, which digest) so a later
round can re-check a row without re-deriving the cache; the `spans ≥ 32768` boundary
debt; the metadata-screener locale seam. No round-43 work is started here; freeze only
1–3 separately falsifiable claims after scoring their do-nothing controls.

## Round 43 verdict — 2026-10-24 (absent-class split; one local adoption)

Selected claims, frozen in `corpus/evidence/round43/claims.md` before any seat
scored: C1 operability (lowest scored non-retired axis, 3/10); C2 calibration;
C3 depth, sourced on S078. No external fetch. The planned block above is the
candidate list and is not rewritten.

| claim / axis | before → after | counting command | verdict |
|---|---|---|---|
| C1 operability | no command split the 15 `absent` rows. After: `ABSENT_ENUMERATED=15/15`, `CLASSED=15/15`, `BOTH_NONEMPTY=1/1` (9 misquote, 6 not-carried), `REPRODUCIBLE=1/1`, `MUTANT_DETECTED=1/1`, exit 0. Missing-tool control exits 1 | `python3 corpus/evidence/round43/c1-count.py` | **improved** |
| C2 calibration | the single `absent` label did not agree with a two-mode rule. After: `SPLIT_AGREES=15/15`. Flipping S086 scores 14/15 and exits 1 | `python3 corpus/evidence/round43/c2-count.py` | **improved** |
| C3 depth | the lane held no opened source for how a search log is kept. After: the entry cites S078, the quote is in the committed capture, the row URL matches | `python3 corpus/evidence/round43/c3-count.py` | **improved** |

The round-1 operability scale is unchanged: 3 → 3. These observables sit beside it.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** | C1: the split is one command; the missing-tool control fails |
| calibration | **improved** | C2: 15/15 labels match an independent recompute; the flipped row fails |
| depth | **improved** | C3 and `corpus/lessons/round-43.md`: the two failure modes, four mined mistakes, one re-grounded entry |
| coverage | **improved narrowly** | one new measured operation (the split) and one search-log fact the lane did not hold; the three-literatures entry was refused |
| freshness | **improved narrowly** | S078 opened from a committed capture, sha256 recorded; no fetch |
| adjacency | **unchanged** | nothing absorbed from a sibling; campaign tree read-only |

Learning trends, lane view: expansion improved (one opened row, one lesson, one new operation); quality improved (counters against do-nothing controls; QUALITY 61); discernment unchanged until a non-author spot-check.

## Round 44 verdict — 2026-10-24 (launcher receipt, inherited-tree disposition, one version-binding adoption)

Selected claims, frozen in `corpus/evidence/round44/claims.md` before any seat scored:
C1 operability (lowest scored non-retired axis, 3/10); C2 calibration; C3 depth, sourced on
S079. No external fetch: L0 `8d77e6c1` is still open, so every source opened this round was
opened from a committed capture and no URL was fetched.

| claim / axis | before → after | counting command | verdict |
|---|---|---|---|
| C1 operability | no committed launcher log existed, so the round-43 closure could not resolve the parent-lifetime claim. After: `N_SPAWNED=64/64`, `N_REAPED=64/64`, `PARENT_PID_MATCH=1/1`, `ZERO_PIDS=0`, `NAMES_MATCH=64/64`, exit 0. The missing-receipt, `controls/pids0.receipt` and `controls/prose.receipt` do-nothing controls each exit 1 | `python3 corpus/evidence/round44/c1-count.py` | **improved** |
| C2 calibration | the 39 inherited r40/r41 paths were unswept and unnamed. After: `CONSISTENT=39/39`, `REVERIFIED=36/36`, `LEFT_NAMED=3/3`, exit 0. The all-left table scores `REVERIFIED=0/36` and exits 1 | `python3 corpus/evidence/round44/c2-count.py` | **improved** |
| C3 depth | the lane held no opened source binding a citation to a prior state. After: the entry cites S079, the S079 row's URL is the RFC 7089 URL and the located quote is in that URL's committed capture | `python3 corpus/evidence/round44/c3-count.py` | **improved** |

The round-1 operability scale is unchanged: 3 → 3. These observables sit beside it.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** | C1: `tools/parent-lifetime.sh` writes the wait log from the same pid that spawned the children; `corpus/evidence/round44/parent-lifetime.receipt` (`start parent_pid=3226659` … `end parent_pid=3226659 n_spawned=64 n_reaped=64`); the three do-nothing controls fail. The wave-3 receipt `.ufo/waves/round-44/w3/parent-lifetime.receipt` carries the same end line for a wave whose seats ran: `n_spawned=32 n_reaped=32` |
| calibration | **improved** | C2: 36 inherited seat reports re-verified one by one (basename stem, round token, length > 80, sha256) and committed as historical wave evidence; the 3 modified JSON paths stay left-named, uncommitted, reason `not hunk-verified`. Wave-3 mutation seats killed both counters with single-field corruptions (`ZERO_PIDS=1`, `PARENT_PID_MATCH=0/1`, `REVERIFIED=35/36`, `LEFT_NAMED=2/3`) |
| depth | **improved** | C3 and `corpus/lessons/round-44.md`: two entries and three mined rows on one theme, the version binding of a citation to a prior state |
| coverage | **improved narrowly** | one theme the lane did not hold: RFC 7089's Memento promise, the NDL WARP capture cadence and the NDL timestamped-URL anchor |
| freshness | **unchanged** | every capture opened this round was written before this round's launch (`2026-10-24T21:36:37-03:00`): RFC capture mtime 2026-10-23 20:33, WARP 20:36, E2867 20:37 -0300. The round-43 closure routed exactly this inflation; it is not counted as an improvement here and the axis is not harmed |
| adjacency | **unchanged** | the campaign tree was read only and never written; no sibling lane was absorbed; the two new entries are the lane's own re-grounding of staged package material |

Learning trends, lane view: expansion improved (three new mined rows, two new knowledge
entries, one lesson, one new gate); quality improved (three counters against do-nothing
controls, QUALITY 62 mined from `considerthese/2026-10-24.md`, QUALITY 63 from the wave-3
launcher probe, and the wave-3 mutation probes); discernment unchanged until a non-author
spot-check — a seat this lane dispatched is still the lane.

## Round 45 verdict — 2026-10-25 (launcher exit contract, Gates registry, AVeriTeC archive-field adoption)

Selected claims, frozen in `corpus/evidence/round45/claims.md` at
`d82cec904bf0fb8736886b9f17be913c7807427a` before any seat scored: C1 operability (lowest
scored non-retired axis, 3/10); C2 calibration; C3 depth, sourced on S082–S084 opened this
round. Work landed at `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`; measured over a
`git archive` of that commit (`corpus/evidence/round45/measure-after-5e8c7ad2.txt`). No
external fetch: L0 `8d77e6c1` is still open. Tag column per QUALITY 64.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability | the round-44 launcher scores `CASES_MATCH=1/5`, exit 1 (exits 0 on zero tasks and on timed-out seats, silent 420 s default, no `timeout_s`). After: `CASES_MATCH=5/5`, exit 0; four mutants of the landed tool each score 4/5 (wave-2 `MutLauncherPatched`) | `python3 corpus/evidence/round45/c1-count.py` | **improved** | plumbing |
| C2 calibration | the Gates table named 25 of 51 committed entry points at the base tree (`UNREGISTERED=26`; 29 at the freeze tree). After: `REGISTERED=54/54`, `UNREGISTERED=0`, exit 0; eleven of the twelve new rows are load-bearing under single-row removal; the twelfth (`tag-count`) names a check outside the frozen entry-point pattern (wave-2 `MutC2RowRemoval`) | `python3 corpus/evidence/round45/c2-count.py --list` | **improved** | plumbing |
| C3 depth | the lane held no opened source on what a verification corpus's archive fields record (AVeriTeC was an unopened lead). After: `ENTRIES=2/2 CITES_BOUND=3/3 QUOTES_IN_SPAN=4/4 QUOTES_IN_ENTRY=4/4 COUNTS_IN_ENTRY=7/7 CAPTURE_BOUND=4/4 COUNTS_REDERIVED=7/7`, exit 0; `--lane-only` passes with no campaign cache | `python3 corpus/evidence/round45/c3-count.py` (and `--lane-only`) | **improved** | ground |

The round-1 operability scale is unchanged: 3 → 3. These observables sit beside it.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** | C1; the post-wave errexit guard (`controls/c1-errexit-probe.txt`: first landing exit 124 with a truncated receipt, fix exit 3 complete) |
| calibration | **improved** | C2: the lane's own gate registry now agrees with the committed tree; wave-2 row reviews corrected the round-40 and round-31 rows. Limit: path membership, not row truth |
| depth | **improved** | C3 and `corpus/lessons/round-45.md`: two re-grounded entries whose substance moved beyond the staged text (claim archive "no link stored, not why"; 5,959 of 7,572 real-source answers archived; 1,582 sourced answers with no archive key) |
| coverage | **improved narrowly** | one theme on ground the coverage map did not hold (wave-2 `CritCoverageGround`); coverage map +2 rows |
| freshness | **unchanged** | every capture opened predates the launch (2026-10-25T06:19:59−03:00); not counted as an improvement |
| adjacency | **unchanged** | no sibling holds AVeriTeC ground (wave-1 `ConnectSiblings`); campaign tree read only |

Learning trends, lane view: expansion improved (three mined rows, two entries, QUALITY 64–65,
one QUALITY check); quality improved (three counters against do-nothing controls; two
post-landing fixes each shown able to fail; nine mined mistakes); discernment unchanged until a
non-author spot-check — wave-2 seats are still the lane.

## Planned — round 46 (not started)

Candidates, not commitments: the staged AVeriTeC dataset-page amendment as a fresh
document-bound entry (wave-2 `CritRejectDecision` located its quotes; flip in
`lessons/round-45.md` `## Gate`); a C3-style counter that checks an entry's inference
sentences, not only quote and count presence (wave-2 `CritC3Axis`); a gate-registry check
that also covers executable verifiers outside the frozen name pattern (wave-2
`CritC2Framing`). Freeze only 1–3 separately falsifiable claims after scoring their do-nothing
controls.

## Round 46 verdict — 2026-10-25 (inference grounding, verifier registry, evidence-pool adoption)

Claims frozen in `corpus/evidence/round46/claims.md` at
`c2f0e9d100c0d46633a6277b2fd51d2ac99678eb` before any seat scored; work landed at
`d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`. After-measurement:
`corpus/evidence/round46/measure-after.txt`. No external fetch: L0 `8d77e6c1`
is still open and every capture read is on disk. Tag column per QUALITY 64.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10): inference grounding becomes an executable check — `tools/inference-ground.py` refuses an Inference bullet that cites no source and every quoted phrase or figure in one that its cited spans do not carry | `TOOL=absent POSITIVE_PASS=0/3 JUNK_KILLED=0/3` exit 1 (`controls/c1-before.txt`, base tree `6e2630a6`) → `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS` exit 0; controls: always-exit-0 tool `JUNK_KILLED=0/3`, citation-presence-only `1/3`; fixtures byte-pinned in the counter, so a changed fixture reads `FIXTURES_CHANGED=` and fails; a CANARY leg copies the first positive and first junk fixture under neutral names, so a tool that keys on the fixture NAME fails (`CANARY=fail`) | `python3 corpus/evidence/round46/c1-count.py` | **improved** (frozen predicate met). Framing narrowed: the check proves citation and token PRESENCE, not that the inference follows — the round-45 D7 class still passes (`CritC1Attack`, `CritC1D7`); reported, not hidden | plumbing |
| C2 calibration: the gate registry covers the executable verifiers the lane's verdicts name outside the frozen name pattern | under the literal frozen set: freeze-equivalent trees A–C `ENTRY_POINTS=79 (tools=7 counters=50 named=74/77) REGISTERED=58/79 UNREGISTERED=21` exit 1; pristine base tree D `ENTRY_POINTS=76 (7/47/74) REGISTERED=58/76 UNREGISTERED=18` exit 1 (in `controls/c2-before.txt`) → `REGISTERED=81/81 UNREGISTERED=0 C2=PASS` exit 0 at the round close under the literal frozen set (all 79 existing named paths, including the eight `.ufo/waves/` controls — five newly registered by the `round35–41 gate controls` row; the original 72-path enumeration measured `73/73` at the landing, before `CritC2Scope` brought the literal set); forges refused: prose paste, six-cell row, eight-pipe row without `exit`, row after the next `## `, fenced row, `.pyc`-suffix row | `python3 corpus/evidence/round46/c2-count.py --list` | **improved**; limit named: the set samples on MENTION (a path named in a verdict), not on DEPENDENCE, so a gate named only in QUALITY/SKILL (`round45/tag-count.py`) stays outside while two historical probes that disclaim gating come in (`CritC2Framing`, `RevC2TagCount`) | plumbing |
| C3 depth: the evidence-pool theme adopted as two lane entries, five rows S085–S089, eleven capture-bound spans | `ENTRIES=0/2 CITES_BOUND=0/5 QUOTE_ROWS=0/11` exit 1 (`controls/c3-before.txt`) → both modes `ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS` exit 0 (`--lane-only`: `CAPTURE_BOUND=skipped`); control: a forged manifest with invented capture digests passes `--lane-only` and is refused by the default mode at `CAPTURE_BOUND=0/11` | `python3 corpus/evidence/round46/c3-count.py` (and `--lane-only`) | **improved**; the counter measures presence and provenance, not entailment (three inferences were narrowed this round by `CritC3Inference`; anchors are not counter-checked — `ReviewerC3Spans` caught a 13-char anchor slip, fixed) | ground |

The round-1 operability scale is unchanged: 3 → 3. These observables sit beside it.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** | C1: a new runnable check plus its counter and six declared fixtures; the wave-1 survivor (a junk bullet parked in a fence) was fixed and the fixture set is now byte-pinned |
| calibration | **improved** | C2: `UNREGISTERED=0` over a set that grew from 68 to 72 entry points; the counter's own cheap gates (fence, comment, suffix) closed after `MutC2Forge`; the registry now names 13 historical instruments with their real verdict maps, including two that say they do not gate |
| depth | **improved** | C3 and `corpus/lessons/round-46.md`: two entries re-grounded on five newly opened sources, eleven located quotes with context, staged misreadings corrected (field-pairing is practice not invariant; the hedge tracks a missing original URL; the temporal rule belongs to the successor corpus; the staged "limited …" and "We used …" are not verbatim) |
| coverage | **improved narrowly** | two entries on ground the map did not hold (`ScoutCoverageGround`); coverage map +2 rows; no sibling holds this ground (`ConnectSiblings`) |
| freshness | **unchanged** | every capture opened predates the launch (2026-10-25T07:10:05−03:00: captures written 2026-10-23/24); S085's recheck cadence is set `365d` where the staged row said `180d` — a curation choice logged to the lesson, not an improvement |
| adjacency | **unchanged** | no sibling lane holds FEVER/AVeriTeC ground; six lanes already practise capture-digest binding row-by-row, so the entries state a fleet habit rather than discover one (`ConnectSiblings`) |

## Capabilities (round-46 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| inference-grounding check | refuses an `#### Inference` bullet that cites no source, and every quoted phrase or figure in one that its cited spans (or its cited document's designator) do not carry — presence, not entailment | `tools/inference-ground.py`; `corpus/evidence/round46/c1-count.py`; `corpus/fixtures/inference-ground-r46/` | 46 |
| verifier registry alongside the name pattern | enumerates the lane's executables from three legs (tools/, the round-45 counter pattern, and every `*.py`/`*.sh` its verdicts name) and requires each inside a `## Gates` row, refusing fence, comment and suffix forges | `corpus/evidence/round46/c2-count.py` | 46 |
| capture-bound span builder with context | rebuilds `spans.tsv` and the span files as exact capture slices carrying ±80 chars of context, and re-derives them with `--check` | `corpus/evidence/round46/build-spans.py` | 46 |

## Planned — round 47 (not started)

Candidates, not commitments: an ENTAILMENT leg for the inference check — the D7
class still passes (`CritC1Attack`, `CritC1D7`), and the cheapest next move is a
controlled-vocabulary relation per bullet (supports/narrows/contradicts) checked
against the cited span's own polarity words, with the critic's six survivors as
the before-controls; a DEPENDENCE-based C2 set (`RevC2TagCount`: a gate named
only in QUALITY/SKILL is invisible) that adds `round45/tag-count.py`,
`round32/q33-check.py`, `round30/rerun-check.py` and `round29/prose-check.py`
with an `entry paths ⊆ ENTRY_POINTS` assertion; and the amendment's own warrant
for the archiving practice (`S089` char 14603) as a committed span. Freeze 1–3
claims after scoring their do-nothing controls.

## Round 47 verdict — 2026-10-25 (polarity probe, dependence registry, claim-support adoption)

Claims frozen in `corpus/evidence/round47/claims.md` at
`22a44b8b5c923d25123a96a852c11938559bb9b2` before any seat scored. Landed: C1
`a15610a5` + `980fe43f`, C2 `7fb9a232`, C3 `3d2a0637`; the after-measurement is
`corpus/evidence/round47/measure-after.txt`. No external fetch: L0 `8d77e6c1` is still
open. Tag column per QUALITY 64.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10): the inference check refuses a windowed stem-sharing polarity flip (`INF_POLARITY_FLIP`) | `POSITIVE_PASS=3/3 JUNK_KILLED=0/3 CANARY=fail R46_COUNTER=pass R46_ENTRIES=2/2 C1=FAIL` exit 1 (`controls/c1-before.txt`) → `3/3 3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS` exit 0; controls: round-46 tool `JUNK_KILLED=0/3`, always-exit-1 `POSITIVE_PASS=0/3`, negator-word refuser `POSITIVE_PASS=1/3` | `python3 corpus/evidence/round47/c1-count.py` | **verifies** (frozen predicate met). NOT entailment: on wave-2 held-out sets written after the wave-1 fix, the probe killed 4 of 12 natural flips (`HeldOutB`; the round-46 tool kills 0) and refused 2 of 12 correctly-reasoned bullets (`HeldOutA`; the round-46 tool refuses 0); on the lane's 63 real entries it changes no exit (`SweepC1Corpus`, 378 runs, after the wave-2 leaf-key fix). Two wave-2 critics rule the axis a trade (`CritC1Claim`, `CritScorecard`); see the axis row | plumbing |
| C2 calibration: the gate registry agrees with the tree its checks depend on | freeze tree `MISMATCHES=25` (freeze counter) / `21` (final counter), bare base `22` / `18` (`controls/c2-before.txt`) → `ENTRY_POINTS=94 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS` exit 0 (FLOOR=92 met), and the freeze-time counter `93/93 MISMATCHES=0` too; control: the round-46 counter prints `C2=PASS` on the base tree while this counter fails it | `python3 corpus/evidence/round47/c2-count.py --list` | **improved narrowly**: of the 25, 8 were real self-assessment mismatches (7 executables named by QUALITY/SKILL or run by an entry point in no row, 1 row whose unescaped pipes lost its exit map), plus 3 control rows naming no exit code; 10 were the freeze counter's own escaped-pipe split (`CritC2Framing`). Row truth stays a reader's check | plumbing |
| C3 depth: the claim-support test adopted by document — two entries, S090–S094, S085 re-bound, 35 capture-bound spans | `ENTRIES=0/2 CITES_BOUND=0/6 ANCHOR_BOUND=0/6 QUARANTINE_VERDICTS=0/4 C3=FAIL` exit 1 (`controls/c3-before.txt`) → both modes `ENTRIES=2/2 CITES_BOUND=6/6 QUOTE_ROWS=35 SPAN_IDS=6/6 QUOTES_IN_SPAN=35/35 QUOTES_IN_ENTRY=35/35 SPAN_CONTEXT=35/35 CAPTURE_BOUND=35/35 REF_ID_UNBOUND=0 ANCHOR_BOUND=6/6 INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=4/4 QUARANTINE_ABSENT_ADOPTED=0 C3=PASS` exit 0 (`--lane-only`: `CAPTURE_BOUND=skipped`); controls: the staged entries copied unchanged fail `REF_ID_UNBOUND=17 CITES_BOUND=0/6`, invented digests fail `CAPTURE_BOUND=0/12` | `python3 corpus/evidence/round47/c3-count.py` (and `--lane-only`) | **improved** | ground |

The round-1 operability scale is unchanged: 3 → 3. These observables sit beside it.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved, disputed as a trade** | C1: the D7 body of round 46 (`CritC1D7` v7) now exits 1 and 4/12 held-out flips are refused that nothing refused before; the cost is 2/12 held-out correct bullets refused, against zero exit changes on the lane's 63 entries. Wave-2 `CritC1Claim` and `CritScorecard` rule this a trade (axis harm); the L1 reads the synthetic false refusals as a strictness cost with no observed harm to the lane's corpus. Reported for the operator to rule, not resolved here |
| calibration | **improved narrowly** | C2: 8 real registry mismatches closed against an enforced floor; the counter's own parser defects were found by the wave and repaired toward the literal sentence |
| depth | **improved** | C3 and `corpus/lessons/round-47.md`: two entries re-grounded on six captures, nine mined mistakes, eight staged misreadings corrected |
| coverage | **improved narrowly** | the support DEFINITION, the annotator decision rule and per-step reliability figures were ground the coverage map did not hold (`ScoutCoverageGround`); the four-state frame and FEVER's 0.6841 were already held and earn nothing |
| freshness | **unchanged** | every capture opened predates the launch (2026-10-25T08:25:52−03:00; captures written 2026-10-23) |
| adjacency | **unchanged** | no sibling holds this ground (`ConnectSiblings`); PEOPLEPROFILES' model-agreement figure is left to kengaku |

## Capabilities (round-47 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| polarity probe in the inference check | refuses an Inference bullet whose own words reverse a quoted phrase's negation within fixed windows, or re-denominate a counts figure against its leaf key — a windowed stem-sharing negator mismatch, not entailment; the figure leg fires only where an entry is checked with a counts manifest (the lane's entries are checked with `--counts /dev/null`) | `tools/inference-ground.py` (`INF_POLARITY_FLIP`); `corpus/evidence/round47/c1-count.py`; `corpus/fixtures/inference-ground-r47/` | 47 |
| dependence-and-check registry count | counts gate-registry mismatches over the round-46 set plus paths gates run and paths QUALITY/SKILL name as checks, by entry cell and exit-code verdict map, with dangling rows and an enforced floor | `corpus/evidence/round47/c2-count.py` | 47 |
| anchor-bound span manifest | builds capture-bound spans from a quote list and generates Registry anchor cells whose every `char N` is a located quote offset | `corpus/evidence/round47/build-spans.py`; `corpus/evidence/round47/c3-count.py` `ANCHOR_BOUND` | 47 |

## Planned — round 48 (not started)

The following candidates were the pre-freeze plan snapshot; superseded by the measured Round-48 disposition below.

Candidates, not commitments: repair or supersede the four round-39/40 receipts that fail
`gate-sha256-mismatch` since round 41 (QUALITY 68's first run; routed in round 41, never
closed); a held-out precision fixture set for the polarity probe (correct bullets with the
negator outside the window, conflicting-polarity spans) so its false-refusal rate is a
counted leg; a second assimilation theme from `merge/chousa/` whose captures are byte-faithful.
Freeze 1–3 claims after scoring their do-nothing controls.

## Round 48 verdict — 2026-10-25 (held-out polarity precision and refinement coverage)

R48-C1 was frozen at lane commit `4bbd2348578bb6288c0700dabf37cea04225bfb6` before wave-2 scoring. The tool/counter change landed at `671b096e2bd5d5b0994bcd7ab8c17abaf16c62c7`; final measurements over its archive are in `corpus/evidence/round48/measure-after.txt`. No external fetch; L0 `8d77e6c1` remains open.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10): the tool and composite counter reduce false refusals on the fixed R47 regression set and cover the five R47 surviving refinements | current R47 tool control `CORRECT_BULLETS_PASS=9/12`, `PRECISION_GATE=FAIL`, C1 exit 1 → candidate `12/12` (minimum 11), `REFINEMENT_CASES=5/5`, `LEGACY_R47=PASS`, `C1=PASS`; separate mutation probe `MUTANTS_KILLED=5/5`; name-keyed no-read control passes c1-count alone but fails the composite mutation-check leg when installed at the default tool path | `python3 corpus/evidence/round48/c1-count.py`; `python3 corpus/evidence/round48/mutation-check.py`; `python3 corpus/evidence/round48/controls/name-key-control.py` | **improved narrowly** on the recycled R47 regression; W2 `AttackPrecision.md` disputes the a05 label (the prior R47 non-author verdict called it a false refusal); re-open a05 in closure before generalizing the result | plumbing |

The numeric operability scale remains 3/10 (its round-1 observable counts three archived inputs, not these new tests). No other expertise score is invented. The round-47 C2 row `SCORECARD.md:2506` was already corrected: `94/94` final, freeze-time counter `93/93`; `92` is the frozen floor, not an after-state ratio. Re-running `python3 corpus/evidence/round47/c2-count.py --list` after the R48 Gate entries yields `REGISTERED=97/97`, `MISMATCHES=0`, C2=PASS.

The carried R39/R40 receipt mismatch is expected historical revision drift, not corrupted receipts: the round-40 counter at the R48 tool commit reports 2/6 at the current gate (four `gate-sha256-mismatch` refusals after round-41 `1bd9001`), while all six verify at their own adding commits (three at `d164f88`, three at `6d914e9`). Receipt bytes remain untouched; reissuing them would rewrite historical measurement bindings. The phrase “QUALITY 68's first run” in the planned-R48 note refers to an R47 criterion, not a round-41 event; round 41 is the cause of the later gate drift.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved narrowly** | R48-C1 after-state and its no-read composite control; see limitations above |
| calibration | **unchanged** | the R47 SCORECARD correction reproduces, and the current C2 registry is 97/97; no new numeric self-assessment claim is made |
| depth | **unchanged** | no new domain knowledge entry was admitted; docstring changes document this lexical tool's limits |
| coverage | **unchanged** | no province frontier moved into core |
| freshness | **unchanged** | no live or changing external source was opened |
| adjacency | **unchanged** | `PROVINCE.md` remains scoped to chousa method; `.ufo/waves/round-48/w2/SiblingFit.md` found no sibling ownership overlap |

Trends: expansion **unchanged** (no new knowledge entry on uncovered ground); quality **unchanged** (no corpus knowledge entry was re-admitted or failed a re-check; the measured tool work is C1 operability); discernment **unchanged** pending the required independent closure spot-check of `corpus/lessons/round-48.md` Gate decisions. Seats dispatched by this lane are not counted as non-authors.

## Round 49 verdict — 2026-10-25 (section-10 adopter; derived-index theme adopted by document)

Claims frozen in `corpus/evidence/round49/claims.md` at `fe740e7838b338d17fec9338c909557e6e7fed7d` after scoring do-nothing controls. Tool `65940928`→fixes `4ce61fc5`; adoption `1254ab26` and W2 narrowing (this round's final commit). After-measurement: `corpus/evidence/round49/measure-after.txt`. Post-freeze span-builder change and W2 narrowing disclosed in `corpus/evidence/round49/claims-erratum.md`. No fetch; L0 `8d77e6c1` open.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; capability) | `TOOL=absent C1=FAIL` exit 1; copy control `SETS_PASS=0/3`, GUARD/PIPE FAIL → `SETS_PASS=3/3`, GUARD PASS, PIPE PASS, `C1=PASS` exit 0 | `python3 corpus/evidence/round49/c1-count.py` | **improved narrowly**: conformance on fixed inputs; a replay of the tool's outputs also passes (W1 `CritForgeC1`); W2 perturbed-package and held-row probes passed (supplementary) | plumbing |
| C2 depth (sourced) | `ENTRIES=0/2 BOUND=0/9 C2=FAIL` exit 1; staged-copy control `REF_ID_UNBOUND=11 C2=FAIL` → `BOUND=8/9 REFUSED=1 QUOTE_ROWS=31 CAPTURE_BOUND=31/31 ANCHOR_BOUND=8/8 INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=5/5 C2=PASS` exit 0 | `python3 corpus/evidence/round49/c2-count.py` | **improved**, subject to the closure's ruling on the disclosed post-freeze `build-spans.py` change (W2 `CritErratum`: C2 stands) | ground |

The numeric operability scale remains 3/10; no other score is invented.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved narrowly** | C1; `tools/assimilate-rows.py` |
| depth | **improved** | C2; two entries on eight re-opened captures, 31 located quotes, narrowed after W2 |
| calibration | **improved narrowly** | a05 propagations corrected (`a05-check.py` 1→0); QUALITY 69 note, 72; registry `REGISTERED=104/104` |
| coverage | **improved narrowly** | index derivation, link lag, resolution ladder and CNKI counter rules were not held (W1 `CritTheme`); the aggregator-is-not-the-source conclusion was held and earns nothing |
| freshness | **unchanged** | newest readable capture 2026-10-24 23:26 -03; this round's captures 2026-10-23 (QUALITY 71) |
| adjacency | **unchanged** | W1 `ConnSiblings`: no sibling overlap |

## Capabilities (round-49 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| section-10 package adopter | turns staged campaign entries into census-valid lane rows and rewritten entries: by-document renumbering with one simultaneous substitution, held-row detection by census URL normalisation, normalised status/opened/recheck/used-by with the stripped text logged, 0–3-space collision lists | `tools/assimilate-rows.py`; `corpus/evidence/round49/c1-count.py` | 49 |

## Planned — round 50 (not started)

Candidates: add a perturbed-input leg to the adopter counter (QUALITY 72); adopt the next same-theme package entry (`cnki-citation-check-r40.md`) with an NCPSSD help-page row; fold `quote-substance-check.py` into the next span counter before freezing.

## Round 50 verdict — 2026-10-25 (adopter self-test; Chinese citation-checking theme adopted by document)

Claims frozen in `corpus/evidence/round50/claims.md` at `6a068f2ae4847a1e4aa959f088a39ddc1b167bc0` after scoring their do-nothing controls. After-measurement: `corpus/evidence/round50/measure-after.txt`. Disclosures: `corpus/evidence/round50/claims-erratum.md`. No fetch; L0 `8d77e6c1` open.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; capability extension) | base tool `BASELINE=FAIL rc=2`, `LEGS=2/5`, `C1=FAIL`; echo control `LEGS=4/5`, `PERTURB_PASS=0/6`; constant control `LEGS=2/5` → `LEGS=5/5`, `PERTURB_PASS=6/6`, `C1=PASS` | `python3 corpus/evidence/round50/c1-count.py` | **improved narrowly**: the frozen counter is replayable (W2 `R50CritForgeC1`: a forge prints the six literal DIFF lines and passes `LEGS=5/5`); the supplementary `c1-supplement.py` (nonce leg, exclusive DIFF set, hardening probes) passes the real tool 5/5 and fails the forge 1/5 | plumbing |
| C2 depth (sourced) | `ENTRIES=0/3 BOUND=0/4 NEW_GROUND=0/3 C2=FAIL`; staged copy `REF_ID_UNBOUND=15` → `BOUND=3/4 REFUSED=1 NEW_GROUND=3/3 QUOTE_ROWS=67 CAPTURE_BOUND=67/67 SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=3/3 C2=PASS` | `python3 corpus/evidence/round50/c2-count.py` | **improved**, as a presence-and-binding result: the counter cannot see entailment (W2 `R50CritForgeC2`), the CJK polarity rule is unreachable (named limit), and expansion credit is per document (three documents), not per entry | ground |

The numeric operability scale stays 3/10; no other score is invented.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved narrowly** | C1; `tools/assimilate-rows.py --selftest`; the replay weakness is named |
| depth | **improved** | C2; three entries narrowed by 30+ W2 corrections, a rendered-page observation the text form drops |
| calibration | **improved narrowly** | stale counts corrected and checked (`stale-count-check.py` exit 1 → 0); the lesson's mistakes are mined with checks shown able to fail; the report-before-WAVE-DONE defect is not repeated |
| coverage | **improved narrowly** | the 引文核对 feature, its manuals' scope and a Chinese institute's citation service were not held at base (`git grep` at `3c51da77` finds none in `corpus/knowledge`) |
| freshness | **unchanged** | newest readable capture 2026-10-24 23:26 -03; this round's captures 2026-10-23 |
| adjacency | **unchanged** | W2 `R50ConnSiblings`: no sibling overlap |

## Capabilities (round-50 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| adopter self-test | runs the section-10 adopter on an isolated hand-expected fixture package, compares findings as a multiset, prints the fixtures digest and exits 0/1/2; scored on perturbed copies against echo and constant controls | `python3 tools/assimilate-rows.py --selftest`; `corpus/evidence/round50/c1-count.py`; `c1-supplement.py` | 50 |

## Planned — round 51 (not started)

Candidates: make the adopter cite only `source:` ids (QUALITY 77) and fix its three latent input defects (identity before pipe rewrite, plain-split registry pipe, next id without a `## Registry` heading — W2 `R50ExecPerturbAdopter`); fold `c1-supplement.py`'s nonce leg into a successor counter; give `inference-ground` a CJK polarity check; adopt `cnki-public-surface-r43.md` with a re-grounded S160 and a capture of the sibling portal; read the two screenshots' text by a located-quote method instead of a rendered-page note.

## Round 51 pointer corrections (append-only; no row above is edited)

Each line names the row's line number, the bare pointer it prints and the committed non-empty file it meant (W1 `R51ExecC3Pointers`: receipt labels and add-commits). `python3 corpus/evidence/round51/c3-count.py` reads them.

correction: SCORECARD.md:1843 measure/final/ -> .ufo/waves/round-32/measure/final/
correction: SCORECARD.md:2073 measure-l1/c1-s36361.json -> .ufo/waves/round-36/measure-l1/c1-s36361.json
correction: SCORECARD.md:2074 measure-l1/c2-s36371.json -> .ufo/waves/round-36/measure-l1/c2-s36371.json
correction: SCORECARD.md:2616 c1-supplement.py -> corpus/evidence/round50/c1-supplement.py

## Round 51 verdict — 2026-10-25 (adopter v3 and nonce counter; Japanese/Chinese search-record theme; pointer calibration)

Claims frozen in `corpus/evidence/round51/claims.md` at `d603f6f00f78d64f123d3aed2dd9f8701547a4ba` after scoring their controls; errata `claims-erratum.md` E1–E5. After-measurement: `corpus/evidence/round51/measure-after.txt`. No fetch; L0 `8d77e6c1` open.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; capability extension) | lane tool at base `LEGS=1/5 C1=FAIL`; controls base 1/5, echo 2/5, const 1/5, flag-noop 2/5 → `LEGS=5/5 C1=PASS`; supplement `SUPPLEMENT_LEGS=10/10` | `python3 corpus/evidence/round51/c1-count.py`; `python3 corpus/evidence/round51/c1-supplement.py` | **improved narrowly**: the frozen counter is forgeable (a 94-line tool keyed on its directory names passes 5/5; the supplement fails it 1/10), the supplement is post-freeze and forgeable by a tool that reimplements the adopter, and the round-49/50 one-shot counters fail at the new default | plumbing |
| C2 depth (sourced) | `ENTRIES=0/3 BOUND=0/7 C2=FAIL` → `BOUND=6/7 REFUSED=1 QUOTE_ROWS=70 CAPTURE_BOUND=70/70 ANCHOR_BOUND=6/6 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=6/6 C2=PASS` | `python3 corpus/evidence/round51/c2-count.py` | **improved** as presence and binding; entailment is uncounted (W2 found 30+ prose overstatements, narrowed); one document refused for capture form | ground |
| C3 calibration | `CAP_ROWS=36 POINTERS=74 DANGLING=5 C3=FAIL` (first run 8, erratum E1) → `DANGLING=0 C3=PASS` | `python3 corpus/evidence/round51/c3-count.py` | **improved narrowly**: pointer existence, not truth (a correction to any non-empty file passes); the before-count changed once after the freeze | plumbing |

The numeric operability scale stays 3/10; no other score is invented.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved narrowly** | C1; `tools/assimilate-rows.py` v3; the supplement |
| depth | **improved** | C2; three entries on six documents |
| calibration | **improved narrowly** | C3; mistakes row 9 (W2 corrections to the round's own prose) |
| coverage | **improved narrowly** | `git grep -l -e 検索式 -e 検索期間 -e 检索策略` at `9ec1751a` finds nothing in `corpus/knowledge`; six documents now |
| freshness | **unchanged** | newest readable capture 2026-10-24; no fetch |
| adjacency | **unchanged** | W1 `R51ConnSiblings` and W2 `R51W2ConnSiblingsFinal`: no sibling overlap |

## Capabilities (round-51 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| source-only adoption and receipt check | adopts staged entries citing only header `source:` ids, per entry, with refusals for malformed registries and unknown source ids, and checks that a receipt names the tool revision it measured | `python3 tools/assimilate-rows.py --selftest`; `corpus/evidence/round51/c1-supplement.py`; `corpus/evidence/round51/receipt-check.py` | 51 |

## Planned — round 52 (not started)

Candidates: a zip-member form for the refused `.docx` (a counter and span builder that read `word/document.xml`), then bind it; the other search-record entries decided in the round-51 Gate (`search-tracking-record-r40`, `japanese-prisma-item-wording-r40`, `chinese-search-log-r37-amendment`); close the adopter's named limits (twin-id `held` label, refusal ordering); an enforcing form of the supplement that a reimplementing tool cannot pass.

## Round 52 verdict — 2026-10-26 (OOXML capture text form; search-record theme continued by document)

Claims frozen in `corpus/evidence/round52/claims.md` at `37468eadd8d098e80289b2f31a22de3872d4a1f6` after scoring their do-nothing controls; post-freeze disclosures `corpus/evidence/round52/claims-erratum.md` E1–E4. After-measurement: `corpus/evidence/round52/measure-after.txt` (header `tool-rev:`). No fetch; L0 `8d77e6c1` open.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; capability acquisition) | `tools/capture-text.py` absent at base: `LEGS=0/9 C1=FAIL`; controls naive 4/9, cache-txt 0/9, const 0/9 → `LEGS=9/9 C1=PASS` (three unseeded runs and `--seed 7`); supplement `SUPPLEMENT_LEGS=4/4` | `python3 corpus/evidence/round52/c1-count.py`; `python3 corpus/evidence/round52/c1-supplement.py` | **improved narrowly**: the frozen counter is forgeable by XML spelling (`controls/forge-shape.py` 9/9, W1 `R52CritForgeC1`); the post-freeze supplement refuses that forge (0/4) but W2 `R52W2CritForgeSupplement` passed both with a 54-line regex tool and a memoised NIPH text; the tool gained refusal classes after the candidate that no frozen leg measures (erratum E2) | plumbing |
| C2 depth (sourced) | `ENTRIES=0/3 BOUND=0/4 C2=FAIL`; staged-copy control `REF_ID_UNBOUND=31` → `BOUND=4/4 REFUSED=0 QUOTE_ROWS=39 CAPTURE_BOUND=39/39 ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=1/1 C2=PASS` | `python3 corpus/evidence/round52/c2-count.py` | **improved**, as presence and binding: entailment is uncounted (W2 narrowed bullets in all three entries, erratum E5), the CJK polarity check is inert on these entries (W2 `R52W2ExecInfRegression`), and expansion credit is three documents, not four (S113 a second carrier) | ground |

The numeric operability scale stays 3/10; no other score is invented.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved narrowly** | C1; `tools/capture-text.py` on the cache's eight zip captures (two `.docx` rendered, six refused) |
| depth | **improved** | C2; three entries on four documents, 39 located quotes |
| coverage | improved narrowly | three documents on ground the base did not hold (`git grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f5 -- corpus/knowledge` → exit 1); the 梅斯医学 record (S113) is a second carrier, no credit |
| calibration | improved narrowly | the round-51 S120 offset re-located (`char 39411` → 8996 in a named form); QUALITY 87–90; `verdict-gap.py` makes two lane-vs-verifier gaps visible (`VERDICT_GAPS=2 UNPARSED=1`) |
| freshness | unchanged | newest readable capture 2026-10-24; no fetch |
| adjacency | unchanged | W1 `R52ConnSiblings`, W2 `R52W2ConnSiblingsFinal`: no sibling overlap |

## Capabilities (round-52 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| OOXML capture text form | prints the text form of a `.docx` capture (main part from `_rels/.rels`; no Fallback, deleted text, field codes or tab stops), locates a quote's offset in it, and refuses non-zip, relationship-less, non-Word, encrypted and inflated packages | `python3 tools/capture-text.py <raw> --locate '<quote>'`; `corpus/evidence/round52/c1-count.py`; `corpus/evidence/round52/c1-supplement.py` | 52 |

## Planned — round 53 (not started)

Candidates: the adopter twin-id `held` label and refusal-order patch (W1 `R52ExecAdopterTwin`, routed defect 2) with its self-test rows; the anchored `correction:` check (W1 `R52ExecPointerAnchor`, routed defect 4) as a calibration claim; `search-tracking-record-r40.md` with its quote re-cut at char 935; the two verdict gaps `verdict-gap.py` prints (round 47 operability, round 50 calibration) and round 48's unparsed verifier form.

## Round 53 pointer corrections (append-only; no row above is edited)

Anchored successors of the round-51 corrections (round-52 closure section 6 item 4; `python3 corpus/evidence/round53/pointer-anchor-check.py` requires each anchor, ≥12 characters, to occur exactly once in the target) and the stale erratum ranges (closure section 6 item 1; W1 `R53DraftCorrections`, `R53DraftMistakes`).

correction: SCORECARD.md:1843 measure/final/ -> .ufo/waves/round-32/measure/final/ anchor: "seed": 32101,"
correction: SCORECARD.md:2073 measure-l1/c1-s36361.json -> .ufo/waves/round-36/measure-l1/c1-s36361.json anchor: "ENGINE_SWAP_CANARY=14/14"
correction: SCORECARD.md:2074 measure-l1/c2-s36371.json -> .ufo/waves/round-36/measure-l1/c2-s36371.json anchor: "WITNESS_PER_RECORD=5/5"
correction: SCORECARD.md:2616 c1-supplement.py -> corpus/evidence/round50/c1-supplement.py anchor: "SUPPLEMENT_LEGS={n}/{len(res)}"
correction: SCORECARD.md:2664 E1–E4 -> corpus/evidence/round52/claims-erratum.md anchor: "E6 — named, not changed: the frozen span builder's reader is unbounded"
correction: corpus/lessons/round-52.md:153 E1–E4 -> corpus/evidence/round52/claims-erratum.md anchor: "E6 — named, not changed: the frozen span builder's reader is unbounded"
correction: SKILL.md:133 E1-E4 -> corpus/evidence/round51/claims-erratum.md anchor: "E5 — controls and supplements changed after the freeze"

The round-52 erratum range is E1–E6 (E5 in-round narrowing, E6 the unbounded span-builder reader); the round-51 erratum range is E1–E5.

## Round 53 verdict — 2026-10-26 (adopter v4; search-record instruments)

Claims frozen at `a6ff732c70011f11c9beb681d832cedc6e75f566` after do-nothing controls (`corpus/evidence/round53/claims.md`; C1 `controls/c1-before.txt`, C2 `controls/c2-before.txt` / `c2-controls.txt`). Candidate C1 `32aab5edd70e43145cae72ec872278f3bc6efba7`; W1 integration `f4343163b70ce20e6b6d4f52b39935156e8afb26`. No live fetch; L0 `8d77e6c1` open.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; capability extension) | base adopter `LEGS=1/8 C1=FAIL` (REGRESS only); controls base 1/8, const 0/8, refuse 0/8, relabel-only 5/8, all-twin 2/8 → candidate `LEGS=8/8 C1=PASS` (three unseeded and `--seed 7`; W1 `R53ExecSeedRuns` also 45/45 required runs plus 140 seeds). Post-freeze supplement: candidate 3/3, W1 forge-c1 1/3 | `python3 corpus/evidence/round53/c1-count.py`; post-freeze `python3 corpus/evidence/round53/c1-supplement.py` | **improved narrowly**: W1 `R53CritForgeC1` demonstrated a 189-line forge still passes the frozen counter 8/8 by canning REAL, shape-keying date checks and stubbing the R50 self-test strings; supplement kills two of those three shortcuts, but not the valid-map implementation. E2 `--per-leg 0` and E3 cadence mismatch remain named | plumbing |
| C2 depth (sourced; search-record instruments) | `ENTRIES=0/3 BOUND=0/5 C2=FAIL`; staged-copy control `REF_ID_UNBOUND=12 BOUND=0/5`; adopter-rewrite control `BOUND=5/5 REF_ID_UNBOUND=4 ANCHOR_BOUND=0/5 C2=FAIL` → `ENTRIES=3/3 BOUND=4/5 REFUSED=1 QUOTE_ROWS=63 CAPTURE_BOUND=63/63 ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=0/0 C2=PASS` | `python3 corpus/evidence/round53/c2-count.py` | **improved**, as presence, binding and located support; the C2 counter does not judge entailment. The C1 twin was S118 (one row cited by two entries); S190 refused. Expansion credit per document, not entry | ground |

The numeric operability scale remains 3/10; the round-1 score is its narrow archived-export observable, not this adopter counter. No other numeric score is invented.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved narrowly** | C1; candidate v4 fixes the same-run `held` label (S195 is `twin`) and refusal ordering; the frozen counter remains forgeable on REAL, RECHECK edge shapes and R50 self-test attestation |
| depth | **improved** | C2; three entries, four bound documents, 63 quote spans and four anchors; W1 critics narrowed the JMLA line-break, the cross-tradition title and the issued-guideline wording |
| coverage | **improved narrowly** | four unique documents absent at base (S117–S120); S118's S185/S195 staged twins count once; S119 is the release notice, S120 the Cochrane chapter |
| calibration | **improved narrowly** | pointer-anchor check `ANCHORED=7/7`; the round-52 erratum ranges corrected by anchored successors; W1 C1 forge and counter blind spots named rather than hidden; no non-author spot-check yet |
| freshness | **unchanged** | no fetch; newest capture dates remain 2026-10-24 |
| adjacency | **unchanged** | W1 `R53ConnSiblings` reports no sibling ownership of the landed search-record method or adopter; drug-regulator mandates remain report-only |

## Capabilities (round-53 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| section-10 adopter v4 twin and refusal handling | labels `held` only for a URL already in Registry and `twin` for a same-run duplicate; separate counts; validates cited rechecks before output; refuses broken Registry before entry refusals, including without `--entry` | `python3 tools/assimilate-rows.py --selftest` (`FIXTURES_SHA256=9822ad59544cd42d6c6a8c3d34cb14d4d7c98d21e4f388d604486d70dd5db4a6`, findings 40/40); `corpus/evidence/round53/c1-count.py`; supplement (post-freeze only) | 53 |

## Planned — round 54 (not started)

Candidates: a C1 counter with a non-vacuous sample-size guard, generic calendar-invalid inputs and a non-canned held-out REAL leg; resolve the E3 predicate/tool recheck grammar; a defined OLE `.doc` text form or a narrower refusal; continue theme C (GB/T 7714 source-type) or theme B (archived-translation currency) after re-checking their capture state and province fit. C1's streak count (RW-1) is exposure, not failure; pair it with the next C1 verdict.

## Round 54 pointer corrections (append-only; no row above is edited)

The S100 and S101 Registry anchors (round 49) are offsets in a whole-file UTF-16LE decode of the `.doc` capture, a form no lane command prints (263 U+FFFD, 243 `0x0B`, a binary preamble; `corpus/lessons/round-54.md` `## Mistakes` row 2). Re-pointed into the defined OLE text form, dumped by the round-54 tool to the two targets (`python3 tools/capture-text.py <raw>`; S101 sha256 `a8e3e7ad…`, S100 `70ca0f0d…`); `python3 corpus/evidence/round53/pointer-anchor-check.py` requires each anchor to occur exactly once in its target. The two rows' form label "(UTF-16LE text of the raw .doc capture)" is superseded by these lines: their text form is now `tools/capture-text.py` (round 54). W1 `R54DraftS101Reanchor`, `R54DraftMistakes`.

correction: corpus/SOURCES.md:110 char1296->char16 -> corpus/evidence/round54/S100-text-form.txt anchor: "中国知网他引频次的查询需要使用《中国引文数据库》。"
correction: corpus/SOURCES.md:110 char1431->char151 -> corpus/evidence/round54/S100-text-form.txt anchor: "对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引"
correction: corpus/SOURCES.md:110 char2843->char492 -> corpus/evidence/round54/S100-text-form.txt anchor: "“文献来源”等方式进行组合查询，注：被引频次为0的文献将不会显示"
correction: corpus/SOURCES.md:111 char11170->char11972 -> corpus/evidence/round54/S101-text-form.txt anchor: "为便于文献的统计和期刊评价"
correction: corpus/SOURCES.md:111 char11205->char12007 -> corpus/evidence/round54/S101-text-form.txt anchor: "每一篇文章或资料应根据其内容性质标识一个文献标志码"
correction: corpus/SOURCES.md:111 char11993->char12795 -> corpus/evidence/round54/S101-text-form.txt anchor: "本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。"
correction: corpus/SOURCES.md:111 char12161->char12963 -> corpus/evidence/round54/S101-text-form.txt anchor: "文献类型及载体类型标志；"
correction: corpus/SOURCES.md:111 char13247->char14049 -> corpus/evidence/round54/S101-text-form.txt anchor: "参照ISO 690及ISO 690-2，每一参考文献条目的末尾均以“.”结束。"
correction: corpus/SOURCES.md:111 char34374->char25123 -> corpus/evidence/round54/S101-text-form.txt anchor: "参考文献格式，参照ISO 690"

## Round 54 verdict — 2026-10-26 (OLE `.doc` text form; the PRC citation standard by document)

Claims frozen at `5a1a20630d8176a816a60bb43b0d0e7ee2db19a0` after do-nothing controls (`corpus/evidence/round54/claims.md`; `controls/c1-before.txt`, `c1-controls.txt`, `c2-before.txt`, `c2-controls.txt`). Candidate C1 `8a7d0f137a352000d78704ba5695ded8857104fe`; post-candidate tool changes disclosed in `corpus/evidence/round54/claims-erratum.md` E2. After-measurement: `corpus/evidence/round54/measure-after.txt` (header `tool-rev:` with the tool sha256). No live fetch; L0 `8d77e6c1` open.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; capability acquisition) | base tool refuses every OLE file as `not a zip`: `LEGS=1/6 C1=FAIL` (REGRESS only) on three unseeded runs and `--seed 7`; controls CONST 0/6, NAIVE 0/6, REFUSEALL 1/6, SHELL 1/6 → `LEGS=6/6 C1=PASS` on three unseeded runs and `--seed 7`. Post-freeze supplement (E1): landed tool `SUPPLEMENT_LEGS=3/3` ×4; rebuilt forge and all four controls 0/3 | `python3 corpus/evidence/round54/c1-count.py`; post-freeze `python3 corpus/evidence/round54/c1-supplement.py` | **improved narrowly**: W1 `R54CritForgeC1` passed the frozen counter 6/6 with a tool that reads the generated HTML left beside each document and cans REAL by digest (rebuilt: `controls/build-c1-forge.py`, `controls/c1-forge.txt`); W1 `R54CritOracle` and `R54MutOle` showed REAL accepts capped junk and 7 of 16 mutants survive the frozen counter; the supplement closes the three forge shortcuts, but it is not the frozen rule | plumbing |
| C2 depth (sourced; the PRC citation standard GB/T 7714-2025) | `ENTRIES=0/2 BOUND=0/3 SUBSTANCE=FAIL QUARANTINE_VERDICTS=0/3 C2=FAIL`; staged-copy control `REF_ID_UNBOUND=6 HELD_BAD=1`; adopter-rewrite control `BOUND=3/3 REF_ID_UNBOUND=3 HELD_BAD=1 ANCHOR_BOUND=0/3 C2=FAIL` → `ENTRIES=2/2 BOUND=3/3 REFUSED=0 REF_ID_UNBOUND=0 NEW_GROUND=2/2 QUOTE_ROWS=33 CAPTURE_BOUND=33/33 ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=3/3 C2=PASS` | `python3 corpus/evidence/round54/c2-count.py` | **improved**, as presence, binding and located support; entailment is uncounted (W1 `R54CritForgeC2`: boilerplate quotes and an opposite inference also pass). The W1 S101 leg was cut (E3); expansion credit is three documents | ground |

The numeric operability scale remains 3/10; the round-1 score is its narrow archived-export observable, not this text-form counter. No other numeric score is invented.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved narrowly** | C1; the OLE text form reads the five pinned captures and LibreOffice-generated documents, refuses non-Word OLE, encrypted and malformed files; post-candidate fixes: the signed Prc bound (W1 `R54ReviewOleTool` F1, `R54ExecOleFuzz` 37/600 Tracebacks at the candidate) and tracked-deletion runs dropped (W1 `R54ReviewOleSpec`; `tracked-deletion-check.py` candidate FAIL, landed PASS) |
| depth | **improved** | C2; two entries on three documents, 33 located quotes, three anchors; the staged headlines narrowed (the portal notice is about the portal's service; the type enumeration cut; the 7.3 quote re-cut at its line break) |
| coverage | **improved narrowly** | three documents absent at base (`git grep -l -e 'ISO 690:2021' -e 文献载体标识 c49ffc6c -- corpus/knowledge` → exit 1); a new capture form (OLE `.doc`) read; the HIT data specification's carrier alphabet stays open |
| calibration | **improved narrowly** | nine anchored `correction:` lines re-point S100/S101 from an undefined UTF-16LE decode into the defined form (`pointer-anchor-check.py` → `ANCHORED=16/16`); QUALITY 97–100; the round-53 W2 handoff recorded as not dispatched; the frozen counter's forgeability named, not hidden |
| freshness | **unchanged** | no fetch; newest capture dates remain 2026-10-24 |
| adjacency | **unchanged** | W1 `R54ReviewProvince`: no sibling PROVINCE claims citation standards or document-format parsing; `kengaku-shokunin/PROVINCE.md:137` hands the method here |

## Capabilities (round-54 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| OLE Word 97+ `.doc` text form | prints the main-story text form of an OLE `.doc` with no helper program (CFB chains, FIB, Clx piece table, cp1252/UTF-16LE pieces, field results only, tracked deletions dropped) and locates a quote's offset in it; refuses `ole-not-word`, `ole-encrypted`, `ole-malformed` | `python3 tools/capture-text.py <raw> [--locate Q]`; `corpus/evidence/round54/measure-after.txt` (frozen counter 6/6 ×4, supplement 3/3 ×4, tracked-deletion PASS) | 54 |

## Planned — round 55 (not started)

Candidates: a span builder that reads an OLE `.doc` through `tools/capture-text.py`, then the HIT data specification's carrier alphabet beside the standard's (the cut S101 leg, W1 `R54DraftEntryStb`); the refused S130 grey-literature entry, now that its form blocker is gone (W1 `R54ExecS130Probe`); a frozen C1-style counter whose generated inputs never sit beside the tool's input and whose REAL leg cannot be canned by digest (RW-1, sixth round); the counter limits W1 named (REAL ratio and label rule, fObfuscated-only and nFib branches ungenerated).

## Round 55 statement errata

Eleven lane statements committed at `dba605de` that round-54 wave 2 falsified (closure `corpus/lessons/round-54-verifier-spotcheck.md` section 6 items 2, 4, 5, 6; W2 reports under `.ufo/waves/round-54/w2/`). Each line anchors the statement exactly once in its target (the statement stays, append-only) and records the observation as re-derived this round; `python3 corpus/evidence/round55/c3-count.py` recomputes every observation from BASE bytes, the pinned captures and its own probes (claim R55-C3). The in-target corrections are named in `corpus/lessons/round-55.md` `## Corrections`.

erratum: E01 corpus/knowledge/source-type-taxonomy-r36.md anchor: "the stronger claim that the text is unavailable belongs to no line here" observed: "该标准暂无全文，请等待更新 count=1 char=1712"
erratum: E02 corpus/knowledge/source-type-taxonomy-r36.md anchor: "continues that 主管部门为 国家标准委 (char 575)" observed: "主管部门为 国家标准委 char=569"
erratum: E03 corpus/knowledge/source-type-taxonomy-r36.md anchor: "a row scoped to the document-type taxonomy the standard prescribes cannot" observed: "附录 S121=0 S122=0; 文献类型 S121=0 S122=0"
erratum: E04 corpus/knowledge/source-type-taxonomy-r36.md anchor: "count 1 each, on one line" observed: "国家标准委 S121=2 S122=2"
erratum: E05 corpus/QUALITY.md anchor: "11,972 / 12,007 / 12,963 / 12,795 / 14,049 / 25,123" observed: "located=11972,12007,12795,12963,14049,25123 drift=+802,+802,+802,+802,+802,-9251"
erratum: E06 corpus/QUALITY.md anchor: "263 U+FFFD and 18,242 control characters" observed: "C0=18451 C0_excl_tab_lf=18431 C0_excl_tab_lf_cr=18242"
erratum: E07 corpus/QUALITY.md anchor: "gives 27,012 characters, 0 U+FFFD, 0 control characters" observed: "form_C0=469 form_LF=469"
erratum: E08 corpus/lessons/round-54.md anchor: "on a mirror without the two dumps `pointer-anchor-check.py` prints `BAD=6`" observed: "ANCHORED=7/16 UNANCHORED=9 BAD=9"
erratum: E09 corpus/QUALITY.md anchor: "and refuses a tool that delegates to that reader" observed: "ctypes_system_under_hook rc=0 marker=SPAWNED"
erratum: E10 corpus/QUALITY.md anchor: "and the SHELL control's receipt says the same" observed: "SHELL LEGS=1/6"
erratum: E11 corpus/evidence/round54/c1-supplement.py anchor: "randomly named directory outside the generation tree (no HTML, no" observed: "oracle-echo SUPPLEMENT_LEGS=3/3"

Readings: E01 — the string sits in the page's embedded i18n map (`noFullText`), a latent template string, not a displayed line; I3's sentence holds only for displayed lines. E02 — 575 is the offset of the value 国家标准委, the quoted phrase starts at 569. E03 — neither capture shows a taxonomy, so "prescribes" is the standard's own text as carried by S123, not by these two pages. E04 — the count-1 property holds for the eleven anchor quotes, not for every quoted token. E05 — positions 3 and 4 are swapped; five of six anchors drift by the constant +802, so "no constant repairs an old anchor" is false (no constant repairs all six). E06/E07 — the counts hold only under the exclusion sets named; the defined form's only control character is LF. E08 — `BAD=6` reproduces only with S101's dump alone missing. E09 — a ctypes `system()` spawns under the round-54 hook, so QUALITY 98's "refuses a tool that delegates" holds only for audited spawn events. E10 — the SHELL control scored 1/6 (it keys refusals on bytes), the criterion's forge 0/6. E11 — the supplement's oracle files and the ISOLATED leg's generation HTML sit two directories above the isolated document, so an echo tool that never opens the `.doc` scores 3/3.
