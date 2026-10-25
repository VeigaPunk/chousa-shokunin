# R51ExecAdopt — adopter on the three staged entries: exit 0, map S107–S113, five body-only ids and every one is a lane id

Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`; all runs read-only, `--out` under `/dev/shm/chousa-r51-R51ExecAdopt/` (deleted before yield). No lane write, no git index, no jj state, no `/home/vgpnk/Projects/shokuknow` write; none of its campaign tools run. No tool install.
## 0. Revision pin (round-50 closure: pin what a counter was measured against)

```
$ git rev-parse HEAD                       # cfe6c9fb9b56fa80a3005c1a3aaa522b29966306
$ git log --oneline -3 -- tools/assimilate-rows.py
2a3389d round-51: assimilate-rows candidate (source-only citation, bodyonly/bodyclash, …)
$ git status --porcelain tools/assimilate-rows.py; git diff --stat 2a3389d -- tools/assimilate-rows.py   # both empty → tip == candidate
$ sha256sum tools/assimilate-rows.py       # bdaf80f43f39827029b1e849c5a6d8d88252ac88d331bf75fea1df0b51fba29d
```
Inputs pinned: staged rows `a6dec4a0086d3cf767d638d7e52fdda08f78d22b0b376049b0ad14ff0f8aa696` (`SOURCES.append.md`); lane registry `0713a2ea94eeb7fec4d560768c5623bf5ace6f9d6bc30209dcad7cc6c05f068a` (`corpus/SOURCES.md`, 106 rows, max S106); entries `37d6ac65…` (japanese-r38), `f6309cc8…` (chinese-r39), `3e262e8d…` (amendment).
## 1. (1) As staged, default `--cites source`

```
$ python3 …/assimilate-rows.py --staged …/merge/chousa/SOURCES.append.md --knowledge …/merge/chousa/knowledge \
    --registry …/chousa-shokunin/corpus/SOURCES.md --opened 2026-10-25 --out o1 \
    --entry corpus/knowledge/japanese-search-record-r38.md --entry corpus/knowledge/chinese-search-record-r39.md \
    --entry corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
EXIT=0
stdout: COLLISIONS=25 / CITED=7 APPEND=7 HELD=0 / BODYONLY=5
stderr: WARN japanese-r38.md: body-only staged id S105 is also a lane id and reads as that row
        WARN chinese-r39.md: … S097 …   WARN amendment.md: … S097 …, … S105 …, … S106 …  (each: "is also a lane id and reads as that row")
```
`CITED=7` is exactly the seven `source:` ids (`S109 S110 S116 S117 S119 S125 S126`); `HELD=0` — none of the seven URLs is already a lane row, so all seven append.
## 2. Renumber map by document (`o1/renumber.tsv`, all `action=append`)

| staged | lane | document | URL (tool's `url_of`) |
|---|---|---|---|
| S109 | **S107** | システマティックレビューの基礎（喜屋武 享）, 日健教誌 32(2):120-121 | www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja |
| S110 | **S108** | PRISMA声明チェックリスト(2020年) 別紙様式 (V)-4/(V)-5, JAOHFA 第2版 | jaohfa.com/pdf/systematic_review.pdf |
| S116 | **S109** | 动物实验系统评价与Meta分析报告的规范撰写建议, 实验动物与比较医学 2025;45(4) | www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290 |
| S117 | **S110** | GRADE方法的实证研究, 实验动物与比较医学 2025;45(1) | www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237 |
| S119 | **S111** | SinoMed 记录 ui=2026335073, 中国循证医学杂志 26(4) | www.sinomed.ac.cn/article.do?ui=2026335073 |
| S125 | **S112** | 提出様式 Reporting_Format_Jap_202404, NIPH C2H | c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx |
| S126 | **S113** | システマティックレビューとメタアナリシスの実施方法, JAHBS 38(1) | www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf |

Exactly the planned map (ascending staged id from registry max S106), one document per lane id, no twin. `append.md` = 7 lines, 7109 B, ordered S107→S113.
## 3. (3) Row integrity — all seven rows

```
S107 empty_cells=[] kind=paper tier=B  …  S113 empty_cells=[] kind=paper tier=B      (7/7, no raw pipe in any cell)
cells 1-8 byte-identical to the staged row after id substitution: 7/7 "cells ok"
status=mined 7/7 | opened=2026-10-25 7/7 | recheck ∈ {365d,180d} 7/7
used-by: S107,S108 → japanese-search-record-r38.md ; S109,S110,S111 → chinese-search-record-r39.md ;
         S112,S113 → japanese-search-record-r38-amendment-2026-10-23.md
```
Each `used-by` is exactly the one entry whose `source:` line names that staged id — no row has two users, none has a non-citing entry. It is a statement about `source:` lines only: the body-only ids of §5 appear in no `used-by`, which is the intended source-mode reading.
## 4. `stripped.tsv` — the prose for the lesson Gate (14 rows = 7 `recheck` + 7 `opened`)

```
S107 recheck  365d — re-download the PDF and confirm the contiguous run その日時，使用した検索式を同時に記録しておく is unchanged (ran 2026-10-23)
S108 recheck  180d — re-download the PDF and confirm the (V)-5 heading still reads 検索者、検索ワード、検索式 (ran 2026-10-23)
S109 recheck  365d — re-download the PDF and confirm module 3 still reads 灰色文献的检索与记录 (ran 2026-10-23)
S110 recheck  365d — re-download the PDF and confirm 检索时间从各数据库建立至2024年4月1日 is unchanged (ran 2026-10-23)
S111 recheck  180d — re-open the record and confirm 来源出版物 still reads 中国循证医学杂志 卷：26 期：4 (ran 2026-10-23)
S112 recheck  180d — re-download the .docx and confirm "SRにおける文献検索期間について明記する" is unchanged (ran 2026-10-23)
S113 recheck  365d — re-download the PDF and confirm the run still reads "検索の開始日と終了日を記載することで" (ran 2026-10-23)
S107..S113 opened  2026-10-23   (7 rows, replaced by 2026-10-25)
```
Gate lesson: the row keeps the interval and drops the instruction, and each dropped sentence is the only place its row says what to re-open and what the run must still read. Unless the Gate or the entry carries these seven sentences verbatim, the lane lands seven rows whose recheck can only be re-guessed. The three entry `recheck:` lines are separate prose — same intent, different text.
## 5. Body-only ids — is `S097/S105/S106` exactly what the entries mention?

Yes, and only that: 5 `(entry, id)` pairs over 3 distinct ids, from every non-`source:` line.

`japanese-r38.md:54 S105` · `chinese-r39.md:55 S097` · `amendment.md:50 S097` · `amendment.md:56 S105` · `amendment.md:72 S105 + S106`
`o1/bodyonly.tsv` and `o1/bodyclash.tsv` are byte-identical (5 rows each): every body-only id is also a lane id, so the clash file adds no discrimination. The lane rows they would falsely read as:

```
lane S097 = J-STAGE 出版社向け Citation・被引用文献リンク機能 (used-by aggregator-vs-source-r36.md)
lane S105 = 知网学位论文学术不端行为检测系统使用手册 (used-by citation-matching-semantics-r41.md, cnki-citation-check-r40.md)
lane S106 = “中国知网” 大学生论文管理系统使用手册 (used-by citation-matching-semantics-r41.md)
```
None of the five occurrences means any of those three rows. Occurrence-level repair, from each entry's own prose:

| occurrence | what the entry means | staged id of that document | lane id after §2 |
|---|---|---|---|
| japanese-r38:54 `S105` | the lane's own chain-hop entry | staged S105 (own-work) = `corpus/knowledge/chain-resolution-r3.md` | **no lane row** — `grep -c 'chain-resolution-r3.md' corpus/SOURCES.md` → `0`; file exists, sha256 `d794343f8528e263…`, 15,772 B → file path, or drop |
| chinese-r39:55 `S097` | wave 3's Japanese functional-foods hand-search form | staged S110 | **S108** |
| amendment:50 `S097` | the same functional-foods form | staged S110 | **S108** |
| amendment:56, :72 `S105` | "Round 4's Chinese reporting module" (灰色文献的检索与记录) | staged S116 | **S109** |
| amendment:72 `S106` | the Chinese review's own published record | staged S117 | **S110** |

Two consequences for the L1: (a) **the id is not a repair key** — `S105` denotes the chain-hop entry in one entry and the Chinese module in another, and `bodyonly.tsv` is keyed `(entry, staged_id)` so nothing in it says they differ; a blanket "rewrite S105" mis-points one of them. (b) **the copies the adopter emits keep the bad ids** — substitution covers cited ids only, so the landed text still reads japanese-r38 `['S105','S107','S108']`, chinese-r39 `['S097','S109','S110','S111']`, amendment `['S097','S105','S106','S112','S113']`; all five occurrences must be edited in the entry files, which the tool warns about and never touches.
## 6. (2) `--cites all` — the old behaviour on this package

```
$ … --cites all --entry <all three>            EXIT=1
stdout: COLLISIONS=25
stderr: REFUSED S105: staged row names no http(s) URL
        REFUSED S106: staged row names no http(s) URL
```
The round-50 reading **cannot run this package at all**: the two body-only own-work rows (chain-hop, citation-chain fidelity) carry no URL. Isolated per entry, to show what it would have added:

```
chinese-r39 alone:  EXIT=0  CITED=4 APPEND=3 HELD=1 — S097→S085 held (fever.ai/dataset/fever.html), S116→S107,
                    S117→S108, S119→S109 append: the entry's "Japanese hand-search" bound to the FEVER row, map shifted −2
japanese-r38 alone: EXIT=1  REFUSED S105        amendment alone: EXIT=1  REFUSED S105, S106
```
That observed run is the falsifier of the old predicate: one body-only id both binds a false identity (S097→lane S085, FEVER dataset) and moves every appended id (`S116→S107`, not `S109`). Union arithmetic [INFERENCE, from the tool's ascending-assign loop]: had S105/S106 carried URLs, `--cites all` would append 9 rows — S105→S107 and S106→S108 as lane rows for own-work artefacts, the seven documents landing S109–S115 — a different lane for all seven plus two rows the lane must not hold.
## 7. Operability checks I could run (D3, identity, env, idempotence)

```
registry copy, `## Registry` → `## Rows`:      EXIT=1  REFUSED registry has no `## Registry` heading + REFUSED … outside the Registry section: S001…S106 (all 106)
registry copy, S106 moved below `## Paths`:    EXIT=1  REFUSED registry rows outside the Registry section: S106
registry copy with the 7 rows appended:        EXIT=0  CITED=7 APPEND=0 HELD=7  — same map, all held by URL
ASSIMILATE_CITES=all (env, no --cites):        EXIT=1  same two REFUSED lines → env honoured
ASSIMILATE_CITES=bogus:                        EXIT=2  assimilate-rows: ASSIMILATE_CITES='bogus' must be source or all
```
D3 is reachable and specific (missing heading vs. named outside rows), and the URL identity is stable across the append — the L1 can land §2 and re-run without a second numbering.
## 8. Named limits (not closed here)

- **D1 is not exercised by this package**: no cited staged row has an escaped pipe in its `source` cell, so `url_of(pipe_free(cell2))` never differs from `url_of(cell2)` here. The only escaped-pipe staged row is S097 and its two `\|` sit in the recheck cell (`"SUPPORTS\|REFUTES\|NOT ENOUGH INFO"`), which source mode never cites.
- **D2 is exercised only under `--cites all`**, and only by S097: escaped split → 11 cells, naive split → 13. In source mode these three entries do not test the splitter.
- `COLLISIONS=25` is printed as a count only; the ids (`S082…S106`, different documents) are in `o1/collisions`, not on stdout. After landing the count is 32 (S107–S113 also collide with staged rows S107–S113), so the staged and lane namespaces stay indistinguishable to any body-only reader.
- `used-by` correctness rests on the `source:` predicate by construction: I verified it matches the seven source lines, not that the seven URLs are the documents the entries describe (that is the captures' job, not the adopter's).

VERDICT: Built and ran the adopter on the three staged entries as staged (`EXIT=0`, `CITED=7 APPEND=7 HELD=0`, map S109→S107 … S126→S113 exactly as planned, seven 11-cell rows `mined`/`2026-10-25` with `used-by` = the citing entry alone), then attacked it with `--cites all` (`EXIT=1`, REFUSED S105/S106; the chinese-entry run shows S097 silently held at lane S085 and the map shifted −2) and with heading/outside-row registry copies (`EXIT=1`, exact REFUSED lines); the defect this package actually exposes is that all five body-only occurrences are lane-id collisions the emitted entry copies still carry, each needing an occurrence-level repair (S097→S108 ×2, S105→S109 ×2, S106→S110, chain-hop→file path), while `stripped.tsv` shows the seven recheck instructions reduced to bare intervals for the Gate to carry.
