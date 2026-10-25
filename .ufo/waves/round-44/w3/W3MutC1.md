# W3 MutC1 — mutation test of c1-count.py (round 44, claim C1)

Scope: falsify the landed C1 gate. Two single-field mutations of
`corpus/evidence/round44/parent-lifetime.receipt`, applied to copies under
`/tmp` only (production receipt untouched). Counter run unmodified:
`python3 corpus/evidence/round44/c1-count.py --receipt <copy>`.

## Baseline control (unmutated receipt, read via --receipt)

```
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=PASS
EXIT_CODE=0
```

## Mutation A — one `child_pid=` set to 0

Copy `/tmp/w3-mutA-childpid0.receipt`. Diff vs original, single line (a reap
line, since `parse()` collects child pids from `reap` records only):

```
66c66
< reap name=ReviewC1Shape child_pid=3226666 exit_code=1 epoch=1792889281
---
> reap name=ReviewC1Shape child_pid=0 exit_code=1 epoch=1792889281
```

stdout:

```
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=1
NAMES_MATCH=64/64
C1=FAIL
```

exit code: `1`

## Mutation B — `end parent_pid=` changed to a different number than `start parent_pid=`

Copy `/tmp/w3-mutB-endpid.receipt`. Diff vs original, single line:

```
130c130
< end parent_pid=3226659 epoch=1792889282 n_spawned=64 n_reaped=64
---
> end parent_pid=4242424 epoch=1792889282 n_spawned=64 n_reaped=64
```

stdout:

```
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=0/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=FAIL
```

exit code: `1`

## Findings

- Both mutations flip the gate: C1 PASS/exit 0 → C1 FAIL/exit 1. The counter
  is not vaporware on its stated axes — `ZERO_PIDS` and `PARENT_PID_MATCH`
  each independently detect their mutation and nothing else moved
  (N_SPAWNED/N_REAPED/NAMES_MATCH stayed 64/64 in both).
- Mutation A note: zeroing a `spawn` line's `child_pid=` instead of a `reap`
  line would NOT flip the gate — `parse()` only reads child pids from `reap`
  records. The landed receipt's spawn/reap child pids agree pairwise, so this
  is cosmetic today, but the counter's name ("every child_pid is positive")
  is narrower than what it checks.
- Boundary confirmed (matches the script's own docstring, not refuted): a
  self-consistent hand-written receipt — 64 matching seat names, invented
  positive pids, start/end pid equal, n_spawned=n_reaped=64 — still scores
  C1=PASS exit 0. The gate stops prose assertion, pids-0, and pid mismatch;
  it does not stop a coherent forge. Falsification attempt on the gate's
  claimed strength: gate holds for both mutations; forge window remains open
  by design admission.

No production files modified; mutations live only in `/tmp`.
