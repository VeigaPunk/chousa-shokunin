# ExecNoHarmPin

## Verdict
Harm on the prescribed gate observables. Axes: operability (gate verdicts) and freshness (match to round-36 pins); every run deviated from the pinned expected result.

## Evidence
Working directory for all commands: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Commands were executed as prescribed; each displayed `EXIT_CODE` was captured immediately after the gate process.

| Run | Command input / mode | Observed tally line(s) | Exit | Round-36 pin | Result |
|---|---|---|---:|---|---|
| Claims fixture | `verify-claims corpus/fixtures/claims-r2.jsonl --root .` | `VERDICT_BEARING_CLAIMS=0/17`; `RESEARCH_GATE: DRIFT (claims=17 supported=0 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=17 invalid=0 findings=17 drift=17)` | 1 | 17/17 | Harm: 0/17 |
| Chain fixture | `verify-chain corpus/fixtures/chain-r3.md --root .` | `RESOLVED_HOPS=0/22`; `RESEARCH_GATE: DRIFT (hops=22 verified=0 exempt=5 anchor-missing=0 refused=17 invalid=0 findings=17 drift=17 resolvable=0)` | 1 | 17/22 | Harm: 0/22 |
| Broken chain control | `verify-chain corpus/fixtures/chain-r3-broken.md --root .` | `RESOLVED_HOPS=0/2`; `RESEARCH_GATE: DRIFT (hops=2 verified=0 exempt=0 anchor-missing=0 refused=2 invalid=0 findings=2 drift=2 resolvable=0)` | 1 | 1/2 | Harm: 0/2 |
| Archive A | `verify ../research/deep-research-2026-09-28/A-*.md --root ..` | `RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)` | 1 | archives 3/3 aggregate | Harm: per-input verify DRIFT, not a clean archive run |
| Archive B | `verify ../research/deep-research-2026-09-28/B-*.md --root ..` | `RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)` | 1 | archives 3/3 aggregate | Harm: per-input verify DRIFT, not a clean archive run |
| Archive C | `verify ../research/deep-research-2026-09-28/C-*.md --root ..` | `RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)` | 1 | archives 3/3 aggregate | Harm: per-input verify DRIFT, not a clean archive run |

Exact gate commands used (with absolute gate path):

```sh
bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root .
# VERDICT_BEARING_CLAIMS=0/17
# RESEARCH_GATE: DRIFT (claims=17 supported=0 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=17 invalid=0 findings=17 drift=17)
# EXIT_CODE=1
bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root .
# RESOLVED_HOPS=0/22
# RESEARCH_GATE: DRIFT (hops=22 verified=0 exempt=5 anchor-missing=0 refused=17 invalid=0 findings=17 drift=17 resolvable=0)
# EXIT_CODE=1
bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root .
# RESOLVED_HOPS=0/2
# RESEARCH_GATE: DRIFT (hops=2 verified=0 exempt=0 anchor-missing=0 refused=2 invalid=0 findings=2 drift=2 resolvable=0)
# EXIT_CODE=1
bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify ../research/deep-research-2026-09-28/A-*.md --root ..
# RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)
# EXIT_CODE=1
bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify ../research/deep-research-2026-09-28/B-*.md --root ..
# RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)
# EXIT_CODE=1
bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify ../research/deep-research-2026-09-28/C-*.md --root ..
# RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)
# EXIT_CODE=1
```

## Findings
1. Claims are all refused (`0/17` vs `17/17`); output includes 17 `CLAIM_SOURCE_OUT_OF_CORPUS` findings, resolving each source as `./research/deep-research-2026-09-28/...` outside allowed roots. Grounding: observed claims command output; `SCORECARD.md:2058-2061` pins claims 17/17.
2. Valid chain has 17 source refusals and only five exempt hops (`0/22` vs `17/22`). Grounding: observed chain output has 17 `CHAIN_SOURCE_OUT_OF_CORPUS` findings; `SCORECARD.md:2058-2061` pins chain 17/22.
3. Broken control has both hops refused (`0/2` vs 1/2), rather than the pinned partial resolution. Grounding: observed broken-control output has two `CHAIN_SOURCE_OUT_OF_CORPUS` findings; `SCORECARD.md:2060` pins 1/2.
4. Each archived-input `verify` emitted six findings (five drift) and exit 1. The round-36 scorecard states the aggregate archive observable as 3/3, but these three prescribed per-input runs did not return clean verdicts or a 3/3 tally. Grounding: A/B/C observed `RESEARCH_GATE` outputs; `SCORECARD.md:2060`.

## Limits
No files changed except this report; no tools installed. No counter commands or seeded experiments were part of this six-run check.