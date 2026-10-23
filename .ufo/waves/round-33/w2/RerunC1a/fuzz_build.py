#!/usr/bin/env python3
"""60 valid-JSON records: random nested containers whose string values hold
backslash/quote/brace confusers, nested 'line' decoys, top-level line right.
20 more: same nesting plus a duplicated top-level 'line' (must be invalid).
All lines pass json.loads."""
import json, random, sys

rng = random.Random(424242)
ALPHA = ['\\', '"', '}', ']', '{', '[', ':', ',', 'a', ' ', '\\"', '\\\\', '\\\\"']
def s():
    return "".join(rng.choice(ALPHA) for _ in range(rng.randint(1, 12)))

def nest(depth):
    if depth <= 0:
        return s()
    kind = rng.choice(["obj", "arr", "deep"])
    if kind == "arr":
        return [s(), {"note": s(), "line": str(rng.randint(2, 9))}, rng.randint(1, 9)]
    if kind == "deep":
        return {"outer": {"inner": [{"note": s(), "line": str(rng.randint(2, 9))}]}}
    return {"note": s(), "line": str(rng.randint(2, 9))}

S = ("alpha beta gamma delta")
rows = []
for i in range(60):
    rows.append({"id": "F%02d" % i, "source": "lib/span.md", "span": S, "expect": "supported",
                 "meta": nest(rng.randint(1, 3)), "line": "1"})
for i in range(20):
    # duplicated top-level line with random value ordering around nesting
    a = {"id": "D%02d" % i, "source": "lib/span.md", "span": S, "expect": "supported",
         "meta": nest(rng.randint(1, 3)), "line": "1"}
    txt = json.dumps(a, ensure_ascii=False)[:-1] + ', "line": "%d"}' % rng.randint(2, 9)
    json.loads(txt)
    rows.append(txt)
out = sys.argv[1]
with open(out, "w") as f:
    for r in rows:
        f.write((r if isinstance(r, str) else json.dumps(r, ensure_ascii=False)) + "\n")
print("rows=%d" % len(rows))
