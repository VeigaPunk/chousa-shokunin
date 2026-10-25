ATTACKS: S091 registry row (SOURCES.md:101), every claim-support-test-r37.md sentence citing S091, capture reopen (3749141b52b2dbb2e0e821c3.txt)
VERDICT: holds

Capture: /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3749141b52b2dbb2e0e821c3.txt (66,321 chars; sha256 0b3518bf2d2ba3047212d6f4ccb83dfd1cf01960e51acb324f7b74b6b2730573, matches spans.tsv).

## (1) Anchor cell `char N: <quote>` checks (all pass, count==1)
- char 966 "Each claim in CFEVER is labeled as “Supports”," → seg match True, count=1
- char 1567 "a Fleiss’ kappa value of 0.7934 for five-way inter-annotator" → True, count=1
- char 10406 "and CHEF are 0.6841 and 0.74, measured from 4% and 3%" → True, count=1

## (2) Every quoted string in entry attributed to S091 — all verbatim, offsets listed
All `seg_match=True` at the cited offset (Python):
- "could support or refute a claim, the claim was labeled as" 24458 (count 1)
- "CFEVER comprises 30,012" 810 (1)
- "Each claim in CFEVER is labeled as “Supports”," 966 (1)
- "“Refutes”, or “Not Enough Info”" 1043 (count 2 — see note)
- "evidence sentences sourced from single or" 1328 (1)
- "text written in Chinese tends to be more" 4151 (1)
- "a Fleiss’ kappa value of 0.7934 for five-way inter-annotator" 1567 (1)
- "over the 1,936 claims shows a score of 0.7934 in Fleiss κ" 28442 (1)
- "and CHEF are 0.6841 and 0.74, measured from 4% and 3%" 10406 (1)
- "another 700 claims (2.33% of the dataset) for being reviewed" 29246 (1)
- "We discovered that 84.4% of the claims are" 24549 (1)
- "annotated correctly with correct evidence sentences." 24667 (1)
- "The Thirty-Eighth AAAI Conference on Artificial Intelligence (AAAI-24)" 37 (count 9 — running header each page)
- "Copyright © 2024" 6351 (1)

Note: "“Refutes”, or “Not Enough Info”" appears twice in the capture: char 1043 (abstract, cited) and char 20796 (paper's Annotations-Platform section: "the claim as “Supports”, “Refutes”, or “Not Enough Info”. For the first two categories, the annotator must also find…"). The entry cites the abstract occurrence (1043) — correct.

## (3) Char offsets stated by `source:` line / entry — all confirmed
810 (abstract claim count), 966, 1567 (abstract), 24458 (NEI rule: "Once the annotator considered no factual sentences in our fact database could support or refute a claim, the claim was labeled as “Not Enough Info.”"), 28442 ("The five-way inter-annotator agreement over the 1,936 claims shows a score of 0.7934 in Fleiss κ (Fleiss 1971), which is higher than the score of 0.6841 mea-sured with 7,506 claims (4% from total) in FEVER … and the one of 0.74 with 310 claims (3% from…"), 29246 ("To evaluate the correctness of the evidence sentences, we randomly sampled another 700 claims (2.33% of the dataset) for being reviewed"), 24549/24667 ("We discovered that 84.4% of the claims are annotated correctly with correct evidence sentences." — "by the authors." sits at 24533 in the right column, joining the 700-claims clause), 37/6351 (header/copyright). All seg-verified.

## (4) Sentence judgments (all SUPPORTED; no overstatement/contradiction found)
- Obs L14 NEI rule: supported. Verbatim; gloss "no factual sentence in its fact database" matches "no factual sentences in our fact database" (singular/plural trivial).
- Obs L15 three-way label on Chinese Wikipedia: supported. Abstract confirms 30,012 claims over Chinese Wikipedia; "first two categories carry evidence sentences sourced from single or multiple pages" = "claims in the 'Supports' and 'Refutes' categories are also annotated with corresponding evidence sentences sourced from single or multiple pages in Chinese Wikipedia".
- Obs L15 Chinese ambiguity: supported. Capture: "Compared to English, text written in Chinese tends to be more ambigu-[n] ous and nuanced, making it…" — quote truncates at "more"; glossary "ambiguous and nuanced than English" is faithful (hyphen wrap across columns at 4191/4333; "nuanced" at 4341). Minor: the words "ambiguous and nuanced than English" are not contiguous in capture (they span the line/column split); meaning intact.
- Obs L16 kappa: supported. Abstract "holds a Fleiss' kappa value of 0.7934 for five-way inter-annotator agreement" + detail "over the 1,936 claims shows a score of 0.7934 in Fleiss κ".
- Obs L16 FEVER/CHEF scores: supported. Full sentence: "while the scores in FEVER and CHEF are 0.6841 and 0.74, measured from 4% and 3% of claims from the datasets, respectively"; cross-confirmed by the 28442 passage (0.6841 = FEVER kappa on 7,506 claims/4%, 0.74 = CHEF on 310 claims/3%).
- Obs L16 700-claims review: supported. "randomly sampled another 700 claims … for being reviewed [by the authors. We discovered that 84.4% of the claims are annotated correctly with correct evidence sentences]" — quotes verbatim; the "by the authors." fragment (24533) carries the join.
- Inf L23/L25/L26/L28: each cites a verbatim S091 quote and the inferences (pool-dependent third label; same three-way shape; kappa/84.4% reliability bound; 0.6841 restates FEVER agreement cross-checked to S086) are supported by capture context.

## Registry summary cell
"30,012 manually created claims over Chinese Wikipedia are each labelled Supports, Refutes or Not Enough Info, and the Supports and Refutes claims are also annotated with evidence sentences from one or more Chinese Wikipedia pages, so the FEVER label set and evidence requirement carry over to Chinese unchanged" — supported by abstract; "carry over unchanged" is the lane's inference but faithful ("Similar to the FEVER dataset…").

## Counter runs
- python3 corpus/evidence/round47/c3-count.py → C3=PASS (ENTRIES=2/2, CITES_BOUND=6/6, QUOTE_ROWS=35, SPAN_IDS=6/6, QUOTES_IN_SPAN=35/35, QUOTES_IN_ENTRY=35/35, SPAN_CONTEXT=35/35, CAPTURE_BOUND=35/35, REF_ID_UNBOUND=0, ANCHOR_BOUND=6/6, INFERENCE_GROUNDED=2/2, QUARANTINE_VERDICTS=4/4, QUARANTINE_ABSENT_ADOPTED=0)
- build-spans.py --check → SPANS_ROWS=35 STALE=0

## Findings / residual observations (no defects)
1. NO failure found: every S091 anchor cite, entry quote, and stated offset verified verbatim against the capture; count==1 except the two benign duplicates (Refutes phrase, running header) that are not the cited occurrences.
2. Machine-coverage gap (not a defect): entry-only quotes not represented as span rows (e.g. 1043, 1328, 4151, 24458, 28442, 29246, 24549, 24667, 6351) are not checked by c3-count (which validates only anchors via span-row offsets). Manually verified here; the counter would not catch a silent corruption of these entry quotes.
3. Tooling: no tools installed/updated (python3 stdlib used).

Residual risk: low. Verification gap: the only non-machine-checked strings are the entry-only quotes (covered manually above).
