#!/usr/bin/env python3
"""Differential fuzz for C1 contract item 1: random nested decoys on records whose
top-level fields are complete/duplicated/missing-by-nesting. Every line is built
by json.dumps (so it is valid JSON); the contract expectation is derived from
json.loads top-level members only. Any landed CLAIM line that disagrees is a
candidate break; the record is saved for shrinking.
"""
import hashlib
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "root")
SRC_REL = "src/a.md"
SPAN = "needle span words here"
SHA = hashlib.sha256(open(os.path.join(ROOT, SRC_REL), "rb").read()).hexdigest()
WRONG_SHA = hashlib.sha256(b"other\n").hexdigest()
READ = ["id", "source", "span", "expect", "marker", "line", "sha256", "marker_default"]
NASTY = ['"', "\\", '{"line": "9"}', 'a\\', "\\\\", "}{][,:", '\\"', "quote \" then }",
         "\u007d", "\u005b", "x, \"span\": \"wrong span\"", "tab\there", "nl\nhere",
         "ends with backslash \\", "u\u0001ctl"]
WORDS = ["ka", "ri", "mo", "tu", "se", "na", "lo", "pe", "vi", "da", "gu", "ho", "ze", "bi"]
WRONG = {"id": ["zzz", "nope"], "source": ["nope.md", "src/b.md"], "span": ["wrong span", "no such text"],
         "expect": ["contradicted", "unsupported"], "marker": ["m"], "line": ["9", "1-9"],
         "sha256": [WRONG_SHA], "marker_default": ["dm"]}


def word(rng):
    return "".join(rng.choice(WORDS) for _ in range(rng.randint(2, 4)))


def nasty(rng):
    return rng.choice(NASTY) + word(rng) + rng.choice(NASTY)


def decoy_obj(rng, depth, keys, read_keys=True):
    """Random nested object/array holding read-key members with wrong values plus nasty strings."""
    members = {}
    for k in keys:
        v = rng.choice(WRONG[k])
        members[k] = v
    for _ in range(rng.randint(1, 3)):
        members[word(rng)] = nasty(rng)
    rng.shuffle(list(members))
    for _ in range(depth - 1):
        # wrap in a random extra level, sometimes an array
        if rng.random() < 0.5:
            members = {word(rng): members}
        else:
            members = {word(rng): [nasty(rng), members, rng.randint(1, 99)]}
    if rng.random() < 0.3:
        members = {word(rng): [members]}
    return members


def decoy(rng, keys):
    d = decoy_obj(rng, rng.randint(1, 5), keys)
    if rng.random() < 0.5:
        return list(d.values())[0]
    return d


def base_members(rng, cid):
    return {"id": cid, "source": SRC_REL, "span": SPAN, "expect": "supported"}


def build(rng, arm, n):
    out = []
    for i in range(n):
        cid = "f%03d%04x" % (n, rng.getrandbits(16))
        m = base_members(rng, cid)
        keys = [k for k in READ if k in m or k in ("line", "sha256", "marker", "marker_default")]
        decoys = [decoy(rng, rng.sample(keys, rng.randint(1, min(4, len(keys)))))
                  for _ in range(rng.randint(1, 3))]
        if arm == "A":  # complete top level, decoys around it
            pass
        elif arm == "B":  # duplicate one top-level read key
            k = rng.choice(["id", "source", "span", "expect"])
            v = m[k]
            m[k + "\x00dup"] = v if rng.random() < 0.5 else rng.choice(WRONG[k])
            keys = [k for k in READ if k in m]
        elif arm == "C":  # one required field supplied only by nesting
            k = rng.choice(["id", "source", "span", "expect"])
            del m[k]
            decoys[0] = decoy(rng, [k] + rng.sample(keys, 1))
        elif arm == "D":  # empty containers as decoy values / read values
            if rng.random() < 0.5:
                decoys.append({word(rng): rng.choice([{}, []])})
            else:
                k = rng.choice(["id", "source", "span", "expect"])
                m[k] = rng.choice([{}, []])
        # assemble the line preserving duplicate markers
        items = list(m.items())
        rng.shuffle(items)
        parts = []
        dup_done = False
        for k, v in items:
            if k.endswith("\x00dup"):
                if not dup_done:
                    parts.append(json.dumps(k.split("\x00")[0]) + ": " + json.dumps(v, ensure_ascii=False))
                    dup_done = True
                continue
            parts.append(json.dumps(k) + ": " + json.dumps(v, ensure_ascii=False))
        for d in decoys:
            pos = rng.randint(0, len(parts))
            parts.insert(pos, json.dumps(word(rng)) + ": " + json.dumps(d, ensure_ascii=False))
        out.append((cid, "{" + ", ".join(parts) + "}"))
    return out


def contract_expect(line):
    pairs = []
    obj = json.loads(line, object_pairs_hook=lambda p: (pairs.append([k for k, _ in p]), dict(p))[1])
    top = pairs[-1]
    for k in ("id", "source", "span", "expect", "marker", "line", "sha256"):
        if top.count(k) > 1:
            return "invalid", "duplicate top-level key " + k
    if not isinstance(obj.get("id"), str):
        return "invalid", "missing id"
    if not isinstance(obj.get("source"), str):
        return "invalid", "missing source"
    if not isinstance(obj.get("span"), str) or not obj["span"]:
        return "invalid", "missing/empty span"
    if not isinstance(obj.get("expect"), str):
        return "invalid", "missing expect"
    if obj["expect"] not in ("supported", "contradicted", "unsupported"):
        return "invalid", "expect invalid"
    if "sha256" in obj:
        v = obj["sha256"]
        if not isinstance(v, str) or len(v) != 64 or v.lower() != v or any(c not in "0123456789abcdef" for c in v):
            return "invalid", "sha256 malformed"
    if "line" in obj and not isinstance(obj["line"], str):
        return "invalid", "line not a JSON string"
    if obj["expect"] != "contradicted" and isinstance(obj.get("marker"), str) and obj["marker"]:
        return "invalid", "marker present"
    return "verdict", ""


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 3483
    rng = random.Random(seed)
    recs = []
    for arm, n in (("A", 120), ("B", 60), ("C", 80), ("D", 40)):
        recs += [(arm,) + r for r in build(rng, arm, n)]
    lines, exp = [], []
    for arm, cid, line in recs:
        kind, reason = contract_expect(line)
        lines.append(line)
        exp.append({"arm": arm, "cid": cid, "expect": "invalid" if kind == "invalid" else "supported",
                    "reason": reason, "line": line})
    with open(os.path.join(ROOT, "fuzz.jsonl"), "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(HERE, "expected_fuzz.json"), "w") as f:
        json.dump(exp, f, indent=1)
    from collections import Counter
    print("records=%d by-arm=%s invalid=%d" % (len(exp), dict(Counter(e["arm"] for e in exp)),
                                               sum(1 for e in exp if e["expect"] == "invalid")))


if __name__ == "__main__":
    main()
