# R58ScoutS101Electronic — S101 electronic-reference types vs carriers (frozen quote set)

Question: does the frozen 12-quote set support an entry distinguishing S101's electronic
document types (DB/CP/EB) from electronic carrier identifiers (MT/DK/CD/OL)?
Answer: yes for the full mapping if the entry is grounded on the ±80-char span windows;
no for strict quote-verbatim support of CP, EB, and DK. No fetch performed.

## Evidence chain (verified)

- `sha256 corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` = `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` — matches claims.md RAW_SHA.
- `tools/capture-text.py` sha256 = `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` — matches CT_SHA.
- Lane tip `5da0a6375a55…` (freeze `9e73a03` + 2 commits: controls receipt, S101 pin). Base `b13ca7b5…` per claims.
- Defined form produced in scratch: `python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` → 47356 bytes UTF-8, sha256 `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867` (the committed `.txt` beside the raw is a different, 157816-byte artifact — not the defined form; offsets below are defined-form char offsets).
- All 12 frozen quotes: exactly 1 occurrence each in the defined form; offsets 315,330,590,683,734,781,797,838,965,993,1460,11723. Line-start-anchored: Q1(315), Q2(330), Q10(993) → anchors=3/12, meets ≥3 floor.

## The section (defined-form lines 59–78, §1.2.3–1.2.4)

- §1.2.3 (line 59–68): 数据库(database)、计算机程序(computer program)、电子公告(electronic
  bulletin board) → electronic types, double-letter codes DB / CP / EB ("建议以下列双字母作为标识").
- §1.2.4 (line 70–78): carriers 磁带(magnetic tape)—MT，磁盘(disk)—DK，光盘(CD–ROM)—CD，
  联机网络(online)—OL，notation `[文献类型标识/载体类型标识]`; examples [M/CD], [DB/MT],
  [CP/DK], [J/OL], [DB/OL], [EB/OL]. Paper-carrier docs need no carrier mark.
- A second, near-duplicate block exists at §14.3.3–14.3.4 (lines 257–265) using 标志
  instead of 标识 and —— dashes; frozen quotes all bind to §1.2 occurrences (unique).

## Support audit (token → frozen quote / span window)

Span window = `form[off-80 : off+len(quote)+80]` per c2-count.py lines 105–108.

- Fully quote-bound: MT (Q5), OL (Q6), the `[type/carrier]` notation rule (Q7),
  examples [M/CD] (Q8), [J/OL] (Q9), [DB/OL] (Q10); GB3469/单字母 frame (Q2);
  双字母 frame (Q3); carrier-marking rule (Q4).
- DB: name 数据库/database and code appear inside quotes only via `[DB/OL]…(database
  online)` (Q10); the DB↔数据库 type-table link exists in Q3's span window
  (`数据库⏎计算机程序⏎电子公告⏎⏎电子文献类型标识⏎DB⏎CP⏎EB`) and in [DB/MT] context of Q8.
- CP: NO frozen quote contains `CP`, `计算机程序`, or `computer program`. Support only
  via span windows of Q3/Q4 (type table) and Q8/Q9/Q10 (the `[CP/DK]磁盘软件(computer
  program on disk)` example, which is itself unquoted — note source prints it without
  the `—` used by sibling examples).
- EB: same — no quote contains `EB`, `电子公告`, or `electronic bulletin board`.
  Support only via Q3/Q4 spans (type table) and Q9/Q10 spans (`[EB/OL]—网上电子公告
  (electronic bulletin board online)`).
- DK: no quote contains `DK`, `磁盘`, or bare `disk`; supported only via spans Q4–Q8
  (full carrier list text sits inside Q5/Q6/Q7 windows since Q5+Q6+Q7 tile line 71).
- CD: carrier name 光盘 quoted only inside `[M/CD]` (Q8); the `光盘(CD–ROM)—CD` mapping
  is inside Q5–Q7 span windows.
- Missing entirely from quote AND span ground: single-letter codes other than M —
  the 1.2.1 table (M C N J D R S P G B O K) and catch-all "Z" (§1.2.2) lie outside
  every span window; worked examples [N/OL], [P/OL], [CP/DK] (line-161 bibliography
  instance), [DB/CD] are outside all spans. The five 文献标志码 values A–E (§11.6)
  also outside all spans — Q12 supports only that the Document-code field exists as
  a separate numbered section (§11), ~11k chars away from §1.2.
- Q11 (`出版地:出版者,出版年:起止页码…`) binds a print-format template line, not the
  electronic-record rule (§j line 124–131, incl. `[DB/CD]` example, is outside spans).

## Intra-document inconsistency worth citing

Defined-form §1.2.1 table lists 档案→B, 古籍→O, 参考工具→K (codes B,O present); §14.3.1
table omits 档案/古籍 and lists 参考工具→K. An entry enumerating the single-letter
alphabet can only assert "M" from span ground anyway (other letters ungrounded).

## Verdict-relevant findings

1. The entry can distinguish electronic types (DB/CP/EB) from carriers (MT/DK/CD/OL)
   only if it grounds type/carrier tokens on span context, not on verbatim quotes:
   8/12 intended distinctions (CP, EB, DK; plus example forms [DB/MT],[CP/DK],[EB/OL],
   [DB/CD]) have zero quote-level presence. A reviewer requiring "each mapping in a
   quoted string" would find support missing for CP=计算机程序, EB=电子公告, DK=磁盘.
2. Sufficient under the counter's actual mechanics: all required tokens occur
   verbatim inside committed-span byte ranges (Q3–Q10 windows), so SUBSTANCE and
   INFERENCE_GROUND can pass — but any claim like "the document codes programs CP"
   must cite a span, since no quote pins CP↔计算机程序 directly.
3. Unsupportable-by-S101-set claims to avoid in the entry: the full GB3469
   single-letter alphabet beyond M; the "Z" fallback; N/OL, P/OL, DB/CD real-world
   examples; the five document-code values; the §j OL citation-date rule (its
   sentence is outside every span window).

Unrun: c2-count.py end-to-end (needs built entry/manifest — wave work, not mine).

VERDICT: S101 electronic-type vs carrier separation — survives on span-level ground;
falsified only if the entry claims quote-level support for CP/EB/DK mappings or cites
single-letter codes, Z, document-code values, or non-span examples.
