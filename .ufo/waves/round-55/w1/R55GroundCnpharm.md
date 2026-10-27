# R55GroundCnpharm — S131 → S125 grounding

**Scope:** Grounded the staged China Food and Drug News report against its prescribed defined text form. No lane product file, registry, manifest, lesson, scorecard, git index, or campaign file was changed. No tools installed.

## Provenance and observed checks

- Staged source mapping: `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/grey-literature-and-chinese-search-record-r40.md`, lines 4–5: staged `S131` is `http://m.cnpharm.com/201906/18/c280684.html`; its stated capture scope is “the report body”; publication is 中国食品药品网 / 《中国医药报》, 2019-06-18. Lines 25–29 use S131 for issuer, five parts, Cochrane process, and whole-process quality control. The supplied report itself is an issuance report, not the guideline text.
- Opened defined form: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/27d4865f201e99c1fed9f79b.txt`, decoded UTF-8 with universal newlines. The paired `.raw` is HTML, not OLE. Observed: `CR 185 LF 259`; normalized form is 1,673 characters. SHA-256 of the `.txt` bytes: `cd65aa9e26b41d8a0f7a260a7dfacf4cbf0b3fc59ab9dbef7bd7ab6ba1a98626`.
- Quote-check command (using `form=open(path,'r',encoding='utf-8').read()` and each literal below): `form.count(q)`, `form.find(q)`, `len(q)`, `len(q.split())`, ` '\n' not in q`, and `form[offset:offset+len(q)] == q`. Observed, for each quote below: count `1`, exact indicated offset, one line, length ≤160, whitespace words ≤25, slice equality `True`.
- Sweep command: `python3 - <<'PY'` opening the defined `.txt` as UTF-8 and printing `form.count(term)` for `灰色文献`, `检索`, `试行`, `国家药品监督管理局`. Observed: `灰色文献 0`; `检索 0`; `试行 3`; `国家药品监督管理局 3`.
- Additional form counts: `2019-06-18 count 1`; `6月18日 count 1`; `参考文献 1`; `参考依据 0`; `概述 1`; `方法学要点 3`; `报告撰写规范 3`; `附录 1`; `质量控制 2`; `Cochrane 1`.
- Lane source registry format inspected at `corpus/SOURCES.md` lines 7–10: Registry columns are `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`; sample rows use `mined` and `used-by` entry paths. Round-55 counter source inspected at `corpus/evidence/round55/c2-count.py` lines 110–127, 154–175, 200–211: it checks the document URL, citation, and quote containment in span/entry/lesson and verifies offset-derived quote positions. This report supplies evidence only; no counter was run.

## Grounded machine quotes

```text
QUOTE	S125	http://m.cnpharm.com/201906/18/c280684.html	作者：郭婷 2019-06-18 来源：中国健康传媒集团-中国食品药品网	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S125	http://m.cnpharm.com/201906/18/c280684.html	中国食品药品网讯（记者 郭婷） 6月18日，国家药品监督管理局发布通告	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S125	http://m.cnpharm.com/201906/18/c280684.html	6月18日，国家药品监督管理局发布通告，发布《上市药品临床安全性文献评价指导原则（试行）》	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S125	http://m.cnpharm.com/201906/18/c280684.html	指导原则分为概述、方法学要点、报告撰写规范、指导原则所依据的参考文献和附录五个方面	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S125	http://m.cnpharm.com/201906/18/c280684.html	方法学要点包括一般流程、安全性文献评价注意事项、质量控制注意事项	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S125	http://m.cnpharm.com/201906/18/c280684.html	引进了Cochrane系统评价规范化操作流程和全程质量控制的方法	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
```

Offsets in defined form respectively: `242`, `355`, `371`, `780`, `825`, `951` (`form.find(quote)`). The five-part wording is exactly `概述、方法学要点、报告撰写规范、指导原则所依据的参考文献和附录`; this page uses `参考文献`, not `参考依据`.

## Finding and limits

The page supports that the 中国食品药品网 report states NMPA issued the named provisional guideline on 6月18日, with byline metadata dated 2019-06-18, describes its five-part organization, and reports its Cochrane procedure and whole-process quality control. This is a newspaper report of issuance; it does **not** establish the exact text or operative requirements of the guideline. In particular, the page does not itself contain `灰色文献` or `检索`, so it cannot independently ground the entry's grey-literature search-record requirement; the staged entry assigns that requirement to S130 (line 18 and lines 19–24). The date appears once in each printed form (`2019-06-18`, `6月18日`).

**Out of scope:** C1/C2/C3 scoring, S124/S126, registry/entry/lesson edits, and adjudication of other W1 findings.

**Artifact:** `.ufo/waves/round-55/w1/R55GroundCnpharm.md`.

**VERDICT: Grounded S131→S125 issuance-report claims with six unique exact-form quotes; the report does not prove the guideline’s text or grey-literature requirement.**