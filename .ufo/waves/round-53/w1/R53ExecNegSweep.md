# R53ExecNegSweep — negative-claim sweeps over the five search-record documents

seat: R53ExecNegSweep (leaf, chousa round 53 wave 1) · date: 2026-10-26
claims: FROZEN at `a6ff732c70011f11c9beb681d832cedc6e75f566`; nothing here proposes a predicate,
target, counter or control change — every finding is reported for the L1 to route.
scope: the five captures named in the ticket, read as UTF-8 text forms; the three staged entries'
negative sentences; the lane Registry at `BASE_REV` = `5b550133d79bc09c82d8965cce2e48c2598b8c3e`.
No fetch, no network, no install (pacman paused host-wide), no fixture repo. Scratch
`/fast/scratch/hyaku/chousa-r53/R53ExecNegSweep/` removed; every receipt is pasted here.

## 1. Sweep — exact `text.count` / `text.find`, one row per term

Command: `export TMPDIR=/fast/scratch/hyaku/chousa-r53/R53ExecNegSweep && python3 sweep.py` — it opens
each `<key>.txt` under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/` and prints
`f"{t.count(term)}@{t.find(term)}"` (`0@-1` when absent). Observed output, verbatim:

```
FILE	chars	lines	newlines_crlf
Jmla	27659	326	0
Cochrane	210708	1466	0
QcgPdf	27609	1525	0
QcgNotice	1255	269	0
NmpaCopy	21573	906	0

TERM	Jmla	Cochrane	QcgPdf	QcgNotice	NmpaCopy
tracking record	2@447	2@114753	0@-1	0@-1	0@-1
tracking records	2@447	2@114753	0@-1	0@-1	0@-1
each information source	2@1368	0@-1	0@-1	0@-1	0@-1
number of records	11@1334	2@115806	0@-1	0@-1	0@-1
records identified	19@1344	3@119481	0@-1	0@-1	0@-1
PRISMA-S	27@417	11@13592	0@-1	0@-1	0@-1
PRISMA 2020	40@401	10@96438	0@-1	0@-1	0@-1
PRISMA	92@401	31@13541	0@-1	0@-1	10@3904
flow diagram	50@472	10@73316	0@-1	0@-1	0@-1
information specialist	0@-1	23@3905	0@-1	0@-1	0@-1
librarian	0@-1	29@3928	0@-1	0@-1	0@-1
unpublished	0@-1	43@4120	0@-1	0@-1	0@-1
grey literature	0@-1	4@52722	0@-1	0@-1	0@-1
gray literature	0@-1	0@-1	0@-1	0@-1	0@-1
检索	0@-1	0@-1	12@3044	0@-1	50@2323
检索策略	0@-1	0@-1	5@14503	0@-1	10@2987
检索日期	0@-1	0@-1	0@-1	0@-1	0@-1
检索式	0@-1	0@-1	0@-1	0@-1	1@3075
数据库	0@-1	0@-1	3@10360	0@-1	25@2325
灰色文献	0@-1	0@-1	0@-1	0@-1	5@3340
未发表	0@-1	0@-1	0@-1	0@-1	3@3353
质量控制指南	0@-1	0@-1	2@8	5@19	0@-1
试行	0@-1	0@-1	9@27	5@33	5@94
2024 年版	0@-1	0@-1	3@19	0@-1	0@-1
2024年版	0@-1	0@-1	0@-1	5@26	0@-1
发布	0@-1	0@-1	7@4378	4@37	4@74
来源	0@-1	0@-1	9@9578	1@534	20@2339
2019年第27号	0@-1	0@-1	0@-1	0@-1	3@101
```

What the frozen claims turn on: `tracking record`/`tracking records` agree in both English documents
(both occurrences are plural — Jmla 447 and 1622), so the singular is a form neither capture carries;
`grey literature` is 4 in Cochrane, `gray literature` 0 everywhere; `检索日期`, `检索式` and
`gray literature` are 0 in all five; the Chinese terms split — `灰色文献`/`未发表`/`检索式` only in the
2019 NMPA copy (5/3/1), `检索`/`检索策略`/`数据库` in the issued guideline (12/5/3) and the copy;
`PRISMA` answers three ways (92 Jmla, 31 Cochrane, **0 guideline**, 10 NMPA copy).

## 2. Which staged negative claims reproduce

Method: every sentence containing `does not|do not|is not|was not|cannot|never|no |not a|nothing|
neither|without|counts 0|未|没有` in the three staged entries was extracted (`sent.py`,
whitespace-flattened), then tested against the sweep, the one-off `count`/`find` checks in section 3,
and the lane Registry at `BASE_REV` (`git show BASE_REV:corpus/SOURCES.md`,
`git show BASE_REV:corpus/knowledge/`).

| # | entry | sentence (clause tested) | sweep / check | count | verdict |
|---|---|---|---|---|---|
| 1 | r40 | "a tracking record is a *routed* record, not a flat list" | `flow diagram` 50@472, `records identified` 19@1344, `Column 1`/`Column 2` 9/9 (J 5651, 6547, 9995) | 50 / 19 | holds |
| 2 | r40 | "the column the flow diagram does not let a reader reconcile against a database total" | `Column 2` 9, `flow diagram` 50 | 9 / 50 | holds as a reading; not a count claim |
| 3 | r40 | "cannot be closed by a flow diagram" | — | — | needs narrowing (interpretive; no term in the sweep tests it) |
| 4 | r40 | "was not checked beyond the passages quoted" | — | — | holds (self-limited scope statement) |
| 5 | r40 | "is not itself a reporting standard" | J calls itself "this commentary" (J 9995) | 1 | needs narrowing: "commentary" is in the capture, "not a reporting standard" is the entry's own judgement |
| 6 | r40 | "No non-Western analogue of a tracking-record allocation was found" | `检索式` 1 only in NmpaCopy; lane at BASE_REV holds `chinese-prisma-s-reception-r52.md` (S114 Chinese PRISMA 2020 checklist, item 6 lists every source class with a per-source date) | 0 | needs narrowing: the lane's own S114 already allocates per source; only the "column" analogue is missing |
| 7 | r40 | "neither places them in a numbered record with a per-source count" | `灰色文献` 0 guideline, `未发表` 0 guideline, `检索日期` 0 all five | 0 | needs narrowing: per-source **count** holds; "numbered record" is contradicted by S114's numbered items 6–7 |
| 8 | r50 | "Over the whole 27,609-character extraction, PRISMA counts 0" | `len(QcgPdf)`=27609, `PRISMA`=0 | 0 | **holds exactly** (length and count both match) |
| 9 | r50 | "A citation is not an alignment" | — | — | holds (definitional) |
| 10 | r50 | "The corpus's Chinese documents name PRISMA, MOOSE and the Cochrane Handbook" | guideline: `PRISMA` 0, `MOOSE` 0, `Cochrane` 11; NMPA copy: `PRISMA` 10, `MOOSE` 5, `Cochrane` 4 | 0/0/11 | **fails for the governing instrument**: only S190 names all three; needs narrowing to the 2019 copy |
| 11 | r50 | "the corpus held the citations without ever holding the alignment" | BASE_REV lane holds `chinese-prisma-s-reception-r52.md`, `chinese-search-record-r39.md` (citations, no alignment sentence) | — | holds (provisional, read-only) |
| 12 | r50 | "the Chinese document that governs this work never names PRISMA-S at all" | `PRISMA-S` = 0 in QcgPdf | 0 | **holds** (it names neither PRISMA nor PRISMA-S) |
| 13 | r50 | "nothing in the corpus shows a *methodological* document on the Chinese side standing in relation to PRISMA-S, because no such document does" | `git ls-tree BASE_REV corpus/knowledge/` lists `chinese-prisma-s-reception-r52.md`, whose S113 is 中国循证医学杂志's PRISMA-S 解读 | 1 entry | **fails at BASE_REV** (superseded by round 52, not wrong when written) |
| 14 | r50 | "the Chinese instrument is not a PRISMA-S document at all" | `PRISMA-S` 0 | 0 | holds |
| 15 | r50 | "has no field for them at all: 灰色文献, 未发表, 内部资料 and 期刊评审 each count 0" | 0 / 0 / 0 / 0 | 0 | **holds exactly** |
| 16 | r50 | "nothing in its instrument points at the evidence a systematic review is supposed to weigh" | `Cochrane` 11@11581 (RoB tool), `指标 4` 4@16260 → 18046 requires Cochrane-referenced search | 11 / 4 | needs narrowing: 指标 4 does point at Cochrane methods; the no-field-for-unpublished half holds |
| 17 | r50 | "the western half does say something the Chinese half cannot" | Cochrane `aligns` 1@13480: "the reporting aligns with the current reporting guidance for PRISMA" | 1 | holds for the alignment sentence |
| 18 | r50 | "That is a question about practice, not about the documents, and neither document answers it" | — | — | holds (process) |
| 19 | r50 | "provincial derivatives were not opened this round" | package `SOURCES.append.md:86` holds S161 (贵州省 derivative) | 1 | needs narrowing: round-scoped, and the package already holds a provincial derivative |
| 20 | r48 | "灰色文献 counts 0, as do 灰色, 未发表, 内部资料 and 期刊评审" | 5 terms × 0 in QcgPdf; companions all match: `文献检索` 3, `系统评价` 7, `数据库` 3, `PICOS` 1 | 0 | **holds exactly** (and every positive companion count matches) |
| 21 | r48 | "the centre's issued quality-control guideline carries no grey-literature field" | same sweep | 0 | holds |
| 22 | r48 | "The grey-literature count is 0 in both" | issued 0 + draft (`830e358c…`, 26,348 chars) 0 for `灰色文献`/`灰色`/`未发表`/`内部资料`/`期刊评审` | 0/0 | **holds exactly** |
| 23 | r48 | "the issued text kept it" (the omission) | issued 0 | 0 | holds |
| 24 | r48 | "a statement about two **issued** documents rather than about a guideline and a draft" | NmpaCopy `灰色文献` 5@3340, `未发表` 3@3353, `2019年第27号` 3@101 | 5/3 | holds for the NMPA side; needs narrowing: the copy is a pharmwyp repost (S190), not the regulator's host |
| 25 | r48 | "the draft's 纳入标准应基于 PICOS 原则 becomes 可根据评价主题确定纳入与排除标准，可基于 PICOS 原则" | issued 10170: `应根据评价主题确定纳入与排除标准` (1), 10187: `可基于“PICOS”` (1) | 1/1 | **fails in part**: the issued text says **应**根据评价主题确定…, and 可 attaches only to the PICOS clause; the entry's quoted issued sentence does not exist |
| 26 | r48 | "the draft's 所检索的数据库应包括中、英文专业数据库 becomes … 多个中、英文专业数据库" | issued 10360 `数据库应包括多个中、英文专业数据库` (1); draft 10421 `数据库应包括` + `中、英文` 10427 across a line break (`中、英文专业\n\n数据库`) | 1 / 0 | holds on content; needs narrowing: the draft wording is not locatable as one line in its text form |
| 27 | r48 | "a shift from a prescription to an option, and from a minimum to a plurality" | draft has no `一个数据库`; it already requires `中、英文` (two languages) | 0 | needs narrowing: "a minimum" is the entry's gloss, not the draft's text |
| 28 | r48 | "The corpus already held a row for this guideline, quoting the draft for comment" | BASE_REV registry: 116 rows (S001–S116), `质量控制\|综合评价\|临床\|药品\|bjhea\|nhei` = 0 rows | 0 | **fails for the lane**: no row to correct; holds only for the campaign package (`SOURCES.append.md:99,101` = S174 notice, S176 draft) |
| 29 | r48 | "www.nhei.cn has now refused for the eleventh and twelfth time this round" | no network this round (L0 `8d77e6c1` open) | — | needs narrowing: untestable here, process claim |
| 30 | r48 | "released it on **2025-01-03**" | notice 517: `发布时间：2025年01月03日`; `2025-01-03` and `2025年1月3日` are both 0 | 1 | needs narrowing: the date holds, the form does not |

## 3. Receipts for the load-bearing verdicts

### 3.1 The guideline names Cochrane 11 times but PRISMA and MOOSE zero

```
QcgPdf 灰色文献	count=0	find=-1
QcgPdf 未发表	count=0	find=-1
QcgPdf 内部资料	count=0	find=-1
QcgPdf 期刊评审	count=0	find=-1
QcgPdf 灰色	count=0	find=-1
QcgPdf 文献检索	count=3	find=10349
QcgPdf 系统评价	count=7	find=9845
QcgPdf 数据库	count=3	find=10360
QcgPdf PICOS	count=1	find=10191
QcgPdf PRISMA	count=0	find=-1
QcgPdf PRISMA-S	count=0	find=-1
QcgPdf MOOSE	count=0	find=-1
QcgPdf Cochrane	count=11	find=11581
Nmpa PRISMA	count=10	find=3904
Nmpa MOOSE	count=5	find=5120
Nmpa Cochrane	count=4	find=2124
Nmpa 灰色文献	count=5	find=3340
Nmpa 未发表	count=3	find=3353
```

So r50's "PRISMA counts 0" (row 8) and r48's five zeros (rows 20–23) reproduce, while r50's
sentence #10 does not: the document that governs the work names Cochrane only, and the one that names
PRISMA *and* MOOSE is the 2019 NMPA copy. The two halves of r50's inference pull in opposite
directions and only the "never names PRISMA-S" half is sweep-supported.

### 3.2 The issued/draft 应→可 correction is mis-quoted

Draft (S176 capture, `830e358c4a157ff56713af98.txt`) at 10230–10470, line breaks as served:
`应根据主题遴选结果确定评价的纳入与排除标准，其中纳 / 入标准应基于“PICOS”原则进行 … 数据库应包括中、英文专业 / 数据库。`
Issued at 10160–10375:
`证据，应根据评价主题确定纳入与排除标准，可基于“PICOS” / 原则进行 … 数据库应包括多个中、英文专业数据库。`
Issued one-line located forms (each `count=1`, one line, `find` offset): `应根据评价主题确定纳入与排除标准`@10170,
`可基于“PICOS”`@10187, `数据库应包括多个中、英文专业数据库`@10360. Draft one-line located form:
`入标准应基于“PICOS”原则进行`@10263 — the `纳` is on the previous line, so r48's draft quote cannot be
located whole in the text form. The substantive shift (PICOS basis becomes optional) is real; the
sentence r48 prints for the issued text is not the issued text.

### 3.3 The r50 source line names the twin, and both ids are unbound in the lane

`corpus/evidence` aside, the campaign staged map is explicit — same URL, same digest, same character
count minted twice, once per entry:

```
105:S185	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	16fe8487aa97b98576a0dbac	27609			quality-control-guideline-issued-text-r48.md
115:S195	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	16fe8487aa97b98576a0dbac	27609			western-instrument-alignment-r50.md
```
(`.ufo/waves/round-45/assimilation/staged-map.tsv`; the package `SOURCES.append.md` repeats it at
lines 110 and 120.) r50's `source: S195 — <that URL>` therefore cites the twin of S185, not a row.

Lane registry at `BASE_REV`:

```
rows=116
S134 rows=0
S176 rows=0
S185 rows=0
S186 rows=0
S190 rows=0
S193 rows=0
S195 rows=0
guideline-text rows=0
jmla/cochrane4 rows=0
```

Every id the three staged entries cite is absent from the lane registry, and no lane row mentions the
guideline or the 2019 NMPA notice at all — consistent with the C2 counter's `REF_ID_UNBOUND=12` on the
copied-as-is control, and with r48 row 28 having no lane row to correct. This is reported, not
patched: re-binding is the L1's integrate step (S117–S121 per the frozen claim).

### 3.4 Quote forms for the L1's spans

Each of these is one line of its `.txt`, `count=1`, byte-exact, with `text.find` offset:

```
QcgPdf   @10170  应根据评价主题确定纳入与排除标准
QcgPdf   @10187  可基于“PICOS”
QcgPdf   @10360  数据库应包括多个中、英文专业数据库
QcgNotice @517   发布时间：2025年01月03日
QcgNotice @755   现予以发布
NmpaCopy @3320   查找时应当注意收集未公开发表的文献，即“灰色文献”，如
Cochrane @13480  the reporting aligns with the current reporting guidance for PRISMA
Cochrane @36693  is important for minimizing bias
Jmla     @1288   PRISMA-S also recommends
draft    @10263  入标准应基于“PICOS”原则进行
```

Caveat for the C2 spans: r40's recheck sentence and its Observation quotations are **not** single-line
forms. Literal `count` 0 / whitespace-normalised 1 for "PRISMA-S also recommends reporting the number of
records identified from each information source" (J 1344: `PRISMA-S also recommends\n       reporting …`)
and for "the recommendation to report search strategies for all databases, registries, and websites that
were searched"; literal 0 / normalised **0** for "should be reported in Column 2" and "also suggests
reporting an overall number for records identified from databases and registers in Column 1" (J is a
two-column PDF whose text form interleaves columns; the reading at 6547/6920 exists, r40's sentence does
not). r50's unpublished paraphrase is also normalised-0 (Cochrane interleaves `( Cook et al 1993 )`;
content at 35546). None is a located quote as the evidence rule defines it.

## 4. What the L1 should route

Frozen, so nothing is changed here. For the Gate/lesson wiring only:
- r50 #10, #13 and r48 #25, #28 are the four sentences that do not reproduce as printed; #25 is the
  only one where the capture contradicts the substance (应 vs 可), the rest are referent/tense/scope.
- The r48 "correction to the corpus's own row" (#28) has no lane row behind it at `BASE_REV`; the row
  it means is the campaign package's S176, so the entry's bookkeeping finding is about the package.
- Quotable forms for the new S117–S121 spans exist for all five documents (3.4), but not in the forms
  the staged entries print; the twin S195 (3.3) is the staged duplicate the C1 REAL leg rests on, and
  the sweep reproduces that from the map and the registry without running any adopter.

VERDICT: attacked the 28-term absence surface of five search-record documents and all 30 negative
sentences of the three staged entries — 15 hold (4 of them exactly on count, length and companion
counts: rows 8, 15, 20, 22), 11 need narrowing, 4 fail as printed (r50 PRISMA/MOOSE attribution,
r50 "nothing in the corpus", r48 issued 应/可 quote, r48 "the corpus already held a row"), with no
predicate, counter or control touched.
