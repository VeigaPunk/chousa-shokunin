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

F = the commit that first carries `claims.md`: `d41f4cd8b857c6de683e7be5c5e8125b32763a8e` (helper `landed` line),
recorded here by the carrier commit after it. After receipts at F: `corpus/evidence/round99/after/c1-all.txt`,
`after/c2-all.txt` (clean shared clone checked out at F).

F2 = `96d761eec0c006d3df100b1a5d41686568d6d1e1` (helper `landed` line; the commit that first carries `## Amendments`
A1-A7, B1-B2), recorded here by the commit after it. C1 at F2: `corpus/evidence/round99/after-f2/c1-all.txt`
(tool unchanged F..F2, battery docstring only); C2's instrument and entry are unchanged F..F2, so `after/c2-all.txt` grades F2.

F3 = `c3bad643c42ecd1f04620bd6acfddb01d69c4aa3` (helper `landed` line; the commit that first carries B3-B6), recorded
here by the landing commit. C2 at F3: `corpus/evidence/round99/after-f3/c2-all.txt`; C1 bytes unchanged F2..F3.

## Amendments (F2)

Wave-forced narrowings, each recorded with its seat artifact in `.ufo/waves/round-99/claims.md` `## Amendments`
(A1-A7 for C1, B1-B2 for C2). None changes a predicate, a counter's code, a kill rule or a target; the C1 battery's
docstring changed (A1, A2), its code did not (AST of everything below the docstring equal F..F2).

- C1: A1 "28-word" (`R99ReviewerC1` F1, `R99CriticClaims`); A2 battery docstring o3-o5 (`R99ReviewerC1` F2,
  `R99SentinelC1` F-2); A3 separability — the battery reads two C2 captures and the C2 entry; probe receipt
  `corpus/evidence/round99/after-f2/c1-separability.txt` (`R99CriticClaims`); A4 limit (d) — the rev guard is keyed to
  the exact path spelling, `./corpus/captures/<key>.txt` and `.raw` admit a challenge blob (`R99SentinelC1` F-1,
  `R99ConnectorSiblings`, `R99ReviewerC1` F4); A5 limit (g) — markers, bound, `norm` and the rev guard are not shown
  live by the battery, six battery loosenings pass (`R99MutantsC1`); A6 limit (h) — a committed marker-less Chinese
  verification page is admitted (`R99RevenPrior`); A7 limit (g) — the rev legs cannot tell a whole-blob check from a
  quoted-line check (`R99SentinelC1` F-4).
- C2: B1 limit (c) — Never cells and a number's sense are unchecked by the controls (`R99MutantsC2`); B2 sentence —
  the coverage is new to this lane's corpus; tameshi holds Europe PMC records of both papers (S327 A mined, S328 A
  rejected) (`R99ConnectorSiblings` F4).

Routed to round 100 (not this round's claims): normalize the rev path before the capture guard (or check every rev
blob under `corpus/captures/`), marker fixtures one per marker plus 199/200/201 boundary fixtures and a whole-blob rev
fixture whose quoted line carries no marker (kills `R99MutantsC1` survivors and `R99SentinelC1` F-4), a Never-cell
leg and a number-sense leg for entry controls, the fleet tier rule for index-record abstracts (tameshi A vs chousa B).

## Amendments (F3)

C2 only, after `R99ScoutSources` (the last seat to report): B3 entry scope sentence, B4 row-1 Do cell, B5 named limit
(27 vs 28 studies), B6 "numeral" in the C2 sentence and limit (c). Recorded with artifacts in `claims.md`
`## Amendments`. The C2 counters and every C2 tally are unchanged at F3 (`corpus/evidence/round99/after-f3/c2-all.txt`).
S235's flip condition was met by the seat's re-open, not by a lane GET; routed to round 100 with the 2025 update's
Europe PMC record (pmid 40696441, PMC12285159).
