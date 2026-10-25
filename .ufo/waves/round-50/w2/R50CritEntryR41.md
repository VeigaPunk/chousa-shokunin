# R50CritEntryR41 — attack on `corpus/knowledge/citation-matching-semantics-r41.md`

Lane commit `74794db07e1b383d5c3e96ad5122fd158a541271`; entry 31 lines. Captures read as UTF-8 from
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/` (S105 `e3ca8f4fdd15420b80096a75`, 83,384 B;
S106 `28750bcdf5d36cd90a7709fb`, 63,869 B; each `.raw` is the PDF, 57 and 65 pages). No network; no lane write outside
this report. Scratch `/dev/shm/chousa-r50-R50CritEntryR41/` deleted.

## Reproduction — every count in the entry is exact

Ran the `recheck:` line verbatim: `38174 0 4 5 0` / `30937 0 0 0 0`; slice sweep `30727 31262 535 [0, 0, 0, 0, 0, 0, 0, 0]`.
All twelve `char N` anchors resolve to the start of the quoted text, each quote occurring once (`t.find` = listed offset,
`t.count` = 1): S105 48/30738/30778/30793/30880/30947/31101/31218/31273, S106 83/22511/22549. `第 6 章 辅助功能` occurs
once (30661) — checked because it recurs as a page header. A 30-word wider sweep of 30727–31262 found `搜索 2, 自动 1,
作者 1` and nothing else.

## Decisive counterexample: §6.1 does publish which parts are compared — in its screenshots

The `.txt` form drops the section's images (4 blank-line runs in the slice; `pdfimages -list -f 42 -l 43` shows four
large JPEGs on p. 42 and the tooltip JPEGs on p. 43). Rendering PDF p. 43 (= printed 38, where the orange and green
states sit) at 300 dpi and reading the extracted objects gives the two hover tooltips:
- orange state, embedded JPEG `img-004.jpg` 185×59: `篇名相同,作者相同,刊名不同`
- green state, embedded JPEG `img-006.jpg` 194×69: `篇名相同,作者相同,刊名相同`

Neither string is in the text form (`篇名相同` 0, `刊名` 0 in the whole 83,384-char `.txt`; `pdftotext -f 43 -l 43` yields
neither). The section therefore publishes a field set — 篇名, 作者, 刊名, each graded 相同/不同 — with no 年/卷/期/页码
part, no ordering and no threshold. These are image-borne: they cannot be recorded as located `.txt` quotes and the C2
manifest is blind to them by construction — a manifest limit to state, not a predicate to change. Consequence:
`The section publishes no method` (line 14) and Inference 2's `nothing more specific` are falsified at section level.
The sweep is not wrong; it is scoped to a form that excludes the evidence.

## Claim-by-claim

1. l.12 definition + three states, input step, list columns — survives; offsets exact; the same sentence also documents
   `点击“搜索”按钮`.
2. l.13 `The three states grade one returned record` — defect: state 1 is 没找到, so no record exists to grade.
3. l.14 `The section publishes no method` — defect, above; 搜索 2 / 自动 1 are a published procedure.
4. l.14 比对 as the section's verb and §6.2's document-to-document 比对 — survives (30778, 31273).
5. l.15 first-author option a folder property in **both** manuals — survives: S105 §3.7 at 27587 under 第 3 章 检测结果
   (13557) with 3.7.1–3.7.3 all folder-scoped; S106 §2.6 at 22511 `创建文件夹页面`; `仅去除第一作者本人` 11× in S105
   all ch.3/TOC, 9× in S106 all §2.6 — no per-document variant anywhere.
6. l.16 S106 has no 引文核对 and no 辅助 — survives literally (0/0); see O9.
7. l.16 `查重` is not the manuals' word — survives for these copies (0/0); S105's own word is 检测 (343×).
8. l.17 `The two feature texts do not meet` — undefined predicate, tested one direction only; see O7.
9. Inference 4 product fact (two products, S106 ≠ S105) — survives by title blocks; evidence pointer wrong (O10).
10. Inference 1 `Catalogue lookup, then a part-by-part verdict` — partly stronger, partly weaker (O3/O4).

## Overclaims and proposed narrowed wording

O1 — line 14 headline. Replace `The section publishes no method.` with:
> The section's text form publishes no matching rule. Its screenshots (PDF p. 43, printed 38) name the compared
> parts — 篇名, 作者, 刊名, each graded 相同/不同 — and no ordering, threshold, normalisation or candidate rule
> appears in the section in either form.
O2 — line 14 evidence sentence, after `535 characters`:
> in the `.txt` form — the 8-word sweep cannot see the section's images, where the field selection is published; it
> supports "no ranking/weight/ratio word in the text", not "no method".
O3 — Inference 1. `catalogue` is the staged claim's word, not the copy's (`文献资源`):
> A search of CNKI's own literature resource (`引文核对是指，以“中国知网”的文献资源为核对源内容`, char 30738)
> returns one record, graded in three states; when a record is found but the citation differs, the hover names which
> of 篇名, 作者, 刊名 differ. That is the whole of what this copy states.
O4 — title. `part by part` conflates verdict granularity (per citation) with diagnosis granularity (three parts):
> CNKI's 引文核对 searches CNKI's literature resource for a pasted citation, grades the match in three states, and
> names which of 篇名, 作者, 刊名 differs.
O5 — line 13 headline → `The three states grade one input citation against the record the search returns — or none (没找到).`
O6 — Inference 2: `no matching method is stated anywhere in it` — `it` reads as the copy, and the copy uses `相似度` 3× (18007, 18772, 25567, about 复制比/跨语言检测) → `in the §6.1 slice`.
O7 — line 17, give `do not meet` a testable meaning and test both directions:
> Do not meet = neither text carries a cross-reference token to the other and neither carries the other's feature
> term: §6.1 (30727–31262) has 文件夹 0, 属性 0, 去除 0, 复制比 0, 参见 0; §3.7's body (27569–28349) has 引文 0,
> 核对 0, 辅助 0, 参见 0. This is a statement about the two texts, not about the product's behaviour.
O8 — line 16: `so 查重 is not the manuals' own word either` generalises from two copies and omits the word used →
`neither of these two copies uses 查重 (0/0); S105's own word for the flow is 检测 (343×).`
O9 — line 16: `documents no 引文核对` is true, but S106's `引文` occurs 10× (3509, 13948, 19247, 20218, 21064, 21085,
21112, 21283, 21373, 21618), all inside `全文（标明引文）报告单`, a report form that marks in-text citations. Add:
`引文 occurs 10 times in this copy, only as 全文（标明引文）报告单, a report type, not a citation check.` Without it the
absence reads as "no citation feature".
O10 — Inference 4 pointer: `第 6 章 辅助功能` (char 30661) is a chapter heading and does not name the product; the name
is at char 0 (title block `知网学位论文学术不端行为检测系统 … （管理员）`) and char 115 (page-1 header). Also
`a different product` should say same vendor: S106 carries 同方知网, `产品版本 V5.0`, `2014-03-10`; S105 is 2020-07.
→ cite char 0 and write `a different product of the same vendor`.
O11 — Inference 4 close: `only the 学位论文检测系统's 管理员 copy documents it` reads as a role claim (S105 mentions
子账号 32×) → `among the copies opened this round, only S105 documents it`.
O12 — line 12: `The one documented input step` — the same sentence documents the 搜索 click → `The only input step is the paste; a 搜索 click starts the automatic check.`

## `recheck:` line defects

R1 — `then re-download the three copies`, but the entry binds **two** copies (2 `source:` lines). Carried over: the
staged entry's recheck read `re-download all three manuals` when it bound S135/S136/S145. Fix to `the two bound
copies`; the re-download step cannot run this round (L0 `8d77e6c1` open, no network).
R2 — the slice sweep has no guard: if a re-flow moves the heading before char 30000, `find` returns −1 and the command
prints `-1 -1 0 [0, 0, 0, 0, 0, 0, 0, 0]` (observed) — an all-zero result a rechecker reads as "no method words". Append
`assert s>0<e`, or print `SLICE=FAIL`.
R3 — the occurrence sweep omits `引文`, the one word that would surface O9 (10× in S106); add it.

## Provenance

`diff` staged `merge/chousa/knowledge/corpus/knowledge/citation-matching-semantics-r41.md` vs landed: 21+/43−, id map
S135→S105, S136→S106, S145 dropped, `ground` Q16→PROVINCE.md, `adopted:` added. The staged negatives (`CNKI publishes
no matching algorithm`, `no field-selection or ranking rule is published`) and the staged title's `catalogue lookup`
survived — O1/O3 are inherited. The staged title also claimed `field comparison`, which the tooltips support; the
landing dropped that while keeping the denial, so the entry lost its strongest true fact and kept its weakest false one.

## What found nothing (attacks that failed)

- Wider vocabulary sweep of the slice (30 words incl. 检索/题名/年份/卷/期/页码/规则/标准/阈值/精确/模糊/数据库/题录/
  校验/逐条/字符串/相似): only `搜索 2, 自动 1, 作者 1` — no ranking, weight, threshold or algorithm word in the text.
- Per-document variant of the first-author option: none (11× S105 ch.3/TOC, 9× S106 §2.6). Claim 5 stands.
- Cross-reference between the two features: 参见/如上/前述/相关 = 0 in both bodies. O7 is a wording defect, not a false
  claim.
- `引文核对`/`辅助` in S106: 0/0, re-run and confirmed.
- `spans.tsv` S105 offsets (flagged by R50ReopenRowS105, then retracted): the −80 is `CONTEXT` in `build-spans.py`, and
  `capture[off:off+len(span)] == span_file` exactly for S105-1..4 (48-clamp on the head row). No defect there; the
  entry's `char N` values are quote positions and match the capture, so entry and manifest agree.
Entry survives as sourced; twelve wording fixes (O1–O12) and three recheck fixes (R1–R3) before the Gate reads it. O1
is the one that matters: as landed the entry asserts a section-level absence that the section contradicts in its own
screenshots.

VERDICT — attacked `citation-matching-semantics-r41.md` claim by claim (all 12 anchors, all 5 counts, the §3.7/§2.6
folder-property claim, the product fact, the "do not meet" predicate, the "catalogue/part-by-part" inference): defect
found — `The section publishes no method` and Inference 1's `nothing more specific` are falsified by §6.1's own tooltip
screenshots (篇名/作者/刊名 graded 相同/不同, PDF p. 43, no text layer), with secondary defects in the `three copies`
recheck carry-over, the unguarded sweep, the misplaced product-name anchor (char 30661) and the one-record headline.
