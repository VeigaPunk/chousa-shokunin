# ReviewSplitIds — absent-split ids vs round-42 absent rows

- seat: reviewer, leaf (ReviewSplitIds). No subagent was dispatched.
- date: 2026-10-24
- lane (read-only except this report): `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- measured commit: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (`git rev-parse HEAD` equaled that hash; `git merge-base --is-ancestor` exit 0)
- inputs under test are clean at that commit (`git status --porcelain -- tools/absent-split.py corpus/evidence/round42/quarantine-verdicts.tsv` empty before and after the runs)
- writes: this report only. No lane production file, git index, jj state, fleet repo, sibling repo, or `/home/vgpnk/Projects/shokuknow` content was edited. No network. No tool install. No model alias.

## Axes

- **operability** — does `tools/absent-split.py` run on the committed table and emit an id per absent row
- **calibration** — is that id set exactly the round-42 `absent` rows, with none added and none dropped
- **depth** — order, duplicates, same-identity (no renumber), callers, and fail-closed paths that would add or drop ids

## Recommendation

No id was added. No id was dropped. The command's stdout ids are the 15 committed `absent` rows, in table order, with no duplicates. This is a recommendation from the measured bytes, not an admission that any other round-43 predicate has been scored.

## Assigned comparison

Command (verbatim stdout, then the exit line this seat appended):

```
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/absent-split.py; echo "EXIT:$?"
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
EXIT:0
```

Stderr on that run was empty. A second execution in the same comparison was byte-identical (`STDOUT_IDENTICAL True`, both exits 0, both stdouts empty of stderr).

Independent extract of column 2 exactly equal to `absent` (not the tool's function), then a set/order diff against the tool stdout:

```
RUN1_EXIT 0
RUN2_EXIT 0
STDOUT_IDENTICAL True
STDERR1 ''
STDERR2 ''
TOOL_N 15 TABLE_N 15
ORDER_EQUAL True
SET_EQUAL True
ADDED NONE
DROPPED NONE
TOOL_IDS S080 S082 S084 S086 S088 S093 S094 S104 S105 S108 S110 S111 S112 S114 S116
TABLE_IDS S080 S082 S084 S086 S088 S093 S094 S104 S105 S108 S110 S111 S112 S114 S116
TOOL_DUPES NONE
TABLE_DUPES NONE
```

A third parser (`awk -F '\t' 'NR>1 && $2=="absent" {print $1}'`) printed the same 15 ids in the same order, exit 0, empty stderr.

Table facts from a separate read of `corpus/evidence/round42/quarantine-verdicts.tsv` (sha256 `bcfafd534541b6a59f893488408738332e3fe1e5c324d4bdeb58547d44c7395d`, 10013 bytes, 0 CR): 25 lines, header `id\tverdict\treason\tflip`, 24 data rows, 4 columns each. Absent rows are lines 3–9 and 12–19. The nine non-absent rows are all `unverifiable` and are not absent rows, so their absence from the tool stdout is not a drop: S077, S095, S096, S120, S125, S100, S101, S102, S103.

| | ids |
|---|---|
| added (in tool, not an absent row) | none |
| dropped (absent row missing from tool) | none |

The default table path resolves to that same file (`SAME_FILE True`). `tools/absent-split.py` sha256 `c0738c7691dc6d46d6063e8013813962b8b56c4c8c319b28ea22b1c095b8e96b`. The printed id is the table id (`rid` from `absent_ids`), not a register id and not a renumber. There is no S118/S078 remap on this path. Exit 0 means each of those 15 ids was found in the register under that same id; a miss returns 1 before any stdout (`tools/absent-split.py` lines 125–140).

## Callers and identity

- Canonical runtime is this one script. Two runs on the default arguments were byte-identical. No second entry point emits a different id list.
- `corpus/evidence/round43/c1-count.py` `absent_ids` (lines 34–42) uses the same column-2 rule and requires `ids == expected` (line 80), which is order-sensitive. On the bytes above that equality holds. This seat did not run `c1-count.py`.
- `corpus/evidence/round43/c2-count.py` does not read the tool. It reads `corpus/evidence/round43/absent-split.tsv`. That file is byte-identical to the tool stdout (sha256 `bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58` both sides). So the committed split table did not add or drop an id relative to this run either. Labels were not graded here.
- `cache_doc` in `tools/quarantine-check.py` (lines 244–258) only reads. The register mtime stayed `2026-10-24 08:37:00 -0300`. The cache directory mtime stayed `2026-10-24 21:14:35 -0300`, which predates these runs.

## Error paths (not the measured add/drop)

A missing table is the preflight. It returns before classification and before stdout:

```
$ python3 .../tools/absent-split.py --table /tmp/no-such-absent-split-table.tsv; echo "PREFLIGHT_EXIT:$?"
absent-split: table, register or cache unreadable
PREFLIGHT_EXIT:2
```

`/tmp/no-such-absent-split-table.tsv` was not created. Copies of the table under `/tmp/review-split-ids/` (lane file untouched) with S116 relabeled, and with a synthetic `S999` absent row appended:

```
FOURTEEN EXIT 1
FOURTEEN STDOUT ''
FOURTEEN STDERR 'absent-split: expected 15 absent rows, found 14\n'
SIXTEEN EXIT 1
SIXTEEN STDOUT ''
SIXTEEN STDERR 'absent-split: expected 15 absent rows, found 16\n'
```

Those paths print no ids. They do not emit a partial or expanded set. On the committed table the count is 15, so this pin is not an add or a drop.

## Findings by severity

No actionable finding. No high, medium, or low defect in the id set on the measured commit.

## Residual risk

- The count pin is hardcoded at 15 (`tools/absent-split.py` lines 119–121). A later edit of the round-42 table that changes the absent count makes the command exit 1 with empty stdout (every id dropped from output) instead of enumerating the new set. That is not the tree that was measured.
- One bad row (no register quotes, or a capture that is not a text page) also returns 1 before stdout, so a single failure drops every id from the output rather than emitting the rest. Not observed: exit was 0 and all 15 lines were printed.
- A verdict cell that is not exactly `absent` (trailing space, different column) would be excluded. The committed cells are exactly `absent` or `unverifiable`. Not observed as a drop.
- `c1-count.py` lines 89–91 set `MUTANT_DETECTED` by comparing `ids[:-1]` to the 15-id expected list. Those lengths differ, so the check cannot fail when the expected list has 15 ids. It does not add or drop an id, and it was not used as evidence here. Grading that counter is another seat's item.

## Verification gaps

- `c1-count.py` and `c2-count.py` were not executed. The id equality they depend on was checked from their source plus the tool stdout and the two tables.
- Register ids were not dumped as a second population. Source limits stdout to `wanted`, and exit 0 shows each wanted id was present. A register-only id cannot appear in this stdout.
- The 14-row and 16-row probes used `/tmp` copies. They are not the committed table.
- The first assigned run wrote gitignored `tools/__pycache__/absent-split.cpython-314.pyc`. That file was removed. `quarantine-check.cpython-314.pyc` and `quote-reopen.cpython-314.pyc` were already present and were not rewritten by these runs. Later runs used `PYTHONDONTWRITEBYTECODE=1` / `python3 -B`.
- Unrelated dirty and untracked paths exist in the worktree (round-40/41 reports, round-43 wave files). They are not inputs to this comparison.
- No network fetch. The 1/2 bound was not retuned and was not re-scored.

Report: .ufo/waves/round-43/w1/ReviewSplitIds.md
