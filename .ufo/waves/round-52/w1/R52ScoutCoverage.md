# R52ScoutCoverage — coverage-map ground check (round 52, wave 1)

Lane HEAD `13bc2806…`; base `00f8c7f5…` (`git diff --stat base HEAD -- corpus/README.md corpus/knowledge` prints nothing, so base = HEAD for those paths). Lane registry max id: `S112` (corpus/SOURCES.md:122; `grep -o '^| S[0-9]*' | sort -n | tail -2` → S111, S112). Planned S113–S116 are free.

## 1. Base sweep (required command)
```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f5272a1d98b6d34913985fa4537e00aaf9 -- corpus/knowledge
→ rc=1, no output
```
Per term, each `git grep -c … <base> -- corpus/knowledge`: 文献検索期間 rc=1; 完全な検索戦略 rc=1; 检索报告清单 rc=1; 条目清单 rc=1; 检索或查询日期 rc=1; PRISMA2020 rc=1 (all empty). Registry: `grep -n -e medsci -e chinagp -e niph -e lifescience -e c2h -e 23e481c0052069d3 -e item185 corpus/SOURCES.md corpus/README.md corpus/knowledge/*.md` hits nothing for any of the four hosts (only unrelated NDL/AVeriTeC lines).
Where each sweep term lives in the on-disk captures (UTF-8 text forms; NIPH via `tools/capture-text.py <.raw>`, rc=0, 19682 chars):
| term | capture | count | first offset |
|---|---|---|---|
| 文献検索期間 | NIPH docx (`3a8b45977cd111e45e3980a5.raw`) | 2 | 9002 |
| 完全な検索戦略 | JPT archive (`e84bfe97808591d23fe3266f.txt`, 5328 chars) | 1 | 766 |
| 检索报告清单 | 梅斯 (`453d492becd9a2f4632cb8dd.txt`, 8804 chars) | 7 | 35 |
So each sweep term is a distinct document's own term and is absent from the base.

## 2. The four documents against the map
The coverage-map rows (corpus/README.md:3-88) carry no search-record/PRISMA row; the theme's rows are the Round-51 table (README.md:1089 `japanese-search-record-r38.md`, :1090 `chinese-search-record-r39.md`, :1091 `japanese-search-record-r38-amendment-2026-10-23.md`) and `## Round51 coverage and frontier` → `### Frontier` (:1095-1109).

**A. NIPH submission form (staged S125, → lane S115) — NEW GROUND, plus one frontier item advanced.**
- Held already: only the *neighbouring* requirement. `japanese-search-record-r38-amendment-2026-10-23.md:13,18,21` (lane S112, JAHBS article) holds 検索期間 as a PRISMA-P search feature and a start/end-date recommendation; it is a society-journal how-to, "not a national standard" (:21). The NIPH form itself is a recorded refusal: README.md:1091 (text: "refused this round because its text exists only in a compressed member"), README.md:1093, README.md:1107 (".docx … opened and refused for its capture form, so what it binds stays unestablished"), corpus/lessons/round-51.md:55,57 (`refused-doc`, flip: counter+span), :89 (round-51 offset `char 39411` = zip-member form; tool-form offset is 9002 — do not mix).
- New: capture text (tool form) 8900-9400 reads `SRにおける文献検索期間について明記する。なお、文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。` — a national institute (国立保健医療科学院, 2024年4月, 第2.0版, offset 0-400) requires the period stated and pins the END of the window to one point between analysis-framework decision and manufacturer submission. The lane's only prior window statement (JAHBS) names start+end dates; this one is a *rule on where the end falls* (new). Adjacent text at 9257-9430: PRISMA 声明の原則に従い → 使用したデータベース / 使用した検索式 / ハンドサーチ等.
- Frontier advanced: README.md:1107 (Japanese national/academic standard — partly: a national institute's reporting format is now opened, its binding scope is tied to 中央社会保険医療協議会 費用対効果評価の分析ガイドライン第4版 (offset 1446) i.e. cost-effectiveness submissions, not SR reporting in general — keep that scope); README.md:1108 hand-searching (ハンドサーチ present, 1 occurrence, but a presence/inclusion note, not a method field).
- NOT advanced: README.md:1105 searcher identity — `検索者`/`誰が` count 0 in the form (counted).

**B. Japanese PRISMA 2020 checklist (staged S129, → lane S116) — frontier item advanced (README.md:1106); wording otherwise held at second hand.**
- README.md:1106 and japanese-search-record-r38-amendment-2026-10-23.md:26 state the translation is unread because the original URL cache is only `f3dbe2fe59a684b1b94cfadc.fail` (6 bytes, verified `ls -l`). The archive copy `e84bfe97808591d23fe3266f.{txt,pdf,raw}` (10106 bytes txt/5328 chars) exists and has no lane row (amendment :26 says so).
- Held at second hand: japanese-search-record-r38.md:14-15 (lane S108) holds the JAOHFA form's items 6 情報源 and 7 検索戦略; `最後に調べ` appears once in the base entries (r38.md). The checklist's own wording is new: 項目6 `それぞれの情報源が最後に調べられた日付を記載する。` (capture, line after offset ~560) and 項目7 `用いたフィルターや制限も含め，すべてのデータベース，試験登録，Web サイトの完全な検索戦略を記載する。` (`完全な検索戦略` at 766, once). Absence confirmed for README.md:1106's side claim: `検索者` count 0 in the capture, so "PRISMA 2020 names no 検索者" now rests on the translation itself.
- Caveat for the drafter [OBSERVED]: the capture text holds no translator/publisher attribution (`翻訳`, `日本語訳` count 0; `訳` 0 in this capture) — the staged row's "official Japanese translation" is not shown by the capture; frame it as JPT ONLINE (ライフサイエンス) 日本語訳 at an archive, not "the official translation", unless the PDF's first page is shown to say so.
- Offsets are archive .txt (pdftotext form), item 7 text is line-broken (a quote must be cut within a line).

**C. 梅斯医学 page (staged S111, → lane S113) — thin new ground; frontier item NOT advanced.**
- Held already: chinese-search-record-r39.md:5,18,26,28,32 (lane S111 = SinoMed record `https://www.sinomed.ac.cn/article.do?ui=2026335073`): bibliographic fields, abstract *truncated* after `并针对中文` (char 1024, :18), `16个条目`, item text unread (:28, :32). README.md:1090 holds it; README.md:1109 says item text "remains order-only from SinoMed and the portal".
- The portal page adds: the *untruncated* abstract (…`并针对中文数据库等本土化应用挑战提出实践建议。本文旨在为国内学者、期刊编辑及审稿人提供清晰、实用的PRISMA-S应用指引…`, from 简要介绍 at ≈2434), 发布日期 2026-04-25, source 中国循证医学杂志, 发布机构 field empty, and the attachment filename `…PRISMA-S）解读_郑卿勇.pdf` (offset 2737; 5 occurrences in .raw, **0 `.pdf` URLs** in the .raw — the PDF itself is not captured). Author 郑卿勇 (offset 2740).
- No item-by-item text: `PDF`/`附件` count 0 in .txt; `条目` 2 (both in the abstract). So README.md:1109 stays open — do not claim it advanced. It is the second route to one article, not a new reading of the items.

**D. 中国全科医学 PRISMA 2020 checklist page (staged S112, → lane S114) — NEW GROUND (Chinese side of the PRISMA 2020 items).**
- Held already: nothing — `PRISMA2020`, `检索或查询日期`, `条目清单` rc=1 at base; chinese-search-record-r39.md holds a Chinese animal-experiment reporting copy and a PRISMA-S index record, not PRISMA 2020 itself.
- New (txt, whitespace-normalised read; raw .txt is space-fragmented, e.g. `检索策略 7 呈现 所有数据库、注册平台和网站的 完整 检索策略` — a located quote must be chosen so it is contiguous in the raw .txt): 条目6 `详细说明获取文献的所有来源 … 明确说明每一项来源 的 检索或查询日期` (`检索或查询日期` once, offset 1719); 条目7 `完整 检索策略，包括 用到的 过滤器和限制条件`; 发布日期：2023-01-31 (normalised offset 2775). Page is a journal's own published checklist (not a national standard); `检索者`/`检索人`/`国家标准` count 0.
- Frontier: advances nothing named in README.md:1105-1109 on the Chinese side except corroborating README.md:1105 (no searcher field in the Chinese PRISMA 2020 items); does NOT advance :1107 (a journal page is not a national standard).

## 3. Verdict table
| doc | lane id | status |
|---|---|---|
| NIPH form | S115 | new ground (search-end-point rule) + frontier :1107 partly, scope = cost-effectiveness submissions |
| JPT checklist | S116 | frontier :1106 advanced; items 6/7 first-hand wording new; "official" unproved by capture |
| 梅斯 | S113 | duplicate route of lane S111's article; adds untruncated abstract/date/attachment name only; :1109 still open |
| 全科医学 | S114 | new ground (Chinese PRISMA 2020 items 6/7 incl. per-source date) |
Staged ids carried by the same numbers in the lane are other rows (lane S111 = SinoMed, S112 = JAHBS) — S111→S113, S112→S114, S125→S115, S129→S116 as planned.

Tools installed/updated: none. Scratch `/fast/scratch/hyaku/chousa-r52/R52ScoutCoverage` removed.

VERDICT: attacked the four documents against README.md coverage/frontier — base sweep rc=1 (no output); new ground = NIPH search-end-point rule and Chinese PRISMA 2020 items 6/7; JPT advances README.md:1106 (but "official" is not shown by the capture); 梅斯 is a second route to lane S111's article and leaves README.md:1109 open.
