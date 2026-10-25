# MutMissingTool — C1 missing-tool probe

Seat: MutMissingTool (mutation-tester, leaf).
Axes: operability, calibration, depth. This probe scores operability (R43-C1 do-nothing control).
Milestone: Round 43: attack the frozen absent-class split and the one local adoption.
Measured commit named by the wave: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
Observed HEAD before the probe: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
No lane production file, git index, or sibling tree was written. No network. No install. The 1/2 bound was not retuned.

## Mutant

Smallest behavior-bearing point: the `--tool` path is absent. The assigned path `/tmp/absent-split-missing.py` was not a file before the probe (`ls: cannot access '/tmp/absent-split-missing.py': No such file or directory`) and was not created. No production byte was edited. `corpus/evidence/round43/c1-count.py` treats a missing tool as `TOOL_PRESENT` fail and returns 1 before executing the command (`tool.is_file()` false). That is the do-nothing control in `corpus/evidence/round43/claims.md`: a tree that never grew the split command cannot print `C1=PASS`.

Detector invocation (assigned probe):

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py --tool /tmp/absent-split-missing.py
```

A surviving mutant would be a coverage finding, not permission to change R43-C1.

## Expected detector

Frozen kill (`corpus/evidence/round43/claims.md`, C1 do-nothing control; `c1-count.py` docstring): `--tool` pointed at a path that is not the split command must exit 1. The assigned expectation is exit 1 and `TOOL_PRESENT FAIL`.

Committed control `corpus/evidence/round43/controls/c1-control-before.txt` (different missing path, stdout only):

```
TABLE_ABSENT PASS 15/15
TOOL_PRESENT FAIL missing /tmp/no-such-absent-split.py
C1=FAIL
```

Baseline (default tool) must not already fail, or the mutant result is inconclusive.

## Output

Pristine detector, same counter with the default tool (stderr empty, 0 bytes):

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
PRISTINE_EXIT:0
```

Mutated detector (assigned command), verbatim stdout. stderr empty. First run and a later stderr-separated re-run printed the same three lines.

```
TABLE_ABSENT PASS 15/15
TOOL_PRESENT FAIL missing /tmp/absent-split-missing.py
C1=FAIL
MUTATED_EXIT:1
```

Restored detector (default tool again; production bytes were never mutated; stderr empty):

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
RESTORED_EXIT:0
```

Pristine stdout and restored stdout compared identical (`cmp`).

## Verdict

**killed.**

Baseline passed (`C1=PASS`, exit 0), so the missing-tool failure is not a baseline failure and is not inconclusive. The counter printed `TOOL_PRESENT FAIL missing /tmp/absent-split-missing.py` and `C1=FAIL`, and the process exited 1. It did not print `C1=PASS`. `TABLE_ABSENT` still passed `15/15`; the miss is tool presence, not the round-42 absent enumeration. Contract unchanged.

## Restoration evidence

The mutant is absence of `/tmp/absent-split-missing.py`, not a byte edit. That path was absent before the probe and absent after it. Before and after sha256 of the files the detector reads:

```
54ced70767ccd20bc502504ef75d427bc760d10ebdf70a1053812ff8853289c9  corpus/evidence/round43/c1-count.py
c0738c7691dc6d46d6063e8013813962b8b56c4c8c319b28ea22b1c095b8e96b  tools/absent-split.py
bcfafd534541b6a59f893488408738332e3fe1e5c324d4bdeb58547d44c7395d  corpus/evidence/round42/quarantine-verdicts.tsv
```

All three hashes are identical before and after the probe. `git status --porcelain` on those three paths printed nothing after the probe. Restored detector output equals the pristine output. No scratch copy was left behind. Stop after this probe.

Report: .ufo/waves/round-43/w1/MutMissingTool.md
