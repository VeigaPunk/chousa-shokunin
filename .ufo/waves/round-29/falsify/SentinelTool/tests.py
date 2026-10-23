#!/usr/bin/env python3
"""T1-T7 security tests for the landed tools/quote-reopen.py.

Servers: this host's own global IPv6 address (routed locally: `local ... dev lo`)
plus a 127.0.0.1 listener used as a redirect target. No external host is contacted.
"""
import gzip
import os
import resource
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import (Server, build_servers, write_registry, write_items, run_tool,
                     simple, redirect, gzip_bomb, big_body, slow_body, big_header,
                     many_headers, resp, GLOBAL_V6, HERE, TOOL)

RESULTS = []
LAST = {}


def record(name, verdict, evidence):
    RESULTS.append((name, verdict, evidence))
    print("== %-46s %s" % (name, verdict))
    for line in evidence:
        print("     %s" % line)


def case(name, g, lp, routes, rows, items, timeout=120, expect=None, strace=False,
         post=None):
    for path, fn in routes.items():
        g.route(path, fn)
    reg = os.path.join(HERE, "reg.tsv")
    itf = os.path.join(HERE, "items.tsv")
    write_registry(reg, rows)
    write_items(itf, items)
    t0 = time.monotonic()
    try:
        p, el = run_tool(reg, itf, timeout=timeout, strace=strace)
    except subprocess.TimeoutExpired as e:
        record(name, "TIMEOUT", ["tool did not finish in %ds" % timeout,
                                 "partial stdout: %r" % (e.stdout or b"")[:400]])
        return None
    after = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    ev = ["exit=%d elapsed=%.1fs peak_child_rss=%dKB" % (p.returncode, el, after),
          "stdout: %s" % p.stdout.decode("utf-8", "replace").strip().replace("\n", " | ")]
    err = p.stderr.decode("utf-8", "replace").strip()
    if err:
        ev.append("stderr: %s" % err.replace("\n", " | "))
    if post:
        ev.extend(post(g, lp, p))
    record(name, expect or "RAN", ev)
    return p


def loop_post(g, lp, p):
    return ["loopback listener accepted=%d requests=%r" % (len(lp.accepted), lp.requests)]


def main():
    g, lp = build_servers()
    gurl = "http://[%s]:%d" % (GLOBAL_V6, g.port)
    lurl = "http://127.0.0.1:%d" % lp.port
    print("global-v6 server port %d, loopback server port %d" % (g.port, lp.port))

    # ---------- T1: private / loopback / link-local targets ----------
    case("T1-a registry URL is loopback", g, lp, {},
         [("S001", "Loopback doc %s/ok" % lurl)], [("i1", "S001", "alpha beta gamma delta")],
         expect="REFUSED", post=loop_post)

    case("T1-b registry URL is 10.x", g, lp, {},
         [("S001", "Private doc http://10.0.0.1/x")], [("i1", "S001", "alpha beta gamma delta")],
         expect="REFUSED")

    case("T1-c redirect to 127.0.0.1", g, lp,
         {"/redir-loop": redirect(lurl + "/target")},
         [("S001", "Doc %s/redir-loop" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         expect="NOT-FOLLOWED", post=loop_post)

    case("T1-d redirect to 10.0.0.1", g, lp,
         {"/redir-10": redirect("http://10.0.0.1/x")},
         [("S001", "Doc %s/redir-10" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         expect="NOT-FOLLOWED")

    case("T1-e redirect to 169.254.169.254", g, lp,
         {"/redir-meta": redirect("http://169.254.169.254/latest/meta-data/")},
         [("S001", "Doc %s/redir-meta" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         expect="NOT-FOLLOWED")

    case("T1-f redirect to same global host (control)", g, lp,
         {"/redir-ok": redirect(gurl + "/ok")},
         [("S001", "Doc %s/redir-ok" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         expect="FOLLOWED")

    for tag, url in [("decimal-int", "http://2130706433/x"),
                     ("hex", "http://0x7f000001/x"),
                     ("v4mapped", "http://[::ffff:127.0.0.1]/x"),
                     ("decimal-dotted", "http://127.1/x")]:
        case("T1-g registry URL %s" % tag, g, lp, {},
             [("S001", "Doc %s" % url)], [("i1", "S001", "alpha beta gamma delta")],
             expect="REFUSED", post=loop_post)

    # ---------- T2: scheme confinement ----------
    for tag, loc in [("file", "file:///etc/hostname"),
                     ("ftp", "ftp://127.0.0.1:21/secret"),
                     ("data", "data:text/plain,hello")]:
        case("T2-%s redirect scheme" % tag, g, lp,
             {"/r": redirect(loc)},
             [("S001", "Doc %s/r" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
             expect="REFUSED", post=loop_post)

    case("T2-d registry cell holds only a file: URL", g, lp, {},
         [("S001", "Local file file:///etc/hostname")], [("i1", "S001", "alpha beta gamma delta")],
         expect="NO-SOURCE")

    # ---------- T3: decompression bomb ----------
    case("T3-a gzip bomb (64 MiB inflated, small wire)", g, lp,
         {"/gzip": gzip_bomb},
         [("S001", "Doc %s/gzip" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         expect="CAPPED")

    case("T3-b wire body over 8 MiB", g, lp,
         {"/big": big_body},
         [("S001", "Doc %s/big" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         expect="CAPPED")

    small = gzip.compress(b"<html><body>" + b"alpha beta gamma delta " * 100 + b"</body></html>")
    case("T3-c small gzip body still readable (control)", g, lp,
         {"/gzsmall": lambda conn, ln: conn.sendall(
             resp(200, [("Content-Type", "text/html"), ("Content-Encoding", "gzip")], small))},
         [("S001", "Doc %s/gzsmall" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         expect="VERBATIM")

    # ---------- T4: deadline ----------
    def never(conn, line):
        time.sleep(300)

    case("T4-a server never answers", g, lp,
         {"/hang": never},
         [("S001", "Doc %s/hang" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         timeout=120, expect="DEADLINE")

    case("T4-b slow body drip (40 B, 1 B/s)", g, lp,
         {"/slow": slow_body},
         [("S001", "Doc %s/slow" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         timeout=120, expect="DEADLINE")

    # ---------- T5: oversized headers ----------
    case("T5-a 100 kB header line", g, lp,
         {"/bighdr": big_header},
         [("S001", "Doc %s/bighdr" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         expect="UNREACHABLE-NO-ABORT")

    case("T5-b 150 headers", g, lp,
         {"/manyhdr": many_headers},
         [("S001", "Doc %s/manyhdr" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         expect="UNREACHABLE-NO-ABORT")

    case("T5-c big header on one URL, other URL still judged", g, lp,
         {"/bighdr": big_header, "/ok": simple()},
         [("S001", "Doc %s/bighdr" % gurl), ("S002", "Doc %s/ok" % gurl)],
         [("i1", "S001", "alpha beta gamma delta"), ("i2", "S002", "alpha beta gamma delta")],
         expect="NO-ABORT")

    # ---------- T6: userinfo ----------
    secret = "s3cr3tP4ss"

    def leak_post(g, lp, p):
        blob = (p.stdout or b"") + (p.stderr or b"")
        return ["secret present in tool output: %s" % (secret.encode() in blob),
                "tool output bytes: %r" % blob[:300]]

    case("T6-a userinfo in registry URL", g, lp, {},
         [("S001", "Doc https://alice:%s@[%s]:%d/ok" % (secret, GLOBAL_V6, g.port))],
         [("i1", "S001", "alpha beta gamma delta")],
         expect="REFUSED-NO-LEAK", post=leak_post)

    case("T6-b userinfo in redirect Location", g, lp,
         {"/r": redirect("http://bob:%s@127.0.0.1:9/x" % secret)},
         [("S001", "Doc %s/r" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         expect="REFUSED-NO-LEAK", post=leak_post)

    # ---------- T7: no files written ----------
    case("T7-a no files written (strace)", g, lp,
         {"/ok": simple()},
         [("S001", "Doc %s/ok" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
         strace=True, expect="NO-WRITES")

    g.close()
    lp.close()
    return RESULTS


if __name__ == "__main__":
    main()
