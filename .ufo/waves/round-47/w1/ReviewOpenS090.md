# ReviewOpenS090 — round 47 wave 1: opening S090

**Assignment:** open lane source S090 (https://aclanthology.org/2026.findings-acl.19.pdf; staged id S098) from its on-disk capture. Locate the quotes for its Registry row and entry, check every candidate quote, deliver at least 3 contiguous unique quotes, and check the two staged entries against the source. No fetch. No tools were installed. Scratch `/tmp/chousa-r47-ReviewOpenS090/` was deleted.

**Verdict:** OPEN-OK, with corrections. None of the five candidate quotes is a contiguous match in the raw capture, because PDF line breaks and column interleave split them. The first four are each a single unique match once whitespace is collapsed. ABS30 does not match even then: the figure caption "Cited source" is spliced into the middle of it. There are 13 verified single-line replacement slices below. The staged entry overstates the 22%/30% figures, and its statement that the inter-annotator agreement "was not read" is wrong: the paper reports agreement.

## Capture identity
- Path: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/4132ec1b265e60624523251f.txt`
- `sha256 2f8047a877c390f819c83ee1079ca8229ab16ce461c5f2f45304b33931224997`
- 91084 bytes, **90692 chars** (Python str).
- The filename equals `sha256(url)[:24]` = `4132ec1b265e60624523251f` (checked).

## Commands run (decisive output)
1. `sha256sum` / `wc -c` / `python3` length and head → output as above. The title "How Grounded is Wikipedia? A Study on Structured Evidential Support and Retrieval" is at the head.
2. `python3 probe.py`: raw `str.find` for each candidate and a regex census:
   `D1 find=-1 count=0 | D2frag find=80418 count=1 | NOSEL find=-1 | ABS22(…lead sections) 1527 count=1 | ABS30 find=-1`
   Census: `'κ' 1 [25202]`, `'Krippendorff' 3`, `'Fleiss' 3`, `'Cohen' 0`, `'ACL 2026' 1 [4871]`, `'Definition' 2 [80040, 80260]`, `'at most three' 0`.
3. `python3 tsv.py`: whitespace-collapsed match for each candidate, mapped back to raw offsets, plus the TSV check (pasted below).
4. Context dumps of regions 1400–1800, 4700–5100, 5600–6500, 19900–25500, 28600–29950 and 79000–82700, read for the facts below.

## Candidate quotes (raw capture)
| id | raw find / count | ws-collapsed match → raw span | why not contiguous |
|---|---|---|---|
| D1 | -1 / 0 | 80077–80258, ncount 1 | `\n` after "contents of S" |
| D2 | -1 / 0 | 80295–80475, ncount 1 | `\n` after "contents of S were" |
| NOSEL | -1 / 0 | 80634–80711, ncount 1 | `\n` after "document provide" |
| ABS22 | -1 / 0 (prefix only: 1527 / 1) | 1527–1611, ncount 1 | `\n` plus 8-space indent |
| ABS30 | -1 / 0 | **no match even collapsed** | the right-column caption "Cited source" is interleaved between "(2) ∼30%" and "of claims" |

Verbatim 100 chars either side (Python `repr`):
- D1 L: `'both steps, rely on the following two definitions of evidence:\nDefinition 1: “Supporting evidence”:\n'` · R: `'.\nDefinition 2: “Refuting evidence”:\nA set of sentences S provides refuting evidence for a claim c i'`
- D2 L: `'ve you greater reason to believe that c is true, all else equal.\nDefinition 2: “Refuting evidence”:\n'` · R: `'.\n\nStep 1:\n\nSelect 0, 1, 2, or *at maximum* 3 sentence(s) from the document that provide the stronge'`
- NOSEL L: `'rom the document that provide the strongest\nsupporting evidence or refuting evidence for the claim. '` · R: `'.\n\nAdditional guidelines for Step 1:\n(a) You may need to use logic and common sense to *infer* that '`
- ABS22 L: `' on bio-\n        graphical Wikipedia articles. We show that:                   support\n        (1) ∼'` · R: `'; (2) ∼30%                           Cited source\n        of claims in the article body are unsuppor'`
- ABS30, raw text at 1611–1720: `'; (2) ∼30%                           Cited source\n        of claims in the article body are unsupported\n     '`. Fragments: `(2) ∼30%` at 1613, `by their (public) sources` at 1723 (each count 1).

The tilde in the abstract is U+223C `∼`, not ASCII `~`. The staged row's "at most three" does not appear in the capture; the prompt reads `*at maximum* 3 sentence(s)` (markdown asterisks in the capture). Replacement slices: D1 → q1+q2, D2 → q3, NOSEL → q4 (or `If no sentences in the document provide` @80634, 7 words), ABS22 → q12 or q5, ABS30 → q13 or q6.

## Quote set (all 13 pass `capture[offset:offset+len(quote)]==quote`, count=1, 4–25 words)
```tsv
id	offset	quote
S090-q1	80077	A set of sentences S provides supporting evidence for a claim c if, supposing the contents of S
S090-q2	80184	it would give you greater reason to believe that c is true, all else equal
S090-q3	80400	it would give you greater reason to believe that c is false, all else equal
S090-q4	80674	evidence, do not select any sentences.
S090-q5	28672	Indeed, 21.7% of lead claims are judged
S090-q6	28767	unsupported (≤ 0) by the body text and 29.5% of
S090-q7	82467	0: The claim is neither supported nor refuted. It is equally likely to be true or false.
S090-q8	20948	yield average pairwise α=66.3 and F1 =62.7 with
S090-q9	4812	Findings of the Association for Computational Linguistics: ACL 2026, pages 400–420
S090-q10	24474	of the authors annotated evidence sets and scalar
S090-q11	23121	sources as it is simply infeasible to obtain access
S090-q12	1527	22% of claims in Wikipedia lead sections
S090-q13	1669	of claims in the article body are unsupported
```
Check output (tsv.py, verbatim excerpt):
```
S090-q1	80077	…	# words=18 count=1 slice_ok=True 4<=w<=25:True
S090-q2	80184	…	# words=15 count=1 slice_ok=True 4<=w<=25:True
S090-q3	80400	…	# words=15 count=1 slice_ok=True 4<=w<=25:True
S090-q4	80674	…	# words=6 count=1 slice_ok=True 4<=w<=25:True
S090-q5	28672	…	# words=7 count=1 slice_ok=True 4<=w<=25:True
S090-q6	28767	…	# words=10 count=1 slice_ok=True 4<=w<=25:True
S090-q7	82467	…	# words=17 count=1 slice_ok=True 4<=w<=25:True
S090-q8	20948	…	# words=8 count=1 slice_ok=True 4<=w<=25:True
S090-q9	4812	…	# words=11 count=1 slice_ok=True 4<=w<=25:True
S090-q10	24474	…	# words=8 count=1 slice_ok=True 4<=w<=25:True
S090-q11	23121	…	# words=9 count=1 slice_ok=True 4<=w<=25:True
S090-q12	1527	…	# words=7 count=1 slice_ok=True 4<=w<=25:True
S090-q13	1669	…	# words=8 count=1 slice_ok=True 4<=w<=25:True
```
Phrases a bullet can backtick: q1 `supporting evidence`, q2/q3 `greater reason to believe`, q4 `do not select any sentences`, q6 `29.5% of`, q7 `neither supported nor refuted`, q8 `average pairwise`, q9 `ACL 2026`, q11 `simply infeasible`.

## Authors, venue and agreement
- **Authors visible:** yes, at chars ~200–420 of the head: `William Walden∗ Kathryn Ricci∗ Miriam Wanner Zhengping Jiang / Chandler May Rongkun Zhou Benjamin Van Durme / Johns Hopkins University`. This matches the staged row.
- **Venue visible:** yes, q9 @4812, followed by `July 2-7, 2026 ©2026 Association for Computational Linguistics` (count of `ACL 2026` = 1).
- **Agreement IS reported (§3.4, chars ~20850–22160).** The model labels from the final prompt on the pilot claims give `average pairwise α=66.3 and F1 =62.7 with respect to human annotations` (Krippendorff's α, interval difference function, on the scalar labels). The paper calls this "only slightly below human expert agreement reported for related works, including F (α=68.4) and VC (α=70.7)". It says the comparison is "indirect" and "to be interpreted cautiously". Human evidence-selection agreement: `pert agreement on these same examples (F1 =61.4).`, which starts at the hyphenated "human ex-|pert".
- The pilot was 160 body claims from 10 entities, annotated by 3 authors (q10). No human-vs-human α on PeopleProfiles' own scalar labels was found in the regions read. [INFERENCE] The 66.3 is a model-vs-human figure, not inter-human agreement.

## Staged sentences this source SUPPORTS
- r37 Observation 1: the D1 quote, and D2's "…greater reason to believe that c is false, all else equal." Supported, modulo the line break (q1+q2, q3).
- r37 Observation 2: "If no sentences in the document provide evidence, do not select any sentences." Supported, modulo the line break (NOSEL span 80634–80711).
- r37 Observation 4: "about 22 per cent of claims in Wikipedia lead sections are unsupported by the article body, and about 30 per cent of body claims are unsupported by their public sources". Supported by the abstract (`∼22%`, `∼30%`, `(public) sources`); the precise figures are 21.7% and 29.5% (q5, q6).
- r37 Inference 1: "defined as *evidential strength* ('greater reason to believe'), not as entailment". The definitional quote is supported. The contrast with entailment is the staged author's inference: `entail` occurs once (@57142, a reference) and the paper itself draws no such contrast.
- The staged row's authors, affiliation and venue: all supported (see above).

## Staged sentences this source CONTRADICTS or OVERSTATES
1. **Contradicted (r37 Unknown):** "The inter-annotator agreement figures … were not read." The capture reports α=66.3 / F1=62.7 (q8) and human evidence-selection F1=61.4. The fix is to quote them, not to keep the Unknown.
2. **Overstated (r37 Inference):** "If roughly a third of real citations do not support the claim they are attached to". The source says `29.5% of` body claims are judged `unsupported (≤ 0) by … their cited source text(s)` (q6). The unit is decomposed subclaims, not citations. The figure is under a third. It is measured on the **dev split**: "distributions for the P EOPLE P ROFILES dev split" (~24530). Only public sources are covered (q11). The judge is **GPT-4o-mini**, not humans: "Using GPT-4o-mini with the best prompt identi-" @22373; "Annotations were generated with temperature" @70603. The staged row's "measured rate at which real citations fail to support their claims" carries the same unit and judge drift.
3. **Overstated or mis-shaped (r37 Inference "three-way label … is the whole contribution"; row "if no sentence provides evidence, none is selected").** PeopleProfiles' verdict is a **scalar from -1 to 1**, not a three-way label. Step 2 reads "Determine the score according to the following definition of / a scale from -1 to 1:" (~82240), and 0 means "neither supported nor refuted" (q7). "Unsupported" here means a score ≤ 0, so it folds refuted and neutral together. The entry should not imply that S090 shares the FEVER/CFEVER three-way shape.
4. **Undercut (r37 Unknown "decision-procedures or only labels for trained annotators"; amendment Unknown "common-sense reasoning, which a program cannot perform").** In S090 the definitions sit inside an LLM prompt. The prompt was "selected based on highest agreement with the human pilot anno-" (~70210) and run at temperature 0 for bulk annotation of ~150K claims. That is a model applying the test with measured agreement (q8). The prompt itself demands it: "(a) You may need to use logic and common sense to *infer*…". The amendment does not cite S098, but its "a program cannot perform" is contradicted by this held source and should be qualified.

## Residual risk / gaps
- Only the regions listed in the commands were read. The full appendix (A.1 demographics, Table 8, the retrieval results) was not read in full.
- The PDF text layer may differ from the live PDF. No fetch was made, per fetch-scope L0 8d77e6c1.
- The offsets assume Python str indexing over UTF-8-decoded text. Byte offsets differ because of `∼`, `≤`, `α`, `“”`.
