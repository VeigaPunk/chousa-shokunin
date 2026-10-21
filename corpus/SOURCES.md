# SOURCES — where chousa learns

`corpus/knowledge/` holds admitted facts; this file holds the places they come
from. Admission criteria live in `corpus/QUALITY.md`; a row here is a claim that
its author opened the source and judged its tier for the stated scope only.

## Registry

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | chousa research gate — tools/research-gate.sh (verify-all --json manifest append) | own-work | A | this lane's gate behavior at the round-24 landing revision (gate sha recorded once, in corpus/knowledge/json-delimiter-r24.md) | setup check "manifest unreadable", manifest-append block opening "A manifest whose last byte is not", and selftest cases 134-136 (json-unterminated-, json-nul-terminated-, json-unreadable-manifest) in tools/research-gate.sh; round-24 landing commit | An appending writer must terminate an unterminated last line before appending, or the JSONL glues two objects onto one invalid line | mined | 2026-10-19 | on-release | corpus/knowledge/json-delimiter-r24.md |
| S002 | IFCN Code of Principles, the commitments — https://ifcncodeofprinciples.poynter.org/the-commitments | spec | A | what the Code requires signatories to do on source transparency | Principle #2 "A commitment to Standards and Transparency of Sources" and its four criteria; page as served 2026-10-19 | Prefer the best available primary source, explain secondary use, and check key claim elements against more than one named source | mined | 2026-10-19 | 365d | corpus/knowledge/contextual-source-admission-r24.md |
| S003 | SIFT (The Four Moves), Mike Caulfield — https://hapgood.us/2019/06/19/sift-the-four-moves/ | docs | A | Caulfield's own statement of the SIFT method | sections Stop, Investigate the source, Find better coverage, Trace claims to original context; posted 2019-06-19, modified 2021-02-15 | The four moves: stop, investigate the source, find better coverage, and trace claims, quotes, and media back to the original context | mined | 2026-10-19 | 365d | corpus/knowledge/contextual-source-admission-r24.md, corpus/knowledge/citation-chain-fidelity-r24.md |
| S004 | Cochrane Handbook ch.24, Including non-randomized studies on intervention effects — https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-24 | docs | A | the Handbook's own guidance on appraising non-randomized intervention studies | section 24.2.1.3 "Determining which non-randomized studies of interventions to include"; last updated October 2019, Handbook v6.5 (2024) | Judge studies by explicit design features relative to the question, not by fixed design-label evidence hierarchies | mined | 2026-10-19 | on-release | corpus/knowledge/contextual-source-admission-r24.md |
| S005 | Chen, Teplitskiy, Jurgens, The Noisy Path from Source to Citation — https://aclanthology.org/2025.acl-long.1534/ | paper | A | what this study measured about scholarly citation fidelity | Abstract; section 4 "Measuring Citation Fidelity"; section 6 "Telephone Effect in Citation"; Figure 1 footnote 1; ACL 2025, pages 31786-31802, DOI 10.18653/v1/2025.acl-long.1534 | Citation fidelity varies measurably and low fidelity at one hop predicts lower fidelity downstream — the telephone effect | mined | 2026-10-19 | 365d | corpus/knowledge/citation-chain-fidelity-r24.md |
| S006 | Onweller et al., Cited but Not Verified — https://arxiv.org/html/2605.06635v1 | paper | A | the evaluation framework this preprint defines (its own dimensions), not its results about evaluated systems | section 3.3 Evaluation dimensions (3.3.1 Link Works, 3.3.2 Relevant Content, 3.3.3 Fact Check); arXiv:2605.06635v1, 2026-05-07 | Split citation checks into link accessibility, topical relevance, and factual support — three separately failable checks | mined | 2026-10-19 | 90d | corpus/knowledge/claim-support-states-r24.md |
| S007 | Li et al., DeepResearch Bench II — https://arxiv.org/html/2601.08536v3 | paper | A | what this paper itself states, including its section 2.1 statement of what citation-accuracy measurement does and does not establish; not its benchmark results | section 2.1 passage noting support does not confirm correctness; arXiv:2601.08536v3, 2026-09-10 | Whether a citation supports a claim is separate from whether the cited information is correct | mined | 2026-10-19 | 90d | corpus/knowledge/claim-support-states-r24.md |
| S008 | Cochrane Handbook ch.2, Determining the scope of the review and the questions it will address — https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-02 | docs | A | the Handbook's own guidance on framing review scope and questions | sections 2.1 rationale and 2.3 three PICO levels; last updated August 2023, Handbook v6.5 | Frame an answerable question first and keep review PICO, synthesis PICO, and included-study PICO distinct | queued | 2026-10-19 | on-release | — |
| S009 | Cochrane MECIR, Assessing risk of bias in included studies C52-C60 — https://www.cochrane.org/authors/handbooks-and-manuals/mecir-manual/standards-conduct-new-cochrane-intervention-reviews-c1-c75/performing-review-c24-c75/assessing-risk-bias-included-studies-c52-c60 | spec | A | the MECIR conduct standards for risk-of-bias judgments | standards C53, C54, C55 table rows; page as served 2026-10-19 | Require independent duplicate judgments, a predefined disagreement process, and recorded support for each judgment | queued | 2026-10-19 | 365d | — |
| S010 | Xu et al., CiteEval: Principle-Driven Citation Evaluation for Source Attribution — https://aclanthology.org/2025.acl-long.1574/ | paper | A | what this framework proposes and measured on citation evaluation | Abstract; ACL 2025, pages 32759-32778, DOI 10.18653/v1/2025.acl-long.1574 | NLI-style binary support is a suboptimal proxy; evaluate citations across the full query, retrieval, and generated-answer context | queued | 2026-10-19 | 365d | — |
| S011 | Upadhyay et al., Overview of the TREC 2025 Retrieval Augmented Generation Track — https://trec.nist.gov/pubs/trec34/papers/Overview_rag.pdf | paper | A | what the track ran and how it layered evaluation | section 3 Evaluation (relevance, response, support, agreement layers); TREC 34, arXiv:2603.09891v1 | Assess relevance, answer coverage, per-sentence citation support, and assessor agreement as separate layers | queued | 2026-10-19 | 365d | — |
| S012 | Huang et al., DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality — https://aclanthology.org/2026.acl-long.1586/ | paper | A | what this study measured on claim-level factuality verification | Abstract, Audit-then-Score rounds; ACL 2026, pages 34356-34386, DOI 10.18653/v1/2026.acl-long.1586 | Keep labels and rationales revisable through evidence submission and adjudication; experts audit better than they one-shot label | queued | 2026-10-19 | 365d | — |
| S013 | JSON Lines text format — https://jsonlines.org/ | spec | A | the format's stated requirements | requirement 3, Line Terminator is '\n'; undated page, stable since 2013 | A line terminator after every JSON value is recommended, and if one follows the last value it must be the file's last byte | mined | 2026-10-19 | 365d | corpus/knowledge/json-delimiter-r24.md |
| S014 | 2011 OCEBM Levels of Evidence introductory document — https://www.cebm.ox.ac.uk/resources/levels-of-evidence/levels-of-evidence-introductory-document | docs | C | a universal evidence hierarchy for chousa claim admission | "What the OCEBM Levels is NOT" section; 2011 document | REJECTED: scoped to clinical treatment-benefit search order, and itself disclaims definitive judgments; flip: admit as tier A only for what the OCEBM hierarchy says about its own limits | rejected | 2026-10-19 | 365d | — |
| S015 | OpenAI, Introducing deep research — https://openai.com/index/introducing-deep-research/ | docs | C | deep-research method or capability claims | "How it works" and "Limitations" sections; published 2025-02-02, updated 2026-02-10 | REJECTED: vendor marketing whose capability numbers rest on self-reported internal evaluations; flip: admit scoped to what this vendor itself claims and disclaims about its product | rejected | 2026-10-19 | 90d | — |
| S016 | Wikipedia, Hierarchy of evidence — https://en.wikipedia.org/wiki/Hierarchy_of_evidence | community | C | any claim needing an authoritative evidence-hierarchy source | Criticism section; page as served 2026-10-19 | REJECTED: tertiary community-edited synthesis, never sole support and never tier A; flip: use as a lead index once each cited primary source is opened | rejected | 2026-10-19 | 365d | — |
| S017 | PRISMA 2020 statement — https://www.prisma-statement.org/prisma-2020 | spec | A | reporting standard for systematic-review search transparency | PRISMA 2020 checklist and flow diagram links; statement paper DOI 10.1136/bmj.n71 | Report searches with flow counts and checklist items so identification, screening, and inclusion stay auditable | queued | 2026-10-19 | on-release | — |
| S018 | Schreieder, Schopf, Farber, Attribution, Citation, and Quotation survey — https://aclanthology.org/2026.acl-long.1430/ | paper | B | the taxonomy and metric map of evidence-based generation | Abstract; ACL 2026, pages 30956-31000, DOI 10.18653/v1/2026.acl-long.1430 | A survey of 134 papers and 300 metrics across seven dimensions — a lead index to primary sources, never sole support for a claim | queued | 2026-10-19 | 365d | — |
| S019 | Cochrane Handbook ch. IV, Updating a review — https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv | docs | A | the Handbook's own guidance on periodically deciding whether and how to update a Cochrane review | Chapter IV Key Points and sections IV.1-IV.2; last updated August 2023, Handbook v6.5 | A review's currency is assessed on a schedule, not only when someone notices; deciding to update is a recorded, periodic act | mined | 2026-10-21 | on-release | corpus/knowledge/metadata-screen-r25.md |
| S020 | PROV-O: The PROV Ontology, W3C Recommendation 2013-04-30 — https://www.w3.org/TR/2013/REC-prov-o-20130430/ | spec | A | PROV terms for derivation (prov:wasDerivedFrom) and entity generation/invalidation times; not a recheck or verification policy | section 3.1 Starting Point Terms (prov:wasDerivedFrom); section 3.2 Expanded Terms, entity-lifetime paragraph | Provenance is recorded as a derivation link plus time bounds on an entity's validity, so source and as-of time are separate recorded facts | mined | 2026-10-21 | 365d | corpus/knowledge/metadata-screen-r25.md |
| S021 | Shojania et al. 2007, How quickly do systematic reviews go out of date? A survival analysis — https://pubmed.ncbi.nlm.nih.gov/17638714/ | paper | A | the study's measured update-signal timing in its sample of 100 quantitative systematic reviews; not a rule for all records | Abstract, Results (PubMed record; Ann Intern Med 2007;147(4):224-233) | Findings that need updating appear early for a sizable minority of reviews (23% within 2 years), so recheck intervals matter | queued | 2026-10-21 | 365d | — |
| S022 | Elliott et al. 2017, Living systematic review: 1. Introduction — https://pubmed.ncbi.nlm.nih.gov/28912002/ | paper | A | the paper's own living-systematic-review definition and rationale; not metadata design | Abstract, LSR definition clause (J Clin Epidemiol 2017;91:23-30, DOI 10.1016/j.jclinepi.2017.08.010) | A living review is continually updated as new evidence appears, the limit case of a short recheck cadence | queued | 2026-10-21 | 365d | — |
| S023 | DCMI Metadata Terms — https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ | spec | A | DCMI's definitions of dcterms:source, dcterms:modified and dcterms:valid; not a freshness or verification policy | section 2, /terms/ namespace entries source, modified, valid; DCMI Recommendation issued 2020-01-20 | Source (what a resource derives from) and its dates (modified, valid) are distinct metadata properties | queued | 2026-10-21 | 365d | — |
| S024 | Schema.org property lastReviewed — https://schema.org/lastReviewed | spec | A | Schema.org's own definition and declared use of lastReviewed | page heading lastReviewed, definition paragraph | A last-reviewed date for accuracy is a property separate from publication or modification dates | queued | 2026-10-21 | 365d | — |
| S025 | RFC 9111, HTTP Caching — https://www.rfc-editor.org/rfc/rfc9111 | spec | C | a general rule for research-record staleness or knowledge-entry metadata policy | section 4.2 Freshness; Standards Track, June 2022 | REJECTED: a standard for HTTP-cache freshness, not authority for research-record validity; flip: use as an explicitly labelled analogy and pair it with a directly relevant method source | rejected | 2026-10-21 | on-release | — |
| S026 | GO FAIR Foundation, R1.2 (meta)data are associated with detailed provenance — https://www.gofair.foundation/r1-2 | docs | A | the Foundation's own interpretation of FAIR sub-principle R1.2 | Interpretation of R1.2, first paragraph | Detailed provenance names how, why, by whom and under what conditions a resource was generated | queued | 2026-10-21 | 180d | — |
| S027 | Wikipedia:As of — https://en.wikipedia.org/wiki/Wikipedia:As_of | community | C | Wikipedia editors' guidance for dating time-sensitive statements; never sole support | Usage guidelines section; revision 1342587259 as served 2026-10-21 | Date time-sensitive statements and, when the next update is predictable, mark when it is due | queued | 2026-10-21 | 90d | — |
| S028 | Crossref Crossmark — https://www.crossref.org/services/crossmark/ | docs | A | Crossref's own description of the Crossmark update/correction/retraction status service | introductory text before Benefits of Crossmark | A cited work's update, correction or retraction status is published metadata a reader can check, a recheck trigger | queued | 2026-10-21 | 180d | — |

## Paths

- Framing and admitting a claim — S008 → S002 → S004 → S003: scope the question
  before searching (PICO levels), then prefer suitable primary evidence, judge
  sources by fit rather than design labels, and investigate source identity and
  agenda. Question first, authority last.
- Following a citation chain — S003 → S005 → S006 → S007 → S010: trace to the
  original context, then expect fidelity loss per hop, split access, relevance,
  and support, keep support distinct from truth, and evaluate each claim in its
  full retrieval context.
- Keeping judgments honest — S009 → S011 → S012 → S017: duplicate supported
  judgments with a disagreement path, layer evaluation, keep labels revisable
  under evidence, and report the search so the sweep itself is auditable.
- Lane mechanics — S001 → S013: the gate's own append rule and the JSON Lines
  requirement it implements, read together.
- Keeping records current — S019 → S021 → S020 → S023: schedule the currency
  check (a recheck is a periodic, recorded act), expect early staleness for a
  real minority of findings, and record provenance as a derivation link plus
  separate time facts. S025 is kept as a rejected analogy (lifetime vs age), not authority here.

## Search log

- Pre-assigned sweep (round 24, 2026-10-19): question — which of the 13
  pre-assigned ids open and hold their named anchors. Where: the exact URLs and
  the repo path in the round id map. Identified 13, screened 13, included 13
  (S001-S013), excluded 0. Every named anchor existed; two were sharpened on
  opening — S004's subsection is §24.2.1.3, and S005's telephone-effect
  passage is §6 (with §4 defining fidelity). Anchor text is quoted in the
  round Gate. Stopped when every assigned row had an opened anchor.
- Rejected-candidate sweep (2026-10-19): question — which commonly cited pages
  fail admission as universal source-hierarchy or deep-research authority.
  Where: art dossier leads plus one vendor page and one tertiary page.
  Identified 3 (OCEBM 2011 levels, OpenAI deep-research launch, Wikipedia
  hierarchy of evidence), screened 3, included 3 as rejected rows, excluded 0.
  Exclusion reasons: claim-scoped not universal (S014), self-reported vendor
  metrics (S015), tertiary community synthesis (S016). Stopped at three
  because the round assignment asked for at least two rejections (the
  contract sets no row quota) and further candidates added no new rejection
  reason.
- Expansion sweep (2026-10-19): question — which opened sources cover search
  reporting and the citation-evaluation literature map, ground no mined row
  covers. Where: art dossier proposed-row table. Identified 2 (PRISMA 2020,
  Schreieder et al. survey), screened 2, included 2 as queued rows (S017, S018),
  excluded 0. Stopped within the four-row cap; deeper mining waits for a
  knowledge entry that cites them.
- Freshness and provenance sweep (round 25, 2026-10-21): question — which
  opened sources ground a scheduled `recheck:` and separate `source:` /
  `verified-at:` facts for a knowledge entry. Where: 11 pre-assigned URLs (one
  round-25 scout seat each; reports `.ufo/waves/round-25/build/Src*.md`).
  Identified 11, screened 11, included 10 (S019-S028: 2 mined, 7 queued, 1 rejected),
  excluded 1: Garner et al. 2016 BMJ "When and how to update systematic
  reviews" (https://www.bmj.com/content/354/bmj.i3507) returned HTTP 403
  behind a Cloudflare challenge, so no text was inspected and no row is written
  (flip: re-open an accessible full text and quote its checklist). Stopped at
  the pre-assigned set; every included row is at most partial support for the
  compound claim, so the entry cites S019 and S020 for separate parts.

- Correction to the round-24 rejected-candidate sweep's stop rationale
  (appended round 25): an assignment quota is not an epistemic stopping
  condition. That search is only a bounded three-candidate convenience
  sample, not saturation of rejection reasons. New sweeps stop when the
  stated question's candidate set is exhausted or another candidate cannot
  change the admitted distinction, and say which. This historical defect is
  retained, not rewritten (outside review D-6; SOURCES rule 5).

## Leads (unopened)

- TREC RAG track website — https://trec-rag.github.io/ — task data, qrels, and
  run artifacts behind the S011 overview.
- AVeriTeC original shared-task paper — https://arxiv.org/html/2410.23850v1 —
  evidence-verdict schema for claim verification.
- Check, Please! starter course — linked from S003 — applied learner path, not
  primary evidence.
- DRBench — https://arxiv.org/abs/2510.00172 — enterprise deep-research
  benchmark mixing web and private knowledge.
- OCEBM Levels background document — the longer document behind S014, for the
  scoped reading only.
- Garner et al. 2016, BMJ 354:i3507 — https://www.bmj.com/content/354/bmj.i3507 —
  update consensus and checklist; blocked (HTTP 403) on 2026-10-21.
