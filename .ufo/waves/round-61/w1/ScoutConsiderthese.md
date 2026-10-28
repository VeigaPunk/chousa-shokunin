# ScoutConsiderthese — round 61 w1

Seat leaf. Read `corpus/evidence/round61/claims.md` (C1 span-builder output safety, C2 derived-output safety). No frozen predicate, counter, control, `tools/`, `corpus/`, or `SKILL.md` edit. No install. No scratch tree.

## Findings

Recommend **Watch SKILL.md size (~420 lines, mostly prose logs); consider a distillation pass back into decision tables** (`considerthese/2026-10-19.md`, bullet under Self-improvement proposals; ledger id `CT-20261019-4`). It is the only lane proposal the ledger still marks `OPEN`. This round can land the distillation half as a lesson plus a `QUALITY.md` criterion. It does not widen frozen C1 or C2.

The size-watch half stays unnamed. The ledger note is `no threshold agreed`. Rounds 55 and 56 left the row open for that reason. Do not invent a line-count kill.

What to distill, from the file opened this seat: `SKILL.md` is 748 lines. `## Gates` begins at line 76. The `verify-metadata` row at line 86 is `verify-metadata <entry-or-dir> --root .` and does not mention `--as-of`. The only `--as-of` hits are lines 546 and 559, inside `## Round26 metadata options and resource qualification` (line 539), which continues through `### Round 37` (line 721). That block already holds a decision table (lines 557–562: `--as-of`, `META_RECHECK_OVERDUE`, `--registry`, and the four warn ids, sourced to `corpus/knowledge/recheck-due-r26.md` and `registry-link-r26.md`). Later headings in the same tail are status corrections (Round26 recovery, Round27, Round28, Round 35, Round 36, Round 37). A distillation promotes those decision rows onto `## Gates` (or `## Decision table`) and leaves each status correction as a pointer to its owning lesson or knowledge file. Unique limits stay; they move with a pointer.

A check that fails on today's tree and passes after that move: `grep -n -- '--as-of' SKILL.md` prints only lines 546 and 559. After the move, `--as-of` appears on the `verify-metadata` Gates row (before line 539) and `## Round26 metadata options` is gone or reduced to a pointer. Cite `considerthese/2026-10-19.md` and the date 2026-10-19 on the criterion.

Latest file `considerthese/2026-10-26.md` has four proposals. Three are already lane artefacts. The fourth cannot be a lane artefact. Older files 2026-10-20 through 2026-10-25 were read; their bullets are ledger rows `CT-20261020-1` through `CT-20261025-4` (`IMPL`, `FMT`, or `OPS`).

## Rejected

1. **Give my proposals stable ids** (`considerthese/2026-10-26.md:41`, `CT-20261026-1`). Implemented as `corpus/evidence/round54/considerthese-ledger.tsv` plus `corpus/evidence/round55/considerthese-ledger-check.py`. This seat's run printed `PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0`, exit 0. `corpus/lessons/round-57.md:79-86` records a positional rebind (reordering a bullet rebinds an id and the check still exits 0) and dispositions it as an implemented proposal with a surviving identity weakness, explicitly not an unimplemented feature. Rounds 59 and 60 repeat that disposition (`round-59.md:37`, `round-60.md:19`).

2. **Do one independent CJK quote spot-check per review** (`considerthese/2026-10-26.md:44`, `CT-20261026-4`). Ledger status `FMT`. `corpus/lessons/round-58.md:39` carries it: the proposal requires a reader this lane did not dispatch, and a same-lane seat would not be that reader. Flip named there: a non-author review records one CJK quote/claim comparison.

Also already landed, so not the pick: recurring-weakness streaks (`corpus/evidence/round53/weakness-streak.py`, `corpus/evidence/round55/recurring.tsv` RW-1 claimed streak 7) and lane-vs-verifier gaps (`corpus/evidence/round52/verdict-gap.py`). `CT-20261022-2` (admission streaks, seats, wall time, cost per gain) is `OPS`; `PROVINCE.md` sends orchestration to kumitate.

## Evidence

```
python3 -B corpus/evidence/round55/considerthese-ledger-check.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0
EXIT:0
```

Ledger open row (`corpus/evidence/round54/considerthese-ledger.tsv:5`):

```
CT-20261019-4	OPEN	-	SKILL.md size; wc -l = 741; no threshold agreed
```

```
wc -l SKILL.md
748 SKILL.md
```

```
grep -nE 'distillation pass|SKILL.md size|prose logs' corpus/QUALITY.md
```

Exit 1, no output. A wider `grep -rnE 'distill|SKILL.md size|CT-20261019-4' corpus/QUALITY.md corpus/lessons SKILL.md SCORECARD.md LOG.md corpus/evidence/round54/considerthese-ledger.tsv` hits the ledger row, `corpus/lessons/round-55.md:77` (left open), and unrelated `distiller` seat notes. No QUALITY criterion names this distillation.

```
grep -n -- '--as-of' SKILL.md
546:  --as-of 2026-10-21 --registry corpus/SOURCES.md
559:| `--as-of YYYY-MM-DD` | Add `due=` and `freshness=` ...
```

Exit 0. Gates row observed at `SKILL.md:86` (command has `--root .` and no `--as-of`). Headings at and after line 539: `## Round26 metadata options and resource qualification`, `### Round26 recovery safety/status correction`, `### Round27 repair/status correction`, `### Round28 DERIVED honest-negative status`, `### Round 35`, `### Round 36`, `### Round 37`. Line 544 `# cwd:` is inside a fenced shell snippet.

Files read: `considerthese/2026-10-19.md` through `2026-10-26.md`; ledger tsv; round-55 checker; `SKILL.md` gates row and the Round26 block; `corpus/lessons/round-57.md:77-86`, `round-58.md:39`, `round-55.md` considerthese section (via grep), `round-59.md:37`, `round-60.md:19`; `corpus/evidence/round55/recurring.tsv`; `.ufo/waves/round-51/w1/R51ScoutConsiderthese.md` (its own tally line is 19 implemented, 9 reflection-format, 3 open; this seat counted the same table as 19/9/3). `R51W2ReviewLesson.md` D12, cited by round 58, was not opened.

VERDICT: RECOMMENDED=Watch SKILL.md size (~420 lines, mostly prose logs); consider a distillation pass back into decision tables implemented_check=grep -nE 'distillation pass|SKILL.md size|prose logs' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/QUALITY.md
