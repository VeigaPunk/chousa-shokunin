# R56DraftRows — the four new Registry rows S127-S130, drafted and validated

seat: R56DraftRows (chousa lane, round 56 W1, leaf) · date 2026-10-27
lane: /home/vgpnk/Projects/shokunin/chousa-shokunin (base `e5a3795191601797613eb986b36fa0b1a73fe6a1`)
scratch: /fast/scratch/hyaku/chousa-r56/R56DraftRows (removed before yield; every output below was run there with
`export TMPDIR=<scratch> PYTHONDONTWRITEBYTECODE=1`; no tool installed, pacman untouched — nothing was needed)
scope: draft rows only. I wrote no lane file except this report; `corpus/SOURCES.md` was not edited by me. C1 and the
C2 measurement (`c2-count.py`) are other seats' items and were not run.

## Deliverable 1 — the four rows (11 cells each, no `|` inside any cell, first URL of the `source` cell is the document URL)

```
| S127 | 药品临床综合评价工作流程指南（2025 版）（征求意见稿）, T/CLPA XXXX—2025 — 中国药师协会, the draft for comments served by the 全国团体标准信息平台 (ttbz.org.cn) — https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf | docs | B | for what this draft lists as information sources (7.2.3.3, item 9 灰色文献) and the grading systems it names — a draft for comments whose number and dates are placeholders, so tier B for the draft's wording only, never for an issued group standard | 6 需考虑因素 证据分级与依据 (the search sources and the two grading systems), 7.2.3.3 信息来源 items (9) and (10), the closing （证据等级：I 级；推荐强度：A） line and the reference list that end the whole list, and the cover block; text form b27ffd2f0161104c6a28c9f5.txt, byte-identical to a pdftotext -layout run on the 39-page PDF, read as UTF-8 with universal newlines, 70038 characters, sha256 prefix 23306b9f84c95b06; char 166, char 360, char 425, char 8242, char 8285, char 23826, char 24624, char 24791, char 24849 | Under 7.2.3.3 the draft sets 灰色文献 as the ninth of the ten information sources an evaluation is told to gather (未公开发表研究信息), and the one grade line printed after item (10) is 证据等级 I 级 with 推荐强度 A, so a curator can name the instrument and the exact item where a grey-literature search enters it; the cover carries a placeholder number (T/CLPA XXXX—2025) and dates, so the row evidences a circulating draft, never an issued standard | mined | 2026-10-27 | 180d | corpus/knowledge/grey-literature-field-china-r42.md |
| S128 | 《药品临床综合评价工作流程指南》编制说明 — the draft's explanatory note, a 中国药师协会 project, served by the 全国团体标准信息平台 (ttbz.org.cn) — https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf | docs | B | for the draft's provenance as its own explanatory note states it — the proposing bodies, the dated method stage and the policy background — a note by the proponents, tier B, never for the content of the grading system it names | 一、工作简况 1.任务来源 (the three proposing bodies and the 立项 platform), 3.3 起草阶段 item （2） (the 2024 年 6 月-8 月 grading adoption) and 五、采用国际标准和国外先进标准情况 1.国内同类标准水平的对比 (the 2021 管理指南 background); text form de9f5afc3809acbf61f4d5bb.txt, byte-identical to a pdftotext -layout run on the 8-page PDF, read as UTF-8 with universal newlines, 7031 characters, sha256 prefix 7e3e3cf426a787a6; char 4, char 77, char 3064, char 3105, char 4792 | The note dates the adoption of the two grading systems at 2024 年 6 月-8 月 and names 中国药师协会药品临床评价工作委员会, 天津市药品使用监测和临床综合评价中心 and 天津医科大学总医院 as the proposing bodies, 由中国药师协会平台立项, so a curator can date and attribute the workflow guideline's method where the draft's own cover carries placeholders | mined | 2026-10-27 | 180d | corpus/knowledge/grey-literature-field-china-r42.md |
| S129 | 药品临床综合评价工作流程指南 (李正翔 et al.) — 中国药房 (China Pharmacy) 2025, vol. 36 no. 19, p. 2353, the journal-hosted PDF — https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf | docs | A | for the guideline as the journal published it — its 表 10 source rows with their 证据等级 and 推荐强度, and its recommendation scale — tier A for the published wording, never for the group standard's issued status | the title line (·指南与共识·, 药品临床综合评价工作流程指南Δ), the abstract's method sentence, the A 推荐，证据极有效（证据等级为Ⅰ级） scale row, and 表 10 其他研究的研究类型、研究方法及内容 with its 灰色文献 row; text form 5233bf47babaa1ca2b49ed15.txt, byte-identical to a pdftotext -layout run on the 13-page published PDF (two columns, so the form interleaves them line by line), read as UTF-8 with universal newlines, 80732 characters, sha256 prefix beac2b7feb425a88; char 10, char 748, char 3590, char 8950, char 22539, char 22564 | 表 10 grades its 灰色文献 row 未公开发表的研究信息, 可能包含了最新的研究成果和观点 with Ⅰ级 and A, while the scale defines A as 推荐，证据极有效（证据等级为Ⅰ级） — a recommendation strength — so a curator may cite the published guideline as recommending a grey-literature search and never as rating unpublished studies as top-grade evidence | mined | 2026-10-27 | 180d | corpus/knowledge/grey-literature-field-china-r42.md |
| S130 | 药品临床综合评价管理指南（试行）— 国家药物和卫生技术综合评估中心（国家卫生健康委卫生发展研究中心）and 国家卫生健康委药具管理中心, 二〇二〇年十一月, the 附件 served on nhc.gov.cn — https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf | docs | A | for the 2020 text's cover identity (title, the two issuing centres, the date) and for what its captured 16-page text form holds — the file is the 附件 served on the commission's own site, so tier A for those facts; the 2021 年版试行 the draft's note names is not related to this capture here, and the tier is never for which management guideline is current | the cover block of the 附件 (药品临床综合评价管理指南, 国家卫生健康委药具管理中心, 二〇二〇年十一月) and the whole form for absence counts (灰色 0, 检索 0, 中国循证医学中心 0); text form a42feae4448612f949cc715f.txt, byte-identical to a pdftotext -layout run on the 16-page PDF, read as UTF-8 with universal newlines, 6930 characters, sha256 prefix 71fed1a3bc95a7e1; char 11, char 103, char 129 | The 2020 management guideline's captured form names its two issuing centres and its date and holds 灰色 zero times, 检索 zero times and 中国循证医学中心 zero times across 16 pages, so a curator can see that the grey-literature source requirement and the grading systems reached this programme through the workflow guideline, not through this management text | mined | 2026-10-27 | 180d | corpus/knowledge/grey-literature-field-china-r42.md |
```

## Deliverable 2 — S118 `used-by` old→new (the entry cites S118 with its URL, so the cell must grow)

```
old: corpus/knowledge/quality-control-guideline-issued-text-r48.md, corpus/knowledge/western-instrument-alignment-r50.md
new: corpus/knowledge/quality-control-guideline-issued-text-r48.md, corpus/knowledge/western-instrument-alignment-r50.md, corpus/knowledge/grey-literature-field-china-r42.md
```

Ground for the change: `grep -rl 1736907153935975 corpus/knowledge` returns exactly those three entries, and the entry's
line matches `^source:\s*S118\s+—\s+https://www.bjhea.org.cn/…pdf(\s|$)` (`srcline True`). `status` (`mined`), `opened`
(`2026-10-26`), `recheck` (`180d`) and `anchor` are unchanged — rule 2 allows only status/recheck/used-by in place.

## Census validate (required run) — mirror = committed registry at `0c2f4ce` + my four rows + the S118 cell above

```
$ git -C <lane> show 0c2f4ce:corpus/SOURCES.md > $S/SOURCES.base.md      # 126 rows, 337 lines
$ python3 $S/mkrows.py                                                   # appends S127-S130 after S126, patches S118
mirror rows: 130
$ git -C <lane> archive 99eff0e | tar -x -C $S/lane && cp $S/SOURCES.draft.md $S/lane/corpus/SOURCES.md
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/lane/corpus/SOURCES.md
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	/fast/scratch/hyaku/chousa-r56/R56DraftRows/lane/corpus/SOURCES.md
exit=0
```

The five W04s are pre-existing rows S051/S053/S073-S075, untouched by me: the same command on the base registry alone
prints those five lines and `exit=0`, so my four rows add no finding of any code. No E01 (all four rows are 11 cells = NF 13), no E03/E04/E05/E06/E07/E08/E09/E10, no E11 — in particular the new
`used-by` path resolves (`corpus/knowledge/grey-literature-field-china-r42.md` exists in the copy). The `--file` form
resolves `used-by` against `dirname(file)/..`, which is why the mirror was placed inside a lane copy: run from bare
scratch every one of the 130 rows reports E11 and the output is meaningless.

## Receipts behind the cells

1. **Defined text form** — all five `.raw` are PDFs (`rawmagic 25504446`), so the C2 predicate's form is the `.txt`
   capture read with universal newlines. Sizes (characters / bytes) and file digests, computed with
   `open(p, encoding='utf-8', errors='replace').read()` and `sha256(file bytes)`:
   S127 70038/120386 `23306b9f84c95b06008ab5e4a5deaeb9b0e937041f5239ec57792710480f1d5d` · S128 7031/17547
   `7e3e3cf426a787a62b50fdae064e54ab28865a1ef5114cd0bf5687a87d2bd9d2` · S129 80732/118594
   `beac2b7feb425a8885927850ea79ed5e916339c6f5cd4b45c3abbf1753f49b05` · S130 6930/19242
   `71fed1a3bc95a7e1377ef86e364f0aa183f0885175c8f0dce459b818a861688f` (S118 27609/61909, unchanged). All four hold
   0 U+FFFD. Digests equal the `capture_sha256` of the matching `spans.tsv` rows, so the manifest and my cells name the
   same file.

2. **The `.txt` is a faithful extraction** — `pdftotext -layout <cache>/<key>.pdf $S/<key>.layout.txt` reproduces the
   cache `.txt` **byte for byte** for all four (`identical_layout= True`), and `pdfinfo` gives 39 / 8 / 13 / 16 pages,
   matching the formfeeds (S130: `cache segs 17` = 16 pages + trailing empty). So "byte-identical to a pdftotext -layout
   run on the N-page PDF" in each `anchor` is a check I ran, not a guess.

3. **Every `char N` is a real, once-only offset** — for each anchor number I re-derived the offset from the span files
   (`offset + span.find(quote)`, the counter's own rule) and then required `form.count(quote) == 1 and form.find(quote)
   == N`. All 23 span rows pass, all 23 anchor numbers pass; each row carries ≥1 (S127 nine, S128 five, S129 six,
   S130 three):

```
S127 char    166 once+at-offset=True  T/CLPA XXXX—2025          | char 23826 药品临床综合评价工作可根据…资料。全
S127 char    360 （征求意见稿）       | char 24624 （9）灰色文献：未公开发表研究信息，…
S127 char    425 2025 - XX - XX 发布  | char 24791 （10）搜索引擎：公众/媒体关注度等补充数据。
S127 char   8242 将百度等公共搜索引擎及 AI 检索工具作为补充检索。…中国循证 | char 24849 [31,35,79-82]
S127 char   8285 医学中心中国循证医学中心的证据质量分级体系，…推荐强
S128 char      4 《…》编制说明 | 77 床综合评价中心；天津医科大学总医院提出，由中国药师协会平台立项。
S128 char   3064 （2）2024 年 6 月-8 月，工作组采用中国循证医学中心中国循证医学中心的 | 3105 证据分级体系，…
S128 char   4792 （下简称为“管理指南”）。2022 年，国家药物和卫生技术综合评估中心（“国
S129 char     10 药品临床综合评价工作流程指南Δ | 748 研究方法建立研究证据，…推荐强度
S129 char   3590 China Pharmacy 2025 Vol. 36 No. 19   ·2353· | 8950 A        推荐，证据极有效（证据等级为Ⅰ级）
S129 char  22539 表 10   其他研究的研究类型、研究方法及内容
S129 char  22564 灰色文献 未公开发表的研究信息，可能包含了最新的研究成果和观点           Ⅰ级    A
S130 char     11 药品临床综合评价管理指南 | 103 国家卫生健康委药具管理中心 | 129 二〇二〇年十一月
```

   Quote budget: the longest manifest quote is 56 characters and 8 whitespace words (S129 `研究方法…推荐强度`); the
   `span` of each row is longer than its quote (`len(span) > len(quote)`), and each span is the exact slice
   `form[offset:offset+len(span)]` (`cap=True` on all 23). Section names in my `anchor` cells were located, not
   assumed: `7.2.3.3 信息来源` at 23809, `6 需考虑因素` at 7607 (its 证据分级与依据 paragraph holds 8242/8285), `一、工作
   简况 1.任务来源` at 25/…, `3.3 起草阶段` at 2508 (holds 3064), `五、采用国际标准和国外先进标准情况` at 4514 (holds
   4792), `·指南与共识·` at 0, `5.3 证据来源` at 10224, 表 10 at 22539.

4. **The counter's row legs, replayed against the real entry** — `url_of(my source cell) == url_of(document URL)` for
   all four (True, including the percent-encoded S129 path), `used-by split == [entry]` exactly (the only files citing
   any of the four URLs are the entry and the round-56 lesson, which is not an entry path), `^source: <id> — <url>` line
   present for S127-S130 and S118 (True), cells = 11, and the entry's S-token set is exactly
   `{S118, S127, S128, S129, S130}`.

## Findings (reported, not patched)

1. **A concurrent seat landed these rows while I worked.** At my start `corpus/SOURCES.md` held 126 rows and the rows
   were untracked in the worktree; at 01:49 `99eff0e` ("C2 integration") committed rows S127-S130, the entry, `spans.tsv`
   and the S118 cell. My draft was built on `0c2f4ce:corpus/SOURCES.md` (126 rows) so the census measures my rows and
   not its duplicates. Field comparison (my draft vs landed): `source` URL, `kind`, `tier`, `status`, `opened`,
   `recheck`, `used-by` identical on S127/S128/S129; S128's source prose and all four `scope`/`anchor`/`teaches`
   sentences differ in wording only. **One substantive disagreement: S130 `tier` — mine `A`, landed `B`.** I keep `A`
   for the narrow scope I wrote (cover identity + what the captured form holds) because the carrier is the commission's
   own domain serving the bare 附件, and this lane's own calibration denies A only where the carrier is not the
   authority (S118/S124 society and third-party hosts, S123 a journal-office upload). The landed reason conditions the
   tier on currency ("never for the current management guideline"), which is scope, not tier. If the L1 wants tier tied
   to an established publication act (the capture is the bare 附件, no notice page and no 文号 on disk, and no fetch is
   allowed under L0 `8d77e6c1`), `B` follows — that is the one place this draft asks for a decision.
2. **The lesson's S118 old→new is elided.** `corpus/lessons/round-56.md:32` logs the new value as `…, corpus/knowledge/
   grey-literature-field-china-r42.md`; the old value is printed in full. The full new cell is in Deliverable 2 above —
   worth pasting verbatim so rule 2's "logged old→new" is literally satisfied.
3. **The grade line that closes S127's source list is not unique.** `（证据等级：I 级；推荐强度：A）` occurs 31 times in
   the 70038-character form (and `推荐强度：A` 54 times), so it cannot be a quote row; the position after item (10) is
   what binds it. My `anchor` names it by position and keeps all `char` numbers on unique quotes.
4. **S129's form interleaves two columns line by line** (`5.3 证据来源` at 10224 shows left-column body alternating with
   right-column body). Every S129 quote I anchor is a single printed line that survives the interleave; a reader
   re-opening the PDF should expect the form's line order, not the page's.
5. **S130's silence is a property of the form, and the form is complete.** 16 pages, 6930 characters, `灰色 0`,
   `检索 0`, `中国循证医学中心 0`, and an independent `pdftotext -layout` reproduces it exactly; the text ends
   coherently (`本指南自发布之日起，长期接受社会意见与建议，并定期修订完善。`). So the absence claim is scoped to
   this management text; it says nothing about the 2021 年版试行 the note names (4792).
6. **S127 prints the centre's name twice across a line break** (`采用中国循证\n医学中心中国循证医学中心的证据质量
   分级体系`), which makes `中国循证医学中心` count 1, not 2, in that form. The entry's reading ("printed twice in a
   row") rests on the wrap, not on a doubled count — a curator counting strings will see 1.

## Not run / limits

- `c2-count.py` was not run: it measures C2 (entry + spans + lesson + registry), which is the C2 seats' item; my checks
  above are the row-level subset of its legs, computed against the committed `spans.tsv`.
- No C1 artifact was touched; no gate, battery tool or probe was executed.
- No network, no fetch, no `git`/`jj` mutation anywhere, no writes outside my scratch; scratch removed.
- Independent of nothing in one sense: the landed rows were visible in the lane from my first command, so the numeric
  agreement is confirmation, not blind duplication — every number in my cells was re-derived from the `.qcache` form
  and the span files and can fail (a wrong offset, a quote occurring twice, a wrong digest all break the checks above).

VERDICT — I drafted and validated Registry rows S127-S130 (11 cells, first-URL binding, `mined` / 2026-10-27 / 180d /
the r42 entry, 23 once-only `char` offsets re-derived from the forms, census validate exit 0) plus S118's `used-by`
old→new; all four rows survived every check I could run, and the single open decision is S130's tier (my A against the
landed B, argued in Finding 1).
