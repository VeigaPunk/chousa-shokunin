# CritC3Inference — round 47 wave 1 — staged claim-support-test inferences vs captures

Item: attack four staged inferences of the two staged entries
`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/claim-support-test-r37.md`
(sha256 65544cca…68597, "E1") and `…-r37-amendment-2026-10-23.md` (sha256 a6a932cd…eb27e, "E2"),
checked against S090 (`4132ec1b….txt`, sha256 2f8047a8…224997), S092 (`b502d4c6….txt`, sha256
e5b57b48…ac5c5) and S094 (`a9cf4170….txt`, sha256 d24f2315…b136). Offsets are Python `str`
character offsets (`t.find(q)`) into the UTF-8-decoded capture. Lane HEAD a15610a5. No fetch, no
installs, scratch `/tmp/chousa-r47-CritC3Inference/` removed.

Verdict: **all four inferences overreach their sources; none can be adopted as written.** Each has a
narrower true sentence below. C3's leg "both entries exit 0 under tools/inference-ground.py"
does not detect any of the four (probe at the end of this report).

## 1. "support is defined as evidential strength … not as entailment" (E1:39-41)
- Source side (S090): Definition 1 @80202 "greater reason to believe that c is true, all else equal".
  The Step 2 scale @82812: "1: The claim is *fully supported*: The claim would have to be fully true,
  supposing the sentences you selected were true". Unsupported is a threshold on that score, @28767
  "unsupported (≤ 0)". Graded support is framed as kin to NLI, @14299 "partial support in related
  tasks—notably in natural language inference".
- Search: `entail` occurs once in S090, @57142, inside the bibliography title "WiCE: Real-world
  entailment for claims in Wikipedia". `not entail` occurs 0 times.
- Counterexample: the paper's top score is defined by necessitation ("would have to be fully true"),
  which is an entailment criterion. The contrast "not entailment" is the staged author's gloss, and the
  paper's own framing contradicts it. E1's further "not … a similarity score above a threshold" is
  half-right: support is not similarity, but "unsupported" is a cut (≤ 0) on a scalar score.
- Narrowest true sentence: *PEOPLEPROFILES defines supporting evidence counterfactually ("greater
  reason to believe that c is true, all else equal") and grades it on a −1…1 scale whose endpoint 1
  means the claim "would have to be fully true"; it does not contrast support with entailment.*

## 2. "roughly a third of real citations do not support the claim" (E1:59-66; observation E1:31-34)
- Source side (S090): abstract @1526 "∼22% of claims in Wikipedia lead sections are unsupported by the
  article body" and @1617 "∼30% of claims in the article body are unsupported by their (public)
  sources". Body text @28680 "21.7% of lead claims are judged unsupported (≤ 0) by the body text and
  29.5% of body claims by their cited source text(s)".
- Denominators. Neither figure counts citations or cited sources.
  - 22% is lead **subclaims** scored against the article **body**; no citation is involved.
  - 30% is body **subclaims** from sentences "that bear citations to publicly accessible sources"
    (@23007), scored against the scraped source text.
  - Both are dev-split rates (figure caption: "P EOPLE P ROFILES dev split"; dev has 256 articles and
    9,272 lead claims, Table 1 @~19500). The unit is decomposed subclaims (decomposition "using
    GPT-4o-mini" @~16200).
  - The labels are model labels, not human ones: @22373 "Using GPT-4o-mini with the best prompt
    identi-fied in the pilot … we collect support and evidence annotations on all 1,485 entities".
    Pilot agreement with humans is @20971 "α=66.3".
  - "Unsupported" (≤ 0) includes 0, "neither supported nor refuted" (@82400ff), as well as refuted.
    A further "32.6% of lead claims and 35.7% of body claims" (@29247) are partially supported.
- Counterexample: E1 merges two different measurements, swaps subclaims for citations, and rounds 29.5%
  up to "a third". The follow-on claim that existence-checking measures "a minority of the failure
  modes" has no failure-mode distribution in S090 behind it. It is unsupported.
- Narrowest true sentence: *In PEOPLEPROFILES' dev split, GPT-4o-mini labels (pilot α=66.3 against
  humans) score 21.7% of lead subclaims ≤ 0 against the article body, and 29.5% of body subclaims ≤ 0
  against their publicly accessible cited sources.*

## 3. "NOT ENOUGH INFO is a statement about the evidence … demonstrated … repeating exactly this error" (E2:52-61; obs E2:32-37)
- Source side (S094, two-column capture, so the sentence is split into fragments): @19801 "one in
  addition to the evidence from open websites."; @20104 "INFO" label in the original FEVER dataset
  have"; @20304 "we re-assign labels based"; @20794 "ENOUGH INFO" claims being relabeled.". The set
  is the **real-world** set (@21716 "Real-World Set"), not the closed-domain one. Table 2 gives the
  denominator: @17830 Closed-domain 333/333/333 and @17963 Real-world 426/443/131. NEI falls from 333
  to 131, i.e. 202 of 333 (60.7%) NEI claims move once open-web snippets are added.
- FEVER's own definition (S092 @16386): "NotEnoughInfo was used if the claim could not be supported or
  refuted by any amount of information in **Wikipedia**". NEI is relative to the evidence pool by
  definition.
- Counterexample: S094 never calls FEVER's NEI labels wrong. The 202 moves follow from changing the
  pool (Wikipedia, then the open web), which is exactly what FEVER's definition predicts. The passage
  shows evidence-pool relativity, not annotation error, so "repeating exactly this error" is a false
  attribution. Nor does it show the lane conflation ("no evidence found" vs "evidence found, does not
  support"). The moves are NEI to SUPPORT/REFUTE under a new pool, and S094 reports no relabel
  agreement or annotator for them.
- Side note: Table 2's arithmetic is off by one. SUPPORT gains 93 and REFUTE gains 110, a total of
  203 against 202 lost from NEI. The closed-domain rows sum to 999 against "We extract 1,000 claims"
  (@16218). This is a source-internal inconsistency worth one Unknown line.
- Narrowest true sentence: *CorFEVER re-assigned labels for its real-world set from open-web snippets,
  relabelling 202 of the 333 claims FEVER had marked NOT ENOUGH INFO (131 remain), which is consistent
  with FEVER defining NEI relative to Wikipedia; S094 does not say the original labels were errors.*

## 4. "0.6841 five-way Fleiss … 0.792 Cohen's" as the test's reliability (E2:49-51; obs E2:38-39)
- Source side (S092): @2821 "0.6841 in Fleiss κ" for "Supported, Refuted or NotEnoughInfo". The
  section name is "3.4.1 5-way Agreement" (@667). @17967 "to be annotated by 5 annotators" for "4%
  (n=7506) of claims which were not skipped".
- "Five-way" means five raters. There are three categories. E2's "five-way Fleiss" reads as five
  labels, which is false.
- The 0.792 figure is a different measurement. It covers two annotators labelling 1,043 claim-evidence
  pairs over **seven** correlation-degree labels (S094 Label 0 @16134 … Label 6 @13669, with κ at
  @21560 "annotator agreement is 0.792"). It is not a verdict κ, so setting it beside 0.6841 as "the
  test's reliability" compares unlike quantities.
- Narrowest true sentence: *FEVER reports Fleiss κ = 0.6841 among five annotators on a 4% sample
  (n=7506) for its three labels; CorFEVER's Cohen's κ = 0.792 is two-annotator agreement on seven
  claim-evidence correlation labels, not on the verdict.*

## Collateral falsifications (both "Unknown" blocks claim figures unread that the captures hold)
- E2:82-85 says "FEVER's evidence-retrieval figures were not read … truncated". But S092 @6601 has
  "95.42% precision and 72.36% recall in evidence retrieval". That figure is the evidence-step
  reliability the lane is said to lack.
- E1:69-72 says PEOPLEPROFILES' agreement figures "were not read". But S090 has @20971 "α=66.3",
  "F1 =62.7" and @22152 "F1 =61.4" (evidence-selection agreement).

## Gate probe: inference-ground.py does not catch these
Commands (scratch, since removed): a spans TSV with four exact capture quotes (S090 "greater reason
to believe that c is true", "of claims in the article body are unsupported"; S092 "0.6841 in
Fleiss"; S094 "claim-relevant evidence gathered from open"), a counts JSON `{"figures":
{"relabeled_nei":202}}`, and a probe entry whose Inference bullets restate the four defects.
`python3 tools/inference-ground.py --entry probe.md --spans spans.tsv --counts counts.json --root $D`:
```
GROUND entry=probe.md section=1 bullets=4 tokens=5 grounded=5
FINDING INF_POLARITY_FLIP bullet=2 token='of claims in the article body are unsupported / claim'
GROUND: FAIL   exit=1
```
The single finding is incidental. "do **not** support their **claim**" shares the stem `claim` with the
span. Rewording that bullet to "leave the attached assertion unbacked" gives
`GROUND: PASS exit=0`. Bullets 1, 3 and 4 passed unchanged. This matches the tool's named limit
(lexical only; "Semantics stay the critic's and the closure's to judge"). Earlier bare runs without
`--spans/--counts` exited 2 (usage).

## Impacted axes
- **depth (C3):** every lane adoption must replace the four inferences. As written they would land
  false provenance: entailment attributed to S090, citations attributed to S090, error attributed to
  S094, and five labels attributed to S092.
- **calibration:** the reliability numbers are mis-scoped, and two Unknowns are falsely open.
- **operability:** the C3 exit-0 leg is necessary but not sufficient. It cannot be used as evidence that
  the inferences hold.

## Smallest safe correction
1. In the lane entries, replace E1:39-41, E1:59-66, E2:49-51 and E2:52-61 with the four narrowest true
   sentences above, each citing its lane id (S090, S092, S094) and grounded by exact capture
   slices at the listed offsets. For S094, quote the fragments, because the full sentence is not
   contiguous: `find` of the joined sentence = −1.
2. Close E2:82-85 with S092 @6601 and E1:69-72 with S090 @20971/@22152. Add the Table 2 off-by-one
   (203 vs 202; 999 vs 1,000) as an Unknown.
3. Do not change any predicate, counter, fixture, floor or target. These corrections are text-only in
   the two entries and the spans rows.
