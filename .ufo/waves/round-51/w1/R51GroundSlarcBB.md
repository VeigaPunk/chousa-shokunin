# R51GroundSlarcBB — independent second pass on staged S117

seat R51GroundSlarcBB (scribe, round 51 wave 1) · item: second pass on staged S117, 实验动物与比较医学 2025;45(1):101-111, section 3 文献特征分析, the 检索策略 paragraph · no other seat's report opened (R51GroundSlarcBA's not read) · capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/c7266931a1731db3ff6ae77d.txt` — **the `.txt` read as UTF-8**, 69789 bytes / 50952 chars; every offset below indexes that form (QUALITY 76). `.raw` is PDF 1.4, 11 pages: not a text form, so no offset indexes it.

## Operability — capture, key, text form

```
$ python3 -c 'import hashlib;h=hashlib.sha256(b"https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237").hexdigest();print(h,h[:24])'
c7266931a1731db3ff6ae77de60cee46492c911fc11a59f5259d22a4f6c30ac8 c7266931a1731db3ff6ae77d   <- key matches: True
$ sha256sum c7266931a1731db3ff6ae77d.txt c7266931a1731db3ff6ae77d.raw
03342b7ded4f9d687a5319a739cf357e4fa37d96de20ce66cba6cc7f5adfe2dd  .txt   (69789 B, 2026-10-23 20:39:30)
815bea41f8c249010fa11f1d374e5977db3bac5e50999ba190788bd4fc51fd07  .raw   (1140215 B, 2026-10-23 20:39:30)
$ pdftotext -layout .raw /dev/shm/chousa-r51-R51GroundSlarcBB/regen.txt  →  regen chars 50952 = capture chars 50952, identical True
```

The `.txt` is exactly `pdftotext -layout` of the `.raw`: every offset is re-derivable from the on-disk pair.

## Identity stamp

- Title zh 提高动物实验系统评价/Meta 分析的证据确定性：GRADE 方法的实证研究 (`.txt:8-9`); en Improving the Certainty of Evidence in Animal Experiment Systematic Review/Meta-Analysis: An Empirical Study of the GRADE Method (`.txt:33-34`).
- Edition `Feb. 2025, 45(1) … 101` (`.txt:0`), 文章编号 `1674-5817（2025）01-0101-11` (`.txt:30`), 引用本文 `实验动物与比较医学, 2025, 45(1): 101-111` (`.txt:543-545`), 11 PDF pages = 101-111; DOI `10.12300/j.issn.1674-5817.2024.109` (`.txt:2`, PDF `/Subject`); 收稿 2024-07-26 / 修回 2024-12-03 (`.txt:536-538`); PDF `CreationDate 2025-03-12`, Producer Founder.
- **Host is not self-grounded**: `slarc` 0, `www.slarc.org.cn` 0, `http` 0, `/URI` 0 in the `.txt` *and* the `.raw`; the host lives only in the retrieval URL. Every other identity element is in the bytes.

## Located quotes — form: the `.txt` read as UTF-8; each occurs exactly once (`text.find`)

```
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	中国知网、万方、中国生物医学文献数据库	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	PubMed、Embase 和 Web of Science 数据库	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	从各数据库建立至 2024 年 4 月 1 日。	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	题 词 （MeSH/Emtree） 和 关 键 词	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	“animal model”“mice”“rat”“rabbit”“dog”“frog”	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	共得到 42 篇使用 GRADE 方法的动物实验 SRs/MAs	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	据确定性：GRADE 方法的实证研究[J]. 实验动物与比较医学, 2025, 45	corpus/knowledge/chinese-search-record-r39.md
```

`off`/`chars`/`words`/`.txt` line, same order: 11213/19/1/168 · 11299/34/6/169 · 11404/24/7/170 · 11501/25/7/171 · 11910/44/2/175 · 12390/32/6/180 · 49152/42/5/544 — all ≤160 chars, ≤25 words. Suggested span = the whole `.txt` line holding the quote (exact slice, strictly longer, contains it): line offsets/lengths 11141/92, 11234/104, 11339/96, 11436/108, 11846/108, 12323/99, 49080/114. A right-column-segment span would equal the quote for rows 1, 2, 4, 5, 6, 7 and violate "span longer than its quote".

## Negative sweeps — exact counts, three representations

`raw` = `str.count` on the `.txt`; `strip` = all whitespace removed; `reflow` = right-column segments joined, whitespace removed (the view that repairs the two-column interleave).

```
group        term                                                    raw        strip      reflow
searcher     検索者 / 检索者 / 检索人员 / 検索担当                     0 0 0 0    0 0 0 0    0 0 0 0
grey         灰色文献 / グレーリテラチャー / gray literature / grey…   0 0 0 0    0 0 0 0    0 0 0 0
hand-search  ハンドサーチ / 手検索 / 手工检索                          0 0 0      0 0 0      0 0 0
search date  検索日 / 検索期間 / 检索日期                              0 0 0      0 0 0      0 0 0
search date  检索时间                                                  1          1          1  (off 11334)
```

Near-misses, 0 raw and 0 reflow: 独立检索, 两名, 2名, 双人, 交叉核对, 一致性检验, Kappa/kappa, 检索小组, 图书馆员, 学科馆员, 信息专员, 实施检索, 执行检索, 进行检索, 由作者. `研究者` 4 raw / 3 reflow, none naming a searcher (14696, 16934, 21018, 25057 are all "研究者应…" recommendations).

**Absent**: every searcher term, every grey-literature term, every hand-search term, 検索日/検索期間/检索日期. **Present**: 检索时间 only — a window, never a per-strategy execution date.

Spacing hazard (why `raw` alone is not a sweep): `检索词` 0 raw but 2 strip/reflow; `主题词` 0 raw, 0 strip, 1 reflow — stripping does not cross the interleave, only `reflow` does. `检索策略` 2 raw (11428 = this paragraph, 21867 = section 5 prose), so a span must take 11428. The section heading is itself split: `3 动物实验 SRs/MAs 中应用 GRADE 方法的文献特征分析` is 0 contiguous while its halves are 1 (10925) and 1 (11045) — a grep for the heading as the Registry prints it fails.

## Findings

**F1 (depth).** Carried: six databases; the window `从各数据库建立至 2024 年 4 月 1 日`; MeSH/Emtree plus keywords; 15 Chinese and 21 English quoted free-text terms (per right-column segment `len(re.findall("“[^”]*”", seg))` = 8+6+1 on lines 172-174 and 1+6+6+5+2 on 174-179, `fruit fly` split by the interleave between lines 177 and 179); included count 42 (39 English, 3 Chinese). Not carried, all 0: 去重, 查重, 剔除, 重复文献, 检索式, 检索字段, 检索平台, 更新, 再检索, 补充检索, 滚雪球, 引文追溯, 文献类型, 语种, 检索日期, 检索者, 灰色文献, 手工检索. No per-database yield, so `42` is not reproducible and the entry must not present this record as one a reader can re-run to the same number.

**F2 (calibration).** Staged row `SOURCES.append.md:42` and the entry's Observation bullet 2 spell the list `PubMed、Embase和WebofScience`: **0** occurrences in the `.txt` (`Embase和` 0, `WebofScience` 0). The capture form is `PubMed、Embase 和 Web of Science 数据库` (1). Unquoted prose today, but it cannot be lifted as a verbatim quote, and a reader sweeping the row's own spelling finds nothing.

**F3 (calibration).** Inference bullet 3 cites body-only `S097` for "the Japanese hand-search field found in wave 3". `S097` is not a `source:` line (those are S116/S117/S119) and names no hand-search document in either frame: staged S097 = FEVER dataset page (`SOURCES.append.md:22`); lane S097 = J-STAGE Citation・被引用文献リンク機能 help (`corpus/SOURCES.md:107`). The hand-search support here is **S125** (`japanese-search-record-r38-amendment-2026-10-23.md:20`, `ハンドサーチ等により`). Drop `S097` or describe it by file path; never carry it.

**F4 (calibration).** Lane tool's own extractor over the staged entry (`inference_bullets` + `grounding_tokens`, `tools/inference-ground.py`; no spans exist yet): `section True bullets 4` · b1 `cites=[]` `tokens=0` · b2 `cites=[]` `tokens=1` (`what must a search record carry?`) · b3 `cites=['S097']` `tokens=0` · b4 `cites=['S117']` `tokens=0`. So b1-b2 are INF_UNCITED and b3-b4 INF_UNGROUNDED before any span is built; `S117` is scrubbed by `ID_RE` before `NUM_RE`, so the id never yields a token. Each S117-bearing bullet needs a backticked/double-quoted phrase of ≥2 whitespace words or ≥4 CJK chars (`has_two_words`, round-50 CJK floor) present in an S117 span — quote rows 1, 3 and 4 qualify.

**F5 (calibration).** `recheck:` on all three staged entries carries no runnable command and no `--root`: `grep -cE '^recheck:.*--root +"?[^/$"]'` → `chinese-search-record-r39.md: 0`, `japanese-search-record-r38.md: 0`, `japanese-search-record-r38-amendment-2026-10-23.md: 0`; committed lane control `citation-chain-fidelity-r24.md: 1`. Adjudication is the L1's; recorded because the S117 recheck names "the 2024-04-01 date bound", which quote row 3 confirms.

**F6 (depth, for the Unknown bullet).** The searcher-absence claim now carries its sweep for S117: 検索者 0, 检索者 0, 检索人员 0, 検索担当 0 in the `.txt` read as UTF-8, 0 in the stripped and reflowed views; near-misses 独立检索 0, 两名 0, 双人 0, 检索小组 0, 图书馆员 0, 学科馆员 0; 研究者 4 with no searcher named. The staged sentence ("Neither `S116`'s module list nor `S117`'s own record names the person who ran the search") is now **half** tested: S117 swept here, S116 not swept by me. The same sweep separates the other two fields — S117 carries **no** grey literature and **no** hand-search, so grey literature stays attributed to S116 and hand-search to S125.

## Limits

- Section scope by offsets only: 文献特征分析 11045, 4.1 15347, page 104 = 10495..13001; all seven quotes sit inside. Paragraph boundaries are unrecoverable in a layout extraction, so whether `共得到 42 篇…` shares the paragraph with the term lists is not established from this form.
- Quotes verified against the on-disk capture only: `tools/quote-reopen.py verify` fetches registry URLs live and was **not** run (L0 `8d77e6c1` open, no network). My check is `text.find` + `count == 1` in the named form.
- One journal's article; nothing here generalises to Chinese guidance. I ran no round-51 counter, wrote no production file, and nothing here scores C1, C2 or C3.

VERDICT: attacked staged S117's own search record against its capture — identity grounded on title/edition/DOI/dates (host absent from both forms), seven unique located quotes emitted, searcher/grey/hand-search/date sweeps 0 in all three representations with 检索时间 the only date term present; found the entry's `S097` hand-search citation unresolvable, its `Embase和WebofScience` spelling absent from the capture, four Inference bullets uncited or ungrounded, and a non-runnable `recheck:` line.
