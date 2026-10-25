# W2 Quarantine hand-check — chousa round4 S114

Verdict: **PRESENT in the fetched payload — register's `payload-absent` is a
checker artifact, not a fabrication.** Both quoted spans occur verbatim inside
the captured HTTP response body for the cited URL. The one calibration caveat:
the spans sit inside a single HTML comment (`<!-- ... -->`, raw bytes
10330–11243) that SinoMed ships but never renders; the checker's own
`html_to_text` deletes comments, so the derived `.txt` capture legitimately
lacks them. The ABSENT flag is a transform artifact; the row is also honestly
misleading about where on the record these fields live — flag for wave-3
wording review, not as a fabricated quote.

## Row under test

- Frozen slice: `chousa-shokunin/.ufo/waves/round-48/assimilation/quarantine-slice:17` — `S114   payload-absent`
- Register: `shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:53` —
  `| chousa | round4 | S114 | payload-absent | https://www.sinomed.ac.cn/article.do?ui=2026335073 |`
  - Q1 `主题词： *评价研究;*研究报告;Meta分析;*清单;质量控制`
  - Q2 `学科分类号： R-05;R-37;R348.3;R916.3`
- Census: `quote-lint-full-v5.json` lines ~1806–1825 — two `verdict:"ABSENT"`,
  `binding:"id"`, `sweep:false`; two sibling quotes for the same URL folded
  (`来源出版物` no-whitespace; `关键词` whitespace).
- ID crosswalk: register `S114` ≡ staged gate `S119`
  (`lanes/chousa/round4/SOURCES-PROPOSED.md:35`, gate `#### Gate — S119`
  lines 68–76; disputed lines are 73–74) ≡ merge row `S119`
  (`merge/chousa/SOURCES.append.md:44`). Per `lanes/chousa/ID-REMAP.md` the
  landed registry id is `S122`; the census ran on an older numbering — the URL
  is the binding key, so this is bookkeeping drift, not a binding error.
- Companion URLs: `doc.sinomed.ac.cn` order service — no cache entry, never
  fetched (per the lane's own note, paywalled). Wave-3 companion page
  `medsci.cn/guideline/show_article.do?id=23e481c0052069d3` IS cached
  (`453d492becd9a2f4632cb8dd.*`, 276,803 B raw / 14,135 B txt, sha256
  `712cdef6…` / `ad6b09f0…`): `主题词`, `学科分类号`, `R-05`, `评价研究` all
  occur 0 times — it does not carry the fields.
- Local artifacts: `grep -rln "R-05;R-37\|评价研究;.*研究报告;Meta分析"` over
  `lanes/` and `chousa-shokunin/corpus/` outside excluded staging files → no
  hits; the URL does not appear anywhere under `chousa-shokunin/corpus/`.

## Capture examined (local bytes only; no fetch)

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`
`42bac8830527d6f1bb125c49` (key = sha256(url)[:24]):

- `.raw` — 20,142 B, UTF-8 HTML w/ CRLF, sha256
  `0d1c08a6ca7ee09a59c9ff7cef06841b088628135216e93caa8124b5663f572b`
- `.txt` — 2,969 B, 467 lines, sha256
  `4d3bff5067b4cf8e81980618696fdd28c4457f6e64d361b1164b60625c937671`

## Commands and observed output

```
$ python3 -c "import hashlib;print(hashlib.sha256(b'https://www.sinomed.ac.cn/article.do?ui=2026335073').hexdigest()[:24])"
42bac8830527d6f1bb125c49
$ grep -ob "学科分类号\|R-05\|R-37\|R348\|R916" 42bac8830527d6f1bb125c49.raw
10402:学科分类号   10452:R-05   10457:R-37   10462:R348   10469:R916
$ grep -ob "主题词" 42bac8830527d6f1bb125c49.raw
10579:主题词   (also 12433, 13264 — the rendered "查看主题词相同的文献" block)
```

Raw bytes 10330–11243 (UTF-8, tags stripped in reading):
`<!--  <tr><td><span class="cuhuise12a">学科分类号：<span class="huise">
R-05;R-37;R348.3;R916.3</span></span></td></tr>  <tr><td><span
class="cuhuise12a">主题词：<span class="huise"> *评价研究;*研究报告;Meta分析;
*清单;质量控制 </span></span></td></tr> … -->`

Both field runs are verbatim text of the payload — the quoted spans are the
commented-out `<td>` rows with tags and whitespace folded, matching the exact
quote style the lane used for the passing `来源出版物`/`关键词` quotes.

```
$ grep -obn "主题词\|学科分类号\|R-05" 42bac8830527d6f1bb125c49.txt
285:1906:主题词          # only inside "查看主题词相同的文献，请选择：" — terms
                        # themselves render as checkbox chips at txt L288–300
# Q1/Q2 as written: 0 hits; simulated html_to_text fold (comment strip +
# tag strip + whitespace fold) over .raw: both quotes absent — reproduces
# the census result exactly.
```

## Reason

The census matches quotes against `.txt`, produced by `html_to_text`
(`quote-lint.py:515-522`), whose second line is `re.sub(r"(?s)<!--.*?-->", " ", s)`.
SinoMed's record table places `学科分类号` and `主题词` inside a `<!-- -->`
block while `来源出版物`/`关键词`/`摘要` live outside it — which is exactly why
two of the gate's five quotes folded green and these two went ABSENT. The
`.raw` payload contains the fields verbatim, so "the quote is in none of them"
is false for the payload itself; it is true only for the rendered page. The
row's gate claim ("the 来源出版物 / 关键词 / 主题词 / 学科分类号 fields of the
record") is satisfied as record payload data; an editor reading rendered text
alone would not see those two field labels — worth a wave-3 note amendment,
not a fabrication verdict.

## C1 bearing

No bearing. R48-C1 (`corpus/evidence/round48/claims.md`) is a lexical counter
over the polarity-check tool's fixtures; this row's outcome only feeds the
falsification count of `payload-absent` rows: this register row does **not**
survive as a fabricated-quote exemplar (present-in-payload), though it survives
as an absent-in-rendered-text finding.
