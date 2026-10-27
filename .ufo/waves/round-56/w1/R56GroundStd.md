# R56GroundStd — S127 grounding: the ttbz.org.cn text of 药品临床综合评价工作流程指南 (2025 版)

Seat `R56GroundStd`, round 56 wave 1, leaf. Target lane row S127 (`https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf`);
defined text form `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/b27ffd2f0161104c6a28c9f5.txt`
(read with `open(p, encoding='utf-8', errors='replace').read()`, universal newlines). All offsets = `form.find(quote)`.

## Form and provenance
```
$ python3 -c "import hashlib;print(hashlib.sha256('https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf'.encode()).hexdigest()[:24])"
b27ffd2f0161104c6a28c9f5            # sha256(URL)[:24] == capture filename key
$ sha256sum b27ffd2f0161104c6a28c9f5.{txt,raw,pdf}
23306b9f84c95b06008ab5e4a5deaeb9b0e937041f5239ec57792710480f1d5d  .txt   (120386 bytes, 70038 chars, 1818 lines, 0 CR)
51550c5c6b0537f02162fa637c903f60044aef13f481c4e5c2111d7cd1bf1b57  .raw == .pdf (cmp)
$ pdfinfo …pdf -> Pages 39, A4, Producer Microsoft® Word 2021, CreationDate Mon Apr 7 04:57:16 2025 -03
```
`.txt` digest equals the `capture_sha256` the lane records for S127 in `corpus/evidence/round56/spans.tsv`. PDF metadata is
not printed text (cited only as "not printed"). Printed page 11 = PDF page 15 (per-page `pdftotext … | grep 灰色文献`).

## Identity — only what the form prints
- `ICS 11.020` (0), `CCS C 50` (11), type line `团                       体                          标                            准` (24).
- Number `T/CLPA XXXX—2025` (166, em dash); body running head `T/CLPA XXXX-2025` with hyphen, 38×.
- Title `药品临床综合评价工作流程指南` (200) + `（2025 版）` (232; repeated at 4514/4552 on the 范围 page); English
  title at 247 (**unique**); status `（征求意见稿）` (360).
- Dates: `2025 - XX - XX 发布` (425) … `2025 - XX - XX 实施` (472) — placeholders, no date is issued.
- Publisher line `中国药师协会             发 布` (519).
- 提出 `本文件由中国药师协会药品临床评价工作委员会提出。` (2490); 归口 `本文件由中国药师协会归口。` (2519).
- 起草单位 (2537): 中国药师协会药品临床评价工作委员会；天津市药品使用监测和临床综合评价中心；天津医科大学总医院.
- 主要起草人 (2598): 李正翔（天津医科大学总医院）, then `（以下按姓名笔画排序）` (2626); the list ends with `本文件主要执笔人` (3592) 段蓉（天津医科大学总医院）, 文件工作组, and `本文件为首次发布。` (3704). Drafting basis: `GB/T1.1-2020` (2366), `GB/T\n20001.7-2017` (2402).
- Scope (4570): `本文件确立了药品临床综合评价工作的主要流程及相关技术环节。`

## The 灰色文献 row
Section head `7.2.3.3 信息来源` at 23809; the source list is **prose items （1）–（10）, not a table**:
```
（9）灰色文献：未公开发表研究信息，可能包含了最新的研究成果和观点，能够研究
提供新的研究思路和方向。                       # char 24624, item 9 of 10
```
**No 证据等级 / 推荐强度 on that row.** `"证据等级" in form[24624:24791]` → False; the nearest annotation is 195 chars
later, after item （10）. `灰色文献` occurs **once** in the whole 70038-char form, so 表 1 never grades it. `表 1 证据分级
与推荐强度分级` (8366) prints only five level rows — `Ⅰ级 系统评价、HTA、Meta 分析`, `Ⅱ级 政府及相关机构报告`,
`Ⅲ级 有确切研究方法的文献`, `Ⅳ级 综述`, `Ⅴ级 专家意见` — and four strengths A–D; it has no source rows.

## Where 搜索引擎 sits
Item （10）, immediately after （9）, across the page break: `（10）搜索引擎：公众/媒体关注度等补充数据。` (24791). The draft
prints one annotation and one reference line closing the **whole** list: `（证据等级：I 级；推荐强度：A）` (the form's
occurrence at 24819, Latin `I`, not 表 1's fullwidth `Ⅰ`; the string's first occurrence is 18560) and `[31,35,79-82]` (24849). That close is section-level, not item-level: the same string closes
7.2.3.2.6 and 7.2.4 (`count` 31 Latin-I form; 14 use `Ⅰ级`; `证据等级` 79×). So on S127 no source item is graded.

## The adoption sentence (grading systems), 6.2 证据分级与依据
Two consecutive form lines, 8242 and 8285: `将百度等公共搜索引擎及 AI 检索工具作为补充检索。本指南为管理型指南，采用中国循证` /
`医学中心中国循证医学中心的证据质量分级体系，采用牛津大学循证医学中心制定的推荐强` / `度分级标准，见表 1。` The centre's name
is printed **twice in a row** — a draft typo, not an extraction artifact: `pdftotext -layout -f 7 -l 7` prints it identically
(its lines 26–27). Rows 8–9 below reproduce each line byte-exactly, duplication included.

## What the form does NOT print
1. **No grade on the 灰色文献 row** — no Ⅰ级/A beside grey literature anywhere. The grade-per-row form exists only in the
   *journal* copy (S129): `pdftotext -layout` page 5 of `5233bf47babaa1ca2b49ed15.pdf` prints `灰色文献 未公开发表的研究信息，
   可能包含了最新的研究成果和观点 Ⅰ级 A` and `搜索引擎 公众/媒体关注度等补充数据 Ⅰ级 A` as table rows. The staged entry's
   "grades it Ⅰ级 with A" is therefore true of S155/S129, **not of S168/S127**.
2. **No source→grade table**; the only printed table there is 表 1 (levels/strengths by study type).
3. **No assigned number, no dates**: `XXXX` and `XX - XX - XX` are placeholders — it is a 征求意见稿.
4. **No 编制说明 content** (task origin, dated method stages) — that is the separate S128 document.
5. **Wording differs from the journal copy**: S127 `未公开发表研究信息` vs S129 `未公开发表的研究信息` (the staged `recheck:` line
   quotes the S129 wording).
6. No search date, hit counts, or 检索 strategy table beyond the 6.2 database list.

## Cross-check of the lane's existing S127 rows (read-only)
`corpus/evidence/round56/spans.tsv` has 9 S127 rows; I verified each `span_file` == `form[offset:offset+len]`, each quote at
`offset+80`, span longer than quote (window convention: offset = quote_start − 80). My rows carry the true `find` offsets.

## QUOTE machine lines (13; each `count==1`, one line, ≤25 whitespace words, ≤160 chars)
```
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	T/CLPA XXXX—2025	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	Guideline for the workflow of comprehensive clinical evaluation of drugs	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	（征求意见稿）	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	2025 - XX - XX 发布	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	本文件由中国药师协会药品临床评价工作委员会提出。	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	本文件由中国药师协会归口。	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	本文件确立了药品临床综合评价工作的主要流程及相关技术环节。	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	将百度等公共搜索引擎及 AI 检索工具作为补充检索。本指南为管理型指南，采用中国循证	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	医学中心中国循证医学中心的证据质量分级体系，采用牛津大学循证医学中心制定的推荐强	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	表 1 证据分级与推荐强度分级	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	Ⅱ级                                政府及相关机构报告	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	（9）灰色文献：未公开发表研究信息，可能包含了最新的研究成果和观点，能够研究	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	（10）搜索引擎：公众/媒体关注度等补充数据。	corpus/knowledge/grey-literature-field-china-r42.md
```

## 160-char contexts (80 chars either side; `\n`/`\f` escaped; range = form slice)
```
ctx t[86:262] (len 176; quote at 166, 16 ch, 2 word):                   准\n                                                            T/CLPA XXXX—2025\n\n\n\n\n             药品临床综合评价工作流程指南\n                 （2025 版）\n\n     Guideline for t
ctx t[167:399] (len 232; quote at 247, 72 ch, 10 word): /CLPA XXXX—2025\n\n\n\n\n             药品临床综合评价工作流程指南\n                 （2025 版）\n\n     Guideline for the workflow of comprehensive clinical evaluation of drugs\n\n\n\n\n                                    （征求意见稿）\n\n\n\n\n               在提交反馈意见时，请将您
ctx t[280:447] (len 167; quote at 360, 7 ch, 1 word): prehensive clinical evaluation of drugs\n\n\n\n\n                                    （征求意见稿）\n\n\n\n\n               在提交反馈意见时，请将您知道的相关专利连同支持性文件一并附上。\n\n\n\n\n  2025 - XX - XX 发布     
ctx t[345:522] (len 177; quote at 425, 17 ch, 6 word):                （征求意见稿）\n\n\n\n\n               在提交反馈意见时，请将您知道的相关专利连同支持性文件一并附上。\n\n\n\n\n  2025 - XX - XX 发布                              2025 - XX - XX 实施\n\n\n                           中国药
ctx t[2410:2594] (len 184; quote at 2490, 24 ch, 1 word): 01.7-2017《标准编写规则 第7部分：指南标准》的规定起草。\n    请注意本文件的某些内容可能涉及专利。本文件的发布机构不承担识别专利的责任。\n    本文件由中国药师协会药品临床评价工作委员会提出。\n    本文件由中国药师协会归口。\n    本文件起草单位：中国药师协会药品临床评价工作委员会；天津市药品使用监测和临床\n综合评价中心；天津医科大学总医院。\n
ctx t[2439:2612] (len 173; quote at 2519, 13 ch, 1 word): 定起草。\n    请注意本文件的某些内容可能涉及专利。本文件的发布机构不承担识别专利的责任。\n    本文件由中国药师协会药品临床评价工作委员会提出。\n    本文件由中国药师协会归口。\n    本文件起草单位：中国药师协会药品临床评价工作委员会；天津市药品使用监测和临床\n综合评价中心；天津医科大学总医院。\n    本文件主要起草人：李正翔（天
ctx t[4490:4679] (len 189; quote at 4570, 29 ch, 1 word): XX-2025\n\n\n              药品临床综合评价工作流程指南\n                       （2025 版）\n\n1 范围\n\n  本文件确立了药品临床综合评价工作的主要流程及相关技术环节。\n  本文件适用于开展药品临床综合评价工作的各类人员，包括但不限于政策决策人员和管\n理执行人员、医疗机构专业技术人员、大专院校科研人员、企事业单位相关从业人员等
ctx t[8162:8364] (len 202; quote at 8242, 42 ch, 3 word): e、中国生物医学文献数据库、万方、中国期刊全文数据库和维普数据库），官方网站\n（国际和各国卫生行政主管部门、药监部门、医疗保障部门或相关行业协会官方网站）；并\n将百度等公共搜索引擎及 AI 检索工具作为补充检索。本指南为管理型指南，采用中国循证\n医学中心中国循证医学中心的证据质量分级体系，采用牛津大学循证医学中心制定的推荐强\n度分级标准，见表 1。\n                          
ctx t[8205:8405] (len 200; quote at 8285, 40 ch, 1 word): 各国卫生行政主管部门、药监部门、医疗保障部门或相关行业协会官方网站）；并\n将百度等公共搜索引擎及 AI 检索工具作为补充检索。本指南为管理型指南，采用中国循证\n医学中心中国循证医学中心的证据质量分级体系，采用牛津大学循证医学中心制定的推荐强\n度分级标准，见表 1。\n                            表 1 证据分级与推荐强度分级\n 证据质量级别                
ctx t[8286:8461] (len 175; quote at 8366, 15 ch, 3 word): 学中心中国循证医学中心的证据质量分级体系，采用牛津大学循证医学中心制定的推荐强\n度分级标准，见表 1。\n                            表 1 证据分级与推荐强度分级\n 证据质量级别                                        描述\n     Ⅰ级                      
ctx t[8411:8614] (len 203; quote at 8491, 43 ch, 2 word):                   描述\n     Ⅰ级                              系统评价、HTA、Meta 分析\n     Ⅱ级                                政府及相关机构报告\n     Ⅲ级                               有确切研究方法的文献\n     Ⅳ级                       
ctx t[24544:24742] (len 198; quote at 24624, 38 ch, 1 word):  （8）数据库：卫生信息系统数据、医疗保险数据库、药品供应销售及采购数据库、药\n品临床有效性数据库、不良反应监测数据库、其他主要人口健康相关数据库等。\n    （9）灰色文献：未公开发表研究信息，可能包含了最新的研究成果和观点，能够研究\n提供新的研究思路和方向。\n\n\n                                                  11\n\f          
ctx t[24711:24894] (len 183; quote at 24791, 23 ch, 1 word):                  11\n\f                                     T/CLPA XXXX-2025\n\n    （10）搜索引擎：公众/媒体关注度等补充数据。\n    （证据等级：I 级；推荐强度：A）\n            [31,35,79-82]\n7.2.4 研究类型\n    根据研究目的、研究设计、评价维度
```

## Limits
No `c2-count.py`, `inference-ground.py` or `quote-substance-check.py` run (not this seat's target). No lane/production write
other than this report; no network; no git/jj mutation; no tool installs. Scratch `/fast/scratch/hyaku/chousa-r56/R56GroundStd`
removed. S129's 表 10 caption↔table binding is a column-interleaving artifact; only its row text is reported.

VERDICT: built the S127 grounding — draft identity (T/CLPA XXXX—2025, 征求意见稿, 中国药师协会 提出/归口), the ungraded
prose 灰色文献 row at char 24624, 搜索引擎 as item (10) at 24791 with the section-level `Ⅰ级/A` close at 24819, and the
中国循证医学中心 + Oxford adoption sentence at 8242/8285 — survives; 13 byte-exact single-occurrence QUOTE rows with
offsets and 160-char contexts; grade-on-the-row is printed only in S129's published table, never on S127.
