# R54CritNegatives — attack on the staged NEGATIVE/limiting claims in r36/r37

seat: R54CritNegatives (critic, leaf; no subagents dispatched) · date: 2026-10-26
frozen: `corpus/evidence/round54/claims.md` @5a1a2063 — I report findings against staged entry text; I do not patch predicates, counters, or entries.
target files: `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/source-type-taxonomy-r36.md` and `...-r37.md`.

## Grounds (all reads; no writes, no network)

- Samr   `.txt`/`.raw` = `…/.qcache/adf6ba934e813b2c326fa150.{txt,raw}` — std.samr.gov.cn record
- Openstd`.txt`/`.raw` = `…/.qcache/b9ca2a4fdf9455867534f144.{txt,raw}` — openstd newGbInfo hcno=C6CE52E55AC09B9C79A20AEA77CEDD14
- Jmu    `.txt`/`.raw` = `…/.qcache/0f33243fd7ac2fe88b85c1ba.{txt,raw}` — JMU PDF copy

## Sweeps run (terms → form → observed count)

```
openstd.txt: '本系统不提供文本阅读服务' 1× (offset 15188, line 491, 47 chars, single line;
  full sentence '该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务',
  commas U+3001/U+FF0C, count 1); '在线预览' 5; '下载标准' 1; 'showGb' 5; '该标准暂无全文，请等待更新' 1
openstd.raw: buttons rendered for THIS hcno: 1 ('实施信息反馈', data-value=C6CE…EDD14); 0 preview/download
  buttons rendered ('ck_btn'/'xz_btn' occur only inside the generic i18n updater JS); 'showGb?type=online' 0
samr.txt: '查看文本' 1 (offset 3453, line 939); '全文' 0; '阅读' 0; '下载' 0
samr.raw lines 2003-2006: sidebar '查看文本' btn; line 2054: '查看全文' btn; lines 2110-2117: both open
  http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14
samr.txt: '本标准非等效采用ISO国际标准：ISO 690:2021' 1 (offset 1797) — the 采标 basis of the refusal
jmu.txt: '本文件适用于作者和编制者著录参考文献' 1 (offset 5576, line 165);
  '本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献' 1 (offset 5602, line 166);
  '不适用于' 2 (2nd at 51266: an unrelated rule about manually numbered citations)
jmu.txt: fullwidth Latin letters = 17864 (U+FF21-U+FF3A/U+FF41-U+FF5A)
```

## Findings — each negative claim, its sweep, verdict, narrowed wording

1. r36 title: "…and **publishes its text as unreadable**". Sweep: "全文/阅读/下载" in samr.txt = 0/0/0; the record carries a '查看文本'/'查看全文' entry that opens the openstd page; the standard itself was 发布 2025-12-02 (openstd.txt 发布单位 国家市场监督管理总局、国家标准化管理委员会). VERDICT: CONTRADICTED as written — category error: the text is published; one free portal declines the online reading service. Narrowed: "its authority's free full-text portal declines, for the copyright reason it states, to serve its text online".

2. r36: "The official full-text portal **refuses to serve the document's text**… Only metadata is served." Sweep: refusal sentence 1× on openstd.txt (record-level); but the same page's template carries the generic preview/download machinery ('在线预览' 5, '下载标准' 1, showGb 5, '该标准暂无全文' 1) used for other records. VERDICT: SUPPORTED at record level, OVERREACH at portal level — the portal refuses for this record, not as a rule. Narrowed: "the openstd record for this standard serves no text and states why; the portal's generic preview/download path exists but is not rendered for this record".

3. r36 Inference: "authoritative about its own identity and status while being **unreadable in its operative content**". Sweep: jmu.txt is a complete public readable copy (83,061 chars, 附录Ａ 4×); r37 itself cites it. VERDICT: CONTRADICTED — "unreadable" is false of the document; only the authority's free portal does not serve it. Narrowed: "…while its operative text is not served by the authority's own free portal (a public third-party reproduction is readable but is not the authority's typography)".

4. r36: "The lane should not quote the Chinese standard's rules from memory or from a vendor mirror." Sweep: jmu.txt fullwidth Latin = 17,864 chars (e.g. code ＭＴ rendered fullwidth). VERDICT: SUPPORTED as lane guidance (the reproduction's typography is demonstrably shifted). Narrowed: keep, but ground it in the fullwidth sweep, not in the reseller's HTTP status.

5. r36 Unknown: "the one reseller that reproduces the table of contents returned HTTP 403"; "the standard's own text… is **not publicly readable**". Sweep: no reseller capture exists in the qcache (terms 'reseller', '403' have no form here); "not publicly readable" fails against the public JMU copy. VERDICT: 403 = unverifiable from this round's captures (inherited campaign history, needs a dated fetch receipt or hedging); "not publicly readable" CONTRADICTED. Narrowed: "returned HTTP 403 when last fetched (2026-10, campaign wave)"; "not readable from the authority's free portal; a public reproduction exists but is third-party".

6. r37 title: "…and **whom it does not govern**". Sweep: jmu.txt scope clause (offsets 5576/5602, single lines, 1× each). VERDICT: SUPPORTED in scope but overbroad as titled — the clause excludes three actor classes from one activity. Narrowed: "and whom its scope clause excludes from compiling references".

7. r37: "The standard governs the **author**, not the librarian, the catalogue compiler or the indexer." Sweep: the clause governs 作者**和编制者** and the negative half scopes to 著录参考文献 (the sentence ends '…著录参考文献'; activity, not person). VERDICT: OVERREACH in both halves — 编制者 dropped from the positive side; the negative side reads as a blanket exclusion of persons. Narrowed: "the standard states it applies to authors and compilers when they compile references, and does not apply to librarians, catalogue compilers and indexers in that activity".

8. r37 Unknown: "The authority's own portal serves no text for **采标 standards** (wave 1's S075)". Sweep: exactly one 采标 record is in evidence (samr.txt '采标情况' 1×; openstd.raw 采 badge 1×); a class claim needs a class sweep this corpus cannot run (no other 采标 records cached, no fetch allowed). VERDICT: OVERREACH — one record cannot ground a system-level rule. Narrowed: "the authority's portal serves no text for this 采标 standard; whether the same holds for other 采标 standards is untested".

9. r37: "Nothing here is quoted as the authority's own typography." Sweep: fullwidth count above. VERDICT: SUPPORTED — keep.

10. r37 explicit unknowns ("was not checked", "is untested") and r36 "Whether a PRC document-type identifier scheme is in force… was not checked". VERDICT: correctly hedged — no attack.

## System-level overreach list (one record → PRC standards system), with smallest safe corrections

- #2 portal-level refusal → record-level refusal (the portal's generic machinery is in the same capture). Correction: swap "The official full-text portal refuses" for "This standard's openstd record states its system provides no text reading".
- #3/#5 "unreadable / not publicly readable" → "not served by the authority's free portal". Correction: one clause each, as worded above.
- #8 "serves no text for 采标 standards" → "for this 采标 standard". Correction: delete the plural class claim or add "untested for other 采标 records".
- #1 title "publishes its text as unreadable" → "its authority's free portal declines to serve its text online, for the copyright reason it states".
- #7 scope sentence → restore 编制者 and the 著录参考文献 qualifier on both halves.

## Notes for the integrator

- All quotes above are single-line, ≤160 chars, ≤25 whitespace words, count=1 on their form, with offsets — usable as span rows if the L1 adopts the narrowed wordings.
- Finding 5's 403 leg is the only item needing non-capture evidence; everything else is decided inside the three cached forms.
- No LibreOffice, no git, no writes outside this report and scratch; scratch removed on exit.

VERDICT: attacked all 10 negative/limiting sentences and both titles of staged r36/r37 — 3 contradicted (#1,#3,#5-partially), 4 overreach (#2 portal-level,#6 breadth,#7 both halves,#8 class claim), 3 supported (#4,#9,#10); narrowed wording supplied for every defect.
