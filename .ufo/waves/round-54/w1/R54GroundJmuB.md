# R54GroundJmuB — independent second pass, staged S093 → planned lane S123 (JMU PDF copy of GB/T 7714-2025)

Leaf seat, no dispatch. Read: frozen `claims.md`, the staged entry `…/merge/chousa/knowledge/corpus/knowledge/source-type-taxonomy-r37.md`,
its row `…/merge/chousa/SOURCES.append.md:18`, and the one theme row on this URL, `…/corpus-expansion-1/absent-defect-register.md:42` (S088).
No other seat's report was read.

## 1. Object and capture identity

```
$ sha256sum …/0f33243fd7ac2fe88b85c1ba.txt …/0f33243fd7ac2fe88b85c1ba.raw
13a34aa9bb107eefeb8bed6a50a0d574af84ff77a66940e8b88ea895fea1182f  …0f33243fd7ac2fe88b85c1ba.txt
cb3ffbf5013e7a3a60e2c9408aef4fb65e2a23b58d785b57d8830a4c3d3c2a41  …0f33243fd7ac2fe88b85c1ba.raw
$ cmp -s …raw …pdf && echo "raw==pdf identical"   -> raw==pdf identical
$ pdfinfo …raw | head -12   -> ModDate Mon Jan 12 05:00:17 2026 -03; Pages 45; Encrypted no; File size 6209520;
                               PDF version 1.7; no Title/Author/Creator/Producer lines printed
```
`.txt` text form: 83,061 chars, 1,834 lines, 45 `\f` = 45 pages, U+FFFD 0, control chars 45 (all 0x0c), U+3000 0.
URL (frozen): `https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf`

## 2. The document's own identity stamp

| item | bytes in the text form | line | offset |
|---|---|---|---|
| ICS / CCS | `ＩＣＳ ０１．１４０．２０` / `ＣＣＳ Ａ １４` | 1 / 2 | 59 / 73 |
| class, number, supersession | `中华人民共和国国家标准`; `ＧＢ／Ｔ ７７１４—２０２５` (45×); `代替ＧＢ／Ｔ ７７１４—２０１５` | 7 / 8 / 9 | 86 / 161 / 239 |
| titles | `信息与文献 参考文献著录规则`; `Ｉｎｆｏｒｍａｔｉｏｎ ａｎｄ ｄｏｃｕｍｅｎｔａｔｉｏｎ—Ｒｕｌｅｓ ｆｏｒ ｂｉｂｌｉｏｇｒａｐｈｉｃ ｒｅｆｅｒｅｎｃｅｓ ａｎｄ ｃｉｔａｔｉｏｎｓ ｔｏ ｉｎｆｏｒｍａｔｉｏｎ ｒｅｓｏｕｒｃｅｓ` | 14 / 15-16 | 271 |
| dates | `２０２５－１２－０２发布` / `２０２６－０７－０１实施` | 21 | 424 / 490 |
| issuer | `国家市场监督管理总局 发 布` + `国家标准化管理委员会` | 23-24 | 504 / 540 |
| TC | `本文件由全国信息与文献标准化技术委员会（ＳＡＣ／ＴＣ ４）提出并归口。` | 136 | 4943 |
| lineage | `——１９８７年首次发布为ＧＢ／Ｔ ７７１４—１９８７，２００５年第一次修订，２０１５ 年第二次修订；` … `——本次为第三次修订。` | 147-148 | 5321 |
| printing | `中国标准出版社出版发行` (phrase 1×; `中国标准出版社` 4×); `２０２５年１２月第１版 ２０２５年１２月第１次印刷`; `书号：１５５０６６·１－８２５５１ 定价 ７６．００元`; `版权专有 侵权必究` | 1816 / 1827 / 1829 / 1832 | 82465 / 82834 / 82916 / 83007 |

**Host stamp: absent.** `集美` 0, `jmu` 0, `xuebao` 0, `Jimei` 0 in the `.txt`; the PDF Info dict has no `/Title`,
`/Author`, `/Creator`, `/Producer`, `/Subject` (raw byte counts all 0). The colophon names only the national
issuers and 中国标准出版社, so the "集美大学学报 editorial office" attribution is **URL-only** — no byte in the
capture identifies the host. The staged row already scopes it as a hosted copy; no statement may promote that
provenance into the document's own identity.

## 3. Located quotes (machine lines; entry path `corpus/knowledge/source-type-taxonomy-r37.md`)

All eight satisfy `text.count == 1`, one line of the `.txt`, ≤25 whitespace words, ≤160 chars, byte-exact.

```
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	电子资源的创建日期、发布日期、修改日期、引用日期应按照“ＹＹＹＹ－ＭＭ－ＤＤ”格式，用阿拉伯数字	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	代码“ＰＰ”（见附录Ａ，２０１５年版的附录Ｂ），增加了电子资源载体“缩微资料”及其标识代码	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	表Ａ．１ 文献类型和标识代码	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	图书、期刊、报纸、会议录、学位论文、报告、标准、专利、网站、网页、档案、地图、数据集、预印本等的	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	表Ａ．２ 电子资源载体和标识代码	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	中国标准出版社出版发行	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	本文件适用于作者和编制者著录参考文献。	corpus/knowledge/source-type-taxonomy-r37.md
```

Offsets, in the order above (offset/line/chars): 5602/165/33 · 14096/449/48 · 4788/132/45 · 57879/1341/14 ·
58791/1363/48 · 58955/1372/16 · 82465/1816/11 · 5576/164/19. None is a headline line (title, number, dates,
issuers); the last is the staged entry's load-bearing quote and needs an offset of its own.

## 4. Negative sweeps (exact `text.count` on the whole `.txt`)

```
   0  GB/T 7714-2025        0  GB/T 7714-2015      0  ISO 690            0  ISO 690:2021
   0  非等效                0  等同                16  修改              35  文献类型标识
  32  文献载体标识        124  ＯＬ                  0  OL                22  ＥＢ
   0  EB                   15  引用日期              0  本系统不提供文本阅读服务
   4  版权                  1  图书馆员             12  作者
--- fullwidth / probe renderings
  45  ＧＢ／Ｔ ７７１４—２０２５   1  ＧＢ／Ｔ ７７１４－２０２５ (U+FF0D, colophon footer l.1833)
   7  ＧＢ／Ｔ ７７１４—２０１５   7  ＩＳＯ   0  ６９０   0  690   0  采标   0  集美   0  jmu
```

**Absent** (every negative claim on these carries this sweep): `GB/T 7714-2025`, `GB/T 7714-2015` (present only
in fullwidth), `ISO 690`, `ISO 690:2021`, `非等效`, `等同`, `OL`, `EB` (fullwidth `ＯＬ`/`ＥＢ` do occur),
`本系统不提供文本阅读服务`, `采标`, `集美`. **Present**: `修改` 16, `文献类型标识` 35, `文献载体标识` 32,
`ＯＬ` 124, `ＥＢ` 22, `引用日期` 15, `版权` 4, `图书馆员` 1, `作者` 12. `690` and `６９０` are both 0, so
`ISO 690` is absent in every rendering while `ＩＳＯ` occurs 7× and never with 690 (`ＩＳＯ ４` l.260;
`ＩＳＯ ２１３７８：２０１９` l.894, l.1626; `ＩＳＯ／ＩＥＣ ８００７９－２０－２` l.1636, l.1638; `ＩＳＯ ｈｏｍｅ ｐａｇｅ` l.1684;
`ＩＳＯ ４：１９９７` l.1781); the 规范性引用文件 block (l.280-284) lists only `ＧＢ／Ｔ ４８９４` and `ＧＢ／Ｔ ７４０８．１`.
**This capture cannot ground any ISO 690 or adoption/equivalence claim:** r36's "non-equivalent adoption of
ISO 690:2021" must rest on the SAMR record (S085), not here.

## 5. Findings against the staged entry (reported, not patched)

- **F1 — the 7.3 quote is not byte-exact and cannot be a span.** Entry text
  `文献类型标识、文献载体标识应按照附录Ａ著录。电子资源既应著录文献类型标识，也应著录文献载体标识.`
  → `text.count` **0**: the capture breaks after `…也应著录文` (`\n` at 11584) and closes with fullwidth `。`.
  Longest one-line piece: offset 11542, 42 chars, ending `…也应著录文` (1×), then the 6-char line-initial
  `献载体标识。`. A span built from the entry's version fails "inside its span file"; the L1 must cut at the break.
- **F2 — same class, scope quote.** `本文件不适用于…著录参考文献.` with ASCII `.` → 0× (capture: `。`, offset 5602);
  the same for `本文件适用于作者和编制者著录参考文献.` → 0×. Only the punctuation is wrong, but the entry also
  hard-wraps mid-sentence, which no located quote may do.
- **F3 — "17 document types with single-letter codes" is false for 6 of 17.** Table A.1 (l.1344-1360):
  `Ｍ Ｊ Ｎ Ｃ Ｄ Ｒ Ｓ Ｐ Ａ Ｇ Ｚ` = 11 single-letter; `ＥＢ ＣＭ ＤＳ ＰＰ ＣＰ ＤＢ` = 6 two-letter. The count 17 is right.
- **F4 — change-list pair mis-stated.** Entry: "图书 and 舆图 were replaced by 图书 and 地图". Text (l.131, offset
  4736): `将文献类型“普通图书”“舆图”分别更改为“图书”“地图”` — the first pair is 普通图书→图书, so as written the entry
  says 图书→图书.
- **F5 — `采标` is 0 here.** The Unknown's "the authority's portal serves no text for 采标 standards" is a
  cross-document statement about S086/S075 and has no ground in this capture.
- **Verified in the entry's favour:** A.1 has exactly 17 rows (l.1344-1360) and A.2 exactly 5 (l.1375-1379);
  7.6's `YYYY-MM-DD` requirement (offset 14096) and example `（２０１２－０５－０３）［２０１３－１１－１２］` (l.451); 预印本 `ＰＰ`
  added, 缩微资料 `ＭＭ` added, `ＥＢ` re-assigned to 网站、网页 (l.131-134); both section lists exist (entry: 1,
  7.3, 7.6, 附录A; row adds 5.2 l.254, 7.9 l.475, 8.15 l.1127); fullwidth Latin rendering confirmed by census.

## 6. Quarantine hand-check — absent-defect-register row S088 (this URL)

Row quote `磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）ＭＴ / 磁盘（ｄｉｓｋ）ＤＫ / 光盘（ＣＤ－ＲＯＭ）ＣＤ / 联机网络（ｏｎｌｉｎｅ）ＯＬ / 缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）ＭＭ`
→ `text.count` **0**. Its five carrier tokens are each present exactly once, on five separate padded table lines
(l.1375 `…ＭＴ`, l.1376 `…ＤＫ`, l.1377 `…ＣＤ`, l.1378 `…ＯＬ`, l.1379 `…ＭＭ`). The register flattened five table
lines into one `" / "`-joined string and dropped the column padding: the *quote form* is absent, the *payload* is
present. Verdict material for the lesson: not `fabricated`, not `unverifiable` — present-but-reflowed (S080 and
S096 sit on other documents and were not checked here).

## 7. Not done / out of scope

No A-pass report read; no C1, counter, LibreOffice, network or git invocation; nothing installed (`pdfinfo` and
`pdftotext` were already present and used read-only). S101's nine 著录项目 / 文献标志码 claims in the same entry
belong to the HIT `.doc`, not this capture. Scratch `/fast/scratch/hyaku/chousa-r54/R54GroundJmuB` removed at exit.

VERDICT: attacked the JMU capture's identity stamp and the staged S093→S123 entry with 8 unique located quotes and 18 exact-count sweeps — identity stamp complete, host mark absent, six negative terms confirmed absent (ISO 690 in every rendering), and the entry carries three reported defects (non-byte-exact 7.3 and scope quotes, "single-letter codes" false for 6 of 17 type codes) plus register row S088's quote present-but-reflowed.
