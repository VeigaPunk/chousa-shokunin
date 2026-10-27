# R58ScoutS101Section — S101 defined-form section map (round 58, C2 scout)

Scope: map the 12 frozen C2 quotes to section headings in the lane-held S101 `.doc`
capture's defined text form. No fetch; capture `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`
(sha256 `6063a3af…fddf3`, verified by `sha256sum` vs claims.md pin). Defined form generated in
scratch with the pinned tool (sha256 `2c0140bc…2573`, verified):

    TMPDIR=/fast/scratch/hyaku/chousa-r58/R58ScoutS101Section python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > defined-form.txt
    RC=0; form is 47356 bytes UTF-8, 411 lines.

## Document structure (observed)

The text form holds TWO parallel copies of the "中国学术期刊(光盘版)检索与评价数据规范（修订本）"
standard, distinguishable by numbering style and terminology:

- Part A (lines 1–~186): full-width-dot numbers `1`, `1．1`…`1．5`; uses `标识`
  ("identifier"). Title line 1; `1 参考文献` at line 3. Ends line ~186.
- Part B (lines ~187–411): ASCII-dot numbers `8`…`16`; uses `标志` ("mark"). A second title
  block (`中国学术期刊(光盘版)\n检索与评价数据规范\n（修订本）`, lines ~187–189) precedes
  `8 作者简介(Biography)` (line 190). Sections 2–7 of the B numbering are absent from the
  text form. Part B's `14.3` is a near-verbatim parallel of Part A's `1．2` but with
  `标志` wording and double em dashes `——` vs Part A's `—`.

## Quote → section map (offsets are code-point indices into the defined form; each occurs exactly once)

| # | Frozen quote (abbrev) | offset | line | line-start | Section |
|---|-----------------------|--------|------|------------|---------|
| Q1 | `1．2 参考文献类型及其标识` | 315 | 14 | yes | **§1．2** itself — heading "参考文献类型及其标识" (Reference types and their identifiers) |
| Q2 | `1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：` | 330 | 15 | yes | **§1．2．1** — GB3469 single-letter type alphabet |
| Q3 | `建议以下列双字母作为标识：` | 590 | 59 | no | **§1．2．3** — electronic-document double-letter types (DB/CP/EB) |
| Q4 | `被引用为参考文献时需在参考文献类型标识中同时标明其载体类型` | 683 | 71 | no | **§1．2．4** — electronic carrier types and identifiers |
| Q5 | `磁带(magnetic tape)—MT` | 734 | 71 | no | **§1．2．4** — carrier alphabet clause |
| Q6 | `联机网络(online)—OL` | 781 | 71 | no | **§1．2．4** — carrier alphabet clause |
| Q7 | `并以[文献类型标识/载体类型标识]表示` | 797 | 71 | no | **§1．2．4** — `[type/carrier]` notation clause |
| Q8 | `[M/CD]—光盘图书(monograph on CD–ROM)；` | 838 | 72 | no | **§1．2．4** — example list (first example, after `如：`) |
| Q9 | `[J/OL]—网上期刊(serial online)；` | 965 | 75 | no | **§1．2．4** — example list (indented item) |
| Q10 | `[DB/OL]—联机网上数据库(database online)；` | 993 | 76 | yes | **§1．2．4** — example list |
| Q11 | `出版地:出版者,出版年:起止页码(当整体引用时不注).` | 1460 | 82 | no | **§1．3** — inside the monograph format template `[序号] …` (line 82) |
| Q12 | `与文献标志码(Document code)` | 11723 | 210 | no | **§11** — Part B heading `11中图分类号(CLC number)与文献标志码(Document code)`; a substring, not the whole heading |

Line-start anchors: Q1, Q2, Q10 (3 of 12). All quotes unique (`n_occ=1`).

## Source text that limits interpretation

1. Carrier marking is scoped to non-paper electronic documents only. §1．2．4 line 71 opens
   `对于非纸张型载体的电子文献，当` + Q4 — the frozen Q4 string omits the `非纸张型载体的`
   (non-paper) qualifier. Line 78 adds `以纸张为载体的传统文献在引做参考文献时不必注明其载体类型`
   (paper-based traditional literature need not mark carrier type).
2. The carrier alphabet is double-letter: MT/DK/CD/OL per §1．2．4 (`本规范建议采用双字母表示
   电子文献载体类型`), distinct from the single-letter GB3469 type alphabet of §1．2．1
   (M C N J D R S P G B O K — 12 types incl. 档案 B and 古籍 O).
3. §11 文献标志码 (Document code) is a separate field with its own five-code alphabet
   A–E defined in §11.6 (A 基础性理论与应用研究 … E 文件、资料); §11.7 gives the
   `文献标志码：`/`Document code:` markers. Not part of GB3469's reference-type alphabet.
4. §15.5 (Part B) uses yet another code: `文献载体代码…根据GB 3469…P——印刷本，M——缩微制品`
   — a single-letter carrier code for the serial-parameters string, and it cross-references
   `电子文献的载体类型见14.3.4`. So the document holds two distinct carrier-code systems;
   an entry must not conflate the §15.5 P/M serial-parameter code with §1．2．4/§14．3．4
   MT/DK/CD/OL.
5. Part B parallel text does NOT collide with the frozen strings: §14．3．4 (line 261) says
   `文献类型标志中同时标明其载体类型` and uses `——` dashes and `[DB/OL]——网上数据库`
   (missing `联机`), so all Q4–Q10 bind uniquely to Part A wording. Q2's `标识以下` differs
   from §14．3．1's `根据 GB 3469…标志以下` (also has a space after 根据). Q3's `…作为标识：`
   differs from §14．3．3's `…作为标志：`. Q11 binds only to §1．3's template; §14．4．1's
   template inserts `（有编号的知名系列报告可不注出版地和出版者）`.
6. Part A `1．1` item c already lists `c. 文献类型及载体类型标识` as a citation element —
   support for treating type+carrier marking as part of the reference entry, not the article
   metadata fields (摘要/关键词/文献标志码).
7. Structural caveat: `1．4 外文文献的引用格式` (line 132) contains B-numbered fragments
   `14.1 中文参考文献的英译表达` (line 168) and `14.2 文献重复引用标记` (line 174) —
   earlier-draft parallels of Part B §14.6/§14.7. Also a misrendered `2.1` for `12.1`
   at line 229. The capture is a merged two-draft document; section numbers cited for a
   quote should name the draft (A `1．x` vs B `N.x`) to avoid ambiguity.
8. `[CP/DK]磁盘软件` in §1．2．4 (line 74) lacks the em dash that Part B's `[CP/DK]——磁盘软件`
   has — a source defect if quoted verbatim.

## Unrun / not performed

- No counter run (scout task only; `c2-count.py` not executed by this seat — unrun).
- No live fetch of the URL (not authorized); all offsets from the committed capture.
- Knowledge entry `corpus/knowledge/carrier-alphabet-china-r58.md` not inspected for
  existence (out of scope; section map only).

VERDICT: C2 S101 carrier-alphabet section mapping — 11 quotes bind to Part A §1．2．1/§1．2．3/§1．2．4/§1．3 (标识 draft), 1 quote to Part B §11 (文献标志码 document code); uniqueness confirmed against the §14.3 标志 parallel; scope limits = non-paper-only carrier marking, double-letter carriers vs single-letter types vs A–E document codes vs P/M serial-parameter carrier code. survives (mapping complete, evidence reproducible from the pinned capture).
