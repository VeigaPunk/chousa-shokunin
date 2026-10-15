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
