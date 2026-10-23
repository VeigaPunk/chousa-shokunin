#!/usr/bin/env python3
"""Is DNS resolution bounded by the tool's 30 s deadline?

A DNS server on loopback that never answers, and a resolv.conf with default
timeout/attempts. Measures how long the tool takes before it reports UNREACHABLE.
"""
import os
import socket
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py"


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 53))
    stop = threading.Event()
    seen = []

    def sink():
        s.settimeout(0.5)
        while not stop.is_set():
            try:
                d, peer = s.recvfrom(4096)
                seen.append(peer)
            except socket.timeout:
                continue
            except OSError:
                break

    threading.Thread(target=sink, daemon=True).start()

    reg = os.path.join(HERE, "reg_dns.tsv")
    itf = os.path.join(HERE, "items_dns.tsv")
    with open(reg, "w") as f:
        f.write("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n")
        f.write("| S001 | Doc http://silent.test:45810/ok | spec | A | s | a | t | mined | 2026-10-22 | 365d | n |\n")
    with open(itf, "w") as f:
        f.write("id\tsource_id\tquote\ni1\tS001\talpha beta gamma delta\n")
    with open("/etc/resolv.conf", "w") as f:
        f.write("nameserver 127.0.0.1\n")

    t0 = time.monotonic()
    p = subprocess.run([sys.executable, TOOL, "verify", "--items", itf, "--registry", reg],
                       capture_output=True, timeout=180)
    el = time.monotonic() - t0
    print("exit=%d elapsed=%.1fs (tool's own deadline is 30 s)" % (p.returncode, el))
    print("stdout:", p.stdout.decode("utf-8", "replace").strip().replace("\n", " | "))
    print("dns packets received: %d" % len(seen))
    print("WITHIN-DEADLINE" if el <= 35 else "OVERRUN")
    stop.set()


if __name__ == "__main__":
    main()
