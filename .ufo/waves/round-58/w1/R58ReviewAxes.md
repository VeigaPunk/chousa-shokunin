# R58ReviewAxes — axis targeting, sourcing, separability, planned row, do-nothing controls

Seat: R58ReviewAxes (reviewer, leaf — no subagents). Date: 2026-10-27.
Context read at lane HEAD `718e8d20779427dc011ab211d69093160e2367cc` (parent = freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634`).
No installs/updates performed (none needed). No fetches. No lane writes except this report.

## Integrity of the frozen artifacts (precondition checks)

- `git merge-base --is-ancestor b13ca7b5c8bbb40d2d29a37fb443c64ca043f791 HEAD` → OK; `git log --oneline -1 b13ca7b5` → "round-57 verifier spot-check (integrator, hyaku): non-author admit/reject". Claim base verified.
- `git diff --stat 9e73a03..HEAD -- corpus/evidence/round58/` → only ADDs: `controls/REFUSEALL.py` (+4), `controls/build-spans-r55.py` (+217), `controls/c1-controls.txt`, `controls/c2-controls.txt` (post-freeze commit 718e8d2 "record frozen control results").
- Byte-identity to freeze verified for: `claims.md`, `c1-count.py`, `c2-count.py`, `c2/quotes.tsv`, `controls/c1-before.txt`, `controls/c2-before.txt` (all SAME via `git diff --quiet 9e73a03 -- <f>`).
- Pins: `sha256sum` → `controls/build-spans-r55.py` = `1ed2650a…c80bf6` (= R55_BUILDER_SHA); `tools/build-spans.py` = same R55 bytes (pre-wave); `tools/capture-text.py` = `2c0140bc…3e2573` (= CAPTURE_TEXT_SHA); `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` = `6063a3af…fddf3` (= claims.md raw sha256).
- `c2/quotes.tsv`: 13 lines = header + 12 rows; duplicate quotes in col 3: 0; every row S101 + the claims.md URL + entry `corpus/knowledge/carrier-alphabet-china-r58.md`.

## Check 1 — C1 targets the lowest numeric non-retired axis: PASS

- `SCORECARD.md:5-7` Axes table: exactly one numeric row — `operability | 3 | … | 1` (0–10 scale; "this deliberately narrow observable can award at most 3/10", `SCORECARD.md:11-13`).
- `SCORECARD.md` `## Retired`: "None. The unmeasured axes are not retired or asserted saturated."
- claims.md C1 header: "operability (lowest scored non-retired axis, 3/10)"; and C1 explicitly disclaims the numeric scale: "No score increase is claimed on the narrow 3/10 numeric scale; operability verdict is on this observed gate surface."
- Conclusion: operability is the lowest (and only) numeric non-retired axis; C1 targets it. PASS.

## Check 2 — C2 is a distinct, sourced depth claim: PASS

- claims.md C2: axis depth; source S101 with exact URL, raw key `6dc68fd6b32ce9c8dfcebce8`, raw sha256 `6063a3af…` — all three re-verified against lane bytes (digest above matches).
- Sourcing is capture-bound, not URL-bound only: `c2-count.py` pins RAW_SHA and re-derives the defined form via pinned `capture-text.py`, then binds all 12 quotes at exact offsets (`CAPTURE_BIND:<sid>` per row) and requires ≥3 line-start anchors.
- Distinctness from C1: different surface (knowledge entry + spans manifest vs builder hazard battery), different counters (`c2-count.py` vs `c1-count.py`), different receipts. PASS.

## Check 3 — causal separability of C1 and C2: PASS

- C1's counter consumes: candidate builder, synthetic fixtures, pinned capture-text, the S101 capture (heldout leg), `controls/`. It never reads the C2 entry, `c2/quotes.tsv` (C2's), `c2/spans.tsv`, or `corpus/knowledge`.
- C2's counter pins the builder bytes: `BUILDER_SHA='1ed2650a…'`; `if sha(builder.read_bytes())!=BUILDER_SHA: errors.append('BUILDER_PIN')` — i.e. C2 is measured against the round-55 builder bytes, independent of C1's tool change (docstring: "C2 stays causally separate from C1 by pinning the round-55 build-spans.py and capture-text.py bytes"; claims.md: "C2 uses the pinned round-55 builder and capture-text, so it is independent of C1's tool change").
- Coupling direction is conservative: scoring C2 on a root whose `tools/build-spans.py` already carries C1's hardening fails `BUILDER_PIN` — C2 can never pass *because of* C1. Conversely C1 never consumes any C2 artifact, so C2 cannot cause C1's verdict. Shared evidence (S101 capture, capture-text.py) is read-only in both counters.
- Operational note for the L1: C2 must be scored with `--root` pointing at a lane-copy that still holds R55 builder bytes; scoring on a post-C1 lane root fails BUILDER_PIN by design. PASS.

## Check 4 — both claims appear in the round-57 planned row: PASS

- `SCORECARD.md` `## Planned — round 57 (not started)`: "harden `tools/build-spans.py` (`R55W2SentBuilder`: refuse a foreign `spans.tsv` in `--out`, refuse symlinked outputs, unlink orphans last, no `.pyc` in `tools/`, bounded reads) with a frozen counter" … "the S101 carrier-alphabet leg". Both C1 and C2 surfaces named.
- Cross-check, `## Planned — round 58 (not started)`: "the S101 carrier-alphabet leg" and "the build-spans hardening set (`R55W2SentBuilder`)" — both named there too, so the item holds under either reading of "round-57 planned row" (row written for round 57 at the r56 landing, or row written at the r57 landing for round 58).
- `LOG.md` round-58 intake agrees: "the round-57 planned row names the build-spans hardening set (`R55W2SentBuilder`) and the S101 carrier-alphabet leg." PASS.

## Check 5 — do-nothing controls cannot reach targets: PASS

Structural reading of the frozen counters:
- C1 verdict requires: all 4 safe legs pass AND all 7 hazard legs refuse with named reason classes AND `BEFORE_FOREIGN=deleted` AND `denied == total`. `REFUSEALL.py` is `print(…refused…); sys.exit(1)` — safe legs can never pass. The R55 builder is proven to fail FOREIGN (deletes the foreign file) and 6 further refusal-reason checks.
- C2 verdict requires 12/12 exact-quote capture binding, manifest byte rebuild, substance, inference-ground, base-newness. An untouched lane has no entry/manifest (`ENTRY_MISSING`, `MANIFEST_MISSING`).

Actually run by this seat (frozen counter bytes at 9e73a03; scratch-only writes; TMPDIR=/fast/scratch/hyaku/chousa-r58/R58ReviewAxes):
1. Direct do-nothing run: `python3 …/c1-count.py --builder …/controls/REFUSEALL.py --work <scratch>/c1-refuseall --seed 58` → harness crash before any leg line: `FileNotFoundError … c1-refuseall/out-empty/spans/S777-1.txt` (FOREIGN fixture setup at c1-count.py:212 assumes EMPTY_OK created `out/spans/`), `EXIT=1`. No `C1=` line printed — the control trivially cannot reach `C1=PASS`. See Observation O1.
2. Full live replication of the control arm: `python3 …/c1-count.py --work <scratch>/c1-controls-live --controls …/controls --seed 58` → line-for-line equal to the committed `controls/c1-controls.txt`: `EMPTY_OK=pass REBUILD_OK=pass`, all 7 hazard legs `fail`, `ESCAPE_ENTRY=pass(refused)`, `HELDOUT_OK=pass`, `BEFORE_FOREIGN=deleted`, `CONTROL_REFUSEALL=denied`, `CONTROL_build-spans-r55=denied`, `DENIED=2/2`, `SUMMARY OK=4/4 REFUSE=0/7 … DENIED=2/2`, `C1=FAIL`, `EXIT=1`. (16.5 s wall.)
3. Live C2 do-nothing on the untouched lane: `python3 …/c2-count.py --root <lane> --work <scratch>/c2-before-live` → `C2=FAIL`, `EXIT=1`, all 10 ERROR lines byte-identical to the frozen `controls/c2-before-frozen.txt`.
Committed receipts corroborate: `c1-before.txt` (base C1=FAIL EXIT=1), `c2-before.txt`, `c1-control-build.txt` (`BASELINE_SHA256_PINNED_BYTES=1ed2650a…`, `CONTROLS=build-spans-r55.py,REFUSEALL.py`), `c2-controls.txt` (STAGED and REWRITE roots both `C2=FAIL` with `REF_ID_UNBOUND`). Not re-run by this seat: `build-c1-controls.py` / `build-c2-controls.py` staging itself (cited from committed receipts). PASS.

## Observations (findings against frozen artifacts — not fixes; none blocking)

- O1 (robustness gap, frozen harness): `c1-count.py` crashes with `FileNotFoundError` at line 212 when the builder under test fails EMPTY_OK without creating `out/spans/` (observed with REFUSEALL). The counter's own `--controls` arm contains this (subprocess + stdout scan → `denied`), so receipts and the verdict are unaffected, and any candidate that passes EMPTY_OK never reaches the crash path. Denial semantics hold a fortiori.
- O2 (cosmetic drift, frozen): header says controls "REFUSEALL and NAIVE", argparse help "REFUSEALL.py / NAIVE.py"; the code's names tuple is `("REFUSEALL.py", "build-spans-r55.py")` and the receipt shows `CONTROL_build-spans-r55`. Behavior is what the predicate reads.
- O3 (latent variant mismatch, frozen): `c2-count.py` new-ground leg greps base `corpus/knowledge` for the traditional form `載体类型标识` while the prose predicate and entry check use simplified `载体类型标识`. At claim base `b13ca7b5` both greps return rc=1 inside `corpus/knowledge` (measured), so outcome agrees on this base. Note the simplified string DOES exist at base outside `corpus/knowledge` (`corpus/captures/0f33243fd7ac2fe88b85c1ba.txt`, `corpus/evidence/round54/S101-text-form.txt`, wave reports) — the `corpus/knowledge` scoping is load-bearing and matches the prose.
- O4 (control breadth): C2 STAGED/REWRITE control roots fail via ~10 error classes each (including `BUILDER_PIN`/`RAW_PIN` — the minimal roots do not stage pinned tool bytes), so their rejection is conservative multi-cause; quote-binding-only discrimination is carried by the before receipts. The frozen predicate requires only "must fail binding" — satisfied (`REF_ID_UNBOUND` present in both).
- O5 (pre-wave state): `tools/build-spans.py` still equals the R55 pin at review time, so the base receipt and live replication measure the same bytes the wave will harden.

## Verdict summary

| Item | Result |
|---|---|
| C1 targets lowest numeric non-retired axis (operability 3/10; Retired: none) | PASS |
| C2 distinct, sourced (S101 digest-verified) depth claim | PASS |
| C1 ⊥ C2 causal separability (C2 re-pins R55 builder; coupling conservative) | PASS |
| Both named in the round-57 planned row (and round-58's) | PASS |
| Do-nothing controls cannot reach targets (live: DENIED=2/2, C1=FAIL, C2=FAIL) | PASS |

Scratch `/fast/scratch/hyaku/chousa-r58/R58ReviewAxes/` removed before yield. Unrun checks are named inline (control staging scripts). No claim-verdict authority; the L1 integrates.

VERDICT: reviewed the frozen round-58 claim pair — C1 build-spans hazard battery (operability, the lowest numeric non-retired axis 3/10) and C2 S101 carrier-alphabet entry (depth, capture-digest-sourced) — across axis targeting, sourcing, separability, planned-row coverage, and do-nothing controls: survives; observations O1–O5 are non-blocking notes on frozen artifacts for the L1's attention.
