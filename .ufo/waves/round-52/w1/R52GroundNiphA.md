# R52GroundNiphA — S125 re-grounding (NIPH C2H submission form)

seat: R52GroundNiphA (leaf member; no subagent dispatch). Date 2026-10-26.
scope: staged S125 only — 国立保健医療科学院 C2H 提出様式（日本語）`Reporting_Format_Jap_202404` (`.docx`); sections 3, 3.1, 3.2.
read-only inputs: capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.{raw,txt}`; staged entry `knowledge/corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`; row S125 in `SOURCES.append.md` (package `/home/vgpnk/Projects/shokuknow/merge/chousa`).
No network, no source fetch. No counter run (C1/C2 are not this seat). No lane file written.

## Capture receipt (the only form used)

    python3 tools/capture-text.py …/3a8b45977cd111e45e3980a5.raw > $S/niph.txt
    exit 0 | 19682 characters | 1239 newlines | 48936 bytes UTF-8 | md5 8904efc1780f33dc9149ad8a054056ad
    --locate 'SRにおける文献検索期間について明記する。なお、…' -> LOCATED count=1 offset=8996 (exit 0)
    --locate '2015年1月から2018年10月まで'                    -> LOCATED count=1 offset=9189 (exit 0)
    --locate '文献検索期間2015年1月から2018年10月まで'         -> LOCATED count=0 offset=-1 (exit 1)

The cache `.txt` sidecar (319599 bytes) is the ZIP object stream decoded as UTF-8 (`head -c 160` prints `PK\003\004` followed by U+FFFD runs): **not used**. Offsets below are character offsets in the 19682-char text form (UTF-8 stdout of the tool); each quoted string occurs exactly once there (`str.count` = 1, cross-checked with `--locate` for three of them).

## Form identity

| fact | capture |
|---|---|
| title | `医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引` (off 9) — template **and** guidance (手引) |
| edition | `[第2.0版]` (off 42), immediately under the title |
| issuer | `国立保健医療科学院` (off 51) |
| date | `2024年4月` (off 61); matches the filename `…202404` |
| basis | `中央社会保険医療協議会における費用対効果評価の分析ガイドライン第4版` (off 1446) and `費用対効果評価専門組織で決定された分析枠組みに基づき対象品目を分析すること` (off 1496) — i.e. a national cost-effectiveness-evaluation process template, not a self-standing institutional form |
| self-label | the strings `提出様式`, `C2H`, `Evidence to Decision` do **not** occur in the text form (count 0 each); those are the staged row's/project's labels |

## What the form requires a submitter to state about the SR search

| field | where | capture wording (offset) |
|---|---|---|
| 文献検索期間 | §3.1, body line 531 | must be stated, and its end fixed to one point between the analysis framework being decided and submission by the manufacturer — off 8996 |
| worked example | §3.1 table, lines 552/554 | label `文献検索期間` (off 9181, line 552) and value `2015年1月から2018年10月まで` (off 9189, line 554), **separate table-cell paragraphs**, under `(例)` (line 536) |
| databases | §3.2, line 561 | `使用したデータベース` (off 9408) |
| search expression | §3.2, line 562 | `使用した検索式` (off 9419) |
| inclusion/exclusion criteria | §3.2, line 560 | `臨床研究の組み入れ基準や除外基準` (off 9391) |
| PRISMA reference | §3.2 lead, line 559 | follow the PRISMA statement's principles (`http://www.prisma-statement.org/`) and show the items below clearly — off 9257 |
| grey / unpublished | §3.2, line 564 | hand-searched unpublished data go into the above flowchart; submission-application data are only *recommended* (推奨) for inclusion — off 9428 |
| 検索者 (searcher) | absent | sweeps: `検索者` 0, `サーチャー` 0, `検索担当` 0; `灰色文献` 0. §7 実施体制 (line 1227) asks names/affiliation/role/COI of **analysis** advisers, not searchers |
| date(s) | only one window | `文献検索期間` occurs twice in the whole form (off 9002 requirement, 9181 example label); no per-database or per-strategy date; the only other dates are cover 提出日 and version dates (lines 46, 50–53) |

## §3.1 wording (the section the lane entry cites)

Heading `3.1システマティックレビューのリサーチクエスチョン` at body line 525 (off 8471) — also in the TOC at line 77 (off 682), so it appears twice and is not a legal quote. Body: refer to 分析ガイドライン5章「追加的有用性」；state the RQ explicitly, structured e.g. as PICO, and fill the attached table (line 527); similar technologies may be included in I/C with details (528); the O must be justified, one O in principle, and if several, explain how conflicting results are interpreted (529–530); then the period sentence at 531 (off 8996). The attached example table (lines 533–554) has rows 患者/介入/比較対照/アウトカム/研究デザイン/文献検索期間 with RCT and the 2015–2018 window.

## Numbering defect in the capture (cite by heading text, not number)

TOC (lines 76–84) numbers 3.3 as the RQ for different comparators and 3.8 as the added-value assessment; the body numbers 3.3 as `3.3製造販売業者が実施した検証的試験の一覧と概要` (off 11061, line 661), pushes the different-comparator RQ to 3.4 (line 667) and the assessment to 3.9 (off 12599, line 759), while `0. 要旨` still cites `[3.1/3.3節]` and `[3.2/3.4節]` (lines 149/151). A lane claim that cites "3.3" or "3.8" from the TOC would point at the wrong body section.

## Staged-claim triage (entry `japanese-search-record-r38-amendment-2026-10-23.md`, row S125)

| staged sentence (excerpt) | verdict | ground |
|---|---|---|
| entry `source:` line — "3.1 … — .docx opened and its `word/document.xml` extracted 2026-10-23" | NARROW | section correct (off 8471); method phrase names a fixed member; the frozen form resolves the part from `_rels/.rels` (observed `Target="word/document.xml"`, `zipfile` read of 21 members), i.e. the same part, so content is unaffected but the provenance wording predates the form |
| "A Japanese national institute requires the search window to be stated." | SUPPORTED | off 8996, issuer off 51 |
| "…says "SRにおける文献検索期間について明記する", and fixes the end of that window … to the manufacturer" | SUPPORTED | off 8996, whole sentence binds both halves |
| "Its worked example records the window as "文献検索期間2015年1月から2018年10月まで"" | NARROW | label (9181) and value (9189) are separate paragraphs; `--locate` on the concatenated run = count 0, exit 1; and the table is marked `(例)` |
| "The same form requires unpublished data to be declared." | SUPPORTED | off 9428 (`…収集した場合は、そのことを上記のフローチャートに含める。`); the adjacent 承認申請 clause is 推奨, not a requirement |
| "…that fact must be included in the PRISMA flow chart" | NARROW | 9428 says `上記のフローチャート`; PRISMA is only the §3.2 lead (9257). `フローチャート` also occurs at off 9651 attributed to CONSORT (line 567) |
| "…a national institute's own assessment form requires the search period, and a peer-reviewed Japanese methods journal requires the database, the provider and the window…" | NARROW | period half SUPPORTED (8996); the same form also requires `使用したデータベース` (9408) and `使用した検索式` (9419), which this sentence assigns only to S126 |
| "…why a per-strategy date (PRISMA-S item 13) and a per-database date (the Japanese form) are the same requirement…" | UNSUPPORTED | sweep: `データベース` 4 hits (9412 = the token inside the 9408 item; 10258/10304 RWD quality; 15646 cost), none attaches a date; `文献検索期間` 2 hits = one requirement + one example label |
| "…the search period is required by the institute's form …; the searcher's identity appears in neither." | SUPPORTED (form half) | 8996; absence sweeps `検索者`/`サーチャー`/`検索担当` = 0. Caveat: §7 実施体制 (line 1227) does ask personal names/affiliation/role/COI for analysis help |
| unknown: "The form is the institute's own submission template, so it binds that institute's assessments." | NARROW | capture names the issuer (51) but places the form under the 中医協 guideline v4 (1446) and the 専門組織 framework (1496); neither binding force nor institution-only scope is stated |
| unknown: "Whether … a regulatory obligation or an institutional practice was not established." | SUPPORTED as an unknown | sweep `義務`/`遵守`/`拘束`/`提出することが求め` = 0; no obligation vocabulary in the 1239-line form |
| row S125 cell 2: "提出様式（日本語）… — 国立保健医療科学院 C2H（Evidence to Decision）" | NARROW | issuer (51) and 2024年4月 (61) SUPPORTED; self-title is the 記載様式と手引 (9); `提出様式`/`C2H`/`Evidence to Decision` = 0 |
| row S125 cell 5: "the search-record fields a Japanese national institute's own health-technology-assessment submission form requires…" | NARROW | it is a 費用対効果評価 template under the 中医協 guideline (1446), not self-described as HTA; fields are wider than stated (9408, 9419, 9257) |
| row S125 cell 6: "section 3 追加的有用性, 3.1 システマティックレビューのリサーチクエスチョン; … extracted, read 2026-10-23" | SUPPORTED | `3. 追加的有用性` body off 8294 (line 520), 3.1 off 8471; same method caveat as the entry `source:` line |
| row S125 cell 7 | same verdicts | verbatim repetition of the "requires SRにおける文献検索期間…" and "ハンドサーチ等…PRISMA flow chart" sentences above |

## What the new lane entry may claim

1. It may claim, for §3.1: the search **period** must be stated and its **end** is pinned between framework decision and manufacturer submission (8996) — the staged entry's core claim holds.
2. It may also claim, for §3.2 — and the staged entry does not: **databases** (9408), **search expression** (9419), inclusion/exclusion criteria (9391), under an explicit **PRISMA** reference (9257), plus the hand-search/unpublished-data flowchart clause (9428). That is the depth the document actually offers.
3. It must not claim a per-database date, the concatenated `文献検索期間2015年…` run, or "the PRISMA flow chart" as the form's own label at 564.
4. Identity to state: `記載様式と手引` 第2.0版, 国立保健医療科学院, 2024年4月, applying the 中医協 分析ガイドライン第4版 and the 専門組織 framework — so not "institutional practice" alone; obligation status is unstated.
5. Q12 nuance: the form has **no searcher field** (sweeps 0) but §7 does collect adviser identity/COI — the correct statement is "no searcher field; a separate 実施体制 section names analysis advisers".

## Not checked / out of scope

- S126, the other round-52 documents, C1/C2 counters, `SOURCES.md` registry, QUALITY/PROVINCE: untouched (read-only or other seats).
- Table structure beyond paragraph order (merged cells, page numbers in the TOC) was not rendered; only the text form's line/offset order was used.
- The recheck action (re-download) was not executed: no network.

## Located quotes (machine lines)

```
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	[第2.0版]	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	国立保健医療科学院	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	2024年4月	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	中央社会保険医療協議会における費用対効果評価の分析ガイドライン第4版	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	費用対効果評価専門組織で決定された分析枠組みに基づき対象品目を分析すること	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	SRにおける文献検索期間について明記する。なお、文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	2015年1月から2018年10月まで	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	PRISMA(Preferred Reporting Items for Systematic Reviews and Meta-Analyses)声明(http://www.prisma-statement.org/)の原則に従い、下記の内容については明確に示す。	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	臨床研究の組み入れ基準や除外基準	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用したデータベース	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用した検索式	corpus/knowledge/japanese-search-record-niph-form-r52.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。承認申請に用いたデータは未公表のものでも含めることを推奨する。	corpus/knowledge/japanese-search-record-niph-form-r52.md
```

Offsets in the order above: 9, 42, 51, 61, 1446, 1496, 8996, 9189, 9257, 9391, 9408, 9419, 9428. Lengths ≤ 133 characters, ≤ 8 whitespace words, all exactly once.

VERDICT: re-grounded the NIPH `.docx` in the C1 capture-text form — 13 exactly-once quotes; the period/endpoint claim and the hand-search clause stand, while the concatenated `文献検索期間2015…` run, "per-database date" and the "PRISMA flow chart" label for line 564 do not; the entry may additionally claim §3.2's database, search-expression and PRISMA requirements.
