ATTACKS: C2 after-state on lane tip 1fc5ed193ad48a482402c862f4e4cc47e46d5b2d (final counter 60134f25… and freeze-time counter 36b3934e…), and re-production of every number in corpus/evidence/round47/controls/c2-before.txt and c2-controls.txt on archives of 22a44b8b (freeze) and 9a9f94db (base).

VERDICT: holds.

## Method
Worked on /tmp copies built from `git archive` of 1fc5ed193ad48a482402c862f4e4cc47e46d5b2d, 22a44b8b, 9a9f94db:
- `git archive <c> | tar -x -C /tmp/chousa-r47w2-RerunC2/{tip2,freeze2,base2}`
- `git show 22a44b8b:corpus/evidence/round47/c2-count.py` → c2-freeze.py (sha256 36b3934eda5b8ccd569bf577db51f1ac5286463ba8104ec43d777b72658336d1)
- `git show 7fb9a23:corpus/evidence/round47/c2-count.py` → c2-intermediate.py (sha256 99c8762a7d641f73bfb2410405ab697eab58c7a7c3593e0c3348de593a7be8b5)
- tip-tree counter sha256 60134f25a5069eef2e59309ed41511f13ce4557abc1390cc8ffb68f2cfcce4d4; round-46 counter pinned f93cb10795ef7402848ea355680a6b0bd25ad68c8913c24944ef92029c81046f on all three trees.
No tools installed (only python3/git/coreutils); no network; no repo mutation (all writes under /tmp; scratch deleted at end).

## Runs (verbatim decisive lines)

### Tip tree (1fc5ed1)
Final counter, --list:
```
ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7)
FLOOR=92  GATES_ROWS=51
REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0
C2=PASS
exit=0
```
matches measure-after.txt:15-24 exactly.
Freeze counter (36b3934e):
```
ENTRY_POINTS=93 (abc=85 dependence=+1 check_named=+7)
FLOOR=92  GATES_ROWS=46
REGISTERED=93/93 UNREGISTERED=0 DANGLING=0 MISMATCHES=0
C2=PASS
exit=0
```
matches measure-after.txt:26-35 (the "ENTRY_POINTS=93 REGISTERED=93/93" after-state) exactly.
Round-46 counter:
```
ENTRY_POINTS=85 (tools=8 counters=53 named=83) GATES_ROWS=46 REGISTERED=85/85 UNREGISTERED=0 C2=PASS exit=0
```
matches measure-after.txt:83-89.

### Freeze tree (22a44b8b)
Final counter, --list:
```
ENTRY_POINTS=93 (abc=84 dependence=+2 check_named=+7)
FLOOR=92  GATES_ROWS=41
REGISTERED=72/93 UNREGISTERED=21 DANGLING=0 MISMATCHES=21
C2=FAIL  exit=1
```
matches c2-before.txt re-measured tree A (lines 98-106) exactly.
Freeze counter:
```
ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7)
FLOOR=92  GATES_ROWS=36
REGISTERED=67/92 UNREGISTERED=25 DANGLING=0 MISMATCHES=25
C2=FAIL  exit=1
```
matches c2-before.txt original tree A (lines 30-38) exactly.
Intermediate counter (99c8762a): identical numbers to final counter above (93/41/72/21/21 FAIL).
Round-46 counter: `ENTRY_POINTS=84 (tools=8 counters=53 named=82) GATES_ROWS=36 REGISTERED=81/84 UNREGISTERED=3 C2=FAIL exit=1` (not claimed in any control; no conflict).

### Base tree (9a9f94db)
Final counter, --list:
```
ENTRY_POINTS=90 (abc=81 dependence=+2 check_named=+7)
FLOOR=92  GATES_ROWS=41
REGISTERED=72/90 UNREGISTERED=18 DANGLING=0 MISMATCHES=18
C2=FAIL  exit=1
```
matches c2-before.txt re-measured tree D (lines 127-135) and c2-controls.txt re-measured §2 (lines 47-54) exactly.
Freeze counter:
```
ENTRY_POINTS=89 (abc=81 dependence=+1 check_named=+7)
FLOOR=92  GATES_ROWS=36
REGISTERED=67/89 UNREGISTERED=22 DANGLING=0 MISMATCHES=22
C2=FAIL  exit=1
```
matches c2-before.txt original tree D (lines 64-72) and c2-controls.txt original §2 (lines 13-22) exactly.
Round-46 counter:
```
ENTRY_POINTS=81 (tools=8 counters=50 named=79) GATES_ROWS=36 REGISTERED=81/81 UNREGISTERED=0 C2=PASS exit=0
```
matches c2-controls.txt §1 (lines 5-10) exactly.

### Control §3 (freeze tree, corpus/QUALITY.md emptied)
Freeze counter (the counter whose reader is GATES_ROWS=36):
```
ENTRY_POINTS=86 (abc=84 dependence=+2 check_named=+0)
FLOOR=92  GATES_ROWS=36
REGISTERED=67/86 UNREGISTERED=19 DANGLING=0 MISMATCHES=19
C2=FAIL  exit=1
```
matches c2-controls.txt §3 (lines 26-34) exactly.
Final counter on the same emptied tree: `ENTRY_POINTS=87 (abc=84 dependence=+3 check_named=+0) GATES_ROWS=41 REGISTERED=72/87 UNREGISTERED=15 MISMATCHES=15 C2=FAIL exit=1` (expected: different row reader; not claimed).

## Disagreements / findings
1. No number in c2-before.txt or c2-controls.txt disagrees when run with the counter version that produced it. Every before/control value re-produced verbatim.
2. Labeling only: c2-before.txt:74 and c2-controls.txt:36 name the "FINAL counter" as sha256 99c8762a7d64… (commit 7fb9a23), but the final counter committed at the lane tip is 60134f25… (1fc5ed1). On freeze/base the two are numerically identical on every printed line (93/41/72/21/21 and 90/41/72/18/18), so the stale label changes no value.
3. After-state holds under both counters: final 94/94/0/0/0 PASS exit 0; freeze 93/93/0/0/0 PASS exit 0; both ENTRY_POINTS >= FLOOR=92 (freeze-tree count per the frozen counter, enforced in code). R46 instrument pin (f93cb10…) untripped on all trees (never exit 2).
4. Residual risk: none found in scope; the named limit (row truth read by a human; an entry cell can name a non-gate) is declared in claims.md and unchanged.

Verification pointers: counter source tip corpus/evidence/round47/c2-count.py (sha 60134f25…); freeze commit 22a44b8b; intermediate 7fb9a23; claims.md R47-C2 lines 67-99; measure-after.txt lines 15-35, 83-89; controls c2-before.txt / c2-controls.txt as above. Scratch /tmp/chousa-r47w2-RerunC2 deleted.
