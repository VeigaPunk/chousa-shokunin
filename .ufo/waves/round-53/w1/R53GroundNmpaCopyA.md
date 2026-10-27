# R53GroundNmpaCopyA — re-ground staged S190 → lane S120 (pharmwyp copy of the 2019 NMPA notice)

seat: R53GroundNmpaCopyA (leaf, no dispatch) · date: 2026-10-26 · lane HEAD `6365f15`
frozen claims read first: `corpus/evidence/round53/claims.md` (freeze `a6ff732`, `git log --oneline -3` in lane: `6365f15`, `32aab5e`, `a6ff732`). No predicate, target, counter or control touched. No network, no source fetch (L0 `8d77e6c1` open — every byte below is from the on-disk `.qcache`). No installs; `command -v pdftotext` → `/usr/bin/pdftotext` (already present), so no pacman/uv/npx transaction was attempted.
scratch: `/fast/scratch/hyaku/chousa-r53/R53GroundNmpaCopyA/` (TMPDIR), removed at the end; every receipt used below is pasted here first.

## 1. Capture identity (observed)

```
$ file 0435b64f65c3ea7ddc6bb92e.raw/.pdf/.txt
.raw: PDF document, version 1.7   .pdf: PDF document, version 1.7   .txt: Unicode text, UTF-8 text
$ cmp -s .raw .pdf && echo RAW_EQ_PDF          → RAW_EQ_PDF
sha256 .raw/.pdf 1a46faaee6baae091b09dc808627942d411e3cb44646770070380f62eab7da63
sha256 .txt      a2f33bfa34a0b6dcbb70e9aadbc6044c92f54ebe088c987a4305d3d7594a12e3   (43,744 B)
key = sha256(url)[:24] → 0435b64f65c3ea7ddc6bb92e   (= the cache filename)
$ pdfinfo .pdf → Pages 30 · Creator/Producer Adobe Acrobat Pro DC (32-bit) 21.1.20138
                 CreationDate Tue May 30 12:39:46 2023 -03 · ModDate Thu Aug 3 2023 -03 · 960118 bytes
$ pdffonts → embedded CID TrueType: SimSun, MicrosoftYaHei, TimesNewRomanPSMT … (Unicode maps yes)
$ pdfimages -list → 14 images, ALL on page 1 (437x94 banner, 24x24 icons); 0 images on pages 2–30
page sizes: p1 841.92x594.96 (A4 landscape); p2–p30 595.32x841.92 (A4 portrait)
p1 first line: "2023/5/30 23:37  … 关于发布上市药品临床安全性文献评价指导原则（试行）的通告（2019年第27号）"
p2 first lines: "附件" / "上市药品临床安全性文献评价指导原则" / "（试行）"
$ strings .raw | grep -ci pharmwyp → 0      $ grep -ci pharmwyp .txt → 0
```

Text form: 21,573 characters, 906 lines, 13,630 non-space chars, **U+FFFD = 0**, NUL = 0, 29 page-foot markers `— 1 —` … `— 29 —` (notice page + 29 attachment pages = 30 pages, matching `pdfinfo`). Term counts: 检索 50, 数据库 25, 灰色文献 5, 灰色 7, 未发表 3, 会议论文 1, 产业报告 1, 咨询报告 1, 发表偏倚 3, 应当 38, **必须 2**; 药研日记 0, pharmwyp 0, 评论 0, 转载 0, 责任编辑 0.

**Faithful text form?** Yes, byte-for-byte: `pdftotext` is installed, and `pdftotext -layout .pdf out.txt && cmp out.txt .txt` is silent (same sha256 `a2f33bfa…`). `pdftotext` without `-layout` differs (37,420 B) — the sidecar is the *layout* form, so quotes keep their line breaks, which is what the offsets below index.

## 2. Is the copy a scan, a reprint, or a blog post with commentary? — **a reprint**

- **Not a scan**: text layer is born-digital (embedded CID TrueType fonts with Unicode maps, 0 page-image scans — the only 14 images are the page-1 banner/icons), and `pdftotext` reproduces 21,573 characters with 0 U+FFFD.
- **A reprint (print-to-PDF of the official page + its attachment)**: page 1 is the NMPA notice page itself — print header `2023/5/30 23:37`, the site's own footer `本站由国家药品监督管理局主办 版权所有：国家药品监督管理局`, the address `https://www.nmpa.gov.cn/xxgk/ggtg/qtggtg/20190618165701432.html` printed as the page address with `1/1`, and a `中 En` / `请输入关键字` chrome. Pages 2–30 are the attachment with `— 1 —`…`— 29 —` footers. Producer/Creator `Adobe Acrobat Pro DC 21.1.20138`, CreationDate 2023-05-30 12:39:46 -03, matching the printed header time (2023/5/30 23:37 in the print locale).
- **Not a blog post with commentary**: 0 occurrences of `pharmwyp`, `药研日记`, `评论`, `转载`, `责任编辑`, and no byline or host branding anywhere in the text layer or the raw strings. The third-party surface is the file host alone (the URL), not the page.
- No hyperlink either: `strings .raw | grep -c URI` → **0**, i.e. the nmpa address is *printed text*, not a link annotation.

## 3. The notice's own metadata (all located)

- Title: `关于发布上市药品临床安全性文献评价指导原则（试行）的通告（2019年第27号）` — occurs **2×** (print header at off 72, page heading at off 425), so the bare title cannot be a unique quote; the notice's number is instead fixed by the attachment filename `国家药品监督管理局2019年第27号通告附件.doc` (off 1100, unique) and its act by `…现予发布。` (off 710).
- Number: **2019年第27号** (3 textual occurrences: header, heading, attachment filename).
- Issue date, two distinct dates: signature `国家药监局` / `2019年5月23日` (offs 941 / 1086) and publication stamp `发布时间：2019-06-18` (off 602). The staged row calls them "dated 2019-06-18 and signed 2019年5月23日" — that matches.
- Issuance: `现予发布` (off 748) + `特此通告。` (off 761) + `附件：上市药品临床安全性文献评价指导原则（试行）` (off 773).

## 4. Literature-search clause map (what the instrument actually does)

| location | content |
|---|---|
| 二、方法学要点 (off 2230) → 3.全面查找证据 (off 3116) | 检索策略 defined at 3046 (数据库/范围/检索词/检索式/时间范围); 3131 全面查找 through 电子检索/手工检索 |
| off 3260 | `鼓励不限制语种，全面检索中外文数据库。` |
| off 3320–3420 | the grey-literature clause: collect unpublished material, four example classes, negative-results reason, `会引入发表偏倚` (cut at the line break before 倚) |
| 三、报告撰写规范 (off 7448) → 2.文献检索策略 (off 8108) | 检索途径、检索数据库、检索时限、检索式; language limit, hand search, and `是否检索灰色文献等关键问题。` (off 8165) |
| 五、附录（一）常用数据库和相关网站 (off 9790) | Cochrane, Pubmed, Embase, SinoMed（含 CBM）, CNKI, 维普, 万方 (10088 / 10178 / 10258), trial registries |

Mandate modality: the operative modal in this document is `应当` (38×). `必须` occurs only twice (off 4830 `但必须在最终报告中着重说明`, off 5881 `必须对个案病例进行总结分析`) — neither in the grey-literature clause. The four item classes are examples (`如…等`), not an exhaustive list.

## 5. Every claim in the assigned entry that rests on this document

Entry: staged `corpus/knowledge/quality-control-guideline-issued-text-r48.md` (3 source lines S185, S186, S190). Verdicts are mine; the entry is not patched.

| # | claim (first 80 chars) | verdict | located quote (offset in the .txt form) |
|---|---|---|---|
| A1 | "S190 … the counterpart document the entry compares the centre's guideline again" | **located** | `查找时应当注意收集未公开发表的文献，即“灰色文献”，如` @3320 + `若文献评价中只纳入已公开发表的文献会引入发表偏` @3411 |
| A2 | "Read against the regulator's own 2019 guidance for the same clinical domain, which" | located (2019 / regulator / domain) | `国家药品监督管理局2019年第27号通告附件.doc` @1100; `2019年5月23日` @1086; title in `…组织制定了《上市药品临床安全性文献评价指导原则（试行）》，现予发布。` @710 |
| A3 | "… *mandates* collecting 会议论文、未发表的学位论文、产业报告、咨询报告" | **located**, with the modal caveat of §4 | `会议论文、未发表的学位论文、产业报告、咨询报告等。灰色文` @3348 (`应当` + `如…等`; `必须` not used here) |
| A4 | "… and gives publication bias as the reason" | **located** | `若文献评价中只纳入已公开发表的文献会引入发表偏` @3411 — the term 发表偏倚 completes on the next line (`倚。`), so the quote is cut at the break |
| A5 | "… the contrast is now a statement about two **issued** documents rather than" | **located** (this document's issuedness) | `…，现予发布。` @710; `特此通告。` @761; `附件：…（试行）` @773 |
| A6 | source-cell provenance "the counterpart document … its collection duty for unpublished literature" | located | as A1; the duty is `应当注意收集`, the classes are examples |

Nothing in A1–A6 is absent or contradicted. Two provenance limits are reported in §7 (F1, F5), and the "two **issued** documents" reading holds on the text: the issuedness is textual (`现予发布` + annex), and the copy of that issued text is a third-party reprint of the NMPA page, not an NMPA-served file.

## 6. The second staged entry that cites the same URL (`grey-literature-mandate-scope-r48.md`, S190's `used-by` names both)

| # | claim (first 80 chars) | verdict | evidence |
|---|---|---|---|
| G1 | "The corpus has held the regulator's 2019 clinical-safety literature-evaluation" | **contradicted against the lane**, not groundable as stated against the staged package | lane `6365f15`: 0 files in `corpus/knowledge` contain `文献评价指导原则` / `临床安全性文献` / `2019年第27号`; `corpus/SOURCES.md` has 0 hits for `pharmwyp`, `nmpa.gov.cn`, `2019年第27号`. In the staged package the prior quotes sit in `grey-literature-and-chinese-search-record-r40.md` (row S130, gcpunion copy) and `regulator-mandate-vs-centre-silence-r47.md` and draw on **two different sentences** (off 8108 ff. search-report field; off 3320 ff. collection duty), so "both quotations come from the same sentence" does not hold |
| G2 | "The first is the collection duty already known: 查找时应当注意收集未公开发表的" | located | @3320, @3348, @3411 |
| G3 | "The second is **scope**: the guidance places 研究但未发表的临床研究（灰色文献）" | located | `研究但未发表的临床研究（灰色文献）及不良反应个案报道等。` @5298 (context: `包括以药品安全性为研究目的资料…` @5245, `正在研究（已获得中期研究结果）或已完成` @5278) |
| G4 | "The third is an **inclusion duty**: for grey literature initiated or funded by the" | located | `应当纳入研究；应当尽力获取其他灰色文献。` @7212; the holder clause `对于持有人发起或资助的灰色文` is at @7195, on the previous line (break before 献) |
| G5 | "And the requirement is **reportable**: the section on 报告撰写规范 makes" | located | `三、报告撰写规范` @7448; `2.文献检索策略：检索途径、检索数据库、检索时限及检索` @8108; `应当说明是否有检索限制（如语言限制）、是否手工检索、` @8138; `是否检索灰色文献等关键问题。` @8165 |

## 7. Findings (reported, not patched; staged surface, not the claims)

- **F1 — units error in staged row S144** (same URL, same capture): its evidence cell says "PDF text extracted with `pdftotext -layout`, 43,744 characters". 43,744 is **bytes**; the text is **21,573 characters** (13,630 non-space). S190's own cell states 21,573 correctly.
- **F2 — S144's relation claim is mis-stated**: "the NMPA original is linked inside the document". Measured: 0 URI strings in the raw, so there is no link; page 1 *is* a print of the NMPA page (its own footer, its own printed address, `1/1`). The original is reproduced, not linked.
- **F3 — three staged rows for one URL**: S144, S177 and S190 carry the identical 434-character URL (`python3` dedup over the 114 staged rows: `DUP ['S144','S177','S190']`). C2's bound test is *exactly one* lane Registry row whose FIRST source-cell URL is the document's URL, so only one of these may be minted (planned lane id `S120`); landing two fails the test.
- **F4 — recheck gap in the assigned entry**: it cites three sources but its `recheck: 180d —` sentence covers only the issued text and the release notice; S190, on which its substantive contrast rests, has no recheck item.
- **F5 — the "bookkeeping" correction targets a row the lane does not hold**: the entry says "The corpus already held a row for this guideline, quoting the **draft for comment**" and asks that the round-13 row be marked. At `6365f15` no lane entry holds `PICOS`, `应基于`, `文献评价指导原则` or `质量控制指南` (0 files each), and the lane`corpus/knowledge` (74 files) shares only 15 names with the staged package (55 files, 40 staged-only). The row meant is staged (S130 / gcpunion), cited by the staged `grey-literature-and-chinese-search-record-r40.md`; the correction therefore lands on the pending merge, not on lane state. Reported, not patched.
- **F6 — text-form limit, not a capture defect**: the two named flow figures (图 1 文献评价一般流程, 图 2 文献筛选流程) carry no extractable text; all 14 images are page-1 logos, so the figures are vector art. No claim may rest on figure interiors from the `.txt` form.

## 8. QUOTE machine lines

20 rows, all verified `text.count(quote) == 1`, on one line of the `.txt`, ≤160 chars, ≤25 whitespace words, offsets by `text.find` on the whole file. `entry` = the lane path that will cite it. Both entries cite this one URL, so each row's quote must be **pasted verbatim into its entry** and into `corpus/lessons/round-53.md` (C2: quote ∈ span, ∈ entry, ∈ lesson).

```
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	国家药品监督管理局组织制定了《上市药品临床安全性文献评价指导原则（试行）》，现予发布。	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	国家药品监督管理局2019年第27号通告附件.doc	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	附件：上市药品临床安全性文献评价指导原则（试行）	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	发布时间：2019-06-18	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	2019年5月23日	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	https://www.nmpa.gov.cn/xxgk/ggtg/qtggtg/20190618165701432.html	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	本站由国家药品监督管理局主办 版权所有：国家药品监督管理局	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	鼓励不限制语种，全面检索中外文数据库。	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	查找时应当注意收集未公开发表的文献，即“灰色文献”，如	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	会议论文、未发表的学位论文、产业报告、咨询报告等。灰色文	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	若文献评价中只纳入已公开发表的文献会引入发表偏	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	2.文献检索策略：检索途径、检索数据库、检索时限及检索	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	应当说明是否有检索限制（如语言限制）、是否手工检索、	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	是否检索灰色文献等关键问题。	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	（一）常用数据库和相关网站	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	⚫ SinoMed 数据库（含 CBM 数据库）	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	⚫ 万方数据库：http：//new.wanfangdata.com.cn/index.html	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	研究但未发表的临床研究（灰色文献）	corpus/knowledge/grey-literature-mandate-scope-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	应当纳入研究；应当尽力获取其他灰色文献	corpus/knowledge/grey-literature-mandate-scope-r48.md
QUOTE	S120	https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf	是否检索灰色文献	corpus/knowledge/grey-literature-mandate-scope-r48.md
```

Offsets of the same rows, in emission order (for `char N` anchors and for `build-spans.py`'s printed `QUOTE S120 char <N>`): 710, 1100, 773, 602, 1086, 1570, 1197, 3260, 3320, 3348, 3411, 8108, 8138, 8165, 9790, 10088, 10258, 5298, 7212, 8165. The last row's quote is a prefix of row 14's, so it too starts at 8165 — a `char N` anchor of 8165 satisfies both.

## 9. What the integration must satisfy (no rule changed; the claims' own text)

- One lane row only for this URL (F3); `used-by` naming exactly the existing citing entries — both staged entries cite it, so `S120` must name both and **both** must carry `source: S120 — <url>`.
- Since the document is BOUND, no `refused-doc` line may name its URL in `corpus/lessons/round-53.md`; the three-quote floor per bound id is met by the 20 rows above after the L1 pastes them into the entries and the lesson.
- The capture digest recorded in `spans.tsv` will be the `.txt` form's `a2f33bfa34a0b6dcbb70e9aadbc6044c92f54ebe088c987a4305d3d7594a12e3` (all 20 quotes are unique in the `.txt`, so `build-spans.py` picks the `.txt` branch, not the raw form).

## 10. Limits

No entailment judgement is claimed (the counter measures binding, quotes, spans, anchors — the round-50/51/52 limit restated in the claims). No live fetch: the notice's own nmpa address and the presence of the NMPA page on NMPA's host were not re-verified (L0 `8d77e6c1` open) — what is grounded is that this capture reproduces that page. Figure interiors are not groundable from the `.txt` (F6). The second entry's centre-side claims (S176/S185) were not re-grounded here.

VERDICT — attacked the staged S190 → planned S120 grounding of the pharmwyp copy of 国家药品监督管理局 2019年第27号 (title, number, 2019年5月23日 signature / 2019-06-18 publication, the 检索/数据库/灰色文献 clauses, and the copy's class): the copy is a **reprint** — a print-to-PDF of the NMPA page plus its 29-page attachment, no scan (0 page images, 0 U+FFFD, `.txt` byte-identical to `pdftotext -layout`, sha256 `a2f33bfa…`), no commentary (0 host tokens) — both citing entries' document claims come out **located** (A1–A6, G2–G5) with the reason clause naming 发表偏倚 across a line break, the lane at `6365f15` holds no row, entry or quote for this document (so the binding is new), and six staged-surface defects are reported unpatched (S144's byte/character unit error, S144's "linked" vs reproduced relation, three rows for one 434-char URL against C2's exactly-one-row rule, the entry's recheck omitting S190, the "round-13 row" the lane does not hold, and the textless figures).
