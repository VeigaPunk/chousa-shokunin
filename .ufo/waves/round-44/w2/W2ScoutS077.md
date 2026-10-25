# W2ScoutS077

Seat: scout. Question: is S077 a row-start id in the staged `SOURCES.append.md`? If it is only a cell, quote that cell.

Axes: operability (the file was opened and the row-start patterns were run), calibration (a cell mention is not a row id; lane S077 and other lanes' S077 are other documents), depth (which column, which row, and what the current id span actually is).

No production file was modified. No fetch.

## Verdict

No. S077 is not a row-start id in the staged chousa append. It occurs once, and only as a cell.

## File

`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md`

That is the staged append this lane's wave-1 collision seat named, and the only `**/chousa/**/SOURCES.append.md` under `/home/vgpnk/Projects`. The header comment says `corpus-expansion-1 :: staged rows for lane chousa`.

Point measurement of that file:

```
bytes 144266
lines 117
sha256 55505c7c5336372e6494a9d5778bc8d72c4bd55e49741d9aebd9ac483a7bb979
mtime=2026-10-24 21:17:10.406283981 -0300 size=144266
```

## Cell

The only hit is line 21. That line is a row-start for `S093`, not `S077`. The line splits into 11 data cells (13 `|` fields, empty edges). `S077` is only in field index 4, header name `scope`. The scope cell contains no pipe, so the split is not shifted.

Quoted scope cell:

```
what a dark preservation archive guarantees, as the service itself states it; this is the Portico that wave 1's S077 found J-STAGE contracted
```

The words "wave 1's S077" are prose inside that cell. They are not an id cell.

## Commands

`grep -n 'S077'` exited 0 and printed one line:

```
21:| S093 | Preservation approach — Portico, a service of ITHAKA — https://www.portico.org/our-work/preservation-approach/ | docs | A | what a dark preservation archive guarantees, as the service itself states it; this is the Portico that wave 1's S077 found J-STAGE contracted | the four-factor list and the closing paragraph on the dark archive and audit privileges; page modified 2023-05-12, read 2026-10-23 | true preservation rests on four factors, of which authenticity means the content needs to be an authentic replica of the original and its provenance must be verifiable, backed by a maintained audit trail; the archive is dark, with audit privileges for participants rather than open access | mined | 2026-10-23 | 365d — re-open the page and confirm the four factors and the dark-archive sentence are unchanged (ran 2026-10-23) | corpus/knowledge/citation-version-binding-r37.md |
```

`grep -c 'S077'` printed `1` and exited 0. A Python count of the substring `S077` in the file was also 1. No non-row line contains it.

Row-start patterns, both the column-zero form used for the registry count and the 0–3 leading-space form (`^ {0,3}\|`, the same shape as `row_for` in `corpus/evidence/round44/c3-count.py`):

```
CMD: grep -nE '^\|[[:space:]]*S077[[:space:]]*\|'
grep_rowstart_exit:1
CMD: grep -nE '^ {0,3}\|[[:space:]]*S077[[:space:]]*\|'
grep_03_exit:1
```

Exit 1 here is grep's no-match, not a broken command. Python matches of those same patterns, and of any-indent `^ *\|\s*S077\s*\|`, were 0.

Header, from `head -n 6`:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
```

Independent extract of row-start ids with `^ {0,3}\|\s*(S[0-9]{3,})\s*\|`:

```
n 111
unique 111
dups []
min 79 max 189
missing []
monotonic True
S077_in_row_ids False
```

The span is S079–S189 with no gap and no duplicate. S077 is below the first row id. The PRISMA-S extension row in this file is line 7, id `S079`, not S077:

```
PRISMA_ROW line=7 id=S079 start='| S079 | PRISMA-S: an extension to the PRISMA Statement for Reporting Literature'
```

## Not this document

Lane `corpus/SOURCES.md` does have a row-start S077. That is a different file. `grep -nE '^\|[[:space:]]*S077[[:space:]]*\|'` on it exited 0:

```
87:| S077 | Poppler `pdftotext(1)` manual — `/usr/share/man/man1/pdftotext.1.gz` ...
```

Other lanes' staged appends also have their own row-start S077 (revenger, lore, kasegi, game-dev-2d, game-dev-3d, audio, kagi, kengaku). Those are not the chousa staged append. A repo-wide grep of `merge/*/SOURCES.append.md` would answer a different question.

`corpus/lessons/round-43.md` still says "staged S077 is the PRISMA-S DOI" and that lane and staged ids collide on S077. That sentence does not describe this file's current row-start ids: the PRISMA-S extension row here is S079, and there is no S077 row-start. This seat did not open a historical revision of the append, so it does not claim the lesson was false on the day it was written. It does claim that copying that sentence onto the current staged append would be id arithmetic, not a reading of the document.

Consistent with the append, and not used as the proof: `.ufo/waves/round-44/assimilation/staged-ids` has 111 lines and `grep -c '^S077$'` exited 1 (count 0); `.ufo/waves/round-44/assimilation/collisions` has 0 lines.

## Not measured

- Whether "wave 1's S077" in the scope cell named a real capture, or whether J-STAGE contracted Portico. The cell was quoted, not checked against a capture.
- Git or jj history of the append. No `jj`. No commit.
- Live-web truth. No fetch.
