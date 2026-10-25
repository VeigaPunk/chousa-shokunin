# ReviewOpenS093 — round 47 wave 1 — open lane S093 (climate-fever, arXiv:2012.00614v2)

Item: open lane S093 (staged S114 → lane S093 by URL equality) from its on-disk capture; locate grounding
quotes for its Registry row and the entry; check staged sentences against the capture. No fetch made.
Seat: reviewer, leaf. No installs. Scratch /tmp/chousa-r47-ReviewOpenS093/ created and removed.
## Capture identity
- Path: /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/44be8711b50a9daae2865b02.txt
- `sha256sum` → `ab3427c377d1991032d5165cbb6f08bb6ea29d964dda78b2363811dc0c2b2ba4`
- `len(capture)` (Python str, utf-8) → `52704` chars
- Binding check: `echo -n 'https://arxiv.org/html/2012.00614v2' | sha256sum` → `44be8711b50a9daae2865b02e1d9…`,
  so the filename prefix equals sha256(url)[:24]. The capture is this URL.
- Completeness: this is an HTML render (math markup present, e.g. `2.4 ± ± 0.7 2.4\pm\pm 0.7` at 15066+). The capture
  runs from the arXiv header through Appendix D.4 (`D.4 Subtle` at 47853) to the arXiv footer (tail = "About · Help ·
  Contact …"). An apparent `t…` at 14241 was a display cut by the tool, not a capture truncation:
  the codepoints after `For measuring t` are `0x68 0x65 0x20` ("he ").
  The only `…` characters are at offsets 37971, 39380 and 46436, and all three are the paper's own text.

## Candidate quotes (str.find offset, count)
| candidate | verbatim? | offset | count | note |
|---|---|---|---|---|
| `1,535 real-world claims` | **NO** | -1 | 0 | The capture says `We collect 1,535 claims on the Internet.` (4846). "real-world claims" occurs 6× but never next to the number. Use q1. |
| `7,675 annotated claim-evidence pairs` | yes, contiguous | 5157 | 1 | Full sentence q3 at 5132. |
| per-sentence SUPPORTS/REFUTES/NOT_ENOUGH_INFO | yes | 6780 (first) | 11 / 11 / 11 | Not unique as tokens. Use the unique sentences q2 (human labels) and q5 (micro-verdict). |
| claim-level `DISPUTED` | yes | 13442 (first) | 3 | Unique carriers: q7 (§2.3 rule) and q14 (Appendix D rule). |
| Appendix D worked example | yes | D.3 intro 44806; Example D.5 `Verdict: \n \n \n Disputed` 46553 | — | The verdict block is whitespace-laden, so quote q13 instead. |

Context, 100 chars on each side (verbatim `repr`):
- q1 @4846: before `'. In this work, we focus on building a dataset of real-world claims specifically on climate change. '`;
  after `' For each claim, we algorithmically retrieve the top five relevant evidence candidate sentences from'`
- q3 @5132: before `'tate each sentence as supporting, refuting, or not giving enough information to validate the claim. '`;
  after `' 1 1 \n 1 \n \n \n \n We make this dataset publicly available at http://climatefever.ai . .\n\n\n\n \n \n 2 Met'`
- neg2 @5157: before `'porting, refuting, or not giving enough information to validate the claim. We call this database of '`;
  after `' the climate-fever dataset. 1 1 \n 1 \n \n \n \n We make this dataset publicly available at http://climat'`
- q7 @13373: before `'y default NOT_ENOUGH_INFO unless there is supporting ( SUPPORTS ) or refuting ( REFUTES ) evidence. '`;
  after `'\n\n\n\n \n \n 2.4 Entailment prediction\n\n\n \n For entailment prediction, the top five candidate evidence s'`
- q10 @16261: before `'set provides both the micro-verdict labels and the claim-labels for each claim-evidence pair.\n\n\n\n \n '`;
  after `' This low level of agreement signifies the hardness of the task, i.e., even for human annotators, it'`
- q13 @44806: before `'…Verdict: \n \n \n Refutes \n …\n D.3 Disputed claims\n\n\n \n '`;
  after `' Such examples are especially interesting since the original fever dataset does not contain such exa'`
- q14 @37620: before `'ll others are NOT_ENOUGH_INFO ; it is NOT_ENOUGH_INFO , if all micro-verdicts are NOT_ENOUGH_INFO ; '`;
  after `'\n\n\n\n \n D.1 Supported claims\n\n\n \n The following claims were all supported by evidence sentences retri'`

## Verified quote set (TSV; every row count=1, 4–25 words, slice_eq=True)
```
id	offset	quote
S093-q1	4846	We collect 1,535 claims on the Internet.
S093-q2	5021	humans annotate each sentence as supporting, refuting, or not giving enough information to validate the claim
S093-q3	5132	We call this database of 7,675 annotated claim-evidence pairs the climate-fever dataset.
S093-q4	12733	Given our 1,535 climate claims and five sentences per claim, we end up with 7,675 annotations.
S093-q5	13139	The micro-verdict is given by the majority-vote for each claim-evidence pair (or it is NOT_ENOUGH_INFO on a tie).
S093-q6	13253	The claim-label is by default NOT_ENOUGH_INFO unless there is supporting ( SUPPORTS ) or refuting ( REFUTES ) evidence.
S093-q7	13373	If there is both supporting and refuting evidence the claim-label is DISPUTED .
S093-q8	15147	The distribution for aggregate claim-labels SUPPORTS , REFUTES , DISPUTED , and NOT_ENOUGH_INFO is 655 (42.67%), 253 (16.5%), 153 (9.97%), and 474 (30.88%).
S093-q9	15349	we include claims for which both supporting and refuting evidence were found.
S093-q10	16261	For Task-2 we measured an average inter-annotator agreement (Krippendorff’s alpha) of 0.334.
S093-q11	16354	This low level of agreement signifies the hardness of the task
S093-q12	16539	Table 1 details the level of disagreement on a per-slice basis.
S093-q13	44806	For the following claims contradictory evidence was found by the ecrs as labelled by the annotators.
S093-q14	37620	otherwise the claim-label is DISPUTED .
```
Check (Python; `c = open(capture).read()`; for each: `o=c.find(q); n=c.count(q); c[o:o+len(q)]==q`), verbatim result lines:
```
S093-q1	off=4846	count=1	words=7	len=40	slice_eq=True
S093-q2	off=5021	count=1	words=16	len=109	slice_eq=True
S093-q3	off=5132	count=1	words=12	len=88	slice_eq=True
S093-q4	off=12733	count=1	words=16	len=94	slice_eq=True
S093-q5	off=13139	count=1	words=18	len=113	slice_eq=True
S093-q6	off=13253	count=1	words=19	len=119	slice_eq=True
S093-q7	off=13373	count=1	words=13	len=79	slice_eq=True
S093-q8	off=15147	count=1	words=23	len=156	slice_eq=True
S093-q9	off=15349	count=1	words=12	len=77	slice_eq=True
S093-q10	off=16261	count=1	words=12	len=92	slice_eq=True
S093-q11	off=16354	count=1	words=11	len=62	slice_eq=True
S093-q12	off=16539	count=1	words=11	len=63	slice_eq=True
S093-q13	off=44806	count=1	words=16	len=100	slice_eq=True
S093-q14	off=37620	count=1	words=6	len=39	slice_eq=True
S093-neg1	off=-1	count=0	words=3	len=23	slice_eq=False
S093-neg2	off=5157	count=1	words=4	len=36	slice_eq=True
```
Byte traps: q6, q7, q8 and q14 contain a space before `,`, `)` and `.` (HTML token spacing). q10 uses U+2019 in
`Krippendorff’s`. A normalised or ASCII-apostrophe copy will not be found.
Backtickable 2+-word phrases include `1,535 claims`, `7,675 annotated claim-evidence pairs`,
`not giving enough information`, `claim-label is DISPUTED`, `average inter-annotator agreement`
and `contradictory evidence`.
Suggested anchor `char N` values: 5132 for the row (q3), 13373 for the Disputed rule and 16261 for agreement.

## Staged sentences this source SUPPORTS (amendment, `S114`; the base r37 entry never cites S114)
- Amendment lines 25–28 ("retrieved five candidate sentences for each of 1,535 real-world claims … 7,675 annotated
  claim-evidence pairs"). Supported by q1, q2, q3 and q4, and by "top five relevant evidence candidate sentences" (≈4960).
  "real-world claims" is paraphrase, not quotation, and MUST NOT be backticked as a quote.
- Amendment lines 28–31 ("worked examples show the per-sentence verdicts recorded separately and then an aggregate
  claim verdict, which can be **Disputed** …"). Supported by q13 and Example D.5, where Supports, Refutes and
  Not_Enough_Info appear per sentence followed by `Verdict: … Disputed` (46553), and by the rules q7 and q14.
- Amendment lines 62–64 ("four-way aggregate (including Disputed) exists because real claims have mixed evidence").
  Supported by q9 plus the next sentence "these examples … appear to be a common feature of real-world claims" (≈15427).
- Header recheck line 6 ("the '7,675 annotated claim-evidence pairs' sentence"). The sentence is present verbatim (q3).
- Staged SOURCES.append.md:39 (S114 row). Its claim text matches q1–q4 and q13. As above, its leading
  "1,535 real-world claims" is not verbatim.

## Staged sentences this source CONTRADICTS or overstates
1. **CONTRADICTED.** Amendment lines 86–89: "climate-fever's per-slice agreement figures were outside the portion
   opened, so the lane holds the aggregate label distribution but not its per-verdict reliability."
   The capture carries the overall figure (q10, "Krippendorff’s alpha) of 0.334") and the per-slice figures
   (q12 and Table 1 at 17118: α by slice 0.283, 0.399, 0.522, 0.106 (@17917), 0.215, 0.091, 0.252, 0.316, 0.431, 0.229).
   The capture is complete, so "outside the portion opened" is false for this capture.
   The entry also quotes no distribution; the distribution is q8.
   **Per-label agreement figures are NOT in the capture**: `per-label`, `per class`, `per-verdict` and `by label` all
   count 0, and Table 1 is per slice, giving α, total agreement and entropy over the classes. The corrected Unknown is
   "per-slice α read (0.091–0.522, mean 0.334); per-label agreement not reported".
2. **OVERSTATED (contradicted).** Amendment lines 64–65: "its per-sentence verdicts are the unit at which the
   judgement is reproducible." The source says the opposite: q11 "This low level of agreement signifies the hardness
   of the task", followed by "even for human annotators, it is non-trivial to decide if an evidence candidate supports
   or refutes a given claim" (≈16416). The alpha at that unit is 0.334.
3. **CALIBRATION OMISSION.** Amendment lines 49–51 give reliability as "0.6841 five-way Fleiss in FEVER, 0.792 Cohen's
   in CorFEVER" and omit S093's own 0.334, the lowest figure and the only one for real-world claims.
   The Inference "measured rather than perfect" understates it.
   These are different coefficients (Fleiss, Cohen, Krippendorff), so the entry should name each one and not rank them.
4. **ANCHOR SCOPE.** Header line 3 and the staged row's anchor say "section 1 and the appendix D worked examples".
   The aggregation rule (q5–q7) is in §2.3, the label distribution and agreement figures (q8–q12) are in §3, and the
   Appendix D rule (q14) is in the Appendix D preamble. The anchor must name §2.3 and §3 if those quotes are used.
5. **Base entry r37** does not cite S114. One of its Inferences is qualified, not contradicted, by S093: r37:44–45,
   "The three-way label with an evidence field is the whole contribution for a checker." S093 adds a fourth
   claim-level label, DISPUTED (q7), because real claims carry mixed evidence (q9).
   The amendment already concedes this (lines 62–67).

## Source-internal inconsistencies (residual risk; do not quote these as facts)
- "more than 1,535 verifiable climate claims" (10297) vs the exact "We collect 1,535 claims" (q1).
- "we collect five individual votes per claim-evidence pair" (12855) vs "labelled by at least two voters
  ( 2.4 ± ± 0.7 …" (15066). Table 1 lists 2.000–4.019 average voters per slice.
- Table 4 support column (≈34800–35560): SUPPORTS 474, NOT ENOUGH INFO 655. This is the reverse of the q8
  distribution (SUPPORTS 655, NOT_ENOUGH_INFO 474); REFUTES 253 matches. A row citing class counts should use q8.
- Label accuracy is 77.68% in §2.4 vs 77.58% in Appendix C, both on the fever dev set.

## Quarantine cross-note
The register id S093 is not lane S093. absent-defect-register.md:43 reads
`| chousa | round2 | S093 | payload-absent | https://aclanthology.org/2026.findings-acl.19.pdf |`, which is lane S090
by URL. arXiv 2012.00614 has no register row (`rg 'arxiv.org/html/2012|climate'` → no match), so lane S093 has no
absent-defect quarantine of its own. Register S114 (line 53) is a sinomed URL, unrelated to staged S114.

## Verdict
S093 OPENED. It can ground the row and the entry: 14 contiguous unique quotes verified, 3 or more required.
Two staged amendment sentences must be corrected before adoption, under the C3 kill rule "a staged sentence the
captures contradict is corrected … and recorded as a mistake": finding 1 (lines 86–89) and finding 2 (lines 64–65).
Findings 3 and 4 are calibration and anchor fixes.

## Commands run
`sha256sum` and `len` on the capture; `sha256sum` of the URL; Python `find`/`count`/slice checks (the outputs above);
`rg` over SOURCES.append.md, the absent-defect register, lane SOURCES.md and claims.md; `sed -n` on the staged row and
claims.md:95–140. Gaps: I did not run the C3 counter or inference-ground.py, since this seat only opens the source.
