# W2CritVacuous

## Verdict
Census/value/flag/predicate guards refused the requested corruptions; benign ordering verified; deleting C2's refusal-label observation still verified under the now-named equality-only limit.

## Evidence
Axes: **operability** (runnable counter/verifier commands) and **calibration** (what an accepted receipt actually establishes).

Initial revision command: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` → `8e93bc916527b3c21f0f702967fa65c3b4c31699`.

Two verifier byte states were observed; the complete results below were rerun against the second state after the parent's mid-wave notification:
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 8e93bc916527b3c21f0f702967fa65c3b4c31699:corpus/evidence/round38/verify-receipts.py | sha256sum` → `b63e7e200b88022f6747e4b628cb6b251187ad95f5b33d2b6b4b14e08d5cf952` (dispatch bytes).
- `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py` → `33c7c87e7a5f3eb86cd8db3bccaf88c0d8fbd542db3cd5f05a6568d8f2182fdb` immediately before AND after the final attack batch (Errata 9/10 bytes).

Fresh counter commands (the temporary directory already existed):
```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin
E="$L/corpus/evidence/round38"
T=/tmp/chousa-r38-w2-vacuous.9zNPOu
/usr/bin/env PATH=/usr/bin:/bin C1_TMP="$T" C2_TMP="$T" /usr/bin/python3 "$E/c1-count.py" --gate "$L/tools/research-gate.sh" --seed 38471 --receipt "$T/c1-fresh-s38471.json"
/usr/bin/env PATH=/usr/bin:/bin C1_TMP="$T" C2_TMP="$T" /usr/bin/python3 "$E/c2-count.py" --gate "$L/tools/research-gate.sh" --seed 38473 --receipt "$T/c2-fresh-s38473.json"
```
Observed: `ENV_PIN_CAPTURE_MATCH=7/7` and `RECEIPT_BINDING_MATCH=7/7`; both exited 0.

Executed final-byte mutation commands, concurrently, each exiting 0:
```sh
/usr/bin/python3 /tmp/chousa-r38-w2-vacuous.9zNPOu/census-attacks.py --family c1 --source /tmp/chousa-r38-w2-vacuous.9zNPOu/c1-fresh-s38471.json
/usr/bin/python3 /tmp/chousa-r38-w2-vacuous.9zNPOu/census-attacks.py --family c2 --source /tmp/chousa-r38-w2-vacuous.9zNPOu/c2-fresh-s38473.json
```
The temporary harness deep-copies the honest receipt for each attack, recomputes `receipt_sha256 = sha256((json.dumps(body_without_digest, indent=2, sort_keys=True) + "\n").encode())`, and invokes:
`/usr/bin/python3 "$E/verify-receipts.py" --receipt "$T/<family>-<case>.json" --gate "$L/tools/research-gate.sh" --counter "$E/<family>-count.py"`.
It preserves serialized insertion order when writing mutations, so the key-permutation test genuinely changes JSON key order. Full command/output records: `/tmp/chousa-r38-w2-vacuous.9zNPOu/c1-attack-results.json` and `/tmp/chousa-r38-w2-vacuous.9zNPOu/c2-attack-results.json`.

Exact observed labels (every refusal below exited 1; every `VERIFY: ok` exited 0):

| Case / mutation | C1 output | C2 output |
|---|---|---|
| `honest` | `VERIFY: ok` | `VERIFY: ok` |
| `duplicate-eight`: append first frozen row; 8 rows / 7 unique ids | `VERIFY-FAIL: scenario-census-mismatch` | `VERIFY-FAIL: scenario-census-mismatch` |
| `duplicate-missing-seven`: replace last row by first; 7 rows / 6 unique ids | `VERIFY-FAIL: scenario-census-mismatch` | `VERIFY-FAIL: scenario-census-mismatch` |
| `duplicate-missing-foreign-eight`: previous case plus a foreign id; 8 rows / 7 unique ids | `VERIFY-FAIL: scenario-census-mismatch` | `VERIFY-FAIL: scenario-census-mismatch` |
| `reorder`: reverse scenario list | `VERIFY: ok` | `VERIFY: ok` |
| `expect-key-permutation`: reverse first expect dict's keys | `VERIFY: ok` | `VERIFY: ok` |
| `expect-value-change`: change first expect value | `VERIFY-FAIL: expect-tie-mismatch hold-plain` | `VERIFY-FAIL: expect-tie-mismatch hold-receipt-verifies` |
| `ok-flip`: true → false, retaining original totals | `VERIFY-FAIL: ok-rederivation-mismatch hold-plain` | `VERIFY-FAIL: ok-rederivation-mismatch hold-receipt-verifies` |
| `drop-observed-equality`: delete `drift_line` / `receipt`, retaining ok=true | `VERIFY-FAIL: ok-rederivation-mismatch hold-plain` | `VERIFY-FAIL: ok-rederivation-mismatch hold-receipt-verifies` |
| `other-family-predicate`: swap to the other family's frozen predicate string | `VERIFY-FAIL: predicate-mismatch` | `VERIFY-FAIL: predicate-mismatch` |
| `drop-observed-label`: delete `counter-tamper-detected.observed.verify_fail` | Not applicable | `VERIFY: ok` |

Key-order evidence: C1 keys changed from `[drift_line, drift_rc, echo_lines, pin_file, pin_rc]` to `[pin_rc, pin_file, echo_lines, drift_rc, drift_line]`; C2 from `[receipt, verify_rc]` to `[verify_rc, receipt]`. Both reported `dict_equal=true` and `digest_equal=true`.

Strongest counterexample command (also executed by the harness):
```sh
/usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/chousa-r38-w2-vacuous.9zNPOu/c2-drop-observed-label.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py
```
Observed: `VERIFY: ok receipt=c2-drop-observed-label.json gate=research-gate.sh counter=c2-count.py`, exit 0. Affected row still has `expect.verify_fail_contains="counter-sha256-mismatch"`, `observed.clean_verify_rc=0`, `observed.verify_rc=1`, and `ok=true`, but NO `observed.verify_fail`; receipt retains `matched=7`, `predicate_holds=true`. Applying the counter's `_contains` scoring to that row yields false.

## Findings
1. **Calibration: independent scoring is equality-only, not counter-equivalent.** Final `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py:180-185` explicitly skips `_contains`; `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py:258-265` actually tests those assertions. Deleting the named-refusal evidence therefore survives a correct re-seal. This does NOT show the honest counter missed the label—it produced it before mutation—and does not establish execution/authorship forgery. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/claims.md:268-279` now names this producer-side boundary. **Smallest safe correction if independent re-derivation is required:** apply the counter's existing `_contains` scoring in the verifier instead of skipping those keys; otherwise retain the explicit limitation and do not describe verification as re-deriving every counter assertion. Whether the narrowing is admissible is for the canonical judge, not this seat.
2. **Operability/calibration: census and semantic equality behaved as intended.** `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py:149-185` grounds predicate, exact-id census, dict-value equality, and ok re-derivation. Both an overfull list and a same-length duplicate/missing list refused; order changes were harmless. No correction indicated for these tested guards.
3. **Census wording was covered without weakening the attack.** The frozen family has seven ids (`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/expectations.jsonl:1-14`). Exactly one duplicate and one missing id produces seven rows, not eight, unless another extra row exists. The batch separately exercised the eight-row duplicate, the seven-row duplicate/missing, and an eight-row duplicate/missing/foreign-id combination; all refused with the census label.

## Limits
- Scope is the assigned local receipt mutations; no admission, integration, source edits, or broader gate claims. Only this report and files under the newly created `/tmp` directory were written.
- The initial C2 attempt, seed 38472, hit the tool's 50-second deadline; it is not a counter-failure finding and was not used as an attack source. The synchronous fresh-seed 38473 run completed successfully. An initial temporary helper failed on a string-valued expect; it was corrected only under `/tmp`, and both complete final batches exited 0.
- Final results bind verifier digest `33c7c87e…`, not an inferred later commit. No claim that the full batch ran on the dispatch digest. No tools installed or updated.
