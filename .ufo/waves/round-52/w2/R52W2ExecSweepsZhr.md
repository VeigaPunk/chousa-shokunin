# R52W2ExecSweepsZhr — re-run sweep of `corpus/knowledge/chinese-prisma-s-reception-r52.md`

Attacked: every runnable command, every negative statement and every `char N` in the S113/S114 entry,
its cross-file comparisons, and the `tools/inference-ground.py` pass the C2 predicate relies on for it.
Scratch `/fast/scratch/hyaku/chousa-r52/R52W2ExecSweepsZhr` (TMPDIR set there); captures re-opened
read-only from `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`; no install
(none needed); no network (L0 `8d77e6c1` open).

## 1. `recheck:` command — reproduces

`python3 corpus/evidence/round52/build-spans.py --check` (lane root) → `SPANS_ROWS=38 STALE=0`, exit 0.
The second half ("re-open both pages") is **not runnable as written** offline; its on-disk form is
checked in §3/§6.

## 2. Every `char N` — 15/15 reproduce, count 1 at the stated offset (S115: n/a, none quoted)

```
S114 16='中国全科医学 报告清单' 920='P RISMA2020 条目清单'
S114 5530='From: Page MJ, McKenzie JE, Boutro…' 5694='BMJ 2021;372:n71. doi: 10.1136/bmj.n71'
S114 5744='发布日期：2023-01-31' 6121='网站版权 © 《中国全科医学》编辑部'
S114 1650='详细说明获取文献的所有来源，包括 所有数…' 1707='明确说明每一项来源 的 检索或查询日期'
S114 1785='呈现 所有数据库、注册平台和网站的 完整…'
S113 2328='PRISMA-S(PRISMA for Searching)…内在局限' 2433='在逐条阐释…提出实践建议。'
S113 2034='2026-04-25 中国循证医学杂志' 3139='copyright=0, …linkOutUrl=,'
S113 4850='NameList=[AttachmentFileName(…郑卿勇.pdf)])' 7287='梅斯医学是面向医生的综合互联网平台'
rows 15 mismatch 0
```
`len(453d…txt)=8804`, `len(cacddf…txt)=6179` — entry's 8,804/6,179 ✓ (`wc -m` in the C locale prints
7,585 for S114, i.e. bytes; python `len` is the stated form). S113 `.raw` is 276,803 bytes HTML — ✓.

## 3. Negative statements — each re-run

| Statement | Receipt | Result |
|---|---|---|
| `翻译`/`译`/`translat` 0 times (S114) | `[0,0,0]`; raw HTML also `[0,0,0]` | reproduces |
| item 6 unspaced string 0 times | unspaced `count=0`; spaced 1 at 1707; `明确说明每一项来源` once (1707) | reproduces |
| author "only inside that file name" | `郑卿勇` count=3 (2740/4929/4981), all inside `fileName=…pdf`; `author=` empty (2897) | reproduces (3, not 1) |
| "no original URL" | `originalUrl=,`/`linkOutUrl=,` each 1 and empty; only `http` is an image URL at 2996; `doi`=0 | reproduces |
| "attachment's text is not in the capture" | `%PDF`/`stream`/`FlateDecode`=0; `检索式`=0, `检索策略`=0; `条目` only 2392/3499; `全文` only app prompt 7064 | reproduces |
| item text not read | `print([t.count(w) for w in ('CNKI','中国知网','万方','维普','SinoMed')])` → `[0, 0, 0, 0, 0]` | reproduces |
| `检索者`/`检索人员` 0 each `.txt` | S113 `[0, 0]`; S114 `[0, 0]` | reproduces |
| `paymentAmount=10`, no price/purchase step | `paymentAmount` at 4178; `价格/购买/售价/付费/定价/费用/支付/免费`=0 (`下载`=6) | reproduces |
| page's `16` only 16a/16b | `16` count=2 at 3496 (`16a`), 3597 (`16b`) | reproduces |
| SinoMed cuts off at `并针对中文` | `42bac883…txt` len 1675: `并针对中文` off 1024 count 1; `并针对中文数据库`=0 | reproduces |
| Chinese-databases clause only in S113 | S113 count=2 (2477 plain, 3596 `&ldquo;`); SinoMed 0 | reproduces |
| "same split" as Japanese entry | `japanese-prisma-item-wording-r40.md:13,20`: item 7 lacks organisations/reference lists | reproduces |

## 4. Widened negatives — five synonyms each in Chinese

- Databases (S113): `知网 0, 万方数据 0, 维普网 0, 中国生物医学文献数据库 0, 中国生物医学文献服务系统 0`;
  `PubMed/Embase/Cochrane/CINAHL/Scopus` all 0. **Wording holds**, beyond Chinese names too.
- Searcher (each `.txt`): `文献检索员 0, 信息专员 0, 图书馆员 0, 检索专家 0, 检索负责人 0`. **Holds.**
  (S114's four `作者` hits are nav items and item 26 "声明作者的任何利益冲突"; `编译/整理/审校/校对`=0.)
- Translator (S114): `中文版 0, 汉化 0, 本地化 0, 中文化 0, 简体中文版 0` (plus implied `译本/译者/译校 0`,
  since `译`=0). **Holds**, and at document level (raw HTML 0).

## 5. Differs

- **D1 — "names the article only as an attachment" (Obs 5) is contradicted.** The record object at 2752
  carries `title=系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读` (2812), `guiderFrom=中国循证医学杂志`,
  `summary=本文旨在为国内学者…国际化。`; the page also prints `中文标题：` (2171) and the headline (1998).
  Both numbers: 1 naming form claimed vs 3+ naming fields observed.
- **D2 — `verified-at` "every quoted phrase … (count 1 each)" is false for two quoted phrases.**
  `并针对中文数据库等本土化应用挑战提出实践建议。` count=2 (2477, 3596);
  `系统评价_…解读_郑卿勇.pdf` count=3 (2740, 4929, 4981). Both numbers: claimed 1 each, observed 2 and 3.
  No `char N` is affected (§2).

## 6. Cross-file checks behind the inferences

SinoMed capture 1024 truncates mid-clause (`并针对中文`) and ends there — the entry's claim ✓; the same
abstract opens identically in S113 (`文献检索是系统评价（SR）的基石…`), which is why the 简要介绍 block
may be called the abstract. `简要介绍` label exists once at 2264; the quoted block begins *after* it, and
the block's own first sentence (`文献检索是系统评价（SR）的基石…可重复性。`) is not quoted — a wording
nuance, not a count error.

## 7. `tools/inference-ground.py` — command reproduces, polarity blind here

```
python3 tools/inference-ground.py --entry corpus/knowledge/chinese-prisma-s-reception-r52.md \
  --spans corpus/evidence/round52/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root .
GROUND entry=corpus/knowledge/chinese-prisma-s-reception-r52.md section=1 bullets=4 tokens=8 grounded=8
GROUND: PASS        exit=0
```
Mutations in scratch copies: (1) bullet 1 → `item 6 does not ask "明确说明每一项来源 的 检索或查询日期"`
(semantic reversal, negator inside P2's window) — **not caught**, `grounded=8 PASS`; (2) bullet 4 →
`**The portal record does not carry the abstract's last clause.**` with its quote retained — **not caught**,
`PASS`. Mechanism (verified by import): `tools/inference-ground.py:253` `WORDS_RE =
re.compile(r"[a-z][a-z'\u2019]*")` → `words(<CJK token>)=[]`, `content()=[]`, so `phrase_polarity()`
returns `(False, [])` and `:340 if not stems: return []` makes every CJK-quoted phrase polarity-inert.
Mutation 2 sits outside the lexical design (the quote is stripped from the bullet's unquoted words before
P2). So the C2 leg "all three entries exit 0 under inference-ground" is measured but carries no entailment
evidence for this entry's CJK quotes — a limit of the leg, not a counter failure.

Entailment ceilings (not counter failures): "carries the abstract **in full**" — the visible block ends
cleanly at `…国际化。`, but the `content=` field's copy of the same abstract (3229, `ChDivSummary`) is
truncated with `…` after `期刊编辑`, so completeness against the publisher's article is not verifiable
from the capture; and Inf 1's `as PRISMA 2020's English item does` has no captured English item text.

## 8. Files, receipts, risks

Files changed: this report only. No production file, tool, counter, span or lane file written; no git/jj
mutation; no install. Receipts embedded above. Residual risk: D1/D2 are wording defects the C2 counter
cannot see (it measures binding/presence), and the inference-ground PASS does not test CJK entailment.

VERDICT — attacked the 15 located offsets, 13 negative statements, the recheck command and the
inference-ground pass of `chinese-prisma-s-reception-r52.md`: offsets (15/15), negatives and recheck
(STALE=0) reproduce and five-synonym widenings still hold, but "names the article only as an attachment"
is contradicted by the record's `title=`/`summary=`/`中文标题：`, `verified-at`'s "count 1 each" differs
for two quoted phrases (2 and 3), and inference-ground passes both a negated-window and a
negated-conclusion mutation because CJK tokens yield an empty polarity scope.
