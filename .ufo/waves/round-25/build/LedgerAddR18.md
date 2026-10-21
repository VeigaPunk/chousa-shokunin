# Round-18 hardening ledger reconstruction

## Evidence chain

- `SCORECARD.md:906-945` records the round-18 phrase-gap claim, before/after behavior, hold results, and verdict. It says the three landed literal phrases are `llm benchmark|llm benchmarks|llm scoring`; `ai benchmark(s)` stays named debt (`:923-931`).
- `LOG.md:675-685` records the same closure, knowledge note, gate transition, and test results. The round-18 code commit is `a80964c`; the records commit is `216b539`; final report commit is `71b0b5f` (`git log --oneline --all`, round-18 entries).
- `corpus/knowledge/scope-phrase-gap-r18.md:7-40` explains the literal-match boundary and keeps `ai benchmark(s)` and the other inflection candidates as named debt.
- Gate SHA-256, measured with `git show a80964c^:tools/research-gate.sh | sha256sum` then `git show a80964c:tools/research-gate.sh | sha256sum`: `c2915f24d73d656ca23b7f6228cbdd502c27a8c07670776fed84c70f278266f8` → `6e69488160199cc1704bd1d17b7523cd39022016ad123ecf43575467b266de0c`.
- `tools/research-gate.sh:4909-4926` and `corpus/evidence/scope-r18-20261019T173000Z-selftest.log:117-120`: cases 117 `scope-fail-llm-benchmarks` and 118 `scope-fail-llm-scoring` expect DRIFT; case 119 `scope-pass-benchmark-prose` expects CLEAN. The receipt reports PASS (119 cases, 0 skipped); `SCORECARD.md:923-931` records cases 1–116 byte-identical, baseline drift `none`, r1 `3/3`, and masked battery `ALL IDENTICAL`.
- No §3 ledger row or §3.9 round-11 queue item was closed, changed, or added. Proof: `git diff --name-status 2478304 71b0b5f -- corpus/knowledge/hardening-r10.md` → *(empty)*. The round-18 gate commit changed only `tools/research-gate.sh`; the records commit lists LOG/SCORECARD/SKILL/README/evidence/note files, not `hardening-r10.md` (`git show --stat a80964c`; `git show --stat 216b539`). This is a `SCOPE_KENGAKU` declaration-phrase fix, not a ledger disposition.
- No LSP route was exposed in this seat's tool inventory; source grep was only a locator. The behavior claim above is grounded in the committed gate diff, selftest case definitions, and captured receipt.

## Proposed append-only addendum (append at EOF; target left untouched)

### Round-18 addendum (2026-10-19, append-only)

E5 — the round-16 `LLM benchmarks` phrase gap closes at `SCOPE_KENGAKU`: the gate adds the literal phrases `llm benchmark|llm benchmarks|llm scoring`. The plural is a separate entry because `scope_hit` matches literal phrases, never stems. `ai benchmark(s)` remains named debt — too broad for AI-methodology research. Selftest cases 117–119 pin the two Meta-declaration refusals and the prose-only CLEAN control; cases 1–116 remain byte-identical. Gate SHA `c2915f24…` → `6e694881…`; drift `none` vs the r12 baseline; r1 `3/3`; masked battery ALL IDENTICAL. See `knowledge/scope-phrase-gap-r18.md` and `evidence/scope-r18-20261019T173000Z-{demo,selftest,battery,drift}.log`.

No §3 ledger row and no round-11 audit-queue item was closed, changed, or added by round 18. Evidence: `git diff --name-status 2478304 71b0b5f -- corpus/knowledge/hardening-r10.md` is empty; the landed round-18 commits do not modify this ledger.

Installs: none.
VERDICT: Round 18 closed the `SCOPE_KENGAKU` phrase gap; there is no §3 ledger or round-11 queue delta. The proposed addendum is evidence-backed; the ledger file remains unedited by this read-only seat.
