# ExecClassCount — field-2 class counts of the frozen absent-split table

Seat: leaf executor (L2). Date: 2026-10-24.
Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Measured commit named by the dispatcher: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
`git rev-parse HEAD` at measurement time: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
`git log -1 --format='%H %s' -- corpus/evidence/round43/absent-split.tsv`:
`737f40b6aa8f37ffe2269db370fd6d65a720d9a8 round-43: split the absent class and adopt one locally re-opened search-log entry`.
`git status --porcelain -- corpus/evidence/round43/absent-split.tsv`: empty (no output). The counted bytes are the committed file.
Production edits: none. Bound: not retuned. Writes: this file only. Tool installs: none. Network: none. Descendants spawned: none.

## Axes

- operability: the assigned `cut | sort | uniq -c` runs, exits 0, and both classes are nonempty.
- calibration: the two counts are the expected 9 and 6, vocabulary is only `{misquote, not-carried}`, and the 1/2 bound is left untouched.
- depth: the count is pinned to file bytes, row shape, and the id lists under each label, not to a prose retelling.

## Assigned command and verbatim output

```
$ cut -f2 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/absent-split.tsv | sort | uniq -c
      9 misquote
      6 not-carried
```

Exit code: 0.

Byte-exact stdout (`repr`):

```
b'      9 misquote\n      6 not-carried\n'
```

That is `uniq -c`'s width-7 count field: six leading spaces, the digit, one space, the label, newline. `sort` emitted `misquote` before `not-carried` (ASCII byte order). A second run of the same pipeline reproduced the same two lines and `EXIT:0`.

## Expectation

Dispatcher expectation: 9 and 6. Observed: 9 `misquote`, 6 `not-carried`. Expectation holds. 9 + 6 = 15.

## Cross-checks on the same file (not a retune, not a label edit)

| Check | Result |
|---|---|
| `wc -l` | `15 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/absent-split.tsv` |
| file size | 484 bytes |
| sha256 | `bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58` |
| field count | every row has 6 tab fields; the NF!=6 scan printed nothing |
| duplicate ids | `cut -f1 \| sort \| uniq -d` printed nothing |
| vocabulary | `cut -f2 \| sort -u` printed only `misquote` and `not-carried` |
| header | none; row 1 is `S080` |

Ids under each label (`awk -F'\t' '{print $2, $1}' \| sort`):

misquote (9): S084, S093, S094, S105, S108, S110, S111, S112, S116.

not-carried (6): S080, S082, S086, S088, S104, S114.

Both classes nonempty. No third label. No id in both classes.

## What this seat does not claim

This command counts labels already written in `corpus/evidence/round43/absent-split.tsv`. It does not recompute rule R43-SPLIT, does not execute `c1-count.py` / `c2-count.py` / `c3-count.py`, and does not decide whether those labels agree with the captures. A 9/6 table can still fail C2 if a label disagrees with the 1/2 rule. That agreement is outside this seat. The bound was not retuned.

## Remaining risks

- Locale can reorder `sort` output. It cannot change these two counts while the labels stay ASCII. The pasted bytes above are the bytes this process actually emitted.
- The table can be rewritten after this measurement. The sha256 above is the pin for the bytes counted here. Porcelain status was empty at measurement time.

## Blockers

None.
