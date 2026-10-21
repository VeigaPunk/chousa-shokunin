# Shojania et al. (2007) source finding

## Access and source evidence
- Final URL opened: https://pubmed.ncbi.nlm.nih.gov/17638714/ (effective URL unchanged; access date: 2026-10-21).
- HTTP outcome: direct GET returned HTTP/2 203 (`curl -L -sS -o /dev/null -w 'http_code=%{http_code}\nurl_effective=%{url_effective}\n' URL` → `http_code=203`, `url_effective=https://pubmed.ncbi.nlm.nih.gov/17638714/`). Raw HTML was a cookie/PoW challenge, so direct page access was challenge-limited, not shown as a paywall. The reader separately fetched the bibliographic record and abstract via NCBI E-utilities; full-text access was not established.
- Source quote, verbatim (14 words): “A signal occurred within 2 years for 23% of reviews and within 1 year for 15%.” — Abstract, Results. The retrieved abstract also reports 57% with an update signal and median survival free of a signal of 5.5 years.
- Evidence provenance: `read` of the URL returned title, citation (Ann Intern Med. 2007 Aug 21;147(4):224–233; DOI 10.7326/0003-4819-147-4-200708210-00179), abstract, and “Fetched abstract via NCBI E-utilities”; `read` with `:raw` showed the challenge HTML. Lane preregistration: `corpus/evidence/round25-claims.md:10-50`; source contract: `/home/vgpnk/Projects/shokunin/CORPUS.md:86-115`.

## Proposed registry fields
- kind: `paper`
- tier: `A`, scoped only to the primary study's measured update-signal timing in its defined sample of 100 quantitative systematic reviews; not a general rule for all knowledge records.
- scope: Empirical frequency and timing of signals that may warrant updating systematic reviews relevant to clinical practice.
- anchor: Abstract, Results; publication date 2007-08-21; PMID 17638714 / DOI 10.7326/0003-4819-147-4-200708210-00179.
- teaches: Signals warranting review updates occurred on varied timescales in the studied cohort, including within one or two years; freshness checks need to account for potentially early change.
- status recommendation: `queued` (candidate next ID S019; no `used-by` yet). The study is opened and relevant empirical context, but under contract v1 it becomes `mined` only once cited by a knowledge entry/path (`CORPUS.md:103-108`).

## Claim fit
- Verdict: **partial**. It supports that update signals can arise early and at different times (Abstract, Results), lending empirical rationale for freshness checks. It does not test whether a scheduled date/cadence makes a record's staleness computable, and says nothing about `source:` or `verified-at:` provenance as a precondition for re-verification. Those metadata requirements are not established by this paper; the round-25 claim itself is framed at `corpus/evidence/round25-claims.md:12-15,20-40`.
- Recommendation: Admit as `queued` for the narrowly stated empirical scope, not as sole support for the metadata-screen claim. Reassess/cite it only if a knowledge entry needs evidence about review-update timing; do not represent it as evidence for the metadata mechanism.

VERDICT: Admit queued as scoped empirical context; partial support for the broader freshness rationale, no support for the proposed provenance precondition.
Installs: none.
