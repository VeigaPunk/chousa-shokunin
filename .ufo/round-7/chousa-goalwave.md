# chousa round 7 — goal-wave delivery report

Status: **ADMITTED** (round 7). Evidence commit: `a1948c3` (records commit
follows). Baseline: `4835426` (round-6 records). Wave: one 32-seat flash
call, 24/24 reports. Report time: 2026-10-16 ~04:20Z.

## Work performed

- Selected axis **coverage-of-integrity** — the round-6 demonstrated hole:
  dangling cross-section references pass every mode.
- 32-seat wave implemented `verify-integrity` as verify-all's fifth section,
  authored the integrity fixtures, and probed extraction limits.

## Landed changes (evidence commit `a1948c3`)

- `tools/research-gate.sh` → `3ba718bf…` (+536/−20): seventh mode
  `verify-integrity <record> --root PATH` — declared ids (Sources/Claims/
  Negatives/Sweeps), reference cells across chain/claims/negatives/sweeps/
  rejections, exact-id resolution, `REF_UNRESOLVED` (warn, drift),
  exempt-but-counted classes, `INTEGRITY refs=N resolved=M unresolved=K`;
  composed into verify-all (`VA_ORDER` gains integrity); `--json` manifest
  lines carry five sections; selftest 64 → 74 (+10, 1-64 byte-identical).
- Fixtures `integrity-r7.md` / `integrity-r7-broken.md` (+ claims binding +
  README); `corpus/knowledge/reference-integrity-r7.md`; receipts
  `integrity-r7-20261016T030552Z-*.log`.

## Before → after measurements (parent acceptance, 2026-10-16T04:15Z)

| Check | Before (`0c3d51ed…`) | After (`3ba718bf…`) | Exit |
|---|---|---|---|
| selftest | 64/64 | 74/74 ×2 (1-64 byte-identical) | 0 |
| integrity fixture | dangling refs pass CLEAN | 16 refs / 15 resolved / 0 unresolved, CLEAN | 0 |
| broken control | n/a | DRIFT naming REF_UNRESOLVED S9 (chain from) + C9 (sweeps claim_id) | 1 |
| solo holds | 17/17 · 17/22 | held | 0 |

## Named limits and debts

- Extraction limits (critic, dispositioned in the note): substring-looking
  ids, tokens inside quoted spans — documented semantics.
- **Receipt identity: OPEN** (operator side, unchanged).
- Round 8 registered: gate behavioral baseline (`--pin`/`--drift`).

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: zero network; corpus read-only; /tmp quota held (28 clean
samples); seats cleaned scratch; no commits by seats.
