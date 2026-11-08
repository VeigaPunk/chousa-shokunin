"""Probe (c): named limit at its true width.
Claim named limit: "A counter edit that executes a leg and misreports its printed value survives —
the predicate binds the field the leg prints."
Test three distinct survivable classes:
  C-a (misreporting print value): E2/E3/E4/E6: leg body runs but ok hardcoded True; print still shows true measured value.
       The predicate binds the PRINTED field? No — predicate checks printed field VALUE (via substring/PASS?), instrument checks leg ok.
       The printed value in these probes remains correct (e.g. D1_REFUSED=3/3) because it is computed from real data.
       An attacker changing the PRINT to 1/1 while keeping leg True would need to also fake the print; but leg True alone passes instrument.
  C-b (tautology legs): E7 all True still PASS with REAL prints — stronger than named limit.
       Named limit says only "misreports its printed value survives". But E7 shows legs can be gutted entirely (no computation at all)
       and still PASS, because only the leg COUNT (15) and `all(ok)` matter. Deleting the computation inside the leg append is
       indistinguishable from misreporting. Plan doc §54 says "A leg whose body is deleted (the M5 shape) changes the leg count and fails"
       — FALSE. M5 deleted the CONJUNCT (`and setup_ok==1`), which is a tautology edit, not a leg deletion. A body deletion that keeps
       the append (e.g. replacing the ok expression with True) does NOT change the count. So the plan's §54 mechanism is mis-stated:
       it protects against deleting the whole append line, not against gutting the ok expression.
  C-c (narrowing both sides): E1 narrows builder AND counter to 1, still PASS with LEGS=15/15. The predicate's D1_EXPECTED=3
       field WOULD catch E1 if the external auditor checks the printed string (it prints 1), but the instrument itself reports PASS.
       Claim sentence: "a counter that narrows the class to one record ... fails the predicate instead of passing on printed fields."
       E1 passes the instrument's PASS with narrowed class — it only fails the EXTERNAL string match, which the claim conflates.
Quote the plan line and the claim line for the report.
"""
print("Named-limit width analysis done - see probes E1-E7.")
# Also run a no-append probe: actual leg deletion
