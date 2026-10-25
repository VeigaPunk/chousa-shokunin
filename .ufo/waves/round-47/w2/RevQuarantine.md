ATTACKS: quarantine verdicts S093/S094/S108/S110 (register rows, all claimed `present`); lane slice re-derivation
VERDICT: holds

Round 47 wave 2, reviewer seat (leaf; no subagent dispatch, no fetch, no install). Scope: lessons/round-47.md `## Gate` quarantine block (register S093, S094, S108, S110, all `present`). Report-only; no lane production file touched.

## 1. Lane slice re-derivation (operator awk recipe)

Recipe (round-42.md:43, reused verbatim; guards: lane cell `chousa`, a round cell, an id cell):

    awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
      /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md | wc -l

Output: `24`. The 24 rows are register lines 37–56 (S077, S080, S082, S084, S086, S088, S093, S094, S095, S096, S104, S105, S108, S110, S111, S112, S114, S116, S120, S125) plus the `never-checked` block lines 269–272 (S100`, S101`, S102`, S103`). The naive lane-only variant (no round/id guards) prints 25 (it adds the `## By lane` row, whose `chousa` cell has no round/id, and which the recipe's guards exclude). 24 confirmed.

## 2. Word-by-word re-check of the four register quotes

Method (independent normaliser, this seat): for each register row, read the quote cell (cell 6, `|`-split) verbatim from the register; split the capture into the abstract/left column and the interleaved right-column tail. a 2+ space run whose end lies in [45,95] (the figure/table column; S110 uses leading 2+ spaces for pure right-column lines, S108 is single-column HTML); tokenise each column by whitespace; join line-end hyphen splits within a column (`fac-`+`tualness.`→`factualness.`, `Sup-`+`ports”`, `cor-`+`responding`, `inter-`+`annotator`, `an-`+`notate`); strip matching leading/trailing punctuation on both sides; then require every quote word in order as a subsequence of the column stream (final word may match as a prefix, since register cells are 120-char truncations).

Result — all 8 register quotes:

| register row | lane id | capture | quote | result |
|---|---|---|---|---|
| S093 | S090 | 4132ec1b… | 1 of 1 | 22/22 words in order, LEFT col, span [1526,1714) |
| S094 | S091 | 3749141b… | 3 of 3 | 12/12, 19/19, 16/16 words in order, LEFT col, spans [966,1156), [918,1359) |
| S108 | S092 | b502d4c6… | 1 of 1 | 16/16 words in order, LEFT col, span [2731,2839) |
| S110 | S094 | a9cf4170… | 3 of 3 | 16/16 (LEFT), 18/18 (RIGHT), 17/17 (LEFT) words in order, spans [21381,21632), [20304,20682), [20004,20519) |

Interleaved material between matched words, per quote:
- S093: only `(2)` (the elided enumerator, char 1612–1617) and `Cited source` (the figure 1 column label, chars 1621–1669); the quote's final word `un` is a truncation of `unsupported` (char 1703).
- S094 Q1: the Table 1 example interleave `2004 looking for business opportunities.)` (chars 833–901). Q2: the `Evidence:` label (interleave) plus hyphen splits `fac-`/`tualness.` and `Sup-`/`ports”`. Q3: `他在 2004 年…` (interleave) plus `cor-`/`responding`.
- S108: only render markup: `Supported ,` (space before comma, char 2769–2772) and `κ \kappa` (TeX alt-text after κ); both are empty normalisations, no word changed.
- S110 Q1: right-column text between left-column rows (Table 2 distribution line), plus `inter-`/`annotator`; Q2: left-column text between right-column rows (`notate claim-evidence correlations…`, `annotation guideline…`); Q3: right-column text plus `an-`/`notate`.

No quote word is missing or changed. In every case the capture contains the quote's words in order, and every gap is accounted for by one of the three known PDF/HTML render artifacts (column interleave, line-end hyphen split, whitespace/punctuation markup). The register's `payload-absent` class is a mechanical false negative; all four `present` verdicts in lessons/round-47.md `## Gate` hold.

## 3. Cross-check against the lesson's quoted char ranges

My token stream reports the same spans the lesson gives, with two wording notes:
- S093: `[1526,1714)`; the lesson's `1526–1705` counts only the truncated prefix `un` (char 1703–1705) of `unsupported`. OK.
- S094 Q1: my greedy first-word anchor finds `CFEVER` at char 127 (paper title), start quas quote starts at char 810. The full quote is also present at [810,965) (the first word `CFEVER` matches at char 810; the span then continues past the table interleave). Location only; presence and order unaffected.
- S094 Q3 and S110 Q1/Q3: same greedy-anchor effect (`claims`@918 vs 1187; `The`@5590 vs 21381; `We`@6124 vs 20004). All ends match the lesson exactly.

## 4. Findings

- No defect found. 22/22, 12/12, 19/19, 16/16, 16/16, 16/16, 18/18, 17/17 quote words verified verbatim in order against the on-disk captures. All four quarantine verdicts (`present`) hold.
- (info) The register's `payload-absent` cells are false negatives caused by PDF/HTML render layout (column interleave, hyphen splits), reproduced here and matching the wave-1 seat reports (w1/QuarReg093/094/108/110.md) and the lessons' own notes.

## 5. Residual risk / gaps

- Only on-disk captures were read (no fetch, per contract). Capture fidelity to the live sources is assumed.
- Word order is verified as an ordered subsequence, not as a contiguous substring; this is the intended check for these render artifacts. A contiguous-substring comparison would require the de-interleaved column reconstruction, which is documented above.

Commands run (decisive): the awk recipe above (24); `python3` verification scripts in /tmp/chousa-r47w2-RevQuarantine/ (verify.py, vfinal/v6–v11.py, final_verify.py, final2.py, col_stream trace) — internal scratch, deleted below. No tools installed; no lane/fleet/kuknow files modified. Scratch /tmp/chousa-r47w2-RevQuarantine/ removed:
