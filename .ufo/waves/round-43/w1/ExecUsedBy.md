# ExecUsedBy — S078 used-by path

Seat: ExecUsedBy (leaf). No production files edited. No fetch. No descendant.

## Axes

- Operability: the named knowledge file exists as a regular file, and the S078 `used-by` cell resolves to that path.
- Calibration: the quoted cell is column `used-by` (11th registry cell), not a neighbor, and no other column-zero registry row names the same path.
- Depth: the entry's `source:` line cites lane id S078 and does not cite `source: S118`. This seat did not re-run `c3-count.py` and does not claim C3.

## Finding

CONFIRMED. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/search-log-method-r39.md` exists and is the used-by path of S078.

Used-by cell (stripped path token, `corpus/SOURCES.md` line 88, header line 9 column `used-by`):

```
corpus/knowledge/search-log-method-r39.md
```

Raw split cell, including the one leading and one trailing markdown-table space (`USED_BY_RAW_REPR`):

```
' corpus/knowledge/search-log-method-r39.md '
```

Header cell at the same split index:

```
' used-by '
```

The path token has no extra characters. The spaces are table padding.

## Evidence (command output, verbatim)

Existence and column extraction, 2026-10-24, exit 0:

```
=== test -f ===
EXISTS=yes
=== test -L ===
SYMLINK=no
=== stat ===
SIZE=2188 MODE=644 LINKS=1 TYPE=regular file
=== wc -l ===
27 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/search-log-method-r39.md
=== header used-by column ===
HEADER_CELLS=11
HEADER=id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by
USED_BY_INDEX=10
S078_ROW_COUNT=1
ROW0_CELLS=11
ROW0_ID=S078
ROW0_USED_BY=corpus/knowledge/search-log-method-r39.md
ROW0_RAW_TAIL=|
RESOLVED=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/search-log-method-r39.md
RESOLVED_IS_ENTRY=True
ENTRY_IS_FILE=True
ENTRY_CITES_S078=True
ENTRY_CITES_S118=False
ROWS_WITH_SAME_USED_BY=S078
=== exit ===
DONE
```

`ROW0_RAW_TAIL=|` is a defective `rfind("|")` slice from that script. It is not the used-by cell. The second command is the cell quote.

Raw cell and registry line, exit 0:

```
HEADER_SPLIT_LEN=13
HEADER_COL11_REPR=' used-by '
ROW_SPLIT_LEN=13
USED_BY_RAW_REPR=' corpus/knowledge/search-log-method-r39.md '
USED_BY_STRIPPED=corpus/knowledge/search-log-method-r39.md
--- source line ---
3:source: S078 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML — section 6, byte offset 17383 of the committed capture — J Med Libr Assoc 2018;106(4):531-539, doi 10.5195/jmla.2018.283
4:verified-at: 2026-10-24
25:Located quote (12 words), access 2026-10-24, no fetch: "to register the steps taken and to make searches accountable and reproducible."
=== grep -n used-by header ===
9:| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
=== grep -n S078 row ===
88:| S078 | Bramer, de Jonge, Rethlefsen, Mast, Kleijnen, A systematic approach to searching — Europe PMC full-text XML https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML (capture sha256 833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d; not fetched this round) | paper | A | how a search log is kept as a working document, distinct from a checklist of fields a log must carry | section 6 of the Europe PMC full-text XML, byte offset 17383 of the committed capture | Design and keep the complete search strategies in a log document rather than in the database, so the steps taken stay accountable and reproducible | mined | 2026-10-24 | 365d | corpus/knowledge/search-log-method-r39.md |
```

Split index 11 is the 11th cell because a leading `|` produces an empty `parts[0]`. Header order is `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`. Zero-based content index of `used-by` is 10. Both counts agree: 11 cells, last cell is the path.

`grep -n '^| S078 |'` returned one registry row (line 88). A content search of `corpus/SOURCES.md` also shows a narrative mention of S078 at line 250 (round-43 search log). That line is not a registry row and is not a second used-by cell.

`corpus/QUALITY.md` lines 17–19 require a knowledge entry's `source:` to name an `S###` row whose status is `mined` and whose `used-by` names that entry. The S078 row status cell is `mined`. The entry opens with `source: S078 —`. The used-by cell names `corpus/knowledge/search-log-method-r39.md`.

Predicate R43-C3 in `corpus/evidence/round43/claims.md` names this same entry and lane id S078. This seat did not run `python3 corpus/evidence/round43/c3-count.py`. An unrun check has not passed. C3 is not claimed here.

## Files changed

- `.ufo/waves/round-43/w1/ExecUsedBy.md` (this report only)

## Behavior

Read-only confirmation. The knowledge file is a 2188-byte regular file, mode 644, not a symlink, 27 lines. Relative used-by path resolves to that absolute path. Only S078's column-zero registry row carries that used-by path.

## Remaining risks

- Quote-in-capture and URL match are C3's job. This seat did not open the Europe PMC capture and did not run `c3-count.py`.
- A registry row indented by 4 or more spaces would not match `^ {0,3}\|`. None was sought beyond the column-zero `grep -n '^| S078 |'` (one hit) and the 0–3 space row count (1).
- `ROW0_RAW_TAIL=|` must not be cited as the cell.

## Blockers

None.

Report: .ufo/waves/round-43/w1/ExecUsedBy.md
