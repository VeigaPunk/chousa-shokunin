#!/usr/bin/env python3
"""Security probe for tools/quote-reopen.py (landed tool) against wave-1 findings T1-T7.

All servers run on this machine. Two listeners are used:
  * a GLOBAL-V6 listener bound to this host's own global IPv6 address
    (2804:14d:...:5dbe, route: "local ... dev lo table local") -- needed because the
    tool refuses any peer address whose is_global is False, so a 127.0.0.1 registry
    URL is rejected before any request is made.
  * a LOOPBACK listener on 127.0.0.1 that records every accepted connection; it is
    used as the redirect target so we can prove no request was followed.
No external host is contacted: the global IPv6 address is this host's own.
"""
import gzip
import os
import socket
import subprocess
import sys
import threading
import time

TOOL = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py"
GLOBAL_V6 = "2804:14d:5c56:36ef:fe9d:5ff:fe5e:5dbe"
HERE = os.path.dirname(os.path.abspath(__file__))


class Server(threading.Thread):
    def __init__(self, family, addr, name):
        super().__init__(daemon=True)
        self.name_ = name
        self.sock = socket.socket(family, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(addr)
        self.sock.listen(64)
        self.port = self.sock.getsockname()[1]
        self.routes = {}
        self.lock = threading.Lock()
        self.accepted = []          # every accepted connection (peer address)
        self.requests = []          # every request line seen
        self.stop_flag = False

    def route(self, path, fn):
        self.routes[path] = fn

    def run(self):
        while not self.stop_flag:
            try:
                conn, peer = self.sock.accept()
            except OSError:
                return
            with self.lock:
                self.accepted.append(peer)
            threading.Thread(target=self.handle, args=(conn,), daemon=True).start()

    def handle(self, conn):
        try:
            conn.settimeout(60)
            data = b""
            while b"\r\n\r\n" not in data:
                chunk = conn.recv(65536)
                if not chunk:
                    return
                data += chunk
            line = data.split(b"\r\n", 1)[0].decode("latin-1")
            with self.lock:
                self.requests.append(line)
            path = line.split(" ")[1] if " " in line else "/"
            fn = self.routes.get(path)
            if fn is None:
                fn = self.routes.get("*")
            if fn is not None:
                fn(conn, line)
        except Exception as exc:                                # noqa: BLE001
            sys.stderr.write("[%s] handler error: %r\n" % (self.name_, exc))
        finally:
            try:
                conn.close()
            except OSError:
                pass

    def close(self):
        self.stop_flag = True
        try:
            self.sock.close()
        except OSError:
            pass


def resp(status, headers, body=b"", reason="OK"):
    head = "HTTP/1.1 %d %s\r\n" % (status, reason)
    for k, v in headers:
        head += "%s: %s\r\n" % (k, v)
    head += "Content-Length: %d\r\n\r\n" % len(body)
    return head.encode("latin-1") + body


def simple(body=b"<html><body>alpha beta gamma delta</body></html>", ctype="text/html"):
    def fn(conn, _line):
        conn.sendall(resp(200, [("Content-Type", ctype)], body))
    return fn


def redirect(location, status=302):
    def fn(conn, _line):
        conn.sendall(resp(status, [("Location", location)], b"", "Found"))
    return fn


def gzip_bomb(conn, _line):
    payload = gzip.compress(b"A" * (64 * 1024 * 1024), 6)
    conn.sendall(resp(200, [("Content-Type", "text/html"),
                            ("Content-Encoding", "gzip")], payload))
    sys.stderr.write("[gzip] wire=%d inflated=%d\n" % (len(payload), 64 * 1024 * 1024))


def big_body(conn, _line):
    body = b"B" * (9 * 1024 * 1024)
    conn.sendall(resp(200, [("Content-Type", "text/html")], body))
    sys.stderr.write("[bigbody] wire=%d\n" % len(body))


def slow_body(conn, _line):
    """40 bytes, one per second -> ~40 s of transfer, 30 s deadline."""
    conn.sendall(resp(200, [("Content-Type", "text/html")], b"x" * 40))
    for i in range(40):
        time.sleep(1.0)
        try:
            conn.sendall(b"x")
        except OSError:
            return
    sys.stderr.write("[slow] body finished\n")


def big_header(conn, _line):
    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nX-Big: " + b"A" * 100000 +
                 b"\r\nContent-Length: 2\r\n\r\nhi")


def many_headers(conn, _line):
    head = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
    for i in range(150):
        head += b"X-H%d: v\r\n" % i
    head += b"Content-Length: 2\r\n\r\nhi"
    conn.sendall(head)


def build_servers():
    g = Server(socket.AF_INET6, (GLOBAL_V6, 0), "global")
    lp = Server(socket.AF_INET, ("127.0.0.1", 0), "loopback")
    g.start()
    lp.start()
    return g, lp


def write_registry(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
        for sid, cell in rows:
            f.write("| %s | %s | spec | A | scope | anchor | teaches | mined | 2026-10-22 | 365d | note |\n" % (sid, cell))


def write_items(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        f.write("id\tsource_id\tquote\n")
        for iid, sid, quote in rows:
            f.write("%s\t%s\t%s\n" % (iid, sid, quote))


def run_tool(registry, items, timeout=180, strace=False, cwd=HERE):
    cmd = [sys.executable, TOOL, "verify", "--items", items, "--registry", registry]
    if strace:
        cmd = ["strace", "-f", "-e", "trace=connect,socket,openat,write", "-o",
               os.path.join(HERE, "strace.out")] + cmd
    t0 = time.monotonic()
    p = subprocess.run(cmd, capture_output=True, timeout=timeout, cwd=cwd)
    return p, time.monotonic() - t0
