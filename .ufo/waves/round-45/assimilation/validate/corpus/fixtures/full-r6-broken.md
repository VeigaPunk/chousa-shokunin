# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
| claims_file | chousa-shokunin/corpus/fixtures/full-r6-broken.claims.jsonl |
| note | round-6 verify-all fixture: every gate-known section carried correctly, structural twin of full-r6-broken.md |

## Question

Does one record that carries every section at once — ranked sources, a resolved three-hop citation chain, three pointed claims, two kept rejections with flip-conditions, and two named sweeps — compose to a single CLEAN verdict whose per-section tallies equal the tallies the four solo modes report for the same bytes?

## Sources

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | export | research/deep-research-2026-09-28/A-shokunin-tradition.md | archived export A, pin 9033857d |
| S2 | export | research/deep-research-2026-09-28/B-multiagent-knowledge.md | archived export B, pin 6d8dbddd |
| S3 | export | research/deep-research-2026-09-28/C-rank-taxonomy.md | archived export C, pin e48fe70f |
| S4 | fleet-gate | chousa-shokunin/corpus/knowledge/archived-export-intake.md | round-1 intake, source of the kept rejections and of the sweeps below |

## Chain

| hop | from | to | anchor_kind | anchor | status | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S1 | quote | I could not substantiate this spelling as an established artisan rank in the Japanese or English sources searched. | resolved | the A:64 row the rejected README gloss overreads |
| 2 | C2 | S2 | quote | Track five axes separately: task competence, retention, evidence fidelity, cross-domain transfer, and operating costs. | resolved | the B:57 separate-the-axes line |
| 3 | C3 | S3 | line | “Jin’i-ryū” does not support the proposed literal translation | resolved | the C:107 section line, whole line |

## Claims

| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | export A records only failed substantiation for the coined rank's spelling | research/deep-research-2026-09-28/A-shokunin-tradition.md:64 | verified | |
| C2 | observation | export B keeps five evaluation axes separate instead of collapsing them to one | research/deep-research-2026-09-28/B-multiagent-knowledge.md:57 | verified | |
| C3 | observation | export C negates the proposed literal translation of the coined rank | research/deep-research-2026-09-28/C-rank-taxonomy.md:107 | verified | |

## Negatives

| id | text | sweep | status |
|---|---|---|---|
| N1 | nothing external was cached locally: no saved copy of a cited external page exists under the archive directory | SW1 | observed-in-dump |
| N2 | no attestation outside the archive establishes jin'i-ryū as a traditional artisan rank | SW2 | unresolved |

## Sweeps

| id | claim_id | where | observed |
|---|---|---|---|
| SW1 | N1 | research/deep-research-2026-09-28/saved-*,research/deep-research-2026-09-28/*-snapshot-* | zero matches, no saved copy of a cited external page exists under the archive directory |
| SW2 | N2 | S1,S2,S3 | content sweep inside the declared exports; exempt and counted, the gate re-runs path sets only |

## Rejections

| id | ref | reason | flip_condition |
|---|---|---|---|
| R1 | research/README.md:12 | the README gloss asserts jin'i-ryu is not an attested artisan rank and offers four axes, while its cited spans (A:47, A:64) record only failed substantiation — intake RJ-02 | an attested Japanese spelling for jin'i-ryū carried by a local source would flip this rejection |
| R2 | research/deep-research-2026-09-28/B-multiagent-knowledge.md:79 | the ACE numerals are model-quality claims belonging to kengaku province, carried here only as a hedge form — intake RJ-03 | |

## Approval

| target | state |
|---|---|
| (none) | not-required |