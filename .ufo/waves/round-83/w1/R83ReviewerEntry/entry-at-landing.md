# Appraisal judgments — make them twice, settle disagreement by a fixed rule, and record the support and its location (round 83)

source: S009, S212, S213
verified-at: 2026-11-06 (round 83; captures `ea16817cb78993196ea1a095`, `708022d401fd771fc59bd1d9`, `963807d173af711593fd1c45`)
recheck: on-release

## What this entry governs

The lane's method ends in a judgment: a claim is supported by its source or not (`PROVINCE.md` "claim-vs-source
verification"). Held entries say what a support verdict rests on (`claim-support-states-r24.md`) and how support tests
are stated and how reliable they are (`claim-support-test-r37.md`); none says how one judgment is to be *made and
recorded* so that a reader can audit it. Cochrane's conduct standards for risk-of-bias assessment (MECIR C52–C60, queued
in this registry since round 1) and the two Handbook chapters they point to (7 and 8) state that procedure for one kind of
appraisal judgment. The rows below keep only what each quote states about making and recording a judgment; the
risk-of-bias domains themselves are not taken.

## Located quotes

| qid | source | quote |
|---|---|---|
| Q1 | S009 | "Justify judgements of risk of bias (high, low and some concerns) and provide this information in the risk-of-bias tables (as 'Support for judgement')." |
| Q2 | S009 | "Collect the source of information for each risk of bias judgement (e.g. quotation, summary of information from a trial report, correspondence with investigator etc.)." |
| Q3 | S009 | "Where judgements are based on assumptions made on the basis of information provided outside publicly available documents, this should be stated." |
| Q4 | S212 | "Risk-of-bias assessments in Cochrane reviews should be performed independently by at least two people" |
| Q5 | S212 | "Doing so can minimize errors in assessments and ensure that the judgement is not influenced by a single person's preconceptions." |
| Q6 | S212 | "Review authors should also define in advance the process for resolving disagreements." |
| Q7 | S212 | "For example, both assessors may attempt to resolve disagreements via discussion, and if that fails, call on another author to adjudicate the final judgement." |
| Q8 | S212 | "Cochrane review authors are expected to record the source of information (including the precise location within a document) that informed each risk-of-bias judgement" |
| Q9 | S212 | "A judgement of 'notable concern about conflict of interest' should be based on reflected assessment of identified conflicts of interest." |
| Q10 | S212 | "A hypothetical possibility for undeclared conflicts of interest is, as a rule of thumb, not considered sufficient reason for 'notable concern'." |
| Q11 | S213 | "Answers to signalling questions and judgements about risk of bias should be supported by written justifications." |
| Q12 | S213 | "The algorithms provide proposed judgements, but review authors should verify these and change them if they feel this is appropriate." |
| Q13 | S213 | "It is important that reasons are provided for any judgements that do not follow the algorithms." |
| Q14 | S213 | "Brief, direct quotations from the text of the study report should be used whenever possible." |
| Q15 | S213 | "If the question seeks to identify evidence of a problem, then 'No information' corresponds to no evidence of that problem." |
| Q16 | S213 | "concerns should be expressed only about issues that are likely to affect the ability to draw reliable conclusions from the study." |

## Decision table

| Situation | Do | Never | Warrant |
|---|---|---|---|
| A judgment about a source will decide what the record reports | have the judgment made independently by at least two people | record one person's judgment as though two had made it independently | Q4, Q5 (S212) |
| Two independent judgments of the same item disagree | settle them by the process fixed before assessment began, for example discussion and then a third person who adjudicates | choose how to settle a disagreement only after it has appeared | Q6, Q7 (S212) |
| A judgment is entered in the record | write the support for that judgment beside it, so the reader can see why it was made | enter a bare judgment with no written support | Q1 (S009), Q11 (S213) |
| The support for a judgment is being written | use a brief direct quotation from the source text whenever one is possible | use a paraphrase where a brief direct quotation was possible | Q14 (S213) |
| The source behind a judgment is being recorded | name the source and the precise location within the document that informed the judgment | cite a document without saying where in it the support was found | Q8 (S212), Q2 (S009) |
| A judgment rests on assumptions drawn from information outside publicly available documents | state in the record that the judgment rests on such information | present the judgment as if public documents alone supported it | Q3 (S009) |
| A rule or checklist proposes a judgment automatically | verify the proposed judgment, change it where appropriate, and give the reason for any departure | depart from the proposed judgment without recording a reason | Q12, Q13 (S213) |
| A check looks for evidence of a problem and the source gives no information about it | record the silence as no evidence of that problem | record the silence as evidence that the problem is present | Q15 (S213) |
| Deciding whether a weakness of a source deserves a recorded concern | raise a concern only when the issue is likely to affect whether reliable conclusions can be drawn | record a concern about an issue unlikely to affect the reliability of the conclusions | Q16 (S213) |
| The authors of a source may have a conflict of interest | base any notable concern on conflicts actually identified and assessed | treat a merely hypothetical undeclared conflict, as a rule of thumb, as reason enough for notable concern | Q9, Q10 (S212) |

## Inference (lane's, not stated by the sources)

For this lane a "judgment" is a claim-vs-source verdict (`supported`, `contradicted`, `not-found`) and the
"proposed judgment" of row 7 is a gate's or counter's verdict. Read that way, the rows describe practice the lane already
runs in part — a non-author closure re-judges the round's claims (two judgments), quotes are located by line in a
committed capture (rows 4–5), and a lane gate's verdict is overridden only with a stated reason (row 7). The sources state
none of this mapping; it is the lane's reading, to be tested by future rounds.

## Limits

- All three sources are written for risk-of-bias assessment in Cochrane intervention reviews. The rows keep only the
  procedure for making and recording a judgment; the RoB 2 domains, signalling questions and the overall-judgment
  algorithm are not taken.
- Row 8 covers only checks that look for evidence of a problem. The same S213 paragraph states the other case: when the
  question concerns an item expected to be reported, "the absence of information leads to concerns about there being a
  problem" — row 8 does not apply there.
- Row 1 states the Cochrane standard (at least two people). S212 also reports a study in which about one-third of
  articles "could be assessed by just one reviewer" when a machine-learning tool is used; that is a study finding, not the
  standard, and the row does not rely on it.
- Row 10's Never keeps the source's "as a rule of thumb" hedge; the source also suggests assuming no non-financial
  conflicts "unless there are clear suggestions of the opposite".
