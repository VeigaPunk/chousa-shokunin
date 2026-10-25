ATTACKS: S094 registry row — amendment entry lines 18, 19, 24, 25, 26, 28, 34, 35 — capture a9cf41709b6fa5028332d98c.txt
VERDICT: holds

Verdict: S094 holds. Every anchor, quoted string, and stated offset verified verbatim against the capture (sha256 d24f2315aad72d7ba64faa65d2da70bd05702f7404ac63a624a0803ffe78b136, 83246 bytes). No failure in any of the four required checks. All Observation/Inference sentences citing S094 are supported; none overstated or contradicted. Minor stylistic remarks (no defect): §3.3's relevant content is located structurally under the "4.1 Correlation-Enhanced Claim Verification" heading column at char 21845, the row's `observed:` cell ends mid-sentence, and the "NOT" quote's curly quote is one capture line (spans/S094-3.txt).

## Commands and decisive output
- Read SOURCES.md line 104 (S094 row), amendment lines 1-35, quotes.tsv rows 23-27/30/34-35, spans.tsv rows 23-27/30/34-35, spans/S094-*.txt, build-spans.py.
- `python3 /tmp/s094check.py`:
  - ROW.a19167 count=1 offs=[19167] slice_ok=True; ROW.a20462 count=1 offs=[20462] slice_ok=True; ROW.a20650 count=1 offs=[20650] slice_ok=True
  - All 21 quoted strings count=1; offsets: "We extract 1,000 claims" 16218, "FEVER (Thorne et al., 2018) develop-" 16312, "We recruit two NLP" 20004, "In summary, 1,043 claim-evidence correlations" 20834, "are annotated for 1000 claims" 21015, "The Cohen's Kappa (Cohen, 1960) score for inter-" 21381, "annotator agreement is 0.792, indicating substantial" 21560, "Label 0: Evidence definitely supports Claim;" 16134, "Label 6: Evidence has no relation with Claim." 13669, "For the real-world set, the claims are identical to" 21837, "Google Custom Search Engine API" 22496, "no evidence provided, we re-assign labels based" 20282, "on the claim-relevant evidence gathered from open" 20459, "websites. This manner results in total 202 "NOT" 20640, "CorFEVER (Closed-domain)    333     333     333" 17830, "CorFEVER (Real-world)       426     443     131" 17963, "To avoid claim label reversals due to introduc-" 19167, "the claims are identical to" 21861, "This manner results in total 202" 20650, "the claim-relevant evidence gathered from open" 20462
  - All 17 stated source offsets confirmed (16134, 13669, 16218, 16312, 20004, 20834, 21015, 21381, 21560, 17830, 17963, 19167, 20282, 20459, 20640, 21837, 22496): each sits at the stated content — labels 0 and 6, extraction/develop set, two NLP, summary lines, Kappa, 0.792, Table 2 rows, guard sentence, relabell sentences, real-world sentence, Google Custom Search Engine API
- `python3 /tmp/s094span2.py`: every span file is the exact capture slice at spans.tsv offset and the quote sits at 80 within it, so offset+80 = the Registry char N: 21480+80=21560, 21781+80=21861, 20570+80=20650, 20382+80=20462, 19087+80=19167, 21757+80=21837, 17750+80=17830, 17883+80=17963 — all pass. Capture sha256 in spans.tsv matches `sha256sum`.
- `python3 /tmp/s094ctx.py` / `/tmp/s094guard.py` / `/tmp/s094check2.py`:
  - Labels 0-6 all present: 0@16134, 1@16659, 2@17248, 3@11764, 4@12455, 5@13072, 6@13669 (seven labels)
  - Table 2 header "Dataset SUP. REF. NEI" present; rows and values match; FEVER dev set row also present
  - "For the real-world set, the claims are identical to those in the closed-domain CorFEVER." verified
  - Guard sentence continuation: "up to 5 pieces of evidence in the closed-domain CorFEVER are transferred to real-world one in addition to the evidence from open websites." verified
  - No agreement/Kappa statistic appears in the §3.3 real-world region except the 0.792 closed-domain sentence at 21393-21613 — so "reports no agreement figure for the 202 relabelled claims" is confirmed
  - Table 2 arithmetic verified: 333+333+333=999 vs stated 1,000 (off by one, -1); 426-333=93, 443-333=110 (rise 203), 333-131=202 (fall); rise exceeds fall by 1 — "off by one claim" wording exact

## Sentence judgments (S094 cites)
- L18 supported (7 exact quotes at stated offsets; seven labels; 0.792 substantial; 1,043/1,000)
- L19 supported (identical claims, Google API, relabell sentence, Table 2 rows, up-to-5 transfer)
- L24 supported ("annotator agreement is 0.792, indicating substantial" 21560; distinct units across four figures)
- L25 supported ("the claims are identical to" 21861; 202@20650; NEI 333->131)
- L26 supported ("the claim-relevant evidence gathered from open" 20462; guard@19167)
- L28 supported ("For the real-world set, the claims are identical to" 21837)
- L34 supported (no agreement figure for 202; Table 2 off-by-one arithmetic confirmed)
- L35 supported (corrections match capture: 3-class/5-annotator 0.6841, seven correlation labels, 202 for CorFEVER real-world copies not FEVER labels)

## Residual risk
- No live fetch performed (L0 scope 8d77e6c1). Capture is a text-layer PDF render with interleaved columns and glyph-remap artifacts in right-column lines; all quoted strings match it byte-for-byte, but the PDF's printed glyphs cannot be re-verified from this capture.
- Row `observed:` cell (328 chars) ends mid-sentence, cutting off the evidence-pool conclusion; no factual overclaim in what it does state.

## Tooling
No tools installed; no network egress.
