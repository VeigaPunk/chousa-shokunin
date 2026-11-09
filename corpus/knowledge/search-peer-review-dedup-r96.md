# Search peer review and deduplication — what a search report states about who checked the strategy and how duplicates were removed (round 96)

source: S224, S223
verified-at: 2026-11-09 (round 96; capture `1a8c36c4c24444967bd9c3ce` — the PRISMA-S publisher PDF, re-opened this round as S224 with identical bytes — and capture `e94691f583d644da14661ec1`, the PRESS 2015 authors' abstract, opened this round as S223)
recheck: on-release

## What this entry governs

The round-95 entry (`search-rerun-record-r95.md`, S222) holds what PRISMA-S says a search report must file so a
search can be re-run; it names PRISMA-S item 14 (search peer review) and item 16 (deduplication) as not held
(its named limits, and `corpus/README.md:1445`). This entry holds those two items, plus what the PRESS 2015
update's authors say their guideline kept, dropped and recommends about timing. Citation *searching* and its
deduplication step are a different method, held in `citation-searching-tarcis-r81.md` (S203, S204).

What the lane held before this round, measured by the `## Searches` record below at the base revision `bbf64970`:
the PRESS guideline is named in two captures (Q1, Q2: S222's PRISMA-S PDF and S120's Cochrane chapter 4), three
captures mention peer review of a search (Q3), four mention deduplication (Q4) and one reports that duplicates
were removed (Q5); no capture holds the PRESS authors' timing sentence (Q6, 0 hits) or a sentence on translating
a search into other databases (Q8, 0 hits). `重複` (Q7) occurs in three Japanese captures, none of them a search
reporting standard (S098, S107, S112). The column marked *lane* is this lane's reading; it is not what PRISMA-S
or PRESS says.

Text forms: both captures are `pdftotext -layout` of two-column pages, so every quote below is located within one
column line. Consecutive fragments (L4-L6, L7-L8, L9-L10, L11-L13, L14-L16, L17-L18, L19-L23, L24-L25,
L26-L29) are read as one sentence from the text form's line order, not located as one string.

## Located quotes

| qid | source | quote |
|---|---|---|
| L1 | S224 | "Describe any search peer review process." |
| L2 | S224 | "this refers to the peer review of search strategies prior to executing the search." |
| L3 | S224 | "to identify errors, missing keywords or subject headings, and other issues within a search strategy." |
| L4 | S224 | "should strongly consider having the search strategy peer" |
| L5 | S224 | "reviewed by an experienced searcher, information" |
| L6 | S224 | "specialist, or librarian [52, 131]." |
| L7 | S224 | "be conducted generally with publication of a protocol, for" |
| L8 | S224 | "example, this item is designed to document search-specific" |
| L9 | S224 | "Describe the processes and any software used to deduplicate records" |
| L10 | S224 | "from multiple database searches and other information sources." |
| L11 | S224 | "should describe and cite any software or technique used," |
| L12 | S224 | "when applicable. If duplicates were removed manually," |
| L13 | S224 | "authors should include a description." |
| L14 | S224 | "which method is used enables readers to evaluate the" |
| L15 | S224 | "process and understand to what extent these techniques" |
| L16 | S224 | "may have removed false positive duplicates [138]. Authors" |
| L17 | S224 | "section. The total number of references after deduplication" |
| L18 | S224 | "should be reported in the PRISMA flow diagram [34]." |
| L19 | S223 | "quality. Six existing PRESS elements were retained and their" |
| L20 | S223 | "peer review will be briefly described: translation of the" |
| L21 | S223 | "research question; Boolean and proximity operators; subject" |
| L22 | S223 | "headings; text word search; limits and filters, syntax and line" |
| L23 | S223 | "numbers; and spelling. No new elements were identified for" |
| L24 | S223 | "that peer review should occur after the MEDLINE search" |
| L25 | S223 | "has been developed but before other database searches are" |
| L26 | S223 | "developed. The element related to translation of the search" |
| L27 | S223 | "for other databases was removed, with the recommendation" |
| L28 | S223 | "that translations be peer reviewed at the discretion of the" |
| L29 | S223 | "search developer." |
| L30 | S223 | "that peer review checklists were effective at improving search" |

## Decision table

| Situation | Do | Never | Warrant | Lane |
|---|---|---|---|---|
| Reporting whether a search strategy was peer reviewed | describe any search peer review process, and document the review of this search specifically | let a protocol's general review stand in for the review of the search strategy | L1, L7, L8 (S224, item 14) | a chousa search record says which seat or person reviewed the expression before it ran, or that nobody did |
| Choosing who reviews a strategy | strongly consider having the search strategy peer reviewed by an experienced searcher, information specialist or librarian | present peer review as a PRISMA-S requirement: the item asks to describe it, and the explanation says "should strongly consider" | L4, L5, L6 (S224, ITEM 14) | in this lane the reviewer is a seat that did not write the expression (a reviewer or critic item of the round's wave) |
| Timing a peer review | review the search strategy prior to executing the search; under PRESS 2015, after the MEDLINE search has been developed and before the other database searches are developed | review only after the results are in, or review each database's translation by default | L2 (S224, Box 1), L24, L25 (S223) | for a local record: review before the run whose `rev` the record files; a second store searched with a translated expression is the analogue of "other databases" (the lane's analogy) |
| Deciding what a reviewer checks | check the six PRESS elements: translation of the research question; Boolean and proximity operators; subject headings; text word search; limits and filters, syntax and line numbers; spelling | add translation of the search into other databases as a required element: PRESS 2015 removed it and left it to the search developer | L19, L20, L21, L22, L23 (S223); L26, L27, L28, L29 (S223) | the grouping "limits and filters, syntax and line numbers" is the abstract's punctuation; the guideline's own checklist wording was not opened (403), so the split into six named elements is read from this abstract only |
| Saying what a review is for | use peer review to identify errors, missing keywords or subject headings, and other issues within a search strategy | claim a reviewed strategy is complete or has high recall | L3 (S224, Box 1); L30 (S223) | the abstract reports that checklists improved search quality in several studies; the lane holds no measurement of that and claims none |
| Reporting deduplication | describe the processes and any software used to deduplicate records from multiple database searches and other information sources; cite the software or technique, and describe any manual removal | remove duplicates without saying how | L9, L10 (S224, item 16); L11, L12, L13 (S224, ITEM 16) | `tools/search-rerun.py` counts files per expression and never merges hit sets across searches, so a chousa record that reports a union must state how the union was formed (a sorted set of paths is the lane's method) |
| Explaining why the method is reported | report the method so readers can evaluate the process and understand to what extent these techniques may have removed false positive duplicates | treat deduplication as lossless | L14, L15, L16 (S224, ITEM 16) | for paths, identity is byte equality, so a false positive cannot occur; for records from external databases it can, and the lane holds no deduplication method for them |
| Reporting the count after deduplication | report the total number of references after deduplication in the PRISMA flow diagram | report only per-source counts and leave the deduplicated total implicit | L17, L18 (S224, ITEM 16) | per-source counts are the round-95 entry's row 4 (PRISMA-S item 15); this row adds the after-deduplication total |

## As run

Every search in `## Searches` ran on 2026-11-09 against the lane's committed capture store at revision `bbf64970b6c73ca64bcc5f6de2f33b0550459813`
(the round-95 closure tip, round 96's base), materialised read-only with
`git archive bbf64970b6c73ca64bcc5f6de2f33b0550459813 corpus/captures | tar -x -C <scratch>` and searched from `<scratch>` with GNU grep 3.12
(`/usr/bin/grep`):

    /usr/bin/grep -l -F -e '<expression>' corpus/captures/*.txt | LC_ALL=C sort        # engine fixed
    /usr/bin/grep -l -P -e '<expression>' corpus/captures/*.txt | LC_ALL=C sort        # engine regex

In that table a `|` inside an expression cell is written `\|`; the bytes run are the cell with every `\|` read
as `|`. `python3 -B tools/search-rerun.py verify corpus/knowledge/search-peer-review-dedup-r96.md --root .`
re-runs each one at `bbf64970` and over the current tree.

## Searches

| id | engine | where | expression | rev | searched | hits | hit_set |
|---|---|---|---|---|---|---|---|
| Q1 | fixed | corpus/captures/*.txt | `Peer Review of Electronic Search Strategies` | bbf64970b6c73ca64bcc5f6de2f33b0550459813 | 2026-11-09 | 2 | corpus/captures/1a8c36c4c24444967bd9c3ce.txt, corpus/captures/c9d1e74c3ac8d9eb332c9770.txt |
| Q2 | fixed | corpus/captures/*.txt | `PRESS Checklist` | bbf64970b6c73ca64bcc5f6de2f33b0550459813 | 2026-11-09 | 2 | corpus/captures/1a8c36c4c24444967bd9c3ce.txt, corpus/captures/c9d1e74c3ac8d9eb332c9770.txt |
| Q3 | regex | corpus/captures/*.txt | `[Pp]eer[- ]review(ed\|ing)? (of )?(the \|electronic )?search` | bbf64970b6c73ca64bcc5f6de2f33b0550459813 | 2026-11-09 | 3 | corpus/captures/1a8c36c4c24444967bd9c3ce.txt, corpus/captures/c52a1f15884a78028febcf43.txt, corpus/captures/c9d1e74c3ac8d9eb332c9770.txt |
| Q4 | fixed | corpus/captures/*.txt | `deduplicat` | bbf64970b6c73ca64bcc5f6de2f33b0550459813 | 2026-11-09 | 4 | sha256:075e02644f9c115cab201076e652ae646fc0fe85331c6f79943cc1e47aff3500 |
| Q5 | regex | corpus/captures/*.txt | `[Dd]uplicates? (were\|was) removed` | bbf64970b6c73ca64bcc5f6de2f33b0550459813 | 2026-11-09 | 1 | corpus/captures/1a8c36c4c24444967bd9c3ce.txt |
| Q6 | fixed | corpus/captures/*.txt | `MEDLINE search has been developed` | bbf64970b6c73ca64bcc5f6de2f33b0550459813 | 2026-11-09 | 0 | - |
| Q7 | fixed | corpus/captures/*.txt | `重複` | bbf64970b6c73ca64bcc5f6de2f33b0550459813 | 2026-11-09 | 3 | corpus/captures/34fcefc159bf2ebbd1e09540.txt, corpus/captures/7194acc65a18f6555e4b8893.txt, corpus/captures/fea98dc5a5a486c988dd415c.txt |
| Q8 | regex | corpus/captures/*.txt | `translat(ed\|ion) (of the search\|into other databases)` | bbf64970b6c73ca64bcc5f6de2f33b0550459813 | 2026-11-09 | 0 | - |

## Named limits

- PRESS is held through its authors' abstract (S223, tier B); the guideline statement (J Clin Epidemiol
  2016;75:40-46) and the Explanation and Elaboration report answered http 403 this round and were not read, so
  the checklist's own element wording, the assessment form and the evidence for each element are not held.
- PRISMA-S asks a report to *describe* peer review and deduplication; it does not require either to be done.
  "Should strongly consider" (L4) is the strongest wording held.
- The searches are over the lane's own capture store, not a bibliographic database; Q7's hits show only that the
  word occurs, not what it says.
- The re-run over the landing tree (this round's S223 capture added) reports `TREE_CHANGED` for Q1, Q3 and Q8 and
  not for Q6, although S223 holds the timing sentence: it wraps between two column lines ("…after the MEDLINE
  search" / "has been developed…"), and matching is per line. A 0-hit row is an absence of that line form in the
  store, not an absence of the statement.
- The *lane* column's statements about `tools/search-rerun.py` describe the tool at this round's revision.

## Gate records

GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=6 quote="Describe any search peer review process."
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=14 quote="this refers to the peer review of search strategies prior to executing the search."
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=15 quote="to identify errors, missing keywords or subject headings, and other issues within a search strategy."
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=8 quote="should strongly consider having the search strategy peer"
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=6 quote="reviewed by an experienced searcher, information"
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=5 quote="specialist, or librarian [52, 131]."
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=9 quote="be conducted generally with publication of a protocol, for"
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=8 quote="example, this item is designed to document search-specific"
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=10 quote="Describe the processes and any software used to deduplicate records"
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=8 quote="from multiple database searches and other information sources."
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=9 quote="should describe and cite any software or technique used,"
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=7 quote="when applicable. If duplicates were removed manually,"
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=5 quote="authors should include a description."
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=9 quote="which method is used enables readers to evaluate the"
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=8 quote="process and understand to what extent these techniques"
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=8 quote="may have removed false positive duplicates [138]. Authors"
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=8 quote="section. The total number of references after deduplication"
GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=9 quote="should be reported in the PRISMA flow diagram [34]."
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=9 quote="quality. Six existing PRESS elements were retained and their"
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=9 quote="peer review will be briefly described: translation of the"
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=7 quote="research question; Boolean and proximity operators; subject"
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=10 quote="headings; text word search; limits and filters, syntax and line"
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=9 quote="numbers; and spelling. No new elements were identified for"
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=9 quote="that peer review should occur after the MEDLINE search"
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=9 quote="has been developed but before other database searches are"
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=9 quote="developed. The element related to translation of the search"
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=8 quote="for other databases was removed, with the recommendation"
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=10 quote="that translations be peer reviewed at the discretion of the"
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=2 quote="search developer."
GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=9 quote="that peer review checklists were effective at improving search"
GATE-RECORD S223 url=https://www.cda-amc.ca/sites/default/files/pdf/CP0015_PRESS_Update_Report_2016.pdf fetched=2026-11-09T00:35:47Z tier=B decision=reject capture=none curl_rc=22 http=403 words=0 quote=none
