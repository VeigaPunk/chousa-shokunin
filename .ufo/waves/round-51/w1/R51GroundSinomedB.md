# R51GroundSinomedB — independent second pass on staged S119 (SinoMed record)

seat: R51GroundSinomedB, wave 1, round 51 — leaf member, no dispatch
document: staged **S119** (SinoMed record `ui=2026335073`) → planned lane id **S111**
capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/42bac8830527d6f1bb125c49.{txt,raw}`
url: `https://www.sinomed.ac.cn/article.do?ui=2026335073`
key check: `sha256(url)[:24]` recomputed = `42bac8830527d6f1bb125c49`, matches the filename.
forms: `.txt` read as **UTF-8** = 1,675 chars, sha256 `4d3bff50…c937671`; `.raw` decoded as **UTF-8** = 17,523 chars, sha256 `0d1c08a6…5663f572b`. Every offset below is in the form named on its line.
read discipline: no other seat's report opened (R51GroundSinomedA's included); no network; staged package and `.qcache` opened read-only; no `c1/c2/c3-count.py` run; no scratch dir created (inline `python3` heredocs only).

## Identity stamp (the document's own)

- **title (zh)** — `<title>` and the record heading: `系统评价/Meta分析中文献检索报告清单(PRISMA-S)解读`
- **title (en)** — printed under it: `Interpretation of PRISMA statement for reporting literature searches in systematic reviews(PRISMA-S)` (note: "PRISMA statement", not "PRISMA-S" — a translation artifact of the item's own page)
- **edition** — `来源出版物 中国循证医学杂志 卷：26 期：4`. Volume and issue only: **no year and no DOI exist in either form** — `年`=0, `DOI`=0, `doi`=0, `出版日期`=0, `更新日期`=0, `记录`=0. The only year-shaped tokens in the `.txt` are `PRISMA 2020` (×2, the guideline's name) and `©2016` (footer); the `.raw` adds `1999` (XHTML namespace), `2021`/`2025` (grant codes inside the *commented* 基金 row) and `2026` (×9, the record id and its JS call sites). None is a publication year.
- **host** — `中国生物医学文献服务系统` (title suffix, `.txt` 52); footer `©2016 中国医学科学院 北京协和医学院医学信息研究所/图书馆 … 京ICP备10218182`; contact `sinomed@imicams.ac.cn`; outbound hosts in the body: `doc.sinomed.ac.cn` (order form), `new.cnzz.com` (analytics), `www.adobe.com` (Flash), `www.imicams.ac.cn`, `www.w3.org` (DTD). No `https` href in the body.
- **record id** — hidden `input id="ui" value="2026335073"` (`.raw` 13895) and `/detailText.do;jsessionid=…?dbname=zh&sendSql=ui%3d2026335073` (`.raw` 4707).

## Field census — what the page actually carries

Rows in document order, matched as `class="cuhuise12a">LABEL：` in the `.raw`, with comment membership computed from the page's own `<!--`…`-->` spans:

| `.raw` offset | label | state |
|---|---|---|
| 6161 | 作者： | live |
| 7877 | 作者地址： | live, **value empty** (`<span class="huise">` closes with nothing between) |
| 8005 | 来源出版物： | live |
| 8306 | 关键词： | live |
| 8545 | 摘要： | live, **truncated mid-sentence** |
| 8978 | 学科分类号： | **commented out** (comment span 8929–9610) |
| 9135 | 主题词： | **commented out** (same span) |
| 9298 | 基金： | **commented out** (same span) |

The `.txt` text form is derived with comments dropped, which is measurable: `学科分类号` = **0** in `.txt` / 1 in `.raw`; `甘肃海智计划项目` (a 基金 line) = 0 / 1; `R-05;R-37;R348.3;R916.3` (the 学科分类号 codes) = 0 / 1. `主题词` = 1 in `.txt` and 3 in `.raw`, and the single `.txt` hit is the *widget* string `查看主题词相同的文献，请选择：`, not a field label. The controlled-vocabulary **values** (`*评价研究;*研究报告;Meta分析;*清单;质量控制`) survive in `.txt` only as checkbox labels of that widget.

## Located quotes — `.txt` read as UTF-8, `text.find()` offsets, each occurs exactly once

Twelve machine lines, columns `QUOTE`, staged-id, url, quote, entry-path (tab-separated, no header row):

```
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	系统评价/Meta分析中文献检索报告清单(PRISMA-S)解读 - 中国生物医学文献服务系统	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	Interpretation of PRISMA statement for reporting literature searches in systematic reviews(PRISMA-S)	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	中国循证医学杂志 卷：26 期：4	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	作者地址：	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	文献检索是系统评价(SR)的基石	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	作为“报告规范”的内在局限,并针对中文	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	查看主题词相同的文献，请选择：	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	质量控制	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	请登录后再使用此功能， 登录 。	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	最佳分辨率1024×768 建议使用IE7以上版本	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	销售服务：023-67033817 电子邮件：juhesinomed@vip.163.com	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	©2016 中国医学科学院 北京协和医学院医学信息研究所/图书馆 版权所有 京ICP备10218182	corpus/knowledge/chinese-search-record-r39.md
```

Offsets in that same order (`.txt`, UTF-8): 17, 321, 702, 672, 829, 1010, 1078, 1138, 1366, 1440, 1470, 1567. Lengths/chars: 47/3, 100/11, 17/3, 5/1, 16/1, 19/1, 15/1, 4/1, 16/3, 25/2, 46/2, 51/5 (chars/whitespace words) — all inside the ≤160-char, ≤25-word rule. Nine of the twelve are not the headline (title, English title, 来源出版物 are the obvious ones); the `作者地址：` quote is the empty-field datum, `作为“报告规范”的内在局限,并针对中文` is the truncation tail (note its ASCII `,`, which is how the abstract is punctuated — a full-width `，` variant matches nothing).

## Negative sweeps — exact counts, `str.count()` on the `.txt` read as UTF-8

```
searcher identity: 検索者=0  检索者=0  检索人员=0  検索担当=0   | extra 检索员=0  检索人=0
grey literature:   灰色文献=0  グレーリテラチャー=0  gray literature=0  | extra grey literature=0  灰色文献检索=0
hand-search:       ハンドサーチ=0  手検索=0  手工检索=0  | extra 手动检索=0  handsearch=0  hand-search=0  hand search=0
search date:       検索日=0  検索期間=0  检索时间=0  检索日期=0  | extra 检索日=0  检索年限=0  检索年份=0  检索截至=0
```

**Every one of these 26 terms is also 0 in the `.raw` decoded as UTF-8** — so the absence is not a text-extraction artifact. The four asked groups are therefore **all absent from this record**, which is what lets a staged "neither names the searcher" sentence carry its sweep for S119 (see finding 2).
Context counts, same forms: `检索` = 5 (`.txt`) / 11 (`.raw`) — only inside title, keywords and abstract, never as a field label; `数据库`=0, `策略`=0, `PubMed`=0, `CNKI`=0, `万方`=0, `维普`=0, `CBM`=0. The record that indexes a PRISMA-S interpretation carries **none** of PRISMA-S's search-process items: no database list, no strategy, no date bound, no searcher.

## Findings for the integrating L1 (depth, on the entry `corpus/knowledge/chinese-search-record-r39.md`)

1. **`学科分类号` and `主题词` are not fields of this page.** The staged `source:` line reads "the 来源出版物 / 关键词 / 主题词 / 学科分类号 fields". Both of the last two are commented-out rows (`.raw` 8929–9610), invisible to a reader and absent from the `.txt`. A defensible sentence: the live record carries 作者 / 作者地址 (empty) / 来源出版物 / 关键词 / 摘要, and the controlled vocabulary appears only as the labels of the `查看主题词相同的文献` widget. If the codes `R-05;R-37;R348.3;R916.3` are to be kept, they must be marked as coming from a commented-out row.
2. **The searcher sweep currently stops at S116/S117.** The entry's Unknown bullet says "Neither `S116`'s module list nor `S117`'s own record names the person who ran the search". S119 is not covered by that sentence; the sweep above now supplies it (0/4 asked terms, both forms), so the sentence can name three documents — or be left scoped as written, but then S119's own absence is unstated.
3. **"served only through a paid ordering service" is an inference, not printed text.** `订购`/`购买`/`付费`/`收费`/`全文` = 0 in both forms. What the page holds is `<!-- 原文索取的FORM -->` (`.raw` comment span 14278–14293) opening `<form name="frmMall" action="http://doc.sinomed.ac.cn/inter/JspShopCartService.jsp">` (`.raw` 14342) plus the visible sales line at `.txt` 1470. Word it as an inference from a shop-cart form action on `doc.sinomed.ac.cn`, and keep it next to the visible `销售服务` line (QUALITY 67 polarity: the page never says "paid").
4. **Do not let a recheck claim "the year is unchanged".** There is no year: 卷 26 期 4 is the whole edition statement. The staged `recheck:` clause "confirming … the journal/volume/issue are unchanged" is correct as written; a future edit that adds "year" would be unfalsifiable here.
5. **Form choice is load-bearing (QUALITY 76).** Five of the twelve quotes above occur **0** times in the `.raw` (markup interleaves them: `中国循证医学杂志<span …></span>卷：26…`), and `文献检索是系统评价(SR)的基石` occurs **2** times in the `.raw` (meta Description + body) while being unique in `.txt`. The span file for S119 must therefore be the `.txt` form, and the lesson must name it.
6. **Duplicate URL in the staged package.** `SOURCES.append.md:44` is S119 (docs) and `:66` is S141 (dataset), same URL; S141's own cell cites "20,142 bytes", which is exactly this `.raw`'s size. C2 requires *exactly one* lane Registry row carrying a bound URL, so the integration must land S119→S111 and must not also land S141's row (S141 is not one of the seven).

## Named limits

- Presence only: I did not read the item's full text (order-only) and its abstract is truncated at `.txt` 1024, so a term absent here is absent from a truncated abstract plus five live fields — **not** from the item.
- The page's JS could fetch fields after render (`/userInfo.do`, `doSubjectRelatedSearch`); a field absent from the served HTML could still exist behind a call. The capture is the served HTML, nothing more.
- Exact-substring sweeps cannot see a synonym I did not list; the term lists above are the asked four groups plus six extra terms I chose.
- I scored no claim: C1/C2/C3 counters were not run and no lane byte was read except the staged package and the lane registry's id column.

## Commands run (all observed)

`wc -c` and `sha256sum` on both capture files; `python3 -c` recomputing `sha256(url)[:24]`; inline `python3` heredocs reading both forms for: non-blank line dump, `count()`/`find()` on 26 sweep terms and 17 context terms, comment-span mapping, row-label census with comment membership, 4-digit-year enumeration, and per-quote uniqueness/length across both forms; `git rev-parse HEAD` + `grep -o '^| S[0-9]\{3\}'` on `corpus/SOURCES.md` (lane tip `cfe6c9fb…`, registry max S106, URL absent from the lane registry); `grep`/`sed` on `corpus/QUALITY.md` (criteria 25, 30, 67, 72, 76); `grep -n` on `merge/chousa/SOURCES.append.md` and `read` of the staged `chinese-search-record-r39.md`.

Tooling: nothing installed or upgraded (none needed); pacman untouched.

VERDICT — I attacked staged S119 as a source: the record's identity is 中国循证医学杂志 卷 26 期 4 with no year and no DOI, its live field set is five rows with 作者地址 empty, its 主题词/学科分类号/基金 rows are commented out in the served HTML (absent from the `.txt`), all four negative sweeps are 0/26 terms in both forms, and the staged entry's 学科分类号/主题词 field claim and its "paid ordering" wording need repair before binding; twelve unique located quotes with `.txt` offsets are supplied.
