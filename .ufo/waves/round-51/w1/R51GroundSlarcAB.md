# R51GroundSlarcAB — independent second pass on staged S116

seat: independent second pass on staged S116 (A-pass is `R51GroundSlarcAA`; that seat's report was not opened).
document: 实验动物与比较医学 2025;45(4):496-507 — `https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290`
intended lane entry: `corpus/knowledge/chinese-search-record-r39.md` (absent at lane tip `cfe6c9f`; entries go inside reports this round).
No network, no live fetch: every byte below is the on-disk capture. No tool installed (none needed); pacman paused, untouched.

## 1. Capture form and digests — the form every offset below indexes (QUALITY 76)

```
$ ls -la .../corpus-expansion-1/.qcache/ | grep fd468a36
-rw-r--r-- 1 vgpnk vgpnk 1156890 Oct 23 20:39 fd468a36d78ff156b6200946.pdf
-rw-r--r-- 1 vgpnk vgpnk 1156890 Oct 23 20:39 fd468a36d78ff156b6200946.raw
-rw-r--r-- 1 vgpnk vgpnk   82903 Oct 23 20:39 fd468a36d78ff156b6200946.txt
$ cmp -s fd468a36d78ff156b6200946.raw fd468a36d78ff156b6200946.pdf && echo identical
identical
```
`sha256sum`: `.txt` = `90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc` (82903 bytes, 52208 chars, 12 form feeds);
`.raw` = `72763389bbe95ab312de097125baa447370a244cb3f1b1bd3030b9956fb5abce`. `.pdf` and `.raw` are the same bytes.
FORM: **the `.txt` read as UTF-8**; every offset is `text.find(quote)` on that string.

## 2. The document's own identity stamp (nothing here comes from the URL)

| field | value | evidence |
|---|---|---|
| title (metadata) | `动物实验系统评价与Meta分析报告的规范撰写建议` | `.raw` `/Title<FEFF…>` decoded UTF-16BE |
| title (printed) | letter-spaced and split: `动 物 实 验 系 统 评 价 与 Meta 分 析 报 告 的 规 范 撰 写` then an unspaced `建议` | `.txt` char 1176 |
| journal + edition | `实验动物与比较医学 Laboratory Animal and Comparative Medicine`, `Aug. 2025, 45(4)`, page `496` | `.txt` char 0 (header line) |
| 文章编号 | `1674-5817（2025）04-0496-12` → 12 pages from 496 | `.txt` char 4106–4138 |
| DOI (dot form) | `10.12300/j.issn.1674-5817.2025.017` | char 121, char 52171 |
| DOI (hyphen form) | `10.12300/j.issn.1674-5817.2025-017` | char 51644 (引用本文) and `.raw` `/Subject` |
| dates | `收稿日期 2025-02-05`, `修回日期 2025-04-22` | char 50919, 51043 |
| PDF producer | `/Creator 方正飞翔9.0 XML版 9.0.0.1787`, `/Producer Founder`, `/CreationDate = /ModDate = D:20250901085908+08'00'` | `.raw` obj 1 |
| pages | 12 form feeds; page-number markers `498`@8600, `500`@16154, `502`@23188, `504`@30741, `506`@37028 | `.txt` |
| host | **absent**: `http` 0, `www.` 0, `.cn` 0, `slarc` 0, `org.cn` 0, `ISSN` 0, `CN ` 0 in `.txt`; no URL in `.raw` | counts |

Consequence: the URL's host (`www.slarc.org.cn`, path `…/dwyx/EN/…id=5290`) is **not corroborated by the document bytes**; identity rests on
文章编号 + DOI + journal header. A lane row keyed on the URL is fine, but the document cannot be used to prove the host or the `EN` vs `CN` path.

## 3. QUOTE machine lines (11; each occurs exactly once in this `.txt` **and** once across all seven theme captures)

```
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	1674-5817（2025）04-0496-12	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	（2）检索时间范围：	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	（3）灰色文献的检索与记录	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	尚无专门针对动物实验 SR 的报告规范	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	文献检索是 SR 的基础环节	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	研究者应至少提供一个主要数据库的完整检索策略	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	应简要说明是否采取了参考文献追溯	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	动物实验前瞻性注册库，追踪未发表或进行中研究	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	注：CBM 指中国生物医学文献数据库；CNKI 指中国知网	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	引文检索或手工查阅期刊等补充检索措施	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	其他途径 （如手工检索） 初步获得的文献总数	corpus/knowledge/chinese-search-record-r39.md
```
Offsets (chars, `.txt` UTF-8) in the order above: 4113, 15186, 15307, 17709, 22480, 22928, 23170, 24010, 24385, 24601, 29948.
All are 10–29 chars, ≤3 whitespace words, contain no tab and no `\n`; none is a title/abstract/keyword span.
Checked as `assemble-quotes.py` will check them: `{k: t.count(q) for k in seven captures}` printed `{'S116': 1}` for all eleven
(so none is lost to the S117 capture, which is the other `www.slarc.org.cn` file, `…CN/…id=5237`).
**Handoff**: the assembler keeps a quote only if it is also literally inside the entry, so each line above must be pasted into
`corpus/knowledge/chinese-search-record-r39.md` verbatim, spaces included (`（2）检索时间范围：` ends with a fullwidth colon).

## 4. Negative sweeps — exact counts in this `.txt` (UTF-8)

```
searcher identity   検索者 0  检索者 0  检索人员 0  検索担当 0  检索员 0  检索专家 0  图书馆员 0
                    信息专员 0  检索者姓名 0  检索人 0  执行检索 0  谁检索 0  由谁 0  独立检索 0  两名 0  2 名 0  检索由 0
grey literature     灰色文献 3  OpenGrey 1  gray literature 0  grey literature 0  Grey literature 0  グレーリテラチャー 0
hand-search         手工检索 1  手工查阅 1  引文检索 1  参考文献追溯 1  补充检索 1  hand-search 0  handsearch 0  ハンドサーチ 0  手検索 0
search date         检索时间 1  检索时间范围 1  时间范围 1  检索日期 0  检索期间 0  检索年限 0  検索日 0  検索期間 0  建库 0  截至 0  起始日期 0
context             检索 33  检索策略 8  检索数据库 1  检索式 0  表 1 2  表 2 2  表 3 1  表 4 0
```
ABSENT (so a staged "neither names the searcher" claim carries its sweep): **all four required searcher terms are 0** — 検索者, 检索者,
检索人员, 検索担当 — and nine further wordings (检索员, 检索专家, 图书馆员, 信息专员, 检索者姓名, 检索人, 执行检索, 谁检索, 由谁) plus three
procedural forms (独立检索, 两名, 检索由) are 0: 16 wordings, none present. Also absent: every English/Japanese grey-literature and hand-search term, and
检索日期 / 检索期间 / 検索日 / 検索期間.
PRESENT (so a "neither names grey literature" or "neither asks for hand-searching" claim would be **false**): 灰色文献 ×3 (char 15310 in 表1
module 3, 22645 in §2.4.1, 24033 in 表2), and hand-searching ×2 as a requirement (char 24601 §2.4.1, char 29948 §2.5.1).

## 5. Findings

**F1 — calibration: the staged locator's table number is wrong (表3 → 表1).** The module-3 row lives in **表 1**, not 表 3.
Captions: `表 1 研究方案主体报告框架内容` / `Table 1 Framework for main report of research protocol` (char 14179, printed p.499), and
`表 2 动物实验系统评价的数据库检索参考` / `Table 2 Retrieval references…` (char 23316, p.502). `表 3` occurs once, as `原文表 3` (char 33964,
p.504), quoting van Rhijn-Brouwer's own table 3 — not this document's. The staged row (`SOURCES.append.md:41`) and the staged entry
(`chinese-search-record-r39.md:4`) both say `表3 报告模块表, module 3 文献检索策略`; the correct locator is `表1, module 3 文献检索策略`.
The other half of that locator is sound: `2.1.1 遵循国际通用规范` is at char 17069 and its body carries the absence sentence (char 17709).

**F2 — depth: the "three items" reading is right for 表1 and under-reads the document.** 表1 module 3 prints `(1) 检索数据库…含动物实验特殊数据库`,
`(2) 检索时间范围：` + `检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）`, `(3) 灰色文献的检索与记录` — three printed numbers, four requirements.
But §2.4.1 (`文献检索策略`, char 22408) adds requirements the staged entry never cites: a four-part framework
`通用数据库+动物研究专用数据库+灰色文献/预印…` (char 22629, prose continues `本平台）` after the column join), at least one full database
strategy (`研究者应至少提供一个主要数据库的完整检索策略`, char 22928) with Boolean logic, reference-list chasing (`应简要说明是否采取了参考文献追溯`,
char 23170), and reference-manager + deduplication (`引文检索或手工查阅期刊等补充检索措施`, char 24601). 表2 (char 23316) additionally
names `Animal Study Registry` (char 23955, its description `动物实验前瞻性注册库…` at 24010), `ProQuest Dissertations & Theses、EThOS 等`
(char 24136), `CAB Abstracts` (char 24223) and `bioRxiv、medRxiv 等` (char 24298).
An entry that says the document asks for three things is true of 表1 only; the document asks for at least six.

**F3 — depth/correction: S116 itself asks for hand-searching; the staged entry reaches that requirement only through the Japanese S097.** Its
Inference says grey literature "is the Chinese requirement the lane's Western anchors do not carry" and that the Japanese hand-search field is
"the same requirement in a different literature", so the Chinese side is represented by grey literature alone. §2.5.1 makes hand-searching a
*reported count*: `其他途径 （如手工检索） 初步获得的文献总数` (char 29948) alongside the database total and the post-deduplication remainder.
The "two literatures" claim survives and gets stronger; the attribution does not — S116 is the second literature, and it states the requirement
twice (char 24601 §2.4.1, char 29948 §2.5.1).

**F4 — calibration: the date field is table-only.** `检索时间范围` exists once, inside 表1 module 3 (char 15189). §2.4.1's span
(chars 22408–24775) contains `时间` 0 and `日期` 0. The document states no concrete period for any search (`建库` 0, `截至` 0, `起始日期` 0;
the only dates in the file are its own `2025-02-05` / `2025-04-22` receipt dates). A lane claim that this document demands a time range but
supplies no timestamp vocabulary beyond `检索时间范围` is exact; a claim that it demands a search *date* (a per-run timestamp) is not supported.

**F5 — calibration: the document prints its own DOI two ways.** Dot form twice (char 121 header, char 52171 last reference block), hyphen form
once (char 51644 `引用本文`, mirrored in `.raw` `/Subject`). The staged row's `doi` field uses the dot form, which is the majority and the
header form — correct, and worth stating in the lane row because a reader who copies `引用本文` gets a different string.

## 6. Not done / out of scope
Did not open any other seat's report, did not run `c1/c2/c3-count.py`, did not touch the staged package, the lane registry, the git index or any
production file; no network. Scratch `/dev/shm/chousa-r51-R51GroundSlarcAB/` deleted after the runs above.

VERDICT: attacked staged S116 for identity, four-plus located quotes and four negative sweeps — identity holds on 文章编号+DOI+journal header (host not in the bytes), 11 cross-capture-unique quotes located, searcher-identity absent under 16 wordings (sweep carries), grey literature and hand-search present (so "neither names" is false for both), and the staged locator's 表3 is a drift from the document's 表1.
