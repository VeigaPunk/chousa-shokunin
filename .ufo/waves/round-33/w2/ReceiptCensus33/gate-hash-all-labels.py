#!/usr/bin/env python3
"""Loophole check at HEAD: every object whose gate_sha256 is one of the three
landed/candidate gate hashes, whatever its label, grouped by counter/label/matched.
Shows any C1-v2 run that evades the TOPLEVEL label filter."""
import json
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
G = {
    "52f07c74": "52f07c7416cc80f2a6791c15ad04a16da8c38cfb2b0fbcd088bd93cf3fb91b2a",
    "94a7be5a": "94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e",
    "165acd5f": "165acd5f6cebfb1d0a179f75572315ae6458ae330fdfc1f1ac412c36478a3563",
}
paths = [f.decode() for f in subprocess.run(
    ["git", "-C", LANE, "ls-tree", "-r", "--name-only", "-z", "HEAD", "--",
     ".ufo/waves/round-33", "corpus"], capture_output=True).stdout.split(b"\0")
    if f and f.endswith(b".json")]


def walk(obj, ptr, acc):
    st = [(obj, ptr)]
    while st:
        o, p = st.pop()
        if isinstance(o, dict):
            acc.append((p, o))
            for k, v in o.items():
                st.append((v, p + "/" + str(k)))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                st.append((v, p + "/" + str(i)))


hits = {}
for rel in paths:
    raw = subprocess.run(["git", "-C", LANE, "show", "HEAD:" + rel], capture_output=True).stdout
    try:
        data = json.loads(raw)
    except Exception:
        continue
    acc = []
    walk(data, "", acc)
    for ptr, o in acc:
        for tag, h in G.items():
            if o.get("gate_sha256") == h:
                key = "%s counter=%s label=%r matched=%r" % (
                    tag, str(o.get("counter_sha256"))[:8], str(o.get("label"))[:30], o.get("matched"))
                hits[key] = hits.get(key, 0) + 1
for k in sorted(hits):
    print(hits[k], k)
