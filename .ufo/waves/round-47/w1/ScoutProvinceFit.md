# ScoutProvinceFit — round 47 wave 1

**Item:** province check of the two staged C3 entries against `PROVINCE.md` (chousa owns claim-vs-source verification; refuses model-quality or evaluation claims → kengaku). Judge each sentence-group in or out, name sentences to drop, and grep `kengaku-shokunin/corpus/` for FEVER, CFEVER, climate-fever, CorFEVER and PEOPLEPROFILES.
**Seat:** scout, leaf. No fetch, no lane writes except this file, no installs, no scratch dir used. `skill://godspeed` did not resolve on disk (`ls ~/.omp/agent/skills | rg -i godspeed` printed nothing); ran under the dispatch text only.

## Inputs (sha256)
- staged base `claim-support-test-r37.md`: `65544cca5c9b67822dc84107ef31d38d633b4eb9367770a95ef5c23f4ba68597` (83 lines)
- staged amendment `claim-support-test-r37-amendment-2026-10-23.md`: `a6a932cdf981979fe294f9cdc7e040ac2a51257b5eb95e450b4a6395a01eb27e` (91 lines)
- `PROVINCE.md:10-11` — "Refuses: … model-quality or evaluation claims (→ kengaku)"
- captures (byte counts from `wc -c`): S090 `4132ec1b…` 91084, S092 `b502d4c6…` 70165, S093 `44be8711…` 53020, S094 `a9cf4170…` 83246

## Precedent (observed)
The lane already holds a FEVER-based entry: `corpus/knowledge/evidence-pool-versioning-r39.md:1,3` (S085, the dataset page's Data Format section). `round-46-verifier-spotcheck.md:36` records it as "admitted … AGREE". So the lane has already admitted a dataset's **schema and annotation protocol** as research method. The test for each sentence below is the same: does it state a rule that a human or a checker applies, or that rule's human reliability (in province)? Or does it state how a model or system performs (out of province, kengaku)?

## Kengaku grep (`rg -n -i 'fever|cfever|climate-fever|corfever|peopleprofiles' kengaku-shokunin/corpus`)
```
kengaku-shokunin/corpus/knowledge/eval-design-digest-3.md:65:   35.1 EM / 64.6 Fever, better than either alone; each branch covers the
```
That is 1 hit (count mode: `eval-design-digest-3.md:1`). It is a **model score on FEVER** (ReAct↔CoT-SC hybrid, digest of the ReAct paper note, `:3-11`). This is exactly the kind of statement kengaku owns. There are zero hits for CFEVER, climate-fever, CorFEVER or PEOPLEPROFILES. Neither staged entry cites any model score, so there is **no overlap or collision** with kengaku. Outside `corpus/`, kengaku has no hits at all (`rg … kengaku-shokunin --glob '!corpus/**'` returned nothing).

## Verdict per sentence-group: base entry `claim-support-test-r37.md`
| lines | group | verdict |
|---|---|---|
| 13-18 | PEOPLEPROFILES Definitions 1/2 (counterfactual support/refute test) | **IN**: a stated support rule |
| 19-25 | absence is an outcome; FEVER NEI declared-null tuple | **IN**: dataset schema as method (same as r39) |
| 26-30 | CFEVER label set + evidence requirement | **IN**: schema |
| 31-34 | "measured failure rate … ~22 / ~30 per cent unsupported" | **OUT-LEANING. Drop** (see F1) |
| 38-43 | support = evidential strength, not entailment or embedding similarity | **IN** |
| 44-52 | three-way label + evidence field maps to lane states (r24) | **IN** |
| 53-58 | Chinese literature applies the same shape | **IN** (calibration note F4) |
| 59-65 | "22 and 30 per cent figures are a warning … roughly a third of real citations do not support" | **Drop**: it depends entirely on lines 31-34 (F1, F2) |
| 69-72 | Unknown: agreement and human-vs-model drift "not read" | **IN, but false as written. Rewrite** (F3) |
| 73-75 | Unknown: decision procedure vs annotator label | **IN** |
| 76-78 | Unknown: "FEVER paper … only as an abstract via aaron (1,502 characters)" | **IN, stale** (F4) |
| 79-81 | Unknown: not the only support test | **IN** |

## Verdict per sentence-group: amendment
| lines | group | verdict |
|---|---|---|
| 13-23 | FEVER Task 2 guideline: decision question, evidence boundary, Skip/NEI | **IN**: the procedure itself |
| 24-31 | climate-fever per-sentence human labels → aggregate claim label incl. Disputed | **IN**: protocol |
| 32-37 | CorFEVER Cohen κ 0.792 (human annotators) + 202 NEI relabelled | **IN**: human reliability of the test and evidence-relativity. Not CorXFact system results |
| 38-39 | FEVER Fleiss κ 0.6841 | **IN**: human 5-annotator agreement (S092 char 18018: "annotated by 5 annotators … Fleiss κ … 0.6841"), so "five-way" at line 49 is correct |
| 43-51 | Q10 yes with two qualifications; "a semantic arm would need a model or a human" | **IN**: a lane design statement, no model-quality claim |
| 52-61 | NEI is evidence-relative (202 relabelled) | **IN** |
| 62-67 | granularity cost (Disputed, per-sentence unit) | **IN** |
| 68-72 | span-plus-verdict-plus-evidence-set | **IN** |
| 76-81 | Unknown: procedure vs annotator protocol | **IN** |
| 82-85 | Unknown: "FEVER's evidence-retrieval figures were not read … middle was truncated" | **IN, but false. Rewrite** (F5) |
| 86-89 | Unknown: climate-fever per-sentence agreement "outside the portion opened" | **IN, but false. Rewrite** (F6) |
| 90-91 | "No claim is made here about any model's agreement" | **IN**: this is the province fence. Keep |

**Net:** no amendment sentence is out of province. In the base entry, drop **lines 31-34 and 59-65**, and rewrite Unknowns 69-72 and 76-78. After the drop, S090 still carries the Definition and "do not select any sentences" quotes (chars 80202 and 80684), so dropping the 22/30 bullet does not starve S090's ≥2-span leg [INFERENCE: C3 counter not run by this seat].

## Findings (pointers)
**F1: the 22/30 figures are measured from model-produced labels.** In S090, char 19400-20400 reads: "independently annotated two of the three batches … We then use these annotations to guide prompt engineering for the bulk annotation, assessing GPT-4o-mini on the same examples and aiming to optimize agreement with the human annotations". The abstract's "(1) ∼22% … (2) ∼30%" (char 1527 / 1617) is therefore an outcome of GPT-4o-mini bulk labelling [INFERENCE: the abstract does not restate the labeller; the 4o-mini bulk pass is the dataset-wide labeller per the passage above]. Line 31 calls this "measured … quantified". Keeping the figure honestly would require the labeller's reliability (F3), and that figure is a model-quality claim, which goes to kengaku. Drop both lines 31-34 and 59-65.
**F2: unit slip in base line 60.** "roughly a third of real citations do not support" is not what the source says. The source counts **claims** (lead ~22%, body ~30% "unsupported by their (public) sources", S090 char 1617; "unsupported by scrapable sources", char 6158), not citations. This is a second reason to drop 59-65.
**F3: base Unknown 69-72 is false against the capture.** S090 char 21103: "yield average pairwise α=66.3 and F1 =62.7 with respect to human annotations … only slightly below human expert agreement … (α=68.4)". Char 22007: "Evidence selection agreement is also on par with human expert agreement … (F1 =61.4)". So the figures were on disk. They are model-vs-human agreement (kengaku), so the rewrite should say "present in the capture, model-vs-human agreement, refused to kengaku". It should not say "not read" and should not import the numbers.
**F4: base Unknown 76-78 is stale.** The amendment cites S092 (arXiv HTML, 70165 chars), and the lane holds S086 (the NAACL PDF). The "abstract only, 1,502 characters" statement no longer holds for the adopted pair. This is calibration, not a province issue. Base line 57 ("does not need re-deriving in Chinese … without a translation caveat") overreaches one dataset (CFEVER). That is also calibration only.
**F5: amendment 82-85 is false.** S092 char 6516: "inter-annotator agreement of 0.6841 in Fleiss κ … in claim verification classification, and 95.42% precision and 72.36% recall in evidence retrieval". `rg -i truncat` over the capture finds 0 hits. These are **human** annotator evidence-retrieval figures, so they are in province. Rewrite to state them, or narrow the Unknown to "not adopted".
**F6: amendment 86-89 is false.** S093 char 16311: "For Task-2 we measured an average inter-annotator agreement (Krippendorff's alpha) of 0.334. This low level of agreement signifies the hardness of the task, i.e., even for human annotators…". This is human per-claim-evidence-pair agreement, in province, and it materially weakens the "per-sentence verdicts are the unit at which the judgement is reproducible" line (64-65).
**F7: out-of-province material is present in the sources but not cited (keep it that way).** S094's contribution is CorXFact, "an LLM-based framework" (char 3746). S093 has "2.4 Entailment prediction" and "C Baseline evaluation" (chars 13442, 966). S092 is "a pipeline approach" baseline (char 6516+). Any later span or row drawn from these sections would be a model-evaluation claim and belongs to kengaku.
**F8: column interleave in the S090 abstract.** Raw char 1520-1625 is `'  (1) ∼22% of claims in Wikipedia lead sections\n        are unsupported by the article body; (2) ∼30%    '`, followed by the inserted figure label "Cited source". This explains why the register row (`absent-defect-register.md:43`, chousa round2 S093 = this PDF) found the ~30% quote "payload-absent". It is moot if F1's drop is taken.

## Commands run (decisive output)
- `sha256sum` / `wc -l` on both staged entries → hashes above; 83 and 91 lines.
- `rg -n -i 'fever|…|peopleprofiles'` on kengaku corpus → 1 hit (above). Outside corpus → none.
- `rg … chousa-shokunin/corpus --glob '!evidence/round47/**'` → r39 base/amendment, round-46 lesson:306/313, spotcheck:36, round42 quarantine-verdicts.tsv:14 (S108 FEVER arXiv 69/108 run).
- `rg -n -i 'province|kengaku|evaluat|model'` on `round47/claims.md` and `QUALITY.md` → no hits. No frozen predicate is touched by this province judgement.
- python `re` slices over the captures → the char offsets quoted in F1-F8.

## Confidence and gaps
- High: the IN verdicts (guideline, schema, human κ) and F5/F6/F3 (verbatim capture text).
- Medium: F1. It rests on the 4o-mini bulk-labelling passage. Whether the abstract figures were computed on the human-annotated batches or on the bulk set was not traced beyond chars 18900-22400.
- Not done (out of scope): C1/C2/C3 counters, quote-offset location for spans.tsv, and the quarantine rows.
