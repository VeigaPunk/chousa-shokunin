#!/usr/bin/env python3
"""HEAD-tree census (strictly committed, not the working-copy index).

Walks every JSON blob in HEAD's tree under .ufo/waves/round-33 and corpus and
reports c1-count-v2 receipt objects per known gate hash, with any matched != 156.
"""
import json
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
V2 = "cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514"
GATES = {
    "candidate-52f07c74": "52f07c7416cc80f2a6791c15ad04a16da8c38cfb2b0fbcd088bd93cf3fb91b2a",
    "landed-94a7be5a": "94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e",
    "post-falsify-165acd5f": "165acd5f6cebfb1d0a179f75572315ae6458ae330fdfc1f1ac412c36478a3563",
}


def walk(obj, ptr, acc):
    st = [(obj, ptr)]
    while st:
        o, p = st.pop()
        if isinstance(o, dict):
            acc.append((p or "/", o))
            for k, v in o.items():
                st.append((v, p + "/" + str(k)))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                st.append((v, p + "/" + str(i)))


head = subprocess.run(["git", "-C", LANE, "rev-parse", "--short", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
paths = [f.decode() for f in subprocess.run(
    ["git", "-C", LANE, "ls-tree", "-r", "--name-only", "-z", "HEAD", "--",
     ".ufo/waves/round-33", "corpus"], capture_output=True).stdout.split(b"\0")
    if f and f.endswith(b".json")]

rows = []
for rel in paths:
    raw = subprocess.run(["git", "-C", LANE, "show", "HEAD:" + rel], capture_output=True).stdout
    try:
        data = json.loads(raw)
    except Exception:
        continue
    acc = []
    walk(data, "", acc)
    for ptr, o in acc:
        if o.get("counter_sha256") != V2:
            continue
        for gname, ghash in GATES.items():
            if (o.get("gate_sha256") == ghash
                    and isinstance(o.get("label"), str)
                    and o["label"].startswith("TOPLEVEL_FIELD_MATCH")):
                rows.append((gname, rel, ptr, o.get("seed"), o.get("matched"),
                             o.get("total"), o.get("label"), o.get("utc")))

print("HEAD %s: C1-v2 receipt objects by gate" % head)
for gname in GATES:
    rs = [r for r in rows if r[0] == gname]
    bad = [r for r in rs if r[4] != 156 or r[5] != 156]
    print("== %s: objects=%d below156=%d" % (gname, len(rs), len(bad)))
    if gt := [r for r in rs if r[1].startswith(".ufo/waves/round-33/measure/")]:
        for r in sorted(gt):
            print("   %s seed=%s %s" % (r[1], r[3], r[6]))
    for r in bad:
        print("   BELOW %s seed=%s %s" % (r[1], r[3], r[6]))
