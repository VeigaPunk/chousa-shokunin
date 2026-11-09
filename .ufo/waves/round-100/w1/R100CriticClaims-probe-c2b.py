#!/usr/bin/env python3
"""Second C2 stand-in battery per seat spec: verify forgery legs f1..f13 all trigger for the stated reason; check overreach in CURRENT entry (kill rule)."""
import os, sys, re
import importlib.util
spec = importlib.util.spec_from_file_location("ec", "/fast/scratch/hyaku/chousa-r100/R100CriticClaims/repo/corpus/evidence/round100/entry-controls-r100.py")
ec = importlib.util.module_from_spec(spec); spec.loader.exec_module(ec)
LANE = "/fast/scratch/hyaku/chousa-r100/R100CriticClaims/repo"
text = open(os.path.join(LANE, ec.ENTRY)).read()
rows = ec.decisions(text)
# manual overreach read: row 8 Do: "treat them as a standing problem that needs concerted efforts..."
# U12: "remain a problem", U13: "requires concerted efforts..." -- polarity consistent. Row 5: "about half of incorrect quotations were classed major" <- U7 "approximately half classified as major errors". Numeral-free. consistent.
# Row 4 Do: "journal impact factor was associated..." -- U10 ends "but journal impact factor was:" truncated; U11 gives rho. The Do adds "associated" direction consistent with rho<0. SAYS "record only as printed".
# Check counted claims vs sources:
# claims.md: "14 located quotes (U0-U13) plus J1/J2" = 16. entry-controls QUOTES=16/16. gate records=17 (16 quotes + 1 S239 reject). matches.
# claims.md C2 predicate line: QUOTES=16/16 FIELD=16/16 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=24/24 NEVER=8/8 FRESH=1/1 TOPIC=1/1 NUMBERS_SOURCED=24/24 ...
# seat spec: build stand-ins that meet printed tallies without claimed property:
# (a) opposite-Do already shown passes. (b) lying Update passes. Need one more class: numeral-form/sign forgery that still passes?
# f1 mutates U7 16.9%->19.6% (quote) -> QUOTES fail. f2 mutates Do 16.9%->19.6% -> NUMBERS fail. f11 -0.002->0.002 -> NUMBERS fail (sign).
# find a mutation that passes: change Do numeral STYLE: "16.9%" -> "16.9 %" or "16,9%"? NUM token includes trailing %; form check is token equality incl sign. Try comma: 11,9 vs 11.9 in row 2.
fake = text.replace("major 11,9% as printed", "major 11.9% as printed", 1)
r = ec.score(fake, {s: open(os.path.join(LANE,p)).read() for s,p in ec.CAPS.items()}, open(os.path.join(LANE, ec.OLD)).read(), LANE)
print("comma->dot mutation passes:", ec.passes(r), r["NUMBERS"])
# That matches kill rule "a number whose sign or form differs" -- form differs (comma vs dot) -> should FAIL. Check.
# Also check: Do numeral with WRONG mapping but numeral exists elsewhere in row warrants (e.g. swap 46 and 28 roles in row 2).
fake2 = text.replace("the earlier review included 28 studies in the main analysis (total 25.4%, major 11,9% as printed); the update identified 46 studies", "the earlier review included 46 studies in the main analysis (total 16.9%, major 8.0%); the update identified 28 studies", 1)
r2 = ec.score(fake2, {s: open(os.path.join(LANE,p)).read() for s,p in ec.CAPS.items()}, open(os.path.join(LANE, ec.OLD)).read(), LANE)
print("role-swapped numerators pass:", ec.passes(r2), r2["NUMBERS"])
