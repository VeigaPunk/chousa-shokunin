# R52GroundNiphB — staged S125, independent second pass (国立保健医療科学院 提出様式, `.docx`)

freshness: the newest capture this seat may read is the NIPH `.docx`, cached 2026-10-23 (`.qcache/3a8b45977cd111e45e3980a5.raw`, mtime `2026-10-23 20:40:30 -0300`, 178,056 bytes); L0 `8d77e6c1` open — no fetch, no re-open of the URL, so freshness cannot move this round.
revisions: lane tip `13bc28063b4bd7ea2e521167413ee9829202a420`; `tools/capture-text.py` blob `07401e12f0e953e7b62aa054b14f663c5d31e389`, identical to its candidate commit `804a4537…`, sha256 `3986a971…`; `corpus/evidence/round52/build-spans.py` sha256 `1732615412cf…`; `git status --porcelain` on both paths prints nothing; python3 3.14.8; nothing installed (none needed).
form of every offset below: the `.raw` decoded by `python3 tools/capture-text.py <raw>` — **19,682 code points** — never the `.txt` sidecar. I read no seat report, ran neither counter, and wrote only this file.

## 1. Operability on this capture

```
$ python3 tools/capture-text.py $RAW > niph.txt ; echo exit=$?    # exit=0
$ wc -c -m niph.txt                                               # 48936 19682  (bytes, code points)
$ md5sum niph.txt ; sha256sum $RAW                                # 8904efc1780f33dc9149ad8a054056ad / 16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763
$ python3 -c "…build-spans.docx_text(raw)…"                       # builder chars 19682 tool chars 19682 equal True
$ python3 tools/capture-text.py $RAW --locate 検索者                # LOCATED count=0 offset=-1  exit=1
$ python3 tools/capture-text.py $RAW --locate <the 15 quotes below>   # LOCATED count=1 offset=<n>  exit=0, all 15
```
The two independent readers agree exactly on this capture, so C2's `.raw` form is not a second rule. The `.txt` sidecar is unusable, confirmed here: 168,952 chars, **72,117 U+FFFD**, 0 hits each for `文献検索期間`, `SRにおける文献検索期間について明記する`, `使用した検索式`; `form_texts` therefore picks the `.raw` form (form 0 `.txt` 168,952 chars/0 term hits; form 1 `.raw` 19,682/2). Package: 21 members, `_rels/.rels` names `word/document.xml` as officeDocument — no fixed member name. `word/header1.xml` has no `w:t`; `word/footer1.xml` has one `w:t` `9` and instrText `PAGE \* MERGEFORMAT`, both outside the main part by rule. `docProps/app.xml` `Characters` 19449, `Words` 3411 against 19,682 code points (+233) — a crude corroboration that no bulk text is lost, not a claim about Word's counting (`Pages` reads 1).

## 2. The document's own identity stamp

| element | where | value |
|---|---|---|
| title | char 9 | 医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引 |
| edition | char 43 | `[第2.0版]`, once; template slots `【製品名】…[第X版]` at 121-297 |
| host / author | char 51 | 国立保健医療科学院 |
| date | char 61 | 2024年4月 |
| package metadata (not the text form) | `docProps/core.xml` | `dc:creator` 国立保健医療科学院 保健医療経済評価研究センター · `lastModifiedBy` 由美 林 · `revision` 6 · created/modified `2024-04-11T08:53Z`/`12:33Z`, agreeing with the cover month · `app.xml` `Company` 厚生労働省 |

`C2H` occurs **0** times in the text form, `Evidence` **0**; the host string `c2h` occurs once (char 1612) and only inside another document's URL (`https://c2h.niph.go.jp/tools/system/disclosure_2024.pdf`). The staged row's gloss `国立保健医療科学院 C2H（Evidence to Decision）` is therefore not the document's stamp: C2H lives in the URL host and in `core.xml`'s creator (`保健医療経済評価研究センター`), never in the form.

## 3. Located quotes (machine lines)

id cell = planned lane id **S115** for staged S125 (lane registry max at base is S112; the staged id is not carried over). Form: `.raw` through `capture-text.py`, 19,682 chars; offsets = `--locate` (exit 0, count=1) in block order 9 · 51 · 61 · 1782 · 9020 · 9189 · 9391 · 9419 · 9428 · 9934 · 11061 · 11353 · 11552 · 19496 · 19521; lengths 7-51 chars, ≤3 whitespace words, no tabs.

```
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	国立保健医療科学院	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	2024年4月	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	説明や手引き部分(斜体部分)は削除して使用すること。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	2015年1月から2018年10月まで	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	臨床研究の組み入れ基準や除外基準	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用した検索式	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	SRで同定され、追加的有用性の評価に採用する論文はrisk of biasの評価を行うことが望ましい。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	3.3製造販売業者が実施した検証的試験の一覧と概要	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	3.4 システマティックレビューのリサーチクエスチョン(異なる比較対照あるいは単群試験)	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	3.3節で定義されたRQに基づき、3.2節と同様にSRを実施する。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	その名前と所属、役割、利益相反等を記載すること。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S115	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	上記の協力を受けた研究者の個人名や所属については原則として公開しない。	corpus/knowledge/japanese-search-record-niph-form-r52.md
```
The thin rows (`2024年4月`, `使用した検索式`, `国立保健医療科学院`) are field labels; substance rests on the long ones (QUALITY 72's ≥12-char floor met several times).

## 4. Negative sweeps — exact counts in the stated form

Sweep `python3 -c "t=open('niph.txt',encoding='utf-8').read();print(t.count(w))"` per term over the 19,682-char form; absent terms re-checked through the tool, which prints `LOCATED count=0 offset=-1` exit 1, so sweep and locator agree.
- searcher identity — **absent**: `検索者` 0 · `検索担当` 0 · `检索者` 0 · `检索人员` 0 · (also `担当` 0, `氏名` 0, `連絡先` 0, `作成者` 0)
- search date — `検索日` 0 · `文献検索期間` 2 (char 9002, 9181) · `検索期間` 2 (char 9004, 9183, both inside `文献検索期間`, so no bare 検索期間) · `文献検索終了時点` 1 (char 9020) · `检索日期` 0 · `检索时间` 0
- strategy — `検索式` 1 (char 9423, the tail of `使用した検索式` at 9419) · **`検索戦略` 0 · `检索策略` 0 · `检索式` 0**
- grey literature — **`灰色文献` 0 · `グレーリテラチャー` 0**; nearest rule `ハンドサーチ` 1 (char 9428)
- PRISMA — **`PRISMA-S` 0** · `PRISMA` 1 (char 9257, the `prisma-statement.org` citation) · `PRISMA 2020` 0 · `2020` 0 · `チェックリスト` 0

So the entry may write: no searcher field in any of the four spellings; no exact search date (a period plus an end-point rule, no bare 検索期間); no strategy label other than the single `使用した検索式`; no grey-literature term; no PRISMA-S and no PRISMA edition.

## 5. Findings

**F1 — the guidance the theme quotes is the italic, deletable layer.** char 1782 tells the applicant to drop `表紙部分`/`本様式の1ページ目` and `説明や手引き部分(斜体部分)`. At the XML level in `word/document.xml` the three search-record paragraphs are wholly italic — p#519 (5/5 runs, the 文献検索期間 sentence), p#547 (7/7, the PRISMA three-item sentence), p#552 (5/5, the handsearch sentence), and the `使用した検索式` bullet p#550 (1/1) — while the example-table label `文献検索期間` p#540 is not (0/1); 1,240 paragraphs total. So the entry must say *the template's guidance requires …*, never *a submitted form contains …*: a submission under this template deletes both stamp and sentences.

**F2 — the form's numbering is stale and one in-body cross-reference is off.** TOC (chars 660-860): 3.1 RQ p18, 3.2 結果 p19, 3.3 RQ(異なる比較対照…) p21, 3.4 結果(異なる…) p21, 3.5 既存データの再解析 p21. Body: 3.3 is `3.3製造販売業者が実施した検証的試験の一覧と概要` (11061) — absent from the TOC — then 3.4 RQ variant (11353), 3.5 結果 variant, 3.6 既存データ (11613); body 3.5 says `3.3節で定義されたRQに基づき` (11552), pointing at the 検証的試験 section rather than the RQ one (body 3.4 / TOC 3.3). The template's own `目次は最後に更新すること` explains the stale TOC, not the wrong in-body reference. Cite sections by title or char offset, never by number.

**F3 — searcher identity is absent for a reason, not from terseness.** §7 実施体制 (19496) requires `名前と所属、役割、利益相反` for the experts engaged, and 19521 says those personal names and affiliations are as a rule **not published**; the only other person field is the submitter's `【提出者名】` (125) / `【提出日】` (132). The form has person-identity machinery and still names nobody who ran the search.

**F4 — date: a window with a fixed end point, no search date.** 9020 fixes the end of the window between the framework decision and the analysis submission; the worked example carries only a range (9189); `検索日` 0.
**F5 — strategy: one field inside a three-item PRISMA list, no edition.** 3.2, following PRISMA's principles, requires 組み入れ/除外基準 (9391), 使用したデータベース (9412), 使用した検索式 (9419) to be shown clearly; PRISMA is named once with a bare URL (9257), no edition, no checklist, `PRISMA-S` 0.
**F6 — unpublished material is a flowchart note, not a source field.** The only grey-adjacent rule is 9428 (handsearch-collected unpublished data marked in the flow chart) plus the following recommendation to include unpublished data used in the application.
**F7 — RoB is desirable, not required.** 9934 ends `…行うことが望ましい。`, weaker than the `記載する` used for the search fields; do not report it as a requirement.

## 6. The staged row cannot be the C2 binding row (routed for the L1)

`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md:50` (S125) anchors with `.docx opened and its word/document.xml extracted, read 2026-10-23` — the fixed-member form round 51 refused — and carries **no `char N`**, so C2's "every `char N` in a bound row's `anchor` cell (at least one)" has nothing to read; `opened`/`mined` are `2026-10-23` where the frozen predicate requires `opened 2026-10-26`; its `used-by` names `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`, which at BASE_REV cites only `source: S112 — https://www.jahbs.info/…` and holds no c2h URL (`git grep -n 'c2h.niph.go.jp' 00f8c7f5… -- corpus/SOURCES.md corpus/knowledge` prints nothing). Build the lane row new (planned S115) with the opening date, used-by = the r52 entry, and anchors from §3's offsets.
Second: that entry's Unknown says the form's text "exists only inside a compressed `word/document.xml` member that the round's span pipeline cannot read from either capture form" — now false, `docx_text` returns the same 19,682 characters as the tool, so the round-52 lesson needs the flip (L0 open: this proves the cached copy readable, not the host still serving it). I did not touch that BASE_REV file.
Base-REV premise for C2's new-ground leg re-checked: `git grep -c <term> 00f8c7f5… -- corpus/knowledge | wc -l` prints `0` for each of `文献検索期間`, `完全な検索戦略`, `检索报告清单`; registry maximum there is S112.

## 7. Limits

- The text form is main-part only; header/footer parts are excluded by rule. Nothing is lost here (header has no `w:t`, footer only a PAGE field), but a footer-stamped identity elsewhere would be.
- Italic/`w:i` and `core.xml`/`app.xml` are XML-level observations about the package, **not** the text form; they carry no quote lines.
- No fetch: stamp and quotes describe the cached 2026-10-23 copy. Whether c2h.niph.go.jp still serves this file, or the same bytes, is unverified and unclaimed.
- 19,449 (`app.xml`) vs 19,682 code points is a counting-rule difference, not a measured loss.
- Absence claims cover this one file's main part; they say nothing about the 分析ガイドライン the form points to 11 times, which is not a lane capture this round.

VERDICT: attacked staged S125's ground independently — identity stamp (第2.0版 / 国立保健医療科学院 / 2024年4月, "C2H"/"Evidence" absent from the form), 15 exactly-once quotes at tool-agreed offsets, and counted negative sweeps in the `.raw`-through-`capture-text.py` form (searcher identity 0 in four spellings, 検索日 0, 検索戦略 0, 灰色文献 0, PRISMA-S 0) — and the staged S125 row fails the frozen C2 binding legs (no `char`, fixed member name, opened 2026-10-23, used-by an entry that never cited the URL) and must be rebuilt as S115.
