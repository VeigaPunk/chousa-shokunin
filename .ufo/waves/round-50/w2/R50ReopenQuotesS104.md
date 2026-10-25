# R50 Reopen Quotes S104 — round 50 wave 2 (falsify)

Seat: R50ReopenQuotesS104 · Date: 2026-10-25 · Lane: chousa-shokunin@6a068f2 (frozen claims), L1 landed @74794db0.
Tooling: no installs (RULES.md read; python3 only). Scope: S104 quotes/spans only, read-only; no fetch.

## 1. Checks run (commands + output)

All under `/dev/shm/chousa-r50-R50ReopenQuotesS104/verify_s104.py`; capture read as UTF-8 from `.qcache/001287c436f0e6b1d166ae8d.txt` (sha256 = `67f6f2df8ce96d01673d8f2f740e663f55ed8324bbf804834562bf746740a1db`, matches spans.tsv `capture_sha256`).

```
capture_len 2288
quotes_S104_rows 18 spans_S104_rows 18
=== quote verification ===
1 occ= 1 off= 194 words= 1 chars= 51 in_entry= True len_quote= 51
2 occ= 1 off= 194 words= 1 chars= 108 in_entry= True len_quote= 108
3 occ= 1 off= 211 words= 1 chars= 56 in_entry= True len_quote= 56
4 occ= 1 off= 246 words= 1 chars= 21 in_entry= True len_quote= 21
5 occ= 1 off= 268 words= 1 chars= 33 in_entry= True len_quote= 33
6 occ= 1 off= 380 words= 6 chars= 25 in_entry= True len_quote= 25
7 occ= 1 off= 422 words= 9 chars= 39 in_entry= True len_quote= 39
8 occ= 1 off= 549 words= 1 chars= 16 in_entry= True len_quote= 16
9 occ= 1 off= 549 words= 3 chars= 24 in_entry= True len_quote= 24
10 occ= 1 off= 662 words= 1 chars= 21 in_entry= True len_quote= 21
11 occ= 1 off= 684 words= 1 chars= 12 in_entry= True len_quote= 12
12 occ= 1 off= 735 words= 1 chars= 53 in_entry= True len_quote= 53
13 occ= 1 off= 849 words= 1 chars= 23 in_entry= True len_quote= 23
14 occ= 1 off= 849 words= 1 chars= 50 in_entry= True len_quote= 50
15 occ= 1 off= 1236 words= 1 chars= 33 in_entry= True len_quote= 33
16 occ= 1 off= 1380 words= 1 chars= 38 in_entry= True len_quote= 38
17 occ= 1 off= 1469 words= 1 chars= 43 in_entry= True len_quote= 43
18 occ= 1 off= 1784 words= 1 chars= 30 in_entry= True len_quote= 30
=== span verification ===
1 spans/S104-1.txt off= 114 span_len= 211 slice_match= True span_eq_quote_col= False
2 spans/S104-2.txt off= 114 span_len= 268 slice_match= True span_eq_quote_col= False
3 spans/S104-3.txt off= 131 span_len= 216 slice_match= True span_eq_quote_col= False
4 spans/S104-4.txt off= 166 span_len= 181 slice_match= True span_eq_quote_col= False
5 spans/S104-5.txt off= 188 span_len= 193 slice_match= True span_eq_quote_col= False
6 spans/S104-6.txt off= 300 span_len= 185 slice_match= True span_eq_quote_col= False
7 spans/S104-7.txt off= 342 span_len= 199 slice_match= True span_eq_quote_col= False
8 spans/S104-8.txt off= 469 span_len= 176 slice_match= True span_eq_quote_col= False
9 spans/S104-9.txt off= 469 span_len= 184 slice_match= True span_eq_quote_col= False
10 spans/S104-10.txt off= 582 span_len= 181 slice_match= True span_eq_quote_col= False
11 spans/S104-11.txt off= 604 span_len= 172 slice_match= True span_eq_quote_col= False
12 spans/S104-12.txt off= 655 span_len= 213 slice_match= True span_eq_quote_col= False
13 spans/S104-13.txt off= 769 span_len= 183 slice_match= True span_eq_quote_col= False
14 spans/S104-14.txt off= 769 span_len= 210 slice_match= True span_eq_quote_col= False
15 spans/S104-15.txt off= 1156 span_len= 193 slice_match= True span_eq_quote_col= False
16 spans/S104-16.txt off= 1300 span_len= 198 slice_match= True span_eq_quote_col= False
17 spans/S104-17.txt off= 1389 span_len= 203 slice_match= True span_eq_quote_col= False
18 spans/S104-18.txt off= 1704 span_len= 190 slice_match= True span_eq_quote_col= False
spans_matching 18 of 18
DISTINCT offsets: 15 of 18 [114, 131, 166, 188, 300, 342, 469, 582, 604, 655, 769, 1156, 1300, 1389, 1704]
=== redundancy ===
sub: 1 in 2 len 51 of 108
sub: 3 in 2 len 56 of 108
sub: 4 in 2 len 21 of 108
sub: 4 in 3 len 21 of 56
sub: 5 in 2 len 33 of 108
sub: 8 in 9 len 16 of 24
sub: 13 in 14 len 23 of 50
```

Cross-check (final.py): quotes/spans rows equal per id (quote/url/entry columns identical), `capture_sha256` matches file hash, and `offset == text.find(quote) − 80` for all 18 (spans carry 80 chars of leading context; CONTEXT=80 in `build-spans.py:44,119`).

## 2. Findings

- **Exactly-once occurrence:** all 18 S104 quotes occur exactly once (`occ= 1`) in the capture; `text.find` offsets in centre column above.
- **Span equality:** every span file equals `text[offset:offset+len(span)]` (`slice_match= True` for 18/18); span offsets are the span's start (quote start + 80).
- **Constraints:** max whitespace words = 9 (quote 7), max chars = 108 (quote 2) — all ≤25 words and ≤160 chars.
- **Inside citing entry:** all 18 quotes found in `corpus/knowledge/istic-citation-verification-r39.md` (`in_entry= True`).
- **Redundant rows (proper substring of another S104 row):** rows 1⊂2, 3⊂2, 4⊂2 and ⊂3, 5⊂2, 8⊂9, 13⊂14 → 6 of 18 rows are redundant fragments of a longer same-id quote.
- **DISTINCT start offsets:** 15 (of 18 rows); quote find-offsets distinct = 15 ([194,211,246,268,380,422,549,662,684,735,849,1236,1380,1469,1784]).
- The entry's "eleven quotes" claim corresponds to the 11 primary locations; the 4 extra offsets (211/246/268 fragments of the 194 definition; 684 heading) plus nested rows explain 18 rows.

## 3. Five highest-weight quotes vs Inference bullets

1. `按合作者排除自引标准统计他引次数， 1 元/篇次` (char 549) → B2 "standard invoked to price a count, not defined": **supports** — the standard appears only in the fee row; "not defined" corroborated by re-run `grep -c` 核对/匹配/查重 = 0 over capture.
2. `03 完成并审核 报告 06 出具正式报 告并存档` (char 380) → B3 workflow closing steps: **supports** — step list explicitly ends in 完成并审核/出具正式报告并存档 (stamped deliverable from char 1784 sibling).
3. `对于在2年内提供检索要求相同的用户进行多次委托时，用户在提供上次检索结果同时，本次检索可免去相同数据的费用` (char 735) → B4 supplied-result waiver: **supports** — matches "waived when earlier result supplied within two years" word-for-word.
4. `所有文章必须包括全部作者（全拼）、标题、期刊、年、卷、页码、DOI等完整信息` (char 1380) → B1 bibliography side: **supports** — establishes per-article bibliography object at whole-article-list level (index-records leg is carried by the definition quote at char 194, not this quote alone).
5. `1.委托5篇以内收录检索，检索费300元。` (char 662) → B1 priced unit: **supports less than claimed** — states fee for ≤5-work commission, but "300元 buys the matching against what SCI… record" is an inference beyond this quote (relies on 收录检索 term + definition quote).

## 4. VERDICT

Attacked S104's 18 quote rows / 18 spans (occurrence, offsets, span-slice equality, length constraints, entry containment, redundancy); all checks pass with 15 distinct offsets and 6 redundant substring rows — **survived** (no defect found).
