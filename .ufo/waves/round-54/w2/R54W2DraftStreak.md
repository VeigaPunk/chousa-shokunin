# R54W2DraftStreak — round-54 recurring-weakness table (scribe)

seat: `R54W2DraftStreak` (scribe, leaf; no dispatch)
date: 2026-10-26
lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`, observed `HEAD=178667dc2c9d1656e864abfdc251c68757428613`
(the L1 integration is `447cf7ed4dc1a3708518b99e9a5e62e177c11ce9` under it)
task: extend `corpus/evidence/round53/recurring.tsv` to round 54, re-run `weakness-streak.py`,
answer whether the script needs a code change to read a round-54 table.
writes: this report only. The table draft is the fenced block labelled
`corpus/evidence/round54/recurring.tsv`; nothing was written to the lane.

## Behaviour

Read: round-53 table (`sha256 060400a4e791748e52580d50348e0531b333aa64eb72b1ef5f90543ff16aaf62`),
`weakness-streak.py` (`sha256 5915b632eff0b3d1b852680c1676d5fc4b4d4efda17982cdac847d0fd901ef1c`),
round-54 lesson (`sha256 df3f0f780c9479991eb90dda81cc617e80124436005b043bc4aa7de2c28cc33b`),
the round-54 forge receipt and supplement (`sha256 bf73f1ebeabf642f8004b0e1303970b2160b4db8cc11a65fbe9479a5cb16384f`),
the forge builder (`sha256 9293b0dd88728d03cbf94c4a9a1ab2486978dc10854718d5d3ce0f7a7529cab1`),
and `measure-after.txt`. All commands ran with `PYTHONDONTWRITEBYTECODE=1`, cwd the lane root,
scratch under `/fast/scratch/hyaku/chousa-r54/R54W2DraftStreak/` (removed at the end).

## 1. The round-53 table is already stale (baseline, pasted)

```
$ python3 corpus/evidence/round53/weakness-streak.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin \
    --table /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round53/recurring.tsv
FAIL RW-1 streak=6 claimed=5 first_in_run=49 routed=corpus/evidence/round53/c1-supplement.py frozen counter forgeable
FAIL RW-3 streak=0 claimed=2 first_in_run=- routed=- stray write outside scratch
WEAKNESS_ROWS=2 FAILING=2
EXIT=1
```

The round-53 table is a snapshot: `corpus/lessons/round-54.md` now exists, so the script's
"newest round" moved and the claimed 5 / 2 no longer match. This is expected, not a regression
in the lane — but it means a table is only green while its own round is the newest.

RW-1 grounds per round 49–54: `grep -o -i -E '.{30}forg(e|ed|able|ery).{30}'` over
`corpus/lessons/round-{49..54}*.md` returns the frozen-counter class in every round
(e.g. `round-49.md:21` replay-of-outputs, `round-53.md:19` "forgeable frozen counter, fifth round
running", `round-54.md:17` "forgeable frozen capability counter, sixth round running (RW-1)").
RW-3 does not match `round-54.md` at all (`grep -i -E 'relative redirect|fleet root|misroot|fleet-root'`
→ exit 1), so its consecutive streak from the newest round is 0.

## 2. Round-54 table draft

```tsv (intended lane path: corpus/evidence/round54/recurring.tsv)
RW-1	frozen counter forgeable	forg(e|ed|able|ery)	corpus/evidence/round54/c1-supplement.py	6
RW-3	stray write outside scratch	relative redirect|fleet root|misroot|fleet-root	-	0
```

Same five columns, same ids, labels and regexes as round 53 (changing the regex would rewrite the
recorded streak). Only the `routed` cell of RW-1 moved to this round's mitigation
(`corpus/evidence/round54/c1-supplement.py`) and the claimed streaks are re-derived. Tabs proven on
the scratch copy with `cat -A`:

```
RW-1^Ifrozen counter forgeable^Iforg(e|ed|able|ery)^Icorpus/evidence/round54/c1-supplement.py^I6
RW-3^Istray write outside scratch^Irelative redirect|fleet root|misroot|fleet-root^I-^I0
```

Why RW-1 = 6: `corpus/lessons/round-54.md:17` names the class as the sixth consecutive round and
records W1 `R54CritForgeC1` passing four `LEGS=6/6` runs. The receipt
`corpus/evidence/round54/controls/c1-forge.txt` shows the rebuilt forge scoring
`LEGS=6/6` / `C1=PASS` on `--seed 7` and one unseeded run while the supplement scores
`SUPPLEMENT_LEGS=0/3`; `measure-after.txt:53` shows the candidate at `SUPPLEMENT_LEGS=3/3`.
The routed path exists (`sha256 bf73f1eb…`, 175 lines). I did not rerun the forge; these are the
receipt's observed lines, not my measurement.

## 3. Script run on the scratch copy (pasted)

```
$ python3 corpus/evidence/round53/weakness-streak.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin \
    --table /fast/scratch/hyaku/chousa-r54/R54W2DraftStreak/recurring.tsv
OK   RW-1 streak=6 claimed=6 first_in_run=49 routed=corpus/evidence/round54/c1-supplement.py frozen counter forgeable
OK   RW-3 streak=0 claimed=0 first_in_run=- routed=- stray write outside scratch
WEAKNESS_ROWS=2 FAILING=0
EXIT=0
```

## 4. Does the script need a code change to read a round-54 table?

No, to read one today: `--table` is a plain path (`pathlib.Path(a.table)`) and the script derives the
rounds from `<root>/corpus/lessons/round-*.md`, so a table outside round53 was read unmodified
above, exit 0. The only round-53 coupling is the docstring sentence "Reads
corpus/evidence/round53/recurring.tsv" and the tool's own location; neither is functional.

Yes, if a round-54 table must stay re-checkable after round 55 lands. Fixture: a scratch root
holding the real lessons plus a synthetic `round-55.md` containing "forgeable", same table:

```
$ python3 corpus/evidence/round53/weakness-streak.py --root $S/asof-root --table $S/recurring.tsv
FAIL RW-1 streak=7 claimed=6 first_in_run=49 routed=corpus/evidence/round54/c1-supplement.py frozen counter forgeable
OK   RW-3 streak=0 claimed=0 first_in_run=- routed=- stray write outside scratch
WEAKNESS_ROWS=2 FAILING=1
EXIT=1
```

Draft (NOT applied; intended lane path `corpus/evidence/round53/weakness-streak.py`, two added lines
plus a docstring word):

```diff
--- corpus/evidence/round53/weakness-streak.py
+++ corpus/evidence/round53/weakness-streak.py
@@ -5,7 +5,7 @@
-"""weakness-streak — consecutive rounds a recurring weakness is named in the lane's own round record
-(considerthese 2026-10-26, proposal 2). Reads corpus/evidence/round53/recurring.tsv:
+"""weakness-streak — consecutive rounds a recurring weakness is named in the lane's own round record
+(considerthese 2026-10-26, proposal 2). Reads a per-round recurring.tsv:
@@
-ap = argparse.ArgumentParser(); ap.add_argument("--root", default="."); ap.add_argument("--table", required=True)
+ap = argparse.ArgumentParser(); ap.add_argument("--root", default="."); ap.add_argument("--table", required=True); ap.add_argument("--as-of", type=int)
@@
-rounds = sorted(int(m.group(1)) for p in les.glob("round-*.md") if (m := re.fullmatch(r"round-(\d+)\.md", p.name)))
+rounds = sorted(int(m.group(1)) for p in les.glob("round-*.md") if (m := re.fullmatch(r"round-(\d+)\.md", p.name)))
+if a.as_of is not None: rounds = [n for n in rounds if n <= a.as_of]
```

Run of that draft on a scratch copy, against the same round-55 fixture:

```
$ python3 $S/weakness-streak-asof.py --root $S/asof-root --table $S/recurring.tsv --as-of 54
OK   RW-1 streak=6 claimed=6 first_in_run=49 routed=corpus/evidence/round54/c1-supplement.py frozen counter forgeable
OK   RW-3 streak=0 claimed=0 first_in_run=- routed=- stray write outside scratch
WEAKNESS_ROWS=2 FAILING=0
EXIT=0
```

Without the cap the historical table fails after the next round; with it the table pins its own
round. The cap adds no rule, predicate or target to any claim counter.

## Gates

| gate | how | observed |
|---|---|---|
| draft read by the unmodified script | §3 command | `FAILING=0`, exit 0 |
| draft columns/labels/regex preserved | `cat -A` on scratch copy | five tab-separated cells per row, ids/regexes byte-equal to round 53 |
| routed path exists (streak ≥ 3 rule) | `sha256sum corpus/evidence/round54/c1-supplement.py` | file exists, 175 lines |
| round-54 name for RW-1 | `corpus/lessons/round-54.md:17` | "sixth round running (RW-1)" |
| RW-3 absent this round | regex over `round-54.md` + `round-54-verifier-spotcheck.md` | no match (spotcheck file does not exist) |
| self-invalidation after a later round | §4 fixture | `FAIL RW-1 streak=7 claimed=6`, exit 1 |
| `--as-of` draft fixes it | §4 draft run | `FAILING=0`, exit 0 |

## Findings

1. **RW-1 recurs in round 54, streak 6** (rounds 49–54), routed to the post-freeze supplement. The
   lesson and receipt agree; the frozen counter is still forgeable (`LEGS=6/6`, `C1=PASS` for the
   rebuilt forge) and the supplement is the only thing that separates it (`SUPPLEMENT_LEGS=0/3`
   vs candidate `3/3`). Per the round-53 framing, the streak is exposure, not the C1 verdict.
2. **RW-3 breaks to 0.** Round 54's lesson does not name a stray-write incident. Note the round-53
   count of 2 was partly a negation: `corpus/lessons/round-53.md:30` reads
   "`| 6. Status-neutral strays | None this round at the fleet root or the lane root (misroot sweep …)`"
   and the regex counts it. The counter cannot distinguish a recurrence from its denial. I left the
   regex untouched (same columns, same meaning of the recorded streak) and record this as the
   table's named limit; a negation-aware rule would be a new table, not an extension of this one.
3. **A per-round table is a snapshot that self-invalidates** the moment the next lesson lands
   (§1 live, §4 fixture). Either the lane accepts that old tables exit 1, or the script gains
   `--as-of N`; the probe above shows the cap is sufficient and touches no claim rule.
4. **The script's round-53 coupling is documentation only.** `--table` accepts any path; the
   round list comes from the lesson directory. No change is required to read the round-54 table at
   its intended path (`corpus/evidence/round54/recurring.tsv`) under `--root` = lane root.
5. Small residual: the routed-path existence check only fires for streaks ≥ 3, so RW-3 at 0 is
   exempt from the dead-pointer guard. That is the script's existing rule and matches the round-53
   run; not changed here.

## Touched surfaces

- new: `.ufo/waves/round-54/w2/R54W2DraftStreak.md` (this report).
- lane production files: none written. The table draft and the patch are in this report.
- scratch `/fast/scratch/hyaku/chousa-r54/R54W2DraftStreak/` — created, used, removed.

## Out of scope

Claims, predicates, targets, counters, controls, QUARANTINE, QUALITY rows, SCORECARD/LOG/lesson
edits, other seats' reports, git/jj state, network. The recurring table is an evidence index; no
claim verdict is asserted from it.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round53/recurring.tsv`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round53/weakness-streak.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/controls/c1-forge.txt`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/controls/build-c1-forge.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/c1-supplement.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/measure-after.txt`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-54.md:17`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-53.md:30`

VERDICT: attacked (a) the round-54 extension of the recurring table and (b) the script's ability to
read and re-check it — RW-1's streak of 6 survived on the lesson and the forge receipt, RW-3 broke
to 0, the unmodified script reads the round-54 table (exit 0) but a per-round table self-invalidates
after the next lesson, so an `--as-of` cap is needed only for historical re-checking, not to read it.
