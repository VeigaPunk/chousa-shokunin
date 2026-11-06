# R81ReviewerEntries — domain review of C1 entries (K3)

Subject: `corpus/knowledge/citation-searching-tarcis-r81.md`, `corpus/knowledge/correction-retraction-status-r81.md`,
registry rows S203–S208, read at candidate landing `7e2da96a0541946e796384d42fea18e09ede9e9f`
(tree extracted with `git archive ... | tar -x` into `/fast/scratch/hyaku/chousa-r81/R81ReviewerEntries/tree7e2d`).
Captures read: `corpus/captures/<key>.txt` (committed bytes). Seat did not edit any lane file.

Receipts (this folder):
- `receipt-k3-quote-check.txt` — `python3 check.py` (quote location, word counts, row listing), rc=0.
- `receipt-k3-anchors.txt` — grep receipts for each anchor cited below, rc per line.

Capture sha256 (match refetch.tsv 2026-11-06 success rows S203, S204, S205, S207; S206 row not re-printed by my grep,
see §Method):
- f2489455cc311a4de981e926 (S203) 31493aa6…8cdb3c
- c52a1f15884a78028febcf43 (S204) b905aae1…c6ed1
- 371c55117727d526805f030d (S205) 08b4b3c0…8b3bc9
- f221c90f69188f775e32cd34 (S206) e1251d47…ab54e
- 43a45b49723f7677d6446c92 (S207) 72a5a93d…af734ecb

## Method

1. Located all 13 blockquote quotes in both entries against whitespace-collapsed captures (`check.py`): 13/13 found;
   word counts 8–25 (max = S207 quote, exactly 25, passes `<= 25`).
2. Matched every recommendation number in the decision tables against the **final** recommendations section of S203
   (capture lines 261–503, headings `Recommendation 1`–`10` at lines 262, 289, 309, 334, 355, 383, 400, 422, 448, 463).
   The Delphi-draft numbering (lines 1240–2408) was checked and **not** used by the entry: every table citation uses the
   final numbering. No draft-numbering defect found.
3. Checked each decision-table row's cited source passage for contradiction (K3) and for overreach (routed defect).

## Overall K3 result

**FIRES on one row:** correction entry, decision-table row "A newer article version exists" (cites S206).
The row says to "cite the version read, with its date" when a newer version exists. S206 capture line 222 says,
verbatim: "The citation should be to the most recent version." (`receipt-k3-anchors.txt`, grep rc=0, line 222).
The row's situation is exactly the one S206 addresses; the row does the opposite.

Note on the reading of K3: the frozen text says "its cited **located quote** contradicts". The two S206 quotes the entry
locates (capture lines 218 and 220) do not themselves contradict the row. The contradicting sentence is in the same S206
passage, two lines below the entry's quoted span. The orchestrator's seat spec says "a decision-table row that its cited
source contradicts fires K3", and I apply that reading. The counter cannot see this defect (it counts located quotes
only); this is why the finding is reviewer-only. Main agent should rule on the letter-versus-source reading.

No other decision-table row is contradicted by its cited source.

## Per-row verdicts — citation entry (`citation-searching-tarcis-r81.md`)

| # | Row (situation → Do) | Cited warrant | Verdict | Located passage |
|---|---|---|---|---|
| T1 | difficult-to-search topic → run backward **and** forward as supplement | S203 rec 2 | **overreach (routed), not K3** | f2489455 line 289–290: "backward and forward citation searching should be seriously considered as supplementary search techniques." (13 words). Entry upgrades "should be seriously considered" to "run"; the Never cell ("rely on the database search alone without saying why") has no basis in rec 2. |
| T2 | completeness of recall → DB search first; citation only supplement; never stand-alone | S203 rec 9 | **supported** | f2489455 line 448–449: "Stand-alone citation searching should not be used for literature searches that aim at completeness of recall." (16 words) |
| T3 | forward-link source → combine two indexes when access allows; never trust one index | S203 rec 6; S204 §4.2.2 | **supported by rec 6; S204 warrant mismatched (routed)** | f2489455 line 383–384: "Using the combined coverage of two citation indexes for citation searching to achieve more extensive coverage should be considered if access is available." (23 words). S204 §4.2.2 (c52a1f15 lines 1424–1434) only says Web of Science and Scopus "can be used for both forwards and backwards citation searching"; it says nothing about combining indexes or single-index sufficiency. Cited warrant does not support the Never cell. |
| T4 | several directions → deduplicate before screening | S203 rec 7 | **supported** | f2489455 line 400–401: "Before screening, the results of supplementary backward and forward citation searching should be deduplicated." (14 words) |
| T5 | new eligible records → another iteration with them as seeds | S203 rec 8 | **supported; Do strengthened (routed)** | f2489455 line 422–423: "If citation searching finds additional eligible records, another iteration of citation searching should be considered using these records as new seed references." (22 words). Source says "should be considered"; Do says "run". Never cell ("stop after one pass without saying so") matches rec 8's report-the-iterations sentence (line 436–437). |
| T6 | writing methods → state seeds, directionality, dates, iterations, indexes/tools | S203 rec 10 | **supported** | f2489455 line 466: "the directionality of searching (backward, forward, co-cited, co-citing)," (8 words); rec 10 list lines 463–480 covers every Do item. |
| T7 | cite TARCiS wording → cite VoR and check erratum ("rec 5 was corrected") | S208 (rejected, unreachable) — "lane inference" | **unanchored assertion (routed), not K3** | No committed capture holds the correction text. `grep -rln 'small error' corpus/` returns only the entry itself (`receipt-k3-anchors.txt`, rc=0). The fact "rec 5 was corrected" rests on an unrecorded web-search snippet. The row self-labels its warrant as inference, but the Do cell states the fact without a label. A rejected row is used as warrant (S208 is tagged `REJECTED`). |

## Per-row verdicts — correction entry (`correction-retraction-status-r81.md`)

| # | Row (observation → Do) | Cited warrant | Verdict | Located passage |
|---|---|---|---|---|
| C1 | PubMed Retracted Publication type → record support as withdrawn; cite notice | S205 | **supported (type); "withdrawn" is lane inference (routed)** | 371c5511 line 342: "The Publication Type Retracted Publication [PT] is assigned to the retracted article." (12 words). S205 does not say how a claim's support should be recorded. |
| C2 | PubMed links an erratum notice → corrected; re-check quoted span | S205 | **supported in reading; quote drops its condition (routed)** | 371c5511 line 323: "If the erratum involves correction of a portion of the article that is not included in the NLM citation, such as the text, graphs, or tables, the erratum notice is simply linked to the citation for the corrected article." The entry quotes only "the erratum notice is simply linked to the citation for the corrected article." (13 words) and drops the antecedent condition. The row's reading survives because NLM links every erratum notice (371c5511, errata section, `NLM links the citation for the erratum notice to the citation for the referent article`), but the entry cites neither that sentence nor the condition. The SOURCES S205 teaches cell repeats the unconditional form. |
| C3 | newer article version exists → cite version read, with date, say newer exists; never version-less | S206 (superseded wording) | **FIRED (K3)** | f221c90f line 222: "The citation should be to the most recent version." — see Overall. Row Do ("cite the version read") is contradicted by its cited source for exactly this situation. |
| C4 | Retraction Watch no hit → record check as negative sweep | S207 | **supported** | 43a45b49 (line 393): "Some other update types, such as expressions of concern and corrections, are also included in the data, but these are not as comprehensive as retractions." (25 words, exactly at limit). Never cell reads this correctly. The "negative sweep" Do is lane method, labeled in the entry's Inference section. |
| C5 | notice unreadable → status unknown; keep source; name the notice | none | **unsourced judgment (routed), not K3** | No warrant cell. Not contradicted by any capture. Row's Never cell ("treat unreachable as 'no notice'") is the right direction but is not sourced to a passage. |

## Terms and caveats (not decision-table rows; not K3 by definition)

- **Terms, citation entry — "A second, independent guide uses the same split."** The S204 passage the entry quotes
  ends with `(Hirt et al., 2024)` (c52a1f15 line 1428; `grep -c` = 2 hits, `receipt-k3-anchors.txt`). S204 derives the
  split from Hirt et al. It is not independent corroboration. **Routed defect (mischaracterization of a source).**
- **Version caveat (rec 5).** The caveat is honest about what was and was not read: it says the snippet, not the page,
  reports a rec-5 correction, and that the page answered HTTP 403. It is also honest that the entry cites no
  rec-5 wording. Gap: the snippet itself is not in any committed capture or receipt (`grep -rn 'small error' corpus`,
  `receipt-k3-anchors.txt`). The caveat is therefore a claim with no committed evidence. **Routed (unanchored).**
- **Inference, correction entry.** The "negative claim carries a sweep" rule is labeled as lane inference. Good.

## SOURCES rows

| Row | Cell checked | Verdict | Evidence |
|---|---|---|---|
| S203 | tier A, paper, scope "as worded in the accepted manuscript; not VoR", anchor "Final recommendations section, recs 1–10" | **matches** | f2489455 line 11: "Version: Accepted Version"; line 261 "Final recommendations…"; lines 262–463 recs 1–10. Teaches cell "supplement, never replace…" matches rec 9 and rec 2 wording. |
| S204 | tier A "docs", anchor §4.2.2 + citation-searching paragraph | **anchor matches; tier A is doubtful (soft)** | c52a1f15 line 1424 `4.2.2. Citation indexes`; line 1428 contains the Hirt-attributed paragraph. A methods guide that attributes its own description to Hirt et al. is a secondary source. I did not locate an explicit tier rubric in `corpus/SOURCES.md` (the header points to tier definitions but the grep did not find a rubric list in the file), so the tier call is judged, not checked against a written definition. Teaches cell "backward (references of included studies)" paraphrases the source's "references of identified relevant studies" (line 1428). Mild. |
| S205 | tier A, scope errata/retractions/EoC, anchor sections | **matches** | 371c5511 has Errata, Retraction, and Expression of Concern sections (lines ~307–356). Teaches cell "an erratum notice is linked to the corrected article's citation" drops the line-323 condition. Routed (see C2). |
| S206 | tier A spec, anchor "correction minimum standards and version-control paragraph" | **anchor matches; teaches cell omits the operative rule (routed, feeds K3)** | f221c90f lines 212–222. Teaches cell "mark earlier electronic versions as superseded, so a reader can tell which version was cited" leaves out line 222: "The citation should be to the most recent version." That omission is why the correction entry's "cite the version read" row was written against its own source. |
| S207 | tier A docs, anchor update-cadence/types paragraph | **matches** | 43a45b49 line 393: "updated every working day"; "not as comprehensive as retractions". Teaches cell's "no-hit is weaker" is a fair paraphrase. |
| S208 | REJECTED, unreachable, flip condition stated | **matches** | refetch.tsv 2026-11-06 row (`curl rc 22, HTTP 403`). Rejected row correctly teaches nothing. Used as warrant in T7 (see above). |

## Residual notes

- No K1/K2/C2 work was done by this seat (leaf; scope is K3 only).
- `tools/quote-reopen.py` not run (no re-open in this seat's scope; no network used).
- Tools installed: none. Scratch `/fast/scratch/hyaku/chousa-r81/R81ReviewerEntries` deleted before yield.

VERDICT: R81ReviewerEntries C1 fired — K3 fires on correction entry row "A newer article version exists" (cites S206): the row says cite the version read, and S206 line 222 says "The citation should be to the most recent version."
