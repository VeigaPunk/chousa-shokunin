# R55W2ReviewEntryShape — round-55 C2 entry review

Reviewed `corpus/knowledge/grey-literature-and-chinese-search-record-r40.md` as committed at `29cfb12abd70f688b48c0d17f31e636f2d81104a`, against that snapshot's `corpus/QUALITY.md` and `source-type-taxonomy-r37.md`.

## Findings

1. **[P2] Line 7: `recheck:` omits the required working-directory/layout.** QUALITY.md criterion 13 (lines 59–62) requires a new recheck to state its cwd or the checkout layout assumed by a relative path. The command invokes relative `tools/capture-text.py` but does not say where to run it. Running it from the scratch lane root succeeds, but does not make the command placement-independent. The r37 provenance example explicitly says “from the lane root” in its recheck line.

   Observed command/output (scratch lane cwd):
   ```text
   python3 tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw --locate '是否检索灰色文献'
   LOCATED count=1 offset=4678
   exit=0
   ```

2. **[P3] Line 29: currency-status negative has no sweep.** “None of the three captures says whether it is still in force, revised or replaced” is a negative claim about the captured forms, but the entry supplies no sweep command, terms/counts, or equivalent reproducible review for this assertion. A reviewer probe found status-adjacent words in the forms (`S124`: `有效` 6, `修订` 2, `替代` 2, `更新` 2; `S125`: `更新` 1; `S126`: all 0); those occurrences are not themselves evidence about this guideline's currency, so a scoped sweep/review is needed rather than an unsupported absence assertion. The entry's separate line-28 sweep does not cover these status terms.

## Checks and supported shape

- `python3 tools/build-spans.py --quotes corpus/evidence/round55/quotes.tsv --out corpus/evidence/round55 --check` (scratch snapshot): `SPANS_ROWS=19 STALE=0`, exit 0.
- The `recheck:` locator above returned the stated unique offset, 4678.
- `git grep -n '是否检索灰色文献' dba605deb5cd5ed4874e0e3c39ba24737409cd80 -- corpus/knowledge`: rc 1, empty output, matching line 8's base-ground claim. At the r55 revision the term occurs in the entry (the recorded `git grep -c` result is `...r40.md:5`).
- Quote/form probe: all 20 checks (19 manifest quotes plus the locate string) were found once at the stated character offsets and on one line; `TOTAL_MISMATCH=0`. S124 form: length 13,718, U+FFFD=0, sweep counts for (`灰色文献`, `是否检索灰色文献`, `即“灰色文献”`, `即灰色文献`, `2019`, `发布`, `国家药品监督管理局`, `试行`, `PRISMA`, `Cochrane`) = `[7,1,1,0,0,0,1,1,8,5]`. The S124 `.txt` sidecar contains none of the checked quotes; the two report-field quotes at chars 4625 and 4652 are on the same line.
- Source lines 3–5 put the URL immediately after the em dash and give exact char anchors. All entry S-tokens are bound ids only: S124 (11), S125 (7), S126 (6). Registry rows `SOURCES.md:134–136` bind those same URLs, are `mined`, opened `2026-10-27`, and list this entry under `used-by`; tiers/scopes distinguish the third-party text (S124), issuance report (S125), and regulator notice (S126). The round-55 `## Gate` map at `lessons/round-55.md:35,51` corroborates the by-document renumbering and adoption note.
- Title/body calibration is supported: S124's report-field sentence and unpublished-material examples are quoted at chars 4652 and 994; the entry distinguishes the third-party copy from issuance evidence in its observation/inference. `adopted:` is present and consistent with the Gate decision. The named W1 records `R55CritEntailInf` and `R55ReviewProvinceC2` are present in `w1-results.json`.
- `python3 corpus/evidence/round29/prose-check.py corpus/knowledge/grey-literature-and-chinese-search-record-r40.md`: `TOTAL hits=0`, exit 0. The entry has no template-token or `live` hits.

VERDICT: The R55W2 C2 entry-shape claim is falsified narrowly: sourcing, bindings, and quote anchors survive, but line 7's recheck portability and line 29's unswept currency-negative remain defects.
