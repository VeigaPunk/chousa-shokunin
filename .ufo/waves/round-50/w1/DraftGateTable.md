# DraftGateTable — round 50 wave 1: assimilation Gate table draft (seat DraftGateTable)

Scope: the eight staged CNKI-cluster entries of `MERGE-REPORT.md` judged against the frozen R50-C2 predicate
(`corpus/evidence/round50/claims.md`), `PROVINCE.md`, and `QUALITY.md` criteria 1–72. No fetch; every source is an
on-disk capture. No tool install was needed (nothing recorded). `git rev-parse --short HEAD` = `7754172`.

## Documents → planned lane ids (registry max S103; ascending by document)

| document | staged id(s) | capture key sha256(url)[:24] | capture form | lane id |
|---|---|---|---|---|
| CNKI 学位论文学术不端行为检测系统使用手册（管理员） (gs.sxu.edu.cn) | S124, S135, S180, S187 | `e3ca8f4fdd15420b80096a75` | .txt UTF-8, 38,174 chars (pdftotext -layout) | S105 |
| CNKI 大学生论文管理系统使用手册（子账号） (rwxy.seu.edu.cn) | S136 | `28750bcdf5d36cd90a7709fb` | .txt UTF-8, 30,937 chars | S106 |
| CNKI 大学生论文管理系统使用手册（教师） (bs.bnu.edu.cn) | S145 | `275c79d45b1e9b0fd32cef93` | .txt UTF-8, 9,914 chars | **refused** (no lane id) |
| 中国科学院文献情报中心 引证检索 service page (chaxin.las.ac.cn) | S118 | `001287c436f0e6b1d166ae8d` | .txt UTF-8, 2,288 chars | S104 |

Keys: `for u in <7 urls>; do printf '%s' "$u" | sha256sum | cut -c1-24; done` → `e3ca8f4fdd15420b80096a75`,
`28750bcdf5d36cd90a7709fb`, `275c79d45b1e9b0fd32cef93`, `001287c436f0e6b1d166ae8d`,
`9c3aca545490cdfad8428e40` (privacy policy), `625375f640d6eb3be0990ef2` (gb-manual),
`dd50f086f911d06fa2bbd5f9` (tmlc). Decisive offsets in the admin capture: definition
「引文核对是指，以“中国知网”的文献资源为核对源内容」 at 30738 (1×); 「把待检测文献的参考文献复制到“引文核对”文本框，点击“搜索”按钮」 at 30793 (1×);
「态共分为三种类型」 at 30935 (1×; the string 「状态共分为三种类型」 does **not** occur contiguously — a newline sits after 状, so r40's recheck quote is not byte-exact);
「第二类是橙色的标识」 at 31063 (1×); 「红色提示」 at 31157 (1×). Term counts (admin): 引文核对 4, 匹配 0, 橙色 1, 琥珀 0, 绿色 3.

## Decisions

| entry | decision | reason | flip | evidence |
|---|---|---|---|---|
| `cnki-citation-check-r40.md` | **admit, narrowed** | The theme's core claim: what the feature compares (中国知网's own 文献资源 as 核对源内容) and its three states; S124→S105 is bound this round. Narrowing required: (a) the middle marker is 橙色, not "amber" (橙色 1, 琥珀 0 in the capture); (b) drop `S076`, `S109`, `S111` — the C2 predicate forbids any S token but bound ids, and S109/S111 are staged rows for a Japanese review-basics article and the Chinese PRISMA-S interpretation, not FEVER corpora (the lane's FEVER rows are S085–S087, SOURCES.md:95-97); (c) Inference bullets 1 and 3 cite no S id and carry tokens not in any span (`inference-ground` rc=1, 5 FINDINGs: `INF_UNCITED` ×2, `INF_TOKEN_NOT_IN_SPAN` ×2, `INF_UNGROUNDED` ×1); (d) recheck quote must be a contiguous capture fragment. | — | capture `e3ca8f4f…`; staged header r40:4; rg findings above; S109/S111 staged rows show other URLs |
| `citation-matching-semantics-r41.md` | **admit, narrowed** | Carries the theme's second half ("which manuals document it") with a measurable negative: 匹配 0 across the admin manual, and 引文核对/核对/匹配 all 0 across the 子账号 manual's 30,937 chars; the 仅去除第一作者本人文献 option lives in the 子账号 manual's §2.6 (8×, 创建文件夹 6×). Narrowing required: (a) drop S145 / the 教师 manual (refused) and reword "systematic across CNKI's own manuals" to the two manuals; (b) S136's own declared flip ("flip to B if a CNKI manual with a 引文核对 section is found and opened") is now true — the admin manual is opened, so S106's scope cell must be rewritten and the §2.6 claim stays scoped to that manual (tier-C row); (c) its Inference section is prose, not bullets — `inference-ground` prints `INF_NO_BULLETS` (rc=1); convert to bullets, each citing S105/S106 with a verbatim token; (d) recheck line drops the 教师 clause. | — | captures `e3ca8f4f…`, `28750bcdf…`; staged headers r41:2-7; inference-ground rc=1 |
| `istic-citation-verification-r39.md` | **admit, narrowed** | A second, institutional citation-verification authority for the theme; S118→S104 bound (引证检索 6×, 「按合作者排除自引标准统计他引次数」 at 549, 1×). Narrowing required: (a) the path's "istic" misnames the carrier — the page is 中国科学院文献情报中心 (中国科学院 5×, 文献情报中心 3×, 中国科学技术信息研究所 0×, ISTIC 0×); body text already says "Chinese Academy of Sciences' own information centre", so only the lesson records the frozen-path defect; (b) its Unknown "CNKI's own 引文核对 feature remains unopened … timed out for a second time" is stale — the admin-manual capture exists and was opened 2026-10-23, the entry's own `verified-at`; replace with a cross-reference by path to the admitted r40/r41 entries; (c) Inference bullets 1–4 cite no S id; tokens `counting is a property of the index's rules` and `300` are not grounded (`inference-ground` rc=1, 8 FINDINGs: `INF_UNCITED` ×4, `INF_TOKEN_NOT_IN_SPAN` ×2, `INF_UNGROUNDED` ×2). | — | capture `001287c436…`; staged header r39:4-7; rg findings above |
| `cnki-matching-modes-r42.md` | **refuse** | Its own Observation/Inference say the three modes govern the search platform, "not the 引文核对 feature" — out of the frozen theme (first half asks what the *citation-check feature* compares). S149 (gb-manual, capture `625375f6…`) was not re-grounded this round: no round-50 span/quote row names it (grep of `corpus/evidence/round50/` and `.ufo/waves/round-50/` for its key: no hits). Same refusal as round 49. | a frozen question on CNKI's search-platform matching taxonomy, with S149 bound by a re-grounded capture and quotes | capture `625375f640…`: 匹配方式 7, 相关度匹配 3, 精确匹配 4, 模糊匹配 5, 引文核对 0; staged header r42:2 |
| `cnki-public-surface-r43.md` | **admit-later** | Answers the theme's second half only negatively: S160 (check.cnki.net/tmlc/, capture `dd50f086…`, 1,115 chars, 全文比对数据库 1×, 引文核对 0×) was not re-grounded this round, and the claim's second surface (the 科研·人事 诚信档案 portal) has no capture in this round's set at all — "neither surface carries any documentation" is supported for one surface only. | a bound, re-grounded row for check.cnki.net/tmlc/ with a located quote, plus a capture of the sibling portal, in a round whose question is the vendor's public surface | capture `dd50f086f…`; staged header r43:2 |
| `cnki-comparison-basis-r46.md` | **refuse** | (a) Its numeric tally does not reproduce: it states a 13,527-character extraction in which 比对 occurs ten times; the capture `9c3aca54…` (.txt, 52,741 bytes) is 28,114 characters / 20,484 non-whitespace, and 比对 occurs 25 times — no reading I can construct yields 13,527 or ten, and the entry names no counting command (QUALITY 37). (b) Its closure inference ("the feature's query-formation rule is nowhere among them") is falsified by the same document set: the admin manual's §6.1 states the rule and the submission (offsets 30738/30793 above). (c) S175 was not re-grounded this round. | re-scope to the observation only (policy names comparison libraries; 引文核对 0, 匹配 0, 比对 25, 优先出版文献库 1×) with a re-derived count and a bound row, and delete the closure inference | capture `9c3aca545…`; staged header r46:2 |
| `cnki-citation-check-query-r47.md` | **refuse** | Its frame is a correction of "round 12's denial" — a claim the lane never made: at HEAD, `grep -rc '引文核对\|引证检索' corpus/knowledge/*.md corpus/SOURCES.md` has zero non-zero hits. It also mis-cites its document: it calls the manual "the document the corpus has held since round 5 as S119", but staged S119 is 系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读 on SinoMed — the admin manual is S124. Its substance (paste, press 搜索, compare against 中国知网's 文献资源) is already carried by the admitted r41, so admitting both would duplicate one claim on one document (QUALITY 9). | a round whose theme needs the query-formation sentence as its own entry (not as a correction), standing on the bound S105 row | staged S119 row URL; grep sweep verdict; staged header r47:2 |
| `citation-check-status-vocabulary-r48.md` | **refuse** | Restates r40's three states on the same document and capture (staged S187 and S124 both name gs.sxu.edu.cn/…9e5cdd21….pdf → capture `e3ca8f4f…`), and it disagrees with r40 on the middle marker's colour — r48 "orange", r40 "amber", capture says 橙色 (橙色 1, 琥珀 0) — so both cannot be admitted as-is. It repeats r47's S119 mis-citation and the round-12/13 correction narrative. Its only residue (the 状态、篇名、作者和文献来源 column list and the 红色提示) is one sentence, foldable into r40; it does not justify a second entry on one document. | r40's admission fails, or a frozen question on the status vocabulary needs its own entry — then admit on S105 with 橙色 and no S119 | capture `e3ca8f4f…`; staged header r48:2 |

## Refused-doc line (to land in `corpus/lessons/round-50.md`)

```
refused-doc: https://bs.bnu.edu.cn/docs/20160407183946745914.pdf — CNKI 大学生论文管理系统使用手册（教师）, mirror 北京师范大学; tier-C negative-scope row; refused this round (Gate): negative-only, 2016 capture, duplicates the 子账号 manual's absence; no lane row, no source: line
```

## Cross-reference S tokens to drop in the admitted entries

r40: `S076` (lane row, GNU sed manual), `S109`, `S111` (staged rows, other documents), `S124` → renumber to S105.
r41: `S135` → S105, `S136` → S106, `S145` → drop (refused).
r39: `S118` → S104.
(r42/r43/r46/r47/r48 are not admitted; their ids are moot.)

## Checks run (all output observed this wave)

- Term sweep, lane HEAD: `grep -rc '引文核对\|引证检索' corpus/knowledge/*.md corpus/SOURCES.md` → no non-zero lines (the only corpus hits are round-49 spot-check prose and the round-50 counter/claims, not knowledge or SOURCES).
- Capture measurements (python3, one block): numbers in the table above — 子账号 30,937 chars, zeros ×3; 教师 9,914 chars, 引文核对 0, 全文（标明引文） 8;  admin 38,174 chars; policy 28,114/20,484, 比对 25, 引文核对 0, 匹配 0; gb-manual/tmlc counts above.
- `python3 tools/inference-ground.py --entry <staged entry> --spans /dev/shm/chousa-r50-DraftGateTable/empty-spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root <staged knowledge dir>` (empty header-only spans manifest): r40 rc=1 5 findings; r41 rc=1 1 finding (INF_NO_BULLETS); r39 rc=1 8 findings. `GROUND: FAIL` printed for all three.
- Staged-row identity greps (SOURCES.append.md): S109 = 日本健康教育学会誌 review-basics article; S111 = PRISMA-S interpretation (梅斯医学); S119 = PRISMA-S interpretation (SinoMed); S170 = 药品临床综合评价…质量控制规范 2024版 (hdpr.shd…).
- Freshness (QUALITY 71): newest capture the lane may read is `a190e843af842a48739defc5.txt`, 2026-10-24 23:26:57; the four theme captures were written 2026-10-23 20:39 – 2026-10-24 10:13.

VERDICT: I drafted the round-50 assimilation Gate table for the eight CNKI-cluster entries — admit-with-narrowing for r40/r41/r39 (inference-ground failures, 橙色-vs-amber, S109/S111/S119 mis-citations, stale ISTIC Unknown, refused 教师 manual), admit-later r43, refuse r42/r46/r47/r48 — and verified every reason against the on-disk captures and the lane registry.
