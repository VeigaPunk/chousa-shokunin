# Fenced-heading shadow (round 17)

source: tools/research-gate.sh (load_sections ~:394-470; scope_decl_screen :669-695); receipts: corpus/evidence/fence-r17-20261019T171200Z-{demo,selftest,battery,drift}.log; round-16 named debt closed
verified-at: 2026-10-19 (round 17, landed; selftest PASS (116 cases, 0 skipped); gate sha c2915f24…)
recheck: `bash tools/research-gate.sh --selftest` (cases 112–116 pin the shadow class); the demo record in `evidence/fence-r17-…-demo.log`

## The shadow

`load_sections()` splits a record into `SEC_BODY[section]` on every line
matching `^##[[:space:]]+`. It has no fence state — a `## ` line inside a
fenced code block is literal text in Markdown but was parsed as a heading,
resetting that section's body. The scope screen (`scope_decl_screen`)
checks only `SEC_BODY[Meta]` — so a record whose real Meta declares a
refused province (e.g. `domain: bounty program scope`) but carries a
fenced `## Meta` declaring an in-province domain passed CLEAN: the fenced
copy overwrote the real body.

## The fix shape (two-pass, measured)

Pass 1 pairs fences: a line matching `^\ {0,3}(\`{3,}|~{3,})` opens a
fence (same char must close it, closing length >= opening, 0–3 literal-
space indent only — a tab-indented closer is content). An unclosed opener
IS a fence: everything after it is literal (fail closed — a `## ` inside
an unclosed fence cannot shadow a real heading).

Pass 2 skips `## ` lines inside paired fences; fenced content still flows
into the open section's body (literal text, not a section reset).

## Why the naive fix fails (measured)

A single `^``` ` toggle fixes only the simplest shadow:

| shape | naive toggle | two-pass |
|---|---|---|
| real refused Meta + fenced in-province Meta | DRIFT | DRIFT |
| fenced refused Meta alone (no real Meta) | DRIFT (phantom) | CLEAN |
| 4-backtick outer, 3-backtick inner `## Meta` | **CLEAN** | DRIFT |
| 4-space-indented ``` inside a fence | **CLEAN** | DRIFT |
| unclosed fence, refused Meta before it | **CLEAN** | DRIFT |

The naive toggle closes on the first 3-backtick line regardless of the
outer fence's length, treats an indented closer as a close, and treats an
unclosed opener as plain text (letting the shadow through). The two-pass
shape closes all five variants.

## Call-site audit

`load_sections` serves every mode that reads `SEC_BODY`: verify_record
(scope screen + structure checks), verify_chain, verify_sweeps,
verify_integrity, verify-all's section state builder. No caller depends
on fenced headings being treated as sections — the corpus has zero `## `
lines inside fences (measured: 58/58 `.md` files under `corpus/`).

## Named limits

- Fenced **data rows** inside a real section are still trusted
  (`table_rows` doesn't check fence state — a fenced `approved` row can
  suppress `EXTERNAL_WITHOUT_APPROVAL`; named debt).
- The parser is not a Markdown renderer — HTML blocks, indented code,
  and mixed fence chars are edge cases the two-pass shape covers by
  construction.
