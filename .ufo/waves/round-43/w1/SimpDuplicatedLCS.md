# SimpDuplicatedLCS — local `longest_run` is required

- **Seat:** SimpDuplicatedLCS (L2 leaf, simplifier). **Lane:** chousa-shokunin. **Date:** 2026-10-24.
- **Measured commit:** `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (`git rev-parse HEAD` matched).
- **Asked:** `corpus/evidence/round43/c2-count.py` defines `longest_run` instead of importing it from `tools/absent-split.py`. Is that duplication required by the separability claim? Do not edit.
- **Axes:** operability (C1 alone executes `tools/absent-split.py`), calibration (C2's recompute must not require that file, and must not share its function object), depth (duplicate authority vs unreachable copy — prove which, then stop).
- **Edit scope honored:** zero production writes. Experiments ran under `/tmp/r43-simp-dup/` or in-process against the committed paths. No tool installed. Pacman untouched.
- **Deletions made:** none.
- **Deletion candidate:** `c2-count.py` `longest_run` (lines 46–59), the named collapse being "import it from `tools/absent-split.py`". **Rejected.** The next deletion harms calibration. Stop.

## Verdict

**Yes. The local duplicate is required by the separability claim, relative to the alternative the question names.**

The frozen claim is two operational sentences, not a style preference (`corpus/evidence/round43/claims.md` lines 72–73):

> C1 and C2 are separable. C1 does not read the split table's labels. C2 does not require `tools/absent-split.py` to exist.

`c2-count.py` meets the second sentence by recomputing the run itself (docstring lines 10–12; definition lines 46–59; call at line 92). It does not import `tools/absent-split.py`. Replacing that definition with an import makes the tool file a precondition of `SPLIT_AGREES`. That falsifies the claim. The duplicate is therefore not removable weight.

What the claim does **not** require: the two function texts being copies of each other. A different local implementation of the same rule would also satisfy "does not require `tools/absent-split.py` to exist." The bodies happen to match after the tool's docstring is stripped. That match shows they are not a second convention today. It is not a frozen predicate that they stay textually identical.

Adjacent, and also broken by the same import, but not the separability sentence: predicate R43-C2 requires an **independent** recompute (`claims.md` lines 54–56). A mutated `absent-split.longest_run` moves an importing counter to `SPLIT_AGREES=6/15` and leaves the local-def counter at `15/15`. The import would couple the calibration kernel to the operability command.

## Preserved contract

Unedited tree, this seat:

| Check | Result |
|---|---|
| `python3 corpus/evidence/round43/c2-count.py` | `SPLIT_AGREES=15/15`, `C2=PASS`, exit 0 |
| same with `--flip S086` | `SPLIT_AGREES=14/15`, exit 1 |
| `python3 corpus/evidence/round43/c1-count.py` | `C1=PASS`, exit 0 |
| `python3 corpus/evidence/round43/c3-count.py` | `C3=PASS`, exit 0 |
| production C2 open audit | opens `absent-split.tsv` only; does not open `tools/absent-split.py` |
| byte copy of C2 in a tree with no `tools/absent-split.py` | `C2=PASS`, exit 0 |

Production hashes before and after the scratch runs, unchanged:

```
5cbfe2f1127b50ae894bc48027ba119ca4eaf67fadc88251299512629bc9ba43  corpus/evidence/round43/c2-count.py
c0738c7691dc6d46d6063e8013813962b8b56c4c8c319b28ea22b1c095b8e96b  tools/absent-split.py
cc9e4822fc0115fc67a80f7d98c2efc05faaa61367b0b92c36c5379eb006a788  corpus/evidence/round43/claims.md
```

`git status --porcelain` on those paths (and `c1-count.py`, `c3-count.py`) printed nothing.

## Evidence

### 1. The duplicate is real, local, and not an import

Callers of the name `longest_run` in lane `*.py` outside `.ufo`:

- `tools/absent-split.py:55` defines it; `:97` calls it from `classify`.
- `corpus/evidence/round43/c2-count.py:46` defines it; `:92` calls it from `independent_labels`.
- `corpus/evidence/round43/c1-count.py` names `tools/absent-split.py` only as a subprocess (`TOOL`, `run`). It has no `absent-split.tsv` match. That is the other half of the separability sentence: C1 does not read the split table.

No production file imports the other's `longest_run`. `c2.longest_run is tool.longest_run` is `False`. A validation mirror at `.ufo/waves/round-43/assimilation/validate/corpus/evidence/round43/c2-count.py` is a byte copy of the counter (`cmp` exit 0). It is not a third caller. There is no assimilation copy of `tools/absent-split.py` (`cmp` exit 2).

Raw diff of the two definitions is the tool docstring only:

```
--- c2-count.py
+++ absent-split.py
@@ -1,4 +1,5 @@
 def longest_run(quote: str, document: str) -> int:
+    """Longest contiguous common run. Quote is the short side."""
     if not quote or not document:
         return 0
     best = 0
```

`AST_EQUAL_DOCSTRING_STRIPPED True`. `UNPARSE_EQUAL_DOCSTRING_STRIPPED True`.

`nfkc_ws` is the same pattern with a formatting-only split (tool binds the NFKC result to `text`, then collapses whitespace). Not asked as the deletion, and not imported either. Live compare below: 0 fold diffs.

### 2. Production C2 does not open the tool

```
$ python3 - << 'PY'   # runpy of corpus/evidence/round43/c2-count.py under an open audit hook
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
AUDIT_RC 0
AUDIT_ABSENT_SPLIT_OPENS 1
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/absent-split.tsv
AUDIT_OPENED_TOOL_PY False
```

The one `absent-split` open is the committed label table, which C2 is specified to read. It is not `tools/absent-split.py`.

### 3. Baseline and flip, unedited

```
$ python3 corpus/evidence/round43/c2-count.py; echo "EXIT:$?"
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
EXIT:0
$ python3 corpus/evidence/round43/c2-count.py --flip S086; echo "EXIT:$?"
SPLIT_AGREES=14/15
VOCAB_OK=15/15
MISMATCHES=1
MISMATCH S086 table=misquote independent=not-carried
C2=FAIL
EXIT:1
```

Retained siblings, same tree, not the asked predicate:

```
$ python3 corpus/evidence/round43/c1-count.py; echo "EXIT:$?"
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
EXIT:0
$ python3 corpus/evidence/round43/c3-count.py; echo "EXIT:$?"
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
EXIT:0
```

### 4. Separability sentence, positive: C2 passes with the tool file absent

Scratch root `/tmp/r43-simp-dup/absent/`. `c2-count.py` was `cmp`-equal to the committed file. `tools/` contained only `quarantine-check.py`. Register and cache stayed at their absolute paths (the counter's own defaults). No production path was renamed.

```
SCRATCH_TOOL_LISTING
quarantine-check.py
tools
SCRATCH_C2_CMP
CMP_OK
=== ABSENT_TREE_C2 ===
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
EXIT:0
```

So the committed duplicate does not require `tools/absent-split.py` to exist. The separability sentence holds of the unedited counter.

### 5. Named collapse, negative: importing the tool makes the file required

Scratch only. The local `longest_run` body was replaced with `importlib.util.spec_from_file_location` of `parents[3] / "tools" / "absent-split.py"`, then `mod.longest_run(...)`. A normal `import` is not available: the filename contains a hyphen. `importlib` from that path is the import the question names, and it is the same mechanism both files already use to load `quarantine-check.py`.

Tool file absent:

```
=== IMPORT_MISSING ===
Traceback (most recent call last):
  File "/tmp/r43-simp-dup/import-missing/corpus/evidence/round43/c2-count.py", line 135, in <module>
    sys.exit(main())
             ~~~~^^
  File "/tmp/r43-simp-dup/import-missing/corpus/evidence/round43/c2-count.py", line 107, in main
    expected = independent_labels(gate, pathlib.Path(args.register), pathlib.Path(args.cache))
  File "/tmp/r43-simp-dup/import-missing/corpus/evidence/round43/c2-count.py", line 86, in independent_labels
    ratio = longest_run(folded, document) / len(folded)
            ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/tmp/r43-simp-dup/import-missing/corpus/evidence/round43/c2-count.py", line 52, in longest_run
    spec.loader.exec_module(mod)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "<frozen importlib._bootstrap_external>", line 759, in exec_module
  File "<frozen importlib._bootstrap_external>", line 896, in get_code
  File "<frozen importlib._bootstrap_external>", line 954, in get_data
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/r43-simp-dup/import-missing/tools/absent-split.py'
EXIT:1
```

No `SPLIT_AGREES` line. Exit 1. That is the separability miss: C2 now requires `tools/absent-split.py` to exist.

Same importing counter, unmutated tool copied into the scratch tree (behavior-preserving on the happy path, so the only new fact is the dependency):

```
=== IMPORT_PRESENT ===
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
EXIT:0
```

### 6. Same import also drops the independent recompute

Scratch tool copied from production, then `return 0` inserted as the first statement of its `longest_run`. Probe: `mutated_longest_run('abcdef', 'xxabcdexx') = 0`.

Importing counter against that file:

```
=== IMPORT_MUTATED ===
SPLIT_AGREES=6/15
VOCAB_OK=15/15
MISMATCHES=9
MISMATCH S084 table=misquote independent=not-carried
MISMATCH S093 table=misquote independent=not-carried
MISMATCH S094 table=misquote independent=not-carried
MISMATCH S105 table=misquote independent=not-carried
MISMATCH S108 table=misquote independent=not-carried
MISMATCH S110 table=misquote independent=not-carried
MISMATCH S111 table=misquote independent=not-carried
MISMATCH S112 table=misquote independent=not-carried
MISMATCH S116 table=misquote independent=not-carried
C2=FAIL
EXIT:1
```

Byte-copied production counter in a tree that contains the same mutated tool (the file is present and wrong; the local def ignores it):

```
=== LOCAL_BESIDE_MUTANT ===
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
EXIT:0
```

The 9 mismatches are the table rows labeled `misquote`. A shared `longest_run` would make C2's "independent" labels a second call into C1's command. That is R43-C2, not a restatement of the existence sentence, and it is a second reason the import is not a simplifier win.

### 7. Not a second convention on current captures

Both implementations loaded from the committed paths. Every register row with quotes and a text-page capture was scored with each file's own `nfkc_ws` and `longest_run` (superset of the 15 absent ids: C2's `15/15` requires those ids to be in that page set).

```
ROWS_WITH_QUOTES_PAGE 20
QUOTES_COMPARED 28
QUOTE_NFKC_DIFF 0
DOC_NFKC_DIFF 0
RUN_DIFF 0
ROW_RATIO_OR_LABEL_DIFF 0
LABEL_DIFF 0
EXAMPLES []
BOUND 0.5 0.5 True
FUNC_IDENTITY False
```

Bound is `1/2` in both files. Folds, runs, and labels agree. The functions are still distinct objects. Agreement today does not license the import.

## Tradeoff

Keeping two source authorities means a later edit can drift them. That cost is what the separability sentence buys: C2 must still pass when `tools/absent-split.py` is gone, and its ratios must not be that file's function. Measured drift today is the docstring on `longest_run` and the statement split in `nfkc_ws`. Neither changes a label on the 28 compared quotes.

A third module that only C2 imported would also satisfy the existence sentence. It would not remove a duplicate unless `absent-split.py` imported it too, and that share is the coupling section 6 measured. The question's alternative was the import from `absent-split.py`. That alternative is forbidden. No other collapse was applied.

## Stop

The next deletion — drop `c2-count.py`'s `longest_run` and import it from `tools/absent-split.py` — harms calibration (separability existence sentence, and the independent recompute). It improves no axis: C1 already executes the tool as a command; C2 already agrees 15/15 without it. Not kept.
