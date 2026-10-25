# Round 50 lesson

author: chousa L1 (hyaku run 7, `ChousaR50`)
date: 2026-10-25
base: `3c51da77b3696ed884c943548ec4b4006e3ca528`
freeze: `6a068f2ae4847a1e4aa959f088a39ddc1b167bc0`

No external fetch or network egress: L0 `8d77e6c1` remains open. Every source re-opened below is an on-disk capture under the read-only campaign cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`, accessed 2026-10-25 (captures written 2026-10-23 and 2026-10-24). Decode form: every `char N` below is an offset into the capture's `.txt` read as UTF-8 (`pdftotext -layout` of the PDF for the three CNKI manuals — `GroundSxuStates` proved the `.txt` is that rendering byte for byte; the page text for the ISTIC page, whose `.raw` is HTML). C1 is plumbing; C2 is ground (QUALITY 64). This is the lane's second package-adoption round under addendum section 10.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| number-drift: a restated count kept the old figure after its manifest grew | `corpus/QUALITY.md:746` prints `IDS=8 QUOTES=28 FAILURES=0`, `corpus/README.md:1074` says "28-row manifest", `LOG.md:1803` says "28 located quotes … `CAPTURE_BOUND=28/28`", `corpus/lessons/round-49.md:20` repeats `QUOTES=28`; `corpus/evidence/round49/measure-after.txt` and `spans.tsv` carry 31 (`awk 'NR>1 && NF' corpus/evidence/round49/spans.tsv \| wc -l` → 31); round-49 spot-check defect 2 (`corpus/lessons/round-49-verifier-spotcheck.md:96`) | QUALITY 37 (a tally carries its command) named the command and nobody re-ran it; QUALITY 9 (one home per number) | `corpus/evidence/round50/stale-count-check.py` (QUALITY 74): before the correction lines it prints four `STALE … says 28, receipt 31`, exit 1; after the append-only `correction: … superseded by …` lines it prints `STALE_COUNT=PASS`, exit 0 (receipts `corpus/evidence/round50/stale-count-before.txt`, `stale-count-after.txt`) |
| landing: the round-49 closure report was filed before WAVE-DONE of either wave, with seat reports it named as outstanding still uncommitted | `.ufo/reports/round-49/chousa.md` §"Conformance defect" (W1 39/40, W2 27/35); spot-check defects 1 and 4 (`round-49-verifier-spotcheck.md:95,98`) | QUALITY 61 (a dispatch is complete only when every seat settled) — it did not name the filing order | `corpus/evidence/round50/wave-complete-check.py` (QUALITY 75): at `5275c892` it prints `MISSING` for the round-49 w2 gaps, exit 1 (`wave-complete-before.txt`); this round's report is filed only after WAVE-DONE of both waves and the check's output is pasted in the report |
| scope: the adopter's cited set is every staged id token of an entry, body cross-references included, so a body-only id is renumbered and its unrelated document appended | `tools/assimilate-rows.py` docstring ("Tokens that are not staged ids pass through unchanged — checking … is the reader's job"); `w1/ExecAdopt.md` §2: run on the three staged entries gives `CITED=7 APPEND=6`, rows for staged S109 (a Japanese review-basics article) and S111 (a Chinese PRISMA-S interpretation) become lane S104/S105 and every real document shifts by two; staged S076 passes through naming the GNU sed row | none in QUALITY 1–72 (the by-document rule is addendum section 10) | `corpus/evidence/round50/cited-id-check.py` (QUALITY 77): run on the as-staged renumber table it prints `BODY_CROSSREF S109->S104`, `S111->S105`, exit 1 (`cited-id-before.txt`); on the cleaned run `CITED_IDS=PASS`; adoption this round used entries with body-only ids removed |
| attribution: wave 1 reused 13 seat names of round 49; the dispatcher resumed the parked round-49 agents of those names and each answered with its round-49 report | `w1-results.json`: 13 seats (MineConsider, ExecMirrorCensus, ExecInfStaged, ExecReplayC1, ExecFormProbe, CritForgeC1, CritForgeC2, ReviewProvince, ReviewQuarMap, CritTheme, ConnSiblings, ConnCrossClaim, ScoutCoverage) return `.ufo/waves/round-49/w1/<name>.md`; none wrote a round-50 report | none (the validator checks names are unique inside one wave, not across rounds) | `corpus/evidence/round50/name-collision-check.py` (QUALITY 78): on `w1-spec.json` it prints 13 `NAME_COLLISION`, exit 1 (`name-collision-before.txt`); every wave-2 seat name carries the `R50` prefix and the check is run on the spec before dispatch |
| vacuous: the C2 inference leg was unattainable for pure-Chinese captures — `inference-ground` counted grounding words by ASCII letters, so a correctly grounded Chinese bullet read as zero tokens (`INF_UNGROUNDED`); round 49 passed only because its quotes held Latin runs | `w1/DraftEntryR41.md` F1 (`tokens=0`, 4 × `INF_UNGROUNDED`, rc=1 on a grounded draft); `w1/DraftEntryR39.md` (the unmodified tool's phrase leg read only fee figures); `tools/inference-ground.py` `has_two_words` | QUALITY 66 states "two or more words" without a script condition | `has_two_words` also accepts four CJK characters; `corpus/evidence/round50/cjk-ground-check.py` (QUALITY 79): case A correct bullet rc 0 (old tool rc 1 `INF_UNGROUNDED`), case B a CJK phrase absent from the span rc 1 `INF_TOKEN_NOT_IN_SPAN`, case C no id rc 1 `INF_UNCITED`; round-46/47/48 counters unchanged (`inference-regression-before.txt` = `-after.txt`) |
| vacuous: the new `--selftest` compared findings as sets, so a duplicated expected line passed and the doubled finding of a future regression would pass too; three lower defects (`--selftest` silently ignoring normal options, a trailing-space `ENTRYCITES` line, no work floor for a fixture with no entry) | `w1/ReviewSelftestCode.md` F1–F4 (repro: `SELFTEST=PASS findings=26 expected=27`, rc 0); `w1/ExecSelftestEdge.md` (a), (d), (f2) | the frozen C1 counter has no duplicate-line perturbation (its P1–P6 each change a distinct finding) | `tools/assimilate-rows.py` multiset comparison (`collections.Counter`), exit 2 on option clash or no entry, `ENTRYCITES … -`, 120 s child timeout, tab-free findings; the frozen counter stays `LEGS=5/5`; duplicate probe now prints `DIFF missing TOOLEXIT 0`, rc 1 (`selftest-duplicates-after.txt`) |
| reference-drift: the staged entries disagreed with their own document — the middle result state is "amber" in two staged entries and "orange" in a third; the PDF says 橙色 | `w1/GroundSxuStates.md` §3, §5 (橙色 1, 琥珀 0, 黄 2 in the similarity report only); staged `cnki-citation-check-r40.md` and `citation-matching-semantics-r41.md` say amber, `citation-check-status-vocabulary-r48.md` says orange | QUALITY 29 (a quote names its location) would have caught it only if a quote of the state sentence had been located | both adopted entries use the PDF's word, located at char 31063; the counter's `QUOTES_IN_ENTRY` leg holds the quote |

## Spot-check intake

| round-49 routed item | round-50 disposition |
|---|---|
| 1. Late seat reports uncommitted | Committed: `MutA05`, `MutSubstance`, `ReviewQuality` (`4d13657e`), `ScoutInherited`, `ScoutPlanned` (`ec52e632`; `ScoutPlanned` modified again later by its live round-49 seat, committed `2573dc16`). |
| 2. Stale quote count (28 vs 31) | Corrected by append-only `correction:` lines in `corpus/QUALITY.md`, `corpus/README.md`, `LOG.md` and `corpus/lessons/round-49.md`; `stale-count-check.py` exit 1 → 0 (Mistakes row 1). |
| 3. Gate standard — self-test and digest pin | `tools/assimilate-rows.py --selftest` with a hand-written `expected.json`, a printed fixtures digest and the counter's digest pin (C1, QUALITY 73). The round-49 counters stay one-shot frozen counters, not reused gates; the row says so (SKILL.md Gates). |
| 4. Report before WAVE-DONE | This report is filed after WAVE-DONE of both waves (Mistakes row 2; QUALITY 75). |
| 5. Decode form next to offsets | Every offset in this Gate names its form; QUALITY 76. |
| 6. Prompt commit attribution | Not lane-owned: the prompt `.ufo/prompts/chousa-round-50.md` is not committed by this lane. |

## Gate

### Collision check (section 10, 0–3-space pattern, scratch)

Run from `.ufo/waves/round-50/assimilation/` (`ExecCollision`): registry ids `reg-ids` 103 lines (S001–S103), staged ids `staged-ids` 114 lines (S082–S195), `collisions` 22 lines (S082–S103). 18 are hard collisions (same id, different document: S082–S099); four are re-staged rows (S100–S103 carry the same URL as the round-49 rows). The staged file digest is the round-49 pin (`a6dec4a0086d3cf767d638d7e52fdda08f78d22b0b376049b0ad14ff0f8aa696`). Guard proof (`guard-proof.txt`): a two-space-indented `  | S002 | y |` registry row against a staged `| S002 | x |` gives a nonempty collisions list under the 0–3-space pattern and an empty one under the column-zero pattern. Collisions are fixed in scratch only: adopted ids continue the lane registry and every citation is re-pointed by document.

Renumber map (`assimilation/renumber.tsv`, adopter run on entries with body-only ids removed): staged S118 → S104 (ISTIC page); staged S124 → S105 and staged S135 → S105 held (CNKI 管理员 manual, one document; staged S180 and S187 name the same URL and are not cited); staged S136 → S106 (CNKI 子账号 manual); staged S145 (CNKI 教师 manual) refused, no lane id. Body-only ids in the staged entries (S076, S109, S111) were removed or replaced by a lane file path.

Scratch validation before the append: `assimilation/validate/census.txt` — `sources-census.sh validate --file` on a mirror of the base registry plus `assimilation/append.md` plus the lane lessons, tools and the three entries: exit 0, the five pre-existing W04 warnings only.

### Re-opened sources (access 2026-10-25; no fetch)

| lane id | document | URL | decode form | headline quote (location) |
|---|---|---|---|---|
| S104 | ISTIC-named service page, in fact 中国科学院文献情报中心 引证检索 (the path says istic; the page names the Chinese Academy of Sciences centre: 中国科学院 5 × and 中国科学技术信息研究所 0 × in the capture) | https://chaxin.las.ac.cn/service/citation-search | `.txt` UTF-8, 2288 characters (the `.raw` is HTML) | 按合作者排除自引标准统计他引次数 (char 549, the 收费标准 其他 row) |
| S105 | CNKI 知网学位论文学术不端行为检测系统使用手册（管理员）, 更新时间 2020 年 7 月, copy hosted by 山西大学 | https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf | `.txt` UTF-8, 38174 characters (`pdftotext -layout` of the 57-page PDF) | 第二类是橙色的标识 (char 31063, §6.1 引文核对 under 第 6 章 辅助功能) |
| S106 | CNKI 大学生论文管理系统使用手册（子账号）, V 5.0, copy hosted by 东南大学 | https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf | `.txt` UTF-8, 30937 characters | 在创建文件夹页面中第一个选项为“仅去除第一作者本人文献” (char 22511, §2.6) |

Refused document (no lane row): CNKI 大学生论文管理系统使用手册（教师）, copy hosted by 北京师范大学, https://bs.bnu.edu.cn/docs/20160407183946745914.pdf — `.txt` UTF-8, 9914 characters; opened 2026-10-25: 引文核对 0, 核对 0, 匹配 0, 引文 9 (all inside 标明引文); a located sentence, 教师可查看的报告单包括简洁报告单、全文（标明引文）报告单、去除本人 (char 8033).

refused-doc: https://bs.bnu.edu.cn/docs/20160407183946745914.pdf — CNKI 大学生论文管理系统使用手册（教师）, mirror 北京师范大学; staged tier C, negative-scope only (it only adds that its report-sheet name 标明引文 is not a checking feature, and carries no in-text version or host); refused this round; flip: a claim of the lane that cannot be carried by the 管理员 and 子账号 manuals alone, with the 教师 manual's date and host located.

All located quotes (every one ≤25 whitespace words, exactly once in the stated form, inside the citing entry; `corpus/evidence/round50/spans.tsv` is derived from this set by `build-spans.py`, and `quote-substance-check.py` exits 0 on it):

| lane id | form | char offset | located quote (≤25 words, exactly once in that form) | cited by |
|---|---|---:|---|---|
| S104 | `.txt` UTF-8 | 194 | 论文收录引用检索（简称引证检索）指通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 194 | 论文收录引用检索（简称引证检索）指通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库，查询个人、团队等的代表性论著收录和引用情况，为职称评定、项目申报、人才评价等需求提供客观、准确的第三方检索报告。 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 211 | 通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库，查询个人、团队等的代表性论著收录和引用情况 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 246 | 查询个人、团队等的代表性论著收录和引用情况 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 268 | 为职称评定、项目申报、人才评价等需求提供客观、准确的第三方检索报告 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 380 | 03 完成并审核 报告 06 出具正式报 告并存档 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 422 | 证明费 300 元/份。提供 1 份证明，需要多份证明，增加 1 份 50 元 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 549 | 按合作者排除自引标准统计他引次数 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 549 | 按合作者排除自引标准统计他引次数， 1 元/篇次 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 662 | 1.委托5篇以内收录检索，检索费300元。 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 684 | 2.针对中国科学院用户： | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 735 | 对于在2年内提供检索要求相同的用户进行多次委托时，用户在提供上次检索结果同时，本次检索可免去相同数据的费用 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 849 | 将一周之内的网络检索结果打印后到我中心进行复核 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 849 | 将一周之内的网络检索结果打印后到我中心进行复核，复核收费为：收录5元/篇，引用按提供论文数每篇20元 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 1236 | 出具1个检索报告即填写1项委托；需要多个检索报告，需逐个填写委托单 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 1380 | 所有文章必须包括全部作者（全拼）、标题、期刊、年、卷、页码、DOI等完整信息 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 1469 | 委托论文在10篇以内可在5个工作日完成报告（不含邮寄时间），超过10篇双方协商完成时间 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S104 | `.txt` UTF-8 | 1784 | 检索报告默认提供打印盖章文件1份，且仅打印报告正文，不含附件 | `corpus/knowledge/istic-citation-verification-r39.md` |
| S105 | `.txt` UTF-8 | 48 | 更新时间：2020 年 7 月 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 27587 | 创建文件夹时，设置文件夹的属性中，第一个选项为“仅去除第一作者本人 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 30661 | 第 6 章 辅助功能 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 30738 | 引文核对是指，以“中国知网”的文献资源为核对源内容 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 30745 | 以“中国知网”的文献资源为核对源内容 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 30778 | 以核对引文内容的正确性 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 30793 | 把待检测文献的参考文献复制到“引文核对”文本框 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 30880 | 状态、篇名、作者和文献来源 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 30947 | 第一类是“没找到” | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 30947 | 第一类是“没找到”，表示经过核对，没有找到与输入的这条引文一一对应 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 31101 | 但是引文中有某一部分的信息与源内容不同 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 31218 | 各项内容都相同 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 31273 | 两两比对是将输入的两篇文献进行比对 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S105 | `.txt` UTF-8 | 48 | 更新时间：2020 年 7 月 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 30661 | 第 6 章 辅助功能 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 30745 | 以“中国知网”的文献资源为核对源内容 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 30778 | 以核对引文内容的正确性 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 30778 | 以核对引文内容的正确性。 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 30800 | 参考文献复制到“引文核对”文本框，点击“搜索”按钮， | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 30844 | 系统会将搜索到的有关引用文献的详细情况以列表形式展示在下方 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 30878 | 容有状态、篇名、作者和文献来源。 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 30879 | 有状态、篇名、作者和文献来源。 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 30880 | 状态、篇名、作者和文献来源 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 30935 | 态共分为三种类型： | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 30947 | 第一类是“没找到” | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 31063 | 第二类是橙色的标识 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 31079 | 表示系统经过核对已经找到了该条引文记录 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 31101 | 但是引文中有某一部分的信息与源内容不同 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 31137 | 提示具体哪部分不同，列表中对应的内容也会红色提示。 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 31169 | 第三类则是绿色的标识 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 31206 | 相同，鼠标放上去也会提示各项内容都相同。 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 31209 | 鼠标放上去也会提示各项内容都相同。 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 31218 | 各项内容都相同 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S105 | `.txt` UTF-8 | 31233 | 列表中的“篇名”可以点击，链接到该引用文献的详细信息。 | `corpus/knowledge/cnki-citation-check-r40.md` |
| S106 | `.txt` UTF-8 | 83 | 产品名称：“中国知网”大学生论文管理系统使用手册 | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S106 | `.txt` UTF-8 | 22511 | 在创建文件夹页面中第一个选项为“仅去除第一作者本人文献” | `corpus/knowledge/citation-matching-semantics-r41.md` |
| S106 | `.txt` UTF-8 | 22549 | 该文件夹下的所有检测文献在去除本人文献检测结果中 | `corpus/knowledge/citation-matching-semantics-r41.md` |

### Absent-defect register rows on the theme URLs

Section-10 slice (`awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'` over the campaign register): 24 data rows. Sweep for the four theme hosts over the slice's URL column — `awk … {print $6}` then `grep -c -e 'gs.sxu.edu.cn' -e 'rwxy.seu.edu.cn' -e 'bs.bnu.edu.cn' -e 'chaxin.las.ac.cn'` → `0`; the same `grep -c` over the whole register file → `0`. No register row names a theme URL, so there is no row to re-check and the counter's `QUARANTINE_VERDICTS=0/0` is vacuous by construction; the record is the sweep, not a verdict. Slice rows for other URLs stay quarantined (round 48 holds their 24 verdicts).

### Decisions

| entry | decision | reason | flip | evidence |
|---|---|---|---|---|
| `cnki-citation-check-r40.md` | admit, narrowed | the feature's definition and three states are located in §6.1; narrowed: 橙色 not amber, the staged 诚信档案 attribution dropped (诚信档案 0 in the capture), body ids and a live-fetch note dropped | the manual's §6.1 changes | `w1/GroundSxuStates.md`, `w1/DraftEntryR40.md` |
| `citation-matching-semantics-r41.md` | admit, narrowed | the "no matching method is documented" negative carries its sweep (匹配 0 in 38174 characters; the §6.1 slice has 算法 0, 相似度 0); narrowed: "not an author-year or string-similarity algorithm" became "undocumented", the 教师 manual dropped, "documented on the administrative side" became a product fact (two products) | a manual that documents a matching method | `w1/DraftEntryR41.md`, `w1/ExecNegSweep.md` |
| `istic-citation-verification-r39.md` | admit, narrowed | a second institutional authority for the co-author self-citation boundary, stated in a price line; narrowed: the reuse concession sits under `2.针对中国科学院用户：` (char 684) and is discretionary (可免去), "CNKI's feature remains unopened" replaced by a path pointer, "a property of Chinese citation practice" narrowed to what two documents state | the page's 收费标准 or workflow changes | `w1/GroundIsticRecheck.md`, `w1/DraftEntryR39.md` |
| `cnki-citation-check-query-r47.md` | refuse | it corrects a statement of "round 12" that the lane never made (`grep -rc '引文核对' corpus/knowledge` was empty at base) and mis-cites its document; its substance (paste, press 搜索) is carried by the admitted r41/r40 | a round whose question needs the query-formation sentence as its own entry | `w1/DraftGateTable.md` |
| `citation-check-status-vocabulary-r48.md` | refuse | repeats r40's three states on the same PDF; its "orange" is right and its residue (the four result-list columns) is folded into r40 | r40's admission fails | `w1/GroundSxuStates.md` |
| `cnki-matching-modes-r42.md` | refuse | its own text says the matching modes govern the search platform, not 引文核对; S149's capture was not re-grounded | a frozen question on CNKI's search-platform taxonomy | `w1/DraftGateTable.md` |
| `cnki-comparison-basis-r46.md` | refuse | its tally (13,527 characters, 比对 ten times) does not reproduce (capture 28,114 characters, 比对 25) and its closing inference is falsified by §6.1 | a re-scoped observation with its counting command | `w1/DraftGateTable.md` |
| `cnki-public-surface-r43.md` | admit-later | supports the second half of the theme negatively for one surface only; S160 not re-grounded | a bound re-grounded row for check.cnki.net/tmlc/ plus a capture of the sibling portal | `w1/DraftGateTable.md` |

Tier decisions on the appended rows: S104 A (the institute's own page for its own service); S105 B (staged S124 said B, staged S135 said A; the content is the vendor's, the carrier a university file host, so B — the tool keeps the first staged row's cells and the reader decides); S106 B (staged C "negative scope only; flip to B if a CNKI manual with a 引文核对 section is found and opened" — the 管理员 manual is that manual, and the entry's §2.6 claim is a positive statement of this manual).

### Rows appended (3, all `mined`, opened 2026-10-25)

S104–S106 in `corpus/SOURCES.md` (`assimilation/append.md`). Stripped prose kept from the staged rows (`assimilation/stripped.tsv`): S104 recheck `90d — re-open the service page and confirm the self-citation note still reads 按合作者排除自引标准统计他引次数 (ran 2026-10-23)`; S105 recheck `180d — re-download the PDF and confirm 6.1 引文核对 still reads "状态共分为三种类型" (ran 2026-10-23)` (the string is not contiguous in the capture: a line break follows 状, so the entries' recheck line uses 态共分为三种类型); S105 `used-by` staged `corpus/knowledge/cnki-citation-check-r40.md`, widened to both citing entries by the tool; S106 recheck `180d — re-download the manual and confirm the strings 引文核对 and 匹配 still occur zero times in its extracted text (ran 2026-10-24)`; staged opened dates 2026-10-23 and 2026-10-24 replaced by 2026-10-25.

### Wave-2 narrowing

(filled after wave 2)

### Outside spot-check

(pending: the closure's non-author spot-check; every seat this lane dispatched is still the lane)

## considerthese

`considerthese/2026-10-25.md` (the latest file): proposal "Report a capture-age line" was mined in round 49 (QUALITY 71); the other proposals concern the reflection's own format (a "waiting on you" box, leading with spot-checks) and name no lane artefact. Nothing left to mine; the sweep is `grep -n 'Self-improvement proposals' -A 12 considerthese/2026-10-25.md` and the capture-age check below.

## Census

Round start: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, `ok`, five W04 (S051 S053 S073 S074 S075), 103 rows. Round end: (filled at the report).

## Disclosed post-freeze changes

C1 and C2 predicates, counters, controls and targets are byte-unchanged since `6a068f2a` (`git diff 6a068f2a <tip> -- corpus/evidence/round50/c1-count.py corpus/evidence/round50/c2-count.py corpus/evidence/round50/claims.md corpus/evidence/round50/controls corpus/evidence/round50/c1-fixtures`). Changed after the freeze, all outside the counters: `tools/assimilate-rows.py` (selftest hardening and `used-by` widening across twin staged ids — Mistakes row 6; the frozen C1 counter and the round-49 counter still pass); `tools/inference-ground.py` (`has_two_words`, Mistakes row 5; the frozen C2 leg "all three entries exit 0 under `tools/inference-ground.py`" is unchanged and was unattainable for pure-Chinese captures without it); `build-spans.py` and `quote-substance-check.py` are the round-49 files with the round number changed.
