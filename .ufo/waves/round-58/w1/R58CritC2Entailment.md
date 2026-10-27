# R58CritC2Entailment — adversarial C2 entailment review

## Scope and evidence

Reviewed the Scribe draft in `.ufo/waves/round-58/w1/R58ScribeEntryDraft.md` (proposed entry, lines 17–48) against the frozen 12 rows in `corpus/evidence/round58/c2/quotes.tsv` and the committed S101 capture only. Re-read frozen `claims.md` and `c2-count.py`; did not change either or make a live fetch. Draft file is a proposal in another seat's report; no lane entry exists at review time.

Command run in `/fast/scratch/hyaku/chousa-r58/R58CritC2Entailment`:

```sh
sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > form.txt
sha256sum form.txt
```

Observed: capture-text pin `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`; raw pin `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`; form `47356` bytes, sha256 `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`, matching Scribe report.

## Counterexamples and precise narrowing

1. **Draft observation bullet “Carrier marking is required on citation, not optional” (draft line 35) materially broadens the rule.** Quote 4 is only the predicate clause, not its subject. The same source sentence at chars 668–796 begins `对于非纸张型载体的电子文献` (“for electronic documents on non-paper carriers”); it then says when cited as references, mark the carrier type too. Its next sentence recommends two-letter carrier marks. Narrow to: **“For electronic documents on non-paper carriers, S101 says that when cited as references their carrier type must also be marked in the reference-type identifier.”** Avoid “not optional” without this limitation. The specification immediately says traditional paper-carrier literature need not state the carrier type (char 1090 onward), reinforcing the counterexample.

2. **“Two carrier pairs are printed” (line 36) falsely sounds exhaustive and conflicts with the source itself.** Frozen quotes 5–6 supply MT and OL, but the full source sentence at chars 668–796 prints four pairs: MT, DK, CD, OL. Narrow to: **“Two of the carrier pairs in the source sentence are captured in the frozen quotes: MT and OL.”** Or call them “the two quoted pairs,” not the two printed pairs.

3. **“Three bracketed composites are printed” (line 37) is likewise an incorrect count/exhaustiveness claim.** The source's 1.2.4 examples at chars 838 onward print six: `[M/CD]`, `[DB/MT]`, `[CP/DK]`, `[J/OL]`, `[DB/OL]`, `[EB/OL]`. The frozen set quotes only `[M/CD]`, `[J/OL]`, `[DB/OL]`. Narrow to: **“Three bracketed composites are included in the frozen quotes: …”** This also avoids implying the quotes contain the complete example list.

4. **“The second rule” (line 34) is ambiguous as a count.** The cited two-letter recommendation is specifically subsection 1.2.3, but it is not the source's second rule: subsection 1.2.2 first recommends single-letter Z for other unspecified types. The 1.2.3 sentence names electronic reference classes (database, computer program, electronic bulletin board) before the quoted recommendation. Narrow to: **“Subsection 1.2.3 recommends the following two-letter marks for the named electronic reference classes; the frozen fragment quotes the recommendation, not the class list.”** Also avoid “a two-letter alternative” in line 26: it is recommended for those named electronic classes, not established as an alternative applicable to all types.

5. **Line 33's “makes the document-type mark a single letter under GB3469” should retain the stated scope.** The quote says “the following various reference types,” whose membership table is not in the frozen quote set. Narrow to: **“The quoted 1.2.1 text says that the reference types it lists are identified by single letters under GB3469.”** Do not make the quoted fragment alone stand for every document/reference type.

6. **Line 39 overstates “the document code is a field apart from the bracketed type/carrier mark.”** The frozen quote is only `与文献标志码(Document code)`; the source context (char 11704) is heading 11 `中图分类号(CLC number)与文献标志码(Document code)`. It supports that the phrase “文献标志码” is glossed “Document code” in a distinct section-11 heading, not a claim that it is a separately defined data field or that the two marks are formally independent. Narrow to: **“A later, separate section-11 heading includes ‘文献标志码(Document code)’; the frozen fragment does not define that field or establish its relation to the 1.2 notation.”** “Second conjunct phrase” is safer than “second conjunct” if describing the fragment.

7. **Source status in line 17/48 needs modest, explicit attribution.** Registry S101 row calls this a “copy hosted by 哈尔滨工业大学”; the draft correctly disclaims an issuing-body copy at line 48. Keep that caveat, and describe it as **“the lane-held capture of a university-hosted copy”**, not as a verified official or current standard. Its `verified-at` must remain a capture-read date; no live-fetch/current-status inference is supported. The frozen claims explicitly limit C2 to located text, not present-day standards validity or truth.

8. **Line 38 generalizes a template fragment.** Quote 11 is only the trailing publication-element sequence. Its local source context is subsection 1.3 and a preceding list of particular reference-entry categories; quote 11 alone does not establish a universal form “for reference entries.” Narrow to: **“The quoted fragment gives a publication-element sequence (place, publisher, year, pages; omit pages when citing the whole item); the frozen fragment does not include its template/category heading.”**

9. **Source-status/title phrasing in line 17 is not wholly established by the 12 quotes.** The quote set contains no title or hosting statement. These can be reported as capture/registry metadata, but not as facts entailed by quote fragments. Mark the title and host as **registry/capture metadata** (registry S101 says “copy hosted by…”), and keep the explicit distinction from issuing-body provenance. Do not describe these metadata as one of the 12 quote-supported observations.

## Checks / limits

- The full defined form confirms all frozen strings occur at Scribe-reported occurrence offsets. Among the three quoted bracketed examples, only `[DB/OL]` at char 993 begins at a line start; `[J/OL]` at 965 is preceded by indentation and `[M/CD]` at 838 also is not line-start-bound. This does not itself invalidate the draft, but line 17's `spans.tsv` receipt citation should not be represented as proving those occurrence offsets: the pinned builder's offset is context-span start, as the Scribe's own probe found.
- The form also confirms the `[M/CD]` / `[J/OL]` / `[DB/OL]` decompositions when combined with the quoted type/carrier notation and labels. State these as readings of the examples in context, not as an exhaustive alphabet or a comprehensive rule for all codes.
- I did not run C2 counter or any C1 battery; no counter output is claimed here. Scratch form was created only under the authorized scratch root.

VERDICT: The draft's broad carrier-requirement sentence and the exhaustive “two carrier pairs” / “three composites” counts are falsified by the committed capture; several other phrasings need the precise scope limits above. Narrowing them as specified preserves the 12-quote evidence without upgrading the university-hosted capture into source authority or treating the fragments as comprehensive.