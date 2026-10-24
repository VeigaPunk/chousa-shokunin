# ExecMutGateC2

## Verdict
Removing only `-u BASH_ENV` from the scratch gate yields the expected separability: C2 scores 3/7 (exit 1) while C1 remains 7/7 (exit 0).

## Evidence
- Dispatch tip: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` → `b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65`.
- Scratch mutant: copied `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` to `/tmp/chousa-r37-mutgate.YTepIk/research-gate-mutant.sh`; removed only `-u BASH_ENV` from the `gate_canonical_capture` child `env` line (line 3936 of the copy). The resulting line is `-u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO \`.
- Existing temp parent: `/tmp/chousa-r37-mutgate.YTepIk/tmp`.
- C1 command (fresh seed 37137): `C1_TMP=/tmp/chousa-r37-mutgate.YTepIk/tmp python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-mutgate.YTepIk/research-gate-mutant.sh --seed 37137`

  Observed output:
  ```text
  PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
  PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
  PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
  PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
  PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
  PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
  PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
  CLAIM_PIN_PROVENANCE_MATCH=7/7
  COUNTER_EXIT_CODE=0
  ```
- C2 command (fresh seed 37138): `C2_TMP=/tmp/chousa-r37-mutgate.YTepIk/tmp python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /tmp/chousa-r37-mutgate.YTepIk/research-gate-mutant.sh --seed 37138`

  Observed output:
  ```text
  PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
  PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
  FAIL env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=1 drift_rc=1 'GATE_DRIFT: -GATE_GREP'
  FAIL env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=1 'GATE_DRIFT: +GATE_GREP'
  FAIL env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=1 drift_rc=1 'GATE_DRIFT: -GATE_GREP'
  FAIL env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=1 'GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused root supported tallies tally verdict verified'
  PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
  PIN_CAPTURE_ENV_MATCH=3/7
  COUNTER_EXIT_CODE=1
  ```

## Findings
1. The C2 fix is isolated by the assigned mutation: the capture child no longer scrubs `BASH_ENV`, and the C2 separation scenarios fail as expected. Grounding: scratch mutant `/tmp/chousa-r37-mutgate.YTepIk/research-gate-mutant.sh:3934-3938`; C2 frozen predicate and base behavior `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/claims.md:60-96`.
2. C1 stays at 7/7 under the same mutant, supporting independence of its PATH-pinning behavior from this C2 line. Grounding: C1 run above; frozen separability description `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/claims.md:98-105`.

## Limits
- This was a scratch-copy mutation only; the lane source and git/jj state were not edited.
- No build, lint, test, formatter, or other verification was run; only the two assigned counters were executed.
- No tools were installed or updated.
