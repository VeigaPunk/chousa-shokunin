# Scope phrase gap (round 18)

source: tools/research-gate.sh (SCOPE_KENGAKU :694; scope_decl_screen :669-695; scope_norm :696-701; scope_hit :703-708); receipts: corpus/evidence/scope-r18-20261019T173000Z-{demo,selftest,battery,drift}.log; round-16 named debt closed
verified-at: 2026-10-19 (round 18, landed; selftest PASS (119 cases, 0 skipped); gate sha 6e694881…)
recheck: `bash tools/research-gate.sh --selftest` (cases 117–119 pin the new phrases); the demo record in `evidence/scope-r18-…-demo.log`

## The gap

`SCOPE_KENGAKU` covers `model benchmark(s)` and `model scoring` but not
`llm benchmark(s)` or `llm scoring` — a record declaring `domain: LLM
benchmarks` passed CLEAN despite the model-quality boundary. `scope_hit`
matches literal phrases after `scope_norm` lowercases and folds punctuation;
it never stems, so `llm benchmarks` needs its own entry — `model benchmarks`
does not cover it.

## The fix (minimal, conservative)

`SCOPE_KENGAKU` gains `llm benchmark|llm benchmarks|llm scoring` — three
phrases, not five. The wave's adversary seats confirmed `ai benchmark(s)` is
too broad: "AI benchmark methodology research" can be about benchmark methods
without declaring model-quality scope. `ai benchmark(s)` stays named debt
for a future round that can prove the boundary.

## The audit's other findings (dispositioned)

| finding | disposition |
|---|---|
| `bug bounties` not covered by `bug bounty` | named debt — inflection variant, needs owner confirmation |
| `dispatch mechanisms` not covered by `dispatch mechanism` | named debt — same class |
| `llm evaluations`/`llm evals` not covered by singular forms | named debt — same class |
| `ai benchmark(s)` too broad | named debt — kept out of the fix |
| `language model benchmark(s)`/`language model scoring` | named debt — no local record establishing them as required |
| `llmbenchmark` (camel-case fused) | named debt — `scope_norm` doesn't split camel case |

## Named limits (unchanged)

- Bare `benchmark`, `evaluation`, `eval`, `dispatch`, `swarm` stay
  non-triggers — the r12 note's deliberate exclusions hold.
- The screen reads only Meta `domain`/`scope` rows — prose mentions are
  never scanned (case 119 pins this).
