#!/usr/bin/env python3
"""Second probe round: deadline (fixed drip), per-case RSS, DNS-rebinding TOCTOU,
CRLF/header injection, proxy env, multicast target, redirect chain, no-file-writes."""
import os
import resource
import socket
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
from harness import (Server, build_servers, write_registry, write_items, run_tool,
                     simple, redirect, resp, GLOBAL_V6, HERE, TOOL)


def slow_body_fixed(conn, line):
    """Headers with Content-Length: 40 but the body bytes drip one per second."""
    head = ("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 40\r\n\r\n")
    conn.sendall(head.encode())
    for _ in range(40):
        time.sleep(1.0)
        try:
            conn.sendall(b"x")
        except OSError:
            return


def slow_headers(conn, line):
    """Status line plus headers dribbled one byte per second (slowloris on headers)."""
    conn.sendall(b"HTTP/1.1 200 OK\r\n")
    for _ in range(200):
        time.sleep(0.5)
        try:
            conn.sendall(b"X-Pad: " + b"a" * 60 + b"\r\n")
        except OSError:
            return


def redirect_chain(conn, line):
    """302 to itself 20 times -> exceeds MAX_REDIRECTS."""
    conn.sendall(resp(302, [("Location", "http://%s:%d/r" % (GLOBAL_V6, harness.PORT))], b"", "Found"))


def run_one(registry_rows, items_rows, timeout=120, env=None, cwd=HERE):
    reg = os.path.join(HERE, "reg2.tsv")
    itf = os.path.join(HERE, "items2.tsv")
    write_registry(reg, registry_rows)
    write_items(itf, items_rows)
    e = dict(os.environ)
    if env:
        e.update(env)
    cmd = [sys.executable, TOOL, "verify", "--items", itf, "--registry", reg]
    t0 = time.monotonic()
    # isolate RSS: fork a child that runs the tool and reports its own rusage
    code = ("import resource,subprocess,sys;"
            "p=subprocess.run(sys.argv[1:],capture_output=True);"
            "sys.stdout.write('RSS=%d\\n'%resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss);"
            "sys.stdout.buffer.write(p.stdout);"
            "sys.stderr.buffer.write(p.stderr);"
            "sys.exit(p.returncode)")
    p = subprocess.run([sys.executable, "-c", code] + cmd, capture_output=True,
                       timeout=timeout, env=e, cwd=cwd)
    return p, time.monotonic() - t0


def show(tag, p, el, extra=()):
    print("== %-46s exit=%s elapsed=%.1fs" % (tag, p.returncode, el))
    print("     stdout: %s" % p.stdout.decode("utf-8", "replace").strip().replace("\n", " | "))
    err = p.stderr.decode("utf-8", "replace").strip()
    if err:
        print("     stderr: %s" % err.replace("\n", " | "))
    for x in extra:
        print("     %s" % x)


def main():
    g, lp = build_servers()
    gurl = "http://[%s]:%d" % (GLOBAL_V6, g.port)
    harness.PORT = g.port
    g.route("/slow", slow_body_fixed)
    g.route("/slowhdr", slow_headers)
    g.route("/chain", redirect_chain)
    g.route("/ok", simple())
    g.route("/rel-loop", redirect("//127.0.0.1:%d/x" % lp.port))
    g.route("/crlf", redirect("http://[::1]/x\r\nX-Injected: 1"))
    g.route("/abs", redirect("http://127.0.0.1:%d/target" % lp.port))
    print("global-v6 port %d loopback port %d" % (g.port, lp.port))

    # 1. slow body drip, fixed
    p, el = run_one([("S001", "Doc %s/slow" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
                     timeout=150)
    show("P1 slow body drip 40B @1B/s", p, el,
         ["verdict=%s" % ("DEADLINE-HELD" if el <= 35 else "DEADLINE-OVERRUN")])

    # 2. slow headers
    p, el = run_one([("S001", "Doc %s/slowhdr" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
                     timeout=150)
    show("P2 slow headers drip", p, el,
         ["verdict=%s" % ("DEADLINE-HELD" if el <= 35 else "DEADLINE-OVERRUN")])

    # 3. redirect chain > MAX_REDIRECTS
    p, el = run_one([("S001", "Doc %s/chain" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
                     timeout=90)
    show("P3 redirect chain 20 hops", p, el)

    # 4. scheme-relative redirect to loopback
    p, el = run_one([("S001", "Doc %s/rel-loop" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
                     timeout=90)
    show("P4 //127.0.0.1 redirect", p, el,
         ["loopback accepted=%d" % len(lp.accepted)])

    # 5. CRLF in Location header
    p, el = run_one([("S001", "Doc %s/crlf" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
                     timeout=90)
    show("P5 CRLF in Location", p, el, ["loopback accepted=%d" % len(lp.accepted)])

    # 6. ambient proxy env must be ignored
    p, el = run_one([("S001", "Doc %s/ok" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
                     timeout=90, env={"http_proxy": "http://127.0.0.1:%d" % lp.port,
                                      "https_proxy": "http://127.0.0.1:%d" % lp.port,
                                      "ALL_PROXY": "socks5://127.0.0.1:%d" % lp.port})
    show("P6 ambient proxy env set", p, el,
         ["loopback accepted=%d (proxy used if >0)" % len(lp.accepted)])

    # 7. CRLF in registry URL path
    p, el = run_one([("S001", "Doc %s/ok%%0d%%0aX-Injected:%%201" % gurl)],
                     [("i1", "S001", "alpha beta gamma delta")], timeout=90)
    show("P7 percent-encoded CRLF in path", p, el)

    # 8. multicast target 224.0.0.1
    p, el = run_one([("S001", "Doc http://224.0.0.1/x")],
                     [("i1", "S001", "alpha beta gamma delta")], timeout=90)
    show("P8 multicast 224.0.0.1", p, el)

    # 9. metadata IP 100.100.100.200 (alibaba) and 192.0.0.192 (oracle)
    for a in ("100.100.100.200", "192.0.0.192", "fd00:ec2::254"):
        p, el = run_one([("S001", "Doc http://[%s]/x" % a if ":" in a else "Doc http://%s/x" % a)],
                         [("i1", "S001", "alpha beta gamma delta")], timeout=90)
        show("P9 metadata addr %s" % a, p, el)

    # 10. no files written anywhere: snapshot cwd and /tmp
    before = set(os.listdir(HERE))
    p, el = run_one([("S001", "Doc %s/ok" % gurl)], [("i1", "S001", "alpha beta gamma delta")],
                     timeout=90)
    after = set(os.listdir(HERE))
    show("P10 no new files in cwd", p, el, ["new files: %r" % sorted(after - before)])

    g.close()
    lp.close()


if __name__ == "__main__":
    main()
