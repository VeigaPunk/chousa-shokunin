# Attack02 — C1 strict-output injection review

Axes: output-contract fidelity, false acceptance resistance, frozen/supplement identity, and bounded reproducibility. Advisory findings only; no admission or production change.

## Findings by severity

### Medium — ZERO early return accepts injected, contradictory summary fields

Location: `corpus/evidence/round64/c1-battery-v3.py:480-487`; inherited `c1-battery-supplement.py:482-489` has identical logic.

With exit 2 and all eight correctly named, ordered gates SKIP, the judge accepts either of these final lines:

```
PREFLIGHT=0/999 FAILED=none ENV=none SKIPPED=G01,G02,G03,G04,G05,G06,G07,G08
PREFLIGHT=0/0 FAILED=G01,G01 ENV=G99 SKIPPED=none
```

Both returned `(True, 'ok')` from the actual frozen judge and supplemental judge. The first contradicts the promised `PREFLIGHT=0/0` ZERO contract (`c1-battery-v3.py:50-54`). The second injects duplicated FAILED membership, an invalid ENV gate id, and a false SKIPPED set, contradicting the stated strict distinct-valid-id/component contract (`:63-68`). The ZERO branch checks only summary syntax and numerator `0`, returning before the denominator and component checks at `:503-516`. A tool mutation confined to ZERO summaries therefore remains undetected by this judge; this does not demonstrate a full-battery pass.

Recommendation to canonical planner: route to a distinctly named future instrument. Validate ZERO denominator 0 and empty FAILED/ENV plus all-eight SKIPPED sets before accepting. Do not alter frozen bytes.

### Known claim failure — frozen E12/E13 fixtures are not benign

`c1-battery-v3.py:386-394` separately draws `tag()` for the created filename and README reference. These are not the same filename by construction; a conforming G02 checker must reject mismatched cases rather than earn the promised benign pass. `claims.md:89-93` requires the unchanged frozen battery's three full passes and makes a miss an honest stop. No supplemental pass substitutes for that condition.

Read-only comparison to freeze `bf40d99bda9eefdad3ed6276da077cfb24ba82f1` found frozen battery bytes unchanged. SHA256 is `4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2`, matching the frozen prefix in `claims.md:264`. The supplement is separately named, SHA256 `a7057ae33ac958f060a25ea325537bec7bed728e7ea2dad3f3a961e715fc33f1`; the entire observed diff stores one tag per E12/E13 and reuses it. It does not fix the ZERO judge weakness. The inherited erratum independently records this frozen failure at `claims-erratum.md:5`. I did not rerun the already reported full-battery failure or repair the fixture.

## Probe evidence

Files in this seat folder: `probe.py` and `probe-output.txt` (exact command, stdout, stderr and exit).

Command: `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack02/probe.py`, cwd absolute lane root, bounded to 30 seconds by its caller. Exit 0; stderr empty. Directly invokes each instrument's canonical `judge`; no alternate judge/runtime implementation. Seven cases per instrument: canonical ZERO accepted; both contradictory summary injections accepted; nonzero numerator rejected; unrelated extra line rejected; ASCII form-feed rejected; Unicode U+2028 line-separated output accepted.

The U+2028 result is recorded as a parser-boundary observation, not an additional confirmed defect: `splitlines()` recognizes those separators, and the frozen contract does not explicitly require LF-only framing. No claim of arbitrary noncontract-line injection, positive ZERO numerator acceptance, or positive-exit acceptance is made.

Additional read-only command: `git diff bf40d99bda9eefdad3ed6276da077cfb24ba82f1 -- corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/claims.md && git diff --no-index corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/c1-battery-supplement.py`. First diff empty; second prints only the E12/E13 changes; overall exit 1 is the expected no-index difference status, not a probe error.

## Residual risk and verification gaps

- No end-to-end 43-leg malicious tool run was performed; evidence establishes direct canonical judge acceptance, not BATTERY=PASS or production behavior.
- Candidate `controls/ref-preflight-v3.py` is not treated as production. Its correctness and the three frozen landing runs are outside this scoped probe.
- No saturation claim: these seven deterministic cases are not exhaustive output-language coverage.
- LSP device unavailable: `read xd://lsp` returned `No such tool`; references/definitions/diagnostics therefore unavailable. Source ranges and literal search are the fallback, not semantic proof.
- No frozen rules, counters, operator inputs, production files, git state or sibling outputs edited. No clone or scratch tree created, so no scratch cleanup remains. No network requests or installs.
- Existing tools: Python 3.14.8 and git 2.56.0, existing system executables, used for direct bounded probes and read-only frozen-byte comparison. No tool installation/update channel used.

## Self-evaluation

Accuracy 4/5: exact judge outputs and byte identity recorded; full execution impact is deliberately not claimed. Completeness 4/5: frozen and supplemental paths covered, not the full battery. Clarity 4/5: separates claim failure from instrument weakness; evidence file is verbose. Actionability 4/5: identifies precise early return and future validation change without editing frozen rules. Conciseness 4/5: retains command/output provenance at some length. Overall 4.0/5. Improvement priority: if the planner needs end-to-end impact, commission a bounded ZERO-only wrapper probe without treating PARTIAL as a claim pass. User agreement check: report stays within strict-judge scope and explicitly preserves the known frozen failure.
