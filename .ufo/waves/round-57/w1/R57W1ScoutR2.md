# R57W1ScoutR2 — R2 (国卫办药政发〔2021〕16号) standalone source URLs

Seat: scout (URL location only; no fetches). Target: R2 = 关于规范开展药品临床综合评价工作的通知
(R2 row of `corpus/evidence/round57/c3-count.py:76`, token 〔2021〕16号) as a STANDALONE document —
not the lane-held 公报 compilation PDF (two-column title split, cannot bind under the frozen heading rule).

Frozen rule applied (c3-count.py:151-159 `heading_title` + :228 token check): some `.txt` line,
whitespace removed, one trailing （…）/(…) dropped, must END with the title after a prefix of ≤16 chars
containing none of 《》.[]［］; token 〔2021〕16号 must occur in the whitespace-stripped text form.
〔202〕 are NOT in the forbidden prefix set (only 《》.[]［］ are), so 文号-prefixed lines are legal
if short enough.

## Ranked candidates (best frozen-rule fit first)

key = sha256(url)[:24] (capture-store key, computed here for the L1).

1. `https://www.nhc.gov.cn/yaozs/c100097/202107/d2a45e6ae041423f950b3865e43f5ef6.shtml`
   key 2c2a982dd977da3737b6a2b5. Canonical 药政司 copy. Search snippet shows body line
   "国卫办药政发〔2021〕16号" and the notice text; page `<h1>` on the NHC template is the bare
   full title → prefix 国家卫生健康委办公厅 (10 chars, clean) = clean FIT. ALREADY IN FLIGHT:
   refetch.tsv:81 (attempt 1) and :99 (wayback twin) — both curl_rc=22 http_code=412.
2. `https://www.nhc.gov.cn/wjw/c100175/202107/58a87de5349a484e9ef87b8ac0a32ce7.shtml`
   key 8266eefc0e859892757769a6. Same document, NHC 主站 (wjw/c100175) copy; identical body
   snippet with 文号. Same template → same heading FIT. Same host → same 412 risk.
3. `https://www.nhc.gov.cn/yaozs/s2908/202107/532e20800a47415d84adf3797b0f4869.shtml`
   key 899edcc0631124c0957bb2a3. Original yaozs/s2908 URL cited as the official source in ≥3
   published reference lists (Frontiers Pharmacol 2022 fphar-2022-869319; 中国药房
   91242139; wap.china-pharmacy.com 20220525 PDF; Europe PMC MED/37197536). May 301-redirect
   to #1 or be dead — unverifiable without a fetch.
4. `https://wsjkw.hebei.gov.cn/zcfg2/380991.jhtml` key b94ae2164b62fb824b5d49e2.
   Hebei 卫健委 standalone full-text repost incl. 落款 "国家卫生健康委办公厅 2021年7月21日"
   and the 附件 line (snippet observed). Cited as [EB/OL] in ≥4 journal reference lists
   (chinjmap 20240544 et al.). Search-engine page title = full official title → heading line
   expected to FIT [INFERENCE: heading line itself unobserved, no fetch permitted]. gov.cn host,
   likely no WAF block.
5. `https://web.archive.org/web/2021/https://www.nhc.gov.cn/yaozs/c100097/202107/d2a45e6ae041423f950b3865e43f5ef6.shtml`
   key cdcf171337acb74bdb0c0943. Wayback snapshot of candidate 1 (frozen HTML bytes → same
   heading FIT). NOTE: refetch.tsv:99 shows web.archive.org also answered 412 from this host
   at 08:31:49Z under the frozen recipe — currently blocked, reported not patched.
6. `https://www.pharnexcloud.com/data/zcfg_546372fed05fbed1fa6fb3600f264192.html`
   key d83545d9abc2faa002876d23. 摩熵医药 policy mirror. Observed page title starts
   "国卫办药政发〔2021〕16号国家卫生健康委办公厅关于规范开展药品临床综合评价工作的通知".
   If 文号+title render as ONE line the prefix is 25 chars > 16 → heading FAIL; as separate
   lines (typical) the title line FITs. CONDITIONAL — verify after fetch.
7. `https://doc.docsou.com/bdf846b6db364558e3ad13c59b333b30705f22ef5.html`
   key b0d1c2f980df7c73ea751432. docsou mirror; page title observed as the bare full official
   title → expected FIT [INFERENCE: line structure unobserved]. Commercial host, low block risk.
8. `https://www.regulet.com/index/regulation/detail.html?id=702` key 5361b37e9eeb290d600735bd.
   注册圈 (杭州几度数据) regulation-detail mirror matched to this 文号. Heading unobserved;
   CONDITIONAL.

## Rejected false positive (recorded)

- `https://rsj.sh.gov.cn/tzpgg_17408/20220512/t0035_1407003.html` — first-pass snippet
  appeared to quote the full notice text under this URL; direct verification search shows the
  page is a 2022 上海市质子重离子医院 recruitment announcement. The notice quote was a
  misattributed snippet. EXCLUDED.

## Collision / set-membership checks (commands run)

- `grep` of SOURCES.md, corpus/knowledge/*.md, all evidence rounds' spans.tsv for all 8
  candidate URL strings: no hits → no registry/spans collision; none of S127/S128/S129's
  URLs (ttbz.org.cn PDF ×2, journal.china-pharmacy.com PDF — SOURCES.md:137-139) equals any
  candidate URL.
- key for candidate 1 recomputed here (2c2a982dd977da3737b6a2b5) matches refetch.tsv:81 col 3,
  confirming the in-flight S132 row IS this URL.

## Findings against frozen items (reported, not patched)

- Fetch risk under the frozen recipe (one curl GET, max 3 attempts, ≥600s apart): nhc.gov.cn
  AND web.archive.org both returned HTTP 412 to the recipe's curl at 08:31Z (refetch.tsv:81,99).
  Candidates 1/2/3/5 may stay unreachable from this host; the practical byte-backed path to an
  R2 binding is candidate 4 (Hebei gov.cn) and/or 6-8 (commercial mirrors), accepting the
  provenance trade-off (B/C-tier vs official). Heading lines for 4/6/7/8 are inferred from
  search snippets, not observed — the L1's post-fetch `.txt` is the first ground truth.

## Residual unknowns

- Whether NHC 412 is UA-based WAF (recipe cannot change) — retries per recipe may keep failing.
- Whether s2908 URL (candidate 3) still serves or redirects.
- Exact heading-line structure of candidates 4/6/7/8 (no fetches permitted for scouts).

No tools installed; no lane/fleet/fleet-root writes; scratch /fast/scratch/hyaku/chousa-r57/R57W1ScoutR2
(empty but for this report's temp files) removed on exit.

VERDICT: attacked "locate standalone R2 (国卫办药政发〔2021〕16号) URLs" — SURVIVED: 8 candidates
located and ranked by frozen heading-rule fit (3 official nhc.gov.cn, 1 wayback, 1 Hebei gov.cn
repost, 3 commercial mirrors), 1 false-positive candidate caught and rejected, 412-block finding
on nhc.gov.cn + web.archive.org reported against the frozen recipe.
