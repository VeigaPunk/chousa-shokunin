#!/usr/bin/env python3
"""Redirect-limit behaviour and a precise measure of the deadline overrun."""
import os
import socket
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
from harness import (Server, build_servers, write_registry, write_items, run_tool,
                     simple, resp, redirect, GLOBAL_V6, HERE, TOOL)


def main():
    g, lp = build_servers()
    gurl = "http://[%s]:%d" % (GLOBAL_V6, g.port)

    def self_loop(conn, line):
        conn.sendall(resp(302, [("Location", gurl + "/loop")], b"", "Found"))

    def chain(conn, line):
        # /c0 -> /c1 -> ... -> /c11 -> /ok
        n = line.split(" ")[1]
        i = int(n[2:]) if n[2:].isdigit() else 0
        if i >= 11:
            simple()(conn, line)
        else:
            conn.sendall(resp(302, [("Location", "/c%d" % (i + 1))], b"", "Found"))

    def drip(conn, line):
        conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 100000\r\n\r\n")
        try:
            while True:
                time.sleep(2.0)
                conn.sendall(b"x")
        except OSError:
            return

    g.route("/loop", self_loop)
    for i in range(12):
        g.route("/c%d" % i, chain)
    g.route("/ok", simple())
    g.route("/drip", drip)

    def one(tag, path, timeout):
        reg = os.path.join(HERE, "reg6.tsv")
        itf = os.path.join(HERE, "items6.tsv")
        write_registry(reg, [("S001", "Doc %s%s" % (gurl, path))])
        write_items(itf, [("i1", "S001", "alpha beta gamma delta")])
        t0 = time.monotonic()
        try:
            p, el = run_tool(reg, itf, timeout=timeout)
        except subprocess.TimeoutExpired:
            print("== %-40s STILL RUNNING after %ds (killed)" % (tag, timeout))
            return
        print("== %-40s exit=%d elapsed=%.1fs" % (tag, p.returncode, el))
        print("     stdout: %s" % p.stdout.decode("utf-8", "replace").strip().replace("\n", " | "))

    one("S1 self-redirect loop", "/loop", 90)
    one("S2 11-hop chain to /ok (limit 10)", "/c0", 90)
    one("S3 drip 1B/2s, deadline is 30 s", "/drip", 70)

    g.close()
    lp.close()


if __name__ == "__main__":
    main()
