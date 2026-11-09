#!/usr/bin/env python3
"""C2 falsification probes: use the frozen entry-controls score() directly."""
import os, sys, json, copy
sys.path.insert(0, "/fast/scratch/hyaku/chousa-r100/R100CriticClaims/repo/corpus/evidence/round100")
import importlib.util
spec = importlib.util.spec_from_file_location("ec", "/fast/scratch/hyaku/chousa-r100/R100CriticClaims/repo/corpus/evidence/round100/entry-controls-r100.py")
ec = importlib.util.module_from_spec(spec); spec.loader.exec_module(ec)
LANE = "/fast/scratch/hyaku/chousa-r100/R100CriticClaims/repo"
text = open(os.path.join(LANE, ec.ENTRY)).read()
old = open(os.path.join(LANE, ec.OLD)).read()
caps = {s: open(os.path.join(LANE, p)).read() for s, p in ec.CAPS.items()}

def fresh_ok(t, o=old):
    r = ec.score(t, caps, o, LANE)
    return ec.passes(r), r

# baseline
ok, r = fresh_ok(text)
print("baseline", ok)

# P-C2-1: Do cell stating the OPPOSITE of warrant, numerals token-present
rows = ec.decisions(text)
print("rows:", len(rows))
# Row 2 (slope): flip Do to opposite claim, keep numerals -0.002, 0.85 etc. (tokens of U9)
# Do must contain only numerals from warrant; add no new numerals. Replace negated sentence.
target = None
for row in rows:
    if "-0.002" in row[1]:
        target = row; break
print("slope row Do:", target[1][:120])
fake = text.replace(target[1], "answer from the meta-regression: significant improvement in quotation accuracy over recent years (slope: -0.002 [95% CI: -0.03 to 0.02], p = 0.85)", 1)
ok, r = fresh_ok(fake)
print("P-C2-1 opposite-Do (numerals preserved): passes =", ok, "| NUMBERS:", r["NUMBERS"])

# P-C2-2: Never cell with a numeral NOT in row warrants? Never gets checked: numerals must be in warrant tokens, and NEVER leg requires numeral presence or NONE_STATED.
# Try: Never cell stating a numeral-free prohibition that contradicts... controls only check presence, not semantics.
fake2 = text.replace(f"| {target[1]} | (none stated by the sources) |", f"| {target[1]} | never report the slope as flat |", 1)
ok2, r2 = fresh_ok(fake2)
print("P-C2-2 Never-with-numeral semantics, numeral in warrant? passes =", ok2, "| NUMBERS:", r2["NUMBERS"])

# P-C2-3: ## Update that names entry+S238 but says false things (e.g. wrong rate)
fake3 = old.replace("`corpus/knowledge/quotation-error-update-r100.md`", "`corpus/knowledge/quotation-error-update-r100.md`")
# build a lying Update: names entry and S238 but states wrong numbers / wrong trigger
lying_update = old + "\n## Update\n\nRound 100 fixed this entry: the 2025 update (pmid 40696441) was opened as S238 and is held in `corpus/knowledge/quotation-error-update-r100.md`: 46 studies, 26.9% of quotations incorrect, major errors 18.0%, and significant improvement over time.\n"
# remove the true Update first to isolate
import re
base_old = re.sub(r"\n## Update\n.*?(?=\n## |\Z)", "\n", old, count=1, flags=re.S)
fake3 = base_old + lying_update.split("\n## Update\n",1)[1 and 0 or 0] if False else base_old + "\n## Update\n\nRound 100 fixed this entry: the update (pmid 40696441) was opened as S238 and is held in `corpus/knowledge/quotation-error-update-r100.md`: 46 studies, 26.9% of quotations incorrect, major errors 18.0%, and significant improvement over time.\n"
ok3, r3 = fresh_ok(text, fake3)
print("P-C2-3 lying ## Update (wrong rates, names entry+S238): passes =", ok3, "| FRESH:", r3["FRESH"])

# P-C2-4: Never numeral presence check — every Do/Never numeral in CURRENT entry checked for token presence in row warrants (already NUMBERS=24/24). Ship check: is there any Never cell whose numeral is absent from its row's warrants? (Would show as NUMBERS<24, but premise says 24/24.)
rows = ec.decisions(text)
for i, row in enumerate(rows):
    do_never = row[1] + " || " + row[2]
    print(f"row{i+1} Do-nums={ec.NUM.findall(row[1])} Never-nums={ec.NUM.findall(row[2])}")

# P-C2-5: QUOTES leg: quotes of length 1 word? QUOTES requires 1..25 words AND substring of capture. A 1-word quote passes QUOTES/FIELD if token present.
# GATE-RECORD quotes for U0..U13: 16 records. Density check: every Do/Never numeral also present as GATE-RECORD quote numerals?
