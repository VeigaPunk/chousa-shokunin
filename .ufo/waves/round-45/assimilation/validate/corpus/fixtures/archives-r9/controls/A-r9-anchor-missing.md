# research-record v1
<!-- chousa-record: v1 -->

## Meta

| key | value |
|---|---|
| window | loopback |
| fetch | none |
| claims_file | chousa-shokunin/corpus/fixtures/claims-r9.jsonl |
| archive | research/deep-research-2026-09-28/A-shokunin-tradition.md |
| archive_sha256 | 9033857d4625555c7b778dfad6df80e3e1b24ed8bffa3fee2fd445b9c5540b85 |
| note | round-10 archive-scale negative control (anchor-missing): byte-copy of A-r9.md except this row and chain hop 2’s anchor cell, whose quote was mutated to text absent from archive A |

## Question

What does archive A (research/deep-research-2026-09-28/A-shokunin-tradition.md, sha256 9033857d) assert about artisan apprenticeship, independence and transmission, and can each recorded claim be re-derived verbatim from the archive bytes alone - with every external citation it names left marked, not walked?

## Sources

Ranked: the archive itself (S1) is the only locally readable source; the works and accounts it names (S2-S6) rank above it by authority class but are word-of-export only - no external document is held locally, and each pointer is the archive line where the item is named. Bare chips and hosts the export renders as citation furniture are deliberately absent from this table; they appear as marked hops in ## Chain.

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | export | research/deep-research-2026-09-28/A-shokunin-tradition.md | archive A, tier export: a chat-export specimen, pinned 9033857d, never promoted to primary |
| S2 | secondary | research/deep-research-2026-09-28/A-shokunin-tradition.md:67 | Daijisen, Nihon Kokugo Daijiten and Kanjipedia lexical entries, named at A:67; the dictionaries themselves are not held locally |
| S3 | secondary | research/deep-research-2026-09-28/A-shokunin-tradition.md:80 | Adachi's own workshop account of customary apprenticeship terms, named at A:80; the page itself is not held locally |
| S4 | secondary | research/deep-research-2026-09-28/A-shokunin-tradition.md:81 | Taitō City interview with carver Ishii Torao, named at A:81; not held locally |
| S5 | secondary | research/deep-research-2026-09-28/A-shokunin-tradition.md:82 | Echigo Yoita forged-blade association program, named at A:82; not held locally |
| S6 | secondary | research/deep-research-2026-09-28/A-shokunin-tradition.md:88 | Takenaka Carpentry Tools Museum report of Ogawa Mitsuo on Nishioka Tsunekazu, named at A:88; not held locally |

## Chain

| hop | from | to | status | anchor_kind | anchor | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | I could not substantiate this spelling as an established artisan rank in the Japanese or English sources searched. | the A:64 table cell, byte-verbatim; a record of failed substantiation, not proof of nonexistence |
| 2 | C2 | S1 | resolved | quote | The sources point to craft-specific apprenticeship systems, not a universal certification ladder. | A:47 first sentence |
| 3 | C3 | S1 | resolved | quote | There is no universal sacred number of years or common final examination. | A:86 close, source of the no-universal-number claim |
| 4 | C4 | S1 | resolved | quote | This documents graduated responsibility through actual work, rather than independence established by a declaration of knowledge. | A:88 close |
| 5 | C5 | research/deep-research-2026-09-28/B-multiagent-knowledge.md | resolved | quote | Track five axes separately: task competence, retention, evidence fidelity, cross-domain transfer, and operating cost. | cross-archive convergence: A:54 keeps four axes, B:57 tracks five for the same roster problem; the archives are independent chats and A never literally cites B, so this hop records convergence, not citation |
| 6 | C2 | research/deep-research-2026-09-28/C-rank-taxonomy.md | resolved | quote | is not a standard rank sequence | cross-archive convergence: C:53 corrects the same rank-ladder premise A:52 declines; convergence, not citation |
| 7 | C1 | コトバンク | blocked-no-fetch | | | the A:68 chip naming the aggregator behind A's lexical checks; expanding a chip into a locator needs an external document, and this window opens none |

## Claims

| id | kind | text | span | pointer | status |
|---|---|---|---|---|---|
| C1 | observation | A records only failed substantiation for jin'i-ryū as an established artisan rank | I could not substantiate this spelling as an established artisan rank in the Japanese or English sources searched. | research/deep-research-2026-09-28/A-shokunin-tradition.md:64 | verified |
| C2 | observation | A reads the traditions as craft-specific systems and denies a universal rank ladder | The sources point to craft-specific apprenticeship systems, not a universal rank ladder. | research/deep-research-2026-09-28/A-shokunin-tradition.md:47 | verified |
| C3 | observation | A separates finishing, competence and independence and records no universal years count or common final examination | There is no universal sacred number of years or common final examination. | research/deep-research-2026-09-28/A-shokunin-tradition.md:76 | verified |
| C4 | observation | A records graduated responsibility through actual work in the Nishioka account | This documents graduated responsibility through actual work, rather than independence established by a declaration of knowledge. | research/deep-research-2026-09-28/A-shokunin-tradition.md:88 | verified |
| C5 | inference | A's four axes are one partition of the roster problem; B tracks a different set of five (cross-archive convergence, no citation) | keep four axes separate: competence, independence, improvement, and transmission. | research/deep-research-2026-09-28/A-shokunin-tradition.md:54 | verified |

## Negatives

| id | text | sweep | status |
|---|---|---|---|
| N1 | no locally held copy exists, under the archive directory, of any external document this record's sources name | SW1 | swept |

## Sweeps

| id | claim_id | where | status |
|---|---|---|---|
| SW1 | N1 | research/deep-research-2026-09-28/saved-*,research/deep-research-2026-09-28/*-snapshot-* | swept |

## Rejections

| id | ref | reason | flip_condition |
|---|---|---|---|
| R1 | research/deep-research-2026-09-28/A-shokunin-tradition.md:52 | A records that the traditions do not establish the universal minarai → deshi → shokunin → jin'i-ryū → kiwami ladder the request presumed | a local source establishing that ladder as a universal tradition would flip this |
| R2 | research/deep-research-2026-09-28/A-shokunin-tradition.md:64 | jin'i-ryū as an attested artisan rank: A reports only failed substantiation in the searched sources | an attested Japanese spelling for jin'i-ryū carried by a local source would flip this |
| R3 | research/deep-research-2026-09-28/A-shokunin-tradition.md:71 | the shokunin kishitsu reading as the standard one: A records katagi as the dictionary reading of 職人気質 | a dictionary giving kishitsu as the reading would flip this |
| R4 | research/deep-research-2026-09-28/A-shokunin-tradition.md:65 | kiwami as an artisan credential or final rank: A records its ordinary meaning as an extremity, not a credential | a craft institution conferring kiwami as a final rank would flip this |
