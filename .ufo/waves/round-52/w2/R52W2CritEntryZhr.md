# R52W2CritEntryZhr — entailment attack: `chinese-prisma-s-reception-r52.md`

Attacked: the entailment of every `#### Observation` and `#### Inference` bullet of
`corpus/knowledge/chinese-prisma-s-reception-r52.md` against its two captures (S113
medsci.cn, S114 chinagp.net), plus its cross-file comparisons (S111 capture of the
SinoMed record in `chinese-search-record-r39.md`; `japanese-prisma-item-wording-r40.md`).

Method: I ran all probes from my scratch seat (`/fast/scratch/hyaku/chousa-r52/R52W2CritEntryZhr`,
TMPDIR set there; no installs performed — none needed; the two qcache `.txt` captures
re-opened read-only as UTF-8; every quote re-located with `re.finditer`/`str.find`;
comparison files opened; `build-spans.py --check` run).

## Quote/offset verification (all pass)

S114 (`cacddf3bbf780a4c7582bb17.txt`, len 6179 — entry says 6,179 ✓):

```
'中国全科医学 报告清单' count=1 offsets=[16]
'P RISMA2020 条目清单' count=1 offsets=[920]
'详细说明获取文献的所有来源，包括 所有数据库、注册平台、网站 、 机构 、参考列表以及 其他 检索或咨询 途径 。' count=1 offsets=[1650]
'明确说明每一项来源 的 检索或查询日期' count=1 offsets=[1707]
'呈现 所有数据库、注册平台和网站的 完整 检索策略，包括 用到的 过滤器和限制条件。' count=1 offsets=[1785]
'From: Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al.' count=1 offsets=[5530]
'BMJ 2021;372:n71. doi: 10.1136/bmj.n71' count=1 offsets=[5694]
'发布日期：2023-01-31' count=1 offsets=[5744]
'网站版权 © 《中国全科医学》编辑部' count=1 offsets=[6121]
unspaced variants (all three) count=0; 翻译/译/translat all count=0
```

Context: item-6 cell (label `信息来源`, `6`) is contiguous `…途径 。明确说明每一项来源 的 检索或查询日期 。`;
item-7 cell (label `检索策略`, `7`) at 1785; credit window reads `…et al. The PRISMA 2020
statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. doi:
10.1136/bmj.n71`, then `发布日期：2023-01-31 浏览：…3452`; footer at 6121.

S113 (`453d492becd9a2f4632cb8dd.txt`, len 8804 — entry says 8,804 ✓):

```
'2026-04-25 中国循证医学杂志' count=1 offsets=[2034]
'PRISMA-S(PRISMA for Searching)作为PRISMA 2020的扩展版本，为文献检索报告提供了包含16个条目的专项规范。本文旨在对PRISMA-S进行系统性中文解读，基于其原始发布文献，在逐条阐释其内涵与要求的基础上，进一步探讨其跨学科的普适性、作为“报告规范”的内在局限' count=1 offsets=[2328]
'在逐条阐释其内涵与要求的基础上，进一步探讨其跨学科的普适性、作为“报告规范”的内在局限，并针对中文数据库等本土化应用挑战提出实践建议。' count=1 offsets=[2433]
'copyright=0, guiderPublishedTime=Sat Apr 25 00:00:00 CST 2026, originalUrl=, linkOutUrl=,' count=1 offsets=[3139]
'NameList=[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)])' count=1 offsets=[4850]
'梅斯医学是面向医生的综合互联网平台' count=1 offsets=[7287]
CNKI/中国知网/万方/维普/SinoMed all count=0
```

Context: `简要介绍：` label at 2264 then the abstract paragraph (starts 2270); `中文标题：`
label at 2171; headline at 1998; page `<title>` at 21; `GetToolGuiderByIdResponse(projectId=1,
id=23e481c0052069d3, title=系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读 , enTitle=, …
authorId=0, author=, summary=本文旨在为国内学者、期刊编辑及审稿人提供清晰、实用的PRISMA-S应用指引，
以期提升我国SR文献检索部分的报告质量，促进SR研究的规范化与国际化。, …` at 2700+; the quoted
`copyright=0,…` fields continue that same object; `attachmentFileNameList=[AttachmentFileName(sort=1,
fileName=…_郑卿勇.pdf)])` at 4836 (the entry's `NameList=[…]` quote is a substring of this token);
a second serialized attachment token at 2740; the attachment file name displayed at 4981.
`郑卿勇` count=3, all three inside that file-name string. `并针对中文` occurs at 2477 and 3596
(the abstract appears twice: plain, and HTML-entity-escaped `&ldquo;…&rdquo;`).

Comparison files:
- S111 capture (`42bac8830527d6f1bb125c49.txt`): abstract line ends `…作为“报告规范”的内在局限,并针对中文`
  (half-width punctuation), i.e. truncates at `并针对中文`; the Chinese-databases clause is absent there. ✓ r39's claim.
- `japanese-prisma-item-wording-r40.md` line 13/20: item 7 lists databases (second mention), trial registries,
  websites; organisations and reference lists absent from item 7. ✓ "same split".
- `build-spans.py --check` from lane root: `SPANS_ROWS=38 STALE=0`. ✓

## Bullet verdicts

| Bullet | Verdict |
|---|---|
| Obs 1 (journal page/checklist/credit/date/footer/no translator) | supports — all offsets, counts and the contiguous cell text verified |
| Obs 2 (item 6, per-source date, spaced/unspaced) | supports |
| Obs 3 (item 7 strategy/filters/limits) | supports |
| Obs 4 (S113 abstract full; SinoMed truncation) | supports |
| Obs 5 (byline, record fields, no original URL, attachment, portal self-description) | **contradicted as worded** on "names the article only as an attachment" (D1); rest supports |
| Inf 1 (each source dated, not only the search) | Chinese part supports; trailing English comparison unsupported (D2) |
| Inf 2 (strategy covers fewer source classes; same split as Japanese entry) | supports |
| Inf 3 (hosted copy credited, not an attributed translation) | supports |
| Inf 4 (adds last clause, nothing of item text) | supports (minor note N2) |

## Defects

**D1 — Obs 5, "names the article only as an attachment" (S113): contradicted.**
The same record object the bullet quotes also carries the article's title
(`title=系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读` at char 2818, inside the same
`GetToolGuiderByIdResponse`), and the page displays that title as the headline (char 1998)
and under `中文标题：` (char 2179) and in the page `<title>` (char 21). The article is named as a
title and as an attachment file name; "only as an attachment" is false as worded. The context
part ("The author's name appears only inside that file name; the attachment's text is not in the
capture") is carried (郑卿勇 count=3, all inside the file name; no PDF body in the capture).
Narrowed wording (for the same bullet): *"and carries the article's title in the record object
(`title=系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读`, char 2818), shows it as the page
headline (char 1998) and under `中文标题：` (char 2179), and links the PDF only as an attachment
file name (`attachmentFileNameList=[AttachmentFileName(sort=1, fileName=…_郑卿勇.pdf)])`, char 4836;
the `NameList=[…]` quote is a substring of that token, char 4850)."*

**D2 — Inf 1, trailing "as PRISMA 2020's English item does": unsupported.**
No capture in this round or anywhere in the lane corpus carries the English PRISMA 2020 item wording
(corpus-wide greps for `Specify all databases`, `searched or consulted`, `last searched or consulted`,
`Specify the date` match nothing; `japanese-prisma-item-wording-r40.md` line 26 states the English
checklist was not opened). The comparative clause asserts an external fact the captures do not carry.
Narrowed wording: end the inference at *"…carries one date per source."* (drop `, as PRISMA 2020's
English item does`). The Chinese clause itself is fully carried by `S114` item 6.

## Notes (weaker, not defects)

- **N1 — Obs 1, "reporting-guideline column":** the capture text contains no column word
  (`专栏`/`栏目`/`column` all count=0); "column" rests on the S114 row URL (`/CN/column/item185.shtml`).
  Acceptable but the URL is the only support; if kept, it may cite the row URL.
- **N2 — Inf 4:** the portal additionally appends a closing sentence `本文旨在为国内学者、期刊编辑及审稿人提供…`
  (in the 简要介绍 tail and in the record's `summary=` field, char 2906) beyond the last clause; the
  bullet's "adds the abstract's last clause and nothing of the item text" stays true but omits that
  sentence — optionally: "adds the abstract's final clause (plus a closing sentence in the summary
  field) and nothing of the item text".

VERDICT: attacked the entailment of every Observation/Inference bullet of `chinese-prisma-s-reception-r52.md`
against its S113/S114 captures and cross-file comparisons; found two defects — Obs 5 "names the article only
as an attachment" contradicted by the record's own `title=` field and displayed headline (D1), and Inf 1's
"as PRISMA 2020's English item does" unsupported corpus-wide (D2) — all other bullets and every offset/count
verified supports.
