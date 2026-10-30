# Attack13 — C2 mutation-runner kill semantics

Axes: calibration (a kill must distinguish checker behavior), operability (infrastructure failure must fail closed), provenance (frozen bytes and observed receipts must remain distinct).

## Counterexample: timeouts manufacture twelve kills

The frozen runner calls a timeout a kill, even though its own docstring says a leg error is a harness error, exit 2. At `corpus/evidence/round64/c2-mutrun.py:164–168`, `TimeoutExpired` appends a failing `TIMEOUT` leg; `killed = bool(fired)` then credits it. Lines 172–174 award exit 0 when all twelve time out. There is no successful unmutated-target control before scoring.

Bounded probe: `timeout-probe.py` imports the unmodified runner, supplies the `os` import normally provided by its CLI block, and sets only the subprocess timeout budget to zero. It preserves the actual `run()` implementation, generator, targets, anchor checks and scoring code. Both matrices produced twelve `MUT Axx killed leg timeout` lines, `AUDIT_MUTANTS_KILLED=12/12`, and `RUNNER_EXIT=0`. The command and exact output are in `timeout-output.txt`; combined shell exit was 0. No leg returned a checker verdict. The v1 target thus obtains a perfect score under injected infrastructure failure although its frozen ordinary receipt is 6/12, with A05/A06/A07/A08/A10/A11 surviving.

This is fault injection, not a claim that the default 300-second budget timed out. The probe modifies an in-memory budget, not frozen files; it demonstrates the real timeout-handler behavior with a cheap, deterministic trigger. R1 times out before any git fixture command is reached. No git mutation, clone, network access or production edit occurred.

### Classification and smallest safe correction

This is a defect in the **frozen** instrument's error/kill separation, not a weakness introduced by a post-freeze supplement. It contradicts the runner docstring at lines 28–31. The frozen claims at lines 127–129 define kills using exit/output differences; a timeout provides neither a completed exit nor output verdict. However, this probe does **not** establish a miss of C2's exact closure counting command at its normal budget, nor invalidate an independently reproduced default-budget 12/12. That distinction belongs in L1's canonical judgment; this report does not judge or admit C2.

Do not alter the frozen counter. In a distinctly named successor, return harness exit 2 for infrastructure timeouts without crediting a kill, and require the unmutated target to satisfy the same matrix before scoring mutants. Preserve the frozen result and route the instrument defect separately. This changes no legitimate completed-leg expectation and prevents infrastructure-only saturation.

## Additional frozen prose/implementation mismatch

`claims.md:164–167` says the runner prints each unmutated leg's actual output beside its expectation. It does not: `c2-mutrun.py:135–174` runs only patched targets and prints mutant summaries, never an unmutated matrix leg or its actual/expected output. This is static source evidence, not an independently executed baseline. It leaves shared environmental breakage indistinguishable from mutation-specific failure. Smallest safe correction: disclose the missing control in an erratum; add the explicit control only in a separately named successor. Do not manufacture baseline receipts.

## Frozen identity and limits

The working runner and generator SHA-256 values exactly match both the claims' frozen prefixes and bytes read from commit `bf40d99bda9eefdad3ed6276da077cfb24ba82f1`:

- runner: `0045787ee9de39749e1dd06739259cd5f0a494865c921edbed91cfd86249a8c9`
- generator: `6e1055b28d315e32a3d43ee0866f9c32b78470899826f1d29c8c3707610a4191`

Target working hashes match their frozen prefixes as recorded in the evidence. The frozen v1 receipt was read, not rerun. `controls/c2-mutrun-v2.txt` was absent when read; no normal-budget v2 verdict is asserted here. No supplemental C2 implementation was used.

C1 remains independently blocked: the supplied assignment and `claims-erratum.md:5` identify independently drawn E12/E13 filenames and README targets in the frozen battery. The inherited `c1-battery-supplement.py` is a distinct repair, not a frozen C1 pass. This seat neither reran nor repaired C1.

## Execution and cleanup

Existing Python 3.14.8; no installation or update (channel: existing host executable; reason: bounded timeout probe). Tool/version and hash command outputs are recorded in `timeout-output.txt`. Both probe invocations removed their work directories, then successfully removed `/fast/scratch/hyaku/chousa-r64/Attack13/` via `rmdir()` before exiting 0. No clone was created. Only this seat's report/evidence and designated report trailer were written.

Self-check: accuracy 4/5 (normal-budget outcome deliberately unmeasured); completeness 4/5 (runtime timeout branch exercised, ordinary closure left to assigned runners); clarity 4/5 (frozen numerical closure and semantic weakness explicitly separated); actionability 4/5 (successor control specified, not implemented by a critic); conciseness 4/5 (retained provenance and limits to prevent overclaiming). Mean 4.0/5. Highest-impact improvement for a successor: add a real harness-error control and unmutated matrix control. This assessment should match the user's scope: advisory falsification, not canonical closure.

Report: .ufo/waves/round-64/w1/Attack13/report.md
