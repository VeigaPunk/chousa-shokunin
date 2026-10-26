# R52W2ConnCrossEntry — cross-entry consistency, round 52 wave 2

Seat: R52W2ConnCrossEntry · scratch `/fast/scratch/hyaku/chousa-r52/R52W2ConnCrossEntry` (removed on exit, `trap`) · cwd stayed in scratch; every command used absolute lane/cache paths. No tool installed (read `~/.omp/agent/RULES.md`; none needed — `python3`, `git`, `pdftotext` already present; no pacman/uv/npx action). No network, no fetch, no writes outside this report.

## What I attacked

The same fact stated in two places must agree, across: the three round-52 entries (`corpus/knowledge/japanese-search-record-niph-form-r52.md`, `japanese-prisma-item-wording-r40.md`, `chinese-prisma-s-reception-r52.md`), the four rows S113–S116 (`corpus/SOURCES.md`), `corpus/lessons/round-52.md`, the `corpus/README.md` `## Round52 coverage and frontier` block, and `claims-erratum.md` E1–E4; plus non-contradiction with the round-51 entries they cite (`japanese-search-record-r38.md`, `chinese-search-record-r39.md`, `japanese-search-record-r38-amendment-2026-10-23.md`) and existence of every lane file an entry names.

## Fact · place · value table (all agree)

| fact | places (file:line) | value | verified by me |
|---|---|---|---|
| S115 text-form length | niph:3, lesson:8, lesson:48, SOURCES:S115, claims:18, SKILL:134 | 19,682 | `capture-text.py` on `.raw` → `LEN 19682`; `build-spans.docx_text` → `docx_text len 19682` |
| S116 `.txt` length | r40:3, lesson:49, SOURCES:S116, lesson:61, r38-amend Unknown | 5,328 | read `.txt` → `LEN 5328` |
| S113 `.txt` length | chinese:3, lesson:46, SOURCES:S113, lesson:62 | 8,804 | read `.txt` → `LEN 8804` |
| S114 `.txt` length | chinese:4, lesson:47, SOURCES:S114, lesson:62 | 6,179 | read `.txt` → `LEN 6179` |
| NIPH raw zip digest / size | niph:3, SOURCES:S115, lesson:60, SKILL:134 | 16fc8c55…, 178,056 B | `sha256sum` → `16fc8c55ee856f…`; `ls -la` → 178056 |
| NIPH text-form sha256 (E1) | erratum E1; SKILL:135 | 754aae42… | text form sha256 = `754aae4266a19af…` (both readers) |
| S115 quote offsets | niph source:3 + body; lesson quotes table (14 rows); SOURCES anchor: 8996/9020/9408/9419/9428; S120 verdict below | 9,42,51,1446,8389,8996,9020,9189,9257,9391,9408,9419,9428,19496,19521 | every quoted phrase re-found at its exact offset in the text form (count=1 each); canonical `--locate` → `LOCATED count=1 offset=8996` rc 0 |
| S116 quote offsets | r40 source:3 + body; lesson table (9 rows); SOURCES anchor: 475/592/641/753 | 0,475,508,555,592,641,753,766,815,996 | `t.find` → exactly those; `項目7` 0×, `検索戦略` 619/769, `情報源` 453/597 |
| S113 quote offsets | chinese:3–4 + body; lesson table | 2034,2328,2433,3139,4850,7287 | `t.find` matches |
| S114 quote offsets | chinese:4 + body; lesson table | 16,920,1650,1707,1785,5530,5694,5744,6121 | `t.find` matches |
| titles (S113–S116) | SOURCES, lesson:46–49, README:1117–1119, entries | identical strings | opened rows/entries |
| dates | entries `verified-at`/`recheck`, lesson:8/44–49, SOURCES rows, README | opened 2026-10-26; captures 2026-10-23; S113 发布日期 2026-04-25 (+ `guiderPublishedTime=Sat Apr 25 00:00:00 CST 2026`); S114 2023-01-31; S115 2024年4月 | match |
| “three documents” credit | README:1124, lesson:55, claims:76–77,116 | credit three (S115,S116,S114); S113 second carrier through `chinese-search-record-r39.md`; four documents rest on three entries | consistent wording |
| S113–S116 map | lesson:38 (S111→S113, S112→S114, S125→S115, S129→S116), README:1117–1119, entries `adopted:` | same ids | rows/entries open |
| tier | SOURCES S113 B/S114 A/S115 A/S116 B; lesson Census:141 | A S114 S115; B S113 S116 | match |
| S120 verdict offsets | register (absent-defect-register.md:55) quotes; lesson:73–78 (8996/9020/9428, form capture-text); round-51 lesson 39411 superseded | 8996,9020,9428 | each quote count=1 at stated offset; register row quotes identical |

## Cross-entry / round-51 non-contradiction checks

- Entries’ grounding references exist: `japanese-search-record-r38.md`, `japanese-search-record-r38-amendment-2026-10-23.md`, `chinese-search-record-r39.md`, `japanese-prisma-item-wording-r40.md`, `corpus/lessons/round-51.md` (with `## Gate` refused-doc paragraph for the NIPH URL), `round-52.md` — all present.
- r40:27’s “r38 records at char 13710 … who conducted the search” matches r38:12 (`このプロセスに際して，誰が検索を行ったの` char 13710). r40:28’s description of r39 matches r39:18 (SinoMed truncation at `并针对中文`, char 1024). chinese:15 repeats the same truncation fact.
- chinese:21 cites r40’s same item-6/item-7 class split; r40:20 states it — agree.
- NIPH entry's “r51 refusal reversed by the text form” is borne out by round-51 lesson:57 (`refused-doc … refused this round for its capture form`) and this round’s bound S115.
- All W1 reports named in the lesson exist in `.ufo/waves/round-52/w1/` (46 reports; spot-checked `R52SentCapture`, `R52ScoutConsiderthese`, `R52ScoutCoverage`, `R52CritForgeC1/C2`, `R52ExecRealDocx`, `R52ExecFormDiff`, `R52ExecQuarantine`, `R52ExecAdopterTwin`).
- Control numbers in lesson Mistakes rows match the frozen controls: `c1-before.txt` REAL naive line `locate=(0, 1, 10319) chars=21910`; cache-txt REAL `chars=168953` (= 168,952 + print newline; sidecar itself 168,952 chars, 72,117 U+FFFD, `文献検索` 0); main part `50 w:instrText / 60 mc:Fallback`; `提出様式`/`C2H`/`Evidence to Decision` 0×; `データベース` 4×, `検索式` 1×, `文献検索期間` 2×; section-3.1 heading second occurrence at 8471 (TOC first at 682).
- Replayed counters at the landed lane: `build-spans.py --check` → `SPANS_ROWS=38 STALE=0` rc 0; `c2-count.py --lane-only` → `ENTRIES=3/3 BOUND=4/4 QUOTE_ROWS=38 QUOTES_IN_ENTRY=38/38 QUOTES_IN_LESSON=38/38 ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=1/1 (S120) C2=PASS` rc 0; `verdict-gap.py --from 46 --to 51` → `R47 operability lane=improved verifier=harmed`, `R48 UNPARSED lane_axes=6 verifier_axes=0`, `R50 calibration lane=improved verifier=unchanged`, `VERDICT_GAPS=2 UNPARSED=1` rc 1 (as lesson:88). Base sweep `git grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f5… -- corpus/knowledge` → no output, rc 1 (README:1124).
- Independent decode: `pdftotext -layout` on S116 `.raw` reproduced `e84bfe97808591d23fe3266f.txt` byte-for-byte (10,106 B, `cmp` silent). Memento `c280fdf897ab0d488017b63a.raw` sha = `ba9bc9c1…` = S116 `.raw` sha; original-URL cache holds only `f3dbe2fe59a684b1b94cfadc.fail` = `rc=28` (6 B).

## Apparent differences, resolved (not disagreements)

1. `spans.tsv` offset column (e.g. S116: 0/395/428/475/512/561/673/735/916) vs lesson/entry quote offsets (0/475/508/555/592/641/753/815/996): the manifest column is the **span start**; each span slice at that start contains its quote later in the slice (c2 `SPAN_CONTEXT=38/38`; `QUOTES_IN_SPAN=38/38`). No conflict.
2. r40 lists a located quote `完全な検索戦略` at char 766 that is not among the lesson’s 9 S116 quoted rows (lesson/span manifests are the same 38 rows; the frozen predicate requires manifest quotes inside entry+lesson, not every entry quote in the manifest).
3. Erratum E1’s 754aae42… is the text-form digest; SOURCES/SKILL’s 16fc8c55… is the raw zip digest — different objects, both verified.
4. Round-51’s S120 `char 39411` vs round-52’s 8996/9020/9428: the lesson explicitly supersedes the old offset, not the verdict.

## Disagreements found

None among the named fact classes (offsets, character totals, titles, dates, three-documents credit, S113–S116 map, tier, S120 offsets); no entry contradicts another entry or its round-51 references; every lane file an entry names exists.

VERDICT: attacked cross-entry consistency across the three entries, four rows, lesson, README block and erratum — every shared fact (offsets, totals, titles, dates, credit, map, tier, S120) agrees after independent re-location; no disagreement found.
