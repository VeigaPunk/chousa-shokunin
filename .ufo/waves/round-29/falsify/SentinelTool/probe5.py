#!/usr/bin/env python3
"""Abort-resistance: malformed registry URLs and headers must not kill the run."""
import os
import socket
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
from harness import (Server, build_servers, write_registry, write_items, run_tool,
                     simple, resp, GLOBAL_V6, HERE, TOOL)


def main():
    g, lp = build_servers()
    gurl = "http://[%s]:%d" % (GLOBAL_V6, g.port)
    g.route("/ok", simple())

    cases = [
        ("invalid IPv6 bracket", "Doc http://[::1/x"),
        ("no host", "Doc http:///path"),
        ("empty port", "Doc http://example.invalid:/x"),
        ("port over range", "Doc http://example.invalid:99999/x"),
        ("non-numeric port", "Doc http://example.invalid:abc/x"),
        ("fragment only marker", "Doc %s/ok#frag" % gurl),
        ("userinfo empty password", "Doc http://alice@%s/ok" % "example.invalid"),
        ("URL with query", "Doc %s/ok?a=1" % gurl),
        ("percent in host", "Doc http://exa%%6dple.invalid/x"),
        ("very long host label", "Doc http://" + "a" * 300 + ".invalid/x"),
    ]
    for tag, cell in cases:
        reg = os.path.join(HERE, "reg7.tsv")
        itf = os.path.join(HERE, "items7.tsv")
        write_registry(reg, [("S001", cell)])
        write_items(itf, [("i1", "S001", "alpha beta gamma delta"),
                          ("i2", "S002", "alpha beta gamma delta")])
        # also add a second row pointing at a working URL? S002 is absent -> NO_SOURCE
        t0 = time.monotonic()
        try:
            p, el = run_tool(reg, itf, timeout=60)
        except subprocess.TimeoutExpired:
            print("== %-26s TIMEOUT after 60s" % tag)
            continue
        out = p.stdout.decode("utf-8", "replace").strip().replace("\n", " | ")
        print("== %-26s exit=%d elapsed=%.1fs lines=%d" % (tag, p.returncode, el,
                                                           out.count("QUOTE_REOPEN\t")))
        print("     %s" % out)
        e = p.stderr.decode("utf-8", "replace").strip()
        if e:
            print("     stderr: %s" % e.replace("\n", " | "))

    # header-vs-failure interplay: a bad header must not abort the *whole* run
    reg = os.path.join(HERE, "reg7b.tsv")
    itf = os.path.join(HERE, "items7b.tsv")
    g.route("/badhdr", lambda conn, line: conn.sendall(
        b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nX-Big: " + b"A" * 70000 +
        b"\r\nContent-Length: 2\r\n\r\nhi"))
    write_registry(reg, [("S001", "Doc %s/badhdr" % gurl), ("S002", "Doc %s/ok" % gurl)])
    write_items(itf, [("i1", "S001", "alpha beta gamma delta"),
                      ("i2", "S002", "alpha beta gamma delta"),
                      ("i3", "S001", "alpha beta gamma delta")])
    p, el = run_tool(reg, itf, timeout=60)
    print("== %-26s exit=%d elapsed=%.1fs" % ("bad header mixed run", p.returncode, el))
    print("     %s" % p.stdout.decode("utf-8", "replace").strip().replace("\n", " | "))

    g.close()
    lp.close()


if __name__ == "__main__":
    main()
