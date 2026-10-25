# Contextual source admission — the ladder is a default, the claim decides (round 24)
source: S002 https://ifcncodeofprinciples.poynter.org/the-commitments heading "Principle #2 A commitment to Standards and Transparency of Sources" → "Criteria: To be compliant on sources" bullets 2–3; S004 https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-24 §24.2.1.3 (#section-24-2-1-3; Key Points bullet 5); S003 https://hapgood.us/2019/06/19/sift-the-four-moves/ headings "Investigate the source", "Find better coverage"
verified-at: 2026-10-19 (round 24; all three pages opened in full; S004 subsection number read off the live page, not assumed)
recheck: on-release (S004, Cochrane Handbook — v6.5 / chapter last updated Oct 2019 as read); 365d (S002 commitments page, S003 post)

## Claim

Source priority is decided per claim, not per label. For each admitted claim the
supporting source is justified on: role (primary for *what* — states it, measured
it, specifies it), provenance (who produced it and from what observation), method
fit (does the document's or study's design actually address the question asked),
recency (is it inside this claim's decay rate), declared interests, independence
from the claim's subject, and availability (can a reader reopen it). Where a
suitable primary exists it is preferred; a secondary use is named and explained.
Where no suitable primary exists, the best-available source is admissible with
the gap recorded. No source type is correct by label alone.
Falsifier: show one admitted claim for which a lower-ladder source is at least
as suitable on role + method fit, yet the ladder was applied instead with no
per-claim reason — then "the claim decides" is decorative, not operative.

## Evidence

- S002, "Criteria: To be compliant on sources" bullet 2: "The applicant uses the
  best available primary, not secondary, sources of evidence wherever suitable
  primary sources are available." and "the applicant explains the use of a
  secondary source" (same bullet). Bullet 3: "checks all key elements of claims
  against more than one named source of evidence" (substring).
- S004, §24.2.1.3 final paragraph: "We advise caution in assessing NRSI
  according to existing ‘evidence hierarchies’ for studies of effectiveness".
  Key Points bullet 5: "place an emphasis on specific features of study design
  (e.g. which parts of the study were prospectively designed) rather than
  ‘labels’ for study designs".
- S003, "Investigate the source" paragraph 2: "knowing the expertise and agenda
  of the source is crucial to your interpretation of what they say."
  "Find better coverage" paragraph 1: "go out and find the best source you can
  on this topic".

## How chousa applies it

Every source admitted into a research record fills one admission row:

| field | content |
|---|---|
| claim | the claim-id this source supports |
| role | what it is primary for (states / measured / specifies) — or `secondary` |
| why suitable | method fit + recency for this claim |
| interests | declared interests that could colour the evidence |
| corroboration | second named source checked against (or `only source` note) |
| tier-for-this-scope | SOURCES.md contract tier for the row's stated scope |

This qualifies SKILL.md:18 (`primary > secondary > aggregator > unsourced
claim`): the ladder stays the default ordering reached for before the claim is
known, and the row overrides it with a stated reason. An aggregator that *is* the
artifact (a changelog for "what shipped") can be tier-A-for-scope; a source that
is primary elsewhere but off-claim stays tier-C-for-this-scope. The
`tier-for-this-scope` cell uses the SOURCES.md contract meanings: A = primary or
authoritative for that scope, B = strong secondary, C = lead only and never sole
support (QUALITY 7). S002–S004 are each tier-A for "what this source states" —
official criteria, official handbook chapter, author's own post — which is the
scope every Evidence line above uses.

## Limits

- Observation: S002–S004 each express claim-relative admission inside their own
  domain — IFCN signatory fact-check criteria, Cochrane health-intervention
  review method, Caulfield's web-reading practice. None names this lane's
  ladder, and no URL fragment anchors were exposed on S002 or S003; heading
  text is the anchor as opened.
- Inference: extending "design features over design labels" (S004) and
  "suitable primary, else explain" (S002) into general research method is
  analogy — Cochrane is health-intervention guidance and IFCN is fact-checking
  practice; the admission row is the lane's construction on that analogy, not a
  rule the sources state.
- Unknown: whether engineering-spec and code-review traditions carry an
  equivalent per-claim admission norm; no sweep performed this round.

## Rejected

- "primary > secondary > aggregator is a universal theorem — a primary source
  always outranks any secondary." Reason: S002 conditions primacy on
  suitability ("wherever suitable primary sources are available"), S004
  §24.2.1.3 cautions against fixed hierarchies whose labels do not fit the
  question, and SKILL.md:25-33 marks the ladder itself as lane construction.
  Flip: admit as a counter-example only if an opened authority prescribes
  fixed label-rank ordering regardless of the claim under test.
