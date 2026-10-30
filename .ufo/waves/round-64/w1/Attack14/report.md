# Attack14 — C2 selftest fault injection

Axes: calibration (does the negative control exercise the failing guard?), reproducibility (frozen byte identity), operability (bounded, isolated probe).

## High — frozen R6 does not exercise the frozen A11 mutation

The fault injection bypasses, rather than fails through, the guard that A11 mutates.

- `tools/claims-audit-v2.py:280-288` computes `ok`, then handles `fault == ci` by printing FAULT and immediately returning 1 at lines 282–284. Only afterward does the genuine `if not ok` branch return 1 at lines 286–288.
- `corpus/evidence/round64/gen-audit-mutants.py:67-71` changes precisely that latter genuine failure return to 0; it does not change the injected-fault return.
- `corpus/evidence/round64/c2-mutrun.py:160-161` accepts R6 whenever exit is 1 and stdout contains FAULT. The exact frozen A11 mutant still meets that condition.

Minimal counterexample: force the first bad-fixture child result to exit 0 with `FLAGGED=0/6 AUDIT=PASS`. The unmodified checker selftest correctly exits 1; the exact frozen A11 mutant incorrectly exits 0. Enable fault 1 and both exit 1 with identical `AUDIT_SELFTEST: FAULT case 1 forced` output. Thus the advertised red leg cannot distinguish a working failure guard from the frozen broken guard. This is not a new mutant folded into the claim: the probe applies the existing frozen A11 textual replacement, with its one-occurrence anchor asserted.

Frozen claims lines 154–161 require 12/12 and expanded selftest/fault outputs; lines 170–174 make these closure requirements. The ordinary fault-1 output does reproduce. The stronger implication that this proves the real guard is able to fail is invalid. [INFERENCE] If all other A11 legs retain their expected outputs, A11 survives and the claimed 12/12 closure fails. This seat does not claim to have observed the complete mutant count.

No post-freeze supplement was used. This is a defect in the frozen C2 instrument, not merely a supplemental weakness. Keep the frozen result honest; any improved injection must receive a distinct supplemental identity, not rewrite the frozen runner or generator.

## Evidence and commands

Command (cwd = this report's directory):

```text
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack14/probe.py
```

Driver exit: 0. Python: 3.14.8. Reproducer: `probe.py` beside this report. Its JSON records each child exit/stdout/stderr and each in-memory target exit.

Observed outputs:

```text
actual frozen CLI --selftest --selftest-fault 1:
  exit 1; stdout "AUDIT_SELFTEST: FAULT case 1 forced\n"; stderr ""
frozen-v2 selftest(fault=0), bad child forced to pass:
  exit 1; stdout "CASE 1 bad FAIL\nAUDIT_SELFTEST: FAIL bad rc=0\nFLAGGED=0/6 AUDIT=PASS\n\n"
frozen-A11 selftest(fault=0), same child:
  exit 0; stdout "CASE 1 bad FAIL\nAUDIT_SELFTEST: FAIL bad rc=0\nFLAGGED=0/6 AUDIT=PASS\n\n"
frozen-v2 and frozen-A11 selftest(fault=1), same child:
  each exit 1; stdout "AUDIT_SELFTEST: FAULT case 1 forced\n"
  each satisfies the frozen R6 predicate
```

The child-result injection uses `unittest.mock` only to present the unexpected checker verdict to the real selftest guard. It is controlled fault-injection evidence, not a report that an actual independent audit produced that verdict. Each injected run invoked exactly one child-call boundary and stopped before any git fixture creation. The actual CLI red-leg run used no mock and also stopped before git setup.

Read-only comparison command:

```text
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff bf40d99bda9eefdad3ed6276da077cfb24ba82f1 -- corpus/evidence/round64/claims.md corpus/evidence/round64/c2-mutrun.py corpus/evidence/round64/gen-audit-mutants.py tools/claims-audit-v2.py
```

Exit 0, no output: inspected working bytes match that commit for these paths. `sha256sum` exit 0:

```text
0045787ee9de39749e1dd06739259cd5f0a494865c921edbed91cfd86249a8c9  corpus/evidence/round64/c2-mutrun.py
6e1055b28d315e32a3d43ee0866f9c32b78470899826f1d29c8c3707610a4191  corpus/evidence/round64/gen-audit-mutants.py
db0e28dd4c0332591b8898feb727f23a0e80b6e2ad29cbf0a6237d35a4d0b88d  tools/claims-audit-v2.py
```

These match frozen claims lines 264–266.

## Residual risk and verification gaps

- No full mutation matrix or ten-case selftest run: those paths perform git mutations in fixtures, prohibited by this seat's authorization. Therefore no observed `AUDIT_MUTANTS_KILLED` total is asserted here. L1 must determine the closure count under its own authorization.
- LSP unavailable: `read xd://lsp` returned `No such tool`; references/definition/diagnostics could not run. Text/source inspection is not represented as semantic-server proof.
- C1's known E12/E13 independently drawn-name mismatch remains an honest frozen battery failure; not tested or repaired here. `c1-battery-supplement.py` is a separate post-freeze instrument. Candidate `ref-preflight-v3.py` was not treated as production.
- No production/frozen inputs edited, no commits/pushes/clones/network calls, no installed tools. The reproducer removes `/fast/scratch/hyaku/chousa-r64/Attack14/` in `finally`; no clone was created.
- Recommendation only: this report does not admit, integrate, judge, or ship anything.

Self-check: accuracy 4/5 (full matrix unexecuted, inference labeled); completeness 4/5 (scoped counterexample complete, closure count left explicitly unobserved); clarity 4/5 (distinguishes mock injection from real CLI); actionability 4/5 (reproducer and exact frozen branches supplied); conciseness 4/5 (byte evidence retained). Overall 4.0/5. Main improvement: obtain the authorized full frozen matrix receipt rather than infer the remaining A11 legs.
