# R52ExecNegSweep — negative-claim sweep over the four search-record documents

seat: `R52ExecNegSweep` (leaf) · date 2026-10-26 · axes: operability, depth
lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin` tip `13bc280` (claims frozen at `37468ea`, base `00f8c7f5`)
scope: exact `str.count`/`str.find` sweep of the 23 assigned terms over four capture text forms,
then adjudication of the staged negative claims of `r40` / `r37` / `r38`. No file in the lane,
`shokuknow` or the fleet repo was written; this report is my only write.

## 1. The four forms measured — a zero is a zero **in that form**

| doc | capture | form read | chars | sha256 of the file |
|---|---|---|---|---|
| medsci | `.qcache/453d492becd9a2f4632cb8dd.txt` | HTML page text, `.txt` read as UTF-8 | 8804 | `ad6b09f0…571cdc52` |
| chinagp | `.qcache/cacddf3bbf780a4c7582bb17.txt` | HTML page text, `.txt` read as UTF-8 | 6179 | `b1c3cd6a…3abe24f0` |
| archive | `.qcache/e84bfe97808591d23fe3266f.txt` | PDF 1.6 extraction, `.txt` read as UTF-8 | 5328 | `93558b6d…30ab155` |
| NIPH | `.qcache/3a8b45977cd111e45e3980a5.raw` | round-52 `.docx` form, `capture-text.py` stdout | 19682 | `16fc8c55…deb09763` |

Reading rule, stated because offsets depend on it: `.txt` = `Path.read_text(encoding="utf-8",
errors="replace")` — the rule `form_texts` uses at `corpus/evidence/round52/build-spans.py:115-121`.
That form applies **universal newlines**, and `cacddf…txt` carries 1406 CRLF pairs, so it is 6179
chars here but 7585 characters if the bytes are decoded without newline translation; every chinagp
offset below is the lane form's (raw-byte decode would shift it by up to 1406, e.g. `PRISMA 2020`
sits at 5616 lane / 6941 byte-decode). NIPH's `.txt` sidecar is **not** a text form (it is the zip
read as UTF-8: 72117 U+FFFD, `PK\x03\x04` head); the `.raw` through `capture-text.py` is.

## 2. The sweep — `n@first offset` (`-1` = absent), exact `str.count`/`str.find`

| term | medsci | chinagp | archive | NIPH |
|---|---|---|---|---|
| 検索者 | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| 検索担当 | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| 誰が | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| 检索者 | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| 检索人员 | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| 検索日 | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| 検索期間 | 0@-1 | 0@-1 | 0@-1 | 2@9004 |
| 文献検索期間 | 0@-1 | 0@-1 | 0@-1 | 2@9002 |
| 最終検索日 | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| 检索日期 | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| 检索时间 | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| 最后检索 | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| 検索式 | 0@-1 | 0@-1 | 0@-1 | 1@9423 |
| 検索戦略 | 0@-1 | 0@-1 | 2@619 | 0@-1 |
| 完全な検索戦略 | 0@-1 | 0@-1 | 1@766 | 0@-1 |
| 检索策略 | 0@-1 | 2@1756 | 0@-1 | 0@-1 |
| 检索报告清单 | 7@35 | 0@-1 | 0@-1 | 0@-1 |
| 灰色文献 | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| PRISMA-S | 15@42 | 0@-1 | 0@-1 | 0@-1 |
| PRISMA 2020 | 4@2360 | 1@5616 | 2@0 | 0@-1 |
| 16个条目 | 2@2389 | 0@-1 | 0@-1 | 0@-1 |
| 付费 | 0@-1 | 0@-1 | 0@-1 | 0@-1 |
| 下载 | 6@1368 | 0@-1 | 0@-1 | 0@-1 |

Reading notes that the counts alone hide:

- **Twelve terms are zero in all four forms** (48 zero cells): the five searcher-identity terms,
  the five fixed date terms, 灰色文献 and 付费. Per-document non-zero hits: medsci 34, chinagp 3,
  archive 5, NIPH 5.
- **Nesting inflates three rows.** NIPH `検索期間`'s 2 hits (*9004, 9183*) are both inside
  `文献検索期間` (*9002, 9181*); archive `検索戦略`'s second hit (*769*) is inside
  `完全な検索戦略` (*766*). Real distinct occurrences are 2 NIPH / 1 archive.
- **A zero is a wording fact where a field exists.** archive has `最終検索日` 0 but expresses the
  field as `それぞれの情報源が最後に調べられた日付を記載する。` 1@592; chinagp has `检索日期` 0 but
  `检索或查询日期` 1@1719. Neither zero may be quoted as "the field is not required".
- **検索者 is absent from the form that adds fields, too.** NIPH asks for the window, `使用した
  データベース` (*9408*) and `使用した検索式` (*9419*) and has no searcher term — the absence is not
  an artefact of PRISMA's item wording.
- **`下载` 6@1368, `付费` 0** on medsci: the portal does expose a download path, and its page text
  carries no paywall marker — consistent with the staged `r37` `Unknown` that the S111 attachment
  sits behind the portal's download mechanism, and it does not settle whether the PDF is reachable.

## 3. Why a zero in these forms is trustworthy (and where it is not)

- **Each form holds the whole document.** archive: number column complete — 1…27 including
  `10a,10b,13a–13f,16a,16b,20a–20d,23a–23d,24a–24c` (42 tokens), single `\f` at 5327 (last char,
  so no term straddles it); NIPH: 19682 chars, cover page `国立保健医療科学院 / 2024年4月` → item
  3.2; medsci/chinagp: page text down to the site footer.
- **Split-token control, run for all 23 terms in all 4 forms:** `re.compile(r"\s*".join(escaped))`
  vs literal `count` — **0 mismatches**, so no zero is a line-wrap artefact.
- **Named limit, measured:** the same tolerant scan is defeated by two-column interleaving. In the
  S126 jahbs capture (`34fcefc159bf2ebbd1e09540.txt`), `プロバイダー` is split *across* the other
  column (`Ovid などのプロバ\nされるため，世界中の… イダー名`) and matches neither literally (0) nor
  tolerantly (0). The four assigned forms are single-column/sequential (archive wraps only by
  indentation), which is why their zeros survive; a two-column PDF's zeros would not.
- **`build-spans` first-form hazard, tested, does not bite here.** `form_texts` tries the `.txt`
  before the `.raw`, and for NIPH that `.txt` is zip bytes; the four NIPH quotes I test below score
  0 in the sidecar, so the builder falls through to `docx_text`. `bs.docx_text(niph.raw)` is
  byte-identical to `capture-text.py` stdout: **19682 chars, sha256 `754aae42…2f24b0d9`, equal
  True** — the two readers agree on the form C2 will slice.

## 4. Which staged negative claims reproduce

| staged claim | verdict | evidence in these forms |
|---|---|---|
| `japanese-prisma-item-wording-r40.md` title: *PRISMA 2020's own Japanese wording names no searcher* | **REPRODUCES** | `検索者` 0, `検索担当` 0, `誰が` 0 in the 27-item translation (tolerant 0); `完全な検索戦略を記載する。` 1@766 and `情報源` 2@453 confirm the entry reads item 6/7 right. It also closes `r38`'s *Unknown* ("the official Japanese translation remains unread") from the archive copy |
| `chinese-search-log-r37-amendment-2026-10-23.md`: *the Chinese answer is a reception, not a standard* | **REPRODUCES for these two documents; the national-standard half is not probed** | medsci is an interpretation (page title marker `解读` 14@51, `PRISMA-S` 15@42, `为文献检索报告提供了包含16个条目的专项规范` 2@2377, `作为“报告规范”的内在局限` 1@2463); chinagp is one journal's translation (`PRISMA 2020` 1@5616, `Page` 1@5536, `n71` 2@5707, `2023-01-31` 1@5749); neither carries a standard designation (`国标` 0, `GB/T` 0) and neither names a searcher (`检索者` 0, `检索人员` 0). Two captures cannot exclude an unseen Chinese standard — state the claim as "these two documents are a reception" |
| `japanese-search-record-r38-amendment-2026-10-23.md`, NIPH half — the form requires the search period | **REPRODUCES** | `SRにおける文献検索期間について明記する` 1@8996 (`--locate` agrees: `LOCATED count=1 offset=8996`, exit 0) |
| …the window end is one point before manufacturer submission | **REPRODUCES** | `文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める` 1@9020 |
| …the worked example records `文献検索期間2015年1月から2018年10月まで` | **SUBSTANCE REPRODUCES, QUOTED STRING DOES NOT** | the string is **0** in the form (`--locate` → `count=0 offset=-1`, exit 1). The form is a table row: `文献検索期間` *9181*, `\n\n`, `2015年1月から2018年10月まで` *9189*. The rendered-table concatenation in the entry is not the capture's string |
| …unpublished data by hand-search must be declared | **REPRODUCES** | `ハンドサーチ等により` 1@9428; `ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める` 1@9428 |
| …the searcher's identity is in neither Japanese source | **REPRODUCES for NIPH** | `検索者` 0, `検索担当` 0, `誰が` 0, `作成者` 0, `担当` 0 in NIPH |

## 5. Routed defects: prose quotes that will not locate against the round-52 forms

Measured, not inferred — each is `count == 0` while the pieces are `count == 1`:

1. **`r38` NIPH worked example** `文献検索期間2015年1月から2018年10月まで` — 0; use
   `2015年1月から2018年10月まで` 1@9189, or record the `\n\n` form `文献検索期間\n\n2015年1月から
   2018年10月まで` 1@9181. If carried into `quotes.tsv`, this row is refused (`quote not exactly
   once in any form`) and C2's quote leg cannot reach n/n.
2. **`r40` item-7 sentence** `用いたフィルターや制限も含め，すべてのデータベース，試験登録，Web
   サイトの完全な検索戦略を記載する` — 0 (the cell wraps with newline + column indentation); use
   `完全な検索戦略を記載する。` 1@766.
3. **`r37` per-source date sentence** `明确说明每一项来源的检索或查询日期` — 0 (the page inserts
   spaces: `明确说明每一项来源 的 检索或查询日期`); use `检索或查询日期` 1@1719 or
   `明确说明每一项来源` 1@1707.
4. **`r40`/`r37` 16-item sentence on medsci** — `为文献检索报告提供了包含16个条目的专项规范` is
   **2** (introduction and abstract blocks), so it cannot be a once-only quote; the `r37` entry's
   paraphrase is fine but a span row needs another cut.

Candidate quotes, byte-exact and once-only, for whoever builds `quotes.tsv` (form named per offset):

```
QUOTE	archive e84bfe…txt (UTF-8 .txt)	off 766	完全な検索戦略を記載する。
QUOTE	archive e84bfe…txt (UTF-8 .txt)	off 592	それぞれの情報源が最後に調べられた日付を記載する。
QUOTE	archive e84bfe…txt (UTF-8 .txt)	off 475	すべてのデータベース，研究登録，Web サイト，組織，文献リスト
QUOTE	chinagp cacddf…txt (UTF-8 .txt)	off 1719	检索或查询日期
QUOTE	chinagp cacddf…txt (UTF-8 .txt)	off 1707	明确说明每一项来源
QUOTE	medsci 453d49…txt (UTF-8 .txt)	off 2463	作为“报告规范”的内在局限
QUOTE	NIPH 3a8b45….raw (docx text form)	off 8996	SRにおける文献検索期間について明記する
QUOTE	NIPH 3a8b45….raw (docx text form)	off 9020	文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める
QUOTE	NIPH 3a8b45….raw (docx text form)	off 9189	2015年1月から2018年10月まで
QUOTE	NIPH 3a8b45….raw (docx text form)	off 9428	ハンドサーチ等により
```

All ten are ≤25 whitespace words and ≤160 chars (longest: 47 chars; the widest is 2 whitespace words).

## 6. Operability probe on the C1 tool, from real captures (not fixtures)

`tools/capture-text.py` at `804a453` run read-only against the three non-OOXML raws:

```
$ python3 tools/capture-text.py .qcache/453d492becd9a2f4632cb8dd.raw  # HTML
exit=2 stdout_bytes=0 stderr=REFUSED not a zip (an OOXML capture is a zip package)
$ … /cacddf3bbf780a4c7582bb17.raw  # HTML
exit=2 stdout_bytes=0 stderr=REFUSED not a zip (an OOXML capture is a zip package)
$ … /e84bfe97808591d23fe3266f.raw  # PDF
exit=2 stdout_bytes=0 stderr=REFUSED not a zip (an OOXML capture is a zip package)
$ … /3a8b45977cd111e45e3980a5.raw --locate 'SRにおける文献検索期間について明記する'
LOCATED count=1 offset=8996          # exit 0
$ … /3a8b45977cd111e45e3980a5.raw --locate '文献検索期間2015年1月から2018年10月まで'
LOCATED count=0 offset=-1            # exit 1
```

The REAL-leg contract holds on the pinned capture independently of the counter, and the refusal
branch behaves on genuine HTML/PDF bytes. I did **not** run `c1-count.py` or `c2-count.py`: their
legs belong to the wave's other seats, and their output is not evidence I can claim.

## 7. The sweep, as run (intended lane path `corpus/evidence/round52/neg-sweep.py`)

```python
#!/usr/bin/env python3
"""Negative sweep in the lane reading convention: `.txt` via
Path.read_text(encoding="utf-8", errors="replace") (build-spans `form_texts`),
NIPH via `capture-text.py <raw>` stdout."""
import hashlib, pathlib
Q = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
DOCS = [("medsci", Q/"453d492becd9a2f4632cb8dd.txt"), ("chinagp", Q/"cacddf3bbf780a4c7582bb17.txt"),
        ("archive", Q/"e84bfe97808591d23fe3266f.txt"), ("NIPH", pathlib.Path("niph.txt"))]
TERMS = ["検索者","検索担当","誰が","检索者","检索人员","検索日","検索期間","文献検索期間",
         "最終検索日","检索日期","检索时间","最后检索","検索式","検索戦略","完全な検索戦略",
         "检索策略","检索报告清单","灰色文献","PRISMA-S","PRISMA 2020","16个条目","付费","下载"]
T = {n: p.read_text(encoding="utf-8", errors="replace") for n, p in DOCS}
print("TERM\t" + "\t".join(n for n, _ in DOCS))
for term in TERMS:
    print("%s\t%s" % (term, "\t".join("%d@%d" % (T[n].count(term), T[n].find(term)) for n, _ in DOCS)))
# split-token control: whitespace-tolerant regex must not beat the literal count
import re
for term in TERMS:
    rx = re.compile(r"\s*".join(map(re.escape, term)))
    assert all(len(rx.findall(T[n])) == T[n].count(term) for n, _ in DOCS), term
```

Run with `TMPDIR` in my scratch; `niph.txt` = `capture-text.py 3a8b45977cd111e45e3980a5.raw`.

## 8. Risks / limits I am handing over

- The C2 quote legs depend on the *cuts* in §5, not on the entries' prose. Three staged quotes are
  rendered-layout reconstructions; landing them as-is makes `build-spans` refuse.
- chinagp offsets are only valid in the universal-newline form; a raw-byte decode of the same file
  gives different offsets for the same quote. Name the form on every chinagp `char N`
  (QUALITY 76).
- `検索者`/`检索者`/`検索担当` zeros are strong (whole-document forms, split-tolerant scan, both
  languages, four documents) but they are *lexical*: a document could record the searcher under a
  word I did not sweep. NIPH shows the limit — `実施` occurs 38 times (of the analysis, and of the
  form's `実施体制` section at 1402), `作成` once (19096), yet `作成者` and `担当` are 0. The
  negative is "none of these five searcher terms occurs", not "no searcher is implied".
- S126 (jahbs) is not one of my four documents and its two-column extraction interleaves cells;
  `検索の開始日と終了日を記載することで` 1@11294 is contiguous, but `プロバイダー` cannot be quoted
  from that `.txt` at all. Flagged, not adjudicated.

VERDICT — I attacked the four search-record text forms with an exact-count negative sweep and
staged-claim falsification: 12 of 23 terms are zero in all four forms (searcher identity, fixed
date names, 灰色文献, 付费), the r40 / r37 / r38-NIPH negative claims reproduce on substance, but
three staged prose quotes (r38 worked example, r40 item 7, r37 per-source date sentence) do not
locate byte-exactly in the round-52 forms and are routed for re-cutting.
