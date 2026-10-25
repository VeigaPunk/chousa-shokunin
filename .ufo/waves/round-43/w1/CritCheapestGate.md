# CritCheapestGate — cheapest C1=PASS program, and the check that rejects it

Seat: critic. Axes: operability, calibration, depth.
Measured commit: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (observed HEAD, same).
Attacked approach: the frozen cheapest-gate line in `corpus/evidence/round43/claims.md` and the matching docstring in `corpus/evidence/round43/c1-count.py`. Bound not retuned. Counter not edited.

## Axes

- operability: a program that prints `C1=PASS` without running `tools/absent-split.py` must not become the counter's `C1=PASS`, unless it actually enumerates the 15 absent ids. Name that program and the check that rejects it.
- calibration: do not mistake a label-swapped enumerator for a C1 miss, and do not treat an overbroad `--tool` sentence as measured.
- depth: this attack must not touch the S078 adoption or move the 1/2 bound.

## Assigned answer

Cheapest program that prints `C1=PASS` and does not run `tools/absent-split.py`: a 17-byte Python script whose only statement is `print("C1=PASS")`. Run by itself it prints `C1=PASS` and exits 0. It does not name or execute `tools/absent-split.py`.

The claims name a larger script that prints the five target lines. That script is the same gate, not a cheaper one (155 bytes). It also prints `C1=PASS` when run by itself.

Check that rejects either script, when `c1-count.py` executes it as `--tool`: `ABSENT_ENUMERATED` at line 80, `ids == expected`, where `expected` is `absent_ids()` on the round-42 table (lines 34–42), not the tool's own text. The counter does not echo the tool's `C1=PASS`. It prints `C1=FAIL` and exits 1.

`TOOL_PRESENT` does not reject a present file. `TOOL_EXIT` does not reject these scripts (exit 0). `MUTANT_DETECTED` does not reject them (it PASSes). `CLASSED` and `BOTH_NONEMPTY` also fail, because a tab-less printer has no labels. The check the frozen text cites — ids equal an independent read of the round-42 table — is `ABSENT_ENUMERATED`, and it is sufficient.

## Counterexample

The claims sentence "with `--tool` pointed at a path that is not the split command. It must exit 1" is false for a present file.

Strongest local counterexample: `/tmp/crit-cheapest-gate/table-enum.py` reads only `corpus/evidence/round42/quarantine-verdicts.tsv`, prints the 15 absent ids in that order, labels the first 14 `misquote` and the last `not-carried`, and never calls `tools/absent-split.py`. `c1-count.py --tool` on that file prints `C1=PASS` and exits 0. No check rejects it. `strace -f -s 400 -e trace=execve` shows two `execve` of the decoy and zero mentions of `absent-split.py`.

That pass is not a C1 predicate miss of the no-flag counting command. The no-flag command execs `tools/absent-split.py` twice. The decoy is the kill rule the claims already gave to C2: a label swap that keeps both classes nonempty. The defect is the universal `--tool` sentence, not the scored command.

## Evidence

Counter bytes unread as an instruction source and unchanged after the probes. sha256 before and after:

```
54ced70767ccd20bc502504ef75d427bc760d10ebdf70a1053812ff8853289c9  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py
```

`git status --porcelain` on `corpus/evidence/round43/c1-count.py` and `tools/absent-split.py` printed nothing. `tools/absent-split.py` sha256 stayed `c0738c7691dc6d46d6063e8013813962b8b56c4c8c319b28ea22b1c095b8e96b`.

Rejecting check, from the counter, not from the claims prose:

```
    check("ABSENT_ENUMERATED", ids == expected, "%d/15" % len(ids))
```

`run()` is only `subprocess.run([sys.executable, str(tool)], capture_output=True, text=True)`. There is no comparison of `args.tool` to `tools/absent-split.py`. `TOOL_PRESENT` is printed only on the missing-file early return (lines 70–73). `MUTANT_DETECTED` is `ids[:-1] != expected` in-process (line 91). It does not launch a mutant command.

Direct run of the cheapest program (`/tmp/crit-cheapest-gate/one-line.py`, 17 bytes, body `print("C1=PASS")`):

```
C1=PASS
EXIT:0
```

Counter on that program:

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py --tool /tmp/crit-cheapest-gate/one-line.py
```

Stdout, verbatim. Counter stderr 0 bytes. Exit 1.

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED FAIL 1/15
CLASSED FAIL 0/15
BOTH_NONEMPTY FAIL misquote=0 not-carried=0
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=0 expected=15
ABSENT_ENUMERATED=0/15
CLASSED=0/15
BOTH_NONEMPTY=0/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=FAIL
```

Claims-named five-line script, direct (`/tmp/crit-cheapest-gate/five-lines.py`, 155 bytes). It does not mention `absent-split`:

```
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
EXIT:0
```

Same counter, `--tool` that script. Stderr 0 bytes. Exit 1. The counter's summary is `0/15`, not the script's `15/15`. `MUTANT_DETECTED` still PASSes (`short=5`), so it is not the cover.

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED FAIL 6/15
CLASSED FAIL 0/15
BOTH_NONEMPTY FAIL misquote=0 not-carried=0
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=5 expected=15
ABSENT_ENUMERATED=0/15
CLASSED=0/15
BOTH_NONEMPTY=0/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=FAIL
```

A 13-byte `echo C1=PASS` file is fewer bytes, but the counter launches `sys.executable`, so that file does not print `C1=PASS` under the counter. Child error, verbatim:

```
  File "/tmp/crit-cheapest-gate/echo-c1.sh", line 1
    echo C1=PASS
         ^^
SyntaxError: invalid syntax
EXIT:1
```

Counter stdout for that file (stderr 0 bytes, the SyntaxError is captured from the child and discarded). First failing check is `TOOL_EXIT`, then `ABSENT_ENUMERATED` on empty stdout. Exit 1.

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT FAIL exit=1
ABSENT_ENUMERATED FAIL 0/15
CLASSED FAIL 0/15
BOTH_NONEMPTY FAIL misquote=0 not-carried=0
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=0 expected=15
ABSENT_ENUMERATED=0/15
CLASSED=0/15
BOTH_NONEMPTY=0/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=FAIL
```

Decoy that the counter accepts. Direct stdout (labels are not the committed 9/6 split):

```
ARGV ['/tmp/crit-cheapest-gate/table-enum.py']
S080	misquote
S082	misquote
S084	misquote
S086	misquote
S088	misquote
S093	misquote
S094	misquote
S104	misquote
S105	misquote
S108	misquote
S110	misquote
S111	misquote
S112	misquote
S114	misquote
S116	not-carried
EXIT:0
```

`grep absent-split` on `one-line.py`, `five-lines.py`, and `table-enum.py` printed `NO_HITS`.

Counter on the decoy. Exit 0. This is `C1=PASS` without running `tools/absent-split.py`.

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=14 not-carried=1
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
```

`strace -f -s 400 -e trace=execve`, no-flag counter, exit 0. The two children are `tools/absent-split.py`:

```
2934260 execve("/usr/bin/python3", ["python3", "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py"], 0x7fff9af65eb0 /* 226 vars */) = 0
2934274 execve("/usr/bin/python3", ["/usr/bin/python3", "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/absent-split.py"], 0x7ffc682e78e0 /* 226 vars */) = 0
2935312 execve("/usr/bin/python3", ["/usr/bin/python3", "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/absent-split.py"], 0x7ffc682e78e0 /* 226 vars */) = 0
```

Same strace, `--tool /tmp/crit-cheapest-gate/table-enum.py`, exit 0. `absent-split.py` count in that trace: 0.

```
2936298 execve("/usr/bin/python3", ["python3", "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py", "--tool", "/tmp/crit-cheapest-gate/table-enum.py"], 0x7ffdcb1e71e0 /* 226 vars */) = 0
2936331 execve("/usr/bin/python3", ["/usr/bin/python3", "/tmp/crit-cheapest-gate/table-enum.py"], 0x7ffd385bed90 /* 226 vars */) = 0
2936342 execve("/usr/bin/python3", ["/usr/bin/python3", "/tmp/crit-cheapest-gate/table-enum.py"], 0x7ffd385bed90 /* 226 vars */) = 0
```

Same strace, `--tool` the five-line script, exit 1. `absent-split.py` count: 0. Children are `five-lines.py` only.

Committed control `corpus/evidence/round43/controls/c1-control-before.txt` is the missing path. It dies at `TOOL_PRESENT` and never reaches `ABSENT_ENUMERATED`. It does not record the named five-line gate. The lesson's narrower line ("Do-nothing (`--tool` missing) exits 1") matches that receipt. The claims' universal line does not.

## Impacted axes

- operability: the printer is rejected. Hold for the assigned program. The no-flag command does run `tools/absent-split.py`. Not a scored-command miss. `MUTANT_DETECTED PASS` on the printer is false provenance if cited as the cover: the check did not run a mutant, and it did not fail.
- calibration: fixable defect in the claims sentence, not in the 1/2 bound. A present non-split enumerator exits 0. That conflicts with the same file's kill rule that a both-classes label swap is C2's kill, and with the lesson's missing-path wording. Duplicate authority. Do not absorb it by retuning the bound or by folding ratio checks into C1.
- depth: not implicated. None of these programs open the Europe PMC capture or `search-log-method-r39.md`.

Tradeoff the L1 per-axis verdicts must not reject as a C1 miss: `table-enum.py` scoring `C1=PASS` with 14/1 labels. The frozen predicate does not grade ratios, and the kill rule assigns that swap to C2. Killing it inside C1 would collapse the stated split. The no-flag command on this tree is a different fact, and it does exec the split tool.

## Smallest safe correction

Do not edit `c1-count.py`. The printer is already rejected at `ABSENT_ENUMERATED`. A deny-list for the string `C1=PASS` would not be the check that fires; the counter never reads that string as the verdict.

Do not retune 1/2. Do not add ratio grading or a tool-path pin to C1 in order to fail the label-swapped enumerator. A path pin would make the overbroad claims sentence true, but it is a frozen-counter change and it is not required to keep the no-flag command honest.

Correction, claims text only: narrow the do-nothing sentence to the frozen receipt and the lesson — `--tool` missing, `TOOL_PRESENT FAIL`, exit 1. If QUALITY 60 requires the named five-line gate to sit in the controls, record the five-line run above (`ABSENT_ENUMERATED FAIL 6/15`, `C1=FAIL`, exit 1). Do not cite `MUTANT_DETECTED` or the missing-path receipt as that cover.

## Verdict

The cheapest `C1=PASS` program that does not run `tools/absent-split.py` is `print("C1=PASS")`. `ABSENT_ENUMERATED` rejects it. The five-line script named in the claims is the same rejection, not a cheaper program. A table-only enumerator is not rejected; that is C2's swap, and the claims' universal `--tool` sentence overclaims the counter.

Report: .ufo/waves/round-43/w1/CritCheapestGate.md
