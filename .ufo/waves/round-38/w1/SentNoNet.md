# SentNoNet

## Verdict
Operability: fresh C1 run scored 7/7 with no `socket`/`connect` calls; calibration: its receipt verified; caveat: gate capture fixtures spill outside `C1_TMP` when `TMPDIR` is unset.

## Evidence
- Lane revision: `504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f`. Gate SHA-256: `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d`; C1 counter: `da1d915b51801fd6d25ebf857318afc87c08c4876dd25fe4055fdede1ede3f74`; verifier: `756f186c3487461b9c29de5ebbb4b91392706ecc4b5ff8f3a83d482fcaf27605`.
- `/usr/bin/strace --version`: `strace -- version 7.2` (already installed; no tool install/update).
- Exact C1 trace command (fresh seed `38201`):
  ```
  C1_TMP=/tmp/chousa-r38-sentnonet.2PvPcW C2_TMP=/tmp/chousa-r38-sentnonet.2PvPcW strace -f -e trace=openat,socket,connect -o /tmp/chousa-r38-sentnonet.2PvPcW/c1.trace python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38201 --receipt /tmp/chousa-r38-sentnonet.2PvPcW/c1-receipt.json
  ```
  Output: all seven scenarios PASS (`hold-plain`, `hold-fn-benign`, `env-fn-echo-scrub`, `env-fn-root-move`, `env-fn-suppress`, `env-override-missing`, `env-override-fake`); `ENV_PIN_CAPTURE_MATCH=7/7`; exit `0`.
- Exact verifier trace command:
  ```
  strace -f -e trace=openat,socket,connect -o /tmp/chousa-r38-sentnonet.2PvPcW/verify.trace python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt /tmp/chousa-r38-sentnonet.2PvPcW/c1-receipt.json --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py
  ```
  Output: `VERIFY: ok receipt=c1-receipt.json gate=research-gate.sh counter=c1-count.py`; exit `0`. Receipt has matching `gate_sha256_pre/post` = `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d`, `matched=7`, `predicate_holds=true`, and counter SHA matching the file above.
- Network evidence: search for `(?:socket|connect)\(` across `/tmp/chousa-r38-sentnonet.2PvPcW/c1.trace` and `/tmp/chousa-r38-sentnonet.2PvPcW/verify.trace` returned `No matches found` (zero such syscall lines in either run).
- Write evidence: C1 counter scratch and receipt are under `/tmp/chousa-r38-sentnonet.2PvPcW` (e.g. C1 trace lines 8057, 79016, 79148); verifier trace has no write-capable `openat` match. Search for write-capable opens into `/home/vgpnk/Projects/shokunin/chousa-shokunin/` returned no matches. `TMPDIR` was unset. Gate writes capture fixtures such as `/tmp/chousa-gate-pin.NN3aOP/lib/primary.md` and `capture.txt` (C1 trace lines 303-317; another capture at 8191-8205), outside `C1_TMP`; `/dev/null` write opens are subprocess output redirections. C1 work and sampled gate temp dirs were absent after the run; receipt remained. Gate source uses `${TMPDIR:-/tmp}` at `research-gate.sh:3991`, `cd`s to the fixture at 4000, and removes it at 4020. C1 source removes its work dir at `c1-count.py:230-231`.
- Trace SHA-256: `c1.trace` `20e6f2267a358f1e87f3c0e7ef89f376023ca21edb1d785a4034c0a1f742490`; `verify.trace` `ee209c7dda2228ff31c966af5c4d05976aa86e34533077f6da19c80c883c027f`. Receipt SHA-256: `354bea99b3315751940510d03d3ef24e2261ec33b2984680f9c1bbec5a025e39`.

## Findings
1. **Informational — no network syscall observed in the sampled C1 pass or verifier.** Exploit path: none demonstrated; these traced processes made no `socket()` or `connect()` call. Evidence: commands and trace search above. Impact: none observed. Smallest remediation: none for this sample; this is not evidence about unrun counters or other seeds.
2. **Low — `C1_TMP` does not contain gate capture scratch by itself.** Exploit path: a runner confines/quotas `C1_TMP` but leaves `TMPDIR` unset; the gate's `mktemp` falls back to shared `/tmp` and writes capture fixtures there. Evidence: `/tmp/chousa-gate-pin.*` openat paths above and `research-gate.sh:3991-4020`; observed paths were cleaned up. Impact: the run's subprocess scratch bypasses the caller-selected temp root, though no lane-repository writes were observed and sampled gate dirs were removed. Smallest remediation: set `TMPDIR="$C1_TMP"` for the counter invocation when strict end-to-end scratch confinement is required.

## Limits
Only one C1 pass and one `verify-receipts.py` invocation were traced, as assigned; `c2-count.py` was not run. The syscall filter was `openat,socket,connect`, not a full syscall trace; no claim is made about other runs or inherited nonstandard file descriptors. No repository files were edited except this scoped report; trace and receipt artifacts remain under `/tmp/chousa-r38-sentnonet.2PvPcW`.
