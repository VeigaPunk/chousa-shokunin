# ExecMutC1Counter

## Verdict
Both isolated expectation mutants score 6/7 and exit 1; the corrected `sha-shim-other` expectation and the `hold-match` CLEAN expectation are load-bearing.

## Evidence
Lane tip observed with `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master`: `b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65`.

Workspace: `/tmp/chousa-r37-mut-c1.06nNwV` (`C1_TMP` existed). Mutants were copies of `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py`; both used gate `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`.

Seed 37101 command:
```sh
C1_TMP=/tmp/chousa-r37-mut-c1.06nNwV python3 /tmp/chousa-r37-mut-c1.06nNwV/sha-shim-other-mutant.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 37101 --receipt /tmp/chousa-r37-mut-c1.06nNwV/sha-shim-other-seed37101.json; status=$?; printf 'COUNTER_EXIT=%s\n' "$status"; test "$status" -eq 1
```
Observed output:
```text
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
FAIL sha-shim-other   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=6/7
COUNTER_EXIT=1
```

Seed 37102 command:
```sh
C1_TMP=/tmp/chousa-r37-mut-c1.06nNwV python3 /tmp/chousa-r37-mut-c1.06nNwV/hold-match-mutant.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 37102 --receipt /tmp/chousa-r37-mut-c1.06nNwV/hold-match-seed37102.json; status=$?; printf 'COUNTER_EXIT=%s\n' "$status"; test "$status" -eq 1
```
Observed output:
```text
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
FAIL hold-match       expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=6/7
COUNTER_EXIT=1
```

## Findings
1. Restoring the inherited wrong `sha-shim-other` expectation in the temporary mutant yields 6/7: the scenario actually observes `CLEAN/supported`, not `DRIFT/stale`. Grounding: mutant `/tmp/chousa-r37-mut-c1.06nNwV/sha-shim-other-mutant.py:48`; frozen counter expectation `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py:48`; seed 37101 output above.
2. Flipping `hold-match` to expect `DRIFT/stale` also yields 6/7 because the hold observes `CLEAN/supported`. Grounding: mutant `/tmp/chousa-r37-mut-c1.06nNwV/hold-match-mutant.py:45`; frozen counter expectation `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py:45`; seed 37102 output above.
3. This reproduces the counter-table failure mechanism described by frozen claim erratum 1: the old wrong-digest-shim expectation encoded the vulnerable result; restoring it prevents a 7/7 score. Grounding: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/claims.md:125-132`.

## Limits
Only the two requested temporary counter mutants were run. Lane source files were not modified; no build, lint, formatter, or separate test suite was run. No tools were installed.
