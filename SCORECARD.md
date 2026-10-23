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
| C2 operability (lowest scored axis): `verify-claims` verifies spans of 32765..32767 bytes (the PCRE dead zone: the 4N-byte pattern fits argv but PCRE2 refuses it, "regular expression is too large", S065) | `DEADZONE_MATCH=21/37` (unfixed gate `772a1d8e`, seeds 5011/5023, `measure-a2/c2-before-s*.json`) → `37/37` on seeds 5011, 5023, 5033, 5047 on gate `a6307edf…` (`measure-a2/c2-after-s*.json`); no committed run below 37 | `LC_ALL=C python3 corpus/evidence/round34/c2-count.py --seed N --receipt F` | **verified (measured)** — do-nothing 21/37, two fresh-seed receipts at 37/37, no-harm battery 11 rows PASS (`measure-a2/battery/`), selftest cases 254–256 (PASS 256) |
| C3 calibration: self-assessment text vs observed repo state, counted | no committed count existed (E4/E5 were point repairs) → first counted run prints `SELF_AUDIT_MISMATCHES=0` / `SELF_AUDIT_UNDISPOSITIONED=0` over 43 checks, reproduced by re-run (`measure-a2/audit-first-run.txt`); negative control: 2 injected lies → 2 counted, disposition key verified | `python3 corpus/evidence/round34/self-audit.py` | **verified (measured)** — the count is the claim; every counted mismatch carries a committed disposition; the do-nothing control (no audit) cannot produce the receipt |

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
