# ExecC1BaseRederive

## Verdict
C1 operability is falsified on the base gate: fresh seeds 37101 and 37123 each scored 2/7 (counter exit 1). Both persisted receipts pin the same gate bytes as my independent `sha256sum` result.

## Evidence

Seed 37101 command (with the shell exit-code capture used):
```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 37101 --tmp /tmp/chousa-r37-c1-seed-37101 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/w1/ExecC1BaseRederive/c1-base-s37101.json; rc=$?; printf 'EXIT_CODE=%s\n' "$rc"
```
Observed output:
```text
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
CLAIM_PIN_PROVENANCE_MATCH=2/7
EXIT_CODE=1
```
Receipt: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/w1/ExecC1BaseRederive/c1-base-s37101.json` — seed 37101, matched 2 of 7, `predicate_holds=false`, `gate_sha256=a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.

Seed 37123 command (with the shell exit-code capture used):
```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 37123 --tmp /tmp/chousa-r37-c1-seed-37123 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/w1/ExecC1BaseRederive/c1-base-s37123.json; rc=$?; printf 'EXIT_CODE=%s\n' "$rc"
```
Observed output:
```text
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
CLAIM_PIN_PROVENANCE_MATCH=2/7
EXIT_CODE=1
```
Receipt: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/w1/ExecC1BaseRederive/c1-base-s37123.json` — seed 37123, matched 2 of 7, `predicate_holds=false`, `gate_sha256=a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.

Independent re-hash command and observed output:
```sh
sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh
```
```text
a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh
```

## Findings
1. The five failing cells on both seeds are `sha-shim-forge` (observed `rc=0/CLEAN/supported/finding=False`), `cut-shim-forge` (same), `sha-shim-other` (`rc=1/DRIFT/stale/finding=True`), `sha-shim-broken` (same), and `cut-shim-broken` (same). Evidence: both command outputs and the scenario records in the two receipts above.
2. Both receipt `gate_sha256` values equal the independently re-derived base-gate SHA-256 exactly. Evidence: both receipt headers and the `sha256sum` output above.

## Limits
This is the requested C1 base-gate re-derivation only; it does not measure a candidate/landed gate or C2. The runs used existing tools; no tool installation was needed.
