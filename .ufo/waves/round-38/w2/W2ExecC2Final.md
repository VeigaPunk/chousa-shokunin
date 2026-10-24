# W2ExecC2Final

## Verdict
P2 reproduced on the final landed gate bytes at both assigned seeds; the r37-counter control is 0/7 at both seeds, and the r37 base-gate separability run is 7/7. All five generated c2 receipts verify.

## Evidence
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` → `8e93bc916527b3c21f0f702967fa65c3b4c31699`.
- `sha256sum` on the measured artifacts returned:
  - `tools/research-gate.sh`: `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d`
  - `.ufo/waves/round-37/controls/base-gate-r37.sh`: `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`
  - `corpus/evidence/round38/c2-count.py`: `414a7a10571263e781137fcbb0fb4e16bd9dbb9a44fda4931d9fe4d67cc403e3`
  - `corpus/evidence/round37/c1-count.py`: `eec810050dd174e3b6e8401efab35df2a18e310a27c212eb775e96c55830ba29`
  - `corpus/evidence/round38/expectations.jsonl`: `d34f17353fec83ed2e7b78b41cebcd2a6d309a85d724dbf1097cf6a17afaf8aa`
  - `corpus/evidence/round38/verify-receipts.py`: `3fc416612085a4ba8333b6b39a9ad2f4e32eb17ebcbc53ae6cd2e048f8abf919`
- All counter commands used existing `C1_TMP=C2_TMP=/tmp/chousa-r38-w2-c2final.CAm0QX`; receipts are in that directory.
Counter runs (`C1_TMP` and `C2_TMP` both pointed at existing `/tmp/chousa-r38-w2-c2final.CAm0QX`):
```sh
C1_TMP=/tmp/chousa-r38-w2-c2final.CAm0QX C2_TMP=/tmp/chousa-r38-w2-c2final.CAm0QX python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38421 --receipt /tmp/chousa-r38-w2-c2final.CAm0QX/landed-c2-s38421.json --tmp /tmp/chousa-r38-w2-c2final.CAm0QX
# observed: RECEIPT_BINDING_MATCH=7/7
C1_TMP=/tmp/chousa-r38-w2-c2final.CAm0QX C2_TMP=/tmp/chousa-r38-w2-c2final.CAm0QX python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38441 --receipt /tmp/chousa-r38-w2-c2final.CAm0QX/landed-c2-s38441.json --tmp /tmp/chousa-r38-w2-c2final.CAm0QX
# observed: RECEIPT_BINDING_MATCH=7/7
C1_TMP=/tmp/chousa-r38-w2-c2final.CAm0QX C2_TMP=/tmp/chousa-r38-w2-c2final.CAm0QX python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --seed 38421 --receipt /tmp/chousa-r38-w2-c2final.CAm0QX/r37-control-s38421.json --tmp /tmp/chousa-r38-w2-c2final.CAm0QX
# observed: RECEIPT_BINDING_MATCH=0/7
C1_TMP=/tmp/chousa-r38-w2-c2final.CAm0QX C2_TMP=/tmp/chousa-r38-w2-c2final.CAm0QX python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --seed 38441 --receipt /tmp/chousa-r38-w2-c2final.CAm0QX/r37-control-s38441.json --tmp /tmp/chousa-r38-w2-c2final.CAm0QX
# observed: RECEIPT_BINDING_MATCH=0/7
C1_TMP=/tmp/chousa-r38-w2-c2final.CAm0QX C2_TMP=/tmp/chousa-r38-w2-c2final.CAm0QX python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 38461 --receipt /tmp/chousa-r38-w2-c2final.CAm0QX/base-r37-c2-s38461.json --tmp /tmp/chousa-r38-w2-c2final.CAm0QX
# observed: RECEIPT_BINDING_MATCH=7/7
```
Receipt JSON reads returned `matched/total=7/7`, `predicate_holds=true` for the two landed runs; `0/7`, `false` for the two r37-counter runs; and `7/7`, `true` for the base gate run. The landed receipts bind pre/post digest `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d`; base receipt binds pre/post `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.
Each of these exact verifier invocations returned the shown output:
```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/chousa-r38-w2-c2final.CAm0QX/landed-c2-s38421.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py
# VERIFY: ok receipt=landed-c2-s38421.json gate=research-gate.sh counter=c2-count.py
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/chousa-r38-w2-c2final.CAm0QX/landed-c2-s38441.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py
# VERIFY: ok receipt=landed-c2-s38441.json gate=research-gate.sh counter=c2-count.py
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/chousa-r38-w2-c2final.CAm0QX/r37-control-s38421.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py
# VERIFY: ok receipt=r37-control-s38421.json gate=research-gate.sh counter=c2-count.py
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/chousa-r38-w2-c2final.CAm0QX/r37-control-s38441.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py
# VERIFY: ok receipt=r37-control-s38441.json gate=research-gate.sh counter=c2-count.py
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/chousa-r38-w2-c2final.CAm0QX/base-r37-c2-s38461.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py
# VERIFY: ok receipt=base-r37-c2-s38461.json gate=base-gate-r37.sh counter=c2-count.py
```

## Findings
1. The two fresh landed-gate measurements satisfy P2 (7/7, predicate true) and bind identical pre/post final gate bytes. Grounding: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/claims.md:91-104`; Errata 2–3 describe the strengthened verifier and tamper checks.
2. The r37 counter scores 0/7 at both fresh seeds; both resulting c2 receipts verify, preserving a valid record of the failed predicate. Grounding: `claims.md:106-116` and Erratum 4 at `claims.md:193-201`.
3. The default r38 counter scores 7/7 against the r37 base gate, confirming the stated C2/gate separability after Erratum 4. Grounding: `claims.md:118-126` and `claims.md:193-201`.

## Limits
The verifier's `VERIFY: ok` establishes receipt integrity/self-consistency against the committed bindings and frozen census, not execution authorship; this is the narrowed limit in `claims.md:177-183`. No tools were installed or repository implementation files changed; no blockers encountered.