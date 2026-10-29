# Round 62 w1 — ScoutConsiderthese (scout, seat ScoutConsiderthese-3)

Scope: mine `considerthese/` for ONE still-unimplemented proposal that could land this round as a lesson, QUALITY criterion or registry row. Read-only. No lane file written; scratch created and removed. Nothing under corpus/, tools/, SKILL.md or round-62 frozen evidence touched. The reflections are pointers; each candidate was checked against the lane.

## Findings

1. **Round 61's open half is still open.** `corpus/lessons/round-61.md:26` mined the distillation half of CT-20261019-4 and records the size-watch half as open ("no threshold agreed; no line-count kill was invented"). The ledger agrees: `corpus/evidence/round54/considerthese-ledger.tsv:5` reads `CT-20261019-4	OPEN	-	SKILL.md size; wc -l = 741; no threshold agreed`. It is the only OPEN row that is not operator-owned.

2. **The size watch is now measurably live.** The proposal (2026-10-19, `considerthese/2026-10-19.md:19`) says "~420 lines". The series below is from `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show <rev>:SKILL.md | wc -l`, sampled every eighth commit of `git log --format=%h -- SKILL.md`:

   | rev | date (-0300) | SKILL.md lines |
   |---|---|---|
   | 02a615a | 2026-10-14 21:18 | 53 |
   | 85eda51 | 2026-10-19 16:04 | 434 |
   | e17742f | 2026-10-19 10:24 | 432 |
   | 457fbb0 | 2026-10-21 15:27 | 549 |
   | 53cf649 | 2026-10-23 04:47 | 583 |
   | 8bc930a | 2026-10-23 16:23 | 591 |
   | 2738202 | 2026-10-25 06:59 | 712 |
   | 1fc5ed1 | 2026-10-25 09:02 | 729 |
   | 41b4dca | 2026-10-25 21:34 | 736 |
   | 2a5029e | 2026-10-28 20:05 | 753 |

   Working tree `wc -l < SKILL.md` = 753 (matches HEAD `d173d14`). Growth 434 → 753 in nine days (about +35 lines a day, sampled). The reflection's "~420" is off by 14 lines at its own date (INFERENCE: the reflection was written from memory, not measured). QUALITY has no criterion on SKILL.md size: `grep -n -i "distill\|size\|prose" corpus/QUALITY.md` lists only unrelated hits (digits, long-line normalization, SKILL-as-pointer checks).

3. **Recommended landing (measure-and-verify, no invented threshold).** Land a registry-style series plus a counter that can fail:
   - `corpus/evidence/round62/skill-size.tsv`: one row per round, columns round, rev, `SKILL.md` lines.
   - `corpus/evidence/round62/skill-size-watch.py --root .`: recomputes each row from `git show <rev>:SKILL.md | wc -l`, exits 1 on any mismatch or a missing row for a round that landed, prints `SIZE_WATCH=k/k` and the newest delta.
   - The threshold stays an operator decision: an L0 line in `.ufo/l0-questions.md` asking for the kill number. The watch is a recorded, checkable series; it never gates a round on a number nobody agreed.
   - Shown able to fail: plant a wrong count in a copy of the tsv under the scratch dir; the counter must exit 1. The L1 runs that control, not this seat.

4. **Distillation half: no further action this round.** `corpus/lessons/round-61.md:26` already moved `--as-of` options into a Gates row (`grep -n -- '--as-of' SKILL.md` first hits line 150). Its effect on size is not measured here: the promotion moved lines, the total is still 753.

## Candidates rejected

- **CT-20261022-2 (OPS, "seats / wall time / cost", `considerthese/2026-10-22.md:12`).** Rejected: out of province. `PROVINCE.md:9-12` refuses "orchestration, multi-agent dispatch and agent lifecycle (→ kumitate)". The ledger already marks it `OPS` (`considerthese-ledger.tsv`, row CT-20261022-2). The data it asks for is fleet-wide dispatch cost, not a lane artefact a lesson, criterion or row could count.
- **CT-20261026-4 (FMT, "independent CJK quote spot-check per review", `considerthese/2026-10-26.md:8`).** Rejected for this round: the proposal needs a reader outside the lane's dispatch, and no such reader is available (network and fleet-wide dispatch are closed to this round). A lane-internal version would be same-author, which `corpus/lessons/round-58.md:39` already declined and carried with its flip condition. Not re-opened.

## Sweep (how the candidate set was built)

- `python3 -B corpus/evidence/round54/considerthese-ledger-check.py --root .` (run from the lane root) → `PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0`, exit 0.
- Bullets listed across all eight `considerthese/2026-10-*.md` files by `awk`+`grep` on the proposal sections; every bullet maps to a ledger row (IMPL 24, FMT 9, OPEN 1, OPS 1). None is unledgered.
- `grep -rn -i "SKILL.md.*\(line\|size\|lines\)\|wc -l\|CT-20261019-4\|size-watch\|size watch" corpus/QUALITY.md corpus/lessons corpus/evidence tools SCORECARD.md LOG.md` — no implementation of the size watch found; the only hit naming CT-20261019-4 is the ledger row and `round-61.md:26`.
- `grep -rln -i "kumitate\|wall time\|CJK" corpus tools PROVINCE.md` — no lane artefact implements CT-20261022-2.

## Implementation check (must fail today, pass after landing)

`python3 -B corpus/evidence/round62/skill-size-watch.py --root .` — the file does not exist yet (expected: no such file, exit 2 today). It exits 0 only after the series and counter land.

## Verdict basis

Operability: the watch is a command the L1 can run and a counter that can be shown to fail. Coverage: it closes the one OPEN ledger row that is in province. Calibration: the reflection's "~420" is measured at 434 at its own date; the 753 figure is from git, not memory.

Commands run (read-only): `wc -l`, `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show <rev>:SKILL.md | wc -l` (ten revs above), `git log --format=%h -- SKILL.md`, `git rev-parse --short HEAD`, `git log -1 -- considerthese`, the ledger check, the greps above. Scratch dir created and removed; no file written in the lane.

VERDICT: RECOMMENDED=Watch SKILL.md size (~420 lines, mostly prose logs); consider a distillation pass back into decision tables implemented_check=python3 -B corpus/evidence/round62/skill-size-watch.py --root .
