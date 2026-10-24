# ExecC1LandedRederive

## Verdict
Both fresh-seed C1 runs passed 7/7 with exit code 0; both receipt gate hashes match the re-derived gate SHA-256.

## Evidence

Seed 37111 command (receipt: `/tmp/chousa-r37-c1-37111.YZXpiA/c1-s37111.json`):
```sh
C1_TMP=/tmp/chousa-r37-c1-37111.YZXpiA python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 37111 --receipt /tmp/chousa-r37-c1-37111.YZXpiA/c1-s37111.json
```
Observed counter output:
```text
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=7/7
EXIT_CODE=0
```

Seed 37133 command (receipt: `/tmp/chousa-r37-c1-37133.pnRH8Y/c1-s37133.json`):
```sh
C1_TMP=/tmp/chousa-r37-c1-37133.pnRH8Y python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 37133 --receipt /tmp/chousa-r37-c1-37133.pnRH8Y/c1-s37133.json
```
Observed counter output:
```text
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=7/7
EXIT_CODE=0
```

Direct re-derivation command, run after each seed:
```sh
sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
```
Observed twice:
```text
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
```
Receipt fields observed: seed 37111 and seed 37133; each `predicate_holds=true`, `matched=7/7`, `total=7`, and `gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39`.

## Findings
1. On seed 37111, the counter printed `CLAIM_PIN_PROVENANCE_MATCH=7/7`, exited 0, and its receipt digest equals the direct `sha256sum` output. Evidence: `/tmp/chousa-r37-c1-37111.YZXpiA/c1-s37111.json` and command/output above.
2. On seed 37133, the counter printed `CLAIM_PIN_PROVENANCE_MATCH=7/7`, exited 0, and its receipt digest equals the direct `sha256sum` output. Evidence: `/tmp/chousa-r37-c1-37133.pnRH8Y/c1-s37133.json` and command/output above.

## Limits
The seat's write boundary permits only this report under the lane and temporary files under `/tmp`; therefore the two generated receipts are in `/tmp`, not the requested `.ufo/waves/round-37/w1/ExecC1LandedRederive/` directory. No tools were installed or updated.