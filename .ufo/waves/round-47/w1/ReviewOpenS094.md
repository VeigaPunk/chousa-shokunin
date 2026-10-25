# ReviewOpenS094 — open lane S094 (CorFEVER, COLING 2025) from capture, round 47 wave 1

## Item
Open lane source S094 (https://aclanthology.org/2025.coling-main.108.pdf; staged S115; register S110) from the capture only.
Locate the quotes for its Registry row and the amendment entry, give contiguous unique slices, and say what the source supports
or contradicts in the two staged entries. No fetch was made, no tool was installed, and no lane production file was touched.

## Capture
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/a9cf41709b6fa5028332d98c.txt`
- sha256 `d24f2315aad72d7ba64faa65d2da70bd05702f7404ac63a624a0803ffe78b136`, 83246 bytes, **82876 chars**.
  `sha256(url)[:24]` = `a9cf41709b6fa5028332d98c` (computed), so the filename binds to the URL.
- It is a pdftotext layout render of a two-column page. There is no math markup (`κ` count = 0); "Kappa" is spelled out once, at char 21393.
- Typography matters for the backtick phrases: the capture has `Cohen’s` with U+2019. It has `“NOT ENOUGH` with U+201C but closes with a
  straight `INFO"`. It spells `relabeled` the US way. Every offset below is a Python `str` (code-point) offset, as `c3-count.py` uses.

## Commands (decisive output)
1. `sha256sum; wc -c` printed `d24f2315…b136` and `83246`. Python `len` printed `chars 82876` and `key a9cf41709b6fa5028332d98c`.
2. `q.py` ran a raw `find`/`count` on each candidate. Output: `K_reg find= -1 count= 0`, `K_row` (row recheck "score for inter-annotator
   agreement is 0.792") `-1 0`, `R_reg -1 0`, `N202 -1 0`, `NLP_reg -1 0`. **None of the candidates is contiguous.**
   My first matcher allowed only line-end interleave, and it also returned `[]` for all of them, because whole lines from the other column sit
   between the fragments.
3. `d.py` split each line at col 81 into a left and a right stream (chars 19000–22200), joined `-`+newline splits and collapsed whitespace.
   Output: `K {'L': (21381, 21644)}`, `R {'R': (20304, 20682)}`, `N {'R': (20650, 20830)}`, `NLP {'L': (20004, 20529)}`,
   `M {'R': (19934, 20649)}`, `S {'L': (20834, 21044)}`, `A {'R': (19167, 19549)}`. `Kh` (with the hyphen kept: `inter-annotator`)
   returned `None`. The hyphen sits at a line end, so the capture cannot tell `inter-annotator` from `interannotator`.
4. `v.py` and `f.py` checked each slice with `find`, `count` and `capture[o:o+len(q)]==q`, plus 100 chars of context on each side. Output: below; `ALL_OK True`.

## Per-candidate result
**C1** `The Cohen’s Kappa (Cohen, 1960) score for interannotator agreement is 0.792` has `find=-1`, `count=0`, and is **not contiguous**.
It is present in the left column (§3.2 Closed-Domain Set; header at 16104, and §3.3 follows at 21709) as three line fragments:
[21381) `The Cohen’s Kappa (Cohen, 1960) score for inter-` (8 words, count 1). The right-column tail `The distribution of labels is listed in Table 2.` sits in between.
Then [21560) `annotator agreement is 0.792, indicating substantial` (6 words, count 1), and [21613) `agreement among the annotators.`.
- The longest contiguous unique slice carrying the figure is `annotator agreement is 0.792, indicating substantial` at **char 21560**.
- 100 chars before 21560: `'                                                   The distribution of labels is listed in Table 2.\n'`
- 100 chars after its end: `'\nagreement among the annotators.                                                  4     CorXFact\n3.3'`

**C2** `we re-assign labels based on the claim-relevant evidence gathered from open websites` has `find=-1`, `count=0`, and is **not contiguous**.
It is present in the right column (§3.3 Real-World Set), with left-column lines (`notate claim-evidence correlations based on the`, and so on) between the fragments:
[20282) `no evidence provided, we re-assign labels based` (7 words, count 1); [20459) `on the claim-relevant evidence gathered from open` (7 words, count 1);
[20640) `websites. This manner results in total 202 “NOT`.
- The longest unique slices are `no evidence provided, we re-assign labels based` at **char 20282** and `on the claim-relevant evidence gathered from open` at **char 20459**.
- Context before 20282: `'sh to manually an-\n' + 81 spaces`. Context after: `'\nnotate claim-evidence correlations based on the\n…'`.

**C3** The 202 sentence, `This manner results in total 202 “NOT ENOUGH INFO" claims being relabeled.`, has `find=-1` and is **not contiguous**.
It is present at R 20650–20830, as [20640) `websites. This manner results in total 202 “NOT` (8 words, count 1) and [20794) `ENOUGH INFO" claims being relabeled.` (5 words, count 1).
- The slices are `websites. This manner results in total 202` at **char 20640** and `ENOUGH INFO" claims being relabeled.` at **char 20794**.
- Context after 20640+42: `' “NOT\nhigh-quality annotation.\n…'`. Context before 20794: `'uality annotation.\n' + 81 spaces`.

The register's third quote, `We recruit two NLP researchers … based on the annot`, is also present at L 20004–20529, joining `an-`/`notate`. This agrees
with `.ufo/waves/round-47/w1/QuarReg110.md`, whose offsets 21381/21560/20304/20459/20640 I reproduced independently.

## Deliverable: contiguous unique quotes (8; each count=1, 5–7 words)
```
id	offset	quote
S094	21560	annotator agreement is 0.792, indicating substantial
S094	21381	The Cohen’s Kappa (Cohen, 1960) score for
S094	20282	no evidence provided, we re-assign labels based
S094	20459	on the claim-relevant evidence gathered from open
S094	20640	websites. This manner results in total 202
S094	20794	ENOUGH INFO" claims being relabeled.
S094	19167	To avoid claim label reversals due to
S094	20834	In summary, 1,043 claim-evidence correlations
```
These are phrases a bullet can backtick: `agreement is 0.792`, `Cohen’s Kappa`, `re-assign labels`, `claim-relevant evidence`, `total 202`,
`claims being relabeled`, `claim label reversals`, `claim-evidence correlations`. Slice check, as pasted from `f.py`:
```
for sid,o,q in TSV: r=capture[o:o+len(q)]==q
S094 21560 … slice_eq=True count=1 find=21560 | 21381 True 1 | 20282 True 1 | 20459 True 1
S094 20640 … slice_eq=True count=1 find=20640 | 20794 True 1 | 19167 True 1 | 20834 True 1
ALL_OK True
```
Extra (count 1, one line): `If the evidence fully covers the overall content` at char 74346 (Appendix A.1). Table 2 is at 17830 / 17963.
Suggested `anchor` cell offsets are **char 21560** for the agreement passage and **char 20640** for the relabel passage.

## What the source supports (amendment; the base entry does not cite it)
- Amendment lines 32–37: "CorFEVER reports a Cohen's Kappa of 0.792 for interannotator agreement on claim-evidence correlations" is
  **supported** (21381–21644). The re-assign and 202 sentence is **supported** (19934–20830).
- Row S115 anchor "annotation-agreement and relabelling passages in the closed-domain and real-world sections" is **accurate**: the kappa is in §3.2
  and the relabelling is in §3.3.
- Base entry, lines 20–25: the NOT ENOUGH INFO "declared null" is **corroborated** by `INFO" label in the original FEVER dataset have` (20104) followed by
  `no evidence provided` (20282).
- Amendment observation (S114) that per-evidence verdicts are aggregated into a claim verdict: CorFEVER runs the same procedure, a correlation per
  piece of evidence followed by a verdict "by comprehensively weighing all claim-evidence correlations" (`sively weighing all claim-evidence correlations.`, 23728).

## Contradictions and overstatements (both sides quoted)
1. **Medium (depth/calibration): the scale is conflated.** The amendment (lines 49–50) says "its reliability is measured rather than perfect (0.6841 five-way Fleiss in
   FEVER, 0.792 Cohen's in CorFEVER)". The source's 0.792 is two annotators labelling **claim-evidence correlations** on CorFEVER's own 7-label scale
   (`Label 0: Evidence definitely supports Claim;` at 16134 … `Label 6: Evidence has no relation with Claim.` at 13669). It covers
   `In summary, 1,043 claim-evidence correlations` / `are annotated for 1000 claims` (20834/21015) in the closed-domain set only.
   It is not agreement on the claim verdict, and it does not measure the FEVER test. The source reports no agreement for the real-world set or for the relabelling.
2. **Medium (depth): "demonstrated" and "this error" overstate.** The amendment (lines 53–57) says: "it is demonstrated rather than argued: 202 FEVER claims labelled NEI
   were relabelled … would be repeating exactly this error". The source's own words cut against that reading:
   - `To avoid claim label reversals due to introduc-`/`tion of ambiguity or fake evidence on public web-` (19167/19374).
     The authors treat open-web evidence as a cause of spurious reversals, and they transfer `up to 5 pieces of evidence in the closed-` domain set to offset it.
   - The relabelling is done by the authors, with no reported procedure or agreement. The source never calls FEVER's NOT ENOUGH INFO labels an error.
   - Table 2 shows that 131 of the 333 NOT ENOUGH INFO claims stayed NOT ENOUGH INFO even with web evidence (`CorFEVER (Real-world)       426     443     131`).
   What the source does support is that NOT ENOUGH INFO is evidence-relative. It does not show that 202 FEVER labels were wrong.
3. **Low (calibration): the base entry's "only support test" Unknown is now answerable.** Base lines 79–81 say "Nothing here establishes that the counterfactual definition
   is the only support test". S094 gives a second, coverage-based graded test (A.1: `If the evidence fully covers the overall content` → definite;
   "supplemented with additional knowledge" → indirect; "only partially covers" → partial). Base Inference lines 39–41, "defined as evidential strength … not as
   entailment", holds for PEOPLEPROFILES only. CorFEVER's "fully covers" reads closer to entailment, so the claim of a single literature definition overstates.
4. **Low (operability): the staged strings would fail quote-in-span.** The row and the amendment write `Cohen's` with a straight apostrophe (the capture has U+2019) and
   `relabelled` (the capture has `relabeled`). The row's recheck string "score for inter-annotator agreement is 0.792" has `find=-1`, because the
   line break falls after `inter-`, so a mechanical recheck on this capture always fails. It should be replaced with the char 21560 slice.
5. **Low (source-internal arithmetic, info):** Table 2's closed-domain row 333/333/333 sums to **999**, but the text says `For the closed-domain set, We extract 1,000 claims` (16191).
   The real-world row sums to 1000. The NOT ENOUGH INFO count drops by 202 while SUPPORTS+REFUTES grows by 203. An entry should quote the text's "202" and not derive it from the table.

## Residual risk and verification gaps
- Only the capture was read. Whether the PDF prints `inter-annotator` or `interannotator` cannot be settled offline; neither form is contiguous in the capture anyway.
- The column split at col 81 was applied to chars 19000–22200 only. Every delivered slice was checked independently with `find`/`count`/slice equality.
- `inference-ground.py` and `c3-count.py` were read but not run; no lane `spans.tsv` or S094 row exists yet.
- Scratch `/tmp/chousa-r47-ReviewOpenS094/` was deleted before finishing.
