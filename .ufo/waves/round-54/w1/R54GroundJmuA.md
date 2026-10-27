# R54GroundJmuA — grounding pass A: staged S093 → lane S123 (JMU PDF copy of GB/T 7714-2025)

Leaf seat, no dispatch. Scratch `/fast/scratch/hyaku/chousa-r54/R54GroundJmuA` (TMPDIR there), removed at exit; no soffice run, no git/jj mutation, no tool install, no writes outside this report. Every fact below is re-read from capture bytes this round; the campaign's quotes and dates were used for nothing. No soffice was started, so no `soffice.bin` of mine can linger: `pgrep -u $USER -af R54GroundJmuA` → rc=1 (the two live `soffice.bin`/`oosplash` under `/fast/scratch/hyaku/chousa-r54/` belong to `R54CritSeparable`, a different seat).

## Inputs (digests recomputed, not copied)

```
sha256 13a34aa9bb107eefeb8bed6a50a0d574af84ff77a66940e8b88ea895fea1182f 190614 B  .qcache/0f33243fd7ac2fe88b85c1ba.txt
sha256 cb3ffbf5013e7a3a60e2c9408aef4fb65e2a23b58d785b57d8830a4c3d3c2a41 6209520 B  .qcache/0f33243fd7ac2fe88b85c1ba.raw  (b'%PDF-1.7', 45 /Type/Page objects)
sidecar: 83061 chars / 1834 lines, U+FFFD 0, ASCII letters 0, ASCII digits 0, mtime 2026-10-23 21:08 -0300
```
`sha256(URL)[:24]` → `0f33243fd7ac2fe88b85c1ba`, so the qcache key checks out against `https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf`. Entry `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/source-type-taxonomy-r37.md`; row `SOURCES.append.md:18` (`S093`), which cites 1/5.2/7.3/7.6/7.9/8.15/附录A, while the entry itself rests only on **1, 7.3, 7.6, 附录A**.

## Located fields (offset = `text.find` on the whole `.txt`; every string below occurs exactly once)

| field | printed value | offset |
|---|---|---|
| 标准号 + 代替 | `ＧＢ／Ｔ ７７１４—２０２５` (161, ×45 in body headers); `本文件代替ＧＢ／Ｔ ７７１４—２０１５《信息与文献 参考文献著录规则》` | 161; **3602** |
| 发布 date | `２０２５－１２－０２发布` | **424** |
| 实施 date | `２０２６－０７－０１实施` | **490** |
| 发布机构 | `国家市场监督管理总局 发 布` / `国家标准化管理委员会` | 525 / 561 |
| 起草依据 | `本文件按照ＧＢ／Ｔ １．１—２０２０《标准化工作导则 第１部分：标准化文件的结构和起草规则》的规定` | 3546 |
| ICS / CCS | `ＩＣＳ ０１．１４０．２０` / `ＣＣＳ Ａ １４` | 58 / 78 |
| 附录A status | `附录Ａ（规范性） 文献类型和文献载体标识代码` | 2512 (TOC) |

**ISO 690 relation: ABSENT from this document.** `t.count("690")`=0, `t.count("６９０")`=0, `t.count("ISO 690")`=0, `t.count("ＩＳＯ ６９０")`=0; `采用`→10 hits, none an adoption statement; `采标`/`等同`/`修改采用`/`非等效`→0. All 7 `ＩＳＯ` hits are references, not a 采标 relation: `ＩＳＯ ４`@8118 (§5.5 abbreviation rule), `ＩＳＯ ２１３７８`@36504, `ＩＳＯ ２１３７８`@72591, `ＩＳＯ／ＩＥＣ ８００７９`@73304, `ＩＳＯ／ＩＥＣ ８００７９`@73441, `ＩＳＯ ｈｏｍｅ ｐａｇｅ`@76040, `ＩＳＯ ４：１９９７`@81167. The ISO 690 relation belongs to the SAMR record (S085→S121, `本标准非等效采用ISO国际标准：ISO 690:2021。`), not to this copy; nothing in `r37.md` currently claims it, and nothing here can.

## Section 1 范围 (both load-bearing clauses locate cleanly)

`本文件规定了参考文献的著录信息源、著录用文字、著录用符号、著录通则、各文献类型著录项目与` @5506 / `著录格式以及参考文献标引体系编制法。` @5551 (split across lines). Then `本文件适用于作者和编制者著录参考文献。`@**5576** and `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。`@**5602**, each on one line, each ×1. The entry's two scope quotes are substantively exact; only their terminal punctuation is not (see defects D1/D2).

## Section 7.3 (line 4 of the body is where the entry's quote breaks)

Body lines at 11542: `'   文献类型标识、文献载体标识应按照附录Ａ著录。电子资源既应著录文献类型标识，也应著录文'` / `'献载体标识。'`. So `文献类型标识、文献载体标识应按照附录Ａ著录。`@**11542** is one line ×1, and `电子资源既应著录文献类型标识`@**11564** is one line ×1 — but the clause the entry prints as one string (`…也应著录文献载体标识`) **is not contiguous in the text form**: its count is 0. Example 7 confirms the composite practice: the §7.3 example at 11778 is `Ｑｕａｎｔｕｍ ｆｉｅｌｄ ｔｈｅｏｒｙ…ｃｈｅｍｉｃａｌ ｐｈｙｓｉｃｉｓｔｓ［ＥＢ／ＯＬ］` (one line, elided middle, ×1).

## Section 7.6 + the bracket convention (7.6 alone does not assign the bracket)

`电子资源的创建日期、发布日期、修改日期、引用日期应按照“ＹＹＹＹ－ＭＭ－ＤＤ”格式`@**14096** (line ends at `…用阿拉伯数字`, `著录。`@14145 wraps). Example @**14151**: `示例：（２０１２－０５－０３）［２０１３－１１－１２］`. 7.6 itself never says which side is 引用日期; §6 does: `“［］”用于文献序号、文献类型和文献载体标识、引用日期以及自拟的信息`@**8800**, and §8.15.3.2 spells the pairing `（创建或修改日期）［引用日期］`@50005 (also §8.11.2.2 @40022, §8.14 @47970).

## Appendix A tables A.1 / A.2 (counted, not eyeballed)

Parser over `表Ａ．１ 文献类型和标识代码`@57879 … `Ａ．２ 电子资源载体和标识代码`@58771, splitting each row on 2+ spaces: **17 rows**, in exactly the entry's order and with exactly the entry's codes —
`图书 Ｍ · 期刊 Ｊ · 报纸 Ｎ · 会议录 Ｃ · 学位论文 Ｄ · 报告 Ｒ · 标准 Ｓ · 专利 Ｐ · 网站、网页 ＥＢ · 档案 Ａ · 地图 ＣＭ · 数据集 ＤＳ · 预印本 ＰＰ · 汇编 Ｇ · 计算机程序 ＣＰ · 数据库 ＤＢ · 其他 Ｚ`.
Code width: **11 single-letter** (Ｍ Ｊ Ｎ Ｃ Ｄ Ｒ Ｓ Ｐ Ａ Ｇ Ｚ), **6 two-letter** (ＥＢ ＣＭ ＤＳ ＰＰ ＣＰ ＤＢ) — the entry's "single-letter codes" is false for a third of the table. Table A.2 @58955: **5 rows**, `磁带 МＴ`, `磁盘 ＤＫ`, `光盘 ＣＤ`, `联机网络 ＯＬ`, `缩微资料 ＭＭ` — matches the entry's five names/codes exactly.

## Preface change list (§o, the entry's "two consecutive standards" continuity claim)

One line @4736: `将文献类型“普通图书”“舆图”分别更改为“图书”“地图”` — it is **普通图书**, not 图书, that was renamed 图书. `增加了文献类型“预印本”及其标识`@4765 + `代码“ＰＰ”`@4788 (crosses a line break at `标识`/`代码`). `增加了电子资源载体“缩微资料”及其标识代码`@**4812**. `将“ＥＢ”代表的文献类型更改为“网站、网页”`@**4852**. Also present and unclaimed by the entry: §o's `缩微资料／ＭＭ` addition means one of the five carriers is new in 2025, so "5 carrier codes" is a 2025 count, not an inherited one.

## Quote machine lines (staged id = planned lane id S123)

```
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	本文件适用于作者和编制者著录参考文献。	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	文献类型标识、文献载体标识应按照附录Ａ著录。	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	电子资源既应著录文献类型标识	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	电子资源载体和标识代码应按照表Ａ．２著录。	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	电子资源的创建日期、发布日期、修改日期、引用日期应按照“ＹＹＹＹ－ＭＭ－ＤＤ”格式	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	示例：（２０１２－０５－０３）［２０１３－１１－１２］	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	“［］”用于文献序号、文献类型和文献载体标识、引用日期以及自拟的信息	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	网站、网页                        ＥＢ	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	地图                         ＣＭ	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	数据集                         ＤＳ	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	预印本                         ＰＰ	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）                 ＭＭ	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	将文献类型“普通图书”“舆图”分别更改为“图书”“地图”	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	增加了电子资源载体“缩微资料”及其标识代码	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	将“ＥＢ”代表的文献类型更改为“网站、网页”	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	２０２５－１２－０２发布	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	２０２６－０７－０１实施	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	本文件代替ＧＢ／Ｔ ７７１４—２０１５《信息与文献 参考文献著录规则》	corpus/knowledge/source-type-taxonomy-r37.md
```
(19 quotes, each `count==1`, each inside one line, ≤44 chars, ≤3 whitespace words. NB `代替ＧＢ／Ｔ ７７１４—２０１５` alone is ×2 — cover @239 and preface @3631 — so the preface form above is the unique one.)

## Staged sentences that do not reproduce, with narrower honest wording

- **D1** `…first clause: "本文件适用于作者和编制者著录参考文献",` → drops the terminal `。`. Fix: quote it with `。` (offset 5576).
- **D2** `…"本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献."` → terminal ASCII `.` where the text has `。`. Fix: `…著录参考文献。` (offset 5602).
- **D3** `Section 7.3: "文献类型标识、文献载体标识应按照附录Ａ著录。电子资源既应著录文献类型标识，也应著录文献载体标识."` → printed as one contiguous quote, but the clause is split by a line break at `…也应著录文|献载体标识。`; as a single string its count is **0**. Also terminal `.`→`。`. Fix: cite the two single-line quotes, or cut at the break.
- **D4** `Appendix A lists **17 document types** with single-letter codes` → 17 is right (row count), **"single-letter" is wrong**: ＥＢ ＣＭ ＤＳ ＰＰ ＣＰ ＤＢ are two letters (11×1, 6×2). Fix: "with one- or two-letter codes".
- **D5** `the change list records that 图书 and 舆图 were replaced by 图书 and 地图` → the renamed type is **普通图书**, not 图书: the table type 图书 survives, its former name 普通图书 does not. Fix: "普通图书 and 舆图 were renamed 图书 and 地图".
- **D6** `the code formerly used for EB now denotes 网站、网页` → the text changes the **type EB represents**, not the code: `将“ＥＢ”代表的文献类型更改为“网站、网页”`. Fix: "the document type that EB denotes was changed to 网站、网页 (the code EB is unchanged)".
- **D7** `Section 7.6 requires … with an example carrying both a creation date and a bracketed retrieval date` → 7.6 gives only the `YYYY-MM-DD` duty and a bare example; the bracket=引用日期 and parenthesis=创建/修改日期 assignment lives in §6 @8800 and the §8 type formats @50005, not in 7.6. Fix: cite §6 with §7.6, or say "an example pairing a parenthesised date with a bracketed one".
- **D8** (gap, not falsehood) the entry asserts `GB/T 7714-2025`, its 2025 date and its succession to 2015 without any located cover quote; this document supplies them at 424 / 490 / 3602. Add them, and note 实施 2026-07-01 predates `verified-at: 2026-10-23`, so "current" is checkable rather than assumed.
- Verified-true, for completeness: `17` types and `5` carriers, every one of the 22 codes, the row order, `缩写`-free scope wording, and the Unknown-section claim `the copy renders Latin letters in fullwidth` (**0 ASCII letters and 0 ASCII digits in 83061 chars**).

## Quarantine hand-check — register `S088` (`payload-absent`) on this same URL

Register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:42` records `payload-absent` for `磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）ＭＴ / 磁盘（ｄｉｓｋ）ＤＫ / 光盘（ＣＤ－ＲＯＭ）ＣＤ / 联机网络（ｏｎｌｉｎｅ）ＯＬ / 缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）ＭＭ`. Hand-check verdict: **not an absence — a column-whitespace artifact.** The literal string has count 0, and each of its five `label+code` fragments also has count 0; but splitting each at the code and re-matching `label\s*code` gives **1 hit for all five** (offsets 59025, 59073, 59116, 59161, 59201; the label→code gap is 17–34 characters in every row). The register's rendered payload deleted the 17–27 spaces pdftotext emits between the 载体类型 column and the 标识代码 column. Same class as the S080 artifact closed by `R54GroundSamrA`: the payload is on the cited page; the register's normalisation is what is absent. Recommend `present-with-whitespace-normalisation`, not `payload-absent`; I did not edit the register.

VERDICT: attacked S093 as the ground for lane S123 by re-parsing the JMU copy — all five target sections re-locate (scope in/out, 7.3 rule, 7.6 format+example, A.1's 17 rows/codes, A.2's 5 carriers) and yield 19 unique single-line quotes, and the pass falsified four staged claims (7.3 quote not contiguous, "single-letter codes", 舆图/普通图书 renaming, EB phrasal) plus one absent field (no ISO 690 relation anywhere in the document: `690`=0, `ＩＳＯ ６９０`=0, no 采标 statement) and closed quarantine row S088 as a whitespace artifact by finding all five label→code pairs in table A.2.
