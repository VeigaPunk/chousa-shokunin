# Search re-run record — what a search record must file so the search can be re-run and its count compared (round 95)

source: S222
verified-at: 2026-11-08 (round 95; capture `1a8c36c4c24444967bd9c3ce`, the JMLA publisher PDF of PRISMA-S, opened this round)
recheck: on-release

## What this entry governs

The lane holds how a search is reported for transparency (`search-transparency-reporting-r84.md`, PRISMA 2020
items 6-8 and 16a through `S214`) and how a search log is kept as a working document (`search-log-method-r39.md`,
`S078`). Neither holds PRISMA-S's own checklist text: at the base revision `7b237358` no `.txt` capture contains
the item-15 sentence `Document the total number of records identified` (`/usr/bin/grep -l -F` over
`corpus/captures/*.txt`, exit 1); two captures (S120's Cochrane chapter, S204's Campbell guide) cite the paper's
title only, and the DOI route the lane tried earlier returned a `Client Challenge` page
(`corpus/lessons/round-47.md:251-253`). The coverage map names the gap this entry works: the sweep re-run is a
glob/existence check over the named locations, never the recorded command (`corpus/README.md:398-399`; the
pointer `corpus/README.md:390-391` at line 1108 is stale). The rows below keep only what PRISMA-S states a search
report must file about each
search, and what it says a re-run that finds a different number means. The column marked *lane* is this lane's
reading for a local, committed corpus; it is not a PRISMA-S requirement.

Text form: the capture's `.txt` is `pdftotext -layout` of a two-column page, so a sentence that wraps inside one
column is interleaved with the other column's line. Q6-Q9 are therefore single column-line fragments, each
located on its own; that Q7-Q9 belong to one ITEM 15 sentence is read from the PDF's layout, not located.

## Located quotes

| qid | source | quote |
|---|---|---|
| Q1 | S222 | "Include the search strategies for each database and information source, copied and pasted exactly as run." |
| Q2 | S222 | "For each search strategy, provide the date when the last search occurred." |
| Q3 | S222 | "Document the total number of records identified from each database and other information sources." |
| Q4 | S222 | "Report the methods used to update the search(es) (e.g., rerunning searches, email alerts)." |
| Q5 | S222 | "Specify that no limits were used, or describe any limits or restrictions" |
| Q6 | S222 | "to view the same "slice" of the database that the original" |
| Q7 | S222 | "If a reader tries to duplicate a search from" |
| Q8 | S222 | "drastically different number of results than reported in the" |
| Q9 | S222 | "published search [22] or major changes to a database, both" |

## Decision table

| Situation | Do | Never | Warrant | Lane |
|---|---|---|---|---|
| Filing a search's expression | file the strategy for each database and information source copied and pasted exactly as run | file a paraphrase, a summary or one example strategy in place of what was run | Q1 (S222, item 8) | the record's `expression` cell holds the bytes the engine ran; `tools/search-rerun.py` re-executes that cell |
| Filing where a search looked | state that no limits were used, or describe the limits and restrictions applied | leave the searched scope implicit | Q5 (S222, item 9) | the `where` glob is the limit; a different glob is a different search (`rerun-controls-r95.py` f8) |
| Filing when a search ran | give, for each strategy, the date the last search occurred | give one date for several strategies run on different days | Q2 (S222, item 13) | the record files the date and the committed revision; for a corpus under version control the revision is the same "slice" Q6 describes |
| Filing what a search found | document the total number of records identified from each database and other information source | report only the deduplicated total, losing the per-source count | Q3 (S222, item 15) | the record files the count and the set of matching files, so a same-count different-set re-run is still caught |
| Re-running a recorded search | expect nearly the same results when the search is duplicated over the original timeframe | read a drastically different count as noise | Q7, Q8 (S222, ITEM 15) | over a committed corpus at the recorded revision the expectation is exact, not "nearly": any difference is a finding |
| Reading a different re-run count | treat it as indicating an error in the reported search or a major change to the database | assume one cause without separating them | Q9, Q8 (S222, ITEM 15) | re-run twice: at the recorded revision (a difference is the record's fault, `COUNT_DRIFT`/`SET_DRIFT`) and over the current tree (a difference is a corpus change, `TREE_CHANGED`) |
| Updating a search | report the method used to update it, rerunning searches included | update silently and keep the old date | Q4 (S222, item 12) | a re-run over the tree that reports `TREE_CHANGED` is the cue to file a new row with the new revision, date and count |

## Named limits

- PRISMA-S speaks of bibliographic databases and expects "nearly" the same results; exactness and the two-revision
  split are the lane's reading for a committed local corpus, not the standard's.
- Matching the recorded count and set proves the record agrees with what its expression finds; it does not prove
  the expression was the right one to run (recall, search quality and peer review — PRISMA-S item 14 — are not
  measured).
- Q7-Q9 are three located fragments of one sentence (two-column text form); their joining is read from the layout.

## Gate records

GATE-RECORD S222 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-08T22:51:39Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=16 quote="Include the search strategies for each database and information source, copied and pasted exactly as run."
GATE-RECORD S222 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-08T22:51:39Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=12 quote="For each search strategy, provide the date when the last search occurred."
GATE-RECORD S222 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-08T22:51:39Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=14 quote="Document the total number of records identified from each database and other information sources."
GATE-RECORD S222 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-08T22:51:39Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=13 quote="Report the methods used to update the search(es) (e.g., rerunning searches, email alerts)."
GATE-RECORD S222 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-08T22:51:39Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=12 quote="Specify that no limits were used, or describe any limits or restrictions"
GATE-RECORD S222 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-08T22:51:39Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=11 quote="to view the same "slice" of the database that the original"
GATE-RECORD S222 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-08T22:51:39Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=9 quote="If a reader tries to duplicate a search from"
GATE-RECORD S222 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-08T22:51:39Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=9 quote="drastically different number of results than reported in the"
GATE-RECORD S222 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-08T22:51:39Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=10 quote="published search [22] or major changes to a database, both"
