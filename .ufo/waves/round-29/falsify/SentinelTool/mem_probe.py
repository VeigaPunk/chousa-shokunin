#!/usr/bin/env python3
"""Peak-RSS measurement for the gzip/deflate path and the wire cap.

Runs the tool as a child of a measuring wrapper and reports the child's
ru_maxrss, for each bomb shape.
"""
import os
import subprocess
import sys
import time
import zlib
import gzip

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
from harness import (Server, build_servers, write_registry, write_items, resp,
                     GLOBAL_V6, HERE, TOOL)


def bomb_gzip(conn, line):
    payload = gzip.compress(b"A" * (256 * 1024 * 1024), 6)
    conn.sendall(resp(200, [("Content-Type", "text/html"), ("Content-Encoding", "gzip")], payload))
    sys.stderr.write("[gzip256] wire=%d inflated=268435456\n" % len(payload))


def bomb_deflate(conn, line):
    co = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    payload = co.compress(b"A" * (256 * 1024 * 1024)) + co.flush()
    conn.sendall(resp(200, [("Content-Type", "text/html"), ("Content-Encoding", "deflate")], payload))
    sys.stderr.write("[deflate256] wire=%d inflated=268435456\n" % len(payload))


def bomb_wire(conn, line):
    conn.sendall(resp(200, [("Content-Type", "text/html")], b"B" * (64 * 1024 * 1024)))
    sys.stderr.write("[wire64] sent=67108864\n")


def normal(conn, line):
    conn.sendall(resp(200, [("Content-Type", "text/html")],
                      b"<html><body>alpha beta gamma delta</body></html>"))


def measure(tag, url):
    reg = os.path.join(HERE, "reg4.tsv")
    itf = os.path.join(HERE, "items4.tsv")
    write_registry(reg, [("S001", "Doc %s" % url)])
    write_items(itf, [("i1", "S001", "alpha beta gamma delta")])
    code = ("import resource,subprocess,sys;"
            "p=subprocess.run(sys.argv[1:],capture_output=True);"
            "sys.stdout.write('RSS_KB=%d\\n'%resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss);"
            "sys.stdout.buffer.write(p.stdout)")
    t0 = time.monotonic()
    p = subprocess.run([sys.executable, "-c", code, sys.executable, TOOL, "verify",
                        "--items", itf, "--registry", reg],
                       capture_output=True, timeout=180)
    el = time.monotonic() - t0
    out = p.stdout.decode("utf-8", "replace").strip().replace("\n", " | ")
    print("== %-34s exit=%d elapsed=%.1fs" % (tag, p.returncode, el))
    print("     %s" % out)


def main():
    g, lp = build_servers()
    g.route("/gz", bomb_gzip)
    g.route("/df", bomb_deflate)
    g.route("/wire", bomb_wire)
    g.route("/ok", normal)
    gurl = "http://[%s]:%d" % (GLOBAL_V6, g.port)
    measure("R1 baseline 40-byte page", gurl + "/ok")
    measure("R2 gzip 256 MiB inflated", gurl + "/gz")
    measure("R3 deflate 256 MiB inflated", gurl + "/df")
    measure("R4 wire 64 MiB", gurl + "/wire")
    g.close()
    lp.close()


if __name__ == "__main__":
    main()
