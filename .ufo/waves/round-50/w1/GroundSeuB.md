# GroundSeuB — round 50 / wave 1 — independent second pass on the CNKI 子账号 manual

Leaf seat on capture `28750bcdf5d36cd90a7709fb` only: no other seat's report read, no lane file
written but this one, no network, no fetch, no install.

## Capture identity (verified)

```
.txt  63869 B  sha256 c799044be4e0e6e62ccf96175edc6f56490e5872569633eebf2a1606fdb694c6  30937 chars  1931 lines
.raw  6398584 B sha256 0f426ea25661fbee4f2becd5bbf83b1c627d3eb1d0265a11d7c2f9d7504e8370
key   sha256("https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf")[:24] = 28750bcdf5d36cd90a7709fb  ✓
$ cmp 28750bcdf5d36cd90a7709fb.raw 28750bcdf5d36cd90a7709fb.pdf   -> IDENTICAL
```

**Text form for every offset:** `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/
.qcache/28750bcdf5d36cd90a7709fb.txt` read as UTF-8 (`open(p,encoding='utf-8').read()`), 30,937
chars. It identifies itself (chars 0–600) as `“中国知网” 大学生论文管理系统使用手册（子账号）`, V 5.0,
2014-03-10, 65 pages, 作者 王诗云. `.raw` is the PDF byte stream; no page image was rendered, so
every claim is about the extracted text, not the layout.

## 1. Every use of 引文 — offsets, counts

```
$ python3 -c "text.count(term) ..."
引文 10 | 标明引文 10 | 全文（标明引文） 9 | 引证 2 | 引文核对 0 | 核对 0 | 匹配 0 | 查重 0
文献资源 0 | 比对库 3 | 比对 23 | 文字复制比 35 | 检测 181 | 引用 9 | 引注 14 | 参考文献 4 | 溯源 5
```

All ten offsets, each inside the report-form name `全文（标明引文）` (the tenth is that name
wrapped as `全\n文标明引文` in §2.4.2's body), all in chapter 2:

```
3509  TOC 2.4.2 line (entry at 3485)           13948 §2.2.1 (13548) 五种报告单 list
19247 §2.3.2 (15251) five report forms          20218 §2.4 intro (20092) five report forms
21064 §2.4.2 heading (21053)                    21085 §2.4.2 body 若选择查看“全文（标明引文）报告单”
21112 §2.4.2 body 标题会提示为“全\n文标明引文”   21283 §2.4.3 (21197) 该类报告单与全文（标明引文）…
21373 §2.4.4 (21338) …与全文（标明引文）报告单一致  21618 §2.4.5 (21530) …同全文（标明引文）报告单相同…
```

No occurrence names a feature, an input, or a checked object: the word is one report-form name.

## 2. Does it ever describe a check of a citation against a catalogue?

**No.** The checking feature is text-similarity duplicate detection; it never verifies a citation.

- `引文核对` 0, `核对` 0, `匹配` 0, `文献资源` 0; the check's own word is `检测` (181), never 查重.
- `引证` twice, both `引证关系` (19494, 21011): a statement on the duplicate-source list about the
  relation between the checked paper and an overlapping source, not a verdict on its citations.
- The one catalogue-like object is `比对库` (27798 §4.1.1 `勾选比对库，选择比对时间`; 29347, 29364 §5.2
  `加入个人比对库`): the corpus similarity runs against. No flow looks a citation up in it.
- The only system-side handling of a citation is *subtraction, not verification* — §2.3.2 (15452)
  `去除引用文献复制比：…`: the author's marked citations are trusted and excluded from the ratio.
- Citation-adjacent statements are display or flags: §5.2 (29207) `显示该文献的参考文献信息。`; §5.3
  (29635) a source is annotated "作者是否是本人，是否引用"; §5.4 文献溯源 (29853) traces overlap.
- Structurally, no TOC entry among 8 chapters names a citation-check flow (§3).

## 3. Table of contents — the flows it documents

`$ python3` over TOC chars 411–8748: 77 dot-leader lines = 8 chapter lines + 69 numbered entries
(23 at `x.y`, 46 at `x.y.z`). Theme-relevant entries, page and TOC offset:

```
ch1 系统使用前准备 411 · ch2 检测结果 1374 · ch3 信息统计 4443 · ch4 上传论文 6779 · ch5 结果查询 7440
ch6 问题库 7985 · ch7 用户管理 8097 · ch8 诚信档案 8534
p22 2.2.3 校内互检 (2120)            p24 2.3.2 各项检测结果展示 (2652)    p29 2.3.4 重合文字来源 (2856)
p30 2.4.1 简洁报告单 (3377)          p31 2.4.2 全文（标明引文）报告单 (3485)
p31 2.4.3 去除本人已发表文献报告单 (3575)  p31 2.4.4 全文对照报告单 (3662)  p32 2.4.5 跨语言报告单 (3764)
p35 2.6 仅去除第一作者本人文献 (4138)      p61 5.3 段落检测结果 (7766)      p62 5.4 文献溯源 (7873)
```

Negative TOC evidence: `引文` once (3509, the §2.4.2 line), `核对` zero times. Flows documented: setup,
detection + five report forms, statistics, upload/folders, result query incl. 段落检测结果 and 文献溯源,
问题库, 用户管理, 诚信档案. No citation-checking flow exists.

## 4. Located quotes (machine lines)

Each verified: `text.count(q)==1`, `text.find(q)==offset`, `len(q)<=160`, `len(q.split())<=25`, no tab,
no newline, in the `.txt` form. `staged-id` = planned lane id **S106**; the staged package carries this
document as row **S136** (`SOURCES.append.md:61`; `source: S136 — <url>` at `merge/chousa/knowledge/
corpus/knowledge/citation-matching-semantics-r41.md:3`), renumbered by the integrator.

```
QUOTE	S106	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	5.4 文献溯源...............................................................................................62	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S106	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	5.3 段落检测结果........................................................................................61	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S106	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	若选择查看“全文（标明引文）报告单”，则打开的报告单标题会提示为“全	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S106	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	该类报告单与全文（标明引文）报告单的大部分内容相同，其特殊之处仅在	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S106	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	系统能够生成一份针对检测文献的文本复制检测报告单，在报告单上，列出	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S106	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	以列表的形式展示重合文字来源，并展示其文字复制比例和引证关系，点击	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S106	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	去除引用文献复制比：指去除了作者在文中标明了引用的文献后，计算	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S106	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	点击“文献溯源”按钮，可以进入到文献溯源页面。	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S106	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	进入文件夹管理页面，填写文件夹名称，勾选比对库，选择比对时间，点击	corpus/knowledge/citation-matching-semantics-r41.md
```

Offsets in that order (for span files; slice the `.txt` form): 7879, 7772, 21074, 21272, 20102,
19468, 15452, 29853, 27778. None is the title or a §2.6 line; none repeats the staged §2.6 quote.

## 5. Second pass on the staged entry's claims about this document

Confirmed: `citation-matching-semantics-r41.md:13-16` says "zero occurrences of 引文核对, 核对 and 匹配
across 30,937 extracted characters" — measured 0, 0, 0 and `len(text)==30937` ✓; "no 引文核对 section at
all" ✓ (no 核对 anywhere, so no rephrased section either); `SOURCES.append.md:61`'s negative scope holds. Two deltas:

1. `citation-matching-semantics-r41.md:3` anchors this document only at `# 2.6 仅去除第一作者本人
   文献`. The 引文-bearing material is §2.2.1/§2.3.2/§2.4–§2.4.5 (plus §5.4 for the "closest
   thing" claim); under a §2.6-only anchor the entry's own quotes sit outside its declared anchor.
2. For the 子账号 manual the citable statement is that 引文 is 10/10 the report-form name 全文（标明引文）
   — the marked-quotation report form, not a citation being checked. Also `SOURCES.append.md:61` calls this
   "the 查重 (similarity-check) manual", but 查重 never occurs in the text; the manual's word is 检测, so an
   entry writing 查重 must mark it as the lane's shorthand.

## 6. Limits

One document, one text form; no page-image or layout check. `pdftotext` artifacts untouched (`比对哭` for
`比对库` at 19210; wraps splitting `全文标明引文`, `并且说明了文`/`献来源`). §3 pages are TOC figures. Nothing
asserted about the 管理员 or 教师 manuals — other seats' ground.

VERDICT: attacked the 子账号 manual's citation vocabulary and structure — 引文 is 10/10 the
report-form name, 引文核对/核对/匹配/文献资源/查重 are all 0, no TOC entry documents a citation-check
flow, so the manual documents similarity detection only; 9 new byte-exact quotes emitted with
offsets; the staged entry's zero-count claim confirmed and its §2.6-only anchor flagged.
