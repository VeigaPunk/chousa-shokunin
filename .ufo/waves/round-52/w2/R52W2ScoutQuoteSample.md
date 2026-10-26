# R52W2ScoutQuoteSample — independent 15-row sample of spans.tsv

Attacked: 15 of the 38 rows of `corpus/evidence/round52/spans.tsv` (S113 6 rows, S114 9, S115 14, S116 9). I did not read the lesson table. Scratch `/fast/scratch/hyaku/chousa-r52/R52W2ScoutQuoteSample` (chk.py, ent.py), removed at the end. No tool installed.

## Method
- Rows picked by manifest row number (1-38): 2, 4, 5 (S113) · 9, 12, 14 (S114) · 16, 19, 23, 27, 29 (S115) · 31, 34, 36, 38 (S116). Split S113 3 / S114 3 / S115 5 / S116 4; chosen by position, before reading any entry sentence.
- For each row I derived the text form myself: key = sha256(url)[:24]; `.txt` if the quote occurs there exactly once, else `.raw`. S115's `.raw` starts with `PK\x03\x04`, so I used `python3 tools/capture-text.py <raw>` (19,682 chars). Then compared against the manifest.
- `chk.py` result (columns: row, id, form, sha256 of the file read == manifest, `form.count(quote)`, `offset+span.find(quote)`, `form.find(quote)`, `form[offset:offset+len(span)]==span file`):

```
2  S113 txt      sha_ok True count 1 off+find 2328  real_find 2328  spanslice_ok True
4  S113 txt      ... count 1 3139 3139 True
5  S113 txt      ... count 1 4850 4850 True
9  S114 txt      ... count 1 1650 1650 True
12 S114 txt      ... count 1 5530 5530 True
14 S114 txt      ... count 1 5744 5744 True
16 S115 raw-docx ... count 1 9    9    True
19 S115 raw-docx ... count 1 8389 8389 True
23 S115 raw-docx ... count 1 9257 9257 True
27 S115 raw-docx ... count 1 9428 9428 True
29 S115 raw-docx ... count 1 19521 19521 True
31 S116 txt      ... count 1 475  475  True
34 S116 txt      ... count 1 592  592  True
36 S116 txt      ... count 1 753  753  True
38 S116 txt      ... count 1 996  996  True
```
Manifest side: 15/15 sha256 match, 15/15 occur exactly once, 15/15 offset+find equals independent find, 15/15 span file equals the form slice. Whole manifest: 38 rows, longest quote 15 whitespace words (148 characters; the 25-word bound is blind to CJK — S113-2 is 148 characters in 4 whitespace words, met by the letter).
- Entry char anchors that are not manifest rows, rechecked against the same forms: S113 byline 2034, portal 7287; S114 title 16, header 920, BMJ 5694, footer 6121, unspaced item-6 string 0 hits, `翻译/译/translat` 0/0/0; S115 `使用したデータベース` 9408 and `使用した検索式` 9419 (1 hit each), `[第2.0版]` 42, 8471 = start of the section 3.1 heading (2 hits for the heading text, first in the TOC at 682), 1446 guideline title, 19496; S116 508, 555, 641, 815 (1 hit each). All equal the entry's stated char. `郑卿勇` occurs 3 times (2740, 4929, 4981), i.e. the entry's "appears only inside that file name" is FALSE in the capture — 2740 is outside the attachment name (see row 5 below).

## Judgement per row (entry sentence read after the check)
| row | id | quote (short) | verdict |
|---|---|---|---|
| 2 | S113 | PRISMA-S(PRISMA for Searching)作为…内在局限 (char 2328) | **weaker** |
| 4 | S113 | copyright=0, guiderPublishedTime=…originalUrl=, linkOutUrl=, (3139) | supports ("no original URL": `originalUrl=` empty) |
| 5 | S113 | NameList=[AttachmentFileName…郑卿勇.pdf)]) (4850) | supports the attachment claim; the sentence's next clause is **false** (below) |
| 9 | S114 | 详细说明获取文献的所有来源，包括 所有数据库、… (1650) | supports (the spaced spelling is real; unspaced = 0 hits) |
| 12 | S114 | From: Page MJ, McKenzie JE, …, et al. (5530) | supports "credits the checklist to" |
| 14 | S114 | 发布日期：2023-01-31 (5744) | supports "carries" (only 1 hit of the date) |
| 16 | S115 | 医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引 (9) | supports (title line) |
| 19 | S115 | 2.2節で定めた比較対照技術に対するRCTのシステマティックレビュー (8389) | supports; "opens the section" holds loosely: a parenthetical IP-note line sits between heading `3. 追加的有用性` and this sentence |
| 23 | S115 | PRISMA(…)声明 (9257) | supports (L15); L22's "it does not set a format for them" is a negative this quote does not test |
| 27 | S115 | ハンドサーチ等により未公表データを収集した場合は、…含める。(9428) | **weaker** |
| 29 | S115 | 上記の協力を受けた研究者の個人名や所属については原則として公開しない。(19521) | **weaker** |
| 31 | S116 | すべてのデータベース，研究登録，Web サイト，組織，文献リスト (475) | supports (five classes, item 6) |
| 34 | S116 | それぞれの情報源が最後に調べられた日付を記載する (592) | supports |
| 36 | S116 | 試験登録，Web サイトの完全な検索戦略を記載する (753) | supports (item 7, three classes; organisations and reference lists absent from item 7's list) |
| 38 | S116 | データを収集したレビュー担当者の数 (996) | supports (item 9, reviewer count, same independence question) |

**Counts: 15 sampled · quote once at the stated offset 15/15 · supports 12 · weaker 3 (rows 2, 27, 29) · unrelated 0.** Row 5 supports its own quote but sits in a sentence with an unsupported follow-on clause, counted below as an extra defect, not as "weaker quote".

## Weaker cases and the narrowing
1. **Row 2, S113-2/3 (entry chinese-prisma-s-reception-r52.md, bullet "The portal record carries the PRISMA-S reading's abstract in full").** The 简要介绍 block begins at ~2260 with a sentence the entry never quotes (`文献检索是系统评价（SR）的基石，但其报告质量长期存在不足，严重影响研究的透明度与可重复性。`, shown in `t[2200:2480]`) and continues past `…提出实践建议。` with a further sentence (`本文旨在为国内学者、期刊编辑及审稿人提供`, `t[2380:2520]`). The quotes show two sentences, not the abstract in full; "reads" also starts mid-block. Narrow to: "the portal's 简要介绍 block carries the abstract's second and third sentences, which state the 16-item PRISMA-S reading, its limits and the 中文数据库 recommendations" — or quote the whole block. Entry does not quote the first sentence (`'文献检索是系统评价' in entry` → False).
2. **Row 5 follow-on clause (same entry, bullet "The portal record is a record, not the article").** "The author's name appears only inside that file name" — 郑卿勇 occurs at 2740, 4929, 4981 (3 hits); 4929 and 4981 are the file name (and its duplicate inside the attachment object), 2740 is elsewhere (not in that file name). Narrow to: "the author's name appears in the capture at 2740 and inside the attachment file name (4929, 4981)", or open 2740 first (I did not read the context at 2740; unresolved whether it is an author byline). This is a stated universal over the capture that my count falsifies as worded.
3. **Row 27 (japanese-search-record-niph-form-r52.md L23 "Hand-searched unpublished data is counted in the flow chart, not hidden").** Source sentence: "if unpublished data were collected by hand search etc., include that in the above flow chart" (the next sentence, 承認申請に用いたデータは未公表のものでも含める, is cut). The entry's "so a record of a search for this form keeps the non-database route as a counted source" turns a flow-chart inclusion rule for unpublished data into a rule about every hand-searched/non-database source, and "counted" is the entry's word (the source says 含める = include, the flow chart's contents are not visible in the text form). Narrow to: "unpublished data collected by hand search is to appear in the flow chart that the text form refers to but does not reproduce".
4. **Row 29 (same entry, L16 header and L24 header).** Source: 原則として公開しない = "in principle not published". Header L16 "their names are not published" and L24 "and privately" drop the hedge (the quote is quoted correctly in the body). Narrow to: "…are, in principle (原則として), not published".

## Notes (not defects of the manifest)
- S116 rows 31/34/36/38: the `recheck:` line of the entry contains each quote as a `find()` probe, so entry_count of the quote string is 2–4 for S116 and also 2 for rows 16, 23, 27, 29 (second sentence use in the Inference section; the anchor `char N` is attached only to the first). Not an uniqueness problem: uniqueness is per capture form, not per entry.
- Row 16: the entry's source line cites chars 8996/9020/9189 for "section 3.1 … (char 8996, char 9020)"; at 8996 the text is `SRにおける文献検索期間について明記する。…`, i.e. body text of 3.1, not the heading (heading at 8471). Reads as the section's content, accepted; row 16's own quote is correct.

VERDICT: attacked a 15-row sample of the 38-row spans.tsv (S113–S116, S115 via capture-text): all 15 occur exactly once at offset+find with matching sha256 and span slices; entailment 12 supports / 3 weaker than the sentence (rows 2 abstract "in full", 27 hand-search flow-chart "counted source", 29 dropped 原則として) / 0 unrelated, plus one falsified universal in the row-5 sentence ("author's name only in the file name": 3 hits, 2740 outside it).
