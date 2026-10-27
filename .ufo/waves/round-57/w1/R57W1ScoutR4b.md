# R57W1ScoutR4b — R4 (《抗肿瘤药品临床综合评价技术指南》2022年版 试行) third-angle scout: hospital/CDC mirrors, library guides, cnki-adjacent hosts

Seat: scout (leaf; search-only, **no fetches**). Claim served: R57-C3 binding of R4 (title `抗肿瘤药品临床综合评价技术指南`, token `2022年版`).
Method: 15 `web_search` queries (CDC/疾控中心, 医院/药学部, 图书馆/学科导航, site:edu.cn, doc88/book118/原创力, 万方/维普/医脉通/知网, sohu/163/sina/qq, trio-notice title, 关于印发/转发, cicams deep page, takara identity); reads of committed lane bytes (captures + refetch.tsv + round-56 note). No URL was fetched; rankings rest on snippets and lane bytes, so every candidate still needs a fetch. Tooling: no installs (none needed).

## 1. Orphan-copy origin cross-check (attack: "reposts likely" — CONFIRMED)

The two 2022-指南 orphans both carry office-converter producer strings, consistent with the seat brief's hypothesis:

- `corpus/captures/d473754a0cbf8d3095255d5a.raw` (抗肿瘤, 66 pp): `pdfinfo` → Author `CNHDRC`, Creator/Producer `Microsoft® Word 2016`, CreationDate 2022-06-28T04:04:13-03 (= 07:04 UTC, one day before the 2022-06-29 release). Interior (pdftotext lines 147–151) names `NCHTA@nhei.cn` and the official acquisition channels `http://www.nhei.cn` and `http://www.cicams.ac.cn/Html/News/Main/249.html`. Its only documented URL is a repost host: `https://www.hnysfww.com/data/article/1656481023744041713.pdf` (S128 ref [6]; R56GroundNote ref table; refetch.tsv S135 rows). S134's committed HTML identifies that host's identity: capture `9695437cac165bb4b6145deb.txt` line 8 `<title>…指南•规范•共识_药讯中心_湖南药事服务网</title>` (beian 430111 = Changsha, Hunan; ICP link hnicp.com). Verdict: the centre's own Word-2016 export, reposted unchanged by a Hunan pharmacist-service site.
- `corpus/captures/d8b4f8f8829b813f16227893.raw` (儿童, 68 pp): Author `Administrator`, Creator/Producer `Microsoft® Word 适用于 Microsoft 365`, created 2022-06-22. Documented URLs: `cpia.org.cn/uploads/20220630/…pdf` (S128 ref [5]) and `https://www.hnysfww.com/data/article/1656481067585283603.pdf` (refetch.tsv S136 rows). Same converter class → repost-likely.
- The third orphan, 公报 `53a92273a452a58f28368691.raw` (31 pp), is a different class: metadata scrubbed to placeholder strings (标题/科目/关键字/作者/创建者/生产者), untagged PDF 1.4 — no origin clue in metadata.

## 2. Trap findings (falsified decoys)

- **Official nhei 2022 PDF cover splits the title** — two independent engine renderings of `…/202206/…/files/4e062c199b17474ca680da5aac3b6d89.pdf` show cover lines `# 抗肿瘤药品临床综合评价` / `# 技术指南` / `## （2022 年版 试行）`, matching the held orphan's split cover. Under the frozen heading rule (a single line, ws-removed, one trailing （…） dropped, ending with the full title, prefix ≤16 chars free of 《》.[]［］) this layout CANNOT bind R4. Any byte-identical repost (hnysfww, cnki-adjacent hosts) fails the same way. [INFERENCE for un-fetched mirrors: same centre export.]
- **S134 (held hnysfww article) cannot bind R4 on committed bytes.** `9695437cac165bb4b6145deb.txt` line 189 is the antitumor anchor `☛/抗肿瘤药品临床综合评价技术指南（2022年版 试行）.pdf` — even after html_to_text the line ends `.pdf` after the parenthetical; and the committed `.txt` currently equals the raw HTML (refetch.tsv S134 row: raw_sha == txt_sha == 84df89a7…), so the heading test would run on markup lines containing `.`/`[`. Two independent failures; do not spend C3 effort here.
- **book118 item is the 2021年版**: `https://max.book118.com/html/2022/0510/8137011036004100.shtm` snippet cover = `（2021 年版）…二〇二一年十二月`. Wrong token; cannot bind R4. Same for `zk.cn-healthcare.com/doc-show-60003.html` (2021年版).
- **takara PDFs are junk-template, and engines mislabel them.** refetch.tsv already shows S135→`takarabiomed.com.cn/DownLoad/2540A.pdf` (200) and S136→`…/6170.pdf` (200) with **identical txt_sha 36a9e7f1…** across two different raws — a shared non-document template. The recurrent search-engine claim that `takarabiomed.com.cn/DownLoad/5261.pdf` is the guide (it kept appearing as "source [1]") is an engine mirage; ScoutR3 already rated it D.
- **Name-variant trap**: Sohu `https://www.sohu.com/a/562890724_121118853`, CACA `wap.cacakp.com/appnews/detail/id/17057`, and tiprpress `…/ywpjyj/article/pdf/20250732` all print the variant `抗肿瘤药物临床综合评价技术指南` (药物, not 药品). Not the R4 title.
- **wjw.ankang.gov.cn/Content-2212114.html is the wrong document** (2020 抗肿瘤药物临床应用管理办法 转发, per snippet) — falsified lead from an earlier query.

## 3. Ranked candidates (rank = frozen-rule fit × evidence strength; key = sha256(url)[:24])

| # | URL (key) | Angle | Snippet evidence (2022年版 token) | Heading-rule assessment |
|---|---|---|---|---|
| 1 | `http://www.nhei.cn/nhei/znfb/202206/c01d87a290664b01bf42a9dad769d69f.shtml` (b444fa93d8041a6264d71fc9) | official notice | page title + body `…《抗肿瘤药品临床综合评价技术指南（2022年版 试行）》…` ✓ | likely FAILS (title inside 《》 in body sentences; page heading ends `通知`) — fetch to commit the canonical notice bytes + read the official attachment href |
| 2 | `http://www.cicams.ac.cn/Html/News/Main/249.html` (5f35a2b5432c04d71415cae5) | 国家癌症中心/中国医学科学院肿瘤医院 mirror | named as official 指南获取 channel inside the guide's own committed bytes (orphan pdftotext line 151); no live snippet | UNKNOWN content — highest-upside fetch of this wave; a hospital-hosted HTML copy with a standalone title line would bind |
| 3 | `http://www.nhei.cn/nhei/znfb/202206/c01d87a290664b01bf42a9dad769d69f/files/4e062c199b17474ca680da5aac3b6d89.pdf` (a8cb9d9a7666a618b2c80c1c) | official PDF | cover `（2022 年版 试行）…二〇二二年六月` ✓ | FAILS (split cover, §2); fetch value = canonical digest, byte-identity with orphan d473754a would prove the orphan's provenance |
| 4 | `http://cnhdrc.cn/nhei/znfb/202206/c01d87a290664b01bf42a9dad769d69f/files/4e062c199b17474ca680da5aac3b6d89.pdf` (013ed74e9ccdf0384f920abd) | centre's alias domain mirror | cnhdrc.cn already mirrors nhei paths (2021 PDF + 专家解读 both resolve there) | same bytes as #3 → FAILS; only if the L1 wants a second independent URL for the same document |
| 5 | `http://docs.cn-healthcare.com/sharedoc/src_files/20220629/c3d41c4356d62b67607c0a02bd53ba5f.pdf` (6436e65f96510ddee17172c5) | cnki-adjacent free doc host (健康界 doc server) | engine-rendered cover `（2022 年版 试行）` ✓ | FAILS (same split cover); reliable free host if a drift comparison copy is wanted |
| 6 | `https://www.phirda.com/artilce_28170.html` (43c3f782ef30cbded05c861a) | 中国医药工业研究总院信息中心 repost | reposts the notice; snippet body ✓ `2022年6月29日…《抗肿瘤…（2022年版 试行）》` | likely FAILS (《》 body), attachment print style unverified |
| 7 | `http://cpia.org.cn/index/Xharticle/info.html?cate=17&id=477` (dc6b4b5d363a2011cac92cbd) | association mirror of the notice | ScoutR5 #4: `…《抗肿瘤…（2022年版 试行）》` ✓ | likely FAILS (《》 body); note cpia.net.cn/uploads/ already returned 503 ×2 this wave |
| 8 | `https://www.cn-healthcare.com/api/third/article/570821` (b3465801426707761b50007e) | 健康界 news repost | title `《抗肿瘤药品临床综合评价技术指南2022年版 试行》印发` ✓ | FAILS (heading line ends `印发`) |

Already-tried-this-wave (from refetch.tsv, do not re-queue without cause): hnysfww antitumor PDF (S135 ×2 timeout, rc 28), cpia.net.cn/uploads antitumor PDF (S135 ×2, 503), wanfangdata subject PDF (301), gsdpf DOCX (rc 35), nhei `…/d4c3a96d…pdf` (timeout).

## 4. Sweep negatives (angle coverage, for the UNBOUND sweep line)

- CDC mirrors: 0 confirmed hits for `疾控中心 OR cdc.cn OR 疾病预防控制中心` — the 国家癌症中心 (cicams) is the disease-institute mirror, not a CDC; no provincial CDC repost found.
- University library subject guides: 0 hits (`图书馆 学科导航/学科服务`, `site:edu.cn` relaxed) — no OPAC/subject-guide page surfaced.
- CNKI-adjacent free full text: no wanfang/vip/medlive/cnki item page for the 2022年版 confirmed; only the 2021年版 traps (§2) and the mislabeled takara PDFs.

## 5. Calibration notes for the L1 (reported, not patched)

- S135/S136 hnysfww attempt pairs are 78 s apart (08:37:14Z→08:38:32Z; 08:37:29Z→08:38:47Z) — under the 600 s spacing, so they cannot ground UNREACHABLE under the frozen predicate; the recipe's third attempt remains available.
- S134's committed `.txt` equals its raw HTML (recipe expects html_to_text for HTML raws) — flag for whoever owns S134's evidence; it is outside C2's frozen 47-set, so C2's CONSISTENT check does not cover it.

Scratch: `/fast/scratch/hyaku/chousa-r57/R57W1ScoutR4b/` used for key computation only; removed via `rm -rf` before yield. Nothing written outside the seat report. No tools installed.

VERDICT: R4 third-angle scout survived — 8 candidates ranked with snippet/token evidence (top actionable fetches: the official nhei notice page and the guide-named cicams.ac.cn/Html/News/Main/249.html hospital mirror); orphan-origin cross-check CONFIRMED both 2022-指南 orphans are office-converter exports reposted by provincial/association hosts (hnysfww 湖南药事服务网, cpia.org.cn); falsified traps: the official 2022 PDF's split-title cover and every byte-identical mirror cannot bind R4 under the frozen heading rule, the held S134 capture cannot bind on committed bytes, book118/zk items are the 2021年版, and takara PDFs are junk-template engine mirages.
