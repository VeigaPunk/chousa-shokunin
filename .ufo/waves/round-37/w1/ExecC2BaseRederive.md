# ExecC2BaseRederive

## Verdict
C2 base claim re-derived on both fresh seeds: `PIN_CAPTURE_ENV_MATCH=3/7`; predicate fails both times.

## Evidence
- Seed 37201 command:
  `C2_TMP=/tmp/chousa-c2-seed37201.3TOGYC python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 37201 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/w1/ExecC2BaseRederive/c2-base-s37201.json`
  Observed output: `PIN_CAPTURE_ENV_MATCH=3/7`; command exit code **1**. Receipt records seed `37201`, `matched=3`, `total=7`, `predicate_holds=false`, gate SHA-256 `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.
- Seed 37223 command:
  `C2_TMP=/tmp/chousa-c2-seed37223.WBOYQi python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 37223 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/w1/ExecC2BaseRederive/c2-base-s37223.json`
  Observed output: `PIN_CAPTURE_ENV_MATCH=3/7`; command exit code **1**. Receipt records seed `37223`, `matched=3`, `total=7`, `predicate_holds=false`, same gate SHA-256.
- Both output lines and return codes were observed directly from the counter invocations. Receipts:
  - `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/w1/ExecC2BaseRederive/c2-base-s37201.json`
  - `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/w1/ExecC2BaseRederive/c2-base-s37223.json`

## Findings
Tuple field order: `(pin_rc, pin_file, baseline_echo_lines, drift_rc, drift_line)`. For both seeds, all four failing cells have these expected-versus-observed values:
1. `env-echo-pin`: expected `(0, True, 0, 0, "GATE_DRIFT: none")`; observed `(0, True, 1, 1, "GATE_DRIFT: -GATE_GREP")`.
2. `env-echo-drift`: expected `(0, True, 0, 0, "GATE_DRIFT: none")`; observed `(0, True, 0, 1, "GATE_DRIFT: +GATE_GREP")`.
3. `env-fn-echo-pin`: expected `(0, True, 0, 0, "GATE_DRIFT: none")`; observed `(0, True, 1, 1, "GATE_DRIFT: -GATE_GREP")`.
4. `env-root-pin`: expected `(0, True, 0, 0, "GATE_DRIFT: none")`; observed `(0, True, 0, 1, "GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused root supported tallies tally verdict verified")`.

Grounding: counter stdout from both runs; receipt fields and failed-scenario JSON at the two absolute paths above. The other three scenarios passed in each run.

## Limits
No gate or counter code changed. No tooling was installed. Findings are limited to the assigned base-gate C2 re-derivation; no remediation or additional checks were performed.
