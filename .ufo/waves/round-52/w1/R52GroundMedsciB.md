# R52GroundMedsciB — second pass on staged S111 (梅斯医学 PRISMA-S record)

Seat: independent second pass (write scope: this report only). Lane commit read
`37468eadd8d098e80289b2f31a22de3872d4a1f6` (frozen claims); C1 candidate at `804a453`.
No network, no live fetch.

Document: 系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读 — the 简要介绍 block plus the record's
metadata block. Capture (read-only): `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/453d492becd9a2f4632cb8dd.{txt,raw}`,
URL `https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3`.
**Text form for every offset below**: the `.txt` read as UTF-8 — 8804 characters, sha256
`ad6b09f0599c5820a4d283c953d07f457f3f540edcb5ebc3406e50ae571cdc52`, mtime 2026-10-23 20:38:36.
Cross-check form: the `.raw` decoded UTF-8 — 265058 characters in 276803 bytes, sha256
`712cdef66a94b2dd69f38a43c47e5dc0932259ebb060cf50989ddf8d19b90e00`.
## 1. Provenance and one refusal

`sha256(url)[:24]` = `453d492becd9a2f4632cb8dd` = the cache key of both files (checked). The
`.txt` holds 0 U+FFFD, so the block text is intact. The `.raw` is plain HTML (`<!DOCTYPE HTML>`),
and the C1 tool refuses it rather than emitting text:

`$ python3 tools/capture-text.py <…>.raw >out 2>err; echo rc=$?` → `rc=2`, stdout 0 bytes, stderr
`REFUSED not a zip (an OOXML capture is a zip package)`.

A real non-zip capture refused with exit 2, empty stdout and a `REFUSED` stderr line — R52-C1's
REFUSE branch observed outside the counter's generated packages. Not a counter leg; not claimed as one.
## 2. Identity stamp

| element | what the record states | char |
|---|---|---|
| title | 系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读 | 2010, 2791 |
| host | MedSci.cn 梅斯医学, 指南&解读指南; record id `23e481c0052069d3` | 11, 2791 |
| journal | `guiderFrom=中国循证医学杂志` — a field, not a byline | 2863 |
| date printed | header `2026-04-25 中国循证医学杂志`; 发布日期 2026-04-25 | 2034 |
| date stamped | `guiderPublishedTime=Sat Apr 25 00:00:00 CST 2026` **and** `publishedTime=Tue May 05 13:50:00 CST 2026`: two dates ten days apart, both weekday words correct (2026-04-25 = Saturday, 2026-05-05 = Tuesday) | 3152, 4380 |
| author | `authorId=0, author=,` is **empty**; the only author evidence is the attachment name `…_郑卿勇.pdf` | 2885, 4836 |
| edition | none — no volume, issue, page range or DOI line; `originalUrl=, linkOutUrl=` empty, `journalId=0, articlesId=null` | 3202, 3055 |
| placement | `guiderLanguage=0, guiderRegion=3`; `ipAttribution=河南省`, header `发表于河南省`; 创建人：小M / `创建时间：2020-05-29` (dates the contributor account, six years before the item) | 4120, 4817, 6974 |
| access | `haveAttachments=1, attachmentList=null`, `paymentAmount=10`, page prints `下载请点击：` | 4051, 4178, 4996 |
## 3. Located quotes — 11, each exactly once in the `.txt` form

`text.count(quote) == 1` for each; the longest is 102 characters and 2 whitespace words. The char
values are the builder's own `char N` output (§3.1), not hand-copied.

| char | quote | chars |
|---|---|---|
| 2034 | `2026-04-25 中国循证医学杂志` | 19 |
| 2264 | `简要介绍：` | 5 |
| 2791 | `id=23e481c0052069d3, title=系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读` | 59 |
| 2863 | `guiderFrom=中国循证医学杂志` | 19 |
| 3152 | `guiderPublishedTime=Sat Apr 25 00:00:00 CST 2026` | 48 |
| 4051 | `haveAttachments=1, attachmentList=null` | 38 |
| 4178 | `paymentAmount=10` | 16 |
| 4380 | `publishedTime=Tue May 05 13:50:00 CST 2026` | 42 |
| 4817 | `ipAttribution=河南省` | 17 |
| 4836 | `attachmentFileNameList=[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)]` | 102 |
| 6974 | `创建时间：2020-05-29` | 15 |

The machine lines carry the package's staged id for this document (S111); the lane id is **S113**,
and `quotes.tsv` for `build-spans.py` must carry S113 (§6).

```
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	2026-04-25 中国循证医学杂志	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	简要介绍：	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	id=23e481c0052069d3, title=系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	guiderFrom=中国循证医学杂志	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	guiderPublishedTime=Sat Apr 25 00:00:00 CST 2026	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	haveAttachments=1, attachmentList=null	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	paymentAmount=10	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	publishedTime=Tue May 05 13:50:00 CST 2026	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	ipAttribution=河南省	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	attachmentFileNameList=[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)]	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S111	https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3	创建时间：2020-05-29	corpus/knowledge/chinese-prisma-s-reception-r52.md
```

**The 简要介绍 prose cannot be a located quote — measured, not assumed.** The `.txt` prints the full
abstract twice (char 2282 the display block, char 3389 the `ChDivSummary` span of the page's own JSON)
and a short blurb carrying its closing sentence four times (char 2143, 2559, 2973, 3678); the 16-item
clause prints twice (char 2387, char 3494). Only the block's last five characters are single-occurrence,
and only with the block's trailing space (`国际化。 ` at char 2570), which `build-spans.py` strips
(`cells = (c.strip() …)`) — so that candidate degrades to 4 occurrences and is refused. For the drafter:
carry the block's content in `#### Observation` with these counts; never as a Gate quote or a backticked
Inference token.
### 3.1 Builder and gate cross-check (scratch root only)

```
$ python3 corpus/evidence/round52/build-spans.py --root $S/probe
QUOTE S113 char 2034 spans/S113-1.txt    … QUOTE S113 char 2264 spans/S113-11.txt
SPANS_ROWS=11 WRITTEN=11
$ python3 corpus/evidence/round52/build-spans.py --root $S/probe --check
SPANS_ROWS=11 STALE=0
$ python3 corpus/evidence/round51/quote-substance-check.py $S/probe/corpus/evidence/round52/spans.tsv
IDS=1 QUOTES=11 FAILURES=0
```
## 4. Negative sweeps — exact counts, both forms, one URL key

A Python count over `453d492becd9a2f4632cb8dd.txt` (UTF-8) and over the `.raw` decoded UTF-8.

| group | terms | `.txt` | `.raw` |
|---|---|---|---|
| searcher identity | 検索者, 検索担当, 检索者, 检索人员 | 0,0,0,0 | 0,0,0,0 |
| search date | 検索日, 検索期間, 文献検索期間, 检索日期, 检索时间 | 0 ×5 | 0 ×5 |
| strategy | 検索式, 検索戦略, 检索策略, 检索式 | 0 ×4 | 0 ×4 |
| grey literature | 灰色文献, グレーリテラチャー | 0,0 | 0,0 |
| Chinese checklist date phrase | 检索或查询日期, 查询日期 | 0,0 | 0,0 |
| named databases | PubMed, CNKI, 万方, 维普, SinoMed, 中国生物医学文献, Web of Science, Embase, Cochrane Library | 0 ×9 | 0 ×9 |
| **positive controls** | PRISMA-S / 文献检索 / 16个条目 | **15 / 15 / 2** | **26 / 20 / 2** |

**Absent, therefore**: all 4 searcher-identity terms, all 5 search-date terms, all 4 strategy terms, both
grey-literature terms, the Chinese checklist's own date phrase, and every named database. `数据库` occurs
4 times — twice in site navigation (`期刊数据库查询`, `数据库建立与管理`) and twice in the abstract's class
phrase `中文数据库` — never as a named source. `DOI` and `doi` occur 0 times in both forms. So this record
states no searcher, no search date, no expression, no database and no DOI; a lane claim that it does
would be false.
## 5. Draft entry (S113 half; lane path `corpus/knowledge/chinese-prisma-s-reception-r52.md`)

The S112 half (中国全科医学) is another seat's. This S113 slice is complete and gated on its own; no
staged id appears in it.

```markdown
# The Chinese PRISMA-S reception is a portal record of a paid interpretation

source: S113 — https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3 — the record's display header and 简要介绍 block, its `GetToolGuiderByIdResponse` metadata block and the attachment name it lists — capture written 2026-10-23, read 2026-10-26
verified-at: 2026-10-26 — re-read the two capture files of the cache key for this URL (`.txt` 8804 characters, `.raw` 265058 characters decoded) and swept the fifteen searcher, date, strategy and grey-literature terms
recheck: 180d — re-open the capture key `453d492becd9a2f4632cb8dd` and confirm the 16-item sentence and the ten-point attachment are unchanged
ground: the lane held no opened Chinese document that states what PRISMA-S is and how a Chinese reading of it argues. Round 51 refused the item for capture form; round 52 reads the portal record itself and states only what the record states.

#### Observation

- The record is a MedSci.cn (梅斯医学) 指南&解读指南 item, id `23e481c0052069d3, title=系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读`, and its displayed date-and-source line is `2026-04-25 中国循证医学杂志` (S113).
- The metadata block carries two dates ten days apart: `guiderPublishedTime=Sat Apr 25 00:00:00 CST 2026` (the date the header prints) and `publishedTime=Tue May 05 13:50:00 CST 2026` (the record's own publish stamp); both weekday strings match their dates (S113).
- The journal is a field, not a byline: `guiderFrom=中国循证医学杂志`; the author field is empty (`authorId=0, author=,`) and the only author evidence is the attachment's file name, `attachmentFileNameList=[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)]` (S113).
- The attachment is announced but not served: `haveAttachments=1, attachmentList=null` and `paymentAmount=10`, and the page prints `下载请点击：` above the file name (S113).
- The record carries no route back to the article: `originalUrl=, linkOutUrl=` are both empty and `journalId=0, articlesId=null`; the text holds no `DOI` and no `doi` token (S113).
- The item's placement fields are `guiderLanguage=0, guiderRegion=3` (a Chinese-language, region-3 interpretation), and its location tag is `ipAttribution=河南省` under the header's `发表于河南省` (S113).
- The record's own creation fields read `创建时间：2020-05-29` under `创建人：小M` — six years before the item's date, so they date the contributor account, not the article (S113).
- **What the 简要介绍 block states.** PRISMA-S is presented as PRISMA for Searching, an extension of the 2020 statement, providing `包含16个条目的专项规范` for the search half of a review; the Chinese reading works through the items one by one from the original publication, then argues the standard's cross-disciplinary generality and `作为“报告规范”的内在局限，并针对中文数据库等本土化应用挑战提出实践建议` (S113).
- **The block occurs more than once in the text form.** The full abstract prints twice, at char 2282 (the 简要介绍 block) and char 3389 (the `ChDivSummary` span of the page's own JSON); its closing sentence prints four times (char 2143, 2559, 2973, 3678) because a short blurb repeats it; the 16-item clause prints twice (char 2387 and char 3494); and only the block's last five characters are single-occurrence, and only with the block's trailing space (char 2570), which the span builder trims — so no sentence of the block can be a located quote (S113).

#### Inference

- A Chinese reception of PRISMA-S exists as a `中国循证医学杂志` article, but the page is a reception *record*: it states the standard's shape and the reading's argument, and it does not carry the reading itself, which sits in a file the record prices at ten points (S113).
- The page is a portal summary, not the article's body: the label `简要介绍：` sits directly over the abstract that opens `文献检索是系统评价（SR）的基石`, and the same abstract prints again inside the page's `ChDivSummary` block, so the text form holds two copies of one abstract and no article text (S113).
- The sweeps are a null result, not a matcher failure: the same text that returns zero for all fifteen searcher, date, strategy and grey-literature terms returns the block's opening sentence `文献检索是系统评价（SR）的基石`, so the record answers none of the lane's field questions — no searcher, no search date, no expression, no database is named on it (S113).

#### Unknown

- Whether the ten-point PDF attachment reproduces the sixteen items item by item. The attachment was not opened; the record only names it.
- Whether the article's printed date is 2026-04-25 or 2026-05-05. The record holds both, and no issue or volume line is printed to settle it.

#### Gate

Located quotes (each unique in the `.txt` form read as UTF-8, capture key `453d492becd9a2f4632cb8dd`, file sha256 `ad6b09f0599c5820a4d283c953d07f457f3f540edcb5ebc3406e50ae571cdc52`, 8804 characters, written 2026-10-23, no fetch):

- char 2034 `2026-04-25 中国循证医学杂志`
- char 2264 `简要介绍：`
- char 2791 `id=23e481c0052069d3, title=系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读`
- char 2863 `guiderFrom=中国循证医学杂志`
- char 3152 `guiderPublishedTime=Sat Apr 25 00:00:00 CST 2026`
- char 4051 `haveAttachments=1, attachmentList=null`
- char 4178 `paymentAmount=10`
- char 4380 `publishedTime=Tue May 05 13:50:00 CST 2026`
- char 4817 `ipAttribution=河南省`
- char 4836 `attachmentFileNameList=[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)]`
- char 6974 `创建时间：2020-05-29`

The lane id is S113 because the URL is the evidence: the staged package's id for this URL names a different lane row, so it is not carried here, and S113 is the next free id above the registry maximum.
```

Gates on that draft, in a scratch root, with the lane's tools read-only:

```
$ python3 tools/inference-ground.py --entry $S/probe/corpus/knowledge/chinese-prisma-s-reception-r52.md \
    --spans $S/probe/corpus/evidence/round52/spans.tsv --counts /dev/null \
    --registry corpus/SOURCES.md --root $S/probe
GROUND entry=corpus/knowledge/chinese-prisma-s-reception-r52.md section=1 bullets=3 tokens=4 grounded=4
GROUND: PASS    rc=0
```

Three failures preceded that pass and are findings, not noise: a bullet quoting the block's
`作为“报告规范”的内在局限` fails `INF_TOKEN_NOT_IN_SPAN` (that phrase has no span, §3); a bullet with
no backticked phrase and no 3+ digit figure fails `INF_UNGROUNDED`; and offsets written as figures inside
a bullet (`2282`) become tokens no span grounds, so offsets belong in Observation and Gate only. Draft
hygiene measured: `\bS\d{3,}\b` finds `['S113']` only; 11/11 quotes present in the entry; `short 11/11`.
## 6. Row plan for S113 (for the row drafter; not written here)

First source cell = the URL; `kind` docs; `status` mined; `opened` 2026-10-26; `used-by` exactly
`corpus/knowledge/chinese-prisma-s-reception-r52.md`; `anchor` carries `char 2034` (or any of the 11).
`quotes.tsv` rows must use **S113**: `c2-count.py` keys `on_bound` / `SPAN_IDS` / `ANCHOR_BOUND` on the
bound lane id, so a staged id there leaves `ON_BOUND=0/11`.

**Tier conflict for the L1.** The same URL is tiered twice in the staged package: line 36 of
`SOURCES.append.md` says `B`, line 106 says `C` ("a third-party portal's record of a journal article, so
the tier is C"). Every claim above is about *this record's own fields*, which the portal is the authority
for, so `B` scoped to "what this record states about itself, not the article's text" is the reading that
survives QUALITY 7; a `C` row would fail criterion 7 for the entry. The frozen C2 counter does not read tier.

**One staged figure is a unit slip.** Staged line 106 says "page read 2026-10-24, 265,058 bytes, 8,804
characters of text extracted". Measured: the `.txt` is 8804 characters (14135 bytes); the `.raw` is
**276803 bytes on disk** / 265058 *characters* decoded UTF-8, and no `.raw` in the cache is 265058 bytes
(all 2596 `.raw` files of the 2549-key cache scanned). So 265,058 is a decoded character count, not a byte
count — same numbers, one unit wrong.
## 7. Boundaries and out-of-scope

Read: the two files of one cache key; `corpus/evidence/round52/{claims.md,c2-count.py,build-spans.py}`;
`corpus/QUALITY.md`, `PROVINCE.md`, `tools/inference-ground.py`, `corpus/SOURCES.md`; the row text of
`merge/chousa` (read-only); `tools/capture-text.py` and `corpus/evidence/round51/quote-substance-check.py`
(executed read-only).

Deliberately not done: the S112 (中国全科医学) capture; the `.docx`/NIPH work; the C1 counter;
`corpus/lessons/round-52.md` (it must carry every quote of §3 verbatim for `QUOTES_IN_LESSON` — L1's
file); the registry write; the entry write; any staging campaign tool. No other seat's report was
opened, so `R52GroundMedsciA`'s pass stays independent. Scratch
`/fast/scratch/hyaku/chousa-r52/R52GroundMedsciB` (TMPDIR) held the probe root and is removed after this
report; every receipt above is copied into it. No tool was installed or upgraded; no pacman transaction ran.

VERDICT: re-grounded staged S111 through the `.txt` UTF-8 form — identity stamp fixed (two dates ten days
apart, no author field, ten-point paywall, no DOI/originalUrl), 11 unique located quotes (char 2034…6974)
built and gated PASS by `build-spans.py`, `inference-ground.py` and `quote-substance-check.py`, 15 field
terms and 9 database names swept absent at 0 in both forms with PRISMA-S/文献检索/16个条目 at 15/15/2
(26/20/2 in the `.raw`) as positive controls, and the 简要介绍 block proved unquotable (two full copies,
four blurb copies) so it must carry occurrence counts, not a quote.
