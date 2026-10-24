# W2MutCounterFinal

## Verdict
All four counter mutants are killed on the final tip bytes (baseline 7/7 → M1 6/7, M2 6/7, M3 1/7, M4 1/7); catchers `self-rewrite-refused` (M1, M2) and `hold-receipt-verifies` (M3, M4); C1's own predicate stays 7/7 under every mutant; restored bytes return 7/7.

## Evidence

Bytes pinned read-only from lane tip `8e93bc9` (`git -C …/chousa-shokunin rev-parse master`), working tree == master for all four at pin time; scratch `/tmp/r38-w2-mutcf`:
```
790407908444b3e99fbf3fba9e9afdcf654d565a5a4304bd4f23daedc3462221  c1-count.py
414a7a10571263e781137fcbb0fb4e16bd9dbb9a44fda4931d9fe4d67cc403e3  c2-count.py (detector)
b63e7e200b88022f6747e4b628cb6b251187ad95f5b33d2b6b4b14e08d5cf952  verify-receipts.py
d34f17353fec83ed2e7b78b41cebcd2a6d309a85d724dbf1097cf6a17afaf8aa  expectations.jsonl
eec810050dd174e3b6e8401efab35df2a18e310a27c212eb775e96c55830ba29  ../round37/c1-count.py (legacy cell)
37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d  tools/research-gate.sh
```
Mutants (minimal textual hunks on the pristine copy; each dir also holds the pinned `expectations.jsonl`):
```
12f0893b9d0cac194a0355c2f0ac959f462f9aa4e2e6c74d61809fb78fd7c3ac  M1  post-run gate hash only (gate_sha_pre := gate_sha_post; mid-run compare removed)
fa44b3bbf70eed4666ee976a6ed14fea16013bdff9674eb153ff5cab59c6841f  M2  pre!=post refusal dropped (pre and post still measured)
fe5a782ebdb91ab69e45d6cd1c1e21b28f42c114ec4a8d18d3aa4c4d5ca1d6c7  M3  `"counter_sha256": …` removed
a1bfd30e05cbb309af6044ab25ceb243410ba1dfdab34d2f297b2f910ebc9736  M4  `receipt["receipt_sha256"] = …` removed
```
Detector = pinned c2, `--counter <c1>` (all five receipts audit `gate_sha256_pre=37e2b996…`, `pre==post`):
```
$ C2_TMP=…/pt python3 /tmp/r38-w2-mutcf/pin/c2-count.py --gate <landed> \
    --counter pin/c1-count.py --seed 38401 --receipt …/c2-base-38401.json
  RECEIPT_BINDING_MATCH=7/7   exit 0   (c1 own, seed 38402: ENV_PIN_CAPTURE_MATCH=7/7, exit 0)
$ … --counter mut/M1/c1-count.py --seed 38412
  FAIL self-rewrite-refused  expect={'counter_rc': 2, 'receipt': False} observed={'counter_rc': 0, 'receipt': True}
  (other six PASS)  RECEIPT_BINDING_MATCH=6/7  exit 1; receipt matched=6 total=7 holds=False
$ … --counter mut/M2/c1-count.py --seed 38422
  FAIL self-rewrite-refused  (same observation)  RECEIPT_BINDING_MATCH=6/7  exit 1
$ … --counter mut/M3/c1-count.py --seed 38432
  FAIL hold-receipt-verifies   observed={'counter_rc': 0, 'receipt': True, 'verify_rc': 1}
  FAIL foreign-gate-distinguished  observed={'verify_foreign_rc': 1, 'verify_landed_rc': 1}
  FAIL counter-/expect-/body-tamper-detected  clean_verify_out='VERIFY-FAIL: missing-field counter_sha256', verify_rc='not-measured' (x3)
  FAIL legacy-receipt-refused  observed={'hold_verify_rc': 1, …}
  RECEIPT_BINDING_MATCH=1/7  exit 1
$ … --counter mut/M4/c1-count.py --seed 38442
  same seven cells with 'VERIFY-FAIL: missing-field receipt_sha256'  RECEIPT_BINDING_MATCH=1/7  exit 1
```
C1's own predicate per mutant (landed gate, receipts `c1-M{1..4}-384{11,21,31,41}.json`):
```
M1/M2/M3/M4 each: ENV_PIN_CAPTURE_MATCH=7/7, exit 0, receipt matched=7 total=7 holds=True gate=37e2b996…
```
Kill mechanism probed directly against a fresh F1 self-rewrite shim (replica of c2's fixture):
```
M1, seed 38451: shim 81d271cb… → rewritten to 37e2b996…; c1 7/7 exit 0;
  receipt matched=7 holds=True gate_pre=gate_post=37e2b996… (no trace of 81d271cb);
  verify-receipts.py --receipt …/f1-M1.json --gate <rewritten shim> --counter mut/M1/… -> VERIFY: ok, exit 0
M2, seed 38452: shim c5d06049… → 37e2b996…; receipt gate_pre=c5d06049… != gate_post=37e2b996…;
  verify -> VERIFY-FAIL: gate-sha-changed-across-run, exit 1
```
Restoration (all four overwritten with pristine bytes):
```
790407908444b3e99fbf3fba9e9afdcf654d565a5a4304bd4f23daedc3462221  mut/M1/c1-count.py
790407908444b3e99fbf3fba9e9afdcf654d565a5a4304bd4f23daedc3462221  mut/M2/c1-count.py
790407908444b3e99fbf3fba9e9afdcf654d565a5a4304bd4f23daedc3462221  mut/M3/c1-count.py
790407908444b3e99fbf3fba9e9afdcf654d565a5a4304bd4f23daedc3462221  mut/M4/c1-count.py
$ C1_TMP=… python3 pin/c1-count.py --gate <tip-gate copy> --seed 38463  -> ENV_PIN_CAPTURE_MATCH=7/7, exit 0
$ C2_TMP=… python3 pin/c2-count.py --gate <tip-gate copy> --counter mut/M1/c1-count.py \
    --seed 38462 --receipt …/c2-restored-38462.json -> RECEIPT_BINDING_MATCH=7/7, exit 0
```
No tool installs. No lane writes: only `/tmp/r38-w2-mutcf` and this report.

## Findings
1. Every requested mutant dies at the predicted cell: M1/M2 by `self-rewrite-refused` (6/7), M3/M4 by `hold-receipt-verifies` first, then the receipt-consuming cascade (1/7). Baseline pristine 7/7 (seed 38401) and restored 7/7 (38462) rule out a broken detector. (pointer: `/tmp/r38-w2-mutcf/out-c2-{M1..M4}.txt`, `c2-*.json`).
2. M1 is the stronger defect: with the pre-run measurement gone, an F1 gate whose first invocation ran different bytes (shim 81d271cb…) gets `gate_pre=gate_post=37e2b996…`, `matched=7`, `holds=True` and `VERIFY: ok` — the verifier is blind to it. M2 at least leaves `gate_pre != gate_post` in the receipt, so `verify-receipts.py` refuses `gate-sha-changed-across-run`. Only the counter's own pre-hash+refusal cell stands between M1 and an accepted forgery. (pointer: seeds 38451/38452 vs 38412/38422).
3. The gate-identity defence is one cell wide: under M1/M2 the other six cells (including foreign-gate and all three tamper cells) still PASS. `self-rewrite-refused` is load-bearing for the whole `gate_sha256_pre` binding family. (pointer: out-c2-M1/M2 PASS lines).
4. M3/M4 collapse six cells, not one, because every scenario presupposes a verifying honest receipt (`verify_rc`/`clean_verify_rc`/`hold_verify_rc`/`verify_foreign_rc`). A single dropped field is scored as total receipt-shape failure (1/7): the predicate fails closed but cannot localize the broken binding. (pointer: out-c2-M3/M4).
5. Wave-1 Erratum 3 is confirmed fixed on final bytes: the baseline's tamper cells now observe the named refusals `VERIFY-FAIL: counter-sha256-mismatch`, `expect-sha256-mismatch`, `receipt-self-digest` (not all at the self-digest layer), so the re-sealing doctors do exercise the named binding checks. (pointer: c2-base-38401 output).
6. Live drift inside the lane, after my probes: at 01:20:15 `tools/research-gate.sh` changed 37e2b996 → 0447ad14, and the working tree gained post-tip edits to `c1-count.py` (POSIXLY_CORRECT scrub), `verify-receipts.py` (strict schema) and `claims.md`; tip is still 8e93bc9. My first restored baseline exited 2 with `c2-count: gate bytes changed across the run (pre 37e2b9968706adab != current) — no receipt published` — the strengthened refusal working on a live sibling edit — and I re-ran it against a byte-copy of the tip gate (37e2b996) to get the clean 7/7. All five mutant/base c2 receipts were audited to bind gate 37e2b996, so no probe crossed the drift. (pointer: `git diff master -- tools/research-gate.sh`, `out-c2-restored.txt` vs `out-c2-restored2.txt`).
7. The four mutant anchors (`gate_sha_pre = …`, the refusal `if`, `counter_sha256` line, `receipt_sha256` assignment) are each still unique on the drifted working-tree `c1-count.py` (a48e5b22…), so the mutants remain constructible there, but they were not re-run on post-tip bytes. (pointer: anchor count 1/1/1/1).

## Limits
- One mutant per requested point, one seed each (38401-38463); no repeated sampling, no fuzzing of the verifier's recount/type/order checks.
- Verdicts bind master tip `8e93bc9` bytes and gate `37e2b996`; the post-tip working-tree edits (POSIXLY_CORRECT, strict schema) were not exercised and are a sibling's in-flight change, not mine.
- The F1 shim probes use a line-for-line replica of c2's fixture (same marker/rewrite/exec shape), not the detector's own temp copy.
- `/tmp/r38-w2-mutcf` is disposable scratch; scratch mutants restored byte-exact before returning.
