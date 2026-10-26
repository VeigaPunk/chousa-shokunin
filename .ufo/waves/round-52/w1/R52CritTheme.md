# R52CritTheme — C2 axis/expansion critique (search-record theme, round 52 wave 1)

Seat: R52CritTheme. Object: the frozen C2 claim (`corpus/evidence/round52/claims.md` §R52-C2), attacked on its two names: **is this depth** and **is any of it ground the lane already holds**. No production file touched; scratch only (removed at exit).

## What C2 asserts

Three entries over four documents: (a) NIPH `.docx` form → lane S115; (b) Japanese PRISMA 2020 translation at its web-archive copy → lane S116; (c) 梅斯医学 PRISMA-S interpretation page → lane S113; (d) 中国全科医学 PRISMA 2020 checklist page → lane S114. Expansion credit is "per document, not per entry" (claims.md:116). The predicate requires ≥3 of the 4 documents BOUND, each bound id holding at least three quote rows.

## Evidence

1. Base sweep (lane at `00f8c7f5272a1d98b6d34913985fa4537e00aaf9`):
```
git -C …/chousa-shokunin grep -n -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 BASE_REV -- corpus/knowledge
```
→ no output (none of the three terms in any knowledge file at base). `git grep -c -e 検索期間` → only `japanese-search-record-r38-amendment-2026-10-23.md:6` (検索期間 without the 文献 prefix). The predicate's base premise holds.

2. Archive translation capture `e84bfe97808591d23fe3266f.txt` (5,328 chars): 検索者 0, 情報源 2, 検索戦略 2, 最後に調べられた 1, フィルター 1; item 7 text: `用いたフィルターや制限も含め，すべてのデータベース，試験登録，Web サイトの完全な検索戦略を記載する。` The r38 amendment already names this exact capture and declines to rest on it: "A 2024 archive capture of the same checklist is in the campaign cache (`e84bfe97808591d23fe3266f.txt`, 5,328 characters) but has no lane Registry row, so nothing in this entry rests on it" (`japanese-search-record-r38-amendment-2026-10-23.md:26`).

3. 梅斯医学 page `453d492becd9a2f4632cb8dd.txt` (8,804 chars): the only content line is the 简要介绍 blurb at char 2264 — "PRISMA-S(PRISMA for Searching)作为PRISMA 2020的扩展版本，为文献检索报告提供了包含16个条目的专项规范。本文旨在对PRISMA-S进行系统性中文解读…" — 16×3, 条目×2, and an attachment line `[AttachmentFileName(sort=1, fileName=系统评价_Meta分析中文献检索报告清单（PRISMA-S）解读_郑卿勇.pdf)]`. The raw HTML (276,803 bytes) has 购买×1, 附件×2, 下载×30 — a purchase/download wall, no item body. The deemed ARTICLE — 郑卿勇's PRISMA-S 解读, 中国循证医学杂志 26(4) — is already a held lane row: `S111` (SinoMed) in `chinese-search-record-r39.md:5,18`, which already teaches the same 16-item extension claim (`包含16个条目的专项规范`) and records that the page serves no full text. The r39 entry's open Unknown is "the 16-item text stays unread at item level" — the 梅斯医学 capture does not close it (no item text in either form).

4. 中国全科医学 page `cacddf3bbf780a4c7582bb17.txt` (6,179 chars): item 6 `明确说明每一项来源 的 检索或查询日期` (char 1719) and item 7 `呈现 所有数据库、注册平台和网站的 完整 检索策略，包括 用到的 过滤器和限制条…` (char 1756). These are the same checklist items already held in Japanese via S108 (r38: item 6 sources + per-source last-search date; item 7 complete strategy).

5. NIPH `.docx` (`3a8b45977cd111e45e3980a5.raw`) through the C1 tool:
```
python3 tools/capture-text.py …/3a8b45977cd111e45e3980a5.raw --locate 'SRにおける文献検索期間について明記する'   → LOCATED count=1 offset=8996 rc=0
python3 tools/capture-text.py …/3a8b45977cd111e45e3980a5.raw --locate 'ハンドサーチ等'                            → LOCATED count=1 offset=9428 rc=0
python3 tools/capture-text.py …/3a8b45977cd111e45e3980a5.raw | wc -c                                       → 48936
```
Round 51 refused exactly this document for its capture form (`corpus/lessons/round-51.md:55,57`: "refused-doc: https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx … refused this round for its capture form, not for its source quality; flip: a counter and span builder that read a zip member… after which the staged claims narrowed as above can be re-grounded and bound"). Lane-held knowledge never carried its content (r38 amendment:28: "A second Japanese document was opened and is not adopted").

## Per-document verdict

| Document (staged → lane) | New ground? | Verdict |
|---|---|---|
| NIPH form (S125 → S115) | Yes — first time the document's substance enters lane-held knowledge with located quotes; its window-endpoint teaching (search period fixed between framework decision and manufacturer submission) appears in no held document | depth improved; expansion improved |
| Japanese PRISMA 2020 translation (S129 → S116) | Yes as a document (first held copy of the official translation), but the negative "no searcher field" and items 6/7 substance were already implied by held S108 (the industry form's own item 6/7 text and its 検索者-on-attachment structure) and S112 | depth improved narrowly (primary source replaces inference); expansion improved |
| 中国全科医学 checklist (S112 → S114) | Yes as a document (first Chinese checklist), but it restates items 6/7 already held from S108/S112 | depth ~unchanged (corroborative); expansion improved |
| 梅斯医学 page (S111 → S113) | No — same 郑卿勇 PRISMA-S 解读 article already cited as lane S111 (SinoMed); the page's only content is a duplicate of the held 16-item blurb; the item text stays unread | depth unchanged; no new-document credit (second carrier) |

## Counterexample and impacted axes

Counterexample: C2 can pass `BOUND=4/4` while only three of the four documents are substantively new — the medsci page is a second copy of held article ground (lane S111), and its only distinctive fact (portal paywall shape) is not even expressible from the `.txt` capture form (no 购买/付费 token in it; only 1×购买 in raw HTML). The claim's "four documents" framing therefore overstates expansion credit by one.

Impacted axes: C2 depth (an entry grounded on medsci would pass `inference-ground` while adding nothing the r39 entry does not already hold) and expansion credit (per-document credit would count a duplicate carrier as a document).

Smallest safe correction: in the round-52 lesson Gate, judge the medsci row as **no expansion credit** — scope it explicitly as a second carrier of held row S111's article (tier B, reachability/paywall fact only), and require the `chinese-prisma-s-reception-r52.md` entry to state the item text remains unread (as r39 already did), not claim item-level reception; keep credit at three new documents (NIPH, translation, chinagp), with chinagp's corroborative status named. The counter's arithmetic is not wrong; the lesson's credit judgment must be.

VERDICT: attacked C2's axis and expansion credit — found NIPH and archive translation are genuine new depth, chinagp is a new but corroborative document, and the medsci page is a second copy of held ground (no credit), so the round's four-document expansion claim overstates by one.
