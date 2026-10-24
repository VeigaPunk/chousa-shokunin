# Claim-support states — access, relevance, support, truth (round 24)

source: S006 https://arxiv.org/html/2605.06635v1 §3.3 "Evaluation dimensions" (§3.3.1–3.3.3); S007 https://arxiv.org/html/2601.08536v3 §2.1 "Deep Research Benchmarks" (support-vs-correctness paragraph); local: corpus/README.md §"Known gaps", the bullet containing "None of the five proves semantic support"
verified-at: 2026-10-19 (round 24; both arXiv HTML pages fetched and the quoted sentences re-read at the named anchors; the corpus/README.md §"Known gaps" bullet re-read at this worktree revision)
recheck: 90d (re-open S006 §3.3 and S007 §2.1 — a new arXiv version may renumber or rephrase the anchors; `grep -n 'None of the five proves' corpus/README.md` for the known-gaps bullet)

## Claim
A claim-support verdict rests on four distinct observations, each separately
checkable and separately failable: **(1) access** — the cited source exists
and opens; **(2) relevance** — the opened content is on the claim's topic;
**(3) support** — the source states (or contradicts) the claim at a named
anchor; **(4) truth** — the claim itself is true. The method rule: a record
never reports `verified` from observations 1–2 alone, and never reports truth
from observation 3 alone — a source can state a claim that is itself false.
Falsifier: a citation whose source opens and is on-topic yet never states the
claim (3 absent), or a supported claim independently shown false (4 absent);
the rule fails if any lane record reports `verified` without observation 3,
or truth without evidence beyond the source's own assertion.

## Evidence

| source | anchor | verbatim (≤25 words) |
|---|---|---|
| S006 | §3.3 | "These dimensions form an increasing hierarchy of verification difficulty." |
| S006 | §3.3.1 | "Link Works assesses URL accessibility without LLM inference." |
| S006 | §3.3.3 | "citations where the source exists and is topically relevant but does not support the specific claims attributed to it" |
| S007 | §2.1 | "this only measures the accuracy of the citations and does not necessarily confirm that the information is correct" |
| local | corpus/README.md §"Known gaps" | "None of the five proves semantic support, location binding, uniqueness or the source's own truth" |

S006 §3.3.1 names observation 1 (Link Works), §3.3.2 names observation 2
(Relevant Content), §3.3.3 names observation 3 and defines the residual class
this note exists to keep distinct. S007 §2.1 separates observation 3 from 4:
citation accuracy does not confirm correctness (its example: false information
from unofficial sources). The corpus/README.md §"Known gaps" bullet is the
lane's standing statement that no gate mode proves states 3–4.

## How chousa applies it

The Verify-a-claim row (SKILL.md:20) — "claim → source → the source's own
evidence" → `verified / contradicted / unresolved` — maps onto the states:

| observations | verdict |
|---|---|
| 1 opens, 2 on-topic, 3 states the claim | `verified` (state 4 never claimed) |
| 1 opens, 2 on-topic, 3 states the opposite | `contradicted` |
| 1 opens, 2 on-topic, claim absent from source | `unresolved`, never `verified` |
| source refused, dead, or off-topic | `unresolved`, with the reason recorded |

The gate's span check is observation 3 locally, at byte granularity only:
`verify-claims` proves the cited span occurs byte-exact at token boundaries in
its cited local source (SKILL.md:103-115); it does not evaluate entailment and
its `contradicted` is "structural, never semantic" (SKILL.md:112). For
external URLs the gate refuses and never fetches, so states 1–3 on remote
sources are analyst observations, not gate verdicts. State 4 has no gate
surface at all — the README §"Known gaps" bullet is the owning statement.

Worked example — the residual class S006 §3.3.3 names, in lane terms:

| record row | 1 access | 2 relevance | 3 support | verdict |
|---|---|---|---|---|
| claim "verify-claims proves the cited claim true", citing `tools/research-gate.sh` | opens | on-topic (it is the gate) | absent — the script performs a byte span match; the README §"Known gaps" bullet denies semantic support | `unresolved`, never `verified` |

## Limits

- Observation: S006's three dimensions are that study's evaluation
  framework, cited here for the distinctions it draws, not for any result it
  reports about the systems it evaluated (those results are model-quality
  evidence — kengaku province, reported in the round report, not admitted);
  S007's support-vs-correctness sentence is the paper's own statement in its
  related-work section, illustrated by "false information from unofficial
  sources".
- Inference: state 4 (truth) is added here; S006's framework does not score
  it — an extension of the cited dimensions, not a claim about the paper.
- Inference: mapping the states onto the gate's span check is the lane's own
  application; neither source describes this gate.
- Unknown: whether either preprint is revised (v1/v3 pinned here) or the
  passages move — the recheck covers anchor drift.
- No benchmark scores or model rankings are imported as claims — kengaku
  province (PROVINCE.md); the sources are cited for method distinctions only.

## Rejected

- **"Working URL + topically matching page = verified."** Rejected: S006
  §3.3.3 names exactly this residual failure — the source exists and is
  topically relevant yet does not support the claim; SKILL.md:41 records
  `source cited but not read → unresolved`. Flip: a mode checking semantic
  entailment, not just access/relevance, lands and is cited; until then
  `verified` requires observation 3.
- **"Source states the claim = claim is true."** Rejected: S007 §2.1 —
  citation accuracy does not confirm correctness; an unofficial source can
  state a falsehood. Flip: only an independent truth-establishing step (out
  of scope for a citation check) could collapse states 3 and 4.
