# R57W1ScoutR2Gaz — R2 gazette/reprint scouting (round 57, wave 1)

Seat: scout (web-search only, 0 fetches). Target: R2 = 国家卫生健康委办公厅《关于规范开展药品临床综合评价工作的通知》（国卫办药政发〔2021〕16号）, which S127's `2 规范性引用文件` lists.
Frozen-rule axis: defined text form must hold token `〔2021〕16号` AND a one-line heading that, whitespace/paren-tail-stripped, ends with title `关于规范开展药品临床综合评价工作的通知` (prefix ≤16 chars, no 《》.[]［］).

## 1. Held gazette cannot bind — re-verified against committed bytes

`file corpus/captures/53a92273a452a58f28368691.raw` → `PDF document, version 1.4, 31 page(s)`; sha256 = `460121b411d754f94c597b8d20066c45901a729c5d88f7f86fb065057cb5da84` (first 64 hex).
`pdftotext -layout …raw -` at the body (printed p.21) gives the heading as two lines:

```
      国家卫生健康委办公厅关于规范开展药品临床综合
                     评价工作的通知
```

Probe of the frozen counter (imported read-only via importlib, run in scratch):

```
heading_title(gazette body): False        # neither split line ends with the full title
token 〔2021〕16号 in nows(form): True      # "国卫办药政发〔\n2021〕16号" strips to 国卫办药政发〔2021〕16号
heading_title(one-line h1): True          # prefix "国家卫生健康委办公厅" = 10 chars ≤ 16, no brackets
```

Conclusion: held 公报 2021·07 = right doc, fails only the heading rule. Any single-line rendering binds if fetched.

## 2. Answer to the nhc.gov.cn sub-question

YES — www.nhc.gov.cn serves the notice's own HTML page, title as page heading (NHC notice template; list page www.nhc.gov.cn/yaozs/c100097/new_list_2.shtml prints the full one-line title). Two channels found. CAVEAT: the yaozs URL **is the C2-pinned S132**; refetch.tsv shows attempt 1 = http 412 (curl_rc 22) and its lazy archive twin 404 — plain curl is WAF-blocked, so a lane fetch needs headers/retry (L1's job, not mine). No m.nhc.gov.cn mobile page was found in any search — mobile sub-question answer: not served / not indexed.

## 3. Ranked candidates (5+ required; 13 found)

| # | URL | Type | One-line title evidence (snippet) | Token | Fit |
|---|-----|------|-----------------------------------|-------|-----|
| 1 | https://www.nhc.gov.cn/yaozs/c100097/202107/d2a45e6ae041423f950b3865e43f5ef6.shtml | NHC own page (=S132) | page h1 = full title; body "国卫办药政发 〔 2021 〕 16 号 各省…" | yes | A, blocked by 412 |
| 2 | https://www.nhc.gov.cn/wjw/c100175/202107/58a87de5349a484e9ef87b8ac0a32ce7.shtml | NHC 政府信息公开 dup | full body snippet; 文件名称 = full title | yes | A, same WAF risk |
| 3 | https://wsjkw.hebei.gov.cn/zcfg2/380991.jhtml | 河北省卫健委 full-text repost | page title "国家卫生健康委办公厅关于规范开展药品临床综合评价工作的通知---河北…" | yes | A |
| 4 | https://wsjkw.qinghai.gov.cn/zwgk/jgzn/nsjg/ywzcyjbywzdc/gzdt_6118/202108/t20210830_204140.html | 青海省卫健委 repost | title shown one line in result | yes | A |
| 5 | https://doc.docsou.com/bdf846b6db364558e3ad13c59b333b30705f22ef5.html | mirror HTML full text | snippet begins notice body; title = page heading | yes | B |
| 6 | https://www.pharnexcloud.com/data/zcfg_546372fed05fbed1fa6fb3600f264192.html | 摩熵医药 policy DB | "国卫办药政发〔2021〕16号国家卫生健康委办公厅关于规范开展药品 …" | yes | B |
| 7 | https://www.nmgyyxh.org.cn/nmgyyxh/zcfg/686cdcc3f266ba2c90c8412d.shtml | 内蒙古药学会 repost | title one line | yes | B |
| 8 | https://www.sohu.com/a/480763225_121123735 | Sohu full-text reprint | title + "_管理" one line | yes | C (commercial) |
| 9 | https://cmei.org.cn/uploads/20210804/9b15e786d682e9618949a5273dc44aeb.pdf | digest PDF (2021\|07.31) | likely single-column reprint; layout unverified | likely | C, needs fetch |
| 10 | https://www.nhc.gov.cn/bgt/201807sgf/202109/5e18d6d8d86e405bad64dd4a8b666310/files/1733795726978_35780.pdf | NHC serving of the SAME 公报 2021·07 | TOC snippet splits title ("…综合 评价工作的 通知"); body two-column | yes | does NOT fix split — identity corroboration only |
| 11 | CNKI 政报公报库 record for 公报 2021年07期 (mirror seen: 210.44.9.79:88/urtpweb/jdetail?sysid=23&pykm=WSGB&year=2021&issue=07) | CNKI per-article page | DB record titles print one line | yes | D, paywalled/unfetchable |
| 12 | https://web.archive.org/web/*/https://www.nhc.gov.cn/yaozs/c100097/202107/d2a45e6ae041423f950b3865e43f5ef6.shtml | Wayback calendar | no confirmed snapshot (lazy /web/2024/ twin 404'd in refetch) | n/a | D, unverified |
| 13 | https://wjw.chengde.gov.cn/art/2021/7/29/art_464_784401.html | 承德市卫健委 news | quotes 《关于规范开展药品临床综合评价工作的通知》 one line in body | yes | C, news not full text |

## 4. Notes for L1 / connectors

- Best bind path: #1 or #2 (official, heading = h1, token in body) — but both must beat the 412 (browser-like UA/headers/retry) to land a successful attempt row in refetch.tsv; #3/#4 (provincial .gov reposts) are the fallback with no observed WAF.
- #10 is the SAME two-column gazette under a different NHC URL — useful to corroborate the orphan capture's identity, not to bind R2.
- Overlap flagged: candidate #1's URL is already pinned as S132 in C2's frozen 47; a C3 bind via it needs its own successful attempt recorded for (row,URL) and a non-S127/128/129 registry row.
- No tools installed (none needed): only system `pdftotext`/`python3` used; no pacman, no network fetches.

## 5. Sweep line for the entry (if R2 stays unbound)

`- UNBOUND R2 sweep: "关于规范开展药品临床综合评价工作的通知" 16号; hosts: nhc.gov.cn (yaozs/wjw, 412 to curl), wsjkw.hebei.gov.cn, wsjkw.qinghai.gov.cn, doc.docsou.com, pharnexcloud.com, nmgyyxh.org.cn, cmei.org.cn; gazette 公报2021·07 two-column split confirmed in held capture 53a92273a452a58f28368691`

Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ScoutR2Gaz` (gaz.txt + probe) deleted after report write; TMPDIR/PYTHONDONTWRITEBYTECODE were set inside it. Lane writes: this file only.

VERDICT: attacked R2's gazette angle — held 公报 2021·07 confirmed non-binding by direct byte evidence, 13 candidate URLs located (3 official/primary, 10 mirrors/compilations) with nhc.gov.cn's own one-line-title HTML page confirmed existent but 412-blocked; scouting survived, no fetches made.
