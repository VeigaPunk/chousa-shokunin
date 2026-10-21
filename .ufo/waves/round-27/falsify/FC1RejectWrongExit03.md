# FC1RejectWrongExit03 — falsify C1 control `reject-wrong-exit`

Target: dd72641e574679c4f7882dd43de072b4c8892d6f. The gate sha256 matches the assignment: ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84.
Sandbox: /tmp/chousa-r27-falsify-FC1RejectWrongExit03, created with `git archive | tar -x`. All mutants and fixtures stayed there. No lane files were edited, and nothing was installed.

**Verdict: INCONCLUSIVE.** The landed gate is correct for every input of the "wrong exit" kind that I tried, so the gate itself holds. The control is weak in two ways:

- **(A) It does not test the fix it is named for.** It passes even after the targeted fix is reverted.
- **(B) It is narrow.** It checks only exit code 1, so two mutants that loosen the exit check survive it.

## What the control is

`corpus/evidence/round27-regressions.py:83` declares `('reject-wrong-exit', 1, usage, 1)`. A stub CLI prints `usage`:

```text
expected diagnostic
usage: fixture
Verdict: RESEARCH_GATE: CLEAN|DRIFT
```

The stub exits 1. The harness pulls the shipped bash function `metadata_asof_usage_case` out of the gate, runs it against the stub, and expects the harness to exit 1 (the case was rejected). The only check besides the exit code is that the output does not contain `command not found`.

## Question 1: is the expectation independent of gate code?

**Yes.** The expected value of 1 is hard-coded, and it comes from the C1 contract text: "exit1 fails" and "without … changing expected exit2". It is not computed from gate code.

The harness observes the gate's own `failures` counter (`exit "$failures"`), not an outside oracle. This is acceptable because the helper is the thing under test.

## Question 2: what happens when the targeted fix is reverted?

**The control does not fail. It passes under the revert, so it is not a mutation control for the fix.**

The diff from base 64eec5d to dd72641 changes one predicate in `metadata_asof_usage_case`, at gate line 6048:

- Before: `$out != *'RESEARCH_GATE: '*` (substring match).
- After: an anchored count, `nverdict=$(grep -c '^RESEARCH_GATE: ')` with `nverdict -eq 0`.

The `$rc -eq 2` conjunct is unchanged from base. `reject-wrong-exit` rejects because of `rc`, which is code the round did not change.

I ran `probe.py`, which replicates `round27-regressions.py` lines 69–93 for selected scenarios. Exit codes and outcomes:

| Gate variant (one-line change at :6048) | correct-usage (rc=2) | reject-wrong-exit (rc=1) | rc 0 | rc 3, 127, 130, 255 |
|---|---|---|---|---|
| landed | accept (correct) | reject (correct) | reject | reject (all correct) |
| `base`: substring predicate restored | **MISMATCH** (rejects) | **still passes** | reject | reject |
| `norc`: `rc -eq 2` removed | accept | **MISMATCH** (harness exit 0) | MISMATCH | MISMATCH |
| `ne0`: `rc -ne 0` | accept | **MISMATCH** | reject | MISMATCH |
| `le2`: `rc -le 2` | accept | **MISMATCH** | MISMATCH | reject |
| `ge2`: `rc -ge 2` | accept | **survives** | reject | **MISMATCH** |
| `ne1`: `rc -ne 1` | accept | **survives** | MISMATCH | **MISMATCH** |

- The landed gate's probe exited 0. Every mutant's probe exited 1.
- In the `base` row, the revert is caught only by the sibling control `correct-usage-with-help`.
- When the control does fail, it fails for the intended reason: the stub's exit code, not a parse or setup error. For example, under `norc` the output is `ok-case 1 fixture exit=2` with harness exit 0, against an expected 1. Helper extraction succeeded every time, and no `command not found` appeared.

## Question 3: nearby inputs where the gate is wrong or the control is vacuous

**Gate wrong: none found.** The landed gate rejects rc ∈ {0, 1, 3, 127, 130, 255} and accepts rc=2. An `FAKE_RC=258` wraps to exit status 2 at the OS level and is correctly accepted as 2.

**Control gaps:**

1. **Surviving mutants (minimal counterexample).** With `$rc -ge 2` or `$rc -ne 1` at line 6048, every C1 regression scenario still passes. All of them use rc ∈ {1, 2}: the scenarios at lines 80–85.
   - Yet usage errors with exit 0, 3, 127, or 255 would be wrongly accepted. For example, under `ge2` a stub at rc=3 gives `ok-case 1 fixture exit=2`, and that ok-line still reports `exit=2`.
   - The in-tree selftest control `metadata-asof-usage-exit-control` (gate line 6300) also uses only rc=1. [INFERENCE, by inspection; the full selftest was not run, as the assignment requires.] So the same mutants would survive it.
   - **Impacted axes:** operability, calibration.
2. **The reason for rejection is not asserted.** `observe(...)` for this control checks only the exit code. A mutant that breaks diagnostic matching (`*"XX$expected"*`) still passes `reject-wrong-exit`; only `correct-usage-with-help` catches it. The pair discriminates on `rc`, but the control alone could pass for the wrong reason.
3. **`metadata_asof_usage_accepts` is never called** (gate :6036–6040). The gate has one definition and no call site. The harness extracts it (regressions.py:74) and never invokes it.
   - Mutating its body to `true` leaves all 8 probe scenarios passing (probe exit 0).
   - It duplicates the predicate at :6048. That contradicts the harness comment "not a duplicated predicate" and creates a second source of truth that could drift unnoticed.

## Smallest safe correction (advice to the author lane)

- **Widen the scenarios.** In regressions.py, either add `('reject-exit0', 0, usage, 1)` and `('reject-exit3', 3, usage, 1)`, or parametrize the wrong-exit case over rc ∈ {0, 1, 3, 127}. Mirror the same values in the selftest's `*-exit-control`. This kills the `ge2` and `ne1` mutants.
- **Assert the reason.** Add `required=('FAIL-case', 'rc=1 ')` to the wrong-exit observation so that it fails only for the exit-code reason.
- **Settle the duplicate predicate.** Either delete `metadata_asof_usage_accepts` from the gate and drop it from the harness extraction list, or have `metadata_asof_usage_case` call it.
- **Relabel the evidence.** `reject-wrong-exit` should not be cited as evidence for the anchored-verdict repair. The controls that do discriminate the repair are `correct-usage-with-help` and `nonrecord-mention-is-not-verdict`.

## Limits

- I did not run the full selftest or the whole regression script; L1 owns those.
- The in-tree selftest control's behaviour under the mutants is inferred from inspection only.
- The probe replicates harness lines 69–93 faithfully: the same stub, helper extraction, script, env, and `forbidden` check.
- Mutant files `mut-*.sh` and `probe.py` remain in the sandbox only.
