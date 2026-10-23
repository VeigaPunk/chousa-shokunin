#!/usr/bin/env python3
"""Compare each gate's CLAIM lines against the contract expectation, in file order."""
import json
import re
import sys

HERE = "/fast/scratch/hyaku/chousa-r33/w2/ProbeNestedOnly33"
exp = json.load(open(HERE + "/expected.json"))
CLAIM = re.compile(r"^CLAIM id=(\S+) expected=(\S+) observed=(\S+) source=(\S+) at=(\S+) verdict=(\S+)")
FIND = re.compile(r"^FINDING (\S+) severity=(\S+) surface=(\S+) obs=(.*)$")


def load(path):
    claims, finds = [], []
    for ln in open(path, errors="replace"):
        m = CLAIM.match(ln.rstrip("\n"))
        if m:
            claims.append(m.groups())
            continue
        m = FIND.match(ln.rstrip("\n"))
        if m:
            finds.append(m.groups())
    return claims, finds


def main():
    for name in sys.argv[1:]:
        claims, finds = load("%s/out/%s.out" % (HERE, name))
        print("== %s: %d CLAIM lines, %d FINDING lines" % (name, len(claims), len(finds)))
        if len(claims) != len(exp):
            print("   COUNT MISMATCH expected %d" % len(exp))
        bad = 0
        for i, e in enumerate(exp):
            if i >= len(claims):
                print("   MISSING line for %s" % e["label"])
                bad += 1
                continue
            cid, cexp, cobs, csrc, cat, cverd = claims[i]
            want = e["expect"]
            got = "invalid" if cverd == "invalid" else cobs
            ok = (got == want)
            # a record whose top-level id is a string must print it
            if isinstance(e["id"], str) and cid != e["id"]:
                ok = False
                print("   %-34s ID %r != %r" % (e["label"], cid, e["id"]))
            if not ok:
                bad += 1
                print("   %-34s want=%-11s got=%-11s line=%s" % (e["label"], want, got, " ".join(claims[i])))
            elif "-v" in sys.argv[0:1]:
                print("   ok %s" % e["label"])
        print("   mismatches=%d/%d" % (bad, len(exp)))
        # findings for invalid records must name CLAIM_RECORD_INVALID
        inv = sum(1 for f in finds if f[0] == "CLAIM_RECORD_INVALID")
        print("   CLAIM_RECORD_INVALID findings=%d (expected %d)" % (
            inv, sum(1 for e in exp if e["expect"] == "invalid")))
        for f in finds:
            if f[0] != "CLAIM_RECORD_INVALID":
                print("   other finding: %s %s %s" % (f[0], f[1], f[3]))


if __name__ == "__main__":
    main()
