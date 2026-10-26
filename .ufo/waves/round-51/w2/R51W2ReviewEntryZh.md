# R51W2ReviewEntryZh — `corpus/knowledge/chinese-search-record-r39.md` vs QUALITY 1–86 and PROVINCE

Seat R51W2ReviewEntryZh, round 51 wave 2 (falsify), leaf seat. Target 37 lines, sha256
`092d9d3e8155e59d9db08ddc49136b5ea84ec092da96e8078aaf4d369fd5b499`, equal to
`git show 4436e279:corpus/knowledge/chinese-search-record-r39.md | sha256sum`; lane tip
`4436e279b91d8d68fd439c9095695035fbeeab74`. No tool installed (pacman paused; none needed).
Scratch `/dev/shm/chousa-r51-R51W2ReviewEntryZh/` deleted after the runs.

## Provenance trio and registry rows (criteria 6, 7)
- `entry:3–5` three `source:` lines; URLs byte-equal to `corpus/SOURCES.md:119–121` (S109 `…/EN/…id=5290`,
  S110 `…/CN/…id=5237`, S111 `https://www.sinomed.ac.cn/article.do?ui=2026335073`). Rows read
  `| … | paper | A | … | mined | 2026-10-25 | 365d | corpus/knowledge/chinese-search-record-r39.md |`
  (S111 `docs | B | … | mined | 2026-10-25 | 180d |`): status mined, tier A/A/B, `used-by` exactly this
  entry. S111's scope ("as this record page shows them; not the interpretation's item text") is kept by
  `entry:28,32`.
- `entry:6` `verified-at: 2026-10-25 … .txt form read as UTF-8 (52,208 / 50,952 / 1,675 characters)`;
  lengths re-derived below. `entry:7` `recheck: 365d` plus one command.
- **F3:** `entry:7` `365d` contradicts `SOURCES.md:121`'s S111 cadence `180d` (S109/S110 rows do say
  `365d`), so S111's overdue date is computable two ways (criterion 9, one home per number).
- The recheck command runs from a foreign cwd; run verbatim from `/dev/shm/chousa-r51-R51W2ReviewEntryZh`,
  exit 0:
  `fd468a36…txt 52208 [1, 3, 0, 0, 0, 0, 4] [14179, 17709, 22932, -1, -1]`
  `c7266931…txt 50952 [0, 0, 0, 0, 0, 0, 0] [-1, -1, -1, 11404, -1]`
  `42bac883…txt 1675 [0, 0, 0, 0, 0, 0, 0] [-1, -1, -1, -1, 934]`
  Vector order `布尔,灰色文献,检索者,检索式,学科分类号,国家标准,全文`; find list `表 1…, 尚无专门…,
  至少提供…, 从各数据库…, 包含16…`. This matches `entry:19`'s 3/0/0, 1/0/0, 4/0/0 and four zeros. It
  prints and never asserts: a moved anchor prints `-1` and exits 0 (criterion 13 passes as runnable;
  it is a probe, not a screen).
- `sha256sum` of the three `.txt` = `90f2f54cef21cb49…`, `03342b7ded4f9d68…`, `4d3bff5067b4cf8e…`,
  byte-equal to the `capture_sha256` column of rows S109-1…S111-6 in `corpus/evidence/round51/spans.tsv`.
  Criterion 57's bytes therefore exist in the committed manifest, though `entry:6` prints no digest.

## Counts, sweeps and quotes
- Sweeps re-run (above): 检索者/检索式/学科分类号/国家标准 = 0 in all three forms; 灰色文献 3/0/0;
  布尔 1/0/0; 全文 4/0/0; word-boundary counts AND 0 and OR 0 in S110. `entry:19` holds until its
  last clause, which says "the only 全文 occurrences are in the two PDFs (S109, S110, S111)": all four
  are in S109's form (finds 20856, 22789, 25488, 30115) and S110's form has 0. **F2.**
- I widened the searcher negative past the entry's token: 检索员/检索人员/检索人/信息专员/图书馆员/
  实施检索/执行检索 = 0 in all three; `由[^。\n]{0,40}检索` = 0 in S109 and S110 (every `由` is
  由于/由词/由多). `entry:27`'s "unrecorded here rather than refused" holds.
- Quotes: the 26 manifest rows naming this entry (13 S109, 7 S110, 6 S111) each occur exactly once.
  Independent `text.find`: S109 14179/15310/15240/17709/22932/
  24606/24298; S110 11110/11211/11404; S111 695/934/1138/1078/1366 — each equals the find of the quote
  the entry uses. Four quoted fragments absent from `entry:3–5` (`含动物实验特殊数据库` 15140,
  `AND，OR 等` 23097, `参考文献追溯` 23180, `表 2 …` 23316) carry offsets in the Gate
  (`lessons/round-51.md:126–149`).
- **F1 (one false sentence).** `entry:18` ends "The abstract ends truncated at 在逐条阐释其内…;". In the
  `.txt` read as UTF-8, `在逐条阐释其内` is at 980 (count 1), but the abstract field (`摘要：` at 808) ends
  at 1024 with `并针对中文` (count 1, `t.count('…')` = 0). The raw HTML's abstract `<p>` tail is
  `…内在局限,并针对中文` before `</p></span></td></tr>` (raw 8850–8930). Neither this phrase nor
  `·比较医学研究与报告规范·` appears in `spans.tsv`, `quotes.tsv` or the Gate (`grep -n` exits 1), so it
  is also the one entry quote the Gate does not hold.
- `entry:13` holds: title set with inter-character spaces (`动 物 实 验 系 统 评 价 与 Meta 分 析 报 告
  的 规 范 撰 写\n      建议`, 1176); `entry:14`'s row 3 is exact (15000–15420, `（3）灰色文献的检索与记录`);
  `entry:15` holds against 22380–23260 and 24520–24780; `entry:16` against 16980–17920; the sole `表 3`
  token is `（原文表 3）` at 33964 inside the cited example's paragraph (33580–34080).
- **F5:** `entry:17` "an English one running from animal experimentation to systematic review" — the
  English list runs on to `meta-analysis` (11822–12290: `… "fruit fly" "systematic review"
  "meta-analysis" 等`).
- **F4:** `entry:5` names "the 来源出版物 / 关键词 / 主题词 fields", but the `主题词` row is inside an HTML
  comment (raw 8929–9610 holds both `学科分类号` 8997 and `主题词` 9154) and the `.txt`'s only `主题词` is
  at 1080 inside `查看主题词相同的文献` (1078). The values (*评价研究 … 质量控制) are visible there; the
  field label is not in the form the entry says it read (`lessons/round-51.md:51` says the same).
- **F6:** `entry:23` and the title make 表1 and §2.4.1 one record's floor and bar. 表1 is the protocol
  framework (`表 1 研究方案主体报告框架内容`, English "Framework for main report of research protocol",
  14179); §2.4 is `研究方法` (21841) and §2.4.1 `文献检索策略` (22408), i.e. the report's methods.
  "A record can fill the three module items and still carry nothing a reader could run" compares a
  protocol row with a report requirement.

## Criterion-by-criterion (entry-level surfaces only)
1 pass (falsifiable; one claim proved false). 2 **fails on `entry:18`'s last sentence** — the 980 anchor
supports the phrase, not an abstract end at 1024. 3 pass (`entry:11/21/30`). 4 n/a (entry not edited).
5 pass (`entry:9` keeps the dropped staged continuation and body reference; `test -e
corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md` → ABSENT; staged line 55 calls it "the
Japanese hand-search field found in wave 3 (`S097`)"). 6 pass except F3. 7 pass. 8 pass. 9 partial (F3;
lengths restated in `entry:6`, `SOURCES.md:119–121`, `lessons/round-51.md:49–51` with one command).
10 pass (`grep -nE '\$\{[A-Z_]+\}|\bTODO\b|\bTBD\b|LANE_HASH' entry` → exit 1). 13 pass (ran from two
cwds, exit 0; the "then re-download" clause is a blocked network step, not a command). 23 pass
(`prose-check.py entry` → `TOTAL hits=0`). 25 **not run** (F7). 26 pass (`grep -nwi live` → exit 1).
30 not run (F7), else the Gate's 26 rows resolve verbatim at their offsets. 37 pass (recheck).
57 held via the manifest hashes. 66/67 pass (`inference-ground.py` → `GROUND: PASS`, `bullets=6
tokens=9 grounded=9`); named limit: it reads Inference only, which is why F1 (Observation) survives it.
72 pass (`quote-substance-check.py spans.tsv` → `IDS=6 QUOTES=61 FAILURES=0`). 76 pass
(`decode-form-check.py entry` → `FORM_NAMED`; `entry:6` names `.txt` UTF-8). 77 pass: body S-ids are
`18 S109 / 15 S110 / 11 S111`, each opened by a `source:` line, no staged id leaks. 79 pass (CJK handled
by the tool above). Integration: `env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py`
prints, among its lines, `QUOTES_IN_ENTRY=61/61 CAPTURE_BOUND=61/61 INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120)`, `C2=PASS`, exit 0.

## Province
In province. Every bullet's subject is what a Chinese reporting copy asks a search record to carry
(search-strategy taxonomy: databases, window, terms+logic, grey literature, supplementary techniques)
or how a claim sits against its source (claim-vs-source verification). The animal-experiment/GRADE
material is the sources' subject, not an asserted biomedical finding; species and database tokens are
the record's term families and 表2's source taxonomy; the standards-body question is a scoping Unknown
(`entry:34`), not an absorbed regulatory claim; the staged headline ("China has no standard for one
yet", staged line 1) was narrowed to the field-scoped sentence (`entry:16/26`). No product
description. Only taxonomy imprecision is F6.

## Residual risk / gaps
- F7: QUALITY 25/30's `tools/quote-reopen.py verify` was not run — `grep -rln
  'QUOTE_REOPEN\|quote-reopen' corpus/evidence/round51 .ufo/waves/round-51` finds only wave-1 reports,
  and `R51GroundSlarcBB.md:74` says so (L0 `8d77e6c1` open). Substitute is sound but different:
  spans + `c2-count` + capture sha256 equality + my `text.find`/`count==1`. Two entry quotes fall
  outside the Gate (`·比较医学研究与报告规范·` 201, `在逐条阐释其内` 980), so "the Gate holds every located
  quote" is not literally true here.
- The entry prints no capture digest (57's evidence lives in `spans.tsv`); a reader without the host
  `.qcache` cannot re-read the bytes the hash binds. F3–F6 are prose-level repairs that touch no frozen
  predicate, target, counter or control.

## VERDICT
VERDICT: attacked `corpus/knowledge/chinese-search-record-r39.md` against QUALITY 1–86 and PROVINCE — **admit-with-narrowing**: cut `entry:18`'s `The abstract ends truncated at 在逐条阐释其内…;` (replace with "The abstract ends mid-sentence at `并针对中文` (char 1024)") and `entry:19`'s `the only 全文 occurrences are in the two PDFs (S109, S110, S111)` (replace with "all four 全文 occurrences are in S109's text form; S110's has none"); also align `entry:7`'s `365d` with `SOURCES.md:121`'s `180d` for S111, drop `主题词` from `entry:5`'s field list (or say "the subject-heading list under `查看主题词相同的文献`"), end `entry:17`'s English range at `meta-analysis`, and separate 表1 (protocol framework) from §2.4.1 (report methods) in `entry:23`; provenance trio, the 26 quotes and their offsets, the hashes, C2 integration and province all hold.
