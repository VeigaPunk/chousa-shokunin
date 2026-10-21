# ScoutCarriedDebt — open/carried named debt at base ba333325 (round 26, attempt 1)

Base verified: `git log --oneline -2` → ba333325 (r25 final) is parent of prereg
f361d12e; `git diff --name-status ba333325…f361d12e` shows ONLY
corpus/evidence/round26-claims.md added. Observations at prereg state; paths
relative to lane root. Read-only seat; no installs.

## A. Debts this round's claims touch
1. C1 (bounded metadata reader) — closure-routed from MANIFEST rounds[395] via
   round26-claims.md:11-19; amplification site grounded: per-line read loop at
   tools/research-gate.sh:2386, inside the cited :2383-2387 window.
2. C3 = SCORECARD.md:1380-1383 (Planned item 3); directly answers R25-M10
   "syntactic screen ≠ full bar" (round-25.md:46) — carried until C3 lands.
3. C2 = SCORECARD.md:1377-1379 (item 2); makes QUALITY 6's "overdue
   uncomputable" computable for scheduled entries only (QUALITY.md:22-23).
4. NOT claimed — appender race / Planned item 1 (SCORECARD.md:1373-1376):
   prereg carries it explicitly (round26-claims.md:15-19, QUALITY 11
   disposition). flock candidate still unlanded:
   .ufo/waves/round-25/build/unlanded-append-race.patch exists; repro
   .ufo/waves/round-25/build/ExecAppendRace.md exists.
5. NOT closed by C2 — three legacy entries lack `recheck:`
   (archives-verified-r9, audit-r11, gate-baseline-r8; see
   corpus/evidence/round25-final-measure.log:19); C2 yields
   due=unknown/freshness=unknown for them (round26-claims.md:67-70);
   META_RECHECK_ABSENT persists.

## B. hardening-r10 ledger queue (live counts owner hardening-r10.md:685-696)
- Committed 24 / queue-true 25; re-derive `python3
  corpus/evidence/round25-ledger-recount.py`; output at
  corpus/evidence/round25-ledger-recount.log:1.
- Carried §3 rows (22): 11,13,14,22,24,25,26,29,32,33,38-45,47,49,53,57 —
  hardening-r10.md:206,208,209,222,224,225,231,234,242,243,253-260,267,269,273,282.
- Operator rows (3): 68,69,71 — hardening-r10.md:298-301 (70 closed by E1,
  :444-451).
- 25th queue-true item = committed-count undercount, the same-device-bind
  mountinfo walk (closure text :478-482, :502-504; arithmetic :691-692).
- No C1/C2/C3 claim touches any of these classes [INFERENCE from
  round26-claims.md:26-125; all 22 rows are token/integrity/baseline classes
  outside the metadata reader].

## C. Carried inside closures (no §3 row)
- TOCTOU, same-device binds, unmeasurable-stat fallback, legit in-root
  multilink families refusing — hardening-r10.md:478-482; reconfirmed :581-583.
- Row 9 residual: record reads (load_sections, scan_secrets) + verify-all
  claims-surface binding uncapped — :420-425; reconfirmed :575-578.
- Row 56 residual: no mode pairs a pointer line with its span's occurrence
  line — :438-441; reconfirmed :595-597.
- Row 70 residual: scope screen stays declaration-only — :584-586.
- Claim touch: none; C1 is same-surface adjacency only (it changes the
  reader's internal representation, adds no cap) [INFERENCE].

## D. round-25 lesson out-of-population paragraph (round-25.md:50-57) — all carried, none touched
1. Historic placeholder slots in LOG/SCORECARD (seat report
   .ufo/waves/round-25/build/ScoutPlaceholderSweep.md exists).
2. r15–r23 battery receipts show DRIFT under `root=.` while prose says "ALL
   IDENTICAL".
3. r16 has no dedicated receipt.
4. pointer-boundary-r21.md contradicts itself on the path-start bypass.
Carrying bar: QUALITY 2/4/9/10 — all exist (QUALITY.md:4,6,33-37,38-45).

## E. Spot-check intake carried rows (round-25.md:18-31)
- :20 appender blank line — the D-11 carrier; origin
  lessons/round-24-verifier-spotcheck.md "Debts:" line; evidence
  evidence/json-r24-20261019T213117Z-demo.log:26-29 (per intake row).
- :21 and :26 — remaining parent-root rechecks carried under criterion 13
  (exists, QUALITY.md:59-68); class live at base: META_RECHECK_ROOT_PARENT on
  hardening-r10.md (round25-final-measure.log:21).
- :31 — D-11 retained open, separate from the r24 delimiter fix.
- All other intake rows are fixes/closures, not carries.

## F. Staleness flags — stated carrying criterion still exists?
- No vanished carrying criterion found: criteria cited by carried items (2, 6,
  9, 10, 11, 13) all present at base (QUALITY.md:4,17-23,33-45,46-51,59-68).
- Superseded-but-still-cited carriers: hardening-r10.md:305-307 and :320-348
  (the 30-item queue line) plus E1–E4 counts lines are history; the live owner
  is :685-696 — an r26 seat citing the 30-item line or any pre-E5 tuple is
  stale.
- Row 9's residual text "record reads … stay uncapped" (:420-425) predates the
  r25 verify-metadata reader, which is itself size-capped (C1 observation,
  round26-claims.md:29-31): carrying text partially outdated; the residual is
  not closed for load_sections/scan_secrets/verify-all surfaces.
- Same-device-bind mountinfo walk "r15+ candidate" (:502-504) has no owning
  round in Planned r26 — carried unscheduled; criterion text intact.
- Working-tree note: QUALITY.md now shows a Round-26 criterion 18 (:102-113)
  absent from both base and prereg — uncommitted live wave write; not used for
  base judgments here.

## G. Adjacent (outside the five named sources)
- verification-r16.md named-limit queue (same-device binds, overlay roots,
  TOCTOU, unmeasurable-stat — verification-r16.md:54-57) remains open; r19
  closed that round's one named debt (hardening-r10.md:635-639); no later
  movement observed.

VERDICT: 25 queue-true items (22 carried rows + 3 operator + 1 undercount item), 4 inside-closure residuals, 4 out-of-population debts and the D-11 appender race all remain carried; C1/C2/C3 touch only the closure-routed reader risk, the R25-M10 screen-vs-bar debt, and QUALITY-6 overdue computability; no carried item's stated carrying criterion has vanished.
