# R52GroundMedsciA — re-ground staged S111 (梅斯医学 PRISMA-S interpretation page)

Seat: scribe/ground, leaf (no dispatch). Lane write: this file only.
Staged package read-only; no network; no lane tool run that writes (build-spans.py imported in scratch, never executed as a CLI).

## Provenance and forms

| item | value |
|---|---|
| URL | `https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3` |
| cache key `sha256(url)[:24]` | `453d492becd9a2f4632cb8dd` (recomputed; matches both file names) |
| `.txt` (the text form used here) | 8804 chars, `sha256 ad6b09f0599c5820a4d283c953d07f457f3f540edcb5ebc3406e50ae571cdc52` |
| `.raw` | 276803 bytes, `file(1)`: `HTML document, Unicode text, UTF-8 text`; `sha256 712cdef66a94b2dd69f38a43c47e5dc0932259ebb060cf50989ddf8d19b90e00` |
| staged entry | `merge/chousa/knowledge/corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md` |
| staged row | `merge/chousa/SOURCES.append.md` line 36 (S111); S133 at line 58 |

`tools/capture-text.py` is the `.docx` reader and refuses this capture —
```
$ python3 tools/capture-text.py .../453d492becd9a2f4632cb8dd.raw ; echo exit=$?
REFUSED not a zip (an OOXML capture is a zip package)
exit=2
```
So **every quote below is located in the `.txt` form read as UTF-8** (stated per row), never in the HTML attributes.

## What the page is (what the "secondary copy" is a copy of)

It is **MedSci (梅斯医学) 指南・解读指南 — a commercial portal record** of an article published in
《中国循证医学杂志》: the portal holds an abstract block, a header byline and an attachment *name*, with
`originalUrl=` empty and `copyright=0` in its own record object. It is not the journal's own page; the item
text itself is the attachment PDF, which the capture does not contain.

## Located quotes

Form for every row: the `.txt` read as UTF-8 (8804 chars). Command shape:
`python3 -c 't=open(P,encoding="utf-8").read(); print(t.count(q), t.find(q))'`.

| # | offset | chars x words | quote (byte-exact) | grounds |
|---|---|---|---|---|
| Q1 | 2328 | 148 x 4 | `PRISMA-S(PRISMA for Searching)作为PRISMA 2020的扩展版本，为文献检索报告提供了包含16个条目的专项规范。本文旨在对PRISMA-S进行系统性中文解读，基于其原始发布文献，在逐条阐释其内涵与要求的基础上，进一步探讨其跨学科的普适性、作为“报告规范”的内在局限` | extension claim, 16 items, 逐条 reading, generality + limits |
| Q2 | 2433 | 67 x 1 | `在逐条阐释其内涵与要求的基础上，进一步探讨其跨学科的普适性、作为“报告规范”的内在局限，并针对中文数据库等本土化应用挑战提出实践建议。` | the 中文数据库 clause = *generic* 中文数据库 challenge |
| Q3 | 2034 | 19 x 2 | `2026-04-25 中国循证医学杂志` | visible byline: portal date + source journal |
| Q4 | 4051 | 143 x 9 | `haveAttachments=1, attachmentList=null, guiderType=0, guiderArea=解读, guiderLanguage=0, guiderRegion=3, opened=0, paymentType=, paymentAmount=10` | attachment present, **paymentType empty**, price field 10 |
| Q5 | 3139 | 89 x 9 | `copyright=0, guiderPublishedTime=Sat Apr 25 00:00:00 CST 2026, originalUrl=, linkOutUrl=,` | no original URL → secondary copy |
| Q6 | 4850 | 89 x 2 | `NameList=[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)])` | attachment is a *name*, author only inside it |
| Q8 | 7057 | 14 x 1 | `前往APP阅读全文，体验更佳` | reading full text is pushed to the app |
| Q9 | 7287 | 17 x 1 | `梅斯医学是面向医生的综合互联网平台` | portal self-description (commercial) |
| Q10 | 8272 | 27 x 1 | `本站旨在介绍医药健康研究进展和信息，不作为诊疗方案推荐` | portal disclaimer; it is not the publisher |

Q1's uniqueness depends on a byte the HTML-source copy renders as `&ldquo;` while the visible block renders
`“`; Q2 likewise. Both were verified `count=1` on the `.txt`. Two further observations were **verified but are
NOT emitted as machine lines** because they are under the criterion-72 substance floor (6 non-space chars,
`quote-substance-check.py` needs ≥12): `下载请点击：` (off 4996, count 1) and `发表于河南省` (off 2056, count 1).

Machine lines (staged id S111; lane id for the entry is **S113**, never carried over):

```
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	PRISMA-S(PRISMA for Searching)作为PRISMA 2020的扩展版本，为文献检索报告提供了包含16个条目的专项规范。本文旨在对PRISMA-S进行系统性中文解读，基于其原始发布文献，在逐条阐释其内涵与要求的基础上，进一步探讨其跨学科的普适性、作为“报告规范”的内在局限	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	在逐条阐释其内涵与要求的基础上，进一步探讨其跨学科的普适性、作为“报告规范”的内在局限，并针对中文数据库等本土化应用挑战提出实践建议。	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	2026-04-25 中国循证医学杂志	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	haveAttachments=1, attachmentList=null, guiderType=0, guiderArea=解读, guiderLanguage=0, guiderRegion=3, opened=0, paymentType=, paymentAmount=10	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	copyright=0, guiderPublishedTime=Sat Apr 25 00:00:00 CST 2026, originalUrl=, linkOutUrl=,	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	NameList=[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)])	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	前往APP阅读全文，体验更佳	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	梅斯医学是面向医生的综合互联网平台	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	本站旨在介绍医药健康研究进展和信息，不作为诊疗方案推荐	corpus/knowledge/chinese-prisma-s-reception-r52.md
```

Builder anchors (derived in scratch by importing `build-spans.py`'s own `form_texts` + `CONTEXT=80`, no CLI run,
nothing written to the lane): `char N` for the rows above = **2328, 2433, 2034, 4051, 3139, 4850, 7057, 7287, 8272**,
each a `char N` that is the offset of a quote of S113.

## Staged sentences about this document

`S` = supported by a located quote; `N` = narrow (what the capture really says); `U` = unsupported.

| staged sentence (staged entry / row S111) | verdict | basis |
|---|---|---|
| "PRISMA-S, as 'the PRISMA 2020 extension', supplies 'a dedicated specification containing 16 items' for the search half" (entry Obs. 1; row cell 6) | **S** | Q1 off 2328 |
| "a Chinese-language, item-by-item reading of PRISMA-S … works through the items one by one" (entry Obs. 1; row cell 4) | **S** | Q1 `在逐条阐释其内涵与要求的基础上` |
| "examines … its cross-disciplinary generality and its intrinsic limitations as a 报告规范" (entry Obs. 1, Inf. 1/3; row cell 6) | **S** | Q1/Q2 `跨学科的普适性、作为“报告规范”的内在局限` |
| "offering practical recommendations for **Chinese databases**" (entry Obs. 1; row cell 6; row recheck cell 9) | **N** | Q2 says `针对中文数据库等本土化应用挑战提出实践建议` — the *challenge* is named generically; no database is named. Sweep on `.txt`: `CNKI=0 中国知网=0 知网=0 万方=0 维普=0 VIP=0 SinoMed=0 中国生物医学文献=0` (same sweep on `.raw` bytes: all 0) |
| "the item's claim … the challenges of applying it to Chinese databases" in S133 (same URL) | **N** | same as above: `中文数据库` occurs once (off 2477; twice overall incl. the HTML-source copy at 3596), never with a named database |
| "from 中国循证医学杂志" (row title cell); "the 简要介绍 block" (row cell 5) | **S** | Q3 off 2034 + `guiderFrom=中国循证医学杂志` (off 2863, count 1) |
| "（郑卿勇）" as the item's author (row title cell; S133 title cell) | **N** | the name occurs only inside the PDF filename — off 2740, 4929, 4981, all `…解读_郑卿勇.pdf`; the page carries no byline and `发布机构：` is empty (label only, followed by whitespace then `发布日期：`) |
| "page read 2026-10-23" (row cell 5) | **S** | read date is seat metadata, not page content; the page's own dates are 发布日期 `2026-04-25` (Q3) and record `publishedTime=Tue May 05 13:50:00 CST 2026` (off 4380, count 1) — two portal dates, no journal date |
| "The S111 attachment itself was not opened … behind the portal's download mechanism" (entry Unknown) | **N** | the capture holds `haveAttachments=1`, `attachmentList=null` and the filename only (Q4/Q6); `下载请点击：` (off 4996) is followed by no link text in the text form. Nothing in the capture shows a gate |
| S133: "the Chinese PRISMA-S interpretation item **is sold, not blocked** … `paymentAmount=10` … the measured shape of the paywall" | **U** as stated | `paymentType=` is **empty** in the same record object (Q4), and the page source's download controls read `value="会员免费下载"` (raw off 113165) and `value="点击下载（会员免费）"` (raw off 117481) with `onclick="downGuiderFileMember(event, 1)"` (raw off 117500) — member-free, no price; sweep `售价/价格/付费/收费/购买/金币/积分兑换/会员/免费` on `.txt` = all 0, and in `.raw` `购买=1` (nav comment `<!-- 微应用会员购买 -->`), `会员=23`, `免费=3` (all three at the download controls/function) |

## Findings for the L1 (two, both outside my write)

**F1 — a raw-only quote for an HTML capture cannot be spanned.** `build-spans.py` `raw_form()` decodes any
non-zip `.raw` as UTF-16LE; for this HTML capture that is mojibake (`'ℼ佄呃偙⁅呈䱍…'`, scratch derivation), and
`docx_text()` returns None. Consequence measured in scratch: the member-free button string occurs `0` times in
the `.txt` and `0` times in the raw form, so `build-spans.py` would refuse it (`quote not exactly once in any
form`). **Therefore the `会员免费下载` evidence must not go into `quotes.tsv`;** it is report-grade only. If the
Gate needs it spanned, the builder needs an HTML raw form — a rule change, so it belongs in
`claims-erratum.md` and not in this round's counter.

**F2 — S133's "sold, not blocked / sold rather than free" is contradicted by the capture at the same URL.**
`paymentAmount=10` is present (Q4, off 4178 within the text form) but `paymentType=` is empty and the page's own
controls say 会员免费. The transferable fact is: *the item is a portal record with an attachment name, a price
field of 10, no payment type and a member-free download control; the attachment was never served into the
capture.* "Sold" is not a measurement this capture supports.

## Draft lane entry (intended path: `corpus/knowledge/chinese-prisma-s-reception-r52.md` — S111 half only; the S112 half is another seat's ground)

```markdown
# The Chinese PRISMA-S reception, as a commercial portal records it

source: S113 — https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3 — the 简要介绍 block, the item's
record fields and the attachment's name; capture .txt read as UTF-8, 8804 characters; char 2328, char 2433,
char 2034, char 4051, char 3139, char 4850, char 7057, char 7287, char 8272
verified-at: 2026-10-26
recheck: 180d — re-open the page and confirm the 16-item sentence, the 中文数据库 clause and `paymentType=` empty
with `paymentAmount=10` are unchanged (ran 2026-10-26)

#### Observation

- **The reception's own abstract states the two facts the lane needs.** The item calls
  `PRISMA-S(PRISMA for Searching)作为PRISMA 2020的扩展版本，为文献检索报告提供了包含16个条目的专项规范` and
  describes itself as a 系统性中文解读 that works 逐条, then examines 跨学科的普适性 and the standard's
  `内在局限` as a 报告规范 (`S113`, char 2328).
- **Its localisation clause is generic.** The reading offers 实践建议 against `中文数据库等本土化应用挑战`
  (`S113`, char 2433) — the *category* 中文数据库, never a named database: no CNKI, 中国知网, 万方, 维普 or
  SinoMed string occurs in the capture in either form.
- **The page is a portal record, not the publisher's page, and it links nowhere.** The byline is
  `2026-04-25 中国循证医学杂志` (`S113`, char 2034) while the record carries `copyright=0, … originalUrl=,
  linkOutUrl=` (`S113`, char 3139); the portal describes itself as `梅斯医学是面向医生的综合互联网平台`
  and disclaims clinical use (`S113`, char 7287, char 8272). The item's text is an attachment *name*
  (`NameList=[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)])`,
  `S113`, char 4850); the author's name exists nowhere on the page outside that filename, and 发布机构 is empty.
- **The attachment is member-free by the page's own control, not sold.** The record holds
  `haveAttachments=1, … opened=0, paymentType=, paymentAmount=10` (`S113`, char 4051): a price field with no
  payment type. The page **source** (the capture's `.raw` form, bytes off 113165 and 117481) labels its download
  control `value="会员免费下载"` / `value="点击下载（会员免费）"`; no price string (`售价`/`价格`/`付费`/`金币`)
  occurs in the text form at all. Nothing was served into the capture, and full-text reading is pushed to the
  portal's app (`前往APP阅读全文，体验更佳`, `S113`, char 7057).

#### Inference

- **The lane may cite this item for the reception's shape, not for its item text.** The abstract grounds the
  `PRISMA-S(PRISMA for Searching)` extension claim, the 16 条目 count and the critique of the standard's limits;
  it grounds nothing about which databases the recommendations name (`S113`). The entry therefore treats the
  Chinese reception as a *reception at abstract level*, and the 16-item count as the portal's rendering of the
  article's own claim.
- **The "paywalled Chinese item" the lane has carried since round 37 is not supported by the record's fields.**
  The portal's own record sets `guiderArea=解读, guiderLanguage=0` with an empty payment type and a member-free
  download label (`S113`); what was blocking the lane was never payment but the fact that the portal serves an
  attachment name and an abstract, and the round-51 capture took neither.

#### Unknown

- **The attachment's text was not opened, in this round either.** The capture contains the abstract and the file
  name; whether the PDF's item-by-item recommendations name particular Chinese databases is unverified, and the
  entry must not assert it.
- **Whether the portal copy equals the journal's published text is unknown.** `originalUrl=` is empty, so the
  portal record cannot be checked against 中国循证医学杂志's own page from this capture.
- **The two portal dates disagree** (`2026-04-25` on the header, `publishedTime=Tue May 05 13:50:00 CST 2026` in
  the record) and neither is the journal's publication date; the entry states neither as the article's date.
```

Both Inference bullets already carry a two-word Latin grounding token present verbatim in a cited S113 span
(`PRISMA-S(PRISMA for Searching)` in span 1; `guiderArea=解读, guiderLanguage=0` in span 4), so
`tools/inference-ground.py` has a token to match — the L1 should still run it after integration.

## Out of scope / unchanged

- S112 (中国全科医学), S125 (NIPH form), S129 (Japanese checklist) — other seats; I touched no lane file.
- No lane row, no entry, no lesson, no `quotes.tsv`, no `spans.tsv` written; `build-spans.py` imported, not run
  (it writes to the lane). No counter run (`c1-count.py`, `c2-count.py` are the L1's).
- No install performed (tooling: nothing needed; `python3`, `file(1)` host-provided).
- Scratch `/fast/scratch/hyaku/chousa-r52/R52GroundMedsciA/` — removed at exit.

VERDICT: attacked the S111 ground — rebuilt nine once-only `.txt` quotes with offsets 2328/2433/2034/4051/3139/4850/7057/7287/8272, found the "Chinese databases" phrasing generic (no named database in either form) and S133's "sold" claim contradicted by an empty `paymentType` plus a 会员免费下载 control, and found that an HTML raw-only quote is unspannable by the round-52 builder; the entry may claim the reception's abstract-level shape and 16-item count, nothing about item text or payment.
