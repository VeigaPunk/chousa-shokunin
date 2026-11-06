# R82ReviewerEntry — K3 semantic review of `corpus/knowledge/question-framing-frames-r82.md`

Seat: R82ReviewerEntry (non-author reviewer; leaf). Candidate bytes: `b4a41d251b488f06b4a6ab01a11bc12ce72edd20`
(working-tree file verified byte-identical: `diff` rc=0, `receipts/command-log.txt` [2]).
All quote locations below are `grep -n -i -F` line numbers in the committed captures
(`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures/<key>.txt`), re-derived this session, rc=0 each
(`receipts/command-log.txt` [3]). Capture sha256s match `corpus/evidence/round57/refetch.tsv` rows 152–156
(`receipts/capture-sha256.txt`, `receipts/refetch-rows.txt`). No network was used; no fetch, no re-open.

## Headline

**K3 FIRES — C2 falsified per the frozen kill rule.** One decision row's Never is not supported by its warranting
quotes read in context, and is contradicted in part by the same capture two paragraphs away.

- Row 1 (situation "The question asks what exists on a topic (a map, not a test of an effect)") — Never cell:
  "force an intervention, comparator and outcome onto a mapping question".
- Warrant: Q6, Q7 (S210, capture `bcb4a695b2aa019305121cff`, line 838).
- Q6 in context: "JBI suggests utilising the PCC (population, concept and context) approach to formulate review
  questions for scoping reviews." — a suggestion, not a prohibition (`receipts/excerpts-S210-bcb4a695.txt` line 838).
- Q7 in context: "A scoping review question is broader than those in systematic reviews and can be seen as
  hypothesis-generating, whereas a systematic review is hypothesis-testing" — descriptive, not prohibitive (same line).
- Same capture, line 840 (the Q8 quote that row 2 itself warrants on): "there may be a compelling argument to use a
  different question format (such as PICO or Population, Exposure, Comparator, Outcome [PECO]), such as when
  performing a structured analysis of existing research or research gaps, or as a precursor to a systematic review."
  The row's situation ("a map, not a test of an effect") covers structured gap analyses and SR-precursor maps, so the
  source read in context affirmatively endorses the very framing the Never forbids for a subset of the row's situation.
- Escape readings fail: reading "force" as "impose without justification" still leaves the cell unsupported — Q6/Q7 say
  nothing about justification or forcing, and the suggestion-to-prohibition step is the reviewer check K3 exists to catch
  (claims.md: "whether a row follows from its quote is K3's reviewer check, declared here before data").
- Do cell of row 1 is supported (see table). One row suffices under K3; the other eight rows are judged below so the
  repair scope is visible. Per the frozen rule: "A repair after scoring does not rescue the claim."

## Row-by-row judgment (Do and Never separately; passages ≤25 words, located by capture:line)

| # | Situation (abbrev.) | Cell | Judgment | Located passage (capture:line) |
|---|---|---|---|---|
| 1 | map, not test of effect | Do | supported | bcb4a695:838 "JBI suggests utilising the PCC (population, concept and context) approach to formulate review questions for scoping reviews." ("can be seen as hypothesis-generating", same line, is mildly stronger in the Do's "say it is") |
| 1 | | **Never** | **not supported — K3 FIRES** | bcb4a695:840 "there may be a compelling argument to use a different question format (such as PICO or Population, Exposure, Comparator, Outcome [PECO])" — same source endorses I/C/O frames for mapping questions; Q6/Q7 prohibit nothing |
| 2 | map feeds SR / gap analysis | Do | supported | bcb4a695:840 "compelling argument to use a different question format … as a precursor to a systematic review" (the "record why" clause is the lane's proceduralization of "argument") |
| 2 | | Never | supported | bcb4a695:840 "For some scoping reviews, it may be that one of the elements of the PCC is not required, depending on the question and objective" |
| 3 | criteria being written | Do | supported | 97223722:736 "each element of the PCC approach is broken down into a further description of what the review will include and exclude" ("chosen frame" generalizes PCC — declared transfer) |
| 3 | | Never | supported (borderline) | 97223722:736 "Having a clear alignment between the objective and review question creates clarity when developing the eligibility criteria" — derivation direction implies frame-produced criteria; exclusivity is implied, not stated (residual R3) |
| 4 | frame fixed before searching | Do | supported | fd7eed5e:560 "The review PICO (planned at the protocol stage) is the PICO on which eligibility of studies is based"; fd7eed5e:561 (synthesis PICO defines each synthesis's question) |
| 4 | | Never | supported | fd7eed5e:553 "Throughout the Handbook we make a distinction between three different stages in the review at which the PICO construct might be used" |
| 5 | findings written up | Do | supported | fd7eed5e:562 "The PICO of the included studies (determined at the review stage) is what was actually investigated in the included studies" (reporting step is the declared lane transfer, `## Inference`) |
| 5 | | Never | supported | fd7eed5e:562+560 — actual is "determined at the review stage", distinct from the protocol-stage eligibility PICO; presenting planned as actual conflates constructs the source distinguishes |
| 6 | some elements matter more | Do | supported | fd7eed5e:558 "Equal emphasis in addressing, and equal precision in defining, each PICO component is not necessary." plus the uneven-precision breast-cancer example, same line |
| 6 | | Never | supported | fd7eed5e:558 same sentence; "not necessary" compressed to a Never against padding — noted as mild strengthening, not a contradiction |
| 7 | no relevant source read yet | Do | supported | fd7eed5e:690 "It is generally not possible to formulate an answerable question for a review without knowing some of the studies relevant to the question" |
| 7 | | Never | supported (hedge-loss) | fd7eed5e:690 same passage; "generally" dropped in the Never; reconciled by "final" vs the same paragraph's "questions should be posed in the protocol before initiating the full review" (residual R2) |
| 8 | question cannot be stated clearly | Do | supported | bcb4a695:837 "then informs the foundation for the eligibility criteria, search strategy, screening, extraction, analysis, presentation and findings of the review" — ordering warranted; "rewrite until it can be" is the implied remedy |
| 8 | | Never | supported | bcb4a695:837 "If a review question is unclear, the review will lack coherence." |
| 9 | frame/criteria change after protocol | Do | supported | 21323730:766 "deviations from the protocol with supporting justification should be made transparent within the final scoping review" |
| 9 | | Never | supported | 21323730:766 — "made transparent" entails not presenting a deviation as planned; adjacent sentence: changes "be avoided, sometimes this is not possible … due to its iterative nature" |

Every quoted cell was also verified verbatim: all 11 located quotes match their captures byte-for-byte at the cited lines
(rc=0; `receipts/command-log.txt` [3]); the truncated display of long lines 558 and 766 was read `:raw` and confirmed.

## Inference / Limits sections

- `## Inference (lane's, not stated by the sources)` — the heading itself marks it as the lane's own, and the body closes
  "Neither source states this mapping." Honest and correctly fenced. No finding.
- `## Limits` — discloses health-synthesis provenance (Cochrane intervention reviews; JBI scoping reviews), claims only
  structural rules were taken, and correctly discloses the S209 title/slug drift: capture line 189 shows page title
  "10.2.2 Developing your protocol" while the refetch URL slug reads "10.2.2+Developing+the+title+and+question"
  (`receipts/refetch-rows.txt` row 153). Verified accurate. No finding.

## Registry rows (`corpus/SOURCES.md`; `receipts/sources-rows.txt`)

- S008 (line 18): tier A, scope/anchor/teaches consistent with the capture (2.3 three-PICO passage at fd7eed5e:553–562;
  "Key Points" present at line 531). Residual R4: the anchor names only "sections 2.1 Key Points and 2.3", but Q5 — a
  counted quote of the new entry — sits in section **2.5.2 Changing review questions** (heading fd7eed5e:499, quote :690),
  which the anchor does not name.
- S209 (line 221): tier A; anchor "the protocol paragraph on deviations" = capture line 766; teaches matches ("a priori
  protocol", deviations transparent with justification). Consistent.
- S210 (line 222): tier A; anchor/teaches match capture lines 837–840. Residual R5: teaches "scoping questions **use**
  population, concept and context" upgrades the source's "JBI **suggests** utilising the PCC" — same hedge-loss family as
  row 1; and it omits the structured-gap-analysis case from the PICO/PECO clause. Incomplete, not false.
- S211 (line 223): tier A; anchor "opening paragraphs and the Population/Concept/Context headings" matches (quote at
  :736); teaches generalizes "each element of the **PCC approach**" to "the question frame" — mild generalization,
  consistent with the entry's declared transfer. Acceptable.
- S028 (line 38): tier A; anchor "introductory text before Benefits of Crossmark and the How Crossmark works paragraph"
  = dedff231:158–190; teaches "status is published metadata a reader can check, a recheck trigger" — supported by
  dedff231:159 and :183. Consistent.

## Crossmark addendum (`corpus/knowledge/correction-retraction-status-r81.md`, round-82 addendum)

- Both S028 quotes verified verbatim: dedff231:164 ("Crossmark lets readers know when a substantial change affecting the
  citation or interpretation has occurred…") and :183 ("Members place the Crossmark button close to the title of an item
  on their web pages and in PDFs."). rc=0.
- Reading cell ("the publisher has committed to report updates for that record") — supported by :183 "They commit to
  informing us if there is an update such as a correction or retraction".
- Honesty of the "never" clause: the addendum states "The 'never' clause is the lane's reading of S028's 'Members place
  the Crossmark button…': the signal exists only where a member placed it; S028 does not itself state what an absent
  button means." That is an explicit inference disclosure, and the capture supports the reading (Crossmark is opt-in per
  member; :185 even notes "the presence of Crossmark itself is not a guarantee"). Honest. No finding.

## Health-synthesis transfer check

The entry claims structural-only transfer, and eight of nine rows honor it. The single transfer beyond source support is
row 1's Never (the K3 firing above): a health-synthesis default (PCC suggested for scoping reviews) is hardened into a
prohibition that the same source explicitly relaxes for part of the row's own situation. No risk-of-bias, meta-analysis,
or equity-framework content was imported (PROGRESS-Plus appears in S211's capture but is correctly excluded by Limits).

## Residuals (not kills)

- R1 (subsumed by the firing): rows 1 and 2 give opposite I/C/O guidance for overlapping situations (a map feeding an SR
  satisfies both), with no precedence rule; a reader must reconcile "never force I/C/O" with "consider PICO/PECO".
- R2: row 7's Never drops Q5's "generally" hedge.
- R3: row 3's Never asserts exclusivity (no criterion outside frame elements) that Q10 implies but does not state —
  e.g., date or language limits are criteria no PICO/PCC element "produces" in the quote's sense.
- R4: S008 registry anchor omits section 2.5.2, where counted quote Q5 lives.
- R5: S210 registry teaches strengthens "JBI suggests" to "use", and omits the gap-analysis case.
- Informational: S008's registry row keeps `mined 2026-10-19` with an anchor updated to the 2026-11-06 serving; the
  re-open date is carried by refetch.tsv row 152 (19:42:03Z), consistent with claims.md's re-open of S008.

## Verification gap

None material: every counted quote was located verbatim in a capture whose sha256 matches the committed refetch row, and
every row cell was judged against at least the warranting paragraph. K4 (ground already held) was not in this seat's
scope and was not run.

## Commands and receipts

Extraction: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive b4a41d251b488f06b4a6ab01a11bc12ce72edd20 | tar -x -C /fast/scratch/hyaku/chousa-r82/R82ReviewerEntry/candidate` (rc 0, EXTRACT_OK).
Quote location: `grep -n -i -F '<quote>' corpus/captures/<key>.txt` per quote (rc 0 each; log [3]).
Identity: `diff` working-tree entry vs candidate revision (rc 0). Receipts in `receipts/` beside this file.

VERDICT: R82ReviewerEntry C2 fired — row 1's Never ("force an intervention, comparator and outcome onto a mapping question") is not supported by Q6/Q7 (bcb4a695:838, a suggestion plus a description) and is contradicted in part by the same capture's line 840, which endorses PICO/PECO exactly for mapping questions feeding structured gap analyses or systematic reviews.
VERDICT: R82ReviewerEntry C1 n/a — C1 was not this seat's assignment and no C1 check was run.
