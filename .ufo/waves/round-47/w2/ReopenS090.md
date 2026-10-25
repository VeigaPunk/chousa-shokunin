ATTACKS: S090 registry row (SOURCES.md:100) and every sentence citing S090 in corpus/knowledge/claim-support-test-r37.md
VERDICT: holds

## 1. Anchor-cell char slices (task item 1)
Capture: /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/4132ec1b265e60624523251f.txt (91084 bytes, 90692 chars; sha256 2f8047a877c390f819c83ee1079ca8229ab16ce461c5f2f45304b33931224997, matches spans.tsv capture_sha256).
Python check, every stated char offset, capture[N:N+len(quote)]==quote and count==1:
- char 1526 "∼22% of claims in Wikipedia lead sections" match count=1
- char 1576 "are unsupported by the article body; (2) ∼30%" match count=1
- char 1669 "of claims in the article body are unsupported" match count=1
All three verified. No failure.

## 2. Every quoted string cited to S090 (task item 2)
All double-quoted/backticked strings in the entry attributed to S090, verbatim in capture, offset (char index of first char), count=1:
- "A set of sentences S provides supporting evidence for a claim c if, supposing the contents of S" @80077 (Def 1 first clause; split across newline: gap raw[80169:80173]=="f S\nwe", so "…contents of S" ends 80169, "\nwe" begins 80173)
- "were true, it would give you greater reason to believe that c is true, all else equal." @80173
- "true, it would give you greater reason to believe that c is false, all else equal." @80394 (Def 2, verbatim, count=1)
- "Select 0, 1, 2, or *at maximum* 3 sentence(s)" @80487 (Step 1, verbatim)
- "a scale from -1 to 1:" @82148 (Step 2, verbatim)
- "0: The claim is neither supported nor refuted. It is equally likely to be true or false." @82467
- "∼22% of claims in Wikipedia lead sections" @1526
- "are unsupported by the article body; (2) ∼30%" @1576
- "of claims in the article body are unsupported" @1669
- "by their (public) sources" @1723
- "ported by scrapable sources" @6302
- "to paywalled and print sources for all articles." @23238
- "of 160 body claims obtained from 10 randomly" @24245 (§3.4 Pilot Annotation, heading @23725)
- "Using GPT-4o-mini with the best prompt" @22373 (§3.5 Bulk Annotation, heading @22281)
- "ceivably provide a rough upper bound on the degree" @20882
Count=1 for each. No failure. Unquoted offsets 20954 ("average pairwise α=66.3 and F1 =62.7 with respect to human annotations" — agreement figure the entry leaves to the evaluation lane), 82148/82467 confirmed above.

## 3. Offsets stated in source: line (task item 3)
source: S090 line (r37.md:4) states chars 1526, 1576 (two support rates), 24245, 20954, 22373 (§3.4/§3.5), 80077, 80394, 80487 (Definitions 1-2, Step 1). All confirmed above; 20954 sits mid-column in the interleaved two-column capture and is the human-agreement/F1 figure. No failure.
Span manifest cross-check: spans.tsv offset column = span-file start = quote char offset −80 (e.g. S090-4 @1446 vs char 1526; S090-1 @80122 vs char 80202; S090-2 @80407 vs char 80487; S090-8 @79997 vs char 80077). build-spans.py --check: SPANS_ROWS=35 STALE=0.

## 4. Observation/Inference sentence judgments (task item 4)
- L12 counterfactual twice: SUPPORTED verbatim (Def 1 @80077/80173, Def 2 @80394).
- L14 absence-of-evidence outcome: "Select 0…" @80487, scale @82148, midpoint @82467 all verbatim; "0" selection = no sentences, corroborated by Step 2 "-1… fully refuted: The claim would have to be false, supposing the sentences you selected were true" and "Scores between…0… equally likely" (@82239, @82841 supposing clauses). SUPPORTED.
- L17 pilot/bulk: "of 160 body claims obtained from 10 randomly" @24245; "Using GPT-4o-mini with the best prompt" @22373; agreement figure @20954 left to evaluation lane. SUPPORTED.
- L18 failure rates: all five slices verbatim (1526, 1576, 1669, 1723, 6302, 23238). SUPPORTED.
- L22 evidential strength under supposition: quote "greater reason to believe that c is true, all else equal" verbatim; "supposing the contents of S" appears in BOTH Definition 1 (@80145) and Definition 2 (@80361). "greater reason to believe that c is true" is the Def-1 clause; Def 2 mirrors with "c is false" — the sentence says "both definitions… ask whether that would give `greater reason to believe that c is true, all else equal`", i.e. both definitions ask whether supposition gives greater reason to believe the claim true. Read charitably as the common supposition clause of both definitions (each definition's evidential-strength-under-supposition form), supported. If strict "both definitions literally share the c-is-true clause", the mirrored clause is Def 2's c-is-false variant — a wording nicety, not a factual defect.
- L24 empty evidence set: "Select 0…" @80487; FEVER clause is S085. SUPPORTED.
- L25 three-way vs scalar: "a scale from -1 to 1:" @82148. SUPPORTED.
- L27 rates warn about input at scope measured: quote slices verbatim; "measured on model labels" supported: §3.5 "Using GPT-4o-mini with the best prompt identi-fied in the pilot" @22373 (bulk annotation produced by model with best prompt); abstract rates are of the dataset/annotations. No defect.
- L34 outside biographies: "ceivably provide a rough upper bound on the degree" @20882 ("of evidential support for claims in Wikipedia arti-" @20961). SUPPORTED.

## Findings
No failure, no overstated sentence, no contradicted sentence in S090 registry row or entry citations. C3 S090 leg holds.

Verification gaps: none. No tools installed. Scratch /tmp/chousa-r47w2-ReopenS090/ deleted.
