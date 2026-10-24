# W2CritDoNothingFinal
## Verdict
No scoped counterexample reproduced on `8e93bc916527b3c21f0f702967fa65c3b4c31699`; the four requested do-nothing/census barriers held.

## Evidence
Axes: **operability** (C1 discrimination), **calibration** (C2 discrimination, hard-seven and exact census).
All counter commands below used `env -i PATH=/usr/bin:/bin HOME=/home/vgpnk LANG=C.UTF-8 C1_TMP=/tmp/chousa-r38-w2-donothing-Fc95eG C2_TMP=/tmp/chousa-r38-w2-donothing-Fc95eG`; verifier commands used the same clean prefix without the two temp variables. Working directory was `/tmp/chousa-r38-w2-donothing-Fc95eG`. The existing temp parent was created with `mktemp -d /tmp/chousa-r38-w2-donothing-XXXXXX`.

Entry identity, re-executed:
```text
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master
8e93bc916527b3c21f0f702967fa65c3b4c31699
```
Concurrent worktree edits were isolated by extracting the requested commit with `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 8e93bc916527b3c21f0f702967fa65c3b4c31699:<member>` into `/tmp/chousa-r38-w2-donothing-Fc95eG/frozen/round38/`, its sibling `round37/`, and `frozen-gate/`. Observed SHA256s (also matched the initial live bytes):
```text
research-gate.sh 37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d
round38/c1-count.py 790407908444b3e99fbf3fba9e9afdcf654d565a5a4304bd4f23daedc3462221
round38/c2-count.py 414a7a10571263e781137fcbb0fb4e16bd9dbb9a44fda4931d9fe4d67cc403e3
round38/verify-receipts.py b63e7e200b88022f6747e4b628cb6b251187ad95f5b33d2b6b4b14e08d5cf952
round38/expectations.jsonl d34f17353fec83ed2e7b78b41cebcd2a6d309a85d724dbf1097cf6a17afaf8aa
round37/c1-count.py eec810050dd174e3b6e8401efab35df2a18e310a27c212eb775e96c55830ba29
```

**1. Original r37 pipeline against the landed gate — seed 38981; exit 1.**
```text
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --seed 38981 --receipt /tmp/chousa-r38-w2-donothing-Fc95eG/c2-r37-s38981.json
RECEIPT_BINDING_MATCH=0/7
```
All seven rows were FAIL. The three tamper rows recorded `clean_verify_out: 'VERIFY-FAIL: missing-field counter_sha256'` and `verify_rc: 'not-measured'`; self-rewrite recorded `{'counter_rc': 0, 'receipt': True}`.
Exact-byte immutable replay, seed 38993; exit 1:
```text
python3 /tmp/chousa-r38-w2-donothing-Fc95eG/frozen/round38/c2-count.py --gate /tmp/chousa-r38-w2-donothing-Fc95eG/frozen-gate/research-gate.sh --counter /tmp/chousa-r38-w2-donothing-Fc95eG/frozen/round37/c1-count.py --seed 38993 --receipt /tmp/chousa-r38-w2-donothing-Fc95eG/c2-r37-immutable-s38993.json
RECEIPT_BINDING_MATCH=0/7
```
Receipt fields: `"matched": 0, "total": 7, "predicate_holds": false`.

**2. Both base gates under C1 — seeds 38982/38983; each exit 1.**
```text
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 38982 --receipt /tmp/chousa-r38-w2-donothing-Fc95eG/c1-base-r37-s38982.json
ENV_PIN_CAPTURE_MATCH=2/7
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/controls/base-gate-r38.sh --seed 38983 --receipt /tmp/chousa-r38-w2-donothing-Fc95eG/c1-base-r38-s38983.json
ENV_PIN_CAPTURE_MATCH=2/7
```
Both passed only `hold-plain` and `hold-fn-benign`; echo attack observed `echo_lines: 1` and `GATE_DRIFT: -GATE_GREP`. Both receipts have `"predicate_holds": false`.

**3. Six-row expectation table cannot pass; both hard-seven guards exercised.**
`table-only/c1-count.py` is byte-identical to the frozen C1 counter; its adjacent table contains precisely the first six frozen C1 rows (omits `env-override-fake`). Seed 38985; exit 2, no predicate printed and no receipt:
```text
python3 /tmp/chousa-r38-w2-donothing-Fc95eG/table-only/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38985 --receipt /tmp/chousa-r38-w2-donothing-Fc95eG/c1-table-six-s38985.json
c1-count: expectations missing for: env-override-fake
```
Stronger attack: `six-order/c1-count.py` additionally omits that ID from `SCENARIO_ORDER`; its hard-seven scoring expression is untouched. Six genuine scenarios passed; seed 38994, exit 1:
```text
python3 /tmp/chousa-r38-w2-donothing-Fc95eG/six-order/c1-count.py --gate /tmp/chousa-r38-w2-donothing-Fc95eG/frozen-gate/research-gate.sh --seed 38994 --receipt /tmp/chousa-r38-w2-donothing-Fc95eG/c1-six-frozen-s38994.json
ENV_PIN_CAPTURE_MATCH=6/6
```
Receipt fields: `"matched": 6, "total": 6, "predicate": "ENV_PIN_CAPTURE_MATCH=7/7", "predicate_holds": false`.
C2 analogue: `six-c2/c2-count.py` omits only `legacy-receipt-refused` from the order; adjacent table retains all seven C1 rows and six C2 rows; adjacent C1 counter is unchanged. `VERIFY` points at the frozen verifier. All six genuine C2 scenarios passed; seed 38992, exit 1:
```text
python3 /tmp/chousa-r38-w2-donothing-Fc95eG/six-c2/c2-count.py --gate /tmp/chousa-r38-w2-donothing-Fc95eG/frozen-gate/research-gate.sh --seed 38992 --receipt /tmp/chousa-r38-w2-donothing-Fc95eG/c2-six-frozen-s38992.json
RECEIPT_BINDING_MATCH=6/6
```
Receipt fields: `"matched": 6, "total": 6, "predicate": "RECEIPT_BINDING_MATCH=7/7", "predicate_holds": false`.
C2 using the unchanged counter with the six-C1-row subject also scored `RECEIPT_BINDING_MATCH=1/7`, seed 38989 (receipt `/tmp/chousa-r38-w2-donothing-Fc95eG/c2-six-c1-table-s38989.json`), not a passing predicate.

**4. Re-sealed frozen-six-plus-one-bogus census — rejected by the named check.**
Honest receipt generated with the original C1 command on seed 38984 printed `ENV_PIN_CAPTURE_MATCH=7/7` (exit 0). The doctor changes only the last scenario ID, `env-override-fake` → `bogus-not-frozen`, and recomputes `receipt_sha256 = SHA256(json.dumps(body_without_digest, indent=2, sort_keys=True) + "\n")`. It retains all public bindings, `matched=7`, `total=7`, `predicate_holds=true` and the other six frozen IDs.
```text
python3 /tmp/chousa-r38-w2-donothing-Fc95eG/frozen/round38/verify-receipts.py --receipt /tmp/chousa-r38-w2-donothing-Fc95eG/c1-landed-s38984.json --gate /tmp/chousa-r38-w2-donothing-Fc95eG/frozen-gate/research-gate.sh --counter /tmp/chousa-r38-w2-donothing-Fc95eG/frozen/round38/c1-count.py
VERIFY: ok receipt=c1-landed-s38984.json gate=research-gate.sh counter=c1-count.py
python3 /tmp/chousa-r38-w2-donothing-Fc95eG/frozen/round38/verify-receipts.py --receipt /tmp/chousa-r38-w2-donothing-Fc95eG/c1-six-plus-bogus-s38984.json --gate /tmp/chousa-r38-w2-donothing-Fc95eG/frozen-gate/research-gate.sh --counter /tmp/chousa-r38-w2-donothing-Fc95eG/frozen/round38/c1-count.py
VERIFY-FAIL: scenario-census-mismatch
```
Honest verify exit 0; doctor verify exit 1. The same refusal was also reproduced against the original verifier path before the immutable replay.

## Findings
1. **No do-nothing escape reproduced (calibration).** Original and immutable r37 pipelines both scored exactly 0/7. This grounds `claims.md:106-116,193-201`; the control is the old counter pipeline, not the old gate.
2. **No C1 control collapse reproduced (operability).** Both named base gates remain exactly 2/7. Pointers: the two absolute control paths above; `claims.md:229-236` and frozen `expectations.jsonl:1-7`.
3. **No six-scenario passing predicate reproduced (both axes).** Table-only truncation refuses early; order-plus-table truncation reaches 6/6 but returns exit 1 with `predicate_holds=false` for both counters. Pointers on the audited commit: `corpus/evidence/round38/c1-count.py:226-231,267-271` and `c2-count.py:298-303,340-343`.
4. **No re-sealed census escape reproduced (calibration).** The honest positive control verifies, while the six-plus-bogus body reaches `scenario-census-mismatch`, not a digest refusal. Pointer: frozen `corpus/evidence/round38/verify-receipts.py:142-149`.
Smallest safe correction: none required by these four tests; operationally, pin review inputs to immutable commit bytes while integration writes the checkout. No canonical judgment or axis score is issued here.

## Limits
The live gate changed during seed 38991; the run correctly refused with exit 2, printed `c2-count: gate bytes changed across the run (pre 37e2b9968706adab != current) — no receipt published`, and left no `/tmp/chousa-r38-w2-donothing-Fc95eG/c2-six-order-frozen-s38991.json`. Its command was the C2 six-order invocation above with the live gate `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` and seed 38991. That interrupted run is not evidence about the frozen predicate; immutable reruns 38992–38994 supply that evidence.
All seeds used were 38981–38994; intermediate repeats 38986/38988/38990 agreed with their reported counterparts. Seed 38987's direct r37 counter printed `CLAIM_PIN_PROVENANCE_MATCH=7/7`, then its receipt was refused as `VERIFY-FAIL: missing-field counter_sha256`; old C1 success is not C2 success. Scope is the four assigned checks, not authorship, hostile observation forgery, or all ambient-environment vectors. No tools installed; no lane/fleet/index changes made other than this report; all generated fixtures and receipts remain under the named `/tmp` directory.
