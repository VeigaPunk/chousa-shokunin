# chousa-r38.W2MutVerifyFinal

## Verdict
Of six plausible weakenings of the strengthened `verify-receipts.py`, only **M2 (self-digest skipped) is
killed** by the strengthened c2 predicate (`RECEIPT_BINDING_MATCH=6/7`, seed 38403); **M1, M3, M4, M5, M6
all survive at 7/7** — the census and ok-re-derivation checks added in wave 1 are implemented but never
exercised by the predicate that certifies them, and the same pass-through holds on final lane bytes for
the four probes I could re-run.

## Evidence
Base bytes = lane `corpus/evidence/round38/verify-receipts.py` sha256
`b63e7e200b88022f6747e4b628cb6b251187ad95f5b33d2b6b4b14e08d5cf952` (read at probe start, lane tip
`8e93bc916527b3c21f0f702967fa65c3b4c31699`). Scratch layout `/tmp/w2mv-b70b17/`:
`m0..M6/round38/{c1-count,c2-count,expectations.jsonl,verify-receipts.py}` + `round37/c1-count.py`
(counters `c1-count.py 79040790…`, `c2-count.py 414a7a10…`, expectations `d34f1735…` byte-copied; only the
verifier is swapped). Gate untouched: `tools/research-gate.sh 37e2b996…` (equals claims.md candidate).

Mutant hashes (sha256 of verifier): M1 accept-missing-`gate_sha256_pre` `16158728…`; M2 skip self-digest
`fe77aea6…`; M3 drop `pre!=post` `494af355…`; M4 `.lower()` both sides of all six hash equals `790b0d79…`;
M5 drop `scenario-census-mismatch` `934747e5…`; M6 drop `ok-rederivation-mismatch` `63edc7e5…`.

Command per mutant (parallel, 7 workers, clean env with `BASH_FUNC_*`/`BASH_ENV`/`ENV`/`SHELLOPTS`/`BASHOPTS`/`CHOUSA_*`/`RESEARCH_GATE_*` scrubbed):
`python3 /tmp/w2mv-b70b17/<m>/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed <N> --tmp /tmp/w2mv-b70b17/tmp-<m> --receipt .../c2-receipt.json`

Observed c2 predicate (all runs rc and count; wall ~131 s each, concurrent):

| mut | seed | c2 result | failing cell | observed vs expected |
|---|---|---|---|---|
| m0 pristine | 38401 | rc=0 `RECEIPT_BINDING_MATCH=7/7` | — | all PASS |
| M1 | 38402 | rc=0 `7/7` | none | **SURVIVED** |
| M2 | 38403 | rc=1 `6/7` | `body-tamper-detected` | `VERIFY-FAIL: matched-recount-mismatch` vs expected `receipt-self-digest` |
| M3 | 38404 | rc=0 `7/7` | none | **SURVIVED** |
| M4 | 38405 | rc=0 `7/7` | none | **SURVIVED** |
| M5 | 38406 | rc=0 `7/7` | none | **SURVIVED** |
| M6 | 38407 | rc=0 `7/7` | none | **SURVIVED** |

Receipts bound the copied bytes, not the lane: m0 c2 receipt `gate_sha256_pre 37e2b996…`, `counter_sha256
414a7a10…`, `expect_sha256 d34f1735…`, `matched 7/7`, `predicate_holds true`.

MutVerify-original probes (honest receipt `/tmp/w2mv-b70b17/probe/honest.json`,
`1a14098a…`, from the copied c1 counter seed 38411, `ENV_PIN_CAPTURE_MATCH=7/7`), verifier command
`python3 <m>/round38/verify-receipts.py --receipt <fx> --gate <gate> --counter <m>/round38/c1-count.py --expectations <m>/round38/expectations.jsonl`:

| fixture (sha256) | m0 | M1 | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|---|
| honest | 0 OK | 0 OK | 0 OK | 0 OK | 0 OK | 0 OK | 0 OK |
| `d-field-only` `d16bf733…` (seed 38411→38412, no re-digest) | 1 `receipt-self-digest` | 1 same | **0 OK** | 1 same | 1 same | 1 same | 1 same |
| `d-upper` `954ffdd0…` (upper-case gate hashes, re-digest) | 1 `gate-sha256-mismatch` | 1 same | 1 same | 1 same | **0 OK** | 1 same | 1 same |
| `d-missing-pre` `21621997…` (extra) | 1 `missing-field gate_sha256_pre` | **0 OK** | 1 same | 1 same | 1 same | 1 same | 1 same |
| `d-post-moved` `df0fa5f7…` (extra) | 1 `gate-sha-changed-across-run` | 1 same | 1 same | **0 OK** | 1 same | 1 same | 1 same |

Mid-probe the lane verifier changed by sibling edits (parent irc: Erratum 9 strict schema): observed
`b63e7e20…` → `3fc41661…` → `33c7c87e…` (`33c7c87e…`, 8603 bytes, at probe end; unchanged after). Diff is
additive/orthogonal: `unknown-field`, `scenario-row-malformed`, `ok-type-mismatch`, `count-type-mismatch`,
`predicate-holds-type-mismatch`. Re-ran the five fixtures on a byte copy of `33c7c87e…`: identical to m0
rows above. A c2 run on those bytes (seed 38408) returned rc=2, `c2-count: gate bytes changed across the
run (pre 37e2b9968706adab vs current) — no receipt published` — a sibling landed the gate under it
(now `0447ad14…`), i.e. the counter's own changed-gate refusal firing, not a mutant result.

## Findings
1. **M2 is the only kill, and the kill is label-coupled.** With the self-digest check deleted, c2's
   `body-tamper-detected` still refuses (rc=1) but at `matched-recount-mismatch`; the frozen expectation pins
   `verify_fail_contains: receipt-self-digest`, so the cell fails → 6/7. The three tamper cells' re-sealed
   doctors never reach the deleted check (their `counter_sha256`/`expect_sha256` refusals fire first), and
   `d-field-only` succeeds under M2 (rc=0): a receipt whose `seed` was edited and not re-digested verifies.
   Pointer: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py:191-232`
   (`doctor(..., re_digest=True)` for counter/expect only; body stays unsealed).
2. **M5 (census skipped) survives 7/7 — the strengthened census check has no scenario.** No c2 cell edits
   `scenarios` (add/remove/duplicate a row), so `scenario-census-mismatch` is unreachable in the predicate.
   Pointer: `verify-receipts.py:157-160` (`len(scenarios) != len(frozen) or ids != sorted(frozen)`), versus
   the seven fixture cells in `c2-count.py:163-236`, none of which touches the row set.
3. **M6 (per-row `ok` re-derivation skipped) survives 7/7 — unreachable for the same reason plus shadowing.**
   The body doctor flips `matched`/`predicate_holds` without re-sealing, so `receipt-self-digest` refuses
   first; even with the digest bypassed the cell would die on `matched-recount-mismatch`, not the `ok`
   equality. No fixture ships a row whose stored `ok` disagrees with its observations but whose count
   agrees. Pointer: `verify-receipts.py:162-174`; `c2-count.py:222-231`.
4. **M1 and M3 survive 7/7; their probes separate them.** `d-missing-pre` verifies rc=0 under M1 and
   `d-post-moved` rc=0 under M3 — both remain refused by pristine and by final lane bytes. c2 exercises
   neither shape: `legacy-receipt-refused` drops *all* binding fields (caught at `counter_sha256`), and
   `self-rewrite-refused` publishes **no** receipt, so `gate-sha-changed-across-run` is never reached by the
   verifier. Pointer: `c2-count.py:233-245` (self-rewrite refusal asserted on the counter's rc, not on a
   receipt); `verify-receipts.py:141-154`.
5. **M4 survives 7/7; `d-upper` separates it.** Case-folding all six hash equals accepts an upper-cased
   `gate_sha256{,_pre,_post}` receipt (rc=0) while pristine and final bytes refuse
   `gate-sha256-mismatch`. No c2 fixture varies hash case. Pointer: `verify-receipts.py:126-153`.
6. **Coverage, not contract:** every survivor is refused by a sub-second, no-gate fixture already defined in
   the wave-1 report (`d-missing-pre`, `d-post-moved`, `d-upper`, `d-field-only`); adding them (or a
   re-sealed row-census/ok doctor) to `c2-count.py` would bind what C2 claims. This seat changes no contract.
7. **The final-bytes strict-schema additions do not disturb these verdicts** (fixture re-run identical on
   `33c7c87e…`); the only final-byte c2 attempt was voided by a concurrent gate landing, recorded above.

## Limits
- c2 predicate results are on base bytes `b63e7e20…` (the state at probe start), not the final `33c7c87e…`;
  a full 7/7 baseline on final bytes could not be measured because the gate changed mid-run (rc=2). The
  probe-level equivalence on `33c7c87e…` is direct, the predicate-level equivalence is inferred.
- No M7/M8 (delete `counter_sha256`/`expect_sha256` comparisons) mutants were run; by the refusal ordering
  observed they would be caught by the re-sealed cells, but that is unexecuted.
- I did not mutate the counters or the gate; only `verify-receipts.py` copies in `/tmp`. No lane/fleet write
  outside this report; no `git`/`jj` mutation. No tools installed or upgraded.
