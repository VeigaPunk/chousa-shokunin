# W2RevVerifyFinal

## Verdict
The strengthened verifier refuses every assignment bypass except one class it still accepts: a re-sealed receipt can doctor the asserted refusal *labels* (`verify_fail`) and all provenance strings, and carry extra fields inside scenario rows, and still print `VERIFY: ok` — the strict-schema fix is one level too shallow. No honest receipt regressed.

## Evidence

Both byte states observed (the file changed under me mid-seat, per L1 notice):

```
$ sha256sum corpus/evidence/round38/verify-receipts.py
3fc416612085a4ba8333b6b39a9ad2f4e32eb17ebcbc53ae6cd2e048f8abf919   # working tree (strict schema, +10 lines)
$ git show master:corpus/evidence/round38/verify-receipts.py | sha256sum
b63e7e200b88022f6747e4b628cb6b251187ad95f5b33d2b6b4b14e08d5cf952   # master 8e93bc9
$ git diff master -- corpus/evidence/round38/verify-receipts.py   # adds KNOWN field set + unknown-field refusal at :73,:128-130
```
All attacks below were re-run on **3fc41661** (identical verdicts on **b63e7e20** except the strict-schema cells, noted). Honest receipts re-checked on both byte states.

```
$ cd chousa-shokunin && python3 corpus/evidence/round38/verify-receipts.py \
    --receipt corpus/evidence/round38/receipts/<f> --gate <f's own gate field> --counter <family counter>
c1-after-s38001 ok | c1-after-s38011 ok | c1-after-s38351 ok | c2-after-s38101 ok
c2-after-s38111 ok | c2-after-s38371 ok | c2-base-s38101 ok (binds landed gate; subject=round37/c1-count.py, matched=0)
c1-base-s38001 ok (own gate base-gate-r37.sh) | c1-base2-s38003 ok (own gate base-gate-r38.sh)
9/9 VERIFY: ok against their own bound gate; the two c1 base receipts on the *landed* gate:
VERIFY-FAIL: gate-sha256-mismatch  (separability claim confirmed)
```
Fresh-seed honest runs (new bytes; c2 run spanned the byte change, final verify on 3fc41661):
```
C1_TMP=/tmp/w2rev-c1tmp python3 corpus/evidence/round38/c1-count.py --gate $PWD/tools/research-gate.sh \
    --seed 38403 --receipt /tmp/w2rev-verify/c1-fresh-38403.json      -> ENV_PIN_CAPTURE_MATCH=7/7 ; verify ok
C2_TMP=/tmp/w2rev-c2tmp python3 corpus/evidence/round38/c2-count.py --gate $PWD/tools/research-gate.sh \
    --seed 38401 --receipt /tmp/w2rev-verify/c2-fresh-38401.json      -> RECEIPT_BINDING_MATCH=7/7 ; verify ok
```
c2's seven cells on seed 38401 re-derived the three tamper refusals by name (`counter-sha256-mismatch`,
`expect-sha256-mismatch`, `receipt-self-digest`) and `hold_verify_rc: 0` on the legacy receipt.
Assignment bypasses, receipts synthesized from `receipts/c1-after-s38001.json` / `c2-after-s38101.json`, re-sealed with the published digest algorithm, run as `python3 verify-receipts.py --receipt /tmp/w2rev-verify2/<n>.json --gate tools/research-gate.sh --counter <abs counter>`:

| attack | rc | exact output |
|---|---|---|
| duplicate scenario ids (7 rows) | 1 | `VERIFY-FAIL: scenario-census-mismatch` |
| scenario id as int `7` | 1 | `TypeError: '<' not supported between instances of 'str' and 'int'` (traceback, **no label**) |
| expect dict + injected `receipt_contains` | 1 | `VERIFY-FAIL: expect-tie-mismatch hold-receipt-verifies` |
| scenarios as a dict | 1 | `VERIFY-FAIL: scenarios-not-a-list` |
| `matched` as string `"7"` | 1 | `VERIFY-FAIL: matched-recount-mismatch` |
| one `ok` flipped + re-sealed | 1 | `VERIFY-FAIL: ok-rederivation-mismatch hold-plain` |
| c2 receipt, `--counter c1-count.py` as-is | 1 | `VERIFY-FAIL: counter-sha256-mismatch` |
| same, counter_sha256 swapped to c1 + re-sealed | 1 | `VERIFY-FAIL: predicate-mismatch` |
| observed + extra keys (`extra`, `drift_contains`) | 0 | `VERIFY: ok` (required; extra observations not refused) |

New-bytes probes:
```
[top-extra-field]       rc=1 VERIFY-FAIL: unknown-field extra_top
[row-extra-field]       rc=0 VERIFY: ok                      # extra key INSIDE scenarios[i]
[provenance-deleted]    rc=0 VERIFY: ok                      # gate,counter,seed,expectations,subject_counter all removed
[identity-strings-swapped] rc=0 VERIFY: ok                   # gate=/tmp/not-the-gate.sh expectations=/tmp/fake.jsonl counter=/tmp/other.py
[verify_fail-doctored]  rc=0 VERIFY: ok                      # observed.verify_fail := "VERIFY-FAIL: nothing"
[verify_fail-deleted]   rc=0 VERIFY: ok                      # observed.verify_fail removed entirely
[int-launder]           rc=0 VERIFY: ok                      # ok:1, matched:7.0
[evil-counter]          rc=0 VERIFY: ok                      # /tmp/evil/c1-count.py, forged comment, digest rebound
[doctored-table]        rc=0 VERIFY: ok                      # --expectations /tmp/doctored.jsonl, expect loosened to "FAKE"
```
Verifier bytes unchanged before/after the probe batch (`3fc41661`), so the results are a single stable state.

## Findings

1. **`_contains` expectations are never re-derived (medium).** At `verify-receipts.py:169-174` the `ok` re-derivation skips every frozen key ending `_contains`; nothing else checks containment. Consequence: `observed.verify_fail` may be altered to any string or deleted, re-sealed, and the receipt still prints `VERIFY: ok` — demonstrated above for `counter-tamper-detected`. This is exactly the "re-sealed doctoring of the observations" the module docstring promises fails, and the only evidence binding the tamper doctors' asserted refusal labels. The producer does enforce it (`c2-count.py:260-261`), so honest receipts are sound; the verifier's re-derivation claim is not.
2. **Strict schema is top-level only (medium).** `KNOWN` (`verify-receipts.py:73`) rejects an added top-level field (`unknown-field extra_top`) but not an added key inside a scenario row (`row-extra-field` → ok). Same fixture class as the one Erratum 9 closed, one nesting level deeper: `scenarios[i]{"note":"x"}` survives.
3. **Provenance strings are neither required nor bound (medium).** `REQUIRED` (`:69-71`) omits `gate`, `counter`, `expectations`, `seed`, `subject_counter`; the verifier binds only digests, never the body's identity fields. Deleting all five verifies ok, and swapping them to unrelated paths (`/tmp/not-the-gate.sh`, `/tmp/fake.jsonl`) verifies ok while the run is checked against the real `--gate`/`--counter`. A reader of the receipt cannot rely on the body's provenance fields. (The `verifier_sha256` debt is already named in Erratum 2; this is the counter/table/gate half of it.)
4. **"Frozen" table and counter are pinned to the CLI file, not to a canonical digest (low–medium, claim accuracy).** Docstring/Erratum 2 say "against committed bytes". Demonstrated false as stated: `/tmp/evil/c1-count.py` (forged comment, digest rebound) verifies ok, and `--expectations /tmp/doctored.jsonl` with `env-override-missing.expect.refusal="FAKE"` plus a matching observation verifies ok. Only the caller's chosen path is bound; `FAMILIES` (`:57-60`) carries no pinned counter sha and no pinned table sha.
5. **Unlabeled crash on a malformed id (low).** `ids = sorted(s.get("id") ...)` (`:156-157`) raises `TypeError` on mixed/absent id types (int `7`; missing id → `None`). Exit code is 1, so it refuses, but a consumer keying on `VERIFY-FAIL:` sees no refusal line. A `None`/int id is unfalsifiable as "refused by name".
6. **Python-equality type laundering (low).** `ok: 1`, `matched: 7.0` (and `predicate_holds: 1`) pass `:174-179` because `1 == True` and `7.0 == 7`; a strict JSON consumer (`jq '.matched == 7'` is true, but `.scenarios[].ok == true` is false for `1`) reaches the opposite verdict on the same receipt.

No defect found in the equality-key path: duplicate ids, expect injection, dict-shaped scenarios, string arithmetic, flipped `ok`, cross-family counter, empty census, non-dict row, legacy receipt and gate-digest tamper all refuse by name (table above).

## Limits
- No LSP server/tool was exposed to this seat (`lsp` is absent from the tool inventory); caller/definition/diagnostic checks were done by reading `verify-receipts.py:69-191`, the producer assertion at `c2-count.py:260-261` and the frozen table textually. Recorded as tooling unavailability, not as semantic proof.
- Attacks are on the verifier alone; gate/counter mutant sweeps were other seats' scope. Fresh-seed receipts generated: c1 seed 38403, c2 seed 38401, both 7/7 and both VERIFY: ok.
- Synthetic receipts live in `/tmp/w2rev-verify*`; nothing in the lane repo, its jj/git state, or `/tmp` inputs of other seats was modified. No tools installed or upgraded.
