# R57W1ScoutR5b — R5 second-angle scout: society hosts / NCCD / provincial centres / one-line HTML title

Seat: R57W1ScoutR5b (scout, leaf). Item: second angle on R5 (`c3-count.py` REFS: `("R5","心血管病药品临床综合评价技术指南","2022年版")`).
Method: `web_search` only — **zero fetches** (scout rule). Read-only inspection of committed lane bytes
(`corpus/captures/*.txt|raw`, `refetch.tsv`) to calibrate frozen-rule fit. Complements R57W1ScoutR5 (first angle).
Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ScoutR5b` used for two read-only rule-replication checks; deleted before
yield. No tools installed, no lane writes but this file. Frozen claims untouched.

## 1. Live-wave state observed in refetch.tsv (S135 row, R5)

8 attempts, none byte-backed valid (lines 103–125 of `corpus/evidence/round57/refetch.tsv`):
cpia.net.cn canonical PDF rc22/503 ×2; takarabiomed 2540A.pdf rc0/200 but capture
`ad3010d2aee49a95e0c7cb0b.raw` is a WAF JS challenge (`<html><script>var arg1=…`, sha e96cdea38ef2646c, .txt 1
byte) — and the search index shows 2540A is the **2021年版** cover anyway → double trap; hnysfww
`1656481023744041713.pdf` rc28 ×2; gsdpf `_546037_611133.DOCX` rc35 (search snippet now shows 404);
`www.nhei.cn/…/files/d4c3a96d751f44d4a78a8979ccf97cf6.pdf` rc28; wanfang subject URL rc92/301.
Note: search index shows `http://nhei.cn/…/files/d4c3a96d751f44d4a78a8979ccf97cf6.pdf` (issuer's own 2022
attachment, content-verified by indexed snippet on 有效性评估/RWS) — the L1 tried the **www** host variant, not
the bare host.

### Swap finding (from committed bytes, cross-seat relevant)
Hub capture `9695437cac165bb4b6145deb.txt` (hnysfww article.php?id=3275, S134 attempt, rc0/200) lines 186–192 map
the data PDFs: `…1656480976136156414.pdf` = **心血管病**; `…1656481023744041713.pdf` = 抗肿瘤; `…1656481067585283603.pdf` = 儿童.
refetch currently attempts 1656480976… under **S134** and 1656481023… under **S135** → for R5, S135's hnysfww
attempts target the 抗肿瘤 file; the R5 file was only attempted under the S134 label. Row labels are the L1's to
fix at registry-commit time; flagging, not patching.

## 2. Ranked candidates (ranked by frozen-rule fit; keys = sha256(url)[:24])

| # | URL (key) | axis | evidence | fit |
|---|---|---|---|---|
| 1 | `http://nhei.cn/nhei/znfb/202206/c01d87a290664b01bf42a9dad769d69f/files/d4c3a96d751f44d4a78a8979ccf97cf6.pdf` (4f5a4c1f65b6271a6968eb7c) | issuer attachment, bare host | search-index snippet: real 2022 text; www variant rc28'd | high if fetch lands; cover title may split across 2 lines under `pdftotext -layout` [INFERENCE — cpia cover renders as `心血管病药品临床综合评价` + `技术指南` in one snippet] |
| 2 | `https://cpipc.acge.org.cn/sysFile/downFile.do?fileId=c3fee2dcb9634ab38e386b51c544c981` (6b3823a0cea553aeb8d9ef41) | 中国医药工业信息中心 file endpoint | two R5-flavored searches surfaced this fileId | high if it serves the R5 PDF; mapping unverified |
| 3 | `https://cpipc.acge.org.cn/sysFile/downFile.do?fileId=3145cb0e7fa94edc87b8c19533e50a3a` (2d1499034bd9706cb8d94d66) | same host, other fileId | surfaced in first NCCD-axis search | same as #2 |
| 4 | `https://www.pha-bj.org/news/show/contentid/107928.html` (0abc8953621fb12c63b90aa0) | society host (北京药学会) | snippet: 2022 结题报道 cites full title with 《》 in-sentence | heading FAIL predicted (prefix holds 《》) — corroboration only |
| 5 | `https://www.dxye.com/thread-36798-1-1.html` (22af91c425a53ab42ed6b32a) | dxy forum thread | engines blocked ("Learn why"); may carry attachment links | low; possible HTML/attachment lead |
| 6 | `https://www.gsdpf.org.cn/ArTicle/details/455416.pptx` | provincial-adjacent host | search snippet live | **rule-level unusable**: pptx zip → `tools/capture-text.py` refuses `.pptx` → `form_of` None → cannot bind |
| — | `http://www.nhei.cn/nhei/znfb/202206/c01d87a290664b01bf42a9dad769d69f.shtml` and hnysfww hub | HTML announcements with one-line title | both fetched/landed (S137 phirda rc0/200; hub rc0/200) | heading FAIL — executed checks §3 |

## 3. Attack: HTML-announcement axis fails the frozen heading rule (executed on committed bytes)

Replicated `heading_title` from `c3-count.py:118-127` in scratch against the two landed HTML captures:
- phirda `d2a1cf3d2c385daee67c4afd.txt` (S137, 200, token `2022年版` present): only title-terminated line is
  163 `1.心血管病药品临床综合评价技术指南（2022年版 试行）` → after one paren-drop, prefix `1.` contains `.` ∈
  BAD_PREFIX → **FAIL**. Attachment-list lines `2.…`/`3.…` fail identically (same for R4/R6 scouts).
- hnysfww hub `9695437cac165bb4b6145deb.txt` (token present): title lines are (a) the notice sentence with 《》
  prefixes, (b) the download link whose defined-form line ends with `.pdf`/`</a>` → **FAIL**.
Survives as a calibrated negative: "any HTML announcement printing the full title on one line" must print it
*without* a `N.` list marker, 《》, or a trailing filename to bind — none of the four announcement surfaces found
(phirda, hnysfww, pha-bj predicted, nhei notice body predicted) satisfies it.

## 4. Negative axes (searched, zero bindable surfaces)

- 中国医师协会心血管内科医师分会 / CMDA domains: no surface; no evidence the branch hosts or mirrors R5.
- 中华医学会心血管病学分会 `csc.cma.org.cn`: `site:` search 0 hits; col619 listing carries other guidelines only.
- 国家心血管病中心 (`nccd.org.cn` / 阜外): 0 hits; centre is a drafting org — the 2021版 PDF's own 指南获取 text
  names nhei.cn + NCCD, but no NCCD URL is indexed. Distribution runs through the centre's nhei.cn.
- Provincial drug-evaluation centres / `site:gov.cn`: 0 hits (zhihu answer says provinces 转发 implementation, but
  nothing indexed); only provincial-adjacent repost is the commercial hnysfww hub.
- medlive/yiigle: no hits for this title.

## 5. Traps re-confirmed

- takarabiomed `DownLoad/2540A.pdf` = 2021年版 cover per index (and landed bytes = WAF JS junk, §1).
- nhei `202112/9e350a54…/0ac56e4c…pdf` = 2021年版 (cover `二〇二一年十二月`) — same as first scout flagged.
- gsdpf `_546037_611133.DOCX`: now 404; its wave attempt rc35.

## 6. Commands / queries (evidence)

- `awk -F'\t' '$1=="S135"…' corpus/evidence/round57/refetch.tsv` → 8 attempts, §1.
- `head -c 600 corpus/captures/ad3010d2aee49a95e0c7cb0b.raw` → WAF JS; `od -c` of `.txt` → 1 byte.
- scratch python: `heading_title` replication over `d2a1cf3d2c385daee67c4afd.txt` (1 FAIL line) and
  `9695437cac165bb4b6145deb.txt` (2 FAIL lines); token checks True/True.
- `sed -n '176,200p' corpus/captures/9695437cac165bb4b6145deb.txt` → attachment↔PDF mapping (swap, §1).
- key computation via `hashlib.sha256(url.encode()).hexdigest()[:24]` for all §2 URLs.
- web_search queries (11): R5 title with `site:cma.org.cn OR cmda…`; `site:nccd…`; title + 评价中心/评估中心;
  title + 通知/印发/发布 html; title + site:gov.cn; title `filetype:pdf`; `site:csc.cma.org.cn`; 医师协会心血管内科医师分会…;
  `site:medlive.cn OR 药学会…`; title minus known hosts; 中心 + 转发/培训.

VERDICT: attacked R5's second-angle axes (society hosts, 国家心血管病中心, provincial centres, one-line HTML
announcements) — 3 fresh fetch candidates delivered (bare-host nhei attachment #1; cpipc fileIds #2/#3) with store
keys, the hnysfww PDF-to-row swap flagged from committed bytes, and the HTML-announcement axis falsified against
the frozen heading rule by executed checks on two landed captures; society/NCCD/provincial/medlive axes negative —
survives as a calibrated scouting deliverable; binding awaits L1 fetches.
