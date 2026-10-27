# R57W1ScoutR1 — R57-C3 reference R1 URL scouting (調査, web-search only)

Seat: R57W1ScoutR1 (scout, leaf). Item: locate source URLs for R1 = 国家卫生健康委《关于开展药品使用监测和临床综合评价工作的通知》（国卫药政函〔2019〕80号）; rank by likelihood of satisfying the frozen binding rule. **No fetches, no curl** — search snippets only. Nothing in this report changes any frozen predicate; findings are reported, not patched.

## Frozen rule being scouted against (read, not run)

- `corpus/evidence/round57/c3-count.py:75`: `("R1", "关于开展药品使用监测和临床综合评价工作的通知", "〔2019〕80号")`.
- `c3-count.py:150-159 heading_title`: some line of the defined text form, whitespace-removed and one trailing `（…）` dropped, **ends with the title** after a prefix ≤16 chars holding none of `《》.[]［］`; token must appear with whitespace removed (`nows`). Citation sentences and reference-list lines fail by construction.

## Ranked candidates (most → least likely to bind R1)

| # | URL | Host / kind | (a) title as ONE bare heading line | (b) token 〔2019〕80号 | key = sha256(url)[:24] |
|---|-----|-------------|---|---|---|
| 1 | `https://www.nhc.gov.cn/yaozs/c100097/201904/6bc8f273684845d3ab76fed841eb42d2.shtml` | nhc.gov.cn, HTML notice page (canonical, 药物政策与基本药物制度司, 发布时间 2019-04-09) | **Yes** — search snippet of the page head prints exactly `国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知` on its own line, then `国卫药政函〔2019〕80号`, then body `各省、自治区、…` (web_search result, source [1] of query `"国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知" "各省、自治区、直辖市及新疆生产建设兵团卫生健康委"`). nows → prefix `国家卫生健康委` = 7 chars, no banned chars → passes heading rule. | **Yes** — 文号 line `国卫药政函〔2019〕80号` present in snippet (same source). | `9d57f9cade3bdcbdf2fd6572` |
| 2 | `http://www.gcpunion.org/portal/article/index.html?id=2395` | gcpunion.org (临床试验机构联盟), HTML full-text repost | **Likely** — page indexed under the exact title; full text confirmed via snippet (addressees + all four sections + 落款 2019年4月3日). Non-gov mirror so heading layout unverified, but reposts of NHC notices typically print title as a bare H1 line. | **Yes** — search summary states page shows `文号：国卫药政函〔2019〕80号`. Host proven fetch-friendly today: gcpunion served S124's `.doc` with curl_rc=0/200 in refetch.tsv (row with key `bdff491a75c6abeda1d9c01d`). | `de34c41f76e5a5c0e1f4d1a2` |
| 3 | `https://wsjsw.linyi.gov.cn/info/1040/11703.htm` | wsjsw.linyi.gov.cn （临沂市卫健委）, HTML full-text repost | **Likely** — indexed under exact title (`国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知-临沂市…`); snippet body starts at `为贯彻落实党中央、…`, i.e. title sits above body as a heading. | **Unverified** — snippet starts at body text; the 文号 line is not shown. Gov-reposts of NHC 函 usually carry it, but not confirmed. | `68f75319532a1bb7de0f2c5b` |
| 4 | `https://web.archive.org/web/2019/https://www.nhc.gov.cn/yaozs/c100097/201904/6bc8f273684845d3ab76fed841eb42d2.shtml` (timestamped-snapshot form, e.g. `/web/20190410id_/…`) | web.archive.org, archived HTML of #1 | **Yes if snapshot exists** — same bytes as #1, so the heading line and 文号 line are present in the archived copy. | **Yes** (same bytes as #1). | `fd68e8e2ab8b9939fdfb505e` (for the `/web/2019/` form; changes with exact timestamp) |
| 5 | `https://wenku.baidu.com/view/cc158778f31dc281e53a580216fc700abb6852a4.html` (+ sibling `724ee8ff5cbfc77da26925c52cc58bd631869389`) | wenku.baidu.com, JS/paywall document viewer | **Unlikely in defined form** — full text is in snippet (so the text exists) but Baidu Wenku renders in JS/canvas; campaign `html_to_text` would likely yield a login/skeleton page, not the title line. | Text present server-side per snippet; reachability of a plain-text form doubtful. | `9cf904a79571bc8d2626d162` |
| 6 | `http://www.nhc.gov.cn/yaozs/pqt/201904/…` (old `pqt` channel; exact tail unpreserved — a china-pharmacy journal cites `http://www.nhc.gov.cn/yaozs/pqt/201904/` truncated) | nhc.gov.cn legacy channel for 药物政策 | Same content as #1 if it redirects; NHC migrated `pqt` → `c100097`. | Same as #1 if reachable. | not computable (URL incomplete) |

## Observed lane state (read-only; commands run)

```
$ awk -F'\t' '$1=="S131" || $1=="S132"' corpus/evidence/round57/refetch.tsv
S131  https://www.nhc.gov.cn/yaozs/c100097/201904/6bc8f273684845d3ab76fed841eb42d2.shtml  9d57f9cade3bdcbdf2fd6572  1  2026-10-27T08:31:03Z  22  412  -  -
S132  https://www.nhc.gov.cn/yaozs/c100097/202107/d2a45e6ae041423f950b3865e43f5ef6.shtml  2c2a982dd977da3737b6a2b5  1  2026-10-27T08:31:04Z  22  412  -  -
S131  https://web.archive.org/web/2024/https://www.nhc.gov.cn/…6bc8f273684845d3ab76fed841eb42d2.shtml  8146b1e3acfe7f08c9454262  1  2026-10-27T08:31:46Z  22  404  -  -
S132  https://web.archive.org/web/2024/https://www.nhc.gov.cn/…d2a45e6ae041423f950b3865e43f5ef6.shtml  676178c60248d95850d6efbf  1  2026-10-27T08:31:49Z  22  412  -  -
$ ls corpus/captures | grep ^9d57f9cade3bdcbdf2fd6572   → (no output; no capture for the R1 URL)
```

Facts: the L1 already mined candidate #1 as Registry row **S131** (new row, opened today) and attempted it once; NHC returned **HTTP 412** (bot gate) to the campaign curl; the `web.archive.org/web/2024/<url>` form returned **404/412**. No committed bytes exist for R1 yet. Same 412 hit S132 (R2's NHC page, row exists). Meanwhile NHC **PDF** URLs fetch fine today (S130, S133, S127 all curl_rc=0/200, refetch.tsv) — the block is specific to NHC HTML notice pages, so R1/R2 (HTML-only documents) need a mirror or a working archive URL to bind.

## Negative controls (located, checked, would NOT bind — calibration)

- `http://www.haiwen-law.com/35/317` — newsletter prints `国卫药政函[2019]80号` with **half-width** `[ ]` and the title only inside `《…》` in running sentences → token 〔2019〕80号 fails (nows), heading rule fails (prefix contains 《, line doesn't end with bare title).
- NHC 2021-notice pages (`…/202107/d2a45e6ae041423f950b3865e43f5ef6.shtml`, `…/wjw/c100175/202107/58a87de5349a484e9ef87b8ac0a32ce7.shtml`) and stats.gov.cn `t20250702_1960308.html` — quote R1's title only as `《关于开展…通知》（国卫药政函〔2019〕80号）的工作部署/制定…`; line does not end with the title → heading rule fails by design.
- `https://ylqxzb.com/ZBZcfg/Item84e33c7a673d0c38.html` — is Shanghai's **own** follow-up notice （标题不同）, not R1; excluded.

## Coordination notes for the L1 fetch (planner seat)

1. Candidate #1 satisfies the text-form rule on snippet evidence but is fetch-blocked (412); retry as-is will likely re-fail. Candidate #2 (gcpunion article page) is the strongest practical path: same full text, host proven 200-friendly today, title/token expected to satisfy the rule once bytes land. Candidate #3 needs one fetch to confirm the 文号 line.
2. The wayback attempt used a bare `/web/2024/` prefix and failed; a timestamped form (`/web/<ts>id_/<url>`) was not tried and is scout-unverifiable without a fetch.
3. Same 412 pattern will hit R2 (S132's URL) — its mirror hunt should start from provincial reposts of the 2021 notice (e.g. Hubei `wjw.hubei.gov.cn/zfxxgk/zc/gkwj/ywh/202106/t20210630_3622439.shtml` is a provincial *deployment* notice, not a full-text repost of R2 — do not count it).

Method note: 6 web searches (site:nhc.gov.cn; site:gov.cn; general; PDF; gazette/汇编; distinctive addressee phrase; reposts), no fetches, no edits outside this report. No tools installed/upgraded; no scratch dir created (nothing to delete). Frozen counters read only.
