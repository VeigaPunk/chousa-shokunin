# chousa — Scorecard

## Axes

| Axis | Score (0–10) | Evidence | Last-change round |
|---|---:|---|---:|
| operability | 0 | Baseline `34774a1777d4058ca8c2b4456ce2e6ccee9e24c5`: the A/B/C archived exports each exit 1 with zero stdout bytes and zero verdict lines; `LOG.md` round-1 operability entry | 1 |

This missing-at-baseline scorecard starts with the one measured axis, operability
(AXES.md's runnable-artifact axis). No expertise scores are invented for the
other five axes. Score = the number of the three named archived inputs that
exit 1 **and** emit exactly one `RESEARCH_GATE: DRIFT` summary, one point each;
this deliberately narrow observable can award at most 3/10, not field readiness.

## Planned

One move: make informational findings non-fatal so the real `verify` CLI emits
its declared verdict for all three local archived exports. Preserve strict-mode
drift, finding IDs, secrecy, approval boundaries, and setup exit 2. Exercise the
real CLI from the hermetic selftest; record the resulting counts and revision.

Baseline inputs, read-only under the fleet root:
`research/deep-research-2026-09-28/A-shokunin-tradition.md`,
`B-multiagent-knowledge.md`, and `C-rank-taxonomy.md`.

Counting command (run from this lane; no fetch):

```bash
python3 -c 'import subprocess; names=("A-shokunin-tradition.md","B-multiagent-knowledge.md","C-rank-taxonomy.md"); rows=[subprocess.run(["bash","tools/research-gate.sh","verify","../research/deep-research-2026-09-28/"+n,"--root",".."],capture_output=True,text=True) for n in names]; print("VERDICT_BEARING_EXPORTS=%d/3" % sum(r.returncode==1 and sum(s.startswith("RESEARCH_GATE: DRIFT (") for s in r.stdout.splitlines())==1 for r in rows))'
```

## Retired

None. The unmeasured axes are not retired or asserted saturated.
