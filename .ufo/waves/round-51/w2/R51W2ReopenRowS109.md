# R51W2ReopenRowS109 — Re-open and falsify registry row `S109` (`corpus/SOURCES.md:119`)

seat: `R51W2ReopenRowS109` (reviewer, leaf; no subagent dispatch)
lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin` at tip `4436e279b91d8d68fd439c9095695035fbeeab74` (base `9ec1751a24231e899ceea4688e21c8edf6046d35`, freeze `d603f6f00f78d64f123d3aed2dd9f8701547a4ba`)
attacked: `corpus/SOURCES.md:119` (`S109`, staged `S116`), capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/fd468a36d78ff156b6200946.txt` (`sha256(url)[:24] = fd468a36d78ff156b6200946`)
Decode form for every located quote and offset below: **the `.txt` read as UTF-8** (`open(p, encoding='utf-8').read()`, 52,208 chars, 82,903 bytes, sha256 `90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc`). No network, no live fetch, no tool installed (pacman paused, untouched), no scratch left in `/dev/shm`.

## 1. Required commands and observed output

```
$ grep -n '^| S109 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
119:| S109 | 动物实验系统评价与Meta分析报告的规范撰写建议（郑卿勇 等）— 实验动物与比较医学 2025;45(4):496-507 — https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290 | paper | A | what this reporting-recommendation copy asks of a systematic review's search record and says of the absence of a reporting standard for animal-experiment reviews | 表 1 研究方案主体报告框架内容 row 3, section 2.1.1, section 2.4.1 and 表 2; capture .txt read as UTF-8, 52208 characters; char 14179, char 15310, char 15240, char 17709, char 22932, char 24606, char 24298 | the protocol table's search module carries the databases, the time range with terms and their logic, and grey-literature retrieval and recording; the method section asks for a complete strategy of at least one main database; the copy says no reporting standard exists for animal-experiment systematic reviews and advises the PRISMA framework | mined | 2026-10-25 | 365d | corpus/knowledge/chinese-search-record-r39.md |
$ awk -F'\t' '$1=="S109"' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/spans.tsv
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	41	spans/S109-1.txt	DOI:10.12300/j.issn.1674-5817.2025.017	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	4033	spans/S109-2.txt	1674-5817（2025）04-0496-12	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	14099	spans/S109-3.txt	表 1 研究方案主体报告框架内容	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	15060	spans/S109-4.txt	含动物实验特殊数据库	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	15160	spans/S109-5.txt	检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	15230	spans/S109-6.txt	灰色文献的检索与记录	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	17629	spans/S109-7.txt	尚无专门针对动物实验 SR 的报告规范	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	22852	spans/S109-8.txt	至少提供一个主要数据库的完整检索策略	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	23017	spans/S109-9.txt	AND，OR 等	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	23100	spans/S109-10.txt	参考文献追溯	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	23236	spans/S109-11.txt	表 2 动物实验系统评价的数据库检索参考	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	24218	spans/S109-12.txt	预印本平台	corpus/knowledge/chinese-search-record-r39.md
S109	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc	24526	spans/S109-13.txt	手工查阅期刊	corpus/knowledge/chinese-search-record-r39.md
$ grep -ln '^source: S109 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/*.md
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/chinese-search-record-r39.md
```

Offset check (`build-spans.py:44,119,139` stores `start = off - 80` in col 4 of `spans.tsv`; `c2-count.py:207,222` checks `int(offset) + span.find(quote) == text.find(quote)`):

```
spans/S109-1.txt:  span_off=41    +80 = 121   text.find=121   count=1 q='DOI:10.12300/j.issn.1674-5817.2025.017'
spans/S109-2.txt:  span_off=4033  +80 = 4113  text.find=4113  count=1 q='1674-5817（2025）04-0496-12'
spans/S109-3.txt:  span_off=14099 +80 = 14179 text.find=14179 count=1 q='表 1 研究方案主体报告框架内容'
spans/S109-4.txt:  span_off=15060 +80 = 15140 text.find=15140 count=1 q='含动物实验特殊数据库'
spans/S109-5.txt:  span_off=15160 +80 = 15240 text.find=15240 count=1 q='检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）'
spans/S109-6.txt:  span_off=15230 +80 = 15310 text.find=15310 count=1 q='灰色文献的检索与记录'
spans/S109-7.txt:  span_off=17629 +80 = 17709 text.find=17709 count=1 q='尚无专门针对动物实验 SR 的报告规范'
spans/S109-8.txt:  span_off=22852 +80 = 22932 text.find=22932 count=1 q='至少提供一个主要数据库的完整检索策略'
spans/S109-9.txt:  span_off=23017 +80 = 23097 text.find=23097 count=1 q='AND，OR 等'
spans/S109-10.txt: span_off=23100 +80 = 23180 text.find=23180 count=1 q='参考文献追溯'
spans/S109-11.txt: span_off=23236 +80 = 23316 text.find=23316 count=1 q='表 2 动物实验系统评价的数据库检索参考'
spans/S109-12.txt: span_off=24218 +80 = 24298 text.find=24298 count=1 q='预印本平台'
spans/S109-13.txt: span_off=24526 +80 = 24606 text.find=24606 count=1 q='手工查阅期刊'
```

## 2. Cell-by-cell audit against `fd468a36d78ff156b6200946.txt` (read as UTF-8)

Every located quote below is ≤25 whitespace words, ≤160 chars, and occurs **exactly once** (`text.count(q) == 1`) in `fd468a36d78ff156b6200946.txt` read as UTF-8.

1. **`id`** (`S109`) — **HOLDS**. New since `BASE_REV` (which ended at `S106`); maps staged `S116` (`SOURCES.append.md:41`).
2. **`source`** (`动物实验系统评价与Meta分析报告的规范撰写建议（郑卿勇 等）— 实验动物与比较医学 2025;45(4):496-507 — https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290`) — **HOLDS**.
   - Title & authors: `动 物 实 验 系 统 评 价 与 Meta 分 析 报 告 的 规 范 撰 写` (char `1176`, 19 words, 40 chars, count 1); `[第一作者] 郑卿勇（1998—），` (char `2947`, 2 words, 18 chars, count 1); self-citation `郑卿勇, 杨冬华, 马智超, 等 . 动物实验系统评价与 Meta 分析报告的规` (char `51391`, 8 words, 40 chars, count 1) + `范 撰 写 建 议 [J]. 实 验 动 物 与 比 较 医 学 , 2025, 45(4): 496-507. DOI:` (char `51507`, 20 words, 61 chars, count 1).
   - Journal/issue/pages/DOI: running header `496                      实验动物与比较医学 Laboratory Animal and Comparative Medicine                          Aug. 2025, 45(4)` (char `0`, 10 words, 119 chars, count 1); article no. `1674-5817（2025）04-0496-12` (char `4113`, 1 word, 25 chars, count 1); `DOI:10.12300/j.issn.1674-5817.2025.017` (char `121`, 1 word, 38 chars, count 1). URL hashes to `fd468a36d78ff156b6200946`.
3. **`kind`** (`paper`) — **HOLDS**. Peer-reviewed journal paper (`[文献标志码] A`, line 75) in *Laboratory Animal and Comparative Medicine*.
4. **`tier`** (`A`) — **HOLDS**. Argued by `scope`: `what this reporting-recommendation copy asks of a systematic review's search record and says of the absence of a reporting standard for animal-experiment reviews`. An own-document statement is primary (tier A) for what the document itself asks and states (improved from staged `S116`'s tier B + uncorroborated "no Chinese standard" framing).
5. **`scope`** (`what this reporting-recommendation copy asks of a systematic review's search record and says of the absence of a reporting standard for animal-experiment reviews`) — **HOLDS**. Scoped strictly to this copy's own search-record requirements and field-scoped absence statement; matches `corpus/knowledge/chinese-search-record-r39.md:8` (`ground:`).
6. **`anchor`** (`表 1 研究方案主体报告框架内容 row 3, section 2.1.1, section 2.4.1 and 表 2; capture .txt read as UTF-8, 52208 characters; char 14179, char 15310, char 15240, char 17709, char 22932, char 24606, char 24298`) — **HOLDS**.
   - Corrects staged `S116`'s wrong `表3 报告模块表` locator to `表 1 研究方案主体报告框架内容`.
   - States decode form (`.txt read as UTF-8`) and exact character count (`52208`).
   - All 7 `char N` values are exact `text.find(quote)` offsets of `S109` rows in `spans.tsv` (`S109-3`=`14179`, `S109-6`=`15310`, `S109-5`=`15240`, `S109-7`=`17709`, `S109-8`=`22932`, `S109-13`=`24606`, `S109-12`=`24298`), where `int(spans.tsv col 4) + 80 == text.find(quote)`.
7. **`teaches`** — **HOLDS** (every clause is directly stated in the capture):
   - Clause 1 (*"the protocol table's search module carries the databases, the time range with terms and their logic, and grey-literature retrieval and recording"*): carried by `表 1 研究方案主体报告框架内容` (char `14179`, 3 words, 16 chars, count 1), row `3         文献检索策略            （1）检索数据库（如 PubMed、Embase 等，含动物实验特殊数据库）` (char `15085`, 5 words, 66 chars, count 1; `含动物实验特殊数据库` at char `15140`), `（2）检索时间范围：` (char `15186`, 1 word, 10 chars, count 1) + `检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）` (char `15240`, 3 words, 32 chars, count 1), and `灰色文献的检索与记录` (char `15310`, 1 word, 10 chars, count 1).
   - Clause 2 (*"the method section asks for a complete strategy of at least one main database"*): under `2.4.1   文献检索策略` (char `22408`, 2 words, 14 chars, count 1), carried by `至少提供一个主要数据库的完整检索策略` (char `22932`, 1 word, 18 chars, count 1), with `AND，OR 等` (char `23097`, 2 words, 8 chars, count 1), `参考文献追溯` (char `23180`, 1 word, 6 chars, count 1), `手工查阅期刊` (char `24606`, 1 word, 6 chars, count 1), `表 2 动物实验系统评价的数据库检索参考` (char `23316`, 3 words, 20 chars, count 1) and `预印本平台` (char `24298`, 1 word, 5 chars, count 1).
   - Clause 3 (*"the copy says no reporting standard exists for animal-experiment systematic reviews and advises the PRISMA framework"*): under `2.1.1    遵循国际通用规范` (char `17069`, 2 words, 17 chars, count 1), carried by `尚无专门针对动物实验 SR 的报告规范` (char `17709`, 3 words, 19 chars, count 1) and `考 PRISMA 框架，对研究实施过程的细节进行全面 、` (char `17783`, 4 words, 28 chars, count 1).
8. **`status`** (`mined`) — **HOLDS**. Active citation in `corpus/knowledge/chinese-search-record-r39.md:3`.
9. **`opened`** (`2026-10-25`) — **HOLDS**. Matches `OPENED = "2026-10-25"` in `c2-count.py:56` and `verified-at: 2026-10-25` in the citing entry.
10. **`recheck`** (`365d`) — **HOLDS**. Valid `NNd` cadence (`sources-census.sh validate` passes with 0 errors on `S109`).
11. **`used-by`** (`corpus/knowledge/chinese-search-record-r39.md`) — **HOLDS**. Exact 1-to-1 match with `grep -ln '^source: S109 ' corpus/knowledge/*.md`.

## 3. Non-author re-open survivability

The row **survives** a non-author re-open without defect: `env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py` prints `BOUND=6/7 … ANCHOR_BOUND=6/6 … C2=PASS` (rc 0) and `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` prints `chousa ok` (rc 0). Every staged defect in `S116` (`表3` for `表1`, "no Chinese standard", unanchored `char N`) was repaired before landing.

VERDICT: attacked `corpus/SOURCES.md:119` (`S109`) across all 11 cells against `fd468a36d78ff156b6200946.txt` (UTF-8, 52,208 chars) — 11/11 cells HOLD (0 defects), all 7 anchor `char N` offsets match `text.find(quote)` and `spans.tsv` (`offset + 80`), every `teaches` clause is carried verbatim by the capture, and the row survives a non-author re-open.
