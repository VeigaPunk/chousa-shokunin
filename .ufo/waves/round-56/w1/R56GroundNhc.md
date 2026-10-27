# R56GroundNhc — S130 grounding: the NHC-hosted 2020 药品临床综合评价管理指南

seat: R56GroundNhc (leaf; no dispatch). Lane `chousa-shokunin`, base `e5a37951`, lane worktree HEAD `0c2f4ce5` while reading.
Target: lane S130 = https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf
Form: `.qcache/a42feae4448612f949cc715f.txt` (key = sha256(url)[:24] = `a42feae4448612f949cc715f`, recomputed).
No fetch, no lane write, no counter run, no git/jj. Tooling: nothing installed; `pypdf 6.21.2` loaded ephemerally by `uv run --with pypdf` (no persistent tool, no PATH write).

## 1. Identity as printed

Cover block, `s[0:138]` of the form (repr, `python3`):
`'附件：\n\n      药品临床综合评价管理指南\n            （试行）\n\n\n\n\n        国家药物和卫生技术综合评估中心\n       （国家卫生健康委卫生发展研究中心）\n         国家卫生健康委药具管理中心\n            二〇二〇年十一月\n'`

- **Title** `药品临床综合评价管理指南` at char **11**; trial status `（试行）` at char **36** — the two are on *different lines*, so the joined string `药品临床综合评价管理指南（试行）` occurs **0×** in the form.
- **Issuer** as printed: `国家药物和卫生技术综合评估中心` (char 53) with its host `国家卫生健康委卫生发展研究中心` (char 77), then `国家卫生健康委药具管理中心` (char 103). The centred-array text puts the parenthetical on its own line: `国家药物和卫生技术综合评估中心（国家卫生健康委卫生发展研究中心）` occurs **0×**.
- **Date** as printed: `二〇二〇年十一月` at char **129** (no day).
- **No document number of its own.** Every `号` hit is a citation of another instrument: `（国办发〔2018〕88 号）` char 324, `（国卫药政发〔2019〕1 号）` 380, `（国卫药政函〔2019〕80 号）` 443, `（国卫医发〔2020〕2 号）` 482; `印发` 0×, `公告` 0×. The first line is `附件：` (char 0): the PDF is an attachment served on nhc.gov.cn.
- **The NHC relation is body text, not a cover stamp:** char **632** `药政司委托国家药物和卫生技术综合评估中心（挂靠国家卫生` (continues `健康委卫生发展研究中心，以下简称“评估中心”）、国家卫生` …). So the printed signatories are the two centres, acting under 国家卫生健康委药政司's commission; the cover prints no ministry seal line.
- File metadata (pypdf, not printed): `/Title` `关于药品临床综合评价管理指南公开`, `/Author` `药政司,基本药物目录处,李孟涛`, `/Creator` `WPS 文字`, `/CreationDate` `D:20201104155352+07'53'`. Metadata only — not identity evidence.
- Structure at chars 150 `指南起草说明`, 1142 `第一章 概述`, 1876 `第二章 评价流程、内容与维度`, 4185 `第三章 证据评价与应用`, 6711 `第四章 指南管理`.

## 2. Is the `.txt` the WHOLE document? — YES (16/16 pages, text-identical)

`file(1)`: `PDF document, version 1.7, 16 page(s)` for both `.raw` and `.pdf`; `.raw` and `.pdf` have the same digest `d01795dd60264371ed4d81c77d4453446b333e8f9cbb322f7c7dfe9e1a9d8e7d` (the `.raw` *is* the PDF). `pypdf 6.21.2`: `pages 16`.

Form facts (`python3`, `pypdf`): `bytes 19242 chars 6930 CR 0 sha256 71fed1a3bc95a7e1377ef86e364f0aa183f0885175c8f0dce459b818a861688f`, strict UTF-8 decode OK, U+FFFD 0, 16 form feeds → 17 segments with the 17th empty = 16 pages.

Page-by-page, text vs pypdf, after removing all whitespace (`nw(a)==nw(b)`):
`1 True, 2 True, 3 True, 4 True, 5 True, 6 True, 7 True, 8 True, 9 True, 10 True, 11 True, 12 True, 13 True, 14 True, 15 True, 16 True`
(`ALL_PAGES_NORM_EQUAL True`; per-page char counts differ only by layout whitespace — e.g. page 1 `138` vs `78`, page 16 `228` vs `214`.)

Whole document: `txt_chars 6930 txt_nonspace 6237 pdftext_chars 6530 pdf_nonspace 6237` → `nonspace_equal True`; the 693-character gap is whitespace (`txt_ws_total 693`). **Last page's last line is `修订完善。` in both forms** (`TXT_LASTPAGE_LASTLINE '修订完善。'`, `PDF_LASTPAGE_LASTLINE '修订完善。'`).

PDF outline: 24 destinations, **every title present in the form** (`in_txt=True` for all, incl. `第一章 概述`…`（三）评价结果优化完善`); 0 attachments, 0 annotations on all 16 pages. Two metadata defects only: the four chapter destinations point one page early (`outline_p=3/5/10/15` vs `form_p=4/6/11/16`), and `一、评价流程` (char 2017, page 6) is in the text but missing from the outline. Neither removes text.

## 3. Negative claim — licensed for the whole document

Counts on the form and on `"\n".join(pypdf per-page text)`, raw and whitespace-stripped:

| term | txt raw | txt nw | pdf raw | pdf nw |
|---|---|---|---|---|
| 灰色文献 | 0 | 0 | 0 | 0 |
| 灰色 | 0 | 0 | 0 | 0 |
| 未公开发表 | 0 | 0 | 0 | 0 |
| 文献检索 | 0 | 0 | 0 | 0 |
| 检索 / 搜索 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| 文献 | 1 | 1 | 1 | 1 |
| 证据 | 20 | 22 | 20 | 22 |
| 数据库 / 循证 / 系统评价 | 2 / 3 / 1 | 2 / 3 / 1 | 2 / 3 / 1 | 2 / 3 / 1 |

The one `文献` is char **6390** `业药品临床综合评价的实践，扩大文献证据储备；2.推动科研` — a *use of evaluation results* sentence (`第三方评价机构药品临床综合评价结果可用于：1.丰富行业药品临床综合评价的实践，扩大文献证据储备`), **not** a search instruction, and the form has no 检索/搜索 wording at all. `证据` 20 raw → 22 stripped proves one instance is split across a line break (so the stripped count is the one that clears split words); 灰色 stays 0 under both.

## 4. QUOTE machine lines (lane id S130)

Each: occurs **exactly once**, lies on **one line** of the form, ≤25 whitespace words (1), ≤160 chars (max 21), byte-exact; offset = `form.find(quote)` on `open(p, encoding='utf-8', errors='replace').read()`.

```
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	药品临床综合评价管理指南	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	（试行）	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	国家卫生健康委卫生发展研究中心	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	国家卫生健康委药具管理中心	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	二〇二〇年十一月	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	药政司委托国家药物和卫生技术综合评估中心	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	扩大文献证据储备	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	证据核查或更新的书面请示	corpus/knowledge/grey-literature-field-china-r42.md
```

Offsets: title 11, `（试行）` 36, host centre 77, 药具中心 103, date 129, commission 632, `扩大文献证据储备` 6390, `证据核查或更新的书面请示` 6657. Rows 1–5 are identity; row 6 carries the issuer relation; rows 7–8 are the guideline's own evidence/literature wording (row 8 = `…提出证据核查或更新的书面请示，经牵头组织机构委托开展咨询论证后…`).

## 5. Findings (reported, not patched)

1. **Completeness is established, so the entry's negative is licensed for the whole text.** `corpus/knowledge/grey-literature-field-china-r42.md:20` says "its text form holds the string 灰色 zero times"; `corpus/SOURCES.md:140` says `灰色 ×0`. With all 16 pages text-identical to the PDF and the last line identical, that zero covers the entire guideline, not just a cover capture. Both also agree with the measured `6930` chars and `sha256 prefix 71fed1a3bc95a7e1`; the form is strictly UTF-8 with 0 U+FFFD (contrast the retired OLE `.doc` path, 887 U+FFFD).
2. **Quoteable identity is line-fragmented; three natural strings are unusable.** `药品临床综合评价管理指南（试行）` 0×, `国家药物和卫生技术综合评估中心（国家卫生健康委卫生发展研究中心）` 0×, and `国家药物和卫生技术综合评估中心` **2×** (char 53 cover, char 637 body) — an identity quote must take char 11 + char 36, and the host/药具 lines separately, as the existing rows do.
3. **Issuer calibration.** The printed signatories are the two centres; the ministry appears only as `药政司委托…（挂靠…）` at char 632 and as the host of the URL. The text prints no 国卫 document number. An entry calling the text a 国家卫生健康委-issued guideline (the staged label "国家卫生健康委 … 2020", staged S157) overstates the cover; "the national centres' text, hosted on nhc.gov.cn, commissioned by 药政司" is what the document says. The registry's tier-B caution (relation to a 2021 管理指南 not established) is consistent with the only date printed (二〇二〇年十一月, metadata 2020-11-04).
4. **The existing S130 span rows are exact.** `spans.tsv:22-24` offsets 0/23/49, files `spans/S130-1..3.txt`; each `s[off:off+len(span)] == span` (True/True/True), each `len(span) > len(quote)`, and `off + span.find(quote)` = **11 / 103 / 129** — the three `char N` anchors the entry prints. The recorded capture digest `71fed1a3…861688f` is the sha256 of the form.
5. **Coverage gap for my mandate, not a defect in C2:** the entry cites S130 only for identity (3 quotes); it carries **none** of rows 6–8 above (no `药政司委托…`, no `扩大文献证据储备`, no `证据核查或更新的书面请示`). Adding them means new span rows plus entry and lesson text — outside my write scope, so they are offered as located QUOTE lines only.
6. **`文献` must not be read as a search requirement.** Its single occurrence (6390) is about the reserve that third-party evaluation results can enlarge; 检索/搜索 are 0×. The guideline is a management text: its evidence vocabulary is 证据 (20/22), 真实世界 (17/18), 数据库 (2), 循证 (3).
7. Outline destinations for the four chapters are one page early and `一、评价流程` is absent from the outline; both are PDF bookkeeping, no text is missing.

## 6. Touched surfaces / out of scope

Written: this report only. Not run: `c2-count.py`, any gate/battery/probe, `build-spans.py`, `capture-text.py`; not edited: entry, `SOURCES.md`, `spans.tsv`, lesson, any lane file; no git/jj mutation anywhere; scratch `/fast/scratch/hyaku/chousa-r56/R56GroundNhc/` removed after the receipts above were copied in.

VERDICT: grounded S130 (NHC 2020 药品临床综合评价管理指南, 16-page PDF vs 6930-char `.txt`, non-space-identical on all 16 pages, last line `修订完善。` both) — identity and the whole-document 灰色/文献 negative survived; the guideline carries 灰色文献 0×, 灰色 0×, 未公开发表 0×, 文献检索 0× in both forms, and 8 located QUOTE lines (3 already in the entry, 5 offered) all pass the once/one-line/byte-exact rule.
