#!/usr/bin/env python3
"""Build probe claims + source root for C1 top-level-reader contract checks."""
import json, os, sys

root = sys.argv[1]
os.makedirs(os.path.join(root, "lib"), exist_ok=True)
open(os.path.join(root, "lib/span.md"), "w").write(
    "alpha beta gamma delta\nepsilon zeta eta theta\niota kappa lambda mu\nnu xi omicron pi\n")

S = '"source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported"'
L = [
 # nested duplicates change nothing (contract item 1)
 '{"id":"B1",%s,"meta":{"line":"9","line":"8"},"line":"1"}' % S,
 '{"id":"B2",%s,"meta":[{"line":"9"},{"line":"8"}],"line":"1"}' % S,
 '{"id":"B3",%s,"meta":{"z":{"line":"9","line":"8"}},"line":"1"}' % S,
 '{"id":"B4",%s,"meta":{"sha256":"00","sha256":"11"}}' % S,
 # duplicated top-level read fields with non-string second values (item 2)
 '{"id":"A1",%s,"line":"1","line":4}' % S,
 '{"id":"A2",%s,"span":null}' % S,
 '{"id":"A3",%s,"expect":["x"]}' % S,
 '{"id":"A4",%s,"source":{}}' % S,
 '{"id":"A5",%s,"sha256":"ab","sha256":7}' % S,
 # string content is never structure (item 3)
 '{"id":"C1",%s,"note":"\\"line\\": \\"9\\", \\"sha256\\": \\"00\\"","line":"1"}' % S,
 '{"id":"C2",%s,"note":"ends with \\\\","line":"1"}' % S,
 '{"id":"C3",%s,"note":"\\u007b\\u0022line\\u0022:\\u00229\\u0022\\u007d","line":"1"}' % S,
 '{"id":"C4",%s,"meta":["}\\"line\\": \\"9\\"", {"line":"8"}],"line":"1"}' % S,
 # uncounted-by-v2 duplicate keys the contract lists
 '{"id":"M1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"contradicted","marker":"m1","marker":"m2"}',
 '{"id":"M2","id":"M2b",%s}' % S,
 # marker_default row precedence vs duplicated read fields
 '{"marker_default":"md","line":"1","line":"2"}',
 '{"id":7,"marker_default":"md","line":"1","line":"2"}',
 '{"marker_default":"md","source":"lib/span.md","span":"alpha","span":"beta"}',
 '{"marker_default":"md","line":"1"}',
 # malformed scalar tokens (line is not valid JSON; v2 asks fail-closed)
 '{"id":"E1",%s,"line":"1","x":01}' % S,
 '{"id":"E2",%s,"line":"1","x":tru}' % S,
 '{"id":"E3",%s,"line":"1","x":xyz}' % S,
 '{"id":"E4",%s,"line":"1","x":+1}' % S,
 '{"id":"E5",%s,"line":"1","x":.5}' % S,
 '{"id":"E6",%s,"line":"1","x":1.}' % S,
 '{"id":"E7",%s,"line":"1","x":NaN}' % S,
 '{"id":"E8",%s,"x":1"line":"1","line":"9"}' % S,
]
out = sys.argv[2]
with open(out, "w") as f:
    for i, ln in enumerate(L, 1):
        try:
            json.loads(ln); v = "valid"
        except Exception as e:
            v = "INVALID:" + type(e).__name__
        print("%2d %-18s %s" % (i, v, ln[:100]))
        f.write(ln + "\n")
