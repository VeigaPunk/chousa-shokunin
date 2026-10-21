# Garner et al. 2016 — source check

- **Access date:** 2026-10-21.
- **Final URL actually opened:** https://www.bmj.com/content/354/bmj.i3507 (the browser's transient Cloudflare challenge URL added a query parameter; the destination remained this article page).
- **HTTP outcome:** blocked, not confirmed paywalled. Static fetch returned HTTP 403. Browser navigation returned HTTP 307 followed by HTTP 403; the 403 response carried `cf-mitigated: challenge`. No article text was served.
- **Quote/location:** none available. The source body was blocked before any section or heading could be inspected; I will not quote from memory.

## Proposed registry fields (conditional, not admitted)

- **kind:** paper.
- **tier:** A, scoped only to the authors' own consensus/checklist recommendations, if the article is accessible and those contents are verified. This is a provisional classification, not a tier judgment from inspected text.
- **scope:** the article's own recommendations on when and how to update systematic reviews; not general source-record metadata requirements.
- **anchor:** unavailable; exact section/heading and publication revision could not be verified from the blocked page.
- **teaches:** unavailable from inspected source text. [INFERENCE from the title only:] it may teach criteria for deciding when and how to update a systematic review. The title alone does not establish a lesson about `source:` or `verified-at:` provenance fields.

## Claim assessment and recommendation

- **Claim:** “a scheduled recheck (date or cadence) makes a record's staleness computable; provenance metadata (source, verified-at) is a precondition of re-verification.”
- **Verdict:** **no — not established by the accessible evidence.** This is an access verdict, not a finding that the article substantively contradicts the claim. The article could not be read, and its supplied title concerns systematic-review updates rather than source-record provenance; no support/partial-support judgment about its contents is defensible without the text.
- **Recommendation:** **reject for this round** because the source content, exact anchor, and grounded teaching could not be inspected; do not add a registry row on title-only evidence. **Flip condition:** re-open the BMJ page (or an official BMJ-hosted full-text version) successfully, then record the exact section/heading, access date, and a ≤25-word quote grounding the teaching; reassess the claim narrowly, especially whether the article actually covers provenance fields and scheduled rechecks.

**Evidence locations:** `CORPUS.md:86-108` (registry columns and tier/scope/anchor/teaches definitions); `CORPUS.md:112-115` (row requires opening in-round and a located quote); `corpus/SOURCES.md:1-10` (lane registry header); tool result for `https://www.bmj.com/content/354/bmj.i3507` (HTTP 403) and browser request record (307 then 403, Cloudflare challenge).

VERDICT: Reject this round as inaccessible; source-specific support remains unassessed until the article text is retrievable. Installs: none.