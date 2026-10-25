# receipt binding — round 38

source: `.ufo/waves/round-37/residual/RevC1FreshSeed.md` findings F1/F4 (the
motivating debt) + `corpus/evidence/round38/claims.md` (C2 body, Errata 2–4,
8–12) + S073 (the sha256sum manual row this entry's digest contract cites)
verified-at: 2026-10-24
recheck: on-release

## Motivating debt (round-37 residual)

The round-37 counters hashed the gate file AFTER the run and wrote receipts with
no counter identity: a gate that rewrote itself mid-run got a receipt stamped
with bytes that did not run every scenario (F1, replayed live in wave 1 and
again in waves 2), and a counter edit that kept seven scenarios and seven passes
would silently redefine its predicate (F4).

## The binding model as landed

Every round-38 counter receipt binds, measured by the counter itself (never by
the gate under test): `gate_sha256_pre`/`gate_sha256_post` (a changed gate
refuses exit 2 and publishes NOTHING), `counter_sha256`, `expect_sha256` (the
frozen table, hashed before the run and re-checked after), and
`receipt_sha256` (the canonical body's own digest). `verify-receipts.py`
re-derives: the counter family and the frozen predicate string; the exact frozen
scenario census with each row's `expect` tied to the frozen table (parsed, not
only hashed); every `ok` from the frozen expectations and the receipt's own
observations; strict types; a strict top-level schema; and the file bindings +
arithmetic. Measured: `RECEIPT_BINDING_MATCH=7/7` on the landed gate across
construction seeds 38101/38111, wave-1 seeds 38221/38241, wave-2 seeds
38421/38441 (receipts under `corpus/evidence/round38/receipts/`); the
round-37-counter pipeline scores 0/7 on every seed (the frozen do-nothing
control); the r38 counters on the UNFIXED gate also score 7/7 — separability,
not a do-nothing path (claims.md §Errata 4).

## What the waves did to it (the discernment record)

- Wave 1 killed the frozen verifier four ways — a re-bound legacy r37 receipt,
  a c1 receipt rerouted under `--counter c2` with the counter hash swapped to a
  public digest, doctored observations keeping `ok=true`, and a vacuous empty
  receipt all verified `ok` (w1/CritC2Kill.md findings 1–3). Erratum 2 closed
  each with the census tie + ok re-derivation; wave 2 re-ran every fixture —
  each refuses at its named check (w2/W2CritLaundering, w2/W2ScribeKnowledgeC2).
- Wave 1 also found the tamper doctors never re-sealed (the named binding checks
  were unexercised — w1/MutVerify) and three cells over-asserted the subject
  counter's exit code (C2 was gate-coupled at 4/7 on the base gate —
  w1/ExecDoNothingCtl); Errata 3/4 closed both, and wave 2 confirmed the
  re-sealed doctors reach their named checks (w2/W2RevC2Final) and the mutated
  verifier that drops the counter/expect checks is caught at 4/7 by the
  re-sealed-doctor cells (w2/W2ScribeKnowledgeC2).
- Wave 2's surviving class (claims.md §Errata 11): the seven cells do not
  discriminate a verifier weakened in the census/ok-rederivation/type/schema
  checks — five of six such mutants still score 7/7; those checks are bound only
  through the landed verifier's committed bytes. The closing fix is the carried
  `verifier_sha256` debt (also demonstrated live when the verifier changed
  mid-wave and old receipts re-adjudicated silently).

## The honest boundary (named, load-bearing)

Verification certifies integrity and self-consistency against committed bytes —
NOT authorship. A fabricator holding the public hashes who reproduces honest
observations can write a receipt indistinguishable from an executed one (the
round-37 F2 residual, verify side; the wave-2 zero-execution synthetic receipt
verified `ok` by design). A `VERIFY: ok` also never implies the subject's
predicate passed: the 0/7 base receipt verifies with `predicate_holds=false`.
The receipts' evidentiary force is the whole chain — committed counter bytes,
committed gate bytes, the frozen table, and an honestly conducted run — which is
why the counters bind their own bytes and refuse to publish when the gate or the
table changes mid-run.

Carried debts (r39): bind `verifier_sha256` (and `subject_counter_sha256`) into
receipts; re-derive the producer-side refusal-label annotations; the dead-field
deletions from w1/w2 SimpCounters (recorded in SCORECARD planned-39).
