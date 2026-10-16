# chousa round 3 — goal-wave delivery report

Status: **ADMITTED** (round 3). Evidence commit: `cc9fe8f`; records: `7f60755`.
Baseline: `0aa794d` (round-2 records). Wave: one 32-seat flash call, 24/24
reports. Report time: 2026-10-16T00:25Z.

## Work performed

- Selected axis **coverage** — citation chaining becomes verdict-bearing
  (round 2's named continuation).
- 32-seat wave implemented `verify-chain`, authored the 22-hop fixture (+ a
  broken control), and verified the boundary policy composes across all three
  modes.

## Landed changes (evidence commit `cc9fe8f`)

- `tools/research-gate.sh` → `67daf85e…`: `verify-chain <record> [--root PATH]`
  — each resolved hop's citation must resolve: source = a declared Sources id
  or an in-corpus path (unknown ids refused; same canonicalization as
  verify-claims), anchor exists (heading trimmed-equality / quote verbatim /
  whole-line) with `at=line:N` line-aware misses; unresolved-or-marked hops
  exempt-but-counted; `RESOLVED_HOPS=N/M` + CLEAN|DRIFT under the 0/1/2
  contract; selftest 30 → 40 (+10, first 30 byte-identical).
- `corpus/fixtures/chain-r3.md` (22 real hops from the archived inputs) +
  `chain-r3-broken.md` control + README; `corpus/knowledge/chain-resolution-r3.md`;
  receipts `chain-r3-20261015T235623Z-*.log`.

## Before → after measurements (parent acceptance, 2026-10-16T00:15Z)

| Check | Before (`03a33244…`) | After (`67daf85e…`) | Exit |
|---|---|---|---|
| selftest | 30/30 | 40/40 ×2 | 0 |
| chain fixture | structural only | `RESOLVED_HOPS=17/22` CLEAN (17 verified / 5 exempt) | 0 |
| broken control | n/a | DRIFT, `anchor-missing` named | 1 |
| verify-claims | 17/17 | 17/17 byte-identical | 0 |
| r1 archive observable | 3/3 | 3/3 intact | — |

## Environmental note

The host's per-user /tmp quota exhausted mid-acceptance (nine waves of
accumulated declared-ephemeral scratch). The parent freed 727 MB
(`/tmp/mori-*`, `/tmp/chousa-*`, etc.) and re-ran the battery clean. No lane
artifact was affected; the scratch was always declared ephemeral. Future waves
were instructed to fall back to `$HOME/.cache/<lane>-tmp` if /tmp refuses
writes.

## Named limits and debts

- **Anchor substring semantics:** a truncated quote still resolves (no
  token-boundary check) — round 4's registered hardening, for both
  verify-chain anchors and verify-claims spans.
- **Receipt identity: OPEN** (operator side, unchanged from rounds 1–2).
- Named residuals from seat reports live in `chain-resolution-r3.md`.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: zero network (strace-confirmed by seats); research corpus
read-only; no secrecy reads; no commits by seats.
