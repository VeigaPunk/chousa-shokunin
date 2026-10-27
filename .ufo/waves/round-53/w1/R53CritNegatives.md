# R53CritNegatives — falsification of staged negative claims (round 53 wave 1)

Seat: R53CritNegatives. Scratch: /fast/scratch/hyaku/chousa-r53/R53CritNegatives (TMPDIR exported there; no
installs needed — RULES.md read, no pacman/uv action taken). Captures opened (read-only qcache, normalized = all
whitespace stripped): Jmla=0ae65ac01b93119d3c2f3fed.txt (27659 raw / 15983 norm), Cochrane=c9d1e74c3ac8d9eb332c9770.txt
(210708 / 176917), QcgPdf=16fe8487aa97b98576a0dbac.txt (**27609 raw / 20390 norm**), QcgNotice=cfa080b4046592eb9490a82c.txt
(1255 / 726), NmpaCopy=0435b64f65c3ea7ddc6bb92e.txt (21573 / 13630).

Sweep driver (run in eval, py):

```python
import re, os
Q='/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache'
caps={'Jmla':'0ae65ac01b93119d3c2f3fed.txt','Cochrane':'c9d1e74c3ac8d9eb332c9770.txt',
 'QcgPdf':'16fe8487aa97b98576a0dbac.txt','QcgNotice':'cfa080b4046592eb9490a82c.txt',
 'NmpaCopy':'0435b64f65c3ea7ddc6bb92e.txt'}
txt={k:open(os.path.join(Q,v),encoding='utf-8').read() for k,v in caps.items()}
norm={k:re.sub(r'\s+','',t) for k,t in txt.items()}
def cnt(k,t,ci=False): return norm[k].lower().count(t.lower()) if ci else norm[k].count(t)
```

## 1. search-tracking-record-r40.md negatives

| Claim (loc) | Sweep (terms/form/count) | Observed | Verdict |
|---|---|---|---|
| "not a checklist" (L49-50) | Jmla `checklist`, `checklists` (raw+norm, ci) | 0, 0 | supported |
| "is not itself a reporting standard; its authority is explanatory" (L51-52) | Jmla `reporting standard(s)`, `standard`, `commentary` | 0,0,0,2 | supported at token level; `reporting guideline(s)`=2 refers to PRISMA 2020/PRISMA-S, not this paper |
| "No non-Western analogue … was found; … neither places them in a numbered record with a per-source count" (L53-56) | scan all five captures for any placement of grey/unpublished items in numbered per-source records | none found; QcgPdf 灰色文献/灰色/未发表/内部资料/期刊评审 all 0; NmpaCopy mandates 会议论文、未发表的学位论文 but in an extraction table, no numbered record | **OVERREACH**: corpus-wide search-negative; S114/S130 Japanese sources not among the five captures. Narrow: "none of this round's five opened captures places grey or hand-search items in a numbered record with a per-source count" |

**Defect found (quote/recheck claim):** r40's recheck line asserts the sentence "PRISMA-S also recommends reporting the number of records identified from each information source" still reads as printed. In the capture it crosses a line break: raw offset 1288 starts "PRISMA-S also recommends", newline at 1312, continuation "reporting the number of records identified from each information source." @1320 (10 words, 72 chars, occurs exactly once). Same for "the recommendation to report search strategies for all databases, registries, and websites that were searched" (raw 0, norm 1). So the sentence is present (normalized count 1, offset 772) but **lies on no single line** — C2's located-quote rule forces cutting at the break; the unique continuation fragment @1320 is the valid quote.

## 2. western-instrument-alignment-r50.md negatives

| Claim (loc) | Sweep (terms/form/count) | Observed | Verdict |
|---|---|---|---|
| **Title L8**: "The alignment between the two traditions exists only in the western handbook's own voice" | Cochrane: `aligns with the current reporting guidance for PRISMA … and PRISMA-S` @13494 (exists); QcgPdf: PRISMA/PRISMA-S/对齐/保持一致 = 0 | western voice confirmed; QcgPdf silent | **OVERREACH / counterexample** — NmpaCopy (Chinese regulatory guidance, same clinical domain, S190) states "参考 PRISMA" (figure caption @3901) and **"撰写报告时应当逐一对照清单条目"** (@7797, "when writing reports, compare item-by-item against the checklist items" of PRISMA/MOOSE) — a Chinese voice stating method-attachment to PRISMA. "Only in the western handbook's own voice" holds only scoped to **PRISMA-S** and to QcgPdf alone |
| "PRISMA counts 0" over "27,609-character extraction" (L34) | QcgPdf `PRISMA` ci raw+norm; OCR-variant regex `P\s*R\s*[Ii1l]\s*S\s*M\s*A` (ci); len() | 0,0, none, **27609** | supported exactly |
| "never names PRISMA-S at all" (L43) | QcgPdf `PRISMA-S` ci | 0 | supported |
| "nothing in the corpus shows a methodological document on the Chinese side standing in relation to PRISMA-S, because no such document does" (L47-49) | all captures `PRISMA-S` | QcgPdf/QcgNotice/NmpaCopy = 0; Jmla 28, Cochrane 11 | **OVERREACH** (corpus-wide; NmpaCopy stands in relation to PRISMA, 10×). Narrow: "among the documents opened this round, none names PRISMA-S; the NMPA copy does name PRISMA" |
| "the Chinese instrument is not a PRISMA-S document at all" (L50) | QcgPdf PRISMA-S=0; Cochrane 11×, AMSTAR 3×, GRADE 1× (reference pattern) | supported for QcgPdf | narrow to "the issued guideline's text" |
| "has no field for them at all: 灰色文献, 未发表, 内部资料 and 期刊评审 each count 0" (L57-58) | QcgPdf counts | 0,0,0,0 | supported |
| "nothing in its instrument points at the evidence a systematic review is supposed to weigh" (L60) | token scan | no grey/unpublished tokens | supported at token level; normative phrase "supposed to weigh" not sweepable -> narrow: "the issued guideline's extracted text contains no token naming grey literature or unpublished evidence" |
| "the Chinese half cannot [say it] … only gestures at" (L64-65) | see title row | NmpaCopy does state PRISMA attachment | **OVERREACH**; QcgPdf's gesture is to Cochrane (指标 4 @18064: "是否参照 Cochrane 等组织制定的相应规范或指南开展文献检索") |

## 3. quality-control-guideline-issued-text-r48.md negatives

| Claim (loc) | Sweep (terms/form/count) | Observed | Verdict |
|---|---|---|---|
| "27,609 characters … 灰色文献 counts 0, as do 灰色, 未发表, 内部资料 and 期刊评审, while 文献检索 counts 3, 系统评价 7, 数据库 3 and PICOS 1" (L28-30) | QcgPdf len + counts (raw, norm) | 27609; 0,0,0,0,0; 3,7,3,1 | fully replicated |
| "The grey-literature count is 0 in both" (L36-37) | QcgPdf counts | issued text re-verified | draft row is not among the five captures (earlier-round capture); "both" not re-swept here |
| "carries no grey-literature field" (L44) | token counts | 0 | supported (token proxy) |
| "the omission is a property of the instrument rather than of its drafting history" (L47) | — | not sweepable (argument) | unverified, not a text claim |
| "the draft's is not itemised the same way" (L69-70) | — | draft unavailable in captures | unverifiable here |

## Verdict

Attacked 16 staged negative sentences + 1 title-level generalisation across the three knowledge docs; all quantitative `counts 0`/length claims replicated exactly (QcgPdf 27,609 chars; PRISMA/PRISMA-S/灰色文献/灰色/未发表/内部资料/期刊评审 all 0; 文献检索 3, 系统评价 7, 数据库 3, PICOS 1), the r50 title was falsified as written (NMPA copy states PRISMA-checklist attachment — Chinese voice, not "only western"), three corpus-wide negatives narrowed, and an r40 quote/recheck line-break defect found (located-quote cut required at offset 1320).
