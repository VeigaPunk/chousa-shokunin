# QuarantineS112 — hand-check, register `chousa` S112 (staged/lane id S114 → merged S117)

Scope: re-verify the `payload-absent` verdict on chousa-register row S112 against the on-disk capture of
https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237 . No live fetch.
Read-only; leaf member. Scratch `/tmp/chousa-r48-QuarantineS112/` deleted on finish.

## Identity caveat (matters)

Register S112 joins by **staged (pre-remap) id, not by final registry id**. The URL is the only stable key:
`lanes/chousa/ID-REMAP.md` maps round4 `S114`→`S117`, and `merge/chousa/SOURCES.append.md:42` binds the
slarc/5237 PDF to **S117**. Round3 already owns a different `S112` (chinagp.net). So this register row is
"the slarc-5237 gate block" whatever the S-label — the same collision S110's check recorded.

## Inputs

- Register row: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:52`
  — `chousa | round4 | S112 | payload-absent | …/downloadArticleFile.do?attachType=PDF&id=5237 | <3 quotes>`.
- Lane gate block: `lanes/chousa/round4/SOURCES-PROPOSED.md:50-57` (Gate — S117 in the file, census id S112):
  `Opened: 2026-10-23 (HTTP 200, 1,140,215 bytes; text extracted with pdftotext -layout, 56,027 bytes)`,
  five quoted spans; the register carries the three that failed.
- Quote spans (sha256 of UTF-8):
  Q1 74 ch/162 B `检索中国知网、万方、中国生物医学文献数据库、PubMed、Embase和WebofScience数据库，检索时间从各数据库建立至2024年4月1日。` `4892b649a7ef3506751b674e56c5d66992546be1c23eeba0ebd9e14c07ab8d55`
  Q2 27 ch/59 B `检索策略结合主题词（MeSH/Emtree）和关键词。` `80d56e16328f686f3103a1e6ad85c3b04971c4602b41d3b9e397bd68359b9f5e`
  Q3 72 ch/90 B `实验动物与比较医学, 2025, 45(1): 101-111  DOI: 10.12300/j.issn.1674-5817.2024.109` `1bf2ae6eeed5cdae0dfead633709ba8cb3fd3d2dc7c2a378e4626e743f61e5bf`
  (digests match `corpus/evidence/round42/receipts/examine.txt:33-35` for S112).
- Captures, cache-key = sha256(url)[:24] = `c7266931a1731db3ff6ae77d` ✓:
  `.qcache/c7266931a1731db3ff6ae77d.pdf` — 1,140,215 B, sha256 `815bea41f8c249010fa11f1d374e5977db3bac5e50999ba190788bd4fc51fd07` (matches gate byte count).
  `.qcache/c7266931a1731db3ff6ae77d.txt` — 69,789 B, sha256 `03342b7ded4f9d687a5319a739cf357e…` — the checker's `pdftotext -layout` render (two-column interleaved).
  `pdftotext` (stream order) → 56,027 B, `32b2cc3fb50ece7cd2c70b982b7efe2c…` — byte-identical in size to the gate's own record; this is the lane's working text.
  `pdftotext -raw` → 54,599 B, `43edfcb9022072188932dbadd2dd4db2…`.
- Companion named in SEARCH-LOG (`1674-5817-2025-45-1-101.shtml`, corroboration): no qcache entry
  (key `2d01a05bc679a11de712419b` absent) — companion never fetched; only the PDF decided this row.
- Lane-local artifacts: round4 has no `evidence/` dir; only staging md files (excluded by `local_candidates`).
  The quote string exists nowhere else on disk but `SOURCES-PROPOSED.md` itself.

## Commands run (decisive output)

1. `sha256sum` on pdf/.txt and my three extractions — identities above; `.raw` == `.pdf`.
2. Byte windows in `.txt` (layout): `检索中国知网` char 11211 (byte 16819, line 169);
   `PubMed、Embase 和 Web of Science` char 11299 (line 170); `从各数据库建立至` char 11404 (line 171);
   `题 词 （MeSH/Emtree）` char 11501 (line 172) — all in the **right column** (col ≥64) interleaved with
   left-column `…分级。如果直` / `献质量基于直接证据` fragments on the same lines.
3. Rebuilt right column (split lines 150–195 at col 64, whitespace removed): yields
   `…检索中国知网、万方、中国生物医学文献数据库、PubMed、Embase和WebofScience数据库，检索时间从各数据库建立至2024年4月1日。检索策略结合主题词（MeSH/Emtree）和关键词。中文检索词包括：“动物实验”…`
   — Q1 and Q2 **present verbatim end-to-end** once whitespace is removed; under `.txt` direct
   `f_nows` still fails because columns interleave; under the 56,027-B stream text `f_nows` **matches**
   (my run: `q1 True, q2 True`; the checker never sees this render — it stores only `-layout`).
4. PDF's own bytes differ from the quotes in spacing: PDF has `PubMed、Embase 和 Web of Science 数据库`
   (spaces, → `WebofScience` only after squeeze) and `题 词 （MeSH/Emtree） 和 关 键 词` (glyph gaps).
   Stream `pdftotext` keeps `Embase和Web of Science` — quote wrote `WebofScience`, a silent space
   deletion that only the loosest fold forgives.
5. Q3: `.txt`/`stream`/`raw` greps — the only near-occurrence is the `[引用本文]` citation block
   (`.txt` line 545, char 49175; stream byte ~51 k):
   `…实证研究[J]. 实验动物与比较医学, 2025, 45\n(1): 101-111. DOI: 10.12300/j.issn.1674-5817.2024.109.`
   — differs by a hard line wrap inside `45(1)`, a period after `101-111`, and a trailing period; every
   running head carries `Feb. 2025, 45(1) 实验动物与比较医学 Laboratory Animal and Comparative Medicine`,
   never the `journal, year, vol(issue): pages  DOI:` flat form. `f_nows`/`dewrap`/`nfkc`/`typo`: all
   False on all three renders. Not present under any fold.
6. Prior committed ruling: `corpus/evidence/round43/absent-split.tsv:13` — `S112 misquote 40 71 0.563 3`
   (max contiguous common run 40/71 chars ≥ the frozen 1/2 bound), and
   `corpus/lessons/round-43-verifier-spotcheck.md:60` lists S112 among the nine `misquote` rows.

## Per-quote verdicts

- Q1 `检索中国知网…至2024年4月1日。` — **present** (as a whitespace-squeezed span): right column of page 3,
  `.txt` chars 11211–11600 (lines 169–172). Two mechanical blindings: two-column interleave and the
  quote's unspaced `WebofScience`/`（MeSH/Emtree）` vs the PDF's spaced glyphs. Not fabrication-grade.
- Q2 `检索策略结合主题词（MeSH/Emtree）和关键词。` — **present**, same right column, continuing
  immediately after Q1's `。` (lines 171–172). Same blinding mechanism.
- Q3 `实验动物与比较医学, 2025, 45(1): 101-111  DOI: …` — **absent-as-written**: the document's own
  flat citation is `…[J]. 实验动物与比较医学, 2025, 45(1): 101-111. DOI: ….109.` with `45`/`(1)` split
  across a wrap and a period before `DOI`; the gate's string (comma-form, double space before `DOI:`,
  no period) is a re-punctuated mashup of running head + citation block. The content is all there; the
  quoted character sequence is not.

## Row verdict

`payload-absent` **stands, but for the wrong reason**: the row is **absent-as-written**, not
fabricated-content. Q1/Q2 live verbatim in the cited PDF once de-interleaved/whitespace-squeezed —
the checker is blind to both (layout render interleaves columns; its loosest fold forgives only pure
whitespace, and the quote also edits spacing inside a term). Q3 is a genuine misquote of
punctuation/wrap. This matches the frozen R43 ruling (`misquote`, ratio 0.563): a quote-typography
defect, not a fabricated-source defect. Correction, not refusal: quote the stream text verbatim
(`PubMed、Embase 和 Web of Science`, `主\n题词（MeSH/Emtree）和关键词` spans) or mark the spans
whitespace-squeezed, and replace Q3 with the document's own citation line.

Residual risk: column split at char 64 verified only on the page-3 band (lines 150–195); each fragment
independently located once. Companion landing page unfetched — nothing on disk contradicts the PDF verdict.
