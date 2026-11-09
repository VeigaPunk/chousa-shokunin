# chousa round 99 — plan (L1 `ChousaR99`)

Base `47ed34fa785288837f84cde9db15c41300854a78` (round-98 landing plus its non-author spot-check). No earlier attempt
of round 99 (`.ufo/watchdog.log`: one `launch chousa round=99 … attempt=1` line); nothing inherited.

## Load and inputs

Read: the round prompt (`.ufo/prompts/chousa-round-99.md`, §1-§8 and amendments through 65), the round-98 report,
`corpus/lessons/round-98.md`, `corpus/lessons/round-98-verifier-spotcheck.md`, SCORECARD `## Planned — round 99`,
`corpus/README.md` `## Round98 coverage and frontier`, QUALITY 126 and 229, `tools/gate-records.py`.
Fresh-start rule: not bound (MANIFEST closures r91-r98 admitted).

Round-98 spot-check routed defects:
1. `claims.json` `freeze.F3` placeholder — convention fixed this round: a commit cannot carry its own hash, so the
   freeze hash is recorded below (`## Freeze`) by the commit after F, and `claims.json` says so. Round 98's F3 is
   `1c6e01c52149c7b4d6dfc4a8cfc419243dc8c101` (its report's landed-changes table); recorded in the round-99 lesson,
   the frozen round-98 file is not rewritten.
2. `R98MutantsC1` survivor R32 (verify-line whitespace) — carried into SCORECARD `## Planned — round 100` with
   G01-G03/D05.
3. `tools/gate-records.py` admits a quote from an http-200 challenge page — this round's C1.

## Claims (frozen in `.ufo/waves/round-99/claims.md`)

- C1 operability (lowest axis): the gate refuses challenge-page captures (CHALLENGE), battery
  `corpus/evidence/round99/challenge-controls-r99.py`.
- C2 coverage: `corpus/knowledge/quotation-error-rates-r99.md`, sourced on S236 and S233 (opened this round), controls
  `corpus/evidence/round99/entry-controls-r99.py`.

Routes (approval table `corpus/evidence/round99/egress-approval.md`; `refetch.tsv` rows S232-S236): PeerJ 403 (S232),
PLoS One 200 (S233, admitted), RIPR 2025 http-200 "Client Challenge" page (S234, rejected — and a live instance of
C1's defect class that QUALITY 229's lexical pattern misses), Europe PMC full text 500 (S235), Europe PMC core record
200 (S236, admitted).

Pre-freeze change P0: the CHALLENGE check was first written for the url/admit form only; before the freeze it was
extended to rev records whose path is a capture (a rev record citing S230's blob passed), and the battery gained two
rev legs on the production path.

## Wave

One v1 wave, 12 seats (`.ufo/waves/round-99/build_spec.py` → `w1-spec.json` → validated `w1-dispatch.json`):
executor 2, mutation-tester 2, reviewer 2, critic 1, sentinel 1, scout 1, revenger 1, connector 1, scribe 1. Attack
share (reviewer, critic, mutation-tester) 5/12. The L1 holds the canonical planner seat (the validator refuses
`planner`). No residual call planned.

## Freeze

F = the commit that first carries `claims.md`; its hash is written here by the carrier commit after it.
