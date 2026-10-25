# Critic report — C3 field-policy inference (r41)

Seat: L1Chousa45.CritFieldPolicyInference · Round 45 wave 1 · 2026-10-25
Target: evidence-archive-field-policy-r41.md (staged) · Verdict: **inference fails as stated (over-reads); narrowed version holds.**

## Item assigned
Attack the r41 staged entry's inference: empty claim-level `cached_original_claim_url` "records that no archive was taken… not that none exists"; empty evidence-level `cached_source_url` "would be the anomaly". Also verify the entry's claim that "Where possible" occurs once in the paper and is about extractive answers.

## Commands run (verbatim, decisive lines)
1. `read` claims.md (frozen), r41 entry, README capture `ce16d57277fedfd4f0e7750e.txt` (4771 B), paper capture `412b146a2720ce6557268d05.txt` (144049 chars).
2. `grep "Where possible"` paper → line 3981: "…Where possible, we strongly prefer extractive answers." — **the only occurrence**.
3. `grep "cached_source_url|cached_original_claim_url|original_claim_url"` paper → **No matches found**.
4. `grep "cache all pages used as evidence"` paper → line 665: "To avoid sources disappearing from the web, we cache all pages used as evidence in the internet archive [3] https://archive.org ."
5. `grep "Where possible|archive.org"` README → line 18 `"cached_original_claim_url": "Where possible, an archive.org link to the original claim url"`; line 36 `"cached_source_url": "An archive.org link for the source url"`.
6. Python scans (eval): offsets, counts, heading location, newline variants.

## Verification of the entry's factual claims (all hold)
- README: "Where possible" occurs exactly once (char 1027; matches claims.md), "An archive.org link for the source url" at char ~1969 (archive.org at 1972; matches). Field names appear once each, in the JSON dictionary.
- Paper: "Where possible" occurs exactly once (char 121574, line 3981), inside section **J.4.6 Answer Generation** (heading at char 130161), on extractive answers — entry's claim correct, including "once".
- Paper: `cached_source_url`, `cached_original_claim_url`, `original_claim_url` occur 0 times — "README is the sole field definition" holds.
- "Archive.org returns a 404 page for these" at char 120884 (exact match). Caching sentence at char 14578 (claims.md says 14575; same sentence, 3-char count difference — immaterial).

## Counterexamples (strongest from the two captures)
**CE1 — documented alternative cause, same dictionary.** README line 17: `"original_claim_url": "If the claim first appeared on the internet, a url to the original location"`. A claim that never appeared online has no original URL → nothing to archive → `cached_original_claim_url` is necessarily empty with **no archiving decision at all**. The entry's causal attribution ("records that no archive was taken") ignores this documented conditionality sitting immediately above the field it cites; empty can simply mean "no original URL".
**CE2 — "Where possible" reads as availability, not choice.** The paper's proactive-caching sentence covers **evidence pages only**; nothing in the paper states claims are cached (the other archive mention is storing *fact-checking articles*, not claims). The README therefore defines the claim field as *a link to an archive.org copy of the original claim URL*, provided "Where possible". Plain reading: empty ⇔ no archive.org link could be provided (no accessible archived copy), not "we chose not to take one". The paper's own "Archive.org returns a 404 page for these" (char 120884) documents that archivability/availability genuinely fails — so "not possible" plausibly *includes* "attempt failed / no copy exists".
**CE3 — format description ≠ process record.** The README is a JSON field dictionary describing intended content; it records nothing about whether archiving was attempted. Concluding record-level semantics ("records that no archive was taken") elevates a schema doc into behavioral policy. The entry's own Unknown section concedes "may have been unarchivable, or archiving may have been skipped" — i.e. cause unrecorded — which contradicts the headline attribution.

## Verdict
Inference **fails as stated**: the positive half ("records that no archive was taken") is ungrounded; the safest supported statement is only "no archive link is recorded, for an undocumented reason". The *asymmetry* it documents is real and survives: evidence field described absolutely + paper's "we cache all pages used as evidence" vs claim field "Where possible".

**Narrowed sentence** (recommended replacement):
> AVeriTeC documents its two archive fields asymmetrically — `cached_original_claim_url` is best-effort ("Where possible"), whereas `cached_source_url` is described without qualifier and the paper says evidence pages are cached — so an empty claim-level field carries no recorded meaning beyond "no archive link is stored", while an empty evidence-level field would contradict the documented practice and is the anomaly worth investigating.

## Impacted axes
- C3 depth (assimilation quality): Observation accurate; Inference over-reads. The C3 predicate (quotes/counts in entries, spans, capture binding) is unaffected — kill rules still pass; this is a content-quality criticism, not a mechanical failure.
- Operability, calibration: unaffected (no Gates/tool/launcher interaction).

## Evidence pointers
- README capture: fields at chars 893–1055 (lines 17–18), 1948–1972 (line 36); "Where possible" @1027.
- Paper capture: caching sentence @14578 (line 665); J.4.6 heading @130161; "Where possible" @121574 (line 3981); archive.org 404 note @120884.

No tool installs made; no scratch files created; no writes outside the report file.
