# Fenced-heading anchor false-positive (round 23)

source: tools/research-gate.sh (chain_anchor_at :1514-1560; the heading arm ~:1518-1540); receipts: corpus/evidence/fanchor-r23-20261019T192000Z-{demo,selftest,battery,drift}.log; round-20 named debt closed
verified-at: 2026-10-19 (round 23, landed; selftest PASS (133 cases, 0 skipped); gate sha b5d0f93d…)
recheck: `bash tools/research-gate.sh --selftest` (case 129 pins the fenced-anchor arm); the demo record in `evidence/fanchor-r23-…-demo.log`

## The false-positive

`chain_anchor_at` for `heading` kind scans raw lines with `^#+[[:space:]]+`
— no fence state. A `## Phantom Heading` inside a fenced code block matched
as a real heading, making a chain hop `verified` on a literal-text anchor
that should be `anchor-missing`.

## The fix

The heading arm now tracks fence state inline (same contract as
`load_sections`: same char must close, closing length >= opening, 0–3
literal-space indent; unclosed = literal to EOF). A `# ` line inside a
fence is consumed as body text, never an anchor target.

## Named limits

- The `quote` and `line` anchor kinds are unaffected — they match literal
  text regardless of fence state (correct: a quote is a quote inside or
  outside a fence).
- The fence tracking is per-call (each `chain_anchor_at` invocation
  resets fence state) — correct: each anchor match is against one
  source file's content.
