"""Check why control M2/M5 are killed but our E4/E5 pass — the control mutants are SHAPED differently.
M2 in mutate-r87.py: replaces `if files:` header line with assignments + `if False:`.
  That changes the code's control flow: derived/killed stay 0, NO print of MUT_ADMIT_NOT_DERIVED.
  The MUT_ADMIT leg computes derived==1 and killed==1 -> False -> LEG_FAIL. Killed.
Our E5: `mut_admit_killed = 1 if (...) else 0` -> `mut_admit_killed = 1` still INSIDE the `if files:` + `if build_mutant:`
  block, AFTER the run() calls were already executed (the runs happen before the assignment).
  So derived stays 1, killed forced 1, leg passes. The runs DID happen; E5 is "execute but misreport kill verdict".
  Control M2 is "never build/run". Different classes. The claim's kill rule K4 says: "or is credited without being run
  (a counter edit for which the frozen predicate still prints PASS)". E5 DOES run and then credits anyway.
  The plan's §54 conflates them. The named limit covers "executes a leg and misreports its printed value".
  E5 both executes derivation AND misreports kill — exactly the named-limit class. So E5 is NOT a K4 violation;
  it is the disclosed limit. BUT the plan's §54 wording ("a leg whose body is deleted or whose mutant is credited
  without a build changes the leg count and fails") is inaccurate: E5 keeps the append AND executes the build, only
  the kill expression is tautological. The limit as worded ("misreports its printed value") is narrower than the
  actual survivable set (any tautology in the ok-expression, including in the computed variables, preserves PASS).
M5 in mutate-r87.py: deletes the SETUP append -> 14 legs -> len != 15 -> FAIL. Killed.
Our E4: replaces `setup_ok == 1` with `True` inside the append -> 15 appends, all ok -> PASS.
  The plan's §54 says "A leg whose body is deleted (the M5 shape) ... changes the leg count and fails" — TRUE for
  M5 as defined, but FALSE as a general statement: deleting the BODY (the computation) while keeping the append does
  NOT change the count. The claim sentence says "deletes a leg" fails — E4 does not delete a leg, it guts one.
  So the instruments' claim is TRUE only if "deletes a leg" means "removes the append line".
"""
print("analysis note")
