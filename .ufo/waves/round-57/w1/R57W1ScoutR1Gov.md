# R57W1ScoutR1Gov — R1 (国卫药政函〔2019〕80号) second-angle URL scout

Seat: scout (leaf, no subagent dispatch). Claim worked: R57-C3 (depth, sourced). Target reference: R1
`关于开展药品使用监测和临床综合评价工作的通知` / token `〔2019〕80号` (c3-count.py REFS[0],
corpus/evidence/round57/c3-count.py:75). Method per seat spec: web search ONLY over provincial health
commissions (wjw/wsjsw.*.gov.cn), cnpharm.com, sinopharm/industry-association mirrors, academic course
packs. NO fetches (scout seat). Ranked for the C3 heading rule (defined text form must hold the title as a
heading, ≤16-char clean prefix) and HTML-over-PDF preference. Nothing frozen was touched; the only write
is this report. First-angle scout R57W1ScoutR1 covers site:nhc.gov.cn/site:gov.cn; no sibling report was
present in .ufo/waves/round-57/w1/ at write time (`ls` showed only swarm-registry.json).

## Evidence base (commands = web_search calls; outputs = returned snippets)

Searches run (all 2026-10-27, seat R57W1ScoutR1Gov):
1. `国卫药政函〔2019〕80号 关于开展药品使用监测和临床综合评价工作的通知` (general)
2. `"国卫药政函" "2019" "80号" … site:wjw.*.gov.cn` (relaxed by engine; no direct wjw.* hit)
3. `"国卫药政函〔2019〕80号" OR "关于开展…" site:cnpharm.com` (relaxed; 0 cnpharm hits)
4. `"关于开展药品使用监测和临床综合评价工作的通知" 卫生健康委 转发 site:gov.cn`
5. `"国卫药政函〔2019〕80号" 药品使用监测 临床综合评价 全文` (aggregated full text; surfaced cnpharm docx)
6. `cnpharm.com 98980.docx 药品临床综合评价` (identification of docx)
7. `"关于开展…通知" 2019 … 广东 OR 江苏 OR 浙江 OR 四川 OR 山东 wjw`
8. `"国卫药政函〔2019〕80号" site:edu.cn` (0 hits)
9. `"关于开展…通知" 协会 OR 学会 OR 药业 OR 医药 全文 2019`
10. `gcpunion.org 国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知`
11. `"转发" "关于开展…" 2019 省卫生健康委 wjw.gd.gov.cn OR wjw.sc.gov.cn OR wjw.henan.gov.cn OR wsjkw.sh.gov.cn OR wjw.beijing.gov.cn`
12. `nmgyyxh.org.cn 国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知`
13. `"国卫药政函" "2019" "80号" 课件 OR 讲义 OR 课程 OR PPT 药事管理`
14. `wsjsw.linyi.gov.cn 11703 药品使用监测 临床综合评价 国卫药政函`
15. `cmea-cmec.com 国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知 334`
16. `waizi.org.cn 62262 国卫药政函 2019 80号 药品使用监测`
17. `"国卫药政函〔2019〕80号" 卫生健康委 湖南 OR 安徽 OR 福建 OR 陕西 OR 重庆 OR 广西 OR 云南 通知`

## Ranked candidate table (R1 binding candidates, this angle)

Rank | URL | Host / page kind | One-line title (as printed) | 〔2019〕80号 evidence from snippet
---|---|---|---|
1 | https://wsjsw.linyi.gov.cn/info/1040/11703.htm | 临沂市卫生健康委员会 (city health comm., .gov.cn HTML) | 国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知 | full text opens 为贯彻落实党中央…现就开展药品使用监测和临床综合评价有关事项通知如下 (search 1/14, src[10] "…通知-临沂市…")
2 | https://www.nmgyyxh.org.cn/nmgyyxh/zcfg/686cdcc3f266ba2c90c83be7.shtml (mobile: https://m.nmgyyxh.org.cn/sjz/zcfg_sjz/6870847af2664b4e33a51881.shtml) | 内蒙古医院协会 政策法规 (industry-association mirror, HTML) | 国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知 | snippet: "来源：国家卫生健康委网站 时间：2019-04-18 10:25:59. 国卫药政函〔2019〕80号. 各省、自治区、直辖市…" (search 12, src[1]); list page confirms 2019-04-18 (src[2])
3 | http://www.gcpunion.org/portal/article/index.html?id=2395 | 中关村玖泰药物临床试验技术创新联盟 政策法规 (industry-alliance mirror, HTML) | 国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知 | 政策法规 list page 9: "国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知 2019-04-10" (search 10, src[8]); detail page src[8] of search 17 dated 91mo ago
4 | https://www.waizi.org.cn/doc/62262.html | waizi.org.cn repost (non-gov) | 国卫药政函〔2019〕80号《国家卫生健康委关于开展药品使用监测和临床综… | snippet: title + full opening paragraph (search 16, src[8]); heading prefix carries 《 after the 文号 → likely FAILS the BAD_PREFIX heading rule; keep as fallback only
5 | https://www.cmea-cmec.com/nd.jsp?groupId=9&id=334 | 中国医药教育协会 药品研究与临床评价工作委员会 (industry assoc.) | 国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知 (per search 1 src[9], "中国…") | fetch failed in engine (search 15); title/token unverified — speculative
6 | https://scd.fudan.edu.cn/45/f6/c39942a476662/page.htm | 复旦大学 药学院 药品政策法规动态汇编（2019年4月） (academic pack, HTML) | 汇编 page (title is a monthly compilation, not the notice) | unverified snippet; heading rule would fail on this page even if the notice text is inside

Cross-check (first scout's territory, listed for ranking completeness only): NHC official
https://www.nhc.gov.cn/yaozs/c100097/201904/6bc8f973684845d3ab76fed841eb42d2.shtml — confirmed canonical
full text w/ 文号 in line 1 of body (multiple searches, src[3]/src[29]-class snippets).

## Citing-only pages found in this angle (NOT binding candidates — title heading is their own)

- http://wjw.hubei.gov.cn/zfxxgk/zc/gkwj/ywh/202106/t20210630_3622439.shtml — 湖北省卫健委办公室 2021 通知 (鄂卫办通〔2021〕42号); body cites 《…通知》（国卫药政函〔2019〕80号）.
- https://wjw.xinjiang.gov.cn/hfpc/zhgl41/202604/418bf075c1a74a81b2482429900ce54c.shtml — 新疆 2026 项目申报通知; cites 80号 in body.
- https://wsjk.ln.gov.cn/wsjk/index/syxwxx/zwgk/E0315A064035445AB75FBE83E3E9D5AC/P020220210321828195300.docx — 辽宁省药品临床综合评价工作方案.docx; cites 80号 (docx, not the notice).
- http://www.sinopharmacy.com.cn/notification/2526.html — 广东省药学会 DPP-4 共识发布通知; cites 80号 (sinopharmacy = 广东省药学会, an industry-association host, but no republication of R1 itself found there).
- https://ylqxzb.com/ZBZcfg/Item84e33c7a673d0c38.html — repost of 上海 沪卫药政〔2021〕8号 (2021 local follow-up, not R1).

## Negative findings (this angle, reported for the UNBOUND sweep line)

- cnpharm.com: zero notice pages. The one surfaced attachment http://www.cnpharm.com/upload/resources/file/2021/09/15/98980.docx was identified per search 6 (src[17]-class) as 附件 2021年8月批准注册医疗器械产品目录 — UNRELATED to R1. cnpharm.com = dead end for R1.
- Province-level wjw.*.gov.cn: no province-level republication of the 2019 notice found across 12+ provinces swept (GD/JS/ZJ/SC/SD/HN/AH/FJ/SX/CQ/GX/YN + SH/BJ + Hubei/Xinjiang/Liaoning). Only city-level 临沂 wsjsw.linyi.gov.cn (rank 1) republishes the full text.
- Academic course packs: site:edu.cn with the 文号 → 0 hits; 课件/讲义/PPT sweeps found only adjacent materials (2019 药品管理法 PPT, 药物经济学课件) that do not carry the 文号.

## Calibration notes for the L1 / binding executor

- Best bindable from this angle: rank 1 (Linyi, gov health authority, exact one-line heading, HTML) and rank 2 (内蒙古医院协会, exact title + 文号 + 来源 line, HTML). Both fit the ≤16-char clean-prefix heading rule (prefix "国家卫生健康委" = 8 chars).
- Rank 3 (gcpunion) needs a fetch-time check that the detail page's defined text form carries the title as a heading (list evidence is strong; detail-body evidence is indirect).
- waizi (rank 4) likely fails the BAD_PREFIX heading rule — do not spend a fetch on it unless ranks 1–3 all fail.
- All findings are reported, not patched; no counter/predicate/target/recipe was touched. No fetches performed (scout seat). Scratch dir /fast/scratch/hyaku/chousa-r57/R57W1ScoutR1Gov created and removed (`rm -rf`, verified). No tools installed. Lane repo untouched except this report file.

VERDICT: scouted R1 second angle (provincial WJW + cnpharm + sinopharm/industry mirrors + academic packs) — 2 strong HTML binding candidates located (wsjsw.linyi.gov.cn full-text repost; nmgyyxh.org.cn association mirror), cnpharm.com and province-level wjw.*.gov.cn and edu.cn courseware angles falsified as sources; report survives.
