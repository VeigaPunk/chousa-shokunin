# chousa round 2 — goal-wave delivery report

Status: **ADMITTED** (round 2). Evidence commit: `c3df458` (records commit
follows). Baseline: `6344569` (round-1 publication). Wave: one 32-seat flash
call, 24/24 reports. Report time: 2026-10-15 ~23:50Z.

## Work performed

- Selected axis **coverage** — the lane's core method: claim-vs-source
  verification, registered in round 1.
- 32-seat wave implemented `verify-claims`, authored and span-verified the
  17-claim fixture, attacked the corpus boundary, and documented the honest
  limits of structural matching.

## Landed changes (evidence commit `c3df458`)

- `tools/research-gate.sh` → `03a33244…`: `verify-claims <file> [--root
  PATH]` — corpus-boundary canonicalization (refused unopened:
  out-of-corpus/URL/session), verbatim span match with line-aware misses,
  contradicted structural marker, per-claim verdicts, exact
  `VERDICT_BEARING_CLAIMS=N/M`, CLEAN|DRIFT under the 0/1/2 contract;
  selftest 20 → 30 (+10, first 20 byte-identical).
- `corpus/fixtures/claims-r2.jsonl` (17 claims from the three archived
  inputs) + `claims-r2.README.md` (provenance, marker convention, re-run).
- `corpus/knowledge/claim-verification-r2.md` (semantics + limits);
  lesson `2026-10-15-claims-span-fidelity.md`; receipts `claims-r2-*
  -{fixture,selftest,gate,live}.log`.

## Before → after measurements (parent acceptance, 2026-10-15T23:45Z)

| Check | Before (`0884355…`) | After (`03a33244…`) | Exit |
|---|---|---|---|
| selftest | 20/20 | 30/30 | 0 |
| fixture run (`--root ..`) | n/a | `VERDICT_BEARING_CLAIMS=17/17` CLEAN (13 sup/2 contra/2 unsup) | 0 |
| round-1 observable | 3/3 exports | 3/3 exports intact | — |
| boundary escapes | n/a | absolute/traversal/symlink/pipe refused; zero network (strace) | 2/refused |

## Debts (per the mission contract)

- **Receipt identity: OPEN** — these receipts are lane-local evidence logs,
  not queue taskKey/expected-receipt bags; proven receipt-backed completed
  rounds remain 0 pending integrator binding (operator/integrator surface,
  unchanged from round 1's handoff).
- Named residuals: in-root hardlink bypass; no claim-source size cap; the
  banner still prints `research-gate-r1`.
- Routing debt from round 1: satisfied for in-session waves by the
  operator's direct dispatch (this wave); the fleet-driver route bindings
  remain an operator surface.

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]` (no named non-author
  verifier; wave seats are the lane per protocol).

Boundaries held: no external live-target fetches (local-only round,
strace-confirmed); research corpus read-only; secrets untouched; fixtures and
scratch under `/tmp`; no commits by seats.
