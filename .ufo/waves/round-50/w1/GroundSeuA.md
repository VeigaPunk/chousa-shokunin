# GroundSeuA — re-ground S136: CNKI 大学生论文管理系统使用手册（子账号）

round 50 · wave 1 · seat GroundSeuA · leaf (no dispatch) · no network, no live fetch
target entry: `corpus/knowledge/citation-matching-semantics-r41.md`
scratch `/dev/shm/chousa-r50-GroundSeuA` (deleted before this report lands) · no tool installed or upgraded

## 1. Capture identity

| field | value |
|---|---|
| URL | `https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf` |
| cache key | `sha256(url)[:24]` = `28750bcdf5d36cd90a7709fb` |
| text form | `28750bcdf5d36cd90a7709fb.txt`, **read as UTF-8** — every offset below indexes this form |
| raw | `28750bcdf5d36cd90a7709fb.raw`, PDF 1.7, 65 pages |
| digests | `.txt` `c799044be4e0e6e62ccf96175edc6f56490e5872569633eebf2a1606fdb694c6` · `.raw` `0f426ea25661fbee4f2becd5bbf83b1c627d3eb1d0265a11d7c2f9d7504e8370` |
| extent | 30,937 characters / 63,869 bytes in the .txt |
| staged id | S136 (row 61, staged `SOURCES.append.md`) → planned lane id **S106** |

```
$ python3 -c "import hashlib;print(hashlib.sha256('https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf'.encode()).hexdigest()[:24])"
28750bcdf5d36cd90a7709fb
$ sha256sum 28750bcdf5d36cd90a7709fb.txt 28750bcdf5d36cd90a7709fb.raw
c799044be4e0e6e62ccf96175edc6f56490e5872569633eebf2a1606fdb694c6  28750bcdf5d36cd90a7709fb.txt
0f426ea25661fbee4f2becd5bbf83b1c627d3eb1d0265a11d7c2f9d7504e8370  28750bcdf5d36cd90a7709fb.raw
$ file 28750bcdf5d36cd90a7709fb.raw
28750bcdf5d36cd90a7709fb.raw: PDF document, version 1.7, 65 page(s)
$ pdftotext -layout 28750bcdf5d36cd90a7709fb.raw /dev/shm/chousa-r50-GroundSeuA/re.txt \
  && sha256sum /dev/shm/chousa-r50-GroundSeuA/re.txt 28750bcdf5d36cd90a7709fb.txt
c799044be4e0e6e62ccf96175edc6f56490e5872569633eebf2a1606fdb694c6  /dev/shm/chousa-r50-GroundSeuA/re.txt
c799044be4e0e6e62ccf96175edc6f56490e5872569633eebf2a1606fdb694c6  28750bcdf5d36cd90a7709fb.txt
```

The text form is reproducible: `pdftotext -layout` over the `.raw` reproduces the `.txt` byte for byte, so the offsets below are re-derivable from the pinned raw digest.

## 2. Character and term counts (exact command)

```
$ python3 -c "t=open('28750bcdf5d36cd90a7709fb.txt',encoding='utf-8').read(); print(len(t), t.count('引文核对'), t.count('核对'), t.count('匹配'))"
30937 0 0 0
$ python3 -c "t=open('28750bcdf5d36cd90a7709fb.txt',encoding='utf-8').read(); print(t.count('查重'), t.count('检测'), t.count('复制比'), t.count('引文'), t.count('科研诚信'))"
0 181 47 10 0
```

So r41's count claim is exact: **30,937 extracted characters; 引文核对 0, 核对 0, 匹配 0**.

## 3. Located quotes (form: the `.txt` read as UTF-8; each occurs exactly once)

| # | char | len | ws-words | quote | what it grounds |
|---|---|---|---|---|---|
| 1 | 54 | 20 | 3 | `2014-03-10     V 5.0` | version stamp + issue date on the cover |
| 2 | 83 | 38 | 4 | `产品名称：“中国知网”大学生论文管理系统使用手册    共   65   页` | product name and 65-page extent (matches `file`: 65 pages) |
| 3 | 4144 | 85 | 2 | `2.6 仅去除第一作者本人文献....................................................................35` | §2.6 heading as printed in the TOC, page 35 |
| 4 | 22511 | 28 | 1 | `在创建文件夹页面中第一个选项为“仅去除第一作者本人文献”` | the option is a folder-page option |
| 5 | 22549 | 24 | 1 | `该文件夹下的所有检测文献在去除本人文献检测结果中` | it applies folder-wide |
| 6 | 22655 | 24 | 1 | `在创建文件夹时，勾选“仅去除第一作者本人文献”。` | §2.6.1: it is ticked at folder creation |
| 7 | 23039 | 32 | 1 | `如果检测文献作者不是相似文献中的第一作者，而是第二作者或第三作者` | §2.6.2: only first-authorship is removed |
| 8 | 23319 | 24 | 1 | `如果检测文件夹没有勾选“仅去除第一作者本人”选项` | §2.6.3: the un-ticked contrast |

Structure of §2.6, all from the text form: TOC line at 4144 (page 35); the body heading `2.6 仅去除第一作者本人文献` at **22493** (second occurrence — the string occurs twice, TOC + body, so it is not a locatable quote on its own); page footer `第 34 页` at 22434, form feed, then the heading; footer `第 35 页` at 22883. The body runs 22493 → 23432 (`第 3 章 信息统计`), i.e. printed pages 35-37. The one sentence that states the effect spans 22511-22627 (116 chars raw / 113 normalised), wrapped over four lines, so no single-line slice of it exceeds 28 chars: rows 4-5 carry its two longest single-line clauses, and a span built around 22511 covers the whole sentence.

```
QUOTE	S136	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	2014-03-10     V 5.0	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S136	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	产品名称：“中国知网”大学生论文管理系统使用手册    共   65   页	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S136	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	2.6 仅去除第一作者本人文献....................................................................35	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S136	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	在创建文件夹页面中第一个选项为“仅去除第一作者本人文献”	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S136	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	该文件夹下的所有检测文献在去除本人文献检测结果中	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S136	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	在创建文件夹时，勾选“仅去除第一作者本人文献”。	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S136	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	如果检测文献作者不是相似文献中的第一作者，而是第二作者或第三作者	corpus/knowledge/citation-matching-semantics-r41.md
QUOTE	S136	https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf	如果检测文件夹没有勾选“仅去除第一作者本人”选项	corpus/knowledge/citation-matching-semantics-r41.md
```

The staged id S136 is emitted here per this seat's contract; the lane `quotes.tsv`/`spans.tsv` id must be **S106**, because `c2-count.py:154-167` binds on the lane registry row id and `:173` counts every other `S###` token in an entry as `REF_ID_UNBOUND`.

## 4. What r41 asserts about this document, checked

- **Supported.** 30,937 characters and 引文核对/核对/匹配 = 0/0/0 (§2). §2.6 is a folder attribute: the option is the first option on the 创建文件夹 page (22511) and governs 该文件夹下的所有检测文献 (22549); only a first-author match is removed (23039). Title/version/date and the 65-page extent (54, 83; `file`). No 引文核对 section exists anywhere in the text form.
- **Imprecise — "the 查重 flow" (entry lines 24-25, 41).** The capture never uses 查重 (0 occurrences); it uses 检测 (181) and 复制比 (47). "查重" is the staged row's gloss, carried into r41's Observation *and* its Inference. Either mark it as the lane's gloss or use the document's own words (检测结果 / 去除本人文献检测结果).
- **Imprecise — "the 去除本人已发表文献复制比 figure".** §2.6's sentence names 文字复制比 ("完整检测结果和去除本人文献检测结果的文字复制比不同", inside 22511-22627); the bare phrase 去除本人已发表文献复制比 occurs 5 times in the manual — as a report button with 点击 it appears at 22940 and 23243 (twice, so no locatable quote). The sentence should name 文字复制比, or quote the button by its offset.
- **Understated — "neither does the 教师 manual, which instead uses 引文…".** This manual itself uses 引文 10 times, all in the report type 全文（标明引文）报告单 (offsets 3509, 13948, 19247, 20218, 21064, 21085, 21112, 21283, 21373, 21618). The "instead" contrast implies 引文 is absent here; it is present in the same report-sheet sense.
- **Not in the capture — the row's publisher.** Staged row S136 says "CNKI 科研诚信管理系统研究中心"; 科研诚信 occurs 0 times in the text form and `pdfinfo` shows Title `同方知网`, Author `Administrator`, Creator `WPS Office 个人版`, CreationDate 2014-03-11. The S106 row must not assert a publisher this capture does not show.
- **Minor.** "checkbox" (entry line 24) — the document says 第一个选项 and 勾选, never 复选框.

## 5. Blockers this capture can decide for the C2 target

1. **r41 cannot pass `inference-ground` as staged.** Observed, with an empty spans manifest and `{}` counts:
-   `python3 tools/inference-ground.py --entry <staged r41> --spans /dev/shm/chousa-r50-GroundSeuA/spans.tsv --counts /dev/shm/chousa-r50-GroundSeuA/counts.json` → `GROUND entry=citation-matching-semantics-r41.md section=1 bullets=0 tokens=0 grounded=0` / `FINDING INF_NO_BULLETS bullet=0 token=''` / `GROUND: FAIL`, exit 1. The Inference section (lines 33-43) is prose paragraphs; `inference-ground.py:128` recognises only lines starting `- ` or `* `. Even after bulleting, both bullets carry **zero** `S###` ids (`re.findall(r'\bS\d{3,}\b', inference section)` → `[]`), failing rule 2. `c2-count.py:218,226` scores `INFERENCE_GROUNDED` by this exit code, so the entry needs Inference bullets that cite S106/S135/S145 and carry tokens that occur verbatim in those ids' spans.
2. **The S106 `anchor` cell needs `char N` values that are quote offsets.** `c2-count.py:214-216` requires *every* `char N` in a bound row's anchor cell to be an offset of a quote row of that id. `char 22511` (row 4) or `char 23039` (row 7) satisfies it; a bare `char 30937` would not. The staged anchor cell has none.
3. **Tier.** Staged S136 is tier `C`, scope "negative scope only"; r41 also states the positive content of §2.6, and QUALITY 7 says a tier-C row is never sole support. S106 should be tier A or B scoped to §2.6's folder-attribute statement plus the absence of 引文核对, not C.

## 6. Not done here

The 教师 manual (S145/S107), the 管理员 manual (S135/S105) and the ISTIC page (S118/S104) were not opened — other seats. `c2-count.py`, `c1-count.py`, `build-spans.py` and `quote-substance-check.py` were read but not run against the lane: no `spans.tsv`, `quotes.tsv` or lesson exists yet, and writing them is the L1's job. No capture was fetched; all evidence is the on-disk cache pair above.

VERDICT: attacked the staged S136 provenance and r41's claims about the 子账号 manual — the 30,937-char and 0/0/0 counts reproduce exactly and §2.6 is a folder attribute on the 创建文件夹 page, but r41 fails `inference-ground` (INF_NO_BULLETS, exit 1), uses 查重 which occurs 0 times in the capture, and needs its S136→S106 renumbering plus `char`-anchored quotes before C2 can bind it.
