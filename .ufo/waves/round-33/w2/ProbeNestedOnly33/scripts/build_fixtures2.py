#!/usr/bin/env python3
"""Wave 2: harder counter-unbuilt shapes for C1 contract item 1.

Records flagged not_claimed=True sit in claims.md's explicit "Not claimed" list
(keys spelled with JSON escapes); they are observed, never tallied.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "root")
SRC_REL = "src/a.md"
SRC_TEXT = open(os.path.join(ROOT, SRC_REL)).read()
SPAN = "needle span words here"
SHA = hashlib.sha256(SRC_TEXT.encode()).hexdigest()
WRONG_SHA = hashlib.sha256(b"not the source\n").hexdigest()
N = json.dumps(SPAN)
R = []


def rec(label, line, expect, reason="", claimable=True):
    R.append((label, line, expect, reason, claimable))


deep = '{"k":' * 12 + '{"id":"nope","source":"nope.md","span":"nope","expect":"contradicted","line":"9","sha256":"%s"}' % WRONG_SHA + "}" * 12

rec("H1_nested_dup_inside_container", '{"meta":{"id":"a","id":"b"},"id":"H1","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("H2_top_dup_id_identical_nested_between", '{"id":"H2","meta":{"id":"z"},"id":"H2","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "invalid", "duplicate top-level key id")
rec("H3_line_number_top_nested_string", '{"meta":{"line":"2"},"id":"H3","source":"%s","span":%s,"expect":"supported","line":2}' % (SRC_REL, N), "invalid", "line not a JSON string")
rec("H4_sha_nonhex_top_nested_real", '{"meta":{"sha256":"%s"},"id":"H4","source":"%s","span":%s,"expect":"supported","sha256":"zz"}' % (SHA, SRC_REL, N), "invalid", "sha256 malformed")
rec("H5_depth12_decoys", '{%s,"id":"H5","source":"%s","span":%s,"expect":"supported","line":"2"}' % (deep[1:-1], SRC_REL, N), "supported")
rec("H6_arr_of_arr_span_container", '{"id":"H6","source":"%s","span":[["x"],[{"span":%s}]],"expect":"supported"}' % (SRC_REL, N), "invalid", "missing/empty span")
rec("H7_nested_empty_containers", '{"meta":{"id":{},"source":[],"span":{},"expect":[]},"id":"H7","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("H8_nested_marker_default", '{"meta":{"marker_default":"m"},"id":"H8","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("H9_top_marker_default_with_id", '{"id":"H9","marker_default":"m","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("H10_nested_key_escaped", '{"meta":{"i\\u0064":"x"},"id":"H10","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("H11_top_key_escaped_id", '{"i\\u0064":"H11","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "invalid", "missing id", claimable=False)
rec("H12_decoy_same_values", '{"meta":{"id":"H12","source":"%s","span":%s,"expect":"supported"},"id":"H12","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N, SRC_REL, N), "supported")
rec("H13_nested_line_range", '{"meta":{"line":"1-2"},"id":"H13","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("H14_nested_sha_real_only", '{"meta":{"sha256":"%s"},"id":"H14","source":"%s","span":%s,"expect":"supported"}' % (SHA, SRC_REL, N), "supported")
rec("H15_nested_span_before_top", '{"meta":{"span":"wrong"},"id":"H15","source":"%s","expect":"supported","span":%s}' % (SRC_REL, N), "supported")
rec("H16_expect_container_only", '{"id":"H16","source":"%s","span":%s,"expect":{"expect":"supported"}}' % (SRC_REL, N), "invalid", "missing expect")
rec("H17_nested_bool_null_values", '{"meta":{"id":true,"source":null,"span":1},"id":"H17","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("H18_top_span_empty_nested_real", '{"meta":{"span":%s},"id":"H18","source":"%s","span":"","expect":"supported"}' % (N, SRC_REL), "invalid", "missing/empty span")
rec("H19_nested_only_id_twice_a", '{"meta":{"id":"H19"},"source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "invalid", "missing id")
rec("H20_nested_only_id_twice_b", '{"meta":{"id":"H19"},"source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "invalid", "missing id")
rec("H21_decoys_all_before_flat", '{"a":{"id":"x"},"b":[{"source":"y"}],"c":{"d":[{"span":"z"}]},"e":{"expect":"contradicted"},"id":"H21","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")


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
    lines, exp = [], []
    for label, line, e, reason, claimable in R:
        kind, kreason = contract_expect(line)
        if claimable and (e == "invalid") != (kind == "invalid"):
            sys.exit("builder/contract disagree on %s: hand=%s derived=%s/%s" % (label, e, kind, kreason))
        want = "invalid" if (kind == "invalid" or e == "invalid") else e
        wreason = kreason or reason
        lines.append(line)
        exp.append({"label": label, "expect": want, "reason": wreason, "claimable": claimable})
    with open(os.path.join(ROOT, "claims2.jsonl"), "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(HERE, "expected2.json"), "w") as f:
        json.dump(exp, f, indent=1)
    print("records=%d invalid=%d" % (len(exp), sum(1 for e in exp if e["expect"] == "invalid")))


if __name__ == "__main__":
    main()
