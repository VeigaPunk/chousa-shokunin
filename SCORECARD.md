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

The lane's saturation line and stagnation window N are to be declared by the lane on its next round per `AXES.md` §The stagnation nudge; not asserted by this conformance change.

## Planned — round 12 (pre-registered 2026-10-19, goal turn 1)

Wave: one 64-seat AgentSwarm call, opencode-go key 1 / deepseek-v4.1-flash (curriculum loop 1, round 1; opencode-go keys rotate between rounds). Seat roster is logged in the round-12 report. Before-receipts (2026-10-19): selftest `PASS (85 cases)` exit 0; `--drift` vs the r8 baseline `GATE_DRIFT: none` exit 0; r1 counting command `VERDICT_BEARING_EXPORTS=3/3`; `grep -c SCOPE_ tools/research-gate.sh` → 0; `VERSION=research-gate-r1` at `tools/research-gate.sh:227`; A-r9.md C3 cites `A-shokunin-tradition.md:76`, span verified at `:86`.

1. **coverage — scope-refusal teeth** (the r1 landing requirement, open since 2026-10-15): the structure check gains a DECLARED-scope screen — only a record's `## Meta` `domain:`/`scope:` row triggers it (prose is never keyword-scanned, so the B archive on multi-agent knowledge cannot trip it); a refused declaration (bounty-program scope → kasegi; model-quality claims → kengaku; orchestration/dispatch → kumitate) emits its named finding — `SCOPE_BOUNTY_ABSORBED` / `SCOPE_MODEL_QUALITY_ABSORBED` / `SCOPE_ORCHESTRATION_ABSORBED` — at warn severity, which drifts (exit 1). One symmetric selftest fixture per province asserting exit 1 + one clean/absent control. Observable: `SCOPE_` emitting sites 0 → 3; selftest 85 → 85+N (N≥4, settled at landing); scope-less records byte-identical (canary: archives-r9 A/B/C + r6/r7 fixtures re-run unchanged).
2. **operability — r2-carried residuals**: (a) `VERSION=research-gate-r1` corrected to a mode-agnostic version string with a selftest case pinning the banner; (b) claim/chain source reads gain a size cap (8 MiB default; oversized source → named refusal `SOURCE_READ_TOO_LARGE`, refused never partially read) with just-under/over boundary fixtures. Observable: selftest grows by the landed case count; every prior case byte-identical (cmp against `corpus/evidence/pin-r8-20261016T033757Z-selftest.log`); `--drift` vs the r8 baseline stays `none` or a re-pin lands with a recorded reason.
3. **calibration — close the r11 open finding**: A-r9.md row C3 citation `:76` → `:86` (span re-verified at `:86` 2026-10-19); `hardening-r10.md` ledger row dispositioned closed; append-only errata to `audit-r11.md` and the ledger naming the superseded text. Observable: the ledger's one open finding → 0 open; verify-all on A-r9 CLEAN at the corrected bytes; no other A/B/C-r9 row carries the same cite-vs-span mismatch (mechanically swept).

Conformance (not an axis claim): §Saturation below declares the line + window the 2026-10-16 rollout deferred to this round.
