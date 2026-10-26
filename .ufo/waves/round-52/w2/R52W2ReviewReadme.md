# R52W2ReviewReadme — attack: README block `## Round52 coverage and frontier` (corpus/README.md:1113–1138)

Seat: R52W2ReviewReadme (leaf, no subagents). Target: every count and command in the block, the "held before" claims, the S113 second-carrier judgment, and every Left-open item. All evidence below is from commands I ran 2026-10-26; captures opened read-only from `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (verified hash keys: S113 `453d492becd9a2f4632cb8dd`, S114 `cacddf3bbf780a4c7582bb17`, S115 `3a8b45977cd111e45e3980a5` (.raw), S116 `e84bfe97808591d23fe3266f`, SinoMed `42bac8830527d6f1bb125c49`).

## 1. Base sweep (README line 1124)

Command as written, against the lane at base:
```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f5272a1d98b6d34913985fa4537e00aaf9 -- corpus/knowledge
(no output)
$ echo $? → 1
```
PASS — empty output, exit 1. The three terms are absent from `corpus/knowledge` at base; each round-52 entry holds its own term (r52 lesson line 84 restates it).

## 2. "Held before" claims (README lines 1130–1131)

`git ls-tree -r --name-only 00f8c7f… -- corpus/knowledge` → 72 files, including `japanese-search-record-r38.md` (S107 journal 特別報告, S108 industry-body 留意点), `japanese-search-record-r38-amendment-2026-10-23.md`, `chinese-search-record-r39.md` (S109/S110 journal copies, S111 SinoMed record), `search-log-method-r39.md`. S108 is titled 別紙様式(V)-4/5 of 一般社団法人 健康食品産業協議会 and r38 itself calls it "the form" — so "society-journal articles and one industry form (round 51)" stands. "round 51's 'refused for capture form' class": round-51 lesson line 57 (`refused-doc: … refused this round for its capture form, not for its source quality`) — stands; the NIPH entry's ground restates it. PASS.

## 3. S113 second-carrier check (README line 1124)

Compared the SinoMed record the lane holds via r39 S111 (42bac883) with S113's capture (453d492):

- Same title: 系统评价/Meta分析中文献检索报告清单(PRISMA-S)解读 (both; MedSci's label is the page title, the record's is the abstract title).
- Same authorship: SinoMed lists 郑卿勇; 周泳佳; …; 田金徽 (12 names); MedSci has no author field but its attachment filename carries 郑卿勇 (453d492 char 4850; 郑卿勇 occurs 3×, all in that filename).
- Same journal: SinoMed 来源出版物：中国循证医学杂志 卷：26 期：4; MedSci byline "2026-04-25 中国循证医学杂志" (char 2034).
- Abstract overlap: SinoMed truncates mid-sentence at `并针对中文` (42bac883, no clause); MedSci continues `并针对中文数据库等本土化应用挑战提出实践建议。` — the added last clause claimed. (Punctuation differs between the two renderings, half- vs full-width; same article.)

Conclusion: same article; S113 is a second carrier, per-document credit of three (S115, S116, S114) holds.

## 4. Counts and manifest

- Lesson: collisions 31 (round-52.md line 36, `collisions` 31 lines), renumber by document (S111→S113, S112→S114, S125→S115, S129→S116), six mined mistakes (line 143), S120 verdict re-located (line 75–77: char 8996/9020/9428 in capture-text form). All present.
- Manifest: `spans.tsv` 39 lines incl. header = 38 quote rows; `c2-count.py` prints `QUOTE_ROWS=38 ON_BOUND=38/38`; `build-spans.py --check --root <lane>` prints `SPANS_ROWS=38 STALE=0` exit 0. "38-quote manifest" holds.
- QUALITY 87–90 exist with runnable checks; SKILL Gates rows `capture-text` and `chousa round-52 counters and checks` exist; erratum E1–E4 exist.

## 5. Commands in the block, run

```
$ python3 corpus/evidence/round52/c1-count.py → LEGS=9/9 C1=PASS exit 0 (REAL rc=0 count=1 locate=(0,1,8996) chars=19682)
$ python3 corpus/evidence/round52/c1-supplement.py → SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS exit 0
$ python3 corpus/evidence/round52/c2-count.py → BOUND=4/4 REFUSED=0, NEW_GROUND=3/3, ANCHOR_BOUND=4/4, QUARANTINE_VERDICTS=1/1 (S120), C2=PASS exit 0
$ python3 corpus/evidence/round52/verdict-gap.py --from 46 --to 51 → R47/R48 gaps reported (its purpose), exit 1
$ python3 tools/capture-text.py <qcache>/cb101e95f5f5e98d019eeca1.raw → exit 2 REFUSED main part 'xl/workbook.xml' is not WordprocessingML (root …spreadsheetml…workbook)
$ python3 tools/capture-text.py <qcache>/b539a80218080da56a75b624.raw → exit 2 REFUSED main part 'theme/theme/themeManager.xml' … not WordprocessingML
```

".xlsx … refused, not read" verified live on both workbook captures; `.pptx` has no cache capture (rule is the same non-`w:document` root test, so the class claim is consistent but not directly exercisable from cache). NIPH quotes re-located: 8996/9020/9428/19496/19521 all exactly once.

## 6. DEFECT — Left-open "searcher identity" line (README:1135) overstates "count reviewers for screening and data collection only"

Both checklists carry a THIRD reviewer count, risk-of-bias assessment (item 11), so "only" is false for both:

- S116 (Japanese, e84bfe9.txt): item 8 `スクリーニングしたレビューアの数` (char 830), item 9 `データを収集したレビュー担当者の数` (char 1012), item 11 `各研究を評価したレビューアの数` (char 1844). The only other 数 hits are item 16a's record-flow counts (3120/3134), not reviewer counts.
- S114 (Chinese, cacddf3.txt): item 8 `每项检索记录由几人进行筛选` (char 1917), item 9 `几人提取数据` (char 2019), item 11 `评价 人数` (char 2455, inside "详细说明 评价 纳入研究偏倚风险的方法，包括使用评价工具的细节， 评价 人数以及是否独立 进行").

The entries themselves do not make the "only" claim (r40 paragraph observes items 8/9 as "neither is a search field"; it never says no other count exists). The README's "only" is its own overstatement: the two checklists count reviewers for screening, data collection AND risk-of-bias assessment. Smallest safe correction: drop "only" or list all three steps.

## 7. Minor observation (not a claims failure): spans.tsv "offset" column = span start

`build-spans.py` writes `start = max(0, off - CONTEXT)` (CONTEXT=80) into the `offset` column; the frozen C2 predicate ties "recorded offset" to the slice, and `c2-count.py` reconciles by `int(offset) + span.find(quote)` (c2-count.py:213), so counters are consistent. But the manifest's offsets differ from the entries'/SOURCES `char N` values by 80 (e.g. S113-1 row 1954 vs quote 2034; S116-8 row 735 vs 815; S116-9 row 916 vs 996). The header just says `offset`; the README/claims do not define it as span-start. Documentation nit only — nothing in the block's claims depends on it.

## 8. Other Left-open items — verified against entries

- NIPH section 7 private outside experts: chars 19496/19521 re-located; "names outside experts privately" stands.
- Chinese PRISMA-S item text unread: S113 `CNKI/中国知网/万方/维普/SinoMed` all 0 in 453d492; portal names article only as attachment (4850); SinoMed cuts abstract off at 并针对中文. Stands.
- Publisher's current Japanese translation: `f3dbe2fe59a684b1b94cfadc.fail` = 6 bytes `rc=28`; memento `c280fdf8…` `.raw` sha256 `ba9bc9c1…` == `e84bfe9…` `.raw` sha256. Stands.
- Other capture forms: OLE .doc UTF-16LE form recorded in round-48 lesson (S095/S125 rows); xlsx refusal verified live above. Stands.

## VERDICT

Attacked the Round52 README block: base sweep (pass), held-before claims (pass), S113 second-carrier judgment (pass, SinoMed and MedSci are the same article), all counts/counters (pass), and the Left-open items — one defect: README:1135 "count reviewers for screening and data collection only" is false for both checklists, which also count reviewers for risk-of-bias assessment (S116 item 11 char 1844; S114 item 11 char 2455); plus one documentation nit (spans.tsv offset = span start, +80 from quote offsets).
