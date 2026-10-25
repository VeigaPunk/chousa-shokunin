# Seat R50ReopenQuotesS106 — wave-2 falsify: re-open row S106 quotes

Skill: `skill://godspeed` read first. No tool installs needed or performed (rules read: /home/vgpnk/.omp/agent/RULES.md; pacman paused — nothing required). No scratch created (scratch dir `/dev/shm/chousa-r50-R50ReopenQuotesS106` does not exist).

## Targets
- Row S106 = CNKI 子账号 manual PDF, url `https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf`
- Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/28750bcdf5d36cd90a7709fb.txt` (UTF-8; 63869 bytes = 30937 chars — matches the entry's `recheck:` fingerprint `30937 0 0 0 0`)
- Manifest rows: `corpus/evidence/round50/quotes.tsv:54-56`, `corpus/evidence/round50/spans.tsv:54-56`; span files `spans/S106-1.txt`, `spans/S106-2.txt`, `spans/S106-3.txt`
- Citing entry: `corpus/knowledge/citation-matching-semantics-r41.md` (source line 4; obs lines 15-16; Inference bullets lines 23-24)

## Check program (python3)

```python
import csv, os
CAP='/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/28750bcdf5d36cd90a7709fb.txt'
LANE='/home/vgpnk/Projects/shokunin/chousa-shokunin'
C=open(CAP,encoding='utf-8').read(); E=open(LANE+'/corpus/knowledge/citation-matching-semantics-r41.md',encoding='utf-8').read()
def load(p): return list(csv.DictReader(open(p,encoding='utf-8'),delimiter='\t'))
q=list(filter(lambda r:r['id']=='S106', load(LANE+'/corpus/evidence/round50/quotes.tsv')))
s=list(filter(lambda r:r['id']=='S106', load(LANE+'/corpus/evidence/round50/spans.tsv')))
for rw,sp in zip(q,s):
    qv=rw['quote']; off=int(sp['offset']); sc=open(LANE+'/corpus/evidence/round50/'+sp['span_file'],encoding='utf-8').read()
    print(sp['span_file'],'count',C.count(qv),'find',C.find(qv),'span_off',off,'slice_eq',C[off:off+len(sc)]==sc,'words',len(qv.split()),'chars',len(qv),'in_entry',qv in E)
red=[(a,b) for a in [r['quote'] for r in q] for b in [r['quote'] for r in q] if a!=b and a in b]
print('substring_relations',red)
print('distinct_span_offsets',len(set(int(r['offset']) for r in s)),'distinct_find_offsets',len(set(C.find(r['quote']) for r in q)))
```

## Observed output

```
spans/S106-1.txt count 1 find 83 span_off 3 slice_eq True words 1 chars 24 in_entry True
spans/S106-2.txt count 1 find 22511 span_off 22431 slice_eq True words 1 chars 28 in_entry True
spans/S106-3.txt count 1 find 22549 span_off 22469 slice_eq True words 1 chars 24 in_entry True
substring_relations []
distinct_span_offsets 3 distinct_find_offsets 3
```

Context slices around find offsets (same run): Q1 `…\n       产品名称：“中国知网”大学生论文管理系统使用手册    共   65   页\n\n…`; Q2 `…除第一作者本人文献\n  在创建文件夹页面中第一个选项为“仅去除第一作者本人文献”，如果勾选\n…`; Q3 `…献”，如果勾选\n该选项，该文件夹下的所有检测文献在去除本人文献检测结果中，将去除相似文\n献列表中第一作者为本人的相似文献，所以完整检测结果和去除本人文献检测结…果的文字复制比不同。…`

## Findings

1. **Uniqueness**: all 3 quotes occur exactly once in the capture (count = 1). `text.find` offsets: 83, 22511, 22549.
2. **Span equality**: for each row `C[offset:offset+len(span_file)] == span_file` — True for all three (offsets 3, 22431, 22469 are span starts; verified exact including leading spaces and page marker `   第 34 页`).
3. **Size bounds**: each quote is 1 whitespace token and 24/28/24 chars — ≤25 words, ≤160 chars.
4. **Inside citing entry**: all three quotes appear in `citation-matching-semantics-r41.md` (in_entry True; Q1 at entry lines 15-16, Q2/Q3 at lines 15 and 23).
5. **Redundancy**: no quote is a substring of another same-id quote (no redundant rows).
6. **Distinct start offsets**: 3 (spans: {3, 22431, 22469}; find offsets: {83, 22511, 22549}).
7. **Observation (calibration)**: spans.tsv offset is the *span start*, 80 chars before each quote's find offset; the entry's `source:` char refs (83, 22511, 22549 — entry line 4) equal the find offsets exactly, so the entry's citations are exact against this capture. The 80-char lead is the span's leading context (e.g., page header `   第 34 页`), not a mis-location.

## Weight-bearing quotes vs Inference bullets

The id has only 3 quotes, so all 3 are evaluated (a "top 5" cannot be formed). Inference bullets: line 23 (bullet 3) uses Q2+Q3; line 24 (bullet 4) uses Q1.

- Q1 `产品名称：“中国知网”大学生论文管理系统使用手册` (find 83) → Inference bullet 4 "S106 documents a different product (`产品名称：…使用手册`)": **supports** — verbatim title block. The bullet's second clause "carries 辅助 0 times" rests on the recheck count (`30937 0 0 0 0`), not Q1; the quote is used only for the product claim, which it carries exactly.
- Q2 `在创建文件夹页面中第一个选项为“仅去除第一作者本人文献”` (find 22511) → Inference bullet 3 "S106 places the option on the folder page (`…仅去除第一作者本人文献`)": **supports** — verbatim. The same bullet's "documented as acting on a ratio" is carried by Q2+Q3 plus unquoted continuation (`…所以完整检测结果和去除本人文献检测结果的文字复制比不同。`); Q2 alone supports less than that full clause, but the bullet quotes Q2 only for placement, so as worded it does not overreach.
- Q3 `该文件夹下的所有检测文献在去除本人文献检测结果中` (find 22549) → Inference bullet 3 "and ties it to the 去除本人文献检测结果": **supports** — verbatim.

## Addendum — cross-id spans.tsv offset audit (peer R50ReopenRowS105 flag + own run)

Same python script over all 55 spans.tsv rows against committed captures (S104 001287c436f0e6b1d166ae8d, S105 e3ca8f4fdd15420b80096a75, S106 28750bcdf5d36cd90a7709fb). Observed `rec - find` deltas:

```
S104 18/18 rows: -80   (e.g. S104-1 rec 114, find 194)
S105 32/34 rows: -80; 2 edition-line rows: -48 (S105-1/-14 rec 0, find 48)
S106 3/3 rows: -80     (rec {3,22431,22469}, find {83,22511,22549})
all 55 rows count=1
```

Conclusion: the uniform −80 (and −48 at the clamped S105 head row) is the DESIGNED CONTEXT=80 context window (build-spans.py:44,116,119-120; docstring lines 17-18 and 24-25): `offset` is the span's start (`start = max(0, off − CONTEXT)`), and the quote's anchor char N = offset + the quote's position in its span — which equals the entry layers' char refs exactly (S106 83/22511/22549; S105 48/27587/30661/30745). Span slice equality passes for every row. No defect in the offset semantics; residual is only the bare column-header naming (`offset` vs the entries' `char N`) — a readability note, not an error.
VERDICT: attacked S106 quote integrity (uniqueness, find offsets, span-slice equality, size bounds, entry containment, substring redundancy, distinct offsets) and Inference-bullet grounding — survived; 3/3 quotes exactly-once with exact span slices, no redundant rows, 3 distinct offsets, bullets 3/4 grounded verbatim; cross-id re-verification after peer retraction and source check of build-spans.py confirms the uniform −80/−48 delta is the designed CONTEXT=80 window (offset = span start), not drift — no defect; only a naming-ambiguity note on the `offset` header.
