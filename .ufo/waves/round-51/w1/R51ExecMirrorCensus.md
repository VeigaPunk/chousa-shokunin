# R51ExecMirrorCensus — scratch lane mirror, append, census validate

Scratch `/dev/shm/chousa-r51-R51ExecMirrorCensus/` (deleted after this report); lane read-only; no production file written.
ExecAdopt had published no report and no `/dev/shm/chousa-r51-R51ExecAdopt/` at run time, so I reproduced its (1) command verbatim.
## Mirror + adopter
```
cp -a .../chousa-shokunin/corpus /dev/shm/chousa-r51-R51ExecMirrorCensus/lane/corpus
sha256sum lane/corpus/SOURCES.md corpus/SOURCES.md   # both 0713a2ea94eeb7fec4d560768c5623bf5ace6f9d6bc30209dcad7cc6c05f068a
python3 tools/assimilate-rows.py --staged /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md \
  --knowledge /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge \
  --registry /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md --opened 2026-10-25 --out .../o1 \
  --entry corpus/knowledge/japanese-search-record-r38.md \
  --entry corpus/knowledge/chinese-search-record-r39.md \
  --entry corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
EXIT=0
stdout: COLLISIONS=25 / CITED=7 APPEND=7 HELD=0 / BODYONLY=5
stderr: WARN japanese-search-record-r38.md: body-only staged id S105 is also a lane id and reads as that row
        WARN chinese-search-record-r39.md: body-only staged id S097 is also a lane id and reads as that row
        WARN ...amendment-2026-10-23.md: body-only staged id S097 is also a lane id and reads as that row
        WARN ...amendment-2026-10-23.md: body-only staged id S105 is also a lane id and reads as that row
        WARN ...amendment-2026-10-23.md: body-only staged id S106 is also a lane id and reads as that row
```
`renumber.tsv` (map by document; all `append`, none `held`):
```
S109 S107 append www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja
S110 S108 append jaohfa.com/pdf/systematic_review.pdf
S116 S109 append www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290
S117 S110 append www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237
S119 S111 append www.sinomed.ac.cn/article.do?ui=2026335073
S125 S112 append c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx
S126 S113 append www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf
```
`bodyonly.tsv` = `bodyclash.tsv` (all five are also lane ids): ja-r38:S105; zh-r39:S097; amendment:S097,S105,S106.
## Hand removal of body-only ids in the rewritten copies
Lane S097/S105/S106 are unrelated rows (J-STAGE publisher page; two CNKI manuals), so the unchanged tokens read as wrong documents. Replaced in the copies before placing them at `lane/corpus/knowledge/`:
| copy | token | replaced with | reason |
|---|---|---|---|
| japanese-search-record-r38.md | `S105` | `corpus/knowledge/chain-resolution-r3.md` | staged S105 is that own-work row |
| chinese-search-record-r39.md | `S097` | `S108` | Japanese hand-search field = JAOHFA form (staged S110) |
| ...amendment-2026-10-23.md | `S097` | `S108` | functional-foods notification form = staged S110 |
| ...amendment-2026-10-23.md | `S105` | `S109` | Chinese reporting module = staged S116 |
| ...amendment-2026-10-23.md | `S106` | `S110` | Chinese review's published record = staged S117 |

Post-edit `grep -nE 'S09[0-9]|S10[0-9]|S11[0-9]'` on the three copies shows only cited ids S107-S113; no S097/S105/S106 remains.
## Insertion
`{ head -n 116 SOURCES.md; cat o1/append.md; tail -n +117 SOURCES.md; } > new` (line 116 = last Registry row S106; line 118 = `## Paths`). `sed -n '117,123p'` vs `append.md` → `diff` empty (`APPEND-MATCH`); file 314 → 321 lines; append.md sha256 `5ca9b185169a2936029b1da195c42031516f3df610a9405f1f17f4f72b07b860`.
Appended rows (11 cells each, escaped-pipe splitter):
```
S107 11 mined 2026-10-25 365d used-by=corpus/knowledge/japanese-search-record-r38.md
S108 11 mined 2026-10-25 180d used-by=corpus/knowledge/japanese-search-record-r38.md
S109 11 mined 2026-10-25 365d used-by=corpus/knowledge/chinese-search-record-r39.md
S110 11 mined 2026-10-25 365d used-by=corpus/knowledge/chinese-search-record-r39.md
S111 11 mined 2026-10-25 180d used-by=corpus/knowledge/chinese-search-record-r39.md
S112 11 mined 2026-10-25 180d used-by=corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S113 11 mined 2026-10-25 365d used-by=corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
```
## Census validate
First run on the corpus-only mirror (as instructed) is **not clean** — `EXIT=1`:
```
file  E11  S077 missing used-by tools/quarantine-check.py
```
Mirror artifact, not an append defect: `--file` sets `dir_abs = dirname(file)/..`, and the mirror had no `tools/`; the base lane has it. After `ln -s .../chousa-shokunin/tools lane/tools`, re-run on the same mirror:
```
file  W04  S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file  W04  S053 duplicate url docs.python.org/3/library/socket.html across scopes
file  W04  S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file  W04  S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file  W04  S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file  ok    /dev/shm/chousa-r51-R51ExecMirrorCensus/lane/corpus/SOURCES.md
EXIT=0
```
No E lines; the five W04 are pre-existing (identical five on `validate --file corpus/SOURCES.md` at the base, exit 0).
Positive control (E03/E04 are live): duplicated the S113 row inside Registry of a throwaway `SOURCES.dup.md` → `E03 S113 duplicate id`, `E04 S113 duplicate url www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf within scope …`, `EXIT=1`; file deleted.
## Counts before vs after (frozen awk from CORPUS.md §Census)
```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' FILE
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' FILE
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' FILE
```
```
before: rows 106  tier A=93 B=8 C=5   status mined=82 queued=19 rejected=5
after : rows 113  tier A=94 B=14 C=5  status mined=89 queued=19 rejected=5
```
`census --file` corroborates exactly (106→113; A 93→94, B 8→14, C 5→5; mined 82→89; queued 19; rejected 5; invalid 0; missing 0).
## 13-field check and duplicates
```
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' mirror/SOURCES.md
0
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' mirror/SOURCES.md | sort | uniq -d
(no output)
```
E03/E04 absent from the clean validate; the control above shows both can fire.
## stripped.tsv (prose for the Gate)
```
S107 recheck  365d — re-download the PDF and confirm the contiguous run その日時，使用した検索式を同時に記録しておく is unchanged (ran 2026-10-23)
S107 opened   2026-10-23
S108 recheck  180d — re-download the PDF and confirm the (V)-5 heading still reads 検索者、検索ワード、検索式 (ran 2026-10-23)
S108 opened   2026-10-23
S109 recheck  365d — re-download the PDF and confirm module 3 still reads 灰色文献的检索与记录 (ran 2026-10-23)
S109 opened   2026-10-23
S110 recheck  365d — re-download the PDF and confirm 检索时间从各数据库建立至2024年4月1日 is unchanged (ran 2026-10-23)
S110 opened   2026-10-23
S111 recheck  180d — re-open the record and confirm 来源出版物 still reads 中国循证医学杂志 卷：26 期：4 (ran 2026-10-23)
S111 opened   2026-10-23
S112 recheck  180d — re-download the .docx and confirm "SRにおける文献検索期間について明記する" is unchanged (ran 2026-10-23)
S112 opened   2026-10-23
S113 recheck  365d — re-download the PDF and confirm the run still reads "検索の開始日と終了日を記載することで" (ran 2026-10-23)
S113 opened   2026-10-23
```
## Risks / notes
- The five body-only replacements are my reading of the staged entries' own referents; the "wave 3"/"round 3"/"round 4" labels were not re-checked (content seats' scope).
- E11 artifact: a corpus-only mirror cannot satisfy used-by paths outside `corpus/`; the lane's `tools/` had to be symlinked for a faithful validate. Worth a lesson line.
- `recheck` prose is dropped from the row (365d/180d kept) and preserved only in `stripped.tsv`, per the adopter contract.
- No tool installs; no network; lane and shokuknow untouched (read-only); scratch removed.

VERDICT — Built the corpus-only lane mirror, ran the default `--cites source` adopter (exit 0, 7 appends S107-S113, 5 body-only ids hand-removed), inserted append.md after the last Registry row, and the mirror validates clean (exit 0, five pre-existing W04, no E03/E04, NF!=13 = 0) once the lane's tools/ is visible; the only first-run E line (E11 S077) was the corpus-only mirror's missing `tools/`.
