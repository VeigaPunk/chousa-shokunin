# R82ReviewerEntry — scoped findings (round 82, C2 kill rule K3)

Candidate: `b4a41d251b488f06b4a6ab01a11bc12ce72edd20`. Full review with per-row judgments and receipts:
`.ufo/waves/round-82/w1/R82ReviewerEntry/review.md` (receipts in `…/R82ReviewerEntry/receipts/`).

## K3 FIRED — one row suffices under the frozen rule

**Row 1 of `corpus/knowledge/question-framing-frames-r82.md`** (situation "The question asks what exists on a topic (a
map, not a test of an effect)"):

- Never cell: "force an intervention, comparator and outcome onto a mapping question".
- Warrant Q6+Q7 (S210, capture `bcb4a695b2aa019305121cff` line 838) is a suggestion ("JBI **suggests** utilising the
  PCC…") plus a description ("…can be seen as hypothesis-generating…"). Neither states or entails a prohibition.
- Same capture, line 840 — the Q8 quote row 2 itself warrants on — says "there may be a compelling argument to use a
  different question format (such as PICO or Population, Exposure, Comparator, Outcome [PECO]), such as when performing a
  structured analysis of existing research or research gaps, or as a precursor to a systematic review." Row 1's situation
  covers those cases, so the source in context endorses the forbidden framing for a subset of the row's own situation.
- Judgment: Never **not supported** (and contradicted in part) by its warranting quote read in context → C2 falsified per
  claims.md K3. "A repair after scoring does not rescue the claim."
- Row 1's Do is supported; the other eight rows' Do and Never cells are all judged supported in the full review (three
  hedge/implication residuals noted there, none firing).

## Secondary observations (non-kill)

1. Rows 1 and 2 conflict for overlapping situations (a map feeding an SR) with no precedence rule — same defect family as
   the firing cell.
2. Row 7's Never drops Q5's "generally" hedge (fd7eed5e:690); row 3's Never asserts an exclusivity Q10 implies but does
   not state (97223722:736).
3. S008 registry anchor names "sections 2.1 Key Points and 2.3" but counted quote Q5 lives in 2.5.2 Changing review
   questions (fd7eed5e:499, :690). S210 registry teaches upgrades "suggests" to "use" and omits the gap-analysis case.
4. `## Inference` is honestly fenced ("lane's, not stated by the sources"); `## Limits` correctly discloses the S209
   title/slug drift (capture title "10.2.2 Developing your protocol" at 21323730:189 vs slug "Developing the title and
   question" in refetch.tsv row 153). Crossmark addendum in `corpus/knowledge/correction-retraction-status-r81.md`: the
   "never" clause is explicitly disclosed as the lane's reading ("S028 does not itself state what an absent button
   means") and both S028 quotes verify (dedff231:164, :183). Honest.

## Evidence basis

All 11 located quotes verified verbatim in the committed captures (`grep -n -i -F`, rc=0 each, `receipts/command-log.txt`
[3]); capture sha256s match refetch.tsv rows 152–156 (`receipts/capture-sha256.txt`, `receipts/refetch-rows.txt`);
working-tree entry byte-identical to the candidate revision (`diff` rc=0). No network, no fetches, no re-opens; scratch
`/fast/scratch/hyaku/chousa-r82/R82ReviewerEntry` deleted before yield. K4 not in scope, not run.

VERDICT: R82ReviewerEntry C2 fired — row 1's Never ("force an intervention, comparator and outcome onto a mapping question") is not supported by Q6/Q7 (bcb4a695:838) and is contradicted in part by the same capture's line 840, which endorses PICO/PECO for mapping questions feeding structured gap analyses or systematic reviews.
VERDICT: R82ReviewerEntry C1 n/a — not assigned to this seat; no C1 check was run.
