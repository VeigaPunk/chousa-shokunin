# W2ExecCollision

Seat: executor. Axes: operability (run the count and the row-start test), calibration (row-start id versus a cell string), depth (document, not arithmetic). Campaign tree not edited. Collisions file not rewritten.

## Answers

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-44/assimilation/collisions` exists. Line count is **0**. It is a regular empty file (0 bytes), so the zero is not a missing trailing newline.
- A row-start `S077` does **not** exist in the staged append file `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md`.
- The string `S077` occurs once in that file, in the scope cell of row `S093`, not in the id cell.

## Collisions file

```
=== test -e / test -f / test -s ===
exists
regular_file
empty_or_missing
=== stat ===
size=0 lines_via_wc_pending mode=644 mtime=2026-10-24 21:48:13.426533671 -0300 type=regular empty file
=== wc -l -c ===
0 0 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-44/assimilation/collisions
=== od -An -tx1 ===
=== awk NR ===
0
=== python line count ===
bytes 0
repr b''
splitlines 0
splitlines_keep 0
```

`od` printed no bytes. `wc -l`, `awk` `NR`, and `splitlines` agree on 0.

## Row-start test

Row-start is the round-44 extractor, not a bare `S077` grep: `^ {0,3}\|[[:space:]]*S[0-9]{3,}` (census accepts 0–3 leading spaces). Staged append: 117 lines, 144266 bytes, mtime `2026-10-24 21:17:10.406283981 -0300`.

```
=== row-start pattern hits for S077 (0-3 leading spaces) ===
NO_ROW_START_S077
=== extractor ids equal to S077 ===
EXTRACTOR_NO_S077
=== count of S077 string ===
1
=== any | S077 | not at 0-3-space row start ===
NO_ID_CELL_S077
=== indented beyond 3 spaces starting with pipe+S077 ===
NO_DEEP_INDENT_ROW_S077
=== all S077 occurrences with line numbers ===
21:| S093 | Preservation approach — Portico, a service of ITHAKA — https://www.portico.org/our-work/preservation-approach/ | docs | A | what a dark preservation archive guarantees, as the service itself states it; this is the Portico that wave 1's S077 found J-STAGE contracted | the four-factor list and the closing paragraph on the dark archive and audit privileges; page modified 2023-05-12, read 2026-10-23 | true preservation rests on four factors, of which authenticity means the content needs to be an authentic replica of the original and its provenance must be verifiable, backed by a maintained audit trail; the archive is dark, with audit privileges for participants rather than open access | mined | 2026-10-23 | 365d — re-open the page and confirm the four factors and the dark-archive sentence are unchanged (ran 2026-10-23) | corpus/knowledge/citation-version-binding-r37.md |
```

Pipe-split of line 21: 11 cells. `S077` is only in column 5 (scope). Column 1, the row-start id, is `S093`.

Scope cell, quoted:

> what a dark preservation archive guarantees, as the service itself states it; this is the Portico that wave 1's S077 found J-STAGE contracted

The same prose, not an id cell, is in the staged knowledge file `knowledge/corpus/knowledge/citation-version-binding-r37.md` line 37: `J-STAGE contracted (wave 1's `S077`)`.

A 4-space indent would also miss the census pattern. No such line exists. There is no `| S077 |` id cell anywhere in the append.

## What the empty collisions file matches

On-disk lists were not rewritten. Fresh extracts were compared in memory and discarded.

```
=== on-disk staged-ids contains S077? ===
STAGED_IDS_NO_S077
=== on-disk reg-ids contains S077? ===
S077
REG_IDS_HAS_S077
=== comm -12 of on-disk lists (stdout only) ===
comm_exit=0
=== wc of on-disk id lists ===
 78 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-44/assimilation/reg-ids
111 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-44/assimilation/staged-ids
  0 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-44/assimilation/collisions
=== fresh extractor vs on-disk staged-ids ===
fresh_staged_lines=111
STAGED_IDS_MATCH_DOCUMENT
=== fresh registry extract vs on-disk reg-ids ===
fresh_reg_lines=78
REG_IDS_MATCH_DOCUMENT
=== fresh comm -12 (stdout) ===
fresh_comm_exit=0
fresh_collision_lines=0
=== fresh staged row-start range ===
S079
S189
=== S077 in fresh extracts ===
fresh_staged_no_S077
S077
```

`comm -12` printed no ids. Fresh staged row-starts run `S079`–`S189` (111). Fresh registry row-starts are 78 and include `S077`. Intersection is empty, and that empty set matches the on-disk `collisions` file. The zero is not a stale false green of a row the current documents still share.

## Calibration

- Empty `collisions` means no shared **row-start** id between `corpus/SOURCES.md` and the staged append. It does not mean the string `S077` is absent from the append.
- Lane row-start `S077` is a different document: `corpus/SOURCES.md` line 87, Poppler `pdftotext(1)`, opened 2026-10-24. The append's only `S077` is a cross-reference to "wave 1's S077" inside the Portico/J-STAGE scope cell of staged `S093`. Those are not the same source. Do not map them by subtracting 2 from a staged id.
- A string grep for `S077` would false-positive the scope cell. The 0–3-space row-start extractor does not.

## Not done

No write under `/home/vgpnk/Projects/shokuknow`. Append mtime after the reads was still `2026-10-24 21:17:10.406283981 -0300`. No fetch. No `jj`. No git commit. `collisions`, `reg-ids`, and `staged-ids` were not modified.
