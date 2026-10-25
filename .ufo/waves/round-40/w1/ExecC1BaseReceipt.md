# ExecC1BaseReceipt — regenerated c1-base-s39001 receipt vs the base-gate-r39 control

Lane: chousa-shokunin. Round: 40, wave 1. Lane HEAD at audit: `6bc90e04ac60307befacd554f7eee2b7284e2652`; receipts committed at `d164f88` and unchanged since. Read-only audit; no lane file modified except this report.

## Assigned attack

Run the committed verifier for `corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json` against the `base-gate-r39` control, `corpus/evidence/round39/c1-count.py`, the current committed `expectations.jsonl`, and the committed verifier; decide whether the expected **7/8 negative-control** result is a **valid receipt** (not a verifier failure and not a laundered pass).

## Verdict

**Valid — and correct.** `VERIFY: ok`, exit 0. The receipt honestly binds `matched=7`, `total=8`, `predicate="ENV_PIN_CAPTURE_MATCH=8/8"`, `predicate_holds=false`; the verifier re-derives every binding and re-derives `predicate_holds` as `(matched == total)`, so a false predicate is not an error, it is the recorded negative-control outcome. 7/8 is exactly the pre-registered value for the pre-pin base gate (`corpus/evidence/round39/claims.md:63-72`), and only the `capture-bash-path-pin` family fails — the family the round-39 bash pin was built to close. An independent re-run of the committed counter against the committed base gate reproduces the committed receipt **byte for byte**.

Reading caution (calibration): `VERIFY: ok` certifies binding integrity, not gate success. `R39_ACTIVE_RECEIPTS=6/6` likewise counts receipts that re-derive, not receipts whose predicates hold — two of the six legitimately carry `predicate_holds=false` (base 7/8, mutant 4/8). The base receipt must never be cited as 8/8 evidence.

## Exact commands and output

All commands run at the lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

### 1. Committed verifier on the regenerated base receipt

```
python3 corpus/evidence/round39/verify-receipts.py \
  --receipt corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json \
  --gate .ufo/waves/round-39/controls/base-gate-r39.sh \
  --counter corpus/evidence/round39/c1-count.py \
  --expectations corpus/evidence/round39/expectations.jsonl
```
```
VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py
rc=0
```

### 2. Frozen round-40 counter (active population)

```
python3 corpus/evidence/round40/c1-count.py
```
```
corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json: ok VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: ok VERIFY: ok receipt=c1-after-s39011-regenerated.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: ok VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
corpus/evidence/round39/receipts/c1-after-s39111.json: ok VERIFY: ok receipt=c1-after-s39111.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round39/receipts/c2-after-s39101.json: ok VERIFY: ok receipt=c2-after-s39101.json gate=research-gate.sh counter=c2-count.py
corpus/evidence/round39/receipts/c2-after-s39121.json: ok VERIFY: ok receipt=c2-after-s39121.json gate=research-gate.sh counter=c2-count.py
R39_ACTIVE_RECEIPTS=6/6
rc=0
```

### 3. Independent reproduction of the 7/8 measurement

```
python3 corpus/evidence/round39/c1-count.py \
  --gate .ufo/waves/round-39/controls/base-gate-r39.sh --seed 39001 \
  --tmp /tmp/c1base-repro --receipt /tmp/c1base-repro/receipt.json
```
```
PASS hold-plain / hold-fn-benign / env-fn-echo-scrub / env-fn-root-move / env-fn-suppress
PASS env-override-missing / env-override-fake
FAIL capture-bash-path-pin
ENV_PIN_CAPTURE_MATCH=7/8
COUNTER_RC=1
```
```
cmp /tmp/c1base-repro/receipt.json corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json
CMP: byte-identical reproduction
```
The reproduction is byte-identical including `receipt_sha256`, so the committed receipt is a genuine counter output, not a hand-edited file. The counter emits no timestamp, so the body is deterministic for fixed gate/expectation bytes.

Failing-family cells in the committed receipt (observed vs frozen expect):

| cell | expect | observed |
|---|---|---|
| `path_bash_shim_echo.echo_lines` | 0 | **1** |
| `path_bash_shim_echo.drift_rc` / `drift_line` | 0 / `GATE_DRIFT: none` | **1** / **`GATE_DRIFT: -GATE_GREP`** |
| `path_bash_shim_suppress.pin_rc` / `pin_file` | 0 / true | **2** / **false** |
| `override_relative_refused.pin_rc` / `pin_file` / `refusal` | 2 / false / `BASH_PROVENANCE` | **0** / **true** / **`""`** |
| `path_env_shim_echo.*`, `override_honoured.*` | hold | hold |

This is verbatim the round-39 before-state description (`corpus/evidence/round39/claims.md:66-71`), including the hostile `-GATE_GREP` drift and the suppressed capture.

### 4. Digest table (receipt fields vs measured bytes)

```
91618e91640f748df76282244186088218d5f2b7a65364137fa6add29fea05d5  corpus/evidence/round39/c1-count.py
01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a  corpus/evidence/round39/expectations.jsonl
0447ad14b6135441f39f9220d02ae2967b810f791a2f1058654ee0c800c3b85a  .ufo/waves/round-39/controls/base-gate-r39.sh
1b6e0de688deda7493db3af5397d1e5bbf1fcdf556d8e254acae3ac6a8496267  corpus/evidence/round39/verify-receipts.py
e33199c1193ce6f0fb12cef788b41d79d2eb31181bbfdafe3d2f2eba97aa46af  corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json
```
Every receipt field matches: `counter_sha256`, `expect_sha256`, `gate_sha256[_pre|_post]` (all three equal), `verifier_sha256`, self-digest `receipt_sha256`. The receipt is committed: `git show HEAD:corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json | sha256sum` → `e33199c1…`, `git diff HEAD -- corpus/evidence/round40` empty.

### 5. Refusal probes (the "valid" is not vacuous)

| probe | result |
|---|---|
| old `round39/receipts/c1-base-s39001.json` under current committed bindings | `VERIFY-FAIL: expect-sha256-mismatch`, rc=1 |
| regenerated receipt against the **landed** gate `tools/research-gate.sh` | `VERIFY-FAIL: gate-sha256-mismatch`, rc=1 |
| regenerated receipt doctored to `matched=8/8`, `predicate_holds=true`, re-sealed | `VERIFY-FAIL: matched-recount-mismatch`, rc=1 |
| regenerated receipt rebound to the old `expect_sha256=3abd2dcb…`, re-sealed | `VERIFY-FAIL: expect-sha256-mismatch`, rc=1 |

The 7/8 cannot be laundered to 8/8: `matched` is recounted from the per-scenario `ok` flags and `ok` is re-derived from `observed` vs the frozen table. The regeneration was necessary — the old receipt is refused now.

## Depth checks

- **The control is genuinely pre-fix.** `sha256(tools/research-gate.sh)=4253c187…` ≠ base gate `0447ad14…`; `diff base-gate-r39.sh tools/research-gate.sh` is 148 lines and adds the whole `BASH_BIN`/`BASH_PIN_SOURCE`/`BASH_PROVENANCE` block. A base gate that reached 8/8 would mean the expectation set does not discriminate.
- **Regeneration is a binding repair, not a re-measurement of different bytes.** Comparing the old and regenerated receipts: exactly two keys differ, `expect_sha256` (`3abd2dcb…` → `01cbdc3a…`) and the self-digest. Every `scenarios`/`observed`/`expect`/`matched`/`total`/`gate_sha256` field is identical, and both receipts' embedded `expect` rows equal the current committed c1 table (0 rows differ). The 7/8 observation is stable across the r39 run, the r40 regeneration, and this independent r40 re-run.
- **Family/predicate binding is enforced.** `FAMILIES["c1-count.py"]` pins `predicate="ENV_PIN_CAPTURE_MATCH=8/8"` and `verifier_sha256`; `predicate_holds` must equal `(matched == len(scenarios))`. A receipt that dropped the failing scenario would fail `scenario-census-mismatch`; one that relabelled it would fail `ok-rederivation-mismatch` or `expect-tie-mismatch`.

## Risks / named limits

1. **Population reading.** `R39_ACTIVE_RECEIPTS=6/6` is a binding-integrity count, not a pass count: base is 7/8 and the mutant is 4/8 (`predicate_holds=false`, honest). The round-40 claims P1 only requires `VERIFY: ok` per row, so this is compliant, but any downstream text that renders 6/6 as "all six gates passed" would be wrong.
2. **Path fields are unbound.** The verifier checks digests, not the receipt's `gate`/`counter`/`expectations`/`verifier` path strings; a body naming path A while `--gate` is a byte-identical path B verifies. Pre-existing, documented limit ("integrity and self-consistency, not authorship") — not introduced here.
3. **Provenance of the stale digest is not recoverable.** `corpus/evidence/round39/expectations.jsonl` has a single commit (`6d914e9`) whose blob is `01cbdc3a…`; the draft bytes hashing to `3abd2dcb…` exist in no committed object. The R1 diagnosis therefore rests on (a) four c1 receipts sharing that digest and (b) their embedded expect rows matching the committed table — sufficient to justify re-issue, but the draft file itself cannot be re-opened as evidence.
4. **Coverage note.** This audit covers the base receipt only; `ExecC1LandedReceipt`, `ExecC1MutantReceipt`, and `ExecC1Count` own the other five rows.

## Tooling

No installs, no updates, no pacman transactions. Only `python3`, `sha256sum`, `cmp`, `diff`, `git log/show/ls-tree/status` (read-only) were used.

## Artifacts

- Receipt: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json` (sha256 `e33199c1193ce6f0fb12cef788b41d79d2eb31181bbfdafe3d2f2eba97aa46af`)
- Verifier: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/verify-receipts.py`
- Gate under control: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-39/controls/base-gate-r39.sh`
- Reproduced run: `/tmp/c1base-repro/receipt.json` (byte-identical; transient, not lane evidence)
- Pre-registration: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/claims.md:63-72`
- Stale-before control: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/controls/r1-stale-before.txt`

Files changed: this report only.
