# FxSrcSchema — Round 25 advisory review

Axes: freshness; calibration.
Checkpoint: read-only `HEAD` observed as `e93ac711f885a10d44fdd80a1734997419595b5a`. This is source-only review; no gate/count run.

## Findings

- **P3 — S019 quote location is not exact.** `corpus/lessons/round-25.md:68` labels the quote “Key Points” and includes “All Cochrane reviews…”. The freshly opened Cochrane page's Key Points bullet starts “Cochrane reviews should be assessed periodically to determine whether an update is needed” (13 words, without “All”); the exact “All Cochrane reviews…” sentence appears later in §IV.1, not Key Points. Correct either the location to §IV.1 or quote the actual Key Points wording. `SOURCES.md:29` anchors both Key Points and IV.1–IV.2, so the underlying periodic-assessment claim is supported.
- **P3 — S019 `teaches` overstates recording.** `corpus/SOURCES.md:29` says deciding to update is a “recorded, periodic act”; the cited Key Points / §§IV.1–IV.2 establish periodic assessment and decision factors, not that every assessment/decision is recorded. Keep S019 mined for periodic Cochrane-review assessment, but remove or explicitly mark “recorded” as a lane inference. The actual use is calibrated more carefully: `corpus/knowledge/metadata-screen-r25.md:20-27` labels the mapping an inference and says neither source prescribes the header.
- **P3 — S024 row’s comparison needs clearer anchoring.** The fresh `https://schema.org/lastReviewed` page matches the Gate quote at `corpus/lessons/round-25.md:73` exactly (16 words: “Date on which the content on this web page was last reviewed for accuracy and/or completeness.”). It identifies a Schema.org Property, expects `Date`, and lists `WebPage` under “Used on these types.” `corpus/SOURCES.md:34` calls its scope both definition and declared use, but the anchor only names the heading/definition; its teaching also compares publication/modification dates, which this property page does not explicitly compare. The comparison is consistent with Schema.org's separate `datePublished` and `dateModified` definitions, but those anchors are absent here. Narrow the scope/teaching to this page or cite the comparator definitions if retaining the comparison.

## Decision and residual risk

- **S019 mined: agree narrowly** for periodic assessment of Cochrane reviews, subject to the quote-location and “recorded” wording corrections above.
- **S020 mined: agree narrowly.** The exact Gate quote at `round-25.md:69` is present in PROV-O §3.2's entity-lifetime paragraph; `SOURCES.md:30` explicitly excludes verification/recheck policy. The knowledge entry labels its `source:` / `verified-at:` mapping as inference and disclaims header endorsement (`metadata-screen-r25.md:20-27`). PROV-O generation/invalidation times are entity-lifetime facts, not themselves a claim-verification timestamp; retain that distinction.
- **S024 queued: agree.** Definition quote is verbatim; `used-by` is `—`, so it is not presented as an admitted source for a knowledge entry. Keep queued until used, with the row anchoring caveat above.
- **S025 rejected: agree.** Lesson `round-25.md:74` cites RFC 9111 §4.2; the actual equation is in that HTTP-cache freshness section. `SOURCES.md:35` correctly rejects it as authority for research-record validity and gives a meaningful flip: labelled analogy only, paired with a directly relevant method source.

Packaging history preserved: `round-25.md:111-125` records that `0fc037e` omitted `tools/research-gate.sh`; `round-25.md:127-133` records that `d8c8cff` also omitted `corpus/evidence/README.md`. The corrected full pin observed here is e93ac above; no gate/count result was rerun by this source-only seat. Round-25 outside admit/reject closure was not performed by this lane (`round-25.md:103-105`); these judgments remain advisory.

Installs: none.
VERDICT: Agree with the four status decisions as scoped; S019's quote locator/recorded claim and S024's anchor/teaching need the stated calibration corrections before outside closure.