# HTML-comment heading shadow (round 20)

source: tools/research-gate.sh (load_sections :394-470; scope_decl_screen :669-695); receipts: corpus/evidence/verify-r20-20261019T180000Z-{demo,selftest,battery,drift}.log; round-20 wave finding
verified-at: 2026-10-19 (round 20, landed; selftest PASS (124 cases, 0 skipped); gate sha 49b36759…)
recheck: `bash tools/research-gate.sh --selftest` (case 124 pins the HTML-comment arm); the demo record in `evidence/verify-r20-…-demo.log`

## The shadow

Same class as the fenced-heading shadow (r17) but a different syntax:
`load_sections` has no HTML-comment state — a `## ` line inside `<!-- -->`
is literal text in Markdown but was parsed as a heading, resetting the
section's body. A record whose real Meta declares a refused province plus
an HTML-comment `## Meta` declaring in-province passed CLEAN.

## The fix

`load_sections` now tracks `in_comment` alongside `fence_char`. Comment
state is checked after fence state (a `<!--` inside a fence is fence
content, not a comment) and before the heading check (a `## ` inside a
comment is literal). A `<!--` opener that has no `-->` on the same line
keeps `in_comment=1` until a `-->` line or EOF — same fail-closed
semantics as an unclosed fence.

## Named limits

- HTML comments inside a fenced block are fence content, not comments —
  correct by the check order.
- A `<!-- -->` on one line is handled (both markers on the same line
  don't toggle state).
- The parser is still not a Markdown renderer — CDATA, processing
  instructions, and other HTML constructs are edge cases outside the
  declared-record contract.
