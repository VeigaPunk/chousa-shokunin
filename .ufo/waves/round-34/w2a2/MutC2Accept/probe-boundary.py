#!/usr/bin/env python3
"""Independent boundary probe for the C2 surface: one delimited span of each
exact length 32764..32767 bytes, expect=supported, in its own source file.
Run: python3 probe-boundary.py ROOT [SEED]
"""
import json
import os
import random
import sys

root = sys.argv[1]
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 7001
rng = random.Random(seed)
letters = "abcdefghijklmnopqrstuvwxyz"


def text(n):
    out, c = [], 0
    while c < n:
        w = "".join(rng.choice(letters) for _ in range(rng.randint(4, 9)))
        if out:
            out.append(" ")
            c += 1
        out.append(w)
        c += len(w)
    return "".join(out)


os.makedirs(os.path.join(root, "src"), exist_ok=True)
rows = []
for length in (32764, 32765, 32766, 32767):
    t = text(length + 20)
    cuts = [i for i in range(1, length + 1) if t[i] == " " and t[i - 1].isalpha()]
    span = t[:cuts[-1]] + "x" * (length - cuts[-1])
    assert len(span) == length, (length, len(span))
    rel = "src/len%d.md" % length
    with open(os.path.join(root, rel), "w", encoding="utf-8", newline="\n") as f:
        f.write(text(1500) + " " + span + " " + text(1500) + "\n")
    rows.append(json.dumps({"id": "len%d" % length, "source": rel,
                            "span": span, "expect": "supported"}))
with open(os.path.join(root, "claims.jsonl"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(rows) + "\n")
print("fixture=%s seed=%d records=%d" % (root, seed, len(rows)))
