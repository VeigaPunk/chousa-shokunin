# CritC2Kill
## Verdict
Frozen-C2 kill candidates: re-sealed legacy receipts, counter misattribution, and doctored observations verify successfully; the unchanged seven-cell predicate still scores 7/7. No canonical judgment performed.

## Evidence
Axes: **calibration** (identity, provenance, predicate truth) and **operability** (refusal/no publication, path selection).
All fixture paths are under `/tmp/chousa-r38-CritC2Kill-kQmBeT`; seeds **38981–38985**. Commands below were executed; outputs are labeled excerpts where shortened.

```sh
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master
# stdout: 504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f
env C1_TMP=/tmp/chousa-r38-CritC2Kill-kQmBeT C2_TMP=/tmp/chousa-r38-CritC2Kill-kQmBeT PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38981 --receipt /tmp/chousa-r38-CritC2Kill-kQmBeT/honest-c1.json
# stdout excerpt: ENV_PIN_CAPTURE_MATCH=7/7
env C1_TMP=/tmp/chousa-r38-CritC2Kill-kQmBeT C2_TMP=/tmp/chousa-r38-CritC2Kill-kQmBeT PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38982 --receipt /tmp/chousa-r38-CritC2Kill-kQmBeT/honest-c2.json
# stdout excerpt: RECEIPT_BINDING_MATCH=7/7
env C1_TMP=/tmp/chousa-r38-CritC2Kill-kQmBeT C2_TMP=/tmp/chousa-r38-CritC2Kill-kQmBeT PYTHONDONTWRITEBYTECODE=1 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38983 --receipt /tmp/chousa-r38-CritC2Kill-kQmBeT/legacy.json
# stdout excerpt: CLAIM_PIN_PROVENANCE_MATCH=7/7
env PYTHONDONTWRITEBYTECODE=1 python3 /tmp/chousa-r38-CritC2Kill-kQmBeT/probes.py data
```
The runner prints every expanded absolute verifier command and exit code. It invokes `/usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py --receipt <fixture> --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --counter <counter> --expectations /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/expectations.jsonl`.
Observed case / exit / exact verifier stdout (one line per case):
```text
honest-c1 / 0 / VERIFY: ok receipt=honest-c1.json gate=research-gate.sh counter=c1-count.py
extra-unsealed / 1 / VERIFY-FAIL: receipt-self-digest
extra-resealed / 0 / VERIFY: ok receipt=extra-resealed.json gate=research-gate.sh counter=c1-count.py
pre-post-differ-resealed / 1 / VERIFY-FAIL: gate-sha-changed-across-run
legacy-plain / 1 / VERIFY-FAIL: missing-field counter_sha256
legacy-garbage-resealed / 1 / VERIFY-FAIL: counter-sha256-mismatch
legacy-public-hashes-resealed / 0 / VERIFY: ok receipt=legacy-rebound.json gate=research-gate.sh counter=c1-count.py
c1-as-c2-unmodified / 1 / VERIFY-FAIL: counter-sha256-mismatch
c1-as-c2-resealed / 0 / VERIFY: ok receipt=counter-swapped.json gate=research-gate.sh counter=c2-count.py
zero-scenarios-resealed / 0 / VERIFY: ok receipt=zero-scenarios.json gate=research-gate.sh counter=c1-count.py
false-observation-resealed / 0 / VERIFY: ok receipt=false-observation.json gate=research-gate.sh counter=c1-count.py
```
```sh
env PYTHONDONTWRITEBYTECODE=1 python3 /tmp/chousa-r38-CritC2Kill-kQmBeT/probes.py boundary
```
Exact relevant output (seed 38984; unchanged C1 source executed via runpy, temporary gate copy):
```text
CASE gate-changed-between-scenarios
$ /usr/bin/python3 /tmp/chousa-r38-CritC2Kill-kQmBeT/boundary-probe.py
exit=2
INJECT after=hold-plain before=hold-fn-benign
stderr: c1-count: gate bytes changed across the run (pre 37e2b9968706adab != current) — no receipt published
receipt_exists=false
```
```sh
env PYTHONDONTWRITEBYTECODE=1 python3 /tmp/chousa-r38-CritC2Kill-kQmBeT/probes.py selfmodify
```
The runner executed `/usr/bin/python3 /tmp/chousa-r38-CritC2Kill-kQmBeT/self-writing-counter.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38985 --receipt /tmp/chousa-r38-CritC2Kill-kQmBeT/self-writing.json`. Relevant observed output:
```text
exit=0
ENV_PIN_CAPTURE_MATCH=7/7
counter_hash_equals_pre=true counter_hash_equals_post=false
CASE self-writing-current-bytes
exit=1
VERIFY-FAIL: counter-sha256-mismatch
```
```sh
env PYTHONDONTWRITEBYTECODE=1 python3 /tmp/chousa-r38-CritC2Kill-kQmBeT/probes.py symlink
```
Observed case / exit / exact verifier stdout:
```text
symlink-initial-honest / 0 / VERIFY: ok receipt=receipt-link.json gate=research-gate.sh counter=c1-count.py
symlink-swapped-tamper / 1 / VERIFY-FAIL: receipt-self-digest
symlink-swapped-rebound-legacy / 0 / VERIFY: ok receipt=receipt-link.json gate=research-gate.sh counter=c1-count.py
```
Provenance command: `sha256sum /tmp/chousa-r38-CritC2Kill-kQmBeT/probes.py /tmp/chousa-r38-CritC2Kill-kQmBeT/honest-c1.json /tmp/chousa-r38-CritC2Kill-kQmBeT/honest-c2.json /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py`.
Observed hashes respectively: `b4c96a34dd14101fd628afbfbb575c10da2093dcc291a1119f45f570c91ff87a`, `e2872202408b62e697efce647c981d3e7d6b26c67a4756e3e1dc7a4577bcfadf`, `753a12e7d48cfe30232124e5f93a410438e88958278aa16b239e6613aabbabbd`, `756f186c3487461b9c29de5ebbb4b91392706ecc4b5ff8f3a83d482fcaf27605`.

## Findings
Pointers below are absolute via prefix `/home/vgpnk/Projects/shokunin/chousa-shokunin/`; fixture pointers use the absolute temp directory above.
1. **KILL candidate — legacy laundering; calibration.** `probes.py:39-46`: start from freshly generated r37 receipt; garbage added bindings fail. Replace garbage with public SHA256s of the actual r37 counter, current gate and r38 expectations, then recompute the unkeyed self-digest: accepted. `legacy-rebound.json:10,21` still names `CLAIM_PIN_PROVENANCE_MATCH=7/7` and `hold-stale`, not r38 scenarios. The r37 counter never measured the newly asserted pre/post or r38 expectations. This directly meets `corpus/evidence/round38/claims.md:101-104`'s legacy-accept kill language. No counter code was altered. Smallest local correction: require a supported round/counter/predicate/scenario schema; refuse r37 identities even when dressed in binding fields.
2. **KILL candidate — identity substitution; calibration.** `probes.py:47-49`: unmodified C1 receipt under `--counter .../round38/c2-count.py` fails, but changing only `counter_sha256` to C2's publicly computed hash and recomputing `receipt_sha256` succeeds. C1 predicate/scenarios remain unchanged. `corpus/evidence/round38/verify-receipts.py:89-92,109-118` checks supplied hash equality and truthy `ok` counts, not that C2's predicate/schema was used. Smallest local correction: validate exact expected predicate and scenario IDs/count for the explicitly selected counter; do not accept a checksum as execution provenance.
3. **KILL candidate — doctored observation and premature saturation; calibration.** `probes.py:50-53`: changing `scenarios[0].observed.pin_rc` from 0 to 99, leaving `expect.pin_rc=0` and `ok=true`, then resealing succeeds with every file binding unchanged. An empty scenario list with `matched=total=0`, `predicate_holds=true`, and the unchanged `ENV_PIN_CAPTURE_MATCH=7/7` predicate also verifies. `verify-receipts.py:94-97` hashes expectations but never parses them; `:112-118` trusts `ok` and vacuous success. Smallest local correction: require the full frozen scenario census and re-derive each `ok` from frozen expectations and observations, then require seven successes. This is not the named lying-counter limit: honest counter output was doctored afterward, without touching scoring code.
4. **NAMED LIMIT — unknown fields/checksum, not authentication; calibration.** Extra unknown nested field is covered: without resealing it fails `receipt-self-digest`; with resealing it is accepted (`probes.py:34-36`; verifier `:55-58,86-87`). No field-exclusion bug found. An unkeyed digest supplied in the same editable object cannot establish who produced it. To uphold the frozen “any doctored field” wording, the smallest general correction is a trusted receipt digest/manifest outside the editable receipt, anchored to committed bytes; schema checks alone cannot authenticate arbitrary observation changes. Narrowing to accidental-corruption detection is a contract tradeoff for the canonical judge, not a repair of this frozen claim.
5. **NAMED LIMIT / no kill — durable between-scenario gate changes are covered; operability/calibration.** Boundary fixture appends to a gate copy immediately after `hold-plain` returns and before `hold-fn-benign`; C1 refuses exit 2 and publishes nothing. A separately resealed pre/post mismatch also fails verification. Grounding: `corpus/evidence/round38/c1-count.py:220-229`, verifier `:101-105`, `probes.py` boundary mode. This establishes the requested durable-change boundary, not continuous immutability against change-and-restore.
6. **OUT-OF-SCOPE as a kill — deliberately substituted self-editing counter; calibration.** Temp counter appends a comment after `main()` publishes. Its receipt hash equals pre-edit executed bytes, not post-edit bytes, and verification of the current file refuses. `c1-count.py:244,258-262` and `probes.py` selfmodify mode ground the timing. No stale current-byte acceptance or false hash was demonstrated; C2 does not promise a counter remains unchanged after publication. No correction needed for this witness.
7. **NAMED LIMIT — receipt pathname identity is not bound; operability/calibration.** `probes.py` symlink mode creates the receipt-path symlink after publication and switches its target before each verify. Tampered unsealed data is rejected; an independently verifying forged legacy target is accepted for the same root cause as finding 1. `verify-receipts.py:74-76` opens the selected path once. No independent symlink bypass was found, and output pathname/inode identity is not among the frozen bindings. If required separately, hold/open the intended artifact or require an externally trusted digest; do not confuse path identity with body integrity.

## Limits
No production/corpus/index/jj edits; only this report and isolated temp fixtures. No tools installed. No judge, admission, integration, shipping, or orchestration runtime invoked. The report classifies counterexamples against literal frozen C2; canonical judgment remains external.
The seven-cell fresh-seed run stayed 7/7: these are additional doctoring fixtures, not a claimed below-seven run. Self-editing counter is a temp copy with an absolute expectations path; the boundary probe instruments the runtime namespace and mutates only a temp gate copy. No concurrent in-open symlink race or transient gate change-and-restore claim is made. Fixture files remain available under the named temp directory.

Post-review provenance alert from `chousa-r38.SimpCounters` (attributed, not independently re-executed): expectations reportedly changed `7cd5d824…→c986c5fd…` and C2 counter `bc325cf4…→5ae3bd8c…` during the wave; see `.ufo/waves/round-38/w1/SimpCounters.md` F9. All evidence above concerns the explicitly hashed **pre-drift** bytes, not the edited counter/table. Replaying these commands against a changed worktree is a different experiment; no claim is made about those new bytes.
