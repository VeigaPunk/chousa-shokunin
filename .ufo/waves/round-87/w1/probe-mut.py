"""Probe (b) precise: 'accounts its verdict by counting executed legs' vs. what legs actually verify.
Line 566: passed = len(legs) == EXPECTED_LEGS and all(ok for _, ok, _ in legs)
So verdict requires (1) exactly 15 appends, (2) all ok. It does NOT count executions.
Every leg's ok is an expression computed before the append. Any expression can be replaced by True.
E2-E7 demonstrate each single-leg tautology passes. E8 shows the count only guards append count.
Also test: what about the TOOL leg? legs.append(("TOOL", os.path.isfile(tool), ...)) at line 375,
plus 14 more at 536-553 = 15 total. If tool absent, the else branch never runs, legs stays at 1,
passed=False. But printed LEGS would be 0/15 (line 565 special-case prints LEGS=0/15, not sum).
"""
import re
src = open("/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/wt/corpus/evidence/round87/gate-records-r87.py", encoding="utf-8").read()
m = re.search(r"passed = .*", src)
print(m.group(0))
print(src[src.index("legs += ["):src.index("legs += [")+300])
# mutant derivation probe details
print("\nMutant legs check: DERIVE derived only when build_mutant returns True (file written, bytes differ).")
print("DERIVE_NEG checks reversed (rewritten literal -> not derived). E5 showed killed can be hardcoded.")
