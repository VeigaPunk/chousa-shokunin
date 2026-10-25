# GroundS104 — Round 49 W1: re-ground staged row S103 (S104 after renumbering)

## Assignment
Re-ground staged row S103 (lane id S104) — URL https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf — cited by the staged entry `merge/chousa/knowledge/corpus/knowledge/citation-count-semantics-r37.md`. Draft the lane Gate block for this row (quotes ≤25 whitespace words, ≤160 chars, exactly-once occurrence, byte-exact, with char offsets in the .txt form). Ground every claim that rests on this row. Confirm the absent-defect register names no such URL.

## Files opened
- Stage: `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/citation-count-semantics-r37.md` (line 7: `source: S103 — ... — section 2.1 and the result-field list — PDF read 2026-10-23`; Observation bullet 4 and Inference bullets rely on this row).
- Capture .txt: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/02aefcf570a7108e699d0990.txt` (22,631 bytes, 586 lines; read in full).
- Capture .raw: same qcache, `file` → `PDF document, version 1.7, 36 page(s)` (6,550,066 bytes). The .raw is the original PDF, so the UTF-16LE branch does not apply; the .txt is the sole text form.
- `renumber.tsv` line 10: `S103 S104 append library.um.edu.mo/...c1b0fa89e2809581b12c79b9c60ea1af.pdf` (mapping confirmed).
- Staged `append.md` row S104 (line 9): same URL, `section 2.1 文献溯源模式 and the result-field list`.

## Absent-defect register check (grep, both run)
`grep` pattern `c1b0fa89e2809581b12c79b9c60ea1af|library\.um\.edu\.mo` on `absent-defect-register.md` → **No matches found**.
`grep` pattern `um\.edu\.mo|02aefcf570a7108e699d0990` → **No matches found**.
No absent-defect register row names this URL.

## Quote location (python3 via eval; file read as UTF-8)
```
t = open(".../02aefcf570a7108e699d0990.txt", encoding="utf-8").read()
```
Observed counts/offsets (`t.count(q)`, `t.find(q)`):
- Q1 `CNKI AI 根据相关文献，生成可信增强回答。` → count=1, offset=892, 24 chars, 3 ws words
- Q2 `文献的标题、摘要、作者、出版日期、文献来源、来源数据库、引用量以及下载` → count=1, offset=931, 35 chars, 1 ws word
- Q3 `相关度、发表时间、被引次数和下载量` → count=1, offset=3175, 17 chars, 1 ws word
- Q4 `序方式从高到低进行结果排序。` → count=1, offset=3197, 14 chars, 1 ws word
All ≤25 whitespace words, ≤160 chars, each occurring exactly once in the .txt form.

PDF-extraction line folds (bytes verified via `repr`): Q2 is followed by `'\n\x0c量。点击右侧'` — the panel sentence completes as `…引用量以及下载\n\x0c量。` (form-feed = page break; `量` at char 968, `。` at 969). Q3 is followed by `'四种排\n\n序方式从高到低进行结果排序。'` — Q3 and Q4 are the two halves of one sentence, `并按照相关度、发表时间、被引次数和下载量四种排\n\n序方式从高到低进行结果排序。`.

## Gate block draft (row S103 → lane S104)
- URL: https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf
- Access date: 2026-10-25
- Quotes (form: `.txt`; offsets from `text.find`):
  - Q1 @ 892: `CNKI AI 根据相关文献，生成可信增强回答。`
  - Q2 @ 931: `文献的标题、摘要、作者、出版日期、文献来源、来源数据库、引用量以及下载` (sentence tail `量。` at chars 968–969 after a page-break fold)
  - Q3 @ 3175: `相关度、发表时间、被引次数和下载量`
  - Q4 @ 3197: `序方式从高到低进行结果排序。`
- Context: 中国知网AI使用指南 (CNKI AI User Guide), 澳門科技大學圖書館 copy.

## Claim-by-claim support (staged entry claims resting on this row)
1. "溯源 mode 根据相关文献，生成可信增强回答" — **supported**: Q1 verbatim (offset 892), section 2.1 文献溯源模式.
2. Traced-source panel fields 标题/摘要/作者/出版日期/文献来源/来源数据库/引用量/下载量 — **supported**: Q2 lists all eight fields in the claimed order (title, abstract, author, publication date, source, source database, citation count, download count); the sentence finishes `量。` at chars 968–969.
3. Sorting by 相关度/发表时间/被引次数/下载量 — **supported**: Q3 gives exactly these four keys; Q4 (`从高到低进行结果排序`) confirms the ordering mechanism. Location note: this sentence sits in section 3.1.1 文献检索 (result-field list), not 2.1 — the entry's "section 2.1 and the result-field list" attribution is still within the same capture and the claim itself is fully supported.
4. Inference "exposes 引用量 per source" — **supported**: Q2 includes 引用量 among the panel fields.
5. Inference "溯源 mode answers from literature and shows documents used" — **supported**: Q1 plus the panel sentence (Q2).

No claim resting on this row is narrower or unsupported.

## anchor cell draft
`2.1 文献溯源模式` → `char 892` (Q1), `char 931` (Q2; sentence tail `量。` at `char 968`–`969`); `3.1.1 文献检索` → `char 3175` (Q3), `char 3197` (Q4).

## Tooling
No installs made (none expected; RULES.md read). No scratch created.

## VERDICT
Re-grounded staged row S103 (S104) via four unique byte-exact quotes in the .txt capture (offsets 892/931/3175/3197); all staged claims resting on the row supported; register grep clean; Gate block + anchor drafted.
