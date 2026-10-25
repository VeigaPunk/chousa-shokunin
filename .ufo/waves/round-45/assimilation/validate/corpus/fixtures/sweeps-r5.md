# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
| note | round-5 sweep/rejection fixture; every kept rejection carries reason + flip_condition, every negative sweep names where it looked |

## Question

Do the kept rejections in this record carry both a reason and a flip-condition, and does each negative sweep name where it looked, so that a rejection with no flip-condition or a sweep naming nowhere (or naming a false emptiness) cannot pass?

## Sources

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | export | research/deep-research-2026-09-28/A-shokunin-tradition.md | archived export A, pin 9033857d |
| S2 | export | research/deep-research-2026-09-28/B-multiagent-knowledge.md | archived export B, pin 6d8dbddd |
| S3 | export | research/deep-research-2026-09-28/C-rank-taxonomy.md | archived export C, pin e48fe70f |
| S4 | fleet-gate | corpus/knowledge/archived-export-intake.md | round-1 intake record, source of the kept rejections and sweeps below |

## Chain

| hop | from | to | anchor_kind | anchor | status | notes |
|---|---|---|---|---|---|---|
| 1 | R1 | S1 | quote | I could not substantiate this spelling as an established artisan rank in the Japanese or English sources searched. | resolved | the A:64 row the rejected gloss overreads |
| 2 | W1 | S4 | quote | zero matches, no URL locator exists in the archive set | resolved | the intake's own zero-match census cell (its W2) |
| 3 | W2 | https://kotobank.jp/ | - | - | blocked-no-fetch | external dictionary attestation stays unwalked |

## Claims

| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| CL1 | observation | export A records failed substantiation for the jin'i-ryū spelling | research/deep-research-2026-09-28/A-shokunin-tradition.md:64 | verified | |
| N1 | negative | nothing external was cached locally: no saved copy of a cited external page exists under the archive set | research/deep-research-2026-09-28/A-shokunin-tradition.md:64 | observed-in-dump | W1 |
| N2 | negative | no attestation establishes jin'i-ryū as a traditional artisan rank outside the archive | research/deep-research-2026-09-28/A-shokunin-tradition.md:64 | unresolved | W2 |

## Rejections

| id | ref | reason | flip_condition |
|---|---|---|---|
| R1 | research/README.md:12 | the gloss asserts jin'i-ryu is not an attested artisan rank while the spans it cites (A:47, A:64) record only failed substantiation | an attested Japanese spelling for jin'i-ryū carried by a local source would flip this rejection |
| R2 | research/deep-research-2026-09-28/B-multiagent-knowledge.md:79 | the ACE numerals are model-quality claims from kengaku province, carried here only as a hedge form | a kengaku-lane adjudication of those numerals would flip this rejection |
| R3 | research/deep-research-2026-09-28/B-multiagent-knowledge.md:63 | the work table is an export-unverified bibliography whose only onward hop is citation furniture (B:71-73) | locators resolving inside the corpus boundary would flip this rejection |

## Sweeps

| id | claim_id | where | observed |
|---|---|---|---|
| W1 | N1 | research/deep-research-2026-09-28/kotobank-*,research/deep-research-2026-09-28/saved-* | zero matches, no saved copy of a cited external page exists under the archive set |
| W2 | N2 | https://kotobank.jp/ | non-local target would need an external fetch; recorded, never walked |

## Approval

| target | state |
|---|---|
| (none) | not-required |