#!/usr/bin/env python3
"""Round 33 w2 ProbeLongLines33: flat (no nesting) claim records whose *span* is
0.5/4/16/64 KiB, plus a 200-record file of ~1 KiB records, plus one control
where the long padding is a non-read member (reader-only differential)."""
import json
import os
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
FX = os.path.join(OUT, "fx")


def pad(n, unit="w"):
    """ASCII padding of exactly n chars, word tokens separated by single spaces,
    never ending in a space (exact length)."""
    if n <= 0:
        return ""
    s = unit
    while len(s) + 2 <= n:
        s += " " + unit
    rem = n - len(s)
    if rem == 1:
        s += unit
    elif rem >= 2:
        s += " " + unit * (rem - 1)
    return s


def span_of(size, tag):
    head = tag + " "
    body = pad(size - len(head))
    s = head + body
    assert len(s) == size, (len(s), size)
    return s


def rec(id_, src, span, extra=""):
    # flat object: seven-ish read keys and nothing nested
    return ('{"id":"%s","source":"%s","span":"%s","expect":"supported"%s}'
            % (id_, src, span, extra))


def write_case(name, record, source):
    d = os.path.join(FX, name)
    os.makedirs(os.path.join(d, "spans"), exist_ok=True)
    sp = os.path.join(d, "spans", "src.txt")
    with open(sp, "w", encoding="utf-8") as f:
        f.write(source)
    with open(os.path.join(d, "claims.jsonl"), "w", encoding="utf-8") as f:
        f.write(record + "\n")
    return d


def main():
    os.makedirs(FX, exist_ok=True)
    cases = {}
    for size in (512, 4096, 16384, 65536):
        tag = "L%d" % size
        span = span_of(size, tag)
        r = rec(tag, "spans/src.txt", span)
        assert len(r) < size + 96, (len(r), size)
        cases["span%d" % size] = write_case("span%d" % size, r, span + "\n")
    # control: long padding in a member the reader never reads; short span
    for size in (65536,):
        tag = "P%d" % size
        span = "distinct-marker-%d" % size
        note = pad(size - len('"note":""'))
        r = rec(tag, "spans/src.txt", span, ',"note":"%s"' % note)
        cases["pad%d" % size] = write_case("pad%d" % size, r, "heading\n" + span + "\n")
    # 200 records of ~1 KiB each, 200 source lines
    d = os.path.join(FX, "many200")
    os.makedirs(os.path.join(d, "spans"), exist_ok=True)
    src_lines = []
    recs = []
    for k in range(200):
        tag = "R%04d" % k
        # target whole record ~1024 B: line = 82-ish fixed + span
        span = tag + " " + pad(1024 - 100 - len(tag) - 1)
        recs.append(rec(tag, "spans/src.txt", span))
        src_lines.append(span)
    with open(os.path.join(d, "spans", "src.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(src_lines) + "\n")
    with open(os.path.join(d, "claims.jsonl"), "w", encoding="utf-8") as f:
        f.write("\n".join(recs) + "\n")
    cases["many200"] = d
    sizes = [len(open(os.path.join(p, "claims.jsonl"), "rb").read()) for p in cases.values()]
    for (k, p), n in zip(cases.items(), sizes):
        ln = len(open(os.path.join(p, "claims.jsonl"), "rb").readline())
        print("%-10s %s bytes_file=%d bytes_line1=%d" % (k, p, n, ln))


if __name__ == "__main__":
    main()
