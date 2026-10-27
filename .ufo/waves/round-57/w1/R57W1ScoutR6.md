# R57W1ScoutR6 — R6 (儿童药品临床综合评价技术指南 2022年版 试行) alternate source URLs

Seat: scout R6 (leaf, no subagents) · wave 1 · 2026-10-27. Scope: URL scouting only — no fetches run by this seat
(L1 fetches candidates during this wave). Target: R6 per `corpus/evidence/round57/c3-count.py` REFS
(`("R6", "儿童药品临床综合评价技术指南", "2022年版")`), frozen at claims.md R57-C3.

## Lane state observed (commands run)

- `grep -l 儿童药品临床综合评价技术指南 corpus/captures/*.txt` → only `b27ffd2f0161104c6a28c9f5.txt` (S127) and
  `de9f5afc3809acbf61f4d5bb.txt` (S128). No R6-document capture is lane-held: `ls 700aa93054e967318bc47d2d.*` →
  absent; no cover match (`head -c2000` over all 98 `.txt`). `refetch.tsv` has no 儿童/cpia row yet.
- Split-title evidence in held bytes: `corpus/captures/b27ffd2f0161104c6a28c9f5.txt:1367-1371` — S127's own
  reference [33] wraps the title: `…儿童药品临床综合评价技术指南（2022 年版 试` / `行 …）` + URL wrapped
  `…eef00a18bd641c9b3bbf21` / `3193df2730.pdf`. So the lane's only R6 title text is line-split (cannot bind).
- Search snippets show the same split on the official PDF covers (see PDF candidates below): cover line reads
  `儿童药品临床综合评价` then `技术指南 （2022 年版 试行）`. [INFERENCE] all three PDF mirrors appear to be the
  same typeset file; byte-identity is a post-fetch check, not asserted.

## Candidates — HTML pages carrying the title on ONE line (snippet evidence from web_search results)

1. `http://www.nhei.cn/nhei/znfb/202206/c01d87a290664b01bf42a9dad769d69f.shtml` — key `1c3fff255511f91ed83c014c`.
   Official 通知 page (指南发布 column, 2022-06-29). Snippet: "国家药物和卫生技术综合评估中心关于发布心血管病、
   抗肿瘤、儿童药品临床综合评价技术指南…按照…国卫办药政发〔2021〕16号…国卫药政函〔2019〕80号…等文件要求".
2. `http://cpia.org.cn/index/Xharticle/info.html?cate=17&id=477` — key `dc6b4b5d363a2011cac92cbd`. CPIA HTML repost
   of the same 通知. Snippet: "…会同有关单位制定了《心血管病药品临床综合评价技术指南（2022年版 试行）》《抗肿瘤
   药品临床综合评价技术指南（2022年版 试行）》《儿童药品临床综合评价技术指南（2022年版 试行）》…" (titles one per line in body).
3. `https://www.hnysfww.com/article.php?id=3275` — key `9695437cac165bb4b6145deb`. 河南药学服务网 repost w/ download
   links. Snippet: "2022年6月29日发布：…制定了《…儿童药品临床综合评价技术指南（2022年版 试行）》。现予以发布，
   自发布之日起实施。… ☛ / 儿童药品临床综合评价技术指南（2022年版 试行）.pdf".
4. `https://www.cn-healthcare.com/article/20220629/content-570822.html` — key `dcb4fcb05b5d53f1967e9af9`. 健康界 news
   headlined "《儿童药品临床综合评价技术指南（2022年版 试行）》印发" (2022-06-29). API variant
   `https://www.cn-healthcare.com/api/third/article/570822` (key `3caa2ffef03fc5fa8b39e4dd`) snippet: "该指南遵循国家
   管理指南的原则，突出儿童用药供应保障决策的需求…".
5. `http://www.nhei.cn/nhei/zjjd/202206/90b070c5b3ff4384a57a17c1c4392a94.shtml` — key `28ce1cf0d1d8da1967eeb833`.
   Official 专家解读 (2022-06-29). Snippet: "《儿童药品临床综合评价技术指南（2022年版试行）》专家解读. 时间：2022-06-29
   文章来源：药物评价与技术评估. …近日，《儿童药品临床综合评价技术指南（2022 年版 试行）》由国家药物和卫生技术综合评估中心…牵头发布".
6. `https://zk.cn-healthcare.com/doc-show-66493.html` — key `5e5996522bdf96e6e85c63e4`. 健康界智库 viewer; page title
   "儿童药品临床综合评价技术指南（2022年版 试行）.pdf" — one line, no 《》, token 2022年版 on the same line.
7. `https://journal.china-pharmacy.com/journal-web/182/34238137/16/` — key `11392e3bfd3417f16ca6f1f3`. 中国药房 网刊 page:
   "2022年6月29日国家药物和卫生技术综合评估中心发布了《心血管病药品临床综合评价技术指南》《抗肿瘤药品临床综合
   评价技术指南》《儿童药品临床综合评价技术指南》" — one-line titles but NO edition token in that sentence (weaker).

## Candidates — PDF bytes (title split across cover lines in snippets; still useful as byte sources)

8. `http://www.nhei.cn/nhei/znfb/202206/c01d87a290664b01bf42a9dad769d69f/files/60c39855fa6048e6aae17323b1fbd546.pdf`
   — key `52f3bf6585d3aca9aaef8a63`. Official PDF. Snippet first cover line: "技术指南 （2022 年版 试行） 国家药物和卫生
   技术综合评估中心…二〇二二年六月" (title split "儿童药品临床综合评价" / "技术指南（2022 年版 试行）").
9. `http://cpia.org.cn/uploads/20220630/eef00a18bd641c9b3bbf213193df2730.pdf` — key `700aa93054e967318bc47d2d`. The URL
   S127's reference [33] itself cites (line-reconstructed from b27ffd2f:1369-1371). Snippet: "儿童药品临床综合评价 技术指南…
   技术指南 （2022 年版 试行）…二〇二二年六月".
10. `http://www.cpia.net.cn/uploads/20220630/eef00a18bd641c9b3bbf213193df2730.pdf` — key `20a83add4bef521452e03ac1`.
    cpia.net.cn mirror of #9; search summary: "封面确认为《儿童药品临床综合评价技术指南（2022年版 试行）》，落款为二〇二二年六月".

## Rejected near-misses (calibration)

- `https://www.takarabiomed.com.cn/DownLoad/5261.pdf` — Agarose D-1 LE product manual; false positive from a loose query.
- `http://www.nhei.cn/nhei/znfb/202112/9e350a54d2ea4c3ab9a0237ee4eab9f0/files/b91a31e231614faaa485971756aabb5b.pdf`
  (also mirrored at `https://www.cnhdrc.cn/...` same path) — the 2021年版 (二〇二一年十二月); lacks token 2022年版. Do not bind.
- `http://cpia.net.cn/uploads/20220630/59831d29ddfe35745066ea54956a9b0f.pdf` — per S127's own reference list this file is
  the 心血管病 (R5) guideline, not R6.
- `https://max.book118.com/html/2024/0525/7201103015006113.shtm` — "儿童药品临床综合评价技术指南2021年版.pdf"; wrong edition.

## Heading-shape note (against the FROZEN rule; reported, not patched)

Announcement HTML bodies quote the title inside 《》 (prefix contains 《 → fails the ≤16-char clean-prefix test); the
doc-show page's bare-title line ends in ".pdf" (no trailing （…） to drop → fails as-is). Whether any candidate's
html_to_text line satisfies the frozen heading rule is a post-fetch measurement for the builder seat — the L1 should
fetch several of #1–#7 and run `c3-count.py`'s own heading logic, not pre-commit to one.

No tools installed/upgraded; no lane, fleet, or shokuknow writes; no fetches (scout seat: search only). Scratch
`/fast/scratch/hyaku/chousa-r57/R57W1ScoutR6` removed on exit (`trap 'rm -rf -- "$S"' EXIT`).

VERDICT: scouted 6+ one-line-title R6 source URLs (7 HTML + 3 PDF mirrors, keys computed; 4 near-misses rejected) —
the "find alternate sources for R6" item survives, pending L1 fetch + frozen-counter heading judgment.
