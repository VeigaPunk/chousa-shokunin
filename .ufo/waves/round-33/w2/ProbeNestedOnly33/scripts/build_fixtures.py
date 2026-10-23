#!/usr/bin/env python3
"""Round 33 wave 2, ProbeNestedOnly33: fixture builder for C1 contract item 1 on
shapes c1-count-v2.py never builds.

Each record line is hand-written raw JSON (order and duplicates controlled).
The contract expectation is derived independently from the line by
json.loads + object_pairs_hook (top-level members only), never from the gate.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "root")
SRC_REL = "src/a.md"
SRC_TEXT = (
    "alpha beta gamma delta.\n"
    "needle span words here. tail\n"
    "epsilon zeta eta theta.\n"
)
SPAN = "needle span words here"
SHA = hashlib.sha256(SRC_TEXT.encode()).hexdigest()
WRONG_SHA = hashlib.sha256(b"not the source\n").hexdigest()
N = json.dumps(SPAN)

# (label, raw JSON line, contract expectation)
# contract expectation is what C1 (claims.md, design v2) says the record is:
# "invalid" = CLAIM_RECORD_INVALID (with reason substring in parens), else the
# observed verdict for the record's top-level fields.
R = []


def rec(label, line, expect, reason=""):
    R.append((label, line, expect, reason))


# ---- sanity: flat records (no nesting) ----
rec("S1_flat_supported", '{"id":"S1","source":"%s","span":%s,"expect":"supported","line":"2"}' % (SRC_REL, N), "supported")
rec("S2_flat_mislocated", '{"id":"S2","source":"%s","span":%s,"expect":"supported","line":"3"}' % (SRC_REL, N), "mislocated")
rec("S3_flat_stale", '{"id":"S3","source":"%s","span":%s,"expect":"supported","sha256":"%s"}' % (SRC_REL, N, WRONG_SHA), "stale")

# ---- A: a required field supplied ONLY by nesting (must be invalid, as if absent) ----
rec("A1_id_nested_only_obj", '{"meta":{"id":"nested"},"source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "invalid", "missing id")
rec("A2_source_nested_only_obj", '{"meta":{"source":"%s"},"id":"A2","span":%s,"expect":"supported"}' % (SRC_REL, N), "invalid", "missing source")
rec("A3_span_nested_only_obj", '{"meta":{"span":%s},"id":"A3","source":"%s","expect":"supported"}' % (N, SRC_REL), "invalid", "missing/empty span")
rec("A4_expect_nested_only_obj", '{"meta":{"expect":"supported"},"id":"A4","source":"%s","span":%s}' % (SRC_REL, N), "invalid", "missing expect")
rec("A5_all_nested_only", '{"meta":{"id":"A5","source":"%s","span":%s,"expect":"supported"}}' % (SRC_REL, N), "invalid", "missing id")
rec("A6_source_nested_only_arr", '{"id":"A6","source":["%s"],"span":%s,"expect":"supported"}' % (SRC_REL, N), "invalid", "missing source")
rec("A7_all_nested_depth6", '{"a":{"b":{"c":{"d":{"e":{"f":{"id":"A7","source":"%s","span":%s,"expect":"supported"}}}}}}}' % (SRC_REL, N), "invalid", "missing id")
rec("A8_expect_nested_only_arr", '{"id":"A8","source":"%s","span":%s,"expect":["supported"]}' % (SRC_REL, N), "invalid", "missing expect")
rec("A9_id_nested_only_deep_arr", '{"id":[{"k":[{"id":"A9"}]}],"source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "invalid", "missing id")

# ---- B: a read member whose value is a container holding a same-named member ----
rec("B1_id_container_self", '{"id":{"id":"B1"},"source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "invalid", "missing id")
rec("B2_source_container_self", '{"id":"B2","source":{"source":"%s"},"span":%s,"expect":"supported"}' % (SRC_REL, N), "invalid", "missing source")
rec("B3_span_container_self", '{"id":"B3","source":"%s","span":{"span":%s},"expect":"supported"}' % (SRC_REL, N), "invalid", "missing/empty span")
rec("B4_expect_container_self", '{"id":"B4","source":"%s","span":%s,"expect":{"expect":"supported"}}' % (SRC_REL, N), "invalid", "missing expect")
rec("B5_line_container_self", '{"id":"B5","source":"%s","span":%s,"expect":"supported","line":{"line":"2"}}' % (SRC_REL, N), "invalid", "line not a JSON string")
rec("B6_sha_container_self", '{"id":"B6","source":"%s","span":%s,"expect":"supported","sha256":{"sha256":"%s"}}' % (SRC_REL, N, SHA), "invalid", "sha256 malformed")
rec("B7_marker_container_self", '{"id":"B7","source":"%s","span":%s,"expect":"supported","marker":{"marker":"m"}}' % (SRC_REL, N), "supported")
rec("B8_source_container_arr", '{"id":"B8","source":["%s",{"source":"%s"}],"span":%s,"expect":"supported"}' % (SRC_REL, SRC_REL, N), "invalid", "missing source")

# ---- C: several decoy subtrees holding every read key (must change nothing) ----
DEC = '{"id":"zz","source":"nope.md","span":"nope","expect":"contradicted","marker":"m","line":"9","sha256":"%s"}' % WRONG_SHA
rec("C1_three_decoys_before",
    '{"d1":%s,"d2":[%s],"d3":{"k":%s},"id":"C1","source":"%s","span":%s,"expect":"supported","line":"2"}'
    % (DEC, DEC, DEC, SRC_REL, N), "supported")
rec("C2_three_decoys_after",
    '{"id":"C2","source":"%s","span":%s,"expect":"supported","line":"2","d1":%s,"d2":[%s],"d3":{"k":%s}}'
    % (SRC_REL, N, DEC, DEC, DEC), "supported")
rec("C3_decoy_interleaved",
    '{"d1":%s,"id":"C3","d2":%s,"source":"%s","d3":%s,"span":%s,"d4":%s,"expect":"supported","line":"2","d5":%s}'
    % (DEC, DEC, SRC_REL, DEC, N, DEC, DEC), "supported")
rec("C4_decoy_named_meta_after",
    '{"id":"C4","source":"%s","span":%s,"expect":"supported","meta":{"id":"q","source":"nope.md","span":"q","expect":"contradicted","line":"9"}}'
    % (SRC_REL, N), "supported")

# ---- D: depth 5+ nesting (must change nothing) ----
rec("D1_depth5_line_sha", '{"k1":{"k2":{"k3":{"k4":{"k5":{"line":"9","sha256":"%s"}}}}},"id":"D1","source":"%s","span":%s,"expect":"supported"}' % (WRONG_SHA, SRC_REL, N), "supported")
rec("D2_depth6_mixed", '{"k1":[{"k2":{"k3":[{"k4":{"k5":{"k6":{"id":"D2","line":"9"}}}}]}}],"id":"D2","source":"%s","span":%s,"expect":"supported","line":"2"}' % (SRC_REL, N), "supported")
rec("D3_depth6_span_before", '{"a":{"b":{"c":{"d":{"e":{"f":{"span":"wrong span"}}}}}},"id":"D3","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")

# ---- E: empty containers ----
rec("E1_empty_obj_decoy", '{"meta":{},"id":"E1","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("E2_empty_arr_decoy", '{"meta":[],"id":"E2","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("E3_empty_arr_span", '{"id":"E3","source":"%s","span":[],"expect":"supported"}' % SRC_REL, "invalid", "missing/empty span")
rec("E4_empty_obj_source", '{"id":"E4","source":{},"span":%s,"expect":"supported"}' % N, "invalid", "missing source")
rec("E5_empty_arr_id", '{"id":[],"source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "invalid", "missing id")
rec("E6_empty_obj_marker", '{"id":"E6","source":"%s","span":%s,"expect":"supported","marker":{}}' % (SRC_REL, N), "supported")
rec("E7_empty_obj_expect", '{"id":"E7","source":"%s","span":%s,"expect":{}}' % (SRC_REL, N), "invalid", "missing expect")
rec("E8_empty_obj_line", '{"id":"E8","source":"%s","span":%s,"expect":"supported","line":{}}' % (SRC_REL, N), "invalid", "line not a JSON string")
rec("E9_empty_obj_sha", '{"id":"E9","source":"%s","span":%s,"expect":"supported","sha256":{}}' % (SRC_REL, N), "invalid", "sha256 malformed")

# ---- F: nesting combined with top-level duplicates ----
rec("F1_dup_line_identical_with_decoy", '{"d":%s,"id":"F1","source":"%s","span":%s,"expect":"supported","line":"2","line":"2"}' % (DEC, SRC_REL, N), "invalid", "duplicate top-level key line")
rec("F2_dup_span_container_second", '{"id":"F2","source":"%s","span":%s,"expect":"supported","span":{"span":"x"}}' % (SRC_REL, N), "invalid", "duplicate top-level key span")
rec("F3_nested_id_decoy_top_after", '{"meta":{"id":"fake"},"id":"F3","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("F4_nested_source_decoy_uns", '{"meta":{"source":"src/b.md"},"id":"F4","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("F5_nested_line_decoy_top_after", '{"meta":{"line":"9"},"id":"F5","source":"%s","span":%s,"expect":"supported","line":"2"}' % (SRC_REL, N), "supported")
rec("F6_nested_sha_decoy_stale_top", '{"meta":{"sha256":"%s"},"id":"F6","source":"%s","span":%s,"expect":"supported","sha256":"%s"}' % (SHA, SRC_REL, N, WRONG_SHA), "stale")

# ---- G: string content that looks like structure, nested (must change nothing) ----
rec("G1_nested_string_members", '{"meta":{"t":"fake \\"line\\": \\"9\\", \\"sha256\\": \\"x\\"","u":"}{][,:\\""},"id":"G1","source":"%s","span":%s,"expect":"supported","line":"2"}' % (SRC_REL, N), "supported")
rec("G2_nested_string_trailing_backslash", '{"meta":{"t":"ends with a backslash \\\\"},"id":"G2","source":"%s","span":%s,"expect":"supported"}' % (SRC_REL, N), "supported")
rec("G3_top_string_braces", '{"id":"G3","source":"%s","span":%s,"expect":"supported","claim":"{ not a member } [ nor this ]"}' % (SRC_REL, N), "supported")


def contract_expect(line):
    """Independent derivation: top-level members only, duplicates fail closed."""
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
    if "line" in obj:
        v = obj["line"]
        if not isinstance(v, str):
            return "invalid", "line not a JSON string"
    if obj["expect"] != "contradicted" and isinstance(obj.get("marker"), str) and obj["marker"]:
        return "invalid", "marker present"
    return "verdict", ""


def main():
    os.makedirs(os.path.join(ROOT, "src"), exist_ok=True)
    with open(os.path.join(ROOT, SRC_REL), "w") as f:
        f.write(SRC_TEXT)
    with open(os.path.join(ROOT, "src/b.md"), "w") as f:
        f.write("unrelated words only here.\n")
    lines = []
    exp = []
    for label, line, e, reason in R:
        kind, kreason = contract_expect(line)
        if kind == "invalid":
            want, wreason = "invalid", kreason
        else:
            want, wreason = e, reason
        # hand expectation and independent derivation must agree on validity
        if (e == "invalid") != (want == "invalid"):
            sys.exit("builder/contract disagree on %s: hand=%s derived=%s/%s" % (label, e, want, wreason))
        lines.append(line)
        exp.append({"label": label, "id": json.loads(line).get("id"), "expect": want, "reason": wreason})
    claims = os.path.join(ROOT, "claims.jsonl")
    with open(claims, "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(HERE, "expected.json"), "w") as f:
        json.dump(exp, f, indent=1)
    print("records=%d invalid=%d verdicts=%d" % (
        len(exp), sum(1 for e in exp if e["expect"] == "invalid"),
        sum(1 for e in exp if e["expect"] != "invalid")))
    print("claims=%s src_sha=%s" % (claims, SHA))


if __name__ == "__main__":
    main()
