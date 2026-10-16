# chousa round 6 — goal-wave delivery report

Status: **ADMITTED** (round 6). Evidence commit: `74c533d` (records commit
follows). Baseline: `1d1f56c` (round-5 records). Wave: one 32-seat flash
call, 26/26 reports. Report time: 2026-10-16 ~03:25Z.

## Work performed

- Selected axis **operability/composition** — one record, one deep verdict.
- 32-seat wave implemented `verify-all` (+ the append-only `--json`
  manifest), authored the full/broken/absent fixtures, and probed the
  omission limit the absent!=drift semantics create.

## Landed changes (evidence commit `74c533d`)

- `tools/research-gate.sh` → `0c3d51ed…` (+450 lines): `verify-all <record>
  [--claims PATH] [--json PATH] [--root PATH]` — sections as fresh solo-mode
  invocations (tally-equal by construction), composed CLEAN|DRIFT,
  `SECTION … state=absent|run` reporting, `VERIFY_ALL sections=N run=N
  absent=N drift-sections=N` + one closing verdict; `--json` appends
  (>> only) the verification state to `corpus/evidence/verify-all-manifest.jsonl`;
  selftest 54 → 64 (+10, 1-54 byte-identical).
- Fixtures `full-r6.md` / `full-r6-broken.md` (+ absent-case reproduction);
  `corpus/knowledge/verify-all-r6.md`; receipts `compose-r6-*`.

## Before → after measurements (parent acceptance, 2026-10-16T03:20Z)

| Check | Before (`55adb92d…`) | After (`0c3d51ed…`) | Exit |
|---|---|---|---|
| selftest | 54/54 | 64/64 ×2 (1-54 byte-identical) | 0 |
| full record | 4 manual runs | CLEAN, sections=4 run=4, tallies = solo runs | 0 |
| broken record | n/a | DRIFT, drift-sections=2 (chain + sweeps named) | 1 |
| manifest | none | append-only jsonl, first lines committed | — |
| solo modes | 17/17 · 17/22 · sweeps CLEAN | held | 0 |

## Named limits and debts

- **absent != drift omission hole** (demonstrated by the omission-hunter): a
  claims-heavy record with no `## Claims` verifies-all CLEAN — round 7's
  registered binding-integrity move; record-type obligations beyond the
  lane's single type are an honest out-of-scope item.
- **Receipt identity: OPEN** (operator side, unchanged).
- Round 7 registered: binding integrity — cross-section references resolve
  fail-closed.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: zero network (strace-confirmed); corpus read-only; seats
cleaned scratch; no commits by seats.
