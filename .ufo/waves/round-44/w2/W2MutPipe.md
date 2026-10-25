# W2MutPipe — one cell census rejects for a pipe

Seat: W2MutPipe (leaf). Axes: operability (both the reject and the pass were run), calibration (a backslash does not protect `|`; the wrong cell does not save the row; stripping the pipes and keeping the prose is not a pass), depth (which cell, which field index, why a second code fires). No production file was written. `corpus/SOURCES.md` was not appended. No fetch. No jj. No git commit.

`date -u +%F` printed `2026-10-25`. Census default `--today` is that date. Pipe rejection does not depend on it. Opened dates in the fixtures are earlier, so E08 did not fire.

## The pair

Staged file `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` line 22, id S094, is the only data row in that file whose census split is not 11 columns. The pipe is in the recheck cell, not the anchor. Anchor pipe count on that row is 0.

Rejected cell (recheck; two bytes `5c 7c` at file offsets 794 and 803):

```
180d — re-open the dataset page and confirm the label list still reads "SUPPORTS\|REFUTES\|NOT ENOUGH INFO" (ran 2026-10-23)
```

Rewritten cell that passes (same row, that cell only; census trims to this):

```
180d
```

`180d` is the cadence token already at the start of the rejected cell. The confirmation sentence, including the label list, does not stay in the cell. A census recheck is an ISO date, `NNd`, or a symbolic cadence (`sources-census.sh` lines 663–666). The prose is none of those.

## What census printed

Scratch registries under `/tmp/w2mutpipe-census/`. Not the lane registry. Each fixture had a stub `corpus/knowledge/claim-support-test-r37.md` so a real missing used-by would not be confused with the pipe. The stub is not an admission.

Exact staged line, header plus that one row:

```
CMD: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/w2mutpipe-census/rawline/corpus/SOURCES.md
exit=1
file	E01	S094 fields=13
file	E11	S094 missing used-by REFUTES\
```

Same row, recheck cell replaced by ` 180d `, every other cell unchanged:

```
CMD: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/w2mutpipe-census/recheck-180d/corpus/SOURCES.md
exit=0
file	ok	/tmp/w2mutpipe-census/recheck-180d/corpus/SOURCES.md
```

`gawk -F'|'` on those two data lines:

```
s094-raw 15 13
s094-180d 13 11
```

Contract census is `NF==13` (11 columns plus the two edge empties from the wrapping pipes). `fields=` in E01 is `NF-2` (`sources-census.sh` lines 3–4 and 635–637). Two interior `|` characters make `NF=15`, so `fields=13`. The backslash is not a field-separator escape. `\|` is still a pipe.

Frozen manual counter, the `NF!=13` awk from `corpus/evidence/round25-sources-census.sh` line 8:

```
s094-raw-malformed=1
s094-180d-malformed=0
```

## What does not pass

Replacing `\|` with `, ` and leaving the rest of the recheck prose. Field count is legal. Census still rejects. The reason is no longer the pipe.

```
CMD: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/w2mutpipe-census/strip-pipes-keep-prose/corpus/SOURCES.md
exit=1
file	E09	S094 recheck=180d — re-open the dataset page and confirm the label list still reads "SUPPORTS, REFUTES, NOT ENOUGH INFO" (ran 2026-10-23)
```

```
s094-strip-malformed=0
```

Rewriting the anchor and keeping the recheck pipes. The anchor of this row has no pipe. Changing it does not clear E01.

```
CMD: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/w2mutpipe-census/anchor-rewritten-pipe-kept/corpus/SOURCES.md
exit=1
file	E01	S094 fields=13
file	E11	S094 missing used-by REFUTES\
```

```
s094-anchor-malformed=1
```

The campaign note that says to rewrite the anchor applies when the pipe is in the anchor. On this row it is not. The cell to rewrite is the cell that contains the pipe.

## Why E11 names `REFUTES\`

`row_pass` stops the row after E01 (`next` at line 638). E11 is the other walker, `usedby_findings` (lines 555–560). That walker splits on every `|`, requires only 12 or more fields, and if `cells[8]` is `mined` it treats `cells[11]` as used-by. On a legal row `cells[11]` is the used-by path. The two extra pipes sit in recheck, which is before used-by, so `cells[8]` is still `mined` and `cells[11]` is the fragment `REFUTES\`. The stub file was present. The `180d` rewrite of the same row, same stub, exited 0 and did not print E11. The `REFUTES\` finding is the pipe shift, not a missing knowledge file.

## Isolation: one interior pipe, nothing else wrong

Copy of live registry row S008 (queued, used-by `—`, live `NF=13`). Not appended. Only the anchor cell was changed, by inserting ` | section 2.1`.

Rejected cell:

```
sections 2.1 rationale and 2.3 three PICO levels; last updated August 2023, Handbook v6.5 | section 2.1
```

Rewritten cell (the original anchor, pipe removed, no other cell changed):

```
sections 2.1 rationale and 2.3 three PICO levels; last updated August 2023, Handbook v6.5
```

```
CMD: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/w2mutpipe-census/s008/bad/corpus/SOURCES.md
exit=1
file	E01	S008 fields=12
```

```
CMD: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/w2mutpipe-census/s008/pass/corpus/SOURCES.md
exit=0
file	ok	/tmp/w2mutpipe-census/s008/pass/corpus/SOURCES.md
```

```
s008-bad 14 12
s008-pass 13 11
s008-bad-malformed=1
s008-pass-malformed=0
```

One interior `|` is enough. `fields=12` is `NF=14` minus 2. Status on this copy is `queued`, so the used-by walker does not run, and E01 is the only finding. That is the clean "because it contains a pipe" case. S094 is the row that already contains one.

## Registry not appended

Live scan of `corpus/SOURCES.md`: 78 column-zero `| S` rows, 0 with `split("|")` length other than 13, 0 with `\|`.

```
CMD: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
exit=0
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

Those five W04 lines are the standing warnings. They are not a pipe reject. Warnings do not change a clean lane.

`sha256sum` of `corpus/SOURCES.md` before the scratch runs and after the live validate was the same:

```
1d4c5004beb48a4e3ba67715cd342d406f159f238de91407fe412a9d09209a7c  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

`registry_rowstart_S094 False`. `registry_S094_mentions 0`. The staged append file was not edited. Scratch stays under `/tmp/w2mutpipe-census/`.

## Boundary

This seat did not adopt S094 and did not write a Gate block. The passing cell is the text that makes this row parse. Putting `180d` into `corpus/SOURCES.md` is still an append, and this seat did not do it. No other staged row in the chousa append failed the pipe scan. A row with no pipe can still fail census for a prose recheck; that was not this check, and it was not claimed for any row that was not run.
