# ScribeKnowledgeC2

## Verdict

C2 re-derives 7/7 on fresh seed 38317 (frozen expectations) and all six committed round-38 receipts re-derived byte-exact at check time; entry drafted below. Two calibration nuances recorded (tamper cells caught by self-digest first; publication does not itself assert pre==post), and two lane-integrity events: working-tree `claims.md` and `expectations.jsonl` were both mutated by another seat during this run, the latter *after* my measurement — `verify-receipts` then refused my receipt with `expect-sha256-mismatch`, which is the binding doing its job.

## Evidence

Ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin`; tip `504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f`; wrote only this report and `/tmp`.

```sh
sha256sum tools/research-gate.sh corpus/evidence/round38/{c1-count,c2-count,verify-receipts}.py corpus/evidence/round38/expectations.jsonl
git rev-parse master
```
gate `37e2b996…d27d` (frozen candidate); c1-count `da1d915b…3f74`; c2-count `bc325cf4…7818`;
verify-receipts `756f186c…7605`; expectations `7cd5d824…ebc9`; tip `504c1d2a…d05f`.

```sh
W=$(mktemp -d /tmp/skb-c2-XXXXXX); C2_TMP=$W python3 corpus/evidence/round38/c2-count.py \
  --gate tools/research-gate.sh --seed 38317 --receipt /tmp/skb-c2-fresh-38317.json; echo EXIT=$?
python3 corpus/evidence/round38/verify-receipts.py --receipt /tmp/skb-c2-fresh-38317.json \
  --gate tools/research-gate.sh --counter corpus/evidence/round38/c2-count.py; echo verify_rc=$?
```
```
PASS hold-receipt-verifies       {'counter_rc': 0, 'receipt': True, 'verify_rc': 0}
PASS self-rewrite-refused        {'counter_rc': 2, 'receipt': False}
PASS foreign-gate-distinguished  {'counter_rc': 0, 'receipt': True, 'verify_foreign_rc': 0, 'verify_landed_rc': 1}
PASS counter-tamper-detected     {'clean_verify_rc': 0, 'verify_rc': 1}
PASS expect-tamper-detected      {'clean_verify_rc': 0, 'verify_rc': 1}
PASS body-tamper-detected        {'clean_verify_rc': 0, 'verify_rc': 1}
PASS legacy-receipt-refused      {'hold_verify_rc': 0, 'counter_rc': 0, 'receipt': True, 'verify_rc': 1}
RECEIPT_BINDING_MATCH=7/7
EXIT=0
VERIFY: ok receipt=skb-c2-fresh-38317.json gate=research-gate.sh counter=c2-count.py
verify_rc=0
```

Committed receipts, each with the counter it binds: all six print `VERIFY: ok`, `rc=0` — `receipts/c1-{after-s38001,after-s38011}.json` and `c1-base-s38001.json` (counter `c1-count.py`; base gate `.ufo/waves/round-37/controls/base-gate-r37.sh` = `a7d3922c…f54e8`), `receipts/c2-{after-s38101,after-s38111,base-s38101}.json` (counter `c2-count.py`). The base receipts verify while `matched` is 2/7 and 0/7, `predicate_holds: false`.

Legacy: `verify-receipts.py --receipt corpus/evidence/round37/receipts/c1-after-s37001.json --gate tools/research-gate.sh --counter corpus/evidence/round37/c1-count.py` → `VERIFY-FAIL: missing-field counter_sha256`, `rc=1`.

Re-stamped doctoring (copy with `receipt_sha256` recomputed, so only the named field can fail):
```
flip-counter -> VERIFY-FAIL: counter-sha256-mismatch rc=1
flip-expect  -> VERIFY-FAIL: expect-sha256-mismatch rc=1
flip-matched -> VERIFY-FAIL: matched-recount-mismatch rc=1
flip-gate-pre-> VERIFY-FAIL: gate-sha-changed-across-run rc=1
```

Integrity (unexpected working-tree changes; not written by this seat). `git diff -- corpus/evidence/round38/claims.md` inserts six lines at 131 (the C1 `LD_PRELOAD`/Erratum-6 limit bullet) absent from `master` (working sha `5950f87e…7687`, master `a651d12e…bee2d`). At 00:49:20 (-03) `expectations.jsonl` changed: three c2 rows lost their `counter_rc` assertion (`hold-receipt-verifies`, `foreign-gate-distinguished`, `legacy-receipt-refused`); working sha `c986c5fd…eefb`, master `7cd5d824…ebc9`. My seed-38317 receipt (written 00:46:19, binding `7cd5d824`) now prints `VERIFY-FAIL: expect-sha256-mismatch`, `rc=1`. Re-run on the mutated table (seed 38329): `RECEIPT_BINDING_MATCH=7/7`, exit 0, `expect_sha256 c986c5fd…`.

## Findings

1. **C2 predicate holds on a fresh seed.** Seed 38317: `RECEIPT_BINDING_MATCH=7/7`, exit 0, receipt verifies `rc=0`, gate pre==post `37e2b996…d27d`. `/tmp/skb-c2-fresh-38317.json`.
2. **Before-state is real.** `receipts/c2-base-s38101.json` (`subject_counter` = r37 `c1-count.py`) is 0/7: r37 counter accepts the self-rewrite shim (rc 0, receipt published), its receipts verify nowhere, its legacy receipt lacks binding fields.
3. **All six committed receipts re-derive; counter identity.** `counter_sha256` matches the scoring counter (`bc325cf4…` c2 receipts, `da1d915b…` c1 receipts), `expect_sha256` `7cd5d824…ebc9`, pre==post everywhere. A c2 receipt binds `c2-count.py` and names the tested counter in `subject_counter`, so verification must pass `--counter c2-count.py`.
4. **Bindings are individually load-bearing; committed tamper cells do not isolate them.** `c2-count.py` `doctor()` rewrites the receipt without recomputing `receipt_sha256`, and `verify-receipts.py:87` checks the self-digest first, so `counter-tamper-detected`/`expect-tamper-detected` can pass on the self-digest alone. The re-stamped probe shows counter, expect, gate and recount bindings each refuse independently.
5. **`verify-receipts` exit 0 is binding truth, not predicate truth.** `receipts/c2-base-s38101.json` verifies `rc=0` with `matched 0/7` because `predicate_holds: false` is self-consistent (`verify-receipts.py:118`). Only c2-count's 7/7 establishes C2.
6. **Publication does not assert pre==post.** `c1-count.py:220-229`, `c2-count.py:277-289` hash before the loop and after each scenario (refusal exit 2, no receipt) but write the receipt without comparing pre/post; a change landing between the last per-scenario check and the post hash would publish a receipt that verify-receipts rejects as `gate-sha-changed-across-run`. The committed self-rewrite fixture (rewrites on first invocation) is refused, so C2 as frozen is not falsified. `[INFERENCE]`, not demonstrated.
7. **`expectations.jsonl` was weakened mid-run (kill-rule-adjacent, not mine).** Three c2 rows dropped `counter_rc` (working `c986c5fd…`, frozen master `7cd5d824…`), after my seed-38317 receipt bound the frozen table. Under the mutated table the predicate still prints 7/7 (seed 38329) but no longer asserts counter rc on three cells — the weakened-fixture case C1's kill rule excludes as a measurement, and the reason C2's `expect_sha256` binding exists. The binding refused my pre-mutation receipt with `expect-sha256-mismatch`.
8. **`claims.md` also differs from `master` (not mine).** Six inserted lines at 131 (C1 LD_PRELOAD limit) contradict the file's own freeze rule ("a later change is an erratum appended below, never an edit"). Reported, not repaired; the C2 section is byte-identical to `master`'s.

*Peer attribution (claim, not evidence):* `chousa-r38` states both working-tree edits are the L1's disclosed wave-1 integration fixes — `counter_rc` decoupling (per `ExecDoNothingCtl` 4/7 finding) and verifier strengthening (per `CritC2Kill` kills) — landing as append-only `claims.md` errata plus regenerated receipts in the next commit. My observations above are of the pre-commit working tree; whether the committed shape is truly append-only errata is for the canonical judge to check on the next revision, and my `7cd5d824`-bound receipts stand as pre-fix evidence.

## Draft knowledge entry — `corpus/knowledge/receipt-binding-r38.md`

```markdown
# Receipt binding — one scoring counter, four digests, fail-closed re-derivation
Lane: chousa. Round 38 (C2, calibration). Surface: `corpus/evidence/round38/{c1-count,c2-count,verify-receipts}.py`, `expectations.jsonl`.
source: `.ufo/waves/round-37/residual/RevC1FreshSeed.md` findings F1 (receipt `gate_sha256` computed post-run only — a self-rewriting gate got a 7/7 receipt stamped with bytes that did not answer every scenario) and F4 (no counter identity — a counter edit keeping seven passes silently redefined P1); frozen design `corpus/evidence/round38/claims.md` §C2; receipts `corpus/evidence/round38/receipts/{c2-base-s38101,c2-after-s38101,c2-after-s38111}.json`.
verified-at: 2026-10-24 (gate `37e2b996…d27d`, c2-count `bc325cf4…7818`; `RECEIPT_BINDING_MATCH=7/7` on fresh seed 38317 and committed seeds 38101/38111)
recheck: on-release (`python3 corpus/evidence/round38/c2-count.py --gate tools/research-gate.sh --seed <n>` → `7/7` with `predicate_holds=true`; each new receipt must pass `verify-receipts.py --counter corpus/evidence/round38/c2-count.py`; any run below 7/7 against the landed gate kills C2)
## What changed
Round-37 receipts stamped the gate hash once, after every scenario, and carried no counter identity. Round-38 receipts bind four facts, all measured by the counter, never by the gate:
- `gate_sha256_pre` — digest before the first scenario (`c1-count.py:220`, `c2-count.py:277`); re-hashed after every scenario, any change exits 2 with "gate bytes changed across the run — no receipt published" (`c1-count.py:224-227`).
- `gate_sha256_post` and alias `gate_sha256` — digest after the last scenario.
- `counter_sha256` — the scoring counter's own file digest (`c1-count.py:244-245`, `c2-count.py:296-297`): the F4 hole closed.
- `expect_sha256` — frozen `expectations.jsonl` digest (`7cd5d824…ebc9`, the master blob): the operative expectations cannot move under a receipt, and a table with any other digest is a different measurement.
- `receipt_sha256` — canonical digest of the receipt body excluding itself (`sort_keys`, indent 2, trailing newline); any doctored field fails.
`verify-receipts.py` re-derives every binding from committed bytes and fails closed, named: `missing-field <k>` (legacy round-37 shape), `receipt-self-digest`, `counter-sha256-mismatch`, `expect-sha256-mismatch`, `gate-sha-changed-across-run`, `gate-sha256-mismatch`, `gate-sha-alias-mismatch`, `matched-recount-mismatch`, `total-recount-mismatch`, `predicate-holds-inconsistent`.
## The seven scenarios (counter `c2-count.py`)
| id | expected observation |
|---|---|
| hold-receipt-verifies | counter rc 0, receipt published, verify rc 0 |
| self-rewrite-refused | counter rc 2, NO receipt (the F1 replay shim) |
| foreign-gate-distinguished | modified gate's receipt verifies against itself (0), fails against the landed gate (1) |
| counter-tamper-detected | clean verifies (0), doctored `counter_sha256` fails (1) |
| expect-tamper-detected | clean verifies (0), doctored `expect_sha256` fails (1) |
| body-tamper-detected | clean verifies (0), doctored `matched`/`predicate_holds` fails (1) |
| legacy-receipt-refused | honest hold verifies (0); r37-counter receipt verifies nowhere (1) |
## Frozen observable
The round-37 counter (the control: the exact pre-round pipeline) scores `RECEIPT_BINDING_MATCH=0/7` (`receipts/c2-base-s38101.json`); the round-38 counters score `7/7` on seeds 38101, 38111 and the fresh 38317, and all six committed receipts re-derive `VERIFY: ok` against the `7cd5d824…` table. Legacy r37 receipts are never re-stamped — `missing-field counter_sha256`.
## Named limits (from claims.md §Limits, frozen)
- A counter or gate that lies end-to-end (prints the expected strings) still scores: black-box observability, the round-37 F2 class. Receipts bind which counter and which expectation bytes judged the run; a forger must attack committed bytes, not stdout alone.
- Seeds namespace only the fixture temp dirs; receipt content is seed-invariant.
- `verify-receipts` exit 0 re-derives bindings, not the predicate: `c2-base-s38101.json` verifies with `matched 0/7` because `predicate_holds: false` is self-consistent; only `7/7` from `c2-count.py` establishes C2.
- The per-scenario refusal catches mid-run rewrites; publication does not assert `pre == post` — `verify-receipts` does (`gate-sha-changed-across-run`).
- `counter_sha256` identifies the scoring counter: c2 receipts bind `c2-count.py`; the tested counter is `subject_counter`.
```

## Limits

- Draft only: lane repo read-only for this seat; `corpus/knowledge/receipt-binding-r38.md` was not written.
- C1 was not exercised here; the draft asserts nothing about C1.
- Findings 4/6 are code reads plus re-stamped doctoring probes; the publication-window race (6) was not attempted.
- No installs; no lane/jj/git mutation by this seat.
