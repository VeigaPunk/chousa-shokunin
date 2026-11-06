# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none at record level; one live re-open of S205 by the item-5 check under the round-81 approval table |
| claims_file | corpus/evidence/round81/trial/claims.jsonl |
| note | item-4 attack twin: R1's flip_condition cell states "none" — the record itself declares no flip condition exists |

## Question

Is the TARCiS statement's recommendation on stand-alone citation searching supported by the accepted manuscript, and is the statement's correction status known?

## Sources

| id | tier | pointer | notes |
|---|---|---|---|
| S203 | primary | corpus/captures/f2489455cc311a4de981e926.txt | TARCiS statement, author accepted manuscript of BMJ 2024;385:e078384, text form of capture key f2489455cc311a4de981e926 |
| S205 | primary | corpus/captures/371c55117727d526805f030d.txt | NLM, Errata, Retractions, and Other Linked Citations in PubMed, text form of capture key 371c55117727d526805f030d |

## Chain

| hop | from | to | anchor_kind | anchor | status | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S203 | quote | Stand-alone citation searching should not be used for literature searches that aim at completeness of recall. | resolved | recommendations summary of the accepted manuscript, capture line 789 |
| 2 | C2 | S205 | quote | the erratum notice is simply linked to the citation for the corrected article. | resolved | Errata section of the NLM page, capture line 323 |
| 3 | N1 | https://www.bmj.com/content/387/bmj.q2458.full.txt | - | - | blocked-no-fetch | one GET on 2026-11-06 answered HTTP 403 (curl rc 22, refetch.tsv row S208) |

## Claims

| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | Stand-alone citation searching should not be used for literature searches that aim at completeness of recall. | corpus/captures/f2489455cc311a4de981e926.txt | verified | |
| C2 | observation | the erratum notice is simply linked to the citation for the corrected article. | corpus/captures/371c55117727d526805f030d.txt | verified | |
| N1 | negative | no readable copy of the BMJ correction q2458 was obtained this round | corpus/evidence/round81/egress-approval.md | observed-in-dump | W1 |

## Rejections

| id | ref | reason | flip_condition |
|---|---|---|---|
| R1 | https://www.bmj.com/content/387/bmj.q2458.full.txt | S208 answered HTTP 403 (curl rc 22, 2026-11-06T18:44:31Z); no text was located, so nothing is taught from it | none |

## Sweeps

| id | claim_id | where | observed |
|---|---|---|---|
| W1 | N1 | https://www.bmj.com/content/387/bmj.q2458.full.txt | one GET, HTTP 403 (refetch.tsv row S208, 2026-11-06); zero readable bytes of the correction |

## Approval

| target | state |
|---|---|
| nlm.nih.gov page S205, item-5 quote re-open | granted under corpus/evidence/round81/egress-approval.md |
