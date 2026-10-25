# R51GroundNiphA — re-ground staged S125 (NIPH Japanese submission format)

Scope: staged id S125 (`https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx`),
staged entry `.../merge/chousa/knowledge/corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`
(claims at lines 12–21 and 66–71). Planned lane id S112 (registry max confirmed `S106`, 106 rows:
`grep -c -E '^\| S[0-9]{3}' corpus/SOURCES.md` → `106`). No production file written; no network.

## 1. Which form carries the text — the `.txt` does not

```
$ python3 -c "..."
3a8b45977cd111e45e3980a5.raw: Microsoft Word 2007+   178056 bytes
   sha256 16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763
3a8b45977cd111e45e3980a5.txt 319598 bytes / 168952 chars; 72117 U+FFFD; head repr 'PK\x03\x04\x14\x00\x06\x00'
  .txt == raw.decode('utf-8',errors='replace') with CRLF/CR→LF : True
  検索 / システマティック / 文献 in .txt : 0 / 0 / 0
```

**The `.txt` is the `.docx` binary decoded as UTF-8 with `errors='replace'` (newlines normalised), not
extracted text.** It carries zero document text; every Japanese string is absent. The text lives only in
the `.raw`, after unzipping `word/document.xml` (1,379,262 chars, sha256 `5ec29c33d3085fe1…`).
Consequence for C2: an S125 span cannot be sliced from the `.txt`; the span form must be the derived
extraction below, recorded as such in `spans.tsv`.

Form used for every offset and quote (reproducible, 19,885 chars, sha256
`dff1e6a51d8bbeaa099a7b1f9b939581dae285977b999e183ee2dd81b7f01023`; the docx's own `docProps/app.xml`
reports `Characters 19449`, so the length is plausible):

```python
xml = zipfile.ZipFile(RAW).read('word/document.xml').decode('utf-8')
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
body = xml.etree.ElementTree.fromstring(xml).find(W+'body')
txt = '\n'.join(''.join(n.text or '' for n in p.iter(W+'t')) for p in body.iter(W+'p'))  # 1240 paras
```

## 2. Located quotes (form = the 19,885-char extraction above; offset = `txt.find(quote)`)

| # | char | quote | supports | does NOT support |
|---|------|-------|----------|------------------|
| 1 | 8936 | `SRにおける文献検索期間について明記する。` | §3.1 requires the search period to be stated, verbatim, once | says nothing about *how* (format, per-database dates, provider); does not say "PRISMA" |
| 2 | 8960 | `文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。` | the **end** point is fixed to one point (`一時点`) in the interval after the analysis framework is decided and before the manufacturer submits the analysis | constrains only the **end**; no calendar date, no start bound, no rule who chooses the point |
| 3 | 9129 | `2015年1月から2018年10月まで` | the `(例)` RQ table's 文献検索期間 row shows a 2015-01→2018-10 window | not a "worked example" prose; it is a table value, and `文献検索期間` (para 540) is separated from it by a blank paragraph (541) — the staged concatenation does not exist |
| 4 | 9348 | `使用したデータベース` | §3.2 (PRISMA paragraph) requires the databases used to be shown clearly | does not name which databases, nor a per-database date |
| 5 | 9359 | `使用した検索式` | §3.2 requires the search formula used to be shown clearly | does not require the provider name, the full strategy syntax, or limits/filters |
| 6 | 9307 | `の原則に従い、下記の内容については明確に示す。` | the three items that follow (inclusion/exclusion criteria, databases, search formula) are required **by PRISMA's principles** | PRISMA governs items 4/5 and the criteria list only; the flowchart sentence (q7) does not name PRISMA |
| 7 | 9368 | `ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。` | unpublished data collected by hand-search must be included in **上記のフローチャート** | the capture never says *PRISMA* flowchart: `PRISMA` occurs once (9307) and `フローチャート` twice (9368 `上記の`, 9406 `CONSORT声明の推奨するフローチャート`); no flowchart is in the file — the only image is `word/media/image1.png`, 884×409, a chemical structure `C–C2–H` |
| 8 | 9 | `医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引` | the document's own identity: a **reporting format + handbook** for cost-effectiveness analysis of drugs and devices, cover `[第2.0版] / 国立保健医療科学院 / 2024年4月`; `docProps/core.xml` creator `国立保健医療科学院 保健医療経済評価研究センター`, `app.xml` Company `厚生労働省` | not "health-technology assessment" (the word is absent), not a bare "submission form", and not an internal institute assessment template |

Each quote was asserted `txt.count(q)==1` before offsetting. Token census in the same form:
`検索` 4 (3 paragraphs only: 519, 540, 550), `検索者` 0, `担当` 0, `実行者` 0, `氏名` 0, `データベース` 4,
`検索式` 1, `検索期間` 2, `フローチャート` 2, `PRISMA` 1, `国立保健医療科学院` 1.

## 3. Staged claims about this document the capture does not carry

1. **Line 17** — the quoted worked example `"文献検索期間2015年1月から2018年10月まで"` occurs **0 times**
   in the form; `文献検索期間` occurs 2× — at 8942 inside q1 and at 9121 (paragraph 540) — and the window
   value sits at 9129 (paragraph 542), separated by the blank paragraph 541. The staged quote is a
   hand-stitched concatenation presented as one string.
   Fix: quote either `2015年1月から2018年10月まで` (q3) or the two cells separately.
2. **Line 21 and staged row S125** — "the PRISMA flow chart": the capture contains no such string and no
   flowchart. `上記のフローチャート` has no antecedent figure in the document; the only flowchart the file
   names is CONSORT's. The PRISMA link is an inference from the preceding paragraph (q6), not carried.
3. **Lines 68–70** — "The form is the institute's own submission template, so it binds that institute's
   assessments." Not carried, and the capture points the other way: the form is filled by a submitter
   (`【提出者名】`, `【提出日】`), the end-of-window rule names `製造販売業者による分析提出`, and the file's
   Company is `厚生労働省`. It governs manufacturers' submissions to the MHLW cost-effectiveness scheme,
   not NIPH's own assessments.
4. **Line 13** — "submission form for health-technology assessment": the capture says 費用対効果評価
   (cost-effectiveness evaluation) and 記載様式と手引, 第2.0版, 2024年4月. "HTA" and the version are the
   entry's gloss/omission.
5. **Line 4 (source locator)** — `3.1 システマティックレビューのリサーチクエスチョン` with a space; the
   document reads `3.1システマティックレビューのリサーチクエスチョン` (paragraph 513; no space). Filename/
   locator drift of the kind round 50 routed.
6. **Lines 68–69 (Unknown)** — "whether the requirement is a regulatory obligation or an institutional
   practice was not established": consistent with the capture (no 義務/通知 language; the only 推奨する is
   `承認申請に用いたデータは未公表のものでも含めることを推奨する。`, a different item). Not a defect — but
   the entry could record that the form defers the method to `分析ガイドライン5章「追加的有用性」` (para 514).

Depth omission (capture carries it, entry does not use it): the same §3.2 paragraph that the entry cites
for the hand-search clause also requires **使用したデータベース** and **使用した検索式** (q4, q5) — database
and search formula are the two fields the theme is about, and the entry never says this form requires them.

Q12 negative claim (lines 45–48: the searcher is in neither Japanese source) holds **for this document by
absence**: `検索者`/`担当`/`実行者`/`氏名` all 0 in the form. Limit: absence of four tokens, not proof that
no field exists under another name.

## 4. Machine lines

```
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	SRにおける文献検索期間について明記する。	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	2015年1月から2018年10月まで	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用したデータベース	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用した検索式	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	の原則に従い、下記の内容については明確に示す。	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
```

Column 2 is the **staged** id as specified; the lane id per the plan is **S112**. Offsets for these
quotes are in §2 and are offsets in the 19,885-char extraction, not in the `.txt` — the `anchor` cell must
say which form, or C2's `char N` leg will fail on this document.

## 5. Not tested / limits

- Re-download and the 180d recheck (no network; L0 `8d77e6c1` open). The capture mtime is 2026-10-23 20:40.
- Whether the `上記のフローチャート` antecedent exists in the `別添` attachment — not in the capture.
- The other six captures and the Chinese entry are other seats' items.
- No tool installed or upgraded; no pacman transaction run.

VERDICT: attacked staged S125 against its own capture — all 8 located quotes verified verbatim and once-only in the extracted form, while the staged worked-example quote exists nowhere, "PRISMA flow chart" is not in the document (no flowchart, only a chemical-structure PNG), the `.txt` cache form carries no text at all, and the entry's "binds that institute's assessments" is contradicted by 提出者名/製造販売業者/Company=厚生労働省.
