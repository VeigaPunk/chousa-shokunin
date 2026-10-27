# R57W1ScoutR3Alt — R3 (管理指南 2021年版) URL scout, second angle

Seat: R57W1ScoutR3Alt (scout, leaf). Item: locate HTML pages announcing/adopting the 2021 管理指南
where the title prints as one line; assess whether the 2021 管理指南 is publicly served at all;
rank least-bad. No fetches (scout seat); 10 web searches + reads of committed lane bytes only.
No frozen predicate/target/counter/recipe is proposed for change; findings below are reported, not patched.

## Established from committed lane bytes (read-only)

- R3 per frozen REFS (c3-count.py:74-82): title `药品临床综合评价管理指南`, token `2021年版`.
  S127's own foreword (`corpus/captures/b27ffd2f0161104c6a28c9f5.txt:152`) and the S128/S129 captures
  (`de9f5afc3809acbf61f4d5bb.txt:53,155`) record the full styled name 《药品临床综合评价管理指南
  （2021年版 试行）》, 配发 with the 2021-07 通知 (国卫办药政发〔2021〕16号).
- S130 (`corpus/SOURCES.md:140`) is the 2020-11 征求意见 text; its row says "never for the current
  management guideline" — R3 must not be bound through S130 (matches claims.md freeze-time note).
- Wave fetch log (`corpus/evidence/round57/refetch.tsv`, 111 rows at read time): the L1 already
  queued R3-adjacent URLs this wave —
  - S132 = `https://www.nhc.gov.cn/yaozs/c100097/202107/d2a45e6ae041423f950b3865e43f5ef6.shtml`
    attempt 1 (08:31:04Z) curl_rc=22 http=412; archive.org mirror also 412.
  - S131 = 2019 通知 page, same 412.
  - S133 = `http://www.tcmevidence.net/UserFiles/upload/file/20230410/6381676262587201848492833.pdf`
    attempt 1 curl_rc=28 (timeout), attempt 2 (08:35:01Z) http=200, raw_sha256=c4bedad5…,
    txt_sha256=ceef80d9…. Note: refetch.tsv reuses id S133 for two distinct URLs (this tcmevidence
    PDF and the NHC 2020-draft downFiles PDF, byte-identical to S130) — triples are (id,url,key) so
    both rows stand, but a mined registry row for R3 should get its own fresh id, not S133, if S133
    is taken by the 2020-draft fetch (builder/L1 call).
- The landed tcmevidence capture was checked against the frozen rule in a scratch copy of the
  counter (original never edited; scratch deleted after):
  `cp corpus/evidence/round57/c3-count.py $SCRATCH/c3-copy.py`, then
  `m.heading_title(form,"药品临床综合评价管理指南")` → **True**; `m.nows(form).count("2021年版")` → **1**;
  matching line printed as `               药品临床综合评价管理指南` (standalone heading, prefix 0,
  no 《》.[]［］). Head of the .txt also shows `（2021 年版试行）` two lines below the title.
  So the capture-side conditions (token + heading) for binding R3 via this URL are already met by
  committed lane bytes, pending the L1's registry/manifest work.

## Candidates (announcement/adoption HTML where the title prints as one line)

Title-in-h1/title candidates, most relevant first:
1. `https://wjw.chengde.gov.cn/art/2021/7/29/art_464_784401.html` — 承德市卫健委 2021-07-29
   announcement "药品临床综合评价管理指南发布"; article title prints the guide title as one line.
2. `http://www.tcmevidence.net/evidence/img/2068/2116.html` — 中医药证据网 repost page; h1
   《药品临床综合评价管理指南（2021年版 试行）》(《》-wrapped; fails heading rule but announces).
3. `https://www.pharnexcloud.com/data/zcfg_546372fed05fbed1fa6fb3600f264192.html` — 医药魔方
   mirror, notice + attachment full text, title one line in title tag.
4. `https://www.nhc.gov.cn/yaozs/c100097/202107/d2a45e6ae041423f950b3865e43f5ef6.shtml` — official
   notice HTML with the 指南 full text inline (附件 block prints the guide title as its own line).
5. `https://www.nhc.gov.cn/wjw/c100175/202107/58a87de5349a484e9ef87b8ac0a32ce7.shtml` — same
   notice+full text on the wjw channel.
6. `http://wsjkw.hebei.gov.cn/zcfg2/380991.jhtml` — Hebei repost (cited as EB/OL by two journals).
7. `https://ylqxzb.com/ZBZcfg/Item84e33c7a673d0c38.html` — Shanghai 药械招标 repost of the notice.

Binding-oriented byte surfaces (PDF; heading + token expected, cf. gazette index text showing the
guide title as a heading line):
8. `https://www.nhc.gov.cn/cms-search/downFiles/d5e6c29ceff147118d7c266870106c79.pdf` — 公报
   2021·07 bound PDF (notice + 指南全文). Official. Not yet fetched this wave.
9. `https://www.nhc.gov.cn/bgt/201807sgf/202109/5e18d6d8d86e405bad64dd4a8b666310/files/1733795726978_35780.pdf`
   — same gazette issue via /bgt/ path.
10. `https://wsjkw.qinghai.gov.cn/zwgk/jgzn/nsjg/ywzcyjbywzdc/gzdt_6118/202108/P020230908664799012997.pdf`
    — Qinghai gov hosting the notice PDF scan.
11. `http://dxpharm.net/uploadfiles/2021/07/20210730153530542.pdf` — dxpharm notice PDF mirror.
12. `https://cmei.org.cn/uploads/20210804/9b15e786d682e9618949a5273dc44aeb.pdf` — CMEI PDF (search
    engine could not read it; unverified content).

## Is the 2021 管理指南 publicly served at all?

Yes. It is publicly served from the publisher's own host (NHC: notice HTML + gazette PDF + the
2020/2021 file endpoints) and from at least two provincial gov hosts (Qinghai PDF, Chengde HTML)
plus several third-party mirrors. Not every lead is paywalled/captcha. Observed caveats from the
wave's own fetch record: NHC `.shtml` article endpoints returned HTTP 412 to this host at 08:31Z
(while NHC `/cms-search/downFiles/` and `/yaozs/.../files/` PDF endpoints returned 200 within the
same minute — S130 twice, S133 2020-draft) — consistent with transient anti-bot throttling of the
article route rather than a paywall; the campaign recipe's ≥600 s-spaced retry on S132 will test
this. web.archive.org mirrors of the NHC pages also failed (404/412), so the archive is not a
fallback for these two URLs today.

Least-bad ranking for R3 (bindability × authority × fetchability):
1. tcmevidence standalone 指南 PDF (already 200 in lane; token+heading verified mechanically) —
   least effort, but third-party mirror: edition fidelity is inferred from its own cover text, not
   from the issuer's bytes.
2. NHC gazette PDF d5e6c29c… (official, full text incl. guide; not yet fetched).
3. NHC notice HTML S132 (official, full text inline; currently 412 — retry after spacing).
4. Qinghai gov PDF / Chengde HTML (gov mirrors of the national instrument).
5. pharnexcloud / tcmevidence HTML (readable mirrors; 《》-wrapped headings fail the rule).
Ranked last (captcha/paywall/doc-mill — do not spend attempts): doc.docsou.com, doc.quark.cn,
scribd, book118 (also a fake "2026版" doc), baidu wenku.

## Attack surface notes (reported, not patched)

- The 412 rows for S131/S132 are facts of the fetch record; they do not touch any frozen predicate.
- If the L1 binds R3 via the already-landed tcmevidence capture, every capture-side condition I can
  check mechanically holds; manifest quotes/anchors remain builder-side work I did not do.
- Overlap: a first-angle R3 scout seat may exist among hidden peers; no R3 report was present in
  `.ufo/waves/round-57/w1/` when I checked (`ls` → only swarm-registry.json).

## Evidence log

- `grep`/`sed` on `corpus/captures/b27ffd2f0161104c6a28c9f5.txt:152`,
  `de9f5afc3809acbf61f4d5bb.txt:53,155`, `corpus/SOURCES.md:140`, `c3-count.py:74-82` — outputs above.
- `awk` on refetch.tsv (S118/S127/S130-S136 rows) and `tail -5` — outputs above.
- Python check in scratch (counter copy): heading_title True; token count 1; scratch dir removed
  (`rm -rf /fast/scratch/hyaku/chousa-r57/R57W1ScoutR3Alt` confirmed).
- 10 web_search calls (exact-phrase, notice-number, provincial, filetype, host-restricted variants).
- No network fetches by this seat. No lane/fleet/shokuknow writes except this report. No tools installed.

VERDICT: scouted second angle on R3 (管理指南 2021年版) — 12 candidate URLs located (≥6 one-line-title
HTML announcement/adoption pages incl. Chengde, tcmevidence, pharnexcloud, both NHC notice pages), public
availability confirmed (NHC gazette/notice + provincial + mirror; NHC .shtml currently 412-throttled),
least-bad ranked; the already-landed tcmevidence capture passes the frozen token+heading rule mechanically
— attack item survived with evidence, no frozen claim touched.
