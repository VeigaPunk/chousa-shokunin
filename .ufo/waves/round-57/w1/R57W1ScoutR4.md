# R57W1ScoutR4 — R4 alternate-URL sweep (《抗肿瘤药品临床综合评价技术指南》（2022年版 试行）)

Scope: scout only. Zero external fetches by this seat (all searches via the session search tool; all byte reads on
committed lane captures). Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ScoutR4/` used only for a scratch copy of
`d473754a…raw` + local `pdftotext` (deleted before yield; no installs needed — all tools present).

## Frozen rule this item ranks against (c3-count.py:64-90,146-157)

A capture binds R4 iff its defined text form holds token `2022年版` (whitespace removed) AND some line passes
`heading_title`: nows(line) minus ONE trailing `（…）`/`(…)` ends with `抗肿瘤药品临床综合评价技术指南`, with prefix
≤16 chars containing none of `《》.[]［］`. So `《抗肿瘤…（…）》` fails (residual `》`), `[EB/OL]`-tail lines fail
(not a paren), and `2.` / `1.` list markers fail (ASCII `.` ∈ BAD_PREFIX).

## Premise verified — the lane-held copy cannot bind

- `corpus/captures/d473754a0cbf8d3095255d5a.raw` (= sha256(`https://www.hnysfww.com/data/article/1656481023744041713.pdf`)[:24]),
  the URL S128's ref [6] cites ([2023-07-10], `de9f5afc3809acbf61f4d5bb.txt:213-216`), landed 06:23Z, PDF 1.5, 66 pp.
- My scratch `pdftotext -layout` prints the cover `抗肿瘤药品临床综合评价` + `技术指南` + `（2022 年版 试行）` on three
  separate lines — no line passes `heading_title`. Premise confirmed: this copy cannot bind R4.

## Candidate ranking by frozen-rule fit (6+ URLs)

| # | URL | kind | fit |
|---|---|---|---|
| 1 | https://www.medsci.cn/guideline/show_article.do?id=b4b601c0026a2922 | HTML guideline page | **Best.** MedSci convention: plain H1 = guideline name without 《》; MedSci search index (medsci.cn/search?q=…) literally lists `抗肿瘤药品临床综合评价技术指南，77页. 肿瘤药品- 2022-09-03`. If html_to_text emits the H1 as one line → binds; `2022年版` appears in page metadata → token ok. Not yet in refetch.tsv as of 08:48Z. |
| 2 | http://www.nhei.cn/nhei/znfb/202206/c01d87a290664b01bf42a9dad769d69f/files/4e062c199b17474ca680da5aac3b6d89.pdf | PDF, issuing centre's own host (国家卫生健康委卫生发展研究中心) | Strongest provenance (nhei.cn = same domain S128's ref [7] uses for R7). L1 attempts a1/a2 both rc=28 (slow host; retried 08:39-08:40Z). Layout risk HIGH: search snippet of this PDF shows `抗肿瘤药品临床综合评价` / `技术指南` split (same master as the held copy). Fetch confirms; likely same heading-rule failure — still worth the authoritative provenance. |
| 3 | http://www.nhei.cn/nhei/znfb/202206/c01d87a290664b01bf42a9dad769d69f.shtml | HTML official release notice | Same notice text family as phirda (see #4): expects the `2.抗肿瘤…（2022年版 试行）` numbered-list line → near-miss on ASCII `.`. Not yet fetched. |
| 4 | https://www.phirda.com/artilce_28170.html?cId=2 | HTML notice (中国医药创新促进会) | **Already fetched** (S137 a1 0/200, capture `d2a1cf3d2c385daee67c4afd`). Attachment list in `.txt:167` = ` 2.抗肿瘤药品临床综合评价技术指南（2022 年版 试行）` — fails `heading_title` by one char: prefix `2.` contains `.` ∈ BAD_PREFIX. Near-miss, reported not patchable. |
| 5 | https://www.dlc-projects.com/uploads/20220630/e1e977be16fba47c9678b119e234fd99.pdf | PDF mirror | Search title `抗肿瘤药品临床综合评价 技术指南` (space = split line) → same master, likely fails heading rule. The `/uploads/20220630/<32hex>.pdf` path matches cpia's own naming (ref [5] R6 = cpia.org.cn/uploads/20220630/…) → derived candidates to try: `http://cpia.org.cn/uploads/20220630/e1e977be16fba47c9678b119e234fd99.pdf` and `http://cpia.net.cn/uploads/20220630/e1e977be16fba47c9678b119e234fd99.pdf` [INFERENCE — never confirmed served]. |
| 6 | https://www.exapt.cn/uploads/tmp/97d4701c05a4e04ec13ecd8cde5006d6.pdf | PDF, exam-site upload | Found via exapt.cn pdfjs viewer (`websrcexam`). Layout unknown; cheap GET. |
| 7 | http://www.cicams.ac.cn/Html/News/Main/249.html | HTML, co-issuer page (国家癌症中心) | The 2021 edition's colophon names `nhei.cn` + `cicams.ac.cn` as official 获取 channels; this is the co-issuer's release page. Edition/format unconfirmed. |
| 8 | https://www.scribd.com/document/739900174/抗肿瘤药品临床综合评价技术指南 | HTML (JS-heavy) | Scribd doc page exists. Low fit: curl gets viewer HTML; title may surface in html_to_text but `2022年版` token presence unverified. Last resort. |

## Negative / already-failed results (do not re-try)

- takarabiomed.com.cn `DownLoad/2540A.pdf` and `DownLoad/6170.pdf`: both rc=0/200 but body = 4,321-byte ASCII junk
  HTML shell (no newlines; `ad3010d2aee49a95e0c7cb0b.txt` = 1 byte) — endpoint does not serve the PDF to curl.
  Likewise `DownLoad/5261.pdf` from a search snippet — same endpoint family, same expected failure.
- cpia.net.cn R5 file `…/59831d29ddfe35745066ea54956a9b0f.pdf`: a1+a2 both 503 (service dead).
- gsdpf.org.cn `…_546037_611133.DOCX`: a1 rc=35 (SSL error) — unreachable.
- subject.med.wanfangdata.com.cn `…/753dbddb…pdf`: a1 rc=92 after a 301 — dead.
- hnysfww `article.php?id=3275` notice (S134, fetched `9695437cac165bb4b6145deb`): title embedded mid-sentence inside
  《…（2022年版 试行）》《…》 at `.txt:180-182`, download anchors render as `☛/抗肿瘤…（2022年版 试行）.pdf`
  (`.txt:189` raw shows span-split anchor) → trailing `.pdf` defeats the paren-drop. Fails. Both sibling
  data-article PDFs (`1656480976136156414`, `1656481067585283603`) timed out a1+a2 (rc=28) — but those are R5/R6 ids.
- Wrong editions: nhei 2021年版 PDF `…/202112/9e350a54d2ea4c3ab9a0237ee4eab9f0/files/f5ef45cc87c14e7d8d04f2e9e7b8441d.pdf`
  and max.book118 `…/2022/0510/8137011036004100.shtm` — token `2021年版` ≠ `2022年版`, cannot bind R4.
- Provincial pharmacist-network mirrors (浙江/江苏/广东/山东): sweep returned none confirmed; hnysfww is the only
  known provincial host.
- Repost notices (sohu `a/562890724_121118853`, cn-healthcare `api/third/article/570821`, dxy h5 clinicalGuidelines/72222
  JS-app): title wrapped in 《》 or rendered by JS → cannot produce a qualifying line.

## Wave-state note (for the L1/planner)

As of 08:48Z `refetch.tsv` holds 19 C3-candidate rows (S134–S137) — the L1 is fetching in parallel with this sweep;
nhei.cn PDF attempts are timing out at 60 s (rc=28, http 000); consider a 3rd attempt or `web.archive.org/web/2024/`
snapshot of the same nhei URL. Captures already in the store from this wave that I inspected: `d473754a…` (R4 split
cover — premise), `9695437cac…` (hnysfww notice — fails), `d2a1cf3d…` (phirda notice — near-miss on `2.`),
`ad3010d2…`/`0cebd3c8…` (takarabiomed junk).

VERDICT: R4 alternate-URL sweep survives as a build item — ranked 8 candidates (MedSci HTML page best frozen-rule fit;
nhei.cn PDF best provenance; phirda near-miss `2.` documented; takarabiomed/cpia.net.cn/gsdpf/wanfang-subject dead;
2021-edition and repost-copy dead ends enumerated); the lane-held hnysfww copy's split cover cannot bind, verified.
