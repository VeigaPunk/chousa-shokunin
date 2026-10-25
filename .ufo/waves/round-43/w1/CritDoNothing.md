# CritDoNothing — do-nothing control does not print C1=PASS

Seat: critic. Axes: operability, calibration, depth.
Measured commit named by the dispatcher: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
Attacked approach: R43-C1's do-nothing control (`--tool` pointed at a path that is not the split command). Bound not retuned. No lane production file edited.

## Axes

- operability: a tree that never grew `tools/absent-split.py` must not print `C1=PASS` (claims.md, predicate R43-C1, do-nothing control).
- calibration: this control must not be mistaken for a label agreement, and must not move the frozen 1/2 bound.
- depth: this control must not touch the S078 adoption or invent a quote.

## Counterexample

Strongest local counterexample for this seat: invoke the frozen C1 counter with `--tool /tmp/no-such-absent-split.py`, a path that is not `tools/absent-split.py` and is not a file. If that invocation prints `C1=PASS` or exits 0, the do-nothing control is dead and operability is a miss.

The path was absent before the run (`PATH_EXISTS=0`; `CONTROL_IS_FILE=False`; `CONTROL_EXISTS=False`). The default tool file was present (`DEFAULT_TOOL_IS_FILE=True` at `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/absent-split.py`), so the failure is the override, not a missing production command.

## Evidence

Command (assigned, run):

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py --tool /tmp/no-such-absent-split.py
```

Stdout, verbatim:

```
TABLE_ABSENT PASS 15/15
TOOL_PRESENT FAIL missing /tmp/no-such-absent-split.py
C1=FAIL
```

Exit code: `1`.

`C1=PASS` is not in that stdout (`C1_PASS_ABSENT=1`). A second run of the same command exited 1 and was byte-identical to the frozen control receipt (`RECEIPT_MATCH=1` against `corpus/evidence/round43/controls/c1-control-before.txt`). That receipt is:

```
TABLE_ABSENT PASS 15/15
TOOL_PRESENT FAIL missing /tmp/no-such-absent-split.py
C1=FAIL
```

The scored PASS receipt is a different file and was not produced by this control. `corpus/evidence/round43/receipts/c1-after.txt` ends in `C1=PASS` and includes `TOOL_EXIT`, `ABSENT_ENUMERATED`, `CLASSED`, `BOTH_NONEMPTY`, `REPRODUCIBLE`, and `MUTANT_DETECTED`. None of those lines appear in the do-nothing stdout.

Source of the kill, `corpus/evidence/round43/c1-count.py`: after `absent_ids` reads the round-42 table, `tool.is_file()` is false, `check("TOOL_PRESENT", False, ...)` prints the FAIL line, then the function prints `C1=FAIL` and `return 1` before `run()` and before the five summary lines. The missing path is never executed.

## Impacted axes

- operability: control holds. The assigned counterexample is rejected. A missing command cannot print `C1=PASS`. Exit 1 matches claims.md and `corpus/lessons/round-43.md` ("Do-nothing (`--tool` missing) exits 1"). Not a C1 miss.
- calibration: not scored by this command. C1 does not read `absent-split.tsv` labels and does not recompute R43-SPLIT. The 1/2 bound is untouched. No calibration regression from this control.
- depth: not scored. The missing-tool path does not open `corpus/knowledge/search-log-method-r39.md` or the Europe PMC capture. No depth regression.

Not a hidden regression, duplicate verdict, identity change, or false provenance of a pass:

- The early return hardcodes `C1=FAIL`. It does not fall through to `ok = all(...)`, so a `TABLE_ABSENT PASS` token cannot be aggregated into `C1=PASS`.
- No id is added or dropped; the tool is not run, so no label is emitted.
- The frozen control receipt matches the live stdout. It records a FAIL, not a fabricated PASS.

Tradeoff the L1 per-axis verdicts must not reject as a C1 miss: the first line is `TABLE_ABSENT PASS 15/15`, and the five target summary lines are omitted. That PASS is the table census, not the predicate. A scorer that promotes the first `PASS` token, or that treats a missing summary key as pass, would misread a control that the exit code and the `C1=` line already kill. Widening the claims sentence "a path that is not the split command" to an existing decoy file is a different attack (the cheapest gate named in claims.md and QUALITY 60). This seat's counterexample is the missing path, and that path does not pass. An alternate enumerator that emits the 15 ids is outside this control by the frozen predicate: C1 does not pin the tool's bytes, and a label swap that keeps both classes nonempty is C2's kill.

## Smallest safe correction

None to the counter, the receipt, the bound, or the split table. Do not edit `c1-count.py` after freeze to print the five summary lines on the missing-tool path: that would desync `controls/c1-control-before.txt` and would not change the verdict.

Scorer correction, not a lane edit: grade this control on the line `C1=FAIL` and exit code 1. Do not grade it on `TABLE_ABSENT PASS`.

## Verdict

The do-nothing attack fails to falsify R43-C1. Assigned command stdout is not `C1=PASS`. Exit code is 1.
