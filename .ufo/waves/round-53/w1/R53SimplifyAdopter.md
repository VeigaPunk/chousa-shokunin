# R53SimplifyAdopter — YAGNI review of the C1 candidate and the frozen counter

Seat: R53SimplifyAdopter (leaf). Tool installs/upgrades: none. Scratch
`/fast/scratch/hyaku/chousa-r53/R53SimplifyAdopter/` removed before yield. Reviewed
`tools/assimilate-rows.py` v4 (`32aab5e`) vs base `a6ff732` (+102/-35 in that file; the commit
also adds 2 self-test packages, 6 fixture files and a 25-line `cases` block in `expected.json`)
and `corpus/evidence/round53/c1-count.py`. No lane file edited.

## 1. Baseline (untouched copy `$S/v4.py`)

```
$ TMPDIR=$S python3 corpus/evidence/round53/c1-count.py --tool $S/v4.py
… REAL PASS rc=0 map=ok rows=5 count-line=['CITED=6 APPEND=5 HELD=0 TWIN=1']
… REGRESS PASS r50-pin=ok r51-counter=LEGS=5/5
LEGS=8/8
C1=PASS
$ python3 $S/v4.py --selftest --fixtures <lane>/corpus/fixtures/assimilate-selftest
FIXTURES_SHA256=9822ad59544cd42d6c6a8c3d34cb14d4d7c98d21e4f388d604486d70dd5db4a6
SELFTEST=PASS findings=40 expected=40
$ python3 $S/v4.py --selftest --cites all --fixtures corpus/evidence/round50/c1-fixtures --expected …/expected.json
SELFTEST=PASS findings=26 expected=26  FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43
```

## 2. Structural fact: no frozen leg reaches the `cases` harness

TWIN/HELD/MIX/RECHECK/ORDER/NOENTRY run the tool as an ordinary command on generated
packages; REGRESS runs the round-50 expected file (no `cases` key), then round-51 **with
`--tool`**, whose default-self-test leg is hard-skipped — so C1=PASS does not depend on it:

```
$ TMPDIR=$S python3 …/round51/c1-count.py --tool $S/min.py --seed 53 | head -2
SELFTEST_DEFAULT=PASS (skipped: --tool)
```

## 3. Deletion candidates, each proved in a scratch copy
### 3.1 `late` multi-refusal aggregation in the recheck pre-pass (8 lines) — deletable

No leg and no case has more than one invalid recheck (`case_recheck` marks exactly one row;
`twin-recheck` has one). `noagg.py` prints the first refusal and returns:

```
$ TMPDIR=$S python3 corpus/evidence/round53/c1-count.py --tool $S/noagg.py  (x3 unseeded; then --seed 7)
LEGS=8/8 C1=PASS   (all four)
$ python3 $S/noagg.py --selftest --cites all --fixtures corpus/evidence/round50/c1-fixtures …
SELFTEST=PASS findings=26 expected=26      (cmp with v4: IDENTICAL)
```

Only observable difference, on a two-bad package I built in scratch: v4 prints S101 **and**
S102 recheck refusals, `noagg.py` only S101; both `rc=1`. Tradeoff: 8 lines buy the operator
every bad row in one run; the predicate reaches for a single line.
### 3.2 Case-schema validation raises (10 lines) — deletable with byte-identical outputs

`min2.py` drops the `isinstance` checks on `fixtures`/`findings`/`entry` and the case-fixtures
existence raise (a remaining `KeyError` still lands in the existing `except` → `SELFTEST=ERROR`):

```
$ diff $S/base-default.txt $S/min2-default.txt → IDENTICAL ("SELFTEST=PASS findings=40 expected=40")
$ cmp  $S/base-r50.txt $S/min2-r50.txt         → r50 IDENTICAL ("findings=26 expected=26")
$ TMPDIR=$S python3 …/c1-count.py --tool $S/min2.py --seed 7
$ diff $S/base-seed7.txt $S/min2-count-seed7.txt → LEG-BY-LEG IDENTICAL
```

Tradeoff: a typo'd `fixtures` path becomes a confusing `DIFF missing` set instead of
`SELFTEST=ERROR … case fixtures … missing`. Diagnostics, not behaviour.
### 3.3 The whole `cases` harness (45 lines deleted, 15 restored) — deletable from the legs, not free

`min.py` reverts `observe(entries=…)`, the case parsing/loop, the `REFUSED`-order compare and
the `n_got`/`n_want` counters:

```
$ TMPDIR=$S python3 …/c1-count.py --tool $S/min.py   (x3 unseeded, plus --seed 7)
LEGS=8/8 C1=PASS   (all four)
$ diff $S/base-seed7.txt $S/min-count-b.txt      → LEG-BY-LEG IDENTICAL
$ cmp  $S/base-r50.txt $S/min-r50.txt            → r50 IDENTICAL ("findings=26 expected=26")
$ python3 $S/min.py --selftest --fixtures <lane>/corpus/fixtures/assimilate-selftest
SELFTEST=PASS findings=28 expected=28            (v4: findings=40)
```

No leg and no self-test **verdict** changes; the self-test's **coverage** falls 40 → 28
hand-written findings. It qualifies on legs and on the r50 pin, but is not a no-op: it deletes
the only assertions the harness exists for (§4).

## 4. Is the ≈40-line harness justified by the two cases?

Measured shape: 3 case entries over 2 packages (`cases/twin-recheck`, `cases/refusal-order`
twice); both optional features are used exactly once (`entry` with an absent path; `entry: []`).
"Two more root-package rows" **cannot** replace them: a refusal suppresses every other finding
(the tool returns before writing rows; `twin-recheck` expects `TOOLEXIT 1`, `COLLISIONS -` and
one `REFUSED` line), while the root package must keep printing its 28 successful findings. The
twin *label* is already a root row (`MAP S017->S021 twin`, `MAP S014->S020 held`); the cases add
the refusal on a twin row, registry-before-entry order and no-entry refusal — all refusal-shaped.
Verdict: **keep the harness** — 30 net lines + 6 fixture files buy coverage the root package
cannot express, and it is the lane's only *hand-written* oracle of the two refusal behaviours
(the counter's `expect()` recomputes the same rule). §3.1/§3.2 are optional trims; keep §3.1.

## 5. Findings against the frozen claim (reported, not patched)

- **REGRESS is blind to the harness.** `leg_regress` passes `--tool` and round-51 hard-skips its
  `SELFTEST_DEFAULT` leg (§2): no C1 leg runs the default self-test, so C1 passes with a broken or
  deleted cases harness (§3.3 proves it); the 6 new fixture files count only as digest bytes.
- **Default fixture digest is unpinned.** `c1-count.py` pins only `R50_PIN` (`c5c56480…`); the
  planned Gate row quotes `9822ad59…`/`findings=40` (round-52 lesson line 26). Removing the case
  fixtures moves the root-only digest to `2e47b2b0…`, invalidating the quoted pair — a doc coupling.
- No dead branch in the *behavioural* part: `reg_bad` with/without `--entry` (NOENTRY),
  registry-first `refused` list (ORDER), `twin` (TWIN/MIX/REAL), pre-pass recheck incl. the
  `LEAD_RE` prose path (RECHECK; round-50 `STRIPPED S014 recheck`), `HELD=`/`TWIN=` counts (all
  mapped legs + REAL) are each exercised.

## 6. Preserved contract

Frozen predicate, targets, counters, controls and the lane tree untouched:
`git -C …/chousa-shokunin status --porcelain` lists only the round's untracked
`.ufo/waves/round-53/…` paths — no `tools/`, no `corpus/` entry. All variants are scratch copies;
no `lsp` server answered for this tree, so deletion claims rest on execution, not reference search.

VERDICT: attacked the C1 v4 patch for deletable weight — three deletions proved harmless to
the frozen count (`late` aggregation 8 lines, case-schema validation 10 lines, whole `cases`
harness 30 net lines; each `LEGS=8/8` three unseeded + `--seed 7`, round-50 pinned self-test
byte-identical); the harness is measurement-invisible yet justified as the only hand-written
refusal oracle, and REGRESS's `--tool` skip leaves it unguarded (reported, not patched).
