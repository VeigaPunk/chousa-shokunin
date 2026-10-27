# R56CritCurrency — C2 currency and authority review

## Counterexample / finding

Neither S127 nor S129 is evidenced as the issued T/CLPA standard. S127 is explicitly the public-comment draft: the captured cover prints `T/CLPA XXXX—2025`, `（征求意见稿）`, `2025 - XX - XX 发布` and `2025 - XX - XX 实施` (S127 form `b27ffd2f0161104c6a28c9f5.txt`, opening cover; SOURCES.md S127 row, line 137). Thus `XXXX` and both dates are placeholders; 2025 is the nominal edition/year, not an issue date. S129 is a journal-published article/guideline text in 中国药房 2025 vol. 36 no. 19, pp. 2353 ff. (S129 form `5233bf47babaa1ca2b49ed15.txt`, chars 10, 3590; SOURCES.md S129 row, line 139), not proof of an issued group standard. It has no T/CLPA number in the form; the printed `2025CN052` is explicitly under `指南注册` and `注册分类为“标准指南”` (same form lines 96–100), not a T/CLPA standard identifier. S129 records journal receipt 2025-07-30 and revision 2025-09-08 (form lines 1005–1006); it prints no standard 发布/实施 dates. The L1's `round-56.md` line 39 names an issued T/CLPA text as a future condition to flip the refusal, corroborating that this capture set does not establish one.

**Specific attribution defect:** the landed entry cites S129's `表 10` at char 22539 as the table carrying the grey-literature row (entry “Observation”; lesson `round-56.md` lines 69–70). In the captured text, `表7 药品临床综合评价的信息来源情况` begins before the source rows; the table's rows include `灰色文献 ... Ⅰ级 A` and `搜索引擎 ...`, while `表 10 其他研究的研究类型、研究方法及内容` is the separate right-column table. The two-column text extraction interleaves these. This is a correctable citation/anchor defect, not evidence that the row is absent: S129 actually places it in the information-source table (form `5233bf47babaa1ca2b49ed15.txt`, lines 271–294 as opened). Do not call S129 the issued standard. Report this as a finding against the frozen claim/landed entry; do not patch it.

## Currency of S130

S130 is the national centres' 2020-11 text, not established as the current management guideline: its cover reads `药品临床综合评价管理指南（试行）`, names 国家药物和卫生技术综合评估中心 / 国家卫生健康委卫生发展研究中心 and 国家卫生健康委药具管理中心, and dates itself `二〇二〇年十一月` (S130 form `a42feae4448612f949cc715f.txt`, opening; SOURCES.md S130 row, line 140). But S128's explanatory note says the July 2021 commission notice was accompanied by `《药品临床综合评价管理指南（2021 年版试行）》` (S128 form `de9f5afc3809acbf61f4d5bb.txt`, lines 49–53 and 153–156); S127 itself cites that 2021 version in its body/reference list (S127 form lines 1082, 1097, 1359). Therefore the entry's Unknown line 33 is overcautious in saying the relationship is not established: the source evidence identifies a 2021 version after the 2020 text. The current status of the 2021 version as of 2026, and its grey-literature content, remain unknown; S130's captured-text silence cannot be generalized to that version. Lane grep run: `grep -rn '药品临床综合评价管理指南' .../corpus --include='*.md' -l` returned the landed field entry, `corpus/lessons/round-56.md`, and `corpus/SOURCES.md`; the direct 2021-version evidence is in the captured S128/S127 forms above.

## Tier calibration

- **S127 — B**, scoped to wording of the draft and what it names; never evidence of an issued standard. Registry row says this explicitly (SOURCES.md line 137).
- **S128 — B**, drafter's explanatory note for provenance, dates and background, not grading-system content (SOURCES.md line 138).
- **S129 — A** for the wording of the journal-published guideline and its tables/scale, not for issued T/CLPA status (SOURCES.md line 139). Its grey-literature row is Table 7, not Table 10.
- **S130 — B** for the identity/date and captured 2020 text only; not for current-version claims (SOURCES.md line 140).
- Related held S118 is **B**, not A: its carrier is a professional society host, and its tier is explicitly scoped to the issued 2024 quality-control guideline text (SOURCES.md line 128).

## Unknown bullets that must remain

Keep the entry's `#### Unknown` scope (landed entry lines 29–35), with these calibrations:

1. **Sweep of the forms:** preserve as a reported L1 count unless independently re-counted; it is not a currency conclusion.
2. **Which document is issued:** keep unknown whether an issued T/CLPA standard exists and whether its source list matches S127/S129; clarify that S127 is a draft and S129 a published journal version, neither shown to be the issued standard.
3. **Which management guideline is current:** keep current status/content of the 2021 version unknown, but remove the uncertainty that the 2021 version is named as a later version than S130. S130's silence is only about its own captured form.
4. **Completeness of the PDF text forms:** retain the bounded caveat about absence claims unless the underlying independent extraction evidence is examined.
5. **Province:** retain the boundary that the domain requirement and grading systems are adjacent ground, not established by this source-hierarchy/search-record entry.

Evidence commands run (read-only):

```text
head -c 3000 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/b27ffd2f0161104c6a28c9f5.txt
=> cover shows T/CLPA XXXX—2025; （征求意见稿）; 2025 - XX - XX 发布 / 实施

grep -n '2021\|管理指南\|卫生健康委\|征求意见\|立项' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/de9f5afc3809acbf61f4d5bb.txt
=> lines 49–53, 153–156 name the 2021 年版试行 management guideline; lines 101 onward date workflow draft stages

grep -n 'Δ\|T/CLPA\|CLPA\|团体标准\|收稿\|修回\|2025CN052\|注册' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5233bf47babaa1ca2b49ed15.txt
=> `指南注册`, `注册分类为“标准指南”`, `2025CN052`; receipt/revision dates at lines 1005–1006; no T/CLPA hit

sed -n '265,300p' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5233bf47babaa1ca2b49ed15.txt
=> Table 7 is 药品临床综合评价的信息来源情况 and its rows include 灰色文献; separate Table 10 is 其他研究...
```

**VERDICT:** C2 currency/authority review finds neither S127 nor S129 is the evidenced issued standard, S130 is not shown current given the later 2021 version, and the landed S129 Table 10 anchor is wrong (the grey-literature row is in Table 7); report-only, no frozen predicate or production edits.