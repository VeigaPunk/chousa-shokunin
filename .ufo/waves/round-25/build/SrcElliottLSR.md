# Elliott et al. 2017 source assessment

- **Access:** 2026-10-21. Final URL opened: https://pubmed.ncbi.nlm.nih.gov/28912002/ (unchanged). Direct HTTP check: `curl -L -sS -o /dev/null -w 'http_code=%{http_code} final_url=%{url_effective}\n' https://pubmed.ncbi.nlm.nih.gov/28912002/` → `http_code=203 final_url=https://pubmed.ncbi.nlm.nih.gov/28912002/`. The page reader successfully fetched the PubMed abstract via NCBI E-utilities; the abstract is accessible, not paywalled/blocked. Publisher full text was not opened.
- **Verbatim quote (14 words):** “systematic reviews that are continually updated, incorporating relevant new evidence as it becomes available.” Location: PubMed PMID 28912002, Abstract (unstructured), LSR definition clause. The record identifies J Clin Epidemiol. 2017 Nov;91:23–30, DOI 10.1016/j.jclinepi.2017.08.010.
- **Proposed registry fields:**
  - `source`: Elliott et al., Living systematic review: 1. Introduction—the why, what, when, and how — https://pubmed.ncbi.nlm.nih.gov/28912002/
  - `kind`: paper
  - `tier`: A, scoped to the original paper's own LSR rationale and definition (not metadata design).
  - `scope`: What this original paper states about why living systematic reviews are used and their continual updating approach.
  - `anchor`: Abstract, unstructured; LSR definition clause; J Clin Epidemiol. 2017 Nov;91:23–30; PMID 28912002; DOI 10.1016/j.jclinepi.2017.08.010.
  - `teaches`: Review currency, accuracy, and utility can decay when reviews are not kept current; living systematic reviews continually incorporate relevant new evidence.
  - `status`: queued; `opened`: 2026-10-21; `recheck`: 365d; `used-by`: — until a knowledge entry cites the row.
- **Claim assessment: partial.** The abstract states that failure to keep reviews up to date leads to decay in currency, accuracy, and utility, and defines LSRs by continual updating as new evidence becomes available (PubMed record, Abstract). This supports the broad rationale for rechecking current evidence. It does not specify a scheduled date/cadence that makes staleness computable, nor say that source and verified-at provenance fields are prerequisites to re-verification. Those are beyond the observed abstract. The claim's specified header keys are `source:`, `verified-at:`, and `recheck:` (round25-claims.md:26-28); this paper is contextual support, not authority for that metadata contract.
- **Recommendation:** Admit as `queued`, worth mining for the limited LSR/update rationale; do not cite it as sole support for the date/cadence or provenance-metadata parts. `SOURCES.md` contract v1 defines A as primary/authoritative within the stated scope and queued as opened/worth mining (CORPUS.md:93-105); row schema and quote requirement are at CORPUS.md:86-90, 112-115. Current registry paper-row pattern is corpus/SOURCES.md:15-16.
- **Installations:** none.

VERDICT: Admit queued, tier A only for the original paper's LSR rationale and definition; partial support for the broader freshness/provenance claim.