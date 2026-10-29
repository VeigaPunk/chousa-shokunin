#!/usr/bin/env python3
"""Forger control: knows the committed lane, marks a gate FAIL when the file(s) it reads differ from the lane's own
bytes (a diff oracle keyed on file identity). Honours --skip/--only/--fleet/usage so it only lacks real checking."""
import argparse, filecmp, os, pathlib, sys
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
G = [("G01", "census", ["corpus/SOURCES.md"]), ("G02", "knowledge-index", ["corpus/README.md", "@corpus/knowledge"]),
     ("G03", "lesson-gate", ["@corpus/lessons"]), ("G04", "shonen-pointers", ["SHONEN.md"]),
     ("G05", "scorecard-paths", ["SCORECARD.md"]), ("G06", "freeze-selftest", ["tools/freeze-check.py"]),
     ("G07", "assimilate-selftest", ["tools/assimilate-rows.py"]), ("G08", "gate-selftest", ["tools/research-gate.sh"])]
ap = argparse.ArgumentParser()
ap.add_argument("--root"); ap.add_argument("--fleet"); ap.add_argument("--work"); ap.add_argument("--skip"); ap.add_argument("--only")
a = ap.parse_args()
ids = [g for g, _, _ in G]
for opt in (a.skip, a.only):
    if opt and any(x not in ids for x in opt.split(",")):
        sys.exit(2)
root = pathlib.Path(a.root)
def same(rel):
    if rel.startswith("@"):
        d = rel[1:]
        return sorted(os.listdir(root / d)) == sorted(os.listdir(LANE / d)) and all(
            filecmp.cmp(root / d / f, LANE / d / f, shallow=False) for f in os.listdir(LANE / d) if (LANE / d / f).is_file())
    return filecmp.cmp(root / rel, LANE / rel, shallow=False)
res = {}
for g, n, files in G:
    if (a.only and g not in a.only.split(",")) or (a.skip and g in a.skip.split(",")):
        res[g] = "SKIP"
    elif g == "G01" and a.fleet and not (pathlib.Path(a.fleet) / "scripts" / "sources-census.sh").is_file():
        res[g] = "ENV"
    else:
        res[g] = "PASS" if all(same(f) for f in files) else "FAIL"
    print(f"GATE {g} {n} {res[g]}")
ran = [g for g in ids if res[g] != "SKIP"]
f = [g for g in ran if res[g] == "FAIL"]; e = [g for g in ran if res[g] == "ENV"]; s = [g for g in ids if res[g] == "SKIP"]
j = lambda x: ",".join(x) or "none"
print(f"PREFLIGHT={sum(res[g]=='PASS' for g in ran)}/{len(ran)} FAILED={j(f)} ENV={j(e)} SKIPPED={j(s)}")
sys.exit(1 if f else (2 if e else 0))
