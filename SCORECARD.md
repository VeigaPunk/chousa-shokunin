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
