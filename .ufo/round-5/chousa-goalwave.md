# chousa round 5 — goal-wave delivery report

Status: **ADMITTED** (round 5). Evidence commit: `e7ab39a` (records commit
follows). Baseline: `45f8f65` (round-4 records). Wave: one 32-seat flash
call, 27/27 reports. Report time: 2026-10-16 ~02:05Z.

## Work performed

- Selected axis **coverage** — the last r1 structural axis: kept rejections
  and negative sweeps verdict-bearing.
- 32-seat wave implemented `verify-sweeps`, authored the fixture (+ broken
  control), and probed the vacuous-flip / narrow-sweep limits.

## Landed changes (evidence commit `e7ab39a`)

- `tools/research-gate.sh` → `55adb92d…` (+582 lines): `verify-sweeps <record>
  --root PATH` — `SWEEP_REJECTION_INCOMPLETE` (missing reason/flip-condition),
  local path-set emptiness re-run (`SWEEP_CLAIM_FALSE` naming hits), exempt
  non-local class, `SWEEP_LOCATION_ABSENT/OUT_OF_CORPUS/UNRESOLVED`,
  `VERIFIED_SWEEPS=N/M REJECTIONS_OK=K/L` + CLEAN|DRIFT; selftest 44 → 54
  (+10, 1-44 byte-identical).
- `corpus/fixtures/sweeps-r5.md` (+ broken control + README);
  `corpus/knowledge/sweeps-rejections-r5.md`; receipts
  `sweeps-r5-*-{selftest,fixture,broken,live}.log`.

## Before → after measurements (parent acceptance, 2026-10-16T02:00Z)

| Check | Before (`6b83705b…`) | After (`55adb92d…`) | Exit |
|---|---|---|---|
| selftest | 44/44 | 54/54 ×2 (1-44 byte-identical) | 0 |
| sweeps fixture | structural only | `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3` CLEAN | 0 |
| broken control | n/a | DRIFT naming SWEEP_REJECTION_INCOMPLETE + SWEEP_CLAIM_FALSE (hit path listed) | 1 |
| claims / chain holds | 17/17 · 17/22 | held CLEAN | 0 |

## Named limits and debts

- Vacuous flip-conditions and narrow-sweep triviality are documented limits
  (critic demonstrations in seat reports; disposition in the note).
- **Receipt identity: OPEN** (operator side, unchanged).
- Round 6 registered: `verify-all` composition + per-record verification
  state in the lane manifest.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: zero network; corpus read-only; /tmp quota respected; seats
cleaned scratch; no commits by seats.
