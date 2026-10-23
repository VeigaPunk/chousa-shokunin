#!/usr/bin/env python3
"""Edge/valid-forms probe for the hardened worktree claim_scan (263ffb9d):
does the new token/whitespace/duplicate logic reject any VALID JSON record, and
does it still refuse the duplicate forms? All lines are valid JSON except none.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "root")
N = json.dumps("needle span words here")
S = "src/a.md"
L = [
    ("E1_nested_legal_scalars", '{"meta":{"a":0,"b":-0,"c":1.5,"d":1e10,"e":-2.5E-3,"f":true,"g":false,"h":null,"i":[],"j":{}},"id":"E1","source":"%s","span":%s,"expect":"supported"}' % (S, N), "supported"),
    ("E2_top_legal_scalars_nonread", '{"n":-0.0e+0,"b":false,"z":null,"arr":[1,2],"obj":{"k":[]},"id":"E2","source":"%s","span":%s,"expect":"supported"}' % (S, N), "supported"),
    ("E3_ws_tab_cr", '{"id":"E3",\t"source":"%s",\r"span":%s,"expect":"supported"}' % (S, N), "supported"),
    ("E4_three_identical_line", '{"id":"E4","source":"%s","span":%s,"expect":"supported","line":"2","line":"2","line":"2"}' % (S, N), "invalid"),
    ("E5_three_span_third_differs", '{"id":"E5","source":"%s","span":%s,"expect":"supported","span":%s,"span":"other words entirely"}' % (S, N, N), "invalid"),
    ("E6_dup_id_differing", '{"id":"E6","id":"E6x","source":"%s","span":%s,"expect":"supported"}' % (S, N), "invalid"),
    ("E7_dup_marker_top", '{"id":"E7","source":"%s","span":%s,"expect":"supported","marker":"m","marker":"m"}' % (S, N), "invalid"),
    ("E8_nested_empty_containers", '{"meta":[[],{},[{}],{"a":[]}],"id":"E8","source":"%s","span":%s,"expect":"supported"}' % (S, N), "supported"),
    ("E9_escaped_formfeed_string", '{"meta":{"a":"x\\fy"},"id":"E9","source":"%s","span":%s,"expect":"supported"}' % (S, N), "supported"),
    ("E10_nested_number_forms", '{"meta":{"a":0.0,"b":1e+2,"c":-0,"d":12.34e-5},"id":"E10","source":"%s","span":%s,"expect":"supported"}' % (S, N), "supported"),
    ("E11_top_line_nested_number", '{"id":"E11","source":"%s","span":%s,"expect":"supported","line":"2","meta":{"line":9}}' % (S, N), "supported"),
    ("E12_nested_dups_all_read_keys", '{"meta":{"id":"a","id":"b","source":"x","span":"y","expect":"contradicted","line":"9","sha256":"00"},"id":"E12","source":"%s","span":%s,"expect":"supported"}' % (S, N), "supported"),
    ("E13_top_negative_zero", '{"z":-0,"id":"E13","source":"%s","span":%s,"expect":"supported"}' % (S, N), "supported"),
    ("E14_nested_token_boundaries", '{"meta":{"a":1,"b":"x,y:z","c":[true,null,-1.5e-2]},"id":"E14","source":"%s","span":%s,"expect":"supported"}' % (S, N), "supported"),
    ("E15_top_string_structure_chars", '{"id":"E15","source":"%s","span":%s,"expect":"supported","claim":"{\\"a\\": 1} [2] , :"}' % (S, N), "supported"),
    ("E16_nested_spaced_literals", '{"meta":[ true , false , null ],"id":"E16","source":"%s","span":%s,"expect":"supported"}' % (S, N), "supported"),
]


def main():
    with open(os.path.join(ROOT, "edge.jsonl"), "w") as f:
        f.write("\n".join(x[1] for x in L) + "\n")
    for label, line, _ in L:
        json.loads(line)  # every line must be valid JSON
    json.dump([{"label": a, "expect": c} for a, _, c in L], open(os.path.join(HERE, "expected_edge.json"), "w"), indent=1)
    print("records=%d all-valid-json" % len(L))


if __name__ == "__main__":
    main()
