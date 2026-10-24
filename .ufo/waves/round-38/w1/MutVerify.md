# chousa-r38.MutVerify

## Verdict
All four plausible weakenings of `verify-receipts.py` are killed by targeted receipts but every one
of them still scores `RECEIPT_BINDING_MATCH=7/7` on the frozen C2 predicate — the predicate is a
pass-through for exactly the defect classes it claims to bind.

## Evidence

Lane tip `504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f`. Verifier under test
`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/verify-receipts.py`
sha256 `756f186c3487461b9c29de5ebbb4b91392706ecc4b5ff8f3a83d482fcaf27605` (identical before and
after the probe; read-only re-hash at the end of the run). All mutation work in scratch
`/tmp/mutverify-r38-wpOz6r/`; c2 probe layouts in `/tmp/mutverify-r38-probe{,-m1,-m2,-m3,-m4}/`.

Base receipt `/tmp/mutverify-r38-wpOz6r/base.json` sha256
`1d7c80cf7e0e807d22550ff53c645862fd48705ef99d35d9df2415e4f9f0112f`, `cmp`-identical to
`corpus/evidence/round38/receipts/c1-after-s38001.json`. Doctored fixtures re-derive
`receipt_sha256` unless stated (canonical `json.dumps(indent=2, sort_keys=True)+"\n"`), so the
targeted binding check, not the self-digest, decides:

| fixture (sha256) | doctoring |
|---|---|
| `d-missing-pre` `f6411051…` | drop `gate_sha256_pre`, re-digest |
| `d-post-moved` `5b16e0e4…` | `gate_sha256_post=0*64`, re-digest |
| `d-upper` `46b8109c…` | upper-case `gate_sha256{,_pre,_post}`, re-digest |
| `c2-counter-flip` `2f054bb7…` | exact `c2-count.py doctor()` flip, **no** re-digest |
| `c2-expect-flip` `2a5d82fe…` | exact `doctor()` flip, **no** re-digest |
| `c2-body-flip` `ed373ec2…` | exact `doctor()` `matched-1`+`predicate_holds` flip, **no** re-digest |
| `d-field-only` `10d51033…` | `seed 38001→38002`, no re-digest |

Command per cell:
`python3 /tmp/mutverify-r38-wpOz6r/<verifier>.py --receipt <fixture> --gate <lane>/tools/research-gate.sh --counter <lane>/corpus/evidence/round38/c1-count.py --expectations <lane>/corpus/evidence/round38/expectations.jsonl`

Observed (rc + first stdout line; `OK` = `VERIFY: ok`):

| fixture | m0 pristine | m1 `42930190…` | m2 `171f632b…` | m3 `eba8bae1…` | m4 `d436392b…` |
|---|---|---|---|---|---|
| honest | 0 OK | 0 OK | 0 OK | 0 OK | 0 OK |
| d-missing-pre | 1 `missing-field gate_sha256_pre` | **0 OK** | 1 same | 1 same | 1 same |
| d-post-moved | 1 `gate-sha-changed-across-run` | 1 same | 1 same | **0 OK** | 1 same |
| d-upper | 1 `gate-sha256-mismatch` | 1 same | 1 same | 1 same | **0 OK** |
| c2-counter-flip | 1 `receipt-self-digest` | 1 `receipt-self-digest` | 1 `counter-sha256-mismatch` | 1 `receipt-self-digest` | 1 `receipt-self-digest` |
| c2-expect-flip | 1 `receipt-self-digest` | 1 `receipt-self-digest` | 1 `expect-sha256-mismatch` | 1 `receipt-self-digest` | 1 `receipt-self-digest` |
| c2-body-flip | 1 `receipt-self-digest` | 1 `receipt-self-digest` | 1 `matched-recount-mismatch` | 1 `receipt-self-digest` | 1 `receipt-self-digest` |
| d-field-only | 1 `receipt-self-digest` | 1 `receipt-self-digest` | **0 OK** | 1 `receipt-self-digest` | 1 `receipt-self-digest` |

Mutations (unified diffs vs pristine, `/tmp/mutverify-r38-wpOz6r/m0-pristine.py`):
- **M1 accept missing `gate_sha256_pre`**: drop it from `REQUIRED`; guard both comparisons with
  `pre = receipt.get("gate_sha256_pre"); if pre is not None and pre != …`.
- **M2 skip self-digest**: replace `if receipt["receipt_sha256"] != receipt_digest(receipt): return
  fail("receipt-self-digest")` with a comment.
- **M3 compare pre only**: delete the `pre != post` block (`gate-sha-changed-across-run`).
- **M4 case-insensitive**: `.lower()` on both sides of all three gate-hash comparisons.

Frozen predicate, re-executed. `python3 /tmp/mutverify-r38-probe[-mN]/round38/c2-count.py --gate
<lane>/tools/research-gate.sh --seed <N> --tmp <existing tmp> --receipt <tmp>/r.json` (probe layout
is a byte copy of `round38/{c2-count,c1-count,expectations}.jsonl` + `round37/c1-count.py`; only
`verify-receipts.py` is swapped):

```
seed 38291 pristine  -> 7x PASS, RECEIPT_BINDING_MATCH=7/7, rc=0
seed 38292 M2        -> 7x PASS, RECEIPT_BINDING_MATCH=7/7, rc=0
seed 38293 M1        -> 7x PASS, RECEIPT_BINDING_MATCH=7/7, rc=0
seed 38294 M3        -> 7x PASS, RECEIPT_BINDING_MATCH=7/7, rc=0
seed 38295 M4        -> 7x PASS, RECEIPT_BINDING_MATCH=7/7, rc=0
```

Restoration: no lane byte changed. `sha256sum corpus/evidence/round38/verify-receipts.py` after the
probe = `756f186c…f27605`, same as before; no `git add/commit/…`, no `jj` mutation; only file written
in the lane is this report (`git status --porcelain`: pre-existing `M corpus/evidence/round38/claims.md`
and `?? .ufo/waves/round-38/`, both not mine).

## Findings

1. **C2's frozen predicate cannot see any of the four weakenings.** All four mutants score 7/7
   (seeds 38292–38295 above) while each accepts a receipt the landed verifier refuses (rows
   `d-missing-pre`, `d-post-moved`, `d-upper`, `d-field-only`). `RECEIPT_BINDING_MATCH=7/7` is
   therefore evidence that the seven scenarios pass, not that the verifier's bindings hold —
   the round-38 C2 calibration claim over-attributes what this predicate proves.

2. **M1 is a fail-open on the round-37 residual shape it claims to close.** The docstring promises
   `VERIFY-FAIL: missing-field gate_sha256_pre`; M1 returns `VERIFY: ok` rc=0 for a receipt missing
   exactly that field (row `d-missing-pre`), because `post`+`gate_sha256` remain and alias-check
   passes. C2 still passes because `legacy-receipt-refused` uses a receipt missing *all* fields.

3. **M3 defeats the pre==post invariant that C2 is built on.** With `gate_sha256_post` ignored, a
   receipt whose post digest differs from pre verifies rc=0 (row `d-post-moved`). C2 cannot notice:
   its only self-rewrite evidence comes from `self-rewrite-refused`, where the *counter* refuses and
   writes **no** receipt, so the verifier's `gate-sha-changed-across-run` branch is never exercised.

4. **M2 survives c2's own three tamper scenarios.** Under pristine, `counter-tamper-detected`,
   `expect-tamper-detected` and `body-tamper-detected` are *all* refused at the first check,
   `receipt-self-digest` (rows `c2-*-flip` under m0) — `doctor()` rewrites the body without
   re-digesting. One check kills all three named scenarios. With M2, they are still refused by
   `counter-sha256-mismatch`, `expect-sha256-mismatch`, `matched-recount-mismatch`, so M2 passes 7/7;
   only a tamper of a field no other check re-derives (`d-field-only`, `seed`) exposes it.
   [INFERENCE from this ordering] Removing the `counter_sha256`/`expect_sha256` comparisons outright
   would also score 7/7: those lines are unreachable under pristine for every c2 scenario.

5. **M4's case-folding is accepted silently.** Upper-casing all three gate digests verifies rc=0
   (row `d-upper`), so digest identity degrades from byte equality to case-insensitive match; the
   landed verifier's refusal is `gate-sha256-mismatch`, i.e. the only thing standing between the two
   behaviours is the exact-case compare.

6. **Fixture discriminators exist and are cheap** (sub-second, no gate invocation): a re-digested
   per-field doctoring plus one no-re-digest field-only doctoring separate every mutant. Any of the
   four should be added to `c2-count.py`'s scenario set to make the predicate bind what it claims.

## Limits
- Probe is the verifier in isolation plus the c2 counter; I did not run `c1-count.py` against a
  mutated gate, so the C1 operability claim is untouched by this seat.
- No fifth mutant was built for finding 4's bracketed inference; it is reasoned from observed
  refusal ordering, not executed.
- Host was heavily loaded (peers running c2 counters concurrently); c2 wall time ~55 s per run,
  results unaffected.
- No tools installed or upgraded. No lane repo, jj state, index or fleet file mutated.
