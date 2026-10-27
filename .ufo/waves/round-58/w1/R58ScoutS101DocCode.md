# R58ScoutS101DocCode — S101 §11 document-code field vs type/carrier labels

Seat scope: check §11's separate 文献标志码 (Document code) field against frozen quote
`与文献标志码(Document code)`; report what the source says and whether the contrast
with the GB3469 type/carrier labels is justified. Read-only source access; no fetch.

## Verification run (scratch: /fast/scratch/hyaku/chousa-r58/R58ScoutS101DocCode/)

- `sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` →
  `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` — matches claims.md.
- `sha256sum tools/capture-text.py` → `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` — matches pin.
- `python3 tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` →
  defined form, 27,012 chars (receipt s101-open.txt says 27,012 — match).
- Frozen quote `与文献标志码(Document code)`: `find` → offset 11723, `count` → 1. It is the
  tail of the §11 heading `11中图分类号(CLC number)与文献标志码(Document code)` (heading at
  11704, ends newline; `文献标志码(Document code)` alone at 11724). The seat-task rendering
  `(CLC number)与文献标志码(Document code)` is the full heading minus `中图分类号`/`11`;
  the frozen quote itself is exactly `与文献标志码(Document code)`.

## What §11 (chars 11704–12308) actually says

- 11.1 `具有文献标志码的文章应标注分类号。` — articles *having* a document code must carry
  a CLC number (code → CLC-number gating, not vice versa).
- 11.2–11.5: CLC-number rules (《中国图书馆分类法》第四版; 1–3 codes, `中图分类号：` /
  `CLC number:` prefix; example `中图分类号：TK730.2；O357.5`).
- 11.6: document-code purpose — `为便于文献的统计和期刊评价…每一篇文章或资料应根据其内容性质
  标识一个文献标志码。本规范共设置以下五种：` then the A–E alphabet:
  A 基础性理论与应用研究 / B 应用性技术成果报告(科技)、理论学习与社会实践扎记(社科) /
  C 业务指导与技术管理性文章 / D 一般动态性信息 / E 文件、资料. Closing line: digests,
  fillers, ads `等不加文献标志码` — the field is conditional, not mandatory.
- 11.7: front-matter marker `文献标志码： A` (English `Document code:`), e.g.
  `文献标志码： A` — a labelled colon field, not bracketed.
- §15.6: `文章总篇数…为发表在本期中具有文献标志码的文章的总和,据此计算载文量` — the code
  also defines which articles count toward a journal's article total.
- Appendix A, Table A1 (char ~25867): `文献标志码： Article character: 接排分类号之后
  (前空三个汉字)` — the field is set immediately after the CLC number, and Table A1 gives
  it a *different* English label (`Article character`, not `Document code`). Table A2's
  column header row maps article classes to `文献标志码 A B C D E ?` — the A–E set again,
  with `?` for 其他 (uncoded articles).

## Contrast with §1.2 type/carrier labels — justified?

Yes, on the source's own text; the two systems are disjoint in every dimension:

- Location/scope: §1.2 alphabet is inside `参考文献` (cited references); §11 is a
  front-matter metadata field of the host article. 11.1 even predicates the CLC number
  on possessing a document code — the code is article-level, label-level is citation-level.
- Governing norm: §1.2 `根据GB3469规定` (type letters M C N J D R S P G B O K, Z for
  others; DB CP EB electronic types; MT DK CD OL carriers; `[文献类型标识/载体类型标识]`
  notation). §11's A–E set is `本规范共设置` — defined by this specification itself, not
  by GB3469. `载体类型标识`/`文献类型标识` never appear in §11 (occurrences at 631–3253
  and §14.3.4 only).
- Surface form: `[J/OL]`-style bracket appendage inside a citation vs `文献标志码： A`
  colon-labelled field after the CLC number.
- Collision risk is real, which is *why* the contrast matters: letters D, B, C mean
  different things in the two alphabets (§1.2: D=学位论文, B=档案, C=会议论文;
  §11.6: D=一般动态性信息, B=应用性成果/理论学习, C=业务指导管理类). Confusing the two
  fields would corrupt both the citation list and the article's metadata.
- Nuance to carry into the entry: §11 couples CLC number and document code (one heading,
  11.1 gating, Table A1 adjacent placement `接排分类号之后`), so "separate field" means a
  distinct labelled field — not an independent one. Also the source is internally
  inconsistent on the English name (`Document code:` in §11 vs `Article character:` in
  Table A1); an entry pinning the label should quote §11.7 and note the Table A1 variant.

## Terminology note

The source uses `文献标志码` everywhere (15 hits); `文献标识码` (common real-world
variant) never occurs — text form has zero hits. Any entry phrasing must use 标志码.

## Residual unknowns / unrun checks

- Not checked: whether the built entry `corpus/knowledge/carrier-alphabet-china-r58.md`
  phrases this contrast correctly (build wave pending; not this seat's question).
- `c2-count.py` not run by this seat; quote offset verified by direct `find`/`count`
  on the defined form, consistent with s101-open.txt.
- Scratch dir /fast/scratch/hyaku/chousa-r58/R58ScoutS101DocCode removed after writing
  this report. No installs performed; tooling authorization not invoked.

VERDICT: S101 document-code contrast — survives: §11 defines a separate A–E
`文献标志码`(Document code) field disjoint from the §1.2 GB3469 type/`[type/carrier]`
labels (different governing text, surface form, and attachment point), with real letter
collisions (D, B, C) making the contrast substantive; caveats — §11 couples the code to
the CLC number (11.1 gating, Table A1 places it `接排分类号之后`) and Table A1 names it
`Article character`, so "separate" must be reported as distinct-field-not-independent.
