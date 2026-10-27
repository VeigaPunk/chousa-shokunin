# R53ExecMirrorCensus — mirror append, census-validated (round 53, w1)

Reads only: lane corpus at HEAD `6365f15` (registry byte-identical to `BASE_REV` `5b550133`) and the
read-only campaign package `/home/vgpnk/Projects/shokuknow/merge/chousa`. Writes: this report and
`/fast/scratch/hyaku/chousa-r53/R53ExecMirrorCensus/` (removed once the receipts below were copied in).
No production file, no lane registry, no git index, no sibling lane touched. No tool installed
(python3 3.14.8, bash 5.3.20, gawk 5.4.1 used as found).

## 1. The adopter v4 run I drove (row source)

```
S=/fast/scratch/hyaku/chousa-r53/R53ExecMirrorCensus; export TMPDIR=$S/tmp
cp -a chousa-shokunin/corpus $S/lane/corpus; cp -a chousa-shokunin/tools $S/lane/tools
cp -a /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/{search-tracking-record-r40.md,western-instrument-alignment-r50.md,quality-control-guideline-issued-text-r48.md} $S/adopt/knowledge/corpus/knowledge/
git -C chousa-shokunin show 5b550133d79bc09c82d8965cce2e48c2598b8c3e:corpus/SOURCES.md > $S/base/SOURCES.md
env -u ASSIMILATE_CITES python3 chousa-shokunin/tools/assimilate-rows.py --staged .../merge/chousa/SOURCES.append.md \
  --knowledge $S/adopt/knowledge --registry $S/base/SOURCES.md --opened 2026-10-26 --out $S/adopt/out \
  --entry corpus/knowledge/search-tracking-record-r40.md --entry corpus/knowledge/western-instrument-alignment-r50.md \
  --entry corpus/knowledge/quality-control-guideline-issued-text-r48.md
EXIT=0
COLLISIONS=35
CITED=6 APPEND=5 HELD=0 TWIN=1
BODYONLY=3
stderr: WARN search-tracking-record-r40.md: body-only id S094 …; WARN …: body-only id S114 …  (2 lines)
```

`cmp` base vs HEAD registry: byte-identical; base rows 116, base max id `S116`. `renumber.tsv`:

```
staged_id	lane_id	action	url
S134	S117	append	jmla.pitt.edu/ojs/jmla/article/download/1449/2061
S185	S118	append	www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf
S186	S119	append	m.bjhea.org.cn/35/202501/1126.html
S190	S120	append	pharmwyp.com/posts/56814/6.…%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf
S193	S121	append	training.cochrane.org/handbook/current/chapter-04
S195	S118	twin	www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf
```

S195 is `twin` of S118 (same row, nothing appended); five `append` ids, contiguous from `S116`.
The adopter's own entry copies confirm the citation map I use for `used-by`: `source: S117` in the
tracking entry; `S118 S119 S120` in the issued-text entry; `S121` **and** `S118` (S195 substituted)
in the alignment entry.

## 2. Hand normalisation (nothing to change, measured cell by cell)

Per row: `recheck` = `NNd` (365d for S117, 180d for the other four; each row's prose tail sits in
`stripped.tsv`), `used-by` = the lane entry paths, `status` `mined`, `opened` `2026-10-26`. I read all
five cells and they already equal that normalised form, so the pasted rows in §9 are the adopter's bytes
verbatim. Only hand step with any effect is scenario 2's id renumber (§8). `stripped.tsv` shows the four
`opened` values moved `2026-10-23/24` → `2026-10-26` and S120's staged `used-by` (which also named
`corpus/knowledge/grey-literature-mandate-scope-r48.md`, a path not in the package) replaced by the
entry actually cited.

## 3. Insertion + placeholders (mirror only)

Rows inserted after line 126 (`| S116 | …`), i.e. last Registry row before `## Paths` (line 128→133).
Mirror lines 126-131 now read `S116 S117 S118 S119 S120 S121`. Placeholder entries (PLACEHOLDER-marked,
`source:`/`verified-at:`/`recheck:` present) written at the three `used-by` paths under
`$S/lane/corpus/knowledge/`; **none of the three exists in the lane corpus today** (`ls corpus/knowledge`
→ no match), so L1 owes all three real entries.

## 4. `sources-census.sh validate` on the mirror

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/lane/corpus/SOURCES.md
EXIT=0
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W01	S120 tierC mined used-by=corpus/knowledge/quality-control-guideline-issued-text-r48.md
file	ok	/fast/scratch/hyaku/chousa-r53/R53ExecMirrorCensus/lane/corpus/SOURCES.md
```

Pristine lane-corpus copy at `$S/lane-base/corpus/` (same `tools/` shape) prints the same five `W04`
lines plus `file ok`, **exit 0**; `diff` vs the mirror differs only by the added `W01 S120` line and
the path on the `ok` line. So: no E line at all, no new `W04`, and **one new warning, `W01`**, which the
S120 row trips by construction (staged row tier C, and §2 makes its `used-by` non-`—`). W01 is a warning
per the census contract (exit unchanged); the L1's options are to leave tier C with the warning or
re-tier the row, and I propose neither — the tier is the campaign's own `C` scoping and C2 requires the
`used-by` line. This is a finding, not a patch.

## 5. Counts (CORPUS.md §Census awk, run from each corpus root)

| metric | before (lane HEAD) | after (mirror) |
|---|---|---|
| rows | 116 | 121 |
| tier | A=100 B=11 C=5 | A=102 B=13 C=6 |
| status | mined=92 queued=19 rejected=5 | mined=97 queued=19 rejected=5 |
| NF!=13 | 0 | 0 |
| duplicate ids | none | none |
| enum violations / missing used-by | none | none |

Deltas are exactly the rows: +2 A (S117 paper, S121 docs), +2 B (S118, S119), +1 C (S120), +5 mined.
`rows`/`NF!=13`/`tier`/`status`/`uniq -d`/enum/used-by-exists commands are the CORPUS.md block verbatim.

## 6. E03 / E04 / W04 for the five URLs

Normalised identities (`url_of()`: scheme stripped, host lower-cased, trailing `/` and fragment removed),
each compared against every pristine Registry `source` cell:

```
S117 'jmla.pitt.edu/ojs/jmla/article/download/1449/2061'                            pristine_same_url= NONE
S118 'www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf'        pristine_same_url= NONE
S119 'm.bjhea.org.cn/35/202501/1126.html'                                           pristine_same_url= NONE
S120 'pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E…'      pristine_same_url= NONE
S121 'training.cochrane.org/handbook/current/chapter-04'                            pristine_same_url= NONE
ids_present_in_pristine: NONE
```

The five URLs are pairwise distinct (5 distinct normalised forms) and none repeats a lane URL, so
neither E04 nor W04 is possible; ids `S117-S121` sit above the old max `S116`, so E03 cannot fire either.
Mutant proof that the parser would have caught it on exactly this mirror shape:

```
mutA (extra row `| S121 | Duplicate id mutant …`):      file	E03	S121 duplicate id                              EXIT=1
mutB (S118's URL + S118's scope under new id S122):     file	E04	S122 duplicate url www.bjhea.org.cn/…/1736907153935975.pdf within scope **for the national centre's …**   EXIT=1
```

## 7. Ordering hazard the mirror exposes (not a row defect)

Rows landed before their entries (same mirror, placeholders deleted):

```
EXIT=1   … W01 S120 … plus
file	E11	S117 missing used-by corpus/knowledge/search-tracking-record-r40.md
file	E11	S118 missing used-by corpus/knowledge/quality-control-guideline-issued-text-r48.md
file	E11	S118 missing used-by corpus/knowledge/western-instrument-alignment-r50.md
file	E11	S119 missing used-by corpus/knowledge/quality-control-guideline-issued-text-r48.md
file	E11	S120 missing used-by corpus/knowledge/quality-control-guideline-issued-text-r48.md
file	E11	S121 missing used-by corpus/knowledge/western-instrument-alignment-r50.md
```

Six E11 lines (S118 twice, once per entry) unless the three entries and the five rows land in one step.

## 8. Scenario 2 — S120 (NMPA copy) omitted, S121 renumbered S120

Same rows minus the pharmwyp row, Cochrane row id rewritten `S121`→`S120`, alignment placeholder's
`source:` line rewritten to match:

```
EXIT=0
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	/fast/scratch/hyaku/chousa-r53/R53ExecMirrorCensus/lane2/corpus/SOURCES.md
```

Counts: rows 120 (116→120), tier A=102 B=13 C=5, status mined=96 queued=19 rejected=5, NF!=13 = 0,
duplicate ids none. The `W01` disappears with the tier-C row; output is the pristine five `W04` lines,
byte-identical to the baseline apart from the `ok` path. Ids `S117-S120` contiguous from `S116`.

## 9. The five normalised rows (candidate, for L1; byte-verbatim from the mirror)

```
| S117 | PRISMA 2020 and PRISMA-S: common questions on tracking records and the flow diagram (Rethlefsen ML, Page MJ) — Journal of the Medical Library Association 110(2):253-257, doi 10.5195/jmla.2022.1449 — https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061 | paper | A | what PRISMA-S says must go into a search's tracking record and in which column of the flow diagram, as the statement's own authors explain it | the tracking-record and flow-diagram column discussion; publisher's OJS PDF, 5 pages, read 2026-10-23 | PRISMA-S recommends reporting the search strategies for all databases, registries and websites that were searched, and the number of records identified from each information source; and the flow diagram tracks records in two columns — identification of studies via databases and registers in Column 1, and identification of studies via other methods in Column 2 — with an overall number for records from databases and registers reported in Column 1 | mined | 2026-10-26 | 365d | corpus/knowledge/search-tracking-record-r40.md |
| S118 | 《药品临床综合评价质量控制指南（2024 年版 试行）》 — 国家药物和卫生技术综合评估中心（国家卫生健康委卫生发展研究中心），北京市卫生经济学会 载 — https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf | docs | B | **for the national centre's quality-control guideline in its issued (试行) form** — the document is the centre's, but the carrier is a professional society's file host, so the tier is B; this row governs any claim about the guideline's *wording*, because the draft and the issued text differ | the title block, and §1 文献研究的质量控制 with its （1）文献获取 subsection; PDF read 2026-10-24, 415,245 bytes, 27,609 characters of text extracted | the **issued** guideline's title block reads 药品临床综合评价质量控制指南, （2024 年版 试行）, 国家药物和卫生技术综合评估中心, （国家卫生健康委卫生发展研究中心）, 二〇二四年十二月 — and its 文献研究 chapter is worded differently from the draft the corpus quotes: the draft's 纳入标准应基于 PICOS 原则 becomes 可根据评价主题确定纳入与排除标准，可基于 PICOS 原则, and the draft's 所检索的数据库应包括中、英文专业数据库 becomes 所检索的数据库应包括**多个**中、英文专业数据库. So the corpus's round-13 row quotes the **draft**, not the guideline. The grey-literature sweep **holds in the issued text**: 灰色文献 counts 0 over the whole extraction (灰色 0, 未发表 0, 内部资料 0, 期刊评审 0), while 文献检索 counts 3, 系统评价 7, 数据库 3 and PICOS 1 — the draft objection was never about grey literature | mined | 2026-10-26 | 180d | corpus/knowledge/quality-control-guideline-issued-text-r48.md, corpus/knowledge/western-instrument-alignment-r50.md |
| S119 | 《药品临床综合评价质量控制指南（2024年版 试行）》发布 — 北京市卫生经济学会 载，来源 国家卫生健康委卫生发展研究中心 — http://m.bjhea.org.cn/35/202501/1126.html | docs | B | **for the issuance record of the centre's issued quality-control guideline** — the society's republication of the centre's own release notice, so the content is the centre's and the carrier is the society's, which is why the tier is B | the posting's title, its date and stated source, the act of issuance, and the attachment's own name; page read 2026-10-24, 17,592 bytes, 1,461 characters of text extracted under the checker's HTML-to-text transform | the release notice fixes the issuance facts the corpus could not previously source: the guideline was **released**, not merely circulated for comment, on **2025-01-03**, its stated source is 国家卫生健康委卫生发展研究中心, and the notice's wording is 现予以发布 — in contrast with the draft's public-comment notice. The attachment is named 药品临床综合评价质量控制指南（2024年版 试行）.pdf and sits on the society's own file host under a 2025-01-15 upload path, so the issued text and its notice are both open access from a host that answers | mined | 2026-10-26 | 180d | corpus/knowledge/quality-control-guideline-issued-text-r48.md |
| S120 | 关于发布上市药品临床安全性文献评价指导原则（试行）的通告（2019年第27号）及其所附指导原则全文 — 国家药品监督管理局，转载于 药研日记 — https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf | docs | C | **for the scope and the reporting duty of the regulator's grey-literature mandate**, as distinct from its bare existence — the content is NMPA's and the carrier is a third party's site, so the tier is C | 二 方法学要点 3 全面查找证据, and the 报告撰写规范 section that makes the search strategy a reported field; PDF read 2026-10-24, 960,118 bytes, 21,573 characters of text extracted | the 2019 guidance's grey-literature requirement has **three layers, not one**. It requires the searcher to collect unpublished material and gives publication bias as the reason; it places 研究但未发表的临床研究（灰色文献） inside the scope of a safety literature evaluation; it **mandates inclusion** of holder-initiated or holder-funded grey literature — 应当纳入研究；应当尽力获取其他灰色文献 — and it makes 是否检索灰色文献 a field the evaluation report must state. So the requirement is not a mention but a protocol carrying an inclusion duty and a reporting duty, which makes the national centre's issued guideline's silence on all three a substantive contrast rather than a wording difference | mined | 2026-10-26 | 180d | corpus/knowledge/quality-control-guideline-issued-text-r48.md |
| S121 | Cochrane Handbook for Systematic Reviews of Interventions, Chapter 4: Searching for and selecting studies — Cochrane — https://training.cochrane.org/handbook/current/chapter-04 | docs | A | **for the western handbook's own statement of how its searching and selecting guidance relates to PRISMA-S, and for its own wording on unpublished studies** — the publisher's own chapter text, so tier A for that scope | §4.2.1 Role of the information specialist/librarian, and §4.3.2 Ongoing studies and unpublished data sources; Handbook version 6.5.1, chapter last updated March 2025 | the chapter states in its own words that the reporting of the search and selection work aligns with the current reporting guidance for PRISMA and PRISMA-S (Rethlefsen et al 2021) — an explicit **instrument-to-instrument alignment** — and it treats unpublished studies as a bias problem rather than a reporting one: finding out about unpublished studies and including their results in a systematic review when eligible and appropriate is important for minimizing bias, with §4.3.2 on initiatives giving access to ongoing studies and unpublished data. That is the western half of this lane's subject in the handbook's own voice, and it is the kind of statement a Chinese methodological document cannot carry because it does not name PRISMA-S at all | mined | 2026-10-26 | 180d | corpus/knowledge/western-instrument-alignment-r50.md |
```

## Risks

- Exit 0 is the *mirror's* result with three placeholder entries; the lane has none of the three files
  yet, and §7 shows the rows landing first cost six E11 lines and exit 1. Rows and entries must land
  together.
- New warning `W01 S120` (tier-C row, mined, used-by non-`—`) is inherent to the frozen C2 shape, not a
  defect the seat may patch; flagged for L1's Gate block.
- Placeholders prove path resolution only. `used-by` for S118 names two entries because the twin S195
  becomes S118 in the alignment entry's header; if L1 drops that entry, S118's `used-by` must drop it too
  or E11 fires.
- `--file` labels the lane `file`; the census's lane-name column will differ under default discovery.

VERDICT: attacked the append path — my own adopter v4 run reproduced `CITED=6 APPEND=5 HELD=0 TWIN=1`
with S195 `twin` of S118 and S134/S185/S186/S190/S193 → S117-S121, five hand-verified rows plus three
stub entries in a scratch mirror; `validate` exit 0 printing the pristine five `W04` lines plus one new
`W01 S120` (no E line), rows 116→121, A100/B11/C5→A102/B13/C6, mined 92→97, NF!=13 = 0, dup ids none,
no URL trips E03/E04/W04 (E03 and E04 mutant-proved on the same shape), and the same run with the NMPA
row omitted and Cochrane renumbered S120 gives exit 0 with only the five pre-existing `W04` lines.
