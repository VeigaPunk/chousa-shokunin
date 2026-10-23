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
| S019 | Cochrane Handbook ch. IV, Updating a review — https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv | docs | A | the Handbook's own guidance on periodically deciding whether and how to update a Cochrane review | Chapter IV Key Points and sections IV.1-IV.2; last updated August 2023, Handbook v6.5 | A review's currency is assessed on a schedule, not only when someone notices; deciding to update is a recorded, periodic act | queued | 2026-10-21 | on-release | — |
| S020 | PROV-O: The PROV Ontology, W3C Recommendation 2013-04-30 — https://www.w3.org/TR/2013/REC-prov-o-20130430/ | spec | A | PROV terms for derivation (prov:wasDerivedFrom) and entity generation/invalidation times; not a recheck or verification policy | section 3.1 Starting Point Terms (prov:wasDerivedFrom); section 3.2 Expanded Terms, entity-lifetime paragraph | Provenance is recorded as a derivation link plus time bounds on an entity's validity, so source and as-of time are separate recorded facts | queued | 2026-10-21 | 365d | — |
| S021 | Shojania et al. 2007, How quickly do systematic reviews go out of date? A survival analysis — https://pubmed.ncbi.nlm.nih.gov/17638714/ | paper | A | the study's measured update-signal timing in its sample of 100 quantitative systematic reviews; not a rule for all records | Abstract, Results (PubMed record; Ann Intern Med 2007;147(4):224-233) | Findings that need updating appear early for a sizable minority of reviews (23% within 2 years), so recheck intervals matter | queued | 2026-10-21 | 365d | — |
| S022 | Elliott et al. 2017, Living systematic review: 1. Introduction — https://pubmed.ncbi.nlm.nih.gov/28912002/ | paper | A | the paper's own living-systematic-review definition and rationale; not metadata design | Abstract, LSR definition clause (J Clin Epidemiol 2017;91:23-30, DOI 10.1016/j.jclinepi.2017.08.010) | A living review is continually updated as new evidence appears, the limit case of a short recheck cadence | queued | 2026-10-21 | 365d | — |
| S023 | DCMI Metadata Terms — https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ | spec | A | DCMI's definitions of dcterms:source, dcterms:modified and dcterms:valid; not a freshness or verification policy | section 2, /terms/ namespace entries source, modified, valid; DCMI Recommendation issued 2020-01-20 | Source (what a resource derives from) and its dates (modified, valid) are distinct metadata properties | queued | 2026-10-21 | 365d | — |
| S024 | Schema.org property lastReviewed — https://schema.org/lastReviewed | spec | A | Schema.org's own definition and declared use of lastReviewed | page heading lastReviewed, definition paragraph | A last-reviewed date for accuracy is a property separate from publication or modification dates | queued | 2026-10-21 | 365d | — |
| S025 | RFC 9111, HTTP Caching — https://www.rfc-editor.org/rfc/rfc9111 | spec | C | a general rule for research-record staleness or knowledge-entry metadata policy | section 4.2 Freshness; Standards Track, June 2022 | REJECTED: a standard for HTTP-cache freshness, not authority for research-record validity; flip: use as an explicitly labelled analogy and pair it with a directly relevant method source | rejected | 2026-10-21 | on-release | — |
| S026 | GO FAIR Foundation, R1.2 (meta)data are associated with detailed provenance — https://www.gofair.foundation/r1-2 | docs | A | the Foundation's own interpretation of FAIR sub-principle R1.2 | Interpretation of R1.2, first paragraph | Detailed provenance names how, why, by whom and under what conditions a resource was generated | queued | 2026-10-21 | 180d | — |
| S027 | Wikipedia:As of — https://en.wikipedia.org/wiki/Wikipedia:As_of | community | C | Wikipedia editors' guidance for dating time-sensitive statements; never sole support | Usage guidelines section; revision 1342587259 as served 2026-10-21 | Date time-sensitive statements and, when the next update is predictable, mark when it is due | queued | 2026-10-21 | 90d | — |
| S028 | Crossref Crossmark — https://www.crossref.org/services/crossmark/ | docs | A | Crossref's own description of the Crossmark update/correction/retraction status service | introductory text before Benefits of Crossmark | A cited work's update, correction or retraction status is published metadata a reader can check, a recheck trigger | queued | 2026-10-21 | 180d | — |
| S029 | Cochrane Handbook ch. IV, Updating a review — https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv | docs | A | the Handbook's own guidance on periodically deciding whether and how to update a Cochrane review | Chapter IV section IV.1 Introduction; Handbook v6.5, August 2023 | supersedes S019 — Cochrane reviews should be assessed periodically to decide whether an update is needed; this sentence does not prescribe a recorded schedule | mined | 2026-10-21 | on-release | corpus/knowledge/metadata-screen-r25.md, corpus/knowledge/recheck-due-r26.md |
| S030 | Elliott et al. 2017, Living systematic review: 1. Introduction — https://pubmed.ncbi.nlm.nih.gov/28912002/ | paper | A | the paper's own living-systematic-review definition and rationale; not metadata design | Abstract, living-systematic-review definition; J Clin Epidemiol 2017;91:23-30 | supersedes S022 — defines living systematic reviews as continually updated to incorporate relevant new evidence as it becomes available; recheck-cadence comparison is a lane inference | queued | 2026-10-21 | 365d | — |
| S031 | Schema.org property lastReviewed — https://schema.org/lastReviewed | spec | A | Schema.org's own definition and declared use of lastReviewed | lastReviewed property definition paragraph; Schema.org page served 2026-10-21 | supersedes S024 — lastReviewed records the date a web page was last reviewed for accuracy and/or completeness; no comparison to other date properties claimed | queued | 2026-10-21 | 365d | — |
| S032 | Shojania et al. 2007, How quickly do systematic reviews go out of date? A survival analysis — https://pubmed.ncbi.nlm.nih.gov/17638714/ | paper | A | the study's measured update-signal timing in its sample of 100 quantitative systematic reviews; not a rule for all records | Abstract Results; Ann Intern Med 2007;147(4):224-233 | supersedes S021 — in this study a signal potentially warranting an update occurred within 2 years for 23% of reviews; a signal is not itself an update | queued | 2026-10-21 | 365d | — |
| S033 | PROV-O: The PROV Ontology, W3C Recommendation 2013-04-30 — https://www.w3.org/TR/2013/REC-prov-o-20130430/ | spec | A | PROV terms for derivation (prov:wasDerivedFrom) and entity generation/invalidation times; not a recheck or verification policy | section 3.1 Starting Point Terms (prov:wasDerivedFrom); section 3.2 Expanded Terms, entity-lifetime paragraph | supersedes S020 — PROV-O records derivation and entity generation/invalidation times separately; these are entity-lifetime facts, not verification time or truth-validity | mined | 2026-10-21 | 365d | corpus/knowledge/metadata-screen-r25.md |
| S034 | Metadata reader allocation measurements — corpus/evidence/round26-measure-before.log and tools/research-gate.sh verify_metadata | own-work | A | this lane's measured four-shape reader allocation and the streamed header representation; not a universal resource budget | round26 claim base ba3333254dd337658a4f25e7a9471f9cf4e4567e; before receipt C1 table and candidate verify_metadata header loop, 2026-10-21 | A bounded byte snapshot can still amplify into per-line objects; parse the snapshot without retaining a line array and measure both output identity and RSS | mined | 2026-10-21 | on-release | corpus/knowledge/reader-allocation-r26.md |
| S035 | chousa due-date contract and implementation — corpus/evidence/round26-claims.md Claim2; tools/research-gate.sh metadata date helpers and verify_metadata | own-work | A | this lane's declared calendar-day scheduling model and opt-in CLI behavior, not source truth | round26 spec v1 plus decimal/range addendum, 2026-10-21; metadata_add_days and META_RECHECK_OVERDUE branches | Compute declared recheck deadlines at an explicit as-of date, leaving event and unknown schedules distinct from current or overdue | mined | 2026-10-21 | on-release | corpus/knowledge/recheck-due-r26.md |
| S036 | chousa registry-link contract and implementation — corpus/evidence/round26-claims.md Claim3; tools/research-gate.sh metadata_registry_load and metadata_registry_check_source | own-work | A | local ID, mined-status, exact-rooted backlink and descriptive verified-at screening; not full criterion6 or citation support | round26 spec v1 and SOURCES-contract correction, 2026-10-21; META_SOURCE_ROW_MISSING and META_SOURCE_USEDBY_MISSING branches | Registry existence, status and backlink checks establish local declared relationships, not source relevance or truth | mined | 2026-10-21 | on-release | corpus/knowledge/registry-link-r26.md |
| S037 | Guidance for Cochrane living systematic reviews — https://resources.cochrane.org/sites/resources.cochrane.org/files/uploads/inline-files/Transform/201912_LSR_Revised_Guidance.pdf | docs | A | Cochrane intervention LSR guidance on evidence-search versus review-update cadence | section4.3.4 p19; Version December2019 | Review updates may follow a protocol-specified fixed interval approved by the editorial team; this is separate from ongoing evidence searches | mined | 2026-10-21 | 180d | corpus/knowledge/recheck-due-r26.md |
| S038 | Python datetime documentation — https://docs.python.org/3/library/datetime.html | docs | A | Python date proleptic-Gregorian ordinals, calendar-day arithmetic and year limits used by the independent oracle; not a generic freshness policy | Python3.15.0 documentation served 2026-10-21; date.toordinal, date arithmetic note1 and MINYEAR/MAXYEAR | Date arithmetic uses the proleptic Gregorian calendar; adding timedelta days moves the date by that many calendar days within years1–9999 | mined | 2026-10-21 | on-release | corpus/knowledge/recheck-due-r26.md |
| S039 | PROV-DM: The PROV Data Model — https://www.w3.org/TR/2013/REC-prov-dm-20130430/ | spec | A | PROV-DM's derivation model and optional generation/usage detail; not a registry or verification requirement | section5.2.1 Derivation, term-Derivation; W3C Recommendation2013-04-30 | PROV-DM permits explicit generation and usage details for entities in a derivation | mined | 2026-10-21 | 365d | corpus/knowledge/registry-link-r26.md |
| S040 | Usage selftest record-grammar diagnosis — .ufo/waves/round-26/falsify/FNoTrade.md | own-work | A | the reported three r26 usage-harness failures and their help-text versus verdict-record cause; not whole-gate correctness | base 64eec5d41c7cf7f17f5ce1e968e28b3769952596; FNoTrade lines115–137, opened2026-10-21 | Count verdict records by their record grammar, not a phrase also present in usage documentation; preserve expected exit and diagnostic assertions | mined | 2026-10-21 | on-release | corpus/lessons/round-27.md |
| S041 | Date-input regression diagnoses — .ufo/waves/round-26/falsify/FDateAsOfUsage.md and FDateHugeCadence.md | own-work | A | this lane's reported locale-dependent date validation and recursive zero-normalization failures; not generic freshness policy | base 64eec5d41c7cf7f17f5ce1e968e28b3769952596; FDateAsOfUsage lines75–86; FDateHugeCadence lines34–44, opened2026-10-21 | Validate ASCII input in the same representation arithmetic accepts; normalize decimal magnitude without a recursive match on the zero prefix | mined | 2026-10-21 | on-release | corpus/lessons/round-27.md |
| S042 | Registry relationship regression diagnoses — .ufo/waves/round-26/falsify/FRegistryHeaderless.md, FRegistryIdBoundary.md and FRegistryRegistryDeny.md | own-work | A | this lane's reported stale header state, false S-id rescan and filesystem-path versus citation-pointer mismatch | base 64eec5d41c7cf7f17f5ce1e968e28b3769952596; headerless lines41–49, ID boundary lines28–45, registry deny lines23–30, opened2026-10-21 | Reset parser state at boundaries, retain occurrence identity, and distinguish filesystem paths from citation pointers before checking declared relationships | mined | 2026-10-21 | on-release | corpus/lessons/round-27.md |
| S043 | Round27 falsify-wave counterexamples — .ufo/waves/round-27/falsify/FC3ValidTable27.md, IntegTokenCost.md, FC2Allzero128K07.md and FC1CorrectUsageWithHelp00.md | own-work | A | this lane's falsifier reports against checkpoint dd72641e574679c4f7882dd43de072b4c8892d6f: escaped-pipe width over-rejection, per-token cost, long-line CR strip, usage-matcher fail-open; not outside admission | FC3ValidTable27 line59; IntegTokenCost line20; FC2Allzero128K07 line18; FC1CorrectUsageWithHelp00 line7, opened2026-10-21 | Measure table width in GFM cells, filter tokens before a per-item shell loop, strip a trailing byte without a suffix-pattern scan, and fail closed when a matcher errors | mined | 2026-10-21 | on-release | corpus/lessons/round-27.md |
| S044 | Python os.path documentation — https://docs.python.org/3/library/os.path.html | docs | A | Python component-aware commonpath and canonical-path API semantics only; not a shell-equivalence or denylist-policy authority | documentation served Python3.15.1, commonpath/commonprefix/realpath sections, opened2026-10-21 | Distinguish a valid common path from a character prefix, and keep canonical-path computation separate from an application's policy judgment | mined | 2026-10-21 | on-release | corpus/lessons/round-28.md |
| S045 | Round27 canonical ancestor refusal diagnosis — .ufo/waves/round-27/residual/ResNoHarm.md | own-work | A | recorded finite nine-ancestor claims over-refusal and actual denied-path diagnostic mismatch; not an implemented round28 repair or universal read-safety claim | BASE 11d7c5da1ee7f6a4e01b1661d14a9d08fb8de01a, ResNoHarm lines53–69, opened2026-10-21 | Historical/rejected repair diagnosis only: the proposed root exemption is unapproved; denylist not waived; no current instruction to select or exempt roots | mined | 2026-10-21 | on-release | corpus/lessons/round-28.md |
| S046 | W3C Web Annotation Data Model, W3C Recommendation — https://www.w3.org/TR/annotation-model/#text-quote-selector | spec | A | the Recommendation's Text Quote Selector model for locating text by its exact copy plus optional prefix and suffix; not a matching algorithm or claim validation | section 4.2.4 Text Quote Selector, opening paragraph | A quote is located by copying the exact text and, where copies repeat, some text immediately before and after it to tell the copies apart | mined | 2026-10-23 | 365d | corpus/knowledge/quote-reopen-r29.md |
| S047 | URL Fragment Text Directives, WICG draft — https://wicg.github.io/scroll-to-text-fragment/ | spec | A | the specification's own text search, word-boundary and context-term behavior; not this lane's normalization policy | section 3.6.1 Find a String in Range; section 3.6.2 Word Boundaries; section 3.2.1 Context Terms | Its text search is case-insensitive and ignores accents and marks, word boundaries are locale-aware, and context terms disambiguate repeated text | mined | 2026-10-23 | 365d | corpus/knowledge/quote-reopen-r29.md |
| S048 | Unicode Standard Annex 15, Unicode Normalization Forms — https://unicode.org/reports/tr15/ | spec | A | what UAX 15 says about compatibility normalization (NFKC) and the distinctions it can erase; not a quote-verification policy | section 1.1 Canonical and Compatibility Equivalence; section 1.2 Normalization Forms | NFKC folds compatibility-equivalent characters together, so it can erase formatting or meaning distinctions and must not be applied blindly | mined | 2026-10-23 | 365d | corpus/knowledge/quote-reopen-r29.md |
| S049 | Python html.parser documentation — https://docs.python.org/3/library/html.parser.html | docs | A | Python's documented character-reference conversion in HTMLParser; not a general HTML conformance guarantee | HTMLParser constructor, convert_charrefs parameter | With convert_charrefs true, character references in text are converted to Unicode characters, except inside elements like script and style | mined | 2026-10-23 | on-release | corpus/knowledge/quote-reopen-r29.md |
| S050 | HTML 5.2, W3C Recommendation 14 December 2017 (dated snapshot) — https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html#optional-tags | spec | A | what the HTML 5.2 Recommendation text (a dated 2017 snapshot) states about omitting the head end tag; not the current WHATWG HTML Standard, which was not opened | section 8.1.2.4 Optional tags; dated W3C URL (the undated /TR/html52/ URL now redirects to html.spec.whatwg.org) | A page may omit the head end tag, so a text extractor cannot rely on </head> to end the head | mined | 2026-10-23 | 365d | corpus/knowledge/quote-reopen-r30.md |
| S051 | HTML 5.2, W3C Recommendation 14 December 2017 (dated snapshot) — https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html#the-in-head-insertion-mode | spec | A | the HTML 5.2 tree-construction rules of the in head insertion mode; the head boundary only, not fetch behavior or quote verification | section 8.2.5.4.4 The in head insertion mode, branch Anything else | Whitespace stays in head; the listed head start tags are handled there; any other token pops the head element and is reprocessed outside it | mined | 2026-10-23 | 365d | corpus/knowledge/quote-reopen-r30.md |
| S052 | Python socket documentation, Notes on socket timeouts — https://docs.python.org/3/library/socket.html#socket-timeouts | docs | A | Python timeout-mode semantics for blocking socket operations; not a total fetch-deadline guarantee | section Notes on socket timeouts, Python 3.15.1 documentation | A socket timeout bounds each blocking operation, so a separate elapsed-time deadline is needed to bound a whole transfer | mined | 2026-10-23 | on-release | corpus/knowledge/quote-reopen-r30.md |
| S053 | Python socket documentation, socket.create_connection — https://docs.python.org/3/library/socket.html#socket.create_connection | docs | A | documented create_connection behavior for a host name; not a guarantee of DNS pinning or per-hop validation | section socket.create_connection, Python 3.15.1 documentation | create_connection resolves a host name itself and tries each address, so an earlier address check does not pin the later connection | mined | 2026-10-23 | on-release | corpus/knowledge/quote-reopen-r30.md |
| S054 | Python http.client documentation, HTTPConnection — https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection | docs | A | Python HTTPConnection timeout semantics and host-based connection setup; not a total-fetch deadline or DNS-pinning guarantee | class http.client.HTTPConnection, constructor description, Python 3.15.1 documentation | The timeout limits each blocking operation such as a connection attempt, and the connection target is a host name and port | mined | 2026-10-23 | on-release | corpus/knowledge/quote-reopen-r30.md |
| S055 | Python ssl documentation, SSLContext.wrap_socket — https://docs.python.org/3/library/ssl.html#ssl.SSLContext.wrap_socket | docs | A | Python client TLS server_hostname and certificate host-name matching; not DNS resolution or address validation | SSLContext.wrap_socket (Changed in version 3.5 note) and SSLContext.check_hostname, Python 3.15.1 documentation | Pass the host name as server_hostname to keep SNI and the certificate host-name check; the page says nothing about address validation | mined | 2026-10-23 | on-release | corpus/knowledge/quote-reopen-r30.md |
| S056 | Python ipaddress documentation, IPv4Address.is_global — https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address.is_global | docs | A | Python's is_global classification of global reachability; not DNS resolution or connection pinning | section IPv4Address.is_global, Python 3.15.1 documentation | is_global follows the IANA special-purpose registries, with documented exceptions such as IPv4-mapped IPv6 and 100.64.0.0/10 | mined | 2026-10-23 | on-release | corpus/knowledge/quote-reopen-r30.md |
| S057 | RFC 5147, URI Fragment Identifiers for the text/plain Media Type — https://www.rfc-editor.org/rfc/rfc5147.txt | spec | A | how a fragment names a line position or line range inside a text/plain entity, counted from zero between lines; not the lane gate's 1-based `at=` lines, claims-file syntax, or that a named line carries the claim's meaning | §2.2.3 "Line Position" and §2.2.4 "Line Range" (RFC text as served 2026-10-23, SHA-256 `c8fff6f2…24f4`) | A citation can name a line range, not only a file; RFC 5147 counts line positions from zero between lines, so the gate's 1-based line numbers are a different convention that must be stated | mined | 2026-10-23 | 365d | corpus/knowledge/line-binding-r31.md |
| S058 | W3C, Subresource Integrity — https://www.w3.org/TR/2016/REC-SRI-20160623/ (Recommendation, 2016-06-23) | spec | A | Browser Subresource Integrity response-digest validation (tier A: the primary W3C Recommendation for this mechanism); does not establish this lane gate's exact local-file byte contract, claim-schema validation, or read/hash race behavior | sections 3.3.1 “Apply algorithm to response” and 3.3.5 “Does response match metadataList”, dated Recommendation 2016-06-23 | Hash the response representation, compare the resulting digest with expected metadata, and return false when no expected value matches | mined | 2026-10-23 | 365d | corpus/knowledge/revision-binding-r31.md |
| S059 | Python hashlib documentation — https://docs.python.org/3/library/hashlib.html | docs | A | Python hashlib's SHA-256 digest and hexadecimal representation for bytes fed to a hash object; not a general SHA-256 text-encoding standard, lowercase-output requirement, or the lane's revision-pin contract | `Hash algorithms` and `Hash Objects`: `hashlib.hash.digest_size`, `.update()`, `.digest()`, `.hexdigest()`; Python 3.15.1 documentation, page as served 2026-10-23 | A `sha256()` object digests the concatenation of data fed through `update()`; `hexdigest()` returns a string twice the digest's byte length with hexadecimal digits, but the docs do not specify output letter case | mined | 2026-10-23 | on-release | corpus/knowledge/revision-binding-r31.md |
| S060 | Python `fcntl` documentation — https://docs.python.org/3/library/fcntl.html | docs | A | Python's documented `fcntl.flock()` call on a file descriptor and the `LOCK_EX` constant's description; not flock(2) lock lifetime, advisory semantics or NFS behaviour | `fcntl.flock(fd, operation)` ("Perform the lock operation operation on file descriptor fd", which defers to flock(2)) and `fcntl.LOCK_EX` ("Acquire an exclusive lock.", listed among the `fcntl.lockf` cmd values); Python 3.15.1 documentation as served 2026-10-23. The page carries a build clock in its footer ("Last updated … (06:37 UTC)"), so the body sha256 `025727ff…3dda3` pins that snapshot only; a later GET differs in that line (06:57 UTC → `0189dd49…1e56`) | `flock()` performs a lock operation on a file descriptor (or an object with `fileno()`); `LOCK_EX` is described as acquiring an exclusive lock. That the same constant is flock's exclusive operation comes from flock(2), not this page (not opened) | mined | 2026-10-23 | on-release | corpus/knowledge/manifest-append-lock-r32.md |
| S061 | RFC 9110, HTTP Semantics — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | HTTP 404/410 status semantics at the origin server; not local-copy availability and not a rule that a researcher must check a local copy | §15.5.5 "404 Not Found" and §15.5.11 "410 Gone"; RFC 9110 (June 2022), body as served 2026-10-23 (HTTP 200, sha256 `21c1cdce…47232a`) | A 410 says the target resource is no longer available at the origin server and the condition is likely permanent; a 404 does not say whether the absence is temporary or permanent. Both are statements about the origin server only. (That a hop's "could not be followed" therefore leaves a local copy unexamined is the lane's inference, not the RFC's.) | mined | 2026-10-23 | 365d | corpus/knowledge/exempt-hop-audit-r32.md |
| S062 | RFC 8259, The JavaScript Object Notation (JSON) Data Interchange Format — https://www.rfc-editor.org/rfc/rfc8259.txt | spec | A | RFC 8259’s §4 object model: members are string-name/value pairs; §3 permits object and array values; §4 recommends unique names and says duplicate-name receiver behavior is unpredictable. This is standards semantics, not this lane’s top-level `verify-claims` reader contract. | §3 “Values” lines 296–308 and §4 “Objects” lines 316–335, 343–344 (corrected in-round from 316–333 after ReopenS062: the sentence ends on 334 and line 334–335 names implementations that report an error); RFC 8259 (December 2017), body as served 2026-10-23 (HTTP 200, 28,360 bytes, SHA-256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`) | Distinguish RFC semantics from a local record-reader contract: object members pair names with values, including nested objects and arrays; unique names are recommended because duplicate-name receiver behavior is unpredictable. | mined | 2026-10-23 | 365d | corpus/knowledge/claim-record-fields-r33.md |
| S063 | Python `json` documentation — https://docs.python.org/3/library/json.html#repeated-names-within-an-object | docs | A | Python 3.15.1 `json` decoder's default handling of repeated object names and the `object_pairs_hook` option to alter it; not JSON's normative requirements or this lane's top-level-field reader policy | “Repeated Names Within an Object”; `json.load()`/`json.loads()` `object_pairs_hook`; Python 3.15.1 documentation as served 2026-10-23, HTTP 200, body SHA-256 `5ceeeaf6b0c866bd413ac0a9316f92cd46e03984cfec87cf7ac051ca6235608b`; footer `Last updated on Oct 23, 2026 (07:34 UTC)` (same timestamp and body in both GETs) | Python's default decoder ignores all but the last repeated object name-value pair; `object_pairs_hook` can alter that behavior. | mined | 2026-10-23 | on-release | corpus/knowledge/claim-record-fields-r33.md |
| S064 | Linux man-pages, execve(2) — https://man7.org/linux/man-pages/man2/execve.2.html (read from the installed copy; the URL was not fetched) | docs | A | the Linux kernel's per-string argv and environment-string limit; not grep or bash behavior | subsection "Limits on size of arguments and environment" (decompressed `/usr/share/man/man2/execve.2.gz` lines 365–424, quote at 422–424; anchor corrected in-round from `NOTES` after R34ReopenSources); man-pages 6.19-1, local file SHA-256 `4489dfef246682d18365712ce686f3519318b074761f249091c5fc99c8eab0dc` (opened locally 2026-10-23) | The page distinguishes the aggregate argument/environment size limit from the 32-page per-string limit named `MAX_ARG_STRLEN`. | mined | 2026-10-23 | on-release | corpus/knowledge/long-span-argv-r34.md |
| S065 | PCRE2 `pcre2limits(3)` manual — `/usr/share/man/man3/pcre2limits.3.gz` | docs | A | PCRE2 compiled-pattern size versus source-pattern length for the installed library; not the OS argument-byte ceiling or this lane's verifier behavior | “SIZE AND OTHER LIMITATIONS”; PCRE2 10.49 (03 September 2025), installed `pcre2 10.49-1`; file SHA-256 `a3ea2c67c102af649be069fd31bb6b658c2170f15bc1a1728f464fd8e5974bd6` | The manual distinguishes an effectively unlimited source-pattern length from an approximately 64-thousand-code-unit compiled-pattern size ceiling for default 8/16-bit libraries. On this host `/usr/bin/grep -P -f` compiled repeated `\x41` literals through a 32,764-byte span and rejected 32,765 as “regular expression is too large”; an argv workaround using a four-character escape per byte therefore does not remove the compiled-size limit. | mined | 2026-10-23 | on-release | corpus/knowledge/long-span-argv-r34.md |
| S066 | GNU `grep(1)` manual — `/usr/share/man/man1/grep.1.gz` | docs | A | GNU grep 3.12 pattern-file and `-F`/`-P`/`-z` option semantics; not this lane's matcher contract | “OPTIONS / Pattern Syntax” (`-F`, `-P`), “Matching Control” (`-f`), and “Other Options” (`-z`); GNU grep 3.12-modified (2025-03-21), installed `grep 3.12-2`; file SHA-256 `9b027d022ae9533ff3e140ba8d96ccd58955bdf9d1c818c327fd992e575c85ba` | `-f` reads one pattern per line, so a newline-containing span cannot be transported as one `-f` pattern [INFERENCE]; `-F` selects fixed-string syntax, while `-z` makes input/output records NUL-terminated and does not change the documented pattern-file delimiter. | mined | 2026-10-23 | on-release | corpus/knowledge/long-span-argv-r34.md |

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
- Keeping records current — S029 → S032 → S033 → S023: periodic currency
  assessment, then measured update signals (not actual updates), then separate
  derivation and entity-time properties. Scheduling and recording the next
  verification is the lane's inference, not a Cochrane or PROV requirement.
  S025 is a rejected HTTP analogy, not authority for research-record validity.

## Search log

- Round 32 (2026-10-23 UTC): questions: (C1) what call takes an exclusive lock
  on an open file descriptor, so two appenders of one manifest can serialize
  their last-byte probe and append; (C2) what does "could not be followed" say
  about a source — does an origin-server unavailability status say anything
  about a local copy? Searched only registered hosts (docs.python.org,
  www.rfc-editor.org), as the open L0 fetch-scope question asks. Identified 2,
  screened 2, included 2 (S060, S061), excluded 0. Both bodies were fetched by
  a scribe seat and re-fetched by the L1 (same SHA-256, each quote found once).
  Not opened: `https://docs.python.org/3/library/os.html#os.open` (O_APPEND),
  `https://en.wikipedia.org/wiki/Link_rot` (lower tier than the RFC for the
  same point). Stop rationale: each claim's contract has one primary source
  for the one external fact it uses; the rest of each contract is lane design.
- Round 31 (2026-10-23 UTC): question: how does a citation name a line or line
  range inside a text resource, and how does a check pin the exact bytes a claim
  was made against? Searched only registered hosts (www.rfc-editor.org,
  www.w3.org, docs.python.org), as the open L0 fetch-scope question asks.
  Identified 4, screened 4, included 3 (S057 to S059), excluded 1: the
  extensionless `https://www.rfc-editor.org/rfc/rfc5147` fetch answered 301 with
  an empty body and was not followed; the same RFC was opened as `.txt` on the
  same host (S057).
- Round 30 (2026-10-23 UTC): question: what defines where an HTML head ends
  when `</head>` is omitted, and why a socket timeout does not bound a whole
  fetch or pin the address that was checked. Searched only registered hosts
  (www.w3.org, docs.python.org), as the open L0 fetch-scope question asks.
  Identified 8, screened 8, included 7 (S050 to S056), excluded 1: the undated
  `https://www.w3.org/TR/html52/syntax.html` now redirects to
  html.spec.whatwg.org, an unregistered host; flip: none needed, the dated W3C
  snapshot (S050, S051) states the same rule. Stop rationale: each changed
  contract item (v2 items 1 to 3) has one primary source. S051 and S050 share
  one page URL, and S053 and S052 share one page URL, with different sections
  and scopes (census warning W04).

- Round 29 (2026-10-23 UTC): question: what standards and documentation
  define how a quote is located in a web page and how page text is
  normalized. Searched: W3C TR, WICG, Unicode reports, Python documentation.
  Identified 4, screened 4, included 4 (S046 to S049), excluded 0. Stop
  rationale: each normalization and matching rule of the round-29 tool
  contract has one primary source. Also re-opened for the C1 fixture, with no
  row change: S002, S003, S008, S013, S019, S020, S038, S044. Finding: the
  S047 page omits `</head>`, so the round-29 extractor reads it as empty
  (`lessons/round-29.md`).

- DERIVED round28 negative-publication curation (2026-10-21): Python path-API
  documentation and the prior committed diagnosis were opened as S044–S045.
  Their scopes are API semantics and historical diagnosis, not authority for
  a privacy-policy relaxation. Parent did not approve the proposed default/
  nested-root exemption; denylist not waived. The new S045 teaching cell was
  corrected before publication under CURRENT_MAIN_DIRECTIVE
  C28_NEGATIVE_PUBLICATION_v2; v1/new-row hashes and history remain private.
  Two selected GNU manual requests timed out before opening and produced no
  source rows or behavioural evidence. No raw new probe output is admitted.
  Question: which opened authority distinguishes API identity from policy
  approval? Selected locations: Python docs, two GNU manuals, old diagnosis.
  Identified4/screened4/included2/excluded2 (unopened timeouts); these are
  curation-event counts, not behaviour. Stop after scoped API and historical
  authority were available; no privacy-policy inference was admitted.

- Round27 local repair curation (2026-10-21): question — which reported r26
  failures falsify the actual usage/date/registry contracts? Where: the six
  named committed falsifier reports in S040–S042 and their matching gate
  functions at base64eec5d4. Identified6 reports, screened6, included6 grouped
  into3 scoped own-work rows; excluded0 reports. No external source or live
  target was fetched. Stopped after every routed failure class had a located
  report and production site; no exhaustive whole-parser correctness claim.

- Round26 scheduling and declaration-link curation (2026-10-21): question —
  which opened sources support the distinction between declared deadlines,
  actual review/update work and provenance links? Where: the frozen lane
  spec/reader receipt and three selected public primary documents (Cochrane
  LSR guidance, Python datetime documentation, W3C PROV-DM), plus existing
  S029 reopened for the periodic-assessment clause. Identified7, screened7,
  included6 new scoped rows S034–S039 plus the existing S029 backlink,
  excluded0 in this bounded selected set. Other build source reports remain
  advisory leads, not an asserted exhaustive search or implied admissions.
  Stopped when each retained distinction had a located primary/own-work
  statement; generic due/freshness and registry policies remain explicitly
  the lane's design rather than external requirements.

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


Round-25 falsify curation correction: S029–S032 supersede S019/S022/S024/S021
for the locator and teaching precision flagged by fresh source re-openers.
They reuse the same actually re-opened sources this round; no extra search
or quota is claimed. S019 mined→queued and used-by metadata-screen-r25.md→—;
the entry now cites S029. Other old row cells unchanged. Original broader
teachings remain as superseded history, not unmarked current advice.

S033 also supersedes S020: entity lifetime is not verification validity. S020
mined→queued and used-by metadata-screen-r25.md→—; the entry now cites S033
and labels the source/date mapping as a lane inference.
