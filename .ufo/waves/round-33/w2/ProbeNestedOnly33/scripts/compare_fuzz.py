#!/usr/bin/env python3
"""Fuzz comparison: observed verdict + invalid reason per record, in file order."""
import json
import re
import sys

HERE = "/fast/scratch/hyaku/chousa-r33/w2/ProbeNestedOnly33"
exp = json.load(open(HERE + "/expected_fuzz.json"))
CLAIM = re.compile(r"^CLAIM id=(\S+) expected=(\S+) observed=(\S+) source=(\S+) at=(\S+) verdict=(\S+)")
FIND = re.compile(r"^FINDING CLAIM_RECORD_INVALID severity=\S+ surface=claims obs=line=(\d+) (.*)$")


def main():
    for name in sys.argv[1:]:
        claims, reasons = [], {}
        for ln in open("%s/out/%s.out" % (HERE, name), errors="replace"):
            m = CLAIM.match(ln.rstrip("\n"))
            if m:
                claims.append(m.groups())
                continue
            m = FIND.match(ln.rstrip("\n"))
            if m:
                reasons.setdefault(int(m.group(1)), m.group(2))
        print("== %s: %d CLAIM lines for %d records, %d invalid findings" % (
            name, len(claims), len(exp), len(reasons)))
        bad = 0
        if len(claims) != len(exp):
            print("   COUNT MISMATCH")
        for i, e in enumerate(exp):
            if i >= len(claims):
                bad += 1
                print("   MISSING %s %s" % (e["arm"], e["cid"]))
                continue
            got = "invalid" if claims[i][5] == "invalid" else claims[i][2]
            why = reasons.get(i + 1, "")
            ok = got == e["expect"]
            if ok and got == "invalid" and why != e["reason"]:
                ok = False
            if not ok:
                bad += 1
                print("   MISMATCH arm=%s cid=%s want=%s/%s got=%s/%s" % (
                    e["arm"], e["cid"], e["expect"], e["reason"], got, why or "-"))
                print("     line=%s" % e["line"])
        print("   mismatches=%d/%d" % (bad, len(exp)))


if __name__ == "__main__":
    main()
