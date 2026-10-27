# R54 W2 — S123 PDF quote cross-check attacker (`R54W2ExecPdfCross`)

Seat: leaf executor; no dispatch (no spawn tool mounted, **no labrat dispatched**), no tool installs —
`uv run --with pypdf` / `--with pymupdf` fetch into the uv cache, nothing installed system-wide, and
system `pdftotext` already existed. Scratch `/fast/scratch/hyaku/chousa-r54/R54W2ExecPdfCross`
(`TMPDIR` there, `PYTHONDONTWRITEBYTECODE=1`, absolute paths only), removed at exit. No lane file written
but this report; no git/jj mutation anywhere.

## 1. Object under attack — identity
```
lane HEAD 25abbe82b9f2b7c6e24580ac3f028611ba21f01f   (447cf7e + 2 report commits)
97cec0f57deeab5872216a820f3382541d2732273a2faeb2eb08cdf1b52a9ab2  corpus/evidence/round54/pdf-crosscheck.py
53edffa21d57c770fd4eab978fb2c75da49f12e153ce4fff266deb1d985eb3ac  corpus/evidence/round54/quotes.tsv
$ git diff --stat 447cf7e HEAD -- corpus/evidence/round54/{pdf-crosscheck.py,quotes.tsv,spans.tsv}
(empty)   # the check and its input are byte-identical at the integrated tip and at HEAD
```
`quotes.tsv` rows: S121 6, S122 6, S123 21 (33). `spans.tsv` carries the **same multiset** of (id, quote)
pairs (33/33, `sorted(qq)==sorted(ss) True`), so the cross-check reads exactly the quote set the C2 counter reads.

## 2. The frozen-side check re-run (verbatim from the seat item)
```
$ uv run --quiet --with pypdf python corpus/evidence/round54/pdf-crosscheck.py
PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14      # exit 0
```
E4's three numbers reproduce exactly. pypdf wrote 45 `Ignoring wrong pointing object N 0 (offset 0)` lines to
stderr and extracted the document anyway (pypdf 6.21.2, python 3.14.8, pdf 45 pages).

## 3. Third and fourth extractors (raw / NFKC / absent, per quote)
Extractors: `pypdf` (the check's own), **`pymupdf` 1.28.5 `page.get_text()`** (third, independent decoder —
MuPDF, not poppler), **`pdftotext -raw` (poppler 26.08.0)** (fourth). `pdftotext -raw` is a *control*, not an
independent check: the lane's sidecar is `pdftotext -layout` of the same bytes, so it shares engine and
ToUnicode handling. `width`/`real` count the characters that differ inside the matched window (real = the
pair is not NFKC-equivalent).
```
|#|pymupdf|pdftotext -raw|width|real|quote|
|1 |RAW |RAW|0 |0|本文件适用于作者和编制者著录参考文献。
|2 |RAW |RAW|0 |0|本文件不适用于图书馆员、文献目录编制者以及索引编制者
|3 |NFKC|RAW|1 |0|文献类型标识、文献载体标识应按照附录Ａ著录。电子资源
|4 |NFKC|RAW|10|0|电子资源的创建日期、发布日期、修改日期、引用日期应按
|5 |RAW |RAW|0 |0|增加了电子资源载体“缩微资料”及其标识代码
|6 |RAW |RAW|0 |0|将文献类型“普通图书”“舆图”分别更改为“图书”“地
|7 |NFKC|RAW|2 |0|将“ＥＢ”代表的文献类型更改为“网站、网页”
|8 |RAW |RAW|0 |0|图书主要贵任者
|9 |RAW |RAW|0 |0|中国标准出版社出版发行
|10|NFKC|RAW|14|0|２０２５年１２月第１版 ２０２５年１２月第１次印刷
|11|NFKC|RAW|12|0|本文件代替ＧＢ／Ｔ ７７１４—２０１５《信息与文献
|12|NFKC|RAW|10|0|２０２５－１２－０２发布
|13|NFKC|RAW|10|0|２０２６－０７－０１实施
|14|NFKC|RAW|8 |0|ＧＢ／Ｔ ４８９４ 信息与文献 基础和术语
|15|NFKC|RAW|3 |0|附录Ａ（规范性） 文献类型和文献载体标识代码
|16|NFKC|RAW|3 |0|附录Ｂ（资料性）
|17|NFKC|RAW|3 |0|电子资源载体和标识代码应按照表Ａ．２著录。
|18|NFKC|RAW|20|0|缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）
|19|NFKC|RAW|1 |0|图书                          Ｍ
|20|NFKC|RAW|10|0|“／”用于合期的期号或合卷的卷号间（见８．５．１．２
|21|RAW |RAW|0 |0|以数字方式将图、文、声、像等信息存储在磁、光、电介质
```
`pymupdf`: 21/21 present, **0 absent**, 7 RAW + 14 NFKC-only — the identical split pypdf gives, from a
different decoder, so the fullwidth rendering is a property of the PDF's ToUnicode, not of poppler.
`pdftotext -raw`: 21/21 RAW (the control confirms the same engine renders the same widths).

## 4. Is NFKC folding hiding a real difference? **No.**
Every difference consumed by the fold, over all four extractions:
```
$ ... audit.py | awk '/absorbed/{f=1;next} f&&/width-only/'   ->  distinct 33  occurrences 214
U+FF10..FF19 ０-９ -> 0-9   U+FF21..FF5A Ａ Ｂ Ｄ Ｅ Ｇ Ｍ Ｔ Ｙ / ａ ｃ ｅ ｆ ｉ ｌ ｍ ｏ ｒ ｓ ｔ -> A-Z/a-z
U+FF08/09 （） -> ()   U+FF0D － -> -   U+FF0E ． -> .   U+FF0F ／ -> /
every pair: east_asian_width F -> Na, and unicodedata.normalize("NFKC", a) == normalize("NFKC", b)
```
**Zero CJK ideographs and zero CJK punctuation are absorbed** (no `。、，：；《》` pair appears). Aligning the
matched window character by character, the CJK-ideograph subsequence of each quote equals the extractor's
for **21/21 quotes in all four extractions** (`cjk_identical=True`, `real-diffs=0`). So for this document the
fold is exactly a width fold: it turns `附录Ａ` into `附录A` and `２０２５－１２－０２` into `2025-12-02`, and nothing
else. Direction check: rewriting quote 15 halfwidth (`附录A(规范性) …`) still passes and `RAW_NOT_IN` falls
14→13, so the fold is symmetric and a halfwidth quote does not need it.

## 5. Findings
**F1 (medium — the check has no count floor).** `n` counts only rows whose id is in `DOCS`; there is no
assertion that 21 were checked, so a lossy `quotes.tsv` passes:
```
5 of 21 S123 rows  -> PDF_QUOTES=5 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=2   rc=0
0 of 21 S123 rows  -> PDF_QUOTES=0 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=0   rc=0
```
It cannot fail by row loss, an id typo (`S1234`) or a deleted row — only by a *wrong* quote string. Since
QUALITY 96 is not a C2 leg (E4), no claim changes; but `NOT_IN_INDEPENDENT=0` must be read as "every S123 row
that exists matches", not "21 quotes verified". Advisory only (not a rule edit): pin the expected count.

**F2 (informational — the check is substantive, not vacuous).** One CJK character changed
(`本文件`→`本支件`) → `NOT_IN_INDEPENDENT=1`, `rc=1`; the width-only rewrite is §4's direction test. So F1 is a
coverage gap, not a broken check.

**F3 (high — "independent extraction" is decoder-independent but *source*-dependent).** Page 15's text is
render mode **3** (invisible) SimSun over a 1816×1284 jpx scan of a two-page spread; the print reads
`…／／图书主要责任者，图书题名…` while the layer — and therefore **all four** extractors — reads `图书主要贵任者`
(U+8D35 vs U+8D23). Evidence: the scan crop at the layer's char bbox shows 责; the same page's table cell
carries the correct 责任者 (U+8D23); the document holds 责任者 79 times and 贵 1 time. So quote 8 is an
**OCR error in the text layer, faithfully quoted from the span**, and no number of extra extractors can
detect it: they all read the one invisible layer. QUALITY 96's fold therefore proves "not a column-glue /
decoder artefact" only, never "what the page prints". The r37 entry already says exactly this (`… reads
图书主要贵任者 (贵 for 责) … it is an OCR of it` at lines 14-15, and "treats … the occasional wrong glyph as
the reproduction's" at 50-53) — my crop confirms the entry's account; **C2 unaffected, entry correct**.

**F4 (low — adjacency is not stable, quote-level presence is).** Comparing the 25 characters *after* each
quote in the sidecar vs pypdf: 18/21 SAME, 3/21 DIFF — #12/#13 the cover date block (发布/总局/委员会 read in
another order), #19 the appendix-A table (pypdf drops the `J` after 期刊 and reflows the code column). Every
quote itself still matches, but the check compares whole-document text with no page or region constraint, so
a quote long enough to span a cover or table block could "match" from a differently ordered run.

## 6. Not run / limits
- Did not re-run `c2-count.py`, `quote-substance-check.py`, `inference-ground.py` or the C2 legs (other
  seats); this seat attacked the PDF cross-check only. No network, no live fetch; captures read from `.qcache`.
- Read-only lane use: `git rev-parse/log/diff/show` only; nothing written but this report.

VERDICT: attacked the S123 PDF quote cross-check and it **survived on substance** — `PDF_QUOTES=21
NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14` reproduced exactly (exit 0), a third decoder (pymupdf 1.28.5) finds all
21 quotes (7 raw, 14 width-only) and `pdftotext -raw` finds all 21 raw, and the NFKC fold absorbs exactly 33
distinct fullwidth→halfwidth pairs (F→Na, NFKC-identical) with **zero** CJK difference in 21/21 quotes — but
it lost on coverage: no count floor (5 rows and 0 rows both exit 0), and the "independent extraction" is
blind to the one defect actually present — quote 8 `图书主要贵任者` is an OCR-layer error (the printed scan
reads 责任者; the invisible layer reads 贵任者) that all four extractors reproduce, already disclosed in the
r37 entry.

