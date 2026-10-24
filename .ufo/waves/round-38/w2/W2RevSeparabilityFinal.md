# W2RevSeparabilityFinal

## Verdict
PASS on all three assigned measurements on the final bytes, with one calibration correction: the
counter-side 6/7 drop is carried by the SUBJECT counter's `pre != post` guard
(`corpus/evidence/round38/c1-count.py:247`), not by the identically shaped guard inside
`corpus/evidence/round38/c2-count.py:320`, whose removal leaves C2 at 7/7 because no c2 scenario
writes the `--gate` path. Gate-side hunk: c1 4/7; C2 gate-agnostic on the base gate: 7/7.

## Evidence
Repo `/home/vgpnk/Projects/shokunin/chousa-shokunin`, tip `8e93bc916527b3c21f0f702967fa65c3b4c31699`
(`git rev-parse master`), landed gate sha256
`37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` (matches claims.md's frozen
candidate hash). All runs: `C1_TMP=/tmp/r38sep/c1tmp C2_TMP=/tmp/r38sep/c2tmp` (both exist), fresh
seeds ≥ 38401. Fixtures under `/tmp/r38sep`; single-hunk diffs confirmed with `diff -u` (one hunk
each, hashes below). Lane repo untouched; no tool installs.

Single hunks (each a copy of the final bytes):
- H1 gate: `/tmp/r38sep/base/gate-env-bare.sh`, sha `1bda0905…2802dfde`; `research-gate.sh:4001`
  `"$ENV_BIN" -u CHOUSA_RECORD …` → `env -u CHOUSA_RECORD …`.
- H2a c2's own guard: `/tmp/r38sep/treeA/round38/c2-count.py`, sha `f4a4cbab…96fb317c`;
  `c2-count.py:320` `if sha256_file(gate) != gate_sha_pre:` → `if False:`.
- H2b subject guard: `/tmp/r38sep/treeB/round38/c1-count.py`, sha `bc4d75df…525de89c`;
  `c1-count.py:247` same substitution.

(1) Gate-side single hunk → c1:
`python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate
/tmp/r38sep/base/gate-env-bare.sh --seed 38401 --receipt /tmp/r38sep/c1-hunk1-s38401.json`
→ `ENV_PIN_CAPTURE_MATCH=4/7`, rc=1. FAIL `env-fn-echo-scrub` (echo_lines 1, drift
`GATE_DRIFT: -GATE_GREP`), FAIL `env-fn-root-move` (drift lists foreign-root findings), FAIL
`env-fn-suppress` (pin_rc 2, no baseline). The two holds and both override-refusal cells pass (the
provenance refusal runs before the capture, so 4/7 — not 2/7 — is the correct mutant reading).
Receipt binding still works: `gate_sha256_pre == gate_sha256_post == 1bda0905…`,
`counter_sha256 == 79040790…` (landed counter), `matched=4`, `predicate_holds=false`;
`verify-receipts.py --receipt … --gate /tmp/r38sep/base/gate-env-bare.sh --counter <landed c1>`
→ `VERIFY: ok`, while the same receipt against `tools/research-gate.sh` → `VERIFY-FAIL:
gate-sha256-mismatch`. The drop is a bound measurement, not a refusal.

(2) Counter-side single hunks:
- literal H2a (c2's own guard): `python3 /tmp/r38sep/treeA/round38/c2-count.py --gate
  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38402 --receipt
  /tmp/r38sep/c2-hunk2a-s38402.json` → `RECEIPT_BINDING_MATCH=7/7`, 7 PASS / 0 FAIL, rc=0; receipt
  `matched=7`, `predicate_holds=true`, `counter_sha256 == f4a4cbab…` (the mutant's own hash).
- H2b (subject guard): `python3 /tmp/r38sep/treeB/round38/c2-count.py --gate …/tools/research-gate.sh
  --seed 38403 --receipt /tmp/r38sep/c2-hunk2b-s38403.json` (default subject = the H2b c1 copy)
  → `RECEIPT_BINDING_MATCH=6/7`, rc=1; sole FAIL `self-rewrite-refused` expect
  `{'counter_rc': 2, 'receipt': False}` observed `{'counter_rc': 0, 'receipt': True}`; other six PASS.
- c1 stays 7/7 under H2b: `python3 /tmp/r38sep/treeB/round38/c1-count.py --gate
  …/tools/research-gate.sh --seed 38405 --receipt /tmp/r38sep/c1-guardhunk-s38405.json`
  → `ENV_PIN_CAPTURE_MATCH=7/7`, rc=0.

(3) C2 against the base gate, default r38 counter: `python3
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed
38404 --receipt /tmp/r38sep/c2-base-s38404.json` → `RECEIPT_BINDING_MATCH=7/7`, 7 PASS / 0 FAIL,
rc=0; receipt `gate_sha256 == a7d3922c…` (base gate), `subject_counter` = landed c1,
`counter_sha256 == 414a7a10…` (landed c2), `matched=7`, `predicate_holds=true`;
verify against the base gate → `VERIFY: ok`; against the landed gate → `VERIFY-FAIL:
gate-sha256-mismatch`.

Extra probes (same seeds family): landed c1 vs an F1 self-rewrite shim (`/tmp/r38sep/f1-shim-gate2.sh`,
seed 38407) → `c1-count: gate bytes changed across the run (pre 7140e020bb74a7f6 != current) — no
receipt published`, rc=2, no receipt file. H2b c1 vs the same class of shim (`f1-shim-gate.sh`, seed
38406) → `ENV_PIN_CAPTURE_MATCH=7/7`, rc=0, receipt published with `gate_sha256_pre 35af5119…` !=
`gate_sha256_post 37e2b996…`, `predicate_holds=true`; that receipt verified with the mutant counter
→ `VERIFY-FAIL: gate-sha-changed-across-run` (with the landed counter → `counter-sha256-mismatch`).

## Findings
1. **C1's gate half is single-hunk live (H1 → 4/7).** The three function-export cells fail exactly as
   the frozen separation describes (echo re-add, root move, suppress), while the two override cells
   remain gate-independent (`env_pin_init` refuses pre-capture). Pointer: `c1-count.py` scenarios
   `env-fn-{echo-scrub,root-move,suppress}` vs gate `research-gate.sh:4001`. No over-claim: the
   mutant does not reproduce the 2/7 base state, and nothing here extends C1 past Erratum 6's
   narrowed reading (PATH/loader vectors remain out).
2. **The counter-side 6/7 drop belongs to the subject counter, not to c2's own guard (calibration).**
   No c2 scenario writes the `--gate` file — the self-rewrite fixture is a distinct path
   (`c2-count.py:170`, shim body `c2-count.py:114-133`) and the foreign gate is a copy
   (`c2-count.py:179`); so `c2-count.py:320` is inert under the frozen census and H2a scores 7/7.
   The census does exercise the subject's guard through `self-rewrite-refused`: H2b drops c2 to 6/7
   with observed `counter_rc 0 / receipt true`. Reported as the assignment's expected number under
   the mechanism that produces it; the literal file named in the assignment does not move the count.
3. **F1 remains closed even if the guard is deleted, but only at verification (defence in depth).**
   With H2b the F1 shim produced a receipt binding pre 35af5119 ≠ post 37e2b996; `verify-receipts.py`
   refuses it (`gate-sha-changed-across-run`, `verify-receipts.py:198`). What the counter-side guard
   uniquely buys is the exit-2/no-publication behaviour the F1 claim words ("NO receipt published");
   deletion publishes a bound-but-unverifiable receipt. Not a kill; worth naming so the guard is not
   read as the sole barrier.
4. **Erratum 4's gate-agnostic claim holds on final bytes (D = 7/7 on base-gate-r37).** C2's
   predicate no longer depends on the C1 gate fix; the 7/7 receipt binds the base gate
   (`a7d3922c…`), verifies against it, and refuses the landed gate. Combined with H2b (c2 6/7 with
   only the counter guard removed), the c2 cells discriminate counter bytes, not gate bytes.
5. **Minor: the verifier's first named refusal depends on the `--counter` argument.** `counter_sha256`
   is checked (`verify-receipts.py:138`) before the gate pre/post check (`:198`), so a guard-disabled
   F1 receipt names `counter-sha256-mismatch` if handed the landed counter and
   `gate-sha-changed-across-run` only if handed the counter whose digest it carries. Consistent with
   Erratum 2/3's "named observable" design, but a reviewer must pass the receipt's own counter.
   Relatedly, `subject_counter` is covered only by the body digest, not semantically checked —
   admissible under Erratum 2's narrowed (integrity, not authorship) reading.

## Limits
- One seed per measurement (38401-38407) as assigned; no replication across seeds, so these are
  single-run numbers, not distributions (the labelled-not-replicated class of Erratum 6d).
- No `lsp` device exists in this leaf (`read xd://lsp` → "No such tool … Mounted devices: ast_edit,
  debug"), so all citations are line-level and command-level; no semantic-index claims are made.
- I did not re-run the 272-case gate selftest or re-verify all nine committed receipts (not
  assigned); only the base-gate receipt was regenerated (seed 38404) and verified both ways.
- The H1 mutant isolates the capture call site only; it does not test the PATH/loader vectors C1
  already names as r39 debt, and no conclusion is drawn about them.
- All mutants are /tmp copies; the lane repo, its jj/git state, and the fleet tree were not modified.
