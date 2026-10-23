# ScoutOperatorLessons — operator teachings, L0 queue answers, D1-D7 dispositions at base

Round 30, wave 1 build, scout seat. Base `a3a3710e3d0adf2f95882292f17b5093e3baf97c`.
Static read-only check: `git grep`, `git show`, `git ls-tree`, `git log` against the
base commit and the fleet repo; no counter, tool or fixture was executed. Paths are
relative to `/home/vgpnk/Projects/shokunin/chousa-shokunin`; `fleet:` prefixes
`/home/vgpnk/Projects/shokunin`.

## A. Operator teachings (`corpus/lessons/operator-*`): none

`fleet:LEARNING.md:50-53` fixes the contract slot: an operator teaching lands verbatim
as `corpus/lessons/operator-<YYYY-MM-DD>-<slug>.md` and the next round must reflect it
in `QUALITY.md` or `SKILL.md` (or report why not). Results:

| scope | command | result |
|---|---|---|
| base tree | `git ls-tree -r a3a3710e --name-only \| grep -i operator` | 1 row: `.ufo/waves/round-27/build/ScoutOperatorLessons.md` (a report, not a teaching) |
| lessons dir | read of `corpus/lessons/` | 21 `.md` files + `.gitkeep`; no `operator-*` |
| working tree glob | `corpus/lessons/operator-*.md` | no match |

**Verdict: no unreflected operator teaching exists.** The last same-name scout
(round 27) reached the same result.

## B. `fleet:.ufo/l0-questions.md` — chousa lines and operator answers

Five `chousa` rows; the file is append-only, 124 lines at mtime 2026-10-23 00:13.

- `:30` chousa round-1: operator-selected remote URL. Open; no answer on record.
- `:51` chousa round-12: receipt-identity acceptance model. Open; no answer on record.
- `:86` chousa round-27: frozen-C3 path vs prefix policy. Open; no answer on record.
- `:95` chousa round-29: repair-first recovery round after driver block.
  Answered by action: this round exists.
- `:121` chousa round-29 — **the fetch-scope question** ("Does the frontier duty to
  open registered sources … cover credential-free GET re-opens"). Committed at fleet
  `8d77e6c` (`git log --follow` on the queue). **Unanswered**: no answer block follows
  it; lines `:122-124` are dated block notices for kumitate, tsukuroi and tameshi
  (2026-10-23), not operator answers.

Operator-answer scan: `grep -n 'L0 ANSWER'` returns only `:52` and `:53` (both
2026-10-19, planner taxonomy). `tabi :77` carries "RESOLVED-BY-RULING (Main, in-session
orchestrator)" — an orchestrator ruling, not an operator answer, and it predates
2026-10-22 anyway. **No operator answer of any kind is recorded since 2026-10-22.**

Consequence for round 30: the fetch-scope ruling stays operator-owned; the lane's
stated mitigation (registered documentation pages only) remains the standing
boundary. D7 is correctly carried, not resolved.

## C. D1-D7 dispositions at base `a3a3710e`

Routed list: `corpus/lessons/round-29-verifier-spotcheck.md:141-163`.

| defect | routed repair | disposition at base | evidence |
|---|---|---|---|
| D1 liveness wording | add a candidate network observation to a new counter version, or cite `falsify/DiffToolB/landed-fixture.network.json` beside the row | **ABSENT** | "live" claims still stand unqualified at `corpus/evidence/round29/claims.md:29,41`, `SCORECARD.md:1635` (capabilities row), `corpus/knowledge/quote-reopen-r29.md:1`. A limit disclosure exists (`SCORECARD.md:1617-1620`, fleet report `:40`, `knowledge/quote-reopen-r29.md:107-112`) but no row cites the `network.json` receipt as liveness evidence. |
| D2 re-run count | append a dated correction | **ABSENT** | `SCORECARD.md:1603` and `fleet:.ufo/reports/round-29/chousa.md:36` say "6 further runs"/"6 more times"; `corpus/lessons/round-29-verifier-spotcheck.md:90,148-150` shows committed evidence holds 5 (`rederive3.out` records run 3, seed 3497534629407128034, not run 2 seed 12970099299958901445). `git grep -n 'correction'` at base over `SCORECARD.md`, `corpus/evidence/round29/claims.md`: no dated correction for this count. |
| D3 mutant survivors | add fixture classes before data: unreachable over-long item, head-only or script-only quote, case-only edit | **ABSENT at base; carried into round-30 design** | At base the three mutants still score 130 (`SCORECARD.md:1623-1624`; `falsify/MutOrder.md`, `MutSkipScript.md`, `MutCasefold.md`). `SCORECARD.md:1643-1646` plans them for round 30. Round-30 `corpus/evidence/round30/claims.md:118-127` (frozen design, post-base) does carry the classes: script windows, case flips and verdict-order items including TOO_LONG on an unreachable source. The falsify wave must re-apply the 3 mutants. |
| D4 h20 | append a dated correction to `lessons/round-25.md` | **ABSENT** | `corpus/lessons/round-25.md:70` still prints the sentence-cased quote dropping "However,"; `git grep 'However\|h20'` over that file at base: 0 hits. `corpus/lessons/round-29.md:63-64` marks the defect but is not a correction at the quote's location (spotcheck `:134-136` requires one). |
| D5 chronology wording | fix "before any data seat had run the counter"; disclose the v1 reference implementation (82/82) and the MutateCounter replays | **PARTIAL** | The frozen sentence stands at `corpus/evidence/round29/claims.md:13-14`. Disclosures exist beside it elsewhere: v1 scratch implementation at 82/82 in `claims.md:31-33`; MutateCounter replays (01:25:59–01:27:45 UTC, before the v3 freeze 01:28:23) in `corpus/lessons/round-29.md:104-108` and `falsify/CriticClaimDesign.md:28`. Still needed: the reworded sentence and both disclosures beside it, per spotcheck `:156-159`. |
| D6 uncommitted scratch | commit snapshot-control code and data (or hashes and paths) next to the CriticClaimDesign receipts | **ABSENT** | `git ls-tree a3a3710e .ufo/waves/round-29/falsify/CriticClaimDesign/` lists 7 files: `.md` + 6 JSON receipts/provenance. `offline_snapshot_control.py`, `network_guard.py`, `prepare_snapshots.py` and `snapshots.json` exist only as sha256 names in `CriticClaimDesign.md:94-96` pointing at volatile `/fast/scratch/hyaku/chousa-r29/w2/…` paths (`:53,64,73-74`). The zero-socket-event assertion is not auditable from the tree. |
| D7 carried, operator-owned | L0 fetch-scope (fleet `8d77e6c`), sentinels T1/T4, missing-`</head>` and 2xx-challenge limits | **CARRIED — active round-30 scope** | Queue row `fleet:.ufo/l0-questions.md:121` open (section B). T1/T4 open at `falsify/SentinelTool.md:17,20`, `SCORECARD.md:1625-1626`; missing-`</head>`/2xx limits at `SCORECARD.md:1628-1629`, `SKILL.md:66`, `corpus/QUALITY.md:174`. Round-30 `claims.md` maps C1 → missing-`</head>` and C2 → T1+T4. |

## D. Repair drafts for the build wave

- D1: cite `falsify/DiffToolB/landed-fixture.network.json` beside the SCORECARD
  capabilities row and the knowledge entry's limit paragraph as the recorded
  network observation; keep "live" only where such a receipt backs it.
- D2: dated append noting 5 committed re-runs (RerunCounterA 1, RerunCounterB 2,
  ScoutFreshnessH 2 with `rederive3.out` recording run 3), correcting the "6".
- D3: satisfied by the frozen round-30 fixture classes; falsify wave re-applies
  MutOrder, MutSkipScript and MutCasefold to the landed tool and commits receipts
  (round-30 claims.md:122-126 already schedules this — it is evidence, not a second
  predicate).
- D4: dated correction under `corpus/lessons/round-25.md` (append-only, do not edit
  `:70`): h20 is sentence-cased "A signal" and drops "However,"; the source sentence
  begins "However, a signal occurred…" per `falsify/ScoutFreshnessH.md:89`.
- D5: reworded chronology plus both disclosures beside the claims text (v1 reference
  82/82; MutateCounter replays 01:25:59–01:27:45 UTC), and the control-wave rule now
  in round-30 claims.md:90-92 (no control implements the full contract).
- D6: commit `offline_snapshot_control.py`, `network_guard.py`,
  `prepare_snapshots.py`, `snapshots.json` (or their sha256 plus committed paths)
  into `falsify/CriticClaimDesign/`. Blocker: the scratch copies at
  `/fast/scratch/hyaku/chousa-r29/w2/CriticClaimDesign/` may be reaped; the lane can
  regenerate an equivalent control or record the recorded sha256 set alone.
- D7: remains operator-owned; round 30 routes around the unanswered ruling exactly as
  the frozen claims do.

## Limits

I did not execute any counter, tool, seat script or network command. "Absent" means
no committed byte at base carries the routed repair; partial disclosures are marked
as such. Post-base round-30 commits (`f42906d`..`a0bc50b`) are cited only where they
show the defect is already scheduled, not as evidence of repair. Installs/updates:
none.
