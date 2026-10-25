# R51ExecNegSweep — negative-claim sweep over the seven staged captures

seat: `R51ExecNegSweep` (executor, leaf) · wave: round-51 / w1 · date: 2026-10-25
scope: one table — 7 captures × 14 terms — an independent-tool confirmation, and a verdict on the
three staged negative claims. Read-only on `/home/vgpnk/Projects/shokuknow`; this file is the only
write. No tool installed (pacman paused; nothing needed): `pdftotext` 26.08.0, `pdftohtml`, `unzip`, `python3`.

Keys under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`: S109
`7194acc65a18f6555e4b8893`, S110 `62be15a474e866e4bef6c9d5`, S116 `fd468a36d78ff156b6200946`, S117
`c7266931a1731db3ff6ae77d`, S119 `42bac8830527d6f1bb125c49`, S125 `3a8b45977cd111e45e3980a5`, S126
`34fcefc159bf2ebbd1e09540`. Each `.txt` read AS UTF-8 (strict decode attempted; the replaced decode
is what the counts then use). Counts are exact `str.count`; offsets are `str.find` (`-1` = absent).
"CJK" = `[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]`.

Commands: `python3 /dev/shm/chousa-r51-R51ExecNegSweep/sweep.py` (script below; A–D verbatim);
`sha256sum` on each `.txt` and on the `pdftotext -layout` rendering; `pdftotext` (no flag) and
`pdftohtml -xml -i -stdout` re-counts; `unzip -p …raw word/document.xml`; `grep -l` over 2549 `.txt` files.

```python
#!/usr/bin/env python3
"""R51 negative-claim sweep over the seven staged captures."""
import hashlib, os, re, subprocess
Q = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
OUT = "/dev/shm/chousa-r51-R51ExecNegSweep"
CAP = [("S109", "7194acc65a18f6555e4b8893"), ("S110", "62be15a474e866e4bef6c9d5"),
       ("S116", "fd468a36d78ff156b6200946"), ("S117", "c7266931a1731db3ff6ae77d"),
       ("S119", "42bac8830527d6f1bb125c49"), ("S125", "3a8b45977cd111e45e3980a5"),
       ("S126", "34fcefc159bf2ebbd1e09540")]
TERMS = ["検索者", "检索者", "检索人员", "検索式", "检索策略", "検索期間", "検索日", "检索时间",
         "灰色文献", "ハンドサーチ", "手工检索", "PRISMA-S", "ネットワーク", "追跡"]
CJK = re.compile("[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

def textform(h):
    b = open(os.path.join(Q, h + ".txt"), "rb").read()
    try:
        t, state = b.decode("utf-8"), "strict-ok"
    except UnicodeDecodeError as e:
        t, state = b.decode("utf-8", "replace"), "strict-FAIL(%s@%d)" % (e.reason, e.start)
    return t, state, hashlib.sha256(b).hexdigest()

def indep(h):                       # an independent rendering of the same document
    pdf = os.path.join(Q, h + ".pdf")
    if os.path.exists(pdf):
        p = os.path.join(OUT, h + ".pdftotext.txt")
        subprocess.run(["pdftotext", "-layout", pdf, p], check=True)
        return "pdftotext -layout " + h + ".pdf", open(p, encoding="utf-8").read()
    raw = open(os.path.join(Q, h + ".raw"), "rb").read()
    if raw[:2] == b"PK":            # S125 .docx
        x = subprocess.run(["unzip", "-p", os.path.join(Q, h + ".raw"), "word/document.xml"],
                           check=True, capture_output=True).stdout.decode("utf-8")
        return "unzip -p " + h + ".raw word/document.xml (tags stripped)", re.sub(r"<[^>]+>", "", x)
    return h + ".raw decoded UTF-8 (HTML)", raw.decode("utf-8", "replace")

print("== A: .txt read as UTF-8 — count/first offset"); print("capture\t" + "\t".join(TERMS))
for sid, h in CAP:
    t, state, dig = textform(h)
    print(sid + "\t" + "\t".join("%d/%d" % (t.count(w), t.find(w)) for w in TERMS))
print("\n== B: .txt shape"); print("capture\thex\tchars\tcjk\tu+fffd\tdecode\tsha256")
for sid, h in CAP:
    t, state, dig = textform(h)
    print("%s\t%s\t%d\t%d\t%d\t%s\t%s" % (sid, h, len(t), len(CJK.findall(t)),
                                          t.count("\ufffd"), state, dig))
print("\n== C: independent tool — counts"); print("capture\ttool\t" + "\t".join(TERMS))
for sid, h in CAP:
    label, it = indep(h)
    print("%s\t%s\t%s" % (sid, label, "\t".join(str(it.count(w)) for w in TERMS)))
print("\n== D: independent form shape")
for sid, h in CAP:
    label, it = indep(h)
    print("%s\t%s\tchars=%d\tcjk=%d\tu+fffd=%d" % (sid, label, len(it),
                                                   len(CJK.findall(it)), it.count("\ufffd")))
```

## A — term counts and first offsets in the `.txt` (exact `str.count` / `str.find`)

```
capture	検索者	检索者	检索人员	検索式	检索策略	検索期間	検索日	检索时间	灰色文献	ハンドサーチ	手工检索	PRISMA-S	ネットワーク	追跡
S109	0/-1	0/-1	0/-1	8/533	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	1/18441	0/-1	0/-1
S110	3/4409	0/-1	0/-1	3/4419	0/-1	0/-1	0/-1	0/-1	0/-1	3/4211	0/-1	0/-1	0/-1	0/-1
S116	0/-1	0/-1	0/-1	0/-1	8/13422	0/-1	0/-1	1/15189	3/15310	0/-1	1/29955	0/-1	0/-1	0/-1
S117	0/-1	0/-1	0/-1	0/-1	2/11428	0/-1	0/-1	1/11334	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1
S119	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	6/50	0/-1	0/-1
S125	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1	0/-1
S126	0/-1	0/-1	0/-1	11/6436	0/-1	2/10146	0/-1	0/-1	0/-1	0/-1	0/-1	2/12615	0/-1	0/-1
```

## B — `.txt` shape (chars / CJK / U+FFFD / decode / sha256)

```
S109	7194acc65a18f6555e4b8893	21216	7318	0	strict-ok	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f
S110	62be15a474e866e4bef6c9d5	39676	9973	0	strict-ok	960da5cf632dbd278ea941c54d83e3ed8f13657bcb4bcbbfc8d63c9d834acf4a
S116	fd468a36d78ff156b6200946	52208	13880	0	strict-ok	90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc
S117	c7266931a1731db3ff6ae77d	50952	8402	0	strict-ok	03342b7ded4f9d687a5319a739cf357e4fa37d96de20ce66cba6cc7f5adfe2dd
S119	42bac8830527d6f1bb125c49	2065	427	0	strict-ok	4d3bff5067b4cf8e81980618696fdd28c4457f6e64d361b1164b60625c937671
S125	3a8b45977cd111e45e3980a5	168953	320	72117	strict-ok	471e558969d4ec3d7f795c4b499be79aa31c6fb1f16f3065563a3d0025ba85ea
S126	34fcefc159bf2ebbd1e09540	25811	9767	40	strict-ok	065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b
```

## C/D — independent tool, same terms, and that form's shape

```
capture	tool	検索者	检索者	检索人员	検索式	检索策略	検索期間	検索日	检索时间	灰色文献	ハンドサーチ	手工检索	PRISMA-S	ネットワーク	追跡
S109	pdftotext -layout 7194acc65a18f6555e4b8893.pdf	0	0	0	8	0	0	0	0	0	0	0	1	0	0
S110	pdftotext -layout 62be15a474e866e4bef6c9d5.pdf	3	0	0	3	0	0	0	0	0	3	0	0	0	0
S116	pdftotext -layout fd468a36d78ff156b6200946.pdf	0	0	0	0	8	0	0	1	3	0	1	0	0	0
S117	pdftotext -layout c7266931a1731db3ff6ae77d.pdf	0	0	0	0	2	0	0	1	0	0	0	0	0	0
S119	42bac8830527d6f1bb125c49.raw decoded UTF-8 (HTML)	0	0	0	0	0	0	0	0	0	0	0	12	0	0
S125	unzip -p 3a8b45977cd111e45e3980a5.raw word/document.xml (tags stripped)	0	0	0	1	0	2	0	0	0	1	0	0	7	0
S126	pdftotext -layout 34fcefc159bf2ebbd1e09540.pdf	0	0	0	11	0	2	0	0	0	0	0	2	0	0
```
```
S109	pdftotext -layout 7194acc65a18f6555e4b8893.pdf	chars=21216	cjk=7318	u+fffd=0
S110	pdftotext -layout 62be15a474e866e4bef6c9d5.pdf	chars=39676	cjk=9973	u+fffd=0
S116	pdftotext -layout fd468a36d78ff156b6200946.pdf	chars=52208	cjk=13880	u+fffd=0
S117	pdftotext -layout c7266931a1731db3ff6ae77d.pdf	chars=50952	cjk=8402	u+fffd=0
S119	42bac8830527d6f1bb125c49.raw decoded UTF-8 (HTML)	chars=17996	cjk=1013	u+fffd=0
S125	unzip -p 3a8b45977cd111e45e3980a5.raw word/document.xml (tags stripped)	chars=20592	cjk=13770	u+fffd=0
S126	pdftotext -layout 34fcefc159bf2ebbd1e09540.pdf	chars=25811	cjk=9767	u+fffd=40
```

Two more poppler modes — `pdftotext` (reading order, no `-layout`) and `pdftohtml -xml -i -stdout` —
reproduce table C term for term on all five PDFs. **The confirmation is cross-mode, not
cross-library**: each `.txt` is byte-identical to the `pdftotext -layout` rendering of its own `.pdf`
(sha256 prefixes `05c7ee9fe9e55461`, `960da5cf632dbd27`, `90f2f54cef21cb49`, `03342b7ded4f9d68`,
`065b889a97b00f88` — all five `IDENTICAL`), so the cache `.txt` was produced by that very command.

## Findings

1. **S125 has no usable text form anywhere in the cache.** Its `.txt` decodes strictly as UTF-8 but is
   the `.docx` bytes through a replacement pipeline: 319599 B → 168953 chars, **72117 U+FFFD**,
   `head = 'PK\x03\x04\x14\x00\x06\x00'`, `unzip -l …txt` → `zipfile corrupt` (the `.raw` lists
   `word/document.xml`, 1464476 B). All 14 terms are `0/-1` in the `.txt`; the docx has 検索期間 2,
   ハンドサーチ 1, 検索式 1, ネットワーク 7. `grep -l "文献検索期間について明記" *.txt` over all
   **2549** `.txt` files returns **nothing** (control: S126's `検索の開始日と終了日を記載` grep returns
   `34fcefc159bf2ebbd1e09540.txt`, rc=0), so the S125 quotes exist only behind `unzip -p …raw word/document.xml`.
2. **S119's order route lives in the `.raw`, not the `.txt`** (2065 vs 17996 chars; `PRISMA-S` 6 vs
   12). The `.raw` carries `<!-- 原文索取的FORM -->` and
   `action="http://doc.sinomed.ac.cn/inter/JspShopCartService.jsp"` (form `frmMall`,
   `APPLICATION=JAVA_TRSCDS`); the `.txt` strips all form markup. Its abstract ends mid-sentence at
   `并针对中文` (1024) and the page's only gate text is `请登录后再使用此功能， 登录 。`
3. **`学科分类号` sits inside an HTML comment** in S119: `<!-- … -->` spans `.raw` chars 9192–9908
   and holds 学科分类号 (`R-05;R-37;R348.3;R916.3`), the 主题词 row and the 基金 rows; `学科分类号`
   and `R-05` are **0** in the `.txt`, where `主题词` survives only as the link text
   `查看主题词相同的文献` — yet the r39 source line names 学科分类号 as a field of this record.
4. **S126 lost 40 glyphs to the PDF text layer**: one contiguous U+FFFD run at chars 101–140, right
   after `〈鍵概念〉`; `pdftotext` on the `.pdf` shows the same 40, so it is the PDF, not the `.txt`.
   The S126 quote offset below (11294) sits 11k chars away from the damage.
5. **`ネットワーク` is a false friend**: all 7 docx hits are `間接比較やネットワークメタアナリシス` /
   `ネットワークメタアナリシス` — network meta-analysis, never a network/website source. `追跡` is 0
   in all seven captures in every form, so no capture here asks for citation tracking.
6. **`検索日` is 0 everywhere, yet S110 requires the date**: the field is worded
   `それぞれのデータベース毎に最後に検索した日の日付を記載する` (count 2, offset 4137). A
   literal-term sweep under-detects the Japanese date requirement; `检索时间` (S116/S117) does hit.
7. **Column interleave splits runs in the two 实验动物与比较医学 PDFs.** In S116 `由于目前尚无` is
   0 because `由于目` ends a left-column line; the contiguous survivor starts at `尚无…` (17709). In
   S117 the date+strategy run is contiguous only from `从各数据库建立至 2024 年 4 月 1 日。检索策略
   结合主` (11404). `2024-04-01` and `2024年4月1日` are both 0 — the text is `2024 年 4 月 1 日`.

## The three staged negative claims

**N1 "neither names the searcher" — REPRODUCES on both pairs, robust to term choice.** `检索者` and
`检索人员` are 0/0 in S116 and S117, and the module-3 field list is exhaustive without one:
`（1）检索数据库…（2）检索时间范围…检索词及逻辑关系…（3）灰色文献的检索与记录`. Seven further
Chinese variants are 0 in both files (`检索人`, `检索员`, `检索者姓名`, `姓名`, `执行检索`,
`负责检索`, `检索由`). On the Japanese pair `検索者` is 0 in the S125 docx text and 0 in S126, so the
amendment's "the searcher's identity appears in neither" holds. The contrast the entries draw is
real: S110 carries `検索者` 3× (`検索者は、原則、#8に記載する` at 5720) and S109 names the actor as
`誰が検索を行った` at 13721.

**N2 "the full text is order-only" — order-only REPRODUCES; "paid" does NOT.** The S119 capture is an
index record (title, English title, 13 authors, 来源出版物, keywords, a truncated abstract, subject
headings) with exactly one full-text route: a form posting to a shop-cart service. Absent from both
forms: `订购` 0, `付费` 0, `价格` 0, `全文` 0, `购物车` 0 — no price and no order vocabulary, only the
endpoint name `JspShopCartService.jsp`. So "served only through a paid ordering service" is
half-measured: "only through a request form" is in the bytes, "paid" is an inference from an endpoint
name. A `.txt`-only reader sees neither and would report "no full-text route", not "order-only".

**N3 "no Chinese reporting standard" — REPRODUCES only in the narrow, domain-scoped form.** S116
states it in its own words: `尚无专门针对动物实验 SR 的报告规范` (17709, once), followed by
`研究者可参考 PRISMA 框架`. That is an absence **for animal-experiment SR** — exactly r39's
Observation. It does **not** support the broader reading of r39's title ("China has no standard for
one yet"), and it does not say the Chinese literature declined to adopt PRISMA-S: the located
sentence points *to* PRISMA. `标准` (31) and `规范` (27) are ordinary words in S116, so no count-based
reading of "no standard" exists; only the located sentence is.

## Machine lines (located quotes; each occurs exactly once in the form named)

Form: `txt` = cache `.txt` read as UTF-8; `raw` = cache `.raw` decoded UTF-8; `docx` = `.raw` →
`unzip -p … word/document.xml`, tags stripped with `re.sub(r"<[^>]+>","")`, read as UTF-8 (no cache
file holds this string — finding 1).

```
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	誰が検索を行った	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	検索者、検索ワード、検索式	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	（1）检索数据库（如 PubMed、Embase 等，含动物实验特殊数据库）	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	（3）灰色文献的检索与记录	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S116	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290	尚无专门针对动物实验 SR 的报告规范	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S117	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237	从各数据库建立至 2024 年 4 月 1 日。检索策略结合主	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	原文索取的FORM	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S119	https://www.sinomed.ac.cn/article.do?ui=2026335073	action="http://doc.sinomed.ac.cn/inter/JspShopCartService.jsp"	corpus/knowledge/chinese-search-record-r39.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	SRにおける文献検索期間について明記する	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S125	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx	文献検索期間2015年1月から2018年10月まで	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
QUOTE	S126	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	検索の開始日と終了日を記載することで	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
```

Offsets in the named form (`text.find`; each verified `count == 1`, ≤160 chars, ≤25 whitespace
words): S109 txt 13721 · S110 txt 4409 · S116 txt 15113 / 15307 / 17709 · S117 txt 11404 · S119 raw
14691 / 14733 · S125 docx 9729 / 9893 · S126 txt 11294.

## Limits

Counts are existence, not entailment: 0 is not proof a field is absent, a hit not proof the document
requires it (finding 5 is the counter-example). PDF-mode confirmations share poppler; S119's (HTML)
and S125's (docx XML) are independent of the `.txt`; neither has a `.pdf`, so `pdftotext` was impossible.

VERDICT: Attacked the three staged negative claims with a 7×14 exact-term sweep plus three poppler
modes, the S119 HTML and the S125 docx XML — the searcher-absence claim reproduces on both pairs,
order-only reproduces but "paid" does not, the Chinese-standard absence reproduces only in its
domain-scoped form, and S125 is confirmed to have no text form in the cache at all (0/14 terms in a
corrupt-zip `.txt`, 72117 U+FFFD).
