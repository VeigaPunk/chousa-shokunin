# ReviewOpenS091 — round 47 wave 1: open lane S091 (CFEVER) from its capture

Item: open lane S091 (https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432; staged id S099 → held lane S091, bound by URL equality) from capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3749141b52b2dbb2e0e821c3.txt`. Locate grounding quotes, test the three staged candidates for contiguity, check the venue and year, and map support and contradiction against the two staged entries. No fetch was made, nothing was installed, and the scratch directory `/tmp/chousa-r47-ReviewOpenS091/` was deleted.

## Capture identity
`sha256sum` → `0b3518bf2d2ba3047212d6f4ccb83dfd1cf01960e51acb324f7b74b6b2730573`; `wc -c` → `66770` bytes; Python `len(open(F,encoding='utf-8').read())` → `chars 66321`. The capture is pdftotext layout of a two-column PDF. The abstract (left column) is interleaved line by line with the Table 1 example box (right column: `Claim: 尼克·貝爾格…`, `Evidence:`, `Verdict: Supports`).

## Venue/year — staged "AAAI 2021" is WRONG
- offset 41: `The Thirty-Eighth AAAI Conference on Artificial Intelligence (AAAI-24)`. This is a running header, count=9, so it is not unique.
- offset 6351 (unique): `Copyright © 2024, Association for the Advancement of Artificial`.
- The capture also cites 2023 work (`DeHaven and Scott 2023`), so a 2021 date is impossible.
- Correct venue: **AAAI-24 (38th AAAI Conference, 2024)**, consistent with OJS article id 29825.
- Affected staged text: `claim-support-test-r37.md:6` `… — AAAI 2021` and SOURCES.append.md row S099 `CFEVER … — AAAI 2021 — …`. Both MUST read AAAI-24 / 2024 in the lane entry and Registry row.

## Staged candidates — none is contiguous
Command: `python3 f.py <candidates…>` (str.find plus count over the capture).
```
'CFEVER comprises 30,012 manually created claims based on content in Chinese Wikipedia' find= -1 count= 0
'labeled as “Supports”, “Refutes”, or “Not Enough Info”' find= -1 count= 0
'annotated with corresponding evidence sentences sourced from single or multiple pages in Chinese Wikipedia' find= -1 count= 0
```
Each candidate is broken by column interleave: after the line-final word, roughly 24 spaces and the Table 1 right-column text intervene before the next line. The third candidate is also hyphen-split (`cor-` / `responding`, `mul-` / `tiple`). Contexts (±100 chars, verbatim `repr`):
- C1 fragment `CFEVER comprises 30,012` @810 count=1: `'t                      意商機。(Nick Berg traveled to the Middle East in\n  Extraction and VERification. CFEVER comprises 30,012                        2004 looking for business opportunities.)\n  manually created claims based on'`
- C2 fragment `Each claim in CFEVER is labeled as “Supports”,` @966 count=1: `'…manually created claims based on content in Chinese\n  Wikipedia. Each claim in CFEVER is labeled as “Supports”,                   Evidence:\n  “Refutes”, or “Not Enough Info” to depict its degree of fac-'`
- C3 region @1328: `'…tualness. Similar to the FEVER dataset, claims in the “Sup-\n  ports” and “Refutes” categories are also annotated with cor-                他在 2004 年 3 月前往伊拉克 尋找通訊生意商機，自\n  responding evidence sentences sourced from single or mul-                   2004 年 4 月 9 日失蹤。…\n  tiple pages in Chinese Wikipedia.'`

Longest contiguous unique replacements carrying the same facts. The body restates every fact on clean single-column lines:
- C1: `There are 30,012 claims in the CFEVER dataset.` @25003 (Dataset Statistics section). The abstract alternative is `manually created claims based on content in Chinese` @901 (8 words).
- C2: `the claim as “Supports”, “Refutes”, or “Not Enough Info”.` @20771 (Claim Annotation section). The abstract alternative is `Each claim in CFEVER is labeled as “Supports”,` @966.
- C3: no contiguous abstract slice survives, because the hyphen breaks every 4+ word run. The body equivalent is split across two right-column lines broken by a footnote: `For the first two categories, the annotator must also find the` @20905 + `sentences as evidence from the fact database.` @21044.

## Verified quote set (TSV)
```
id	offset	quote
S091-q1	25003	There are 30,012 claims in the CFEVER dataset.
S091-q2	20771	the claim as “Supports”, “Refutes”, or “Not Enough Info”.
S091-q3	20905	For the first two categories, the annotator must also find the
S091-q4	21044	sentences as evidence from the fact database.
S091-q5	966	Each claim in CFEVER is labeled as “Supports”,
S091-q6	901	manually created claims based on content in Chinese
S091-q7	24458	could support or refute a claim, the claim was labeled as
S091-q8	28442	over the 1,936 claims shows a score of 0.7934 in Fleiss κ
S091-q9	28570	(Fleiss 1971), which is higher than the score of 0.6841
S091-q10	24549	We discovered that 84.4% of the claims are
S091-q11	54352	claims in CFEVER require evidence extracted from only
S091-q12	17664	to convert the text to Traditional Chinese.
S091-q13	6351	Copyright © 2024, Association for the Advancement of Artificial
```
Check: `o=c.find(q); ok = c[o:o+len(q)]==q and c.count(q)==1 and 4<=words<=25`. Output, verbatim:
```
S091-q1	25003	… | words 8 count 1 slice_eq True OK
S091-q2	20771	… | words 9 count 1 slice_eq True OK
S091-q3	20905	… | words 11 count 1 slice_eq True OK
S091-q4	21044	… | words 7 count 1 slice_eq True OK
S091-q5	966	… | words 8 count 1 slice_eq True OK
S091-q6	901	… | words 8 count 1 slice_eq True OK
S091-q7	24458	… | words 11 count 1 slice_eq True OK
S091-q8	28442	… | words 12 count 1 slice_eq True OK
S091-q9	28570	… | words 10 count 1 slice_eq True OK
S091-q10	24549	… | words 8 count 1 slice_eq True OK
S091-q11	54352	… | words 8 count 1 slice_eq True OK
S091-q12	17664	… | words 7 count 1 slice_eq True OK
S091-q13	6351	… | words 9 count 1 slice_eq True OK
```
Backtickable 2+-word phrases: `CFEVER dataset` (q1), `Not Enough Info` (q2), `first two categories` (q3), `fact database` (q4), `labeled as` (q5), `manually created claims` (q6), `support or refute` (q7), `Fleiss κ` / `1,936 claims` (q8), `score of 0.6841` (q9), `84.4% of the claims` (q10), `only one Wikipedia page` is NOT contiguous, so use `require evidence` (q11), `Traditional Chinese` (q12), `Copyright © 2024` (q13).

Recommended Registry-row and entry anchors: q1 (size), q2 (label set), q3+q4 (evidence requirement), q8 (reliability), q13 (venue/year). Anchor every `char N` to these offsets, not to the abstract.

## Staged sentences this source SUPPORTS
- r37 l.26–30, "CFEVER comprises 30,012 claims over Chinese Wikipedia … labeled as “Supports”, “Refutes”, or “Not Enough Info” … also annotated with corresponding evidence sentences sourced from single or multiple pages in Chinese Wikipedia". The facts are supported by q1, q2, q5, q6, q3+q4. However, both quoted spans are non-contiguous in the capture: `'Each claim … is labeled'` find=-1, and the "also annotated…" span find=-1. They must be re-anchored or written as paraphrase.
- r37 l.53–55, "CFEVER applies the same label set and the same evidence requirement". Partly supported by `Similar to the FEVER dataset, claims in the “Sup-` @~1340 (hyphen-split, so not quotable) and by q2+q3. See the overstatement below.
- Amendment l.38–39 and 49–50 (FEVER 0.6841 Fleiss): independently corroborated by q9, `higher than the score of 0.6841 mea-sured with 7,506 claims (4% from total) in FEVER` (@28570; hyphen-split after q9).
- Amendment theme "reliability is measured rather than perfect": S091 adds a third figure, 0.7934 five-way Fleiss κ on 1,936 claims (q8, @28442; `0.7934 for five-way inter-annotator` @1592 count=1). It also reports evidence correctness of 84.4% on 700 sampled claims (q10; `another 700 claims (2.33% of the dataset)` @~29180). The staged r37 cites neither figure.

## Staged sentences this source CONTRADICTS or OVERSTATES
1. **Venue/year (contradiction).** Staged r37:6 and row S099 say `AAAI 2021`; the capture says `(AAAI-24)` @99 and `Copyright © 2024` @6351.
2. **Row scope "the dataset-description table" (imprecise).** Table 1 @2620 is `An example from the CFEVER dataset`. The statistics table is `Table 3: Dataset statistics of CFEVER in different splits.` @23350, and Table 2 @8156 is `Comparison of CFEVER with other fact verification datasets in Chinese.` The row should name Table 3, or Table 2 if the comparison is meant.
3. **"single or multiple pages" (true but unweighted).** Table 3 reports Avg. Evidence Pages per Claim of `1.13 … (88.41%)` (train) as the single-page proportion. The limitations section says `most of the` / `claims in CFEVER require evidence extracted from only` (q11 @54352) / `one Wikipedia page.` A lane bullet implying a multi-page evidence requirement overstates this.
4. **r37 l.53–58, "The Chinese literature is not behind … a Chinese-language claim record can use the same three-way state without a translation caveat" (overstated inference).** One dataset is generalised to "the Chinese literature". CFEVER also normalised all text to Traditional Chinese (q12 @17664; `cles in both Traditional and Simplified Chinese` @~17400). Its own NEI rule is evidence-relative and database-bounded (q7 @24458 → `“Not Enough Info.”`; "no factual sentences in our fact database"), which is the exact caveat amendment l.52–61 raises. Nothing in S091 licenses "without a translation caveat". This must stay under Inference, scoped to CFEVER/Traditional Chinese Wikipedia.
5. **Label-name drift (minor).** CFEVER prints both `“Not Enough Info”` (q2) and `“Not Enough Information”` (Table 3 legend @~23660 and the conclusion @~53650). "Same label set" holds semantically, but quotes must use the exact string at the anchored offset.

## Verdict
S091 is OPEN. 13 contiguous unique quotes are verified, and 5 are recommended as anchors. Zero of the 3 staged candidate quotes are contiguous; abstract-level spans must not be used beyond q5/q6. The staged venue/year `AAAI 2021` is falsified (AAAI-24, 2024). r37's "without a translation caveat" inference is overstated.

## Residual risk and verification gaps
- Offsets assume `open(...,encoding='utf-8').read()` with no newline translation. A reader using `newline=''` would see the same offsets only if the capture has no `\r`; this was not checked separately.
- The volume/issue number is not printed in the capture (no `v38`, `38(` or DOI matches; only a reference at @59634 matched `Proceedings of the AAAI`). "AAAI-24" is the header string; volume 38 is [INFERENCE].
- No lane file was edited. C3 counter legs (spans.tsv, char-N anchors) were not run by this seat.
