# ExecC1MutantReceipt — regenerated c1-mutenv-s39013 receipt vs the committed PATH-env mutant control

Lane: chousa-shokunin. Round: 40, wave 1. Lane HEAD at audit: `6bc90e04ac60307befacd554f7eee2b7284e2652`; the receipt is the r39 control re-bound at `d164f88`, the mutant gate committed at `6d914e9`. Read-only audit; the only file written is this report.

## Assigned attack

Run the committed verifier for `corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json` against the committed mutant control `.ufo/waves/round-39/controls/mut-gate-path-env.sh` and the committed r39 counter/expectations/verifier; decide whether the **4/8** mutation-control receipt is valid evidence or evidence of a failed verifier.

## Verdict

**Valid — the 4/8 is measured mutant discrimination, not a verifier failure.**

1. The committed verifier accepts the receipt: `VERIFY: ok`, exit 0, with every binding re-derived (self-digest, counter, expectations, verifier, gate pre/post bytes, scenario census, per-row expectation tie, `ok` flags, matched count, `predicate_holds`).
2. `4/8` is the value **pre-registered in the r39 frozen claims** for this exact mutant at this exact seed (`corpus/evidence/round39/claims.md:74-80`), and I reproduced it live against the committed mutant bytes: `ENV_PIN_CAPTURE_MATCH=4/8`. The live run reproduced the committed receipt **byte for byte, including its self-digest** `e362c695…`.
3. The same counter at the same seed scores **8/8** on the landed gate and 7/8 on the base control. Same table, same harness, different bytes: the 4/8 is a property of the mutant gate.
4. The four failing scenarios are exactly the cells the mutant's single hunk re-opens (three `BASH_FUNC_env%%` cells + the `path_env_shim_echo` hold); every bash-pin cell, both override refusals, and both holds still pass. That is the signature of a PATH-poisonable `env` pin, not of a broken verifier.
5. The verifier is not a rubber stamp: it refuses the stale r39 original by name (`expect-sha256-mismatch`), an 8/8 label without re-derived observations (`matched-recount-mismatch`), a dropped failing scenario (`scenario-census-mismatch`), and the receipt pointed at the landed gate (`gate-sha256-mismatch`).

Reading caution: `VERIFY: ok` certifies binding integrity and internal consistency, **not** that the gate under test passed. The mutant arm's own counter exit is 1 (`predicate_holds=false`) by design; that exit belongs to the mutation measurement, not to verification. The row's `ok` in `R39_ACTIVE_RECEIPTS=6/6` means "this receipt re-derives", not "this gate reached 8/8". This receipt must never be cited as 8/8 evidence.

## Exact commands and output

All commands run at the lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

### 1. Committed verifier on the regenerated mutant receipt

```
python3 corpus/evidence/round39/verify-receipts.py \
  --receipt corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json \
  --gate .ufo/waves/round-39/controls/mut-gate-path-env.sh \
  --counter corpus/evidence/round39/c1-count.py \
  --expectations corpus/evidence/round39/expectations.jsonl
```
```
VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
rc=0
```

This is the exact per-row invocation the frozen round-40 counter issues (it passes the manifest's gate and counter columns with the committed expectations file). The frozen counter's full run confirms the row is integrated as `ok`:

```
python3 corpus/evidence/round40/c1-count.py
…
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: ok VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
…
R39_ACTIVE_RECEIPTS=6/6
COUNTER_RC=0
```

### 2. Independent re-derivation of the 4/8 measurement

```
mkdir -p /tmp/c1r40-repro
python3 corpus/evidence/round39/c1-count.py \
  --gate .ufo/waves/round-39/controls/mut-gate-path-env.sh \
  --seed 39013 --tmp /tmp/c1r40-repro \
  --receipt /tmp/c1r40-repro/mut-s39013-live.json
```
```
PASS hold-plain           observed={pin_rc: 0, pin_file: True, echo_lines: 0, drift_rc: 0, drift_line: 'GATE_DRIFT: none'}
PASS hold-fn-benign       observed={pin_rc: 0, pin_file: True, echo_lines: 0, drift_rc: 0, drift_line: 'GATE_DRIFT: none'}
FAIL env-fn-echo-scrub    observed={pin_rc: 0, pin_file: True, echo_lines: 1, drift_rc: 1, drift_line: 'GATE_DRIFT: -GATE_GREP'}
FAIL env-fn-root-move     observed={pin_rc: 0, pin_file: True, echo_lines: 0, drift_rc: 1, drift_line: 'GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused root supported tallies tally verdict verified'}
FAIL env-fn-suppress      observed={pin_rc: 2, pin_file: False, echo_lines: -1, drift_rc: 2, drift_line: ''}
PASS env-override-missing observed={pin_rc: 2, pin_file: False, refusal: 'ENV_PROVENANCE'}
PASS env-override-fake    observed={pin_rc: 2, pin_file: False, refusal: 'ENV_PROVENANCE'}
FAIL capture-bash-path-pin (only path_env_shim_echo.* fails: echo_lines 0→1, drift_rc 0→1, drift_line 'GATE_DRIFT: none'→'GATE_DRIFT: -GATE_GREP'; the four bash/override cells hold)
ENV_PIN_CAPTURE_MATCH=4/8
COUNTER_RC=1
```

Comparison against the committed receipt:

```
live matched/total/holds: 4 8 False
scenarios identical to committed regenerated: True
full receipt identical except receipt_sha256: True
live receipt_sha256:      e362c695452b7e5be8853c8d3abb3233590ee0686d63858ec5b1651f0a2642bc
committed receipt_sha256: e362c695452b7e5be8853c8d3abb3233590ee0686d63858ec5b1651f0a2642bc
```

Every field, including the self-digest, is identical: the committed file is genuine counter output, not a hand-edited or partially re-sealed receipt. The counter is deterministic (no clock in the body), so this reproduces across runs.

### 3. Contrast arms at the same seed

```
python3 corpus/evidence/round39/c1-count.py --gate tools/research-gate.sh --seed 39013 --tmp /tmp/c1r40-repro
… ENV_PIN_CAPTURE_MATCH=8/8 ; rc=0
```

| gate under the same counter and table | matched | counter exit |
|---|---|---|
| base control `.ufo/waves/round-39/controls/base-gate-r39.sh` (seed 39001, sibling `ExecC1BaseReceipt`) | 7/8 | 1 |
| **mutant control `mut-gate-path-env.sh` (seed 39013, this audit)** | **4/8** | **1** |
| landed gate `tools/research-gate.sh` (seed 39013, this audit; seeds 39011/39111 committed) | 8/8 | 0 |

A verifier/harness breakage would depress the landed arm too; it does not.

### 4. The mutant is one hunk off the landed gate, at the env-pin call site

```
diff .ufo/waves/round-39/controls/mut-gate-path-env.sh tools/research-gate.sh
4068c4068
<     env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_ROOT \
---
>     "$ENV_BIN" -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_ROOT \
```

Exactly one line differs: the canonical capture child reverts from the round-38 pinned `"$ENV_BIN"` to a bare `env`. (`diff base-gate-r39.sh mut-gate-path-env.sh` is 152 lines: the whole round-39 bash-pin block plus this regression, which is why the mutant still holds the bash-pin cells and 8/8's sibling arm is the landed bytes.) The mechanism maps one-to-one onto the failures:

| failing scenario | why the bare-`env` mutation causes it |
|---|---|
| `env-fn-echo-scrub` | bash resolves an exported `env` function before PATH, so the capture child re-adds `CHOUSA_GREP_PIN_ECHO`; the baseline embeds a `GATE_GREP:` line and a plain `--drift` reports `-GATE_GREP` (the hostile-drift vector). |
| `env-fn-root-move` | the same function re-adds `CHOUSA_ROOT` at a foreign root; the fixture capture drifts on findings/root/tallies tokens. |
| `env-fn-suppress` | the function suppresses the capture (`pin_rc=2`, no baseline) while `--pin` refuses honestly. |
| `path_env_shim_echo` (inside `capture-bash-path-pin`) | bare `env` resolves through the caller's PATH, so the PATH `env` shim re-adds the echo. |
| passing holds/overrides | `hold-plain`, `hold-fn-benign` (benign forwarder), both `ENV_PROVENANCE` refusals, `path_bash_shim_*`, `override_honoured`, `override_relative_refused` exercise the untouched bash pin or the pre-capture refusal path, which the env hunk does not reach. |

This is exactly the failure set the r39 claims named in advance: "the three round-38 `BASH_FUNC_env%%` cells re-open … AND `path_env_shim_echo` fails" (`corpus/evidence/round39/claims.md:74-80`).

### 5. Regeneration repaired the expectation binding; it did not re-measure different bytes

Old r39 file `corpus/evidence/round39/receipts/c1-mutenv-s39013.json` under current committed bindings:

```
VERIFY-FAIL: expect-sha256-mismatch
rc=1
```

Field-by-field comparison of old vs regenerated:

```
changed top-level fields: ['expect_sha256', 'receipt_sha256']
scenarios identical: True
old expect_sha256: 3abd2dcb1766c404228cf3929024856240a93ea374760ab77a390b92c3fb6480
new expect_sha256: 01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a
counter_sha256 identical: 91618e91640f748df76282244186088218d5f2b7a65364137fa6add29fea05d5
```

Only the stale expectation digest and the self-digest changed. The 4/8 observation is preserved from the r39 committed run, and my independent r40 re-run confirms it on the current bytes. The old file is correctly preserved and excluded from the active population; it is refused now, which is why the regenerated copy is required.

### 6. Refusal probes (the accept is not vacuous)

| probe (re-sealed where applicable) | verifier result |
|---|---|
| mutant receipt against the **landed** gate `tools/research-gate.sh` | `VERIFY-FAIL: gate-sha256-mismatch`, rc=1 |
| `matched=8`, `predicate_holds=true` without re-derived observations | `VERIFY-FAIL: matched-recount-mismatch`, rc=1 |
| `env-fn-suppress` scenario dropped, counts adjusted | `VERIFY-FAIL: scenario-census-mismatch`, rc=1 |
| the stale r39 original under current bindings | `VERIFY-FAIL: expect-sha256-mismatch`, rc=1 |
| `env-fn-suppress` observed values relabelled to the expected five keys, `ok=true`, matched recomputed to 5, re-sealed | **accepted** (`VERIFY: ok`, rc=0) — see limit 2 |

### 7. Committed bytes at HEAD match the audited bytes

```
git show HEAD:corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json | sha256sum
ac2c24fa10406fad8c60cb7225b43632ccd8ac7fe5372df8b86d2ce5e8150fcb  -
git show HEAD:.ufo/waves/round-39/controls/mut-gate-path-env.sh | sha256sum
e1251030ef61722cbba94b4645bd3dced2c8460b2fef89458f488f01c2bd231a  -
git show HEAD:corpus/evidence/round39/verify-receipts.py | sha256sum
1b6e0de688deda7493db3af5397d1e5bbf1fcdf556d8e254acae3ac6a8496267  -
git show HEAD:corpus/evidence/round39/expectations.jsonl | sha256sum
01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a  -
git show HEAD:corpus/evidence/round39/c1-count.py | sha256sum
91618e91640f748df76282244186088218d5f2b7a65364137fa6add29fea05d5  -
```

The receipt's own bindings equal those bytes: `gate_sha256 = gate_sha256_pre = gate_sha256_post = e1251030…`, `counter_sha256 = 91618e91…`, `expect_sha256 = 01cbdc3a…`, `verifier_sha256 = 1b6e0de6…`. The file digest of the receipt itself is `ac2c24fa…`; `receipt_sha256 = e362c695…` is the body digest by design (the field excludes itself). `git status --porcelain` over the receipt directory, the verifier/expectations/counters and the mutant control is empty.

## Calibration reading

- The 4/8 is **control evidence**: it demonstrates that the eight-scenario harness discriminates a PATH-poisonable `env` from the pinned one. It is not a claim that four of eight capabilities work.
- The count is over **scenarios**, not independent defects. One single-line regression collapses three env-function scenarios and one of the five cells inside the composite `capture-bash-path-pin` scenario; `4/8` therefore understates the mutant's loss rather than overstating it.
- Two of the six active receipts legitimately carry `predicate_holds=false` (base 7/8, mutant 4/8). `R39_ACTIVE_RECEIPTS=6/6` is a receipt-integrity count under the frozen P1, not a gate-pass count. Any downstream sentence rendering 6/6 as "six gates passed" would be wrong; the mutant row is negative-control evidence.

## Risks / named limits

1. **`VERIFY: ok` is a consistency verdict.** The verifier re-derives rows from the receipt's own `observed` values against the frozen expectation table; it never executes the gate. Probe 6E demonstrates that a consistently relabelled receipt is accepted. The load-bearing provenance for this receipt is therefore the **byte-identical live re-run** in §2, not the verifier alone. This is the documented authorship limit ("does not authenticate authorship"), carried from round 38.
2. **Path strings are unbound.** The verifier hashes the bytes passed on the CLI, not the receipt's `gate`/`counter`/`expectations`/`verifier` path fields. A byte-identical gate at another path would verify. Not specific to this receipt; it is why the committed blob digests in §7 matter.
3. **The seed field is provenance only.** The r39 counter records `--seed` but derives no scenario from it; with fixed gate/expectation bytes the receipt body is deterministic across seeds. The three arms are distinguished by gate bytes, not seed.
4. **A regressed landed gate could carry a `predicate_holds=false` receipt that still verifies** given consistent rows. Nothing in the round-40 counter binds "this receipt's arm must be the control"; the manifest comment and the committed gate path are the only markers. Today the gate bytes (`e1251030…`) and the pre-registered 4/8 make the arm unambiguous.
5. **Coverage note.** This report audits the mutant-control row only. `ExecC1BaseReceipt`, `ExecC1LandedReceipt`, and `ExecC1Count` own the other active rows; the population run in §1 is quoted for row integration, not as an independent population audit.

## Tooling

No installs, no updates, no pacman transactions. Only `python3`, `sha256sum`, `diff`, and read-only `git show/rev-parse/status` were used. Scratch receipts and probe fixtures live under `/tmp/c1r40-repro` and `/tmp/c1r40-probes` (transient, not lane evidence).

## Artifacts

- Receipt: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json` (file sha256 `ac2c24fa10406fad8c60cb7225b43632ccd8ac7fe5372df8b86d2ce5e8150fcb`; body digest `e362c695452b7e5be8853c8d3abb3233590ee0686d63858ec5b1651f0a2642bc`; 4/8, `predicate_holds=false`)
- Mutant control: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-39/controls/mut-gate-path-env.sh` (sha256 `e1251030ef61722cbba94b4645bd3dced2c8460b2fef89458f488f01c2bd231a`)
- Landed gate: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` (sha256 `4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3`)
- Verifier: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/verify-receipts.py` (sha256 `1b6e0de688deda7493db3af5397d1e5bbf1fcdf556d8e254acae3ac6a8496267`)
- Counter: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/c1-count.py` (sha256 `91618e91640f748df76282244186088218d5f2b7a65364137fa6add29fea05d5`)
- Expectations: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/expectations.jsonl` (sha256 `01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a`)
- Pre-registration of 4/8: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/claims.md:74-80`
- Stale original (preserved, refused): `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/receipts/c1-mutenv-s39013.json`
- Live reproduction: `/tmp/c1r40-repro/mut-s39013-live.json` (byte-identical to the committed receipt, self-digest included; transient)

Files changed: this report only.
