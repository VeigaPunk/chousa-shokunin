ATTACKS: S085 registry row (SOURCES.md), every S085-citing sentence in claim-support-test-r37.md, capture 5a631adb18988a1a2421ce75
VERDICT: holds

Capture: /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5a631adb18988a1a2421ce75.txt, 4146 bytes, sha256 e18eeb26a5a5902e10f0e0b25a9886d99bbbafcf8adfb85b7846bbd569d1ba92 (matches spans.tsv capture_sha256 column).

## 1. Row anchor cell — all verify
- char 2360 "A list of evidence sets": capture[2360:2383]==quote, count==1 (context: "evidence : A list of evidence sets (lists of …").
- char 1271 "Pre-processed Wikipedia Pages (June 2017 dump)": capture[1271:1317]==quote, count==1; inside Download Links (heading @1124 < 1271).
- Footer: "refs/heads/live build 385" @4047 count 1; "Last updated: 2026-04-02" @4073 count 1 (capture: "Last updated: 2026-04-02T10:58:13.945736", verbatim substring).
- No "revision" anywhere: grep -ci revision|revid|oldid|version over capture -> 0; "2017" count 1. Row gloss "names no page revision … fixed pool" is an interpretation of these facts (the page's own text never says the pool is fixed), noted as gloss.

## 2. Entry source line (line 3) offsets
- 986: "For the first two classes, the annotators also recorded the sentence(s)" — in FEVER Dataset paragraph (paragraph starts @713 "FEVER Dataset").
- 2222: "label : The annotated label for the claim." (field start; quote itself starts @2265).
- 2349: "evidence : A list of evidence sets (lists of …" — field start.
- 2462: "a [Annotation ID, Evidence ID, null, null] tuple if the label is NOT ENOUGH INFO" — tuple alternative, verbatim, count 1.
- 2589: "are for internal use only and are not used for scoring" — verbatim, count 1.
- Build info claims verified (above). No mismatch.

## 3. Quotes in Observation (line 14), attributed to S085 — all verbatim, count 1
- 2265 "Can be one of SUPPORTS|REFUTES|NOT ENOUGH INFO" ✓ (label value; source-line 2222 is the field start)
- 2349 "evidence : A list of evidence sets" ✓
- 2462 "a [Annotation ID, Evidence ID, null, null] tuple if the label is NOT ENOUGH INFO" ✓
- 1013 "the annotators also recorded the sentence(s)" ✓
- 1059 "forming the necessary evidence for their judgment" ✓
- 2589 "are for internal use only and are not used for scoring" ✓

## 4. Inference backticked quotes (lines 23-25) — verbatim, count 1, offsets
- line 23: "a [Annotation ID, Evidence ID, null, null] tuple if the label is NOT ENOUGH INFO" @2462.
- line 24: "For the first two classes, the annotators also recorded the sentence(s)" @986.
- line 25: "Can be one of SUPPORTS|REFUTES|NOT ENOUGH INFO" @2265.

## 5. Judgment per S085-citing sentence
- Line 14 Observation (Absence of evidence is a labelled outcome): supported. All six quotes verbatim (above). Gloss "the two positions the null tuple keeps are for internal use only and are not used for scoring": the annotation says the Annotation ID and Evidence ID fields are for internal use only and are not used for scoring; the NEI tuple's two non-id positions are the URL/sentence-ID slots (tuple definition @2423), so "keeps" = the tuple's two non-id slots. Reasonable reading, not an overclaim. Also quotes S091/S090 (out of scope here).
- Line 23 Inference: supported — FEVER has the NEI label AND the evidence field either lists evidence sets or is the null tuple; the pool is the June 2017 dump (char 1271 anchor). "fixed pool" is the row's gloss (the dump is one dated snapshot), noted.
- Line 24 Inference: supported — FEVER requires sentence evidence only for the first two classes: the 986 quote is in the FEVER Dataset paragraph, "For the first two classes, the annotators also recorded the sentence(s) / forming the necessary evidence for their judgment." (S090 quotes out of scope.)
- Line 25 Inference: supported for the S085 half (verbatim @2265); cross-source synthesis (S091/S090) out of scope.
- Line 36 Unknown (staged material corrected): supported — the page offers the null tuple as the alternative to "A list of evidence sets" (verbatim @2349/2462), "nulls only the Wikipedia URL and sentence ID positions" (tuple definition @2423: "[Annotation ID, Evidence ID, Wikipedia URL, sentence ID]"), and the "are for internal use only" sentence @2589 confirms unscored ids. No word "revision" in capture.
- Line 8 ground: "staged ids bind … by document (URL equality)" — matches: row URL == entry source URL == spans.tsv URL.

## 6. Span manifest crosscheck (not a claimed counter, but consistent)
spans.tsv rows for S085 (3): offsets 2382/906/2185 are quote-start minus 80 (CONTEXT=80, per build-spans.py docstring); slices spans/S085-{1,2,3}.txt byte-equal capture[off:off+len]; quote found at span index exactly 80, i.e., capture char 2462/986/2265 — the same offsets the row/entry state. quotes.tsv 3 rows match. No failures.

## Failures
None. (One out-of-scope probe: evidence-pool-versioning-r39.md line 15 cites "char 2593 of the S085 capture" for "for internal use only"; capture[2593:2615] == that text — also fine.)

No tools installed; no fetch; no mutations; scratch dir unused.
