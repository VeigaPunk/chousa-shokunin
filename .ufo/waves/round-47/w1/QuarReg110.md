# QuarReg110 — quarantine hand-check, register S110 (chousa), round 47 wave 1

## Item
§10 quarantine hand-check of absent-defect-register row `chousa` / register `S110`, which binds to lane id S094 (https://aclanthology.org/2025.coling-main.108.pdf).
Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/a9cf41709b6fa5028332d98c.txt`.
No fetch. No lane production file touched. No tools installed.

## Inputs (pointers)
- Register row: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:50` has lane cell `` `chousa` ``, round `round3`, id `S110`, verdict `` `payload-absent` ``, the URL above, and the reason "cited source, companion URLs and local artifacts were all checked; the quote is in none of them".
- Capture: 83246 bytes, sha256 `d24f2315aad72d7ba64faa65d2da70bd05702f7404ac63a624a0803ffe78b136`. `printf '%s' URL | sha256sum | cut -c1-24` gives `a9cf41709b6fa5028332d98c`, which matches the filename. The capture is a pdftotext-style two-column layout render: the left column is chars 0–80 of each line and the right column starts at char 81.
- Lane `corpus/SOURCES.md` has no S094 row yet (`rg -n S094` returned nothing; the registry holds S001–S089). The lane id comes from the dispatch's URL binding.

## Commands run (decisive output)
1. `rg '\| S110 \|' register` returned line 50 (chousa), line 181 (tabi) and line 217 (tameshi). Only line 50 is in scope.
2. `wc -c; sha256sum` on the capture: `83246`, `d24f2315…b136`.
3. `/tmp/chousa-r47-QuarReg110/check.py` split the lines in capture region 19000–22200 into the left and right column streams, joined each trailing-`-` word with the next word, and ran an ordered whole-word match of each register quote. The last quote word was allowed to match as a prefix, because the register cuts quotes at about 120 chars. Output:
```
Q1 words=16 len=120 -> PRESENT col=L span=21381..21632   joins: ('interannotator', 21423, 21569)
Q2 words=18 len=118 -> PRESENT col=R span=20304..20682   joins: []
Q3 words=17 len=120 -> PRESENT col=L span=20004..20519   joins: ('annotate', 20197, 20336)   last capture word: annotation
```
4. `cap.count(slice)` and `cap.find(slice)` for every slice below: each count is 1, with the offsets shown.

## Per-quote hand-check
The only normalisations used were whitespace and line-break collapse, column de-interleave, and hyphen-split joins. No markup was involved and every word matched verbatim, including `’` (U+2019) in "Cohen’s".

**Q1** — `The Cohen’s Kappa (Cohen, 1960) score for interannotator agreement is 0.792, indicating substantial agreement among the `
Verdict: **present**. All 16 words occur in order in the left column. "interannotator" is the hyphen split `inter-` (ends 21429) + `annotator` (starts 21560).
- [21381,21429) `The Cohen’s Kappa (Cohen, 1960) score for inter-`
- [21560,21612) `annotator agreement is 0.792, indicating substantial`
- [21613,21632) `agreement among the` (the sentence continues "annotators.")

**Q2** — `we re-assign labels based on the claim-relevant evidence gathered from open websites. This manner results in total 202`
Verdict: **present**. All 18 words occur in order in the right column. The left-column lines between them are interleave only. The `-` in "re-assign" and "claim-relevant" is a real hyphen inside a line, not a split.
- [20304,20329) `we re-assign labels based` (inside line slice [20282,20329) `no evidence provided, we re-assign labels based`)
- [20459,20508) `on the claim-relevant evidence gathered from open`
- [20640,20682) `websites. This manner results in total 202` (continues `“NOT ENOUGH INFO" claims being relabeled.`)

**Q3** — `We recruit two NLP researchers proficient in English to manually annotate claim-evidence correlations based on the annot`
Verdict: **present**. All 17 words occur in order in the left column. "annotate" is the hyphen split `an-` + `notate`. The final "annot" is the register's 120-char cut of "annotation".
- [20004,20022) `We recruit two NLP` (inside line slice [19976,20022) `as claim-relevant evidence. We recruit two NLP`)
- [20151,20200) `researchers proficient in English to manually an-`
- [20330,20377) `notate claim-evidence correlations based on the`
- [20509,20529) `annotation guideline` ("annot" is a prefix of "annotation")

## Row verdict
- quarantine: register `S110` (https://aclanthology.org/2025.coling-main.108.pdf) verdict: `present` — all three register quotes occur word-for-word in order in the S094 capture once the two columns are de-interleaved and the hyphen splits are joined (Q1 at chars 21381–21632 joining `inter-`/`annotator`, Q2 at 20304–20682 in the right column, Q3 at 20004–20529 joining `an-`/`notate`), so the mechanical `payload-absent` is false.

Anchor quote (contiguous and unique, `cap.count`=1, 6 words, on one line with no interleave or split):
`annotator agreement is 0.792, indicating substantial` at char 21560 (end 21612).
Alternate 4-word anchor: `we re-assign labels based` at char 20304 (count 1).

## Findings
1. (medium; register defect, read-only so routed rather than fixed) `absent-defect-register.md:50` marks S110 `payload-absent`, but all three quotes are present. This is the same failure seen in rounds 43 and 46: the mechanical census does not de-interleave the two columns of a layout PDF capture (Q1 and Q3 are cut by right-column text, and Q2 sits entirely in the right column) and does not join line-end hyphen splits (`inter-`/`annotator`, `an-`/`notate`).
2. (low) The register cuts quotes at about 120 chars, mid-word (Q3 ends at "annot"). A strict whole-word matcher would call Q3 absent even after normalisation. Prefix matching on the final token is needed.
3. (info) S094 is not yet a row in lane `corpus/SOURCES.md`. The id binding comes only from the dispatch, by URL equality. The C3 adoption must add the row before any `char N` anchor in an entry cites S094.

## Residual risk and verification gaps
- The column boundary at char 81 was chosen by inspecting region 19700–21800. It was applied only to lines in 19000–22200, not checked across the whole capture. Every quote slice was confirmed independently with `cap.find` and `count`=1.
- Offsets are Python `str` (code-point) indices into the UTF-8 file, not byte offsets. There are 47 non-ASCII code points before char 21381, so the byte offset of char 21381 is 21474.
- Scratch `/tmp/chousa-r47-QuarReg110/` is deleted.
