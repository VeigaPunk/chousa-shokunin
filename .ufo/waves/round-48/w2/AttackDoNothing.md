# AttackDoNothing — cheapest controls vs frozen R48 c1-count.py / precision-count.py

Scope: `corpus/evidence/round48/{c1-count.py,precision-count.py}` at freeze commit
`4bbd234`, chains into frozen `round47/c1-count.py` and `round46/c1-count.py`.
All controls lived under `/tmp/chousa-r48-AttackDoNothing/` (scratch, deleted
after run). No counter or fixture edits.

## Verdict: COUNTEREXAMPLE — full C1 reached by a name lookup table

`name-keyed.py` — a tool that maps `basename(--entry)` to a verdict and never
reads a byte of entry/span/counts data — exits **0** on the frozen command:

```
$ python3 corpus/evidence/round48/c1-count.py --tool /tmp/chousa-r48-AttackDoNothing/name-keyed.py
implicit-neg=PASS wanted_rc=0 observed_rc=0
un-neg=PASS wanted_rc=0 observed_rc=0
un-prefix-flip=PASS wanted_rc=1 observed_rc=1 FINDING INF_POLARITY_FLIP bullet=1 token=name-keyed-lookup
repeated-figure=PASS wanted_rc=1 observed_rc=1 FINDING INF_POLARITY_FLIP bullet=1 token=name-keyed-lookup
nested-count-key=PASS wanted_rc=0 observed_rc=0
REFINEMENT_CASES=5/5
p01..a06: all PASS rc=0
CORRECT_BULLETS_PASS=12/12
MIN_CORRECT_PASS=11/12
PRECISION_GATE=PASS
LEGACY_R47=PASS
C1=PASS
exit=0
```

The entire tool is `REFUSE = {un-prefix-flip.md, repeated-figure.md, canary-b.md,
junk-uncited.md, junk-ungrounded.md, junk-borrowed.md, junk-flip-asserted.md,
junk-flip-denied.md, junk-flip-figure.md}`; refuse names → print
`FINDING INF_POLARITY_FLIP …` + `sys.exit(1)`, anything else → `sys.exit(0)`.
~25 lines. `hash-keyed.py` (sha256(entry)→verdict, digests taken verbatim from
the counters' own PINNED tables + replicated generated entries) also scores
`C1=PASS exit=0`, so the hole is not even rename-dependent.

## How each leg fails to detect zero-work

- **r48 cases**: case names are literals in `c1-count.py:13-17`; entries are
  generated into the tmpdir as `<name>.md`, so names are deterministic.
- **precision gate**: counts only `rc==0` (`precision-count.py:48`). Accept-all
  alone yields `CORRECT_BULLETS_PASS=12/12` — the gate has no junk leg at all.
- **r47 leg**: `junk` requires rc=1 + FINDING prefix (`round47/c1-count.py:77-78`)
  — satisfied by printing a string. `CANARY` copies fixtures to
  **`canary-a.md`/`canary-b.md`, compile-time constants** (`:107-110`), so the
  anti-name-keying defense is itself name-keyable. `R46_ENTRIES` only wants
  rc=0 — free.
- **r46 counter**: same hard-coded `canary-a/b.md` (`round46/c1-count.py:100-103`);
  junk legs want bare rc=1, no FINDING required.

Control: `name-keyed-naive.py` (same table minus `canary-b.md`) fails at
`LEGACY_R47=FAIL`; legs observed directly:

```
r47 c1-count: POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=fail R46_COUNTER=fail R46_ENTRIES=2/2 C1=FAIL
r46 c1-count: POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=fail C1=FAIL
```

— canary legs fire exactly as designed, against a *naive* table. The defect is
not the canary idea; it is that the canary names are known constants.

## Control matrix (all runs by me on this host)

| control | cases | precision | legacy r47 | C1 |
|---|---|---|---|---|
| landed tool (do-nothing) | 5/5 | 9/12 FAIL | PASS | FAIL exit=1 (matches before.txt) |
| `/usr/bin/true` (binary) | 0/5 | — | — | FAIL (see anomaly below) |
| `empty.py` (zero bytes) | 3/5 | 12/12 | FAIL | FAIL |
| `accept-all.py` | 3/5 | 12/12 PASS | FAIL | FAIL |
| `reject-all.py` | 2/5 | 0/12 | FAIL | FAIL |
| `name-keyed-naive.py` | 5/5 | 12/12 | FAIL (canary) | FAIL |
| **`name-keyed.py`** | **5/5** | **12/12** | **PASS** | **PASS exit=0** |
| **`hash-keyed.py`** | **5/5** | **12/12** | **PASS** | **PASS exit=0** |

`/dev/null` scores `TOOL=absent` exit=2 (char device fails `is_file`).
`mutation-check.py` observed `PRISTINE_CASES=PASS … MUTANTS_KILLED=5/5 exit=0`;
it mutates the pristine `tools/inference-ground.py`, so `--tool` controls do not
interact with it.

## Secondary defect: frozen capture `controls/before.txt` is not reproducible

`before.txt:36-47` records `c1-count.py --tool /usr/bin/true --cases-only` with
`implicit-neg=FAIL wanted_rc=0 observed_rc=0` (lines 39-40, 43). Under committed
code, `want==0` marks `ok = rc==0` (`c1-count.py:39-40`), so `observed_rc=0`
prints `PASS` — the recorded lines are an impossible (rc,PASS/FAIL) pair.
Observed now: `python3 /usr/bin/true` → `SyntaxError: source code cannot
contain null bytes`, rc=1, and the run prints `observed_rc=1` on all five rows
(0/5, exit=1). Bottom line unchanged, but the frozen control capture's
mechanism column is fabricated or from a different `/usr/bin/true`/harness.

## Verdicts on the frozen claim

- **R48-C1 predicate is FALSIFIED as evidence of a polarity check.** The frozen
  sentence's literal exit conditions are met by a lookup table doing zero
  polarity work; `C1=PASS`/`exit=0` cannot distinguish the landed tool from a
  25-line name dictionary. Cheapest concrete fixes: randomize canary/tmp names
  per run; hash-pin expected entry bytes; require FINDING tokens derivable only
  from case content (e.g., echo the span phrase); add a junk leg to
  `precision-count.py`.
- `MUTANTS_KILLED=5/5` re-verified on the pristine tool — unaffected, but it
  only proves the *landed* tool is killed on its own mutants; a lookup-table
  candidate never undergoes mutation.
- `before.txt` `/usr/bin/true` capture: internally inconsistent / not
  reproducible on this host (evidence-integrity flag for the round).

## Residual risk / gaps

- Tools write nothing and ignore `--root`; a candidate with write side effects
  is untested (out of scope: controls must not mutate).
- Precision set holds only rc=0 checks; nothing verified per-bullet beyond rc.
- Report trailer: `.ufo/waves/round-48/w2/AttackDoNothing.md` (this file).
