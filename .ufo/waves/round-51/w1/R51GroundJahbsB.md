# R51GroundJahbsB — second pass on staged S126 (日本保健医療行動科学会雑誌 38(1) 2023, step 7)

**Scope.** Independent re-ground of the staged `S126` row and of the `S126` source of `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`: identity stamp, located quotes, four negative sweeps. Read-only; no sibling report read (A-pass is `R51GroundJahbsA`); no lane file written except this report. Lane tip observed: `cfe6c9fb9b56fa80a3005c1a3aaa522b29966306` (base `9ec1751a` is no longer HEAD).

## Capture, text form, revision pin
```
$ wc -c .../34fcefc159bf2ebbd1e09540.txt
47473
$ sha256sum .../34fcefc159bf2ebbd1e09540.txt .../34fcefc159bf2ebbd1e09540.raw .../34fcefc159bf2ebbd1e09540.pdf
065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b  ...txt
fe6eae45a1b0efb6bf0f9c5047cf2e0982410f985cb825d5e8c3cd6f393c67a1  ...raw
fe6eae45a1b0efb6bf0f9c5047cf2e0982410f985cb825d5e8c3cd6f393c67a1  ...pdf
$ pdftotext -layout ...raw layout.txt && python3 -c "...;print(u==t)"
True                    # layout.txt is byte-identical to the capture .txt
$ pdftotext ...raw plain.txt; pdftotext -raw ...raw raw.txt   # chars: plain 17899 | -raw 17235 | capture/layout 25811
$ python3 -c "import hashlib;print(hashlib.sha256('https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf'.encode()).hexdigest()[:24])"
34fcefc159bf2ebbd1e09540
```
- The `.txt` is 25,811 chars read as UTF-8; **all offsets and counts below are in that form**. It reproduces exactly from the `.raw` via `pdftotext -layout`, so the form is poppler's default-layout extraction of this two-column PDF, not a bespoke pipeline.
- The cache key equals `sha256(url)[:24]` of the row's URL, so the capture is bound to that exact URL.

## Identity stamp (the document's own, not the row's)
| element | value | `.txt` offset |
|---|---|---|
| JP title + subtitle | システマティックレビューとメタアナリシスの実施方法 / メタアナリシスの経験を通して | 158, 205 (each once) |
| EN title + authors | How to Conduct Systematic Reviews and Meta-Analysis / 剱持貴史・岡美智代, Takashi Kemmochi, RN, MSN | 477, 595 (each once) |
| edition | running header `60  剱持・岡／日本保健医療行動科学会雑誌 … 38（1），2023  60－69` | 0 (once/page, 10×) |
| date | 2023 in header; no 受付/受理 line (0); PDF `CreationDate: Mon Sep  4 23:34:39 2023` | — |
| **host** | **absent**: `jahbs` 0, `JAHBS` 0, `DOI` 0, `ISSN` 0; the three `https://www` strings are reference URLs (22274, 22579, 22856) | — |

The host `www.jahbs.info` is **capture provenance, not a self-stamp**: it exists in the row's URL and the cache key, nowhere in the text or PDF metadata (Info: `Adobe InDesign 17.4` / `Adobe PDF Library 16.0.7`; the only XMP title belongs to an embedded Illustrator figure, `Microsoft Word - 図表原稿`).

## Negative sweeps — exact counts in the `.txt`
| term | count | term | count | term | count |
|---|---|---|---|---|---|
| 検索者 | **0** | 灰色文献 | **0** | ハンドサーチ | **0** |
| 检索者 | **0** | グレーリテラチャー | **0** | 手検索 | **0** |
| 检索人员 | **0** | gray/Grey/grey literature | **0** | 手工检索 | **0** |
| 検索担当 | **0** | 検索日 | **0** | 検索期間 | **2** (10146, 11739) |
| 检索时间 | **0** | 检索日期 | **0** | 日検索 (inverted) | **6** (21651…25209) |
| 司書 | **5** (step 7 only) | 未発表 | **1** contiguous (18404) | プロバイダー | **0** contiguous |

**Absent**, so a staged "neither names the searcher" claim may carry these: 検索者, 检索者, 检索人员, 検索担当; 灰色文献, グレーリテラチャー, gray/grey literature; ハンドサーチ, 手検索, 手工检索; 検索日, 检索时间, 检索日期. **Present**, needing care: 検索期間 (2), 司書 (5), 日検索 (6).

Form caveats, each measured:
- **Column interleave breaks terms.** `プロバイダー` is 0 contiguous in the `.txt` yet the document says it: `Ovid などのプロバ` at 11243 and `イダー名，` at 11289, split by the left column's text. Per-column crops (x 0–298 / 298–596 pt per page) give `プロバイダー` = **1** whitespace-stripped — a bare 0 is a **false negative**, so absence must be re-run per column.
- Same effect on `未発表`: 1 contiguous (18404), **2** whitespace-stripped per column.
- `検索日` is 0, but the document prints `日検索` **6×**, all `（2023 年３月 28 日検索）` access dates: term-level absence is not date-level absence.
- `司書` 5× all inside step 7 (per-column: step 7 at 8300, step 8 at 10251; 司書 9478, 9552, 9625, 9828, 10070).
- Coverage: `pdfimages -list` shows images only on pp.6–7 (four tiled strips each — 図1 PRISMA flow diagram, 図2 forest plot/RoB2); every page yields body text (plain per page 1765/1536/2228/2113/2124/535/687/2017/2007/2887 chars), so no page is a scan; figure interiors were not OCRed.

## Located quotes (each count = 1 in the `.txt`; offsets in that form)
| off | quote | what it carries |
|---|---|---|
| 11229 | 検索した文献データベース名， | first enumeration opens |
| 11294 | 検索の開始日と終了日を記載することで | the row's 365d recheck string, byte-exact |
| 11348 | 最新の結果を反映しているかどうか | currency rationale opens |
| 12179 | 検索した日，検索キーワードと検索式，検索件数を | **second, fuller** enumeration |
| 12263 | 論文中または付録等で示すこと | where the record must be shown |
| 12330 | 再現性を担保する | **second rationale** (reproducibility) |
| 11739 | 検索式と言語制限や検索期間 | protocol must carry strategy + period |
| 13095 | 情報源（学会抄録，Web サイトなど） | non-database sources must be described |
| 15105 | 誰が行ったか | PRISMA's *who* — for 文献選択 (step 8) |
| 11962 | 専門の司書がいない | search constraint to be declared |

The currency sentence crosses a page break: `最新の結果を反映しているかどうか，更新がされて` (11348) … `\x0c64 <running header>` … `いるかどうかの評価がしやすくなる８）。` (11450), so the full reason is not one contiguous string in this form.
```
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索した文献データベース名，	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索の開始日と終了日を記載することで	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	最新の結果を反映しているかどうか	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索した日，検索キーワードと検索式，検索件数を	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	論文中または付録等で示すこと	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	再現性を担保する	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索式と言語制限や検索期間	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	情報源（学会抄録，Web サイトなど）	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	誰が行ったか	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	専門の司書がいない	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
```

## Findings against the staged row and entry
1. **The recheck string holds.** `検索の開始日と終了日を記載することで` occurs exactly once (11294) at the revision pinned above — the row's `365d` target is still byte-exact.
2. **The row's three fields are right but narrower than the document.** Step 7 gives two enumerations: (a) 検索した文献データベース名 / provider (Ovid など) / 検索の開始日と終了日, reason **currency**; (b) 検索した日 / 検索キーワードと検索式 / 検索件数, shown 論文中または付録等, reason **reproducibility**. Row and entry report only (a) and only currency — the missing rationale is the one the lane's recheck discipline itself runs on.
3. **"Neither names the searcher" survives only field-scoped.** 検索者 / 検索担当 = 0, so no searcher *field* is named; but the document requires `誰が行ったか` for 文献選択 (15105, step 8, PRISMA) and names a 司書 5× as co-planner. "No person is named" would be false; "no field records who ran the search" holds.
4. **The hand-search Inference undercounts its own source.** ハンドサーチ / 手検索 / 手工检索 = 0, yet S126 requires the non-database part of a search to be described (13095) and names 学会抄録 / 臨床試験登録 as routes to unpublished studies (18404) — a **third** Japanese statement of that requirement.
5. **Grey literature: term absent, concept present.** 灰色文献 / グレーリテラチャー / gray literature = 0, while 未発表の資料 occurs twice per column (step 5 eligibility, step 10 publication bias). Term-scope it.
6. **Identity drift (minor).** The document prints `38（1）` full-width; row and entry write `38(1)` — a string-comparing recheck should use the full-width form.

## Draft for the integrator (intended lane path `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`)
```
S126 Observation bullet — replace with:
- **A peer-reviewed Japanese methods journal says what to record and why.** Step 7 検索戦略を立案する
  requires the record to carry the database name searched, the provider name (Ovid など) and the start and
  end dates, giving **currency** as the reason ("最新の結果を反映しているかどうか" … "いるかどうかの評価が
  しやすくなる") (`S126`). The same step then requires a second, fuller record — 検索した日, 検索キーワード
  と検索式, 検索件数, shown 論文中または付録等 — with **reproducibility** as its reason ("再現性を担保する"),
  and requires the protocol to carry the complete 検索式 plus 言語制限 and 検索期間. The step names a 司書
  five times as co-planner; PRISMA's 誰が行ったか is required for 文献選択 (step 8), not for the search.
Q12 Inference sentence — tighten to:
  … the **searcher's identity appears in neither as a field**: `S126` records 検索者 / 検索担当 zero times
  [sweep: 検索者 0, 検索担当 0, 检索者 0, 检索人员 0 in the .txt; 司書 5], while requiring a *who* statement
  for screening (誰が行ったか) and naming a librarian as co-planner.
recheck line — pin the form, not only the string:
  365d — re-download the PDF, extract with `pdftotext -layout`, and confirm the text form is still
  sha256 065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b with "検索の開始日と終了日を
  記載することで" occurring exactly once (ran 2026-10-25).
```

## Limits
Figure interiors (pp.65–66) are raster and not OCRed, so absence claims cover the text layer; the per-column check uses half-page crops, which truncate full-width header text and were used only to test term presence, never for quotes. Out of scope by seat: S125 and the other C2 captures, PRISMA-S's sixteen items, any lane file, counter or entry edit. No tool installed (poppler's `pdftotext`/`pdfinfo` present).

VERDICT: attacked the staged S126 quote set and its Q12 negative — the recheck string holds byte-exact at the pinned revision, but row and entry carry only the document's first of two enumerations and one of its two rationales, and the searcher sweep (検索者/検索担当/检索者/检索人员 = 0) supports the claim only in field-scoped wording, because 誰が行ったか is required for screening and a 司書 is named five times.
