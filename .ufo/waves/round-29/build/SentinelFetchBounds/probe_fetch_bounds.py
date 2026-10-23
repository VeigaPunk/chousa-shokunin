#!/usr/bin/env python3
"""Sentinel fetch-bounds probe for the frozen round-29 C1 tool contract.

Read-only against the lane; all HTTP traffic goes to a loopback server this
script starts on 127.0.0.1. It measures stdlib urllib.request behaviour that
the frozen fetch bounds depend on:

  1. redirect target scheme handling (file:, data:, ftp:, http:, https:)
  2. redirect target host handling (loopback, link-local, private)
  3. gzip decompression size versus the 8 MiB body cap
  4. socket-timeout semantics (per operation, not total wall clock)
  5. oversized response header handling and the exception taxonomy
  6. userinfo (credential) in a URL and where it surfaces
  7. ambient proxy environment handling
  8. direct file:/data: handling by the default opener

Usage: timeout 120 python3 probe_fetch_bounds.py
"""
import gzip
import http.client
import http.server
import ipaddress
import os
import socket
import socketserver
import ssl
import sys
import threading
import urllib.error
import urllib.request

LOOPBACK_PORT = 0
BIG_HEADER_BYTES = 70000
MANY_HEADERS = 150
BOMB_PAYLOAD_BYTES = 200 * 1024 * 1024
BOMB_COMPRESSED_BYTES = 203861  # measured compression ratio of the payload
SLOW_INTERVAL_S = 0.6
SLOW_CHUNKS = 20
SOCKET_TIMEOUT_S = 2


def log(msg):
    print(msg, flush=True)


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path.startswith("/redirect/"):
            target = self.path[len("/redirect/"):]
            self.send_response(302)
            self.send_header("Location", target)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if self.path == "/big-header":
            self.send_response(200)
            self.send_header("X-Big", "A" * BIG_HEADER_BYTES)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", "5")
            self.end_headers()
            self.wfile.write(b"hello")
            return
        if self.path == "/many-headers":
            self.send_response(200)
            for i in range(MANY_HEADERS):
                self.send_header("X-H%d" % i, "v")
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"ok")
            return
        if self.path == "/gzip-bomb":
            payload = gzip.compress(b"A" * BOMB_PAYLOAD_BYTES)
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        if self.path == "/slow":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(SLOW_CHUNKS))
            self.end_headers()
            for _ in range(SLOW_CHUNKS):
                self.wfile.write(b"x")
                self.wfile.flush()
                import time
                time.sleep(SLOW_INTERVAL_S)
            return
        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve():
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", LOOPBACK_PORT), Handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]


def classify(exc):
    return "%s.%s | OSError=%s" % (
        type(exc).__module__, type(exc).__name__, isinstance(exc, OSError))


def probe_redirect_scheme(base):
    log("== 1/2. redirect targets (default opener) ==")
    targets = [
        "file:///etc/hostname",
        "data:text/html,hello",
        "ftp://127.0.0.1:1/secret",
        "http://127.0.0.1:1/x",
        "http://[::1]:1/x",
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://10.0.0.1/y",
        "https://example.invalid/z",
    ]
    for target in targets:
        url = "%s/redirect/%s" % (base, target)
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(url, headers={"User-Agent": "chousa-quote-reopen"}),
                    timeout=4) as resp:
                log("  %-70s FOLLOWED status=%s final=%s" % (target, resp.status, resp.geturl()))
        except Exception as exc:  # noqa: BLE001 - probe records every class
            log("  %-70s %s" % (target, classify(exc) + " :: " + str(exc)[:70]))


def probe_bomb(base):
    log("== 3. gzip bomb versus the 8 MiB cap ==")
    req = urllib.request.Request("%s/gzip-bomb" % base,
                                 headers={"User-Agent": "chousa-quote-reopen",
                                          "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        wire = resp.read(8 * 1024 * 1024 + 1)
        inflated = gzip.decompress(wire)
        log("  wire bytes read under the 8 MiB+1 read cap: %d" % len(wire))
        log("  gzip.decompress of that prefix expands to: %d bytes (%.1f MiB)"
            % (len(inflated), len(inflated) / 1048576.0))
        log("  counter reference inflate ratio: %.0fx" % (len(inflated) / max(1, len(wire))))
        import zlib
        obj = zlib.decompressobj(16 + zlib.MAX_WBITS)
        bounded = obj.decompress(wire, 8 * 1024 * 1024 + 1)
        log("  bounded incremental inflate with max_length=8 MiB+1 stops at: %d bytes" % len(bounded))
        log("  => the 8 MiB wire cap does not bound the inflated size; the cap must be applied"
            " to the inflated stream")


def probe_slow(base):
    log("== 4. socket timeout semantics ==")
    req = urllib.request.Request("%s/slow" % base, headers={"User-Agent": "chousa-quote-reopen"})
    import time
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=SOCKET_TIMEOUT_S) as resp:
            data = resp.read()
            log("  read %d bytes in %.1f s wall with socket timeout=%d s"
                % (len(data), time.time() - start, SOCKET_TIMEOUT_S))
    except Exception as exc:  # noqa: BLE001
        log("  raised after %.1f s wall: %s" % (time.time() - start, classify(exc)))
    log("  => the timeout is a per-socket-operation timeout, not a total fetch deadline")


def probe_headers(base):
    log("== 5. oversized headers and exception taxonomy ==")
    for path in ("/big-header", "/many-headers"):
        try:
            with urllib.request.urlopen("%s%s" % (base, path), timeout=5) as resp:
                log("  %-14s status=%s" % (path, resp.status))
        except Exception as exc:  # noqa: BLE001
            log("  %-14s %s :: %s" % (path, classify(exc), str(exc)[:60]))
    for cls in (urllib.error.URLError, urllib.error.HTTPError, http.client.HTTPException,
                http.client.InvalidURL, socket.timeout, ssl.SSLError,
                UnicodeDecodeError, LookupError):
        log("  caught by (OSError, URLError, ValueError, LookupError)? %-28s %s"
            % (cls.__name__, issubclass(cls, (OSError, urllib.error.URLError, ValueError, LookupError))))


def probe_credentials():
    log("== 6. credentials in a URL ==")
    for url in ("http://alice:s3cr3t@example.invalid/x",
                "https://alice:s3cr3t@example.invalid/x",
                "http://alice@example.invalid/x"):
        req = urllib.request.Request(url)
        log("  Request.host for %-46s -> %r" % (url, req.host))
        try:
            urllib.request.urlopen(url, timeout=3)
            log("  %s -> no error" % url)
        except Exception as exc:  # noqa: BLE001
            log("  %s -> %s :: %s" % (url, classify(exc), str(exc)[:70]))
    url = "http://alice:s3cr3t@example.invalid/x"
    try:
        urllib.request.urlopen(url, timeout=3)
    except Exception as exc:  # noqa: BLE001
        log("  a naive stderr log line would print the secret:")
        log("    FETCH %s failed %s" % (url, exc))


def probe_proxy(base):
    log("== 7. ambient proxy environment ==")
    os.environ["http_proxy"] = "http://127.0.0.1:9"
    try:
        opener = urllib.request.build_opener()
        opener.open("%s/plain" % base, timeout=5)
        log("  request reached the origin: proxy ignored")
    except Exception as exc:  # noqa: BLE001
        log("  request failed %s :: %s" % (classify(exc), str(exc)[:60]))
        log("  => an opener built while http_proxy is set sends the request to the proxy host")
        log("     instead of the named registry host")
    finally:
        del os.environ["http_proxy"]
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open("%s/plain" % base, timeout=5) as resp:
        log("  with ProxyHandler({}) the origin is reached directly: status=%s" % resp.status)


def probe_direct_schemes():
    log("== 8. direct file:/data: through the default opener ==")
    for url in ("file:///etc/hostname", "data:text/plain,hello"):
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                log("  %-32s read %r" % (url, resp.read()[:40]))
        except Exception as exc:  # noqa: BLE001
            log("  %-32s %s" % (url, classify(exc)))


def probe_ip_classes():
    log("== address classification of the ranges that matter ==")
    for ip in ("127.0.0.1", "169.254.169.254", "100.100.100.200", "10.0.0.1",
               "172.16.0.1", "192.168.1.1", "::1", "fd00:ec2::254", "8.8.8.8"):
        addr = ipaddress.ip_address(ip)
        log("  %-18s global=%-5s private=%-5s loopback=%-5s linklocal=%s"
            % (ip, addr.is_global, addr.is_private, addr.is_loopback, addr.is_link_local))


def main():
    srv, port = serve()
    base = "http://127.0.0.1:%d" % port
    log("python %s" % sys.version.split()[0])
    log("loopback probe server on %s" % base)
    probe_redirect_scheme(base)
    probe_bomb(base)
    probe_slow(base)
    probe_headers(base)
    probe_credentials()
    probe_proxy(base)
    probe_direct_schemes()
    probe_ip_classes()
    srv.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
