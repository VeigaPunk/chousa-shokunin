# R57W1ScoutR5 — R5 source-URL scout: 《心血管病药品临床综合评价技术指南（2022年版 试行）》

Seat: R57W1ScoutR5 (scout, leaf). Item: locate source URLs for R5 (c3-count.py REFS row 79:
`("R5", "心血管病药品临床综合评价技术指南", "2022年版")`). Method: web_search only — **zero fetches**
(seat rule; egress-approval.md row 4 permits only read-only re-open of a refetch.tsv URL, and none of these are in
refetch.tsv — verified below). No scratch dir used (no fixture, nothing >50 MB); no tools installed; no lane writes
but this file. Frozen claims untouched; findings reported, not patched.

## 1. Canonical URL already attested in committed lane bytes (rank 1)

`http://cpia.net.cn/uploads/20220630/59831d29ddfe35745066ea54956a9b0f.pdf` (中国医药创新促进会/CPIA host)

- Cited verbatim in `corpus/captures/b27ffd2f0161104c6a28c9f5.txt:1364-1366` (ref [33], S129 编制说明 bibliography):
  `…临床综合评价技术指南（2022 年版 试行）[EB/OL].[2023-07-10].http://cpia.net.cn/uploads/20220630/59831d29ddfe35745066ea54956a9b0f.pdf`
- Cited verbatim in `corpus/captures/de9f5afc3809acbf61f4d5bb.txt:204-206` (ref [4], S128 draft bibliography; same URL).
- `.ufo/waves/round-56/w1/R56GroundNote.md:46` records the host (`cpia.net.cn/uploads/20220630/…pdf`) and `:64`
  reports as a source defect that the centre's instrument is served from a non-centre domain — so this URL is the
  authoritative citation yet its liveness is unproven. L1 fetch decides; http (not https) and a domain that may have
  lapsed are the risks.
- Web-snippet evidence of content: query `"心血管病药品临床综合评价技术指南" filetype:pdf` returned this URL with
  cover text `技术指南 （2022 年版 试行）… 国家药物和卫生技术综合评估中心… 二〇二二年六月` — **token 2022年版 present**.
  Heading-fit [INFERENCE from snippet]: cover line is the bare title + edition parenthetical → after dropping one
  trailing （…） it ends with the title, prefix 0 chars, no 《》 — matches the frozen heading rule if the fetch lands.

## 2. Ranked candidates (10)

Evidence = one line quoted from the search snippet I observed; token column = literal `2022年版` in that line.

| # | URL | Host / owner | one-line-title evidence (snippet) | token | note |
|---|---|---|---|---|---|
| 1 | http://cpia.net.cn/uploads/20220630/59831d29ddfe35745066ea54956a9b0f.pdf | cpia.net.cn — 中国医药创新促进会 | `心血管病药品临床综合评价 技术指南 （2022 年版 试行） … 二〇二二年六月` | ✓ | canonical; cited by S128 ref[4]/S129 ref[33] (§1) |
| 2 | http://www.nhei.cn/nhei/znfb/202206/c01d87a290664b01bf42a9dad769d69f.shtml | nhei.cn — 国家卫生健康委卫生发展研究中心 (issuer) | `附件：1. 心血管病药品临床综合评价技术 …` + notice body `《心血管病药品临床综合评价技术指南（2022年版 试行）》` | ✓ | official release notice 2022-06-29; gateway to the PDF attachment (siblings `files/4e062c199b17474ca680da5aac3b6d89.pdf`=抗肿瘤, `files/60c39855fa6048e6aae17323b1fbd546.pdf`=儿童, both covers `（2022 年版 试行）` confirmed by snippets; the 心血管病 attachment hash is NOT indexed — fetch the notice page to read it) |
| 3 | https://www.hnysfww.com/article.php?id=3275 | hnysfww.com — 湖南药事服务网 | `下载：☛/心血管病药品临床综合评价技术指南（2022年版试行）.pdf` | ✓ | hub dated 2022-06-29, 来源:国家卫生健康委卫生发展研究中心; same host family as R4's bibliography PDF (S127 ref[6] `hnysfww.com/data/article/…pdf`) → direct PDF sibling sits behind this link |
| 4 | http://cpia.org.cn/index/Xharticle/info.html?cate=17&id=477 | cpia.org.cn — CPIA official notice mirror | `…会同有关单位制定了《心血管病药品临床综合评价技术指南（2022年版 试行）》《抗肿瘤…` | ✓ | association's own mirror of the release notice (cpia.org.cn hosts R6's canonical PDF per S129 ref[5]) |
| 5 | https://www.phirda.com/artilce_28170.html | phirda.com — 中国医药工业研究总院/信息中心 | `关于发布心血管病、抗肿瘤、儿童药品临床综合评价技术指南的通知 … 通知落款为2022年6月29日` | ✓ | repost carrying the three attachments |
| 6 | http://www.nhei.cn/nhei/zjjd/202206/4c1721e1dfe24972ad9676336bc2f8f4.shtml | nhei.cn — issuer's site | page title `《心血管病药品临床综合评价技术指南（2022年版 试行）》专家解读` (2022-06-29, 林阳/北京安贞医院) | ✓ | official 专家解读; heading ends with 专家解读 → fails the document heading rule [INFERENCE]; corroboration + links the notice |
| 7 | https://www.cn-healthcare.com/article/20220629/content-570820.html | cn-healthcare.com — 健康界 | `《心血管病药品临床综合评价技术指南（2022年版 试行）》印发` (2022-06-29) | ✓ | news item, not the document |
| 8 | https://max.book118.com/html/2022/0630/6003202051004204.shtm | book118 原创力文档 | page title `心血管病药品临床综合评价技术指南2022年版试行.pdf` + ToC text (`目 录 前言 第一章 评价维度与内容…`), uploaded 2022-06-30 | ✓ | doc-share HTML page (page images); fetch returns HTML text form |
| 9 | https://www.docin.com/p-3461355473.html | docin.com — 豆丁网 | `心血管病药品临床综合评价技术指南2022年版试行.pdf 12阅读 文档大小：1.1M 67页 … 上传于2022-06-30` | ✓ | doc-share HTML page |
| 10 | http://nhei.cn/nhei/znfb/zppg_lmlist.shtml | nhei.cn — issuer's site | `国家药物和卫生技术综合评估中心关于发布心血管病、抗肿瘤、儿童药品临床综合评价技术指南的通知 2022-06-29` | ✓ (entry page) | 指南发布 listing — navigation aid to #2, not a document |

Recommended L1 fetch order: 1 (canonical) → 2 (issuer's notice; recovers the true attachment URL) → 3 (dated hub with
PDF link) → 4/5 (mirrors) → 8/9 only if all else fails (doc-share HTML forms). 6, 7, 10 corroborate but are not
documents.

## 3. Version trap — DO NOT FETCH for R5

- `http://www.nhei.cn/nhei/znfb/202112/9e350a54d2ea4c3ab9a0237ee4eab9f0/files/0ac56e4cd1e848da859d623212dd0171.pdf` —
  this is the **2021年版** (cover `（2021 年版）… 二〇二一年十二月`, per observed snippet `技术指南 （2021 年版） … 二〇二一年十二月`);
  token 2022年版 absent. One search answer mislabeled it "指南全文 PDF…使用前请核对版本" — engine confusion; the
  cover/token check is the arbiter.
- `https://max.book118.com/html/2022/0113/8014027076004055.shtm` — same trap (2021年版 doc page).
- Sibling notice for the 2021 consultation: `…/202112/9e350a54d2ea4c3ab9a0237ee4eab9f0.shtml` — not R5.

## 4. Assigned-axis negative findings (reported)

- nhc.gov.cn: `"…" site:nhc.gov.cn` → no R5 surface (constraint relaxed, zero hits). nhc.gov.cn hosts only R3's
  管理指南 PDF (`nhc.gov.cn/cms-search/downFiles/863665c55fd74f29a656990d1a4ea5ce.pdf`) — consistent with S127's
  bibliography not citing nhc for ref [4].
- Provincial wjw (`wjw.*.gov.cn`): no repost found (relaxed search over 21 sources, none a provincial commission).
  The instrument's channel is the centre's own site (nhei.cn), not commission/provincial pages.
- 中国心血管健康联盟 / csc.cma.org.cn (中华医学会心血管病学分会): no mirror found.
- University mirrors: none; only participation news `chuangxin.dlut.edu.cn/info/1017/9818.htm` (大连理工, not a mirror).

## 5. Commands / queries run (evidence)

- `grep -n -i "心血管病药品临床综合评价\|心血管病" corpus/evidence/round57/c3-count.py` → R5 row at line 79.
- `grep -n -i "心血管病药品临床综合评价技术指南" corpus/captures` → hits b27ffd2f0161104c6a28c9f5.txt:186,1364-1366
  and de9f5afc3809acbf61f4d5bb.txt:204-211 (URLs in §1-2).
- `grep cpia|nhei|hnysfww|心血管病 corpus/evidence/round57/refetch.tsv` → **no matches**: every R5 URL above is a
  new open for the L1, covered by egress-approval.md row 2 (public document a registered source cites by name).
- web_search queries (8): `"心血管病药品临床综合评价技术指南" "2022年版" pdf`; same `site:nhc.gov.cn`;
  `"…" filetype:pdf`; `… site:nhei.cn`; `… site:hnysfww.com`; `中国心血管健康联盟 …`; `… 卫生健康委 转发 下载 wjw`;
  `… site:edu.cn`; `"c01d87a290664b01bf42a9dad769d69f" 心血管病 pdf`; `… site:gov.cn`;
  `hnysfww.com … 下载`; `nhei.cn 9e350a54d2ea4c3ab9a0237ee4eab9f0 …` — snippets quoted above are from their outputs.

VERDICT: scouted R5 source URLs for R57-C3 — 10 ranked candidates delivered (canonical cpia.net.cn PDF attested in
two committed lane captures; issuer's nhei.cn notice + attachment family; 8 further mirrors/corroborations), 2021年版
version trap flagged, nhc.gov.cn/provincial-wjw/CCHA/university axes negative — survives as a scouting deliverable;
binding awaits L1 fetches.
