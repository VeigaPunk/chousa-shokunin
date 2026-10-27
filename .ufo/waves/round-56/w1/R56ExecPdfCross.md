# R56ExecPdfCross — PDF cross-check of the five C2 captures

seat: R56ExecPdfCross (executor, round-56 v2 wave 1)
lane commit for the code under test: `46e1758f3d8a5d1bf30200d2ff7d909b0230feed`; base `e5a3795191601797613eb986b36fa0b1a73fe6a1`
scope: C2 only (the five PDF captures behind S127–S130 and held S118). I wrote no lane file; the script below is for the
L1 to commit as `corpus/evidence/round56/pdf-crosscheck.py`. C1, the R55W2 items and the C2 entry construction are not
mine and are untouched.

## What C2 actually reads (grounded, not assumed)

`c2-count.py:form_text` (`corpus/evidence/round56/c2-count.py:148-165`) uses `tools/capture-text.py` only when the
`.raw` is an OLE/zip header (`defined_raw`, `:141-142`); otherwise the DEFINED form is the `.txt` capture read with
universal newlines. All five `.raw` files here are literal PDFs, so the `.txt` form is what every C2 quote is judged in:

```
$ python3 -c "… print(k, (C/k.raw).read_bytes()[:8].hex())"   # five keys from sha256(url)[:24]
b27ffd2f0161104c6a28c9f5 raw_head 255044462d312e37 CR 0 FF 39
de9f5afc3809acbf61f4d5bb raw_head 255044462d312e37 CR 0 FF 8
5233bf47babaa1ca2b49ed15 raw_head 255044462d312e34 CR 0 FF 13
a42feae4448612f949cc715f raw_head 255044462d312e37 CR 0 FF 16
16fe8487aa97b98576a0dbac raw_head 255044462d312e37 CR 0 FF 42
```
`25504446` = `%PDF-`. Cache key → id verified from the URL itself (`sha256(url)[:24]` reproduces all five names,
checked in `terms.txt` run), so the file I read is the file C2 will read. No `.txt` contains `\r`.

## Measurement

Tool: pypdf **6.21.2**, run ephemerally as `uv run --with pypdf python` (uv cache only; no `uv tool install`, no pacman,
nothing written to a PATH directory — pacman is paused host-wide and unused). Scratch
`/fast/scratch/hyaku/chousa-r56/R56ExecPdfCross`, `TMPDIR` there, `PYTHONDONTWRITEBYTECODE=1`.

```
$ cd /fast/scratch/hyaku/chousa-r56/R56ExecPdfCross && uv run --with pypdf python pdf-crosscheck.py
pypdf 6.21.2
S127 standard text: pages txt(39)/pdf(39) chars txt=70038/50640 pdf=57119/50640 MULTISET== TERM_LINES contiguous=5/5 content-ok=5/5 HEAD=ok TAIL=ok PAGE8GRAM pdf->txt=0.581 txt->pdf=0.568 OK
S128 explanatory note: pages txt(8)/pdf(8) chars txt=7031/6296 pdf=6916/6296 MULTISET== TERM_LINES contiguous=2/2 content-ok=2/2 HEAD=ok TAIL=ok PAGE8GRAM pdf->txt=1.000 txt->pdf=1.000 OK
S129 journal copy: pages txt(13)/pdf(13) chars txt=80732/37427 pdf=43170/37427 MULTISET== TERM_LINES contiguous=2/7 content-ok=7/7 HEAD=ok TAIL=ok PAGE8GRAM pdf->txt=0.620 txt->pdf=0.603 OK
  reorder-only line '本指南为管理型指南，采用中国循证医学中心的证社会效益社会、舆论关注程度对伦理、法律、社会心理方面' cells=[True, True, True, True, True]
  reorder-only line '据分级体系，将证据分为5级，证据分级标准见表1；采个人/公共利益5.34' cells=[True, True, True]
  reorder-only line '表1证据分级标准6.2.1研究背景' cells=[True, True, True]
  reorder-only line '证据分级描述研究背景的核心是阐述立题依据，陈述研究人员进' cells=[True, True, True]
  reorder-only line '灰色文献未公开发表的研究信息，可能包含了最新的研究成果和观点Ⅰ级A' cells=[False, True, True]
S130 NHC 2020 guideline: pages txt(16)/pdf(16) chars txt=6930/6237 pdf=6530/6237 MULTISET== TERM_LINES contiguous=0/0 content-ok=0/0 HEAD=ok TAIL=ok PAGE8GRAM pdf->txt=1.000 txt->pdf=1.000 OK
S118 issued QC guideline: pages txt(42)/pdf(42) chars txt=27609/20390 pdf=21560/20390 MULTISET== TERM_LINES contiguous=0/0 content-ok=0/0 HEAD=ok TAIL=ok PAGE8GRAM pdf->txt=0.747 txt->pdf=0.699 OK
CROSSCHECK=PASS
EXIT=0
```

Term counts per form are identical in both extractions (one-off run, `terms.txt`):

```
S127 txt [1, 1, 3, 1] pdf [1, 1, 3, 1]   # 灰色文献, 中国循证医学中心, 证据分级, 未公开发表
S128 txt [0, 2, 1, 0] pdf [0, 2, 1, 0]
S129 txt [1, 2, 6, 1] pdf [1, 2, 6, 1]
S130 txt [0, 0, 0, 0] pdf [0, 0, 0, 0]
S118 txt [0, 0, 0, 0] pdf [0, 0, 0, 0]
```

## Negative control (the checks bite)

Same script, `CACHE` pointed at a scratch cache whose S127 `.txt` is `head -c 63034` of the real one (the other four
symlinked unchanged):
```
S127 standard text: pages txt(18)/pdf(39) chars txt=29842/21171 pdf=57119/50640 MULTISET=DIFF TERM_LINES contiguous=5/5 content-ok=5/5 HEAD=ok TAIL=MISSING PAGE8GRAM pdf->txt=0.006 txt->pdf=0.782 LOSS
CROSSCHECK=FAIL
EXIT=1
```
Truncation is therefore visible to the script (page count, multiset, tail, coverage), so the PASS above is a
measurement and not a vacuous criterion.

## Findings

1. **No `.txt` truncation, no content loss, no duplication.** Page counts agree (39/8/13/16/42); after whitespace is
   stripped the `.txt` and pypdf character multisets are equal char-for-char for all five (raw lengths differ only
   because pdftotext pads with layout spaces: 70038→50640, 80732→37427, 27609→20390). Head and tail lines are present
   in pypdf's text too. Per-page 8-gram coverage never falls to zero in either direction (worst 0.568), so no page is
   missing from either side.
2. **Every term-bearing `.txt` line is contiguous in pypdf's text except five in S129** (2/7 line-contiguous, 7/7
   content-ok). The misses are pdftotext joining two newspaper-style columns onto one line (`corpus .../5233bf….txt:173,
   174,178,179`) and one table row (`:297`). Each of those lines' cells is individually present (`cells=[True,…]`);
   the `:297` row `灰色文献 未公开发表的研究信息，可能包含了最新的研究成果和观点 Ⅰ级 A` is present as its two cell
   texts, because pypdf emits that table column-by-column (sources first, then contents) — pypdf's page 5 text contains
   `…临床资料数据库灰色文献搜索引擎…` and separately `未公开发表的研究信息，可能包含了最新的研究成果和观点…`.
3. **S130 and S118 hold none of the four terms** in either form. Any C2 quote on the grey-literature theme attributed to
   S130 (NHC 2020) or S118 (issued QC guideline) would be a fabrication — S118 can only be cited as held, per the
   frozen predicate.
4. Term-line inventory the entry can draw on: S127 `:60`, `:281`, `:291`, `:293`, `:766` (`（9）灰色文献：未公开发表研究
   信息，可能包含了最新的研究成果和观点，能够研究`); S128 `:98` and `:99` (the source itself doubles
   `中国循证医学中心中国循证医学中心`, so a quote must not straddle that duplication); S129 `:18`, `:171`, `:173`,
   `:174`, `:178`, `:179`, `:297`. Each quote still has to lie on ONE line of its form, ≤25 whitespace words and ≤160
   chars, and be unique in the form — that check is C2's counter's, not mine.

## Residual risks (reported, not patched)

- Multiset equality is order-insensitive: a hypothetical `.txt` that dropped one run and duplicated a run of identical
  characters could conserve the multiset. Page-count equality, per-page coverage > 0 on every page and head/tail
  presence make that implausible but do not formally exclude it.
- For S129 the table row alignment (which 灰色文献 cell belongs to which Ⅰ级/A row) is established by pdftotext's
  layout reading only; pypdf's default extraction is column-major there. A quote may be textually exact and still
  over-claim row association if the authors lean on the merged line for alignment rather than for wording.
- pypdf emits `Multiple definitions in dictionary at byte … for key /Ascent` warnings on S129 (stderr, suppressed in the
  run above); they did not affect extraction (multiset equal), but they show that PDF is mildly malformed.

## Script (80 lines, to be committed as `corpus/evidence/round56/pdf-crosscheck.py`)

```python
#!/usr/bin/env python3
"""pdf-crosscheck — pypdf re-extraction of the five C2 PDF captures against their `.txt` forms.

C2's captures have a PDF `.raw`, so `c2-count.py`'s `form_text` reads the `.txt` as the
DEFINED text form (`tools/capture-text.py` runs only on OLE/zip).  Per document: pages
(`.txt` \f count vs pypdf), characters (raw / whitespace-stripped), the character
multiset (loss or duplication breaks it), each `.txt` line carrying a frozen term
(灰色文献 / 中国循证医学中心 / 证据分级 / 未公开发表) present in pypdf's stripped text
(contiguous) and with its cells / tokens present (content-ok: pdftotext joins table
columns pypdf emits column-wise), head/tail lines, and the weakest per-page 8-gram
coverage both ways.  Exit 0 iff every document conserves content.

usage: uv run --with pypdf python corpus/evidence/round56/pdf-crosscheck.py
"""
from __future__ import annotations

import hashlib, pathlib, re, sys  # noqa: E401
from collections import Counter

CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
DOCS = [
    ("S127", "https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf", "standard text"),
    ("S128", "https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf", "explanatory note"),
    ("S129", "https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf", "journal copy"),
    ("S130", "https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf", "NHC 2020 guideline"),
    ("S118", "https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf", "issued QC guideline"),
]
TERMS = ("灰色文献", "中国循证医学中心", "证据分级", "未公开发表")


def flat(s: str) -> str:  # whitespace-stripped: wrapping and layout padding hide nothing
    return re.sub(r"\s+", "", s)

def grams(s: str, n: int = 8) -> set[str]:
    f = flat(s); return {f[i:i + n] for i in range(len(f) - n + 1)}

def min_cov(parts: list[str], whole: str) -> float:
    gs = [g for p in parts if (g := grams(p))]
    return min((sum(x in whole for x in g) / len(g) for g in gs), default=1.0)

def content_ok(ln: str, npd: str) -> bool:
    for c in (c for c in re.split(r"\s{2,}", ln.strip()) if flat(c) and flat(c) not in npd):
        toks = [flat(t) for t in c.split(" ") if len(flat(t)) >= 2]
        if not toks or not all(t in npd for t in toks):
            return False
    return True


def main() -> int:
    import pypdf
    from pypdf import PdfReader
    print(f"pypdf {pypdf.__version__}")
    bad = 0
    for sid, url, label in DOCS:
        k = hashlib.sha256(url.encode()).hexdigest()[:24]
        txt = (CACHE / f"{k}.txt").read_text(encoding="utf-8", errors="replace")
        pages = [(p.extract_text() or "") for p in PdfReader(str(CACHE / f"{k}.pdf")).pages]
        pdf, lines = "\n".join(pages), txt.splitlines()
        nt, npd = flat(txt), flat(pdf)
        tl = [ln for ln in lines if any(t in ln for t in TERMS)]
        contig, cok = sum(flat(ln) in npd for ln in tl), sum(content_ok(ln, npd) for ln in tl)
        head, tail = next((x for x in lines if x.strip()), ""), next((x for x in reversed(lines) if x.strip()), "")
        pmin, tmin = min_cov(pages, nt), min_cov(txt.split("\f"), npd)
        ok = (cok == len(tl) and txt.count("\f") == len(pages) and Counter(nt) == Counter(npd)
              and flat(head) in npd and flat(tail) in npd and pmin > 0 and tmin > 0)
        bad += not ok
        print(f"{sid} {label}: pages txt({txt.count(chr(12))})/pdf({len(pages)}) chars txt={len(txt)}/{len(nt)} "
              f"pdf={len(pdf)}/{len(npd)} MULTISET={'=' if Counter(nt) == Counter(npd) else 'DIFF'} "
              f"TERM_LINES contiguous={contig}/{len(tl)} content-ok={cok}/{len(tl)} "
              f"HEAD={'ok' if flat(head) in npd else 'MISSING'} TAIL={'ok' if flat(tail) in npd else 'MISSING'} "
              f"PAGE8GRAM pdf->txt={pmin:.3f} txt->pdf={tmin:.3f} {'OK' if ok else 'LOSS'}")
        for ln in tl:
            if flat(ln) not in npd:
                cells = [flat(c) for c in re.split(r"\s{2,}", ln.strip()) if flat(c)]
                print(f"  reorder-only line {flat(ln)[:48]!r} cells={[c in npd for c in cells]}")
    print("CROSSCHECK=" + ("PASS" if not bad else "FAIL"))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
```

sha256 of the run copy: `7ecca2d9b5233c673d7cd7259fcd1c7a952477490fcf91707f57b7a3b9372484`; `wc -l` = 80.

## Files changed

- this report only: `chousa-shokunin/.ufo/waves/round-56/w1/R56ExecPdfCross.md`. Scratch
  `/fast/scratch/hyaku/chousa-r56/R56ExecPdfCross` removed after the two receipts above were pasted; nothing outside it
  was written, no git/jj command was run, no network fetch, `/home/vgpnk/Projects/shokuknow` read only.

VERDICT: attacked the `.txt` text forms of C2's five PDF captures (S127–S130, S118) with pypdf 6.21.2 — all five
survived (CROSSCHECK=PASS: equal page counts, equal whitespace-stripped character multisets, term lines contiguous
9/14, the five S129 misses being column-joins whose cells and tokens are all present, no truncation); S130 and S118
carry none of the four terms, and S129's table-row alignment rests on pdftotext's layout reading alone.
