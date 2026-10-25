# ExecC1Receipt

MATCH. Live `c1-count.py` stdout is byte-identical to `corpus/evidence/round43/receipts/c1-after.txt`.

Axes named (not judged): operability is the subject of this diff; calibration and depth are not measured here.

## Files changed

None in the lane. Scratch only: `/tmp/c1-live.stdout`, `/tmp/c1-live.stderr`. This report is the only write under the lane tree.

## Behavior

Command (cwd irrelevant; absolute path):

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c1-count.py
```

Exit 0. Stderr empty. Stdout 13 lines, 314 bytes, ending in `C1=PASS`. `diff -u` against the receipt was empty (`DIFF_EXIT:0`). `cmp -s` exit 0. SHA-256 equal.

## Exact evidence

Command and captured output, verbatim:

```
EXIT:0
---STDOUT---
TABLE_ABSENT PASS 15/15$
TOOL_EXIT PASS exit=0$
ABSENT_ENUMERATED PASS 15/15$
CLASSED PASS 15/15$
BOTH_NONEMPTY PASS misquote=9 not-carried=6$
REPRODUCIBLE PASS identical=True$
MUTANT_DETECTED PASS short=14 expected=15$
ABSENT_ENUMERATED=15/15$
CLASSED=15/15$
BOTH_NONEMPTY=1/1$
REPRODUCIBLE=1/1$
MUTANT_DETECTED=1/1$
C1=PASS$
---STDERR---
---DIFF---
DIFF_EXIT:0
---CMP---
CMP_EXIT:0
---WC---
314 /tmp/c1-live.stdout
314 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/receipts/c1-after.txt
628 total
---SHA---
9553c682d8db8e7e367ad35d41e3636b70ee6f660b902557546362ce0527653c  /tmp/c1-live.stdout
9553c682d8db8e7e367ad35d41e3636b70ee6f660b902557546362ce0527653c  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/receipts/c1-after.txt
```

The `$` marks are `cat -A` end-of-line markers, not file bytes. No `^M`, no trailing spaces. Receipt read independently is the same 13 lines, last line `C1=PASS`.

Receipt path: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/receipts/c1-after.txt`.

## Remaining risks

- This diff does not grade whether a label matches the R43-SPLIT ratio. `c1-count.py` states that a label swap keeping both classes nonempty does not fail this counter. That is C2, not this receipt.
- Class counts in the matching stdout (`misquote=9 not-carried=6`) are the counter's own print, not a calibration check.
- `MUTANT_DETECTED` in the matching stdout is the counter's own print, not a C3 depth check.
- HEAD was not re-verified against measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. The live command was the committed counter path as invoked above.

## Blockers

None.
