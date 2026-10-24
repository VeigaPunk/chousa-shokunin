# ExecC2Rederive

## Verdict
C2 re-derived: the r37 counter scores 0/7; the round-38 counter scores 7/7 at fresh seeds 38221 and 38241, and both new receipts pass independent verification.

## Evidence
Axes: operability (scenario outcomes); calibration (receipt/hash bindings and verifier result).

Temporary directory setup: `mkdir -p /tmp/chousa-r38-c2-rederive` (no output).

Baseline command:
```sh
C2_TMP=/tmp/chousa-r38-c2-rederive python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38221 --receipt /tmp/c2-base-38221.json
```
Observed:
```text
FAIL hold-receipt-verifies      expect={'counter_rc': 0, 'receipt': True, 'verify_rc': 0} observed={'counter_rc': 0, 'receipt': True, 'verify_rc': 1}
FAIL self-rewrite-refused       expect={'counter_rc': 2, 'receipt': False} observed={'counter_rc': 0, 'receipt': True}
FAIL foreign-gate-distinguished expect={'counter_rc': 0, 'receipt': True, 'verify_foreign_rc': 0, 'verify_landed_rc': 1} observed={'counter_rc': 0, 'receipt': True, 'verify_foreign_rc': 1, 'verify_landed_rc': 1}
FAIL counter-tamper-detected    expect={'clean_verify_rc': 0, 'verify_rc': 1} observed={'clean_verify_rc': 1, 'verify_rc': 'not-measured'}
FAIL expect-tamper-detected     expect={'clean_verify_rc': 0, 'verify_rc': 1} observed={'clean_verify_rc': 1, 'verify_rc': 'not-measured'}
FAIL body-tamper-detected       expect={'clean_verify_rc': 0, 'verify_rc': 1} observed={'clean_verify_rc': 1, 'verify_rc': 'not-measured'}
FAIL legacy-receipt-refused     expect={'hold_verify_rc': 0, 'counter_rc': 0, 'receipt': True, 'verify_rc': 1} observed={'hold_verify_rc': 1, 'counter_rc': 0, 'receipt': True, 'verify_rc': 1}
RECEIPT_BINDING_MATCH=0/7
```

After command, seed 38221:
```sh
C2_TMP=/tmp/chousa-r38-c2-rederive python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38221 --receipt /tmp/c2-after-38221.json
```
Observed:
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

After command, seed 38241:
```sh
C2_TMP=/tmp/chousa-r38-c2-rederive python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38241 --receipt /tmp/c2-after-38241.json
```
Observed:
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

Both verifier invocations used:
```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/c2-after-38221.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py
# VERIFY: ok receipt=c2-after-38221.json gate=research-gate.sh counter=c2-count.py
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/c2-after-38241.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py
# VERIFY: ok receipt=c2-after-38241.json gate=research-gate.sh counter=c2-count.py
```

Receipt bindings read from `/tmp/c2-base-38221.json`, `/tmp/c2-after-38221.json`, and `/tmp/c2-after-38241.json`:
- Common to all: counter `corpus/evidence/round38/c2-count.py`; `counter_sha256=bc325cf4785f62ef3eeca3ea2d8a61094822a0c4345f07ae314c408cf6507818`; expectations `corpus/evidence/round38/expectations.jsonl`; `expect_sha256=7cd5d824b4f927329927679f53c747edff0b6c405ff98d1701619519b2eaebc9`; gate `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`; `gate_sha256=gate_sha256_pre=gate_sha256_post=37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d`; subject counter `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py`; total 7.
- Seed 38221 baseline: `matched=0`, `predicate_holds=false`, `receipt_sha256=98df6c64e8ff1c04fc5db9326ae4d53f078b4558b6305cfecbe04167c0da86c7`.
- Seed 38221 after: `matched=7`, `predicate_holds=true`, `receipt_sha256=300200884e11fdf868d74cb90f26514088a06377e5c56d355001fc8be9de8e3c`.
- Seed 38241 after: `matched=7`, `predicate_holds=true`, `receipt_sha256=363dbe2f1ef36eafa7b4866fa5801172d2d456c6adbe9215005cd31ab9731e3a`.

## Findings
1. **Baseline discrimination reproduced:** the r37 counter failed all seven round-38 scenarios (0/7); `/tmp/c2-base-38221.json` records the r37 subject counter, seed 38221, and `matched=0`.
2. **Round-38 predicate reproduced twice:** all seven named scenarios passed on both fresh seeds, with the gate's measured pre/post SHA-256 equal in each receipt; see `/tmp/c2-after-38221.json` and `/tmp/c2-after-38241.json` and the two observed `RECEIPT_BINDING_MATCH=7/7` outputs above.
3. **Independent receipt verification succeeded against HEAD bytes only:** `verify-receipts.py` returned `VERIFY: ok` for both after receipts while C2 counter SHA was `bc325cf4785f62ef3eeca3ea2d8a61094822a0c4345f07ae314c408cf6507818` and expectations SHA was `7cd5d824…`, binding the specified gate (commands above).
4. **Subsequent calibration drift reported:** `RevCounterC2.md` and a later SimCounters alert report that the working-tree expectations table changed from HEAD SHA `7cd5d824…` to `c986c5fd…`, and C2 counter changed from the receipt-bound `bc325cf4…` to `5ae3bd8c…`; committed receipts reportedly now fail against changed bytes. My two temporary after-receipts bind the HEAD hashes above; their earlier `VERIFY: ok` results are against HEAD bytes only, not the current working tree. See `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/w1/RevCounterC2.md` and the SimCounters in-wave alert for the review evidence.


## Limits
Only C2 was re-derived in this assignment. The baseline receipt was not independently passed through `verify-receipts.py`; the two after receipts returned `VERIFY: ok` against C2 counter SHA `bc325cf4…` and expectations SHA `7cd5d824…` only, before the subsequently reported working-tree changes. I did not rerun verification against the changed files. This seat changed no implementation or expectations files and installed no tools.