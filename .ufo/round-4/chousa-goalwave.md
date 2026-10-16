# chousa round 4 — goal-wave delivery report

Status: **ADMITTED** (round 4). Evidence commit: `a6f3118` (records commit
follows). Baseline: `09153d1` (round-3 report). Wave: one 32-seat flash
call, 25/25 reports. Report time: 2026-10-16 ~01:00Z.

## Work performed

- Selected axis **calibration** — the round-3-named truncation limit.
- 32-seat wave shipped one shared token-boundary matcher for both modes,
  attacked it with truncation/padding/glue games, and kept every prior
  observable green.

## Landed changes (evidence commit `a6f3118`)

- `tools/research-gate.sh` → `6b83705b…` (+186/−15): shared
  `tok_word_char`/`tok_left_ok`/`tok_right_ok`/`tok_span_at` helpers; claims
  call site :907-910; chain quote branch :1060-1061; the character-class rule
  documented at :68-85; selftest 40 → 44 (+4, same fixture bytes through both
  modes).
- `corpus/knowledge/anchor-boundaries-r4.md`; lesson
  `2026-10-15-anchor-token-boundaries.md`; receipts
  `boundary-r4-20261016T002701Z-*.log`.

## Before → after measurements (parent acceptance, 2026-10-16T00:55Z)

| Check | Before (`67daf85e…`) | After (`6b83705b…`) | Exit |
|---|---|---|---|
| selftest | 40/40 | 44/44 ×2 (1-40 byte-identical) | 0 |
| claims fixture | 17/17 | 17/17 CLEAN (held) | 0 |
| chain fixture | 17/22 | 17/22 CLEAN (held); broken control DRIFT | 0/1 |
| truncation/padding games | passed (the defect) | all FAIL, controls PASS | 1 |
| r1 observable | 3/3 | 3/3 intact | — |

## Named limits and debts

- What hardening still cannot catch (in `anchor-boundaries-r4.md`): a real
  quote reused in a wrong context still resolves — semantic/context limits are
  a method matter, not a matching matter.
- **Receipt identity: OPEN** (operator side, unchanged).
- Round 5 registered: `verify-sweeps` — kept rejections + negative sweeps
  verdict-bearing.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: zero network; corpus read-only; /tmp quota respected and
monitored; seats cleaned scratch; no commits by seats.
