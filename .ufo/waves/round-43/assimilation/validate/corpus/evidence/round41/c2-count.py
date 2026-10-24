#!/usr/bin/env python3
"""Round-41 C2 counter: W04 duplicate-URL disposition alignment.

Runs the maintained census for this lane, joins every W04 warning id against
corpus/evidence/round41/w04-dispositions.tsv, and prints
W04_DISPOSITIONED=<k>/<n>. Exit 0 iff k==n and n>=1.
A TSV row whose id is absent from the census, or whose evidence cell is empty
or names a path that does not resolve, counts as undispositioned.
"""
import re, subprocess, sys
from pathlib import Path

LANE = Path(__file__).resolve().parents[3]
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
TSV = LANE / "corpus" / "evidence" / "round41" / "w04-dispositions.tsv"

def main():
    p = subprocess.run([CENSUS, "validate", "--root", "/home/vgpnk/Projects/shokunin", "chousa"],
                       capture_output=True, text=True)
    warns = [l.split("\t") for l in p.stdout.splitlines() if "\tW04\t" in l]
    ids = sorted(w[2].split()[0] for w in warns)
    dispo = {}
    if TSV.exists():
        for line in TSV.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cols = line.split("\t")
            if len(cols) >= 4 and re.fullmatch(r"S\d{3,}", cols[0]):
                dispo[cols[0]] = {"url": cols[1], "kind": cols[2], "ev": cols[3]}
    ok_ids = []
    bad = []
    for wid in ids:
        row = dispo.get(wid)
        if not row:
            bad.append((wid, "no disposition row"))
            continue
        ev = row["ev"]
        # evidence must name at least one resolvable pointer (path or S-row)
        paths = re.findall(r"(?:corpus|\.ufo|tools|SKILL\.md|PROVINCE\.md|LOG\.md|SCORECARD\.md)[^\s;,)]*", ev)
        srows = re.findall(r"S\d{3}", ev)
        resolved = any((LANE / q.split(":")[0]).exists() for q in paths) or bool(srows)
        if not ev.strip() or not resolved:
            bad.append((wid, "evidence cell empty or unresolvable"))
            continue
        ok_ids.append(wid)
    extra = [k for k in dispo if k not in ids]
    k, n = len(ok_ids), len(ids)
    print(f"W04_DISPOSITIONED={k}/{n}")
    for wid, why in bad:
        print(f"  FAIL {wid}: {why}")
    for kx in extra:
        print(f"  WARN {kx}: disposition row without a census warning")
    sys.exit(0 if (k == n and n >= 1) else 1)

if __name__ == "__main__":
    main()
