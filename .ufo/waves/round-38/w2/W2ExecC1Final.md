# W2ExecC1Final

## Verdict
P1 re-derives on final revision `8e93bc916527b3c21f0f702967fa65c3b4c31699`: landed gate 7/7 on both fresh seeds; both base controls 2/7 on both seeds. All six receipts verify.

## Evidence
- Final revision: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` → `8e93bc916527b3c21f0f702967fa65c3b4c31699`.
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show master:tools/research-gate.sh | sha256sum` → `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d`.
- `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/controls/base-gate-r38.sh` → respectively `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d`, `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`, `9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39`.
- Counter: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py`; verifier: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py`. Each run set `C1_TMP=C2_TMP=/tmp/chousa-r38-w2-c1.3f1Lqe` (existing directory); receipts are under `/tmp/chousa-r38-w2-receipts.A22NOm/`.
- Re-executed for each listed gate with seeds `38411` and `38431`: `C1_TMP=/tmp/chousa-r38-w2-c1.3f1Lqe C2_TMP=/tmp/chousa-r38-w2-c1.3f1Lqe python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate G --seed N --receipt R`. `G/N/R` mappings: landed `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` → `38411 /tmp/chousa-r38-w2-receipts.A22NOm/c1-landed-s38411.json`, `38431 /tmp/chousa-r38-w2-receipts.A22NOm/c1-landed-s38431.json`; r37 control `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh` → `38411 /tmp/chousa-r38-w2-receipts.A22NOm/c1-r37-s38411.json`, `38431 /tmp/chousa-r38-w2-receipts.A22NOm/c1-r37-s38431.json`; r38 control `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/controls/base-gate-r38.sh` → `38411 /tmp/chousa-r38-w2-receipts.A22NOm/c1-r38-s38411.json`, `38431 /tmp/chousa-r38-w2-receipts.A22NOm/c1-r38-s38431.json`.
- Per-scenario output, seed 38411, landed gate:
  ```
  PASS hold-plain           expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
  PASS hold-fn-benign       expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
  PASS env-fn-echo-scrub    expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
  PASS env-fn-root-move     expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
  PASS env-fn-suppress      expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
  PASS env-override-missing expect={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'} observed={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'}
  PASS env-override-fake    expect={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'} observed={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'}
  ENV_PIN_CAPTURE_MATCH=7/7
  ```
- Per-scenario output, seed 38411, each control (same output for r37 and r38):
  ```
  PASS hold-plain           expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
  PASS hold-fn-benign       expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
  FAIL env-fn-echo-scrub    expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 1, 'drift_rc': 1, 'drift_line': 'GATE_DRIFT: -GATE_GREP'}
  FAIL env-fn-root-move     expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 1, 'drift_line': 'GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused root supported tallies tally verdict verified'}
  FAIL env-fn-suppress      expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 2, 'pin_file': False, 'echo_lines': -1, 'drift_rc': 2, 'drift_line': ''}
  FAIL env-override-missing expect={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'} observed={'pin_rc': 0, 'pin_file': True, 'refusal': ''}
  FAIL env-override-fake    expect={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'} observed={'pin_rc': 0, 'pin_file': True, 'refusal': ''}
  ENV_PIN_CAPTURE_MATCH=2/7
  ```
- Seed `38431` also produced `ENV_PIN_CAPTURE_MATCH=7/7` on the landed gate and `2/7` on each base gate. Base-control counter commands returned 1 for the expected false predicate; each still wrote its receipt. Verification was then executed for every receipt with `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt R --gate G --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py`.
- Observed verifier output for all six: `VERIFY: ok receipt=c1-landed-s38411.json gate=research-gate.sh counter=c1-count.py`; `VERIFY: ok receipt=c1-landed-s38431.json gate=research-gate.sh counter=c1-count.py`; `VERIFY: ok receipt=c1-r37-s38411.json gate=base-gate-r37.sh counter=c1-count.py`; `VERIFY: ok receipt=c1-r37-s38431.json gate=base-gate-r37.sh counter=c1-count.py`; `VERIFY: ok receipt=c1-r38-s38411.json gate=base-gate-r38.sh counter=c1-count.py`; `VERIFY: ok receipt=c1-r38-s38431.json gate=base-gate-r38.sh counter=c1-count.py`.
- Binding values (for every row, `gate_sha256_pre == gate_sha256_post`; `counter_sha256` is `790407908444b3e99fbf3fba9e9afdcf654d565a5a4304bd4f23daedc3462221`; `expect_sha256` is `d34f17353fec83ed2e7b78b41cebcd2a6d309a85d724dbf1097cf6a17afaf8aa`):

  | Receipt | Seed | gate_sha256_pre = gate_sha256_post | matched/total; predicate_holds | receipt_sha256 |
  |---|---:|---|---|---|
  | `/tmp/chousa-r38-w2-receipts.A22NOm/c1-landed-s38411.json` | 38411 | `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` | 7/7; true | `c0e83ca16bfd811ac0232b9449ed2c0ed11b115a5aac6d8a6908cbf9846cdc9a` |
  | `/tmp/chousa-r38-w2-receipts.A22NOm/c1-landed-s38431.json` | 38431 | `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` | 7/7; true | `d7205ec102e71f485ad3cc10b702c056b2d9a485a97df1b2d9c4b562c9606ecf` |
  | `/tmp/chousa-r38-w2-receipts.A22NOm/c1-r37-s38411.json` | 38411 | `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` | 2/7; false | `e974b1b9fd1e3d2cf04259650bb2d20de626019733599375a1bc79275b39bf0d` |
  | `/tmp/chousa-r38-w2-receipts.A22NOm/c1-r37-s38431.json` | 38431 | `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` | 2/7; false | `c6203e8f4a7c3cddb1987725360c8dc7c8d4d8e4108bba587c0c7cfd327ee923` |
  | `/tmp/chousa-r38-w2-receipts.A22NOm/c1-r38-s38411.json` | 38411 | `9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39` | 2/7; false | `7278a627972d12a903331a52164cf384304cd9c97368cf66856a9e2b0d6a7f2c` |
  | `/tmp/chousa-r38-w2-receipts.A22NOm/c1-r38-s38431.json` | 38431 | `9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39` | 2/7; false | `fffc87d8c39d25b748404c0ae14f3fc168f641efb13656e25f13e648a0a047cf` |

## Findings
1. **Operability:** P1 holds on final bytes for two fresh seed labels (both 7/7, `predicate_holds=true`); the landed gate materially separates from each base control (2/7). Pointers: the exact counter and outputs above; frozen criterion in `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/claims.md` §C1 P1 and Erratum 6.
2. **Calibration:** each receipt binds the expected counter, expectation table and gate hashes, carries the listed self-digest, and passes the strengthened verifier. Pointers: receipt paths and field values above; verifier output above.

## Limits
This re-derivation only measures C1's registered function-export interposition on the capture's `env` call plus override refusal. It does not test the named PATH-resolution / sibling-name vectors or demonstrate independent random replication: see `claims.md` Erratum 6. No blocker; no repository implementation files or tools were changed or installed.
