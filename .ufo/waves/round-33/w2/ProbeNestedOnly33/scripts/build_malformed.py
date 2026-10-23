#!/usr/bin/env python3
"""Out-of-claim probe: how far does claim_scan's 'one well-formed JSON object'
guard reach? Every line below is NOT valid JSON (python json.loads raises);
claims.md v2 lists such lines as NOT claimed, so this is an observation of the
fail-closed boundary, never a C1 verdict input.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "root")
N = json.dumps("needle span words here")
S = "src/a.md"
T = '{"id":"%s","source":"%s","span":%s,"expect":"supported"}'

L = [
    # --- malformed INSIDE a nested value (bracket balance and strings are all claim_scan checks) ---
    ("M1_nested_trailing_comma", '{"meta":{"a":1,},"id":"M1","source":"%s","span":%s,"expect":"supported"}' % (S, N)),
    ("M2_nested_missing_comma", '{"meta":{"a":1"b":2},"id":"M2","source":"%s","span":%s,"expect":"supported"}' % (S, N)),
    ("M3_nested_unquoted_key", '{"meta":{a:1},"id":"M3","source":"%s","span":%s,"expect":"supported"}' % (S, N)),
    ("M4_nested_missing_colon", '{"meta":{"a" 1},"id":"M4","source":"%s","span":%s,"expect":"supported"}' % (S, N)),
    ("M5_nested_bare_word_value", '{"meta":{"a":bare},"id":"M5","source":"%s","span":%s,"expect":"supported"}' % (S, N)),
    ("M6_nested_trailing_garbage", '{"meta":{"a":1} x,"id":"M6","source":"%s","span":%s,"expect":"supported"}' % (S, N)),
    # --- malformed at TOP LEVEL (claim_scan checks these) ---
    ("T1_top_trailing_comma", '{"id":"T1","source":"%s","span":%s,"expect":"supported",}' % (S, N)),
    ("T2_top_missing_comma", '{"id":"T2" "source":"%s","span":%s,"expect":"supported"}' % (S, N)),
    ("T3_top_trailing_garbage", '{"id":"T3","source":"%s","span":%s,"expect":"supported"} x' % (S, N)),
    ("T4_top_unquoted_key", '{"id":"T4",source:"%s","span":%s,"expect":"supported"}' % (S, N)),
    ("T5_top_array", '["id","T5"]'),
    ("T6_top_two_objects", '{"id":"T6a"} {"id":"T6b"}'),
    ("T7_top_unbalanced", '{"id":"T7","source":"%s","span":%s,"expect":"supported"' % (S, N)),
    ("T8_top_bracket_mismatch", '{"id":"T8","meta":[},"source":"%s"}' % S),
]


def main():
    with open(os.path.join(ROOT, "malformed.jsonl"), "w") as f:
        f.write("\n".join(line for _, line in L) + "\n")
    out = []
    for label, line in L:
        try:
            json.loads(line)
            v = "VALID-JSON"
        except Exception as e:
            v = "invalid-json: %s" % type(e).__name__
        out.append({"label": label, "json": v, "line": line})
    with open(os.path.join(HERE, "expected_malformed.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("records=%d" % len(out))
    for o in out:
        print("%-28s %s" % (o["label"], o["json"]))


if __name__ == "__main__":
    main()
