# W2RevClaimsFinal

## Verdict
On the dispatched bytes (`8e93bc9`) the wave-1 integration's measured claims hold (P1/P2 7/7 fresh, 9/9 receipts, controls 2/7 and 0/7, C2 gate-agnostic 7/7), but Erratum 2(iii) overstates ok re-derivation (`_contains` observations are not re-derived), Erratum 6(a)'s named `date` witness does not reproduce, and Erratum 7's stale-receipt universal fails on early refusals.

## Evidence
All probes pinned to git-archive blobs of the dispatched commit, not the mutating worktree (see Finding 5):

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
git rev-parse master            -> 8e93bc916527b3c21f0f702967fa65c3b4c31699
git archive 8e93bc9… | tar -x -C /tmp/w2revclaims/head
sha256 /tmp/w2revclaims/head/tools/research-gate.sh            -> 37e2b996… (claims' candidate)
       corpus/evidence/round38/c1-count.py                     -> 79040790…
       corpus/evidence/round38/c2-count.py                     -> 414a7a10…
       corpus/evidence/round38/verify-receipts.py              -> b63e7e20…
       corpus/evidence/round38/expectations.jsonl              -> d34f1735…
       corpus/evidence/round38/claims.md (256 lines)           -> 2bc82126…
       .ufo/waves/round-37/controls/base-gate-r37.sh           -> a7d3922c…
       .ufo/waves/round-38/controls/base-gate-r38.sh           -> 9fcac047…
```

- Nine receipts, HEAD verifier/counters/gates: `9/9 VERIFY: ok`; `matched`: c1-after 7/7 ×3, c1-base 2/7, c1-base2 2/7, c2-after 7/7 ×3, c2-base 0/7. Every receipt's `counter_sha256` equals the HEAD counter bytes (790407…/414a7a…); `expect_sha256` = d34f1735….
- Fresh HEAD runs (C1_TMP/C2_TMP under /tmp/w2revclaims): c1 seed 38421 → `ENV_PIN_CAPTURE_MATCH=7/7`; c2 seed 38429 → `RECEIPT_BINDING_MATCH=7/7`; c2 on `base-gate-r38.sh` seed 38431 → `7/7` (Erratum 4 separability); c1 on `base-gate-r38.sh` seed 38403 → `2/7`.
- `_contains` doctoring at HEAD (`/tmp/w2revclaims/head-doctored-contains.json`: c2 receipt with `counter-tamper-detected.observed.verify_fail=""`, `expect-tamper-detected.observed.verify_fail="FABRICATED"`, `clean_verify_out` fabricated, self-digest re-sealed) → `VERIFY: ok …` exit 0.
- Extra unknown field (HEAD verifier): re-sealed `extra_unknown_field` → `VERIFY: ok` (premise of working-tree Erratum 9).
- Erratum 6 witnesses on HEAD gate: PATH `bash` shim → `pin_rc=0`, baseline `GATE_GREP:` lines=1, clean-PATH drift `GATE_DRIFT: -GATE_GREP`; suppressing exported `bash` function → `pin_rc=0`, 5 × `VERIFY_ALL_SECTION_UNAVAILABLE`; `command env` mutant (seed 38419) → `ENV_PIN_CAPTURE_MATCH=7/7`.
- Erratum 6(a) `date` witness on HEAD gate: exported `date` (prefix and `export` forms) → 0 `GATE_GREP:` lines, `GATE_DRIFT: none`; marker driver shows the function is called once but inside `$(...)` (gate lines 327–330).
- Valid-override, validate-then-ignore mutant of HEAD gate (seed 38433) → `ENV_PIN_CAPTURE_MATCH=7/7`.
- Stale receipt: HEAD c1, missing gate path, seed 38427 → exit 2, stderr `c1-count: gate not found…`, pre-existing `--receipt` still exists.
- Seed-invariance: c1 and c2 after-receipts each identical modulo `seed` + `receipt_sha256`.

## Findings
### Errata 1–8 marking (reviewed commit `8e93bc9`)
- **E1** bullet inserted post-freeze / body otherwise untouched — MEASURED: diff of `504c1d2:claims.md` vs HEAD body = exactly the 6-line loader bullet + blank.
- **E2 (i)(ii)(iv)** family+predicate binding, parsed census/expect tie, file bindings+arithmetic — MEASURED (code; reroute → `predicate-mismatch`; re-sealed matched flip → `matched-recount-mismatch`).
- **E2 (iii) "re-derives every ok"** — OVERREACH: `_contains` keys excluded (below, Finding 1).
- **E2 five wave-1 kills** — INFERENCE (report-only; the frozen verifier is not committed, so they cannot be replayed).
- **E2 "all committed receipts regenerated"** — MEASURED (9/9 + counter/table hashes above).
- **E2 narrowed reading / verifier_sha debt** — MEASURED+LIMIT: a synthetic self-consistent 0/7 receipt verifies ok; no verifier hash is bound anywhere.
- **E3** doctors re-seal / exact refusal line asserted — MEASURED at scoring time (fresh runs observed `VERIFY-FAIL: counter-sha256-mismatch`, `expect-sha256-mismatch`, `receipt-self-digest`); but the stored line is not re-derived (Finding 1).
- **E4** cell decoupling, base 4/7→r38 7/7, r37 pipeline 0/7 — MEASURED: hold/foreign/legacy expectations carry no subject `counter_rc`; base-gate c2 7/7 (seed 38431); c2-base receipt 0/7. `self-rewrite-refused` still asserts `counter_rc=2`, but that is the r38 counter's own gate-agnostic refusal and is observed on the base gate too.
- **E5** scrub + pinned `/usr/bin/bash` + timeouts + anchored refusal — MEASURED (code; anchored token observed). Seed-38219 BASH_ENV demonstration and the "clean caller environment" premise — INFERENCE (report-only). PATH-shim named limit — MEASURED (Finding 4 evidence).
- **E6(a)** "BASH_FUNC channel untouched, only the `env` name bypassed" — MEASURED via the suppressing `bash` function and PATH shim; the named `date` witness — OVERREACH (Finding 2).
- **E6(b)** `command env` mutant 7/7 — MEASURED (seed 38419). **E6(c)** PATH shim poisons baseline; suppressing `bash` function pins crit baseline with `--pin` 0 — MEASURED (both). **E6(d)** label-level seeds — MEASURED (byte-identity). **E6(e)** `9fcac047` control 2/7 — MEASURED (hash + committed receipt + seed 38403 run).
- **E6 narrowed reading "exactly the cells"** — MEASURED: the 14-row table is 2 holds + 3 env-function + 2 override-refusal per family; no PATH, `bash`-name, or valid-override-acceptance cell. "Pre-registered r39 eighth scenario" — INFERENCE (plan, not an artifact).
- **E7** hard-7 check — MEASURED (`holds = matched == 7 and total == 7`, both counters); frozen P1/P2 text unchanged — MEASURED. Stale-receipt universal — OVERREACH (Finding 3).
- **E8(a)** shlex quoting — MEASURED (metachar gate path: 7/7, no injected marker file; one non-reproduced 3/7 anomaly, see Limits). **(b)** pre-run table hash + mid-run refusal — MEASURED (both counters; receipt binds d34f1735…). **(c)** zero-execution verifies by design — MEASURED (synthetic 0/7 receipt) and consistent with E2's narrowed reading; knowledge-doc wording corrected — MEASURED (phrase absent from `corpus/knowledge/`).

### Numbered findings
1. **HIGH — Erratum 2(iii) overreach: `_contains` observations are never re-derived.** `/tmp/w2revclaims/head/corpus/evidence/round38/verify-receipts.py:159-162` re-derives `ok` only over keys not ending in `_contains`, so the frozen `verify_fail_contains` assertions (`expectations.jsonl` rows `*-tamper-detected`) are unchecked. A re-sealed receipt that empties/fabricates `verify_fail` and `clean_verify_out` still prints `VERIFY: ok` (evidence above). Consequence: Erratum 3's "exact verifier refusal line is the asserted observable" is true only at scoring time; it is not recoverable from committed bytes, and the frozen "fails closed on any doctored field" is narrower than written. (The worktree's Erratum 10 now names this as producer-side by design; at `8e93bc9` it is still an overreach, and an extra top-level field also verifies — the premise Erratum 9 later fixes.)
2. **MEDIUM — Erratum 6(a)'s named `date` witness does not reproduce.** HEAD gate lines 327-330 call `date` only inside command substitutions, so an exported function's `export CHOUSA_GREP_PIN_ECHO=1` cannot reach the parent shell: 0 `GATE_GREP:` lines, `GATE_DRIFT: none`, marker proves the function ran. The class claim is unaffected (suppressing `bash` function and PATH shim both move the baseline), so the narrowing is substantively right; its supporting example is unsupported as stated.
3. **MEDIUM — Erratum 7's "no stale pre-existing `--receipt`" is false on early refusals.** Both counters unlink the receipt only after gate/table/tmp preflights (`c1-count.py:240-242`, `c2-count.py:312-314`); a missing gate exits 2 and leaves the stale receipt (probe above). Not exploitable — a stale receipt still needs the matching gate bytes — but the sentence should be scoped to post-preflight refusals.
4. **LOW — valid-override acceptance is unmeasured.** A gate that validates then ignores a valid `RESEARCH_GATE_ENV` (`/tmp/w2revclaims/h-mut-override.sh`, seed 38433) scores 7/7. Erratum 6's "override refusal shape" is therefore accurate, but the acceptance direction is not named in §Limits as carried debt.
5. **LOW (state) — the worktree moved during review.** `tools/research-gate.sh` 37e2b996→0447ad14, both counters, verifier, receipts modified, `c2-after-s38101.json` deleted, Errata 9-11 appended; `master` unmoved at `8e93bc9`. Findings above are pinned to `git archive 8e93bc9`; probes run before Finding-5 was noticed used worktree bytes and are not cited.

## Limits
- Gate selftest (272 cases) not re-run; context asserts PASS on the final bytes.
- Wave-1 demonstrations whose subjects are not committed (frozen pre-integration verifier; ambient-BASH_ENV seed 38219; seed 38207) are taken as report-only, not re-executed.
- One unreproduced anomaly: `c2-count` with a `;`-containing gate filename scored `3/7` once (three tamper cells' clean receipts absent at verify time), then `7/7` twice with the same construction; unexplained transient, flagged as harness load/timing sensitivity.
- Working-tree Errata 9-11 (strict schema, type checks, verifier-mutant non-discrimination) are outside the assigned diff and not marked; they partly pre-empt Findings 1 and 3 at the worktree state.
- Known disclosed residues re-confirmed: verifier hash unbound, `subject_counter` unbound, receipts seed-invariant, PATH/BASH_ENV named, synthetic consistent receipts verify by design.
- No tool installs or upgrades were needed; nothing outside `/tmp/w2revclaims` and this report was written.
