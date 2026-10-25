# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
| note | chain-hop fixture, broken-anchor control (round 3); hop 2 claims a citation the target does not contain |

## Question

Can a hop that claims status=resolved but cites an anchor the target never contains pass this record's chain?

## Sources

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | export | research/deep-research-2026-09-28/A-shokunin-tradition.md | archived deep-research export A, pin 9033857d |
| S3 | export | research/deep-research-2026-09-28/C-rank-taxonomy.md | archived deep-research export C, pin e48fe70f |

## Chain

| hop | from | to | anchor_kind | anchor | status | notes |
|---|---|---|---|---|---|---|
| 1 | A:47 | S1 | quote | I could not substantiate this spelling as an established artisan rank in the Japanese or English sources searched. | resolved | control hop that does resolve: the row carrying the finding is at A:64 |
| 2 | A:64 | S3 | quote | 人為 — jin’i-ryū | resolved | control hop that must not pass: C anchors 人為 only for jin'i at C:118, never for the coined rank |

## Claims

| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | the broken hop cites a kanji form C does not carry for the coined rank | research/deep-research-2026-09-28/C-rank-taxonomy.md:118 | unresolved |

## Rejections

| id | ref | reason |
|---|---|---|
| R1 | (none) | no source was rejected; this record is the fixture's own negative control |

## Approval

| target | state |
|---|---|
| (none) | not-required |