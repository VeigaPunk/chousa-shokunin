# R52ExecAdopt — lane adopter run on the round-52 staged package

Seat: leaf executor, round 52 wave 1. Wrote nothing but this file; scratch removed at exit; every
receipt below is copied here. No tool installed or upgraded (pacman paused; nothing needed).

## 1. The run

Scratch `$S=/fast/scratch/hyaku/chousa-r52/R52ExecAdopt`, `TMPDIR=$S`,
`ASSIMILATE_CITES=<unset>` (`env | grep -c ASSIMILATE` → `0`), so the default `--cites source` ran.

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/assimilate-rows.py \
  --staged   /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md \
  --knowledge /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge \
  --registry /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md \
  --opened 2026-10-26 --out $S/o1 \
  --entry corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md \
  --entry corpus/knowledge/japanese-prisma-item-wording-r40.md \
  --entry corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md
EXIT=0
```

stdout (verbatim):

```
COLLISIONS=31
CITED=5 APPEND=4 HELD=1
BODYONLY=7
```

stderr (verbatim, 7 lines, no `REFUSED`):

```
WARN corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md: body-only id S097 is also a lane id and reads as that row
WARN corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md: body-only id S105 is also a lane id and reads as that row
WARN corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md: body-only id S106 is also a lane id and reads as that row
WARN corpus/knowledge/japanese-prisma-item-wording-r40.md: body-only id S097 is also a lane id and reads as that row
WARN corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md: body-only id S091 is also a lane id and reads as that row
WARN corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md: body-only id S092 is also a lane id and reads as that row
WARN corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md: body-only id S093 is also a lane id and reads as that row
```

`collisions` = 31 ids, `S082`–`S112` (registry 112 ids `S001`–`S112`, staged 114 ids `S082`–`S195`); the
intersection is the pre-existing staged/lane overlap, not this run's map.

## 2. renumber.tsv — the map

```
staged_id	lane_id	action	url
S111	S113	append	www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3
S112	S114	append	www.chinagp.net/CN/column/item185.shtml
S125	S115	append	c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx
S126	S112	held	www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf
S129	S116	append	www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf
```

**The four planned mappings hold exactly**: S111→S113, S112→S114, S125→S115, S129→S116, minted
contiguously from the registry maximum (112 = `S112`), each `append`. Verified the maximum is the
base state, not a sibling's edit: `git -C <lane> diff --stat 00f8c7f5272a1d98b6d34913985fa4537e00aaf9
-- corpus/SOURCES.md corpus/knowledge` prints nothing (HEAD of the lane is `13bc2806`; only `SKILL.md`
is modified in the working tree).

**The held row is S126, and it is labelled `held`** — answer to the seat's question: yes.
`HELD=1`, it consumes no id, and the substitution is right *by document*: staged S126 is the JAHBS
article and lane `S112` is the JAHBS article (`corpus/SOURCES.md:122`, URL `…jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf`).
It is **not** a carried-over staged id, but it is the hazard the seat names: the rewritten entry now
reads `S112` while staged S112 is the *chinagp* page mapped to S114. Lane row `S112` was **not**
widened by the tool (documented limit, `tools/assimilate-rows.py:88`) — it names only
`corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`, correct today because that lane
file cites it.

## 3. append.md — four rows, in lane-id order

Cells the counters read, verbatim (cell 2 source, cell 6 anchor, cells 8–11). Cells 3–5 and 7
(type, tier, scope, claim) are the staged cells with the id substituted and no pipe rewrite
(`stripped.tsv` carries no `cellN-pipe` row); their claim cells end `…Chinese databases`, `…limits used`,
`…PRISMA flow chart`, `…names no searcher` and hold no S token (row-token check below).

```
S113 | source: 系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读（郑卿勇）— 梅斯医学 指南・解读指南, from 中国循证医学杂志 — https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3
     | type docs | tier B | anchor: the 简要介绍 block and the attachment 系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf; page read 2026-10-23
     | mined | 2026-10-26 | recheck 180d | used-by corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md
S114 | source: 中国全科医学 报告清单 — PRISMA2020条目清单 (Chinese translation of the PRISMA 2020 checklist) — 《中国全科医学》 — https://www.chinagp.net/CN/column/item185.shtml
     | type docs | tier B | anchor: the 报告清单 table, items 5-9; page 发布日期：2023-01-31, read 2026-10-23
     | mined | 2026-10-26 | recheck 180d | used-by corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md
S115 | source: 提出様式（日本語）Reporting_Format_Jap_202404 — 国立保健医療科学院 C2H（Evidence to Decision）— https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx
     | type docs | tier A | anchor: section 3 追加的有用性, 3.1 システマティックレビューのリサーチクエスチョン; .docx opened and its `word/document.xml` extracted, read 2026-10-23
     | mined | 2026-10-26 | recheck 180d | used-by corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S116 | source: 「PRISMA 2020 チェックリスト」（日本語訳, JPT ONLINE, ライフサイエンス株式会社）— **original withdrawn**: https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf — **archived at**: https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf
     | type docs | tier B | anchor: 項目6 情報源 and 項目7 検索戦略, and the 抄録チェックリスト reference; archived PDF text extracted with pdftotext, read 2026-10-23
     | mined | 2026-10-26 | recheck 180d | used-by corpus/knowledge/japanese-prisma-item-wording-r40.md
```

Per-row token check (`re.findall(r'\bS\d{3,}\b', line)`): `S113`/`S114`/`S115`/`S116` only, one
token each — no stale staged id survived inside a row.

## 4. S129's source cell puts the DEAD original first — C2 reads the first URL

Cell 2 of `S116` starts `**original withdrawn**: https://www.lifescience.co.jp/…`, archive second.
The frozen counter takes the **first** http(s) URL of a source cell (`c2-count.py:95 def url_of`,
`:171 hits = [… url_of(r[1]) == url_of(url)]`) and its document URL for that doc is `ARCHIVE`
(`c2-count.py:66`, `DOCS` entry `(E_JPW, "S129", ARCHIVE)`), while `ORIGINAL` is only an alias for
register rows (`:67`, `ALIASES`). With the cell as emitted, `hits` is empty for the E_JPW document,
`no_src` is false (the entry's `source:` line already names the archive URL), so it is neither bound
nor refused → `BOUND+REFUSED != 4` → `C2=FAIL` (`claims.md:78`, `c2-count.py:177`). **The archive URL
must be first in that cell.** Note `renumber.tsv`'s `url` column also shows the dead host, so a reader
who trusts that column will not see the archive at all.

## 5. Every cell the L1 must hand-normalise

| row/cell | emitted | required | read by |
| --- | --- | --- | --- |
| S116 cell 2 | original first, archive second | archive first (`https://web.archive.org/web/2024/…list_1.pdf`) | C2 `hits`/`cites` (`c2-count.py:171,177`) |
| S113 cell 11 | `corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md` | the citing C2 entry `corpus/knowledge/chinese-prisma-s-reception-r52.md` | C2 `used == citing` (`c2-count.py:174,177`) |
| S114 cell 11 | same as above | same as above | same |
| S115 cell 11 | `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` | `corpus/knowledge/japanese-search-record-niph-form-r52.md` | same |
| S116 cell 11 | `corpus/knowledge/japanese-prisma-item-wording-r40.md` | **no change** — equals C2's `E_JPW` | same |
| S113–S116 cell 6 | no `char N` at all (`grep -c 'char ' append.md` → `0`) | ≥1 `char N` per bound row, each an offset of one of its quote rows | C2 `ANCHOR_BOUND` (`c2-count.py:227`) |
| S115 cell 6 | "`.docx` opened and its `word/document.xml` extracted" | name the round-52 text form and offsets in it: `capture-text.py <raw>` = **19682 characters** (verified; byte-identical to `build-spans.raw_form`, quotes located e.g. `SRにおける文献検索期間について明記する` once at char 8996) | round-51 lesson §6 item 3; C2 span/`CAPTURE_BOUND` |
| S113–S116 cell 10 | `180d` (prose stripped) | cadence kept; the re-run command now lives only in `stripped.tsv` — restore after the cadence if the row is to carry it | QUALITY 6 (`QUALITY.md:17`) |
| S113–S116 cells 3–5,7 | staged type/tier/scope/claim | unchanged by the tool; a tier/scope disagreement between twins is the reader's call | tool limit (`:88`) |
| registry row `S112` cell 11 | not widened | widen by hand **if** the r52 NIPH entry also cites `S112` (the staged draft's line 5 does) | C2 doesn't need it; QUALITY 6 does |

`stripped.tsv` (all 8 strips: `recheck` prose and the replaced `opened` date, per row):

```
lane_id	column	stripped
S113	recheck	180d — re-open the page and confirm the 简要介绍 still names the 16 条目 and the 中文数据库 challenge (ran 2026-10-23)
S113	opened	2026-10-23
S114	recheck	180d — re-open the page and confirm item 6 still ends 明确说明每一项来源的检索或查询日期 (ran 2026-10-23)
S114	opened	2026-10-23
S115	recheck	180d — re-download the .docx and confirm "SRにおける文献検索期間について明記する" is unchanged (ran 2026-10-23)
S115	opened	2026-10-23
S116	recheck	180d — re-fetch the archived PDF and confirm 項目7 still reads 用いたフィルターや制限も含め，すべてのデータベース，試験登録，Webサイトの完全な検索戦略を記載する (ran 2026-10-23)
S116	opened	2026-10-23
```

## 6. bodyonly.tsv / bodyclash.tsv — all 7 body-only ids collide

`bodyonly.tsv` and `bodyclash.tsv` are identical (`BODYONLY=7`, `bodyclash` = every one of them), so
**no body-only token in this package is safe to carry**:

| id | staged meaning | lane row of that id | consequence |
| --- | --- | --- | --- |
| S097 | FEVER dataset | J-STAGE publisher page (`aggregator-vs-source-r36.md`) | reads as the J-STAGE page |
| S105 | lane-local `chain-resolution-r3.md` (own-work) | CNKI 知网 manual | reads as the CNKI manual |
| S106 | lane-local `citation-chain-fidelity-r24.md` (own-work) | CNKI 大学生论文管理系统 manual | reads as the CNKI manual |
| S091 | NSSD (ncpssd.cn) | CFEVER dataset | reads as a dataset |
| S092 | Lateral Reading paper | FEVER dataset | reads as a dataset |
| S093 | GB/T 7714—2025 | climate-fever dataset | reads as a dataset |

The load-bearing case: the produced `japanese-prisma-item-wording-r40.md` copy (which *is* C2's
`E_JPW`, line 33) still says "the functional-foods notification form (round 3's `S097`)". The
functional-foods form is staged `S110` and lane `S108` — `S097` names neither; lane `S097` is the
J-STAGE page. That token alone breaks C2's `REF_ID_UNBOUND=0` (`c2-count.py:185` counts every S token
in the three entries not in `bound`), so the reference must be written **without an S token**.

## 7. The produced entry copies are not lane deltas

`japanese-prisma-item-wording-r40.md` and `chinese-search-log-r37-amendment-2026-10-23.md` do not
exist in the lane (`ls corpus/knowledge` → 71 files, neither present), so those copies are new files.
`japanese-search-record-r38-amendment-2026-10-23.md` **does** exist in the lane, and the produced copy
is the *staged, pre-round-51* version: `diff -u` of lane HEAD vs staged shows the staged file adds the
NIPH line (`source: S125 … .docx`) and body ids, while the lane file cites `S112` only with seven
`char` anchors and a capture pointer, its `adopted:` line saying the NIPH document was refused in
round 51 and its body-only ids dropped. **Integrating the produced copy would regress that file**, and
C2 wants the NIPH material in a *new* entry (`japanese-search-record-niph-form-r52.md`), not there.
Likewise `chinese-prisma-s-reception-r52.md` is not in the staged package (55 staged entries, none
match), so C2's Chinese entry is an L1 draft, and C2 requires the r52 entries to be the **sole**
citers of S113/S114/S115 (`used == citing`, `c2-count.py:177`): if the old `chinese-search-log-r37-amendment`
copy is also integrated carrying `source: S113/S114`, the used-by cells fail.

## 8. Two routed adopter defects, probed (wave-2 F5/F6 owns the fixes)

Fixture A (scratch, two staged rows for one URL, registry max S002):

```
COLLISIONS=0
CITED=2 APPEND=1 HELD=1
BODYONLY=1
renumber.tsv:
S010	S003	append	example.org/twin
S011	S003	held	example.org/twin
```

The **twin-id `held` label is real**: S011 is labelled `held` although `S003` is minted by this run
(`tools/assimilate-rows.py:437`), and `HELD=1` counts a row that was in fact appended. The same run
also wrote **two identical `source: S003 — …` lines** into the entry (one per twin), which the lane
would have to dedupe. No twin exists in this package, so `HELD=1` here is the honest S126 case.

Fixture B (`recheck` = `2026-02-30 — prose`):

```
REFUSED S011: recheck '2026-02-30 — prose' has no leading valid date or NNd
EXIT=1
ls -a out: collisions reg-ids staged-ids      (append.md/renumber.tsv/stripped.tsv absent)
```

Refusal **ordering** is sound: exit 1, no claim file left behind, only the documented
`reg-ids`/`staged-ids`/`collisions`. Side observation: a prose recheck with no leading date passes as
a "symbolic cadence" (`RECHECK_RE`) — `soonish please` was kept verbatim (exit 0, both rows appended).

## 9. Risks / blockers for the L1

1. The S116 first-URL fix is mandatory before C2 can bind the JPW document; the counter reads `r[1]`.
2. Three `used-by` cells name staged citers, and C2 demands exactly the r52 entries — the cells must
   be rewritten, not re-run (the staged knowledge dir has no r52 entry to pass to `--entry`).
3. Anchor columns carry no `char N`; C2's `ANCHOR_BOUND` needs at least one quote offset per bound row,
   and for S115 the offsets must index the 19682-character `capture-text.py` form, not the round-51
   `.docx` extraction narrative (the `.txt` sidecar there is 319599 bytes of U+FFFD garbage).
4. Seven body tokens read as unrelated lane rows; one of them (`S097` in the JPW entry) is enough to
   fail C2 on its own.
5. The held `S112` row is not widened; decide by hand whether the r52 NIPH entry cites it, and note
   `BOUND` is counted by document (4 keys, min 3) with the JPW document bound only via S116's cell.

VERDICT: ran the frozen adopter on the round-52 package (exit 0, map equal to the plan plus the honest
`held` S126→S112) and falsified its output as integrable — S129's cell puts the dead original URL
first, so C2's first-URL bind fails, three `used-by` cells name the wrong citers, all four anchor cells
lack `char N`, and all 7 body-only ids read as unrelated lane rows; both routed defects (twin `held`
label, refusal ordering) reproduce as described, the second benign.
