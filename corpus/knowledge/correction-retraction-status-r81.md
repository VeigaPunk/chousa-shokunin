# Correction and retraction status of a cited work — check it before reuse (round 81)

source: S205, S206, S207
verified-at: 2026-11-06 (round 81; captures `371c55117727d526805f030d`, `f221c90f69188f775e32cd34`, `43a45b49723f7677d6446c92`)
recheck: 365d

## What this entry governs

The lane's claim check runs claim → source → the source's own evidence. A source that has since been corrected,
retracted or flagged with an expression of concern can still open, stay on topic and state the claim at a named
anchor — every one of the four support states in `corpus/knowledge/claim-support-states-r24.md` — while no longer
standing behind it. This entry adds the status check that has to precede reuse, read from three primary
descriptions of how that status is published.

## How the status is published (observations)

NLM (PubMed) links notices to the article they concern, in both directions:

> "the erratum notice is simply linked to the citation for the corrected article." — S205

> "The Publication Type Retracted Publication [PT] is assigned to the retracted article." — S205

ICMJE asks journals to keep the version trail readable:

> "The journal should archive all prior versions of the article." — S206

> "Previous electronic versions should prominently note that there are more recent versions of the article" — S206

Crossref distributes the Retraction Watch database, with a stated coverage limit:

> "Some other update types, such as expressions of concern and corrections, are also included in the data, but these are not as comprehensive as retractions." — S207

## Decision table

| Observation about a cited work | Reading | Do | Never |
|---|---|---|---|
| PubMed record carries Publication Type Retracted Publication | retracted (S205) | record the claim's support as withdrawn; cite the retraction notice beside the work | count the work as support because the anchor still opens |
| PubMed record links an erratum notice | corrected (S205) | open the erratum and re-check the quoted span against the corrected text | quote the uncorrected wording as current |
| A newer article version exists (journal's version note) | superseded wording (S206) | cite the version read, with its date, and say whether a newer one exists | cite a version-less "the article says" |
| Retraction Watch data show no retraction | absence of a retraction record only (S207) | record the check (source, date) as a negative sweep | read it as "no correction or expression of concern either" — S207 says those types are less comprehensive |
| The notice cannot be read (host refuses the fetch) | status unknown | keep the source, mark the status check unresolved, name the notice | treat unreachable as "no notice" |

The last row is this round's own case: the TARCiS correction BMJ 2024;387:q2458 answered HTTP 403 (S208, rejected,
unreachable) — `corpus/knowledge/citation-searching-tarcis-r81.md` records the consequence.

## Inference (lane's, not stated by the sources)

A status check is a negative claim ("no retraction found"), so under this lane's checklist it carries a sweep naming
where it looked (PubMed publication types and linked notices, the journal's version note, the Retraction Watch data)
and the date it looked. The three sources describe where status is published; none of them states this checklist rule.
