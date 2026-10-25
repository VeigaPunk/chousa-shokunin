# ExecNoPipe — S078 row cell split

Seat: ExecNoPipe (leaf). Axes: operability (row parses as a registry record), calibration (raw-pipe check, no retune), depth (header alignment and the one non-row S078 hit). No production file, git index, or sibling tree was written. No fetch. No descendant spawned.

Verdict: the column-zero S078 row of `corpus/SOURCES.md` splits into **11** cells. No cell contains a raw pipe (`|`, U+007C).

Cell count: **11**

## What was measured

File: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`
HEAD (clean for this path; `git status --porcelain -- corpus/SOURCES.md` printed nothing): `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`

The Registry section is lines 7–89. The only column-zero `| S078 |` row is line 88. The other `S078` hit is line 250, search-log prose, `pipe_count=0`, not a table row.

A raw pipe here is U+007C inside a cell after the lane's escape-preserving split (`tools/research-gate.sh` `metadata_registry_load`, lines 3346–3361). That split unescapes `\|` into a pipe inside the cell. Delimiter pipes are not cell content. The census reader (`scripts/sources-census.sh` `row_pass`, `gawk -F'|'`) does not honor escapes, so agreement of the two counts is the calibration check: an escaped pipe before a bound column would shift the naive field index (round-27 R27-M15) and is absent on this row.

## Command output (verbatim)

```
ROW_LINE=88
ROW_BYTES=720
RAW_PIPE_CHARS=12
ESCAPED_PIPE_SEQS=0
CELL_COUNT=11
RAW_PIPE_CELLS=0
C1=S078
C3=paper
C4=A
C8=mined
C9=2026-10-24
C10=365d
C11=corpus/knowledge/search-log-method-r39.md
CENSUS_NF=13
CENSUS_FIELDS=11
CENSUS_ID= S078 
EXIT=0
```

`RAW_PIPE_CHARS=12` is the outer pair plus the ten separators of an 11-cell row, not an interior pipe. `CENSUS_NF=13` is the census convention (empty edge fields); content fields are `NF-2` = 11. `CENSUS_ID` is untrimmed `$2`; the gate trim yields `S078`.

Independent Python replay of the same gate split, same file:

```
S078_LINE_HITS=[88, 250]
--- line 88 len=720 start='| S078 | Bra' pipe_count=12 escaped_pipe_count=0 ---
--- line 250 len=1045 start='- Round 43 (' pipe_count=0 escaped_pipe_count=0 ---
REGISTRY_START=7 REGISTRY_END_EXCLUSIVE=90
HEADER_CELL_COUNT=11
COLUMN_ZERO_S078_ROWS=[88]
ROW_LINE=88
CELL_COUNT=11
RAW_PIPE_CELLS=0
LINE_PIPE_COUNT=12
LINE_ESCAPED_PIPE_COUNT=0
CENSUS_NF=13
CENSUS_FIELDS_NF_MINUS_2=11
NAIVE_INNER_COUNT=11
NAIVE_INNER_WITH_PIPE=0
```

Header (line 9), also 11 cells, so the row indexes match the declared schema: id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by.

## Cells (trimmed, gate split)

| n | header | raw pipe | text |
|---|---|---|---|
| 1 | id | no | S078 |
| 2 | source | no | Bramer, de Jonge, Rethlefsen, Mast, Kleijnen, A systematic approach to searching — Europe PMC full-text XML https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML (capture sha256 833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d; not fetched this round) |
| 3 | kind | no | paper |
| 4 | tier | no | A |
| 5 | scope | no | how a search log is kept as a working document, distinct from a checklist of fields a log must carry |
| 6 | anchor | no | section 6 of the Europe PMC full-text XML, byte offset 17383 of the committed capture |
| 7 | teaches | no | Design and keep the complete search strategies in a log document rather than in the database, so the steps taken stay accountable and reproducible |
| 8 | status | no | mined |
| 9 | opened | no | 2026-10-24 |
| 10 | recheck | no | 365d |
| 11 | used-by | no | corpus/knowledge/search-log-method-r39.md |

The em dash in cell 2 is U+2014 (UTF-8 `e2 80 94`), not U+007C. `cat -A` renders it as `M-bM-^@M-^T`. It does not change the pipe count.

## Remaining risks

- This seat did not run `sources-census.sh`. Field-width agreement on S078 does not speak for the other 77 rows or for E03/E04.
- "Raw pipe" is U+007C after the gate split. `ESCAPED_PIPE_SEQS=0` is the stronger fact that makes the census split and the gate split agree. A different definition (for example, rejecting the em dash) was not the assigned check.
- Line 250 names S078 and is not a second registry row. A grep that does not require a column-zero `| S078 |` will over-count.

## Blockers

None.
