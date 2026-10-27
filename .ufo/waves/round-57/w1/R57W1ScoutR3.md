# R57W1ScoutR3 — R3 (《药品临床综合评价管理指南》2021年版 试行) source-URL scout

Seat: scout (leaf; search-only, no fetches). Claim served: R57-C3 binding of R3 (title `药品临床综合评价管理指南`, token `2021年版`).
Method: 11 `web_search` queries (title+token, notice number, attachment hash, s2908/c100097/wjw pages, nhei.cn, ihpe.org.cn, 中国药房/CNKI/医脉通/健康界 mirrors, provincial reposts); plus reads of lane files. No URL was fetched; rankings rest on search-result snippets and lane captures, so every candidate still needs a fetch to confirm its defined form. Tooling: no installs needed (none performed).

## Trap finding (attack): the most-cited "2021年版" URL serves the 2020 text

`http://www.nhc.gov.cn/cms-search/downFiles/863665c55fd74f29a656990d1a4ea5ce.pdf` is cited BY NAME in the lane's own S129 journal capture as the 2021 edition:
`corpus/captures/5233bf47babaa1ca2b49ed15.txt:536-539` — `[9] 国家药物和卫生技术综合评估中心，国家卫生健康委药 具管理中心 . 药品临床综合评价管理指南：2021 年版试 行 [EB/OL]. [2025-07-10]. http：//www. nhc. gov. cn/cms- search/downFiles/863665c55fd74f29a656990d1a4ea5ce. pdf.`
But two independent search snippets of that exact URL show the 2020 cover text:
- q1 result: "关于药品临床综合评价管理指南公开 | https://www.nhc.gov.cn/cms-search/downFiles/863665c55fd74f29a656990d1a4ea5ce.pdf | 药品临床综合评价管理指南 （试行） 国家药物和卫生技术综合评估中心 （国家卫生健康委卫生发展研究中心） 国家卫生健康委药具管理中心 二〇二〇年十一月 ..."
- q2 engine summary: "it is the filename identifier of a PDF hosted by China's National Health Commission, titled 药品临床综合评价管理指南（试行）… dated November 2020", and it warned the 中国药房 ref's PDF "实际封面标注'二〇二〇年十一月''试行'，与2021年正式版存在版本不一致".
That cover string matches held S130 (`corpus/captures/a42feae4448612f949cc715f.txt:3-4` = `药品临床综合评价管理指南 / （试行）`, dated 二〇二〇年十一月 at char 129 per round-56 spans). Conclusion: the downFiles URL (key 2ad153e4d73281407cf1692c) lacks the `2021年版` token and CANNOT bind R3 — the same failure class as S130. Do not spend one of the C3 fetches on it except to document the trap.

## Ranked candidates (rank = token evidence strength × bare-heading likelihood)

Rank rule from seat: defined form must hold `2021年版` AND a line that, whitespace-removed with one trailing （…） dropped, ends `药品临床综合评价管理指南` under a ≤16-char prefix free of 《》.[]［］. Heading checks below are snippet-based inferences, not measurements.

1. A− `https://www.nhc.gov.cn/yaozs/c100097/202107/d2a45e6ae041423f950b3865e43f5ef6.shtml` (key 2c2a982dd977da3737b6a2b5) — NHC 药政 column, 16号 notice page, 落款 2021-07-21. Snippet: "我委组织制定了《药品临床综合评价管理指南（2021年版 试行）》（以下简称《管理指南》）。现印发给你们" and "附件：药品临床综合评价管理指南（2021年版 试行） 国家卫生健康委办公厅 2021年7月21日". Token ✓×2; the `附件：…` line satisfies the heading rule (prefix `附件：`, 3 chars) if html_to_text keeps it on one line.
2. A− `https://www.nhc.gov.cn/wjw/c100175/202107/58a87de5349a484e9ef87b8ac0a32ce7.shtml` (key 8266eefc0e859892757769a6) — wjw-column repost of the same notice; identical snippet incl. the `附件：药品临床综合评价管理指南（2021年版 试行）` line.
3. A− `http://www.nhc.gov.cn/yaozs/s2908/202107/532e20800a47415d84adf3797b0f4869.shtml` (key 986ad9541aa13fc0fac73ae7) — original s2908 posting of the same 16号 notice (engine confirmed the hash = this notice, posted 2021-07-28); also the URL cited by 中国药房 2025 (case-analysis paper ref [3]) as `药品临床综合评价管理指南：2021年版试行[EB/OL].(2021-07-28)`. Same document as #1/#2.
4. B `https://www.nhc.gov.cn/bgt/201807sgf/202109/5e18d6d8d86e405bad64dd4a8b666310/files/1733795726978_35780.pdf` (key 53a92273a452a58f28368691) — 国家卫生健康委员会公报 (2021年第6号) gazette PDF reprinting notice+指南 full text; snippet opens "国家卫生健康委员会公报2021·07 21 国家卫生健康委办公厅关于规范开展药品临床综合 评价工作的通知 国卫办药政发〔2021〕16号". Token ✓ inside the gazette body; heading likely printed but line-wrapped by layout (wraps join under ws-removal).
5. B `http://www.tcmevidence.net/UserFiles/upload/file/20230410/6381676262587201848492833.pdf` (key 6f545e6c16b6b568ea3f591b) — third-party full-text PDF of the 2021 document (uploaded 2023-04). Snippet: "附件药品临床综合评价管理指南（2021 年版试行） 前言一" and body "药品临床综合评价管理指南 （2021 年版 试行） 前言 一、制定依据 … 国家卫生健康委药政司委托…". Token ✓; heading = the first line if `前言` sits on the next layout line (snippet merges them — needs fetch).
6. B− `https://wsjk.ln.gov.cn/wsjk/index/syxwxx/zwgk/E0315A064035445AB75FBE83E3E9D5AC/P020220210321828195300.docx` (key 0f5bf697278a354ade7a1ade) — Liaoning health-commission DOCX (辽宁省工作方案 附件2 = full 指南 text). OLE raw → defined form via `tools/capture-text.py`. Token expected ✓; heading likely a bare line in extracted text. Caveat: derivative provincial carrier, not the issuing-centre document.
7. C+ `https://www.cn-healthcare.com/article/20210728/content-557909.html` (key 24c7e41e76f060bc0f03ca35) — 健康界 full repost (2021-07-28) of 通知+正文; token in title/正文 ✓; heading: repost formatting unknown.
8. C `https://zk.cn-healthcare.com/doc-show-56610.html` (key 292e795016560c8690eeef57) — 健康界智库 doc page titled 《药品临床综合评价管理指南（2021年版试行）》; token in page title ✓; defined form member-walled — heading unverifiable without fetch.
9. D `https://www.takarabiomed.com.cn/DownLoad/5261.pdf` (key ca3eea7033ce16aab9012dae) — surfaced beside medlive results; document title NOT confirmed by any snippet. Verify identity before spending a fetch.

## Gaps reported (UNBOUND sweep material for the entry)

- ihpe.org.cn: spec-named mirror; `site:` queries and direct identification both failed — domain's owner/content unresolvable this wave (0 candidates).
- nhei.cn (NCMTA host): hosts R4/R5 (`nhei/znfb/202112/…`) and R7 (`nhei/znfb/202412/…`, held as S119 notice) but NO 管理指南 page surfaced — the centre appears not to have reposted the management guideline there.
- CNKI and 医脉通/medlive: no verifiable item page for the 2021 指南 surfaced (the one CNKI-family lead was an unrelated 海南医科大学学报 paper).
- The standalone 2021 PDF attachment that the c100097 page links (`.../d2a45e6ae041423f950b3865e43f5ef6/files/<ts>_<n>.pdf` pattern) did not surface in any search; its exact URL is only discoverable by fetching candidate #1 and reading the committed bytes (allowed two-step: record an attempt for the page URL, parse the `href` from the committed capture, then attempt the attachment URL).

## Fetch-priority note for the L1

Bind R3 from candidates 1/2/3 (same official notice document, three URLs — pick whichever fetches cleanest; each is its own Registry row), then 4 or 5 as the standalone-document form if the heading rule fails on the notice HTML. Keep the downFiles trap URL out of the C3 fetch list. All findings are reported, not patched — claims are frozen.

Scratch: created `/fast/scratch/hyaku/chousa-r57/R57W1ScoutR3/` (key computation only); removed via `rm -rf` before yield; nothing else written outside the seat report.

VERDICT: R3 URL scout survived — 9 candidates ranked with snippet evidence (top: the three official nhc.gov.cn 16号-notice postings holding `2021年版` and the `附件：药品临床综合评价管理指南（2021年版 试行）` heading line), plus one falsified decoy: the journal-cited `cms-search/downFiles/863665…` URL actually serves the 2020 text and cannot bind R3.
