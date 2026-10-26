# R52GroundChinagpA — staged S112 (中国全科医学 报告清单) re-grounded

Seat R52GroundChinagpA · round 52 wave 1 · 2026-10-26 · leaf member, no dispatch. No tool installed or upgraded (none expected; pacman paused, nothing fetched).

## Capture and form

- URL `https://www.chinagp.net/CN/column/item185.shtml`.
- `.txt` = `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/cacddf3bbf780a4c7582bb17.txt`, **the form for every `char N` below**: read as UTF-8, 6179 chars, sha256 `b1c3cd6a5c22b97fd44c6c35367292a57c299fe19b5eb6c0b9c156bb3abe24f0`.
- `.raw` = same key `.raw`, 81892 chars, sha256 `c21088e1348bad787e0f02da77278b151a0bc48c3a62aa99dae6b88742e708c6`; raw offsets below are `char N` in the `.raw` read as UTF-8.
- Offsets are `str.find` character offsets; that `.txt`-first form is what `corpus/evidence/round52/build-spans.py` admits (its docstring, lane repo, lines 10-13), so each value is a Registry `anchor` `char N` candidate.
- Capture mtime `2026-10-23 20:38:54 -0300` (`ls -l --time-style=full-iso`) is the receipt for the staged "read 2026-10-23"; it dates the capture, not the page.

## What the page is

- Identity: `<TITLE>中国全科医学 报告清单</TITLE>` (`.raw` char 223, count 1) and `<h4 class="item_title"> 报告清单 </h4>` (`.raw` char 11860, count 1); in the text form `中国全科医学 报告清单` (char 16) and the table heading `P RISMA2020 条目清单` (char 920). Column headers follow: `条目清单` 932, `章节主题` 951, `所在 页码` 997.
- Credit line: `From: Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al.` (char 5530) … `BMJ 2021;372:n71. doi: 10.1136/bmj.n71` (char 5694). In the raw `From:` sits inside `<i>` (char 77910).
- Translation credit: none. `翻译` 0, `译` 0, `translat` 0 in `.txt` and in `.raw`; `本刊` 0, `编制` 0 (`grep -o` counts below).
- Publication: `发布日期：2023-01-31` (char 5744) with hit counter `浏览：3452`; site footer `网站版权 © 《中国全科医学》编辑部` (char 6121).
- **Answer.** The page is a **reproduction with a credit line**, not an attributed journal translation: the checklist is Chinese but the only attribution is `From: Page MJ … BMJ 2021;372:n71`, and no translator, adapter or "翻译" string exists on it. "The journal's own translation" is not a stated fact; what is stated is the journal hosting the Chinese checklist in its 报告清单 column under its own website copyright.

## The questions asked

- Items 5-9 exist and are, in order: 5 `纳 排 标准` (label char 1527, text `详细说明纳入和排除标准` 1558), 6 `信息来源` 1621, 7 `检索策略` 1756, 8 `研究选择` 1855, 9 `资料提取` 1976. Labels 8 and 9 recur in the results half (`研究选择` 3480 = item 16a, `资料提取` 5451 = item 26), so only the lengthened text quotes are unique.
- Per-source date wording: `检索日期` **0**, `最后检索` **0**; the page's wording is `检索或查询日期`, exactly once, ending item 6 at char 1707. Neither of the two wordings the seat spec offered occurs in this capture; only `检索或查询日期` does.
- `发布日期：2023-01-31` at char 5744; `浏览：3452` is a page counter, not a second date.
- Identity is journal + column, not a checklist title: 中国全科医学 in the title, 报告清单 in the `item_title` heading, table heading PRISMA2020 条目清单.
- "Own translation" claim is unsupported (sweeps above); "reproduction with credit" is supported (char 5530, 5694).

## Located quotes

| char | c/w | quote (byte-exact) | grounds |
|---|---|---|---|
| 16 | 11/2 | `中国全科医学 报告清单` | journal + column identity |
| 920 | 16/3 | `P RISMA2020 条目清单` | the table is the PRISMA 2020 checklist; note the inter-span space in `P RISMA2020` |
| 1558 | 11/1 | `详细说明纳入和排除标准` | item 5 |
| 1650 | 57/9 | `详细说明获取文献的所有来源，包括 所有数据库、注册平台、网站 、 机构 、参考列表以及 其他 检索或咨询 途径 。` | item 6 source classes incl. 机构 / 参考列表 / 其他检索或咨询途径 |
| 1707 | 19/3 | `明确说明每一项来源 的 检索或查询日期` | item 6's per-source date requirement |
| 1785 | 42/6 | `呈现 所有数据库、注册平台和网站的 完整 检索策略，包括 用到的 过滤器和限制条件。` | item 7 complete strategy + filters/limits |
| 5530 | 81/15 | `From: Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al.` | reproduction credit |
| 5694 | 38/4 | `BMJ 2021;372:n71. doi: 10.1136/bmj.n71` | the cited original |
| 5744 | 15/1 | `发布日期：2023-01-31` | page publication date |
| 6121 | 18/3 | `网站版权 © 《中国全科医学》编辑部` | hosting site's own copyright |
| raw 223 | 26/1 | `<TITLE>中国全科医学 报告清单</TITLE>` | page title, raw form |
| raw 11860 | 34/3 | `<h4 class="item_title"> 报告清单 </h4>` | column heading element, raw form |

Every quote above printed `count=1` on its stated form and contains no newline (`python3` `text.count`/`find` over the files).

## QUOTE machine lines

```text
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	中国全科医学 报告清单	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	P RISMA2020 条目清单	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	详细说明纳入和排除标准	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	详细说明获取文献的所有来源，包括 所有数据库、注册平台、网站 、 机构 、参考列表以及 其他 检索或咨询 途径 。	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	明确说明每一项来源 的 检索或查询日期	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	呈现 所有数据库、注册平台和网站的 完整 检索策略，包括 用到的 过滤器和限制条件。	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	From: Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al.	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	BMJ 2021;372:n71. doi: 10.1136/bmj.n71	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	发布日期：2023-01-31	corpus/knowledge/chinese-prisma-s-reception-r52.md
QUOTE	S112	https://www.chinagp.net/CN/column/item185.shtml	网站版权 © 《中国全科医学》编辑部	corpus/knowledge/chinese-prisma-s-reception-r52.md
```

## Staged sentences about this document

Sweep used throughout (`$T` = the `.txt` capture): `for p in 翻译 译 translat 明确说明每一项来源的检索或查询日期 检索日期 最后检索 PRISMA-S PRISMA2020条目清单 本刊 编制; do printf '%s\t' "$p"; grep -o -- "$p" "$T" | wc -l; done` → `翻译 0 / 译 0 / translat 0 / 明确说明每一项来源的检索或查询日期 0 / 检索日期 0 / 最后检索 0 / PRISMA-S 0 / PRISMA2020条目清单 0 / 本刊 0 / 编制 0`; the `译 / 翻译 / translat / PRISMA-S` rows are also 0 on `.raw`.

Staged entry `knowledge/corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md`:

1. **SUPPORTED** l.5 `the 报告清单 table, items 5-9 — 发布日期：2023-01-31` — 报告清单 is the column heading (char 904; title char 16) and the table's own heading is `P RISMA2020 条目清单` (920); items 5-9 at 1558/1621/1756/1855/1976; date 5744.
2. **SUPPORTED** l.22-23 `A Chinese journal publishes the PRISMA 2020 checklist in Chinese, with the per-source date item.` — title 16 + date wording 1707.
3. **SUPPORTED** l.23-25 `Item 6 requires every source to be named` (1650) `— databases, registries, websites, organisations, reference lists and any other route of search or enquiry — and requires the "search or query date of each source" to be stated` (1707) `; item 7 requires the complete search strategy for every database, registry and website including the filters and limits used` (1785).
4. **SUPPORTED** l.25-27 `The page names Page et al., *BMJ* 2021;372:n71 as the source of the checklist and carries its own publication date of 2023-01-31` — 5530, 5694, 5744.
5. **NARROW** l.37 `a translation published by a Chinese journal (S112)` — hosting supported (6121); the translation act is unattributed: `翻译 0 / 译 0 / translat 0` and the only credit is `From: Page MJ …` (5530). Claim may say: a Chinese-language checklist the journal hosts, credited to Page et al., translator not stated.
6. **NARROW** l.47-51 `appears in the Chinese checklist in Chinese, as 明确说明每一项来源的检索或查询日期 (S112)` — substance supported, but that space-free string is `count 0`; the byte form is `明确说明每一项来源 的 检索或查询日期` (1707, 19 chars). Quote must carry the inter-span spaces.
7. **NARROW** l.74 `The Chinese checklist S112 is one journal's publication of a translated Western checklist.` — "one journal's publication" supported (6121); "translated" is inferred, unswept-supported as an attribution.
8. **UNSUPPORTED (for this document)** l.6-8 recheck clause `confirm the 16 条目 sentence … unchanged` — `PRISMA-S 0`, `条目数 0`, and `16` occurs twice only as item numbers `16a` (3496) and `16b` (3597); there is no 16-item sentence on this page. That sentence is S111's, so the recheck must name S111 for it and S112 only for the 检索或查询日期 item.

Staged row `SOURCES.append.md` l.37:

9. **NARROW** title `PRISMA2020条目清单 (Chinese translation of the PRISMA 2020 checklist)` — `PRISMA2020条目清单` count 0; the capture heading is `P RISMA2020 条目清单` (920) with a space inside `P RISMA2020`; "Chinese translation" unattributed (`译 0`).
10. **NARROW** scope `a Chinese journal's own published PRISMA 2020 checklist … as the journal states it` — "own" is contradicted by the page's own credit line (`From: Page MJ …`, 5530); the journal's ownership is of the site (6121), not of the checklist text.
11. **SUPPORTED** read cell `the 报告清单 table, items 5-9; page 发布日期：2023-01-31, read 2026-10-23` — labels/quotes at 1558/1621/1756/1855/1976, 5744, capture mtime 2026-10-23 20:38:54 (dates the capture).
12. **SUPPORTED** finding cell `item 6 requires every source to be named … together with the 检索或查询日期 of each source; item 7 requires the complete search strategy … including the filters and limits used` — 1650, 1707, 1785 (item 6's date phrase is `检索或查询日期`, not `检索日期`).
13. **NARROW** recheck cell `confirm item 6 still ends 明确说明每一项来源的检索或查询日期` — item 6 does end with that phrase, but as `明确说明每一项来源 的 检索或查询日期` followed by ` 。` (1707); the space-free form is absent (0).

## Draft for the lane entry (intended path `corpus/knowledge/chinese-prisma-s-reception-r52.md`; staged S112 → lane S114)

- 《中国全科医学》 hosts the PRISMA 2020 checklist in Chinese on its 报告清单 page (`中国全科医学 报告清单`, char 16; table heading `P RISMA2020 条目清单`, char 920), dated `发布日期：2023-01-31` (char 5744) (`S114`).
- It is a credited reproduction, not an attributed translation: the page carries `From: Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. … BMJ 2021;372:n71` (chars 5530, 5694) and no `翻译`/`译` string; the site's own claim is only `网站版权 © 《中国全科医学》编辑部` (char 6121) (`S114`).
- Item 6 (信息来源) lists the source classes — `所有数据库、注册平台、网站 、 机构 、参考列表以及 其他 检索或咨询 途径` (char 1650) — and ends `明确说明每一项来源 的 检索或查询日期` (char 1707): the per-source date field is present in Chinese, but the page never writes `检索日期` or `最后检索` (both 0) (`S114`).
- Item 7 (检索策略) asks for `完整 检索策略` over `所有数据库、注册平台和网站` with `过滤器和限制条件` (char 1785) (`S114`).
- Inference to hold: the Chinese reception of PRISMA-S's per-source date field arrives through a *credited reproduction* of the PRISMA 2020 checklist, so the field's Chinese wording is `检索或查询日期` (char 1707) and a Chinese claim record may quote it — but the page attributes no translator and no adapter to Chinese databases (`S114`; `BMJ 2021;372:n71` at char 5694).

## Limits

- Criterion 30's live gate (`tools/quote-reopen.py verify`) was **not** run: it fetches the registry URL, this seat has no network, and lane `corpus/SOURCES.md:121-122` already bind S111 to the SinoMed record and S112 to the JAHBS article, so the staged id has no lane URL to reopen. Substituted check: unique-occurrence (`count=1`) on the pinned `.txt`/`.raw` digests, which is the admission rule of `build-spans.py`.
- `build-spans.py --check`, the C1/C2 counters and `inference-ground.py` were not run: no `quotes.tsv` row or entry is mine to write, and the counters are another seat's.
- The page's checklist items 10a-27 were read only in passing (offsets 3496, 3597, 5451); no claim here covers them.
- The site footer shows `冀ICP备12018774号-6` with a Beijing address; recorded as observed, not interpreted.
