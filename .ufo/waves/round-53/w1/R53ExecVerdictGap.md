# R53ExecVerdictGap — verdict-gap follow-through (proposal 3)

Seat R53ExecVerdictGap (executor, leaf). No subagents, no background jobs, no installs (pacman is
host-wide paused; `bash`, `python3`, `diff` sufficed). Lane read-only; my only write is this report.
Scratch `/fast/scratch/hyaku/chousa-r53/R53ExecVerdictGap` removed at the end; no git/jj mutation, no network.

## 1. The run as asked (observed, TMPDIR set to scratch)

```
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round52/verdict-gap.py --from 40 --to 52
R40 MISSING scorecard=False verifier=True
R41 MISSING scorecard=False verifier=True
R42 axes lane=6 verifier=6
R43 UNPARSED lane_axes=6 verifier_axes=0
R44 axes lane=6 verifier=6
R45 UNPARSED lane_axes=6 verifier_axes=0
R46 axes lane=6 verifier=6
R47 operability: lane=improved verifier=harmed
R47 axes lane=6 verifier=6
R48 UNPARSED lane_axes=6 verifier_axes=0
R49 axes lane=6 verifier=6
R50 calibration: lane=improved verifier=unchanged
R50 axes lane=6 verifier=6
R51 axes lane=6 verifier=6
R52 axes lane=6 verifier=6
VERDICT_GAPS=2 UNPARSED=5
exit=1
```

## 2. Premise check — R48 does not write its six axes as bullets

`corpus/lessons/round-48-verifier-spotcheck.md:70` is `## Trend verdicts (closure, non-author)`;
its three direction bullets (`:72`–`:74`) are `- **expansion — unchanged.**`, `- **quality —
unchanged.**`, `- **discernment — unchanged.**` — the trend vocabulary, **not** the six axes. R48's
six-axis grades are prose only: `:35` "per-axis table marks calibration/depth/coverage/freshness/
adjacency unchanged … No owned axis harmed" and `:48` "the claim's own 'improved narrowly / no
general-precision claim' framing is the right cap and is kept". So `R48 UNPARSED` is an **axis-
vocabulary absence, not a bullet-form failure**, and the docstring's "round 48 writes its axes as
bullets" is false. Six-axis bullets are **R43**'s (`round-43-verifier-spotcheck.md:112`–`:114`;
`coverage: improved` … `freshness: unchanged` … `adjacency: unchanged`); R45 writes trend bullets
(`:40`–`:42`) and restates the six axes in prose at `:27`.

## 3. The extension, intended lane path `corpus/evidence/round53/verdict-gap.py`

A round-53 successor, not an in-place edit: round-52 W2 receipts quote the round-52 file's output
(`R48 UNPARSED lane_axes=6 verifier_axes=0`), which editing it would falsify. Integrate as `cp
corpus/evidence/round52/verdict-gap.py corpus/evidence/round53/verdict-gap.py` + the diff below
(patch on a copy → `cmp` with the file I ran → `DIFF_APPLIES=identical`):

```
--- corpus/evidence/round52/verdict-gap.py
+++ corpus/evidence/round53/verdict-gap.py
@@ -4,13 +4,22 @@
 `R52ScoutConsiderthese` prototype, made a lane check in round 52).
 
 For each round N in [--from, --to] it reads the first axis table of the
-`## Round N verdict` section of SCORECARD.md and the axis table of
-`corpus/lessons/round-N-verifier-spotcheck.md` (rows `| <axis> | <verdict> |`),
-takes each cell's direction (the first of improved / unchanged / harmed /
-regress; qualifiers such as "narrowly" are dropped) and prints one line per
-axis whose two directions differ. A round whose verifier file holds no axis
-row in that table shape (round 48 writes its axes as bullets) prints
-`R<N> UNPARSED` and is not compared — it is not counted as agreement.
+`## Round N verdict` section of SCORECARD.md and the axis rows of
+`corpus/lessons/round-N-verifier-spotcheck.md`, takes each cell's direction (the
+first of improved / unchanged / harmed / regress; qualifiers such as "narrowly"
+are dropped) and prints one line per axis whose two directions differ.
+
+ROUND-53 EXTENSION: the verifier file may write its verdicts as
+bullets instead of table rows — `- **<axis>: <direction>.**` (round 43) and
+`- **<axis> — <direction>.**` (rounds 45, 48). A bullet counts only when the
+bold label starts with ONE lower-case axis token, the separator (`: ` or ` — `)
+follows it immediately and the direction is the next word, so prose that merely
+mentions an axis is not read, a multi-axis label is not read and a qualified
+direction (`improved narrowly`) is not read (fail-closed: the round is reported,
+not silently misgraded). Rounds whose verifier writes only the trend vocabulary
+(expansion / quality / discernment) are printed `AXES_ABSENT` with the labels it
+did write — they are not comparable on the six axes and are not counted as
+agreement.
 
 Usage: python3 corpus/evidence/round52/verdict-gap.py [--root LANE] --from N --to M
 Prints `VERDICT_GAPS=<gaps> UNPARSED=<rounds>`.
@@ -22,6 +31,7 @@
 import sys
 
 AX = ("operability", "depth", "calibration", "coverage", "freshness", "adjacency")
+BUL = re.compile(r"^- \*\*([a-z]+)(?:: | — )(improved|unchanged|harmed|regress)[.:]*\*\*")
 
 
 def dirn(s: str):
@@ -35,6 +45,10 @@
         m = re.match(r"^\|\s*(%s)\s*\|\s*(.*?)\s*\|" % "|".join(AX), line)
         if m and dirn(m.group(2)):
             out.setdefault(m.group(1), dirn(m.group(2)))
+            continue
+        b = BUL.match(line)
+        if b:
+            out.setdefault(b.group(1), b.group(2))
     return out
 
 
@@ -64,6 +78,10 @@
             print(f"R{n} UNPARSED lane_axes={len(lane)} verifier_axes={len(ver)}")
             unparsed += 1
             continue
+        if not any(x in ver for x in AX):
+            print(f"R{n} AXES_ABSENT verifier_labels={','.join(sorted(ver))} lane_axes={len(lane)}")
+            unparsed += 1
+            continue
         for ax in AX:
             if ax in lane and ax in ver and lane[ax] != ver[ax]:
                 print(f"R{n} {ax}: lane={lane[ax]} verifier={ver[ax]}")
```

Default `--root` still resolves to the lane at the new depth (`parents[3]`), checked at the intended
path in a pseudo root (`SCORECARD.md` a copy, `corpus/lessons` a symlink): `--from 43 --to 43` →
`R43 freshness: lane=improved verifier=unchanged`, `R43 axes lane=6 verifier=6`, `VERDICT_GAPS=1
UNPARSED=0`, rc 1.

## 4. Negative fixtures — the bullet form is read only where the axis is the label

Fixture root `fx/` (`## Round 99 verdict` table + `corpus/lessons/round-99-verifier-spotcheck.md`
with two positives and five negatives); the probe runs `BUL.match` on each line:

```
ACCEPT  ('coverage', 'improved')     R43 axis bullet, colon: - **coverage: improved.** One new mined row (S078)
ACCEPT  ('expansion', 'improved')    R43 trend bullet, colon: - **expansion: improved** — one new mined row (S078)
ACCEPT  ('expansion', 'improved')    R45 trend bullet, dash: - **expansion — improved.** Re-measured SOURCES census
ACCEPT  ('quality', 'unchanged')     R48 trend bullet, dash: - **quality — unchanged.** No knowledge entry re-admitted,
REJECT  -                            NEG prose sentence: The operability axis improved narrowly; depth improved too.
REJECT  -                            NEG label not an axis: - **Note — the operability axis improved narrowly.** See above.
REJECT  -                            NEG two axes in one label: - **calibration and coverage: improved.** One label.
REJECT  -                            NEG qualified direction: - **freshness: improved narrowly.** A qualifier.
ACCEPT  ('adjacency', 'unchanged')   NEG axis only in the tail: - **adjacency — unchanged.** Nothing absorbed; operability impro
REJECT  -                            NEG scorecard trends prose: Trends: expansion **unchanged**; quality **unchanged**; discernm
REJECT  -                            NEG quoted table row: | depth | **improved** | quoted inside prose |
tail-mention bullet parsed as: {'adjacency': 'unchanged'} (operability must be absent)
parsed real R48 verifier bullets: {'expansion': 'unchanged', 'quality': 'unchanged', 'discernment': 'unchanged'}
```

On `fx`: `R99 axes lane=6 verifier=3`, `VERDICT_GAPS=0 UNPARSED=0`, rc 0 — the `freshness: improved narrowly` and `calibration and coverage: improved` negatives were not read (either would have printed false gaps).

## 5. Re-run at the lane (observed)

```
$ python3 verdict-gap-bullets.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --from 40 --to 52
R40 MISSING scorecard=False verifier=True
R41 MISSING scorecard=False verifier=True
R42 axes lane=6 verifier=9
R43 freshness: lane=improved verifier=unchanged
R43 axes lane=6 verifier=6
R44 axes lane=6 verifier=9
R45 AXES_ABSENT verifier_labels=discernment,expansion,quality lane_axes=6
R46 axes lane=6 verifier=6
R47 operability: lane=improved verifier=harmed
R47 axes lane=6 verifier=9
R48 AXES_ABSENT verifier_labels=discernment,expansion,quality lane_axes=6
R49 axes lane=6 verifier=9
R50 calibration: lane=improved verifier=unchanged
R50 axes lane=6 verifier=9
R51 axes lane=6 verifier=9
R52 axes lane=6 verifier=9
VERDICT_GAPS=3 UNPARSED=4
```

`--from 46 --to 51` → `VERDICT_GAPS=2 UNPARSED=1` (R48 now `AXES_ABSENT`); `--from 51 --to 51` →
`VERDICT_GAPS=0 UNPARSED=0` rc 0. Gaps rise 2 → 3 because R43 freshness sat behind the bullet
blindness; `verifier=9` is the six-axis table plus three trend bullets. Dumping both dicts per
round by hand: **rounds 42–52 hold exactly three disagreements**, below.

## 6. VERDICT gaps and the lane's best reading

| round, axis | lane (SCORECARD) | verifier (spot-check) | reading |
|---|---|---|---|
| R43 freshness | `SCORECARD.md:2373` `**improved narrowly**` — "S078 opened from a committed capture, sha256 recorded; no fetch" | `round-43-verifier-spotcheck.md:113` `**unchanged**` — "The only open is a capture written the day before launch. No live surface was re-checked. … Routed below so the next scorecard does not repeat the inflation" | **overstatement — correct it.** Its own verifier routed it (`:159` "Next scorecard must not call a pre-round cache open a freshness improvement") and the lane complied from R44 on (`SCORECARD.md:2399` "The round-43 closure routed exactly this inflation; it is not counted as an improvement here") but never appended the correction. A first open of an old capture is not freshness. |
| R47 operability | `SCORECARD.md:2513` `**improved, disputed as a trade**` — "zero exit changes on the lane's 63 entries … Reported for the operator to rule, not resolved here" | `round-47-verifier-spotcheck.md:35` `**harmed**` (trade; 2–3/12 false refusals, 8/12 misses, 5/7 mutants survive); ruling `:29` "The frozen predicate verifies; the axis move does not." | **disagreement the lane keeps, reason stated — no grade change.** The reason is already in the cell (capability real, zero exit changes on 63 committed entries, harm only on held-out synthetic text); the lane's own W2 seats logged the trade, and R51/R52 scouts record it as open with no ruling (`.ufo/waves/round-51/w1/R51ScoutConsiderthese.md:47` "still open … no ruling recorded"; `.ufo/waves/round-52/w1/R52ScoutConsiderthese.md:10` "OPEN, operator-owned … Not a lane artefact"). Regrading would pre-empt the operator; what is owed is a disposition line in `corpus/lessons/round-53.md`. |
| R50 calibration | `SCORECARD.md:2607` `**improved narrowly**` — "stale counts corrected and checked … report-before-WAVE-DONE defect is not repeated" | `round-50-verifier-spotcheck.md:59` `unchanged` — "the lane's stale-count correction is real … but no calibration claim was declared and the registry row's revision gap (defect c) keeps it from a verdict beyond unchanged" | **overstatement — correct it.** `corpus/evidence/round50/claims.md` froze only `R50-C1` and `R50-C2` (`:18`, `:50`): no calibration claim existed to grade. The revision gap is defect (c) (`:23`, routed `:90`, repaired only in R51). Hygiene the lane did do is not a measured axis claim. |

Draft for the L1 (append-only at the end of `SCORECARD.md`, so `:2373`/`:2607` stay valid, no row edited):

```
## Round 53 verdict corrections (append-only; no row above is edited)

R53 closes the two grade gaps the round-52 check prints as overstatements (round 43 freshness,
hidden until R53 by the bullet-form blindness; round 50 calibration); round 47 operability stays a
stated disagreement under the operator's open ruling and is not regraded.

grade-correction: SCORECARD.md:2373 freshness improved narrowly -> unchanged (corpus/lessons/round-43-verifier-spotcheck.md:113)
grade-correction: SCORECARD.md:2607 calibration improved narrowly -> unchanged (corpus/lessons/round-50-verifier-spotcheck.md:59)
```

Tested inert: with the block appended to a copy of `SCORECARD.md`, the round-53 check prints a
byte-identical 17-line report (`cmp a.txt b.txt` equal, `VERDICT_GAPS=3 UNPARSED=4`), and the four
existing `correction:` keys are untouched (`ANCHORED=0/4`). **Prefix hazard (new):** a grade
correction under the bare `correction:` prefix is read as a pointer redirect by
`corpus/evidence/round51/c3-count.py:41` (`^correction: SCORECARD\.md:(\d+) (\S+) -> (\S+)`) and by
the proposed round-52 `pointer-anchor-check.py` when the old grade is one token. Observed on copies:

```
A multi-token from                         HEAD=no  CORR=no
B two-token from                           HEAD=yes CORR=yes
G grade-correction prefix                  HEAD=no  CORR=no
UNANCHORED SCORECARD.md:2373 freshness -> unchanged anchor=None      # with form B; other four lines are the historical keys
ANCHORED=0/5
```

## 7. Residual limits

- R40/R41 stay `MISSING`: no `## Round 40/41 verdict` section exists though both verifier files carry
  axis tables; unchanged behaviour, nothing invented.
- A qualified bullet (`- **freshness: improved narrowly.**`) is fail-closed unread (reported, not
  silently dropped); no current verifier file uses that shape (11 direction bullets across
  R43/R45/R48, all exact single words). `dirn()` is untouched: `'not harmed'` → `harmed`
  (negation-blind, latent; round-52 W2 found it).
- The trend layer is read for labels, not compared: the only lane/verifier difference there is the
  lane's conditional `discernment unchanged pending a non-author spot-check`, which the verifier
  upgrades by performing it — no correction owed. The check still compares one direction word per
  axis, against the previous round's verifier file, not a held-out one.

VERDICT: extended the verdict-gap parser in scratch (R43 freshness surfaced, gaps 2 → 3; R45/R48 reclassified `AXES_ABSENT` because the round-48 verifier writes trend bullets, not the six axes) with five negative fixtures rejected, and ruled the three real gaps — R43 freshness and R50 calibration are lane overstatements owed an append-only `grade-correction:` line, R47 operability is a disagreement the lane keeps with its stated reason under the operator's open ruling.
