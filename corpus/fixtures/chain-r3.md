# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
| note | chain-hop fixture (round 3); targets are the three archived inputs, opened read-only |

## Question

Does every hop in this record's citation chain resolve to real bytes at its target under the corpus boundary — a section title carried as one whole line, or a verbatim quote — so that a hop citing an anchor the target never contains cannot pass?

## Sources

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | export | research/deep-research-2026-09-28/A-shokunin-tradition.md | archived deep-research export A, pin 9033857d |
| S2 | export | research/deep-research-2026-09-28/B-multiagent-knowledge.md | archived deep-research export B, pin 6d8dbddd |
| S3 | export | research/deep-research-2026-09-28/C-rank-taxonomy.md | archived deep-research export C, pin e48fe70f |

## Chain

| hop | from | to | anchor_kind | anchor | status | notes |
|---|---|---|---|---|---|---|
| 1 | A:35 | S1 | line | 1. When does an apprentice earn domain independence? | resolved | question item (1) is answered under this title line at A:74 |
| 2 | A:47 | S1 | quote | I could not substantiate this spelling as an established artisan rank in the Japanese or English sources searched. | resolved | preamble finding chains to the terminology table row that carries it at A:64 |
| 3 | A:52 | S1 | quote | minarai/deshi/shokunin/jin'i-ryu/kiwami semantics | resolved | the ladder notation the record negates at A:52 is anchored in the user's own term list at A:35 |
| 4 | A:47 | S3 | line | “Jin’i-ryū” does not support the proposed literal translation | resolved | cross-input co-anchor: the same jin'i-ryu negative finding is the section title at C:107 |
| 5 | A:64 | S3 | quote | I found no authoritative attestation establishing jin’i-ryū as “self-legislating school.” | resolved | cross-input co-anchor: failed substantiation of jin'i-ryu stated verbatim at C:109 |
| 6 | A:54 | S2 | quote | Track five axes separately: task competence, retention, evidence fidelity, cross-domain transfer, and operating cost. | resolved | cross-input co-anchor of the separate-the-axes move; A names four at A:54, B names five at B:57; the anchor resolves, agreement is not adjudicated |
| 7 | B:64 | S2 | quote | Sources: Voyager and Generative Agents; Reflexion; Dynamic Cheatsheet and ACE; Memento-Skills; LEGOMem. | resolved | the table rows' citations are enumerated in the Sources line at B:71 |
| 8 | B:47 | S2 | quote | Evolving strategies and domain playbooks | resolved | the preamble's closest-match finding chains to the Dynamic Cheatsheet/ACE row cell at B:67 |
| 9 | B:47 | S2 | quote | In one AppWorld case, a rewrite reduced accumulated context from 18,282 tokens to 122 | resolved | the destructive-compression finding chains to the ACE evidence line at B:79 |
| 10 | B:57 | S1 | quote | graduated responsibility through actual work, rather than independence established by a declaration of knowledge. | resolved | cross-input co-anchor: knowledge changes, not self-assessments (B:57); actual work, not a declaration of knowledge (A:88) |
| 11 | B:57 | S3 | quote | The axes your system needs are knowledge provenance, demonstrated competence, authority to modify itself, and authority to create other agents. | resolved | cross-input co-anchor of the separate-the-axes move; B's five axes and C's four at C:67 are different sets |
| 12 | C:65 | S3 | line | Kyū/dan is a grading structure, not an autonomy ladder | resolved | the no-four-rank-ladder finding at C:65 chains to the section title at C:87 that elaborates it |
| 13 | C:87 | S3 | quote | In Go, kyū 級 counts downward toward 1-kyū; dan 段 counts upward from 1-dan. | resolved | the grading-structure section's claim is anchored in its Go body line at C:89 |
| 14 | C:65 | S1 | quote | They do not establish a universal ladder of minarai → deshi → shokunin → jin’i-ryū → kiwami. | resolved | cross-input co-anchor: no universal ladder, stated at C:65 and verbatim in A at A:52 |
| 15 | C:75 | S1 | quote | A skilled craft worker/artisan. The word itself does not certify supreme mastery or business independence. | resolved | cross-input co-anchor: shokunin as occupational identity, not a mastery certificate, stated at C:75 and verbatim in A at A:63 |
| 16 | C:65 | S2 | quote | It offers much weaker support for unrestricted whole-corpus rewriting or automatic creation of specialists based on topic novelty alone. | resolved | cross-input co-anchor: the create → corpus-verified → self-improving → agent-producing ladder is not established; tradition side C:65, literature side B:55 |
| 17 | C:53 | S3 | line | “Jin’i-ryū” does not support the proposed literal translation | resolved | the preamble negation at C:53 chains to its own section title at C:107; the same anchor bytes are also reached by hop 4 |
| 18 | A:67 | https://kotobank.jp/ | - | - | blocked-no-fetch | the dictionary attestation for A:67's lexical distinctions is cited as コトバンク (the export's chip, A:68), outside the corpus boundary; no external window; never fetched |
| 19 | B:71 | https://arxiv.org/ | - | - | blocked-no-fetch | the five papers enumerated at B:71 are cited as arxiv.org (the export's chip, B:72), outside the corpus boundary; URL sources are refused unopened; never fetched |
| 20 | A:64 | S3 | quote | 人為 — jin’i-ryū | unresolved | C anchors 人為 only for jin'i at C:118, never for the coined rank; the anchor bytes are absent — this marking records a real chain break, not a pass |
| 21 | B:35 | S2 | line | When to split a domain into a new specialist | unresolved | question item (2) at B:35 has no title line; the three exports carry no Markdown headings at all (grep -c '^#' = 0) |
| 22 | C:69 | S1 | quote | Minarai → Shokunin with a self-iteration license | unresolved | C's recommended adaptation at C:69 has no A-side anchor; A carries a different ladder and negates a universal one at A:52 |

## Claims

| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | export A carries the terminology table with the jin'i-ryu substantiation row | research/deep-research-2026-09-28/A-shokunin-tradition.md:64 | verified |
| C2 | inference | the resolved hops above are resolvable against the pinned exports at this revision | S1 | unresolved |

## Rejections

| id | ref | reason |
|---|---|---|
| R1 | (none) | no source was rejected; the fixture's negative controls are separate records |

## Approval

| target | state |
|---|---|
| (none) | not-required |