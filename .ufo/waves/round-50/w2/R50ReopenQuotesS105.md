# R50 w2 — Re-open quotes of row S105 (CNKI 管理员 manual)

Seat: `R50ReopenQuotesS105`. Scope: 34 S105 quote rows in `corpus/evidence/round50/quotes.tsv` (lines 20–53) against capture `…/.qcache/e3ca8f4fdd15420b80096a75.txt` (UTF-8, 38,174 chars, 83,384 bytes).

No tool installs (none required; RULES.md read, no pacman use). No scratch created under `/dev/shm`; only reads from the lane and capture; the only write is this report.

## 1. Per-row verification (python, observed output)

Command (condensed from the runs below, one table for all 34 rows):

```python
import csv, os
base="corpus/evidence/round50"; cap="…/e3ca8f4fdd15420b80096a75.txt"
text=open(cap,encoding="utf-8").read()
spans=[r for r in csv.DictReader(open(base+"/spans.tsv",encoding="utf-8"),delimiter="\t") if r["id"]=="S105"]
for r in sorted(spans,key=lambda r:int(r["offset"])):
    off=int(r["offset"]); q=r["quote"].strip()
    s=open(os.path.join(base,r["span_file"]),encoding="utf-8").read()
    print(r["span_file"],off,text.find(q),text.count(q),len(q),len(q.split()),
          q in s, text[off:off+len(s)]==s, q in open(r["entry"],encoding="utf-8").read())
```

| span_file | offset col | text.find | cnt | qlen | words | in span | slice==capt[off:off+len] | in entry |
|---|---|---:|---:|---:|---:|---|---|---|
| S105-1.txt | 0 | 48 | 1 | 15 | 4 | True | True | True |
| S105-14.txt | 0 | 48 | 1 | 15 | 4 | True | True | True |
| S105-2.txt | 27507 | 27587 | 1 | 33 | 1 | True | True | True |
| S105-3.txt | 30581 | 30661 | 1 | 10 | 4 | True | True | True |
| S105-15.txt | 30581 | 30661 | 1 | 10 | 4 | True | True | True |
| S105-4.txt | 30658 | 30738 | 1 | 25 | 1 | True | True | True |
| S105-5.txt | 30665 | 30745 | 1 | 18 | 1 | True | True | True |
| S105-16.txt | 30665 | 30745 | 1 | 18 | 1 | True | True | True |
| S105-6.txt | 30698 | 30778 | 1 | 11 | 1 | True | True | True |
| S105-17.txt | 30698 | 30778 | 1 | 11 | 1 | True | True | True |
| S105-18.txt | 30698 | 30778 | 1 | 12 | 1 | True | True | True |
| S105-7.txt | 30713 | 30793 | 1 | 23 | 1 | True | True | True |
| S105-19.txt | 30720 | 30800 | 1 | 26 | 1 | True | True | True |
| S105-20.txt | 30764 | 30844 | 1 | 29 | 1 | True | True | True |
| S105-21.txt | 30798 | 30878 | 1 | 16 | 1 | True | True | True |
| S105-22.txt | 30799 | 30879 | 1 | 15 | 1 | True | True | True |
| S105-8.txt | 30800 | 30880 | 1 | 13 | 1 | True | True | True |
| S105-23.txt | 30800 | 30880 | 1 | 13 | 1 | True | True | True |
| S105-24.txt | 30855 | 30935 | 1 | 9 | 1 | True | True | True |
| S105-9.txt | 30867 | 30947 | 1 | 9 | 1 | True | True | True |
| S105-10.txt | 30867 | 30947 | 1 | 33 | 1 | True | True | True |
| S105-25.txt | 30867 | 30947 | 1 | 9 | 1 | True | True | True |
| S105-26.txt | 30983 | 31063 | 1 | 9 | 1 | True | True | True |
| S105-27.txt | 30999 | 31079 | 1 | 19 | 1 | True | True | True |
| S105-11.txt | 31021 | 31101 | 1 | 19 | 1 | True | True | True |
| S105-28.txt | 31021 | 31101 | 1 | 19 | 1 | True | True | True |
| S105-29.txt | 31057 | 31137 | 1 | 25 | 1 | True | True | True |
| S105-30.txt | 31089 | 31169 | 1 | 10 | 1 | True | True | True |
| S105-31.txt | 31126 | 31206 | 1 | 20 | 1 | True | True | True |
| S105-32.txt | 31129 | 31209 | 1 | 17 | 1 | True | True | True |
| S105-12.txt | 31138 | 31218 | 1 | 7 | 1 | True | True | True |
| S105-33.txt | 31138 | 31218 | 1 | 7 | 1 | True | True | True |
| S105-34.txt | 31153 | 31233 | 1 | 27 | 1 | True | True | True |
| S105-13.txt | 31193 | 31273 | 1 | 17 | 1 | True | True | True |

Observed summary lines: `ALL OK: True`; `checked 34 spans; mismatches: []`; `quotes not in lesson: []`; `spans not longer than quote: []`. Capture identity: `sha256(url)[:24] = e3ca8f4fdd15420b80096a75`; content `sha256 = 2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e`, which equals the sole `capture_sha256` recorded on all 34 S105 span rows.

Result: all 34 quotes occur exactly once in the capture; `text.find` offsets above match the anchor `char N` values in both entries' `source:` lines (r41: 48, 30738, 30778, 30793, 30880, 30947, 31101, 31218, 31273; r40: 48, 30745, 30800, 31063, 31101, 31137, 31233); each span file is exactly `text[offset:offset+len(span)]` at the recorded offset; each quote is inside its span file, inside its citing entry, and inside `corpus/lessons/round-50.md`; every quote ≤ 25 whitespace words and ≤ 160 characters (max 33 chars, 4 words); every span longer than its quote.

## 2. Redundant rows and distinct offsets

9 redundant pairs (quote A is a substring of quote B, same id S105):

- `各项内容都相同` ⊂ `相同，鼠标放上去也会提示各项内容都相同。` and ⊂ `鼠标放上去也会提示各项内容都相同。` (spans 12/33 vs 31 vs 32)
- `第一类是“没找到”` ⊂ `第一类是“没找到”，表示经过核对，没有找到与输入的这条引文一一对应` (spans 9/25 vs 10)
- `以核对引文内容的正确性` ⊂ `以核对引文内容的正确性。` (spans 6/17 vs 18)
- `状态、篇名、作者和文献来源` ⊂ `有状态、篇名、作者和文献来源。` ⊂ `容有状态、篇名、作者和文献来源。` (spans 8/23 vs 22 vs 21)
- `鼠标放上去也会提示各项内容都相同。` ⊂ `相同，鼠标放上去也会提示各项内容都相同。` (span 32 vs 31)
- `以“中国知网”的文献资源为核对源内容` ⊂ `引文核对是指，以“中国知网”的文献资源为核对源内容` (spans 5/16 vs 4)

Distinct start offsets for S105: **24** (0, 27507, 30581, 30658, 30665, 30698, 30713, 30720, 30764, 30798, 30799, 30800, 30855, 30867, 30983, 30999, 31021, 31057, 31089, 31126, 31129, 31138, 31153, 31193). Offsets shared by >1 row (same quote text used in both entries, or a shorter quote nesting in a longer one): 0, 30581, 30665, 30698 (×3), 30800, 30867 (×3), 31021, 31138. The redundancy is benign (shorter quote is a true prefix of the longer one; spans differ only by the added chars) — no contradictory rows.

## 3. Five weightiest quotes vs the Inference bullets

1. `但是引文中有某一部分的信息与源内容不同` (find 31101, spans 11/28) — **supports** cnki-r40 Inference bullet 1 ("The second state is a diff, not a verdict"): verbatim the state names a part that differs from the source, i.e. the checker reports *which* part misses; the "record was found" premise is carried by sibling quotes, but the diff reading itself is exactly what the quote states.
2. `以“中国知网”的文献资源为核对源内容` (find 30745, spans 5/16) — **supports** cnki-r40 Inference bullet 4 ("The check is against a named pool, as this copy states it"): the quote fixes the comparison source to CNKI's own literature resources; the "closed corpus" part is a sweep, but the claim's "as this copy states it" qualifier stays inside the quote.
3. `第一类是“没找到”` (find 30947, spans 9/25) — **supports** cnki-r40 Inference bullet 2 ("The three states keep a coverage outcome apart from a support outcome"): verbatim the first state is nothing-matched, which is the coverage-vs-support separation the bullet draws; the middle-state-only wording comes from sibling quotes, the first-state claim is fully carried here.
4. `列表中的“篇名”可以点击，链接到该引用文献的详细信息。` (find 31233, span 34) — **supports** cnki-r40 Inference bullet 3 ("The result row carries the matched work, not only the verdict"): the quote states the title cell links to the cited work's detail record, so the row carries the matched work, not just a verdict.
5. `以核对引文内容的正确性` (find 30778, spans 6/17) — **supports less than claimed** for citation-matching-r41 Inference bullet 2 ("The staged claim … is narrowed to: undocumented"): the quote shows the copy's own verb is 比对 (comparison), but "no matching method is stated" rests on the §6.1 slice sweeps (算法 0, 相似度 0), which this quote alone does not establish.

No quote fails to support its bullet's core assertion; the only under-support is #5, and the bullet itself already hedges ("Absence of a method description cannot establish absence…"), so the bullet's worded claim stays fair.

## VERDICT

Attacked the 34 S105 quote rows of the landed C2 bytes (capture `e3ca8f4fdd15420b80096a75.txt`): **survived** — every quote occurs exactly once, its `text.find` offset matches the span-file `text[offset:offset+len(span)]` slice at the recorded offset, stays ≤25 words/≤160 chars, sits inside its span, citing entry and lesson; 9 substring-redundant rows exist (all benign prefixes), 24 distinct start offsets; all five weightiest quotes support their Inference bullets as worded (one supports-less-than-claimed, already hedged by the bullet) — no defect found.

## Addendum — peer query on spans.tsv offsets

Sibling seat `R50ReopenRowS105` flagged that spans.tsv records S105 quotes at offsets −80/−48 from `text.find(quote)` (e.g. 创建文件夹… 27507 vs 27587). Explained and closed: the spans.tsv `offset` column is the SPAN BLOCK's start, not the quote's; spans include context lines before the quote (the edition-line span starts at 0, its quote at 48). Re-ran the verification over **all 55** span rows (S104/S105/S106, each capture keyed `sha256(url)[:24]`): span-content `text.find` equals the recorded offset and `text[offset:offset+len(span)] == span` for **0 mismatches**, and every quote occurs exactly once. None of the spans.tsv offsets are shifted against the committed captures; the `char N` anchors (quote offsets) in SOURCES.md/entries and the spans.tsv offsets measure different things and are both correct.
