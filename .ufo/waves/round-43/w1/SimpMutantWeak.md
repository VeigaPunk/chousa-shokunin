# SimpMutantWeak — C1 MUTANT_DETECTED does not block a hardcoded printer

Seat: SimpMutantWeak (simplifier, leaf). No dispatch. No production edit. No network. No install. Bound not retuned.
Axes: operability (a hardcoded printer must not become `C1=PASS`), calibration (do not call an in-counter slice a mutant run), depth (name the dead weight and stop before a deletion that drops a frozen token).
Milestone: Round 43: attack the frozen absent-class split and the one local adoption.
HEAD observed: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD`).

## Verdict

No. A seat cannot make `corpus/evidence/round43/c1-count.py` accept a program that only prints the five PASS lines. `MUTANT_DETECTED` does not prevent that. On the printer it still scored `MUTANT_DETECTED=1/1`.

The check that prevents it is `ABSENT_ENUMERATED`: the counter executes the tool and requires the parsed ids to equal an independent read of the round-42 table.

```python
expected = absent_ids(table)
first = run(tool)
rows = [line.split("\t") for line in first.stdout.splitlines() if line]
ids = [row[0] for row in rows if row]
check("ABSENT_ENUMERATED", ids == expected, "%d/15" % len(ids))
```

`absent_ids` is the independent read (`corpus/evidence/round43/c1-count.py` lines 34–42). `run` is `subprocess.run([sys.executable, str(tool)], ...)` (lines 45–48). The five summary lines are printed by the counter after that comparison (lines 93–98). They are not read back from the tool. `ok = all(...)` (line 92) then withholds `C1=PASS` if `ids == expected` failed.

Replacing `c1-count.py` itself would bypass every check in it. That is not a property of `MUTANT_DETECTED`; it is an edit of the frozen counter, which this seat did not do and is outside the counting command.

## What MUTANT_DETECTED actually compares

```python
# mutant: a 14-row prefix of the real output must not be accepted as the enumeration
short = ids[:-1]
check("MUTANT_DETECTED", short != expected, "short=%d expected=%d" % (len(short), len(expected)))
```

(`c1-count.py` lines 89–91; the summary reprint is line 97.)

It does not execute a mutant tool. It slices the ids already parsed from the same stdout. `short != expected` is true for any list that is not `expected` plus one trailing id. A 14-row prefix makes the inequality true, so the named mutant scores `MUTANT_DETECTED PASS`. The comment's "must not be accepted" is already what `ids == expected` does. When that check passes on a 15-id table, `len(short)` is 14 and `MUTANT_DETECTED` cannot fail. The live receipt is that tautology: `MUTANT_DETECTED PASS short=14 expected=15`.

Round 42's counter did drop a register row and re-parse (`corpus/evidence/round42/c1-count.py` lines 125–140). This round's check does not.

## Deletions

Deletions made: none.

Deletion candidate: the `MUTANT_DETECTED` block (lines 89–91 and the line-97 reprint). Not deleted.

References search (`MUTANT_DETECTED` in the lane): the token is required by `corpus/evidence/round43/claims.md` (the C1 target), recorded in `corpus/lessons/round-43.md`, and present in `corpus/evidence/round43/receipts/c1-after.txt`. Those are semantic callers of the printed line. Deleting it would drop a frozen scoring token. That harms the frozen-contract axis. Stop. The next deletion is not taken.

Preserved contract: the counting command is still `python3 corpus/evidence/round43/c1-count.py`. It still executes `tools/absent-split.py`, still requires the 15 absent ids, and still prints the five lines only after its own checks. Live stdout matches the receipt (`diff` empty, live exit 0). Production hashes before and after the probes:

```
54ced70767ccd20bc502504ef75d427bc760d10ebdf70a1053812ff8853289c9  corpus/evidence/round43/c1-count.py
c0738c7691dc6d46d6063e8013813962b8b56c4c8c319b28ea22b1c095b8e96b  tools/absent-split.py
cc9e4822fc0115fc67a80f7d98c2efc05faaa61367b0b92c36c5379eb006a788  corpus/evidence/round43/claims.md
```

`diff` of those three hashes was empty (`BYTE_IDENTICAL=1`). Probes wrote only under `/tmp/simp-mutant-weak-r43/`. This report is the only lane write.

## Evidence

Live counter (stderr empty):

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py
```

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
EXIT=0
```

Second run redirected to a file: `LIVE_EXIT=0`. `diff -u` against `corpus/evidence/round43/receipts/c1-after.txt` was empty (`DIFF_EXIT=0`).

Cheapest gate, the five target lines and nothing else, at `/tmp/simp-mutant-weak-r43/five-only.py`:

```
#!/usr/bin/env python3
print("ABSENT_ENUMERATED=15/15")
print("CLASSED=15/15")
print("BOTH_NONEMPTY=1/1")
print("REPRODUCIBLE=1/1")
print("MUTANT_DETECTED=1/1")
```

Run directly:

```
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
EXIT=0
```

Same program as `--tool` of the frozen counter:

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py --tool /tmp/simp-mutant-weak-r43/five-only.py
```

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED FAIL 5/15
CLASSED FAIL 0/15
BOTH_NONEMPTY FAIL misquote=0 not-carried=0
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=4 expected=15
ABSENT_ENUMERATED=0/15
CLASSED=0/15
BOTH_NONEMPTY=0/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=FAIL
EXIT=1
```

`MUTANT_DETECTED` passed. `ABSENT_ENUMERATED` failed. `C1` did not pass.

A printer that also emitted `C1=PASS` (`/tmp/simp-mutant-weak-r43/five-lines.py`) was the same shape: direct run exit 0 with the six lines; counter result `ABSENT_ENUMERATED FAIL 6/15`, `MUTANT_DETECTED PASS short=5 expected=15`, `MUTANT_DETECTED=1/1`, `C1=FAIL`, exit 1.

Appending those six lines to the real 15-row tool stdout (`smuggle.py`) is the case that shows which check is doing the work. `CLASSED`, `BOTH_NONEMPTY`, `REPRODUCIBLE`, and `MUTANT_DETECTED` all passed. Only the id equality failed:

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED FAIL 21/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=9 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=20 expected=15
ABSENT_ENUMERATED=0/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=FAIL
EXIT=1
```

The five hardcoded lines have no tab, so they are not labels. `CLASSED` counts labels, not rows. It does not prevent the hardcode. `MUTANT_DETECTED` does not either.

The 14-row prefix the comment names (`short.py`, real tool stdout minus the last line) is not accepted, but not by `MUTANT_DETECTED`:

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED FAIL 14/15
CLASSED FAIL 14/15
BOTH_NONEMPTY PASS misquote=8 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=13 expected=15
ABSENT_ENUMERATED=0/15
CLASSED=0/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=FAIL
EXIT=1
```

The only probed shape that made `MUTANT_DETECTED` fail was a lengthened list: the 15 real ids plus a trailing `S999` (`long.py`). `ABSENT_ENUMERATED` had already failed:

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED FAIL 16/15
CLASSED FAIL 16/15
BOTH_NONEMPTY PASS misquote=10 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED FAIL short=15 expected=15
ABSENT_ENUMERATED=0/15
CLASSED=0/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=0/1
C1=FAIL
EXIT=1
```

## Tradeoff

`MUTANT_DETECTED` is weight. It does not detect the shortened enumeration its comment names, and it cannot fail once `ABSENT_ENUMERATED` has passed on this 15-id table. Removing it would make the counter match what it measures. It would also delete a line the frozen claim, the lesson, and the receipt require. That harms the frozen-contract axis and helps none of the three scored predicates. Not removed.

`ABSENT_ENUMERATED` stays. It is the check that rejects the five-line printer, the printer-plus-`C1=PASS`, the smuggled five lines, and the 14-row prefix.

Report: .ufo/waves/round-43/w1/SimpMutantWeak.md
