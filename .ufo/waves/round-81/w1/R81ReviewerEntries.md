# R81ReviewerEntries — scoped findings (C1 K3)

Full per-row review with located passages: `.ufo/waves/round-81/w1/R81ReviewerEntries/review.md`.
Receipts: `.ufo/waves/round-81/w1/R81ReviewerEntries/receipt-k3-quote-check.txt`,
`.ufo/waves/round-81/w1/R81ReviewerEntries/receipt-k3-anchors.txt`.
Subject: candidate landing `7e2da96a0541946e796384d42fea18e09ede9e9f`; both r81 entries; rows S203–S208.

## Firing (K3)

1. **Correction entry, row "A newer article version exists" (cites S206) — FIRES.** The row's Do is "cite the version
   read, with its date". S206 capture `f221c90f69188f775e32cd34.txt` line 222 says, verbatim, "The citation should be to
   the most recent version." Command: `sed -n '218,222p'` on that capture plus `grep -n 'most recent version'`, rc=0,
   observed `222: The citation should be to the most recent version.` The entry's two located S206 quotes (lines 218,
   220) do not themselves contradict the row; the contradiction is in the same cited passage. Under the seat spec
   ("cited source contradicts") this fires; under the letter of K3 ("located quote") it does not. Ruling needed from main.

## Defects that do not fire (routed)

2. Citation entry, Terms: "A second, independent guide uses the same split." The S204 passage ends "(Hirt et al., 2024)"
   (c52a1f15 line 1428; `grep -c` = 2). Not independent.
3. Citation entry, row T3 cites S204 §4.2.2 for "never trust one index"; §4.2.2 (c52a1f15 lines 1424–1434) says nothing
   about combining indexes. Warrant mismatch; rec 6 supports the Do.
4. Citation entry, row T7: "rec 5 was corrected" appears as a fact in a Do cell. No committed capture or receipt holds
   the web snippet it rests on (`grep -rln 'small error' corpus/`: only the entry itself, rc=0). Rejected S208 used as
   warrant.
5. Citation entry, row T1 and T5 strengthen S203 recs 2 and 8 ("should be seriously considered" / "should be
   considered") into "run". T1's Never cell has no basis in rec 2.
6. Correction entry, quote C2: "the erratum notice is simply linked to the citation for the corrected article" drops
   the antecedent condition (`371c5511` line 323: "If the erratum involves correction of a portion … not included in
   the NLM citation…"). Verbatim, but the scope is narrowed by omission. SOURCES S205 teaches cell repeats it.
7. SOURCES S206 teaches cell omits "The citation should be to the most recent version." (line 222) — the rule that
   the C3 row contradicts.
8. SOURCES S204 tier A is doubtful for a secondary methods guide; no explicit tier rubric was located in SOURCES.md to
   check it against. Soft.
9. Correction entry row C5 (unreachable → unresolved) has no warrant cell; not contradicted.

## Checked and clean

- 13/13 blockquote quotes located verbatim (whitespace-collapsed) in their captures; word counts 8–25; S207 at exactly 25.
- All recommendation numbers in the citation entry's decision table match the final recommendations section of S203
  (headings at capture lines 262–463). No Delphi-draft numbering used.
- S203 captured as "Version: Accepted Version" (line 11); the entry's accepted-manuscript caveat is accurate.
- Retraction Watch "not as comprehensive as retractions" (S207, line 393) is quoted accurately and read correctly.
- Capture sha256 for S203, S204, S205, S207 match their 2026-11-06 refetch.tsv success rows.

## Tools

None installed. Scratch `/fast/scratch/hyaku/chousa-r81/R81ReviewerEntries` deleted before yield.

VERDICT: R81ReviewerEntries C1 fired — K3 fires on the correction entry's "newer article version" row (cites S206): it says cite the version read, and S206 line 222 says the citation should be to the most recent version.
