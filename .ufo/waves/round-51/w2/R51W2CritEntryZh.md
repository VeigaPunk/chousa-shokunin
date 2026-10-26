# R51W2CritEntryZh — attack on `corpus/knowledge/chinese-search-record-r39.md`

Seat R51W2CritEntryZh, round 51 wave 2. Lane tip `4436e279b91d8d68fd439c9095695035fbeeab74`; entry, `corpus/SOURCES.md`, `spans.tsv`, `c2-count.py` read at that tip. Captures read from the read-only `.qcache`; scratch `/dev/shm/chousa-r51-CritEntryZh` deleted at the end. No production file, index, jj state or other seat's report touched. No tool installed (none needed).

## Commands run (observed)

1. `python3 tools/inference-ground.py --help` → usage accepted `--entry --spans --counts [--registry --root --json --quiet]`.
2. `env -u ASSIMILATE_CITES python3 tools/inference-ground.py --entry corpus/knowledge/chinese-search-record-r39.md --spans corpus/evidence/round51/spans.tsv --counts corpus/evidence/round51/c2-count.py --registry corpus/SOURCES.md --root .`
   → `GROUND entry=corpus/knowledge/chinese-search-record-r39.md section=1 bullets=6 tokens=9 grounded=9` / `GROUND: PASS` / `EXIT=0`. **It refuses nothing in this entry.**
3. `env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py` → `BOUND=6/7`, `BOUND_IDS=S107,S108,S109,S110,S111,S112`, `QUOTE_ROWS=61 ON_BOUND=61/61`, `QUOTES_IN_SPAN/ENTRY/LESSON=61/61`, `CAPTURE_BOUND=61/61`, `ANCHOR_BOUND=6/6`, `INFERENCE_GROUNDED=3/3`, `C2=PASS`, `EXIT=0`.
4. Replayed the entry's own `recheck:` command verbatim (three `.txt` forms read as UTF-8):
   ```
   52208 [1, 3, 0, 0, 0, 0, 4] [14179, 17709, 22932, -1, -1]
   50952 [0, 0, 0, 0, 0, 0, 0] [-1, -1, -1, 11404, -1]
   1675  [0, 0, 0, 0, 0, 0, 0] [-1, -1, -1, -1, 934]
   ```
   Header anchors all re-locate: S109 14179/15310/15240/17709/22932/24606/24298; S110 11110/11211/11404; S111 695/934/1138/1078/1366.
5. Backtick audit of the entry: 40 backticked strings, 28 are capture quotes, every one unique in its form and ≤160 chars, except `·比较医学研究与报告规范·` which occurs once in S109 and once in S110 (the shared series label; cited for S109 only, still once in that form).
6. S111 `.raw` decoded as UTF-8 (`17523` bytes; `.txt` is `1675` chars): the page's `<!-- … -->` block at raw chars 9192–9908 holds three recorded fields the text form drops.

## What holds (attacked, survived)

- **表1-not-表3 correction.** `表 1 研究方案主体报告框架内容` at 14179; the only `表` + digit tokens in S109 are 13895 (`表 1）`), 14179, 22722 (`表 2）`), 23316, 33964 (`表 3）`) — the 表 3 at 33964 is `（原文表 3）` inside the cited example's discussion. The staged header did say `表3 报告模块表` (`merge/chousa/knowledge/corpus/knowledge/chinese-search-record-r39.md:3`), so the correction is real provenance.
- **Identities.** S109 45(4):496–507 at 51555, DOI at 41, 文章编号 `1674-5817（2025）04-0496-12` at 4107; S110 45(1):101–111 at 49272, DOI at 54, `1674-5817（2025）01-0101-11` at 1553; both `·比较医学研究与报告规范·`.
- **Field-scoped absence.** 2.1.1 at 17069, absence sentence at 17509; the same paragraph calls PRISMA `当前国际通用的 SR 与 Meta 分析报告规范` — the copy does distinguish general from animal-specific. The reading is right.
- **Grey requirement vs S110 practice.** S109 `灰色文献` at 15310/22645/24033, S110 0; S109's own 表2 files CBM/CNKI/万方 under 通用数据库, not 灰色文献, and §2.4.1 at 22628 bundles `通用数据库+动物研究专用数据库+灰色文献/预印本平台`; S110 has 灰色/学位论文/会议/预印本/未发表/追溯/手工 all 0. The contrast holds.
- **Searcher sweep, widened.** `检索者/检索人/检索员/检索专家/信息专员/文献检索人员/检索由/独立检索/执行检索` = 0 in S109, S110 and S111 forms. `国家标准` 0; S109 does carry 标准×31/规范×27, so the claim must stay "no *national* standard", which it does.
- **No full text.** S111 raw carries a `原文索取` POST form to `doc.sinomed.ac.cn/inter/JspShopCartService.jsp` (char 14691); the Flash notice belongs to a `banner.swf` 425×80 object + `expressInstall.swf` (1800–2320), not a full-text viewer; `全文`/`pdf` 0 in raw.
- **16 items.** `包含16个条目的专项规范` at 934, unique.

## Defects

**D1 — Inference 1, floor/bar: "nothing a reader could run" is contradicted by the entry's own Observation.** 表1 row 3 is at 15113 (`（1）检索数据库（如 PubMed、Embase 等，含动物实验特殊数据库）`), 15186 (`（2）检索时间范围：`), 15240 (`检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）`), 15307 (`（3）灰色文献的检索与记录`). Item (2) already requires the terms **and their logic**, so a record that fills the three items does carry a runnable term set; the entry's Observation says as much one paragraph earlier. Attack: fill (1)–(3) and the reader has databases + dates + terms + boolean logic — runnable. The real delta is narrower: one database's *complete* string plus §2.4.1's unlisted extras (supplementary-search disclosure at 23180/24606, `文献管理软件` 24690, `去重方法` 24697). **Narrowing:** "a record can fill the three module items and still lack one main database's complete, re-runnable string (and the supplementary-search / reference-manager record)."

**D2 — Observation 6, truncation point does not reproduce.** The bullet says the abstract "ends truncated at `在逐条阐释其内…`"; in the `.txt` form 在逐条阐释其内 is at 980, mid-abstract, and the abstract runs on to `…作为“报告规范”的内在局限,并针对中文` (last characters 1024–1029, `并针对中文`, unique). The truncation is real; the stated end point is wrong by 44 characters of text. **Narrowing:** "the abstract breaks off mid-sentence after `并针对中文` (char 1024, form ends 1029)" — same prose-named-fragment class as the current token, so no manifest row or count changes.

**D3 — Observation 7, `全文` figure contradicts itself.** The same bullet prints `全文 4 / 0 / 0` and then "the only 全文 occurrences are in the two PDFs (S109, S110, S111)". S110's form has none: all four hits are in S109 at 20856, 22789, 25488, 30115 — and 22789 is a substring hit inside `以补全文献检索结果` (`补全文献` occurs once), not a 全文 token, so S109 carries three genuine `全文` tokens (`为全文提供` 20856; `全文复筛` 25488, 30115), none about full-text access. **Narrowing:** "the four hits are all in S109 (one is the substring `补全文献`); S110 and S111 carry none", or drop the clause and keep `S111 … no full-text token`, which is true.

**D4 — Observation 7, page-level absence from a text-form sweep (the comment-only field).** The bullet says "S111's record page shows no `学科分类号` field". `学科分类号` is 0 in all three `.txt` forms, but the S111 **raw** carries, inside an HTML comment (9192–9908): `学科分类号： R-05;R-37;R348.3;R916.3`, `主题词： *评价研究;*研究报告;Meta分析;*清单;质量控制`, and `基金：` five grants. The 主题词 list is also rendered under `查看主题词相同的文献` (1078), so that half is safe; the 学科分类号 row is comment-only. The page therefore **does** carry the field and does not render it; a sweep over one extraction cannot ground a claim about the page. **Narrowing:** "the rendered text form carries no 学科分类号 token; the S111 raw carries the field in an HTML comment, so the record has it and does not display it" — and drop "S111's record page shows no 学科分类号 field".

**D5 — Inference 4, one document generalised to a standard.** "one is a field-specific reporting standard, the other a general search-reporting extension" calls S109's copy a *standard* while S109's own sentence (`尚无专门针对动物实验 SR 的报告规范`, 17709) denies that such a standard exists, and the entry's own Unknown says "the copy is framed as 建议", while the title ends `…规范撰写建议`. The compatibility conclusion survives; the category label does not. **Narrowing:** "one is a field-specific reporting *recommendation* (S109 records that no 规范 exists yet), the other a general search-reporting extension."

**D6 — Observation 5, minor: English term-list range.** "an English one running from animal experimentation to systematic review": the list's last term is `meta-analysis` (B 12298, right after `systematic review` at 12279, both before `等`). **Narrowing:** "…to `meta-analysis`", or "…from animal experimentation through systematic review and meta-analysis".

## What `inference-ground` cannot see (mutations on scratch copies)

- Refuses fabrication: injected Inference bullet quoting `这不是任何捕获里的引文内容` cited S109 → `FINDING INF_TOKEN_NOT_IN_SPAN … GROUND: FAIL` (EXIT 1).
- Refuses a wrong citation marker: injected bullet quoting S110's `检索中国知网、万方、中国生物医学文献数据库、` cited only `(S109)` → `INF_TOKEN_NOT_IN_SPAN … FAIL`.
- **Cannot see a CJK negation flip:** injected `S109 does not require \`至少提供一个主要数据库的完整检索策略\`` → `bullets=7 tokens=10 grounded=10 / PASS`. The named limit is real: `words()` is Latin-only, a CJK token is presence-checked only.
- **Cannot see the Observation section:** injected Observation bullet `The page shows \`这段文字不在任何捕获中\`` → `bullets=6 tokens=9 grounded=9 / PASS`. D2, D3, D4 and D6 all live there.
- Cannot see counts: `c2-count.py` runs it with `--counts /dev/null`, so every `0 times`, `3/0/0`, `4/0/0`, `61` and the `16`-item figure are unverified by the gate; I checked them by command (above). It also cannot see entailment (D1), the standard/recommendation category (D5), located-once/length of entry quotes (only manifest rows are measured), char offsets, or text-form vs page (D4). Its `PASS` is therefore not evidence against D1–D6.

## Impacted axes and smallest safe correction

- **Depth:** D1 (the entry's core "floor vs bar" inference overstates the gap) and D4 (a page-level absence claim grounded on one extraction). Both are fixable by one-phrase narrowings that keep the reading.
- **Calibration:** D2, D3, D5, D6 — four textual/figure corrections; none needed for the entry's argument to stand.
- **Operability:** unaffected. All six corrections are text-only inside `corpus/knowledge/chinese-search-record-r39.md`: no predicate, target, counter, control, manifest row or lesson line changes; `c2-count.py` stays `C2=PASS` and `inference-ground` stays `PASS` (both were run before the corrections were drafted, on the current bytes).

VERDICT — attacked the 表1/表3 correction, the floor/bar inference, the S109/S110 grey difference, the field-scoped absence, the SinoMed record fields and the three negative sweeps: the correction, the absence reading, the grey contrast and the sweeps hold, but the floor/bar inference overstates ("nothing a reader could run" is contradicted by 表1 item (2)), the S111 truncation and `全文` figures do not reproduce, and "the record page shows no 学科分类号 field" is false at the raw level (comment-only `R-05;R-37;R348.3;R916.3`) — four fixable text defects, no predicate or counter break.
