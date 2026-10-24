# MutCounterC2

## Verdict
All four counter-side C2 mutants are killed (baseline 7/7 → M1 6/7, M2 6/7, M3 1/7, M4 1/7), restored bytes return 7/7, and C1's own predicate stays 7/7 on the landed gate under every mutant.

## Evidence

Everything ran on pinned dispatched bytes, never on the live working tree:
```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show master:corpus/evidence/round38/{c2-count.py,verify-receipts.py,expectations.jsonl}  -> /tmp/r38-pin/round38/
  bc325cf4785f62ef3eeca3ea2d8a61094822a0c4345f07ae314c408cf6507818  c2-count.py
  756f186c3487461b9c29de5ebbb4b91392706ecc4b5ff8f3a83d482fcaf27605  verify-receipts.py
  7cd5d824b4f927329927679f53c747edff0b6c405ff98d1701619519b2eaebc9  expectations.jsonl
$ git show master:corpus/evidence/round38/c1-count.py | sha256sum
  da1d915b51801fd6d25ebf857318afc87c08c4876dd25fe4055fdede1ede3f74   (= subject copy /tmp/r38-mutc2/pristine/c1-count.py)
$ sha256sum .../tools/research-gate.sh
  37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d   (unchanged after every probe)
```
Mutants are byte-identical reconstructions in `/tmp/r38-mutc2/mut/<id>/c1-count.py` (each dir also holds the dispatched `expectations.jsonl`):
```
ae2079b8aeff43f0c79f7ca5d3660aa4eeaab6220259858676920133164609d6  M1  post-run gate hash only
f9a76fa94b852a9a9053ac44f903306c2d4c7bbcb86fc3e874bd07e9f98d9f2f  M2  drop the pre!=post refusal
7aec8256d09d800cf97c2966a4b988cf36839d1864fef3b8206bdb9e539aa714  M3  drop counter_sha256
dd238cb5da63a76b8e28e8307362f706243c6171600d318912e2c9d248a8262e  M4  drop receipt_sha256
da1d915b51801fd6d25ebf857318afc87c08c4876dd25fe4055fdede1ede3f74  restored M1 (later)
```
Exact hunks (`diff -u` pristine vs mutant):
```
M1: -        gate_sha_pre = sha256_file(gate)
    ...      -            if sha256_file(gate) != gate_sha_pre: ... return 2
                 gate_sha_post = sha256_file(gate)
    +        gate_sha_pre = gate_sha_post
M2: -            if sha256_file(gate) != gate_sha_pre: ... return 2      (pre and post still measured)
M3: -            "counter_sha256": sha256_file(os.path.abspath(__file__)),
M4: -        receipt["receipt_sha256"] = receipt_digest(receipt)
```
Detector = the dispatched c2 counter, pinned, `--counter <mutant>`:
```
$ C2_TMP=/tmp/r38-mutc2/pt-base python3 /tmp/r38-pin/round38/c2-count.py \
    --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh \
    --counter /tmp/r38-mutc2/pristine/c1-count.py --seed 38295
  RECEIPT_BINDING_MATCH=7/7   exit 0
$ ... --counter mut/M1/c1-count.py --seed 38296
  FAIL self-rewrite-refused  expect={'counter_rc': 2, 'receipt': False} observed={'counter_rc': 0, 'receipt': True}
  (rest PASS)  receipt p-M1.json: matched=6 total=7 holds=False   [earlier unpinned rerun, seed 38282: c2_exit=1]
$ ... --counter mut/M2/c1-count.py --seed 38297
  FAIL self-rewrite-refused  expect={'counter_rc': 2, 'receipt': False} observed={'counter_rc': 0, 'receipt': True}
  RECEIPT_BINDING_MATCH=6/7   exit 1
$ ... --counter mut/M3/c1-count.py --seed 38298
  FAIL hold-receipt-verifies  expect={'counter_rc': 0, 'receipt': True, 'verify_rc': 0} observed={'counter_rc': 0, 'receipt': True, 'verify_rc': 1}
  FAIL foreign-gate-distinguished  ... observed={'verify_foreign_rc': 1, 'verify_landed_rc': 1}
  FAIL counter-/expect-/body-tamper-detected  observed={'clean_verify_rc': 1, 'verify_rc': 'not-measured'} (x3)
  FAIL legacy-receipt-refused  observed={'hold_verify_rc': 1, 'counter_rc': 0, 'receipt': True, 'verify_rc': 1}
  RECEIPT_BINDING_MATCH=1/7   exit 1
$ ... --counter mut/M4/c1-count.py --seed 38299   -> same seven lines, RECEIPT_BINDING_MATCH=1/7, exit 1
$ cp pristine/c1-count.py mut/M1/c1-count.py   (hash da1d915b..., == dispatched)
$ ... --counter mut/M1/c1-count.py --seed 38300
  RECEIPT_BINDING_MATCH=7/7   exit 0
```
Kill mechanisms probed directly (finite, named tokens):
```
M1 vs FRESH self-rewrite shim (shim e7cae6fe..., seed 38291):
  ENV_PIN_CAPTURE_MATCH=7/7, exit 0; receipt gate_pre=gate_post=37e2b996...; matched=7 holds=True
  verify-receipts.py --receipt M1-f1c-receipt.json --gate <rewritten shim> --counter mut/M1/... -> "VERIFY: ok" exit 0
DISPATCHED counter vs FRESH self-rewrite shim (shim e2c4d39e..., seed 38301):
  "c1-count: gate bytes changed across the run (pre e2c4d39eeeed5584 != current) — no receipt published" exit 2, receipt absent
M2 vs FRESH self-rewrite shim (shim 2b51a1a4..., seed 38290):
  receipt gate_pre=2b51a1a4... != gate_post=37e2b996...; verify -> "VERIFY-FAIL: gate-sha-changed-across-run" exit 1
M3 honest receipt (seed 38289): keys_have_counter=False -> "VERIFY-FAIL: missing-field counter_sha256" exit 1
M4 honest receipt (seed 38289): keys_have_receipt=False -> "VERIFY-FAIL: missing-field receipt_sha256" exit 1
```
C1's own predicate is untouched by every mutant (same counters, landed gate, seed 38286):
```
pristine/M1/M2/M3/M4 each: ENV_PIN_CAPTURE_MATCH=7/7   exit 0
```

## Findings
1. Every requested mutant is killed at the expected cell: M1/M2 by `self-rewrite-refused`, M3/M4 by `hold-receipt-verifies` first (then all receipt-consuming cells). Baseline pristine 7/7 rules out a broken detector. (pointer: baseline seed 38295 vs mutant seeds 38296-38299, `/tmp/r38-mutc2/p-{base,M1..M4}.json`).
2. M1 is a genuine F1 forgery, not just a score dip: a gate whose first invocation ran different bytes still gets `gate_sha256_pre == gate_sha256_post == 37e2b996...`, `matched=7`, and `VERIFY: ok` from `verify-receipts.py`. The verifier cannot see it; only the counter's own refusal cell stands between F1 and an accepted receipt (seed 38291 vs dispatched refusal at seed 38301).
3. Gate-identity defence is exactly one cell wide: with M1 or M2 the other six scenarios (including the foreign-gate and three tamper cells) still pass. `self-rewrite-refused` is load-bearing for the whole `gate_sha256_pre` binding family.
4. M3/M4 collapse 6/7 cells, not one, because every scenario presupposes a verifying honest receipt (`clean_verify_rc`/`hold_verify_rc`/`verify_foreign_rc`). A single dropped field is scored as total receipt-shape failure (1/7); the predicate still fails closed, but the score cannot localize which binding broke.
5. Calibration specificity finding (shipped detector, not mutants): `doctor()` rewrites a bound field without re-stamping, so `counter-tamper-detected` and `expect-tamper-detected` observe `VERIFY-FAIL: receipt-self-digest`, never the named mismatch. Re-stamped control: `VERIFY-FAIL: counter-sha256-mismatch` (exit 1). The re-derivation exists (C2 claim holds) but scenarios 4-5 test only the self-digest layer — a coverage finding, not a contract change.
6. Live-edit drift inside the lane: during this probe `corpus/evidence/round38/` changed under me — `c1-count.py` da1d915b → 1262cb4c (00:54:12), `c2-count.py` bc325cf4 → 6aa80098, `verify-receipts.py` 756f186c → b63e7e20, `expectations.jsonl` 7cd5d824 → d34f1735 (00:55:06). One pre-pin restored rerun (seed 38292) scored 1/7 purely from that drift; it is discarded and replaced by the pinned rerun (seed 38300, 7/7). Verdicts above bind only the pinned dispatched bytes listed in Evidence.
7. No lane writes by this seat: only `/tmp/r38-mutc2` and this report. Scratch restoration is byte-exact to dispatched `da1d915b...` and returned 7/7; the working-tree change to `1262cb4c` is a sibling's write, evidenced by mtime 00:54:12 and my unchanged read-only command set.

## Limits
- One mutant per requested point, single seed each (38281-38301); no repeated sampling, no fuzzing of `verify-receipts.py` recount/order checks.
- The working-tree (`1262cb4c`/`6aa80098`/`b63e7e20`/`d34f1735`) variants were not exercised; they changed mid-wave and are outside the frozen claims.
- `/tmp/r38-mutc2` is disposable scratch; no tool installs were needed.
