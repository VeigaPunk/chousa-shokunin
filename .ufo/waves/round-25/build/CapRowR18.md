# Round 18 capability row backfill

Axes: **freshness** (record the missing capability row) and **calibration** (limit it to demonstrated behavior).

## Evidence

- `LOG.md:683` claims: “**Verdicts** (SCORECARD §Round 18): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1.”
- `SCORECARD.md:923-930` names the round-18 addition: “`SCOPE_KENGAKU` gains `llm benchmark|llm benchmarks|llm scoring`” and “Cases 117–119 pin the new phrases (llm-benchmarks refusal, llm-scoring refusal, prose-only control CLEAN).” The verdict at `SCORECARD.md:935` says the gap closes from CLEAN to `SCOPE_MODEL_QUALITY_ABSORBED` warn + DRIFT. The note is `corpus/knowledge/scope-phrase-gap-r18.md` (`SCORECARD.md:937`).
- `SCORECARD.md:1278-1279` records that the capability acquisitions claimed for rounds 15 and 17–23 still lack rows, including round 18.

## Demonstration rerun

Private clone base observed: `b820e4e40ce52deedf53b191140cd7b08ddda929`.

Command: `bash tools/research-gate.sh --selftest` in `/tmp/chousa-r25-CapRowR18`.

Observed: exit 0; `RESEARCH_GATE_SELFTEST: PASS (136 cases, 0 skipped)`. Round-18 case lines:

```text
ok-case  117 scope-fail-llm-benchmarks    exit=1
ok-case  118 scope-fail-llm-scoring       exit=1
ok-case  119 scope-pass-benchmark-prose   exit=0
```

The current base has later cases too; the round-18 pair and prose control pass unchanged in this rerun.

## Proposed SCORECARD row

```text
| LLM benchmark-phrase scope screening | flags declared LLM benchmark/scoring model-quality scope with `SCOPE_MODEL_QUALITY_ABSORBED` warn + DRIFT; prose-only control remains CLEAN | selftest cases 117–119; `corpus/knowledge/scope-phrase-gap-r18.md` | 18 |
```

Demonstration succeeded and the capability is identifiable; this row is evidence-backed, not pre-claimed. No files in the private clone were edited. No tools installed or updated.
Installs/updates: none.
VERDICT: Demonstrated; recommend adding the round-18 capability row above.
