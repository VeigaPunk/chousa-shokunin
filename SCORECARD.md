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

