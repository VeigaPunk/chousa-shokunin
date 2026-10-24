# W2RevC2Final — c2-count.py + verify-receipts.py review

## Verdict

The re-sealed doctors now reach their named checks (7/7 at seed 38411 with the exact
labels quoted below), but the verifier's `ok` re-derivation is WEAKER than the frozen
expectation table and the counter's own `ok`: dropping the three `*_contains` labels
from a committed c2 receipt and re-sealing it still verifies `ok` — so the frozen
Erratum 2 (iii) "re-derives every ok" is falsified on committed bytes.

## Evidence

Lane tip `git -C …/chousa-shokunin rev-parse master` = `8e93bc916527b3c21f0f702967fa65c3b4c31699`;
gate sha256 `37e2b996…d27d` (matches claims.md). Working tree was DIRTY during this
review (see Finding 6). All temp work under `/tmp/c2rev`.

1. Full c2 run (fresh seed, live gate):
   `mkdir -p /tmp/c2rev/w && C2_TMP=/tmp/c2rev/w python3 corpus/evidence/round38/c2-count.py --gate tools/research-gate.sh --seed 38411 --receipt /tmp/c2rev/r-38411.json`
   → `RECEIPT_BINDING_MATCH=7/7`, wall 2m02s; the three tamper rows recorded
   `verify_fail: 'VERIFY-FAIL: counter-sha256-mismatch'`,
   `'VERIFY-FAIL: expect-sha256-mismatch'`, `'VERIFY-FAIL: receipt-self-digest'`
   with `clean_verify_rc: 0` — i.e. the doctors ARE re-sealed and the NAMED check is
   the asserted observable (Erratum 3 holds on the final bytes).
2. Independent named-check replay on a committed c1 receipt
   (`receipts/c1-after-s38351.json`, doctor logic copied from c2-count.py:135-155):
   `counter-doctor reseal=True (1, ['VERIFY-FAIL: counter-sha256-mismatch'])`,
   `expect-doctor reseal=True (1, ['VERIFY-FAIL: expect-sha256-mismatch'])`,
   `body-doctor reseal=False (1, ['VERIFY-FAIL: receipt-self-digest'])`.
3. Receipts sweep (live verifier): all 9 committed receipts `VERIFY: ok`;
   `c1-base-s38001.json` against the landed gate → `VERIFY-FAIL: gate-sha256-mismatch` rc=1.
   `c2-base-s38101.json` (matched 0, predicate_holds false) → `VERIFY: ok` rc=0.
4. Stale-receipt paths: `printf '{"stale":1}\n' > /tmp/c2rev/stale.json`;
   `C2_TMP=/tmp/c2rev/w2 python3 …/c2-count.py --gate /tmp/c2rev/does-not-exist.sh --seed 38413 --receipt /tmp/c2rev/stale.json`
   → `c2-count: gate not found: …` rc=2, `{"stale":1}` still present.
   Contrast (changed-gate refusal): pre-seeded stale receipt + c2's own F1 shim at
   seed 38423 → `c2-count: gate bytes changed across the run (pre 84b8f95b…) — no
   receipt published`, and `ls /tmp/c2rev/stale2.json` → No such file (unlinked).
5. PYTHONPATH channel: `/tmp/c2rev/site/sitecustomize.py` stubs `hashlib.sha256`;
   a c2 receipt with all six hash fields zeroed + `verify_fail` removed →
   clean env `rc=1 ['VERIFY-FAIL: receipt-self-digest']`,
   `PYTHONPATH=/tmp/c2rev/site rc=0 ['VERIFY: ok receipt=forged-pythonpath2.json …']`;
   marker file shows sitecustomize imported into the child.
6. Weighted axis (operability): seed-38411 run 122 s wall, timeout budget 900 s/invocation
   (c2-count.py:102) — no budget pressure at 7 scenarios.

## Findings

1. **MEDIUM — verifier re-derives a weaker `ok` than the frozen table; named-refusal
   observations are unbound.** `verify-receipts.py:159-162` (HEAD) / `:180-183` (live)
   computes `ok = all(observed.get(k) == v … if not k.endswith("_contains"))`, while the
   producer's predicate `c2-count.py:258-264` includes `_contains`. Demonstration (2 runs,
   committed receipt `c2-after-s38371.json`): set every row's `observed.verify_fail` to
   `"nothing-to-see"` and re-seal `receipt_sha256` → `VERIFY: ok`, rc=0; without the
   re-seal → `VERIFY-FAIL: receipt-self-digest`. So a receipt can carry `ok=true` for a
   tamper cell whose recorded refusal string is wrong/absent and still verify — the exact
   "doctored observations verified ok" class for the one field Erratum 3 designates as the
   asserted observable. Frozen claims.md Erratum 2 (iii) ("re-derives every ok from frozen
   expectations") is false as written; the live (uncommitted) Erratum 10 reclassifies
   `_contains` as "producer-side assertions", i.e. the claim text is being narrowed after
   the fact rather than the verifier strengthened.
2. **MEDIUM — `subject_counter` is unbound, so a receipt's attribution of WHICH pipeline
   was scored is forgeable.** Written at `c2-count.py:355`; `verify-receipts.py` never reads
   it (`KNOWN`, live :73-74, only whitelists it). Doctor a committed c2 receipt's
   `subject_counter` to `corpus/evidence/round37/c1-count.py` + re-seal → `VERIFY: ok` rc=0.
   C2's separability evidence (Erratum 4: "a tree landing only C2 also scores 7/7"; the base
   receipt's `subject_counter`) rests on this field. Erratum 10's "provenance path strings
   are not bound" names the mechanism but not this consequence.
3. **LOW/MEDIUM — the stale `--receipt` unlink sits behind five refusal paths.**
   `c2-count.py:285-303` returns 2 before the unlink at `:311-314` (missing gate / counter /
   verifier / expectations / non-existent `--tmp`); c1 has the same placement
   (`c1-count.py:215-231` vs `:239-242`). Demonstrated at seed 38413 (Evidence 4): rc=2 and
   the stale receipt survives. Erratum 7 states the refusal leaves no stale receipt
   unconditionally; the changed-gate refusal does unlink (evidence 4, seed 38423), so only
   the pre-scenario paths violate it.
4. **LOW — timeouts are declared but unhandled, and c2's budget is smaller than its
   subject's.** `c2-count.py:102,110` and `c1-count.py:118,124` pass `timeout=` with no
   `except subprocess.TimeoutExpired`: a hung child raises through `main()` as a traceback
   with exit 1, not the documented "2 on a harness error" (c2 docstring). The 900 s ceiling
   per subject invocation is below the subject's own worst case (7 scenarios × 2 bash calls
   × 180 s = 2520 s), so the inner timeout, not the outer one, governs.
5. **MEDIUM — the Python startup channel is unscrubbed while `base_env` scrubs the bash
   one.** `c2-count.py:89-95` (identical list to `c1-count.py:104-108`, parity confirmed)
   deletes `BASH_FUNC_*`, `CHOUSA_*`, `RESEARCH_GATE_*`, `BASH_ENV`, `ENV`, `SHELLOPTS`,
   `BASHOPTS` — but not `PYTHONPATH`/`PYTHONSTARTUP`/`PYTHONHOME`, although every child it
   spawns is `sys.executable` (`:100`, `:108`). Evidence 5: with a hostile `PYTHONPATH`
   every hash binding in the receipt is bypassed and the verifier prints `VERIFY: ok` on a
   receipt with six zeroed `sha256` fields. This is Erratum 5's BASH_ENV class one
   interpreter over, and it is not in §Limits.
6. **PROCESS — the reviewed verifier changed under me mid-wave.** `git status` on the lane at
   01:18:43 shows ` M corpus/evidence/round38/verify-receipts.py` and ` M corpus/evidence/round38/claims.md`
   (uncommitted Errata 9/10, +21 lines in the verifier, new `KNOWN` schema and type checks;
   `sha256 33c7c87e…` vs HEAD `796b8eb…`). Receipts bind the counters, not the verifier
   (Erratum 2 carried debt), so the swap silently re-adjudicates old receipts — demonstrated
   live. My seed-38411 run used HEAD bytes; findings 1, 2 and 5 were re-executed against
   the live bytes and still reproduce (`/tmp/c2rev/doctor-demo.py` output unchanged). Any
   seat citing verifier line numbers is citing a moving target.

## Limits

- The `_contains` substring check is fail-closed for a missing observation
  (`str(None)`), and `run_verify` captures stdout only (`c2-count.py:106-111`) — sound only
  because `fail()` prints to stdout (`verify-receipts.py:97-99`); a stderr-printing verifier
  would turn all three tamper cells into FAILs, never false PASSes.
- C2's predicate is integrity-only by design: the hold/foreign/legacy cells accept a subject
  receipt with `matched < 7` (Evidence 3, c2-base 0/7 → ok), so 7/7 on c2 does not imply the
  subject scored 7/7. The r37-pipeline control (0/7) remains the discriminator.
- Endpoint hashing cannot distinguish a gate that changes and restores within one scenario;
  a trampoline gate that re-execs different bytes underneath the bound path gets a valid
  receipt. Falls under the named black-box (F2) limit, reported as reach, not as a kill.
- I did not run the c2 counter against the r37 control (that receipt is committed and
  verifies; seed-38101 evidence not re-derived) or against the r38-counters-on-unfixed-gate
  arm — both are wave-1 claims outside my assigned slice.
- No LSP server was queried for this Python pair; findings are from executed runs plus
  line-cited source reads (single-file, no callers to resolve).
- No tool installs; nothing written outside `/tmp/c2rev` and this report.
