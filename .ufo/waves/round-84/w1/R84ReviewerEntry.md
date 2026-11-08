# R84ReviewerEntry — C2 kill rule K3 (warrant), round 84

Seat spec: fire-or-hold K3 on `corpus/knowledge/search-transparency-reporting-r84.md` at
`03bbb4580b39b442be69f998fae2db48d64b8c93`. Frozen rule (`corpus/evidence/round84/claims.md:106-109`):
K3 fires if for any decision-table row (a) its Do or Never states something its cited quotes do not state
or entail, or (b) a sentence of the same cited source (located in capture, cited by line) contradicts the
row's Do or Never. One firing row falsifies C2.

## Method (commands, receipts)

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 03bbb458... | tar -x -C tree` (scratch
  `/fast/scratch/hyaku/chousa-r84/R84ReviewerEntry/tree`); entry bytes diff-identical to lane; captures
  identical.
- `python3 k3.py` (receipt `R84ReviewerEntry/k3-scratch.log`, sha256 `93601cb7…b9`): whitespace-collapsed
  containment of Q1–Q12 — all `located=True (12/12)`.
- Line numbers below are flat-concatenation indices verified against per-line grep over the three committed
  captures. Spot reads: S214 in full (checklist, 91 lines); S018 abstract line 76 in full + its repeats
  at 120/198/233; S023 context windows around 10318, 3256, 8786, 11517, 3246.

Note on S023 Q10: the entry cites Q10 for row 9 (modified), but Q10 occurs under eight different date
terms in the capture (available 3256, created 4164, dateAccepted 4720, dateCopyrighted 4902,
dateSubmitted 5084, issued 7698, modified 8796, valid 11527). Q10 alone does not fix *which* date — only
the neighboring Definition (`modified` 8786: "Date on which the resource was changed.") does. See row 9.

Rows below use table order 1–11. For each: (a) Do, (b) Never, (c) contradiction search in the full
paragraph/section around the quote.

## Rows 1–5: PRISMA 2020 (S214 `a640b15…`)

**Row 1 — "name every database, register, website, organisation, reference list, and other source
consulted" / Never: "report only the sources that returned results and omit those that returned none."**
Q1 = "Specify all databases … and other sources searched or consulted to identify studies." (L17).
(a) Textual paraphrase; Do = Q1 verbatim minus its tail. Held.
(b) Q1 lists source classes searched *or consulted*, with no results filter; omitting zero-result sources
would violate "all … consulted". Held.
(c) Full Information Sources item (L17-18) contains no hedge or omission allowance. Scanned entire
checklist: no sentence contradicts "name every … consulted". No contradiction found. **Row 1: held.**

**Row 2 — "state the date each source was last searched or consulted" / Never: "report the search without
dating it…".**
Q2 = "date when each source was last searched or consulted." (L18, second sentence of item 6).
(a) Do is a direct restatement; Q2 is embedded in the mandatory "Specify …" item 6. Held.
(b) Negation of the date-specification half of item 6; nothing in the item licenses undated reporting.
Held. (c) Remainder of item 6 (L17-18) and adjacent items 5/7: no contradicting sentence. **Held.**

**Row 3 — "present the full search strategy for each source, including filters and limits" / Never:
"summarize the strategy in prose when the full strategy can be stated."**
Q3 = "Present the full search strategies for all databases, registers and websites, including any filters
and limits used." (L19).
(a) Do = Q3 verbatim ("for each source" = "all databases, registers and websites"). Held.
(b) "summarize in prose when the full strategy can be stated" is the direct negation of "present the
full … strategies"; there is no "may summarize" hedge anywhere in item 7. Held.
(c) Item 7 is one line; items 6/8 give no contradicting instruction. **Held.**

**Row 4 — "state the methods used to decide whether a study met the inclusion criteria" / Never: "report
the selected studies without the selection method."**
Q4 = "Specify the methods used to decide whether a study met the inclusion criteria of the review"
(L20). (a) Do is Q4 verbatim minus tail. The row is *narrower* than the full item 8 (which also requires
reviewer counts, independence, automation) — per seat spec a narrower row is not a K3 firing. Held.
(b) Negation; item 8 mandates the methods, so reporting results without them violates item 8.
(c) Full selection-process paragraph (L20-21): no contradicting sentence. **Held.**

**Row 5 — "describe the results from records identified to studies included, ideally with a flow
diagram" / Never: "report only the final count without the identification-to-inclusion path."**
Q5 = "Describe the results of the search and selection process, from the number of records identified"
(L53-54). (a) Matches; the "ideally using a flow diagram" tail is in the continuation line (L54) — still
entailed. Held. (b) Negation of "from … identified … to … included". Held.
(c) Item 16a (L53-54) + 16b (L55): no contradicting sentence. **Held.**

## Rows 6–7: S018 survey abstract (S018 `248b432…`, abstract = L76; repeats L120/L198/L233 identical)

**Row 6 — "cite, attribute, or quote the supporting evidence so the link is traceable" / Never: "assert a
claim without linking it to the evidence that supports it."**
Q6 = "aiming to link model outputs to supporting evidence to ensure traceability and verifiability."
Q7 = "Thereby, we focus on approaches that use citations, attribution, or quotations for evidence-based
text generation."
(a) Q6 gives the purpose (link outputs to evidence for traceability); Q7 names the three mechanisms the
survey focuses on. Together they entail the Do, with the row's "so the link is traceable" carried by
Q6's "to ensure traceability…". Q6/Q7 describe what papers in the field *aim* at and what the survey
*focuses on* — the move from description to "Do" is the entry's stated normative reading, but it adds no
new mechanism or agent the quotes lack; this is scope narrowing/reading, not a new fact. Held.
(b) Never = negation of Q6's aim; the survey does not license unlinked assertions. Held.
(c) Remainder of the abstract (L76, full text read): the subject is LLM evidence-based generation, not
search reporting; no sentence contradicts linking claims to evidence. **Held.**

**Row 7 — "use a shared taxonomy and unified benchmarks rather than isolated evaluation practices" /
Never: "compare approaches that use different terminologies and metrics without noting the fragmentation."**
Q8 = "However, the field is fragmented due to inconsistent terminology, isolated evaluation practices, and
a lack of unified benchmarks."
(a) Adds: Q8 says the field *is* fragmented and proposes "a unified taxonomy" and investigating
"300 evaluation metrics" (L76, same paragraph, unquoted). The Do says "use a shared taxonomy and
unified benchmarks" — the survey proposes/does this as its remedy; "use … rather than" is a fair
compression of its stance. Not a new fact type. Held.
(b) Q8 identifies different terminologies/evaluation as the fragmentation; the Never is the mirror
image. Held. (c) Same-paragraph remedy sentence ("To bridge this gap … introduce a unified taxonomy…")
*supports*, not contradicts. **Held.**

## Rows 8–11: DCMI terms (S023 `f5545a…`)

**Row 8 — "name the related resource from which the described resource is derived" / Never: "record a
resource without naming its source."**
Q9 = "A related resource from which the described resource is derived." (L10318, Definition of `source`,
Label "Source" L10308).
(a) Q9 defines the property `source`; the Do "name the related resource…" is the definition-to-practice
reading (a property's value being the named related resource). The adjacent comment (L10328) —
"Best practice is to identify the related resource by means of a URI or a string conforming to a formal
identification system" — confirms identification, not mere mention. The row is narrower than that best
practice. Not an entailment failure. Held.
(b) Never is the negation of recording the property; nothing in L10317-10328 licenses unnamed sourcing.
Held. (c) Full `source` definition block (L10307-10328) read; no contradicting sentence. The entry's
own Limit notes the row assumes the source can be named. **Held.**

**Row 9 — "state the date on which the resource was changed" / Never: "record a modification without its
date."**
Cited warrant: Q10 (L3256 etc.).
(a) Q10 = "Recommended practice is to describe the date, date/time, or period of time as recommended for
the property Date, of which this is a subproperty." Standing alone, Q10 does *not* state the date of
change — it states a format recommendation shared by eight date subproperties in the capture (available,
created, dateAccepted, dateCopyrighted, dateSubmitted, issued, modified, valid). What states "Date on
which the resource was changed." is the *neighboring Definition* of `modified` at L8786 ("Date Modified"
label L8776) — a sentence of the same source that is **not** in the cited warrant. The row's Do
therefore does not follow from Q10 *as cited*; it follows from Q10+Definition, but the warrant cell
lists only Q10. This is the weakest cell in the entry.
(b) Same defect on the Never side: "without its date" is licensed by the Definition+comment at L8786-8796,
not by Q10 alone.
Severity under frozen K3: K3(a) as written reads "its cited quotes do not state or entail". Q10 alone
entails "describe *some* date" but not "*the date on which the resource was changed*". A strict
warrant-audit reading fires (a) on this row; a charitable reading (warrant-column ellipsis, neighboring
sentence of the same term) holds it.
(c) Contradiction search: the real `modified` block (L8728-8818) contains no contradicting sentence;
Q10's "recommended practice" language is a soft hedge ("Recommended") that the row hardens into a
categorical Do/Never — but this is a narrowing/leveling, and the Limits section explicitly disclaims
any timing policy. **Row 9: FIRED (a) — warrant mis-citation. Q10 alone does not fix the modification
date; the needed sentence is the uncited L8786.**

**Row 10 — "state the date or range of validity of the resource" / Never: "record a validity period
without its dates."**
Q11 = "Date (often a range) of validity of a resource." (L11517, Definition of `valid`, Label "Date
Valid" L11507; comment L11527 = Q10's text again).
(a) Q11 states the date-or-range semantics; Do is a direct reading. Held.
(b) Negation; nothing in L11516-11548 licenses dateless validity periods. The adjacent comment *is* Q10,
so the Never's "dates" plural is consistent. Held. (c) Full `valid` block read; no contradiction.
**Held.**

**Row 11 — "state the date the resource became or will become available" / Never: "record availability
without its date."**
Q12 = "Date that the resource became or will become available." (L3246, Definition of `available`,
Label "Date Available" L3236; comment L3256 = Q10).
(a) Do is Q12 verbatim. Held. (b) Negation; comment supports date-typed value. Held.
(c) Full `available` block read (L3199-3300); no contradiction. **Held.**

## Residuals — `## Inference` / `## Limits` (not K3 rows; judged for overreach)

- **Inference (L53-57):** explicitly flagged "the lane's, not stated by the sources", mapped onto
  `corpus/logs/`, `SOURCES.md` registry rows, S-ids/Q-ids, and hedged "to be tested by future rounds."
  The one true mapping claim ("claims cite S-ids and Q-ids (claims.md, entry decision tables)") is
  checkable in-lane. No overreach beyond the lane's own reading. Strong.
- **Limits (L61-69):** correct scoping — PRISMA items enumerated by number (6, 7, 8, 16a — matches
  S214); S018 limited to attribution motive; DCMI limited to definitions with "no freshness or
  verification policy implied"; row-8 caveat for unknown sources. One gap vs Row 9 (above): the
  Limitations never mention that Q10 is generic to all date subproperties and that the quoted Do depends
  on the unquoted `modified` Definition at L8786. That gap belongs in the Limits' DCMI bullet.

## Residual risk and verification gaps

- K3 here is settled by quote entailment against the committed capture only; live-page re-open (K2 half)
  is out of this seat's scope and no re-open was attempted.
- S018's relevant text is entirely the abstract (only quotable section); later sections of the paper were
  not in the capture, so a contradiction inside the paper body beyond the abstract is not detectable from
  committed bytes.
- S023's Q10 ambiguity (8 occurrences) is a genuine citation-precision defect, but the intended
  `modified` definition is in the same capture, so pocket fix = amend row 9's warrant to
  Q10+Definition L8786 (quad-count notwithstanding, the counter only needs truth).

VERDICT: R84ReviewerEntry C2 fired — row 9's Do/Never do not follow from Q10 alone (needs uncited L8786), all other rows held.
