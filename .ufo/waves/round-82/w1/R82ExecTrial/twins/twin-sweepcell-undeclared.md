# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
| claims_file | corpus/evidence/round82/trial/trial-claims.jsonl |
| note | round-82 trial record (seat R82ExecTrial): one real question answered through the landed record v1 grammar; every pointer is a file committed in the candidate landing tree, no URL is opened and no live page is read |

## Question

For a chousa research record whose question maps what exists (not a test of an effect), what question frame applies, and what must the record keep separate?

## Sources

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | primary | corpus/captures/fd7eed5e0e6c64e22bc1470c.txt | Cochrane Handbook chapter 2 as served 2026-11-06 (capture key fd7eed5e0e6c64e22bc1470c), sha256 598abc098b57415985b3ed8c774fddc9b716e8b20b34c5e1f49d7e8be2ac433a |
| S2 | primary | corpus/captures/bcb4a695b2aa019305121cff.txt | JBI Manual 10.2.3 as served 2026-11-06 (capture key bcb4a695b2aa019305121cff), sha256 fc857da335013077796dd31bfc138caeb66286783f94677e054b02c8cf889875 |

## Chain

| hop | from | to | anchor_kind | anchor | status | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S1 | quote | The review PICO (planned at the protocol stage) is the PICO on which eligibility of studies is based | resolved | the planned frame is the eligibility boundary |
| 2 | C2 | S1 | quote | The PICO for each synthesis (also planned at the protocol stage) defines the question that each specific synthesis aims to answer | resolved | the frame of each planned comparison is a second record |
| 3 | C3 | S1 | quote | The PICO of the included studies (determined at the review stage) is what was actually investigated in the included studies. | resolved | what was found is a third record, taken at the review stage |
| 4 | C4 | S2 | quote | JBI suggests utilising the PCC (population, concept and context) approach to formulate review questions for scoping reviews. | resolved | the mapping-question frame |
| 5 | C5 | S2 | quote | A scoping review question is broader than those in systematic reviews and can be seen as hypothesis-generating, whereas a systematic review is hypothesis-testing | resolved | why a mapping question is not an effect test |

## Claims

| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | the Handbook fixes the review PICO at the protocol stage as the basis on which study eligibility is decided | corpus/captures/fd7eed5e0e6c64e22bc1470c.txt:560 | verified | |
| C2 | observation | the Handbook plans a separate PICO for each synthesis, defining the question that synthesis answers | corpus/captures/fd7eed5e0e6c64e22bc1470c.txt:561 | verified | |
| C3 | observation | the Handbook names the PICO of the included studies as what was actually investigated, determined at the review stage | corpus/captures/fd7eed5e0e6c64e22bc1470c.txt:562 | verified | |
| C4 | observation | JBI recommends the population, concept and context approach to formulate scoping-review questions | corpus/captures/bcb4a695b2aa019305121cff.txt:838 | verified | |
| C5 | observation | JBI calls a scoping-review question hypothesis-generating and a systematic-review question hypothesis-testing | corpus/captures/bcb4a695b2aa019305121cff.txt:838 | verified | |
| C6 | observation | JBI states that an unclear review question leaves the review without coherence | corpus/captures/bcb4a695b2aa019305121cff.txt:837 | verified | |
| C7 | inference | for a record that maps what exists, the frame is population, concept and context, and the planned frame, the question of each planned synthesis and the frame of what was found stay three separate records | corpus/captures/bcb4a695b2aa019305121cff.txt:838 | inferred | |
| C8 | unknown | whether a frame other than the two read here governs a record whose unit is a claim rather than a study population is not stated in either capture | corpus/captures/fd7eed5e0e6c64e22bc1470c.txt:562 | unresolved | |
| N1 | negative | no knowledge entry named for a question frame exists under corpus/knowledge/ at a base revision before round 82 | corpus/evidence/round82/base-knowledge.txt | observed-in-dump | W9 |

## Rejections

| id | ref | reason | flip_condition |
|---|---|---|---|
| R1 | corpus/captures/dedff231d5c3d3cdb0b4f8e3.txt | the page describes a citation-metadata service for a cited work's update, correction or retraction status, so it speaks to source currency, not to how a review question is framed or aligned with its objective and criteria | a paragraph on that page stating a rule for framing or aligning a research question would flip this rejection |

## Sweeps

| id | claim_id | where | observed |
|---|---|---|---|
| SW1 | N9 | corpus/knowledge/*question-frame*.md,corpus/knowledge/*question*-r[1-9].md,corpus/knowledge/*question*-r[1-7][0-9].md,corpus/knowledge/*question*-r8[01].md | zero matches: the only question-named entry under corpus/knowledge/ is the round-82 one, which none of the four base-revision globs matches |

## Approval

| target | state |
|---|---|
| (none) | not-required |
