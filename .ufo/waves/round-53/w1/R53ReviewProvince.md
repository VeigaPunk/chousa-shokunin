# R53 ReviewProvince — province / QUALITY-bar verdicts for the three staged C2 entries

Seat: R53ReviewProvince (leaf; no subagents). Read: `PROVINCE.md`, `corpus/QUALITY.md`
(criteria 1–90), `corpus/README.md` coverage map, the three staged entries, the frozen
`corpus/evidence/round53/claims.md`, round-51/52 lessons and spot-checks, the campaign
`merge/chousa/SOURCES.append.md`, and the five captures under `.qcache` (all present:
S134 `0ae65ac…`, S185/S195 `16fe8487…`, S186 `cfa080b…`, S190 `0435b64f…`,
S193 `c9d1e74…`). No tool installed (RULES.md read; nothing needed). Scratch
`/fast/scratch/hyaku/chousa-r53/R53ReviewProvince` created, used, and left empty.

## 1. Sibling boundary: no lane owns the pharma/HTA/regulator domain

`grep -inE 'regulator|NMPA|guideline|HTA|pharmacovigilance' /home/vgpnk/Projects/shokunin/*/PROVINCE.md`
→ only kasegi (JPCERT/CC 2026 guideline, vulnerability disclosure) and kake (Jekyll
docs) hits; a Chinese-term sweep (`药物|药|评估|卫生|临床|警戒|药品`) → 0 matches.
The 21 sibling lanes claim: secrets (kagi), RE (kaidoku/revenger), web (kake), model
serving (kama), bounty (kasegi), LLM eval (kengaku), prompt/skill (kotoba),
worldbuilding (kotodama), orchestration (kumitate), desktop (mado), observability
(mori), hygiene (souji), browser (tabi), fixtures (tameshi), host repair (tsukuroi),
audio (which explicitly routes `research method (chousa)` to this lane), game-dev 2d/3d,
lore. Conclusion: drug clinical-evaluation regulation, pharmacovigilance and HTA have
**no sibling owner**; chousa's own rule `Out of province → report, never absorb` is the
sole gate. The lane absorbs only the search-method face of these documents; their
substantive regulatory/HTA content must be reported, not absorbed. Precedent in-repo:
round-51/52 refused `grey-literature-and-chinese-search-record-r40.md` for "out of
province for its spine (a regulator instrument's currency)" (`corpus/lessons/round-51.md:70`,
`round-52.md:64`).

## 2. The S190 blog copy: register it, tier C, scoped; never sole support

- The staged row S190 already tiers it C and states why: "content is NMPA's and the
  carrier is a third party's site, so the tier is C" (`SOURCES.append.md:115`). This is
  exactly the lane's carrier discipline (S105/S106 tier B for university carriers;
  S116 tier B for a web-archive copy with original + failed-fetch marker).
- The captured PDF (960,118 B, `%PDF-1.7`, sha256 `1a46faa…`) is a print of the NMPA
  page itself: it embeds the NMPA chrome and footer (`本站由国家药品监督管理局主办`,
  `Copyright © NMPA`, 网站标识码), the 通告 title/number (2019年第27号, 发布时间 2019-06-18,
  国家药监局 2019年5月23日), and the original NMPA URL
  `https://www.nmpa.gov.cn/xxgk/ggtg/qtggtg/20190618165701432.html` (S190 `.txt` line 34).
  The original's qcache key `b5c2c7c891a79ecbc9317cd8` holds only `.fail` = `rc=22`
  (curl HTTP error) — the primary is unreachable. 21,573 chars extracted (matches the
  staged row; S190 `.txt` length 21,573).
- Verdict: **yes, register** — but as the lane's S116 pattern: the carrier URL is the
  row's URL, the original is named and its fetch-state recorded, tier C, scope limited
  to what the copy renders. What the copy renders is the full notice + 附件 guidance
  (sections 一/二/三 present: `3.全面查找证据。` at offset 3116 once; `是否检索灰色文献`
  at 8165 once; `应当纳入研究；应当尽力获取其他灰色文献` at 7212 once; `会议论文、未发表的学位论文、产业报告、咨询报告` at 3348 once).
- **Admission-bar risk (QUALITY 7):** tier-C is never sole support. `grey-literature-mandate-scope-r48.md` rests solely on S190 for its regulator-mandate claims (collection duty, inclusion duty, report field), and `quality-control-guideline-issued-text-r48.md` rests solely on S190 for the regulator side of its contrast. Neither entry asserts "NMPA requires X" as truth — but the mandates are presented as findings. The lesson Gate must either add a second independent source for the mandate claims or relabel them `observed in this copy only` (source-states-the-claim ≠ claim-is-true, criteria 3/8). The field-absence comparison is fine.

## 3. Per-entry verdicts

### 3.1 `search-tracking-record-r40.md` (S134 JMLA) — IN PROVINCE
Tracking-record fields and flow-diagram columns are core owned search-record territory.
No sibling part. Verdict: **admit**, with the quote re-cut: the entry's sentence
`PRISMA-S also recommends reporting the number of records identified from each information source`
occurs 0 times byte-exact in S134 `.txt` (it breaks after `recommends`); the break-free
span `the number of records identified from each information source` occurs once at
offset 1330 (61 chars, one line). Round-51/52 already recorded this (`round-51.md:66`,
`round-52.md:62` admit-later).

### 3.2 `western-instrument-alignment-r50.md` (S193 Cochrane; S195 issued guideline) — IN PROVINCE for the alignment; NOT for the guideline's operative prescriptions
- S193 (tier A, publisher's own chapter text): the instrument-to-instrument alignment
  and unpublished-studies-as-search-source treatment are in province (search-strategy
  taxonomy, claim-vs-source). Quote fidelity: the entry's `the reporting of the search and selection work aligns with the current reporting guidance for PRISMA and PRISMA-S`
  occurs 0 times; the byte-exact form is `the reporting aligns with the current reporting guidance for PRISMA ( Page et al 2021b , Page et al 2021a ) and PRISMA-S ( Rethlefsen et al 2021 )` (146 chars, offset 13480, once, one line). The unpublished-studies sentence whole is 182 chars (>160) and contains a citation; the usable break-free sub-span `Finding out about unpublished studies, and including their results in a systematic review when eligible and appropriate` (119 chars, offset 36552, once, one line) is the re-cut candidate. The entry's paraphrase `finding out about unpublished studies and including their results … is important for minimizing bias` occurs 0 times (missing comma + `( Cook et al 1993 )`).
- S195/S185: the guideline is used as the counterpart whose silence is measured — in province as a comparative coverage claim. The guideline's own operative prescriptions (PICOS criteria, independent dual screening with third arbitration, flow-chart counts) are the HTA instrument's substantive requirements — sibling ground; the entry must report them only as *what the document says*, never adopt them as lane method. Current text does report them as the document's content (Observation), not as lane method — acceptable with that scoping stated in the lesson.
- Verdict: **admit with re-cut quotes**, and the lesson states the prescriptions are reported, not absorbed.

### 3.3 `quality-control-guideline-issued-text-r48.md` (S185/S195 issued PDF; S186 notice; S190 NMPA copy) — SPLIT
- In province: (a) grey-literature-field absence sweep (`灰色文献` 0, `灰色`/`未发表`/`内部资料`/`期刊评审` each 0 over S185's 27,609 chars — verified); (b) version discipline: draft-vs-issued wording correction is claim-vs-source (the corpus must cite the issued text); (c) source-hierarchy handling of the three carriers (S185/S186 tier B society carrier; S190 tier C).
- Sibling ground (report, don't absorb): the regulator/centre document content — the centre's QC guideline as an issued instrument (its HTA quality-control regime), and the NMPA 2019 guidance's mandate. The contrast conclusion is fine as a search-record-field finding.
- Quote fidelity: the issued wording quoted as `可根据评价主题确定纳入与排除标准，可基于 PICOS 原则` occurs 0 times byte-exact; the capture reads `应根据评价主题确定纳入与排除标准，可基于“PICOS”原则进行` (offset 10187; `可基于“PICOS”` once; `纳入与排除标准` once) — the entry also moves 应→可 across the clause boundary. Both the staged row S185 and the entry repeat this mis-transcription; a located quote must use the capture form. `多个中、英文专业数据库` (issued) vs `中、英文专业数据库` (draft) — verified once each in their captures; `可基于` occurs 0 times in the draft, and `纳入标准应基于“PICOS”原则进行` is the draft form. `现予以发布` and `2025年01月03日` occur once each in S186 (the entry's `2025-01-03` is a conversion; a verbatim quote must use the capture form).
- Bookkeeping target not lane-owned: the draft row the entry says the corpus "should mark as quoting the draft" is a campaign-package row — the lane registry at BASE_REV has no 药品临床综合评价 row (0 hits in `corpus/SOURCES.md` and at BASE_REV; registry ends S116). The disposition belongs in the round-53 lesson / campaign package as report-not-absorb, not in the lane registry.
- Verdict: **admit with re-cut quotes**, lesson records the draft-row disposition and the sub-absorption boundary.

## 4. Frozen-C2 predicate support (checked, not run)
- At BASE_REV (`5b55013…`) no `corpus/knowledge` file holds `tracking record`, `information specialist` or `质量控制指南` (git grep, 0/0/0 files). Each staged entry holds its term: r40 `tracking record` ×3, r50 `information specialist` ×1, r48 `质量控制指南` ×2 (grep -c). S195 is the same URL as S185 (same qcache key `16fe8487…`); the twin label is correct for C1's REAL leg.
- All five documents have on-disk captures with text forms (keys/sizes above); none is a `.fail`.

## 5. Coverage / expansion notes
- S134 was previously judged admit-later (r51/r52); this round's frozen by-document set names it, so the flip is met — no new expansion credit beyond the document.
- S190 earns credit as a document only if the lane does not already hold it; the lane registry has no NMPA-2019-notice row at BASE_REV; the campaign row is the only record. The 2019 notice's *mandate content* is out of province regardless.

## VERDICT
Attacked province fit, QUALITY bar, the S190 carrier question, and the frozen-C2 term predicates: all three entries are in province for their search-record/spine frames (with the S185/S190/S195 document content scoped to reported-not-absorbed), the S190 blog copy should be registered tier C with the original named and fetch-state recorded and never sole support, and every entry carries quote-fidelity defects (S134 line-break, S193 paraphrase, S185 应/可 mis-transcription, S186 date conversion) that require re-cut byte-exact quotes before the Gate can admit them.
