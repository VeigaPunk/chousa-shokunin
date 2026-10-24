# ExecMutGateC1

## Verdict
The claims are separable as stated: removing only the C1 hash fix yields C1 2/7 (exit 1) while C2 remains 7/7 (exit 0).

## Evidence
Scratch mutant: `/tmp/chousa-r37-mut-c1.sYvaWA/research-gate.sh`, copied from `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`; line 2017 replaced with `sha_actual=$(sha256sum < "$path" 2>/dev/null | cut -d' ' -f1 || true)` (edit result, `/tmp/chousa-r37-mut-c1.sYvaWA/research-gate.sh:2017`). No lane source was edited.

C1 command (seed 37101; `C1_TMP` pointed to existing `/tmp/chousa-r37-mut-c1.sYvaWA`):

```sh
C1_TMP=/tmp/chousa-r37-mut-c1.sYvaWA python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-mut-c1.sYvaWA/research-gate.sh --seed 37101 --receipt /tmp/chousa-r37-mut-c1.sYvaWA/c1-seed-37101.json
```

Observed output and exit:

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

Receipt: `/tmp/chousa-r37-mut-c1.sYvaWA/c1-seed-37101.json` records seed 37101, matched 2/7, `predicate_holds=false`, mutant gate SHA-256 `e4fc40a2364baeb534ca61e12c9cc1bfeebdfe1db64a0144e63f7ab8cabec10e`.

C2 command (fresh seed 37102; `C2_TMP` pointed to existing `/tmp/chousa-r37-mut-c1.sYvaWA`):

```sh
C2_TMP=/tmp/chousa-r37-mut-c1.sYvaWA python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /tmp/chousa-r37-mut-c1.sYvaWA/research-gate.sh --seed 37102 --receipt /tmp/chousa-r37-mut-c1.sYvaWA/c2-seed-37102.json
```

Observed output and exit:

```text
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=7/7
EXIT_CODE=0
```

Receipt: `/tmp/chousa-r37-mut-c1.sYvaWA/c2-seed-37102.json` records seed 37102, matched 7/7, `predicate_holds=true`, and the same mutant gate SHA-256 above.

## Findings
1. The sole mutation restores the vulnerable PATH-based `sha256sum | cut` call at scratch gate line 2017; the production gate remains untouched. Pointer: `/tmp/chousa-r37-mut-c1.sYvaWA/research-gate.sh:2017`.
2. C1 regressed to 2/7, with both forge cells and all three hostile-shim stale-direction cells failing. Pointer: the seed-37101 command output and receipt above.
3. C2 was unaffected at 7/7 on fresh seed 37102. This matches the frozen separation rationale that C1's counter checks claim verdicts while C2's fixtures do not carry a `sha256` field. Pointer: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/claims.md:98-105`.

## Limits
This is the requested single-seed-per-counter mutant attack, not a two-seed evaluation of the landed gate. No tools were installed. No blockers observed.