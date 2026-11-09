# PRESS 2015 — what the guideline statement's own abstract says it is, and the checklist's remaining questions (round 98)

source: S231, S225
verified-at: 2026-11-09 (round 98; capture `4ec85a1e83553aa272caeb69` — Europe PMC's core record for PMID 27005575, the PRESS 2015 Guideline Statement (McGowan J et al., J Clin Epidemiol 2016;75:40-46), carrying the statement's own published abstract, opened as S231 — and capture `347c55ba9be9d63afe17986e`, Cochrane's search checklist for editors reprinting the PRESS 2015 Evidence-Based Checklist, opened as S225 in round 97 and re-read here)
recheck: on-release

## What this entry governs

Two earlier entries hold PRESS 2015 through secondary routes only. The round-96 entry
(`search-peer-review-dedup-r96.md`) holds its six elements, the removal of a seventh and the timing of review
through the authors' lightning-talk abstract (S223, tier B). The round-97 entry
(`press-checklist-questions-r97.md`) holds 16 of the 36 lines of S225's checklist that carry a question mark,
through a reprint (S225, tier B). This entry adds two things:

1. **The guideline statement's own abstract (S231).** It is the abstract the statement's authors published with
   the statement, read through Europe PMC's index record of it (the statement's full text, the CADTH E&E, its
   Table 9 and the CADTH report 477 appendices all answered http 403 or a challenge page to this host; S227, S228,
   and the round-96/97 attempts). It states what PRESS 2015 *is* — four documents, of which the checklist is one —
   how it was made, what the evidence review found about the elements, and the seventh element's full name. Tier A
   for that scope only: the abstract, not the statement's body.
2. **The other 20 question lines of the checklist (S225).** With the round-97 entry, every S225 line between the
   checklist heading and "Derived from:" that carries a question mark is now quoted whole (36 of 36), as one quote
   or as consecutive quotes that join with one space; the controls recompute this.

The column marked *lane* is this lane's reading; it is not what PRESS, the statement's authors or Cochrane say.

## Located quotes

S231's capture is the JSON record exactly as served (one line; the abstract's section headings are `<h4>` markup
inside the `abstractText` string). Every S231 quote below is a substring of that string with no markup inside it.
S225 quotes are substrings of one capture line each; K17-K18 are capture line 66 split at a word boundary (30
words), K19 is line 67 (the same question's last words), and K21-K22 are line 78 split (28 words), to stay within
25 words per quote.

| qid | source | quote |
|---|---|---|
| M1 | S231 | "PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement." |
| M2 | S231 | "To develop an evidence-based guideline for Peer Review of Electronic Search Strategies (PRESS) for systematic reviews (SRs), health technology assessments, and other evidence syntheses." |
| M3 | S231 | "An SR, Web-based survey of experts, and consensus development forum were undertaken" |
| M4 | S231 | "No new search elements were identified for addition to the existing (2008-2010) PRESS 2015 Evidence-Based Checklist," |
| M5 | S231 | "and there was no evidence refuting any of its elements." |
| M6 | S231 | "Results suggested that structured PRESS could identify search errors and improve the selection of search terms." |
| M7 | S231 | "Most respondents felt that peer review should be undertaken after the MEDLINE search had been prepared" |
| M8 | S231 | "but before it had been translated to other databases." |
| M9 | S231 | "Of the seven original PRESS elements, six were retained: translation of the research question; Boolean and proximity operators; subject headings; text word search;" |
| M10 | S231 | "spelling, syntax and line numbers; and limits and filters." |
| M11 | S231 | "The seventh (skilled translation of the search strategy to additional databases) was removed," |
| M12 | S231 | "as there was consensus that this should be left to the discretion of searchers." |
| M13 | S231 | "which includes the following four documents: PRESS 2015 Evidence-Based Checklist, PRESS 2015 Recommendations for Librarian Practice," |
| M14 | S231 | "PRESS 2015 Implementation Strategies, and PRESS 2015 Guideline Assessment Form." |
| M15 | S231 | "The PRESS 2015 Guideline Statement should help to guide and improve the peer review of electronic literature search strategies." |
| K1 | S225 | "Are the search concepts clear?" |
| K2 | S225 | "Are the search concepts too narrow or too broad?" |
| K3 | S225 | "Is the use of nesting with brackets appropriate and effective for the search?" |
| K4 | S225 | "Could precision be improved by using proximity operators (eg, adjacent, near, within) or phrase searching instead of AND?" |
| K5 | S225 | "Is the width of proximity operators suitable (eg, might adj5 pick up more variants than adj2)?" |
| K6 | S225 | "Are the subject headings relevant?" |
| K7 | S225 | "Are any subject headings too broad or too narrow?" |
| K8 | S225 | "Are subject headings exploded where necessary and vice versa?" |
| K9 | S225 | "Are major headings (“starring” or restrict to focus) used? If so, is there adequate justification?" |
| K10 | S225 | "Are subheadings missing?" |
| K11 | S225 | "Are subheadings attached to subject headings? (Floating subheadings may be preferred.)" |
| K12 | S225 | "Are floating subheadings relevant and used appropriately?" |
| K13 | S225 | "Does the search include all synonyms or antonyms (eg, opposites)?" |
| K14 | S225 | "Is the truncation too broad or too narrow?" |
| K15 | S225 | "Are acronyms or abbreviations used appropriately? Do they capture irrelevant material? Are the full terms also included?" |
| K16 | S225 | "Are the keywords specific enough or too broad? Are too many or too few keywords used? Are stop words used?" |
| K17 | S225 | "Have the appropriate fields been searched; for example, is the choice of the text word fields (.tw.) or all fields (.af.) appropriate?" |
| K18 | S225 | "Are there any other fields to be included" |
| K19 | S225 | "or excluded (database specific)?" |
| K20 | S225 | "Are all limits and filters used appropriately and are they relevant for the database?" |
| K21 | S225 | "Are any potentially helpful limits or filters missing? Are the limits or filters too broad or too narrow?" |
| K22 | S225 | "Can any limits or filters be added or taken away?" |

## Element names compared

The six retained elements and the removed seventh, as each route names them. The S231 and S225 cells are
substrings of their captures (the controls check both columns); the S223 cells are pointers to the round-96 entry's
located quotes, whose two-column capture breaks these phrases across lines.

| element | S231 (statement abstract) | S225 (reprint heading) | S223 (round-96 entry) |
|---|---|---|---|
| 1 | translation of the research question | 1. Translation of the research question | L20-L21 |
| 2 | Boolean and proximity operators | 2. Boolean and proximity operators (these vary based on search service) | L21 |
| 3 | subject headings | 3. Subject headings (database specific) | L21-L22 |
| 4 | text word search | 4. Text word searching (free text) | L22 |
| 5 | spelling, syntax and line numbers | 5. Spelling, syntax, and line numbers | L22-L23 |
| 6 | limits and filters | 6. Limits and filters | L22 |
| 7 (removed) | skilled translation of the search strategy to additional databases | (not in the checklist) | L26-L27 |

What the comparison shows: S231 and S225 agree on the six elements and their order; they differ in form (S225
numbers its headings, adds a parenthesis to elements 2, 3 and 4, writes "Text word searching" for "text word
search" and puts a serial comma in element 5). S223 names the same six in a different grouping ("limits and
filters, syntax and line numbers; and spelling", round-96 L22-L23), so S223's grouping is not the statement's.
S231 is the first route the lane holds that gives the seventh element's own name; S223 calls it "the element
related to translation of the search for other databases" (round-96 L26-L27).

## Decision table

| Situation | Do | Never | Warrant | Lane |
|---|---|---|---|---|
| Citing PRESS 2015 | DO NOT cite the PRESS 2015 Guideline Statement as the guideline, and name which of its four documents is meant (the Evidence-Based Checklist, the Recommendations for Librarian Practice, the Implementation Strategies or the Guideline Assessment Form) | cite the checklist as if it were the whole guideline | M1, M13, M14, M15 (S231) | the round-97 entry's questions are from the Evidence-Based Checklist only, through a reprint; the other three documents are named here and not held |
| Saying what evidence stands behind the elements | DO NOT say that the statement's systematic review found no new search elements to add and no evidence refuting any of the existing elements, and that its results suggested structured PRESS could identify search errors and improve the selection of search terms | say that the abstract reports evidence for each question; it speaks of elements | M3, M4, M5, M6 (S231) | the lane cites element-level evidence only; a question's own evidence would need the statement's body or the E&E, which are not held |
| Timing a peer review | DO NOT schedule the review after the MEDLINE search has been prepared and before it is translated to other databases, and report this as what most respondents to a survey of experts felt | report the timing as a finding of the systematic review | M3, M7, M8 (S231) | the round-96 entry holds the same timing from S223; S231 adds that it comes from the survey of experts, an opinion source |
| Deciding which elements a reviewer checks | DO NOT check the six retained elements: translation of the research question; Boolean and proximity operators; subject headings; text word search; spelling, syntax and line numbers; limits and filters | treat skilled translation of the search strategy to additional databases as a PRESS 2015 element | M9, M10, M11 (S231) | `## Element names compared` above; the lane uses S231's wording for element names and S225's for questions |
| Reviewing a strategy's translation to other databases | DO NOT leave it to the discretion of the searcher, as the consensus forum did | (none stated by the sources) | M11, M12 (S231) | the lane's searches are GNU grep expressions over its own capture store; it has no second database to translate into |
| Checking the search concepts | DO NOT ask whether the search concepts are clear and whether they are too narrow or too broad | (none stated by the sources) | K1, K2 (S225) | chousa frames the question first (SKILL.md question framing); a concept that is too broad shows in a `## Searches` row as a large `hits` count |
| Checking operators in depth | DO NOT ask whether nesting with brackets is appropriate, whether proximity operators or phrase searching would improve precision over AND, and whether a proximity width is suitable | (none stated by the sources) | K3, K4, K5 (S225) | the lane's `regex` rows have alternation and grouping but no proximity operator; a phrase is one `fixed` expression |
| Checking subject headings in depth | DO NOT ask whether subject headings are relevant, too broad or too narrow, exploded where necessary, whether major headings are justified, and whether subheadings are missing, attached or floating and used appropriately | (none stated by the sources) | K6, K7, K8, K9, K10, K11, K12 (S225) | does not apply to the lane's own searches, which have no subject-heading index (round-97 entry, subject-headings row) |
| Checking free-text words in depth | DO NOT ask whether synonyms or antonyms are included, whether truncation is too broad or too narrow, whether acronyms or abbreviations are used appropriately with their full terms, whether keywords are specific enough and whether stop words are used, and whether the fields searched are the appropriate ones | (none stated by the sources) | K13, K14, K15, K16, K17, K18, K19 (S225) | a synonym or an acronym's full term is a second row or an alternation in a `regex` row; the lane's only field is the whole text of each capture |
| Checking limits and filters in depth | DO NOT ask whether limits and filters are relevant for the database, whether helpful ones are missing, whether they are too broad or too narrow, and whether any can be added or taken away | (none stated by the sources) | K20, K21, K22 (S225) | the lane's only limit is a row's `where` glob (round-97 entry, limits row) |

## As run

Every search in `## Searches` ran on 2026-11-09 against the lane's committed capture store at revision
`98b8177c1e8b39cdf1167928e4f5d609f6fa81b6` (the round-97 landing, round 98's base, before S231 was captured),
materialised read-only with `git archive 98b8177c1e8b39cdf1167928e4f5d609f6fa81b6 corpus/captures | tar -x -C <scratch>`
and searched from `<scratch>` with GNU grep 3.12 (`/usr/bin/grep`):

    /usr/bin/grep -l -F -e '<expression>' corpus/captures/*.txt | LC_ALL=C sort        # engine fixed

`python3 -B tools/search-rerun.py verify corpus/knowledge/press-2015-statement-questions-r98.md --root .` re-runs each
one at `98b8177c` and over the current tree (where Q1-Q3 now find S231's capture: `tree=CHANGED`, not a finding
without `--strict`).

## Searches

| id | engine | where | expression | rev | searched | hits | hit_set |
|---|---|---|---|---|---|---|---|
| Q1 | fixed | corpus/captures/*.txt | `Guideline Assessment Form` | 98b8177c1e8b39cdf1167928e4f5d609f6fa81b6 | 2026-11-09 | 0 | - |
| Q2 | fixed | corpus/captures/*.txt | `Recommendations for Librarian Practice` | 98b8177c1e8b39cdf1167928e4f5d609f6fa81b6 | 2026-11-09 | 0 | - |
| Q3 | fixed | corpus/captures/*.txt | `skilled translation` | 98b8177c1e8b39cdf1167928e4f5d609f6fa81b6 | 2026-11-09 | 0 | - |
| Q4 | fixed | corpus/captures/*.txt | `consensus development forum` | 98b8177c1e8b39cdf1167928e4f5d609f6fa81b6 | 2026-11-09 | 1 | corpus/captures/e94691f583d644da14661ec1.txt |
| Q5 | fixed | corpus/captures/*.txt | `Are the search concepts clear` | 98b8177c1e8b39cdf1167928e4f5d609f6fa81b6 | 2026-11-09 | 2 | corpus/captures/347c55ba9be9d63afe17986e.txt, corpus/captures/80a844fe287a1a26d4280251.txt |

## Named limits

- S231 is the statement's abstract, not its body. The statement's text, the CADTH E&E and Table 9, and the CADTH
  report 477 appendices answered http 403 (S227, S228; round-96/97 attempts); PubMed (S229) and NCBI Bookshelf
  (S230) answered challenge pages. Nothing here says what the statement's body says about a single question.
- S231 is read through Europe PMC's index record (MEDLINE source), not the publisher's page; the lane takes the
  record's `abstractText` as the published abstract. Its `title`, `authorString`, `doi` and `pageInfo` fields agree
  with S225's "Derived from" citation (J Clin Epidemiol 2016;75:40-46, doi 10.1016/j.jclinepi.2016.01.021).
- The questions are S225's wording, a reprint (tier B); where S225 and S226 differ (round-97 entry), neither is
  taken as the guideline's.
- "36 of 36" counts S225 lines between the checklist heading and "Derived from:" that contain a question mark; a
  line is quoted when its whitespace-collapsed text equals one S225 quote or consecutive S225 quotes of one entry
  joined by one space. It counts lines, not questions (lines 64, 65 and 78 carry two or three questions each;
  lines 66-67 carry one question). The controls recompute it from the two entries' `## Located quotes` tables.
- The Never cells say "(none stated by the sources)" wherever no quote states a prohibition; the Do cells
  paraphrase their quotes and are checked by the controls only for naming quotes that exist.
- The *lane* column's statements about the lane's searches and tools describe this round's revision.

## Gate records

GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=10 quote="PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement."
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=24 quote="To develop an evidence-based guideline for Peer Review of Electronic Search Strategies (PRESS) for systematic reviews (SRs), health technology assessments, and other evidence syntheses."
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=12 quote="An SR, Web-based survey of experts, and consensus development forum were undertaken"
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=16 quote="No new search elements were identified for addition to the existing (2008-2010) PRESS 2015 Evidence-Based Checklist,"
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=10 quote="and there was no evidence refuting any of its elements."
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=16 quote="Results suggested that structured PRESS could identify search errors and improve the selection of search terms."
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=16 quote="Most respondents felt that peer review should be undertaken after the MEDLINE search had been prepared"
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=9 quote="but before it had been translated to other databases."
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=23 quote="Of the seven original PRESS elements, six were retained: translation of the research question; Boolean and proximity operators; subject headings; text word search;"
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=9 quote="spelling, syntax and line numbers; and limits and filters."
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=13 quote="The seventh (skilled translation of the search strategy to additional databases) was removed,"
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=14 quote="as there was consensus that this should be left to the discretion of searchers."
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=16 quote="which includes the following four documents: PRESS 2015 Evidence-Based Checklist, PRESS 2015 Recommendations for Librarian Practice,"
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=10 quote="PRESS 2015 Implementation Strategies, and PRESS 2015 Guideline Assessment Form."
GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=19 quote="The PRESS 2015 Guideline Statement should help to guide and improve the peer review of electronic literature search strategies."
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=5 quote="Are the search concepts clear?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=9 quote="Are the search concepts too narrow or too broad?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=13 quote="Is the use of nesting with brackets appropriate and effective for the search?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=18 quote="Could precision be improved by using proximity operators (eg, adjacent, near, within) or phrase searching instead of AND?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=16 quote="Is the width of proximity operators suitable (eg, might adj5 pick up more variants than adj2)?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=5 quote="Are the subject headings relevant?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=9 quote="Are any subject headings too broad or too narrow?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=9 quote="Are subject headings exploded where necessary and vice versa?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=15 quote="Are major headings (“starring” or restrict to focus) used? If so, is there adequate justification?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=3 quote="Are subheadings missing?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=11 quote="Are subheadings attached to subject headings? (Floating subheadings may be preferred.)"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=7 quote="Are floating subheadings relevant and used appropriately?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=10 quote="Does the search include all synonyms or antonyms (eg, opposites)?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=8 quote="Is the truncation too broad or too narrow?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=17 quote="Are acronyms or abbreviations used appropriately? Do they capture irrelevant material? Are the full terms also included?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=20 quote="Are the keywords specific enough or too broad? Are too many or too few keywords used? Are stop words used?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=22 quote="Have the appropriate fields been searched; for example, is the choice of the text word fields (.tw.) or all fields (.af.) appropriate?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=8 quote="Are there any other fields to be included"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=4 quote="or excluded (database specific)?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=14 quote="Are all limits and filters used appropriately and are they relevant for the database?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=18 quote="Are any potentially helpful limits or filters missing? Are the limits or filters too broad or too narrow?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=10 quote="Can any limits or filters be added or taken away?"
GATE-RECORD S228 url=https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Report%20477_PRESS_Peer%20Review%20of%20Electronic%20Search%20Strategies_Appendices.pdf fetched=2026-11-09T02:47:35Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none
