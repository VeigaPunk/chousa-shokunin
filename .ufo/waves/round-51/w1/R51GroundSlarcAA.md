# R51GroundSlarcAA — staged S116 (实验动物与比较医学 2025;45(4):496-507) re-grounded

Attacked: the staged claims carried by `corpus/knowledge/chinese-search-record-r39.md` (staged id S116, row
`SOURCES.append.md:41`) about "表3 报告模块表 module 3 文献检索策略" and §2.1.1, against the on-disk capture only.
No fetch (L0 `8d77e6c1` open). No install performed; no tool upgraded.

## Capture and form

- Form used for every offset below: `fd468a36d78ff156b6200946.txt` **read as UTF-8** — **52208 characters**,
  657 lines, 82903 bytes. Original bytes `…946.raw`: PDF 1.4, 12 pages, 1156890 bytes.

```
$ wc -c …/fd468a36d78ff156b6200946.txt …/fd468a36d78ff156b6200946.raw
  82903 …/fd468a36d78ff156b6200946.txt
1156890 …/fd468a36d78ff156b6200946.raw
$ file …
fd468a36d78ff156b6200946.raw: PDF document, version 1.4, 12 page(s)
fd468a36d78ff156b6200946.txt: Unicode text, UTF-8 text
$ python3 -c "t=open('…946.txt',encoding='utf-8').read(); print('chars',len(t)); print('lines',t.count(chr(10)))"
chars 52208
lines 657
```
Raw cross-check — whitespace-normalised containment in a `pdftotext -enc UTF-8` decode of the `.raw` (run in
`/dev/shm/chousa-r51-R51GroundSlarcAA/`, deleted after): all nine quoted phrases pass, five shown; no `表 3` caption.

```
raw chars 35566 pages marker 12
True 尚无专门针对动物实验SR的报告规范
True 灰色文献的检索与记录
True 含动物实验特殊数据库
True 研究者应至少提供一个主要数据库的完整检索策略
True 表1研究方案主体报告框架内容
raw has 表3 caption? False
```

Limit, recorded not passed: `S116` is a staged id and the lane registry tops out at `S106`
(`grep -c '^| S' corpus/SOURCES.md` → `106`), so QUALITY criterion 30's `tools/quote-reopen.py verify` step cannot
resolve it; that tool also fetches live URLs, which L0 forbids here. Quotes are verified against the committed
capture bytes by `text.find`, not by re-open.

## Located quotes (form: the `.txt` read as UTF-8; each occurs exactly once)

- **off 14179** · `表 1 研究方案主体报告框架内容` — supports: the module table is **表1** and its subject is the research
  **protocol** (`Table 1 Framework for main report of research protocol`, off 14196), introduced in §1.3 预注册与方案撰写
  (off 13301). Not supported: staged "表3 报告模块表" — the only `表 3` is `（原文表 3）` (off 33964), a pointer to a GRADE
  table inside the exemplar paper; `报告模块表` occurs 0 times.
- **off 15113** · `（1）检索数据库（如 PubMed、Embase 等，含动物实验特殊数据库）` — supports: item 1 requires the databases
  searched, expressly including animal-experiment-specific ones. Not supported: the names of those databases — module 3
  names none; MGI, Animal Study Registry, OpenGrey, ProQuest, EThOS and CAB Abstracts sit in 表2 (off 23316), uncited.
- **off 15186** · `（2）检索时间范围：` — supports: item 2 requires a time range. Not supported: any fixed date bound
  (`2024-04-01` occurs 0 times; that bound is S117's), nor per-database timestamps.
- **off 15240** · `检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）` — supports: terms and their logical relations,
  MeSH/Emtree plus free text, as the continuation of item 2. Not supported: a Boolean operator list or a printable
  strategy string — AND/OR appear only in §2.4.1 (off 23003ff).
- **off 15307** · `（3）灰色文献的检索与记录` — supports: grey-literature retrieval **and recording** is a required
  module item. Not supported: which grey sources, or any recording format.
- **off 17709** · `尚无专门针对动物实验 SR 的报告规范` — supports: the §2.1.1 statement that no dedicated reporting standard
  yet exists for animal-experiment SRs, under 遵循国际通用规范, followed by advice to use PRISMA. Not supported: a
  **Chinese** standard or any national body — `国家标准` occurs 0 times and no `中国` hit falls in the §2.1.1 window
  (432, 892, 1438, 24392, 24410, 38844, 39753, 48888, 50445, 51334); nor PRISMA-S (0 occurrences). The `.txt` splits the
  sentence across interleaved column lines, so this contiguous fragment starts mid-clause.
- **off 1984** · `目前应用于动物实验领域的 SR 和 Meta 分析在实施过程与报告撰写上尚缺乏统一规范` — supports: a **second,
  independent** absence statement, in the abstract. Not supported: "China"; it is a statement about the field.
- **off 22928** · `研究者应至少提供一个主要数据库的完整检索策略，` — supports: §2.4.1 文献检索策略 (off 22408) states the
  report's own search-record requirement, which the entry never cites. Not supported: a strategy for **every** database
  ("至少一个主要数据库"), nor a run timestamp.
- **off 23003** · `展示所用主题词 （如 MeSH） 与自由词的组合，以及它` — supports: controlled terms plus free words joined by
  Boolean logic (AND, OR) in §2.4.1, with citation tracking / hand-searching, the reference manager and the
  de-duplication method following (off 24601, 24688). Not supported: an Emtree mention — Emtree occurs once (off 15257,
  module 3 only).

## Staged claims about this document that the capture does not carry

1. **`表3 报告模块表`** — carried identically in the entry's `source:` line and in `SOURCES.append.md:41` col 5. The table
   is **表1**, titled 研究方案主体报告框架内容; `表 3` exists only as `（原文表 3）` (off 33964).
2. **"report module" framing** — 表1 belongs to §1.3 预注册与方案撰写, so module 3 is a *protocol* framework row. The
   capture carries the review **report**'s search requirements in §2.4.1, not in the table.
3. **"no Chinese standard … yet exists"** (staged row col 5; entry title "China has no standard for one yet") — the
   capture says 尚无专门针对动物实验 SR 的报告规范 under a heading about following *international* norms; it names no
   country, no 国家标准, no body.
4. **"the 2024-04-01 date bound"** in the entry's `recheck:` line — 0 occurrences; module 3 carries 检索时间范围 only.
5. **"the third has no counterpart in PRISMA-S's checklist"** (Inference) — PRISMA-S occurs 0 times; that comparison is
   external to S116 and must not be sourced to it.
6. **Animal-specific databases as module content** — the *requirement* is carried (含动物实验特殊数据库); the *names* are
   not in module 3 (see 表2). Read as "module 3 names them", the claim is not carried.
7. **Any English wording of module 3** — the English header exists (No./Module/Report details, off 14340, 14410) but row 3
   is Chinese-only; `Database` occurs 0 times in off 15100-15320. English phrasing is lane translation.

Carried and confirmed (not defects): the three module items; the §2.1.1 absence plus PRISMA advice; no named searcher
(`检索者`, `检索人员` → 0); citation 2025;45(4):496-507 (page-496 header, 文章编号 `1674-5817（2025）04-0496-12`, self-citation
`45(4): 496-507` at off 51400ff). Capture mtime `2026-10-23 20:39:15 -0300` matches the staged `read 2026-10-23`.

## Drafted text for L1 (intended lane path: `corpus/knowledge/chinese-search-record-r39.md`)

Content-only correction: it changes no document in C2's frozen three-entry / seven-capture set.

```
source: S116 — https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290 — 表1 研究方案主体报告框架内容 (Table 1 Framework for main report of research protocol) row 3 文献检索策略, §1.3 预注册与方案撰写; §2.4.1 文献检索策略; 表2 动物实验系统评价的数据库检索参考; §2.1.1 遵循国际通用规范 — 实验动物与比较医学 2025;45(4):496-507
```

Add to Observation: 表2 names the animal-specific and grey sources module 3 only gestures at (MGI, Animal Study Registry;
OpenGrey, ProQuest Dissertations & Theses, EThOS, CAB Abstracts; bioRxiv/medRxiv); §2.4.1 asks for the complete strategy
of at least one major database, MeSH plus free words joined by Boolean logic, citation tracking or hand-searching, the
reference manager and the de-duplication method. Drop "表3" and the "Chinese standard" framing.

## Machine lines

```
表 1 研究方案主体报告框架内容	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	表 1 研究方案主体报告框架内容	corpus/knowledge/chinese-search-record-r39.md
（1）检索数据库（如 PubMed、Embase 等，含动物实验特殊数据库）	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	（1）检索数据库（如 PubMed、Embase 等，含动物实验特殊数据库）	corpus/knowledge/chinese-search-record-r39.md
（2）检索时间范围：	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	（2）检索时间范围：	corpus/knowledge/chinese-search-record-r39.md
检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）	corpus/knowledge/chinese-search-record-r39.md
（3）灰色文献的检索与记录	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	（3）灰色文献的检索与记录	corpus/knowledge/chinese-search-record-r39.md
尚无专门针对动物实验 SR 的报告规范	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	尚无专门针对动物实验 SR 的报告规范	corpus/knowledge/chinese-search-record-r39.md
目前应用于动物实验领域的 SR 和 Meta 分析在实施过程与报告撰写上尚缺乏统一规范	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	目前应用于动物实验领域的 SR 和 Meta 分析在实施过程与报告撰写上尚缺乏统一规范	corpus/knowledge/chinese-search-record-r39.md
研究者应至少提供一个主要数据库的完整检索策略，	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	研究者应至少提供一个主要数据库的完整检索策略，	corpus/knowledge/chinese-search-record-r39.md
展示所用主题词 （如 MeSH） 与自由词的组合，以及它	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	展示所用主题词 （如 MeSH） 与自由词的组合，以及它	corpus/knowledge/chinese-search-record-r39.md
```

VERDICT — attacked staged S116's 表3/module-3 and §2.1.1 claims against the `.txt` capture: module 3's three items and the absence-plus-PRISMA sentence hold verbatim, but "表3" is 表1 (a §1.3 protocol framework), the "Chinese standard" framing and the 2024-04-01 bound are not carried, and the entry omits 表2 and §2.4.1 — the document's actual search-record requirements.
