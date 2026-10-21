# FC1 — C1 `reject-missing-diagnostic` falsification

Pinned revision `dd72641e574679c4f7882dd43de072b4c8892d6f`; lane gate `tools/research-gate.sh`
sha256 = `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (verified).
Sandbox: `/tmp/chousa-r27-falsify-FC1RejectMissingDiagnosti04` (git-archive copy; all mutants and
stubs live there). No lane production file was edited. Full `--selftest` and the whole regression
script were not run (L1 owns them); the probe below replicates only the C1 block of
`corpus/evidence/round27-regressions.py` (lines 69–92).

## Item attacked

`corpus/evidence/round27-regressions.py:84`

```python
('reject-missing-diagnostic', 2, 'usage only\n', 1),
```

driven by lines 69–92: the suite extracts `metadata_asof_usage_accepts` and
`metadata_asof_usage_case` verbatim from the gate text (regex at :74) and invokes
`metadata_asof_usage_case fixture "expected diagnostic"` against a stub whose stdout/exit are
`FAKE_OUTPUT`/`FAKE_RC`. Expected suite exit is 1 (exactly one helper FAIL).

## Verdict: FALSIFIED as an independent missing-diagnostic control; HOLDS only as a self-check of the shipped helper on its one fabricated negative

The landed helper rejects `'usage only\n'` for the textual reason (expected token absent), but the
control (a) is not independent of gate code, (b) does not fail when the actual C1 production change
is reverted, and (c) is green for nearby same-class implementations that accept a *different*
required diagnostic than the caller asks for. The landed helper itself was not shown wrong on real
input; the falsification is of the guarantee the control is claimed to provide.

## (1) Contract derivation and independence

- The outcome mapping is contract-level: expected exit 1 corresponds to claims line 7, “missing
  diagnostic fails”. That part is right.
- The oracle is **not independent**: the script extracts the production helper from the gate under
  test (:69–76 explicitly: “Exercise the exact shipped usage helper in isolation, not a duplicated
  predicate”) and evaluates that helper's own accept/reject. It therefore cannot distinguish a
  defect the helper and the suite share. It also hardcodes the fabricated expected string
  `"expected diagnostic"` (:89), never one of the three real required diagnostics at gate
  `tools/research-gate.sh:6131–6135`.
- The negative fixture `'usage only\n'` is not a shape the CLI emits: every `die_usage` path prints
  the usage banner (`research-gate.sh:390` calls `usage()`; banner at :303–388). Observed on three
  real usage runs: `rc=2 anchored_verdicts=0 banner=1 diagnostic=1` each. So the control tests a
  rejection that cannot arise from a real usage error, and the positive/negative pair differs only
  by the substring, not by process shape.
- It requires `metadata_asof_usage_accepts` to exist (:74–77, `parser.error` if absent) but never
  calls it. That helper has **0 call sites** in the gate (only definition at
  `research-gate.sh:6036`). Consequence 1: mutations to it are invisible to all six C1 scenarios.
  Consequence 2: on the base gate (no such helper) the suite exits 2 at setup
  (`EXTRACT-FAIL metadata_asof_usage_accepts`), so the claims-doc sentence “run unchanged on an
  isolated base archive” is not executable; the later measurement clarification supersedes the base
  run, but this coupling is still real.

## (2) Mutation evidence — does reverting the targeted fix make the control fail?

Probe: `probe_c1.py GATE` (sandbox) runs exactly the six scenarios with the suite's extraction and
expected values.

| Mutant in sandbox gate | C1 block result | `reject-missing-diagnostic` |
|---|---|---|
| landed | exit 0, 6/6 PASS | PASS (rc=1, want 1) |
| M1: revert C1 fix — helper back to base `$out != *'RESEARCH_GATE: '*` instead of anchored count | exit 1; mismatches only `correct-usage-with-help`, `nonrecord-mention-is-not-verdict` | **PASS** (rc=1, want 1) — insensitive to the actual repair |
| M2b: delete the diagnostic clause, `$out == *"$expected"*` → `1 -eq 1` | exit 1; only `reject-missing-diagnostic` mismatches | **FAIL** (helper printed `ok-case ... exit=2`; rc=0, want 1) — intended reason |
| M3b: replace clause with banner proxy `$out == *"usage:"*` | **exit 0, 6/6 PASS** | PASS |
| M4: replace clause with first-word proxy `$out == *"${expected%% *}"*` | **exit 0, 6/6 PASS** | PASS |

M1 answers (2) for the named control: **no**, reverting the anchored-record fix leaves it passing;
the suite as a whole still catches M1 through two other scenarios, but this control is not mutation
evidence for the landed C1 repair. M2b shows total deletion is caught, but only as “not accepted”,
with no assertion of the failing clause.

In-gate comparison (same five `metadata_asof_usage_*_control` cases extracted and run in a mini
harness): landed exit 0; M3b exit 1 (`FAIL-case diagnostic-control accepted=1 want=0`); M4 exit 0.
So the in-gate negative (banner present, no diagnostic) catches the banner proxy, while the
independent block's negative (banner absent) does not. M4 is invisible to both.

## (3) Nearby synthetic input of the same class — minimal counterexample

Input A (control-shape, no banner):

```
usage: fixture
Verdict: RESEARCH_GATE: CLEAN|DRIFT
```
expected `"expected diagnostic"`, rc 2, no anchored verdict. Landed helper: rejects (exit 1).
M3b: accepts (exit 0). The suite's chosen negative `'usage only\n'` cannot tell these apart.

Input B (real-token shape): expected `--as-of must be a valid YYYY-MM-DD date`; stub rc 2, output =
the 82-line real banner only (captured from a real usage run; contains `--as-of` twice, not the
diagnostic). Results: landed helper exit 1 (rejects, correct); M3b **exit 0**; M4 **exit 0**
(accepts banner-only as if the diagnostic were present).

Paired real-CLI check: same landed CLI, expected `--as-of must be a valid YYYY-MM-DD date`, args
`verify-metadata corpus/knowledge/entry.md --root root --as-of` (missing value) produces
`research-gate: --as-of needs YYYY-MM-DD` plus the banner (rc 2, anchored verdicts 0). Landed helper
exits 1 (rejects the wrong diagnostic); M4 helper exits 0 (`ok-case ... exit=2`). Under M4 the
helper accepts a **different** required diagnostic because `--as-of` occurs in the always-printed
banner — the precise “accepting fewer required diagnostics” failure C1 forbids, with all six
independent scenarios and all five in-gate controls green.

## Exact commands and exit codes (sandbox copy)

```
sha256sum tools/research-gate.sh             # ca39d14d...92f84 == pinned claim
python3 probe_c1.py tools/research-gate.sh   # EXIT=0, 6/6 PASS
python3 probe_c1.py mut-m1-unanchored-verdict.sh  # EXIT=1; reject-missing-diagnostic PASS
python3 probe_c1.py mut-m2b-no-diagnostic-check.sh # EXIT=1; reject-missing-diagnostic MISMATCH rc=0 want=1
python3 probe_c1.py mut-m3b-banner-proxy.sh  # EXIT=0, 6/6 PASS
python3 probe_c1.py mut-m4-firstword-proxy.sh# EXIT=0, 6/6 PASS
python3 probe_c1.py base-gate.sh             # EXIT=2 EXTRACT-FAIL metadata_asof_usage_accepts
bash tools/research-gate.sh verify-metadata corpus/knowledge/entry.md --root root --as-of 2026-02-30
  # rc=2 anchored_verdicts=0 banner=1 diagnostic=1
bash tools/research-gate.sh verify-metadata corpus/knowledge/entry.md --root root --as-of
  # rc=2 anchored_verdicts=0 banner=1 diagnostic=1
bash tools/research-gate.sh verify corpus/knowledge/entry.md --as-of 2026-10-21
  # rc=2 anchored_verdicts=0 banner=1 diagnostic=1
# paired helper: landed -> helper_exit=1 FAIL-case; M4 -> helper_exit=0 ok-case
# banner-only real-token stub: landed -> 1; M3b -> 0; M4 -> 0
# in-gate 5 controls: landed -> 0; M3b -> 1 (diagnostic-control accepted=1 want=0); M4 -> 0
```

## Limits

- No full selftest and no full regression run (bounds; L1 owns both). The probe reproduces only the
  six C1 scenarios; C2/C3 untouched.
- Mutants are plausible weakenings used as discriminating-power tests, not evidence that the landed
  helper misbehaves on real emissions — the landed helper rejects inputs A and B.
- The “CLI cannot emit the negative shape” statement is observed for the three metadata `--as-of`
  usage paths; generalizing to every `die_usage` path rests on source at :390 (inference).
- One host shell run per command; no env inheritance beyond `CHOUSA_STRICT=0 LC_ALL=C` and the
  suite's own scrub. No installs were made.

## Author-lane advice

1. Replace the fabricated negative with a real-shape one: expected = a real diagnostic (e.g.
   `--as-of must be a valid YYYY-MM-DD date`), output = the real banner only, rc 2. This fails
   M3b/M4 and passes landed.
2. Add a case whose expected token's first word also occurs in the banner (`--as-of ...`) with a
   banner-only negative; that is the exact M4 blind spot.
3. Drop `metadata_asof_usage_accepts` from both gate and suite, or actually call it; today it is
   dead (0 call sites), its mutation is invisible, and its absence makes base runs exit 2.
4. Enforce the diagnostic's record position (`^research-gate: <expected>$`, or at least require the
   `research-gate: ` prefix) so banner words cannot satisfy the requirement; assert the helper's
   FAIL line/verdict count, not only exit code, for attribution.
