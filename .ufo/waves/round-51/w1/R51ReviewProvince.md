# R51ReviewProvince — round 51 w1 — province & QUALITY bar, three staged entries

Seat: `R51ReviewProvince` (leaf, `/skill:godspeed`). Date: 2026-10-25. Tooling: read `/home/vgpnk/.omp/agent/RULES.md`; pacman guard respected; 0 tools installed/updated. Scratch: none created under `/dev/shm`. No network fetch (L0 `8d77e6c1` open).
Decode form (QUALITY 76): every `char N` below indexes the capture's `.txt` read as UTF-8 (`sha256(url)[:24].txt`), except where noted as `.raw` (`sha256(url)[:24].raw` HTML UTF-8 or `.docx` ZIP `word/document.xml`).

## 1. Commands & observed outputs on staged entries and captures

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ for f in japanese-search-record-r38.md chinese-search-record-r39.md japanese-search-record-r38-amendment-2026-10-23.md; do
    p="/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/$f"
    python3 tools/inference-ground.py --entry "$p" --spans /dev/null --counts /dev/null --registry corpus/SOURCES.md
    python3 corpus/evidence/round29/prose-check.py "$p"
  done
GROUND entry=japanese-search-record-r38.md section=1 bullets=3 tokens=3 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='as actually run'
FINDING INF_UNCITED bullet=2 token=''
FINDING INF_UNGROUNDED bullet=2 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='what the record claims'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='what the gate can check'
GROUND: FAIL
FILE .../japanese-search-record-r38.md | TOTAL hits=0 files=1
GROUND entry=chinese-search-record-r39.md section=1 bullets=4 tokens=1 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_UNGROUNDED bullet=1 token=''
FINDING INF_UNCITED bullet=2 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='what must a search record carry?'
FINDING INF_UNGROUNDED bullet=3 token=''
FINDING INF_UNGROUNDED bullet=4 token=''
GROUND: FAIL
FILE .../chinese-search-record-r39.md | TOTAL hits=0 files=1
GROUND entry=japanese-search-record-r38-amendment-2026-10-23.md section=1 bullets=4 tokens=2 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_UNGROUNDED bullet=1 token=''
FINDING INF_UNCITED bullet=2 token=''
FINDING INF_UNGROUNDED bullet=2 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='a field, but not in PRISMA'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='2020'
FINDING INF_UNGROUNDED bullet=4 token=''
GROUND: FAIL
FILE .../japanese-search-record-r38-amendment-2026-10-23.md | TOTAL hits=0 files=1
```

Capture digests (`sha256(url)[:24]` in `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`):
- `S109->S107` (`7194acc65a18f6555e4b8893.txt`, 21216 chars, sha256 `05c7ee9fe9e55461…`): J-STAGE 日健教誌 32(2).
- `S110->S108` (`62be15a474e866e4bef6c9d5.txt`, 39676 chars, sha256 `960da5cf632dbd27…`): JAOHFA `systematic_review.pdf`.
- `S116->S109` (`fd468a36d78ff156b6200946.txt`, 52208 chars, sha256 `90f2f54cef21cb49…`): 实验动物与比较医学 2025;45(4) id=5290.
- `S117->S110` (`c7266931a1731db3ff6ae77d.txt`, 50952 chars, sha256 `03342b7ded4f9d68…`): 实验动物与比较医学 2025;45(1) id=5237.
- `S119->S111` (`42bac8830527d6f1bb125c49.txt`, 1675 chars, sha256 `4d3bff5067b4cf8e…`; `.raw` 20142B HTML, sha256 `0d1c08a6ca7ee09a…`): SinoMed `ui=2026335073`.
- `S125->S112` (`3a8b45977cd111e45e3980a5.txt`, 168952 chars, sha256 `471e558969d4ec3d…`; `.raw` 178056B ZIP `.docx`, sha256 `16fc8c55ee856fef…`): NIPH `Reporting_Format_Jap_202404.docx`.
- `S126->S113` (`34fcefc159bf2ebbd1e09540.txt`, 25811 chars, sha256 `065b889a97b00f88…`): JAHBS 38(1) `vol38_1_5.pdf`.

## 2. Entry 1 — `japanese-search-record-r38.md` (staged `S109`->`S107`, `S110`->`S108`)

- **Province (`PROVINCE.md:5-15`):** **IN** (`search-strategy taxonomy`, `claim-vs-source verification`). What fields a systematic-review search record carries (`誰が検索を行ったの`, `その日時`, `使用した検索式`, per-database last-search date, hand-search presence/method) is search-strategy method. Zero `kengaku`, `kasegi`, `kumitate`, or `kotoba` spillover.
- **Regulatory drift (`S110` JAOHFA functional-foods form):** The form is a notification guidance manual (`機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文)`, `.txt` `char 835`). Its items 6/7 and `(V) -5` rules are search-record method, **except** Observation b3 (`:29-31`, edition line + "three cooperating bodies" as a standalone finding) and Unknown b1 (`:62-63`, functional-foods claims context), which drift into carrier/regulatory provenance; provenance belongs in `SOURCES.md` `source`/`scope` (justifying tier B), not as a method observation.
- **Generic / overclaimed / ungrounded bullets that must be narrowed:**
  1. **Header `:4`:** names `the section on 1次情報の「収集」, p.121`. In `7194acc65a18f6555e4b8893.txt`, `1 次情報の「収集」` is in the abstract (`char 252`) and section I (`char 1137`); the p.121 heading is `7.    1 次情報のまとめ` (`char 13128`), which splits across the two-column page break between `このプロセスに際して，誰が検索を行ったの` (`char 13367`, 1×) and `か，その日時，使用した検索式を同時に記録しておくこ` (`char 10231`, 1×) / `その日時，使用した検索式を同時に記録しておく` (`char 10234`, 1×) and `が同様の検索を再現できるようになる．` (`char 10369`, 1×).
  2. **Header `:5,7`:** writes unspaced `(V)-4`/`(V)-5`, ASCII `第2版`, and contiguous `検索者、検索ワード、検索式`. In `62be15a474e866e4bef6c9d5.txt`, `2026年6月5日 第２版` is fullwidth (`char 142`, 3×; `第2版` is 0×); `(V) -5` is spaced (`・検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。`, `char 4408`, 1×), while on p.7 (`char 36710-36843`) `検索者、`, `検索ワード、`, `検索式` are split across three table rows.
  3. **Observation b1 (`:18-19`):** "with a checklist in the appendix" — `7194acc65a18f6555e4b8893.txt` `char 12804` (`おいて報告すべき内容のチェックリストも付録されてい`) states PRISMA itself attaches a checklist, not that `S109`'s article has an appendix checklist.
  4. **Observation b2 (`:20-28`):** omits item 8's rule in `62be15a474e866e4bef6c9d5.txt` (`・検索者は、原則、#8に記載する。ただし＃7にも記載してあったとしても差し支えない。`, `char 5719`, 1×). Located quotes in `.txt`: `・検索したデータベース等の情報を全て記載する。` (`char 4046`, 1×), `・それぞれのデータベース毎に最後に検索した日の日付を記載する。` (`char 4122`, 1×), `・ハンドサーチの有無を記載する。ハンドサーチを実施した場合はその方法を記載する。` (`char 4210`, 1×), `・検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。` (`char 36783`, 1×).
  5. **Inference b1–b3 (`:35-56`):** b1 (`:37-42`) makes an ungrounded comparison to PRISMA-S/Cochrane and claims `(V)-5` "must hold what was typed, not a reconstruction", whereas `char 36783` explicitly permits `もしくはそれと同等の詳細なものであること` ("or equivalent detail"); also overlaps held `corpus/knowledge/search-log-method-r39.md` (`S078`) on search-log reproducibility. b2 (`:43-49`) is generic lane commentary (`verify-sweeps`) with zero source citation (`INF_UNCITED`, `INF_UNGROUNDED`). b3 (`:50-56`) cites body-only staged `S105` (`:54`, intended for `chain-resolution-r3.md`, colliding with lane `S105` = CNKI 管理员 manual in `corpus/SOURCES.md:115`) and quotes ungrounded `'what the record claims'` / `'what the gate can check'`.
- **QUALITY criteria failed as staged:** **2 & 30** (exact quotes not in entry; misnamed section/edition strings), **6 & 77** (unrenumbered `S109`/`S110`; body-only `S105` collides with lane `S105`), **8** (b1 overstates "what was typed" over `もしくはそれと同等の詳細なものであること`), **13 & 57** (`recheck:` orders live `re-download both` under open L0 `8d77e6c1`; bare `verified-at:`), **25 & 59** (register rows `S104` and `S105` on its two URLs are `payload-absent` due to two-column layout split and English splice — both re-verified `absent-as-written`), **66** (`inference-ground.py` rc=1: 2 `INF_UNCITED`, 1 `INF_UNGROUNDED`, 3 `INF_TOKEN_NOT_IN_SPAN`).
- **Verdict:** **`admit-with-narrowing`** (bind `S109->S107` and `S110->S108`, drop body-only `S105` in favor of file path `corpus/knowledge/chain-resolution-r3.md` / `sweeps-rejections-r5.md`, fold Observation b3 into provenance, narrow Inference b1–b3 to cited Japanese quotes including `もしくはそれと同等の詳細なものであること` and item 8's `#8` rule).

## 3. Entry 2 — `chinese-search-record-r39.md` (staged `S116`->`S109`, `S117`->`S110`, `S119`->`S111`)

- **Province (`PROVINCE.md:5-15`):** **IN** (`search-strategy taxonomy`). `S117`'s GRADE study is biomedical SR methodology, not LLM/model evaluation (`kengaku`), and the entry reads only its section 3 `检索策略` paragraph. Zero `kengaku`, `kasegi`, `kumitate`, or `kotoba` spillover.
- **Biomedical drift (`S116`/`S117` animal-experiment SRs):** The entry extracts Module 3 (`文献检索策略`) and `S117`'s search record, **but drifts across the biomedical scope boundary** in its Title (`:2`, "and that China has no standard for one yet"), Observation b3 (`:25-27`), and Inference b1 (`:37-42`, "The Chinese literature does not merely fail to adopt PRISMA-S; it says so"): `S116` (`fd468a36d78ff156b6200946.txt` `char 17393`, 1×) states `由于目前尚无专门针对动物实验 SR 的报告规范，研究者可参考 PRISMA 框架，` — an absence specifically for **animal-experiment SRs**, NOT for Chinese search records generally (and `S119` `char 858` explicitly introduces PRISMA-S in Chinese: `本文旨在对PRISMA-S进行系统性中文解读`). Also Observation b4 (`:28-33`, SinoMed indexing/ordering mechanics) drifts from search-record method into index cataloguing.
- **Generic / overclaimed / ungrounded bullets that must be narrowed:**
  1. **Header `:4`:** cites `表3 报告模块表 module 3 文献检索策略`. In `fd468a36d78ff156b6200946.txt`, `表3` and `报告模块表` occur **0×**; module `3         文献检索策略` (`char 15085`, 1×) is in `表 1 研究方案主体报告框架内容` (`char 14181`, 1×), with items `（1）检索数据库（如 PubMed、Embase 等，含动物实验特殊数据库）` (`char 15115`, 1×), `检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词）` (`char 15235`, 1×), and `（3）灰色文献的检索与记录` (`char 15307`, 1×), plus section `2.4.1   文献检索策略` (`char 22465`, `研究者应至少提供一个主要数据库的完整检索策略` at `char 22926`, 1×).
  2. **Header `:6` & Observation b4 (`:28-33`) & Unknown b2 (`:71-74`):** (a) calls `S119` (`中国循证医学杂志 卷：26 期：4`, `.txt` `char 702`, 1×) a "series" with `S116`/`S117` (`实验动物与比较医学`, column `·比较医学研究与报告规范·`); (b) cites `学科分类号`, which in `42bac8830527d6f1bb125c49.raw` (`byte 8997`) sits inside an HTML comment `<!-- ... -->` and occurs **0×** in `.txt` (and 0× in `.raw` decoded as UTF-16LE); (c) claims SinoMed serves full text "only through a paid ordering service" (`:32-33,72`), which has **0 hits** in `.txt` and `.raw` (`.txt` `char 1354` only says `请登录后再使用此功能， 登录 。`).
  3. **Header `:8` & Observation b2 (`:19-24`):** writes `WebofScience` and `2024-04-01`; `c7266931a1731db3ff6ae77d.txt` has `检索中国知网、万方、中国生物医学文献数据库、` (`char 11211`, 1×), `PubMed、Embase 和 Web of Science 数据库，检索时间` (`char 11299`, 1×), `从各数据库建立至 2024 年 4 月 1 日。检索策略结合主` (`char 11412`, 1×), `题 词 （MeSH/Emtree） 和 关 键 词 。` (`char 11499`, 1×; `2024-04-01` is 0×).
  4. **Header `:9` (`ground:`):** cites `corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md`, which **does not exist in the lane repo** (`ls corpus/knowledge/*search*` → only `search-log-method-r39.md`).
  5. **Inference b1–b4 (`:37-63`):** b1 overgeneralizes `S116`'s animal-SR statement (`INF_UNCITED`, `INF_UNGROUNDED`); b2 makes ungrounded claims about PRISMA-S's 16 items (`INF_UNCITED`, `INF_TOKEN_NOT_IN_SPAN`); b3 (`:55`) cites body-only staged **`S097`** (colliding with lane `S097` = J-STAGE publisher TAB2 in `corpus/SOURCES.md:107`); b4 (`:58-63`) overclaims that `S117` is "a search record a reader can re-run", whereas `S117` (`char 11525`) lists only sample terms ending in `等` without a full Boolean expression.
- **QUALITY criteria failed as staged:** **2 & 30** (`表3 报告模块表`, `2024-04-01`, `学科分类号`, and "paid ordering service" absent from `.txt`), **3** (Observation b4 calls two different journals a "series"), **6 & 77** (unrenumbered `S116`/`S117`/`S119`; body-only `S097`; non-existent lane path in `ground:`), **7 & 8** (animal-SR absence generalized to all China; `S117`'s `等` term list called re-runnable), **13 & 57** (live re-download in `recheck:`), **25 & 59** (register rows `S111`, `S112`, `S114` are `payload-absent` due to spacing, two-column split, and HTML comment — all three re-verified `absent-as-written`), **66** (`inference-ground.py` rc=1: 2 `INF_UNCITED`, 3 `INF_UNGROUNDED`, 1 `INF_TOKEN_NOT_IN_SPAN`).
- **Verdict:** **`admit-with-narrowing`** (fix `表3`→`表 1`, drop `学科分类号`/"paid ordering service"/"journal series", scope the absence strictly to `动物实验 SR`, narrow `S117` from "re-runnable strategy" to "databases, date bound and sample term lists", remove body-only `S097` and nonexistent `chinese-search-log-r37-amendment-2026-10-23.md`, and ground all Inference bullets in `S109`–`S111`).

## 4. Entry 3 — `japanese-search-record-r38-amendment-2026-10-23.md` (`S125` refused-doc, `S126`->`S113`)

- **Province (`PROVINCE.md:5-15`):** **IN** (`search-strategy taxonomy`). Database name, provider (`Ovid など`), search window (`検索期間`, `検索の開始日と終了日`), and post-search record fields (`検索した日，検索キーワードと検索式，検索件数`) are search-strategy method. Zero sibling spillover.
- **Regulatory drift & capture-form blocker on `S125` (`Reporting_Format_Jap_202404.docx`):**
  1. **Regulatory drift:** Observation b1 (`:14-16`, fixing the window end between `分析枠組みが決定された後` and `製造販売業者による分析提出までの一時点`) is HTA manufacturer-submission procedure, not general search method.
  2. **Frozen C2 capture-form blocker (`c2-count.py:117-126`, `build-spans.py:55-66`):** `3a8b45977cd111e45e3980a5.raw` is a Deflate-compressed ZIP (`.docx`). While `word/document.xml` inside `.raw` holds `SRにおける文献検索期間について明記する。` (`plain char 9729`), `文献検索期間2015年1月から2018年10月まで` (`plain char 9893`), and `ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。` (`plain char 10128`), **neither form read by `form_text()` (`.txt` UTF-8 nor `.raw` UTF-16LE) contains `文献`, `検索`, `期間`, or `ハンドサーチ` (all 0×)**! Under the frozen `c2-count.py` (`MIN_BOUND = 5`), **`S125` must be refused as a bound `source:` row** (`refused-doc: https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx` in `corpus/lessons/round-51.md`, giving `BOUND=6/7, REFUSED=1`), while register row `S120` is dispositioned `absent-as-written` (extractor `.docx` ZIP limit, QUALITY 25 & 59) and `S125`'s `word/document.xml` content is noted in `#### Unknown` without an `S###` token.
  3. **`S126` (`34fcefc159bf2ebbd1e09540.txt`) carries `検索期間` (`TERMS[E_JA2]`):** `S126` holds `枠など）や検索の特徴（検索期間，言語制限，未発` (`char 10135`, 1×) and `ロトコルには完全な検索式と言語制限や検索期間な` (`char 11730`, 1×), plus `検索した文献データベース名，Ovid などのプロバ` (`char 11229`, 1×), `イダー名，検索の開始日と終了日を記載することで，` (`char 11289`, 1×), `最新の結果を反映しているかどうか，更新がされて` (`char 11348`, 1×), `検索が終了した後は，検索したデータベース名，` (`char 12105`, 1×), and `検索した日，検索キーワードと検索式，検索件数を` (`char 12179`, 1×).
- **Generic / overclaimed / ungrounded bullets that must be narrowed:**
  1. **Observation b1–b2 (`:12-21`):** remove `S125` as a bound `source:` claim; replace with `S126`'s protocol requirement (`完全な検索式と言語制限や検索期間`, `char 11730`) and post-search record requirement (`検索したデータベース名，検索した日，検索キーワードと検索式，検索件数`, `char 12105-12254`).
  2. **Inference b1–b4 (`:31-59`) & Unknown b1,b3 (`:63-74`):** b1/b2 are generic (`INF_UNCITED`, `INF_UNGROUNDED`); b3 (`:45-53`) quotes ungrounded `'a field, but not in PRISMA'` / `'2020'` and cites body-only `S097`; b4 (`:54-59`) and Unknown b3 (`:72`) cite body-only `S105` and `S106` (colliding with lane `S097`/`S105`/`S106`) and mistranslate Chinese `灰色文献的检索与记录` into Japanese `灰色文献の検索と記録`. Unknown b1 (`:64-65`) narrates an unreceipted live HTTP 000 fetch (`www.lifescience.co.jp`, violating QUALITY 57).
- **QUALITY criteria failed as staged:** **2 & 30** (`S125` quotes absent from `.txt` UTF-8 and `.raw` UTF-16LE), **6 & 77** (unrenumbered `S125`/`S126`; body-only `S097`, `S105`, `S106`), **13 & 57** (`recheck:` live re-download; unreceipted `lifescience.co.jp` HTTP 000 claim), **25 & 59** (register row `S120` is `.docx` ZIP tool-limit, `absent-as-written`), **66** (`inference-ground.py` rc=1: 2 `INF_UNCITED`, 3 `INF_UNGROUNDED`, 2 `INF_TOKEN_NOT_IN_SPAN`).
- **Verdict:** **`admit-with-narrowing`** (refuse `S125` as `refused-doc` due to `.docx` ZIP capture-form incompatibility with `c2-count.py:117-126`, bind `S126` (`S112`/`S113`) which carries `検索期間` at `char 10135`/`11730`, strip body-only `S097`/`S105`/`S106` and unreceipted `lifescience.co.jp` fetch prose, and ground all Inference bullets in `S126`).

VERDICT: Audited all three staged entries and all seven captures against `PROVINCE.md`, `QUALITY.md` (1–80), and `corpus/README.md` — all three are in-province (`search-strategy taxonomy`, zero sibling spillover) and **admit-with-narrowing**: as staged all three fail `inference-ground.py` (rc=1) and QUALITY 2/6/8/13/25/30/57/59/66/77 (body-only IDs `S097`/`S105`/`S106` collide with lane rows, `S116` misnames `表 1` as `表3 报告模块表` and overgeneralizes animal-SR absence to all China, `S119` `学科分类号` is HTML-commented and "paid ordering service" is absent, and `S125` `.docx` has 0 hits in `.txt` UTF-8 / `.raw` UTF-16LE so `S125` must be `refused-doc` while `S126` grounds `検索期間` at char 10135/11730 and all 6 register rows are `absent-as-written`).
