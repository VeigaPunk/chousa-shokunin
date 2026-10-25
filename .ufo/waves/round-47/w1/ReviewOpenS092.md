# ReviewOpenS092 — round 47 wave 1: open S092 (arXiv v3 HTML of FEVER)

Item: open lane source S092 (https://arxiv.org/html/1803.05355) from its on-disk capture, locate the
quotes for its Registry row and the entry, check each candidate for contiguity, deliver at least three
contiguous unique quotes as TSV, map the source onto the two staged entries, and test whether the
quotes are absent from S086 (the NAACL PDF). No fetch was made. No tool was installed.
(`skill://godspeed` did not resolve: `ls ~/.omp/agent/skills` printed nothing. The axes taken from the
dispatch were operability, calibration and depth.)

## Capture identity
- S092 `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/b502d4c6a6ee023bee6f8531.txt`
  sha256 `e5b57b4875727b969a646b06b0df748e0efc8796aa1eeabc7c7ce5a2f2c85ac5`, 70165 bytes, **69681 chars** (Python `len`).
- S086 `.../.qcache/1c15b611118dee97e4105fcf.txt` sha256 `c508913aba177ae4d33b29b7076f305bbac578a1ea11d39e30ddee2d787d563f`, 60153 bytes, 60030 chars.
- S092 is the full paper and has every section heading: §3.2 Task 2 - Claim Labeling at char 14735, §3.4.1 5-way Agreement at 17863,
  Appendix A Annotation Guidelines at 46973, **A.6 Task 2 Guidelines at 56788**, A.7.1 What does it mean to Support or Refute a claim at 60453,
  **A.7.3 Skipping at 64612**, A.8 at 65769, Appendix B at 67874.

## Candidate quotes (Python `str.find` on the S092 capture)
1. `If I was given only the selected sentences, do I have stronger reason to believe claim is true (supported) or stronger reason to believe the claim is false (refuted)`
   — contiguous, find=60107, count=1, in A.6. It is **29 words**, which is over the 25-word cap. 100 chars either side:
   `…n presented in the Wikipedia page and dictionary.\n\n\n\n \n As a guide - you should ask yourself:\n\n\n\n \n ` [QUOTE] `. If I’m not certain, what additional information (dictionary) do I have to add to reach this conclu…`
   Replacement slice: `S092-A6-rule` (19 words, offset 60107). The §3.2 body has a variant at 15221 with **"strong reason to believe the claim is true"**.
   The same §3.2 variant is in S086 at 17294, split across lines (`do I have strong reason to be-` / `lieve the claim is true`).
2. `avoid applying your own world-knowledge` — contiguous, find=59925, count=1, in A.6. Context:
   `…pport or refute the claim.\n\n\n\n \n You must apply common-sense reasoning to the evidence you read but ` [QUOTE] ` by basing your decisions on the information presented in the Wikipedia page and dictionary.\n\n\n\n \n A…`
   The longer slice `S092-A6-bound` (offset 59858) also carries `common-sense reasoning`.
3. `by annotators achieving 0.6841 in Fleiss` — contiguous, find=2797, count=1, in the abstract. Context:
   `… sentence they were derived from.\nThe claims are classified as Supported , Refuted or NotEnoughInfo ` [QUOTE] ` κ \\kappa .\nFor the first two classes, the annotators also recorded the sentence(s) forming the nece…`
   The HTML renders math as `κ \kappa`: `'Fleiss kappa'` find = **-1**. So the staged wording "0.6841 in Fleiss kappa" is not verbatim.
   0.6841 appears 3 times in S092 (2821 abstract, 6516 intro, 18060 §3.4.1).
4. Skip / Not enough information — contiguous at find=59679, count=1 (A.6 step 4):
   `If you could not find any supporting evidence, press Skip then select Not enough information`. Context (100 before):
   `…e Wikipedia page. Press Submit if you could find information that supports or refutes the claim. ` … then `\n\n\n\n\n \n\n\n \n The objective is to find sentences that support or refute the claim.\n\n\n\n \n You must appl…`
   A.7.3 has a second, more specific form at 64837 (`S092-A73-nei`).

## Delivered TSV (`id<TAB>offset<TAB>quote`)
```
S092-A6-rule	60107	If I was given only the selected sentences, do I have stronger reason to believe claim is true (supported)
S092-A6-bound	59858	You must apply common-sense reasoning to the evidence you read but avoid applying your own world-knowledge
S092-A6-skip	59679	If you could not find any supporting evidence, press Skip then select Not enough information
S092-A73-nei	64837	If the claim could potentially be verified using other publicly available information. Select Not Enough Information
S092-abs-kappa	2797	by annotators achieving 0.6841 in Fleiss
S092-341-sample	17934	of claims which were not skipped to be annotated by 5 annotators
S092-intro-retr	6601	95.42% precision and 72.36% recall in evidence retrieval
```
Check (python3, verbatim output):
```
S092-A6-rule 60107 slice_eq= True find= 60107 count= 1 words= 19 in_S086= False in_S086_ws_norm= False
S092-A6-bound 59858 slice_eq= True find= 59858 count= 1 words= 16 in_S086= False in_S086_ws_norm= False
S092-A6-skip 59679 slice_eq= True find= 59679 count= 1 words= 15 in_S086= False in_S086_ws_norm= False
S092-A73-nei 64837 slice_eq= True find= 64837 count= 1 words= 16 in_S086= False in_S086_ws_norm= False
S092-abs-kappa 2797 slice_eq= True find= 2797 count= 1 words= 6 in_S086= False in_S086_ws_norm= False
S092-341-sample 17934 slice_eq= True find= 17934 count= 1 words= 12 in_S086= False in_S086_ws_norm= False
S092-intro-retr 6601 slice_eq= True find= 6601 count= 1 words= 8 in_S086= False in_S086_ws_norm= False
full candidate words 29
ascii apostrophe variant found: -1 curly: 15336 2
'Fleiss kappa' literal: -1
```
(`slice_eq` is `capture[offset:offset+len(quote)]==quote`. `in_S086_ws_norm` collapses all whitespace in both texts before matching.)
Phrases a bullet can backtick: `selected sentences`, `common-sense reasoning`, `world-knowledge`, `press Skip`,
`publicly available information`, `annotators achieving`, `5 annotators`, `evidence retrieval`.

## Is a separate row justified by content? (S086 grep)
- **Absent from S086 in substance.** S086 has no `Appendix`, `Guidelines`, `Skip`, `common-sense`, `minimal amount` or `Not enough`
  (0 hits each), and it ends at the reference list on page 819. The A.6 and A.7.3 quotes (`S092-A6-rule`, `-bound`, `-skip`, `-A73-nei`)
  therefore exist only in S092. These quotes justify the separate row, and they sit under the headings **A.6 Task 2 Guidelines** and **A.7.3 Skipping**.
- **Absent only by layout; the fact is in S086.** `S092-abs-kappa` (S086 1869: `by annota-` / `tors achieving 0.6841 in Fleiss κ`),
  `S092-intro-retr` (S086 6741 is already the S086 row's slice), and `S092-341-sample` (S086 18320: `which were not skipped to be annotated by 5 an-`).
  These three do not justify a second row. They may ground S092 bullets, but they duplicate S086.
- A.7.1 (offset 60453) lists the valid support/refute justifications: synonym or antonym, negation or quantification, and a different entity.
  The staged row's locator cites A.7.1, but no staged sentence uses it, so the locator is unused.

## Staged sentences this source supports
- Amendment lines 14–21: the decision rule and the evidence boundary → `S092-A6-rule` and `S092-A6-bound`. Both are in A.6.
- Amendment lines 22–23: "if no supporting evidence is found, press Skip and select Not enough information" → `S092-A6-skip`. This is a paraphrase, correctly unquoted.
- Amendment lines 38–39 ("classified Supported, Refuted or NotEnoughInfo by annotators achieving 0.6841"), from the abstract at 2797.
- Amendment line 49 ("0.6841 five-way Fleiss") → §3.4.1 "5-way Agreement" at 17863 and 18060.
- Amendment lines 77–79 ("leans on common-sense reasoning") → 59873.
- Base entry lines 24–25 ("SUPPORTS and REFUTES each carry the sentence(s) that formed the necessary evidence") are also backed here, at 2876:
  `the annotators also recorded the sentence(s) forming the necessary evidence`. That line cites S097/S085, not this source.
- **Depth gain not in the staged entry:** A.7.3 (64837) defines NEI as "If the claim could potentially be verified using other publicly available
  information. Select Not Enough Information". This is FEVER's own text making NEI **evidence-relative**. The amendment's sharpest inference (lines 52–61)
  argues that point only from S115.

## Contradictions and overstatements (both sides quoted)
1. **Contradicted (calibration).** Amendment lines 82–85: "FEVER's evidence-retrieval figures were not read. The arXiv render's middle was truncated at
   open time … the lane therefore holds no figure for the reliability of the evidence step". The capture is complete, and at 6601 it reads
   `95.42% precision and 72.36% recall in evidence retrieval`. The lane also already holds that figure as S086 (SOURCES.md line 96, char 6737).
   This Unknown bullet must not be adopted as written.
2. **Contradicted.** Base entry lines 76–77: "The FEVER paper itself was retrievable only as an abstract via `aaron` (1,502 characters)".
   This capture is the full paper (69681 chars, with Appendix A). The bullet is stale on adoption.
3. **Not byte-verbatim (operability).** The amendment's quoted rule (lines 15–18) writes `If I'm not certain` with an ASCII apostrophe.
   The capture has U+2019: `If I’m` at 15336, count 2; the ASCII form finds -1. The quoted span is also 29+ words.
   It should be cut to `S092-A6-rule`, or the apostrophe should be fixed.
4. **Overstated.** Staged row S113: "a claim with no supporting evidence is explicitly skipped and labelled Not enough information".
   A.7.3 offers four Skip outcomes: NEI only "If the claim could potentially be verified using other publicly available information", plus
   `The claim is ambiguous or contains personal information`, the WF1-guidelines option, and the typo option. Skip does not imply NEI.
5. **Possible overstatement, [INFERENCE].** The amendment (lines 38–39 and 49) treats 0.6841 as the agreement of the three-way labelling.
   §3.4.1 measures it on `4% ( n = 7506 n=7506 )` `of claims which were not skipped to be annotated by 5 annotators` (17934).
   A.6 step 4 enters NEI via Skip (59679), so whether NEI claims are in the κ sample is not stated in the text. It should become an Unknown, not an equivalence.
6. **Tension, not contradiction.** Base entry lines 39–41 say support is "evidential strength … not … entailment". The guideline (A.6) is indeed
   "stronger reason to believe", but the paper's own verification stage is "Recognizing Textual Entailment" (heading §5.5 at 27933).
   The base entry should say the guideline (not the paper) defines support as evidential strength.
7. **Internal variant.** §3.2 at 15221 says "strong reason"; A.6 at 60107 says "stronger reason … believe claim". The staged recheck clause quotes the A.6 form,
   which is correct for an A.6 locator. A bullet citing §3.2 must use the §3.2 form.

## Commands run
- `sha256sum` and `wc -c` on both captures, plus Python `len(open(..,encoding='utf-8').read())` → the identity lines above.
- `find.py` (str.find, count and ±100 context for each candidate, in S092 and in S086) → offsets in §Candidate quotes.
- `re.finditer` heading scan and section dumps of 14800–15700, 17900–18700, 56788–60460 and 64612–65769 → the headings and section texts quoted above.
- S086 keyword grep (Python) → `'common-sense' 0`, `'Skip' 0`, `'Appendix' 0`, `'Guidelines' 0`, `'minimal amount' 0`, `'Not enough' 0`, `'strong reason' 1 [17294]`, `'95.42' 2 [6741, 20392]`.
- TSV verification → the block above. All scratch was under `/tmp/chousa-r47-ReviewOpenS092/` and is deleted.

## Verdict
S092 opens cleanly, and its row is **justified by content**: the A.6 decision rule, the evidence boundary, the Skip→NEI step and A.7.3's NEI definition
are absent from S086. Seven contiguous unique quotes are delivered, all `slice_eq=True`.
Before the entry is adopted, three fixes are needed: drop or rewrite the amendment's evidence-retrieval Unknown (finding 1) and the base entry's
abstract-only Unknown (finding 2), fix the apostrophe and length of the quote (finding 3), and correct the S113 row's Skip⇒NEI claim (finding 4).
Remaining risk: whether the κ sample covers NEI (finding 5) is unresolved from the capture.
