# R52GroundChinagpB — second independent pass on staged S112 (中国全科医学 PRISMA 2020 checklist)

seat R52GroundChinagpB · round 52 · wave 1 · 2026-10-26 · leaf member, no dispatch
capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/cacddf3bbf780a4c7582bb17.{txt,raw}`, URL `https://www.chinagp.net/CN/column/item185.shtml`
cache key checked: `sha256(url)[:24]` = `cacddf3bbf780a4c7582bb17` (computed, matches the file stem)
No network. No other seat's report read. Scratch `/fast/scratch/hyaku/chousa-r52/R52GroundChinagpB/` (removed; every receipt below copied first).

## 1. The text form, pinned

```
$ file cacddf3bbf780a4c7582bb17.*        # .raw = HTML document, UTF-8, 88313 bytes; .txt = UTF-8, 11676 bytes
$ python3 -c "..."                        # Path('.txt').read_text(encoding='utf-8')
chars 6179 bytes 11676
sha256 b1c3cd6a5c22b97fd44c6c35367292a57c299fe19b5eb6c0b9c156bb3abe24f0
strict utf-8 ok, chars 7585 U+FFFD 0       # decode of the BYTES (CRs kept): 7,585 chars, 1,406 CRLF, 0 replacement chars
```

Form used for every offset and every count below: `pathlib.Path(...).read_text(encoding='utf-8')` — universal newlines, **6,179 characters**, file bytes 11,676, digest `b1c3cd6a…`. This is the same string `corpus/evidence/round52/build-spans.py` `form_texts` builds (`read_text(encoding="utf-8", errors="replace")`; strict decode succeeds, so `errors="replace"` changes nothing). The `.raw` is HTML; the builder's *raw* form for a non-zip raw is the UTF-16LE decoding (44,157 chars), in which the four quotes I tested occur **0** times — so the `.txt` is this capture's only quotable form.

## 2. The document's own identity stamp

| Item | Value in the text form | Location |
|---|---|---|
| Title (`<TITLE>`) | `中国全科医学 报告清单` | char 16 (count 1); `<h4 class="item_title"> 报告清单 </h4>` at char 904 |
| Checklist heading | `P RISMA2020 条目清单` | char 920 (count 1) |
| Date | `发布日期：2023-01-31` | char 5744 (count 1), followed by `浏览：` + `3452` (char 5760) |
| Attribution / edition | `From: Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. doi: 10.1136/bmj.n71` | `From:` char 5530, the citation char 5612 |
| Host / column | `www.chinagp.net`, filed under the navigation entry `国际报告规范` | nav label char 330 (count 1) |
| Publisher block | `网站版权 © 《中国全科医学》编辑部` + `冀ICP备12018774号-6` + `冀公网安备 13040302001295号` + `北京市海淀区中关村大街11号中关村E世界大厦C座` + `zgqkyx@chinagp.net.cn` + `北京玛格泰克科技发展有限公司` | chars 6121 / 6079 / 6098 / 5869 / 5971 / 6146 |
| Author | **none on the page** | see below |

- The page carries **no byline**: `责任编辑` 0, `编译` 0, `翻译` 0, `译` 0, `版本` 0, `修订` 0, `更新` 0; `作者` occurs 4 times (chars 303, 691, 696, 5350) — a nav label `作者中心`, the template link `第一作者和通信作者信息表模板` twice, and item 26's own text `声明作者的任何利益冲突`. The only authorship statement is the `From:` citation of the English original.
- **The page never calls itself a translation.** The staged row's phrase "Chinese translation of the PRISMA 2020 checklist" is an inference from the `From:` line, not a statement the page makes (`译` 0, `翻译` 0, `版本` 0).
- **Operational note:** the checklist heading is two bold runs (`<b>P</b><b>RISMA2020</b><b>条目清单</b>`, `.raw` line 223), so `PRISMA2020 条目清单` occurs **0** times and only `P RISMA2020 条目清单` (char 920) is findable; `条目清单` occurs 2 (heading + its column header at char 981).

## 3. What the document is

A blank, full PRISMA 2020 checklist table, pasted from Word (`class="MsoNormal"` on every cell), four columns `章节主题 | 条目 | 条目清单 | 所在 页码`, 50 `<tr>`, **42 numbered rows** covering top-level items 1-27 plus sub-items 10a/10b, 13a-13f, 16a/16b, 20a-20d, 23a-23d, 24a-24c. In **49 of the 50 rows the last (page-number) cell is empty**; only the header row carries the label `所在 页码` — the journal publishes it as a form for the author to fill, not a worked record. Items 5-9 are the 方法 block's first five rows: label order `方法, 纳排标准(5), 信息来源(6), 检索策略(7), 研究选择(8), 资料提取(9), 资料条目(10a)`. The item-5 label is split across spans and only findable as `纳 排 标准` (char 1527); the contiguous `纳排标准` occurs 0 times.

## 4. Seven located quotes (all in the `.txt` form, each occurring exactly once)

| # | quote | chars / ws-words | quote offset | span offset / len | char N |
|---|---|---|---|---|---|
| n1 | `详细说明纳入和排除标准，以及 在结果综合时 纳入研究 的 分组 情况。` | 35 / 6 | 1558 | 1478 / 195 | 1558 |
| n2 | `详细说明获取文献的所有来源，包括 所有数据库、注册平台、网站 、 机构 、参考列表以及 其他 检索或咨询 途径 。明确说明每一项来源 的 检索或查询日期 。` | 78 / 12 | 1650 | 1570 / 238 | 1650 |
| n3 | `呈现 所有数据库、注册平台和网站的 完整 检索策略，包括 用到的 过滤器和限制条件。` | 42 / 6 | 1785 | 1705 / 202 | 1785 |
| n4 | `详细说明 确定 一项研究是否符合纳入标准的方法，包括每项检索记录由几人进行筛选，是否独立筛选。` | 47 / 3 | 1884 | 1804 / 207 | 1884 |
| n5 | `详细说明数据提取的方法，包括几人提取数据，是否独立提取，以及从纳入研究的 作 者获取或确认数据的过程。` | 51 / 3 | 2005 | 1925 / 211 | 2005 |
| n6 | `网站版权 © 《中国全科医学》编辑部` | 18 / 3 | 6121 | 6041 / 138 | 6121 |
| n7 | `国际报告规范` | 6 / 1 | 330 | 250 / 166 | 330 |

n1, n4 and n5 are content quotes that are **not** in the staged row's claim; n2 and n3 are the row's own theme sentences, re-grounded byte-exactly here; n6/n7 are identity/site chrome and are recorded for the identity stamp rather than recommended as entry quotes. All seven pass the round-51 substance floor (span ≤ quote + 162; every quote ≥ 3 non-space chars, n2 ≥ 12).

## 5. Negative sweeps, exact counts in the text form

Command shape: `python3 -c "...t=read_text(encoding='utf-8'); t.count(w)..."` over `cacddf3bbf780a4c7582bb17.txt`.

```
searcher     : 検索者 0   検索担当 0   检索者 0   检索人员 0
search date  : 検索日 0   検索期間 0   文献検索期間 0   检索日期 0   检索时间 0
               检索期间 0  时间范围 0  起止 0  截至 0  最后检索 0
strategy     : 検索式 0   検索戦略 0   検索式 0   检索式 0   检索词 0   主题词 0   布尔 0
               检索策略 2  (item-7 label char 1756, item-7 text char 1785)
grey lit     : 灰色文献 0   グレーリテラチャー 0   灰色 0
PRISMA-S     : PRISMA-S 0   PRISMA‐S 0 (U+2010)   PRISMA S 0   PRISMA-S 2020 0   PRISMA Search 0
present      : 检索或查询日期 1 (char 1719)   日期 2   查询 2   检索 7   筛选 3   提取 7   几人 2
               PRISMA 2   PRISMA2020 1 (char 1219, item 2's 摘要清单 reference)   扩展 0
```

**Absent, so any negative claim in the entry must carry this list:** every Japanese form (`検索者`, `検索担当`, `検索日`, `検索期間`, `文献検索期間`, `検索式`, `検索戦略`, `グレーリテラチャー`); the searcher nouns `检索者`, `检索人员`; the date literals `检索日期`, `检索时间`, `检索期间`, `时间范围`, `起止`, `截至`, `最后检索`; the strategy nouns `检索式`, `检索词`, `主题词`, `布尔`; `灰色文献`/`灰色`; and `PRISMA-S` in all three spellings plus `扩展`. **Present:** `检索策略` (2), `检索或查询日期` (1), and the person counts `几人` (2, items 8 and 9 only).

## 6. What this document can and cannot carry

- **Can:** item 6 requires every route — databases, registries, websites, organisations, reference lists, any other search-or-consultation route — **and the search-or-query date of each source** (n2, char 1650); item 7 requires the complete strategy for every database, registry and website **including filters and limits** (n3, char 1785); items 8/9 count people for screening and extraction and ask for automated tools to be described (n4, n5); the checklist is the journal's full 27-item PRISMA 2020 form, published as a blank template (Section 3); the page's date is `2023-01-31` and its provenance is the BMJ 2021 PRISMA 2020 statement (Section 2).
- **Cannot, on this capture:** no searcher field (`检索者`/`检索人员` 0, and the only person counts are screening and extraction); no PRISMA-S of any kind (0 in all spellings; `扩展` 0); no grey-literature term (`灰色文献` 0); no `检索式`/`检索词`/`布尔` wording, so the page asks for `完整 检索策略` and never separately names the search string; no period requirement for the search (`检索期間`-family, `时间范围`, `起止`, `截至` all 0) — the date requirement is per source and singular; no translation or edition statement, no byline, no enforcement statement.
- **[INFERENCE]** Whether `完整 检索策略` entails printing the string itself is a reading question this page does not settle; the three inference bullets of the draft below were checked with `tools/inference-ground.py` (Section 7 receipt) and stay inside that limit.

## 7. Draft entry (the S114 half) — verified in scratch, for L1 to integrate

Labelled with intended lane path `corpus/knowledge/chinese-prisma-s-reception-r52.md`. Lane id **S114** (never S112). Checked with a scratch `spans.tsv` of the seven rows above plus this draft:

```
$ python3 corpus/evidence/round51/quote-substance-check.py $S/spans.tsv   # $S = scratch dir
IDS=1 QUOTES=7 FAILURES=0          # exit 0
$ python3 -c "<cap_bound leg: t[offset:offset+len(span)] == span>"       # 7 rows
CAP_BOUND 7 / 7                    # quote offsets 1558 1650 1785 1884 2005 6121 330
$ python3 tools/inference-ground.py --entry $S/entry-draft.md --spans $S/spans.tsv \
      --counts $S/counts.json --root /
GROUND entry=…/entry-draft.md section=1 bullets=3 tokens=5 grounded=5
GROUND: PASS                       # exit 0
```

```markdown
# A Chinese journal ships the full PRISMA 2020 checklist as a blank form, asks each source to carry a search-or-query date, and names no searcher, no PRISMA-S and no grey literature

source: S114 — https://www.chinagp.net/CN/column/item185.shtml — 报告清单 table (P RISMA2020 条目清单), items 5-9, the From: line and 发布日期：2023-01-31 — char 1558, char 1650, char 1785, char 1884, char 2005
verified-at: 2026-10-26 — the capture `cacddf3bbf780a4c7582bb17.txt` opened from the read-only qcache; every offset re-located in the `.txt` form read as UTF-8 (6,179 characters)
recheck: 180d — from any cwd: `Q=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache; python3 -c "import sys;t=open(sys.argv[1],encoding='utf-8').read();print(len(t),[t.count(w) for w in ('检索者','检索人员','检索日期','检索时间','检索式','灰色文献','PRISMA-S','检索策略')],[t.find(q) for q in ('详细说明纳入和排除标准','详细说明获取文献的所有来源','呈现 所有数据库、注册平台和网站的 完整 检索策略','详细说明 确定 一项研究是否符合纳入标准的方法','详细说明数据提取的方法','发布日期：2023-01-31')])" $Q/cacddf3bbf780a4c7582bb17.txt` — expect `6179 [0, 0, 0, 0, 0, 0, 0, 2] [1558, 1650, 1785, 1884, 2005, 5744]`
ground: PROVINCE.md claim-vs-source verification — what one Chinese journal's own PRISMA 2020 checklist page asks of a search record; not a national standard, not a search string, not a worked record
adopted: round 52 from the campaign package `merge/chousa/`, re-bound by document to lane S114 (the staged id is not carried over: it names another lane row)

#### Observation

- **The document is the journal's own full checklist, published as a blank form.** The page's heading is 报告清单 and the table heading is `P RISMA2020 条目清单`; the table runs items 1 through 27 with the sub-items 10a, 10b, 13a-13f, 16a, 16b, 20a-20d, 23a-23d and 24a-24c, and in 49 of the table's 50 `<tr>` the last (page-number) cell is empty, only the header row carrying the label `所在 页码`, so the published checklist leaves that column for the author to fill (S114).
- **Items 5-9 are the 方法 block's first five rows.** In the label column the order is 方法, 纳排标准 (5), 信息来源 (6), 检索策略 (7), 研究选择 (8), 资料提取 (9), 资料条目 (10a); the item-5 label carries inter-character spaces in this text form (`纳 排 标准`), so the contiguous string 纳排标准 occurs 0 times here (S114).
- **Item 5 asks for the criteria and the grouping.** It reads `详细说明纳入和排除标准，以及 在结果综合时 纳入研究 的 分组 情况。` (S114).
- **Item 6 asks for every route and a date for each one.** It reads `详细说明获取文献的所有来源，包括 所有数据库、注册平台、网站 、 机构 、参考列表以及 其他 检索或咨询 途径 。明确说明每一项来源 的 检索或查询日期 。` (S114).
- **Item 7 asks for the complete strategy with its filters and limits.** It reads `呈现 所有数据库、注册平台和网站的 完整 检索策略，包括 用到的 过滤器和限制条件。` (S114).
- **Items 8 and 9 are where the checklist counts people.** Item 8 asks `详细说明 确定 一项研究是否符合纳入标准的方法，包括每项检索记录由几人进行筛选，是否独立筛选。`; item 9 asks `详细说明数据提取的方法，包括几人提取数据，是否独立提取，以及从纳入研究的 作 者获取或确认数据的过程。` Both also ask that automated tools be described (S114).
- **The identity stamp is the journal's, plus an attribution to the English original.** The `<TITLE>` is `中国全科医学 报告清单` (char 16), the page is filed under the navigation entry `国际报告规范` (char 330), the page date is `发布日期：2023-01-31` (char 5744) with a view counter, and the only authorship statement is `From: Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71. doi: 10.1136/bmj.n71` (char 5612). The footer carries `网站版权 © 《中国全科医学》编辑部`, `冀ICP备12018774号-6`, a Beijing address, the address `zgqkyx@chinagp.net.cn` and technical support by 北京玛格泰克科技发展有限公司 (S114).
- **No byline, no translator, no edition label.** 责任编辑, 编译, 翻译, 译, 版本, 修订 and 更新 each occur 0 times in this text form; 作者 occurs 4 times, all in navigation or in the journal's other download links and in item 26's own text, never as a page author. The page never calls itself a translation of PRISMA 2020 (S114).
- **Negative sweeps over the text form.** Read as UTF-8: 検索者 0, 検索担当 0, 检索者 0, 检索人员 0; 検索日 0, 検索期間 0, 文献検索期間 0, 检索日期 0, 检索时间 0, 检索期间 0, 时间范围 0, 起止 0, 截至 0; 検索式 0, 検索戦略 0, 检索式 0, 检索词 0, 主题词 0, 布尔 0; 检索策略 2; 灰色文献 0, グレーリテラチャー 0, 灰色 0; `PRISMA-S` 0, `PRISMA‐S` 0 with U+2010, `PRISMA S` 0; PRISMA 2, PRISMA2020 1, 扩展 0 (S114).

#### Inference

- **The date requirement is per source, and the person the checklist counts is not the searcher.** Item 6 asks `明确说明每一项来源 的 检索或查询日期`, while the person counts the checklist does ask for belong to screening (`每项检索记录由几人进行筛选`) and extraction (`几人提取数据`), and 检索者 and 检索人员 occur 0 times in this text form (S114).
- **The strategy item's own wording asks for a strategy plus filters and limits.** Item 7 reads `呈现 所有数据库、注册平台和网站的 完整 检索策略，包括 用到的 过滤器和限制条件`, the page never uses the words 检索式 or 检索词, so the term an author is asked to satisfy is 完整 检索策略 and the string itself is not separately named here (S114).
- **The route list is a source list, not a people list.** Item 6's enumeration runs `网站 、 机构 、参考列表以及 其他 检索或咨询 途径` beside the databases and registries, and the searcher is absent from the page rather than refused on it (S114).

#### Unknown

- Whether the journal requires this checklist at submission or only publishes it as guidance: the page is filed under 国际报告规范 and carries no enforcement statement.
- Whether the Chinese wording departs from the PRISMA 2020 English items in meaning: the page carries no translator, no edition and no item-level revision note.
- Whether a PRISMA-S style searcher field exists anywhere in this journal's forms: the page does not carry it, and no other page was opened.
```

## 8. QUOTE machine lines

`staged-id` = the package id S112 (field as prescribed). **When pasting into `corpus/evidence/round52/quotes.tsv` the id must become the lane id `S114`** — `c2-count.py` matches a manifest `sid` to the bound lane row (`on_bound += bound.get(sid) == url`), so a staged id there would fail the span leg.

```
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	详细说明纳入和排除标准，以及 在结果综合时 纳入研究 的 分组 情况。	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	详细说明获取文献的所有来源，包括 所有数据库、注册平台、网站 、 机构 、参考列表以及 其他 检索或咨询 途径 。明确说明每一项来源 的 检索或查询日期 。	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	呈现 所有数据库、注册平台和网站的 完整 检索策略，包括 用到的 过滤器和限制条件。	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	详细说明 确定 一项研究是否符合纳入标准的方法，包括每项检索记录由几人进行筛选，是否独立筛选。	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	详细说明数据提取的方法，包括几人提取数据，是否独立提取，以及从纳入研究的 作 者获取或确认数据的过程。	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	网站版权 © 《中国全科医学》编辑部	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	国际报告规范	corpus/knowledge/chinese-prisma-s-reception-r52.md
```

Recommended `quotes.tsv` set: n1-n5 (content). If n6/n7 are sent, they must also appear in the entry body and in `corpus/lessons/round-52.md` — both already appear in the draft's Observation, so that cost is only the lesson.

## 9. Integration constraints for L1 (all read off the frozen counter)

1. **Ids.** Lane max is `S112` (the JAHBS article, `corpus/SOURCES.md:122`); the plan S111→S113, S112→S114 holds. `c2-count.py` counts any `S\d{3,}` token in an entry that is not a bound lane id (`unb`), so the entry must never contain `S111` or `S112`; the capture itself holds neither token (0 / 0), so the quotes cannot leak them, and the draft's `adopted:` line was rewritten to name no staged id.
2. **Row.** One Registry row only, first source-cell URL exactly `https://www.chinagp.net/CN/column/item185.shtml`, new since `00f8c7f5…`, status `mined`, opened `2026-10-26`, `used-by` exactly `corpus/knowledge/chinese-prisma-s-reception-r52.md`, and the entry carrying `source: S114 — https://www.chinagp.net/CN/column/item185.shtml`.
3. **Anchor cell.** Every `char N` in that row's anchor cell must equal a quote offset of S114; with this set the only valid values are 1558, 1650, 1785, 1884, 2005 (adding 6121/330 only if n6/n7 go into `quotes.tsv`). The identity offsets (16, 330, 5612, 5744) must **not** be in the anchor cell unless they are also quote rows.
4. **Spans.** `build-spans.py` derives `spans/S114-<n>.txt` at `offset-80` with 80 chars of trailing context; for the seven rows those slices are verified byte-equal to the capture (CAP_BOUND 7/7 above). Quotes must be copied **with the text form's internal spaces** (`财务…` none here, but `纳 排 标准`, `网站 、 机构`, `作 者` all matter).
5. **Lesson.** Each quote row must also occur in `corpus/lessons/round-52.md`.
6. **Term.** `TERMS[E_ZHR] = 检索报告清单`, and it must be absent at `BASE_REV` and present in the entry. **This document does not contain it** (0 occurrences of `检索报告清单` in the capture) — that half comes from the S113 MedSci page and must not be sourced to chinagp.net.
7. **Round-51 routed defects touched here.** §6.2 twin-id/refusal ordering: staged S112 is already a lane row (JAHBS) — the new row is S114 and the staged id must not be carried over. §6.4 content anchor: the draft's anchors are quote offsets, not file existence.

## 10. Limits and out of scope

- I did **not** run `corpus/evidence/round52/c2-count.py` (it needs the lane entry, row and lesson, which are not mine to write) and did not fetch the live URL (L0 `8d77e6c1` open). The counter-shaped legs I could run against scratch were run and are receipted in §7.
- The `.raw` is only used for two structural facts (the two-run heading, the blank page-number cells); all offsets and counts are in the `.txt` form.
- No English PRISMA 2020 capture was opened, so no item-by-item comparison with the original wording is made; the parity of items 5-9 with the original is not claimed anywhere in the draft.
- `corpus/knowledge/japanese-prisma-item-wording-r40.md` and `…-niph-form-r52.md` do not exist yet at this seat's write time; this report does not depend on them.
- No tool installed or upgraded (nothing needed; pacman paused host-wide).

VERDICT: attacked the staged S112 document as an independent second pass — its identity stamp is the journal's own (title, `2023-01-31`, publisher footer, `From:` BMJ attribution) with no byline, translator or edition, and it is a blank 27-item form; seven byte-exact located quotes (five content, offsets 1558/1650/1785/1884/2005), the four-plus-non-headline set among them, all pass the substance floor, the capture-slice leg 7/7, and a drafted S114 entry whose Inference section passes `inference-ground` — while the negative sweep leaves `検索者/检索者/检索人员`, `検索日/検索期間/文献検索期間/检索日期/检索时间`, `検索式/检索戦略/检索式`, `灰色文献/グレーリテラチャー` and `PRISMA-S` at exact 0, so the entry's negatives must carry these counts.
