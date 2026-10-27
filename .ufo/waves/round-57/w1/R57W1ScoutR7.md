# R57W1ScoutR7 — R7 (《药品临床综合评价质量控制指南（2024年版 试行）》) alternate source URLs

Seat: R57W1ScoutR7 (scout, leaf). Item: locate alternate source URLs for R7 besides held S118 (bjhea.org.cn PDF); resilience + corroboration; 4+ candidates; no fetches. Method: `web_search` only — zero curl/wget, per scout seat rule. Lane files read: `corpus/evidence/round57/claims.md`, `corpus/evidence/round57/c3-count.py:60-84` (REFS/EXCLUDED_URLS), `corpus/knowledge/quality-control-guideline-issued-text-r48.md:4` (S118/S119 sources), `corpus/evidence/round57/refetch.tsv` (S118/S119 attempts). Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ScoutR7` created for the key computation below and deleted on exit; nothing else written.

## Held baseline (facts)

- S118 = `https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf` — the issued 试行 PDF (北京市卫生经济学会 mirror). refetch.tsv rows: attempts 1-2, both curl_rc=0 http=200, sha256 `7b600fe3ee9bda2b…` (reproduced).
- S119 = `http://m.bjhea.org.cn/35/202501/1126.html` — 北京市卫生经济学会's 2025-01-03 posting of the centre's release notice; its HTML links the S118 PDF. Attempts 1-2, http=200.
- R7 in `c3-count.py` REFS = `("R7", "药品临床综合评价质量控制指南", "2024年版")`. A binding row's defined text form must hold token `2024年版` and the title as a HEADING (line, nows, one trailing `（…）` dropped, ends with the title, prefix ≤16 chars, no `《》.[]［］` in prefix). EXCLUDED_URLS holds only S127/S128/S129 URLs — no nhei.cn/cnhdrc.cn URL is excluded.

## Ranked candidates (best frozen-rule fit first)

1. `http://www.nhei.cn/nhei/znfb/202412/d33db3fcddf94daeabe49cfa95fa24f9/files/424b0df546fd45f3ad8c4fc747b2f5d8.pdf` — key `33329b6b7c4a0cbbcdb3f0f0`. The issuer's own host (nhei.cn = 国家卫生健康委卫生发展研究中心) official PDF of the issued 试行版; search snippets show cover `药品临床综合评价质量控制指南 （2024 年版试行） 国家药物和卫生技术综合评估中心 … 二〇二四年十二月`. Heading rule fits by construction (drop trailing `（2024年版试行）` → line ends with bare title; empty prefix); token `2024年版` present. Max resilience: different host from held bjhea. Observed in ≥6 independent search result sets.
2. Scheme/host variants of #1 — keys `da981365cce1410fa4fc8a9b` (`https://www.nhei.cn/…pdf`), and the notice page `http://nhei.cn/nhei/znfb/202412/d33db3fcddf94daeabe49cfa95fa24f9.shtml` / `https://www.nhei.cn/…shtml` — keys `45ff00394e7a6588ec6381ab`, `d28ef47e1437d3afd2fee4d3`. The .shtml notice is the 2024-12-31 发布通知 (《关于发布〈药品临床综合评价质量控制指南（2024年版 试行）》的通知); its body carries the token + full title and links the attachment PDF. Heading-rule fit unverified (page `<title>` is `关于发布《…》的通知_国家卫生健康委卫生发展研究中心` — likely fails the line-ending rule; the bare-title heading may exist only if the attachment caption renders as its own line). Fetch the PDF variants first.
3. `https://www.cnhdrc.cn/nhei/znfb/202412/d33db3fcddf94daeabe49cfa95fa24f9/files/424b0df546fd45f3ad8c4fc747b2f5d8.pdf` — key `165b00421a9f99fe2045d113`. cnhdrc.cn is the centre's alternate domain and mirrors the `/nhei/` tree: the DRAFT path is confirmed mirrored there (`https://www.cnhdrc.cn/nhei/znfb/202412/f1d79e938afd469198a002f82023f4ac/files/1526f091d8074e0ba871371de2268dcc.pdf`, search result [16]). The issued path above is inferred, NOT yet observed — verify at fetch time; if 200, it is a third-host copy of the issued PDF.
4. `http://www.cnwszl.com/docs/wszlzx/details.aspx?documentid=3385` — key `b65c98e05d6aaddbe4635058`. 《中国卫生质量管理》journal's release note "发布|药品临床综合评价质量控制指南（2024年版试行）" (2024-12-31). Corroboration-only: a summary/news page, not the document; title line carries prefix `发布|` (>16-char risk aside, prefix is clean of 《》 but the line ends `（2024年版试行）`→drop→ends with title — actually fits the letter of the rule if rendered as a line; content is NOT the full text, so quote-substance rows would be thin). Low priority.
5. `https://max.book118.com/try_down/995003332333012022.pdf` — key `74ed71b1734d72cb4386c9ee`. Third-party mirror (book118) titled 药品临床综合评价质量控制指南; content unverified, download-gated. Corroboration only; do not bind.
6. `https://www.bjhea.org.cn/35/202501/1126.html` — key `47109f4f5341782fdd7375dc`. Desktop variant of held S119 (mobile URL already in refetch set). Same host as held S118 → no resilience gain; list for completeness only.

## Exclusions (lookalike traps — do NOT bind these to R7)

- `http://www.nhei.cn/nhei/znfb/202412/f1d79e938afd469198a002f82023f4ac/files/1526f091d8074e0ba871371de2268dcc.pdf` (key `357b5cf03c8b36613dc1c33d`) — the **征求意见稿 (DRAFT)** PDF; cover reads `（2024 年版征求意见稿）`. Fails heading rule (title line ends 征求意见稿) and is the wrong edition.
- `https://www.nhei.cn/nhei/znfb/202412/f1d79e938afd469198a002f82023f4ac.shtml` and `https://m.bjhea.org.cn/36/202412/1111.html` — the DRAFT notice pages.
- `https://wjw.guizhou.gov.cn/zwgk/zdlyxx/ywgl/202505/t20250530_87947626.html` — 贵州省's own provincial QC guideline, a different document.
- `https://hdpr.shdrc.org/CN/10.12458/HDPR.202408073` — 《药品临床综合评价项目真实世界研究质量控制规范（2024版）》journal article; different document.
- chinjmap / china-pharmacy journal PDFs — citing articles, not R7 itself.

## Handoff (L1 fetch order, when this wave's C3 fetches run)

1. nhei.cn issued PDF (#1, then #2 variants) — expected to bind R7 exactly like S118 does, on an independent host.
2. cnhdrc.cn issued-path probe (#3) — cheap GET; 200 gives a third-host byte copy.
3. nhei.cn notice .shtml (#2) — corroborates the 2024-12-31 release and the attachment binding; do not rely on it for the heading rule.
4. Skip #4-#6 unless a third source is needed; never fetch the Exclusions list.

No tools installed/upgraded (none needed). No fetches performed. Scratch dir removed on exit (`trap 'rm -rf -- "$S"' EXIT`).

VERDICT: attacked "R7 alternate source URLs" — SURVIVED: 4+ candidates located and ranked by frozen-rule fit (nhei.cn issued PDF + variants top-ranked, cnhdrc.cn mirror hypothesized, cnwszl/book118 corroborative-only), with the draft-edition trap URLs explicitly excluded; corroborates the held S118 binding, no fetches made.
