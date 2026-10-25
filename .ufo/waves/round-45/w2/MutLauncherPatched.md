# MutLauncherPatched — mutation test: C1 launcher (parent-lifetime.sh)

Round 45 wave 2, falsify. Target: LANDED `tools/parent-lifetime.sh`
(commit 5e8c7ad2f7b8254d83358820286e3d12ca4672d1), claim C1 (operability),
counter `corpus/evidence/round45/c1-count.py` (target CASES_MATCH=5/5).

Wave 1 reused the pre-fix tool; here every mutant is derived from the landed
bytes (archive tree at /tmp/chousa-r45-MutLauncherPatched/tree). Counter run
from inside that tree per the measure rule; mutants in
/tmp/chousa-r45-MutLauncherPatched/mutants/ (scratch, deleted at end).

## Mutants (one behavior point each) and results

All runs: `cd <tree> && python3 corpus/evidence/round45/c1-count.py --tool <mutant>`

| Mutant | Mutation | Targeted case | Result |
|---|---|---|---|
| m1-exit0-zero-tasks.sh | final guard drops `n_spawned -eq 0` → zero tasks exit 0 | (a) | 4/5, C1=FAIL, exit 1 — a FAIL, other four ok |
| m2-no-timeout-s.sh | start line drops `timeout_s=%s` | (e) | 4/5, C1=FAIL, exit 1 — e FAIL, other four ok |
| m3-timeout-optional.sh | `[[ "$TIMEOUT" =~ ... ]] || usage` → `TIMEOUT=${TIMEOUT:-300}` | (d) | 4/5, C1=FAIL, exit 1 — d FAIL, other four ok |
| m4-exit0-timeout-seat.sh | final guard drops `n_timeout -gt 0` → timed-out seats exit 0 | (c) | 4/5, C1=FAIL, exit 1 — c FAIL, other four ok |
| pristine (tree tools/parent-lifetime.sh) | none | — | 5/5, C1=PASS, exit 0 |

## Verbatim decisive output

m1:
```
CASE a_empty_exits_3=FAIL
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=ok
CASE d_no_timeout_exits_2=ok
CASE e_start_timeout_s=ok
CASES_MATCH=4/5
C1=FAIL
EXIT=1
```
m2:
```
CASE a_empty_exits_3=ok
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=ok
CASE d_no_timeout_exits_2=ok
CASE e_start_timeout_s=FAIL
CASES_MATCH=4/5
C1=FAIL
EXIT=1
```
m3:
```
CASE a_empty_exits_3=ok
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=ok
CASE d_no_timeout_exits_2=FAIL
CASE e_start_timeout_s=ok
CASES_MATCH=4/5
C1=FAIL
EXIT=1
```
m4:
```
CASE a_empty_exits_3=ok
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=FAIL
CASE d_no_timeout_exits_2=ok
CASE e_start_timeout_s=ok
CASES_MATCH=4/5
C1=FAIL
EXIT=1
```
pristine:
```
CASE a_empty_exits_3=ok
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=ok
CASE d_no_timeout_exits_2=ok
CASE e_start_timeout_s=ok
CASES_MATCH=5/5
C1=PASS
EXIT=0
```

## Verdict

All four mutants KILLED (each scored 4/5, exit 1; each breaks exactly its
targeted case). No surviving mutant. Pristine landed tool HOLDS (5/5,
exit 0): C1 as committed passes the frozen counter. C1's counter is
discriminating: single-point defects in each of the five clauses are caught.
No defect found in the landed tool's C1 behavior.

Resolvable pointers (sha256, full files):
- pristine d2c77c860c9ab051f6e5bc0549931e54a08b3001ab8a7173f956139aae280ff8
- m1 bae7c5421ac51df712ec9c3869c25893756853635f73f247f776e6ab34e54ad9 (anchor: final `if [[ "$n_spawned" -eq 0 || "$n_timeout" -gt 0 ]]; then`)
- m2 82ac152d6fc98956ef4029d1a685d009b4d000f3ebe082db5e1f16e89f008746 (anchor: `printf 'start ... timeout_s=%s\n'`)
- m3 d30d11e06ebb7af242252ccf3939ea4d9f364d45c9fa9d8e964fae97aebbc20a (anchor: `[[ "$TIMEOUT" =~ ^[1-9][0-9]*$ ]] || usage`)
- m4 5bbd6ee3c65c7a3dd4780b5a1b49d0c3ebf8878b6f1a6fc88cccb4e3d9a147ef (anchor: same final guard)

No repo/lane files touched; scratch removed.
