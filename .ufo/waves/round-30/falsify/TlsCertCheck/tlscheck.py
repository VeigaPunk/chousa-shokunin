#!/usr/bin/env python3
"""TLS verification probe for the landed quote-reopen fetch path.

mode local: self-signed loopback TLS server; _check_address monkeypatched to ['127.0.0.1'].
mode real:  one GET of the registered S052 URL through fetch_page, no patching.
"""
import hashlib
import http.server
import importlib.util
import json
import os
import ssl
import sys
import threading
import time

TOOL = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py"
HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = b"<html><head><title>t</title></head><body><p>tls probe body sentinel words</p></body></html>"


def load_tool():
    spec = importlib.util.spec_from_file_location("quote_reopen", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class H(http.server.BaseHTTPRequestHandler):
    hits = 0

    def do_GET(self):
        H.hits += 1
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(PAGE)))
        self.end_headers()
        self.wfile.write(PAGE)

    def log_message(self, *a):
        pass


def serve(certfile, keyfile):
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile, keyfile)
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    srv.handle_error = lambda *a: None
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv


def main():
    mode, cert, key, host = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None, \
        sys.argv[3] if len(sys.argv) > 3 else None, sys.argv[4] if len(sys.argv) > 4 else "localhost"
    tool = load_tool()
    tool_sha = hashlib.sha256(open(TOOL, "rb").read()).hexdigest()
    rec = {"mode": mode, "tool_sha256": tool_sha, "python": sys.version.split()[0],
           "openssl": ssl.OPENSSL_VERSION, "SSL_CERT_FILE": os.environ.get("SSL_CERT_FILE")}
    if mode == "local":
        calls = []

        def fake_check(h, p):
            calls.append([h, p])
            return ["127.0.0.1"]
        tool._check_address = fake_check
        tool.DEADLINE = 10.0
        srv = serve(cert, key)
        port = srv.server_address[1]
        url = "https://%s:%d/" % (host, port)
        t0 = time.monotonic()
        status, ctype, text, detail = tool.fetch_page(url)
        rec.update(url=url, check_address_calls=calls, server_get_count=H.hits,
                   wall_s=round(time.monotonic() - t0, 3))
        srv.shutdown()
        srv.server_close()
    else:
        url = sys.argv[2]
        t0 = time.monotonic()
        status, ctype, text, detail = tool.fetch_page(url)
        rec.update(url=url, wall_s=round(time.monotonic() - t0, 3))
        if text:
            rec["contains_notes_on_socket_timeouts"] = "Notes on socket timeouts" in text
            rec["text_sha256"] = hashlib.sha256(text.encode()).hexdigest()
    rec.update(status=status, ctype=ctype, detail=detail,
               text_len=None if text is None else len(text),
               text_head=None if text is None else text[:160])
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
