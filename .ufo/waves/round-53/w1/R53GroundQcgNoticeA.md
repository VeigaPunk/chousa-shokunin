# R53GroundQcgNoticeA — staged S186 re-grounded → planned lane S119

Seat R53GroundQcgNoticeA (leaf, no dispatch), round 53 wave 1. Frozen claims read at
`corpus/evidence/round53/claims.md`; no predicate, target, counter or control touched. Staged
artefacts read only: `merge/chousa/knowledge/corpus/knowledge/quality-control-guideline-issued-text-r48.md`
(96 lines) and `merge/chousa/SOURCES.append.md:111` (S186, 11 cells). No campaign tool run.

## Capture identity (observed)

```
$ sha256sum .qcache/cfa080b4046592eb9490a82c.{txt,raw}
892da7addf636f484580d4c9ea50f1199f2a39b5b8ec73ef7ad8b70a3260dfeb  cfa080b4046592eb9490a82c.txt
95843e4ef72ec3ada97356022742dfebe6ff2ce82dd805b152d37f672e8ab614  cfa080b4046592eb9490a82c.raw
$ python3 -c 'sha256(url)[:24]'
cfa080b4046592eb9490a82c  http://m.bjhea.org.cn/35/202501/1126.html
a184ff6db4644e066a70e3e9  https://m.bjhea.org.cn/35/202501/1126.html
$ builder-space scan   chars 1255  lines 268  nonws 726  FFFD 0
$ txt.count('20250115') 0 · txt.count('http') 0 · txt.count('href') 0 · raw.count(attachment) 1 @ 9051
```

- Only the staged http URL keys this capture; the https variant keys `a184ff6d…`, which has no
  capture — it would be refused by `build-spans.py`.
- `.txt` read as the builder reads it, `txt.read_text(encoding="utf-8", errors="replace")`
  (`corpus/evidence/round53/build-spans.py:123`): **1,255 chars / 268 lines**; the bytes hold 206
  `\r`. Every offset below is in that 1,255-char space. The S186 row's "1,461 characters" is the
  byte-decode count (1,461 = 1,255 + 206 CR): same text, different newline convention.
- **U+FFFD count: 0**, and the `.txt` is a faithful text form of the `.raw`: after removing
  tags/comments/`<script>`/`<style>`, unescaping entities and dropping whitespace, raw and txt both
  normalise to **726 characters and are equal** (common prefix 726, multiset difference empty both
  ways) — no text added or lost. `pdftotext` exists (`/usr/bin/pdftotext`) but this capture is
  HTML (17,592 bytes, `<!DOCTYPE html>`), so the PDF sample check does not apply, and the builder's
  raw form (UTF-16LE decode) is unusable for quoting: every quote lives in the `.txt`.

## Claim-by-claim (every staged-entry sentence resting on S186)

`char` = offset in the 1,255-char `.txt`. **located** = quote supports the sentence as written;
**located-narrower** = quote supports part of it, or the sentence reads more into the text.

| # | claim (first ~80 chars) | line | verdict | quote @ char |
|---|---|---|---|---|
| 1 | `source: S186 — http://m.bjhea.org.cn/35/202501/1126.html — the release notice's title, date, s` | 3 | located — title, date, stated source, act of issuance, attachment name all present | @10, 517, 534, 724, 841 |
| 2 | `技术综合评估中心, also styled 国家卫生健康委卫生发展研究中心 — issued 《药品` | 13-14 | located — the signature prints both names on consecutive lines (190–191), the second parenthesised | @879 + @897 |
| 3 | `临床综合评价质量控制指南（2024年版试行）》 on 2024-12-31 …` | 15 | **located-narrower** — (a) the document's title has a space, `（2024年版 试行）`, so the entry's unspaced title is not byte-exact; (b) `2024年12月31日` is the notice's signature date, not a statement of when the guideline took effect | @724 / @841 / @920 |
| 4 | `**2025-01-03**, with a notice that reads 现予以发布 and names the issuing body` | 16 | 现予以发布 located; **date located-narrower** — `发布时间：2025年01月03日` is the *notice's* posting time | @724; @517 |
| 5 | `as 国家卫生健康委卫生发展研究中心. Both the notice and the **issued text** are` | 16-17 | **located-narrower** — 来源 names only that body, but the signature names `国家药物和卫生技术综合评估中心` first, the 委中心 parenthetically; the entry names one of two | @534 vs @879/@897 |
| 6 | `open access, on a professional society's own file host.` | 18 | **located-narrower** — carrier located (footer); "open access" is stated nowhere, it rests on the fetch; the issued text's host is fixed only by the notice's raw href | @1139; raw @9051 |
| 7 | `before it, so the society's carrier is the corpus's only open copy of an` | 65 | **located-narrower** — "society's carrier" located; "only open copy" is an absence claim resting on the `nhei.cn` refusals, not on this document | @10 / @1139 |
| 8 | `recheck: 180d — … the notice still states the 2025-01-03 date` | 6 | located — the date is printed once, so the recheck predicate is decidable from this form | @517 |
| R | row S186 `teaches:` "the attachment … sits on the society's own file host under a 2025-01-15 upload path" | SOURCES 111 | **absent in the text form** (0 hits `20250115`, 0 `http`); **located only in the raw markup** (`href` @9051) | raw only |

Nothing resting on S186 is contradicted: the notice does read 现予以发布, is posted 2025-01-03,
is signed 2024年12月31日, states 来源 国家卫生健康委卫生发展研究中心, and names the attachment.
The three narrowings are wording/spacing, not fact.

## Machine lines (planned lane id S119; byte-exact, unique, one line, ≤25 words / ≤160 chars)

```
QUOTE	S119	http://m.bjhea.org.cn/35/202501/1126.html	《药品临床综合评价质量控制指南（2024年版 试行）》发布_北京市卫生经济学会	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S119	http://m.bjhea.org.cn/35/202501/1126.html	发布时间：2025年01月03日 来源：国家卫生健康委卫生发展研究中心	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S119	http://m.bjhea.org.cn/35/202501/1126.html	来源：国家卫生健康委卫生发展研究中心	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S119	http://m.bjhea.org.cn/35/202501/1126.html	按照《国家卫生健康委办公厅关于规范开展药品临床综合评价工作的通知》（国卫办药政发〔2021〕16号）	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S119	http://m.bjhea.org.cn/35/202501/1126.html	形成了《药品临床综合评价质量控制指南（2024年版 试行）》，现予以发布。	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S119	http://m.bjhea.org.cn/35/202501/1126.html	药品临床综合评价质量控制指南（2024年版 试行）》采用开放式动态修订机制	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S119	http://m.bjhea.org.cn/35/202501/1126.html	附件： 药品临床综合评价质量控制指南（2024年版 试行）.pdf	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S119	http://m.bjhea.org.cn/35/202501/1126.html	国家药物和卫生技术综合评估中心	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S119	http://m.bjhea.org.cn/35/202501/1126.html	（国家卫生健康委卫生发展研究中心）	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S119	http://m.bjhea.org.cn/35/202501/1126.html	2024年12月31日	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S119	http://m.bjhea.org.cn/35/202501/1126.html	北京市卫生经济学会版权所有	corpus/knowledge/quality-control-guideline-issued-text-r48.md
```

Offsets in block order — each `text.count(q) == 1`, none contains `\n`, longest 50 chars, at
most 3 whitespace words: **10, 517, 534, 567, 724, 764, 841, 879, 897, 920, 1139.** #4 is the
notice's legal basis; #6 is the page's own defect (below), kept so it is not mistaken for a sound
sentence start.

## Findings for the L1 (reported, nothing patched)

1. **The newline space is load-bearing.** `build-spans.py` reads the `.txt` in text mode, so CRLF
   collapses and the offset space is 1,255 chars, not the row's 1,461. A binary decode shifts
   every late offset (`（国家卫生健康委卫生发展研究中心）` is 897 here, 1,049 there). Record
   offsets from the builder's read.
2. **`发布时间` is not an issuance date.** The text gives two dates and labels neither as the
   guideline's effective date: `发布时间：2025年01月03日` (posting) and the signature
   `2024年12月31日`. "Issued 2024-12-31, released 2025-01-03" is a defensible reading of those two
   lines, but no sentence states the instrument's issue date; a C2 quote must say which line it
   stands on.
3. **Two issuing bodies, one named.** `国家药物和卫生技术综合评估中心` (line 190) with
   `（国家卫生健康委卫生发展研究中心）` (line 191), and a 来源 line naming only the second.
4. **Title spacing.** Document `（2024年版 试行）`; entry `（2024年版试行）` (line 15, one hit).
   The unspaced string occurs nowhere in the capture, and `build-spans.py` refuses a non-exact
   quote — any C2 quote or anchor must use the spaced form.
5. **The attachment href is S185's URL.** The notice's markup links
   `https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf` (raw @9051),
   byte-identical to the staged S185/S195 source cell: a *documentary* link from S186 to the
   issued text, stronger than the entry's two independent host observations and not yet stated.
   It also confirms the row's "2025-01-15 upload path", which must not be quoted as text.
6. **The page's own typo.** The second body paragraph opens mid-bracket:
   `药品临床综合评价质量控制指南（2024年版 试行）》采用开放式动态修订机制` (@764, unbalanced
   `》`). Quote the 现予以发布 sentence (@724) instead.
7. **Carrier.** `北京市卫生经济学会版权所有` (@1139) and the title line (@10) are the only
   in-text evidence of the carrier; the text says 学会, never "professional society". The capture
   is the mobile host (`m.bjhea.org.cn/35/…`), the same society as the issued text's file host.

## Not done / limits

- No `c1-count.py` / `c2-count.py`, no `quotes.tsv`/`spans.tsv`, no lane file written: the L1
  integrates, and my offsets are inputs, not a manifest.
- No network: the capture was not re-fetched, so "the notice still states …" (claim 8) holds for
  the on-disk capture only, not for the live host at recheck time.
- S185/S190/S193 (title block, 灰色文献 count, the 2019 NMPA contrast) are out of this seat's
  scope and were not re-checked.
- Tooling: **no install, no upgrade, no pacman** (paused host-wide). Scratch
  `/fast/scratch/hyaku/chousa-r53/R53GroundQcgNoticeA` had `TMPDIR` set there and was removed.

VERDICT: attacked the staged S186 → S119 claim set — notice title, 来源, date (2025-01-03 posting vs 2024-12-31 signature), 现予以发布 act, attachment name — all **located**, with three narrowings found (unspaced title, singular issuing body, 发布时间 read as release date), one **absent-from-text** row claim (2025-01-15 upload path, raw-only), 0 U+FFFD, a byte-faithful `.txt` under the builder's read, and 11 byte-exact quotes at offsets in the 1,255-char span space.
