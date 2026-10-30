# Attack12 — C2 A10/A11/A12

Axes: calibration accuracy, mutant discrimination, frozen-byte fidelity; preserve production and frozen rules. Advisory review only; no admission or integration.

## Findings, severity order

### High — A10's purported new detector tests a different invariant

`gen-audit-mutants.py:64–66` changes row validation from `or` to `and`, admitting a six-column unknown rule. `tools/claims-audit-v2.py:109–111,351–361` adds/tests duplicate-id rejection instead. That guard is untouched by A10. Minimal observed counterexample: baseline rejects `R1\tunknown-class\tanchor line one\t\t\tunknown` with exit 1 / `bad rule row`; frozen A10 returns exit 0 / `FLAGGED=0/1 AUDIT=PASS`. Both baseline and A10 reject the actual C7 duplicate fixture with exit 1 / `duplicate rule id`.

This contradicts the claimed correspondence in `claims.md:159–160` and checker docstring lines 6–9. The frozen matrix (`c2-mutrun.py:88–100,148–163`) adds no unknown-rule input. R6 fault case 1 and R7 git history do not exercise row validation; the frozen probe's eleven legs use recognized rule names (`round63/audit-probe.py:66–120`). [INFERENCE from matrix/fixture inspection, not a full runner measurement] A10 remains a survivor under the unchanged matrix. This is an existing frozen C2 defect, not a fresh supplementary-mutant limit.

### High — A11 is not exercised by the advertised red leg

`gen-audit-mutants.py:67–71` changes the unexpected-fixture return at checker lines 286–288. However, `--selftest-fault 1` exits at lines 282–284 before that guard. Observed baseline and frozen A11 both produce `AUDIT_SELFTEST: FAULT case 1 forced`, exit 1. Thus R6 cannot kill A11.

A bounded in-process counterexample forces the first child audit to return a false-clean result: baseline `selftest()` returns 1; A11 prints `CASE 1 bad FAIL` and `AUDIT_SELFTEST: FAIL bad rc=0` but returns 0. This intentionally injected child result is probe evidence, not an honest checker output or claim of a matrix run. No git fixture is reached. Ordinary R1 runs have passing fixtures, while R2–R5/R7 do not invoke this selftest guard. [INFERENCE] A11 remains a survivor; a frozen `12/12` claim is unsupported by the advertised fault leg. Do not fold a repaired red leg into the frozen claim.

### Low — A12 kills more than the prose's second-arm description implies

`gen-audit-mutants.py:72–74` replaces both original quantifier arms with `the lane holds nothing at all`, rather than merely deleting `nothing in the lane`. Bounded probes confirm baseline flags both original arms (exit 1); A12 silently passes both (exit 0); both flag the retained `at all` wording (exit 1). Therefore A12's kill can be caused by the original first-arm fixtures (checker lines 243–244, probe lines 84–87), not uniquely the added C8 second-arm fixture. This is attribution weakness, not a survivor or an independent failure of the frozen kill count.

## Byte identity and evidence

`evidence.txt` records exact commands, stdout/stderr, exits and SHA-256. Read-only `git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:<path>` compared equal to current claims, generator, runner and v2 checker bytes, all git exits 0. Frozen instrument hashes match claims.md:264–266. The bounded driver exited 0 using Python 3.14.8. Reproducer preserved as `probe.py`; copy it into a newly created `/fast/scratch/hyaku/chousa-r64/Attack12/` and run `python3 -B /fast/scratch/hyaku/chousa-r64/Attack12/probe.py` from that scratch directory. It creates no git repository or commits.

Inherited `controls/c2-mutrun-v1.txt:10–13` records A10/A11 surviving and A12 killed, overall 6/12. That is inherited evidence, not a rerun by this seat.

## Residual risk and verification gaps

- Full c2-mutrun was intentionally not run: its selftest, probe and R7 create git commits (`tools/claims-audit-v2.py:289–302`, `round63/audit-probe.py:99–110`, `c2-mutrun.py:114–126`), prohibited by this assignment. No measured v2 total is claimed. L1 should distinguish the directly demonstrated missing detectors from the inferred full-matrix survivor result.
- No LSP device was mounted: `read xd://lsp` returned `No such tool`. All source analysis is literal inspection, not semantic reference/definition/diagnostic proof.
- C1 remains a frozen failure due to the independently drawn E12/E13 fixture-name mismatch, as supplied by the assignment and preserved in `claims-erratum.md:5`; not rerun or repaired here. `c1-battery-supplement.py` is distinct post-freeze evidence and cannot admit C1. Candidate ref-preflight-v3.py is not production.
- No production edits, network, dispatch, git/jj mutations, installations, or other runtime invocation. Existing Python 3.14.8 used; no tool install/update to record. No clone created. Scratch removed before completion.

Self-evaluation: accuracy 4/5 (direct counterexamples, but matrix total inferred); completeness 4/5 (all assigned mutants covered; prohibited full runner omitted); clarity 4/5 (measured/inferred distinction explicit, long source citations); actionability 4/5 (preserved driver; complete matrix requires authorization); conciseness 4/5 (necessary evidence detail). Overall 4.0/5. Highest-impact improvement: authorized canonical-run confirmation of A10/A11 survivors without changing frozen inputs. The user should agree with the explicit verification boundary.
