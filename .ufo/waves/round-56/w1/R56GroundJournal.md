# R56GroundJournal — S129 grounded: the journal-hosted 药品临床综合评价工作流程指南

Seat: leaf member, no dispatch. Target lane row S129 (staged S155, renumbered by document); base `e5a37951`, lane HEAD `99eff0e`
(C2 integration) when read. Sources opened read-only from the campaign cache (no fetch; L0 `8d77e6c1` open). Writes: this report only,
plus scratch `/fast/scratch/hyaku/chousa-r56/R56GroundJournal` (deleted). No tool installed or upgraded (pdftotext already present, pacman
paused host-wide), so no tool/version/channel line to record.

## 1. Identity exactly as printed

```
$ wc -c / sha256sum …/5233bf47babaa1ca2b49ed15.txt
118594 bytes; 80,732 characters read as text; beac2b7feb425a8885927850ea79ed5e916339c6f5cd4b45c3abbf1753f49b05
$ pdfinfo …/5233bf47babaa1ca2b49ed15.pdf | grep -E "Title|Pages"     -> Title: 药品临床综合评价工作流程指南 / Pages: 13
```

- journal **中国药房** (`China Pharmacy` on every masthead); **2025 年第 36 卷第 19 期** = `China Pharmacy 2025 Vol. 36 No. 19` (page-1 footer,
  char 3505, 128 chars, 15 ws words, one line, occurs once).
- **中图分类号 R98**, **文献标志码 A**, **文章编号 1001-0408（2025）19-2353-13** (char 491); **DOI 10.6039/j.issn.1001-0408.2025.19.01** (char 529).
- **pages 2353–2365**: the thirteen footers `·2353·`…`·2365·` (`re.findall(r"·(\d{4})·", form)` returns exactly those 13) and the article
  number's `-2353-13` (start 2353 + 13 pages); `pdfinfo` independently reports 13 pages.
- title as printed `药品临床综合评价工作流程指南Δ` (char 10; Δ carries the 基金项目 note at char 3072).

## 2. The 灰色文献 row: exact text, offset, and where its grade sits

Row, char **22564**, 49 chars, 4 whitespace words, ONE line, occurs ONCE (`form.count`=1):

```
灰色文献 未公开发表的研究信息，可能包含了最新的研究成果和观点           Ⅰ级    A
```

Grade cells sit inside that same line: `Ⅰ级` at char **22606** (line index 42), `A` at char **22612** (index 48).
**It is a 表7 row, not 表10.** `表7    药品临床综合评价的信息来源情况` is at char **20520**, its header row
`信息来源                 信息内容                证据等级 推荐强度` at 20610, and its nine source rows each carry a `Ⅰ级 … A` pair at
20727 文献数据库, 21156 官方网站, 21376 书籍专著, 21480 临床试验注册数据库, 21685 生产企业, 21896 问卷调查, 22086 临床资料数据库,
22564 灰色文献, 22614 搜索引擎. The cache `.txt` prints 表10's title (char 22467) in the two-column page's right column, on the line above
the row; it does not carry the row. Independent extractor: `pdftotext` order is 表7 13017 < 灰色文献 13591 < 表8 13653 < 表10 14578.

## 3. Is "the highest grade in its table" true?

- Evidence axis, `表1    证据分级标准` (char 13373), **five** levels: `Ⅰ级 … 系统评价、卫生技术评估、Meta分析` (13495), Ⅱ级 13569, Ⅲ级 13681,
  Ⅳ级 13720, Ⅴ级 13794. Recommendation axis, `表2   推荐强度分级标准` (char 8805), **four** grades: `A … 推荐，证据极有效（证据等级为Ⅰ级）`
  (8950), B 8977, C 9077, D 9165.

So Ⅰ级 tops five and A tops four: the statement is **true on the guideline's own scales**, but **vacuous as a ranking inside 表7** — all
nine source rows carry Ⅰ级/A, so the pair ranks 灰色文献 above nothing (the entry says this correctly: "attaches Ⅰ级 and A to each row").
Two facts to keep beside it: (i) 表1 defines Ⅰ级 as `系统评价、卫生技术评估、Meta分析`, a research-type definition that does not describe
unpublished literature, so Ⅰ级 beside 灰色文献 cannot be read against 表1; (ii) 表2 defines A as `证据等级为Ⅰ级`, i.e. the pair is a
recommendation-strength cell attached to the source class.

## 4. The 中国循证医学中心 adoption sentence

- Abstract: `采用中国循证医学中心的证据分级体系进行证据分级评价` — char **759**, 25 chars, one line, once.
- Body 5.5: `本指南为管理型指南，采用中国循证医学中心的证` — char **12949**, continuing `据分级体系，将证据分为 5 级，证据分级标准见表 1`
  (char 13055) and `推荐强度分为 4 级` (char 13300): the published text adopts the centre's five-level evidence scale and the Oxford CEBM
  four-level recommendation scale, in the abstract and again in 5.5.
- `中国循证医学中心` occurs 2 times; the affiliation `天津中医药大学循证医学中心` (char 322) does not contain the string.

## 5. Comparison with the ttbz standard text (`b27ffd2f…txt`, 70,038 chars)

The 灰色文献 wording is **NOT identical**. `diff -u` of the two passages:

```
-灰色文献 未公开发表的研究信息，可能包含了最新的研究成果和观点           Ⅰ级    A
+（9）灰色文献：未公开发表研究信息，可能包含了最新的研究成果和观点，能够研究
+提供新的研究思路和方向。
```

Three material differences: (a) the journal inserts `的` (`未公开发表的研究信息` vs `未公开发表研究信息`); (b) the draft adds a clause,
`能够研究提供新的研究思路和方向` (sic: `能够研究` + newline `提供`); (c) the form — the journal prints a table row with grade cells, the
draft prints numbered item (9) under 7.2.3.3 with **no per-item grade**; its one grade line `（证据等级：I 级；推荐强度：A）` (char 24815)
follows item (10) 搜索引擎 and covers the whole list (`[31,35,79-82]` at 24837). The scales differ too: the draft's combined
`表 1 证据分级与推荐强度分级` (8366) gives `Ⅰ级 … 系统评价、HTA、Meta 分析` (8432) and `A  推荐，证据及有效（证据等级为 1 级）` (8725 — HTA
abbreviation, typo `及`, Arabic `1`), against the journal's split 表1/表2 and `证据极有效`/`Ⅰ级`. The draft is for comment:
`T/CLPA XXXX—2025` (166), `（征求意见稿）` (360), `2025 - XX - XX 发布` (425).

## 6. Re-measured S129 lane rows (report only; no lane file edited)

`corpus/evidence/round56/spans.tsv` holds 6 S129 rows (S129-1…6), `quotes.tsv` 6. Per row: `form[offset:offset+len(span)] == span` 6/6,
quote inside its span 6/6, `len(span) > len(quote)` 6/6, `form.count(quote) == 1` 6/6, no newline in the quote 6/6, digest `beac2b7f…`
equals the sha256 of the `.txt`. The offsets are span starts (0, 3510, 22459, 22484, 8870, 668), each 80 chars before the entry's own
`char` for that quote (10, 3590, 22539, 22564, 8950, 748) — consistent with "longer than its quote".

Findings against the landed entry (frozen claims untouched; reported, not patched):

- **F1 — row misattributed.** `source:` line 5 and Observation line 18 call it a `表 10   其他研究…` row (entry: `表 10` ×3, `表7`/`表 7` ×0);
  it is 表7 (header 20520; second extractor 表7 13017 < 灰色文献 13591 < 表8 13653). The bytes are right, the table name is not.
- **F2 — identity incomplete.** The entry has `中国药房 2025 vol. 36 no. 19` but no pages and no DOI (`10.6039` ×0, `2365` ×0; its only `2353`
  is inside the footer quote). Printed: 中国药房 2025, 36(19): 2353–2365, doi:10.6039/j.issn.1001-0408.2025.19.01.
- **F3 — grading half-answered.** The entry states Ⅰ级/A is on every row (true, 9/9) but never shows Ⅰ级/A topping a 5-level / 4-level scale
  (no 表1/表2 line in entry or lesson) nor reconciles 表1's Ⅰ级 definition; from the entry alone "highest grade" is untestable.
- **F4 — offset semantics unstated.** spans.tsv records span starts, the entry records quote chars; consistent, but the files do not say so.

## 7. QUOTE lines (machine form; lane id S129)

```
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	药品临床综合评价工作流程指南Δ	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	文章编号        1001-0408（2025）19-2353-13	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	DOI    10.6039/j.issn.1001-0408.2025.19.01	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	表7    药品临床综合评价的信息来源情况	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	灰色文献 未公开发表的研究信息，可能包含了最新的研究成果和观点           Ⅰ级    A	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	Ⅰ级                          系统评价、卫生技术评估、Meta分析	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	A        推荐，证据极有效（证据等级为Ⅰ级）	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	本指南为管理型指南，采用中国循证医学中心的证	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	采用中国循证医学中心的证据分级体系进行证据分级评价	corpus/knowledge/grey-literature-field-china-r42.md
```

Offsets in order: 10, 491, 529, 20520, 22564, 13495, 8950, 12949, 759 (`form.find` on the `.txt`). Lines 1, 5, 6, 7 already occur in the
entry/lesson; 491, 529, 20520, 12949, 759 do not — landing them is the C2 owner's call.

## 8. Limits

- One pair only (S129 vs S127); S128/S130/S118 not re-measured here. No network: the `.txt` capture is the C2-defined form, the PDF was an
  independent cross-check (`pdftotext`), not an offset source.
- C1 untouched (no gate/battery/probe/counter run); `c2-count.py` not run — C2 is the L1's measurement and this seat reports facts, not C2.
- `spans/S129-*.txt` read and compared, not rewritten; entry, lesson, spans.tsv, quotes.tsv unchanged by this seat.

VERDICT: attacked/grounded the journal-hosted copy (S129) of 药品临床综合评价工作流程指南 — identity, 灰色文献 row, grade scale, 中国循证医学中心
adoption and the ttbz comparison SURVIVE (9/9 quotes byte-exact, unique, one line; 6/6 spans exact slices), with four findings reported on the
landed entry (row attributed to 表 10 not 表 7; pages/DOI missing; "highest grade" untestable from the entry; span-vs-quote offsets unlabelled).
