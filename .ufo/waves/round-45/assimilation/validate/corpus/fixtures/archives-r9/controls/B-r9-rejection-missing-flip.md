# research-record v1
<!-- chousa-record: v1 -->

## Meta

| key | value |
|---|---|
| window | loopback |
| fetch | none |
| claims_file | chousa-shokunin/corpus/fixtures/claims-r9.jsonl |
| archive | research/deep-research-2026-09-28/B-multiagent-knowledge.md |
| archive_sha256 | 6d8dbddd3e2d2f47dcb153c5a3347cc6321db4afc72cf07da40f0f7fe5022006 |
| note | round-10 archive-scale negative control (rejection-missing-flip): byte-copy of B-r9.md except this row and R2’s emptied flip_condition cell |

## Question

What does archive B (research/deep-research-2026-09-28/B-multiagent-knowledge.md, sha256 6d8dbddd) state about self-rewriting knowledge bases and specialist evaluation, and can each recorded claim be re-derived verbatim from the archive bytes alone - with the preprints it lists left as named, unopened waypoints?

## Sources

Ranked: the archive itself (S1) is the only locally readable source; the papers its work table names (S2-S7) rank above it by authority class but are word-of-export only - each pointer is the export line where the paper is named, and none is held locally. The arxiv.org chip cluster and the B:71 sources line are citation furniture, not documents; they appear as a marked hop in ## Chain.

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | export | research/deep-research-2026-09-28/B-multiagent-knowledge.md | archive B, tier export: a chat-export specimen, pinned 6d8dbddd, never promoted to primary |
| S2 | secondary | research/deep-research-2026-09-28/B-multiagent-knowledge.md:64 | Voyager (Wang et al., 2023), named in the B:64 work-table row; the paper is not held locally |
| S3 | secondary | research/deep-research-2026-09-28/B-multiagent-knowledge.md:65 | Generative Agents (Park et al., 2023), named at B:65; not held locally |
| S4 | secondary | research/deep-research-2026-09-28/B-multiagent-knowledge.md:66 | Reflexion (Shinn et al., 2023), named at B:66; not held locally |
| S5 | secondary | research/deep-research-2026-09-28/B-multiagent-knowledge.md:67 | Dynamic Cheatsheet (Suzgun et al., 2025) and ACE (Zhang et al., 2025), named at B:67; not held locally |
| S6 | secondary | research/deep-research-2026-09-28/B-multiagent-knowledge.md:68 | Memento-Skills (Zhou et al., 2026), named at B:68; not held locally |
| S7 | secondary | research/deep-research-2026-09-28/B-multiagent-knowledge.md:69 | LEGOMem (Han et al., 2025), named at B:69; not held locally |

## Chain

| hop | from | to | status | anchor_kind | anchor | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | (1) Self-rewriting knowledge bases: the most important failure is losing the distinction between observation, interpretation, and established knowledge. | B:77 section line, byte-verbatim |
| 2 | C2 | S1 | resolved | quote | ACE identifies “brevity bias” and “context collapse” in iterative context rewriting. | B:79; the case-study hedge stays attached and the ACE numerals are not reproduced here |
| 3 | C3 | S1 | resolved | quote | The strongest design implication is to make knowledge changes—not agent self-assessments—the unit of evaluation. | B:57 first sentence |
| 4 | C4 | S1 | resolved | quote | Below, I distinguish published findings from my proposed engineering rules. | B:59 |
| 5 | C5 | S1 | resolved | quote | team success does not establish which specialist actually improved | B:47 |
| 6 | C6 | research/deep-research-2026-09-28/A-shokunin-tradition.md | resolved | quote | keep four axes separate: competence, independence, improvement, and transmission. | cross-archive convergence: B:57's five axes vs A:54's four for the same roster problem; the archives are independent chats and B never literally cites A, so this hop records convergence, not citation |
| 7 | C3 | arxiv.org | blocked-no-fetch | | | the B:51 and B:72 chips: the work table's only onward hop; expanding a chip into a locator is a new external fetch this window denies |

## Claims

| id | kind | text | span | pointer | status |
|---|---|---|---|---|---|
| C1 | observation | B records the self-rewrite failure as losing the distinction between observation, interpretation and established knowledge | (1) Self-rewriting knowledge bases: the most important failure is losing the distinction between observation, interpretation, and established knowledge. | research/deep-research-2026-09-28/B-multiagent-knowledge.md:77 | verified |
| C2 | observation | B attaches a case-study hedge to the destructive-compression evidence | ACE identifies “brevity bias” and “context collapse” in iterative context rewriting. | research/deep-research-2026-09-28/B-multiagent-knowledge.md:79 | verified |
| C3 | observation | B's strongest design implication makes knowledge changes the unit of evaluation | The strongest design implication is to make knowledge changes—not agent self-assessments—the unit of evaluation. | research/deep-research-2026-09-28/B-multiagent-knowledge.md:57 | verified |
| C4 | observation | B keeps published findings separate from proposed engineering rules | Below, I distinguish published findings from my proposed engineering rules. | research/deep-research-2026-09-28/B-multiagent-knowledge.md:59 | verified |
| C5 | inference | B holds that team success does not establish which specialist actually improved | team success does not establish which specialist actually improved | research/deep-research-2026-09-28/B-multiagent-knowledge.md:47 | verified |
| C6 | inference | B's five axes and A's four axes are different partitions of the same roster problem, with no citation between the archives | Track five axes separately: task competence, retention, evidence fidelity, cross-domain transfer, and operating cost. | research/deep-research-2026-09-28/B-multiagent-knowledge.md:57 | verified |

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
| R1 | research/deep-research-2026-09-28/B-multiagent-knowledge.md:75 | neural expert-expansion results as validating rules for splitting Markdown corpora: B records they can inspire but do not directly validate such rules | a study directly validating Markdown-corpus split rules would flip this |
| R2 | research/deep-research-2026-09-28/B-multiagent-knowledge.md:59 | recent preprints as establishing indefinite, reliable self-improvement: B keeps their benchmark results short of that claim |  |
| R3 | research/deep-research-2026-09-28/B-multiagent-knowledge.md:55 | unrestricted whole-corpus rewriting: B records the literature offers only much weaker support for it | evidence supporting unrestricted whole-corpus rewriting would flip this |
