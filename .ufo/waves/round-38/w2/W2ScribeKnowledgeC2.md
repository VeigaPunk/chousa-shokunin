# W2ScribeKnowledgeC2

## Verdict

On final bytes (tip `8e93bc91…1699`) C2 holds — fresh seed 38413: `RECEIPT_BINDING_MATCH=7/7`, exit 0, receipt verifies; 9/9 committed receipts `VERIFY: ok` — all four wave-1 verifier kills are refused by their *named* checks, the check-stripped-verifier bypass is closed (4/7, exit 1), and only the named NOT-authorship residual survives. Final knowledge doc drafted below, superseding the w1 draft.

## Evidence

From `/home/vgpnk/Projects/shokunin/chousa-shokunin`; seeds 38413–38499; writes only this report plus `/tmp/w2skc2/`. Gate `37e2b996…d27d`, c1-count `79040790…6221`, c2-count `414a7a10…403e3`, verify-receipts `b63e7e20…f952`, expectations `d34f1735…f8aa`.

```sh
C2_TMP=/tmp/w2skc2 python3 corpus/evidence/round38/c2-count.py --gate tools/research-gate.sh \
  --seed 38413 --receipt /tmp/w2skc2/c2-fresh-38413.json    # 7 PASS, 7/7, exit 0
python3 corpus/evidence/round38/verify-receipts.py --receipt /tmp/w2skc2/c2-fresh-38413.json \
  --gate tools/research-gate.sh --counter corpus/evidence/round38/c2-count.py   # VERIFY: ok, rc0
python3 /tmp/w2skc2/probe.py                                 # four wave-1 kill replays, resealed
```

```
P1 legacy laundering (r37 receipt + public hashes + reseal): r37 counter → predicate-mismatch;
   r38 c1-count → counter-sha256-mismatch
P2 identity reroute (c1 receipt, counter_sha256→c2, reseal): predicate-mismatch
P3 doctored observed (expect untouched, ok=true, resealed): ok-rederivation-mismatch hold-receipt-verifies
P4 vacuous receipt (scenarios=[], matched=total=0, predicate_holds=true): scenario-census-mismatch
P5 forged from frozen table, 0 executions: rc0 VERIFY: ok    ← the named residual, reproduced
Committed receipts 9/9 VERIFY: ok: c1 after 3×7/7, c1-base 2/7 ×2, c2 after 3×7/7, c2-base 0/7
Fresh 38413 body == committed c2-after-s38371 body modulo seed+receipt_sha256: True
```

```sh
# mutation: copy round38/ to /tmp, delete the counter & expect checks, rescore
C2_TMP=/tmp/w2skc2/muttmp python3 /tmp/w2skc2/muttree/c2-count.py \
  --gate $PWD/tools/research-gate.sh --seed 38417 --receipt /tmp/w2skc2/mut-c2-38417.json
# FAIL counter-tamper-detected / FAIL expect-tamper-detected — both observe "VERIFY: ok"
#          (minimal-witness: they expect rc1 + the exact VERIFY-FAIL label)   RECEIPT_BINDING_MATCH=4/7, exit 1
#          wave 1: the same mutation still scored 7/7 (RevClaimsC2.md:20, RevCounterC2.md:28)
# debt: mutant verifier accepts a re-sealed counter flip (VERIFY: ok); canonical → counter-sha256-mismatch
```

## Findings

1. **Predicate holds on final bytes.** Seed 38413, gate pre==post `37e2b996…d27d`, receipt `/tmp/w2skc2/c2-fresh-38413.json` (`counter_sha256 414a7a10…`, `expect_sha256 d34f1735…`, 7/7), verifier rc 0. Committed `c2-after-s{38101,38111,38371}` and both c1 families 7/7; `c1-base*` 2/7 and `c2-base-s38101` 0/7 verify with `predicate_holds:false` — integrity ≠ predicate (`verify-receipts.py:43-48`).
2. **Legacy laundering closed by the family/predicate tie, not incidentally.** Public hashes + recomputed self-digest now refuse `predicate-mismatch` / `counter-sha256-mismatch` (`verify-receipts.py:147-150`; w1 attack verified `ok` — `CritC2Kill.md:73`).
3. **Identity reroute closed.** Family is keyed on the `--counter` basename (`verify-receipts.py:60-63`), so a c1 receipt re-bound to c2's hash and re-sealed hits `predicate-mismatch`; w1 reroute verified `ok` — `RevCounterC2.md:17`, `CritC2Kill.md:31`.
4. **Doctored observations and vacuous receipts closed.** Changed `observed` with `ok:true` → `ok-rederivation-mismatch` (`:185`); empty census → `scenario-census-mismatch` (`:170`); both verified `ok` in w1 — `CritC2Kill.md:32-33`, `RevClaimsC2.md:21`.
5. **The mutated-verifier bypass is closed.** With the counter/expect checks deleted the pipeline scores 4/7 exit 1, and those two cells fail because the verifier *printed* `VERIFY: ok` — the doctors re-seal and the labels are the asserted observable (`c2-count.py:198-234`). The body cell still passes: its doctor stays unsealed by design.
6. **NOT-authorship is real.** A zero-execution receipt built from the frozen table verifies `ok`; a forger holding the public hashes and honest observations is indistinguishable (`verify-receipts.py:43-48`, `claims.md:179-181`). Consumers must read `matched`.
7. **Carried debt `verifier_sha256` demonstrated.** A verifier copy minus the counter check accepts a re-sealed flip the canonical verifier refuses; nothing in a receipt names its judge (`claims.md:181-183`).
8. **Seeds are not replication for C2.** Fresh 38413 == committed 38371 modulo `seed`/`receipt_sha256` — Erratum 6(d) class (`claims.md:226-229`), now measured.
9. **Publication still does not assert pre==post.** `c2-count.py:316-325` re-hashes after every scenario and returns 2 on change, but never compares `gate_sha256_post` to `_pre` before writing; `verify-receipts.py:198` is what rejects such a receipt. Code read only; the demonstrated self-rewrite shim is refused at the counter.

## Limits

- Leaf seat: no dispatches, no lane/jj/git mutation, no installs; `/tmp/w2skc2/` plus this report only.
- The mutation ran in a copy, so its legacy cell's rc 2 is an artifact (`R37_C1` = `HERE/../round37/c1-count.py`, absent in the copy) — 4/7 is the honest mutant score; the two named cells carry the conclusion.
- C1 was not re-measured; only its committed receipts were re-verified. The census tie is code-read plus P3/P4 (no rebuilt-table probe inside the time box).
- The P5 forgery is a demonstration of the named residual, not a kill. `unknown-field` (`:130`) means any future receipt field needs an allowlist edit.

## Draft — `corpus/knowledge/receipt-binding-r38.md`

```markdown
# Receipt binding — one scoring counter, a parsed census, a fail-closed verifier

Lane: chousa. Round 38 (C2, calibration).
Surface: `corpus/evidence/round38/{c1-count,c2-count,verify-receipts}.py`, `expectations.jsonl`, `receipts/`.

source: round-37 residual `.ufo/waves/round-37/residual/RevC1FreshSeed.md` F1 (line 31: receipt `gate_sha256` post-run only — a self-rewriting gate got a 7/7 receipt stamped with bytes that did not run every scenario) and F4 (line 96: no counter identity); frozen design `corpus/evidence/round38/claims.md` §C2 (line 72) plus Errata 2/3/4/7/8 (164, 185, 193, 238, 245); wave-1 kill reports `.ufo/waves/round-38/w1/{CritC2Kill.md:73-75, RevCounterC2.md:17,27, RevClaimsC2.md:20-21, CritTextOverreach.md:73, SentScope.md:34}`.
verified-at: 2026-10-24 (tip `8e93bc91…1699`; gate `37e2b996…d27d`, c2-count `414a7a10…403e3`, c1-count `79040790…6221`, verify-receipts `b63e7e20…f952`, expectations `d34f1735…f8aa`; `RECEIPT_BINDING_MATCH=7/7` on fresh seed 38413 and committed 38101/38111/38371; nine committed receipts `VERIFY: ok`)
recheck: on-release (`C2_TMP=<existing dir> python3 corpus/evidence/round38/c2-count.py --gate tools/research-gate.sh --seed <n> --receipt F` → `7/7` with `predicate_holds=true`; `python3 corpus/evidence/round38/verify-receipts.py --receipt F --gate tools/research-gate.sh --counter corpus/evidence/round38/c2-count.py` → `VERIFY: ok`; any run below 7/7 against the landed gate kills C2)

## What changed (binding model as integrated)

Five bindings, all measured by the counter, never by the gate under test:

- `gate_sha256_pre` / `gate_sha256_post` (+ alias `gate_sha256`): hashed before the first scenario and re-hashed after every scenario; a change exits 2 with no receipt (`c2-count.py:316-325`, `c1-count.py:240-255`). Closes F1.
- `counter_sha256`: the scoring counter's own digest (`c2-count.py:347`, `c1-count.py:275`); a c2 receipt also names the tested counter in `subject_counter`, so `--counter` must be the scoring file. Closes F4.
- `expect_sha256`: the frozen table's digest, taken before the scenarios and refused if it moves (`c2-count.py:303-332`). Closes Erratum 8(b).
- `receipt_sha256`: the body's canonical digest (every other field, `sort_keys`, indent 2, trailing newline).
- `predicate`: the frozen predicate string, checked against a per-counter family table (`verify-receipts.py:147-150`).

`verify-receipts.py` re-derives everything from committed bytes, fail-closed and named: shape (`missing-field` :127, `unknown-field` :130), self-digest (:133), counter (:138), expectation (:143), family+predicate (:147-150); then the census — the table is PARSED, not merely hashed: receipt ids must equal the frozen family's ids (`scenario-census-mismatch` :170), each row's `expect` must equal the frozen `expect` (:176), and every `ok` is re-derived from frozen expectations and the receipt's own `observed` (:185; `_contains` keys are harness annotations, not equalities); then arithmetic (`matched` :188, `total` :190, `predicate_holds` :192) and gate identity (pre==post :198, pre==current :200, alias :202). The counter hard-checks the frozen count (`c2-count.py:343` `holds = matched == 7 and total == 7`), so an edited-to-6 table cannot print a passing 6/6.

## Wave-1 kills closed (re-executed on final bytes, seed 38413)

| wave-1 finding | attack | refusal on final bytes |
|---|---|---|
| `CritC2Kill.md:73` | r37 receipt + public hashes + recomputed self-digest | `predicate-mismatch`; `counter-sha256-mismatch` under `--counter c1-count.py` |
| `RevCounterC2.md:17`, `CritC2Kill.md:31` | c1 receipt, `counter_sha256`→c2, re-sealed | `predicate-mismatch` (family keyed on `--counter` basename, :60-63) |
| `CritC2Kill.md:33`, `RevClaimsC2.md:21` | one `observed` changed, `ok` still true, re-sealed | `ok-rederivation-mismatch` |
| `CritC2Kill.md:32`, `SentScope.md:34` | empty census, `matched=total=0`, `predicate_holds=true` | `scenario-census-mismatch` |
| `RevClaimsC2.md:20`, `RevCounterC2.md:28` | verifier with counter/expect checks deleted | counter 4/7 exit 1; the named cells observe `VERIFY: ok` where they demand the label |

## NOT authorship (the narrowed reading)

Verification certifies integrity and self-consistency against committed bytes — never execution. Reproduced: a receipt synthesized from the frozen table with zero counter executions verifies `ok`; `receipts/c2-base-s38101.json` verifies `ok` at `0/7` because `predicate_holds:false` is self-consistent; only `7/7` from `c2-count.py` establishes C2. This is the round-37 F2 residual on the verify side (`claims.md` Erratum 2, verifier docstring): the hashes are public, so a forger must still attack committed bytes — but one who reproduces honest observations is indistinguishable.

## Named limits

- Black-box observability: a counter that lies end-to-end still scores (F2 class).
- Seeds namespace fixture temp dirs only; receipt bodies are seed-invariant.
- Publication does not compare `gate_sha256_pre` to `_post`; `verify-receipts.py:198` does. The demonstrated self-rewrite shim is refused at the counter.
- Receipts at `matched < 7` verify by design (integrity ≠ predicate).
- `R37_C1` is `HERE/../round37/c1-count.py` (`c2-count.py:51`): a relocated `round38/` breaks the legacy cell and reads as subject-counter exit 2.

## Carried debts (r39)

- `verifier_sha256`: no receipt binds the verifier that judged it. A verifier copy minus the counter check accepts a re-sealed `counter_sha256` flip (`VERIFY: ok`) the canonical verifier refuses; a replaced verifier silently re-adjudicates old receipts.
- C1's PATH-half and sibling-name witnesses (Erratum 6) stay C1's, not C2's; unchanged.
```
