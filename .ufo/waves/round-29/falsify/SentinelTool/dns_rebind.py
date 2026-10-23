#!/usr/bin/env python3
"""DNS-rebinding TOCTOU probe for tools/quote-reopen.py.

Runs inside a private network namespace (unshare -m -n --map-root-user):
  * a DNS server on 127.0.0.1:53 answers the FIRST A/AAAA query for the test
    name with a global address (so the tool's _check_address policy check passes)
    and every later query with 127.0.0.1 (so http.client's own connect, which
    resolves the name a second time, lands on loopback);
  * an HTTP server on 127.0.0.1 serving a page;
  * the tool itself, with /etc/resolv.conf replaced inside the namespace.
No external host is contacted: the namespace has only the loopback interface.
"""
import os
import socket
import struct
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py"
GLOBAL_V6 = "2804:14d:5c56:36ef:fe9d:5ff:fe5e:5dbe"
LOOP = "127.0.0.1"
NAME = "rebind.test"
PORT = 45799

dns_log = []
http_log = []
stop = threading.Event()


def dns_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 53))
    s.settimeout(0.5)
    counts = {}
    while not stop.is_set():
        try:
            data, peer = s.recvfrom(4096)
        except socket.timeout:
            continue
        except OSError:
            break
        off = 12
        while off < len(data) and data[off] != 0:
            off += 1 + data[off]
        qname_end = off
        qend = qname_end + 5
        qtype = struct.unpack("!H", data[qname_end + 1:qname_end + 3])[0]
        counts[qtype] = counts.get(qtype, 0) + 1
        total = sum(counts.values())
        # The first resolution round (the tool's policy check) answers with global
        # addresses; every later round (http.client's own connect-time resolution)
        # answers with loopback.
        first = total <= 2
        q = data[12:qend]
        if qtype == 28:
            addr = GLOBAL_V6 if first else "::1"
            rdata = socket.inet_pton(socket.AF_INET6, addr)
            rtype = 28
        else:
            addr = "93.184.216.34" if first else LOOP
            rdata = socket.inet_pton(socket.AF_INET, addr)
            rtype = 1
        ans = b"\xc0\x0c" + struct.pack("!HHIH", rtype, 1, 60, len(rdata)) + rdata
        resp = data[:2] + b"\x81\x80" + struct.pack("!HHHH", 1, 1, 0, 0) + q + ans
        try:
            s.sendto(resp, peer)
        except OSError:
            pass
        dns_log.append((counts[qtype], qtype, addr))


def http_server():
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ls.bind(("127.0.0.1", PORT))
    ls.listen(16)
    ls.settimeout(0.5)
    body = b"<html><body>alpha beta gamma delta</body></html>"
    while not stop.is_set():
        try:
            conn, peer = ls.accept()
        except socket.timeout:
            continue
        except OSError:
            break
        http_log.append(peer)
        try:
            conn.settimeout(5)
            conn.recv(65536)
            conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: %d\r\n\r\n%s"
                         % (len(body), body))
        except OSError:
            pass
        finally:
            conn.close()
    ls.close()


def main():
    threading.Thread(target=dns_server, daemon=True).start()
    threading.Thread(target=http_server, daemon=True).start()
    time.sleep(0.6)

    reg = os.path.join(HERE, "reg_dns.tsv")
    itf = os.path.join(HERE, "items_dns.tsv")
    with open(reg, "w") as f:
        f.write("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n")
        f.write("| S001 | Doc http://%s:%d/ok | spec | A | s | a | t | mined | 2026-10-22 | 365d | n |\n"
                % (NAME, PORT))
    with open(itf, "w") as f:
        f.write("id\tsource_id\tquote\ni1\tS001\talpha beta gamma delta\n")
    with open("/etc/resolv.conf", "w") as f:
        f.write("nameserver 127.0.0.1\noptions timeout:1 attempts:1\n")

    t0 = time.monotonic()
    p = subprocess.run([sys.executable, TOOL, "verify", "--items", itf, "--registry", reg],
                       capture_output=True, timeout=90)
    el = time.monotonic() - t0
    print("exit=%d elapsed=%.1fs" % (p.returncode, el))
    print("stdout:", p.stdout.decode("utf-8", "replace").strip().replace("\n", " | "))
    err = p.stderr.decode("utf-8", "replace").strip()
    if err:
        print("stderr:", err.replace("\n", " | "))
    print("dns answers (nth-of-type, qtype, addr): %r" % (dns_log,))
    print("loopback http connections accepted: %d %r" % (len(http_log), http_log))
    print("REBIND-SUCCEEDED" if http_log else "REBIND-BLOCKED")
    stop.set()


if __name__ == "__main__":
    main()
