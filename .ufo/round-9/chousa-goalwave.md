# chousa round 9 — goal-wave delivery report

Status: **ADMITTED** (round 9). Evidence commit: `ebd04d2` (records commit
follows). Baseline: `f11073a` (round-8 records). Wave: one 32-seat flash
call, 24/24 reports. Report time: 2026-10-16 ~06:25Z.

## Work performed

- Selected axis **coverage** — the archive corpus gets its first full deep
  verification. Fixture-led: no gate change expected or made.
- 32-seat wave authored the three archive records (spans machine-extracted),
  expanded claims (17 → 27), measured coverage, and probed the reframing
  risk.

## Landed changes (evidence commit `ebd04d2`)

- `corpus/fixtures/archives-r9/{A,B,C}-r9.md` + `README.md` (provenance,
  reframing-risk section, re-run recipe); `corpus/fixtures/claims-r9.jsonl`
  (10 new verbatim claims); `corpus/knowledge/archives-verified-r9.md`;
  receipts `archives-r9-*` + three `--json` manifest lines.

## Before → after measurements (parent acceptance, 2026-10-16T06:20Z)

| Check | Before | After | Exit |
|---|---|---|---|
| verify-all on archives | never run | A/B/C all CLEAN, zero findings | 0 |
| A record | — | 6/7 hops · 13 refs/0 unresolved · 4/4 rejections · 1/1 sweeps | 0 |
| B record | — | 6/7 · 14/0 · 3/3 · 1/1 | 0 |
| C record | — | 7/8 · 15/0 · 4/4 · 1/1 | 0 |
| claims coverage | 17 | 27 (10/10 CLEAN: 7 sup / 2 contra / 1 unsup) | 0 |
| holds | — | selftest 85/85 · `GATE_DRIFT: none` · claims-r2 17/17 | 0 |

## Honest folds

- Premise correction: the archives do not literally cross-cite (`grep`
  proof); hops authored intra-archive/conceptual, recorded.
- Reframing risk (record-format distortion) named + mitigated in READMEs.
- **Receipt identity: OPEN** (operator side, unchanged).

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: archives quoted read-only; zero network; gate untouched;
seats committed nothing; parent integrated under the chousa lane identity.
