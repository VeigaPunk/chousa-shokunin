# GroundSxuScope — round 50 / wave 1 (scope pass, CNKI 管理员 manual)

seat: `GroundSxuScope` (scribe/scope) · leaf member, no dispatch
target: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/e3ca8f4fdd15420b80096a75.{txt,raw}`
url: `https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf`
lane entry this feeds: `corpus/knowledge/citation-matching-semantics-r41.md` (staged id **S105**)
network: none used; every byte below is the on-disk capture.

## 1. Capture identity and sizes

```
$ python3 -c "import hashlib;print(hashlib.sha256(b'https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf').hexdigest()[:24])"
e3ca8f4fdd15420b80096a75
$ file e3ca8f4fdd15420b80096a75.raw
PDF document, version 1.5, 57 page(s)
$ sha256sum e3ca8f4fdd15420b80096a75.pdf e3ca8f4fdd15420b80096a75.raw
d36191c72a5ee007e0354b5160d207cffa9e59be86536c997a7dcff9db8ebcb6  e3ca8f4fdd15420b80096a75.pdf
d36191c72a5ee007e0354b5160d207cffa9e59be86536c997a7dcff9db8ebcb6  e3ca8f4fdd15420b80096a75.raw
$ cmp e3ca8f4fdd15420b80096a75.pdf e3ca8f4fdd15420b80096a75.raw && echo IDENTICAL
IDENTICAL
$ sha256sum e3ca8f4fdd15420b80096a75.txt
2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e  e3ca8f4fdd15420b80096a75.txt
```

- `.pdf` bytes: **4,482,989** (= `.raw`, byte-identical; the `.pdf` and `.raw` are the same object).
- `.txt`: **38,174 characters**, 83,384 UTF-8 bytes, sha256 `2197abe2…4f71e`.
- **Lossless text decode: yes, and reproducible.** `pdftotext -enc UTF-8 -layout e3ca8f4fdd15420b80096a75.pdf out.txt` re-produced the cached `.txt` **byte-for-byte** (`equal True`, re-extract sha256 `2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e`). Plain (non-`-layout`) extraction gives 33,412 chars and does **not** match — the capture is `-layout` form.
- Decode health: strict UTF-8 decode succeeds; **U+FFFD = 0**; CJK U+4E00–U+9FFF = **20,192**; non-ASCII = 22,609; form feeds = **57** (= 57 PDF pages); running header string appears 56× (cover page carries none).
- PDF metadata (informational only, not a citation): `Title: 第一章：上传论文`, `Author: Administrator`, `Producer: Microsoft® Word 2016`, `CreationDate: Wed Jul 1 23:26:40 2020`. **Do not trust the `Title` field** — it names chapter 1, not the manual.

## 2. Document title and revision stamp

Title block, `.txt` read as UTF-8, chars 0–69:

```
知网学位论文学术不端行为检测系统\n      使用手册\n     （管理员）\n\n\n\n\n     更新时间：2020 年 7 月\n\x0c
```

- Document: **知网学位论文学术不端行为检测系统使用手册（管理员）**.
- Revision stamp: **更新时间：2020 年 7 月** at char offset **48** (single occurrence; agrees with the 2020-07-01 PDF CreationDate/ModDate).

## 3. Chapter and section numbering around §6.1

Chapters (TOC at head, body heading in back matter), from `re.finditer(r'第\s*\d+\s*章\s*\S+')`:

TOC offset / body offset (title): 1 198/10504 登录系统 · 2 1052/11624 上传论文 · 3 2121/13557 检测结果 · 4 5516/28919 结果查询 · 5 5825/29410 已发表文献 · **6 6739/30661 辅助功能** · 7 7231/31914 信息统计 · 8 7931/33385 管理员中心 · 9 9029/36071 设置. TOC forms are unspaced (`第1章`) except chapter 8, which is spaced (`第 8 章`) — the only spaced TOC line; every body heading is spaced (`第 6 章`).

TOC block for chapter 6 (offsets 6739, 6862, 6984):

```
第6章          辅助功能...................................................................................................... 37
      6.1 引文核对........................................................................................................ 37
      6.2 两两比对........................................................................................................ 38
      6.3 问题库............................................................................................................ 39
```

Body: `第 6 章 辅助功能` (30661) → intro line (30673) → `6.1 引文核对` (30727) → `6.2 两两比对` (31262) → `6.3 问题库`. §6.1 sits on printed page 37 (footer `37` at 30990, header at 31012), matching the TOC's `37`.
**Numbering traps for anyone re-grounding this document:**
1. The string `6.1` occurs **6** times (5046, 6868, 10207, 26957, 30727, 37677); only **2** are §6.1 (6868 TOC, 30727 body) — the others are `3.6.1` (TOC 5046, body 26957) and `9.6.1` (TOC 10207, body 37677).
2. The string `6.1 引文核对` occurs **2** times (6868 TOC with leading spaces, 30727 body, no leading spaces) — never quote it as if unique.
3. TOC writes `第6章` unspaced, body writes `第 6 章` spaced. A predicate keyed on either form alone will miss one half.

## 4. Occurrence counts and offsets (`text.find` sweep, `.txt` as UTF-8)

| term | count | offsets |
|---|---|---|
| `引文核对` | **4** | 6872 (TOC §6.1), 30731 (body heading), 30738 (definition), 30808 (text-box instruction) |
| `核对` | **11** | 6874, 12511, 30733, 30740, 30758, 30779, 30810, 30834, 30961, 31085, 31191 |
| `匹配` | **0** | — |

`核对` context per offset (14 chars either side): 6874 TOC §6.1 · 12511 `上传检测的文件的核对。` (metadata upload, **unrelated** to §6.1) · 30733/30740 §6.1 heading + definition · 30758 `为核对源内容` · 30779 `以核对引文内容的正确性` · 30810 `“引文核对”文本框` · 30834 `系统会自动进行核对` · 30961 `表示经过核对，没有找到` · 31085 `表示系统经过核对已经找到了` · 31191 `标识系统经过核对，判定该条引文与源内容相同`.
Neighbouring vocabulary counts in the same form: `比对` **83**, `引文` **22**, `相似` **38**, `检索` 8, `引证` 2 (both `引证关系` in the 报告单 description, 24844/25828 — not citation matching), `查证` 0, `校对` 0, `核实` 0, `查对` 0.

**Calibration finding:** this manual never says 匹配. The comparison verb is **比对**; the check is **引文核对**, whose source of truth is `以“中国知网”的文献资源为核对源内容`. An entry that writes "CNKI matches citations by …" and tags the word 匹配 to this document would be tagging a term the document does not contain (0 occurrences). The status vocabulary is also only partly lexical: `没找到` is named, while the orange and green states are identified **by colour only** (`第二类是橙色的标识`, `第三类则是绿色的标识`) — the document supplies no word for them.

## 5. Who uses the 管理员 account (as the manual states it)

The manual is written **for** the 管理员 account (title suffix `（管理员）`) and defines that account by its administrative relation to 子账号 users, not by naming an office:
- the main admin account is bound by CNKI staff at contract signing/renewal — `管理员账号绑定：新用户新订合同或老用户续订合同时提交主账号管理员手` (10692);
- it owns the 管理员中心 module — `管理员中心包括子账号管理、文献管理、子账号查询和文献转移功能。` (33431);
- it creates 子账号 users, allocates `上传剩余篇数` (8.1.2, 33704), sets their permissions (8.1.4), and binds their phones — `子账号的手机号码绑定由主账号管理员完成。` (34232);
- the account is per institution (`账号单位名称`, 1.3 at 11126; 用户列表 column `单位名称`, 8.1.6 at 34564).
No occurrence of `研究生院`, `学位办`, `教务` (0 each) — the manual never names the university office that holds the account.

## 6. Located quotes (machine lines)

All quotes: `.txt` read as UTF-8, each occurs **exactly once** (`text.count(q)==1`), each ≤25 whitespace words and ≤160 chars, offsets from `text.find`.

```
QUOTE	S105	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	更新时间：2020 年 7 月	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S105	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	第 6 章 辅助功能	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S105	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	引文核对是指，以“中国知网”的文献资源为核对源内容，将输入的引文内	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S105	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	容进行比对，以核对引文内容的正确性。	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S105	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	把待检测文献的参考文献复制到“引文核对”文本框，点击“搜索”按钮，	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S105	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	该列表的第一列显示的是是否查找到该引用文献，及引文内容的正确性。状	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S105	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	第一类是“没找到”，表示经过核对，没有找到与输入的这条引文一一对应	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S105	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	管理员中心包括子账号管理、文献管理、子账号查询和文献转移功能。	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S105	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	子账号的手机号码绑定由主账号管理员完成。	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S105	https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf	管理员账号绑定：新用户新订合同或老用户续订合同时提交主账号管理员手	corpus/knowledge/citation-matching-semantics-r41.md
```

Offset table for the same ten (chars in `.txt` as UTF-8): 48 · 30661 · 30738 · 30772 · 30793 · 30901 · 30947 · 33431 · 34232 · 10692. Each quote is one physical line of the `-layout` text; the definition sentence (30738 + 30772) and the status sentence (30901) are line-wrapped, so quoting across the wrap would embed a `\n` and break the single-line machine format — quote line-by-line, as above.

## 7. Staged-id collision check (read-only)

`grep -n "9e5cdd215a414bf6b5694912018de4c8" /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` → **4** rows, all one document: S124 (line 49), S135 (60), S180 (105), S187 (112), each with this exact URL. All four describe `§6.1 引文核对` and quote the same sizes I measured (4,482,989 bytes / 38,174 chars) — consistent with §1 above. Per the lane plan this document takes **one** id, S105; S124/S135/S180/S187 must not be carried into any entry body. Lane registry max is currently `S103` (`grep -rhoE "^\| S[0-9]{3}" corpus/SOURCES.md | sort -u | tail -3` → S101, S102, S103), so S105 is free and S104 is reserved for the ISTIC page.

## 8. What I did not do

- No network, no live fetch of the PDF (L0 `8d77e6c1` open); the gs.sxu.edu.cn copy was not re-requested, so the capture's provenance to that URL rests on the cache key only.
- No re-extraction of other captures (子账号 / 教师 manuals, ISTIC page) — other seats own those.
- No edit to any production file, entry, registry row, counter, or fixture; this report is my only write.
- No tool installed (nothing was needed); no pacman transaction attempted.

VERDICT: scoped the CNKI 管理员 manual (57 pp., 4,482,989 B PDF = `.raw`, 38,174-char `-layout` `.txt` reproduced byte-exactly, 0 U+FFFD), fixed its stamp 更新时间：2020 年 7 月 @48 and §6.1 引文核对 @30727 within 第 6 章 辅助功能 @30661, counted 引文核对 4 / 核对 11 / 匹配 **0** (verb is 比对, 83), and emitted 10 unique located quotes for S105 → `citation-matching-semantics-r41.md`.
