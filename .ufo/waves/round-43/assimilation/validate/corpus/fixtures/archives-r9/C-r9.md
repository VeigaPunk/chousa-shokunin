# research-record v1
<!-- chousa-record: v1 -->

## Meta

| key | value |
|---|---|
| window | loopback |
| fetch | none |
| claims_file | chousa-shokunin/corpus/fixtures/claims-r9.jsonl |
| archive | research/deep-research-2026-09-28/C-rank-taxonomy.md |
| archive_sha256 | e48fe70ff92055c217ac6ca6ce68e403aa5689fee8717f3bd0ccf5badc92321b |
| note | round-9 archive record: export C converted to the gate's record format; every span and anchor below was extracted byte-verbatim from the archive; its federation and dictionary citations stay unopened |

## Question

What does archive C (research/deep-research-2026-09-28/C-rank-taxonomy.md, sha256 e48fe70f) state about rank ladders, grading structures and naming, and can each recorded claim be re-derived verbatim from the archive bytes alone - with the federation and dictionary citations it names left marked, not walked?

## Sources

Ranked: the archive itself (S1) is the only locally readable source; the dictionary entries and institutions it names (S2-S6) rank above it by authority class but are word-of-export only - each pointer is the export line where the item is named, and none is held locally. The kotobank and host chips are citation furniture, not documents; jstage.jst.go.jp appears as a marked hop in ## Chain.

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | export | research/deep-research-2026-09-28/C-rank-taxonomy.md | archive C, tier export: a chat-export specimen, pinned e48fe70f, never promoted to primary |
| S2 | secondary | research/deep-research-2026-09-28/C-rank-taxonomy.md:81 | Shōgakukan's Digital Daijisen and Nihon Kokugo Daijiten dictionary entries, named at C:81; not held locally |
| S3 | secondary | research/deep-research-2026-09-28/C-rank-taxonomy.md:89 | Nihon Ki-in Go rank scales and professional promotions, named at C:89 and C:99; not held locally |
| S4 | secondary | research/deep-research-2026-09-28/C-rank-taxonomy.md:92 | Japan Karate Association kyū/dan specification, named at C:92; not held locally |
| S5 | secondary | research/deep-research-2026-09-28/C-rank-taxonomy.md:97 | All Japan Kendo Federation dan/kyū grades and shōgō titles, named at C:97; not held locally |
| S6 | secondary | research/deep-research-2026-09-28/C-rank-taxonomy.md:102 | Todo and Murata research on grading history (J-STAGE), named at C:102; not held locally |

## Chain

| hop | from | to | status | anchor_kind | anchor | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | Japanese traditions don’t collapse these into one ladder. | C:53, byte-verbatim |
| 2 | C2 | S1 | resolved | quote | There is no traditional Japanese four-rank ladder that precisely means created → corpus-verified → safely self-improving → agent-producing. | C:65 |
| 3 | C3 | S1 | resolved | line | Kyū/dan is a grading structure, not an autonomy ladder | C:87, whole line |
| 4 | C4 | S1 | resolved | quote | Rank is conferred through a procedure, not established by a practitioner’s self-description. | C:92 |
| 5 | C5 | S1 | resolved | quote | The cultural mistake to avoid is presenting your product’s invented ordering as an inherited Japanese institution. | C:85 |
| 6 | C6 | research/deep-research-2026-09-28/A-shokunin-tradition.md | resolved | quote | I could not substantiate this spelling as an established artisan rank in the Japanese or English sources searched. | cross-archive convergence: C:109 and A:64 record the same failed substantiation for the coined rank; the archives are independent chats and C never literally cites A, so this hop records convergence, not citation |
| 7 | C7 | research/deep-research-2026-09-28/B-multiagent-knowledge.md | resolved | quote | Track five axes separately: task competence, retention, evidence fidelity, cross-domain transfer, and operating cost. | cross-archive convergence: C:67's four axes vs B:57's five for the same roster problem; convergence, not citation |
| 8 | C8 | jstage.jst.go.jp | blocked-no-fetch | | | the C:103 chip behind the Todo/Murata reference; the paper is not held locally and this window opens no external document |

## Claims

| id | kind | text | span | pointer | status |
|---|---|---|---|---|---|
| C1 | observation | C separates skill, teaching authority and permission to act, and records that the traditions do not collapse them into one ladder | Japanese traditions don’t collapse these into one ladder. | research/deep-research-2026-09-28/C-rank-taxonomy.md:53 | verified |
| C2 | observation | C denies a traditional four-rank ladder that precisely maps its four agent states | There is no traditional Japanese four-rank ladder that precisely means created → corpus-verified → safely self-improving → agent-producing. | research/deep-research-2026-09-28/C-rank-taxonomy.md:65 | verified |
| C3 | observation | C records kyū/dan as a grading structure, not an autonomy ladder | Kyū/dan is a grading structure, not an autonomy ladder | research/deep-research-2026-09-28/C-rank-taxonomy.md:87 | verified |
| C4 | observation | C records rank conferred through a procedure, not established by a practitioner's self-description | Rank is conferred through a procedure, not established by a practitioner’s self-description. | research/deep-research-2026-09-28/C-rank-taxonomy.md:92 | verified |
| C5 | observation | C names the cultural-misrepresentation guard for invented orderings | The cultural mistake to avoid is presenting your product’s invented ordering as an inherited Japanese institution. | research/deep-research-2026-09-28/C-rank-taxonomy.md:85 | verified |
| C6 | inference | C and A converge on failed substantiation of jin'i-ryū as an established rank (cross-archive convergence, no citation) | I found no authoritative attestation establishing jin’i-ryū as “self-legislating school.” | research/deep-research-2026-09-28/C-rank-taxonomy.md:109 | verified |
| C7 | inference | C's four axes and B's five axes are different partitions of the same roster problem, with no citation between the archives | knowledge provenance, demonstrated competence, authority to modify itself, and authority to create other agents | research/deep-research-2026-09-28/C-rank-taxonomy.md:67 | verified |
| C8 | observation | C records that grading history is more complicated than 'ancient samurai belts' and cites Todo and Murata for it | Historically, the story is more complicated than “ancient samurai belts.” | research/deep-research-2026-09-28/C-rank-taxonomy.md:102 | verified |

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
| R1 | research/deep-research-2026-09-28/C-rank-taxonomy.md:53 | the Shokunin → takumi → meishō rank sequence as a standard one: C records it is not, and finds no support for the jin'i-ryū translation either | a source establishing it as a standard rank sequence would flip this |
| R2 | research/deep-research-2026-09-28/C-rank-taxonomy.md:109 | jin'i-ryū as 'self-legislating school': C finds no authoritative attestation; romanization without kanji cannot establish a literal meaning | an authoritative attestation carried by a local source would flip this |
| R3 | research/deep-research-2026-09-28/C-rank-taxonomy.md:133 | menkyo kaiden as a corpus download or a generic license to create peers: C records it as complete transmission of an art's teachings | a school whose menkyo kaiden confers replication authority would flip this |
| R4 | research/deep-research-2026-09-28/C-rank-taxonomy.md:102 | a single timeless Japanese rank tradition: C records the grading history as more complicated | a documented single timeless tradition would flip this |
