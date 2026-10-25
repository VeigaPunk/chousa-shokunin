ATTACKS: S093 registry row (SOURCES.md:103) anchor cell; every S093-citing sentence in claim-support-test-r37-amendment-2026-10-23.md; capture 44be8711b50a9daae2865b02.txt sha256 ab3427c377d1991032d5165cbb6f08bb6ea29d964dda78b2363811dc0c2b2ba4 (52704 chars)
VERDICT: holds

Re-opened the capture; verified with Python (no tools beyond read/bash): capture = open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/44be8711b50a9daae2865b02.txt').read(); len=52704.

(1) Anchor-cell slices — all confirm capture[N:N+len(q)]==q and capture.count(q)==1:
- char 5157: '7,675 annotated claim-evidence pairs' → match=True count=1
- char 13373: 'If there is both supporting and refuting evidence the claim-label is DISPUTED' → match=True count=1
- char 16287: 'average inter-annotator agreement (Krippendorff’s alpha) of 0.334' → match=True count=1

(2) Every quoted string in the entry attributed to S093 — all verbatim, each exactly once:
- L16 'We collect 1,535 claims on the Internet.' @4846 (L16's declared char 4846)
- L16 'We call this database of 7,675 annotated claim-evidence pairs the climate-fever dataset.' @5132 (declared 5132)
- L16 'The micro-verdict is given by the majority-vote for each claim-evidence pair (or it is NOT_ENOUGH_INFO on a tie).' @13139
- L16 'The claim-label is by default NOT_ENOUGH_INFO unless there is supporting ( SUPPORTS ) or refuting ( REFUTES ) evidence. If there is both supporting and refuting evidence the claim-label is DISPUTED' @13253
- L17 'we collect five individual votes per claim-evidence pair' @12844
- L17 'Each evidence sentence is labelled by at least two voters' @15028 (region continues '…( 2.4 ± ± 0.7 2.4\pm\pm 0.7 voters per evidence on average).')
- L17 'The distribution for aggregate claim-labels SUPPORTS , REFUTES , DISPUTED , and NOT_ENOUGH_INFO is 655 (42.67%), 253 (16.5%), 153 (9.97%), and 474 (30.88%).' @15147
- L17/L24 'average inter-annotator agreement (Krippendorff’s alpha) of 0.334' @16287
- L27 '7,675 annotated claim-evidence pairs' @5157; 'If there is both supporting and refuting evidence the claim-label is DISPUTED' @13373

(3) `source:` (L4) and entry char offsets — all confirmed:
- 4846 → 'We collect 1,535 claims on the Internet. For each claim, we algorithmically retrieve the top five…'
- 5132 → 'We call this database of 7,675 annotated claim-evidence pairs the climate-fever dataset.'
- 12844 → 'we collect five individual votes per claim-evidence pair, which allows us to analyze confidence…'
- 13139 → 'The micro-verdict is given by the majority-vote for each claim-evidence pair (or it is NOT_ENOUGH_INFO on a tie). …'
- 13253 → 'The claim-label is by default NOT_ENOUGH_INFO unless there is supporting ( SUPPORTS ) or refuting ( REFUTES ) evidence. If there is both supporting and refuting…' (DISPUTED completes at 13373)
- 15028 → 'Each evidence sentence is labelled by at least two voters ( 2.4 ± ± 0.7 … voters per evidence on average).'
- 15147 → distribution sentence (as above)
- 16287 → alpha sentence
- 35032 → 'Table 4: Classification report with respect to the performance of the baseline claim validation pipeline evaluated on climate-fever …'; table body: SUPPORTS support 474, REFUTES 253, NOT ENOUGH INFO 655, weighted avg support 1382 (and 1382 twice more)
- 46553 → 'Verdict: Disputed' block of Example D.6 (D.3), the claim-label appendix; per-evidence lines under it read Not_Enough_Info/Supports/Refutes, and the 'Verdict: Disputed' is emitted at claim level. Second 'Verdict: Disputed' at 47801 (D.4 header).

(4) Judgment on S093-citing Observation/Inference sentences:
- L16: supported. Claim-label aggregation rule verbatim at 13253; §2.3 defines micro-verdict by majority-vote; DISPUTED appears only at claim level (13253; also 37649 'otherwise the claim-label is DISPUTED'); Appendix D prints claim-level 'Verdict: Disputed' beside per-sentence votes (46553, 47801). 'Verdict:' and 'Disputed' are code-style tokens, not quotes; both exist.
- L17: supported. Distribution sentence verbatim at 15147 (percentages match text: 655/1535=42.67%, 474/1535=30.88%); §3's 'five individual votes' at 12844 vs 'at least two voters' at 15028; Table 4 support column indeed 474 SUPPORTS/655 NOT ENOUGH INFO over 1382, the reverse of §3.
- L24: supported (S093 part). Alpha sentence verbatim at 16287; the inference follows from it.
- L27: supported. '7,675 annotated claim-evidence pairs' verbatim at 5157; DISPUTED verbatim at 13373; inference follows.
- L35: supported. 'α 0.334' is a numeric reference (not a paper quote) — the captured value is 0.334; 'Table 1' exists (16539, 17118: 'Table 1 details the level of disagreement on a per-slice basis', 10 slices of 770 claims, 3,850 pairs each). 'DISPUTED as a claim-level aggregate' stands per 13253.

Failures: none in scope. No sentence citing S093 is overstated or contradicted; no unverified claim remains.

[INFERENCE] Observation: round47 spans.tsv rows for S093 use different offsets than this evaluation (alpha 16207 vs 16287; pairs 5077 vs 5157; DISPUTED 13293 vs 13373; claims 4766 vs 4846) — not adjudicated here (span-file task is separate from the row/entry attack). Also noted: 3850×10=38500 ≠ 7675×5=38375; 7675×2.4=18420 — the capture's own numbers are internally inconsistent about total voter-annotations (7,675 × 5 pairs = 38,375 vs Table 1's 38,500), and §3's 2.4 is the realised per-evidence-sentence figure; the entry's 'five votes per pair' vs '2.4 voters' contrast is faithful to the capture.

All reads used absolute paths; scratch under /tmp/chousa-r47w2-ReopenS093 removed. No installs. No fetches. No lane/fleet writes beyond this report.
