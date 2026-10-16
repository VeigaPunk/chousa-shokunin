# chousa round 8 — goal-wave delivery report

Status: **ADMITTED** (round 8). Evidence commit: `27b55c3` (records commit
follows). Baseline: `848738c` (round-7 records). Wave: one 32-seat flash
call, 23/23 reports. Report time: 2026-10-16 ~05:15Z.

## Work performed

- Selected axis **freshness/operability** — the gate's own drift becomes
  detectable, adapting the sibling mori lane's r10 pattern (lineage declared
  in the gate header).
- 32-seat wave implemented `--pin`/`--drift`, committed the lane baseline,
  and attacked the design with field mutants, mode-skips, and volatile-list
  rewrites.

## Landed changes (evidence commit `27b55c3`)

- `tools/research-gate.sh` → `46f5ddb3…` (+523/−6): `--pin <path>` (canonical
  self-built fixture invocation, relative paths, byte-stable anywhere),
  `--drift <path>` (`GATE_DRIFT: none` 0 / named tokens 1 / missing-malformed
  2; never a false none), declared volatile contract (`ts gate_sha256`
  shape-masked; list-change is drift), token grammar (+finds/-findings,
  -SECTION:<name>, volatile_fields); selftest 74 → 85 (+11, 1-74 byte-
  identical).
- `corpus/evidence/gate-baseline-r8-20261016T033757Z.json` (THE lane
  baseline) + receipts `pin-r8-*`; `corpus/knowledge/gate-baseline-r8.md`.

## Before → after measurements (parent acceptance, 2026-10-16T05:10Z)

| Check | Before (`3ba718bf…`) | After (`46f5ddb3…`) | Exit |
|---|---|---|---|
| selftest | 74/74 | 85/85 ×2 (1-74 byte-identical) | 0 |
| committed baseline drift | n/a | `GATE_DRIFT: none` | 0 |
| field mutant / mode-skip / list-rewrite | passed silently | each named exactly | 1 |
| seven modes | — | byte-stable, solo holds (17/17, 17/22) | 0 |

## Named limits and debts

- Cannot catch: semantic drift inside a stable field (documented).
- **Receipt identity: OPEN** (operator side, unchanged).
- Sentinel recipe note: pattern-kills can self-match (a seat killed its own
  shell once with pkill -f); kill by PID or use the bracket trick.
- Round 9 registered: the three archived inputs through verify-all
  end-to-end + expanded fixtures.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: zero network; corpus read-only; sibling-lane files read-only;
seats cleaned scratch; no commits by seats.
