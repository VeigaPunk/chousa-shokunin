# ExecDoNothingCtl

## Verdict
Operability: the r38 C1 base control scores 2/7; Calibration: r37 C1 remains 7/7 on the landed gate; the requested r38 C2/base-gate 7/7 is contradicted (4/7), while the landed-gate comparison scores 7/7.

## Evidence

1. Revision identity:

   Command: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master`

   Output: `504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f`

2. r38 C1 against the base gate, fresh seed 38201 (C1_TMP was a new existing directory created by `mktemp -d`):

   Command: `tmp=$(mktemp -d /tmp/chousa-r38-c1-base.XXXXXX) && C1_TMP="$tmp" python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 38201`

   Observed stdout (exit 1):
   ```text
   PASS hold-plain           expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
   PASS hold-fn-benign       expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
   FAIL env-fn-echo-scrub    expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 1, 'drift_rc': 1, 'drift_line': 'GATE_DRIFT: -GATE_GREP'}
   FAIL env-fn-root-move     expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 1, 'drift_line': 'GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused root supported tallies tally verdict verified'}
   FAIL env-fn-suppress      expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 2, 'pin_file': False, 'echo_lines': -1, 'drift_rc': 2, 'drift_line': ''}
   FAIL env-override-missing expect={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'} observed={'pin_rc': 0, 'pin_file': True, 'refusal': ''}
   FAIL env-override-fake    expect={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'} observed={'pin_rc': 0, 'pin_file': True, 'refusal': ''}
   ENV_PIN_CAPTURE_MATCH=2/7
   ```

3. r38 C2 against the base gate, default `--counter` (the r38 C1 counter), fresh seed 38202 (C2_TMP was a new existing directory created by `mktemp -d`):

   Command: `tmp=$(mktemp -d /tmp/chousa-r38-c2-base.XXXXXX) && C2_TMP="$tmp" python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 38202`

   Observed stdout (exit 1):
   ```text
   FAIL hold-receipt-verifies      expect={'counter_rc': 0, 'receipt': True, 'verify_rc': 0} observed={'counter_rc': 1, 'receipt': True, 'verify_rc': 0}
   PASS self-rewrite-refused       expect={'counter_rc': 2, 'receipt': False} observed={'counter_rc': 2, 'receipt': False}
   FAIL foreign-gate-distinguished expect={'counter_rc': 0, 'receipt': True, 'verify_foreign_rc': 0, 'verify_landed_rc': 1} observed={'counter_rc': 1, 'receipt': True, 'verify_foreign_rc': 0, 'verify_landed_rc': 1}
   PASS counter-tamper-detected    expect={'clean_verify_rc': 0, 'verify_rc': 1} observed={'clean_verify_rc': 0, 'verify_rc': 1}
   PASS expect-tamper-detected     expect={'clean_verify_rc': 0, 'verify_rc': 1} observed={'clean_verify_rc': 0, 'verify_rc': 1}
   PASS body-tamper-detected       expect={'clean_verify_rc': 0, 'verify_rc': 1} observed={'clean_verify_rc': 0, 'verify_rc': 1}
   FAIL legacy-receipt-refused     expect={'hold_verify_rc': 0, 'counter_rc': 0, 'receipt': True, 'verify_rc': 1} observed={'hold_verify_rc': 0, 'counter_rc': 1, 'receipt': True, 'verify_rc': 1}
   RECEIPT_BINDING_MATCH=4/7
   ```

4. Round-37 C1 against the landed gate, fresh seed 38203 (C1_TMP was a new existing directory created by `mktemp -d`):

   Command: `tmp=$(mktemp -d /tmp/chousa-r38-r37c1-landed.XXXXXX) && C1_TMP="$tmp" python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38203`

   Observed stdout (exit 0):
   ```text
   PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
   PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
   PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
   PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
   PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
   PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
   PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
   CLAIM_PIN_PROVENANCE_MATCH=7/7
   ```

5. Gate comparison for C2, default `--counter`, fresh seed 38204 (C2_TMP was a new existing directory created by `mktemp -d`):

   Command: `tmp=$(mktemp -d /tmp/chousa-r38-c2-landed.XXXXXX) && C2_TMP="$tmp" python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38204`

   Observed stdout (exit 0):
   ```text
   PASS hold-receipt-verifies      expect={'counter_rc': 0, 'receipt': True, 'verify_rc': 0} observed={'counter_rc': 0, 'receipt': True, 'verify_rc': 0}
   PASS self-rewrite-refused       expect={'counter_rc': 2, 'receipt': False} observed={'counter_rc': 2, 'receipt': False}
   PASS foreign-gate-distinguished expect={'counter_rc': 0, 'receipt': True, 'verify_foreign_rc': 0, 'verify_landed_rc': 1} observed={'counter_rc': 0, 'receipt': True, 'verify_foreign_rc': 0, 'verify_landed_rc': 1}
   PASS counter-tamper-detected    expect={'clean_verify_rc': 0, 'verify_rc': 1} observed={'clean_verify_rc': 0, 'verify_rc': 1}
   PASS expect-tamper-detected     expect={'clean_verify_rc': 0, 'verify_rc': 1} observed={'clean_verify_rc': 0, 'verify_rc': 1}
   PASS body-tamper-detected       expect={'clean_verify_rc': 0, 'verify_rc': 1} observed={'clean_verify_rc': 0, 'verify_rc': 1}
   PASS legacy-receipt-refused     expect={'hold_verify_rc': 0, 'counter_rc': 0, 'receipt': True, 'verify_rc': 1} observed={'hold_verify_rc': 0, 'counter_rc': 0, 'receipt': True, 'verify_rc': 1}
   RECEIPT_BINDING_MATCH=7/7
   ```

## Findings

1. **C1 do-nothing control confirmed.** The exact r37 base gate scores `ENV_PIN_CAPTURE_MATCH=2/7` on fresh seed 38201. This reproduces the frozen before/control description at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/claims.md:58-70`; the echoed pin, root move, suppression, and override cells fail in the observed output above.
2. **R37 C1 remains a positive control, not an R38 C1 falsifier.** The old SHA/cut shim predicate scores `CLAIM_PIN_PROVENANCE_MATCH=7/7` on the landed gate at seed 38203. Its own description identifies that SHA-shim predicate at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py:8-19`.
3. **The requested C2/base-gate 7/7 is false for the specified default counter.** It scores 4/7 at seed 38202. The frozen R38 C2 expectations require `counter_rc=0` for hold-receipt, foreign-gate, and legacy-receipt cases (`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/expectations.jsonl:8,10,14`); the base-gate C1 returns 1 in those cases. Receipt verification itself still returned 0 for the hold receipt, and C2 also correctly detected the foreign binding (`verify_foreign_rc=0`, `verify_landed_rc=1`). On the same current default counter, changing only the tested gate to landed produces 7/7 (seed 38204); therefore the aggregate C2 score is not gate-agnostic.
4. **The committed C2 control receipt does use the landed gate, but it is the old-counter control.** `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/receipts/c2-base-s38101.json` records `gate` as `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`, and `subject_counter` as `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py` (matched 0). The paired `c2-after-s38101.json` records the same gate with the r38 C1 subject and matched 7. The frozen claim defines C2's target on the landed gate and its before-state control as the r37 counter (`claims.md:91-116`); it does not establish that the full seven-case score is invariant to switching the gate to the old base gate.

## Limits

No repository source or gate was changed; only this scoped report is written. The requested C2/base-gate result is a measured discrepancy, not a blocker: observed 4/7 rather than 7/7. Counter temp work stayed in fresh `/tmp` directories; no `--receipt` path was supplied to these invocations. No build, lint, or test suite was run.