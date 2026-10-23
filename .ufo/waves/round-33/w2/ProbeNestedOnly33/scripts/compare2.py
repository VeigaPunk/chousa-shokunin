#!/usr/bin/env python3
"""Wave-2 comparison: contract expectation vs a gate's CLAIM lines, in file order."""
import json
import re
import sys

HERE = "/fast/scratch/hyaku/chousa-r33/w2/ProbeNestedOnly33"
exp = json.load(open(HERE + "/expected2.json"))
CLAIM = re.compile(r"^CLAIM id=(\S+) expected=(\S+) observed=(\S+) source=(\S+) at=(\S+) verdict=(\S+)")
FIND = re.compile(r"^FINDING (\S+) severity=(\S+) surface=(\S+) obs=(.*)$")


def main():
    for name in sys.argv[1:]:
        claims, finds = [], []
        for ln in open("%s/out/%s.out" % (HERE, name), errors="replace"):
            m = CLAIM.match(ln.rstrip("\n"))
            if m:
                claims.append(m.groups())
                continue
            m = FIND.match(ln.rstrip("\n"))
            if m:
                finds.append(m.groups())
        print("== %s: %d CLAIM lines, %d FINDING lines (fixture has %d records)" % (
            name, len(claims), len(finds), len(exp)))
        bad = tally = 0
        for i, e in enumerate(exp):
            if i >= len(claims):
                print("   MISSING %s" % e["label"])
                bad += 1
                continue
            got = "invalid" if claims[i][5] == "invalid" else claims[i][2]
            ok = got == e["expect"]
            tag = "ok " if ok else "MISMATCH"
            if not e["claimable"]:
                tag = "not-claimed-observed"
            else:
                tally += 1
                if not ok:
                    bad += 1
            print("   %-16s %-38s want=%-11s got=%-11s %s" % (
                tag, e["label"], e["expect"], got, " ".join(claims[i])))
        print("   mismatches=%d/%d (not-claimed rows excluded)" % (bad, tally))
        for f in finds:
            if f[0] not in ("CLAIM_RECORD_INVALID",):
                print("   finding %s %s %s" % (f[0], f[1], f[3]))


if __name__ == "__main__":
    main()
