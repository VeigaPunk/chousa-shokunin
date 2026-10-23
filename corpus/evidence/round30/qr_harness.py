#!/usr/bin/env python3
"""Round-30 loopback harness for tools/quote-reopen.py (shared by c1-count.py and c2-count.py).

Nothing here reaches the network. The harness runs a candidate tool in a child process
whose socket layer is replaced:

- `socket.getaddrinfo` answers only from the run's name map. Each host has a sequence of
  address lists; call k returns entry min(k, last). An IP literal resolves to itself.
  Any other name raises `socket.gaierror`.
- `socket.socket.connect` / `connect_ex` log every destination address to a JSONL file.
  A destination that is one of the run's routed global addresses, or a loopback address,
  is connected to the harness server on 127.0.0.1. Every other destination is refused.
  So a candidate can never open a connection to a real host.

The child imports the candidate as a module, sets its module constant `DEADLINE` when the
run map gives one, and calls `main(argv)`. The tool contract (round-29 claims.md) already
names `main(argv)` and the round-30 claims file names `DEADLINE`.

Usage as a child bootstrap (internal):
    python3 qr_harness.py boot MAP.json TOOL.py verify --items X --registry Y
"""
import importlib.util
import ipaddress
import json
import os
import random
import socket
import socketserver
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- child bootstrap

def _boot(map_path, tool_path, argv):
    with open(map_path, encoding="utf-8") as f:
        m = json.load(f)
    # The candidate never sees the run map: the file is removed and argv shows only the tool call.
    os.unlink(map_path)
    sys.argv = [tool_path] + list(argv)
    resolve = m["resolve"]                 # host -> [[addr, ...], ...]
    routed = set(m["routed"])              # global addresses routed to the server
    server_port = int(m["server_port"])
    log_path = m["log"]
    calls = {}
    real_gai = socket.getaddrinfo
    real_connect = socket.socket.connect
    real_connect_ex = socket.socket.connect_ex
    lock = threading.Lock()

    def log(rec):
        with lock:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")

    def fake_gai(host, port, family=0, type=0, proto=0, flags=0):
        if isinstance(host, bytes):
            host = host.decode("ascii", "replace")
        try:
            port_n = int(port) if port is not None else 0
        except (TypeError, ValueError):
            port_n = 0
        try:
            ipaddress.ip_address(str(host).split("%", 1)[0])
            addrs = [str(host)]
        except ValueError:
            key = str(host).lower().rstrip(".")
            if key not in resolve:
                log({"ev": "resolve", "host": key, "result": "nxdomain"})
                raise socket.gaierror(socket.EAI_NONAME, "Name or service not known")
            k = calls.get(key, 0)
            calls[key] = k + 1
            seq = resolve[key]
            addrs = seq[min(k, len(seq) - 1)]
            log({"ev": "resolve", "host": key, "call": k, "result": addrs})
        out = []
        for a in addrs:
            ip = ipaddress.ip_address(a)
            if ip.version == 4:
                out.append((socket.AF_INET, socket.SOCK_STREAM, 6, "", (a, port_n)))
            else:
                out.append((socket.AF_INET6, socket.SOCK_STREAM, 6, "", (a, port_n, 0, 0)))
        return out

    def target(address):
        host = str(address[0]).split("%", 1)[0]
        log({"ev": "connect", "dest": host, "port": address[1]})
        try:
            ip = ipaddress.ip_address(host)
        except ValueError:
            raise ConnectionRefusedError(111, "harness: not an address")
        if host in routed or ip.is_loopback:
            return ("127.0.0.1", server_port)
        raise ConnectionRefusedError(111, "harness: unrouted destination")

    def fake_connect(self, address):
        if self.family not in (socket.AF_INET, socket.AF_INET6):
            return real_connect(self, address)
        dest = target(address)
        if self.family == socket.AF_INET6:
            raise ConnectionRefusedError(111, "harness: ipv6 not served")
        return real_connect(self, dest)

    def fake_connect_ex(self, address):
        try:
            fake_connect(self, address)
            return 0
        except OSError as e:
            return e.errno or 111

    socket.getaddrinfo = fake_gai
    socket.socket.connect = fake_connect
    socket.socket.connect_ex = fake_connect_ex

    spec = importlib.util.spec_from_file_location("candidate_tool", tool_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["candidate_tool"] = mod
    spec.loader.exec_module(mod)
    if m.get("deadline") is not None:
        mod.DEADLINE = float(m["deadline"])
    m = None
    rc = mod.main(argv)
    sys.stdout.flush()
    os._exit(rc if isinstance(rc, int) else 2)


# ---------------------------------------------------------------- server

class Server:
    """Threaded raw HTTP/1.1 server on 127.0.0.1. Paths are opaque; behavior is looked up by path."""

    def __init__(self):
        self.docs = {}            # path -> (status, headers list, body bytes)
        self.kinds = {}           # path -> misbehavior name (never visible in the URL)
        self.hits = []
        self.stop = threading.Event()
        outer = self

        class H(socketserver.BaseRequestHandler):
            def handle(self):
                outer._handle(self.request)

        class S(socketserver.ThreadingTCPServer):
            daemon_threads = True
            allow_reuse_address = True

        self.srv = S(("127.0.0.1", 0), H)
        self.port = self.srv.server_address[1]
        self.t = threading.Thread(target=self.srv.serve_forever, daemon=True)
        self.t.start()

    def close(self):
        self.stop.set()
        self.srv.shutdown()
        self.srv.server_close()

    def add(self, path, body, status=200, ctype="text/html; charset=utf-8", extra=(), behavior=None,
            framing="cl", param=None):
        """Serve `body` at `path`. framing: "cl" (Content-Length) or "chunked". behavior: None,
        slow-ok (body in 6 pieces spread over `param` seconds), drip-head (the whole response
        head one byte per 0.2 s), drip-body (head and 200 body bytes at once, then one byte per
        0.2 s), drip-steady (4096 bytes per 0.25 s), stall (head and 200 body bytes, then
        silence). Every behavior uses the same head shape as an ordinary page."""
        self.docs[path] = (status, [("Content-Type", ctype)] + list(extra), body, framing, param)
        if behavior:
            self.kinds[path] = behavior

    def _handle(self, s):
        s.settimeout(10)
        buf = b""
        try:
            while b"\r\n\r\n" not in buf and len(buf) < 65536:
                chunk = s.recv(4096)
                if not chunk:
                    return
                buf += chunk
        except OSError:
            return
        line = buf.split(b"\r\n", 1)[0].decode("latin-1")
        parts = line.split(" ")
        path = parts[1] if len(parts) > 1 else "/"
        self.hits.append((time.time(), path))
        try:
            self._serve(s, path)
        except OSError:
            pass
        finally:
            try:
                s.close()
            except OSError:
                pass

    def _drip(self, s, data, every, limit=40.0):
        end = time.monotonic() + limit
        for b in data:
            if self.stop.is_set() or time.monotonic() > end:
                return
            s.sendall(bytes([b]))
            time.sleep(every)

    @staticmethod
    def _frame(body, framing, pieces):
        """Split the body into wire pieces (chunked framing adds chunk headers)."""
        if framing != "chunked":
            return pieces(body)
        out = [b"%x\r\n%s\r\n" % (len(p), p) for p in pieces(body) if p]
        out.append(b"0\r\n\r\n")
        return out

    def _serve(self, s, path):
        key = path.split("?", 1)[0]
        kind = self.kinds.get(key, "")
        doc = self.docs.get(key)
        if doc is None:
            s.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 9\r\n"
                      b"Connection: close\r\n\r\nnot found")
            return
        status, headers, body, framing, param = doc
        head = "HTTP/1.1 %d %s\r\n" % (status, {200: "OK", 302: "Found"}.get(status, "X"))
        for k, v in headers:
            head += "%s: %s\r\n" % (k, v)
        if framing == "chunked":
            head += "Transfer-Encoding: chunked\r\nConnection: close\r\n\r\n"
        else:
            head += "Content-Length: %d\r\nConnection: close\r\n\r\n" % len(body)
        head = head.encode("latin-1")
        if kind == "drip-head":
            self._drip(s, head + b"".join(self._frame(body, framing, lambda b: [b])), 0.2)
            return
        if kind in ("drip-body", "stall"):
            wire = b"".join(self._frame(body, framing, lambda b: [b[i:i + 1] for i in range(len(b))]))
            s.sendall(head + wire[:200])
            if kind == "stall":
                self.stop.wait(40)
            else:
                self._drip(s, wire[200:], 0.2)
            return
        if kind == "drip-steady":
            wire = b"".join(self._frame(body, framing, lambda b: [b[i:i + 4096] for i in range(0, len(b), 4096)]))
            s.sendall(head)
            end = time.monotonic() + 40
            for i in range(0, len(wire), 4096):
                if self.stop.is_set() or time.monotonic() > end:
                    return
                s.sendall(wire[i:i + 4096])
                time.sleep(0.25)
            return
        if kind == "slow-ok":
            # Six body pieces, each sent after one pacing gap; a chunked terminator follows the
            # sixth piece with no extra gap, so the body completes `param` seconds after the head.
            n = max(1, -(-len(body) // 6))
            pieces = [body[i:i + n] for i in range(0, len(body), n)]
            s.sendall(head)
            gap = float(param or 1.8) / len(pieces)
            for k, p in enumerate(pieces):
                time.sleep(gap)
                if framing == "chunked":
                    p = b"%x\r\n%s\r\n" % (len(p), p) + (b"0\r\n\r\n" if k == len(pieces) - 1 else b"")
                s.sendall(p)
            return
        s.sendall(head + b"".join(self._frame(body, framing, lambda b: [b])))


# ---------------------------------------------------------------- parent helpers

def global_addrs(rng, n):
    """n distinct random global IPv4 addresses (never contacted: the child routes them to loopback)."""
    out = []
    while len(out) < n:
        a = "%d.%d.%d.%d" % (rng.randint(1, 223), rng.randint(0, 255), rng.randint(0, 255), rng.randint(1, 254))
        if ipaddress.ip_address(a).is_global and a not in out:
            out.append(a)
    return out


def registry_text(rows):
    """rows: [(sid, url)] -> a registry file in the SOURCES.md table shape."""
    lines = ["| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sid, url in rows:
        src = ("harness page — %s" % url) if url else "harness own-work row without a URL"
        lines.append("| %s | %s | docs | A | harness | harness | harness | queued | 2026-10-23 | 365d | — |"
                     % (sid, src))
    return "\n".join(lines) + "\n"


def run_tool(tool, workdir, items, registry_rows_, resolve, routed, server_port,
             deadline=None, cap=120.0):
    """Run the candidate once. items: [(id, sid, quote)]. Returns dict with rc, verdicts, wall, connects."""
    os.makedirs(workdir, exist_ok=True)
    items_p = os.path.join(workdir, "items.tsv")
    reg_p = os.path.join(workdir, "registry.md")
    map_p = os.path.join(workdir, "map.json")
    log_p = os.path.join(workdir, "net.jsonl")
    with open(items_p, "w", encoding="utf-8") as f:
        f.write("id\tsource_id\tquote\n")
        for i, sid, q in items:
            f.write("%s\t%s\t%s\n" % (i, sid, q))
    with open(reg_p, "w", encoding="utf-8") as f:
        f.write(registry_text(registry_rows_))
    with open(map_p, "w", encoding="utf-8") as f:
        json.dump({"resolve": resolve, "routed": routed, "server_port": server_port,
                   "log": log_p, "deadline": deadline}, f)
    open(log_p, "w").close()
    cmd = [sys.executable, os.path.join(HERE, "qr_harness.py"), "boot", map_p, os.path.abspath(tool),
           "verify", "--items", items_p, "--registry", reg_p]
    t0 = time.monotonic()
    killed = False
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                         start_new_session=True)
    try:
        out, err = p.communicate(timeout=cap)
    except subprocess.TimeoutExpired:
        killed = True
        try:
            os.killpg(p.pid, 9)
        except OSError:
            pass
        out, err = p.communicate()
    wall = time.monotonic() - t0
    verdicts = {}
    for ln in out.splitlines():
        f = ln.split("\t")
        if len(f) >= 3 and f[0] == "QUOTE_REOPEN":
            verdicts.setdefault(f[1], f[2])
    connects = []
    with open(log_p, encoding="utf-8") as f:
        for ln in f:
            try:
                connects.append(json.loads(ln))
            except ValueError:
                pass
    return {"rc": p.returncode, "killed": killed, "wall": wall, "verdicts": verdicts,
            "net": connects, "stderr_tail": err[-400:]}


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "boot":
        _boot(sys.argv[2], sys.argv[3], sys.argv[4:])
    else:
        sys.stderr.write(__doc__)
        sys.exit(2)
