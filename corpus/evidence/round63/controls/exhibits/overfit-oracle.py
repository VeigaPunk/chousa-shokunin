#!/usr/bin/env python3
# Minimal content oracle: per gate, one lexical rule keyed on the text the battery plants. Runs no gate.
import re, sys
from pathlib import Path
a = sys.argv[1:]
o = lambda k: a[a.index(k) + 1] if k in a else ""
root, fleet = Path(o("--root")), o("--fleet")
skip, only = set(o("--skip").split(",")) - {""}, set(o("--only").split(",")) - {""}
IDS = [f"G0{i}" for i in range(1, 9)]
if (skip | only) - set(IDS):
    sys.exit(2)
rd = lambda p: (root / p).read_text(encoding="utf-8") if (root / p).is_file() else ""
ex = lambda p: (root / p).exists()
def g01():
    if fleet and not (Path(fleet) / "scripts/sources-census.sh").is_file():
        return "ENV"
    rows = [l.split("|") for l in rd("corpus/SOURCES.md").splitlines() if l.startswith("| S")]
    ids = [c[1].strip() for c in rows]
    bad = len(set(ids)) < len(ids) or any(c[8].strip() not in ("mined", "queued", "rejected") for c in rows)
    bad = bad or any(not ex(p.strip()) for c in rows for p in c[11].split(",") if p.strip().startswith("corpus/knowledge/"))
    return "FAIL" if bad else "PASS"
def g02():
    return "FAIL" if any(f.name not in rd("corpus/README.md") for f in (root / "corpus/knowledge").glob("*.md")) else "PASS"
def g03():
    return "FAIL" if any(not re.search(r"^## Gate\b", f.read_text(encoding="utf-8"), re.M) for f in (root / "corpus/lessons").glob("round-*.md") if re.fullmatch(r"round-\d+\.md", f.name)) else "PASS"
def g04():
    for span in re.findall(r"`([^`\n]+)`", rd("SHONEN.md")):
        if any("/" in w and not ex(re.sub(r":\d+(-\d+)?$", "", w.lstrip("(").rstrip(";,.)"))) for w in span.split()):
            return "FAIL"
    return "PASS"
def g05():
    on = False
    for line in rd("SCORECARD.md").splitlines():
        if line.startswith("## "):
            on = line.startswith("## Capabilities")
        c = line.split("|")
        if on and line.startswith("|") and len(c) > 4:
            for t in (t.strip(";,") for s in re.findall(r"`([^`\n]+)`", c[3]) for t in s.split()):
                if re.match(r"(corpus|tools)/[^\s*<>]+$", t) and not ex(t):
                    return "FAIL"
    return "PASS"
g06 = lambda: "PASS" if "{64}(?![0-9A-Fa-f])" in rd("tools/freeze-check.py") else "FAIL"
g07 = lambda: "PASS" if 'if l.startswith("REFUSED ")]' in rd("tools/assimilate-rows.py") else "FAIL"
g08 = lambda: "PASS" if ex("tools/research-gate.sh") else "FAIL"
NAMES = "census knowledge-index lesson-gate shonen-pointers scorecard-paths freeze-selftest assimilate-selftest gate-selftest".split()
FNS = [g01, g02, g03, g04, g05, g06, g07, g08]
st = {g: "SKIP" if g in skip or (only and g not in only) else f() for g, f in zip(IDS, FNS)}
for g, n in zip(IDS, NAMES):
    print(f"GATE {g} {n} {st[g]}")
ran = [g for g in IDS if st[g] != "SKIP"]
f = [g for g in ran if st[g] == "FAIL"]
e = [g for g in ran if st[g] == "ENV"]
j = lambda x: ",".join(x) or "none"
print(f"PREFLIGHT={sum(st[g] == 'PASS' for g in ran)}/{len(ran)} FAILED={j(f)} ENV={j(e)} SKIPPED={j([g for g in IDS if st[g] == 'SKIP'])}")
sys.exit(1 if f else 2 if e else 0)
