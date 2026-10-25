# Scope-refusal screening (round 12)

source: tools/research-gate.sh (scope_decl_screen, SCOPE_* constants); PROVINCE.md:10-15; SKILL.md:42-52; LOG.md 2026-10-15 boundary-parity entry
verified-at: 2026-10-19 (round 12; selftest cases 86-92; gate sha256 91a01695…)
recheck: re-run `bash tools/research-gate.sh --selftest` (cases 86-92) and `bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json` after any gate edit

## The contract

The structure check (`verify` / `verify-all`'s structure section) screens a
record's **declared** scope against the three refused provinces. Only the
record's own `## Meta` rows are read — the table row `| scope | value |` and
the `key: value` line row, keys `domain`/`scope` (case-insensitive). Prose,
`## Question` text, `note` cells, source/archive pointers and every other
section are never keyword-scanned: the round-9 B archive names multi-agent
knowledge in prose and its record stays CLEAN (measured 0 `SCOPE_` findings).

## Classification (normalized: lowercase, punctuation runs → one space)

| Declaration value contains (phrase) | Finding (warn → drift, exit 1) | Route |
|---|---|---|
| `bug bounty`, `bounty program(s)`, `bounty hunt(ing)`, `bounty scope`, `claim package(s)`, `kasegi` | `SCOPE_BOUNTY_ABSORBED` | kasegi |
| `model quality`, `model evaluation(s)`, `model eval`, `model benchmark(s)`, `model scoring`, `llm quality/evaluation/eval`, `language model quality/evaluation`, `kengaku` | `SCOPE_MODEL_QUALITY_ABSORBED` | kengaku |
| `orchestration`, `dispatch mechanism`, `(multi agent\|multiagent\|agent\|fleet) dispatch`, `swarm wave(s)/call(s)/dispatch/orchestration`, `agent lifecycle(s)`, `agent roster(s)`, `kumitate` | `SCOPE_ORCHESTRATION_ABSORBED` | kumitate |

One finding per matched refused province per declaration row, provinces in
the fixed order bounty → model-quality → orchestration; all matching rows are
scanned in body order. Empty values skip.

## Deliberately not triggers

Bare `bounty`, `agent`, `multi agent`, `swarm`, `dispatch`, `evaluation`,
`eval`, `quality`, `benchmark`, `model`, `knowledge`, `claims` — they carry
legitimate research senses (the B-archive vocabulary and this lane's own
working terms). `evaluation claims` and bare `dispatch` are excluded on
purpose. Negations are not parsed: a declaration asserting "not model
quality" fires (named limit; phrase specificity is the guard, not negation
handling).

## Disposition rule

The screen reports, never absorbs: a refused declaration is a warn finding
that drifts the record (exit 1), and the record's author routes the work to
the owning province (kasegi / kengaku / kumitate) — matching the round-1
landing requirement (LOG.md 2026-10-15: "all three refused provinces have
identical gate teeth, with one symmetric selftest fixture per province").

## Named limits

- **Declaration-only detection cannot catch undeclared absorbed scope**: a
  record that silently does bounty research without declaring it in `##
  Meta` passes. The r11 audit's row-70 closure is "teeth for declared
  scope", not a scope police.
- **Solo modes lack the teeth**: `verify-claims/chain/sweeps/integrity` on a
  refused-scope record still pass; enforcement exists only via `verify` /
  `verify-all` (the r1 structural axis).
- **The pin fixture's clean declaration** (`| domain | deep-research method |`
  in the canonical capture) means a pattern-widening regression over-catches
  drifts the committed r12 baseline.
- **A `note` Meta cell naming refused words is not scanned** (key-triggered
  surface only), and the pass-control Approval table's `scope` **column** is
  untouched because only `## Meta` rows are read — the code implements this;
  the selftest fixtures exercise the Meta `domain`/`scope` row forms, not
  the `note` or Approval surface explicitly (corrected round 16).
