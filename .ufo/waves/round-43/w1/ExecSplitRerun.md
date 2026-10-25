# ExecSplitRerun

Seat: leaf executor. Axes: operability, calibration, depth. Milestone: Round 43 absent-class split. Bound not retuned.

## Counts and exit code

Command: `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/absent-split.py`

```
MISQUOTE=9
NOT_CARRIED=6
N=15
EXIT_CODE=0
```

misquote (9): S084, S093, S094, S105, S108, S110, S111, S112, S116.
not-carried (6): S080, S082, S086, S088, S104, S114.
Both classes nonempty. stderr empty (`wc -c` = 0).

## Verbatim stdout (run A)

```
S080	not-carried	19	50	0.380000	1
S082	not-carried	18	43	0.418605	1
S084	misquote	48	90	0.533333	2
S086	not-carried	4	46	0.086957	2
S088	not-carried	26	94	0.276596	1
S093	misquote	79	120	0.658333	1
S094	misquote	63	86	0.732558	3
S104	not-carried	25	88	0.284091	1
S105	misquote	17	24	0.708333	3
S108	misquote	69	108	0.638889	1
S110	misquote	72	119	0.605042	3
S111	misquote	10	19	0.526316	1
S112	misquote	40	71	0.563380	3
S114	not-carried	7	32	0.218750	2
S116	misquote	34	36	0.944444	3
```

## Rerun evidence

Three further invocations (A, B, C) plus the first captured stdout were byte-identical.

```
RUN_A_EXIT=0
RUN_B_EXIT=0
CMP=IDENTICAL
CMP_PRIOR=IDENTICAL
MISQUOTE=9
NOT_CARRIED=6
N=15
bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58  /tmp/absent-split-a.tsv
bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58  /tmp/absent-split-b.tsv
RUN_C_EXIT=0
0 /tmp/absent-split-c.err
CMP_C=IDENTICAL
```

Every printed ratio sits on the frozen side of 1/2 (lowest misquote S111 0.526316; highest not-carried S082 0.418605). Construction examples in `corpus/evidence/round43/claims.md` match the printed runs: S093 79/120, S094 63/86, S108 69/108, S116 34/36, S086 4/46, S114 7/32. No bound change.

## Files changed

- Wrote this report only: `.ufo/waves/round-43/w1/ExecSplitRerun.md`
- No lane production file, git index, jj state, fleet repo, sibling repo, or `/home/vgpnk/Projects/shokuknow` write. Scratch copies under `/tmp` only.

## Behavior

`tools/absent-split.py` classified all 15 round-42 `absent` ids into misquote (9) and not-carried (6) and exited 0. Contract in the tool: exit 0 means both classes nonempty and every absent row classified.

## Remaining risks

- This seat counted the tool's stdout. It did not independently recompute longest-run against captures (other seats own S086/S093).
- This seat did not run `c1-count.py` or `c2-count.py`. Exit 0 here is not a claim that those counters print `C1=PASS` or `SPLIT_AGREES=15/15`.
- Row-maximum rule can hide a mixed quote inside a misquote row. Not measured here. Bound left at 1/2.

## Blockers

None for this seat's assigned command.
