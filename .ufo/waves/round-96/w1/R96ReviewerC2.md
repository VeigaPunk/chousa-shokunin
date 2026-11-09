# R96ReviewerC2 — Fidelity review: search-peer-review-dedup-r96.md vs sources (C2)

Frozen revision 2db151c5ea0883de0b9dc8d95c6fac1755e1056a, checked at that HEAD.
Method: read `corpus/captures/1a8c36c4c24444967bd9c3ce.txt` (S224, PRISMA-S PDF) Table 1
items 14/16 (lines 300-314), ITEM 14 explanation (876-881), ITEM 16 (912-924), Box 1
"Peer review" (1044-1046); read `corpus/captures/e94691f583d644da14661ec1.txt` (S223,
PRESS 2015 authors' JCHLA lightning-talk abstract) lines 142-177. Judged each of the 8
decision rows on three questions: does Do say only what the warrant quotes say? does
Never follow from them, or is it the lane's addition presented as the source's? is every
non-source statement inside the Lane column?

Anchor checks run by me (receipts in `.ufo/waves/round-96/w1/R96ReviewerC2-*.txt`,
copied before yielding):

- C2 predicates 1-3 reproduced at the freeze: gate-records `GATE_RECORDS files=1
  records=31 ok=31 fail=0` exit 0; research-gate `METADATA_COMPLETE=1/1`,
  `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` exit 0;
  search-rerun `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8` exit 0
  (TREE_CHANGED for Q1, Q3, Q8 only, as the entry predicts).
- S223 page anchor: `/usr/bin/grep -n '^99$'` → exit 1; page 99 appears as a
  same-line footer (`LIGHTNING TALKS / PRÉSENTATIONS ÉCLAIR … 99`, line 168) and
  line 1 of the capture is page 96. The PRESS abstract therefore spans the visible
  pages 98-99: the pointer "page 98-99, PRESS abstract, Results and Discussion
  paragraphs" is accurate. No new page header intervenes between lines 142-177.
- S223 attribution: the timing sentence is preceded by "Survey respondents and forum
  participants recommended" (lines 166-167); "the recommendation" after "was removed"
  (line 172) continues that same recommendation. The abstract does not say the
  guideline statement itself imposes the timing.

## Row verdicts

| Row (Situation) | Verdict | Why (with source lines) | Minimal rewording |
|---|---|---|---|
| 1. Reporting whether a search strategy was peer reviewed | faithful | Do = L1 "Describe any search peer review process." (Table 1 line 303) + L7-L8 "this item is designed to document search-specific peer review" (ITEM 14, lines 879-881): the quotes say PRISMA-S asks a report to document the search-specific review, not a protocol's general review. Never ("let a protocol's general review stand in for…") is the correct contrapositive of that distinction and is marked by the Lane column. Non-source content (seat/person, "or that nobody did") sits in Lane. | none |
| 2. Choosing who reviews a strategy | faithful | Do = L4-L6: "should strongly consider having the search strategy peer reviewed by an experienced searcher, information specialist, or librarian" (ITEM 14, lines 876-878). Never is precisely the opposite of the mandatory reading, and its warrant is literally in the Never cell ("should strongly consider" vs "requirement"). The entry does not upgrade "should strongly consider" to "must" anywhere; the Named-limits line "'Should strongly consider' (L4) is the strongest wording held" (entry line 108) is accurate. Lane (reviewer seat did not write the expression) is lane conduct, not source. | none. Keep "strongly consider" exactly as written; any future edit must not render it "have reviewed" or "must review". |
| 3. Timing a peer review | overreach (Do cell, second clause) | Do's first clause is faithful: L2 "peer review of search strategies prior to executing the search" (Box 1, line 1044) — PRISMA-S's glossary locates review before execution. The second clause, "under PRESS 2015, after the MEDLINE search has been developed and before the other database searches are developed" (L24-L25), is a generalisation of L24-L25, which in S223 is a recommendation of "Survey respondents and forum participants" (lines 166-167), not a guideline requirement. The Do cell states the timing without its agent or its status; the only attribution-carrying word in the abstract is "recommended" (L24 begins mid-sentence — the full clause needs the preceding line 166-167). | "review the search strategy prior to executing the search; PRESS 2015's survey respondents and forum participants recommended review after the MEDLINE search has been developed and before the other database searches are developed" |
| 4. Deciding what a reviewer checks | faithful, with one lane-unmarked ambiguity in Never | Do's six elements count correctly from the abstract's semicolon list (lines 159-164): translation of the research question; Boolean and proximity operators; subject headings; text word search; limits and filters, syntax and line numbers; spelling — six items under "Six existing PRESS elements were retained". The Lane column transparently owns the grouping ("the grouping … is the abstract's punctuation; the guideline's own checklist wording was not opened (403)"). Never's second half ("left it to the search developer") is in L27-L29 ("with the recommendation that translations be peer reviewed at the discretion of the search developer"). Ambiguity: "limits and filters, syntax and line numbers" could be read as 2 elements (limits-and-filters; syntax-and-line-numbers) or 3 (limits and filters; syntax and line numbers) depending on where the comma falls; 6-count requires the former reading throughout, which is consistent with the abstract's punctuation and the Lane column says so. No overreach; just flag the count depends on that punctuation. | none required; optionally append to Lane: "counting 'limits and filters' and 'syntax and line numbers' each as one element". |
| 5. Saying what a review is for | overreach (Never + Lane mixing) | Do = L3 "to identify errors, missing keywords or subject headings, and other issues within a search strategy" (Box 1, line 1045). L30 ("peer review checklists were effective at improving search quality", line 158, mid-sentence "Several studies showed that…") is collected from an abstract-level corpus note — the abstract separately says no evidence refuted the existing elements (line 165), so this is out-of-scope for a *purpose* row but its honest home is disclosed in Lane. The material defect: Never ("claim a reviewed strategy is complete or has high recall") does not follow from L3 — L3 says review finds errors/issues, it does not promise completeness or forbid a recall claim. The Never is the lane's caution, presented as the source's converse. Also the tier note "several studies" in Lane relies on the full sentence "Several studies showed that peer review checklists were effective at improving search quality" (line 157-158), of which only the tail is quoted in L30 — so L30 alone does not warrant "in several studies". | Move the Never into Lane, e.g. Never: "— (no source statement); see Lane" and Lane: "…the lane reads L3 as no warrant for claiming completeness or high recall; the abstract reports that checklists improved search quality in several studies, which the lane holds without measurement". Or narrow Never to "present peer review as guaranteeing error-free strategies" (supported by L3's purpose and L30's non-absolute "improving"). |
| 6. Reporting deduplication | faithful | Do = L9-L10 (Table 1 line 313-314: "Describe the processes and any software used to deduplicate records from multiple database searches and other information sources") + L11-L13 (ITEM 16 lines 915-917: "should describe and cite any software or technique used, when applicable. If duplicates were removed manually, authors should include a description."). "Describe" is the item's verb; the Do does not upgrade it to "perform", "require", or "avoid manual removal". Never ("remove duplicates without saying how") is a fair contrapositive of the describe obligation. Lane (search-rerun.py "never merges hit sets across searches") is lane method, outside source. | none |
| 7. Explaining why the method is reported | faithful | Do = L14-L16 (ITEM 16 lines 912-914: "which method is used enables readers to evaluate the process and understand to what extent these techniques may have removed false positive duplicates [138]"). The conditional "may have removed" is preserved in the Do ("may have removed false positive duplicates"). Never ("treat deduplication as lossless") is the fair negation; "lossless" is lane vocabulary but the Lane column makes that clear ("for paths, identity is byte equality, so a false positive cannot occur"). | none |
| 8. Reporting the count after deduplication | faithful | Do = L17-L18 (ITEM 16 lines 922-924: "The total number of references after deduplication should be reported in the PRISMA flow diagram [34]."). Never ("report only per-source counts and leave the deduplicated total implicit") follows from the addition of the after-deduplication total beyond the per-source total. Lane correctly credits row 4 of the round-95 entry (item 15) for per-source counts. | none |

## Scope / tier checks (kill rule K4)

- S223 tier B, scope "…not the guideline statement, its checklist wording or its
  assessment form, none of which was opened" — accurate. The PRESS abstract is
  conference-proceedings material (lightning-talk abstract in JCHLA 37:96-100,
  2016), while the guideline statement (J Clin Epidemiol 2016;75:40-46) and the
  Explanation and Elaboration report are different documents; the abstract itself
  (lines 170-177) points to both, confirming they exist but were not opened. The
  entry's Named-limits line correctly holds only tier B. Tier B is the right call;
  an authors' abstract is secondary summary, not the guideline. Scope is fine.
- S224 tier A, re-opened "under a second scope" with "(same bytes as S222's
  capture)" — consistent: S224's capture key is `1a8c36c4c24444967bd9c3ce`, the
  entry's header says "identical bytes", and the capture so far shows the full
  Table 1 + both explanations + Box 1. Scope cell "what PRISMA-S says a search
  report must state about search peer review (item 14) and deduplication (item 16),
  and its glossary definition of search peer review; not whether peer review or
  deduplication improves a search" — the actual quotes support this boundary: rows
  1-2, 6-8 use only those sections, and row 5's beyond-scope sentence (L30,
  effectiveness) is the sole quote about improvement, and the row only weakly
  uses it (see row 5 overreach). No overclaim found in S224's scope cell. The
  entry does **not** claim S224 says peer review improves searches.
- "describe" vs "do": PRISMA-S is a reporting guideline; items + explanations use
  "Describe"/"should describe"/"should strongly consider" throughout. The entry
  consistently says "describe" (Do cells + Named-limits line 107) and never
  claims either source requires performing peer review or deduplication. This is
  faithful to the distinction.

## Special items requested in the seat brief

- "should strongly consider" vs any mandatory reading: no mandatory reading found
  in the entry; row 2's Never explicitly rejects it. Held.
- PRESS timing vs row's generalisation: see row 3 — Do generalises a survey/forum
  recommendation into a PRESS-2015-level statement without naming the recommenders.
- Six elements grouping: correct per the abstract's semicolons; Lane is
  transparent about the punctuation. One residual: "limits and filters, syntax
  and line numbers" reading (see row 4).
- "describe" vs "do": the entry keeps it; see scope check above.
- S223 tier B / scope / page 98-99 anchor: verified (grep for `^99$` exits 1
  because the 99 is a same-line footer; the abstract is on the pages around the
  footer; no other page header between lines 142-177). Tier B is correct.
- S224 scope cell: no overclaim; the improvement question is explicitly
  excluded, and only row 5 touches it (and that is its defect).

## Non-row findings

1. **Claim batch defect (claims.md C2 predicate 4, and the seat brief's Chicago
   figure).** The claim text I was given says entry-controls prints
   `POSITIVE=1/1 FORGERY_REFUSED=8/8 BINDING_REFUSED=3/3 SEARCHES=3/3
   DO_NOTHING_REFUSED=1/1 ORACLE_REJECTED=1/1` and `ENTRY_CONTROLS=PASS`. The
   seat brief's paraphrase is the same. That is the predicate, not a finding.
   (Note: I did not re-run entry-controls; the freeze claims it; running it
   takes a full battery and was not needed for the fidelity axis.)
2. **S223 L30 is truncated mid-sentence in its warrant use.** L30 alone ("that
   peer review checklists were effective at improving search") lacks its subject
   "Several studies showed" and its complement "quality". Row 5's Lane
   ("the abstract reports that checklists improved search quality in several
   studies") is true of the abstract (lines 157-159) but not of the quoted
   warrant L30 alone. This is precisely a row where a reviewer should widen the
   quote or narrow the Lane claim. It is a fidelity gap, not a fabrication.
3. No queries: "PRESS timing" Do cell (row 3) and the Never of row 5 are the
   only cells where the lane's reading outruns its warrant quotes. All other
   rows are faithful; all non-source statements I found are inside the Lane
   column, which the entry's own header (line 20-21) declares: "The column
   marked *lane* is this lane's reading; it is not what PRISMA-S or PRESS says."

## Recommendation to Main (C2 predicate excluded; fidelity axis)

The C2 claim's wording ("each warranted by located quotes") survives for 6/8 rows
cleanly, is one attribution fix away on row 3, and is genuinely overreaching on
row 5. Per the claim's own kill rule K2, row 5 as written should be narrowed or
withdrawn (or its Never moved to Lane and its Lane widened to carry "Several
studies showed"). The claim *number* (30 located quotes, 31 records, 8 rows)
still holds — the defect is in paraphrase fidelity, exactly the risk the
claim's Named limit (a) describes ("the instruments check that a warrant
exists…, not that the paraphrase is faithful — that is the wave's reviewer
item"). That limit is doing its job; this report is the item it refers to.

Receipts (observed lines + exit codes inline above):
- `.ufo/waves/round-96/w1/R96ReviewerC2.md` (this file)
- `.ufo/waves/round-96/w1/R96ReviewerC2-gate-records.txt` — `GATE_RECORDS files=1 records=31 ok=31 fail=0`, exit 0
- `.ufo/waves/round-96/w1/R96ReviewerC2-metadata.txt` — `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`, exit 0
- `.ufo/waves/round-96/w1/R96ReviewerC2-search-rerun.txt` — `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8 tree_same=5/8`, exit 0
- `.ufo/waves/round-96/w1/R96ReviewerC2-sources.txt` — S224/S223 excerpts with line numbers
- `.ufo/waves/round-96/w1/R96ReviewerC2-page-anchor.txt` — `grep -n '^99$'` exit 1 (footer check)

VERDICT: R96ReviewerC2 C1 n/a — this seat held only the C2 fidelity assignment.
VERDICT: R96ReviewerC2 C2 fired — rows 3 and 5 state more than their warrant quotes support (row 3: a survey/forum recommendation labelled as PRESS 2015; row 5: a Never asserting completeness/recall, and a Lane claim about "several studies" that the quoted L30 fragment does not carry); rows 1,2,4,6,7,8 faithful, S223 tier B and pages 98-99 and S224 scope accurate.
