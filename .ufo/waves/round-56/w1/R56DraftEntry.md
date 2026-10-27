# R56DraftEntry — the grey-literature row of 药品临床综合评价工作流程指南, drafted by document (round 56, C2)

seat: `R56DraftEntry` · date: 2026-10-27 · claim: R56-C2 (frozen at `41c5892`, claims read first) · base `e5a37951`
reads: lane `99eff0ec` (the C2 integration, landed mid-seat) and `0c2f4ce` (wave spec) · no fetch (L0 `8d77e6c1` open) · no tool install, no pacman
scratch: `/fast/scratch/hyaku/chousa-r56/R56DraftEntry` (removed at exit; `TMPDIR` there, `PYTHONDONTWRITEBYTECODE=1`)

## 1. State found, and what this report therefore is

The seat's assignment was to draft `corpus/knowledge/grey-literature-field-china-r42.md` by document. While the seat ran, the
lane advanced: my first `git rev-parse HEAD` printed `0c2f4ce5b846526ad3d7f384cd517fb5470806db`, and a later `git log --oneline -8`
printed `99eff0eca3d7440aeb96a9afac6a421759b4f704 round-56: C2 integration — entry grey-literature-field-china-r42 by document
(rows S127-S130, S118 used-by), quotes/spans via tools/build-spans.py (23 bound + 1 held), lesson Gate draft`, with
`git merge-base --is-ancestor 99eff0e HEAD` → true (`git show --stat 99eff0e` lists the entry, `spans.tsv` + 23 span files,
`held/`, `quotes.tsv` and the registry rows). So the entry exists at the rev I read and the counter passes there:

```
$ python3 corpus/evidence/round56/c2-count.py
ENTRIES=1/1 (min 1) REFUSED_ENTRIES=0 / HELD_CITED=S118 HELD_BAD=0 / BOUND=4/4 (min 3) REFUSED=0
BOUND_IDS=S127,S128,S129,S130 GUIDELINE_BOUND=yes / REF_ID_UNBOUND=0 / NEW_GROUND=1/1
QUOTE_ROWS=23 ON_BOUND=23/23 / SPAN_IDS=4/4 / QUOTES_IN_{SPAN,ENTRY,LESSON}=23/23 / QUOTE_SHORT=23/23
SPAN_CONTEXT=23/23 / CAPTURE_BOUND=23/23 / SUBSTANCE=PASS / ANCHOR_BOUND=4/4 / INFERENCE_GROUNDED=1/1
QUARANTINE_VERDICTS=0/0 () / QUARANTINE_BLOCKED_ADOPTED=0 / C2=PASS          (EXIT=0)
```

I did not write the lane. This report is (a) an independent draft of the same entry, derived from the five text forms, (b) a
measurement of that draft in a scratch lane copy, and (c) the conflicts between the draft and the landed text, reported
verbatim and not patched.

## 2. Measurement of the draft (scratch lane copy, not the lane)

```
$ git -C lane archive 99eff0e | tar -x -C $S/lane          # scratch copy
$ cp entry.md $S/lane/corpus/knowledge/grey-literature-field-china-r42.md
# 20 span files + spans.tsv built from the forms at line offsets; the S127-S130 anchor cells in the copy's
# SOURCES.md re-pointed to my offsets; my 20 quotes appended to the copy's lesson (scratch only)
$ python3 corpus/evidence/round56/c2-count.py --root $S/lane
ENTRIES=1/1 (min 1) REFUSED_ENTRIES=0 / HELD_CITED=S118 HELD_BAD=0 / BOUND=4/4 (min 3) REFUSED=0
BOUND_IDS=S127,S128,S129,S130 GUIDELINE_BOUND=yes / REF_ID_UNBOUND=0 / NEW_GROUND=1/1
QUOTE_ROWS=20 ON_BOUND=20/20 / SPAN_IDS=4/4 / QUOTES_IN_{SPAN,ENTRY,LESSON}=20/20 / QUOTE_SHORT=20/20
SPAN_CONTEXT=20/20 / CAPTURE_BOUND=20/20 / SUBSTANCE=PASS / ANCHOR_BOUND=4/4 / INFERENCE_GROUNDED=1/1
QUARANTINE_VERDICTS=0/0 () / QUARANTINE_BLOCKED_ADOPTED=0 / C2=PASS          (EXIT=0)
$ python3 tools/inference-ground.py --entry …/grey-literature-field-china-r42.md --spans …/spans.tsv --counts /dev/null \
    --registry …/SOURCES.md --root $S/lane
GROUND entry=… section=1 bullets=5 tokens=9 grounded=9 / GROUND: PASS
```
Two failed legs before these receipts, kept as they ran: the first build gave `ANCHOR_BOUND=1/4 INFERENCE_GROUNDED=0/1`
(cause: I patched `split("|")[5]`, the scope cell, instead of the anchor cell, and one Inference bullet cited no id); the
fix was a rebuilt copy, not a narrowed claim.

## 3. The draft entry (41 lines)

```
# A Chinese society's drug-evaluation workflow guideline puts grey literature among its ten information sources and grades the whole list Ⅰ级/A, which singles out nothing; the national commission's management guideline prints the term nowhere

source: S127 — https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf — 药品临床综合评价工作流程指南（2025 版）（征求意见稿）, the draft for comments served by the 全国团体标准信息平台: its cover block, 表 1 证据分级与推荐强度分级 and 7.2.3.3 信息来源; text form `.qcache/b27ffd2f0161104c6a28c9f5.txt` read as UTF-8 with universal newlines (70,038 characters, 0 U+FFFD) — char 360, char 425, char 8289, char 8469, char 23849, char 24624
source: S128 — https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf — 《药品临床综合评价工作流程指南》编制说明, the draft's explanatory note on the same platform: its title, 任务来源, the dated method stage (2) and the policy background; text form `.qcache/de9f5afc3809acbf61f4d5bb.txt` read as UTF-8 with universal newlines (7,031 characters, 0 U+FFFD) — char 4, char 97, char 3112, char 4956
source: S129 — https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf — 药品临床综合评价工作流程指南, the guideline as published in 中国药房 2025 vol. 36 no. 19, pp. 2353–2365: 表 2 推荐强度分级标准, 表 7 药品临床综合评价的信息来源情况 with its 灰色文献 and 搜索引擎 rows, and the article's identifiers; text form `.qcache/5233bf47babaa1ca2b49ed15.txt` read as UTF-8 with universal newlines (80,732 characters, 0 U+FFFD) — char 503, char 759, char 8950, char 20610, char 22564, char 22614
source: S130 — https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf — 药品临床综合评价管理指南（试行）, served by nhc.gov.cn as an attachment, its cover naming 国家药物和卫生技术综合评估中心（国家卫生健康委卫生发展研究中心）and 国家卫生健康委药具管理中心 and dated 二〇二〇年十一月: the cover block and 指南起草说明; text form `.qcache/a42feae4448612f949cc715f.txt` read as UTF-8 with universal newlines (6,930 characters, 0 U+FFFD) — char 11, char 76, char 103, char 129
source: S118 — https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf — the issued 药品临床综合评价质量控制指南（2024 年版 试行）, held by the lane: cited below for a count over its text form only (no quote, no span row)
verified-at: 2026-10-27 — the four captures re-opened read-only from the campaign cache (no fetch; L0 `8d77e6c1` open); each backticked quote below occurs once, on one line of its form, at the char offset given, the offset being `form.find(quote)` on the whole form read with `open(p, encoding='utf-8', errors='replace').read()`
recheck: 180d — re-open the four PDFs and confirm the draft still prints the grey-literature item under 7.2.3.3 behind `（征求意见稿）`, that the journal's 表 7 still carries Ⅰ级 and A on both its 灰色文献 and its 搜索引擎 rows, and whether an issued (not 征求意见稿) T/CLPA text carrying the same list has appeared
ground: source hierarchy and search-record method — where a grey-literature source requirement sits in a Chinese drug-evaluation instrument, and what the grade printed beside it rates. The lane holds the regulator's report field (`grey-literature-and-chinese-search-record-r40.md`) and the issued quality-control guideline's text (`quality-control-guideline-issued-text-r48.md`); at this round's base no `corpus/knowledge` file held 中国循证医学中心 (`git grep -l 中国循证医学中心 e5a37951 -- corpus/knowledge` prints nothing, exit 1)
adopted: round 56 from the campaign package merge/chousa/ (staged `grey-literature-field-china-r42.md`), re-bound by document to S127–S130 (map in `corpus/lessons/round-56.md` `## Gate`); the sibling staged `grey-literature-national-route-r44.md` is not carried (same theme, same document set, and its claim about the national centre's documents is not what S128 prints); the staged three-channels reading is cut (see `#### Unknown`)

#### Observation

- **The draft lists grey literature as one of ten information sources.** Section 7.2.3.3 opens `从多种渠道获得相关信息资料` (`S127`, char 23849) and enumerates ten sources, the ninth reading `（9）灰色文献：未公开发表研究信息，可能包含了最新的研究成果和观点` (char 24624) — unpublished research information, which may carry the newest results and views — and the tenth the public search engine; no grade stands beside the ninth item, one annotation closing the whole list at char 24815 (证据等级：I 级；推荐强度：A).
- **The platform's copy is a comment draft.** Its cover prints `（征求意见稿）` (`S127`, char 360) and the issue and implementation dates as placeholders, `2025 - XX - XX 发布` (char 425), over a standard number printed T/CLPA XXXX—2025.
- **The draft names the grading systems it adopts.** It gives `中国循证医学中心的证据质量分级体系` (`S127`, char 8289) — the centre's name printed twice in a row, the first occurrence split by the line break at char 8284 — beside the Oxford strength standard, and 表 1 then defines Ⅰ级 as `系统评价、HTA、Meta 分析` (char 8469) and descends from there to Ⅴ级, 专家意见.
- **The published copy grades every row of its source table alike.** Under 表 7's header `信息来源                 信息内容                证据等级 推荐强度` (`S129`, char 20610) the row `灰色文献 未公开发表的研究信息，可能包含了最新的研究成果和观点           Ⅰ级    A` (char 22564) is followed by `搜索引擎 公众/媒体关注度等补充数据                        Ⅰ级    A` (char 22614), and the 文献数据库, 官方网站, 书籍专著, 临床试验注册数据库, 生产企业, 问卷调查, 临床资料 and 数据库 rows carry the same pair (chars 20727–22228).
- **The published scale pairs its top recommendation with Ⅰ级.** 表 2 prints `A        推荐，证据极有效（证据等级为Ⅰ级）` (`S129`, char 8950), with B for Ⅱ级或Ⅲ级, C for Ⅳ级 and D for Ⅴ级; that is the same five-step order 表 1 prints, and neither form prints a sentence calling Ⅰ级 the highest.
- **The published article is identified as an article.** `1001-0408（2025）19-2353-13` (`S129`, char 503) and DOI 10.6039/j.issn.1001-0408.2025.19.01 give the journal, year, volume, issue and page span, and its abstract states the method as `采用中国循证医学中心的证据分级体系进行证据分级评价` (char 759).
- **The note is the draft's own and names the national documents it follows.** `《药品临床综合评价工作流程指南》编制说明` (`S128`, char 4) records the project as `由中国药师协会平台立项` (char 97) and its stage (2) as `采用牛津大学循证医学中心制定的推荐强度分级标准对证据进行` (char 3112); its policy background lists `《药品临床综合评价质量控制指南（2024 年版 试行）》` (char 4956) among the national documents.
- **The commission-served management guideline carries no grey-literature wording.** Its cover prints `药品临床综合评价管理指南` (`S130`, char 11), `（国家卫生健康委卫生发展研究中心）` (char 76) as the national centre's parent body and `国家卫生健康委药具管理中心` (char 103) beside it, and is dated `二〇二〇年十一月` (char 129); the strings 灰色文献, 未公开发表, 灰色 and 未发表 each occur 0 times in its form.

#### Inference

- **Grey literature is a named source in the society's workflow guideline and absent from the commission-served management guideline.** `S127` carries `（9）灰色文献：未公开发表研究信息，可能包含了最新的研究成果和观点` and `S129` repeats the row, while `S130` prints `药品临床综合评价管理指南` and no 灰色 wording at all in its form; a search record may cite the requirement as the society guideline's, and may not cite it as the commission's.
- **The Ⅰ级/A beside grey literature is the source list's uniform grade, not a rating of unpublished studies.** In `S129` the same pair stands on the `搜索引擎` row and on every other row of 表 7 under the column headed `证据等级`, and `S127` prints one annotation for all ten items: a lane row may say the guideline grades its information-source list Ⅰ级/A, and may not say it rates grey literature above the rest — nor, as the staged reading had it, that the printed grade is a strength of recommendation, which is the separate column.
- **"Highest" is an order the forms print, not a word they use.** `S129` pairs `A        推荐，证据极有效（证据等级为Ⅰ级）` with the lower strengths, and `S127`'s 表 1 descends from Ⅰ级's `系统评价、HTA、Meta 分析` to Ⅴ级, 专家意见; no sentence in either form calls Ⅰ级 the highest, so a lane row should cite the pairing and the order, not a printed superlative.
- **The platform copy is a draft, so its lists are the draft's.** `S127` prints `（征求意见稿）` and `2025 - XX - XX 发布`, and `S128` is that draft's own explanatory note; the source list may be cited as the comment draft's and the graded table as the journal article's, and neither as an issued group standard.
- **The four captures print one instrument family, not three channels.** `S127` says the evaluator may obtain material `从多种渠道获得相关信息资料` and then enumerates ten sources; no capture prints a count of channels through which the requirement reaches practice, so the staged three-channels reading is not carried.

#### Unknown

- **Sweep of the five text forms.** `python3 -c "w=('灰色','未公开发表','中国循证医学中心');q='/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/';[print(k,len(open(q+k+'.txt',encoding='utf-8').read()),[open(q+k+'.txt',encoding='utf-8').read().count(x) for x in w]) for k in ('b27ffd2f0161104c6a28c9f5','de9f5afc3809acbf61f4d5bb','5233bf47babaa1ca2b49ed15','a42feae4448612f949cc715f','16fe8487aa97b98576a0dbac')]"` prints S127 `70038 [1, 1, 1]`, S128 `7031 [0, 0, 2]`, S129 `80732 [1, 1, 2]`, S130 `6930 [0, 0, 0]`, S118 `27609 [0, 0, 0]`.
- **The issued quality-control guideline prints no grey-literature wording either.** The lane's held capture of the 2024 年版 试行 质量控制指南 (39 pages) holds 灰色 0 times, so the staged entries' question whether that document lists the field the same way is answered in the negative for this capture; what it does require of a source is not read here.
- **Which document is issued.** No capture shows an issued T/CLPA text: the platform serves a comment draft with a placeholder number and placeholder dates, and the journal article is a publication of the guideline, not the standard itself.
- **Which management guideline is current.** The note's policy background and the journal article both name a 2021 年版试行 管理指南, while the nhc.gov.cn capture is dated 二〇二〇年十一月; their relationship is not established here, so the 2020 text's silence on grey literature says nothing about the 2021 version.
- **Why 表 7 grades every source alike.** The forms print the pairs but no note on how a grade attaches to a source category rather than to a study; that the pair reads as the list's grade is an inference from its uniformity, not a printed rule.
- **Completeness of the forms.** The absence counts are counts over the cache's `.txt` forms; S130's form ends mid-sentence at char 6930, so its silence is bounded to the captured form and not to the whole guideline.
- **Staged material not carried.** The sibling staged `grey-literature-national-route-r44.md` reads the national centre's documents as the guideline's inputs on the strength of a reference list; S128 names the national centre as the publisher of the 2022 technical guidelines and of the 2024 quality-control guideline in its comparison section, which is not a normative-reference list, so that provenance claim is cut.
- **Province.** The information-source requirement, the meaning of its printed grade and the search-record method are chousa's; what a drug clinical comprehensive evaluation must assess, and the grading systems themselves, are adjacent ground this entry reports and does not hold.
```

## 4. QUOTE machine lines (20; `span` = the containing line, offsets below)

```
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	（征求意见稿）	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	2025 - XX - XX 发布	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	中国循证医学中心的证据质量分级体系	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	系统评价、HTA、Meta 分析	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	从多种渠道获得相关信息资料	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S127	https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf	（9）灰色文献：未公开发表研究信息，可能包含了最新的研究成果和观点	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	《药品临床综合评价工作流程指南》编制说明	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	由中国药师协会平台立项	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	采用牛津大学循证医学中心制定的推荐强度分级标准对证据进行	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	《药品临床综合评价质量控制指南（2024 年版 试行）》	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	1001-0408（2025）19-2353-13	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	采用中国循证医学中心的证据分级体系进行证据分级评价	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	A        推荐，证据极有效（证据等级为Ⅰ级）	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	信息来源                 信息内容                证据等级 推荐强度	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	灰色文献 未公开发表的研究信息，可能包含了最新的研究成果和观点           Ⅰ级    A	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S129	https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf	搜索引擎 公众/媒体关注度等补充数据                        Ⅰ级    A	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	药品临床综合评价管理指南	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	（国家卫生健康委卫生发展研究中心）	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	国家卫生健康委药具管理中心	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S130	https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf	二〇二〇年十一月	corpus/knowledge/grey-literature-field-china-r42.md
```

Span file = the containing line, `form[offset:offset+len]` verbatim (S129 at 22564 takes the next line too, because the
quote is the whole line: `span len = 164 > quote 49`). `sid span_offset(span_len)->quote_offset`:

```
S127 324(43)->360 423(66)->425 8285(40)->8289 8432(53)->8469 23822(42)->23849 24620(42)->24624
S128 0(24)->4 77(32)->97 3105(35)->3112 4956(38)->4956
S129 444(84)->503 748(56)->759 8901(75)->8950 20610(116)->20610 22564(164)->22564 22614(114)->22614
S130 5(18)->11 69(24)->76 94(22)->103 117(20)->129
```

digests (sha256 of the `.txt` form, the form the counter derives for a PDF `.raw`): S127 `23306b9f84c95b06008ab5e4a5deaeb9b0e937041f5239ec57792710480f1d5d`,
S128 `7e3e3cf426a787a62b50fdae064e54ab28865a1ef5114cd0bf5687a87d2bd9d2`, S129 `beac2b7feb425a8885927850ea79ed5e916339c6f5cd4b45c3abbf1753f49b05`,
S130 `71fed1a3bc95a7e1377ef86e364f0aa183f0885175c8f0dce459b818a861688f`.

## 5. Conflicts with the landed entry (99eff0e) — verbatim, not patched

1. Landed title: “the grade printed beside it belongs to the recommendation, not to the literature”. `S129` 表 7's own header
   prints `信息来源                 信息内容                证据等级 推荐强度` (char 20610) and the 灰色文献 row prints `Ⅰ级` under
   证据等级 and `A` under 推荐强度 (char 22564): the Ⅰ级 column is the evidence grade, 推荐强度 is the A column. My draft's
   Inference 2 says the corrected thing — the pair is uniform across all ten rows, so it discriminates nothing.
2. Landed Observation 4 calls `A        推荐，证据极有效（证据等级为Ⅰ级）` (char 8950) “its scale”; it is 表 2 推荐强度分级标准 in
   `S129` (line 113 of the form) and is the same scale 表 1 prints in `S127`. Not a contradiction, a naming difference.
3. Landed `#### Unknown` says “the round-56 wave cross-checked them against an independent PDF extraction
   (`corpus/evidence/round56/`), and an absence claim stands only for a form shown complete”. My draft states the bound it
   observed instead: S130's form ends mid-sentence at char 6930 (`…结合药品临床应用监测等相关评价研究`), so its silence is
   bounded to the captured form.
4. Landed Inference 1 says the guideline's source list is cited “never as rating unpublished studies as top-grade evidence”;
   that clause survives on my reading (uniformity, not per-row quality) — the sentence I would not carry is the title's
   “belongs to the recommendation”.
5. Landed entry cites S118 with a quote backed by `held/spans.tsv` (23 bound + 1 held rows, 24 span files); mine cites S118
   for a count only and puts no S118 row in `spans.tsv`, because `ON_BOUND` counts every row against the four bound ids.

## 6. Findings — the four staged narrowings

- **Ⅰ级/A**: staged “grades it Ⅰ级 with recommendation strength A” is printed, but as a table-wide pair. `S129` 表 7 carries
  `Ⅰ级 … A` on all ten rows (chars 20727–22228, 22564, 22614), 搜索引擎 (public/media attention) included; `S127` prints one
  annotation for the whole 7.2.3.3 list at char 24815. Carried: “the guideline's source table records every source at Ⅰ级/A”.
- **‘highest grade’**: never printed. `S127` 表 1 orders Ⅰ级 (系统评价、HTA、Meta 分析, char 8469) to Ⅴ级 (专家意见); `S129` 表 2
  pairs A with Ⅰ级 (char 8950); the only 最高 in `S127` is char 17203, about the 层次分析法 method being the highest of seven
  alternatives and itself graded Ⅱ级/B (char 16810). Carried as an ordering, not a superlative.
- **‘no grey-literature wording at all’**: holds for `S130` (灰色 0, 未公开发表 0, 灰色文献 0, 未发表 0 in 6,930 chars) and also
  for the held `S118` (0 in 27,609 chars, 39 pages) — the staged entries' Unknown is answered, bounded to the forms.
- **‘three channels’**: cut. `S127` prints `从多种渠道获得相关信息资料` (char 23849) and enumerates ten sources; no capture prints
  a channel count, and the staged channels rested on round-6/round-7 entries, not on these forms.

## 7. Touched surfaces, out of scope, artifacts

- Lane: read-only throughout (`git rev-parse`, `git log`, `git show --stat`, `git merge-base`, `git archive` to scratch, `git grep`).
  No write to the lane, the fleet repo, `shokuknow`, or any PATH directory. Everything written lived under
  `/fast/scratch/hyaku/chousa-r56/R56DraftEntry` (lane copy from `git archive 99eff0e`, no git repo inside it) and is removed.
- Not mine, not touched: C1 (gate, battery, probes, `c1-count.py`), the round-55 W2 `R55W2*` items, `SCORECARD.md`, `LOG.md`,
  the lesson's Gate and Quarantine sections, and the registry rows themselves (I only re-pointed anchors inside the scratch copy).
- Artifact: the entry text is §3 and the manifest is §4; the scratch copy is deleted. Rebuild command for a landable copy:
  `git -C …/chousa-shokunin archive 99eff0e | tar -x -C $S/lane`, apply §3 over the entry, write §4's spans, then
  `python3 corpus/evidence/round56/c2-count.py --root $S/lane`.

VERDICT: I drafted the round-56 C2 entry by document and it survives the frozen counter — C2=PASS in a scratch lane copy
(`BOUND=4/4`, `QUOTE_ROWS=20`, all quote ledgers 20/20, `CAPTURE_BOUND=20/20`, `ANCHOR_BOUND=4/4`, `INFERENCE_GROUNDED=1/1`) —
while reporting, unpatched, that the landed title's claim that the Ⅰ级 belongs to the recommendation conflicts with 表 7's
证据等级 column header and with the uniform Ⅰ级/A on all ten source rows.
