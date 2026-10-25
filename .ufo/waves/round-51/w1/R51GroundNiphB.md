# R51GroundNiphB — second pass on S125 (国立保健医療科学院 submission form, `.docx`)
Capture `3a8b45977cd111e45e3980a5.{txt,raw}` in `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`;
URL `https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx`, `sha256(url)[:24]` = `3a8b45977cd111e45e3980a5`
(verified). Entry target `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`, absent at lane tip
`cfe6c9fb9b56fa80a3005c1a3aaa522b29966306` (`ls corpus/knowledge | grep -i "japan\|search"` prints only `search-log-method-r39.md`;
`grep -rl "検索期間\|検索式\|检索策略" corpus/knowledge` prints nothing). R51GroundNiphA's report was not opened.
## 1. The `.txt` sidecar holds no document text — no S125 quote is locatable in it
```
$ file 3a8b45977cd111e45e3980a5.raw
Microsoft Word 2007+
$ python3 -c "b=open('3a8b45977cd111e45e3980a5.raw','rb').read();t=open('3a8b45977cd111e45e3980a5.txt','rb').read();print(t==b.decode('utf-8',errors='replace').encode())"
True
```
`.raw` 178056 B, sha256 `16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763`, members `word/document.xml`
1464476 B, `word/footer1.xml`, `docProps/*`. `.txt` 319599 B / 168952 chars, 72117 of them U+FFFD (42.7 %); `検索` 0,
`システマティック` 0, `国立保健医療科学院` 0, `<w:t` absent. It is the raw bytes decoded with replacement and re-encoded —
a lossy decode of the ZIP, not a rendering. PDF sidecars in the same cache *are* rendered text
(`34fcefc159bf2ebbd1e09540.txt` opens `60                       剱持・岡／日本保健医療行動科学会雑誌`), so the gap is
OOXML-specific. In both forms the frozen tools know (`build-spans.py:55-65`; `c2-count.py:117-125`) every entry quote
counts 0/0 (`.txt` as UTF-8 / `.raw` as UTF-16LE): `SRにおける文献検索期間について明記する`, `ハンドサーチ等により`,
`使用した検索式`, `使用したデータベース`, and the entry's concatenation `文献検索期間2015年1月から2018年10月まで`. So no S125
span row can be built and `CAPTURE_BOUND` (`c2-count.py:209`, `ft is not None and ft[o:o+len(span)] == span`) cannot hold:
C2's `≥3 quote rows per bound id` leg is **unsatisfiable for this document** while its `source:` leg keeps S125 bound, so
refusing it is no option.
## 2. The document's own identity stamp
| stamp | value | char (form 3) |
|---|---|---|
| title | 医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引 | 9, unique |
| edition | [第2.0版] | 43, unique |
| publisher | 国立保健医療科学院 | 51, unique |
| date | 2024年4月 | 61, unique |
| host, self-cited | `https://c2h.niph.go.jp/tools/system/disclosure_2024.pdf` | 1552, unique |
| chain | 「中央社会保険医療協議会における費用対効果評価の分析ガイドライン第4版」 | 1394, 1417, unique |
`docProps/core.xml`: `dc:title` **empty**; `dc:creator` 国立保健医療科学院 保健医療経済評価研究センター;
`cp:lastModifiedBy` 由美 林; `cp:revision` 6; created 2024-04-11T08:53:00Z, modified 2024-04-11T12:33:00Z.
`docProps/app.xml`: `Company` 厚生労働省, `Words` 3411, `Characters` 19449, but `Pages` **1** — stale (the TOC runs to
p. 35), so `app.xml` page count must not be cited. Filename `…202404.docx` agrees with the cover date; the centre name
(and `C2H`) occurs 0 times in the body — it lives only in metadata.
## 3. Text form used for every offset below (form 3)
`.raw` opened as a ZIP, member `word/document.xml` decoded as UTF-8, runs read in document order with a newline at each
paragraph end. Lossless: `<w:t>` text 18478 chars == form text minus newlines 18478.
```python
import re, zipfile
def docx_form(raw_path):
    x = zipfile.ZipFile(raw_path).read("word/document.xml").decode("utf-8")
    out, buf = [], []
    for m in re.finditer(r"<w:t(?: [^>]*)?>(.*?)</w:t>|</w:p>", x, re.S):
        if m.group(1) is None: out.append("".join(buf)); buf = []
        else: buf.append(m.group(1))
    out.append("".join(buf))
    return "\n".join(out)
```
Form 19716 chars, sha256 (UTF-8) `7b58acbd591f202699a171d4cd14f945add4e3288e4e07f7f1f75d38aa28f787`, source file digest
`16fc8c55…b09763`. Offsets are `form.find(quote)` in this form and no other: not `.txt` (no text), not `document.xml`
offsets — four of the six below also occur once in the raw XML at other indices, and the two 3.1 sentences occur 0 times
there (split across `<w:r>` runs).
## 4. Located quotes (each unique in form 3, byte-exact)
```
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用したデータベース	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	使用した検索式	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	臨床研究の組み入れ基準や除外基準	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	2015年1月から2018年10月まで	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	承認申請に用いたデータは未公表のものでも含めることを推奨する。	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
```
Chars 9348, 9359, 9331, 9413, 8960, 9129. The first four and 9413 sit in **3.2** (body heading char 9151); 8960 and
9129 sit in **3.1** (body heading char 8411, TOC char 661). Max 48 chars, 1 whitespace word; all six differ from the
staged entry's headline three.
## 5. Negative sweeps (exact counts, `.txt` then form 3)
| group | terms | `.txt` | form 3 |
|---|---|---|---|
| searcher | 検索者 / 检索者 / 检索人员 / 検索担当 | 0/0/0/0 | 0/0/0/0 |
| searcher extras | 検索担当者, 検索責任者, 文献検索担当, サーチャー, 担当者, 実施者, レビュアー | all 0 | all 0 |
| grey literature | 灰色文献 / グレーリテラチャー / gray literature / grey literature | 0/0/0/0 | 0/0/0/0 |
| grey extras | グレー, gray, Gray, grey, Grey | all 0 | all 0 |
| hand-search | ハンドサーチ / 手検索 / 手工检索 | 0/0/0 | **1**/0/0 |
| search date | 検索日 / 検索期間 / 检索时间 / 检索日期 | 0/0/0/0 | **0**/**2**/0/0 |
| search date extras | 文献検索期間, 検索終了時点, 検索対象期間, 検索年月, 検索実施日, データベース名, 検索の開始日 | all 0 | **2**, **1**, 0, 0, 0, 0, 0 |
| present | 未公表 / データベース / 検索式 / 文献 / 検索 (total) | — | 2 / 4 / 1 / 11 / 4 |
Absent in the whole package (body plus `word/footer1.xml`, whose only text is `9`): every searcher term above, every
grey-literature term above, 手検索, 手工检索, 検索日, 检索时间, 检索日期, and all simplified script (`检索` 0). Both
`検索期間` hits sit inside 文献検索期間 (char 8942 in the 3.1 sentence, char 9121 as the field label), so bare
`検索期間` is not unique and cannot be a span quote. The one `ハンドサーチ` hit is ハンドサーチ等により at 9368 (3.2).
## 6. Defects in the staged entry, and handoff items
1. **A quoted span that does not exist.** Staged entry line 17 quotes `文献検索期間2015年1月から2018年10月まで`; label
   `文献検索期間` (9121) and value `2015年1月から2018年10月まで` (9129) are separate table cells and the concatenation
   counts 0 in `.txt`, in `.raw`-as-UTF-16LE, in `document.xml` and in form 3. Quote the value alone.
2. **Locator too narrow.** Staged entry line 4 locates the document at `3.1 システマティックレビューのリサーチクエスチョン`
   only, yet three of the required fields I located (databases, search formula, inclusion/exclusion criteria) are in
   **3.2**; the body heading carries no space (2 hits), so the source line's inserted space is drift too.
3. **S125 is understated.** Under PRISMA's principles the form requires 臨床研究の組み入れ基準や除外基準, 使用したデータベース
   and 使用した検索式 (9331/9348/9359) — the search *formula* and the *databases*, not only the window.
4. **The sweep the "neither names the searcher" sentence needs** is §5: seven searcher terms, 0 in form 3 and in `.txt`.
5. **Grey literature: vocabulary absent, requirement present.** 0 for every grey term, but 未公表 2 and the
   ハンドサーチ等により declaration (9368): say *unpublished data by hand-search*, never that the form uses that term.
6. **`decode-form-check.py` (QUALITY 76) has no docx form.** A scratch file naming `char 9348` and "`word/document.xml`
   decoded as UTF-8" prints `FORM_MISSING`, exit 1 (`DECODE_FORM=FAIL`), while the same line naming "the `.txt` read as
   UTF-8" prints `FORM_NAMED`; a lesson carrying form-3 offsets fails until the vocabulary is extended.
7. **Body-only ids in the staged entry** (C2 forbids any `S###` that is not a bound id): `S097` ×1, `S105` ×2, `S106` ×1 in
   body; `S125` ×4, `S126` ×2 including both `source:` lines (planned lane ids S112, S113). Drop or path-describe those four.
## 7. Proposed third form (lane path `corpus/evidence/round51/build-spans.py`; mirror in `c2-count.py:117-125`)
Add after the `.raw` leg of `form_texts`, and the same leg to `form_text` — the counter re-derives, so both must agree:
```python
    # OOXML .docx: the .txt sidecar is a lossy byte decode (round-51 S125); the text form is the
    # paragraph text of word/document.xml, digest = the .raw file's (capture_sha256 unchanged).
    if raw.is_file() and b[:4] == b"PK\x03\x04" and "word/document.xml" in zipfile.ZipFile(raw).namelist():
        out.append((docx_form(raw), hashlib.sha256(b).hexdigest(), raw.name + "!word/document.xml"))
```
with `docx_form` exactly as in §3. S112's spans then slice the 19716-char form, `capture_sha256` stays `16fc8c55…b09763`,
and the `anchor` `char N` values are 9348, 9359, 9331, 8960, 9129, 9413.
## Limits
Offsets index form 3 only. One capture; no network (L0 `8d77e6c1` open), nothing re-fetched. I ran none of
`c1-count.py`/`c2-count.py`/`c3-count.py` (lane rule); the `form_text` behaviour cited is read at `c2-count.py:117-125`,
`:209`. Whether the requirement binds applicants (MHLW programme) or only the institute was not tested. No tool installed,
upgraded or version-changed; no pacman transaction attempted.
VERDICT: attacked the NIPH `.docx` capture's text form and the staged entry's S125 quotes — the `.txt` sidecar holds zero
document text (42.7 % U+FFFD), both frozen span forms locate 0 of 5 entry quotes so C2's span leg cannot bind S125, the
entry's `文献検索期間2015年…` span does not exist, and six new quotes (databases, search formula, window-end rule, worked
example, unpublished-data rule, inclusion/exclusion criteria) plus the empty searcher and grey sweeps are grounded in form 3.
