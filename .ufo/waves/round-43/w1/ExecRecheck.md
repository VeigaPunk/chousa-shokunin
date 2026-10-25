# ExecRecheck — round 43, wave 1 (executor)

## Assigned check

Confirm the S078 recheck cell is exactly `365d`, not a prose sentence. Quote the cell.

Axes: operability (the cell is the census `recheck` field and parses), calibration (exact token, not a sentence prefix), depth (the staged prose sentence is a different cell and did not land here).

## Verdict

**Confirmed.** The S078 recheck cell is exactly `365d`.

Quoted cell: `365d`

It is four characters, has no space, and is not a sentence. The prose sentence that begins `365d — re-open the Europe PMC...` is the staged S120 cell in the read-only campaign append file. It is not this cell.

## Where the cell is

Registry header in `corpus/SOURCES.md` (line 9):

`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`

The census splitter (`gawk -F'|'`, `scripts/sources-census.sh:580,628`) stores `recheck=trim($11)`. On a column-zero row that is the 10th data cell. S078 is that row, line 88, and it is the only column-zero `| S078 |` row. No indented pipe-row names S078.

Working tree `HEAD` is the measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. The committed blob's trimmed `$11` is the same token.

## Exact commands and output

Python column extract of the live Registry row (trimmed cells, same pipe split the census uses):

```
HEADER ['id', 'source', 'kind', 'tier', 'scope', 'anchor', 'teaches', 'status', 'opened', 'recheck', 'used-by']
N_HITS 1
---
KIND registry-row
LINE 88
NF 13
N_CELLS 11
CELL[0] 'id' = 'S078'
CELL[1] 'source' = 'Bramer, de Jonge, Rethlefsen, Mast, Kleijnen, A systematic approach to searching — Europe PMC full-text XML https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML (capture sha256 833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d; not fetched this round)'
CELL[2] 'kind' = 'paper'
CELL[3] 'tier' = 'A'
CELL[4] 'scope' = 'how a search log is kept as a working document, distinct from a checklist of fields a log must carry'
CELL[5] 'anchor' = 'section 6 of the Europe PMC full-text XML, byte offset 17383 of the committed capture'
CELL[6] 'teaches' = 'Design and keep the complete search strategies in a log document rather than in the database, so the steps taken stay accountable and reproducible'
CELL[7] 'status' = 'mined'
CELL[8] 'opened' = '2026-10-24'
CELL[9] 'recheck' = '365d'
CELL[10] 'used-by' = 'corpus/knowledge/search-log-method-r39.md'
RECHECK_CELL 365d
RECHECK_REPR '365d'
EXACT_365d True
LEN 4
HAS_SPACE False
HAS_EMDASH False
LOOKS_SENTENCE False
CENSUS_NND True
```

`gawk -F'|'` on the working tree, field index matching the census (`$11`, trim):

```
HEADER_NF=13
H2=id
H3=source
H4=kind
H5=tier
H6=scope
H7=anchor
H8=teaches
H9=status
H10=opened
H11=recheck
H12=used-by
ROW_LINE=88
NF=13
RECHECK_FIELD=$11
RECHECK=365d
RECHECK_RAW=[ 365d ]
EXACT=YES
USED_BY=corpus/knowledge/search-log-method-r39.md
GAWK_EXIT=0
```

`RECHECK_RAW=[ 365d ]` is the untrimmed pipe field: one leading space and one trailing space, the markdown padding. After `trim`, the cell is `365d`. That padding is not prose.

Committed blob at `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`:

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
COMMIT_NF=13
COMMIT_RECHECK=[365d]
COMMIT_EXACT=YES
```

Uniqueness and the knowledge-entry field (not the cell):

```
KNOWLEDGE_LINE 5
REPR 'recheck: 365d'
EXACT_FIELD True
COLUMN_ZERO_S078_ROWS [88]
OTHER_PIPE_S078_LINES []
```

Assimilation validate copy, same path under `.ufo/waves/round-43/assimilation/validate/corpus/SOURCES.md`:

```
VALIDATE_LINE 88
VALIDATE_RECHECK_REPR '365d'
VALIDATE_EXACT True
VALIDATE_N_CELLS 11
```

## Not the cell

The sentence the lesson says was stripped is still the recheck cell of staged id S120 in `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` line 48. Same 11-cell split:

```
LINE 48
ID S120
N_CELLS 11
NF 13
RECHECK_REPR '365d — re-open the Europe PMC full-text XML and confirm section 6 still reads "to register the steps taken and to make searches accountable and reproducible" (ran 2026-10-23)'
EXACT_365d False
HAS_SPACE True
LEN 174
```

That value has a space and an em dash. Census E09 accepts an ISO date, `^[0-9]+d$`, or a symbolic cadence (`scripts/sources-census.sh:663-666`). `365d — re-open ...` matches none of those. The lane cell `365d` matches `^[0-9]+d$`. This seat did not run `sources-census.sh`.

`corpus/lessons/round-43.md:51` records the strip: staged recheck prose was reduced to `365d`, and the prose is the Gate block, not a registry cell. The live cell matches that record.

`corpus/knowledge/search-log-method-r39.md:5` is `recheck: 365d`. That is the entry field, not the registry cell. It is also the cadence token, not the staged sentence. QUALITY criterion 6 allows a cadence optionally followed by a command; this entry does not use that optional tail.

## What was not checked

C1, C2, and C3 were not run. An unrun counter has not passed. No fetch. No production file was edited. No subagent was spawned.

## Remaining risks

A later copy of staged S120's recheck cell onto lane S078 would put a sentence back in `$11` and fail E09. That has not happened at `737f40b6`. The raw markdown field is ` 365d `, not the four-character token; callers that skip `trim` would not see exact `365d`. The census trims.

## Blockers

None.

Report: .ufo/waves/round-43/w1/ExecRecheck.md
