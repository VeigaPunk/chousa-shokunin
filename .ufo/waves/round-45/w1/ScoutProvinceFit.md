# Scout: ProvinceFit — round 45 wave 1

**Item:** Province check for the two staged AVeriTeC entries to adopt (C3 depth).

**Verdict: BOTH ENTRIES ARE IN PROVINCE.** Nothing needs cutting. No sentence in either entry is out of province.

## Deciding clauses (PROVINCE.md, /home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md)

- Line 5-8, Owns: "question framing; source hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution; claim-vs-source verification; search-strategy taxonomy; the external-target approval table for a research window; this lane's own corpus and gates."
- Line 10-11, Refuses: "bounty-program scope and claim packages (→ kasegi); model-quality or evaluation claims (→ kengaku); orchestration, multi-agent dispatch and agent lifecycle (→ kumitate …)". Also "external live-target research without operator approval (loopback-only otherwise)" and "secret values in any record".
- Line 17: "Out of province → report, never absorb."

The refusal that matters here is "model-quality or evaluation claims (→ kengaku)". Neither entry scores, benchmarks, or evaluates a fact-checking model, an AVeriTeC system, or any AI system. Both entries describe what a corpus's schema **records** (documentation) and what its fields **contain** (coverage counts). That is "claim-vs-source verification" / "source hierarchy" / "how a corpus binds a claim/evidence citation to an archived state" — owned, not refused.

## Entry 1 — evidence-archive-field-policy-r41.md (staged S139/S140) — IN PROVINCE

Path: /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-archive-field-policy-r41.md

Deciding sentences:
- Lines 12-18 (Observation): "The two archive fields in the AVeriTeC corpus are **not symmetric**, and the corpus's own documentation says so. At the **evidence** level, `cached_source_url` is documented as 'An archive.org link for the source url' — no qualifier — and the corpus's paper states that it caches *all pages used as evidence* in the internet archive. At the **claim** level, `cached_original_claim_url` is documented as 'Where possible, an archive.org link to the original claim url' — explicitly best-effort."
- Lines 27-32 (Inference): "An empty claim-level field records that **no archive was taken** for that claim's original URL; it does not mean that no archived copy of it exists. … an empty `cached_source_url` on an answer would be the anomaly worth investigating, because the evidence-level archiving is documented as comprehensive…"

This is a claim-vs-source verification question: what an archive field records about the binding between a citation and an archived state. The claim is grounded in the corpus's own README and paper text (source interpretation, citation chaining). No model evaluation; no orchestration; no live fetch (recheck note is a future scheduled fetch, not performed here).

## Entry 2 — evidence-snapshot-coverage-r40.md (staged S132) — IN PROVINCE

Path: /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-snapshot-coverage-r40.md

Deciding sentences:
- Lines 11-17 (Observation): "The per-citation binding is effectively universal. Of the 6,511 evidence entries in the file that carry `cached_source_url`, **6,510 hold a non-empty archive.org URL and 1 is empty**. … The claim-level binding is not. Of the 3,068 records, 2,531 carry a `cached_original_claim_url` field, and of those **1,145 are non-empty and 1,386 are empty**."
- Lines 21-28 (Inference): "The answer to Q17 is 'it depends which binding you mean', and the two differ by two orders of magnitude. The instrument that matters for verifying a *claim against its evidence* — the archived copy of each cited source — is present almost always. The instrument that binds the *claim itself* to the page it first appeared on is present for under half."
- Lines 45-46 (Unknown): "Whether an empty `cached_source_url` means 'no archive exists' or 'no archive was taken' was not determined — the field is empty either way."

Counting how much of the corpus is bound to archived snapshots is a measurement of corpus binding coverage — directly "claim-vs-source verification" and "this lane's own corpus" material. The "Unknown" bullets are honest scope limits, not evaluation claims.

## Sentences that would have to be cut as out of province: NONE

Screened every sentence of both entries against the Refuses list (model-quality/evaluation → kengaku; orchestration → kumitate; live-target research; secret values):
- No sentence evaluates a model's or system's performance, accuracy, or quality (no F1/EM/scores, no verdicts on AVeriTeC's usefulness as a benchmark).
- No sentence touches orchestration, agent lifecycle, or multi-agent dispatch.
- No secret values; no live fetch performed (both entries read on-disk captures; recheck lines are future-dated maintenance notes, not actions).
- The r40 inference bullet comparing to the lane's own r31 `sha256` pin (lines 29-34) is lane-methodology (owned: "this lane's own corpus and gates"), not evaluation.
- The r41 mention that the paper's "Where possible" is "about extractive answers, not about archiving" (line 23) is textual source interpretation, not model evaluation.

## Commands run
1. `read` /home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md (15 lines, header CAA6)
2. `read` /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-archive-field-policy-r41.md (41 lines, header 7FC3)
3. `read` /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-snapshot-coverage-r40.md (51 lines, header 0410)
4. `glob` /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-45/** (report dir exists; wrote this file at /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-45/w1/ScoutProvinceFit.md)

No tools installed; no network; no writes outside the designated report file. Scratch: none used.

## Pointers
- PROVINCE.md: lines 5-11 (Owns/Refuses), line 17 (out-of-province rule).
- r41 entry: lines 12-18, 27-32 for the in-province core; line 23 (extractive-answers aside) in-province as source interpretation.
- r40 entry: lines 11-17, 21-28 for the in-province core; lines 29-34 (lane pin comparison) in-province.
- SHA256 (report-relevant sources): PROVINCE.md header CAA6 file snapshot; r41 header 7FC3; r40 header 0410 (snapshot tags from read).
