# ReopenS100 — S100 (CNKI 他引频次 note, OLE .doc) re-opened and attacked

Seat: ReopenS100 (W2 FALSIFY, round 49). Lane checkout `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
tip `87e93353d046f2d7e4f0d2f5d3b87b7008a64ef0`; frozen claims `fe740e7`; code measured `4ce61fc`.
Capture: `shokuknow/.ufo/waves/corpus-expansion-1/.qcache/b539a80218080da56a75b624.{raw,txt}`.
No production file written; scratch `/dev/shm/chousa-r49-ReopenS100` (deleted at end). No install needed.

## 1. Every S100 row in `corpus/evidence/round49/spans.tsv` (3 rows) — holds

```
$ python3 verify_s100.py     # script body: for each S100 row: recompute key, pick form by FILE digest,
                             # compare text[off:off+len(span)].encode('utf-8') == span file bytes, count quote
S100 key=b539a80218080da56a75b624 form=raw/utf-16le digest_ok=True off=1296 spanlen_chars=105 spanbytes=295
   slice==span_bytes: True  slice_sha=d8cebaabba2d0c77 span_sha=d8cebaabba2d0c77
   quote_occ_in_form=1 quote_occ_in_span=1 quote_off=1296 lead=0 tail=80
   span_longer_than_quote=True span_cr=0 span_lf=0 span_nul=0
S100 key=b539a80218080da56a75b624 form=raw/utf-16le digest_ok=True off=1423 spanlen_chars=48 spanbytes=144
   slice==span_bytes: True  slice_sha=320ccd91f581e4b8 span_sha=320ccd91f581e4b8
   quote_occ_in_form=1 quote_occ_in_span=1 quote_off=1431 lead=8 tail=1
   span_longer_than_quote=True span_cr=0 span_lf=0 span_nul=0
S100 key=b539a80218080da56a75b624 form=raw/utf-16le digest_ok=True off=2781 spanlen_chars=128 spanbytes=357
   slice==span_bytes: True  slice_sha=df09faa118c2c1fc span_sha=df09faa118c2c1fc
   quote_occ_in_form=1 quote_occ_in_span=1 quote_off=2861 lead=80 tail=34
   span_longer_than_quote=True span_cr=0 span_lf=0 span_nul=1
```
Key/digest check, separately: `sha256(url)[:24] = b539a80218080da56a75b624`; `.raw` 801280 B
`sha256=46d1866ce9afd51682e7e77cdf62612876da22c9bdbc9e8e299090128cb378f6` = the row digest;
`.txt` 1406840 B `sha256=ce30e735…` (not the row digest). The `.txt` form is a garbled decode
(`head = '��ࡱ�>…'`, 762306 chars) and **carries none of the three quotes** (`occ=[]` for each), so the
`.raw` UTF-16LE form is the only form that can hold these rows: the row's form choice is forced, not preferred.
Frozen counter replay (read-only): `c2-count.py` → `CAPTURE_BOUND=28/28 … C2=PASS` (exit 0).

## 2. Registry row `corpus/SOURCES.md:110` — anchor holds, `teaches` holds, `scope` partly

Anchor cell `located quotes char 1296, char 1431, char 2861`: 3/3 are located quote starts, each quote
`occ=1` in the form, each inside its span (`lead=0, 8, 80`). They are quote offsets, not the spans.tsv
`offset` column (1296, 1423, 2781) — that convention is uniform across all eight bound rows:
`S096 [3599,3707,3752] … S103 [892,953,959,3175] match True`, and matches the counter's
`offset + span.find(quote)` derivation (`ANCHOR_BOUND=8/8`).

`teaches` — both clauses carried: `他引频次 is queried through 中国引文数据库` ← char 1296;
`a citation counts as a self-citation whenever the citing work shares any co-author` ← char 1431
(`对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引`). The
co-authorship-vs-authorship inference is a fair restatement.

`scope` — **one clause not carried**: "CNKI's own **definition of 他引频次**". The capture contains no
definitional sentence: `是指 []  定义 []  扣除 []  排除 []  不含 []  除自引 []  自引文献 []`, and all seven
`他引频次` hits (1284 title, 1300, 1473, 1692, 1732, 3019, 3150) are query/display instructions
(`他引频次具体查询方法如下`, `检索结果列表中可以看到他引频次`). The document's own title is
`中国知网他引频次查询方法说明` — a query-method note plus a self-citation boundary, not a definition.
"as CNKI states them" and "the document is CNKI's, hosted by a university" are carried (title +
`咨询中国知网高教分公司尚菲`; host `zcmu.edu.cn`).

## 3. Every entry sentence citing S100 (`corpus/knowledge/citation-count-semantics-r37.md`)

Entry quotes are verbatim: `entry_has True capture_occ 1 at 1296 / 1423 / 2861`.

| line | sentence | verdict |
|---|---|---|
| 15-17 | `The CNKI note says "中国知网他引频次的查询需要使用《中国引文数据库》。"` | supported (char 1296) |
| 17-19 | `under its self-citation heading, "关于自引的说明：…自引。"` | supported (char 1423; standalone paragraph, CRs at 1421-1422 and 1471-1472) |
| 19-20 | `a citation in which any co-author appears is counted as a self-citation` | supported, capture's `合作发文` qualifier dropped (effect identical) |
| 20-21 | `Its query steps add "被引频次为0的文献将不会显示": records cited zero times are not listed` | supported literally (char 2861, `注：` at 2859); **narrower**: the field is `被引频次` in 中国引文数据库 高级检索, and the capture never says a `他引频次` of 0 is hidden, while the sentence sits in a 他引频次 paragraph |
| 43-46 | `The CNKI copy counts as self-citation any reference sharing a co-author (…, S100)` | supported (char 1423) |
| 50-51 | `A displayed zero, or a missing row, in an index query is a display-conditioned result: S100 says 被引频次为0的文献将不会显示` | **partly**: "missing row" supported; "a displayed zero" not supported — this capture says the zero is *not* displayed, so it cannot illustrate a displayed zero |
| 69-71 | `whether 被引 counts records in 中国引文数据库 or across CNKI as a whole: S100 … states only that the query uses that database` | supported: `被引` occurs twice only (the zero note, `高被引文献`), `总被引 0`; no statement of the counted population |
| 73 | `whether the counted records in S100 or S102 apply its codes` | consistent (no factual claim; `文献标志码 0` hits in S100) |

## 4. Context consistency — no quote lifted against its context; two manifest-hygiene defects

- char 1296 sits in the intro under the title, followed by `为了配合此轮评估工作，大部分高校已经开通了试用…`
  → "The CNKI note" and the university-hosted framing are correct in context.
- char 1431 sits directly under the standalone heading `关于自引的说明：` and ends at the paragraph mark
  (1471) → the entry's "under its self-citation heading" is exact; nothing in the surrounding paragraphs
  qualifies the rule (`自引` occurs 2×: heading 1425 + rule 1468; no counter-rule elsewhere).
- char 2861 sits in the 高级检索 step: `成功登录《中国引文数据库》后，也可选择高级检索，通过 …“学科”、“篇名”、
  “作者”、“单位”、“出版时间”、“文献来源”等方式进行组合查询，注：被引频次为0的文献将不会显示。` — consistent
  with "query steps". But its manifest span (`2781-2909`) begins with **80 chars of Word OLE formatting
  junk**, 42/65 of the pre-quote span being non-CJK and one NUL: `'J开ň漀Ĩᘚ౨㼑䌀ᡊ䬀H伀J儀J开ň\x00ᘝ써…ⴀ“学科”…'`.
  The sentence's verb `通过` (1783) is separated from its field list (`“学科”` 2816) by **1031 chars of
  binary with no CR** — so the CR-clip rule cannot trim it and `SPAN_CONTEXT` (len>quote) cannot tell prose
  from OLE junk. The context had to be recovered by widening ~1 KB; the span alone is not human-checkable.
- Rows 1 and 2 are clean prose; only row 3 carries this. No quote is context-inverted.

## 5. Post-freeze span-builder change, judged on S100

```
$ python3 build-spans.py --check          → SPANS_ROWS=28 STALE=0  (exit 0)
$ # old = git show fe740e7:…/build-spans.py, new = tip; both built from the SAME quotes.tsv, nothing written
rows where old span contains CR: 7 ['spans/S100-1.txt','S100-2.txt','S100-3.txt','S101-1.txt','S101-2.txt','S101-4.txt','S101-5.txt']
rows changed by the repair: 7   (S100-1 185→105, S100-2 199→48, S100-3 174→128; 21 rows identical)
```
The repair touches exactly the 7 CR-bearing `.raw` rows and nothing else — reproducing the errata's
`CAPTURE_BOUND=21/28 → 28/28` figure exactly; the committed manifest is the current builder's output
(`STALE=0`), not a hand edit. The disclosed quote shortening is in `quotes.tsv` (`S100-2` body, `char 1431`),
and the entry still quotes the full paragraph verbatim. Cost: `S100-2`'s span shrinks to heading + quote
(48 chars, no trailing prose), so its "context" is now only the heading — exactness bought by context loss.

## Risks / blockers

- `scope` cell overstates ("definition of 他引频次"); `S100-3`'s span context is OLE binary; the inference's
  "displayed zero" half has no instance in this capture. None of these touch a frozen predicate, target or
  counter, and none changes `C2=PASS`.
- Blockers: none. No network, no live fetch, no lane write beyond this report.

VERDICT: S100 (CNKI 他引频次 note, OLE .doc) — partly — all three span rows, the capture key/digest/form and all three anchor `char` offsets hold exactly, and no quote is lifted against its context, but the registry `scope` cell's "definition of 他引频次" is not in the capture, the entry's "a displayed zero" inference has no instance (the capture suppresses zeros), and `S100-3`'s span context is 80 chars of OLE binary.
