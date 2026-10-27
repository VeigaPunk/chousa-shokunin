# SourceCaptureScout — bounded source-evidence findings

## Scope and result

Read-only analysis of frozen round-60 claims, the current local S101 capture/text rendering and related prior committed records. No external/live fetch, no git/jj operation, and no source/corpus edits. **C2 source-text component is supportable only as a statement about this captured copy; present-day validity and CNKI implementation remain unknown.** This does not adjudicate C2's counter or QUALITY admission, and does not judge C1.

## Observed evidence

- Frozen C2 asks for a scoped correction distinguishing the captured bibliographic type/carrier notation from current validity or CNKI implementation, and requires a source digest, located quote, entry/citation metadata, disposition and QUALITY test (`corpus/evidence/round60-claims.md:13-16`).
- The local round-60 text rendering contains the directly relevant passage at `.ufo/waves/round-60/s101-open.txt:70-78`: for non-paper electronic references, it describes a carrier identifier and gives `[M/CD]`, `[DB/MT]`, `[CP/DK]`, `[J/OL]`, `[DB/OL]`, `[EB/OL]` examples; it says traditional paper references need not state carrier type. The later rendering at lines 240-268 likewise describes type/carrier notation and says the format recommends GB/T 7714 while its reference-list section cites ISO 690/690-2. These are statements in this local rendering, not present-day standards findings.
- Prior committed capture ledger `.ufo`-independent source record `corpus/evidence/round57/refetch.tsv:66` records S101's URL, capture id `6dc68fd6b32ce9c8dfcebce8`, access timestamp `2026-10-27T08:29:36Z`, HTTP 200, raw digest `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`, and text-form digest `d4e7e5adc9f723d61852a6dffd559062ba3db5603c43ec158d96d6d4e564e112`. This is prior recorded capture metadata, not a live re-fetch.
- The current registry lists S101 as an opened tier-B document source for identification of the 2006 edition and carrier (§ scope), with status mined and use by `corpus/knowledge/normative-reference-chain-china-r57.md` (`corpus/SOURCES.md:142-143`; full row should be read there). Its tier/scope do not license a claim about present-day validity or implementation.
- Existing S101 entry `corpus/knowledge/citation-count-semantics-r37.md:4-10,84-86` already characterizes S101 as a hosted copy and limits what it asserts; it records a quote-location/attribution limitation. Thus a proposed correction should quote the local source exactly and preserve that boundary rather than imply CNKI behavior.

## Inference and unresolved gap

The local text supports accurately scoped observations about what this particular captured rendering says. The source evidence alone does not establish current validity, authenticity at origin, the operative standard today, or CNKI's implementation. The round-60 counter's checks, any new entry's exact metadata/disposition and its QUALITY acceptance are not adjudicated by this source-only review. No claim admission verdict follows from this finding.

## Freeze integrity

The assignment specifies immutable claim SHA-256 `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; locally observed `sha256sum corpus/evidence/round60-claims.md` is `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. These differ. The frozen file was not modified. Cause and timing are unresolved; do not treat this observed file as matching the assignment's declared digest.
