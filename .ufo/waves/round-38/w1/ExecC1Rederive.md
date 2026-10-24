# ExecC1Rederive

## Verdict
C1's before/after behavior re-derived: base gate 2/7; landed gate 7/7 on both fresh seeds. Both after-receipts verify. Axes: operability (primary) and calibration (receipt verification only).

## Evidence
Commands were run from `/home/vgpnk/Projects/shokunin/chousa-shokunin`; each `C1_TMP` directory existed before its counter run.

```sh
C1_TMP=/tmp/chousa-c1-base-38211 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 38211 --receipt /tmp/c1-base-38211.json
```

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
Counter exited 1, as observed for this below-predicate baseline.

```sh
C1_TMP=/tmp/chousa-c1-current-38211 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38211 --receipt /tmp/c1-current-38211.json
```

```text
PASS hold-plain           expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
PASS hold-fn-benign       expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
PASS env-fn-echo-scrub    expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
PASS env-fn-root-move     expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
PASS env-fn-suppress      expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
PASS env-override-missing expect={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'} observed={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'}
PASS env-override-fake    expect={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'} observed={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'}
ENV_PIN_CAPTURE_MATCH=7/7
```

```sh
C1_TMP=/tmp/chousa-c1-current-38231 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38231 --receipt /tmp/c1-current-38231.json
```

```text
PASS hold-plain           expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
PASS hold-fn-benign       expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
PASS env-fn-echo-scrub    expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
PASS env-fn-root-move     expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
PASS env-fn-suppress      expect={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'} observed={'pin_rc': 0, 'pin_file': True, 'echo_lines': 0, 'drift_rc': 0, 'drift_line': 'GATE_DRIFT: none'}
PASS env-override-missing expect={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'} observed={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'}
PASS env-override-fake    expect={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'} observed={'pin_rc': 2, 'pin_file': False, 'refusal': 'ENV_PROVENANCE'}
ENV_PIN_CAPTURE_MATCH=7/7
```

Receipt bindings read from the three generated receipts:

| Run | `gate_sha256` | `counter_sha256` | `expect_sha256` | `receipt_sha256` | `predicate_holds` |
|---|---|---|---|---|---|
| base, seed 38211 | `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` | `da1d915b51801fd6d25ebf857318afc87c08c4876dd25fe4055fdede1ede3f74` | `7cd5d824b4f927329927679f53c747edff0b6c405ff98d1701619519b2eaebc9` | `91456581e53ee6c514f2d8487082f35d794a335fa761388bbec5f662e708d9ee` | false |
| current, seed 38211 | `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` | `da1d915b51801fd6d25ebf857318afc87c08c4876dd25fe4055fdede1ede3f74` | `7cd5d824b4f927329927679f53c747edff0b6c405ff98d1701619519b2eaebc9` | `d62be3ae48e57d14380a3a95388b383c4816021f964af224412a9b863ab2bb1e` | true |
| current, seed 38231 | `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` | `da1d915b51801fd6d25ebf857318afc87c08c4876dd25fe4055fdede1ede3f74` | `7cd5d824b4f927329927679f53c747edff0b6c405ff98d1701619519b2eaebc9` | `ae4d99455b479435c8aebbcddc83fb23f939ba4514eb9581b8350bbae06b10c1` | true |

Re-executed verification commands and observed outputs:

```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/c1-current-38211.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py
# VERIFY: ok receipt=c1-current-38211.json gate=research-gate.sh counter=c1-count.py
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/c1-current-38231.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py
# VERIFY: ok receipt=c1-current-38231.json gate=research-gate.sh counter=c1-count.py
```

## Findings
1. Fresh-seed baseline reproduces the frozen 2/7 separation: only `hold-plain` and `hold-fn-benign` pass; the function and override attack cells fail as expected for the pre-round gate. Pointer: `corpus/evidence/round38/claims.md:25-70`; fixture expectations: `corpus/evidence/round38/expectations.jsonl:1-7`.
2. The landed gate reproduces the frozen predicate on two fresh seeds (38211, 38231), with `predicate_holds=true` and matching gate hash pre/post in both receipts. Pointer: `corpus/evidence/round38/claims.md:37-56`; generated receipts `/tmp/c1-current-38211.json` and `/tmp/c1-current-38231.json`.
3. Both after-receipts pass the requested verifier, which independently accepts their bindings to the landed gate and C1 counter. Pointer: `corpus/evidence/round38/verify-receipts.py`; exact command/output above.

## Limits
This re-derives C1 only; it is not a C2 evaluation. C1's frozen limits remain: caller-exported `bash` interposition, loader environment/`LD_PRELOAD`, `SHELLOPTS=noexec`, and provenance from a binary that lies about `--version` are outside the claim (`claims.md:130-146`). Counter receipts are in `/tmp`; the report preserves the exact requested hashes and observed output. Only this scoped report was written; no implementation files changed.
