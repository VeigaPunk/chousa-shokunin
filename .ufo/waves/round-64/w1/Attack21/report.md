# Attack21 — causal separation review

Scope: advisory criticism only; no claim admission, production edit, or canonical judgment. Axes: **operability (C1), calibration (C2), sourced depth (C3)**; cross-cutting provenance and causal independence.

## 1. Frozen C1 failure cannot become supplemental success

**Counterexample/evidence.** Frozen `corpus/evidence/round64/c1-battery-v3.py:386–394` draws two independent tags in each of E12 and E13: the file is created using one tag and its purported index row uses another. E12 therefore need not be a valid escaped-underscore fixture; E13 need not be a valid percent-encoded fixture. The assigned known frozen failure is accepted, not re-run or hidden. A contract-correct G02 may reject these malformed purportedly benign fixtures. This is an instrument defect, not evidence that rejecting tool behavior is defective.

The inherited `c1-battery-supplement.py:386–396` draws `t` once per fixture and reuses it. These are different bytes and a distinct post-freeze instrument. Its header also retains the frozen v3 identity and 43-leg/28-defect description at lines 2–21, while lines 56–58 describe 44 legs/29 defects: a reader can confuse identity or denominator without inspecting the implementation.

**Impacted axes:** operability, calibration/provenance. Frozen claims lines 89–93 require the unmodified battery to pass three times at landing. A supplemental pass cannot satisfy that requirement. `controls/ref-preflight-v3.py` is a candidate, not proof of landed `tools/lane-preflight.py` behavior.

**Smallest safe correction:** record frozen C1 as failing its frozen closure requirement; report any supplement results under their own identity, counts, digest, target and status. Correct supplemental descriptive text only through L1, without changing frozen instruments or claims. No runtime output for this finding is invented.

## 2. C2 mutation score does not independently establish calibration

**Counterexample (static, not executed).** Take a target preserving every textual mutation anchor and insert `raise RuntimeError("baseline broken")` after its imports. Every generated mutant still patches successfully but exits before producing expected output. `c2-mutrun.py:148–168` treats every missing expected line/exit mismatch as a kill, so all twelve can be scored killed even though the unmutated target is unusable. This follows from the code; it is not a measured 12/12 receipt.

**Evidence.** `c2-mutrun.py:86` reads working-tree target bytes, not bytes resolved from a commit. Lines 135–174 contain only mutant execution and scoring; no unmutated matrix precondition exists. The claims' controls paragraph (166–167) promises unmuted actual outputs beside expectations, which this runner does not print. Lines 164–167 even count a timeout as a kill, despite the docstring's statement that a leg that itself errors is a harness error (lines 30–31). The existing v1 receipt genuinely records six survivors; it does not supply the missing baseline prerequisite for arbitrary v2 inputs.

**Impacted axes:** calibration and provenance. This is a weakness in the mutation instrument's causal interpretation, not a demonstrated failure of the actual v2 checker or of the exact frozen twelve-mutant closure outcome. C2 also separately requires expanded selftest/fault receipts; the static counterexample is not a claim that all those closure conditions were satisfied by a broken checker.

**Smallest safe correction:** in a separately named future/supplemental runner, require every unmutated matrix leg to match first, distinguish timeout/environment/harness errors from mutation-caused differences, and bind measured target digests to the intended committed bytes. Preserve and report frozen C2 results unchanged; do not silently replace its scoring rule.

## 3. C3 smoke and relocation do not establish full independence or coverage

**Strongest local counterexample.** The inherited `controls/c3-before.txt:2–4` already contains `LEG CLEAN clean FAIL rc=1 want 0`, followed by `BATTERY=PARTIAL` and `raw-exit=0`. That is direct local evidence that failed CLEAN and successful partial-process exit coexist.

`c3-count.py:72–76` accepts its C1 battery smoke solely when process exit is 0 and stdout contains `BATTERY=PARTIAL`. `c1-battery-v3.py:618–620` always returns 0 in `--only` mode regardless of leg failures. Therefore a failed CLEAN run of this exact shape satisfies C3's smoke condition. This is an observed semantic witness plus static composition, not a new executed probe.

Other separation limits:
- `c3-count.py:77–81` uses receipts `--runs 0` (argument/startup smoke, not a receipt measurement) and a source substring for its own third smoke leg. Thus `SMOKE=3/3` is not three functional success tests.
- Its relocation loop checks only `needs[0]` (`corpus/SOURCES.md`, lines 85–92). It does not exercise missing `tools/lane-preflight.py` independently for the two instruments listing that second prerequisite.
- Frozen claims lines 194–198 say “every round-64 instrument” deriving lane files, then freeze a three-member list. But `c2-mutrun.py:49–54` also derives its lane and probe from `__file__`, outside that list. The bounded list is not complete family coverage.
- C3's first smoke depends on the C1 harness; its receipts smoke addresses the C1 runner. C2/C3 therefore share machinery and root assumptions rather than being independent replication of each other.

**Impacted axes:** depth and calibration; operability if a partial smoke is represented as a valid clean lane. These findings do not prove the relocation assertions themselves fail or invalidate a correctly reported narrow three-member counter result. The frozen C3 requirement can be satisfied while the stronger functional-smoke/family-wide interpretation is false.

**Smallest safe correction:** retain literal frozen C3 receipts and explicitly qualify smoke semantics/list scope; use a distinctly named supplemental counter that requires `LEG CLEAN clean ok` and `CLEAN=1/1`, independently removes each asserted prerequisite, and enumerates additional family members. Do not present a C3 pass as curing frozen C1 or confirming C2 calibration.

## Byte provenance and commands

Executed read-only command, cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`:

```text
sha256sum corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/gen-audit-mutants.py corpus/evidence/round64/c2-mutrun.py corpus/evidence/round64/c3-count.py corpus/evidence/round64/run-receipts-v3.py corpus/evidence/round64/controls/root-shift-mutant.py tools/claims-audit-v2.py
```

Tool returned success (no numeric exit field exposed). Output:

```text
4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2  corpus/evidence/round64/c1-battery-v3.py
6e1055b28d315e32a3d43ee0866f9c32b78470899826f1d29c8c3707610a4191  corpus/evidence/round64/gen-audit-mutants.py
0045787ee9de39749e1dd06739259cd5f0a494865c921edbed91cfd86249a8c9  corpus/evidence/round64/c2-mutrun.py
465a8c5efbb870f73c7c6306c813c4fe35f4ccaf5a996a56ab71d4da5feec682  corpus/evidence/round64/c3-count.py
0f3cfae75f711f17251174a2e123321040c91394497bafe4a64c9148d7c3abd7  corpus/evidence/round64/run-receipts-v3.py
f0f9b26083ff62c35b9d54fe5bf7733f233c496368a5a62a3da02dbbb3f89175  corpus/evidence/round64/controls/root-shift-mutant.py
db0e28dd4c0332591b8898feb727f23a0e80b6e2ad29cbf0a6237d35a4d0b88d  tools/claims-audit-v2.py
```

All seven prefixes match frozen claims lines 263–266. This checks current instrument bytes against the frozen digest declarations, not the commit identity of the entire live lane. No Python/runtime probe was invoked under the critic's no-other-runtime restriction; no git/jj mutation, network access, install, clone or scratch tree was created. Inherited receipts are labeled as inherited, not fresh measurements. No tool installation/update to record.

## Self-evaluation

Accuracy 4/5: exact source spans and hash evidence; C2 counterexample remains static, explicitly labeled. Completeness 4/5: all three causal paths reviewed; no fresh runtime receipt under role restriction. Clarity 4/5: separates frozen failure, supplemental weakness and narrow counter semantics; source references require opening files. Actionability 4/5: smallest corrections specified without changing frozen rules; only L1 may apply them. Conciseness 4/5: provenance is long but independently reusable. Overall 4.0/5. Highest-impact improvement is a separately authorized unmutated-baseline probe, followed by a separately named C3 per-prerequisite supplement. Would the user agree: likely, provided advisory findings are not substituted for canonical judgment.
