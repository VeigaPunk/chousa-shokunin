# R51GroundSinomedA — re-ground staged S119 (SinoMed ui=2026335073, 中国循证医学杂志 26(4))

Target: `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/chinese-search-record-r39.md`, its `source: S119` line.
Staged row: `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md:44`. Lane target path: `corpus/knowledge/chinese-search-record-r39.md`
(planned lane id S111; registry max S106 at `corpus/SOURCES.md:116`).
Capture: `.qcache/42bac8830527d6f1bb125c49.txt` and `.qcache/42bac8830527d6f1bb125c49.raw`, URL `https://www.sinomed.ac.cn/article.do?ui=2026335073`.
**Forms used: the `.txt` read as UTF-8, 2,065 characters (2,969 bytes); the `.raw` decoded as UTF-8, 17,996 characters (20,142 bytes).**

## 1. Capture identity (observed)

```
$ python3 -c "import hashlib;print(hashlib.sha256(b'https://www.sinomed.ac.cn/article.do?ui=2026335073').hexdigest()[:24])"
42bac8830527d6f1bb125c49            # cache key = sha256(url)[:24] — matches the filename exactly
$ wc -c 42bac8830527d6f1bb125c49.txt 42bac8830527d6f1bb125c49.raw
2969 ...txt     20142 ...raw
$ sha256sum 42bac8830527d6f1bb125c49.txt 42bac8830527d6f1bb125c49.raw
4d3bff5067b4cf8e81980618696fdd28c4457f6e64d361b1164b60625c937671  ...txt
0d1c08a6ca7ee09a59c9ff7cef06841b088628135216e93caa8124b5663f572b  ...raw
$ python3 -c "print(len(open('...txt',encoding='utf-8').read()))"  → 2065
$ python3 -c "print(len(open('...raw',encoding='utf-8').read()))"  → 17996
$ stat -c '%y' ...txt                                              → 2026-10-23 20:39:54   # staged "page read 2026-10-23" holds
```

The `.txt` is a **rendered-text extraction: every HTML comment is stripped** — `<!--` = 0, `加入用户信息` = 0, `加载结果页面` = 0,
`原文索取` = 0, `cuhuise12a` = 0 in the `.txt`, while the `.raw` carries 15 comment spans. That one fact decides §2 and §4.

## 2. What the index records for this item, field by field, form by form

| field | `.txt` (rendered) | `.raw` | where |
|---|---|---|---|
| 来源出版物 | present | present | raw 8274, txt 896 |
| 关键词 | five terms, one per line | same | raw 8557 |
| 主题词 | the five headings present, but only as the link list under `查看主题词相同的文献，请选择：` — the **`主题词：` label is not rendered** | label + values 9429–9512, **inside comment 9192–9908**; also hidden input `id="subject"` at 14012 | raw only for the field |
| 学科分类号 | **absent — 0 occurrences** | `学科分类号：` at 9264, values at 9302, **inside the same comment 9192–9908** | raw only |
| 基金 | absent | five grant numbers, 9517–9905, same comment | raw only |
| 作者地址 | present, empty | present, empty | raw 8240 |
| year / DOI / ISSN / pages | absent | absent (`年：`=0, `DOI`=0, `ISSN`=0, `页码`=0) | — |
| record id | absent from the text | `id="ui" value="2026335073"` at 14280; `ui%3d2026335073` in the `/detailText.do` href at 4739 | raw only |

## 3. Located quotes (each exactly once in the stated form; offsets are `text.find(quote)`)

- **`.txt` 29** `系统评价/Meta分析中文献检索报告清单(PRISMA-S)解读 - 中国生物医学文献服务系统` — supports: this page is the SinoMed record
  for the Chinese PRISMA-S interpretation, and the host names itself 中国生物医学文献服务系统. Does **not** support journal, volume, issue, year.
- **`.txt` 896** `来源出版物： 中国循证医学杂志 卷：26 期：4` (one space after `：`) — supports: journal + volume 26 + issue 4, exactly the
  staged `recheck:` string. Does **not** support a publication year, a page range, a DOI or an ISSN — the record carries none of them.
- **`.txt` 1168** `包含16个条目的专项规范` — supports: the item is a 16-item specification, the count the entry's Inference leans on.
  Does **not** support the item list: the abstract is cut at `并针对中文` (txt 1258 / raw 9134), mid-sentence, by the index.
- **`.txt` 1334** `查看主题词相同的文献，请选择：` — supports: the five subject headings are rendered as a link list. Does **not** support
  that a `主题词：` field label is displayed (that label is in the comment, raw 9429).
- **`.txt` 1706** `请登录后再使用此功能， 登录 。` — supports: page features sit behind a login gate. Does **not** support a fee, a price,
  an order flow, or that full text is reachable only this way.
- **`.txt` 1930** `©2016 中国医学科学院 北京协和医学院医学信息研究所/图书馆 版权所有 京ICP备10218182` — supports: the operator identity of
  the index (the institute that runs SinoMed). Does **not** support "national"/国家 (that word is absent) nor recency.
- **`.raw` 9264** `学科分类号：` — supports: a 学科分类号 field exists in the record. Does **not** support that it is displayed (9264 lies
  inside comment 9192–9908), nor that the marks are 中图法 (no such label appears).
- **`.raw` 9302** `R-05;R-37;R348.3;R916.3` — supports the four class marks the record assigns. Does **not** support any subject label per mark.
- **`.raw` 14686** `<!-- 原文索取的FORM -->` — supports: a full-text-request form is present in the page source, under a comment label.
  Does **not** support "paid", a fee, or exclusivity of that route.
- **`.raw` 14741** `http://doc.sinomed.ac.cn/inter/JspShopCartService.jsp` — supports: the request form posts to a **shop-cart** service, i.e.
  an ordering mechanism exists. Does **not** support a price, a delivery term, or that the index itself holds the PDF (`pdf`=0, `全文`=0).
- **`.raw` 4739** `/detailText.do;jsessionid=E6BA7348F63277E6F1E9B6F5AFBF2362?dbname=zh&sendSql=ui%3d2026335073` — supports: a **second**
  in-index route to this record's detail text; does **not** support (or refute) that it serves full text — I did not fetch it; it weakens "only".

### Machine lines

```
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	系统评价/Meta分析中文献检索报告清单(PRISMA-S)解读 - 中国生物医学文献服务系统	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	来源出版物： 中国循证医学杂志 卷：26 期：4	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	包含16个条目的专项规范	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	查看主题词相同的文献，请选择：	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	请登录后再使用此功能， 登录 。	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	©2016 中国医学科学院 北京协和医学院医学信息研究所/图书馆 版权所有 京ICP备10218182	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	学科分类号：	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	R-05;R-37;R348.3;R916.3	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	<!-- 原文索取的FORM -->	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	http://doc.sinomed.ac.cn/inter/JspShopCartService.jsp	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	/detailText.do;jsessionid=E6BA7348F63277E6F1E9B6F5AFBF2362?dbname=zh&sendSql=ui%3d2026335073	corpus/knowledge/chinese-search-record-r39.md
```

## 4. Staged claims about this document that the capture does not carry

1. **"Its full text is served only through a paid ordering service from that index"** (entry, Observation) and the row's "the index serves
   the full text only through a paid document-ordering service". `付费`=0, `订购`=0, `价格`=0, `费用`=0 in **both** forms. What exists is a
   login gate (`请登录后再使用此功能`) plus a form posting to `JspShopCartService.jsp`. "paid" is not stated; "only" is unsupported while
   `/detailText.do…sendSql=ui%3d2026335073` (raw 4739) offers a second in-index route I did not open.
2. **The 学科分类号 field is not displayed, and the 主题词 label is not displayed.** The entry's Observation and the row's scope both name
   the four fields as what the index *records*; in the rendered form only 来源出版物 and 关键词 are fields a reader sees. A `.txt`-only
   re-grounding — the form the sibling seats use — finds `学科分类号` = 0 and would be entitled to call this row **unverifiable** under
   QUALITY 59. The field is real, but only in `.raw`, and only inside a comment.
3. **No year, DOI, ISSN or page range.** The `recheck:` line asks to confirm "the journal/volume/issue are unchanged": that is checkable
   (26/4). It cannot date the volume — `年：`=0, and no 出版年/日期 field exists anywhere in the record.
4. **"indexed by a national biomedical index"** — the operator is carried (`中国医学科学院 北京协和医学院医学信息研究所/图书馆`), but `国家`
   never appears, and the string `SinoMed` = 0 in both forms. "national" and "SinoMed" are the lane's glosses on 中国生物医学文献服务系统.
5. **Title drift**: the staged row writes `（PRISMA-S）` with full-width parens; the capture's title uses ASCII `(PRISMA-S)`. Substantively
   nil, but it is the round-50 filename/title-drift class — the entry should quote the ASCII form, which is what the capture carries.
6. **The abstract is truncated by the index** at `并针对中文` (txt 1258), so the record carries neither the abstract's remainder nor the
   item-by-item content. The entry's "the item-by-item Chinese text is therefore still unread" is consistent with this capture — but it is
   consistent because the index truncates, not only because of the paywall.
7. **Fields the capture carries and the entry/row omit**: `基金` with five numbered grants (甘肃省科技重大专项 24ZD17FA003; 天津杰青
   20JCJQJC00120; 中国医学科学院医学与健康科技创新工程 2021RU017; 甘肃海智 KPZX-011030; 教育数字化 JYSZH[2025]ZD126) — all in the same
   comment, hence `.raw`-only; and `作者地址：` present-but-empty, so the record yields no author affiliation.
8. **"the same item as wave 3's med-sci portal row"** is not checkable from this capture — it holds no cross-reference to that portal. I did
   not open the wave-3 row, so I do not rule on the identity claim.

## 5. Commands run (all read-only; no scratch dir created, nothing to delete, no install needed)

```
$ for s in 学科分类号 来源出版物 关键词 主题词 全文 获取 订购 付费 登录; do grep -c "$s" ...raw; done  → 1 1 1 3 0 1 0 0 1
$ for s in 学科分类号 来源出版物 关键词 主题词 全文 获取 订购 付费 登录; do grep -c "$s" ...txt; done  → 0 1 1 1 0 0 0 0 1
$ python3 … comment spans of .raw → 15 spans; 9192–9908 holds 学科分类号/主题词/基金; .do endpoints → detailText.do, login.do, online.do, userInfo.do, zh/basicSearch.do
$ python3 … txt.count(q)/txt.find(q) and raw.count(q)/raw.find(q) for all 11 quotes → 1 each (subject string alone = 2 in raw: comment 9465 + hidden input 14032)
$ python3 … raw.lower().count('pdf'|'fulltext'|'openurl'|'linkout') → 0 0 0 0 ; txt.count('基金'|'学科分类号'|'主题词：') → 0 0 0
```

No file under `chousa-shokunin`, `shokuknow` or the fleet repo was modified; this report is the only write.

VERDICT: attacked the staged S119 claims against the on-disk capture — journal/volume/issue, the five keywords, the five subject headings and
the 16-item scope hold verbatim (with the subject-heading *label* and the whole `学科分类号` field confined to an HTML comment, hence invisible
in the `.txt`), while "paid … only through a paid ordering service", "national index"/"SinoMed", any publication year and the omission of the
five 基金 grants are staged claims the capture does not carry.
