# R53ExecAdopt — adopter v4 on the round-53 staged package

Leaf executor. Scratch `/fast/scratch/hyaku/chousa-r53/R53ExecAdopt` (removed). No install.
`tools/assimilate-rows.py` at lane tip `6365f15`, blob `50c2a2d9…c56d08dec6`, is the v4 candidate
(`32aab5e`; `HELD=`/`TWIN=` at line 574). Claims file read first; no predicate touched.

## 1. Run 1 — all three entries

```
$ python3 tools/assimilate-rows.py --staged …/merge/chousa/SOURCES.append.md --knowledge …/merge/chousa/knowledge \
  --registry corpus/SOURCES.md --opened 2026-10-26 --out $S/run1 --entry corpus/knowledge/search-tracking-record-r40.md \
  --entry corpus/knowledge/western-instrument-alignment-r50.md --entry corpus/knowledge/quality-control-guideline-issued-text-r48.md
EXIT=0   STDOUT: COLLISIONS=35 / CITED=6 APPEND=5 HELD=0 TWIN=1 / BODYONLY=3
STDERR: WARN …search-tracking-record-r40.md: body-only id S094 is also a lane id and reads as that row
        WARN …search-tracking-record-r40.md: body-only id S114 is also a lane id and reads as that row
FILES: append.md bodyclash.tsv bodyonly.tsv collisions corpus/ reg-ids renumber.tsv staged-ids stripped.tsv
renumber.tsv: S134->S117 append jmla.pitt.edu/ojs/jmla/article/download/1449/2061
              S185->S118 append www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf
              S186->S119 append m.bjhea.org.cn/35/202501/1126.html
              S190->S120 append pharmwyp.com/posts/56814/6.%E7%89%B9…2019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf
              S193->S121 append training.cochrane.org/handbook/current/chapter-04
              S195->S118 twin   www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf
bodyonly.tsv: search-tracking-record-r40.md S094 / S114 / S130   (3 rows)
bodyclash.tsv: search-tracking-record-r40.md S094, S114          (2 rows — both read as lane rows)
```

`append.md`: 5 rows × **11 cells**, lane-id order, sha256 `91a142292e7c7f661c8a762933d6a490987b4bbfdc3e87e2142204670f303ae2`.

```
S117 paper A mined 2026-10-26 365d used-by r40-search-tracking  | PRISMA 2020 and PRISMA-S: common questions…
S118 docs  B mined 2026-10-26 180d used-by r48-QCG, r50-western | 《药品临床综合评价质量控制指南（2024 年版 试行）》…
S119 docs  B mined 2026-10-26 180d used-by r48-QCG              | 《药品临床综合评价质量控制指南（2024年版 试行）》发布…
S120 docs  C mined 2026-10-26 180d used-by r48-QCG              | 关于发布上市药品临床安全性文献评价指导原则（试行）的通告…
S121 docs  A mined 2026-10-26 180d used-by r50-western          | Cochrane Handbook…, Chapter 4…
```

Cell diff vs the staged rows (all other cells byte-identical):

```
S117<-S134 id, opened 2026-10-23→2026-10-26, recheck prose→365d
S118<-S185 id, opened 10-24→10-26, recheck→180d, used-by widened (+r50 western)
S119<-S186 id, opened, recheck
S120<-S190 id, opened, recheck, used-by NARROWED (dropped corpus/knowledge/grey-literature-mandate-scope-r48.md)
S121<-S193 id, opened, recheck
```

`stripped.tsv`: 12 rows (5 recheck prose, 5 opened, S118 + S120 used-by), prose preserved verbatim,
e.g. `S117 recheck 365d — re-download the PDF and confirm the sentence still reads "PRISMA-S also
recommends reporting the number of records identified from each information source" (ran 2026-10-23)`.
No pipe rewrite occurred, so no title/scope cell was altered. Entry outputs land at
`run1/corpus/knowledge/<name>` with headers rewritten in place (`source: S117…`, `S121`,`S118`,
`S118/S119/S120`) and two body mentions S134→S117. Rerun reproduced every file and both streams
byte-identically (renumber `de2822…2553`, append `91a142…ae2`, stripped `f14b82…0379`).
## 2. Map vs the frozen expectation

**Equal, exactly**: S134→S117, S185→S118, S186→S119, S190→S120, S193→S121, S195→S118 `twin`, `HELD=0
TWIN=1` — the REAL-leg expectation; the base tool's S195 `held` mislabel is gone.
## 3. Run 2 — first two entries (no QCG entry)

```
EXIT=0  CITED=3 APPEND=3 HELD=0 TWIN=0 BODYONLY=3
S134->S117 append ; S193->S118 append ; S195->S119 append
```
Moved: S193 S121→**S118**, S195 twin@S118→**append S119**. Minting is contiguous over *cited* rows only in staged-id order; with S185/S186 uncited the QCG URL is minted by S195 itself.
## 4. Run 3 — QCG entry admitted, S190 refused

Scratch `--knowledge` tree `$S/know3` = the three entries with the single `source: S190 — …` line
deleted from the QCG entry (`grep -n S190` → line 4 only before, 0 after).

```
EXIT=0  CITED=5 APPEND=4 HELD=0 TWIN=1 BODYONLY=3
S134->S117 append ; S185->S118 append ; S186->S119 append ; S193->S120 append ; S195->S118 twin
```
Only **S193 moves S121→S120**; S190 gets no row, S195 stays twin. The adopter emits nothing about the refused document, so `refused-doc`/lesson traffic stays an L1 duty (C2's REFUSED leg).

## 5. Operability probes (scratch fixtures; real package untouched)

```
A) staged copy, S195 (twin) recheck = "whenever the mood takes us, no cadence here"
   EXIT=1  REFUSED S195: recheck 'whenever…' has no leading valid date or NNd
   out: collisions reg-ids staged-ids only — no renumber.tsv, no append.md        [C1 recheck ✓]
B) registry with `## Registry` renamed, run WITHOUT --entry
   EXIT=1  REFUSED registry has no `## Registry` heading
           REFUSED registry rows outside the Registry section: S001, …, S116      [no-entry gate ✓]
B0) sound registry, no --entry:  EXIT=0  COLLISIONS=35                             [✓]
C) stray `| S999 |` row outside Registry + a missing --entry
   EXIT=1  order: REFUSED registry rows outside the Registry section: S999
                  REFUSED entry missing: corpus/knowledge/no-such-entry.md         [registry first ✓]
D) non-existent --out dir: auto-created, EXIT=0    E) r40 alone: CITED=1 APPEND=1 S134->S117
```

## 6. Cells the L1 must still hand-normalise

1. `opened`, 5 rows: 2026-10-23/24 → `2026-10-26` (run date, not read date).
2. `recheck`, 5 rows: cadence kept, prose cut — the prose lives only in `stripped.tsv`; copy it to the Gate.
3. `used-by` S118 widened to both entries — correct per the twin limit; keep.
4. `used-by` S120 narrowed and stale: the staged cell named `corpus/knowledge/grey-literature-mandate-scope-r48.md`,
   which does not exist in the lane. No lane file names any of the five URLs (`grep -rln
   "pharmwyp\|chapter-04\|jmla\.pitt\|bjhea" corpus/knowledge corpus/SOURCES.md` → 0 hits), so `HELD=0` is genuine.
5. Body tokens in `search-tracking-record-r40.md` passed through: `S094`, `S114` (bodyclash — read as the wrong
   lane rows), `S130` (not a lane id, dangling), and `S069` — **no warning, since it is not in this staged file,
   yet lane `S069` is the GNU grep manual** (`corpus/SOURCES.md:79`). All four must be reworded, else C2's
   "no `S###` token except a bound id" leg fails.
6. `anchor` cells: zero `char N` (`grep -c 'char ' append.md` → 0), but C2 needs ≥1 per bound row, each an offset
   of a quote of that id (`c2-count.py:234-238`, `anchors == nbound`) — L1 injects them from `build-spans.py`;
   this reproduces the TOOLED control's `ANCHOR_BOUND=0/5`.
7. Remainder is final: ids, `status=mined`, kind/tier/scope/anchor/teaches, and the three rewritten entries.

## 7. Risks

- The package cannot be landed unedited: rows are safe in four columns, but the r40 body tokens and the missing
  `char N` anchors are L1 work, not adopter work. The map shifts with the citation set (S193→S121/S120/S118), so
  any re-run after an entry or source-line change must be re-diffed against §1, not assumed.
- Read-only package, `shokuknow` and the lane repo untouched; nothing written outside scratch and this report.

VERDICT: ran adopter v4 on the real package — built: exit 0, `CITED=6 APPEND=5 HELD=0 TWIN=1`, map exactly
S134→S117 S185→S118 S186→S119 S190→S120 S193→S121 S195→S118 twin, deterministic, twin-recheck /
registry-first / no-entry refusals all correct; attacked: citation-set variants — dropping the QCG entry
moves S193→S118 (S195 becomes append S119) and refusing only S190 moves S193→S120, leaving six
hand-normalisation cells that block C2 as staged.
