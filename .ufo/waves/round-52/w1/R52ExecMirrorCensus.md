# R52ExecMirrorCensus — mirror append, census-validated (round 52, w1)

Reads only: lane corpus at `37468eadd8d098e80289b2f31a22de3872d4a1f6` and the staging package
`/home/vgpnk/Projects/shokuknow/merge/chousa`; writes only this report and
`/fast/scratch/hyaku/chousa-r52/R52ExecMirrorCensus/` (removed once the receipts below were
copied in). No production file, git index or sibling lane touched.

## 1. Mirror + the adopter run I drove myself

```
S=/fast/scratch/hyaku/chousa-r52/R52ExecMirrorCensus; export TMPDIR=$S/tmp
cp -a /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus $S/lane/corpus
cd /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge   # read-only source
cp chinese-search-log-r37-amendment-2026-10-23.md japanese-search-record-r38-amendment-2026-10-23.md japanese-prisma-item-wording-r40.md $S/adopt/knowledge/corpus/knowledge/
env -u ASSIMILATE_CITES python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/assimilate-rows.py --staged /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md --knowledge $S/adopt/knowledge --registry $S/lane/corpus/SOURCES.md --opened 2026-10-26 --out $S/adopt/out --entry corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md --entry corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md --entry corpus/knowledge/japanese-prisma-item-wording-r40.md
EXIT=0
stdout: COLLISIONS=31 | CITED=5 APPEND=4 HELD=1 | BODYONLY=7
stderr: 7 WARN lines, all "body-only id SNNN is also a lane id and reads as that row"
```

`renumber.tsv` verbatim (registry max `S112`, `tail -3 .../reg-ids` = `S110 S111 S112`):

```
staged_id	lane_id	action	url
S111	S113	append	www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3
S112	S114	append	www.chinagp.net/CN/column/item185.shtml
S125	S115	append	c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx
S126	S112	held	www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf
S129	S116	append	www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf
```

S126 is `held` against lane S112 (same normalised URL) — no fifth id minted; `stripped.tsv` removed
only the recheck prose tails and the old `opened 2026-10-23`; `bodyonly.tsv` = 7
`entry<TAB>staged_id` lines (S091/S092/S093, S097 twice, S105, S106).

## 2. Hand normalisation (only the values the seat names)

1. `used-by` per document: S113, S114 -> `corpus/knowledge/chinese-prisma-s-reception-r52.md`;
   S115 -> `corpus/knowledge/japanese-search-record-niph-form-r52.md`; S116 ->
   `corpus/knowledge/japanese-prisma-item-wording-r40.md`.
2. S116 source cell reordered **archive URL first**, then `**original withdrawn**:` with the
   publisher URL — exactly the URL the census's `url_of()` reads for the row.
3. `recheck` `180d` (NNd), `status` `mined`, `opened` `2026-10-26` (adopter wrote the last two);
   every other cell byte-identical, **including** each anchor's own read date (`page read
   2026-10-23`) — when the capture was read, not the row's `opened`.

## 3. Insertion + placeholder entries (mirror only)

Rows inserted after line 122 (last Registry row `| S112 | ...`), before the blank line preceding
`## Paths`; mirror lines 121-126 now read `S111 S112 S113 S114 S115 S116`. Stub entries
(`source:`/`verified-at:`/`recheck:` fields, marked PLACEHOLDER) sit at the three `used-by` paths under
`$S/lane/corpus/knowledge/`. The third is absent from the lane corpus too (`ls corpus/knowledge |
grep -i prisma` -> only `cnki-citation-check-r40.md`, `evidence-snapshot-coverage-r40.md`,
`receipt-expectation-digests-r40.md`), so L1 needs a real entry there.

## 4. `sources-census.sh validate` on the mirror

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/lane/corpus/SOURCES.md
EXIT=1
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	E11	S077 missing used-by tools/quarantine-check.py
```

All six lines are pre-existing: a pristine lane-corpus copy at the same `.../lane-base/corpus/`
shape prints byte-identical output (`diff` -> `IDENTICAL`, exit 1), so the four rows add no E and
no W. The E11 is a mirror-shape artefact: `--file` resolves `used-by` against the mirror root and
the real `tools/quarantine-check.py` (16281 B) was not copied. Copied in: `EXIT_WITH_TOOLS=0`, the
same five `W04` lines plus `file	ok	/fast/scratch/hyaku/chousa-r52/R52ExecMirrorCensus/lane/corpus/SOURCES.md`
(W-codes never change status, per the census contract).

## 5. Counts before/after (CORPUS.md section-Census awk, from each lane root)
| metric | before | after (mirror) |
|---|---|---|
| rows | 112 | 116 |
| tier | A=98 B=9 C=5 | A=99 B=12 C=5 |
| status | mined=88 queued=19 rejected=5 | mined=92 queued=19 rejected=5 |
| NF!=13 · dup ids · missing used-by | 0 · none | 0 · none · none |

Deltas are exactly the rows: +1 A (S115), +3 B (S113, S114, S116), +4 mined.

## 6. Does either URL trip E03/E04?

No. **E03** is id duplication only, and S113-S116 sit above the old max S112 (`grep -c
'^| S11[3-6] |'` = 4, one each; `uniq -d` over all ids empty). **E04** needs the same normalised
URL *and* the same scope, and no lane row carries either URL as its source URL: `grep -c` gives
`medsci.cn`=0, `chinagp.net`=0, `lifescience.co.jp`=0, `niph.go.jp`=0, and the lone
`web.archive.org` hit is in **S084's `teaches` cell** (cell 8), never a `source` cell, so
`url_of()` never sees it. Scopes differ, so even a repeat would be a W04. Mutants `$S/mutA`/`$S/mutB`
(mirror copy plus one row repeating a URL *and* its scope under a new id) both fire — the mirror's
silence is real, and the nested archive URL is read whole:

```
file<TAB>E04<TAB>S800 duplicate url www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3 within scope a Chinese-language, item-by-item ...
file<TAB>E04<TAB>S802 duplicate url web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf within scope the Japanese-language wording ...
```

## 7. The four normalised rows (candidate, for L1)
```
| S113 | 系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读（郑卿勇）— 梅斯医学 指南・解读指南, from 中国循证医学杂志 — https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3 | docs | B | a Chinese-language, item-by-item interpretation of PRISMA-S and of its limits as a reporting standard, as a Chinese source states it | the 简要介绍 block and the attachment 系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf; page read 2026-10-23 | that PRISMA-S is the PRISMA 2020 extension providing a 16-item specification for the search half of a review; and that a Chinese reading of it examines, item by item, its cross-disciplinary generality and its intrinsic limitations as a 报告规范, with practical recommendations for Chinese databases | mined | 2026-10-26 | 180d | corpus/knowledge/chinese-prisma-s-reception-r52.md |
| S114 | 中国全科医学 报告清单 — PRISMA2020条目清单 (Chinese translation of the PRISMA 2020 checklist) — 《中国全科医学》 — https://www.chinagp.net/CN/column/item185.shtml | docs | B | a Chinese journal's own published PRISMA 2020 checklist, including the per-source search-date item, as the journal states it | the 报告清单 table, items 5-9; page 发布日期：2023-01-31, read 2026-10-23 | item 6 requires every source to be named — databases, registries, websites, organisations, reference lists and any other route used — together with the 检索或查询日期 of each source; item 7 requires the complete search strategy for every database, registry and website, including the filters and limits used | mined | 2026-10-26 | 180d | corpus/knowledge/chinese-prisma-s-reception-r52.md |
| S115 | 提出様式（日本語）Reporting_Format_Jap_202404 — 国立保健医療科学院 C2H（Evidence to Decision）— https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx | docs | A | the search-record fields a Japanese national institute's own health-technology-assessment submission form requires, as that institute states them | section 3 追加的有用性, 3.1 システマティックレビューのリサーチクエスチョン; .docx opened and its `word/document.xml` extracted, read 2026-10-23 | the form requires SRにおける文献検索期間について明記する and fixes the end of the search window at one point between the analysis framework being decided and the analysis being submitted to the manufacturer; and where unpublished data were collected by ハンドサーチ等, that fact must be included in the PRISMA flow chart | mined | 2026-10-26 | 180d | corpus/knowledge/japanese-search-record-niph-form-r52.md |
| S116 | 「PRISMA 2020 チェックリスト」（日本語訳, JPT ONLINE, ライフサイエンス株式会社）— **archived at**: https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf — **original withdrawn**: https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf | docs | B | the Japanese-language wording of PRISMA 2020's own information-source and search-strategy items, as the official Japanese translation renders them — the primary translation, reached through an archive because the publisher's host no longer serves the file | 項目6 情報源 and 項目7 検索戦略, and the 抄録チェックリスト reference; archived PDF text extracted with pdftotext, read 2026-10-23 | the translation names every information source consulted — databases, registries, websites, organisations, reference lists — and requires the date each was last searched; and requires the complete search strategy for every database, registry and website, including the filters and limits used; the term 検索者 does not occur anywhere in the document, so PRISMA 2020 itself names no searcher | mined | 2026-10-26 | 180d | corpus/knowledge/japanese-prisma-item-wording-r40.md |
```

## Risks

- Exit 1 on the prescribed mirror shape is the pre-existing S077 E11, not these rows (section 4);
  the stubs prove only that paths exist — `japanese-prisma-item-wording-r40.md` is missing from the
  lane corpus today.

VERDICT: attacked the append path — adopter exit 0 with S126 `held` and S111/S112/S125/S129 ->
S113/S114/S115/S116, four hand-normalised rows plus three stub entries in a scratch mirror; `validate`
exit 1 printing exactly the six lines the pristine baseline prints (exit 0 / `file ok` once `tools/`
is mirrored), 112->116 rows, A98/B9/C5->A99/B12/C5, mined 88->92, NF!=13 = 0, dup ids none, and
neither the medsci nor the archive URL trips E03/E04 (mutant-proved the parser reads both).
