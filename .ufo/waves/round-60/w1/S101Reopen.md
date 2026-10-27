# S101 reopen — bounded source-evidence finding

## Result

**Source-text reopening: supported as an offline capture check; present-day validity and CNKI implementation remain unknown.** This is evidence for the narrow source-text side of frozen C2 only, not a finding that the source is current, authentic at origin, or implemented by CNKI. No external/live fetch was made.

## Observations

- The round-60 local reopen `.ufo/waves/round-60/s101-open.txt` includes the carrier notation passage: non-paper electronic references are to carry a carrier identifier, with `[M/CD]`, `[DB/MT]`, `[CP/DK]`, `[J/OL]`, `[DB/OL]`, `[EB/OL]` examples (lines 70–78). Its later section 14.1 recommends GB/T 7714 formats, while 14.4 says “参照ISO 690及ISO 690-2” (lines 240–268). These are directly observed statements in this captured text, not conclusions about current standards or software behavior.
- The capture is locally pinned in the existing source ledger: `corpus/evidence/round57/refetch.tsv:66` records S101's URL, capture identity `6dc68fd6b32ce9c8dfcebce8`, response metadata and SHA-256 `6063a3af…`; `corpus/evidence/round49/spans.tsv:20-25` binds six S101 excerpts to that same full digest. These are prior recorded capture facts, not a live re-fetch.
- The existing knowledge entry correctly limits its account: `corpus/knowledge/citation-count-semantics-r37.md:4-10, 67-86` identifies S101 as a university-hosted copy, frames claims as what copies state, and names version-in-force and application of codes to counted records as unknown. The entry's precise quote limit is recorded at lines 84–86: the register quote attributing GB/T 7714 to the parameter-table sentence is absent as written; the capture places GB/T 7714 in 14.1 and ISO 690 in 14.4 and the table.
- `corpus/evidence/round60/c2-count.py:5-21` pins the raw SHA and round-60 text-form SHA, requires the specific observed phrase once, and checks the entry's S101 citation/metadata and version-limit statement. It verifies presence/pins and limited scope markers, not semantic entailment, source authenticity/currentness, or QUALITY acceptance. It also binds `FORM` to the lane's absolute round-60 text-form path (line 7), even when `--root` varies (lines 13-16); any claim that it reopens a form inside an arbitrary root would be unsupported.
- Historic caution: `corpus/evidence/round42/quarantine-verdicts.tsv:23` records the earlier unchecked S101 registry family as *unverifiable, not fabrication*, because no locator had then been named. Later committed quote/span ledger rows provide locators and capture digest; they do not retroactively turn that earlier event into a contemporaneous check.

## Inference / gap

The local text supports accurately scoped statements about what this particular captured copy says. It does not establish that the document remains in force or that CNKI uses these identifiers; the existing knowledge entry already preserves those gaps. C2's frozen predicate expressly requires the raw capture and text form, citation/metadata and disposition, but this seat has not run that counter or evaluated the proposed entry's QUALITY verdict; therefore C2 is **not adjudicated here**.

## Freeze-integrity discrepancy

The assignment specified immutable claim SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`. The observed `sha256sum` of `corpus/evidence/round60-claims.md` was `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`, which does **not** match. I did not edit the frozen claims. This is a provenance discrepancy; without the expected bytes/hash source beyond the assignment, its cause and timing are unresolved.

## Evidence boundary

Read-only inspection of the frozen-claims file, local S101 text, C2 counter, existing S101 knowledge entry, source registry and prior round evidence. No source/live network access, no edits besides this report, and no git/jj operations.