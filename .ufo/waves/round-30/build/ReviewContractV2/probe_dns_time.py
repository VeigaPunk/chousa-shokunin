#!/usr/bin/env python3
"""Inside a private net+mount namespace: is name resolution bounded by a socket timeout or by
the round-29 tool's DEADLINE? A silent DNS sink on 127.0.0.1:53; resolv.conf and nsswitch.conf
are bind-mounted by the caller (hosts: files dns; nameserver 127.0.0.1; timeout:2 attempts:1).
"""
import importlib.util
import os
import socket
import sys
import threading
import time

TOOL = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py"


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 53))
    seen = []
    stop = threading.Event()

    def sink():
        s.settimeout(0.2)
        while not stop.is_set():
            try:
                seen.append(s.recvfrom(4096)[1])
            except OSError:
                pass

    threading.Thread(target=sink, daemon=True).start()

    socket.setdefaulttimeout(0.5)
    t0 = time.monotonic()
    try:
        socket.getaddrinfo("slowdns.test", 80, type=socket.SOCK_STREAM)
        r = "resolved"
    except socket.gaierror as e:
        r = "gaierror %s" % e.errno
    print("getaddrinfo with setdefaulttimeout(0.5): wall=%.2fs result=%s dns_packets=%d"
          % (time.monotonic() - t0, r, len(seen)))
    socket.setdefaulttimeout(None)

    spec = importlib.util.spec_from_file_location("qrtool", TOOL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.DEADLINE = 1.0
    n0 = len(seen)
    t0 = time.monotonic()
    out = m.fetch_page("http://slowdns.test/x")
    print("round-29 fetch_page with DEADLINE=1.0: wall=%.2fs detail=%r dns_packets=%d"
          % (time.monotonic() - t0, out[3], len(seen) - n0))
    stop.set()
    return 0


if __name__ == "__main__":
    sys.exit(main())
