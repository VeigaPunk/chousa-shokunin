# ScribeClaimSurfaces — round-40 claim-surface cross-read

author: ScribeClaimSurfaces (L2 leaf seat, chousa round 40 wave 1)
date: 2026-10-24
round: 40 (attempt 1)
attack: Cross-read `LOG.md`, `SCORECARD.md`, and the round-40 report for consistent
claim wording, exact counts, measured lane revision, source pointer, and
correction/disposition statements.
mode: read-only; this seat wrote only this file. No counter was executed.

## Verdict

**PASS WITH FINDINGS.** Among the three named documents the measured claims and
their counts are mutually consistent and reproduce structurally from committed
bytes. Eight defects were found, all wording/pointer/revision-scope/record
completeness; none falsifies the frozen predicates P1 or P2. The material one is
F1: the three named documents say the round has no non-author spot-check, while
the lane's current tip contains a committed non-author spot-check that says
otherwise.

| Dimension | Verdict | Basis |
|---|---|---|
| Claim wording (C1/C2) | consistent, two wording defects (F4, F5) | claims.md 9, 19, 23 vs report 8-11, LOG 1474-1478, SCORECARD 2257-2260, 2268-2271 |
| Exact counts | **consistent** | all counts below re-derived from committed trees; no disagreement found |
| Measured lane revision | consistent through `282dc76`; stale at current tip (F1) | `git log`, `git rev-parse HEAD` |
| Source pointer | resolves, one imprecise pointer (F3), one range overhang (F6) | line-by-line reads below |
| Correction/disposition statements | R2-R5 statuses consistent; R4 conflict preserved; R5 paraphrase (F5); after-state absent from claims (F8) | dispositions JSON vs claims 197-200, SCORECARD 2257-2260, report 9 |
| Claim rigor vs counter | overstated for R2/R5 (F2) | claims.md 23 vs `c2-count.py:61-63,81-83` |
| Wave evidence | counts consistent; post-correction validation transcript absent (F7) | spec/plan/dispatch/registry at `d164f88` vs DISPATCH-README |

## Method (exact commands and observed output)

Executed in `/home/vgpnk/Projects/shokunin/chousa-shokunin` unless a path says
otherwise. Counter scripts were **not** run; their committed outputs were read.

1. `git log --oneline -6` →

```
6bc90e0 round-40 verifier spot-check (integrator, hyaku): non-author admit/reject
282dc76 round-40: record committed measurements and lesson
d164f88 round-40: repair receipt evidence and calibrate r39 records
6c01a41 round-40: freeze receipt and calibration claims
691d264 round-39 verifier spot-check (integrator, hyaku): non-author admit/reject
6ac1007 round-39: knowledge x2 (S071 re-opened), lesson (4 mistakes, QUALITY 56), ...
```

`git rev-parse HEAD` → `6bc90e04ac60307befacd554f7eee2b7284e2652`.
`git cat-file -t` returned `commit` for `6c01a41`, `d164f88`, `282dc76`,
`691d264`.

2. Read as committed evidence, not re-executed:
   `.ufo/waves/round-40/controls/control-before.txt` (C1 `3/6`, `C1_EXIT=1`;
   C2 `0/4`, `C2_EXIT=1`), `corpus/evidence/round40/measure-after.txt`
   (C1 `6/6`, `C1_AFTER_EXIT=0`; C2 `4/4`, `C2_AFTER_EXIT=0`), and
   `corpus/evidence/round40/{claims.md,active-r39-receipts.tsv,routed-defect-dispositions.json}`.

3. Role mixes re-derived from committed JSON (jq), not via the counters:

```
r39 spec : 32 = connector1 critic5 executor6 mutation-tester3 revenger2 reviewer6 scout3 scribe3 sentinel2 simplifier1
r39 plan : 32 = identical mix
r40 spec : 33 = connector1 critic6 executor6 mutation-tester3 revenger2 reviewer6 scout3 scribe3 sentinel2 simplifier1
r40 plan : 33 = identical mix
```

`w1-spec.json`: 33 items, 33 distinct names. `w1-plan.json`: 33 tasks, 33
distinct names. `w1-dispatch.json`: `counts.spawn=33`, `counts.total=33`,
`taskCall.tasks=33`; policy `waveMinLanes=32`, `waveMaxLanes=64`,
`hardCeiling=256`. Committed `w1/swarm-registry.json`: 33 members (object keyed
by seat name), mix identical to the LOG line 1480.

4. Census re-derived with the report's own awk program over committed blobs:

```
6c01a41 ROWS=73 A=67 B=1 C=5 mined=50 queued=19 rejected=4
d164f88 ROWS=74 A=68 B=1 C=5 mined=50 queued=19 rejected=5
HEAD    ROWS=74 A=68 B=1 C=5 mined=50 queued=19 rejected=5
```

Knowledge `.md` counts: `8c7c867=50`, `6ac1007=52`, `6c01a41=52`, `d164f88=53`.
On disk now: `ls corpus/knowledge/*.md | wc -l` → `53`;
`find corpus/evidence/round39/receipts -maxdepth 1 -type f -name '*.json' | wc -l` → `7`.

5. Append-only checks: `git diff 6c01a41 d164f88 -- corpus/evidence/round40/claims.md`
is `+5` lines (the `## Errata` block only). The r39 claims diff replaces
`None yet.` with the R1-R5 erratum block, body untouched. The SCORECARD diff is
`+8` lines. `git diff --stat 691d264 d164f88 -- corpus/evidence/round39/receipts/`
produced no output: no committed r39 receipt byte changed.

6. Pointer resolution by line read:
   - `corpus/SOURCES.md:69` = S059 row; its used-by cell is exactly
     `corpus/knowledge/revision-binding-r31.md, corpus/knowledge/receipt-expectation-digests-r40.md`.
   - `corpus/SOURCES.md:84` = S074 row, tier A, status `rejected`, with reason and flip.
   - `corpus/SOURCES.md:106-109` = coverage bullet + `## Search log` round-40 entry.
   - `corpus/README.md:1038,1059` = round-40 frontier paragraph and coverage row.
   - `corpus/evidence/round39/claims.md:197-200` = R2, R3, R4, R5 errata, in that order.
   - `fleet:.ufo/reports/round-39/chousa.md:132-133` = `29 → 31`; `:169-170` =
     `reviewer 6 / critic 5 / revenger 2` (32 seats).
   - `corpus/lessons/round-39-verifier-spotcheck.md:74` = `reviewer 8 / revenger 0`.
   - `corpus/lessons/round-40.md` `## Gate` exists with the S059 quote and S074 rejection.

7. `git show --stat --oneline 6bc90e0` → one new file,
`corpus/lessons/round-40-verifier-spotcheck.md` (+71). Commit time
`2026-10-24 04:15:00 -0300`; lane metadata `282dc76` was `04:08:45`; fleet report
commit `72ab899` was `04:13:07`.

## Findings

### F1 — "no non-author spot-check" is false at the lane's current tip (moderate; revision-scope)

Verbatim, three named documents:

- report `.ufo/reports/round-40/chousa.md:54`: "**discernment: unchanged** — the round's admitted/rejected sample has no non-author spot-check. No lane-dispatched seat is counted as independent review."
- `SCORECARD.md:2273`: "**discernment unchanged** — the round's admit/reject sample has no non-author spot-check yet."
- `LOG.md:1481`: "discernment unchanged pending a non-author admit/reject spot-check."
- `corpus/lessons/round-40.md:51`: "Pending an outside non-author review of at least one admit and one reject."

Against the lane tip:

- `corpus/lessons/round-40-verifier-spotcheck.md:49` (committed at `6bc90e0`, lane HEAD): "**discernment: improved** — this non-author spot-check agrees with the gate on both sampled admits and both sampled rejects (4/4 agreement, 0 disagreements)."
- The same file, line 5, names `lane tip 282dc76856b22747fc531f188df1718a8e18e99a`; line 12 records `git status --porcelain` empty and pushed.

The three named documents are mutually consistent; the inconsistency is against a
fourth committed lane artifact that postdates them. The report's revision claim is
also overtaken: report line 18 calls `282dc76856b22747fc531f188df1718a8e18e99a`
"(final lane tip)", while `git rev-parse HEAD` = `6bc90e04ac60307befacd554f7eee2b7284e2652`.

Effect on predicates: none. P1/P2 do not read discernment text. Effect on
calibration: the round's own record at HEAD contains two opposite discernment
verdicts. Resolution is append-only (erratum naming the spot-check and revising
"unchanged" to "improved per `corpus/lessons/round-40-verifier-spotcheck.md`", or
scoping the statements to `282dc76`); this seat made no edit.

Observation O1 (same root cause): the wave is now being dispatched by the host.
`git status --porcelain` shows ` M .ufo/waves/round-40/w1/swarm-registry.json`
and 14 untracked `w1/*.md` seat reports, including this seat. The report's
"not dispatched by this seat" (line 11) remains scoped-true; the spot-check's
"never dispatched" (item 1) is overtaken by execution.

### F2 — C2 claim says "not count prose labels alone"; R5 is prose-only (moderate; calibration)

`corpus/evidence/round40/claims.md:23`: "The counter must re-derive these states
from the committed evidence, not count prose labels alone."

Counter implementation:

- R3 re-derives (`c2-count.py:73-77`: `git ls-tree` counts at the two named r39 commits; observed 50 and 52).
- R4 re-derives (spec/plan role mixes; observed 6/2, 32 seats).
- R2 (`c2-count.py:61-63`) requires `git ls-files --error-unmatch` plus the substrings `"not committed"`, `"R2"`, `receipt`, `"superseded"`.
- R5 (`c2-count.py:81-83`) is four substring checks only: `"two independent runners"` and `"R5"` and `"two seeds"` in SCORECARD, `"L1's construction runs"` in r39 claims.

So two of four dispositions rest substantially on prose, and R5 has no structural
re-derivation. The claim sentence overstates the counter's method. P2 still passes
(`4/4` is the frozen condition); no document acknowledges the narrower R2/R5
mechanism. Suggested correction is append-only wording ("R3/R4 re-derived;
R2 checks trackedness and the correction text; R5 checks the corrected wording").

### F3 — R2 disposition cites the wrong lesson line (low; source pointer)

`corpus/evidence/round40/routed-defect-dispositions.json:7` cites
`"corpus/lessons/round-39.md:60"`. Line 60 reads: "c2 construction receipt and the
broken-shim mutant receipt were discarded as superseded drafting states, named in
`## Mistakes`." The assertion the R2 disposition rests on is line 27: "receipt
`c1-mutenv-s39003.json` (superseded, not committed)". The round-40 lesson itself
cites the correct span as `corpus/lessons/round-39.md:27,54-61`
(`corpus/lessons/round-40.md:18`). The counter passes because it tests the whole
file for `"not committed"`; only the citation is imprecise.

### F4 — C1 kill rule overstates what C2 dispositions cover (low; claim wording)

`corpus/evidence/round40/claims.md:19`: "The four superseded originals remain
outside the active population and are dispositioned under C2." The dispositions
record has exactly four keys, R2-R5, and only R2 names a receipt
(`c1-mutenv-s39003.json`). The other three originals —
`c1-base-s39001.json`, `c1-after-s39011.json`, `c1-mutenv-s39013.json` — are
superseded by regeneration and recorded in the r39 claims Erratum R1, not in C2.
`c2-count.py` reads no receipt (consistent with the stated separability). Suggested
wording: "three originals superseded under R1; the fourth dispositioned under R2."

### F5 — R5 replacement wording is not one phrase across the record (low; claim wording)

- report line 9: "R5's 'two independent runners' wording is corrected to **two L1 construction seeds**."
- disposition JSON R5 decision: "Replace ... with **two L1 construction seeds**."
- `LOG.md:1477`: "superseded by '**two seeds, both L1 construction runs**.'"
- `SCORECARD.md:2260`: "Correct wording: **two seeds, both L1 construction runs**."

Two paraphrase forms for a correction whose subject is wording. Semantically
equivalent; the canonical judge should read either as the same disposition, but a
single quoted replacement phrase would remove ambiguity.

### F6 — LOG range overhangs the entry (low; pointer)

Report line 18 cites `LOG.md:1472-1482`. The round-40 entry occupies lines
1472-1481; line 1482 is blank and no further `## ` heading exists in the file
(`awk 'NR>1472 && /^## /'` returned nothing). The cited content is correct except
the end line.

### F7 — "validated" wave: no committed transcript for the corrected bytes (low; inference flagged)

The frozen handoff `.ufo/waves/round-40/DISPATCH-README.md` (commit `6c01a41`)
records validator `plan` and `run` exit 0. Commit `d164f88` then edits
`w1-spec.json` (4 items: S074 → S059) and regenerates `w1-plan.json`,
`w1-dispatch.json`, `w1/swarm-registry.json` (4 items and 4 registry entries
changed). The report line 11 says "Prepared and validated one v1 wave under policy
v1: 33 distinct items"; `LOG.md:1478/1480` say "validated v1 wave evidence" /
"validated under policy v1". No validator stdout for the corrected bytes is
committed. The regenerated payloads are mutually consistent (33 items / 33 tasks /
33 spawn / 33 members, all names distinct, mix matches), so re-validation almost
certainly ran — `[INFERENCE]`, not observed. The report should either cite the
re-validation command/output or say validation applies to the freeze spec.

### F8 — frozen claims never record the after state (low; record completeness)

`corpus/evidence/round40/claims.md:17` still reads "**After.** Pending
re-derivation after all three replacements are committed." and line 31 reads
"**After.** Pending re-derivation after the disposition record, append-only
corrections, and scorecard text are committed." No appended erratum points to
`measure-after.txt`, although the file's own erratum mechanism was used for the
S059/S074 row. The after state lives only in `measure-after.txt`, the report
table, LOG 1475, and SCORECARD 2268-2269. Defensible reading: the body is frozen
and the after belongs elsewhere; but the frozen claims alone show no outcome, so
the completion is not discoverable from the claim record. A one-line append-only
erratum naming `measure-after.txt` would close it.



## Verified-consistent counts (no defect)

| Count | Value | Where stated | Independent check |
|---|---|---|---|
| C1 active receipts | 3/6 → 6/6, exit 1 → 0 | claims 15 (before) and 17 ("Pending"); control; measure-after; LOG 1474-1475; SCORECARD 2268; report table | committed control/after text read; 6 manifest rows; 6 `ok` lines |
| C2 dispositions | 0/4 → 4/4, exit 1 → 0 | claims 29 (before) and 31 ("Pending"); control; measure-after; LOG 1474-1475; SCORECARD 2269; report table | committed control/after text read |
| Active population | 6 distinct receipts | manifest; c1-count `EXPECTED_ACTIVE=6` | `wc -l` data rows = 6 |
| r39 receipt dir | 7 JSON = 6 active + 1 superseded | LOG 1476-1477; lesson 18; SCORECARD 2257; measure-after | `find ... | wc -l` = 7 |
| r39 role mix | reviewer 6, revenger 2, 32 seats | claims 199; dispositions R4; report 9; LOG 1477; lesson 29 | jq: spec 32, plan 32, both 6/2 |
| contrary spot-check | reviewer 8 / revenger 0 | report 9; LOG 1477; lesson 29; dispositions R4 | `round-39-verifier-spotcheck.md:74` verbatim |
| round-40 wave | 33 items / 33 tasks / 33 spawn / 33 members | report 11; LOG 1480; DISPATCH-README | jq on committed spec/plan/dispatch/registry |
| registry rows | 73 → 74; A 67→68, B 1, C 5; mined 50, queued 19, rejected 4→5 | report; LOG 1479; lesson; measure-after | awk at `6c01a41` and `d164f88` (above) |
| knowledge files | 52 → 53 | report; LOG 1479; lesson; measure-after | `git ls-tree` per commit: 52, 53 |
| R3 historical count | 50 → 52 | claims 198; dispositions R3; SCORECARD 2258; report 9; LOG 1477 | `git ls-tree`: `8c7c867`=50, `6ac1007`=52 |
| source pointers | S059 used-by both notes; S074 rejected | report "Sources & frontier"; LOG 1479 | SOURCES.md:69,84,106-109; README:1038,1059 read |
| append-only | claims40 +5; r39 claims erratum appended; SCORECARD +8 | report 16-17; claims erratum | `git diff 6c01a41 d164f88` |
| originals untouched | 0 r39 receipt bytes changed | report 8; claims 19; r1-stale-before | `git diff --stat 691d264 d164f88 -- corpus/evidence/round39/receipts/` empty |

## Verbatim conflicts for the canonical Rust judge

1. Discernment, same round, same lane:
   - `report:54` + `SCORECARD.md:2273` + `LOG.md:1481`: no non-author spot-check / "unchanged".
   - `corpus/lessons/round-40-verifier-spotcheck.md:49`: "discernment: improved ... (4/4 agreement, 0 disagreements)".
2. Lane tip: `report:18` "(final lane tip)" = `282dc768...`; `git rev-parse HEAD` = `6bc90e04ac60307befacd554f7eee2b7284e2652`.
3. R5 replacement phrase: "two L1 construction seeds" (report 9, dispositions R5) vs "two seeds, both L1 construction runs" (LOG 1477, SCORECARD 2260, lesson 20).
4. C2 method: claims.md 23 "not count prose labels alone" vs `c2-count.py:81-83` (R5 substring checks only).
5. R2 source: dispositions R2 `round-39.md:60` vs `round-39.md:27` (the "not committed" line).

No resolution was applied; this seat is read-only.

## Touched surfaces

- Wrote: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/w1/ScribeClaimSurfaces.md` (this file).
- Read-only: lane repo files and git objects; `/home/vgpnk/Projects/shokunin/.ufo/reports/round-40/chousa.md` and its fleet git history.
- Observed, not mine, untouched: ` M .ufo/waves/round-40/w1/swarm-registry.json`; untracked `w1/*.md` seat reports; `?? .ufo/waves/round-41/`; `?? corpus/evidence/round41/`; fleet ` M .ufo/state/chousa.report-baseline`.

## Out of scope / not performed

- No execution of `c1-count.py` or `c2-count.py` (execution seats own that; this seat would otherwise duplicate their runs).
- No production edit, no git/jj index or state change, no commit/push.
- No external fetch; no live target.
- No re-litigation of R4's source bytes beyond reading the committed spec, plan, report, and spot-check.
- No QUALITY.md criterion scoring.

## Gate

- Read-only boundary held: one write, to the assigned report path.
- No tool installs; no pacman transaction attempted (`pacman` is host-paused).
- Exact-command audit: every command above ran in the lane root or with `-C` naming the repo; outputs quoted are the observed outputs, with long JSON reduced to the relevant fields.

## Artifact pointers

- Frozen claims: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/claims.md`
- Controls: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/controls/control-before.txt`, `.../r1-stale-before.txt`
- After-measurement: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/measure-after.txt`
- Dispositions: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/routed-defect-dispositions.json`
- Round-40 report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-40/chousa.md` (fleet commit `72ab899bfbd3bfb226c1d21de2536de52368b586`)
- Round-40 lesson: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-40.md`
- Non-author spot-check: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-40-verifier-spotcheck.md` (lane commit `6bc90e04ac60307befacd554f7eee2b7284e2652`)
- Wave payloads: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/w1-spec.json`, `w1-plan.json`, `w1-dispatch.json`, `w1/swarm-registry.json`
