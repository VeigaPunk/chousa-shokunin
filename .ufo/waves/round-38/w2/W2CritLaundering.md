# W2CritLaundering

## Verdict
One requested attack still accepts: the re-sealed unknown-field fixture; the other seven requested attacks refuse with named labels. This meets the assignment's acceptance counterexample condition; no canonical judgment performed.

## Evidence
Axes: **calibration** (receipt identity, schema, observation consistency) and **operability** (named, fail-closed refusals).
Read the frozen claims and Errata 1–8 first. Original fixture authority: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/w1/CritC2Kill.md:21-34` and its `/tmp/chousa-r38-CritC2Kill-kQmBeT/probes.py:31-53`.
All new fixtures are under `/tmp/chousa-r38-W2CritLaundering-Y9U4K3`; fresh seeds **38491** (r38 C1) and **38492** (r37 C1).

Executed provenance command:
```sh
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master
# stdout: 8e93bc916527b3c21f0f702967fa65c3b4c31699
```
Executed fresh receipt commands (both temporary directories already existed):
```sh
env C1_TMP=/tmp/chousa-r38-W2CritLaundering-Y9U4K3 C2_TMP=/tmp/chousa-r38-W2CritLaundering-Y9U4K3 PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38491 --receipt /tmp/chousa-r38-W2CritLaundering-Y9U4K3/honest-c1.json
# stdout excerpt: ENV_PIN_CAPTURE_MATCH=7/7
env C1_TMP=/tmp/chousa-r38-W2CritLaundering-Y9U4K3 C2_TMP=/tmp/chousa-r38-W2CritLaundering-Y9U4K3 PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38492 --receipt /tmp/chousa-r38-W2CritLaundering-Y9U4K3/legacy.json
# stdout excerpt: CLAIM_PIN_PROVENANCE_MATCH=7/7
```
Executed replay command; the runner printed every expanded absolute verifier command and exit code, and saved them in `/tmp/chousa-r38-W2CritLaundering-Y9U4K3/results.json`:
```sh
env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /tmp/chousa-r38-W2CritLaundering-Y9U4K3/replay.py
```
All eight requested results (exact verifier stdout):

| Attack / fixture filename | Exit | Exact output |
|---|---:|---|
| Legacy rebound / `legacy-rebound.json` | 1 | `VERIFY-FAIL: predicate-mismatch` |
| Identity reroute, re-sealed / `counter-swapped.json` | 1 | `VERIFY-FAIL: predicate-mismatch` |
| Doctored observation, re-sealed / `false-observation.json` | 1 | `VERIFY-FAIL: ok-rederivation-mismatch hold-plain` |
| Vacuous empty without predicate / `vacuous-empty.json` | 1 | `VERIFY-FAIL: missing-field predicate` |
| Zero scenarios retaining predicate / `zero-scenarios.json` | 1 | `VERIFY-FAIL: scenario-census-mismatch` |
| Extra unknown field, unsealed / `extra-unsealed.json` | 1 | `VERIFY-FAIL: receipt-self-digest` |
| Extra unknown field, re-sealed / `extra-resealed.json` | **0** | **`VERIFY: ok receipt=extra-resealed.json gate=research-gate.sh counter=c1-count.py`** |
| C1 as C2, unmodified / `honest-c1.json` with C2 counter | 1 | `VERIFY-FAIL: counter-sha256-mismatch` |

Original data-mode auxiliary controls also replayed:

| Control | Exit | Exact output |
|---|---:|---|
| Honest C1 | 0 | `VERIFY: ok receipt=honest-c1.json gate=research-gate.sh counter=c1-count.py` |
| Re-sealed pre/post mismatch | 1 | `VERIFY-FAIL: gate-sha-changed-across-run` |
| Plain legacy | 1 | `VERIFY-FAIL: missing-field counter_sha256` |
| Re-sealed legacy with garbage hashes | 1 | `VERIFY-FAIL: counter-sha256-mismatch` |

The accepted counterexample's expanded executed command:
```sh
/usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/chousa-r38-W2CritLaundering-Y9U4K3/extra-resealed.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --expectations /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/expectations.jsonl
# exit=0
# VERIFY: ok receipt=extra-resealed.json gate=research-gate.sh counter=c1-count.py
```
Executed `sha256sum` before replay and runner-computed hashes after replay agreed on these final reviewed files (paths rooted at `/home/vgpnk/Projects/shokunin/chousa-shokunin/`):
```text
b63e7e200b88022f6747e4b628cb6b251187ad95f5b33d2b6b4b14e08d5cf952  corpus/evidence/round38/verify-receipts.py
790407908444b3e99fbf3fba9e9afdcf654d565a5a4304bd4f23daedc3462221  corpus/evidence/round38/c1-count.py
414a7a10571263e781137fcbb0fb4e16bd9dbb9a44fda4931d9fe4d67cc403e3  corpus/evidence/round38/c2-count.py
d34f17353fec83ed2e7b78b41cebcd2a6d309a85d724dbf1097cf6a17afaf8aa  corpus/evidence/round38/expectations.jsonl
37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d  tools/research-gate.sh
```
Replay-script SHA256 printed by the runner: `d22f3ee5f2b98250fd21c290a49f2a826a64726d3a43d8801fbe8ad4eb4f4b6a`.

## Findings
1. **Remaining acceptance; calibration.** The fixture adds exactly `"EXTRA_unknown": {"provenance": "doctor-added"}` to the fresh honest receipt and recomputes `receipt_sha256` using the verifier's canonical serialization. No observation, identity, census or score changes. It still verifies. Grounding: `/tmp/chousa-r38-W2CritLaundering-Y9U4K3/replay.py` (`extra-unknown-resealed`), its `results.json`, and `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py:65-67,118-123,150-171`: required-field presence and digest are checked, but unknown top-level fields are never refused. Smallest safe correction: an explicit per-family allowed-key schema with a named unknown-field refusal, plus this re-sealed fixture as a regression case. This is a fixable schema defect under the assignment's every-fixture-must-refuse requirement, not proof of a falsified seven-scenario score. If extension fields are intentionally acceptable, that is a contract tradeoff for the canonical Rust judge, not an observed refusal.
2. **Legacy laundering and identity reroute now stop; calibration/operability.** The legacy fixture preserves `predicate="CLAIM_PIN_PROVENANCE_MATCH=7/7"` and first scenario `hold-stale`, while adding the actual r37 counter hash, current gate pre/post hashes and current r38 expectation hash, then re-sealing. The identity fixture changes only the C1 receipt's `counter_sha256` to C2's public hash and re-seals. Both hit `predicate-mismatch`; unmodified C1-as-C2 hits the earlier hash check. Grounding: replay cases and verifier `:125-140`. No correction needed for these exact witnesses. The legacy counter shares basename `c1-count.py`, so its observed refusal is predicate-based, not `unknown-counter`.
3. **Observation and vacuity kills are blocked; calibration/operability.** The observation fixture retains `expect.pin_rc=0` and `ok=true` while changing `observed.pin_rc=99` on `hold-plain`; it hits re-derivation. Both empty fixtures set `scenarios=[]`, `matched=total=0`, `predicate_holds=true`; one removes `predicate`, the other preserves `ENV_PIN_CAPTURE_MATCH=7/7`. They hit required-field and census checks respectively. Grounding: replay cases and verifier `:118-120,139-164`. No correction needed for these exact witnesses.
4. **No digest exclusion demonstrated; calibration.** The identical unknown-field addition without re-sealing fails `receipt-self-digest`, while the re-sealed version accepts. This distinguishes missing schema refusal from accidental-corruption detection. Grounding: paired extra-field cases and verifier `:78-81,122-123`. It does not overcome the explicitly named non-authentication limit in `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/claims.md:177-183`.

## Limits
No lane source, corpus, index, jj state, fleet root or peer files changed; only this report and isolated `/tmp` fixtures were written. No tools installed. No judge, admission, integration, shipping, subagent dispatch or orchestration runtime invoked.
All eight requested attacks and all original data-mode auxiliary controls completed. Boundary instrumentation, self-editing-counter and symlink-path experiments are outside this assigned doctoring replay and were not rerun. No blanket authorship/authenticity claim or below-seven counter claim is made.
