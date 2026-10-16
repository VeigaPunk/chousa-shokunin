# chousa round 10 — goal-wave delivery report

Status: **ADMITTED** (round 10). Evidence commit: `5f99fa3` (records commit
follows). Baseline: `d5c99c2` (round-9 records). Wave: one 32-seat flash
call, 23/23 reports. Report time: 2026-10-16 ~07:25Z.

## Work performed

- Selected axis **hardening/calibration** — archive-scale negative controls
  and the final limit-disposition ledger.
- 32-seat wave authored six class-isolated controls, audited every exempt
  item, and reconciled every limit named across rounds 2-9.

## Landed changes (evidence commit `5f99fa3`)

- `corpus/fixtures/archives-r9/controls/` — six controls (one per defect
  class, each a scripted byte-edit of its clean record + README with expected
  verdicts + named non-coverage); `corpus/knowledge/hardening-r10.md` (the
  disposition ledger); receipts `controls-r10-*`.

## Before → after measurements (parent acceptance, 2026-10-16T07:20Z)

| Control | Verdict (parent re-run) | Exit |
|---|---|---|
| A-r9-span-not-found | CLAIM_SPAN_NOT_FOUND (exactly one finding) | 1 |
| A-r9-anchor-missing | CHAIN_ANCHOR_NOT_FOUND | 1 |
| B-r9-rejection-missing-flip | SWEEP_REJECTION_INCOMPLETE | 1 |
| B-r9-false-sweep | SWEEP_CLAIM_FALSE (hits named) | 1 |
| C-r9-dangling-ref | REF_UNRESOLVED (C9 named) | 1 |
| C-r9-structure-break | NO_QUESTION (crit) | 1 |
| clean A/B/C | held CLEAN | 0 |
| holds | selftest 85/85 · `GATE_DRIFT: none` · gate byte-unchanged | — |

## Named

- `RECORD_SCHEMA_INVALID` cannot fire alone (companion structural findings
  drag) — documented non-coverage.
- **Receipt identity: OPEN** (operator side, unchanged).
- Round 11 registered: the chousa capstone audit (evidence chains, receipts,
  verdicts, limit reconciliation, SHONEN readiness, re-executions).

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: zero network; corpus read-only; no gate change (the round's
standing rule); seats committed nothing.
