# R58ScoutS101Carriers — S101 §1.2.4

## Evidence and method

- Read frozen claims at `corpus/evidence/round58/claims.md` and the exact 12-row set at `corpus/evidence/round58/c2/quotes.tsv`; claims pin URL `https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc`, raw key `6dc68fd6b32ce9c8dfcebce8`, and SHA-256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`.
- No live network used. Ran the lane-pinned converter against only the committed raw capture: `TMPDIR=/fast/scratch/hyaku/chousa-r58/R58ScoutS101Carriers python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > /fast/scratch/hyaku/chousa-r58/R58ScoutS101Carriers/s101.txt`; observed `rc=0`, 469 lines / 47,356 bytes. Raw SHA matched claims; converter SHA matched `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`.
- Checked all quote strings against this output by exact substring search: 12 rows, 12 distinct strings, each occurs exactly once. Offsets are converter-output character offsets, zero-based: heading 315; §1.2.1 lead 330; electronic types phrase 590; carrier requirement 683; MT 734; OL 781; notation 797; M/CD example 838; J/OL 965; DB/OL 993; publication-fields phrase 1460; Document-code phrase 11723. Three quote starts are line-start-bound (315, 330, 993), consistent with the counter's anchor condition.

## Observed source wording

In the defined form, heading `1．2．4 电子文献的载体类型及其标识` (line 70) is followed by:

> 对于非纸张型载体的电子文献，当被引用为参考文献时需在参考文献类型标识中同时标明其载体类型。本规范建议采用双字母表示电子文献载体类型：磁带(magnetic tape)—MT，磁盘(disk)—DK，光盘(CD–ROM)—CD，联机网络(online)—OL，并以[文献类型标识/载体类型标识]表示包括了文献载体类型的参考文献类型标识：

Examples immediately following (lines 72–77):

- `如：[M/CD]—光盘图书(monograph on CD–ROM)；`
- `[DB/MT]—磁带数据库(database on magnetic tape)；`
- `[CP/DK]磁盘软件(computer program on disk)；` (no dash is present between `]` and `磁盘` in this defined form)
- `[J/OL]—网上期刊(serial online)；`
- `[DB/OL]—联机网上数据库(database online)；`
- `[EB/OL]—网上电子公告(electronic bulletin board online)。`

The section closes: `以纸张为载体的传统文献在引做参考文献时不必注明其载体类型。` Thus the stated carrier alphabet in this section is MT (magnetic tape), DK (disk), CD (CD–ROM), and OL (online network); bracket notation is `[文献类型标识/载体类型标识]`, exemplified by combinations such as `[M/CD]` and `[DB/OL]`. The source labels these as recommended two-letter carrier identifiers for non-paper electronic documents and says traditional paper-carrier items need no carrier type.

## Distinction and caveats

- The frozen quote set includes standalone exact quotes for `磁带(magnetic tape)—MT` and `联机网络(online)—OL`, but not standalone DK or CD strings. DK/CD occur in the larger §1.2.4 passage and in examples; the frozen `[M/CD]` quote plus its ±80-character bound span should be inspected for local context. Do not imply that DK/CD are independent rows in the frozen quote set.
- The defined form has a second, later section `14.3.4` (lines 261–267) with similar material but different wording/typography: it says `文献类型标志` / `载体类型标志` instead of §1.2.4's `…标识`, uses double em dashes `——`, and spells `CD-ROM` with ASCII hyphen. §1.2.4's `CD–ROM` uses U+2013 en dash; its separators `—` use U+2014 em dash. This is document-internal variation, not grounds to normalize the frozen quotes.
- §11 is separately headed `中图分类号(CLC number)与文献标志码(Document code)`. It defines five document-code categories A–E (A基础性理论与应用研究; B应用性技术成果报告/理论学习与社会实践札记; C业务指导与技术管理性文章; D一般动态性信息; E文件、资料), says unclassified articles and certain items get no document code, and gives `文献标志码：` / `Document code:` as the labels. That is an article classification mark, distinct in name and function from the bibliography's `文献类型标识/载体类型标识` pair; the quote `与文献标志码(Document code)` itself appears in a later heading, not §1.2.4.
- In §1.2.1, the converter preserves the single-letter table (M, C, N, J, D, R, S, P, G, B, O, K), despite the terminal's line-oriented rendering splitting table cells across lines. Claims concern source text presence, not whether these recommendations remain authoritative standards or are semantically/currently correct.
- Inference boundary: this capture establishes the document's wording and examples only. It does not establish present-day standards validity or truth beyond the captured document, as claims.md explicitly limits C2.

## Verification status

No C2 counter was run; this is a source-reading assignment, not a C2 result. No claim verdict is asserted.

VERDICT: S101 §1.2.4's carrier-alphabet and bracket-notation wording survives as located text in the frozen capture; no conclusion on standards truth or overall C2 predicate.