# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
| note | round-81 checklist fixture (item 4 fail: the kept rejection has no flip-condition) |

## Question

Does the TARCiS statement appear in the lane's pre-round knowledge set, and is every kept rejection complete?

## Sources

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | fleet-gate | corpus/fixtures/sweeps-r5.md | round-5 sweep fixture, used here only as a declared local source |

## Claims

| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| N1 | negative | no pre-round knowledge entry file is named for the TARCiS statement | corpus/fixtures/sweeps-r5.md | observed-in-dump | W1 |

## Kept rejections

| id | ref | reason | flip_condition |
|---|---|---|---|
| R1 | corpus/fixtures/sweeps-r5.md | a round-5 fixture is test data, not a source on citation searching |  |

## Sweeps

| id | claim_id | where | observed |
|---|---|---|---|
| W1 | N1 | corpus/knowledge/*tarcis-r80*,corpus/knowledge/*tarcis-pre-r81* | zero matches |

## Approval

| target | state |
|---|---|
| (none) | not-required |
