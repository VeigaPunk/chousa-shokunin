# FC1 — `reject-clean-verdict` (C1 usage-harness control)

Revision: `dd72641e574679c4f7882dd43de072b4c8892d6f` (lane master)
Gate: `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches declared)
Control: `corpus/evidence/round27-regressions.py:81`
Sandbox: `/tmp/chousa-r27-falsify-FC1RejectCleanVerdict01` (archive extract only; no lane file touched)

## Verdict

**HOLDS** for the control's own hard-coded expectation (a synthetic anchored CLEAN/DRIFT line on a
usage error must make the shipped helper report failure, exit 1; removing the verdict guard does make
it fail for that reason).

**FALSIFIED** for the surrounding calibration claim: this control has **zero differential power over
the declared anchoring repair**, and a mutant that still consults the help-text substring in the
*accept* direction passes all six C1 scenarios. The suite therefore does not enforce the contract's
"count verdict records by anchored `^RESEARCH_GATE: `, not help-text substrings" in both directions.

## Method

Faithful single-block reproduction of `round27-regressions.py:68-103` (same helper extraction, same
constructed script, same env) in `c1probe.py`; gate mutants are sandbox copies. No full
`--selftest`, no full regression run, no network/host probes, no installs.

## Observed facts

### F1 — expectation vs independence

- Expected exit `1` is contract-derived: claims C1 requires "actual CLEAN/DRIFT verdict fails".
- The harness is **not** gate-independent: it extracts `metadata_asof_usage_accepts` and
  `metadata_asof_usage_case` out of the gate text and executes them, and its `usage` fixture copies
  the gate's help line `Verdict: RESEARCH_GATE: CLEAN|DRIFT`. The expected *values* are independent;
  the unit and fixture are not.

### F2 — mutation of the verdict guard (the fix this control names)

Mutant M2: remove `&& ${nverdict:-0} -eq 0` from `metadata_asof_usage_case` (keep rc/diagnostic).

```
$ python3 c1probe.py mutants/gate-M2-noverdictguard.sh
PASS              correct-usage-with-help       rc=0 expected=0
CONTROL-MISMATCH  reject-clean-verdict          rc=0 expected=1 helper_said=ok-case
CONTROL-MISMATCH  reject-drift-verdict          rc=0 expected=1 helper_said=ok-case
```

`observe()` records `exit 0 != 1` — the helper **accepted** the verdict; not a parse/setup error.
The gate's own added wrapper agrees:

```
$ bash -c '<extracted wrapper+helpers>; metadata_asof_usage_control_case clean-control 0 2 ...'
LANDED : ok-case  1 clean-control accepted=0      failures=0  exit=0
M2     : FAIL-case clean-control accepted=1 want=0 failures=1 exit=1
```

### F3 — the control is insensitive to the anchoring repair (no differential power)

Mutant M1: revert `grep -c '^RESEARCH_GATE: '` to `grep -c 'RESEARCH_GATE: '` in both usage helpers.

```
PASS              reject-clean-verdict       rc=1 expected=1 helper_said=FAIL-case
CONTROL-MISMATCH  correct-usage-with-help    rc=1 expected=0
CONTROL-MISMATCH  nonrecord-mention-is-not-verdict rc=1 expected=0
```

`reject-clean-verdict` stays green because the rejected input also carries the unanchored help line;
the substring guard rejects for the wrong reason. The anchoring fix is detected only by the two
*accept* scenarios, not by this control.

Base check (`git show 64eec5d…:tools/research-gate.sh`): the base helper's
`$out != *'RESEARCH_GATE: '*` guard also rejects the same scenario, so this control was already
green before the repair. (The base lacks `metadata_asof_usage_accepts`, so the official suite would
abort at extraction on base — noted, not run.)

### F4 — surviving mutant: help-substring still gates acceptance

Mutant M3: acceptance condition additionally requires the unanchored help substring, i.e.
`... && $out == *'Verdict: RESEARCH_GATE: '*`.

```
$ python3 c1probe.py mutants/gate-M3-helpgated.sh
PASS  correct-usage-with-help   PASS  reject-clean-verdict   PASS  reject-drift-verdict
PASS  reject-wrong-exit         PASS  reject-missing-diagnostic
PASS  nonrecord-mention-is-not-verdict
CONTROL-MISMATCH accept-without-help  rc=1 expected=0   # rc2, required diagnostic, no help line
```

All six declared C1 scenarios pass with help-substring logic still present. The suite never feeds an
output without the help line, so only an extra `accept-without-help` input exposes it. The mechanism
probe does not catch it either — `round27-mechanisms.py` counts only the literal old predicate:

```
$ python3 corpus/evidence/round27-mechanisms.py mutants/gate-M3-helpgated.sh
"C1_faulty_usage_substring": 0
```

### F5 — control-registration deletion is invisible

M5 deletes the five `metadata_asof_usage_control_case …` registrations added by the repair (6→1
occurrences of the wrapper name). The six C1 scenarios are unchanged (still PASS). By code read,
`--selftest` prints PASS from `failures -eq 0` only (gate 6518-6523) with no case-count assertion, so
the gate would print `PASS (205 cases)` and exit 0. No file outside `tools/research-gate.sh`
references those case names (`grep -rn` over `corpus/evidence/*.py|*.sh|*.md`).

### F6 — dead helper is load-bearing for the suite

`metadata_asof_usage_accepts` occurs exactly once in the gate (definition, line 6036, never called).
`round27-regressions.py:74` *requires* it; `parser.error` on absence exits the whole 58-control suite
with status 2. Deleting this dead code (the default hygiene move) turns the independent suite into a
setup abort.

### F7 — latent same-class accepted verdicts

Landed helper accepts verdict-looking lines it cannot see at column 0:

```
crlf-verdict    exit=0 (ACCEPTED verdict)
ansi-verdict    exit=0 (ACCEPTED verdict)
crlf-after-nl   exit=1 (rejected)
```

The gate emits no ANSI (`grep -c '\\033\|\\e\[' = 0`) and no CR before its verdicts, so this is latent,
not live — but the predicate is syntactic decoration-sensitive.

### F8 — real gate outputs checked

Three usage-error invocations on a synthetic root (`--as-of 2026-13-01`, `--as-of 2026-1-2`,
`verify --as-of` wrong mode): each `exit=2`, `anchored_verdicts=0`, diagnostic present. The landed
helper's accept path is consistent with real CLI output.

## Counterexamples (precise)

1. **Control vacuity / surviving mutant:** gate mutant M3 above. Synthetic inputs:
   - `rc=2`, `expected diagnostic\nRESEARCH_GATE: CLEAN\n` → landed rejects (exit 1, correct), M3 also
     rejects (nverdict catches it), so this input alone does not distinguish — the distinguishing input
     is the missing-help pair:
   - `rc=2`, `expected diagnostic\n` → landed accepts (exit 0), M3 rejects (exit 1).
   No scenario in `round27-regressions.py` covers either shape without the help line.
2. **Contract-boundary input:** `rc=2`, `expected diagnostic\n…\nRESEARCH_GATE: CLEAN|DRIFT\n` at
   column 0 in *help text* → landed rejects (exit 1) though the line is a usage example, not a record.
   Consistent with the literal anchored rule; collides with "correct usage passes" if the help text
   ever prints the format line unindented (the shipped `usage()` prefixes it with `Verdict: `, so not
   live).

## Limits

- Did not run the full `--selftest` or the full 58-control script (L1 owns those); F5's selftest claim
  is a code read of the PASS/FAIL branch, not an execution.
- Mutants are source-level copies; only test-harness behavior changes, production CLI paths are
  untouched (helpers run only under `--selftest`).
- M3's difference is not reachable through the shipped CLI (every `die_usage` prints `usage()`,
  including the help line); it falsifies control coverage, not current user-visible behavior.
- No installs performed.

## Author-lane advice

1. Add two C1 scenarios: verdict without the help line (expect reject) and required diagnostic without
   the help line (expect accept). That is what pins "not help-text substrings" rather than merely
   "does not reject the substring".
2. Either use `metadata_asof_usage_accepts` in the control wrapper or delete it; if kept, do not make
   the independent suite `parser.error` when an unused helper disappears.
3. Make the five selftest control registrations checkable (name presence or expected case count); a
   `--selftest` PASS does not pin membership, and `C1=0` does not pin semantics.
4. Record that `reject-clean-verdict` is a hold control (green at base), not evidence for the anchoring
   repair; the differential evidence for C1 is `correct-usage-with-help` and
   `nonrecord-mention-is-not-verdict`.

## Qualification to F5 (appended after writing)

The five added cases are recorded in the committed receipt
`corpus/evidence/round27-selftest-after.log:188-192` (`ok-case 188..192 metadata-asof-usage-*-control`
with `accepted=1/0`). So the registration set is evidenced by that log, not by an executable check.
No current control re-runs or compares against that log, so M5 would still print
`PASS (205 cases)` and exit 0, differing from the recorded `PASS (210 cases)` only to a reader who
diffs the log by eye.
