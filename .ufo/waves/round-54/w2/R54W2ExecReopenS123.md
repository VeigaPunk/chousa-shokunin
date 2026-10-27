# R54W2ExecReopenS123 — independent re-open of S123 (JMU reproduction of GB/T 7714—2025)

Leaf seat, no dispatch. Scratch `/fast/scratch/hyaku/chousa-r54/R54W2ExecReopenS123` (`TMPDIR` there, removed at
exit); `PYTHONDONTWRITEBYTECODE=1` throughout — `find . -name __pycache__ -newermt -30min` in the lane → nothing.
Tooling: no install, no pacman; `uv run --quiet --with pypdf` (uv cache only, nothing on PATH); host `pdftotext`
(poppler) 26.08.0. Capture read-only; freeze, quotes and anchors untouched.

## 0. Capture identity, and the text form (finding F2)

`sha256(URL)[:24] = 0f33243fd7ac2fe88b85c1ba` = the qcache key ✓. `.txt` = 83,061 chars / 190,614 B,
`sha256 13a34aa9bb107eefeb8bed6a50a0d574af84ff77a66940e8b88ea895fea1182f` — the digest in all 21 S123 span rows
and the `13a34aa9bb107eef` prefix at `SOURCES.md:133`; no CR, 45 U+000C. Re-extracting the `.raw`:

| flags | chars | bytes | sha256 |
|---|---:|---:|---|
| `-layout` | 83061 | 190614 | `13a34aa9…1182f` — byte-identical to the sidecar |
| (default) | 59206 | 166687 | `94e00b96…cd050` |
| `-raw` / `-nopgbrk` | 58054 / 59161 | 165609 / 166642 | — |

**F2:** only `pdftotext -layout` reproduces the text form, and no lane file records the flag — `SOURCES.md:133`
says "read as UTF-8 with newline normalisation", the lesson says "`.txt` (pdftotext)". A re-checker with default
flags puts every quote elsewhere. The entry's `recheck:` reads the sidecar by absolute path and is immune; its
"re-download … and confirm" instruction is not. Not a C2 leg (C2 binds the on-disk `.txt` by path+digest).

## 1. Every S123 quote in `quotes.tsv` — 21/21, count=1, at the offset, inside the entry

`t.count(q)`, `t.find(q)`, `q in` r37; one-line = no `\n`, ≤25 whitespace words, ≤160 chars. `FAIL_ROWS=0`.

| off | ct | entry | quote (cut) | off | ct | entry | quote (cut) |
|---|---:|---|---|---|---:|---|---|
| 5576 | 1 | Y | 本文件适用于作者和编制者著录参考文献。 | 3602 | 1 | Y | 本文件代替ＧＢ／Ｔ ７７１４—２０１５《…》 |
| 5602 | 1 | Y | 本文件不适用于图书馆员、文献目录编制者… | 424 | 1 | Y | ２０２５－１２－０２发布 |
| 11542 | 1 | Y | 文献类型标识、文献载体标识应按照附录Ａ著录。… | 490 | 1 | Y | ２０２６－０７－０１实施 |
| 14096 | 1 | Y | 电子资源的创建日期…“ＹＹＹＹ－ＭＭ－ＤＤ”… | 5751 | 1 | Y | ＧＢ／Ｔ ４８９４ 信息与文献 基础和术语 |
| 4736 | 1 | Y | 将文献类型“普通图书”“舆图”分别更改为… | 2512 | 1 | Y | 附录Ａ（规范性） 文献类型和文献载体标识代码 |
| 4812 | 1 | Y | 增加了电子资源载体“缩微资料”及其标识代码 | 2655 | 1 | Y | 附录Ｂ（资料性） |
| 4852 | 1 | Y | 将“ＥＢ”代表的文献类型更改为“网站、网页” | 58840 | 1 | Y | 电子资源载体和标识代码应按照表Ａ．２著录。 |
| 21382 | 1 | Y | 图书主要贵任者 | 59201 | 1 | Y | 缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ） |
| 82465 | 1 | Y | 中国标准出版社出版发行 | 57965 | 1 | Y | 图书                          Ｍ |
| 82834 | 1 | Y | ２０２５年１２月第１版 ２０２５年１２月第１次印刷 | 8881 | 1 | Y | “／”用于合期的期号…文献载体标识前。 |
| 5982 | 1 | Y | 以数字方式将图、文、声、像等信息存储在磁… | | | | |

The lesson's 21-row located-quote table verifies identically (`lesson_rows_bad=0`). All 21 `spans.tsv` rows:
`t[offset:offset+len(span_file)] == span_file` (slice exact), digest ok, quote ⊂ span, `len(span) > len(quote)`
(each span = 80 chars lead-in + quote), quote in entry and in the lesson.

## 2. Every `char N` — S123 row anchor (3) and the entry `source:` line (16): text and section match

`SOURCES.md:133` anchor cell `char 5576, char 5602, char 11542` — all three are exact quote offsets (above).

| char | text that starts there | line names | char | text that starts there | line names |
|---:|---|---|---:|---|---|
| 2512 | `附录Ａ（规范性） 文献类型和文献载体标识代码…２８` | 附录Ａ ✓ 目次 line | 2655 | `附录Ｂ（资料性） 顺序编码制参考文献表…３０` | 附录Ｂ ✓ 目次 line |
| 4736 | `将文献类型“普通图书”“舆图”分别更改为…` | 前言 ｏ） ✓ | 4812 | `增加了电子资源载体“缩微资料”及其标识代码` | 前言 ｏ） ✓ |
| 4852 | `将“ＥＢ”代表的文献类型更改为“网站、网页”…` | 前言 ｏ） ✓ | 5576 | `本文件适用于作者和编制者著录参考文献。` | 第１章 范围 ✓ |
| 5602 | `本文件不适用于图书馆员、文献目录编制者…` | 第１章 范围 ✓ | 8881 | `“／”用于合期的期号…文献载体标识前。` | 第６章 著录用符号 ✓ |
| 11542 | `文献类型标识、文献载体标识应按照附录Ａ著录。…` | ７．３ ✓ | 14096 | `电子资源的创建日期、发布日期、修改日期…` | ７．６ ✓ |
| 21382 | `图书主要贵任者，图书题名：其他题名信息…` | ８．３．２ ✓ | 57965 | `图书                          Ｍ` | 附录Ａ ✓ 表Ａ．１ 1/17 |
| 58840 | `电子资源载体和标识代码应按照表Ａ．２著录。` | 附录Ａ ✓ Ａ.２ | 59201 | `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ） ＭＭ` | 附录Ａ ✓ 表Ａ．２ 5/5 |
| 82465 | `中国标准出版社出版发行` | colophon ✓ | 82834 | `２０２５年１２月第１版 ２０２５年１２月第１次印刷` | colophon ✓ |

Headings that confirm the attribution: `１ 范围` @5497, `６ 著录用符号` @8170 (`６．２` @8316), `７．３` @11519,
`７．６ …` @14071, `８．３．２ 著录格式` @21294, `Ａ．２ …` @58760. The two 目次 anchors are not a defect — they
are quotes, and they are where `（规范性）`/`（资料性）` attach to the appendix titles; the bodies corroborate:
`附 录 Ａ` @57686 / `（规范性）` @57722, `附 录 Ｂ` @59367 / `（资料性）` @59408.

## 3. Every backticked CJK fragment in the entry — 33/33 occur in the capture

58 backtick spans, 36 CJK-bearing, 33 real quotations: each found whitespace-free in the sidecar. The 3
non-matches are the two `python3 -c …` commands and one F3 fragment (§6). No fabricated fragment.

## 4. Every Observation sentence — holds

- **O1 reproduction/colophon/OCR** — HOLDS. `２０２５－１２－０２发布` 1× @424 beside `２０２６－０７－０１实施` @490;
  `本文件代替…—２０１５《…》` 1× @3602 under `前 言`; `中国标准出版社出版发行` 1× @82465, `２０２５年１２月第１版
  ２０２５年１２月第１次印刷` 1× @82834. "it is an OCR" is understated: `图书主要贵任者` 1× @21382 (贵/责) **plus**
  `健名` 1× @34243 (健/题, 8.8.3) **plus** `ＧＢ／Ｔ７１４－２０２５` 1× @82280 (running head; ７ missing, `－` for
  `—`) — n≥3 glyph errors, not the single one the entry cites.
- **"主要责任者 occurs 31 times"** — HOLDS exactly: `t.count('主要责任者') = 31`; `主要[责贵]任者` = 31 + 1 OCR
  variant, so the figure is neither inflated nor deflated.
- **O2 scope** — HOLDS: @5576 then @5602, contiguous under `１ 范围` @5497; triad 图书馆员/文献目录编制者/索引编制者.
- **O3 7.3 / slash / appendix status** — HOLDS: 7.3 1× @11542 with `献载体标识。` continuing next line (the quote
  ends at `也应著录文`, a genuine one-line cut); slash rule 1× @8881 in `６ 著录用符号`; `（规范性）` @2515/57722
  vs `（资料性）` @2658/59408.
- **O4 five-row carrier table** — HOLDS, exactly five: `磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ） ＭＴ` @59025, `磁盘（ｄｉｓｋ）
  ＤＫ` @59073, `光盘（ＣＤ－ＲＯＭ） ＣＤ` @59116, `联机网络（ｏｎｌｉｎｅ） ＯＬ` @59161, `缩微资料（ｍｉｃｒｏｆｏｒｍ
  ｍａｔｅｒｉａｌｓ） ＭＭ` @59201 — each 1×, no sixth row. Addition item @4812 inside 前言 `ｏ）`; 表Ａ．１ has 17
  type rows and `图书                          Ｍ` is row 1.
- **O5 date rule** — HOLDS: 1× @14096 under `７．６` @14071.
- **Unknown sweeps** — HOLD, both runnable lines reproduce verbatim: the `recheck:` command prints `11542 32`; the
  sweep prints `[32, 0, 0, 0]` (`文献载体标识` 32, `3469` 0, `ＩＳＯ ６９０` 0, `690` 0; NFKC `ISO 690` 0).

## 5. Counters and checks re-run at the integrated tip (read-only)

- `python3 corpus/evidence/round54/c2-count.py` → `C2=PASS`, exit 0: `BOUND_IDS=S121,S122,S123`, `QUOTE_ROWS=33`,
  `ON_BOUND=33/33`, `CAPTURE_BOUND=33/33`, `ANCHOR_BOUND=3/3`, `SUBSTANCE=PASS`, `INFERENCE_GROUNDED=2/2`,
  `QUARANTINE_VERDICTS=3/3 (S080,S088,S096)`, `QUARANTINE_BLOCKED_ADOPTED=0`.
- `python3 corpus/evidence/round54/build-spans.py --check` → `SPANS_ROWS=33 STALE=0`, exit 0.
- `uv run --quiet --with pypdf python corpus/evidence/round54/pdf-crosscheck.py` → `PDF_QUOTES=21
  NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14`, exit 0 — E4 reproduced. The width direction is independently true: pypdf
  holds `附录A` 4×/`附录Ａ` 0× and `YYYY-MM-DD` 2×/`ＹＹＹＹ－ＭＭ－ＤＤ` 0×, and holds `图书主要贵任者` 1× with
  `图书主要责任者` 1× — the OCR glyph is in the PDF, not a sidecar artefact.
- E3: no `source: S101` line in either entry; only S121/S122/S123 tokens occur (12/8/14); S101 `used-by` is still
  `citation-count-semantics-r37.md`. Novelty: at BASE `c49ffc6c…` `SOURCES.md` has no `S123` row and
  `git grep -e "ISO 690:2021" -e 文献载体标识 <BASE> -- corpus/knowledge` → exit 1.

## 6. Findings

**F1 — WRONG, `SOURCES.md:133` anchor cell: "the 附录Ａ 表A.1 rows marked 电子资源必备".** `电子资源必备` occurs
25× and **none** in 附录Ａ (57654–59325); 表Ａ．１'s header is `参考文献类型 / 文献类型标识代码` — two columns, no
必备性 column (17 rows dumped). The marking belongs to the chapter-8 per-type tables: `文献载体标识  电子资源必备
７．３、Ａ．２` @17657, `获取和访问路径  电子资源必备  ７．８` @18323. The cell should read "…and the 表１/表２ rows
marking 文献载体标识 `电子资源必备`". Not a C2 leg — the cell's `char N` are valid quote offsets and
`ANCHOR_BOUND=3/3` is untouched — but it is a false statement in the cell the predicate names "anchor".

**F2 — recheckability, §0.** The one extractor recipe that reproduces the sidecar (`pdftotext -layout`) is in no
lane file; default `pdftotext` yields 59,206 chars and different offsets.

**F3 — misdescription in the entry's "Staged material corrected on adoption".** It says the staged entry "quoted
７．３ across a line break (`…也应著录文` / `献载体标识。`)". In
`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/source-type-taxonomy-r37.md` the staged
quote breaks after `附录Ａ` (→ `著录。…`) and writes the tail as `也应著录文献载体标识` on one line — the
parenthetical names the capture's break, not the staged quote's. The staged defect (a reflowed quote carrying an
in-quote newline) is real and rightly corrected; only where the break sat is misdescribed. The other two clauses
are true of the staged file: it says "图书 and 舆图 were replaced by 图书 and 地图" (misses 普通图书) and never
marks 附录Ａ normative / 附录Ｂ informative.

**F4 — Inference 1 headline loose.** "The type letters are renamed between editions": the change list renames type
*names* (普通图书/舆图→图书/地图) and changes ＥＢ's referent; the letters persist (表Ａ．１ `图书 Ｍ`, `地图 ＣＭ`,
`网站、网页 ＥＢ`). The body sentence ("the same letter can stand for a differently named type") is supported.
Agrees with `R54W2CritEntailStb.md` I1; my §4 O1 corrects that report's I6 (OCR evidence is n≥3, not n=1).

**No attack landed on:** quote offsets/counts (21/21), span slices and digests (21/21), the 3 registry and 16 entry
anchors and their sections, the entry's 33 fragments, the five Observation sentences, both runnable commands, the
digit-only predicates (`int(offset)+span.find(quote)` on every row), E3's cut, E4's NFKC check.

VERDICT: attacked S123's 21 quotes, 21 spans, 3 registry + 16 entry anchors, all 5 Observation sentences, both
runnable commands and the live C2/pdf-crosscheck/build-spans at the tip — the claim SURVIVES. Three non-claim
defects stand: one false registry-anchor clause (F1: `电子资源必备` is not in 表Ａ．１), one recheckability gap
(F2: the `-layout` flag), one meta misdescription (F3); plus one loose Inference headline (F4). None touches a
predicate, target, counter, control, quote or span.
