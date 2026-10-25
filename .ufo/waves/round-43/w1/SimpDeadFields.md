# SimpDeadFields

Seat: simplifier, advisory. Axes: operability, calibration, depth. Milestone: Round 43 absent-class split. Bound not retuned. `tools/absent-split.py` was not edited.

## Verdict

No unused argument. No unused function.

Deletions made: none.

Advisory deletion candidates (neither is an argument or a function):

1. `import hashlib` at line 31. Stale name. No load in the file.
2. local `path` at line 130. Bound from `gate.cache_doc` and never read.

Both are safe to drop. The next deletion is not. Stop.

## Axes

- Operability. The six functions and the three path arguments are the command C1 executes. Dropping either candidate does not change that command's stdout. Dropping a function or a path argument would.
- Calibration. Rule R43-SPLIT and the 1/2 bound are untouched. C2 does not import this file. No label was retuned.
- Depth. No knowledge entry, registry row, or capture was touched.

## Functions — all used

In-file callers (grep of `tools/absent-split.py`):

```
tools/absent-split.py:50:def nfkc_ws(text: str) -> str:
tools/absent-split.py:55:def longest_run(quote: str, document: str) -> int:
tools/absent-split.py:72:def load_gate():
tools/absent-split.py:79:def absent_ids(table: pathlib.Path) -> list[str]:
tools/absent-split.py:90:def classify(row, body: str) -> tuple[str, int, int, str]:
tools/absent-split.py:92:    document = nfkc_ws(body)
tools/absent-split.py:94:        folded = nfkc_ws(quote)
tools/absent-split.py:97:        run = longest_run(folded, document)
tools/absent-split.py:105:def main(argv=None) -> int:
tools/absent-split.py:117:    gate = load_gate()
tools/absent-split.py:118:    wanted = absent_ids(table)
tools/absent-split.py:134:        label, run, qlen, ratio = classify(row, body)
```

`main` is the process entry, line 145: `sys.exit(main())`.

No other Python file imports this module. `c1-count.py` runs it as a subprocess and does not call these names. `c2-count.py` defines its own `nfkc_ws`, `longest_run`, and `load_gate`. Those are duplicates, not callers. Collapsing them is out of this seat (separability: C2 must not require this tool).

## Arguments — all read

AST parameter loads, unread list empty for every function:

```
FUNC nfkc_ws line=50 params=['text'] unread=[]
FUNC longest_run line=55 params=['quote', 'document'] unread=[]
FUNC load_gate line=72 params=[] unread=[]
FUNC absent_ids line=79 params=['table'] unread=[]
FUNC classify line=90 params=['row', 'body'] unread=[]
FUNC main line=105 params=['argv'] unread=[]
```

CLI `--table`, `--register`, and `--cache` are read (`args.table`, `args.register`, `args.cache`, lines 111–114). Each override is live: a missing path returns exit 2 before classification.

```
---FLAG_PROBE---
FLAG_EXIT:2
FLAG_STDOUT:
FLAG_STDERR:absent-split: table, register or cache unreadable
---REGISTER_PROBE---
REGISTER_EXIT:2
REGISTER_STDOUT:
REGISTER_STDERR:absent-split: table, register or cache unreadable
---CACHE_PROBE---
CACHE_EXIT:2
CACHE_STDOUT:
CACHE_STDERR:absent-split: table, register or cache unreadable
```

C1 invokes the tool with no flags, so the defaults are the scored path. The flags are still used. Removing them would be a second convention (hardcoded paths only) and would delete the usage/env exit the contract names. Keep.

## Advisory candidates

Linters on the committed file:

```
/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/absent-split.py:31:1: 'hashlib' imported but unused
PYFLAKES_EXIT:1
---VULTURE---
chousa-shokunin/tools/absent-split.py:31: unused import 'hashlib' (90% confidence)
chousa-shokunin/tools/absent-split.py:130: unused variable 'path' (60% confidence)
VULTURE_EXIT:3
---RUFF---
chousa-shokunin/tools/absent-split.py:31:8: F401 [*] `hashlib` imported but unused
Found 1 error.
[*] 1 fixable with `--fix`.
RUFF_EXIT:1
```

References search: `hashlib` occurs once, the import. `path` occurs once, the unpack `path, body, kind = gate.cache_doc(cache, row["url"])`. `body` and `kind` are read on the next line. No semantic caller of either name.

Scratch copy only, under `/tmp/simp-dead-fields/lane/`. Corpus and `quarantine-check.py` were symlinks. The copy dropped `import hashlib` and rebound `path` to `_`. Production file not written.

```
SCRATCH_BYTES 5339
DELTA_IMPORT import hashlib
DELTA_BINDING path, body, kind = gate.cache_doc(cache, row["url"]) -> _, body, kind = gate.cache_doc(cache, row["url"])
SHA_BEFORE c0738c7691dc6d46d6063e8013813962b8b56c4c8c319b28ea22b1c095b8e96b  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/absent-split.py
PROD_EXIT:0
SCRATCH_EXIT:0
PROD_STDERR:
SCRATCH_STDERR:
STDOUT_CMP:identical
PROD_LINES:15
SCRATCH_LINES:15
```

Scratch linters after that drop: `SCRATCH_VULTURE_EXIT:0`, `SCRATCH_PYFLAKES_EXIT:0`.

Narrow existing check, scratch tool, not the lane file:

```
C1_EXIT:0
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=9 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
```

C1 stderr empty. `C1_EXIT:0`.

## Preserved contract

Documented contract in the tool: read the committed table and the read-only cache; print TSV `id, class, max_run, max_qlen, max_ratio, nquotes`; no network; do not write the cache, the register, or the campaign tree; exit 0 when both classes are nonempty and every absent row is classified.

Production stdout (exit 0), byte-identical to the scratch stdout:

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

Shared tree check after the probes:

```
SHA_AFTER c0738c7691dc6d46d6063e8013813962b8b56c4c8c319b28ea22b1c095b8e96b  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/absent-split.py
PROD_STILL_HAS_HASHLIB True
PROD_STILL_HAS_PATH_BINDING True
PROD_BYTES 5357
GIT_DIFF_EXIT:0
```

`git diff --numstat -- tools/absent-split.py` printed no lines. SHA before and after match. Scratch sha is different (`17e1a01d5cf8c8c7881a5b8088a421d5cb33bb43733bc92b2cb69250857d0151`) and lives only under `/tmp`.

## Stop — next deletion harms an axis or the contract

- Delete any of `nfkc_ws`, `longest_run`, `load_gate`, `absent_ids`, `classify`, `main`: the command C1 executes stops classifying. Operability fails.
- Delete `--table`, `--register`, or `--cache`: the probed exit-2 path and the documented read of table, register, and cache go away. That is a second path convention, not a free deletion.
- Drop TSV columns `max_run`, `max_qlen`, `max_ratio`, `nquotes`: C1 reads only id and class, so C1 could still pass, but the tool's own contract names those columns and the committed `absent-split.tsv` has the same six fields. Dropping them creates a thinner convention. Not done.
- Unread register fields `line`, `round`, `class`, `checked_family` are payload fields, not arguments of this file. This file reads only `id`, `url`, and `quotes`. Deleting the unread fields means editing `quarantine-check.parse_register`, a shared authority. Out of scope. Not done.
- Do not retune the 1/2 bound. Do not import C2's copy of `longest_run` into this file or the reverse.

## Tradeoff

Dropping `hashlib` and `path` removes weight (5357 → 5339 bytes) and harms none of the three axes. Proven on a scratch copy; not applied. The finding is advisory. Applying it would not raise C1, C2, or C3. Leaving it does not fail them.

Report: .ufo/waves/round-43/w1/SimpDeadFields.md
