# What an AVeriTeC archive field documents, and what it does not establish

source: S082 — https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md — the JSON field dictionary, claim-level and answer-level fields — capture chars 1027 and 1969
source: S083 — https://arxiv.org/html/2305.13117v3 — the data-collection paragraph on caching evidence pages (capture char 14575) and Appendix J.4.1 annotation guideline 8 (capture char 120884)
verified-at: 2026-10-25
recheck: 365d
ground: when a verification corpus pairs a cited URL with an archive link, what does the link field document, and what does an empty or a filled field let a reader conclude? Opened from on-disk captures; the located spans are committed in `corpus/evidence/round45/spans/`. The filename is the package's label, not a lane round number.

#### Observation

- At the answer (evidence) level, the README describes `cached_source_url` as "An archive.org link for the source url" — no qualifier (S082, capture char 1969).
- At the claim level, the README describes `cached_original_claim_url` as "Where possible, an archive.org link to the original claim url" (S082, capture char 1027). The neighbouring field `original_claim_url` is itself conditional: "If the claim first appeared on the internet, a url to the original location" (S082).
- The paper says that, to avoid sources disappearing from the web, "we cache all pages used as evidence in the internet archive" (S083, capture char 14575). It says nothing of caching claim URLs.
- The paper does not restate the field dictionary: `cached_source_url`, `cached_original_claim_url` and `original_claim_url` occur zero times in the capture, and its one "Where possible" is the annotator guideline on extractive answers, not on archiving (S083).
- The paper's annotation guideline 8 warns that fact-checking articles may carry double-archived links (an archive.org capture of an archive.is page) and that "Archive.org returns a 404 page for these" (S083, capture char 120884, Appendix J.4.1).

#### Inference

- The two fields are documented asymmetrically. The evidence-level archive is stated without condition and matches the paper's caching sentence; the claim-level archive is best-effort. Lane inference.
- An empty `cached_original_claim_url` records only that no archive link is stored. It does not say why: the claim may never have appeared online (then there is no original URL to archive), or an archive attempt may have failed or been skipped. It does not mean that no archived copy of the claim's page exists anywhere. Lane inference, narrowed after the round-45 critic `CritFieldPolicyInference`.
- An answer that names a source and stores no archive link — the field empty, absent, or holding something other than an archive.org link — contradicts the documented practice. In the training split that is not the rare empty field but the far commoner absent field (`corpus/knowledge/evidence-snapshot-coverage-r40.md`).
- A filled archive field is a link, not proof that the archived capture resolves: the corpus's own guideline names a class of archive.org link that returns a 404. For claim-vs-source verification, a record that relies on a corpus's archive link should open that link, not count it.

#### Unknown

- No archive link was opened (no fetch this round): whether any particular stored link resolves today is not known.
- The documentation does not say why a given claim's archive is missing; no per-record cause is inferred.
- The README is a field dictionary, not a process record: it says what a field is meant to hold, not that archiving was attempted for each record. How the stored values actually fall is measured in `corpus/knowledge/evidence-snapshot-coverage-r40.md`.
