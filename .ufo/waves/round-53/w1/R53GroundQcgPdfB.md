# R53GroundQcgPdfB — second pass on staged S185 + twin S195 → planned lane S118

seat: R53GroundQcgPdfB (scribe; the A-pass seat's report was not opened)
target: 《药品临床综合评价质量控制指南（2024 年版 试行）》 issued text — staged S185, twin S195, planned id S118
capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/16fe8487aa97b98576a0dbac.{txt,raw,pdf}` (read-only)
lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`: read-only for this seat — no lane file written; nothing fetched (L0 `8d77e6c1` open); `c1-count.py`/`c2-count.py`/`inference-ground.py` not run.
scratch `/fast/scratch/hyaku/chousa-r53/R53GroundQcgPdfB`: all receipts copied inline below, then deleted.

## 1. Identity stamp — and three things the document does NOT carry

```
first char U+836F
line  1 off   0 count 2 '药品临床综合评价质量控制指南'
line  2 off  15 count 2 '（2024 年版 试行）'          # bare paren at 18
line  7 off  35 count 5 '国家药物和卫生技术综合评估中心'   # bare name at 36
line  9 off  53 count 1 '（国家卫生健康委卫生发展研究中心）'
line 13 off  74 count 1 '二〇二四年十二月'            # bare date at 78
ident 0 北京市卫生经济学会   ident 0 bjhea   ident 0 印发   ident 0 号〕   ident 0 2025
ident 1 版本 ('版本的项目设计方案')   ident 1 修订 ('修订指南框架')
fed 42 pages: 42
```

- **No host line.** `北京市卫生经济学会` and `bjhea` are 0 in the text: the society is the URL's host only. The
  issuance act (`2025-01-03`, `现予以发布`) belongs to the release notice (S186), not this file. No 印发, no 文号 —
  the four `〔…〕号` in the preamble cite *other* instruments (国办发〔2018〕88、国卫药政函〔2019〕80、国卫医发〔2020〕2、国卫办药政发〔2021〕16).
- **No version line** beyond `2024 年版 试行`; the single `版本` and `修订` are ordinary words, not edition statements.
- **Author is PDF machine metadata, not a printed stamp.** Info dict: `/Author (Xue Li) /Company () /CreationDate (D:20241231170153+08'00')
  /Creator (WPS 文字…) /Producer () /Title () /Trapped /False`. `pdfinfo` renders that date `Tue Dec 31 06:01:53 2024 -03`;
  the file's own stamp is `+08'00` → **2024-12-31 17:01:53 +08:00** (host TZ rendering, not the file's). A personal name on an
  authoring workstation; the document names no individual author. So "issued 2024-12-31" rests on a WPS carrier stamp — the
  printed date is 二〇二四年十二月.
- **The entry's anchor must use the document's own numbering:** 第二章 (line 385, off 6181) → 二、工作内容 (off 8782) →
  （三）评价方法和数据的质量控制 (off 9724; TOC off 1639 prints page 16, footer `16` on line 685) →
  `1.文献研究的质量控制` (off 9938, unique) → `（1）文献获取` (off 10098, opening page 17 — formfeed is the first char of
  line 686). There is **no `§1`**, and indicator ids **restart per stage** (`指标 4：` occurs 4×).

## 2. Capture binding and text-form determinism

```
KEY 16fe8487aa97b98576a0dbac capture True        # sha256(URL)[:24] == capture stem
CHARS 27609 SHA256 927ff71c6d499477c9cc7a3acf9ed7e335cd63b802850e5f39f5aa86a398d3a4
pdfinfo: Author Xue Li / Creator WPS 文字 / Pages 42 / 595.3 x 841.9 pts (A4) / Encrypted no
cmp 16fe…pdf 16fe…raw → silent; pdftotext -layout 16fe…pdf → sha256 == 927ff71c… (BYTE-IDENTICAL to the .txt)
wc -c -m -l .txt → 61909 27609 1524 ; form feeds 42 == PDF pages 42 ; \r count 0 ; no BOM
```

The `.txt` form IS `pdftotext -layout` of the capture PDF, deterministic, so `build-spans.py` slices reproduce from cache alone.

## 3. QUOTE machine lines (each: count 1, on one line, byte-exact; span `[off-80, off+len+80]` longer than quote)

```
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	数据库应包括多个中、英文专业数据库。	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	根据文献筛选流程制定流程图，注明每环节	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	纳入与排除文献的数量及理由，以保证纳入文献的可靠性。	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	数据库检索策略、文献质量评价表、药物经济学评价模型、真实	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	提供系统检索策略和文献筛选流程等资料	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	提供项目主要的技术附件，如检索策略、检索结果和纳入/排除研究列表、	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	及最终结果是否完整可追溯（包括操作人、复核人、操作时间、操	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	指标 4：在文献检索和筛选阶段，是否参照 Cochrane 等组织制定的	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	二〇二四年十二月	corpus/knowledge/quality-control-guideline-issued-text-r48.md
```

Offsets = the `char N` values for the row's `anchor` cell (`c2-count.py:222-223` recomputes `offset + span.find(quote)`;
span starts at `off-80`, except `char 78` whose span starts at 0): `char 10360, 10459, 10480, 14500, 17222, 27444, 17958, 18046, 78`.
Quote 1-2 = 文献获取 + flow counts; 3 = technical appendix's `数据库检索策略`; 4 = 指标 6; 5 = 附件四 六、附件;
6 = the field-level traceability the instrument *does* give (for data processing, and 指标 3 is 选填/non-core per the
footnote at `char 22312`); 7 = the Cochrane-alignment entry's quote; 8 = printed date stamp. All nine occur **0×** in the
`.raw` decoded as UTF-16LE, so `form_texts` picks the `.txt` first — no raw-form span clipping. `quotes.tsv` rows are these
same four fields minus the `QUOTE` prefix (`id  url  quote  entry`, tab-separated; intended `corpus/evidence/round53/quotes.tsv`).

## 4. Negative sweeps, exact `text.count` over the whole `.txt` (27,609 chars)

```
tracking record=0 each information source=0 information source=0 number of records=0 PRISMA-S=0 PRISMA 2020=0
information specialist=0 librarian=0 unpublished=0 grey literature=0 检索=12 检索策略=5 检索日期=0
灰色文献=0 未发表=0 PRISMA=0 数据库=3 信息源=0 检索式=0 主题词=0 关键词=0 灰色=0 内部资料=0
期刊评审=0 文献检索=3 系统评价=7 PICOS=1 检索结果=2 筛选流程=3 纳入与排除=2 文献获取=1
文献研究的质量控制=1 指标 4=4 选填=17
```

**ABSENT (0) — every negative claim an entry makes here carries its sweep:** tracking record · each information source ·
information source · number of records · PRISMA-S · PRISMA 2020 · information specialist · librarian · unpublished ·
grey literature · 检索日期 · 灰色文献 · 未发表 · PRISMA · 信息源 · 检索式 · 主题词 · 关键词 · 灰色 · 内部资料 · 期刊评审.
**PRESENT:** 检索 12 · 检索策略 5 · 数据库 3 · 文献检索 3 · 系统评价 7 · PICOS 1 · 检索结果 2 · 筛选流程 3 · 纳入与排除 2 · 选填 17.

**Depth reading the entry can carry.** The instrument makes the search-strategy *artefact* mandatory — `数据库检索策略`
in the 技术附件 (char 14500), `检索策略、检索结果和纳入/排除研究列表` in 附件四 (char 27444), `系统检索策略和文献筛选流程`
at 指标 6 (char 17222) — and the per-stage counts with reasons (10459, 10480); it names **no content standard** for that
artefact: no term vocabulary (信息源/检索式/主题词/关键词 all 0), no date field, no grey or unpublished category, no named
instrument (PRISMA 0). Field-level traceability (操作人、复核人、操作时间、操作步骤、数据保存位置, char 17958) exists only
for data processing, and that indicator is 选填 = 非核心. An audit checklist that mandates the search artefact and leaves its
contents unspecified.

## 5. The staged entry's claims — reproduced, and four that do not hold (reported, not patched)

Reproduces exactly: `27,609 characters`; 灰色文献 0, 灰色 0, 未发表 0, 内部资料 0, 期刊评审 0, 文献检索 3, 系统评价 7,
数据库 3, PICOS 1; the two-text comparison in §6; the 附件四 title.

1. **`§1` is not the document's numbering** (see §1). The anchor cell and Observation say `§1 文献研究的质量控制`.
2. **The corpus row it says it corrects is not in the lane.** Entry, verbatim: "The corpus already held a row for this
   guideline, quoting the **draft for comment**." / "the round-13 row should be marked as quoting the draft, not silently
   read as the guideline." Observed: `grep -c bjhea corpus/SOURCES.md` = **0**; no lane row holds `1735802822163204`; no
   `corpus/knowledge` entry cites it or `征求意见稿`; round 13 in this lane is the hardlink-alias round
   (`corpus/knowledge/hardlink-alias-r13.md`) and mentions no guideline. The two rows that do exist (S174 notice, S176 draft)
   are staged rows in the read-only package's `SOURCES.append.md`, not the lane registry — say that, or drop the sentence.
3. **A quoted string crosses a line break.** "所检索的数据库应包括**多个**中、英文专业数据库" cannot be a located quote
   (line 699 ends `…所检索的`, line 701 begins `数据库应包括多个…`); the located form is `数据库应包括多个中、英文专业数据库。`
   at char 10360. No `**` marker and no line break may fall inside a quote row, and each quote must appear byte-exact in both
   the entry and `corpus/lessons/round-53.md`.
4. **"issued on 2024-12-31" needs its carrier named** — it is the PDF's `/CreationDate`, not a printed statement (§1).

## 6. Draft (S176, `830e358c…`, 26,348 chars) vs issued — located divergences

```
draft: 检索=9 检索策略=3 检索日期=0 灰色文献=0 未发表=0 灰色=0 内部资料=0 期刊评审=0 PRISMA=0 选填=21 附件四=0 多个=0
draft stages: 共 10/11/19/33 条核查重点 at 16801/17557/18595/20401 ; 指标 4 starts 18803, 选填 at 18891
draft line 692: '\x0c标准后进行系统文献检索，所检索的数据库应包括中、英文专业'   (phrase at 10417)
issued stages: 共 10/11/18/32 条核查重点 at 16066/16809/17763/19389   (ids contiguous 1..N per stage in both)
```

| divergence | draft | issued |
|---|---|---|
| plurality | `数据库应包括中、英文专业数据库` (`多个` = 0 in the whole draft) | `数据库应包括多个中、英文专业数据库。` (char 10360; `多个` at 10366) |
| 指标 4 | `参照《Cochrane 干预措施系统评价手册》规范开展文献检索` (18803) | `参照 Cochrane 等组织制定的相应规范或指南…` (char 18046) |
| 指标 4/5/6 status | `选填` on 指标 4's line (18891), 5 (19019), 6 (19147) | no `选填` between char 18001 and 18466 → core; footnote `2.备注中“选填”的指标为非核心指标` (char 22312) defines it |
| stage census | 10/11/**19**/**33** | 10/11/**18**/**32** |
| attachments | no `附件四` (`附件四` = 0); 附件三 = `规范和常用工具` | `附件四：药品临床综合评价报告模板` (TOC off 2274, body off 25598); 附件三 = `规范和常用评价工具` |
| vocabulary | 检索日期 0, PRISMA 0, 灰色文献 0 | unchanged (0/0/0) |

The issued text *strengthens* the search requirement (plurality; three literature-research indicators promoted from
选填 to core) while the grey/unpublished absence is continuous — an instrument property, not a drafting slip.

## 7. Row to land (S118) and the twin/binding consequence

`c2-count.py:78-86` pairs **S195 → `western-instrument-alignment-r50.md`** and **S185 → `quality-control-guideline-issued-text-r48.md`**
for this one URL, and C2 wants *exactly one* lane row. So the row's `used-by` must name **both** entries, both must carry
`source: S118 — <url>`, and C1's twin rule is what stops S195 minting a second id.

```
| S118 | 《药品临床综合评价质量控制指南（2024 年版 试行）》 — 国家药物和卫生技术综合评估中心（国家卫生健康委卫生发展研究中心），北京市卫生经济学会 载 — https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf | docs | B | **for the national centre's issued quality-control guideline and the search record it demands** — what the 文献获取 and 文献研究 indicators require of a search (multiple Chinese/English databases, two independent screeners, per-stage flow counts, a database search strategy in the technical appendix) and what they do not name (no PRISMA/PRISMA-S, no search date, no term vocabulary, no grey or unpublished category); tier B because the document is the centre's and the carrier a professional society's file host, and this row governs *wording* claims because draft and issued text differ | 第二章 二、工作内容（三）评价方法和数据的质量控制 → 1.文献研究的质量控制 → （1）文献获取 (page 17), the 指标 6 and 指标 4 rows of 附件一, and 附件四's 六、附件; capture .txt read as UTF-8, 27,609 characters, pdftotext -layout of the 42-page PDF, sha256 927ff71c…; char 10360, char 10459, char 10480, char 14500, char 17222, char 27444, char 17958, char 18046, char 78 | the issued instrument makes the search artefact mandatory and its contents unspecified — a database search strategy and per-stage counts in the appendix, not a field list for the search itself | mined | 2026-10-26 | 180d | corpus/knowledge/quality-control-guideline-issued-text-r48.md, corpus/knowledge/western-instrument-alignment-r50.md |
```

## 8. Not verified here / out of scope

- S186 (release notice), S190 (2019 NMPA copy) and S193 (Cochrane ch.4) belong to sibling seats: I opened none of their
  captures, so the entry's `2025-01-03` / `现予以发布` and the 2019 counterpart's duties are unverified by this pass.
- The `多个` at char 8420 (outside the 文献获取 sentence) was not read in context; the plurality claim rests on 10366 only.
- No lane file, span, quotes.tsv or registry row written; no counter run. Tooling: none installed or upgraded (pacman guard
  respected, no network); used `pdfinfo`/`pdftotext` (poppler), `python3`, `cmp`, `strings` as found.

VERDICT — attacked the S185/S195 → S118 binding as an independent second pass: identity stamp, the document's silence on
host/issuance/version, nine located quotes (six substantive, all unique, single-line, span-longer) and 21 counted negative
terms all hold, and the pass adds that the issued text strengthens the search requirement over the draft (多个 added;
指标 4/5/6 promoted from 选填 to core; stage census 19→18, 33→32; 附件四 added); the staged entry's `§1`, its unsupported
"round-13 row" and its line-crossing quoted string do not hold and are reported, not patched.
