# MutEmptyClass — empty-class mutation probe (round 43, w1)

Role: mutation-tester (leaf). Assigned probe: copy the committed split labels, replace every `not-carried` with `misquote` in `/tmp` only, count the classes, and show `BOTH_NONEMPTY` fails on that copy. Lane file not edited. No network. No other runtime.

Axes: operability (same detector runs on pristine, mutant, restored), calibration (kill is the empty class, not a confused miss), depth (field-2 token only; hashes prove restoration).

## Mutant

Subject: committed split labels `corpus/evidence/round43/absent-split.tsv` at HEAD `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. Git blob `46352664d648e85f91335c0f1c04ef068a7b4318`. `git status --porcelain` on that path, `tools/absent-split.py`, and `corpus/evidence/round43/c1-count.py` printed nothing.

Scratch (isolated; lane bytes never written):

- pristine capture: `/tmp/mutemptyclass-r43/pristine.tsv`
- working copy: `/tmp/mutemptyclass-r43/scratch.tsv`
- mutant bytes kept: `/tmp/mutemptyclass-r43/mutant.tsv`
- harness emitter (not the mutant): `/tmp/mutemptyclass-r43/emit.py` — writes `scratch.tsv` bytes to stdout and exits 0

Mutation, field 2 only, exact token `not-carried` → `misquote`. Six rows replaced (S080, S082, S086, S088, S104, S114). Nine rows untouched. Other columns unchanged. 484 bytes → 466 bytes (6 × 3).

```
-1:S080	not-carried	19	50	0.380000	1
+1:S080	misquote	19	50	0.380000	1
-2:S082	not-carried	18	43	0.418605	1
+2:S082	misquote	18	43	0.418605	1
-4:S086	not-carried	4	46	0.086957	2
+4:S086	misquote	4	46	0.086957	2
-5:S088	not-carried	26	94	0.276596	1
+5:S088	misquote	26	94	0.276596	1
-8:S104	not-carried	25	88	0.284091	1
+8:S104	misquote	25	88	0.284091	1
-14:S114	not-carried	7	32	0.218750	2
+14:S114	misquote	7	32	0.218750	2
```

Class counts (column 2):

| copy | misquote | not-carried | rows |
|---|---:|---:|---:|
| pristine | 9 | 6 | 15 |
| mutant | 15 | 0 | 15 |
| restored | 9 | 6 | 15 |

## Expected detector

Frozen counter `corpus/evidence/round43/c1-count.py`, check `BOTH_NONEMPTY`: both `misquote` and `not-carried` must appear in the tool stdout labels. Same command on every cell:

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py --tool /tmp/mutemptyclass-r43/emit.py
```

Expected: pristine and restored print `BOTH_NONEMPTY PASS` / `BOTH_NONEMPTY=1/1` and exit 0. Mutant prints `BOTH_NONEMPTY FAIL` / `BOTH_NONEMPTY=0/1` and exits 1. A baseline failure would be inconclusive. This baseline passed, so the mutant cell is readable.

## Output

Pristine (exit 0):

```
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

stderr: empty.

Mutant (exit 1):

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY FAIL misquote=15 not-carried=0
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=0/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=FAIL
```

stderr: empty.

Restored (exit 0): byte-identical stdout to pristine. stderr empty.

`sha256sum` after restore:

```
bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/absent-split.tsv
bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58  /tmp/mutemptyclass-r43/pristine.tsv
bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58  /tmp/mutemptyclass-r43/scratch.tsv
9717e27addcfe11e1e1bae6afb426f9d62a7740c9ef3e5e3065bad4bf1abfa1e  /tmp/mutemptyclass-r43/mutant.tsv
```

`cmp` scratch vs pristine: identical. `cmp` lane file vs captured pristine: identical.

Non-interference, committed tool, after restore (exit 0):

```
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

## Verdict

**killed.** Baseline `BOTH_NONEMPTY=1/1` exit 0. Mutant emptied `not-carried` (15 misquote, 0 not-carried); `BOTH_NONEMPTY=0/1`, `C1=FAIL`, exit 1. Not inconclusive.

The kill is that check alone. Enumeration, vocabulary, exit 0 of the emitter, and reproducibility still passed. `MUTANT_DETECTED` stayed `PASS` on this copy: that line compares a 14-id prefix to the 15 absent ids, so it does not see an empty class. That is a coverage note about a different check, not permission to change the contract. This probe stops here.

## Restoration evidence

| bytes | sha256 |
|---|---|
| lane file before | `bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58` |
| scratch pristine | `bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58` |
| scratch mutant | `9717e27addcfe11e1e1bae6afb426f9d62a7740c9ef3e5e3065bad4bf1abfa1e` |
| scratch restored | `bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58` |
| lane file after | `bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58` |

Restored scratch equals the captured pristine bytes. Lane file hash unchanged before and after the probe. No lane production path was written.
