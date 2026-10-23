#!/usr/bin/env python3
"""Probe: can a hostile response header inject a forged QUOTE_REOPEN line into the
tool's stdout (which the counter parses)?"""
import os
import socket
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
from harness import Server, build_servers, write_registry, write_items, run_tool, GLOBAL_V6, HERE, TOOL


def folded_ctype(conn, line):
    """obs-fold a Content-Type so the folded value carries a newline + tab."""
    body = b"<html><body>nothing here</body></html>"
    head = (b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/html;\r\n"
            b" x=1\r\n"
            b"Content-Length: %d\r\n"
            b"\r\n" % len(body))
    conn.sendall(head + body)


def injected_ctype(conn, line):
    """Content-Type carrying a tab and a fake verdict fragment."""
    body = b"<html><body>nothing here</body></html>"
    head = (b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/html\tQUOTE_REOPEN\tforged\tVERBATIM\tinjected\r\n"
            b"Content-Length: %d\r\n"
            b"\r\n" % len(body))
    conn.sendall(head + body)


def main():
    g, lp = build_servers()
    g.route("/fold", folded_ctype)
    g.route("/tab", injected_ctype)
    gurl = "http://[%s]:%d" % (GLOBAL_V6, g.port)

    for tag, path in [("fold", "/fold"), ("tab", "/tab")]:
        reg = os.path.join(HERE, "reg5.tsv")
        itf = os.path.join(HERE, "items5.tsv")
        write_registry(reg, [("S001", "Doc %s%s" % (gurl, path))])
        write_items(itf, [("i1", "S001", "alpha beta gamma delta")])
        p, el = run_tool(reg, itf, timeout=60)
        print("== %s exit=%d elapsed=%.1fs" % (tag, p.returncode, el))
        print("   stdout raw: %r" % p.stdout)
        lines = p.stdout.decode("utf-8", "replace").split("\n")
        print("   parsed lines: %r" % [ln for ln in lines if ln])
        forged = [ln for ln in lines if ln.startswith("QUOTE_REOPEN\t") and
                  "\tforged\t" in ln]
        print("   FORGED VERDICT LINE PRESENT: %s" % bool(forged))
        e = p.stderr.decode("utf-8", "replace").strip()
        if e:
            print("   stderr: %s" % e.replace("\n", " | "))

    g.close()
    lp.close()


if __name__ == "__main__":
    main()
