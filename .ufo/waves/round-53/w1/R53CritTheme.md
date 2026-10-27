# R53CritTheme — C2 axis and expansion credit review (round 53, W1)

Seat: critic; lane: chousa; frozen claims: `corpus/evidence/round53/claims.md` (C1, C2). Base: `5b550133d79bc09c82d8965cce2e48c2598b8c3e`. No subagents, no writes outside this report. Scratch: `/fast/scratch/hyaku/chousa-r53/R53CritTheme` (created, removed).

## Method (all commands run, outputs observed)

- `git -C chousa-shokunin grep -n -i -e 'tracking' -e 'information specialist' -e 'Cochrane Handbook' -e 'PRISMA-S' -e 'jmla' -e '质量控制' 5b550133… -- corpus/knowledge` → hits only in `chinese-prisma-s-reception-r52`, `chinese-search-record-r39` (S111 subject heading `质量控制`), `citation-version-binding-r36`, `contextual-source-admission-r24` (S004 ch.24), `japanese-search-record-r38/-niph-form-r52`, `metadata-screen-r25` (S029 ch.IV), `search-log-method-r39` (S078). None holds any of the five C2 documents.
- `git -C … grep -n -e '1449' -e 'chapter-04' -e '1736907153935975' -e '1126.html' -e 'pharmwyp' -e 'bjhea' -e 'jmla.pitt.edu' 5b550133… -- corpus` → zero registry/knowledge mentions of the five targets; `chapter-04` appears only in round-49/52 evidence/lesson text (S083 staging).
- `git -C … grep -n -i -e 'PICOS' -e 'nhei' -e '综合评价' -e '指导原则' -e '临床安全' -e 'bhea' -e 'draft' -e '征求意见' -e '评估中心' -e '综合评估' 5b550133… -- corpus` → no output: the QCG guideline cluster is entirely absent at BASE_REV.
- Registry: `git show 5b550133…:corpus/SOURCES.md` (116 rows) scanned; no QCG, JMLA-2022, ch.4 or NMPA row.
- Capture keys resolved with `printf %s "$u" | sha256sum | cut -c1-24`; all five exist under `.qcache/`; text forms read as UTF-8 with `python3 text.find`.

## Per-document verdicts

### S117 — JMLA tracking-record paper (planned entry `search-tracking-record-r40.md`)
Capture `0ae65ac01b93119d3c2f3fed.txt` (27,659 chars). Title verified: "PRISMA 2020 and PRISMA-S: common questions on tracking records and the flow diagram", Rethlefsen & Page, JMLA 2022;110(2):253–257, doi 10.5195/jmla.2022.1449. **Distinct document from held S078** (JMLA 2018;106(4):531–539, the PRISMA-S original, in `search-log-method-r39.md`). Not held at base (no URL/doi trace). Read-51/52 already adjudicated the staged entry: `README.md:1101` (refused once, non-contiguous span) and round-52 lesson "admit-later" with quote re-cut. Key strings: "PRISMA-S also recommends\n reporting the number of records identified from each information source." at char 1288 (line break after `recommends` — the draft's contiguous quote fails byte-exact; re-cut to break-free span); column allocation at chars 5430–5700 (Column 1/2) and 6720.
**Verdict: NEW ground; depth improved (field/column-level routing, beyond S078's log-as-document method); expansion improved. Credit yes.**

### S121 — Cochrane Handbook ch.4 (planned entry `western-instrument-alignment-r50.md`)
Capture `c9d1e74c3ac8d9eb332c9770.txt` (`training.cochrane.org/handbook/current/chapter-04`, 210,708 chars). §4.2.1 alignment sentence at char 13494: "the reporting aligns with the current reporting guidance for PRISMA (…) and PRISMA-S (…)"; §4.3.2 at 36710: "Finding out about unpublished studies … is important for minimizing bias"; "fast-moving field" at 35632. Base holds other Handbook chapters as separate rows (S004 ch.24 mined → `contextual-source-admission-r24`; S008 ch.2, S009 MECIR queued; S029 ch.IV mined) — **no ch.4 row or entry at base**. Caveat: ch.4 text was already staged/captured before base (campaign row S083: `14aaa168a5cb4d833ca78b0b` = cochrane.org host, same 210,708 chars; round-49 control text already re-checks "the chapter-04 URL … section 4.5"); the entry that used it, `search-log-fields-r36.md`, was refused rounds 43/47/52 for other conjuncts (PRISMA-S full-strategy sentence absent; S090 cell), not for the chapter.
**Verdict: NEW lane-held ground (no entry held it at base), but pre-staged/pre-captured material — completing a previously refused package entry, not fresh discovery. Depth improved (instrument-to-instrument alignment vs the Chinese side); expansion improved. Credit yes, with the pre-staging caveat.**

### S118 — issued QCG PDF (planned entries `quality-control-guideline-issued-text-r48.md` + twin row S195 in the western entry)
Capture `16fe8487aa97b98576a0dbac.txt` (27,609 chars). Issued-form markers: title block 《药品临床综合评价质量控制指南（2024年版试行）》 at 0, `二〇二四年十二月` at 78, `征求意见` absent, §1 `文献研究的质量控制` at 9940, PICOS at 10191, `指标 4` at 16260, Cochrane at 11581, PRISMA 0, `灰色/未发表/内部资料/期刊评审` all 0. **Base has no trace of the guideline at all** (registry + corpus scans above). The package draft's claim "The corpus already held a row for this guideline, quoting the draft for comment" and its "round-13 row" correction are **not supported at BASE_REV** — the bookkeeping pretext is unverifiable; the substantive finding stands on its own.
**Verdict: NEW ground (first appearance of the guideline in the lane); depth improved (issued text opened; grey-literature absence established on the issued form); expansion improved. Credit yes; flag the unsupported draft-row claim.**

### S119 — release notice
Capture `cfa080b4046592eb9490a82c.txt` (1,255 chars). Own body present in the text form: `发布时间：2025年01月03日` at 517, `来源：国家卫生健康委卫生发展研究中心` at 534, `现予以发布` at 755, attachment name at 845, `国家药物和卫生技术综合评估中心` at 879, `2024年12月31日` at 920; raw HTML adds the NCMTA@nhei.cn contact and the two 国卫办药政发〔2021〕16号 / 国卫药政函〔2019〕80号 references. Content is **procedural/announcement only** — it certifies the act, date and carrier of issuance, no domain substance.
**Verdict: a carrier stamp with verifiable provenance, not a document with substantive own ground. Depth unchanged; expansion credit only for the act-of-issuance fact. If bound by C2, quotes exist (title/body), but they measure presence of issuance, not theme depth — refuse as a bound document unless the Gate wants the issuance fact bound.**

### S120 — NMPA 2019 notice, pharmwyp copy
Capture `0435b64f65c3ea7ddc6bb92e.txt` (21,573 chars). **Not a blog re-write**: it is a faithful print of the official NMPA page (doc number `2019年第27号` at 101; `2019-06-18` at 607; signing `2019年5月23日` at 1086; official URL `nmpa.gov.cn/xxgk/ggtg/qtggtg/20190618165701432.html` at 1582; NMPA copyright footer) followed by the guideline 附件 text. The decisive mandate sentence at chars 3340–3367: `灰色文献”，如会议论文、未发表的学位论文、产业报告、咨询报告等。灰色文献中可能包含阴性研究结果…只纳入已公开发表的文献会引入发表偏倚。` Lane precedent admits third-party hosted reproductions as tier B scoped to reproduction (rows S093/S100/S101/S102/S103/S124). Province: **in scope for instrument-content claims** (what the 2019 guideline mandates and why); **out of scope for currency/legal-status claims** (round-52 refused the same document family's currency spine: `grey-literature-and-chinese-search-record-r40.md` — "PROVINCE: out of province, report, never absorb").
**Verdict: NEW ground; depth improved (mandate contrast); expansion improved. Credit yes, tier B — never as authority for official status.**

## Answer to the axis question

No C2 document is held by any base entry; the only overlaps are (a) ch.4 pre-staged/captured since round 49 (never held), (b) the JMLA-2022 paper named in the frontier since round 43/51 (never held), (c) the S195 twin re-citing S118's URL — one document counted once, consistent with "expansion credit per document". The deep counter ceiling (binding + located-quote presence, not entailment) is restated in the freeze; all five captures genuinely support located quotes, so measured depth is real, but "depth improved" for S119 is presence-only.

## VERDICT
Attacked C2's axis and expansion credit across all five documents: four (JMLA-2022, Cochrane ch.4, issued QCG PDF, NMPA-2019 copy) are new ground with improved depth/expansion — credit yes, with ch.4 pre-staging and NMPA tier-B caveats and the unsupported draft-row claim flagged; the release notice is a carrier stamp (depth unchanged, provenance-only credit); no document duplicates held ground.
