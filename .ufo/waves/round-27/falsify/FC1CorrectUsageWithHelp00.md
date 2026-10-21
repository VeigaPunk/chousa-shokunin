# FC1 — correct-usage-with-help

Target: `dd72641e574679c4f7882dd43de072b4c8892d6f`, round27 attempt1 only.

Axes: **operability** attacked; **calibration** of the control's scope examined. Freshness/C2 and C3 were not tested.

**Verdict: HOLDS for the assigned control and its intended substring-regression defect. Mutant KILLED.** A nearby, explicitly dependency-fault-injected counterexample shows that the landed helper fails open when its record matcher errors. The named positive alone does not expose that error, but the existing adjacent CLEAN/DRIFT negative controls do. This is not evidence of a false-green complete C1 suite, nor outside admission.

## 1. Is the expectation contract-derived?

Yes. `corpus/evidence/round27-claims.md:5–7` independently requires exit2, the required diagnostic, no actual verdict, and anchored `^RESEARCH_GATE: ` record recognition rather than a help-text substring. `corpus/QUALITY.md:117–123` separately states the diagnostic/record distinction.

The fixture at `corpus/evidence/round27-regressions.py:69–93` supplies exit2 and these literal bytes:

```text
expected diagnostic
usage: fixture
Verdict: RESEARCH_GATE: CLEAN|DRIFT
```

It has the diagnostic and zero anchored verdict records, so expected helper exit0 follows from the declared contract, not the gate's answer. The test extracts the shipped functions as its subject, rather than copying their predicate into its oracle. It actually invokes `metadata_asof_usage_case`; the additionally extracted `metadata_asof_usage_accepts` is not called by this control. This is helper-level testing, not an end-to-end invocation of the real metadata CLI.

## 2. One targeted mutation; identical bounded detector

Sandbox only: `/tmp/chousa-r27-falsify-FC1CorrectUsageWithHelp00`.

Setup, exit0:

```sh
mkdir /tmp/chousa-r27-falsify-FC1CorrectUsageWithHelp00 && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e574679c4f7882dd43de072b4c8892d6f | tar -x -C /tmp/chousa-r27-falsify-FC1CorrectUsageWithHelp00
```

The detector `fc1-probe.py` uses Python AST selection to execute only the original regression preamble and its C1 fixture block, stopping immediately after the C1 scenario loop. In `named` mode it selects only the original `correct-usage-with-help` tuple. Original helper extraction, subprocess execution, expected result and `observe()` are unchanged. Temporary fixture directories are forced inside this sandbox. No full regression script or full selftest ran.

Smallest behavioral reversion: only `tools/research-gate.sh:6048` changed, in the function the control actually calls:

```diff
-    if [[ $rc -eq 2 && $out == *"$expected"* && ${nverdict:-0} -eq 0 ]]; then
+    if [[ $rc -eq 2 && $out == *"$expected"* && $out != *'RESEARCH_GATE: '* ]]; then
```

The count computation and all other bytes were retained. This reintroduces the exact historical substring-rejection mechanism; it does not change the unused accepts helper.

The exact same command ran in the sandbox for each phase:

```sh
timeout 60s python3 fc1-probe.py tools/research-gate.sh named
```

| Bytes | Command exit | Control actual/expected | Key stdout; stderr |
|---|---:|---|---|
| Pristine | 0 | 0/0, zero mismatches | `ok-case  1  fixture                      exit=2`; empty stderr |
| Mutated | 1 | 1/0, one mismatch | `FAIL-case fixture                      rc=2 expected=expected diagnostic verdicts=0`; empty stderr |
| Restored | 0 | 0/0, zero mismatches | `ok-case  1  fixture                      exit=2`; empty stderr |

Mutant stdout then prints the three fixture lines verbatim. Thus the CLI stub still returned the required exit2, its diagnostic was present, extraction/parsing succeeded, and the anchored count was zero. Rejection is specifically caused by the help line's nonrecord substring. **This is a behavioral kill, not a setup/parse failure.**

SHA-256, measured using `sha256sum` (all hash commands exit0):

| Artifact/phase | SHA-256 |
|---|---|
| Gate pristine | `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` |
| Gate mutated | `d3ee8161e87bb713362324b8307394f00b2b446758173bccc65074b56bdee91f` |
| Gate restored | `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` |
| Unchanged regression script, before/after | `5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df` |
| Unchanged claims, before/after | `80b77621f37f4366319e362f27cdef488eebe7277985b15fb0b3dcdc373ded6b` |
| Unchanged focused detector | `6ca0653cf8d6c5a7cd259bae25551b896ce9a7dd4d2b380693c8cb3001fe1090` |

The inverse one-line edit restored the exact original gate hash, and the identical detector passed on those restored bytes.

## 3. Nearby synthetic cases and bounded counterexample

Pristine command, exit0:

```sh
timeout 60s python3 fc1-probe.py tools/research-gate.sh nearby
```

Ten synthetic output cases, zero mismatches: diagnostic-only/no-help; quoted CLEAN mention; space-indented CLEAN; actual CLEAN first; actual DRIFT last; exit0 instead of exit2; help without diagnostic; empty output; bare anchored `RESEARCH_GATE: ` prefix; actual CLEAN with CRLF. Their helper actual exits were respectively `0,0,0,1,1,1,1,1,1,1`, matching the declared prefix/diagnostic/exit contract. Accepting diagnostic-only output is not a falsifier: C1 does not require help prose to be present.

**Nearby counterexample, limited to a matcher dependency fault:** without modifying the landed gate, put an executable synthetic `grep` first in the child process's PATH. Its complete contents were:

```sh
#!/usr/bin/env bash
printf '%s\n' 'grep: synthetic matcher failure' >&2
exit 2
```

Fixture SHA-256: `7d5505483da302a625e444e4ed6569b498b9dddea9d0b7174ea714f17afd7043`.

The `grep-fault` detector mode prepends only this sandbox directory to its own PATH, then runs the original positive and four original negative C1 tuples. Command, exit1:

```sh
timeout 60s python3 fc1-probe.py tools/research-gate.sh grep-fault
```

Actual results:

| Original control | Expected helper exit | Actual | Key output |
|---|---:|---:|---|
| correct-usage-with-help | 0 | 0 | `ok-case ... exit=2` |
| reject-clean-verdict | 1 | 0 | `ok-case ... exit=2`; mismatch `exit 0 != 1` |
| reject-drift-verdict | 1 | 0 | `ok-case ... exit=2`; mismatch `exit 0 != 1` |
| reject-wrong-exit | 1 | 1 | `FAIL-case ... rc=1 ... verdicts=0` |
| reject-missing-diagnostic | 1 | 1 | `FAIL-case ... rc=2 ... verdicts=0` |

Every result has stderr `grep: synthetic matcher failure\n`. For the CLEAN counterexample the synthetic CLI still exits2 and emits exactly the three positive-fixture lines above, followed by `RESEARCH_GATE: CLEAN\n`; DRIFT substitutes `DRIFT`. The helper incorrectly accepts those actual verdict records because `grep ... || true` discards the error and `${nverdict:-0}` converts absent count output into zero. The positive's forbidden substring check only excludes `command not found`, not this matcher error.

**Calibration:** the named positive is blind to this dependency failure, but the existing negative controls expose it: the bounded run reports five cases/two mismatches, not a green suite. This does not establish an input-only defect with a functioning matcher. Author-lane advice: do not interpret the positive alone as evidence that record counting succeeded; count-error handling is a separate boundary.

## Reproduction detector

The saved sandbox `fc1-probe.py` is unchanged across pristine/mutated/restored runs. Its named-mode selection is equivalent to the following executable extraction, with the original `observe()` and fixture body retained rather than reconstructed:

```python
import ast, sys, tempfile
from pathlib import Path
root = Path('/tmp/chousa-r27-falsify-FC1CorrectUsageWithHelp00')
p = root / 'corpus/evidence/round27-regressions.py'
tree = ast.parse(p.read_text(), filename=str(p))
fixture = next(n for n in tree.body if isinstance(n, ast.With))
i = next(i for i, n in enumerate(fixture.body)
         if isinstance(n, ast.For) and isinstance(n.target, ast.Tuple)
         and [part.id for part in n.target.elts] == ['name', 'rc', 'output', 'expected'])
fixture.body = fixture.body[:i + 1]
tree.body = tree.body[:tree.body.index(fixture) + 1]
fixture.body[-1:-1] = ast.parse(
    "scenarios = [row for row in scenarios if row[0] == 'correct-usage-with-help']"
).body
ast.fix_missing_locations(tree)
tempfile.tempdir = str(root)
sys.argv = [str(p), '--gate', str(root / 'tools/research-gate.sh')]
ns = {'__name__': '__focused_control__', '__file__': str(p)}
exec(compile(tree, str(p), 'exec'), ns)
print(ns['results'])
raise SystemExit(int(any(row['errors'] for row in ns['results'])))
```

## Limits and tools

All test execution used the one sandbox; the only lane write is this requested report. No production source/index/history changes, no network, host secrets, live-process inspection, subagents or background jobs. No C2/C3 evaluation, full selftest, complete regression run, resource-safety claim or outside-admission judgment. The fault fixture is explicit dependency substitution, not evidence that the installed matcher spontaneously fails.

Observed tools: Python `3.14.8`; Bash `5.3.20(1)-release`; `grep grep (pi-uu-grep) 0.2.0`. Version/hash command exited0: `python3 --version && bash --version && grep --version && sha256sum fc1-probe.py`. No installations or updates. Final hash command exited0: `sha256sum tools/research-gate.sh fc1-probe.py corpus/evidence/round27-regressions.py corpus/evidence/round27-claims.md fault-bin/grep`.
