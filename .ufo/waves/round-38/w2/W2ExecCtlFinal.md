# W2ExecCtlFinal

## Verdict
All three requested final-byte controls reproduced: r37 C1 remains 7/7 on the landed gate; r38 C1 scores 2/7 on the pre-r38 base; the c1-base2 receipt verifies only against its bound base gate.

## Evidence
1. Command: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master`
   Output: `8e93bc916527b3c21f0f702967fa65c3b4c31699`.
2. Command: `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/controls/base-gate-r38.sh`
   Output:
   ```text
   37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
   9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/controls/base-gate-r38.sh
   ```
3. Seed **38451**; receipt `/tmp/chousa-r38-w2-r37c1-38451.json`. Command (both temp variables pointed at the existing `/tmp/chousa-r38-w2-r37c1-38451`):
   ```text
   mkdir -p /tmp/chousa-r38-w2-r37c1-38451 && C1_TMP=/tmp/chousa-r38-w2-r37c1-38451 C2_TMP=/tmp/chousa-r38-w2-r37c1-38451 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38451 --receipt /tmp/chousa-r38-w2-r37c1-38451.json
   ```
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
   ```
4. Seed **38452**; receipt `/tmp/chousa-r38-w2-r38c1-38452.json`. Command (both temp variables pointed at the existing `/tmp/chousa-r38-w2-r38c1-38452`):
   ```text
   mkdir -p /tmp/chousa-r38-w2-r38c1-38452 && C1_TMP=/tmp/chousa-r38-w2-r38c1-38452 C2_TMP=/tmp/chousa-r38-w2-r38c1-38452 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/controls/base-gate-r38.sh --seed 38452 --receipt /tmp/chousa-r38-w2-r38c1-38452.json
   ```
   Observed output:
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
   Counter exited with code 1.
5. Receipt verification, base binding. Command:
   ```text
   python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/receipts/c1-base2-s38003.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/controls/base-gate-r38.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --expectations /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/expectations.jsonl
   ```
   Output: `VERIFY: ok receipt=c1-base2-s38003.json gate=base-gate-r38.sh counter=c1-count.py`; verifier status `EXIT=0`.
6. Receipt verification, landed-gate mismatch. Same command/arguments as item 5, with `--gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`.
   Output: `VERIFY-FAIL: gate-sha256-mismatch`; verifier status `EXIT=1`.

## Findings
1. The r37 C1 control's own predicate remains `CLAIM_PIN_PROVENANCE_MATCH=7/7` against landed gate SHA `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` (evidence 1–3). This is consistent with the control role stated in `corpus/evidence/round38/claims.md`, Erratum 6, lines 229–236.
2. r38 C1 against the true pre-round-38 base SHA `9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39` produced `ENV_PIN_CAPTURE_MATCH=2/7` (evidence 2, 4), the documented base result in Erratum 6, lines 229–232.
3. The `c1-base2-s38003.json` receipt accepts its bound base and refuses the landed gate with the exact `gate-sha256-mismatch` (evidence 5–6). The binding is checked by `corpus/evidence/round38/verify-receipts.py`, lines 173–181.

## Limits
No blockers. This report records only the requested C1 and receipt-binding controls; the generated counter receipts remain under `/tmp` and are not copied here. No repository files other than this report were changed.