#!/usr/bin/env python3
"""Generate one-line JSON claim records of exact byte sizes for the C1 walk benchmark.

Each record: a JSON object with the seven read keys once at top level, a nested
object with decoy read-key members, an array with a decoy object, and string
values containing structure-looking text. Padding is an extra string member.
"""
import json
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
SIZES = [500, 4096, 16384, 65536]

DECOY = {"line": "1", "sha256": "deadbeef", "id": "nested-id",
         "meta": {"span": "nested-span", "marker": "nested-marker"}}
ARR = [{"source": "nested-source", "expect": "unsupported"}]
CONFUSER = 'tricky { "line": "9", "id": \\"zz\\" } [x] : , back\\\\'


def record(size):
    rec = {
        "id": "rec-%04d" % size,
        "source": "src-a.txt",
        "span": "L3-L5",
        "expect": "supported",
        "marker": "MARK-1",
        "line": "7",
        "sha256": "0123456789abcdef",
        "meta": DECOY,
        "arr": ARR,
        "conf": CONFUSER,
        "pad": "",
    }
    base = json.dumps(rec, separators=(",", ":")).encode()
    extra = size - len(base)
    if extra < 0:
        raise SystemExit("size %d too small for base record %d" % (size, len(base)))
    rec["pad"] = "p" * extra
    line = json.dumps(rec, separators=(",", ":")).encode()
    assert len(line) == size, (len(line), size)
    assert json.loads(line)["pad"] == "p" * extra
    return line


for s in SIZES:
    path = "%s/line_%d.jsonl" % (OUT, s)
    with open(path, "wb") as f:
        f.write(record(s) + b"\n")
    print(path, s)
