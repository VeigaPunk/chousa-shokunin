# ExecRowCount

Seat: executor. Scope: registry row-start count in `corpus/SOURCES.md`. No production file was modified.

## Axes

- Operability: the assigned `grep -cE` runs and exits 0.
- Calibration: the printed count equals the frozen expectation 78, and an independent id extract is the same 78 lines.
- Depth: those 78 lines are the contiguous registry rows S001–S078 at the measured commit, not prose mentions and not an admitted-only census.

## Assigned command

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

Verbatim stdout:

```
78
```

Exit code: 0.

A second run of the same command printed `78` and exited 0.

Expectation 78: met.

## What the 78 are

`grep -nE` of the same pattern listed exactly these row starts, and no others:

- first: line 11, `S001`
- last: line 88, `S078`
- ids strictly increasing, no gaps, no duplicate row id
- `n 78 min 1 max 78 span 78`
- `nonunique 0`

The only `^\|` lines that do not match the assigned pattern are the header and the separator:

```
9:| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
10:|---|---|---|---|---|---|---|---|---|---|---|
```

Every matching line splits on `|` into 13 fields (empty edge + 11 cells + empty edge). `bad_width none`. Status cells inside those 78 rows:

- mined 54
- queued 19
- rejected 5
- sum 78

Rejected rows inside the count, not outside it: S014, S015, S016, S025, S074. 78 is every registry row start, including rejected and queued rows. It is not an admitted-only census.

## Identity of the file counted

HEAD and the goal's measured commit are the same:

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
```

`git status --porcelain -- corpus/SOURCES.md` printed no lines and exited 0. Working-tree blob equals `HEAD:corpus/SOURCES.md`:

```
3c7811d07cd1b033b9a9a7e37b9a446f121abc94
```

`sha256sum`:

```
1d4c5004beb48a4e3ba67715cd342d406f159f238de91407fe412a9d09209a7c  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

`wc -l`: `277`.

`git grep -cE` of the same pattern at `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` printed:

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8:corpus/SOURCES.md:78
```

Exit code: 0.

## Depth: S078 is the last registry id; S118 is not a row

Last matching row (line 88), id cell `S078`, source cell begins:

`Bramer, de Jonge, Rethlefsen, Mast, Kleijnen, A systematic approach to searching — Europe PMC full-text XML https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML`

Unique `S[0-9]{3,}` mentions in the file: 79. Unique row-start ids: 78. Mentioned but not a row start: `S118` only. No line contains an id cell `| Snnn |` that fails the anchored pattern (`unanchored_id_cell_lines none`).

The round-43 search-log bullet names the staged id in prose, which the assigned regex does not count:

`included 1 (S078, Europe PMC full-text XML of Bramer et al. 2018, staged id S118 re-pointed by document)`

A mention-counter would print 79 unique ids and miss the expectation. The assigned line-start counter prints 78 and matches the registry.

## Not measured here

- Cell contents of S078 beyond the id and the start of the source cell (other seats).
- `tools/absent-split.py`, the round-43 counters, and `sources-census.sh` (other seats). Those commands were not run, so they are not claimed to pass.
- Live-web truth. No fetch.

## Remaining risks

- The number is a point measurement of the clean tree at `737f40b6`. A later uncommitted registry row would change it.
- Treating 78 as "admitted sources" over-counts: 5 of the 78 are `rejected` and 19 are `queued`.
- The pattern requires a line-start pipe and at least three digits. An indented row, or an id with fewer than three digits, would be missed. None of either was present: every pipe-start line is the header, the separator, or S001–S078.
- Python `\s` is not POSIX `[[:space:]]`. The independent extract used `\s` and agreed on this ASCII file; that agreement is not a proof the two character classes are identical.

## Blockers

None.
