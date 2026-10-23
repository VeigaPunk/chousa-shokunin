#!/usr/bin/env python3
"""Third probe round: unbounded slow drip, cross-host redirect, IPv4-mapped metadata,
deflate bomb variants, chunked encoding, Content-Length lie."""
import os
import socket
import subprocess
import sys
import time
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
from harness import (Server, build_servers, write_registry, write_items, run_tool,
                     simple, redirect, resp, GLOBAL_V6, HERE, TOOL)

SECOND_V6 = "2804:14d:5c56:36ef:2ed8:aeff:0:2c0"


def slow_drip_forever(conn, line):
    """1 byte every 5 s, forever: no total read bound at all."""
    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 100000\r\n\r\n")
    try:
        while True:
            time.sleep(5.0)
            conn.sendall(b"x")
    except OSError:
        return


def deflate_bomb(conn, line):
    co = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    payload = co.compress(b"A" * (64 * 1024 * 1024)) + co.flush()
    conn.sendall(resp(200, [("Content-Type", "text/html"),
                            ("Content-Encoding", "deflate")], payload))
    sys.stderr.write("[deflate] wire=%d inflated=%d\n" % (len(payload), 64 * 1024 * 1024))


def double_gzip(conn, line):
    import gzip
    inner = gzip.compress(b"B" * (64 * 1024 * 1024))
    outer = gzip.compress(inner)
    conn.sendall(resp(200, [("Content-Type", "text/html"),
                            ("Content-Encoding", "gzip")], outer))
    sys.stderr.write("[2gzip] wire=%d inner=%d\n" % (len(outer), len(inner)))


def lying_length(conn, line):
    """Claims 10 MiB, sends 10 MiB, then keeps the connection open."""
    body = b"C" * (10 * 1024 * 1024)
    conn.sendall(resp(200, [("Content-Type", "text/html")], body))
    time.sleep(120)


def chunked_bomb(conn, line):
    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nTransfer-Encoding: chunked\r\n\r\n")
    chunk = b"D" * 65536
    try:
        for _ in range(200):                       # 12.5 MiB chunked
            conn.sendall(b"%x\r\n" % len(chunk) + chunk + b"\r\n")
        conn.sendall(b"0\r\n\r\n")
    except OSError:
        return


def cross_host_redirect(conn, line):
    conn.sendall(resp(302, [("Location", "http://[%s]:%d/ok" % (SECOND_V6, harness.PORT2))], b"", "Found"))


def main():
    g, lp = build_servers()
    g2 = Server(socket.AF_INET6, (SECOND_V6, 0), "global2")
    g2.route("/ok", simple())
    g2.start()
    harness.PORT = g.port
    harness.PORT2 = g2.port
    gurl = "http://[%s]:%d" % (GLOBAL_V6, g.port)
    g.route("/drip", slow_drip_forever)
    g.route("/defl", deflate_bomb)
    g.route("/2gz", double_gzip)
    g.route("/lie", lying_length)
    g.route("/chunk", chunked_bomb)
    g.route("/xhost", cross_host_redirect)
    print("global-v6 port %d second-global-v6 port %d loopback port %d" % (g.port, g2.port, lp.port))

    def one(tag, url, timeout=90, items=None, rows=None):
        reg = os.path.join(HERE, "reg3.tsv")
        itf = os.path.join(HERE, "items3.tsv")
        write_registry(reg, rows or [("S001", "Doc %s" % url)])
        write_items(itf, items or [("i1", "S001", "alpha beta gamma delta")])
        t0 = time.monotonic()
        try:
            p, el = run_tool(reg, itf, timeout=timeout)
        except subprocess.TimeoutExpired:
            print("== %-44s TIMEOUT after %ds" % (tag, timeout))
            return None
        print("== %-44s exit=%d elapsed=%.1fs" % (tag, p.returncode, el))
        print("     stdout: %s" % p.stdout.decode("utf-8", "replace").strip().replace("\n", " | "))
        e = p.stderr.decode("utf-8", "replace").strip()
        if e:
            print("     stderr: %s" % e.replace("\n", " | "))
        return p

    # unbounded slow drip: the tool must not run past the 30 s deadline
    one("Q1 slow drip 1B/5s (expect <=35s)", gurl + "/drip", timeout=60)

    # deflate bomb
    one("Q2 raw-deflate bomb 64 MiB", gurl + "/defl")

    # double gzip: server says gzip once, body is gzip-of-gzip
    one("Q3 gzip-of-gzip", gurl + "/2gz")

    # Content-Length lies about the body size
    one("Q4 10 MiB body", gurl + "/lie")

    # chunked transfer encoding over the cap
    one("Q5 chunked 12.5 MiB", gurl + "/chunk")

    # redirect to a DIFFERENT global host (host allowlist question)
    one("Q6 redirect to a different global host", gurl + "/xhost")

    # IPv4-mapped metadata address
    one("Q7 registry URL [::ffff:169.254.169.254]", "http://[::ffff:169.254.169.254]/x")

    # NAT64-style translation prefix carrying the metadata address
    one("Q8 registry URL [64:ff9b::169.254.169.254]", "http://[64:ff9b::169.254.169.254]/x")

    g.close()
    g2.close()
    lp.close()


if __name__ == "__main__":
    main()
