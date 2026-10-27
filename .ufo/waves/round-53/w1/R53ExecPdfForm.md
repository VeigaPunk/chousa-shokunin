# R53ExecPdfForm — text-form fidelity of the three C2 PDF captures (round 53, wave 1)

Seat: R53ExecPdfForm (leaf). Scratch `/fast/scratch/hyaku/chousa-r53/R53ExecPdfForm/` (TMPDIR exported, removed at exit). `/home/vgpnk/.omp/agent/RULES.md` read: **no install performed** — `pdftotext` 26.08.0, `pdfinfo`, `qpdf` 12.4.2 already present, `mutool` absent; the independent extractor was fetched ephemerally by `uv run --with pypdf` (pypdf 6.21.2, no PATH change). pacman untouched; nothing written but this report.

## 0. The sidecar's provenance makes `pdftotext` useless as the independent check

`command -v pdftotext pdfinfo mutool qpdf python3` → `/usr/bin/pdftotext /usr/bin/pdfinfo /usr/bin/qpdf /usr/bin/python3` (no `mutool`). Fresh extraction of each capture in three modes, compared byte-wise:

```
for mode in "" "-layout" "-raw"; do pdftotext $mode -enc UTF-8 $Q/$h.raw out; cmp -s out $Q/$h.txt; done
0ae65ac0  default no  -layout YES  -raw no   sidecar 27659 chars
16fe8487  default no  -layout YES  -raw no   sidecar 27609 chars
0435b64f  default no  -layout YES  -raw no   sidecar 21573 chars
```

All three sidecars are **byte-identical to `pdftotext -layout -enc UTF-8`** of the bytes beside them (`sha256sum $Q/$h.raw $Q/$h.pdf` → c2aa0e12d45f…, 7b600fe3ee9b…, 1a46faaee6ba… identical per capture). The sample check the round-53 spec hands the QCG scribe — *"compare a sample with `pdftotext` if installed"* — is therefore circular: it compares the sidecar with itself. pypdf (no poppler code) is the independent instrument below; `pdftotext -raw` is a third reading with a different reading order.

## 1. Page count and character count, page by page

```
capture   pages pdfinfo/pypdf/sidecar-\f   stripped chars sidecar/pypdf/raw   per-page sums  per-page multiset
0ae65ac0  5     5 / 5 / 5                  15983 / 15983 / 15983               0/5 differ     0/5 differ
16fe8487  42    42 / 42 / 42               20390 / 20390 / 20390               0/42 differ    0/42 differ
0435b64f  30    30 / 30 / 30               13630 / 13630 / 13630               0/30 differ    0/30 differ
```

Whole-document character multisets are equal under both other readings **and per page**. No character is lost, added or substituted in any capture; only inter-character whitespace and within-page ORDER differ. No page is image-only (every page carries text in both readings).

## 2. Ten random one-line spans per capture, seeds 53 and 7

Span = a 5–8 word window (Latin) or 12–18 character window (CJK) from a random non-blank line, searched whitespace-normalised (`WS`), then with all whitespace removed (`DSP`, to separate spacing from lost characters).

`0ae65ac0` seed53 **pypdf 10/10 WS, 10/10 DSP** (sidecar control 10/10, raw 10/10); seed7 10/10, 10/10.
L136 `Word format on the PRISMA website` · L273 `was introduced in the PRISMA` · L314 `Commons Attribution 4.0 International License.` · L297 `Melissa L. Rethlefsen, MSLS, AHIP, mlrethlefsen@gmail.com,` · L215 `either by individual information source or` · L272 `the number of reports of included` · L30 `retrieved per database in the “records identified` · L33 `provide direct guidance on how to report the` · L112 `put the total number of records that` · L207 `hand or by other means) from`.

`16fe8487` seed53 **pypdf 10/10 WS, 10/10 DSP**; seed7 10/10, 10/10.
L626 `、创新性、适宜性、可及性六个维度` · L1273 `评价是否根据所选评价方法的报` · L1432 `Appraisal Skills Programme,CASP）；定性研究统一报告标准（Consolidated Criteria for` · L1345 `评价的药品及其对照药品有` · L1484 `家充分论证），以及每个维度所` · L1010 `体职责：由三级质控主体负责对` · L1268 `：每个维度所选用的评价指标是` · L76 `................` · L91 `委《关于开展药品使用监测和临床综` · L489 `选择、评价维度选择、评价指标选择、评`.

`0435b64f` seed53 **sidecar 7/10 WS, 10/10 DSP; pypdf 5/10 WS, 10/10 DSP; raw 7/10 WS, 10/10 DSP**. The three sidecar WS misses are char-windows that straddle a space inside a Latin token — L372 `陵，PaulGlasziou` (sidecar `Paul Glasziou`), L546 `照试验方法学评价指标采用MI` (`采用 MINORS`), L624 `态独立评估*；b）记录链接*` (`评估* ；`) — all spacing, not content. seed7: sidecar 9/10 WS 10/10 DSP; pypdf 7/10 WS **9/10 DSP**; raw 8/10 WS 9/10 DSP, the single de-spaced miss being L88 `全文浏览后符合纳入标准的文`, a cell run in the PRISMA-flow figure whose blocks pypdf emits in another order.

## 3. Hyphenation and line-wrap behaviour

* **JMLA: 3 lines end in `-`** — L187 `…review teams will pre-`, L258 `…10.1186/s13643-020-`, L261 `…and meta-`. The two word breaks resume in the same column, but the file puts left-column lines between the halves, so a de-hyphenating re-join in file order mixes columns; the DOI break is a mid-number break, not a hyphen.
* **`each information source` does NOT cross a wrap; the sentence does.** `count` = 2, offsets 1368 and 9081, both on one line. `PRISMA-S also recommends reporting the number of records identified from each information source` has count **0**: it breaks after `…PRISMA-S also recommends` (L21→L22) and the unique continuation `reporting the number of records identified from each information source.` is at **offset 1320**, count 1, one line. This is the sentence r40's `recheck:` asserts — the round-53 critic's defect reproduced independently.
* **CJK lines do split mid-word.** QCG: 545 breaks with CJK both sides, **272** joining a bigram that also occurs intact ≥3× (L53 splits `评价`, L91 `工作` 54×, L102 `规范` 49×); NMPA 340 / **123**. So a term can be unfindable whole: `所检索的` ends L699 and `数据库应包括多个中、英文专业数据库。` begins L700, giving count 0 for the joined sentence r48 attributes to the issued text.
* **Layout letter-spaces justified CJK**: 5 runs in the QCG (`随 机 对 照 试 验`, `临 床 实 践 指 南`), 2 in the NMPA (`基 本 药 物 目 录`). A quote copied from the visual page without those spaces is unfindable; byte-exact copying from the sidecar is mandatory. No U+FFFD, NUL or TAB in any sidecar.

## 4. Ligatures

`U+FB00–U+FB06` occur **0** times in every sidecar and every pypdf extraction, and `qpdf --qdf --object-streams=disable … | grep -c '/fi[^a-z]'` / `'/fl[^a-z]'` returns **0** for all three PDFs (control: 165 `/Font`, 9 `ToUnicode` objects in the NMPA QDF). None of these PDFs encodes ligature glyphs; nothing to expand, nothing lost. The JMLA's 40 `fi` / 57 `fl` are ordinary letter pairs.

## 5. Two-column interleave — and the staged sentences

The JMLA is two-column and `-layout` pairs the columns on one line where baselines meet and alternates them line by line where they do not (L114–L119 vs L101–L130). 88 of 326 lines (27.0 %) hold two blocks, carrying **10193 of 20285 body characters (50.2 %)**; QCG 56 lines (9.9 %) and NMPA 58 (16.9 %) are table cells and browser chrome. The artefact exists in both directions, proved on one sentence (JMLA, whitespace-normalised):

```
ARTEFACT  'should be reported matching inclusion criteria'   sidecar 1   pypdf 0
REAL      'other methods should be reported in Column 2'     sidecar 0   pypdf 1
```

The artefact is L78's right-column tail glued to L79's left-column line; the real sentence is split by the interleave (right-column L78 + L80, left-column L79 between). Staged strings tested (`sidecar / pypdf / raw`, whitespace-normalised; `–` = capture not involved):

```
r40 JMLA  the recommendation to report search strategies for all databases, registries, and websites that were searched  1 / 2 / 2  exact 0, wrap L20→L21
r40 JMLA  PRISMA-S also recommends reporting the number of records identified from each information source              1 / 1 / 1  exact 0, wrap L21→L22; tail @1320
r40 JMLA  the number of records identified from each information source                                                1 / 1 / 1  one line, offset 1320
r40 JMLA  individual databases and other information sources’                                                           1 / 1 / 1  one line, offset 10835
r40 JMLA  should be reported in Column 2                                                                                0 / 1 / 1  COLUMN INTERLEAVE (L78 + L80)
r40 JMLA  also suggests reporting an overall number for records identified from databases and registers in Column 1       0 / 1 / 1  COLUMN INTERLEAVE (L80 + L82 + L84)
r48 QCG   文献研究的质量控制                                                                                              1 / – / –   one line, offset 9940
r48 QCG   多个中、英文专业数据库                                                                                         1 / – / –   one line, offset 10366
r48 QCG   所检索的数据库应包括多个中、英文专业数据库                                                                      0 / – / –   CJK wrap L699→L700
r48 QCG   可根据评价主题确定纳入与排除标准                                                                                0 / 0 / 0   MISQUOTE; issued text reads 应…（offset 10170）
r48 NMPA  会议论文、未发表的学位论文、产业报告、咨询报告                                                                  1 / – / –   one line, offset 3348
r50 NMPA  图 2.文献筛选流程图（参考 PRISMA）                                                                              1 / – / –   one line, offset 3889
```

**Answer as asked:** no staged sentence I could test is a false interleave — none glues the two columns into a sentence the PDF never prints. The live failure is the inverse and it is fatal to a `text.find` substance check: two genuine r40 sentences (`should be reported in Column 2`, `also suggests reporting an overall number … in Column 1`) are **not contiguous in the text form at all**, and r40's `recheck:` sentence is unquotable whole. A scribe who repairs such a sentence by reading consecutive sidecar lines instead lands in the artefact direction.

## 6. Verdict per capture

* **0ae65ac01b93119d3c2f3fed (JMLA 1449/2061) — faithful-with-wraps.** Characters and pages identical (15983 stripped chars, 0/5 pages differ, multiset equal, 10/10 spans both seeds). Defect: two-column **block interleave** — 50.2 % of body characters sit in lines that pair or alternate the columns, so reading order is not the PDF's and quote contiguity is line-and-column dependent.
* **16fe8487aa97b98576a0dbac (质量控制指南 2024 试行) — faithful-with-wraps.** 20390 stripped chars, 0/42 pages differ, multiset equal, 10/10 spans both seeds, no ligatures, no FFFD. Defect: hard wrap at ≈34 CJK characters and inside table cells (272/545 breaks cut a word intact elsewhere), plus 5 letter-spaced CJK runs.
* **0435b64f65c3ea7ddc6bb92e (pharmwyp copy of the 2019 NMPA notice) — faithful-with-wraps.** 13630 stripped chars, 0/30 pages differ, multiset equal. Defect: a **browser print** — 58 lines (16.9 %) mix the page's own chrome (`2023/5/30 23:37`, `请输入关键字`, `…20190618165701432.html1/1`, `备案序号:京ICP备13027807号`) and the flow-figure cells are emitted in a block order other than the PDF's reading order (hence 7/10 WS at seed 53 against 10/10 de-spaced). The notice body itself is clean: `会议论文、未发表的学位论文、产业报告、咨询报告` @3348.

No capture is **unfaithful**: not one character differs from the independent extraction on any page.

## 7. What this means for C2 (reported, not patched — the claims are frozen)

(a) The spec's `pdftotext` sample check is circular; a fidelity note should rest on an engine that did not write the sidecar. (b) r40's two `Column` quotes and its `recheck:` sentence cannot be quoted whole from the text form, so an entry adopted unchanged will fail the located-quote / `inference-ground` leg on those three strings (binding is unaffected). (c) r48's `可根据评价主题确定纳入与排除标准` is a character-level misquote of the issued text (`应根据评价主题确定纳入与排除标准，可基于“PICOS”` @10170, count 1), so r48's own bookkeeping sentence ("应 becomes 可") is false of the issued capture — a substance defect the span machinery cannot see, because the quoted string is never found. (d) `灰色文献` = 0 and `PRISMA` = 0 in the QCG under both engines, so r50/r48's headline negatives survive.

VERDICT: I attacked the three C2 PDF text forms against an independent pypdf extraction — page counts, per-page character multisets, 60 sampled spans and the staged quote strings — and all three are faithful-with-wraps (JMLA two-column block interleave, QCG CJK/table hard wrap, NMPA browser-print block order), with no character lost but two genuine r40 sentences unreachable, one demonstrated interleave artefact and one r48 misquote (应→可).
