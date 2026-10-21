# FxS006Erratum — scoped falsification

Axes: source-text exactness/freshness; registry provenance; method-versus-result boundary.

## Findings

None actionable.

## Evidence

- Reopened S006, https://arxiv.org/html/2605.06635v1, §3.3.1. The exact substring “Link Works assesses URL accessibility without LLM inference” is present (8 words; ≤25). The abstract-page submission history at https://arxiv.org/abs/2605.06635 lists v1 only.
- `corpus/lessons/round-24.md:53` has a composite paraphrase attributed to §3.3, not a verbatim substring there. Reviewer D-4 (`corpus/lessons/round-25.md:25`) correctly identifies a non-verbatim quote; the append-only correction (`round-25.md:94-99`) replaces it with the §3.3.1 substring above. No residual quote/anchor defect found.
- Reopened S007, https://arxiv.org/html/2601.08536v3, §2.1. “this only measures the accuracy of the citations and does not necessarily confirm that the information is correct” remains verbatim in `corpus/knowledge/claim-support-states-r24.md:27` and `corpus/lessons/round-24.md:54`. The abstract-page history at https://arxiv.org/abs/2601.08536 lists v1, v2, v3; v3 is the latest shown (10 Sep 2026).
- S006/S007 registry rows are unchanged between claim base `d730ae4c33989ad9c8535764d4cae77b4db869f6` and full checkpoint `e93ac711f885a10d44fdd80a1734997419595b5a`. `git diff --unified=0 <base> <full> -- corpus/SOURCES.md` reports additions only (35 insertions, 0 deletions); new S019–S028/Search-log material was appended, with no existing row rewritten or requiring a superseding row. The S007 row (`corpus/SOURCES.md:17`) explicitly excludes benchmark results.
- No benchmark-quality result was absorbed into the admitted S006/S007 method note: `claim-support-states-r24.md:65-79` says S006 results are not admitted and no benchmark scores/model rankings are imported; S007 is cited only for its support-versus-correctness statement. Corpus knowledge search found S007 only in that note.
- Private clone recorded base `0fc037e6b07f3820ead8c9207a8034ac854197a1`; reviewed full pin `e93ac711f885a10d44fdd80a1734997419595b5a`. Measured gate SHA-256: `0fc037e` = `752e4e382ed77c06ac5030ce2179c7ca524934f86fd2a6b25ef946ab027ac553`; `d8c8cff` and `e93ac71` = `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2`. The lesson records the first omitted-gate failure (`round-25.md:111-125`) and the intermediate `d8c8cff` missing `corpus/evidence/README.md` (`:127-133`); the private-clone diff confirms that README is present as a changed path by `e93ac71`.

## Residual risk and verification gaps

- Round-25 independent admit/reject sampling was not performed by the lane; the lesson assigns it to a fresh non-author verifier (`round-25.md:103-107`).
- No gate/selftest was run for this source-only assignment.
- Installs: none.

VERDICT: No actionable source, registry, or benchmark-scope defect found at full checkpoint e93ac71.