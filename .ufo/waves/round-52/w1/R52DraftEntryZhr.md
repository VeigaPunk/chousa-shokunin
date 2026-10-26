# R52DraftEntryZhr — C2 entry draft and its two located documents

Seat: R52DraftEntryZhr, wave 1, round 52, lane `chousa-shokunin` at base `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`.
Assignment: draft `corpus/knowledge/chinese-prisma-s-reception-r52.md` from the staged entry
`merge/chousa/knowledge/corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md`, citing the two documents by
lane id S113 (梅斯医学 page, staged S111) and S114 (中国全科医学 报告清单 page, staged S112), holding the C2 NEW_GROUND
term 检索报告清单 inside a located quote, and stating how the 梅斯医学 page relates to the SinoMed record the lane holds.

Nothing was written outside this report; the scratch replica was removed. No tool was installed (none needed).

## Attempted and measured

All commands ran with `TMPDIR=/fast/scratch/hyaku/chousa-r52/R52DraftEntryZhr`; the captures are read-only under
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/` (key = sha256(url)[:24]).

1. Capture sizes and the sweep counts the entry's negative claims rest on (the entry's `recheck:` command, run here):

```
$ QCACHE=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache; python3 -c "import sys;Q=sys.argv[1];M=open(Q+'/453d492becd9a2f4632cb8dd.txt',encoding='utf-8').read();G=open(Q+'/cacddf3bbf780a4c7582bb17.txt',encoding='utf-8').read();N=open(Q+'/42bac8830527d6f1bb125c49.txt',encoding='utf-8').read();[print(l,len(t),[t.count(w) for w in ('检索者','卷','DOI','PRISMA-S','检索报告清单','检索策略')],t.find(q)) for l,t,q in (('S113',M,'2026-04-25 中国循证医学杂志'),('S114',G,'明确说明每一项来源 的 检索或查询日期'),('record',N,'来源出版物： 中国循证医学杂志 卷：26 期：4'))]" "$QCACHE"
S113 8804 [0, 0, 0, 15, 7, 0] 2034
S114 6179 [0, 0, 0, 0, 0, 2] 1707
record 1675 [0, 1, 0, 6, 2, 0] 695
```

2. The identity test behind the entry's central claim (portal 简要介绍 block at char 2282, 292 characters; record
摘要 from char 829, 200 characters): `raw common prefix 9 of 293 200` / folded common prefix `200` / folded equal? `False`
with tail M `研究的规范化与国际化。 ` and tail N `”的内在局限,并针对中文` — i.e. after mapping （），：； to ASCII the
record's whole abstract equals the portal block's first 200 characters and the portal continues 92 more. The mapping was
（），：； → ASCII; a byte comparison fails at char 9 (（SR） vs (SR)).

3. Span manifest built from my eight quotes with the lane's own builder, copied read-only into a scratch replica
(`lane/corpus/evidence/round52/build-spans.py --root <scratch>/lane`):

```
QUOTE S113 char 21 spans/S113-1.txt
QUOTE S113 char 2034 spans/S113-2.txt
QUOTE S113 char 2433 spans/S113-3.txt
QUOTE S113 char 4836 spans/S113-4.txt
QUOTE S114 char 1707 spans/S114-1.txt
QUOTE S114 char 1785 spans/S114-2.txt
QUOTE S114 char 5612 spans/S114-3.txt
QUOTE S114 char 5744 spans/S114-4.txt
SPANS_ROWS=8 WRITTEN=8
```
Re-derivation: `build-spans.py --root <scratch>/lane --check` → `SPANS_ROWS=8 STALE=0`.

4. Substance floor and grounding, on that manifest and the drafted entry:
`quote-substance-check.py <scratch>/lane/corpus/evidence/round52/spans.tsv` → `IDS=2 QUOTES=8 FAILURES=0` (rc 0);
`tools/inference-ground.py --entry …/chinese-prisma-s-reception-r52.md --spans …/spans.tsv --counts /dev/null
--registry …/SOURCES.md --root …/lane` → `GROUND entry=corpus/knowledge/chinese-prisma-s-reception-r52.md section=1
bullets=5 tokens=7 grounded=7` / `GROUND: PASS` (rc 0).

5. The two registry rows drafted below, parsed with the frozen counter's own functions (`registry()`, `url_of()`,
`CHAR_RE` from `corpus/evidence/round52/c2-count.py`): `rows parsed 2 [11, 11]`; S113 URL-match True, S114 URL-match
True; `status mined opened 2026-10-26`; `used corpus/knowledge/chinese-prisma-s-reception-r52.md`; anchor chars
`['21','2034','2433','4836']` and `['1707','1785','5612','5744']` — the eight offsets build-spans printed in step 3.

6. The NEW_GROUND premise: `git -C <lane> grep -l -e 检索报告清单 -e 文献検索期間 -e 完全な検索戦略
00f8c7f5272a1d98b6d34913985fa4537e00aaf9 -- corpus/knowledge` printed nothing (rc 1), so no `corpus/knowledge` file at
BASE_REV held the term this entry is to hold (its occurrence count in the draft is 7).

7. Per-quote facts on the manifest rows: each quote occurs in the entry (`in_entry True` ×8), ≤25 whitespace words
(`2,2,1,2,3,4,13,2`), ≤160 characters (`51,19,43,103,19,25,99,19`), and every span file is longer than its quote
(`152,179,203,263,179,185,259,179`).

## Located quotes (machine lines)

Staged id, document URL and the entry that will carry them; each quote's character offset in the capture's `.txt` form
read as UTF-8 is on the `char` field of the source lines below.

```
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读 -指南&解读指南-MedSci.cn	char 21
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	2026-04-25 中国循证医学杂志	char 2034
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	在逐条阐释其内涵与要求的基础上，进一步探讨其跨学科的普适性、作为“报告规范”的内在局限	char 2433
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	attachmentFileNameList=[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)])	char 4836
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	明确说明每一项来源 的 检索或查询日期	char 1707
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	呈现 所有数据库、注册平台和网站的 完整 检索策略	char 1785
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71.	char 5612
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	发布日期：2023-01-31 浏览：	char 5744
```

## `corpus/evidence/round52/quotes.tsv` rows to write (lane ids; the builder needs these ids, not the staged ones)

```
id	url	quote	entry
S113	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读 -指南&解读指南-MedSci.cn	corpus/knowledge/chinese-prisma-s-reception-r52.md
S113	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	2026-04-25 中国循证医学杂志	corpus/knowledge/chinese-prisma-s-reception-r52.md
S113	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	在逐条阐释其内涵与要求的基础上，进一步探讨其跨学科的普适性、作为“报告规范”的内在局限	corpus/knowledge/chinese-prisma-s-reception-r52.md
S113	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	attachmentFileNameList=[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)])	corpus/knowledge/chinese-prisma-s-reception-r52.md
S114	https://www.chinagp.net/CN/column/item185.shtml	明确说明每一项来源 的 检索或查询日期	corpus/knowledge/chinese-prisma-s-reception-r52.md
S114	https://www.chinagp.net/CN/column/item185.shtml	呈现 所有数据库、注册平台和网站的 完整 检索策略	corpus/knowledge/chinese-prisma-s-reception-r52.md
S114	https://www.chinagp.net/CN/column/item185.shtml	The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71.	corpus/knowledge/chinese-prisma-s-reception-r52.md
S114	https://www.chinagp.net/CN/column/item185.shtml	发布日期：2023-01-31 浏览：	corpus/knowledge/chinese-prisma-s-reception-r52.md
```

## `corpus/SOURCES.md` rows to append (drafted, not written)

```
| S113 | https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3 — 梅斯医学 (MedSci) 指南&解读 页「系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读」 | page | B | what this portal re-host states about the reading's method and the article it carries, and how it relates to the lane's SinoMed record; not the 16 items' text, not the PDF attachment, not the publisher's version | the rendered title line (char 21), the free-text date-and-journal line (char 2034), the 简要介绍 method clause (char 2433) and the payload's attachmentFileNameList (char 4836); capture `.txt` read as UTF-8, 8,804 characters | a portal re-host carries the journal in a free-text line while its 发布机构 field renders empty, and its 简要介绍 completes an abstract an index record truncates | mined | 2026-10-26 | 180d | corpus/knowledge/chinese-prisma-s-reception-r52.md |
| S114 | https://www.chinagp.net/CN/column/item185.shtml — 《中国全科医学》报告清单页 (PRISMA 2020 条目清单, 中文) | page | A | what this journal's Chinese rendering of the PRISMA 2020 checklist states at items 6 and 7, as this copy states it; not a national standard, not PRISMA-S and not the checklist's English original | item 6's 明确说明每一项来源 的 检索或查询日期 (char 1707), item 7's 呈现 所有数据库、注册平台和网站的 完整 检索策略 (char 1785), the From citation line (char 5612) and 发布日期：2023-01-31 (char 5744); capture `.txt` read as UTF-8, 6,179 characters | the per-source search date is required by PRISMA 2020 item 6 as this journal renders it, and the page names PRISMA-S zero times | mined | 2026-10-26 | 180d | corpus/knowledge/chinese-prisma-s-reception-r52.md |
```

## Entry text — intended lane path `corpus/knowledge/chinese-prisma-s-reception-r52.md`

```markdown
# A 梅斯医学 copy of the PRISMA-S reading completes the abstract the lane's SinoMed record truncates, and a 中国全科医学 checklist page carries the per-source search date without naming PRISMA-S

source: S113 — https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3 — the rendered title line, the free-text date-and-journal line, the 简要介绍 block's method clause and the payload's attachmentFileNameList — char 21, char 2034, char 2433, char 4836
source: S114 — https://www.chinagp.net/CN/column/item185.shtml — item 6 (信息来源), item 7 (检索策略), the From citation line and the page's own date line — char 1707, char 1785, char 5612, char 5744
verified-at: 2026-10-26 — both captures opened from the read-only qcache; every offset below re-located in the `.txt` form read as UTF-8 (8,804 and 6,179 characters), and the record-side offsets re-located the same way in the lane's held SinoMed capture (1,675 characters)
recheck: 180d — from any cwd: `QCACHE=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache; python3 -c "import sys;Q=sys.argv[1];M=open(Q+'/453d492becd9a2f4632cb8dd.txt',encoding='utf-8').read();G=open(Q+'/cacddf3bbf780a4c7582bb17.txt',encoding='utf-8').read();N=open(Q+'/42bac8830527d6f1bb125c49.txt',encoding='utf-8').read();[print(l,len(t),[t.count(w) for w in ('检索者','卷','DOI','PRISMA-S','检索报告清单','检索策略')],t.find(q)) for l,t,q in (('S113',M,'2026-04-25 中国循证医学杂志'),('S114',G,'明确说明每一项来源 的 检索或查询日期'),('record',N,'来源出版物： 中国循证医学杂志 卷：26 期：4'))]" "$QCACHE"` — then re-open both pages and re-confirm the item-6 wording, the journal line and the record's volume
ground: PROVINCE.md claim-vs-source verification — what a Chinese portal page re-hosting the PRISMA-S reading states about its own method, whether that page is the article an index record holds in truncated form, and what one Chinese journal's PRISMA 2020 checklist page asks a search record to carry; not a national standard, not the 16 items' text and not the PDF attachment
adopted: round 52 from the campaign package `merge/chousa/` (staged `chinese-search-log-r37-amendment-2026-10-23.md`), re-bound by document to S113 and S114; the staged entry's pointer to a base file the lane refused in round 51 (`corpus/lessons/round-51.md` `## Gate`) and every staged body id are dropped, so this entry names no id but its own two documents

#### Observation

- **The 梅斯医学 page is a 指南&解读 record of one article, and its rendered title is the string a reader would search on.** `.txt` char 21: `系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读 -指南&解读指南-MedSci.cn` (51 characters, the page's `<title>`); the same title re-appears in the body header (char 1998) and in the 中文标题 field (char 2179), and a one-sentence 摘要 blurb sits at char 2084.
- **Its journal attribution sits in a free-text line, not in its publisher field.** `.txt` char 2034: `2026-04-25 中国循证医学杂志`; the structured field 发布机构： (char 2222) has nothing between it and 发布日期： (char 2238), which carries the same date on its next line. The embedded payload names the same journal (`guiderFrom=中国循证医学杂志`, char 2863, unique) and its author slot is empty (`author=,`, char 2897, unique).
- **The page names the attachment and its author, and serves neither.** 相关资料下载： (char 2654) lists `系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf` (char 2707; the same file name occurs three times in the form), and the payload carries `attachmentFileNameList=[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)])` (char 4836, unique). No item text is served: 条目 occurs twice (chars 2392 and 3499), both inside a copy of the abstract's 16-item sentence, and 检索策略 occurs 0 times; the form's only 全文 token sits inside the app banner `前往APP阅读全文，体验更佳` (banner char 7057, token char 7064).
- **The 简要介绍 block states the method and the critique.** The block runs char 2282 to char 2573 (292 characters) and contains, at char 2433, `在逐条阐释其内涵与要求的基础上，进一步探讨其跨学科的普适性、作为“报告规范”的内在局限`.
- **The lane's held record and this page are the same article, and the page continues where the record stops.** The SinoMed record the lane holds (`corpus/knowledge/chinese-search-record-r39.md`, capture read as UTF-8, 1,675 characters) gives `来源出版物： 中国循证医学杂志 卷：26 期：4` (char 695, unique), an author list under 作者： (char 503) beginning `郑卿勇;` (char 511, unique), and an abstract from char 829 that breaks off at `并针对中文` (char 1024, unique) after 200 characters. Titles agree modulo parenthesis width (the portal writes （PRISMA-S）, the record (PRISMA-S)). A byte comparison of the two abstracts diverges at char 9, because the portal keeps （SR） and ， where the record carries (SR) and ,; after mapping （），：； to their ASCII forms on both sides, the record's 200 characters equal the portal block's first 200 exactly, and the portal continues for 92 more characters. That is the relation: one article, two surfaces, the record truncated and the portal complete.
- **The two surfaces split the bibliographic fields.** The record gives 卷：26 期：4 and a twelve-name author list; the portal form gives the date 2026-04-25 and carries 卷 0 times with no 作者 field (作者： 0), naming 郑卿勇 only in the attachment file name. Neither form carries a DOI (0 in both).
- **The 中国全科医学 page is that journal's own table of the PRISMA 2020 items.** Rendered title `中国全科医学 报告清单` (char 16); heading 报告清单 (char 904) over `P RISMA2020 条目清单` (char 920); the table's header row reads 章节主题 / 条目 / 条目清单 / 所在 页码 (章节主题 at char 951, 所在 页码 at char 997), and the rows run item 1 through item 27 with sub-items (24a at char 5000, 注册信息 at char 5017). The citation line (char 5612) reads `The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71.`; the page's own date line is `发布日期：2023-01-31 浏览：` (char 5744) followed by 3452 (char 5768) views.
- **The search items are translated, and one of them is the date field.** Item 6 (信息来源, char 1650) asks for every source — databases, registries, websites, organisations, reference lists and any other route of search or enquiry — and then `明确说明每一项来源 的 检索或查询日期` (char 1707); item 7 (检索策略, char 1756) asks for `呈现 所有数据库、注册平台和网站的 完整 检索策略` (char 1785).
- **Negative sweeps, same command as `recheck:`.** Over the portal form, the checklist form and the record form: 检索者 0 / 0 / 0; 卷 0 / 0 / 1; DOI 0 / 0 / 0; PRISMA-S 15 / 0 / 6; 检索报告清单 7 / 0 / 2; 检索策略 0 / 2 / 0. So the checklist page names neither PRISMA-S nor a 检索报告清单, the portal page carries no volume, and none of the three names the person who ran a search.
- **The checklist's text form inserts spaces inside Chinese phrases** (`每一项来源 的 检索或查询日期`, and the source list renders `网站 、 机构`), so a byte-exact quote of it must keep those spaces; a reader who normalises whitespace will not match this form.

#### Inference

- **The portal page resolves the lane's truncated record to one article, and the resolution is checkable rather than nominal.** The two forms share the title and the journal, and the portal's 简要介绍 continues past `并针对中文`, the point where the record's abstract stops (S113). Folding （），：； to ASCII makes the record's whole abstract equal the portal block's opening stretch, so a reader can decide identity by computation, not by matching titles; what the record truncates is recoverable in the portal block a few characters later.
- **The portal states the reading's method and its critique, and still serves no item text.** The block says `在逐条阐释其内涵与要求的基础上，进一步探讨其跨学科的普适性、作为“报告规范”的内在局限`, and the page renders no item (条目 twice, both in that sentence; 检索策略 0 times) (S113). So the Chinese wording of the sixteen items is not in this copy, and the page's attachment is a name, not text: the item-level question stays with the unserved PDF.
- **The Chinese per-source search date arrived on a journal page through PRISMA 2020 itself.** The 中国全科医学 checklist's item 6 requires every source and `明确说明每一项来源 的 检索或查询日期`, and the page cites only `The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71.`; it names PRISMA-S zero times and a 检索报告清单 zero times (S114). The date field is therefore evidence for the checklist's own item, and it cannot carry the reception of PRISMA-S: the two documents in this entry rest on different instruments.
- **The two surfaces are complementary, and neither is one journal's house standard.** The portal gives a date and an attachment name but no volume (卷 0), while the record gives the volume, the issue and the author list but no date (S113); and the page that carries the search-date item is another journal's translation, dated `发布日期：2023-01-31 浏览：` (S114). A Chinese search-record claim can rest on a field two journals agree on — the per-source date — and cannot treat either journal's page as the national requirement.
- **The checklist floor is higher than the lane's worked Chinese record meets.** Item 7 asks for `呈现 所有数据库、注册平台和网站的 完整 检索策略` (S114), while the record the lane holds for the animal-experiment journal carries no boolean string in its form: 检索式 0, 布尔 0, and `\bAND\b` and `\bOR\b` 0 each (`corpus/knowledge/chinese-search-record-r39.md`, its `recheck:` command). As this copy states, the requirement is a complete strategy for every database, registry and website; the one published Chinese record the lane holds states sources and a date bound and stops short of it.

#### Unknown

- Whether the portal's 2026-04-25 is the article's publication date or the portal's posting date: 发布日期 is a portal field, the record gives 卷：26 期：4 with no issue date, and neither form states the other's date.
- Whether 中国循证医学杂志's volume 26 is the year 2026: neither copy states a volume-to-year rule, and the arithmetic from a founding year is in neither form.
- Whether the attachment's item text departs from PRISMA-S's original items: the page carries the file name and a download link, not the text.
- Whether other Chinese journals' checklist translations carry the same item-6 wording: one journal's page was read, at one address.
- Whether the 中国全科医学 page's 所在 页码 column ever carries a page figure: this text form renders the header and the item rows only, and no page figure appears between them.
- Who ran the searches behind either document: 检索者 is 0 in both forms and in the record, so the identity is unrecorded here rather than refused.
- Whether the portal is authorised to re-host the journal's article: the page states no licence or permission.
```

## Findings

- **The staged entry's leading claim is not supported by its own two documents, and the draft narrows it.** The staged
  text presented the Chinese checklist's per-source date as a PRISMA-S field that "travelled"; the 中国全科医学 page names
  PRISMA-S 0 times and a 检索报告清单 0 times, cites only the PRISMA 2020 statement, and is dated 2023-01-31 — three years
  before the 梅斯医学 item. The date requirement therefore evidences PRISMA 2020 item 6 as that journal renders it, not the
  reception of PRISMA-S.
- **New material the staged entry did not have (C2 depth):** the identity of the portal page with the lane's held SinoMed
  record, established by a checkable fold test rather than by title matching, plus the fact that the portal supplies the 92
  characters the record truncates; the portal's own publisher field rendering empty while the payload carries
  `guiderFrom=中国循证医学杂志`; the item-6 and item-7 wordings with their extraction spaces; the page-number column that
  carries no figure in this form.
- **The C2 NEW_GROUND term 检索报告清单 is held inside a located quote** (the portal's rendered title, char 21, also the
  first machine line), and the term is absent from `corpus/knowledge` at BASE_REV (step 6).
- **No staged id survives in the entry:** the only `S###` tokens are S113 and S114, this entry's own two `source:` ids; the
  staged entry's amendment pointer and body ids are dropped, and the record is named by path
  (`corpus/knowledge/chinese-search-record-r39.md`).
- **No "amends wave 2" sentence remains** and the entry never generalises either journal's page to a national standard; the
  Unknown list keeps the national-standard question open without claiming it.

## Limits and handoff

- I did not write any lane file: the entry, the two registry rows and the `quotes.tsv` rows above are drafts for L1. The
  scratch replica is gone, so the receipts above are the only record.
- The L1 must, in this order: append the two rows to `corpus/SOURCES.md`, write the entry, write `quotes.tsv`, run
  `python3 corpus/evidence/round52/build-spans.py` (it must print the eight `QUOTE … char …` offsets shown here — if any
  differs, the row's `anchor` cell must be corrected, not the quote), then place all eight quotes in
  `corpus/lessons/round-52.md` (the C2 leg `QUOTES_IN_LESSON` reads them from the lesson, and only the lesson's bytes are
  outside my control), then `python3 corpus/evidence/round52/c2-count.py`.
- C2 legs I could not run here: `CAPTURE_BOUND` and `SUBSTANCE` need the real `corpus/evidence/round52/spans.tsv`, and the
  counter reads `git show BASE_REV:corpus/SOURCES.md`, so it needs the real lane repo. I reproduced the two legs that do
  not need a commit (`build-spans --check`, `inference-ground`) and the registry parse with the counter's own functions.
- Named limit of the entry: the offset pairs are `.txt`-form offsets; the `.raw` HTML of both pages was not decoded, so a
  reader who uses the raw form will not find these numbers there.
- The 中国全科医学 page is one journal's page at one address; the entry says so and does not extend it.

VERDICT: built and first-checked the C2 entry draft `corpus/knowledge/chinese-prisma-s-reception-r52.md` — its eight
quotes locate uniquely in the two captures, hold 检索报告清单, build a STALE=0 span manifest, pass the substance floor
(`FAILURES=0`) and ground all 5 inference bullets (`tokens=7 grounded=7`), while the staged entry's PRISMA-S-reception
framing for the checklist page is falsified by that page's own 0 mentions of PRISMA-S.
