# FrontierR11 — draft `## Frontier` paragraph for round 11

Scope: `corpus/README.md` `## Frontier`, round 11 only. Read-only seat; `corpus/README.md` NOT edited. Insert the paragraph below at the gap after `corpus/README.md:485` (end of the Round 10 paragraph) and before `corpus/README.md:487` (`Still open and integrator/operator-owned:`), keeping round order.

## Draft paragraph (every number grounded; citations follow)

Round 11 ran the capstone audit that round 10 registered (SCORECARD.md:421-423), on the in-session wave routing: one 32-seat flash call, which the scorecard records as "31/31+ reports" and the wave report as 32 audit seats; the seat count is unverifiable without rosters and was folded in at admission as a correction. The move re-executed rather than changed anything: every admitted round's evidence commits and gate blobs were resolved by command, the battery was re-run at today's bytes, the 71-row limit ledger and its 30-item queue were re-parsed, and SHONEN readiness was assessed without self-attestation. The before→after observable on the gate is flat: gate `46f5ddb3…` at HEAD `44cbad6…` before and after the battery, selftest `PASS (85 cases)`, `GATE_DRIFT: none` against the r8 baseline `1c81a6cb…`, and the r1 counting command at `VERDICT_BEARING_EXPORTS=3/3`. What moved is the record: 28 re-audited findings rows (A1–A28), five audit-layer defects (D1–D5), and a verdict of ADMIT-with-correction with calibration and depth improved and freshness unchanged. Holds: selftest case lines identical to the r8 receipt, the verify-all manifest at 8 lines with sha `78627e6d…` equal to HEAD, zero network syscalls in the re-run trace, and the fixtures, records and controls reproducing their verdicts. That observable is not saturated: the note re-ran the commit, gate and verdict surfaces, but round 2–10 chain verification is attributed to per-round auditors whose reports the note could not see, so the 15/15 chain re-execution covers round 2 alone; receipt identity stays open for the operator at 0 of 10 receipt-backed rounds; SHONEN is 0/4 with no named non-author verifier; no round-11-named receipt exists under `corpus/evidence/`, so the battery lives verbatim in the note and the 39 logs it counts are the r2–r10 families; D1, D2, D4 and D5 were open when the audit landed (D3 closed at round 12), and this paragraph does not verify their later status. The gate itself moved after this round (round 12, `46f5ddb3…` → `91a01695…`), so the after-sha here is the round-11 end state only.

## Citations for each number (path:line)

| number / claim in paragraph | citation |
|---|---|
| round 10 registration of the capstone | SCORECARD.md:421-423 |
| axis calibration; in-session wave; "32-seat flash call"; "31/31+ reports" | SCORECARD.md:427-428 (`31/31+` at :428) |
| 32 audit seats | .ufo/round-11/chousa-goalwave.md:5, :13 |
| seat count unverifiable without rosters; folded at admission | SCORECARD.md:440-443; LOG.md:503-504 |
| re-execution method (commit/gate resolution, battery at today's bytes, ledger re-parse, SHONEN without self-attestation) | corpus/knowledge/audit-r11.md:33-36; :38-49; :235-239 |
| gate `46f5ddb3…` at HEAD `44cbad6…`, unchanged before/after | audit-r11.md:3-7; :57 (A3); :304 |
| selftest `PASS (85 cases)` | audit-r11.md:58 (A4); :172 |
| case lines identical to r8 receipt | audit-r11.md:59 (A5); :200 |
| `GATE_DRIFT: none` vs r8 baseline `1c81a6cb…` | audit-r11.md:60 (A6); :305; :173 |
| r1 `VERDICT_BEARING_EXPORTS=3/3` | audit-r11.md:75 (A21); :192 |
| 28 findings rows A1–A28 | audit-r11.md:55-82 |
| five defects D1–D5 | audit-r11.md:86 (D1), :102 (D2), :122 (D3), :130 (D4), :147 (D5) |
| ADMIT-with-correction; calibration/depth improved; freshness unchanged | SCORECARD.md:449-455 (calibration :451, depth :452, freshness in the unchanged row :453); LOG.md:508-509 |
| 71-row ledger, 38·25·3·1·4, 30-item queue | audit-r11.md:47; :73 (A19); :209-217; corpus/knowledge/hardening-r10.md:305-306, :320 |
| manifest 8 lines, sha `78627e6d…` == HEAD | audit-r11.md:74 (A20); :199; :306 |
| zero network (0 network syscalls) | audit-r11.md:198 |
| fixtures/records/controls reproduce | audit-r11.md:182-190 |
| round 2 chain 15/15 (round-2 only) | SCORECARD.md:432-434; .ufo/round-11/chousa-goalwave.md:21 |
| rounds 2–10 chains attributed to per-round auditors (not visible to the note) | .ufo/round-11/chousa-goalwave.md:22; audit-r11.md:33-36 |
| receipt identity open, 0 of 10 receipt-backed | audit-r11.md:230 (O1); :251-252; LOG.md:510 |
| SHONEN 0/4; NOT promotion-eligible; no named non-author verifier | audit-r11.md:241-252; :248-250; .ufo/round-11/chousa-goalwave.md:50 |
| 39 logs under corpus/evidence/ (r2–r10 families) | audit-r11.md:45 |
| D1 open (controls receipt 5 of 6 runs) | audit-r11.md:86-100 |
| D2 open (`-SECTION:sweeps` token) | audit-r11.md:102-120 |
| D3 closed at round 12 | LOG.md:567 |
| D4 open (uncommitted SKILL.md registry) | audit-r11.md:130-145 |
| D5 open (lesson cites superseded ledger) | audit-r11.md:147-155 |
| A-r9 C3 `:76`→`:86` closed at round 12 | audit-r11.md:312-340; corpus/knowledge/hardening-r10.md:427-428 |
| gate moved `46f5ddb3…` → `91a01695…` at round 12 | audit-r11.md:334 |
| battery run recorded verbatim in the note | audit-r11.md:169-201 |

## Findings the paragraph depends on (not in the draft's numbers)

1. Seat count conflict: SCORECARD.md:428 says "31/31+ reports"; .ufo/round-11/chousa-goalwave.md:5 and :13 say 32. Paragraph uses "32-seat flash call" as the call size and flags the count as unverifiable (SCORECARD.md:440-443). Not resolved here.
2. Receipt gap: `glob corpus/evidence/*r11*`, `*round-11*`, `*-r11-*` → no files. The round-11 battery exists only as verbatim text in corpus/knowledge/audit-r11.md §4 (:169-201). Paragraph states this; it does not invent a receipt name.
3. Index gap: corpus/README.md:63-65 says `knowledge/audit-r11.md` is unindexed, "queued for round 25". The Frontier paragraph does not index it; that is the round-25 freshness work, not this paragraph.
4. Label drift: SCORECARD.md:458 and .ufo/round-11/chousa-goalwave.md:36 say "rounds 2-11: ten admitted rounds"; audit-r11.md:42 says "10 (r1–r10)". Both total ten; the ranges differ. Paragraph avoids the range label.
5. Remote conflict (outside this paragraph): LOG.md:511-512 says "no lane remote exists for either lane"; LOG.md:569 (round 12) says "the origin remote exists and master is ahead 7". Not used in the paragraph; flagged for the records owner.
6. Gate sha after round 12 is `91a01695…` (audit-r11.md:334). I did not cite SCORECARD for that sha; the only verified location is the errata line.

## Tooling

No installs or updates. Reads and one glob only; no git/jj commands; no network.

VERDICT: Round 11 Frontier paragraph drafted at the `corpus/README.md:485`/`:487` gap with every number cited to path:line (no invented figures); freshness not claimed; gate flat at `46f5ddb3…`; README itself not edited.
